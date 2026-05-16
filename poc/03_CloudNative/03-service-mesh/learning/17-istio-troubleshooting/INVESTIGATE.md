<!-- migrated: write/09_cloud/service-mesh/deepdive/17-01.Istio 트러블슈팅 실습.md (2026-04-19) -->

# Ch17. Istio 트러블슈팅 — Deep Dive Questions

---

## Q1. `istioctl proxy-config`의 Listener → Route → Cluster → Endpoint 추적 순서가 왜 중요한가?

### 왜 중요한가?

트러블슈팅에서 가장 흔한 실수는 "어디서 문제가 발생했는가"를 먼저 결정하지 않고 로그나 메트릭부터 뒤지는 것이다. Envoy는 요청을 처리할 때 Listener에서 받아, Route로 목적지를 결정하고, Cluster로 업스트림 그룹을 선택한 뒤, Endpoint로 실제 Pod IP를 찾아 연결한다. 이 네 단계는 요청이 프록시를 통과하는 물리적 순서와 정확히 일치한다.

이 순서를 무시하고 Cluster나 Endpoint부터 확인하면, 실제로는 Listener가 애초에 존재하지 않아서 요청이 거부되는 경우를 놓치게 된다. 반대로 Listener만 확인하고 멈추면 Route에서 잘못된 가중치 설정이 있어도 발견하지 못한다. 추적 순서가 디버깅의 효율을 결정한다.

### 분석

**Listener 레이어**는 특정 포트에서 요청을 수신하는 진입점이다. `istioctl proxy-config listener <pod>.<ns> --port 9080` 명령으로 해당 포트에 리스너가 존재하는지 먼저 확인한다. 리스너가 없다면 요청 자체가 Envoy에 도달하지 않는 것이므로 이 이상 추적할 필요가 없다. 리스너 부재의 원인은 주로 두 가지다. 서비스 포트 설정이 잘못됐거나(`port.name`이 프로토콜 접두사 없이 선언된 경우), 해당 namespace에 sidecar injection이 비활성화된 경우다.

**Route 레이어**는 리스너가 수신한 요청을 어느 Cluster로 보낼지 결정하는 규칙 집합이다. `istioctl proxy-config route <pod>.<ns> --name 9080`으로 VirtualService에서 정의한 라우팅 규칙이 실제로 반영됐는지 확인한다. 헤더 기반 라우팅이나 가중치 분배 규칙이 의도와 다르게 나타날 경우 VirtualService의 `match` 조건을 재점검해야 한다. Route는 컨트롤 플레인 설정이 데이터 플레인에 반영되는 핵심 지점이므로, `proxy-status`에서 RDS가 STALE이라면 Route 확인이 우선이다.

**Cluster 레이어**는 업스트림 서비스 그룹의 정의다. `istioctl proxy-config cluster <pod>.<ns> --fqdn reviews.default.svc.cluster.local`로 확인한다. 특히 subset이 포함된 Cluster 이름(`outbound|9080|v2|reviews.default.svc.cluster.local`)이 존재하는지 보는 것이 중요하다. VirtualService에서 `v2` subset을 참조했는데 DestinationRule에서 정의되지 않았다면 해당 Cluster 자체가 없고 Response Flag `NC`(No Cluster)가 발생한다.

**Endpoint 레이어**는 Cluster가 알고 있는 실제 Pod IP 목록이다. `istioctl proxy-config endpoint <pod>.<ns> --cluster "outbound|9080|v2|reviews.default.svc.cluster.local"`로 확인한다. Cluster는 존재하는데 Endpoint가 비어 있다면 해당 subset 레이블을 가진 Pod가 없거나, Pod는 있지만 Ready 상태가 아닌 것이다. Response Flag `UH`(No Healthy Upstream)가 이 상황에 대응한다.

한 단계에서 문제를 발견하면 그 레이어에 해당하는 Istio 리소스(VirtualService, DestinationRule, Service, Pod 레이블)를 타겟으로 수정하면 된다. 건너뛰면 오진이 발생한다.

### 실무 적용

트러블슈팅 세션을 시작할 때 다음 순서를 스크립트로 만들어 두면 반복 작업을 줄일 수 있다.

