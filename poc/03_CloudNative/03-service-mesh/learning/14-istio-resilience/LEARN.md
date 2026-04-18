# Ch14. 네트워크 복원력

> 📌 **핵심 요약**: 복원력은 장애를 없애는 것이 아니라 장애가 전파되지 않도록 막는 것이다. Istio는 타임아웃, 재시도, 서킷 브레이킹을 코드 변경 없이 DestinationRule과 VirtualService만으로 제공한다. 각 메커니즘은 독립적으로 동작하지만 잘못 조합하면 서로 상쇄되거나 폭주를 일으킨다. 설계 원칙을 이해하고 적절히 조합하는 것이 핵심이다.

---

## 🎯 학습 목표

1. Envoy의 로드 밸런싱 알고리즘 차이를 설명하고 Fortio로 실제 성능을 비교할 수 있다
2. VirtualService로 타임아웃을 설정하고 서비스 체인에서 타임아웃 전파 원칙을 적용한다
3. 재시도 기본 동작과 `retryOn` 조건을 이해하고 EnvoyFilter로 고급 재시도를 구성한다
4. 서킷 브레이커의 connectionPool과 Outlier Detection 설정을 작성하고 차이를 구별한다
5. 타임아웃, 재시도, 서킷 브레이킹을 조합할 때 발생하는 상호작용을 설명할 수 있다
6. `x-envoy-overloaded` 헤더와 `503 UO` 응답 플래그로 서킷 브레이커 동작을 식별한다

---

## 1. 클라이언트 측 로드 밸런싱

### 1.1 Envoy EDS와 로드 밸런싱 알고리즘

서비스 메시에서 로드 밸런싱은 kube-proxy가 아닌 사이드카 Envoy가 담당한다. Envoy는 Pilot로부터 EDS(Endpoint Discovery Service)를 통해 각 서비스의 엔드포인트 목록을 실시간으로 수신하고, 그 목록을 대상으로 직접 연결을 선택한다. kube-proxy 방식이 iptables 규칙으로 목적지를 결정하는 것과 달리, Envoy는 로드 밸런싱 알고리즘을 선택할 수 있고 각 엔드포인트의 상태를 추적한다.

Istio에서 로드 밸런싱 알고리즘은 DestinationRule의 `trafficPolicy.loadBalancer` 필드로 설정한다:

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: my-service-dr
  namespace: default
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN   # 기본값
```

### 1.2 Round Robin vs Random vs Least Request

세 알고리즘의 차이는 각 엔드포인트로 요청을 배분하는 방식에 있다.

**ROUND_ROBIN**은 기본값이다. 엔드포인트를 순서대로 돌아가며 요청을 배분한다. 모든 엔드포인트의 처리 속도가 비슷하고 요청 처리 시간이 짧을 때 공정한 분산을 제공한다. 엔드포인트 중 하나가 느려지면 그 엔드포인트로 보내진 요청이 큐에 쌓이는 동안 다른 빠른 엔드포인트는 유휴 상태가 된다.

**RANDOM**은 각 요청마다 엔드포인트를 무작위로 선택한다. 장기적으로는 Round Robin과 비슷한 분산을 보이지만, 단기적으로는 특정 엔드포인트에 요청이 몰릴 수 있다. 알고리즘 오버헤드가 없어 Round Robin보다 약간 빠르다.

**LEAST_REQUEST**는 현재 활성 요청 수가 가장 적은 엔드포인트를 선택한다. 처리 시간이 균일하지 않은 요청(어떤 요청은 10ms, 어떤 요청은 500ms)이 섞여 있을 때 가장 효과적이다. 빠른 엔드포인트는 더 많은 요청을 받고, 느린 엔드포인트는 처리 중인 요청이 줄어들 때까지 새 요청을 적게 받는다.

```yaml
spec:
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
```

### 1.3 Fortio를 활용한 부하 테스트와 LB 전략 비교

Fortio는 Go로 작성된 HTTP 부하 테스트 도구다. Istio 공식 예제에서도 사용하며, 레이턴시 분포를 히스토그램으로 보여줘 로드 밸런싱 전략을 비교하기 좋다.

```bash
# Fortio 서버 배포 (테스트 대상)
kubectl apply -f samples/httpbin/httpbin.yaml

# Fortio 클라이언트 실행 (별도 Pod)
kubectl apply -f samples/httpbin/sample-client/fortio-deploy.yaml

FORTIO_POD=$(kubectl get pod -l app=fortio \
  -o jsonpath='{.items[0].metadata.name}')

# 기본 테스트: 50 concurrent, 200 QPS, 30초
kubectl exec $FORTIO_POD -- fortio load \
  -c 50 \
  -qps 200 \
  -t 30s \
  http://httpbin:8000/get
```

주요 Fortio 플래그:

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `-c` | 동시 연결 수 | `-c 50` |
| `-qps` | 초당 요청 수 (0=최대) | `-qps 200` |
| `-t` | 테스트 지속 시간 | `-t 30s` |
| `-n` | 총 요청 수 | `-n 1000` |
| `-H` | 헤더 추가 | `-H "x-test: true"` |

결과에서 중요한 수치는 레이턴시 퍼센타일이다. P50(중간값), P90, P99 값을 LB 알고리즘별로 비교하면 실제 트래픽 패턴에서 어떤 알고리즘이 우위인지 알 수 있다. 요청 처리 시간 분산이 클수록 LEAST_REQUEST가 Round Robin보다 P99 레이턴시를 낮춘다.

---

## 2. 지역 인식 로드 밸런싱

### 2.1 Locality-aware 라우팅 원리

지역 인식 로드 밸런싱(Locality-aware LB)은 같은 가용 영역(AZ)에 있는 엔드포인트를 우선 선택해 크로스 AZ 레이턴시와 데이터 전송 비용을 줄이는 기능이다. Envoy는 Pod가 실행 중인 노드의 토폴로지 레이블(`topology.kubernetes.io/region`, `topology.kubernetes.io/zone`)을 읽어 자신과 같은 AZ의 엔드포인트를 우선 순위에 둔다.

지역 인식이 동작하려면 두 가지 전제 조건이 충족되어야 한다. 먼저 Kubernetes 노드에 토폴로지 레이블이 있어야 한다. AWS EKS, GKE, AKS 같은 관리형 Kubernetes는 노드 생성 시 자동으로 이 레이블을 부여한다. 자체 구축 클러스터라면 수동으로 레이블을 추가해야 한다.

```bash
# 노드 토폴로지 레이블 확인
kubectl get nodes -L topology.kubernetes.io/region,topology.kubernetes.io/zone
```

두 번째 전제 조건은 DestinationRule에 `outlierDetection`이 설정되어야 한다는 점이다. Envoy가 특정 AZ의 엔드포인트가 모두 건강하지 않을 때 다른 AZ로 failover하는 메커니즘이 outlierDetection을 통해 동작하기 때문이다.

### 2.2 Outlier Detection과 지역 인식의 관계

Outlier Detection은 비정상 엔드포인트를 임시로 로드 밸런싱 대상에서 제외(eject)하는 기능이다. 지역 인식 라우팅과 결합하면, 같은 AZ의 엔드포인트가 모두 eject됐을 때 자동으로 다른 AZ로 failover된다.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: my-service-dr
spec:
  host: my-service
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5    # 5회 연속 5xx → eject
      interval: 10s              # 체크 주기
      baseEjectionTime: 30s      # 최소 eject 유지 시간
      maxEjectionPercent: 50     # 최대 50%까지 eject 가능
```

`maxEjectionPercent: 50`은 중요한 안전 장치다. 이 값이 100이면 모든 엔드포인트가 eject되어 서비스가 완전히 다운될 수 있다. 50으로 설정하면 절반은 항상 살아있어 일부 요청이 실패하더라도 서비스는 유지된다.

### 2.3 가중치 분포를 활용한 세밀 제어

기본 지역 인식 라우팅은 "같은 AZ 우선, 나머지는 다음 AZ"를 자동으로 결정한다. 더 세밀하게 제어하고 싶다면 `localityLbSetting.distribute`로 AZ 간 트래픽 분배 비율을 명시할 수 있다.

```yaml
spec:
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
        - from: "us-east-1/us-east-1a/*"
          to:
            "us-east-1/us-east-1a/*": 70    # 같은 AZ 70%
            "us-east-1/us-east-1b/*": 20    # 인접 AZ 20%
            "us-east-1/us-east-1c/*": 10    # 원격 AZ 10%
```

`from` 값은 `region/zone/subzone` 형식이다. 와일드카드 `*`로 해당 레벨 이하를 모두 포함한다. 이 설정은 AZ 간 엔드포인트 수가 불균형할 때 특정 AZ 과부하를 방지하는 데 유용하다.

---

## 3. 타임아웃

### 3.1 VirtualService 타임아웃 설정