```bash
POD="productpage-v1-xxxx"
NS="default"
PORT=9080

echo "=== Listeners ==="
istioctl proxy-config listener ${POD}.${NS} --port ${PORT}

echo "=== Routes ==="
istioctl proxy-config route ${POD}.${NS} --name ${PORT}

echo "=== Clusters ==="
istioctl proxy-config cluster ${POD}.${NS} --fqdn reviews.default.svc.cluster.local

echo "=== Endpoints ==="
istioctl proxy-config endpoint ${POD}.${NS} --cluster "outbound|${PORT}||reviews.default.svc.cluster.local"
```

각 단계의 출력에서 비어 있는 레이어를 찾으면 그것이 문제의 위치다. CI/CD에서 배포 직후 이 스크립트를 smoke test로 실행해 엔드포인트가 올바르게 채워졌는지 검증하면 배포 문제를 조기에 탐지할 수 있다.

---

## Q2. Envoy Response Flag(UT, UO, UC, NR, DC)별 원인과 대응 전략의 차이는?

### 왜 중요한가?

503이나 504 에러가 발생했을 때 HTTP 상태 코드만으로는 "Istio가 타임아웃을 걸었는가, 서킷 브레이커가 열렸는가, 라우팅 규칙이 없는가"를 구분할 수 없다. Response Flag는 Envoy Access Log에 기록되는 짧은 코드이지만, 이 코드 하나가 수십 분의 디버깅 시간을 절약한다.

동일한 503이라도 `NR`이면 VirtualService 설정을 고쳐야 하고, `UO`이면 업스트림 서비스의 처리 용량을 늘려야 한다. 대응 방향이 완전히 다르기 때문에 Flag를 먼저 확인하지 않으면 엉뚱한 곳을 수정하게 된다.

### 분석

**UT (Upstream request Timeout)**는 VirtualService에 설정된 `timeout` 값을 업스트림이 초과했을 때 기록된다. HTTP 상태 코드는 504다. 대응은 두 방향이다. 하나는 업스트림 서비스의 처리 속도를 개선하는 것, 다른 하나는 타임아웃 값을 실제 p99 레이턴시에 맞게 조정하는 것이다. 타임아웃이 0.5s로 설정됐는데 DB 쿼리가 200ms 이상 걸리는 서비스라면 일시적인 DB 부하 시 UT가 빈번하게 발생한다. Grafana의 Request Duration 히스토그램으로 실제 p99를 측정한 뒤 타임아웃을 1.5배 정도의 여유를 두고 설정하는 것이 기준점이 된다.

**UO (Upstream Overflow)**는 DestinationRule의 `connectionPool` 설정에서 정의한 임계값을 초과했을 때 서킷 브레이커가 요청을 차단하며 기록된다. HTTP 상태 코드는 503이다. `http1MaxPendingRequests`, `http2MaxRequests`, `maxRequestsPerConnection` 중 어느 임계값이 초과됐는지 Envoy Admin의 `/stats` 엔드포인트에서 `upstream_rq_pending_overflow` 카운터로 확인할 수 있다. 대응은 `connectionPool` 값을 높이거나, 업스트림 서비스의 수평 확장이다. 서킷 브레이커를 무조건 열어놓는 것은 위험하므로 정상 부하의 1.5~2배 수준으로 임계값을 설정한다.

**UC (Upstream Connection termination)**는 업스트림이 연결을 먼저 끊었을 때 기록된다. 원인은 다양하다. 업스트림 Pod의 재시작, keepalive 설정 불일치, 업스트림의 graceful shutdown 중 진행 중인 요청이 종료된 경우 등이다. Rolling update 중 UC가 급증한다면 `preStop` 훅에 sleep을 추가하거나 `minReadySeconds`를 늘려 구 Pod가 처리 중인 요청을 완료할 시간을 확보해야 한다.

**NR (No Route found)**는 Envoy의 Route 테이블에 요청에 매칭되는 라우트가 없을 때 기록된다. VirtualService의 `match` 조건(URI prefix, 헤더, 메서드)이 실제 요청과 맞지 않거나, VirtualService 자체가 존재하지 않는 경우다. `istioctl proxy-config route`로 Route 테이블을 확인하고, `istioctl analyze`로 VirtualService 설정 오류를 먼저 점검한다.

**DC (Downstream Connection termination)**는 클라이언트가 응답을 기다리지 않고 연결을 먼저 닫았을 때 기록된다. 클라이언트 타임아웃이 서버 타임아웃보다 짧거나, 사용자가 요청을 취소한 경우다. DC 자체는 서버 측 문제가 아니므로 에러율 계산에서 제외하는 것이 일반적이다. Prometheus 쿼리에서 `response_flags!="DC"`로 필터링하면 실제 서버 측 에러율만 측정할 수 있다.

### 실무 적용

Access Log에서 Response Flag를 기반으로 에러를 분류하는 Prometheus 쿼리를 만들어 두면 대시보드 알림에 활용할 수 있다.

```promql
# UO (서킷 브레이커) 에러 비율
rate(istio_requests_total{response_flags="UO"}[5m])

# UT (타임아웃) 에러 비율
rate(istio_requests_total{response_flags="UT"}[5m])

# NR (라우팅 없음) 에러 - 설정 오류 신호
rate(istio_requests_total{response_flags="NR"}[5m])
```

NR이나 NC는 설정 오류를 의미하므로 발생 즉시 알림을 보내야 한다. UO와 UT는 임계값 기반 알림이 적합하다. DC는 정상 트래픽 패턴의 일부이므로 별도 알림 기준을 높게 잡는다.

---

## Q3. 클라이언트 관점 실패율과 서버 관점 실패율이 다를 때 어떤 방향으로 원인을 좁히는가?

### 왜 중요한가?

Istio는 모든 요청에 대해 발신자(클라이언트 사이드카)와 수신자(서버 사이드카) 양쪽에서 메트릭을 수집한다. 동일한 요청에 대해 두 관점이 일치하면 문제가 서버 애플리케이션에 있다는 것이고, 불일치하면 두 사이드카 사이 어딘가에 문제가 있다는 것이다. 이 관점 차이를 먼저 파악하지 않으면 서버 로그를 뒤지는 동안 문제는 네트워크 레이어에 있을 수 있다.

### 분석

**클라이언트 실패율 > 서버 실패율**이 나타날 때는 클라이언트 사이드카와 서버 사이드카 사이에 문제가 있다. 가장 흔한 원인은 Envoy가 자체적으로 요청을 거부한 것이다. 타임아웃(UT), 서킷 브레이커(UO), 라우팅 실패(NR, NC)가 모두 여기 해당한다. 클라이언트 사이드카가 요청을 서버까지 전달하지 않고 자체 거부했기 때문에 서버 사이드카에는 아무 기록이 없다.

이 경우 클라이언트 Pod의 Envoy Access Log를 먼저 확인한다. Response Flag가 무엇인지 파악하면 원인이 타임아웃인지 서킷 브레이커인지 라우팅 오류인지 바로 구분된다. `istioctl proxy-config` 체인으로 해당 Pod의 Route, Cluster, Endpoint를 순서대로 확인하면 어느 레이어에서 막혔는지 찾을 수 있다.

**클라이언트 실패율 = 서버 실패율**이 나타날 때는 서버 사이드카 또는 서버 애플리케이션이 문제다. 서버의 Envoy Access Log에 동일한 에러가 기록된다면 서버 사이드카의 정책(AuthorizationPolicy, PeerAuthentication)을 점검한다. 서버 Envoy는 정상인데 애플리케이션이 5xx를 반환한다면 애플리케이션 레이어 문제다.

**클라이언트는 성공이지만 서버에서 실패가 더 많은** 경우는 드물지만 발생한다. 클라이언트 사이드카가 재시도를 투명하게 처리해서 최종 응답은 200이지만 서버에는 초기 실패 요청이 기록된 것이다. VirtualService의 `retries` 설정이 활성화된 환경에서 자주 나타난다. 이 경우 서버에서 간헐적 에러가 발생하고 있다는 신호이므로, 재시도가 마스킹하고 있는 근본 원인을 찾아야 한다.

두 관점의 메트릭을 Grafana에서 한 화면에 표시하면 이 비교가 직관적이다. Istio Service Dashboard의 "Incoming Requests Success Rate"(서버 관점)와 출발 서비스 대시보드의 "Outgoing Requests Success Rate"(클라이언트 관점)를 나란히 놓고 시계열을 비교한다.

### 실무 적용

두 관점을 Prometheus에서 직접 비교하는 쿼리는 다음과 같다.