타임아웃은 업스트림 서비스로부터 응답이 오지 않을 때 얼마나 기다릴지 정의한다. Istio는 기본적으로 타임아웃을 설정하지 않는다. 타임아웃이 없으면 느린 서비스가 Envoy의 요청 큐와 연결 풀을 가득 채워 연쇄 장애를 일으킬 수 있다.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-vs
spec:
  hosts:
  - ratings
  http:
  - route:
    - destination:
        host: ratings
        port:
          number: 9080
    timeout: 0.5s   # 0.5초 타임아웃
```

타임아웃을 설정하면, Envoy는 0.5초 안에 ratings 서비스로부터 응답을 받지 못하면 `504 Gateway Timeout`을 반환한다. 업스트림 서비스는 계속 처리 중이더라도 클라이언트는 즉시 응답을 받는다.

타임아웃 값 설정 기준은 실제 레이턴시 분포를 기반으로 한다. P99 레이턴시가 200ms라면 타임아웃을 300~400ms로 설정해 정상 요청의 1% 미만이 타임아웃되도록 한다. P99 레이턴시의 1.5~2배를 타임아웃으로 설정하는 것이 일반적인 시작점이다.

### 3.2 서비스 체인에서 타임아웃 전파 (외부→내부 짧게)

A → B → C 서비스 체인에서 타임아웃을 설정할 때는 바깥쪽에서 안쪽으로 갈수록 타임아웃이 짧아야 한다. A가 B를 호출할 때 1초 타임아웃을 가지고 있다면, B가 C를 호출하는 타임아웃은 700ms여야 한다. A의 타임아웃 내에서 B의 처리 시간(B 자체 로직 + C 호출 + 마진)이 충분히 완료되어야 하기 때문이다.

```
클라이언트
  │  2000ms 타임아웃
  ▼
서비스 A (자체 처리: 200ms)
  │  1500ms 타임아웃
  ▼
서비스 B (자체 처리: 300ms)
  │  1000ms 타임아웃
  ▼
서비스 C
```

안쪽 서비스의 타임아웃이 바깥쪽보다 길면 연쇄 장애가 발생한다. 예를 들어 A의 타임아웃이 1초인데 B → C 타임아웃이 2초라면, A는 1초 후 504를 반환하지만 B는 여전히 C를 기다리고 있다. A가 이미 클라이언트에게 에러를 반환했음에도 B와 C는 불필요한 작업을 계속하며 리소스를 소비한다.

---

## 4. 재시도

### 4.1 Istio 기본 재시도 동작 (attempts: 2, retryOn: 5xx)

Istio는 기본적으로 모든 HTTP 요청에 재시도를 적용한다. 기본값은 시도 횟수 2회, 재시도 조건 `5xx,retriable-4xx,connect-failure,reset`이다. 즉, 서버가 5xx를 반환하거나 연결 자체가 실패하면 Envoy가 자동으로 재시도한다. 이 기본 동작은 코드 변경 없이 일시적인 장애를 흡수한다.

```bash
# 기본 재시도 동작 확인
istioctl proxy-config cluster ratings-v1-xxx.default \
  --fqdn ratings.default.svc.cluster.local -o json | \
  grep -A 5 retryPolicy
```

기본 재시도가 항상 좋은 것은 아니다. 멱등성이 없는 POST 요청에 자동 재시도가 적용되면 동일 요청이 두 번 처리될 수 있다. 이 경우 해당 경로만 재시도를 비활성화해야 한다.

### 4.2 VirtualService 재시도 커스터마이징

VirtualService의 `retries` 블록으로 재시도 동작을 세밀하게 제어한다.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-retry-vs
spec:
  hosts:
  - ratings
  http:
  - route:
    - destination:
        host: ratings
        port:
          number: 9080
    retries:
      attempts: 3             # 최대 3회 시도 (초기 1회 + 재시도 2회)
      perTryTimeout: 2s       # 시도당 타임아웃
      retryOn: 5xx,reset,connect-failure,retriable-4xx
```

`perTryTimeout`은 전체 타임아웃 안에서 각 시도에 허용하는 최대 시간이다. `attempts: 3`에 `perTryTimeout: 2s`라면 전체 최대 응답 시간은 6초가 될 수 있다. 이를 고려해 바깥쪽 서비스의 타임아웃이 충분히 커야 한다.

재시도를 비활성화하려면 `attempts: 0`을 설정한다. POST나 결제 API처럼 멱등성이 없는 엔드포인트에는 재시도를 끄는 것이 안전하다.