```promql
# 클라이언트 관점 에러율 (reviews 서비스 대상)
rate(istio_requests_total{
  source_app="productpage",
  destination_service_name="reviews",
  response_code=~"5.."
}[5m])
/
rate(istio_requests_total{
  source_app="productpage",
  destination_service_name="reviews"
}[5m])

# 서버 관점 에러율
rate(istio_requests_total{
  destination_app="reviews",
  reporter="destination",
  response_code=~"5.."
}[5m])
/
rate(istio_requests_total{
  destination_app="reviews",
  reporter="destination"
}[5m])
```

두 쿼리의 차이가 0이면 서버 문제, 양수이면 클라이언트 사이드카 문제다. 이 비율을 Grafana 알림으로 설정하면 장애 발생 시 빠른 방향 전환이 가능하다.

---

## Q4. `istioctl analyze`를 CI/CD 파이프라인에 통합하면 어떤 클래스의 오류를 사전에 잡을 수 있는가?

### 왜 중요한가?

Istio 설정 오류의 상당수는 런타임에서 503이나 흔한 HTTP 에러로 나타나기 전까지 발견되지 않는다. VirtualService가 참조하는 subset이 DestinationRule에 없는 경우가 대표적이다. 배포 후 트래픽이 흐르기 시작해야 에러가 드러나는데, 그때는 이미 일부 요청이 실패한 상태다. `istioctl analyze`를 파이프라인에 넣으면 이 클래스의 오류를 배포 전에 탐지할 수 있다.

### 분석

`istioctl analyze`가 탐지하는 오류는 크게 세 클래스다.

**참조 무결성 오류**가 가장 중요하다. `IST0101 (Referenced selector not found)`는 VirtualService나 DestinationRule이 존재하지 않는 subset, 서비스, 호스트를 참조할 때 발생한다. 이 오류가 배포되면 해당 라우트로 보내지는 모든 트래픽이 503 NC로 실패한다. `IST0104`는 DestinationRule의 host가 실제로 존재하지 않는 서비스를 가리킬 때 경고를 낸다.

**포트 프로토콜 오류**가 두 번째 클래스다. `IST0118`은 Service의 포트 이름이 `http-`, `grpc-`, `tcp-` 같은 프로토콜 접두사 없이 선언됐을 때 발생한다. 이 경우 Istio가 트래픽 프로토콜을 인식하지 못해 HTTP 헤더 기반 라우팅이 동작하지 않는다. 포트 이름을 `http-service-port`처럼 정확히 선언하면 해결된다.

**게이트웨이 오류**가 세 번째 클래스다. `IST0132`는 VirtualService가 참조하는 Gateway가 존재하지 않을 때 경고를 낸다. 외부 트래픽을 처리하는 Ingress Gateway와 VirtualService 간의 연결이 끊어지는 경우로, 배포 전에 잡지 못하면 외부 요청이 전혀 클러스터에 도달하지 않는 상황이 된다.

단, `istioctl analyze`가 탐지하지 못하는 오류 클래스도 있다. **런타임 엔드포인트 상태**는 파일 분석만으로는 알 수 없다. DestinationRule에 `v2` subset을 정의했고 VirtualService도 올바르게 참조하지만, 실제로 해당 레이블을 가진 Pod가 0개인 경우 `analyze`는 경고를 내지 않는다. 이 클래스의 오류는 `istioctl proxy-config endpoint`로 배포 직후 확인해야 한다.

로컬 파일을 대상으로 실행하면 실제 클러스터 없이도 작동한다는 것이 파이프라인 통합의 핵심이다.

```bash
# Pull Request 단계에서 변경된 Istio 설정 파일 검증
istioctl analyze ./k8s/istio/virtualservice.yaml ./k8s/istio/destinationrule.yaml

# 클러스터에 배포된 상태와 함께 검증 (staging 환경)
istioctl analyze -n staging
```

### 실무 적용

GitHub Actions 기준으로 PR 단계와 배포 후 단계를 나누어 통합하는 것이 효과적이다.

```yaml
# PR 단계 — 로컬 파일 분석
- name: Istio config analyze
  run: |
    istioctl analyze ./k8s/istio/ --use-kube=false
    if [ $? -ne 0 ]; then
      echo "Istio configuration errors found"
      exit 1
    fi

# 배포 후 단계 — 클러스터 상태 포함 분석
- name: Post-deploy Istio verify
  run: |
    istioctl analyze -n ${NAMESPACE}
    istioctl proxy-config endpoint ${POD_NAME}.${NAMESPACE} \
      --cluster "outbound|${PORT}||${SERVICE_FQDN}" | grep -v "No endpoints"
```

두 단계를 분리하는 이유는 PR 단계에서는 클러스터 접근이 불가능한 경우가 많기 때문이다. `--use-kube=false` 플래그로 로컬 파일만 분석하면 클러스터 없이도 참조 무결성을 검증할 수 있다.

---

## Q5. Envoy Admin Interface를 프로덕션에서 노출할 때의 보안 위험과 대안은?

### 왜 중요한가?

Envoy Admin Interface(포트 15000)는 프록시의 설정 변경, 로그 레벨 조정, 드레인 실행을 허용하는 매우 강력한 인터페이스다. 이것이 외부에서 접근 가능하다면 공격자가 로그 레벨을 변경해 디스크를 채우거나, 헬스체크 엔드포인트를 조작해 서비스를 다운시킬 수 있다. 트러블슈팅을 위해 잠깐 열어두었다가 닫는 것을 잊는 사고가 실제로 발생한다.

### 분석

Envoy Admin Interface의 위험은 세 가지 차원에서 분석된다.

**정보 노출** 위험이 첫 번째다. `/config_dump` 엔드포인트는 Envoy가 알고 있는 모든 서비스의 IP, 포트, 인증서 정보를 JSON으로 반환한다. 내부 서비스 아키텍처를 그대로 노출하는 셈이다. 공격자가 이 정보를 사용해 내부 서비스를 직접 타겟으로 삼을 수 있다.

**설정 변경** 위험이 두 번째다. `/logging` 엔드포인트는 POST 요청으로 로그 레벨을 변경한다. `curl -X POST localhost:15000/logging?level=debug`를 실행하면 모든 Envoy 로그가 debug 레벨로 출력되어 스토리지를 빠르게 소진한다. `/drain_listeners` 엔드포인트는 Envoy가 모든 리스너를 드레인하게 만들어 사실상 서비스를 중단시킨다.

**인증 부재** 위험이 세 번째다. Admin Interface는 인증 메커니즘이 없다. 포트에 접근할 수 있는 누구나 위의 모든 작업을 수행할 수 있다. Istio의 현재 설계상 Admin Interface에 mTLS를 적용하거나 인증을 추가하는 공식 방법이 없다.

**대안 접근 방법**은 두 가지다. 첫째는 `kubectl port-forward`를 통한 on-demand 접근이다. Admin Interface를 상시 노출하지 않고, 트러블슈팅이 필요한 순간에만 포트 포워딩으로 로컬 접근하는 것이다. 이 방법은 접근 이력이 kubectl audit log에 남는다는 부가 이점도 있다.

```bash
# 트러블슈팅 시에만 실행, 완료 후 Ctrl+C로 종료
kubectl port-forward pod/productpage-v1-xxxx 15000:15000 -n default
# 완료 후 포트 포워딩 종료
```

둘째는 `istioctl proxy-config`와 `istioctl proxy-status` 명령어를 우선 사용하는 것이다. 대부분의 진단은 Admin Interface 직접 접근 없이 이 CLI 래퍼로 해결된다. CLI 래퍼는 kubectl 인증을 거치므로 RBAC으로 접근을 제어할 수 있다.

### 실무 적용

NetworkPolicy로 Admin Interface 포트에 대한 외부 접근을 차단하는 것이 기본 조치다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-envoy-admin
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - ports:
    - port: 15090  # Prometheus 메트릭 (허용 대상에서는 열어둠)
    from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
  # 15000 포트는 명시적으로 허용하지 않아 기본 차단