### 4.3 EnvoyFilter를 통한 고급 재시도 (retriable_status_codes)

VirtualService의 `retryOn` 필드는 특정 HTTP 상태 코드를 직접 지정하는 기능을 제공하지 않는다. 예를 들어 서비스가 과부하 상태일 때 408(Request Timeout)을 반환하는데, 이 경우에만 재시도하고 싶다면 EnvoyFilter로 `retriable_status_codes`를 설정해야 한다.

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: ratings-retry-filter
  namespace: default
spec:
  workloadSelector:
    labels:
      app: productpage   # productpage에서 ratings 호출 시 적용
  configPatches:
  - applyTo: HTTP_ROUTE
    match:
      context: SIDECAR_OUTBOUND
      routeConfiguration:
        vhost:
          name: "ratings.default.svc.cluster.local:9080"
    patch:
      operation: MERGE
      value:
        route:
          retry_policy:
            retry_on: "retriable-status-codes"
            num_retries: 3
            retriable_status_codes:
            - 408
            - 429    # Too Many Requests도 재시도
            per_try_timeout: 2s
```

EnvoyFilter는 Istio의 고급 기능으로, xDS API 레벨에서 직접 Envoy 설정을 조작한다. VirtualService나 DestinationRule로 표현할 수 없는 설정을 적용할 때 사용한다. 단, Istio 버전 업그레이드 시 xDS 구조 변경으로 EnvoyFilter가 동작하지 않을 수 있으므로 업그레이드 시 반드시 검증해야 한다.

### 4.4 재시도 폭주 방지 (retry budget)

재시도가 연쇄 장애를 악화시킬 수 있다. 서비스 B가 느려서 A가 재시도를 반복하면, B는 정상 요청 + 재시도 요청을 모두 처리해야 해서 더욱 느려지고, A는 더 많이 재시도한다. 이 양성 피드백 루프를 "재시도 폭주(retry storm)"라고 한다.

재시도 폭주를 방지하는 기본 전략은 두 가지다. 첫째, `attempts` 값을 낮게 유지한다. 3회를 초과하는 재시도는 폭주 위험이 높아진다. 둘째, 서킷 브레이커와 함께 사용한다. 업스트림 서비스의 에러율이 높아지면 서킷 브레이커가 요청 자체를 차단해 재시도가 발생하지 않게 한다.

Envoy에는 retry budget이라는 개념이 있다. 전체 활성 요청 대비 재시도 요청 비율에 상한을 두는 기능이다. 예를 들어 동시 요청 100개 중 재시도가 20개를 넘으면 추가 재시도를 거부한다. 이 기능은 현재 Istio의 VirtualService 수준에서는 직접 설정이 불가능하고, EnvoyFilter로 `retry_budget` 설정을 적용해야 한다.

---

## 5. 서킷 브레이킹

### 5.1 커넥션 풀 제어 (maxConnections, http1MaxPendingRequests, http2MaxRequests)

서킷 브레이킹의 첫 번째 방어선은 커넥션 풀 제한이다. 업스트림 서비스로 보낼 수 있는 연결 수, 대기 중인 요청 수, 동시 요청 수에 상한을 두면, 느린 서비스가 무한정 연결을 가져가는 것을 막는다. 이 설정은 DestinationRule의 `trafficPolicy.connectionPool`에 정의한다.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: httpbin-circuit-breaker
spec:
  host: httpbin
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100        # TCP 최대 연결 수
        connectTimeout: 30ms       # 연결 타임아웃
      http:
        http1MaxPendingRequests: 10   # HTTP/1.1 대기 요청 최대 수
        http2MaxRequests: 100         # HTTP/2 동시 요청 최대 수
        maxRetries: 3               # 재시도 최대 수
```

`http1MaxPendingRequests`는 연결이 모두 사용 중일 때 큐에 대기할 수 있는 요청 수다. 이 한계를 초과하면 새 요청은 즉시 `503 Upstream Overflow`로 반환된다. 대기 큐를 너무 크게 잡으면 장애가 전파되는 시간만 늘어난다. 적절한 값은 서비스가 정상 처리 가능한 요청 수를 기준으로 정한다.

`maxConnections`는 TCP 레벨 연결 수 상한이다. HTTP/1.1은 연결당 하나의 요청만 처리하므로, 동시 요청 수를 제어하는 것은 `http1MaxPendingRequests`다. HTTP/2는 하나의 연결에서 여러 스트림을 처리하므로 `http2MaxRequests`로 동시 스트림 수를 제어한다.

### 5.2 Outlier Detection (consecutive5xxErrors, baseEjectionTime)

Outlier Detection은 실제로 에러를 반환하는 엔드포인트를 자동으로 로드 밸런싱 대상에서 제외하는 서킷 브레이커다. connectionPool이 "요청 수 제한"이라면, Outlier Detection은 "건강하지 않은 Pod 격리"다.

```yaml
spec:
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5     # 5회 연속 5xx → eject
      interval: 10s               # 감지 주기 (슬라이딩 윈도우)
      baseEjectionTime: 30s       # 첫 eject 유지 시간
      maxEjectionPercent: 50      # 최대 50% Pod까지 eject 가능
      minHealthPercent: 30        # 최소 30%는 항상 건강 상태 유지
```

eject된 엔드포인트는 `baseEjectionTime * eject_횟수` 시간이 지나면 다시 풀에 추가된다. 처음 eject는 30초, 두 번째는 60초, 세 번째는 90초처럼 점점 길어진다. 이 백오프 방식은 간헐적으로 회복하는 엔드포인트가 너무 빨리 복귀해 또 에러를 일으키는 상황을 방지한다.

`consecutive5xxErrors`는 연속 에러 횟수를 기준으로 한다. 5회 중 1회 에러면 eject하지 않고, 5회 연속으로 에러가 나야 eject한다. 간헐적 에러에는 반응하지 않는 보수적 설정이다. 더 빠르게 반응하고 싶다면 `consecutiveGatewayErrors`를 함께 설정하거나 `consecutive5xxErrors` 값을 낮춘다.

### 5.3 서킷 브레이커 + 재시도 조합

connectionPool 한계를 초과한 요청은 `503`으로 즉시 반환된다. 클라이언트 사이드에 재시도가 설정되어 있으면 이 `503`에 대해 재시도를 시도한다. 그런데 서킷 브레이커가 차단한 `503`은 업스트림 서비스가 이미 과부하 상태라는 신호이므로, 재시도해도 또 `503`이 반환될 가능성이 높다. 이런 재시도는 오히려 과부하를 가중시킨다.

이 문제를 해결하려면 `retryOn`에서 `5xx`를 사용하는 대신 더 세밀한 조건을 지정한다. `retriable-4xx`나 `connect-failure`는 재시도하되, `503`은 재시도에서 제외하는 것이다.

```yaml
retries:
  attempts: 2
  retryOn: connect-failure,reset,retriable-4xx  # 503은 미포함
  perTryTimeout: 2s
```

아니면 `503`에서도 재시도를 허용하되, retry budget으로 전체 재시도 횟수에 상한을 두는 방법도 있다.

### 5.4 x-envoy-overloaded 헤더로 서킷 브레이커 식별

Envoy가 서킷 브레이커 때문에 요청을 차단하면 응답에 `x-envoy-overloaded: true` 헤더를 포함한다. 이 헤더가 있는 `503`은 업스트림 서비스의 실제 에러가 아니라 Envoy의 커넥션 풀 초과 또는 Outlier Detection eject에 의한 차단이다.

```bash
# 서킷 브레이커 테스트: 과부하 요청
kubectl exec $FORTIO_POD -- fortio load \
  -c 20 \
  -qps 0 \
  -n 50 \
  http://httpbin:8000/get

# 응답 헤더 확인
curl -v http://httpbin:8000/get 2>&1 | grep -i "x-envoy\|503"
# x-envoy-overloaded: true 가 보이면 서킷 브레이커 동작 중
```

Envoy 응답 플래그에서 `UO`(Upstream Overflow)는 connectionPool 초과를 의미한다. Prometheus 메트릭에서도 확인할 수 있다:

```bash
# 서킷 브레이커 통계
kubectl exec istio-ingressgateway-xxx -n istio-system -- \
  curl -s localhost:15000/stats | \
  grep "overflow\|pending_overflow"
# cluster.outbound|8000||httpbin.default.svc.cluster.local.upstream_rq_pending_overflow: 15
```

이 숫자가 올라가면 서킷 브레이커가 실제로 동작 중이라는 증거다.

---

## 6. 복원력 전략 조합

### 6.1 타임아웃 + 재시도 + 서킷 브레이킹 설계 원칙

세 가지 메커니즘을 함께 설계할 때 따라야 할 원칙이다.