```

15090 포트(Prometheus 메트릭)는 모니터링 namespace에서만 접근 가능하도록 열고, 15000 포트는 명시적 허용 없이 기본 차단 상태로 둔다. 트러블슈팅 담당자는 `kubectl port-forward`로만 접근하고, 접근 완료 후 반드시 포트 포워딩을 종료하는 절차를 팀 내 규칙으로 문서화한다.

---

## Q6. istiod의 `/debug` 엔드포인트가 대규모 클러스터에서 성능에 미치는 영향은?

### 왜 중요한가?

istiod는 컨트롤 플레인의 핵심이다. istiod가 느려지면 설정 배포 지연, 인증서 갱신 실패, xDS 스트림 중단으로 이어져 데이터 플레인 전체에 영향을 미친다. `/debug` 엔드포인트는 진단 목적으로 설계됐지만, 대규모 클러스터에서 이 엔드포인트를 호출하면 istiod 자체의 처리 자원을 소비한다. 트러블슈팅을 위해 실행한 명령이 장애를 악화시키는 상황이 발생할 수 있다.

### 분석

istiod의 `/debug` 엔드포인트 중 성능 영향이 큰 것은 `/debug/adsz`와 `/debug/configz`다.

**`/debug/adsz`**는 현재 xDS 세션에 연결된 모든 Envoy 프록시와 각 프록시에 배포된 설정의 요약을 반환한다. 클러스터에 Pod가 500개 있다면 500개의 xDS 세션 정보를 직렬화해서 반환한다. 이 과정에서 istiod가 보유한 메모리 내 상태를 전부 읽어야 하므로, 대규모 클러스터에서는 수 초 동안 istiod가 다른 요청을 처리하는 속도가 느려진다. 1000개 이상의 Pod가 있는 클러스터에서 `/debug/adsz`를 반복 호출하면 xDS 업데이트 레이턴시가 눈에 띄게 증가한다.

**`/debug/configz`**는 현재 istiod가 보유한 모든 Istio 설정 리소스(VirtualService, DestinationRule, Gateway 등)를 JSON으로 반환한다. 설정 리소스가 수백 개에 달하는 클러스터에서는 응답 크기가 수 MB에 달할 수 있으며, 직렬화 자체가 CPU를 소비한다.

**`/debug/syncz`**는 상대적으로 가볍다. 각 Envoy의 동기화 상태(SYNCED/STALE)만 반환하므로 데이터 크기가 작다. `istioctl proxy-status`가 내부적으로 이 엔드포인트를 사용한다.

성능 영향을 최소화하는 접근 방법은 두 가지다. 하나는 istiod 파드를 직접 포트 포워딩하지 않고, `istioctl` CLI를 통해 필요한 정보만 조회하는 것이다. CLI는 최소한의 API만 호출하도록 최적화되어 있다. 다른 하나는 대규모 클러스터에서 `/debug/adsz` 호출이 필요할 때 off-peak 시간에 실행하거나, Canary 배포 전후처럼 클러스터 활동이 낮은 시점을 택하는 것이다.

istiod 자체의 성능 상태는 다음 메트릭으로 모니터링한다.

```promql
# xDS 푸시 레이턴시 (ms 단위, p99)
histogram_quantile(0.99,
  rate(pilot_xds_push_time_bucket[5m])
)

# EDS 업데이트 속도
rate(pilot_eds_no_instances[5m])

# 연결된 Envoy 수
pilot_k8s_cfg_events
```

`pilot_xds_push_time`의 p99가 갑자기 상승하면 istiod에 부하가 걸리고 있다는 신호다. 이 시점에 `/debug/adsz`를 반복 호출하면 상황을 악화시킨다.

### 실무 적용

대규모 클러스터에서 컨트롤 플레인 디버깅 절차를 정립할 때 다음 우선순위를 따른다.

1. **`istioctl proxy-status`로 먼저 확인** — syncz 엔드포인트만 사용하므로 가볍다
2. **`istioctl proxy-config`로 특정 Pod만 조회** — 전체 클러스터 상태를 읽지 않는다
3. **`/debug/adsz`는 문제 Pod가 특정된 후 마지막 수단으로만** — 전체 상태 덤프는 최소화한다
4. **`kubectl top pod -n istio-system`으로 istiod 자원 상태를 먼저 확인** — istiod가 이미 CPU나 메모리 압박을 받고 있다면 `/debug` 호출을 피한다

istiod의 HPA(HorizontalPodAutoscaler)를 설정해 컨트롤 플레인 부하가 높아질 때 자동 스케일아웃이 되도록 구성하면 진단 작업으로 인한 성능 저하를 어느 정도 완충할 수 있다.