**타임아웃은 재시도 총 시간보다 커야 한다.** `attempts: 3`에 `perTryTimeout: 2s`면 최대 6초가 필요하다. VirtualService의 `timeout`이 4초라면 세 번 시도하기 전에 타임아웃이 발생한다. 이 경우 재시도가 의미가 없어진다. `timeout >= perTryTimeout * attempts`를 만족하도록 설계한다.

**서킷 브레이커는 재시도보다 빨리 반응해야 한다.** Outlier Detection의 `consecutive5xxErrors`가 5이고 재시도가 3회라면, 한 클라이언트의 재시도만으로는 eject를 트리거할 수 없다. 여러 클라이언트의 실패가 합산되어야 eject가 발생한다. 이는 의도된 설계다. 일시적 에러에 너무 민감하게 반응하면 정상 Pod가 불필요하게 eject된다.

**connectionPool과 재시도는 곱셈 관계다.** 동시 요청 100개에 재시도 3회가 설정되어 있다면, 모든 요청이 재시도하는 최악의 경우 업스트림은 300개의 요청을 처리해야 한다. connectionPool의 `maxConnections`와 `http1MaxPendingRequests`는 이 최악의 경우를 기준으로 설정하거나, 재시도 횟수를 낮춰 원래 요청 수를 넘지 않도록 유지한다.

완전한 설정 예시를 참고하면 이해가 빠르다:

```yaml
# VirtualService: 타임아웃 + 재시도
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-resilience
spec:
  hosts:
  - ratings
  http:
  - route:
    - destination:
        host: ratings
        port:
          number: 9080
    timeout: 6s               # 재시도 최대 시간 커버 (3 * 2s)
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: connect-failure,reset,retriable-4xx

---
# DestinationRule: 서킷 브레이커
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: ratings-circuit-breaker
spec:
  host: ratings
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### 6.2 연쇄 장애 방지 패턴

연쇄 장애(Cascade Failure)는 하나의 서비스 장애가 호출 체인을 따라 전파되어 전체 시스템이 다운되는 현상이다. Istio의 복원력 기능을 계층적으로 배치하면 이를 방지할 수 있다.

```
클라이언트
    │
    ▼ [타임아웃: 3s, 재시도: 2회]
서비스 A
    │
    ▼ [타임아웃: 1.5s, 재시도: 1회, connectionPool 제한]
서비스 B
    │
    ▼ [타임아웃: 0.8s, 재시도: 없음, Outlier Detection]
서비스 C (외부 의존)
```

체인의 끝으로 갈수록 타임아웃이 짧아지고 재시도 횟수가 줄어든다. 이렇게 하면 C에 장애가 발생해도 B의 타임아웃이 빠르게 반응하고, connectionPool이 B를 과부하로부터 보호한다. A는 B의 타임아웃 내에 응답을 받지 못하면 대안 처리(fallback, 캐시된 응답 등)를 할 수 있다.

Outlier Detection은 체인의 끝, 즉 가장 불안정한 외부 의존성 서비스에 배치하면 효과가 크다. 외부 API나 데이터베이스처럼 간헐적으로 느려지는 컴포넌트를 가장 빨리 격리할 수 있다.

---

## 📝 핵심 정리

**로드 밸런싱 알고리즘**은 기본 ROUND_ROBIN이 대부분의 경우 충분하다. 요청 처리 시간 분산이 크다면 LEAST_REQUEST가 P99 레이턴시를 개선한다. Fortio로 실제 트래픽 패턴에서 비교 측정한 뒤 결정하는 것이 가장 정확하다.

**타임아웃**은 모든 서비스에 설정해야 한다. 설정하지 않으면 단일 느린 서비스가 전체 연결 풀을 소모한다. 서비스 체인에서는 내부로 갈수록 짧게 설정하는 원칙을 지킨다.

**재시도**는 멱등성이 있는 GET 요청에는 유효하지만, POST/PUT/DELETE에는 신중해야 한다. `retryOn` 조건을 세밀하게 지정하고 `attempts`는 낮게 유지한다. 재시도는 서킷 브레이커와 반드시 함께 설계해야 재시도 폭주를 방지할 수 있다.

**서킷 브레이커**는 connectionPool(요청 수 제한)과 Outlier Detection(비정상 Pod 격리) 두 레이어로 구성된다. `x-envoy-overloaded` 헤더와 `503 UO` 응답 플래그로 서킷 브레이커 동작을 실시간으로 확인할 수 있다. `maxEjectionPercent`는 반드시 100% 미만으로 설정해 서비스가 완전히 다운되지 않도록 한다.
