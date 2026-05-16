<!-- migrated: write/09_cloud/service-mesh/deepdive/12-01.Istio Ingress Gateway 실습.md (2026-04-19) -->

# Ch12. Istio Ingress Gateway — Deep Dive Questions

## Q1. Istio Gateway API와 Kubernetes Gateway API 중 어느 것을 선택해야 하는가? 마이그레이션 경로는?

### 왜 중요한가?

Istio 사용자는 트래픽 진입 설정을 작성할 때 두 가지 API 중 하나를 선택해야 한다. Istio 고유의 `networking.istio.io/v1` Gateway와 VirtualService를 쓸 것인가, 아니면 Kubernetes 표준인 `gateway.networking.k8s.io` API를 쓸 것인가. 두 API가 표현 가능한 기능 범위가 다르고 마이그레이션 비용도 있으므로, 시작 전에 선택 기준을 명확히 이해하는 것이 중요하다.

### 분석

선택의 핵심 기준은 이식성과 기능 완전성의 트레이드오프다. Kubernetes Gateway API를 선택하면 Istio뿐만 아니라 Cilium, Envoy Gateway, NGINX Gateway Fabric 등 다른 Gateway API 구현체로 나중에 교체할 수 있다. 인프라 추상화 레이어를 표준화하려는 조직에게 유리하다. 그러나 Istio 특화 기능인 Fault Injection, Traffic Mirroring 비율 제어, 복잡한 `retryOn` 조건은 Kubernetes Gateway API 표준에 포함되지 않아 `ExtensionRef`나 Istio 전용 어노테이션으로만 표현해야 한다. 이 순간 이식성이 사라진다.

Istio Gateway API를 선택하면 Istio의 모든 기능을 표준 방식으로 사용할 수 있다. 기존 문서와 예제가 대부분 이 방식이므로 참고 자료도 풍부하다. 단점은 Istio에 강하게 종속된다는 점이다. 나중에 다른 서비스 메시로 교체하면 모든 Gateway/VirtualService 리소스를 재작성해야 한다.

실무 선택 기준을 정리하면 다음과 같다. 신규 프로젝트이고 Fault Injection, Traffic Mirroring 같은 Istio 고급 기능을 사용하지 않을 계획이라면 Kubernetes Gateway API를 선택해 이식성을 확보하는 것이 합리적이다. 반면 카오스 엔지니어링, 카나리 배포 자동화, 세밀한 재시도 제어가 필요하다면 Istio Gateway API를 선택하고 Istio에 종속되는 결정을 의식적으로 내리는 것이 낫다.

기존 Istio Gateway API에서 Kubernetes Gateway API로 마이그레이션하는 경로는 이렇다. 먼저 현재 VirtualService 기능을 인벤토리화한다. `kubectl get virtualservice -A -o yaml`로 전체 VirtualService를 추출하고 Fault Injection, mirrorPercentage, 복잡한 retryOn 조건 등 Kubernetes Gateway API로 표현 불가능한 기능을 목록으로 만든다. 표현 불가능한 기능이 없는 서비스부터 순차적으로 `HTTPRoute`로 변환한다. 병행 운영 기간 동안 Istio는 두 API를 동시에 지원하므로 서비스 단위로 점진적 전환이 가능하다.

### 실무 적용

마이그레이션 대응표를 참고하면 변환 작업이 빠르다:

```yaml
# 기존: Istio Gateway API
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: my-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "example.com"

---
# 변환: Kubernetes Gateway API
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
spec:
  gatewayClassName: istio          # Istio를 구현체로 지정
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    hostname: "example.com"
    allowedRoutes:
      namespaces:
        from: All
```

```yaml
# 기존: VirtualService
apiVersion: networking.istio.io/v1
kind: VirtualService
spec:
  hosts:
  - "example.com"
  gateways:
  - my-gateway
  http:
  - route:
    - destination:
        host: my-service
        port:
          number: 8080

---
# 변환: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
spec:
  parentRefs:
  - name: my-gateway
    kind: Gateway
  hostnames:
  - "example.com"
  rules:
  - backendRefs:
    - name: my-service
      port: 8080
```

두 API는 병행 운영이 가능하므로 전환 중 서비스 중단이 없다.

---

## Q2. PASSTHROUGH 모드에서 SNI 기반 라우팅이 실패하는 흔한 원인과 디버깅 방법은?

### 왜 중요한가?

PASSTHROUGH 모드는 설정 자체는 단순하지만, 실제로 동작하지 않을 때 원인을 찾기 어렵다. TLS 핸드셰이크가 Gateway 이전에 실패하는지, Gateway 이후에 실패하는지 구별이 안 되면 디버깅 방향이 틀린다. SNI 라우팅 실패 원인을 체계적으로 분류해두면 문제 발생 시 빠르게 원인을 좁힐 수 있다.

### 분석

SNI 기반 PASSTHROUGH 라우팅 실패의 가장 흔한 원인은 네 가지다.

첫째, 클라이언트가 SNI를 보내지 않는 경우다. TLS 1.0 클라이언트나 일부 레거시 라이브러리는 SNI 확장을 보내지 않는다. Envoy는 SNI 없이 들어온 PASSTHROUGH 트래픽의 라우팅 대상을 결정할 수 없어 연결을 끊는다. `curl`로 테스트할 때 `-k` 옵션만 쓰면 SNI를 보내지만, `openssl s_client`로 확인할 때 `-servername` 옵션을 빠뜨리면 SNI가 없어서 테스트 결과가 실제와 다를 수 있다.

```bash
# SNI 포함 연결 확인
openssl s_client -connect $GATEWAY_IP:443 \
  -servername api.example.com \
  -showcerts 2>/dev/null | head -20

# SNI 미포함 연결 (실패 예상)
openssl s_client -connect $GATEWAY_IP:443 \
  -showcerts 2>/dev/null | head -20
```

둘째, Gateway `hosts`와 VirtualService `sniHosts`의 불일치다. VirtualService의 `sniHosts` 값이 클라이언트가 보내는 SNI 값과 정확히 일치해야 한다. 와일드카드 `*.example.com`은 VirtualService sniHosts에서 지원되지 않으므로, 각 도메인을 명시적으로 나열해야 한다.

셋째, 포트 매칭 문제다. VirtualService `tls.match.port`가 실제 Gateway 포트와 다르면 라우팅이 동작하지 않는다. Gateway에서 443 포트를 열었는데 VirtualService에서 `port: 8443`으로 매칭하면 일치하는 규칙이 없다.

넷째, DestinationRule과의 충돌이다. PASSTHROUGH 모드에서 백엔드 서비스에 대한 DestinationRule이 있고 `trafficPolicy.tls.mode: ISTIO_MUTUAL`이 설정되어 있으면, Envoy가 백엔드로 연결할 때 mTLS를 시도한다. 그런데 백엔드 서비스가 자체 TLS를 처리하는 경우(PASSTHROUGH 의도와 일치) Envoy의 mTLS 시도가 이미 TLS인 트래픽을 이중 암호화해 실패를 일으킨다.

### 실무 적용

PASSTHROUGH 라우팅 실패를 단계별로 디버깅하는 방법이다.

**1단계: Gateway 설정 확인**

```bash
# Gateway가 적용된 Envoy 설정 확인
istioctl proxy-config listeners istio-ingressgateway-xxx -n istio-system \
  --port 443

# 기대 출력: TLS mode: PASSTHROUGH, sniHosts 목록
```

**2단계: VirtualService 라우팅 확인**

```bash
# 라우팅 규칙 분석
istioctl analyze -n default

# PASSTHROUGH VirtualService 상태 확인
istioctl proxy-config routes istio-ingressgateway-xxx -n istio-system \
  --name https.443.tls-passthrough.my-gateway.istio-system
```

**3단계: 실시간 트래픽 로그**

```bash
# 게이트웨이 접근 로그 실시간 확인
kubectl logs -f istio-ingressgateway-xxx -n istio-system

# 연결 시도 + SNI 포함 테스트
curl -v --resolve "api.example.com:443:$GATEWAY_IP" \
  https://api.example.com/ \
  --cacert ca.crt
```

로그에 `upstream connect error` 또는 `no route matched`가 보이면 라우팅 규칙 문제이고, `SSL handshake error`가 보이면 백엔드 서비스의 TLS 설정 문제다.

---

## Q3. mTLS Gateway에서 클라이언트 인증서 검증이 실패할 때 어떤 로그를 확인해야 하는가?

### 왜 중요한가?

mTLS Gateway 설정은 올바르게 동작하는지 확인하기 어렵다. 클라이언트 인증서를 제공했음에도 연결이 실패할 때, 원인이 인증서 자체 문제인지 CA 체인 문제인지 Gateway 설정 문제인지 구별하지 못하면 디버깅에 많은 시간을 쓴다. 구체적인 로그 확인 경로를 알아두면 원인을 빠르게 좁힐 수 있다.

### 분析

mTLS 검증 실패는 크게 세 단계에서 발생한다.

**인증서 체인 검증 실패**: 클라이언트 인증서를 서명한 CA가 Gateway의 `ca.crt`에 포함되지 않으면 검증이 실패한다. `CERTIFICATE_VERIFY_FAILED` 에러가 발생한다. Secret에 포함된 `ca.crt`가 중간 CA만 있고 루트 CA가 없는 경우, 또는 CA 인증서가 만료된 경우에 발생한다.

**인증서 유효 기간 문제**: 클라이언트 인증서가 만료됐거나 아직 유효 기간 전인 경우다. TLS 핸드셰이크 중 `certificate has expired` 에러가 발생한다. 클라이언트 머신의 시스템 시간이 크게 어긋나 있어도 같은 증상이 나타난다.

**SAN(Subject Alternative Name) 불일치**: 일부 Gateway 설정에서 클라이언트 인증서의 SAN을 검증하는 경우, SAN이 기대 값과 다르면 거부된다.

디버깅에 필요한 로그 위치는 다음과 같다.

```bash
# 1. Gateway Pod 에러 로그 (TLS 핸드셰이크 에러)
kubectl logs istio-ingressgateway-xxx -n istio-system | grep -i "tls\|ssl\|cert"

# 2. Envoy 접근 로그에서 응답 플래그 확인
# UC = Upstream Connection terminated (일반 연결 실패)
# DC = Downstream Connection terminated (클라이언트가 끊음)
kubectl logs istio-ingressgateway-xxx -n istio-system | grep '"response_flags"'

# 3. Envoy 관리 인터페이스에서 TLS 통계 확인
kubectl exec istio-ingressgateway-xxx -n istio-system -- \
  curl -s localhost:15000/stats | grep ssl

# 기대 출력:
# listener.0.0.0.0_443.ssl.handshake: 10
# listener.0.0.0.0_443.ssl.fail_verify_cert_hash: 0
# listener.0.0.0.0_443.ssl.fail_verify_no_cert: 3  ← 인증서 미제공
# listener.0.0.0.0_443.ssl.fail_verify_san: 0
```

`fail_verify_no_cert` 카운터가 올라간다면 클라이언트가 인증서를 보내지 않은 것이다. `fail_verify_cert_hash`나 관련 카운터가 올라간다면 인증서 내용 검증 실패다.

### 실무 적용

mTLS 설정 전 단계적으로 검증하는 방법이다.

```bash
# 서버 인증서 + CA 체인 검증
openssl verify -CAfile ca.crt server.crt

# 클라이언트 인증서 검증
openssl verify -CAfile ca.crt client.crt

# mTLS 연결 전체 테스트
curl -v \
  --cert client.crt \
  --key client.key \
  --cacert ca.crt \
  https://api.example.com/

# Secret에 ca.crt가 올바르게 포함됐는지 확인
kubectl get secret my-tls-secret -n istio-system \
  -o jsonpath='{.data.ca\.crt}' | base64 -d | openssl x509 -noout -text
```

Gateway Secret을 생성할 때 mTLS용 Secret은 일반 TLS Secret과 형식이 다르다. `kubectl create secret tls`는 `ca.crt`를 포함하지 않으므로, generic Secret으로 직접 생성해야 한다:

```bash
kubectl create secret generic my-mtls-secret \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key \
  --from-file=ca.crt=ca.crt \
  -n istio-system
```

---

## Q4. 게이트웨이를 역할별로 분리할 때 리소스 할당과 스케일링 전략은?

### 왜 중요한가?

단일 인그레스 게이트웨이를 공용으로 사용하면 트래픽이 많은 서비스가 다른 서비스에 영향을 준다. 내부 API와 외부 공개 API가 같은 게이트웨이를 공유하면, 외부 트래픽 급증 시 내부 API 레이턴시도 올라간다. 역할별 Gateway 분리는 노이즈 이웃 문제를 해결하는 기본 패턴이지만, 분리 방식과 리소스 할당 전략을 이해하지 못하면 오히려 관리 복잡도만 늘어난다.

### 분析

역할별 Gateway 분리의 대표적인 두 가지 패턴은 트래픽 방향 분리와 테넌트 분리다.

트래픽 방향 분리는 인터넷 트래픽용 Gateway와 내부(클러스터 간, VPN) 트래픽용 Gateway를 별도로 만드는 방식이다. 인터넷 Gateway는 LoadBalancer Service를 사용하고, 내부 Gateway는 `service.beta.kubernetes.io/aws-load-balancer-internal: "true"` 어노테이션으로 내부 로드 밸런서에 연결한다. 두 Gateway는 리소스 격리, 보안 정책, 스케일링 정책을 독립적으로 설정할 수 있다.

테넌트 분리는 각 팀 또는 서비스 그룹마다 전용 Gateway를 부여하는 방식이다. 팀 A의 서비스는 `team-a-gateway`를, 팀 B의 서비스는 `team-b-gateway`를 사용한다. 팀별로 트래픽 패턴이 다르면 HPA 설정도 다르게 가져갈 수 있다. 단점은 Gateway 수가 늘어나면서 LoadBalancer 비용과 관리 오버헤드가 증가한다는 점이다.

리소스 할당 전략은 트래픽 패턴에 따라 달라진다. 외부 공개 API Gateway는 burst 트래픽을 감당해야 하므로 HPA를 설정하고 최소 replicas를 2~3으로 유지한다. 내부 전용 Gateway는 트래픽이 상대적으로 예측 가능하므로 고정 replicas로 운영해도 된다.

```yaml
# 외부 Gateway HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: external-gateway-hpa
  namespace: istio-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: external-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

Gateway Pod의 리소스 요청과 제한을 명시해야 노드 자원 경합을 방지할 수 있다. 일반적으로 Gateway Pod는 CPU 250m~500m, 메모리 128Mi~256Mi 요청으로 시작하고 실제 트래픽을 측정해 조정한다.

### 실무 적용

Gateway 분리를 결정하기 전 체크리스트다:

- 트래픽 방향이 다른가? (외부 vs 내부) → 분리 권장
- 보안 정책이 다른가? (mTLS 여부, IP 화이트리스트 등) → 분리 필수
- 스케일링 패턴이 다른가? (예측 가능 vs burst) → 분리 고려
- Gateway 수가 5개 이상이 되는가? → 통합 재검토

분리 후 운영 부담을 줄이려면 IstioOperator 또는 Helm values 파일로 Gateway 생성을 코드화하고, GitOps 파이프라인으로 관리한다. 수동으로 Gateway Deployment와 Service를 만들면 Istio 업그레이드 시 누락될 수 있다.

---

## Q5. Gateway에서 인증서 갱신(cert-manager 연동)을 자동화하는 방법과 주의사항은?

### 왜 중요한가?

TLS 인증서 만료는 서비스 중단의 흔한 원인 중 하나다. Let's Encrypt 인증서는 90일마다 갱신해야 한다. 수동으로 관리하면 만료 일정을 놓칠 위험이 있다. cert-manager는 Kubernetes에서 인증서를 자동 발급·갱신하는 표준 도구이며, Istio Gateway의 `credentialName`과 연동하면 인증서 갱신이 자동화된다.

### 分析

cert-manager와 Istio Gateway 연동의 핵심 흐름은 다음과 같다. cert-manager가 `Certificate` 리소스를 감시하다가 만료 기한이 가까워지면(기본값: 만료 30일 전) Let's Encrypt 또는 내부 CA에 새 인증서를 요청하고, 결과를 Kubernetes Secret으로 저장한다. Istio는 Secret 변경을 감지하고 Gateway의 TLS 설정을 새 인증서로 핫 리로드한다.

```yaml
# cert-manager Certificate 리소스
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls-cert
  namespace: istio-system   # Gateway와 같은 네임스페이스
spec:
  secretName: api-tls-secret  # Gateway의 credentialName과 일치
  dnsNames:
  - "api.example.com"
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  duration: 2160h    # 90일
  renewBefore: 720h  # 만료 30일 전 갱신
```

`secretName`이 Gateway의 `credentialName`과 정확히 일치해야 한다. cert-manager가 Secret을 생성하거나 업데이트하면, Istio 컨트롤 플레인이 변경을 감지해 새 인증서를 게이트웨이에 배포한다. 이 과정에서 인증서 교체 중 기존 연결이 끊기지 않는다. Envoy는 새 인증서로 신규 연결을 받으면서 기존 연결은 이전 인증서로 유지한다.

주의사항이 몇 가지 있다. 첫째, DNS-01 또는 HTTP-01 챌린지 방식을 선택해야 한다. 클러스터 외부에서 접근 불가능한 환경(프라이빗 클러스터)이라면 HTTP-01 챌린지가 동작하지 않는다. 이때는 Route53이나 Cloudflare 같은 DNS 공급자를 통한 DNS-01 챌린지를 사용한다.

둘째, Let's Encrypt의 rate limit이다. 같은 도메인에 대해 주당 5개의 인증서만 발급할 수 있다. 테스트 중 인증서 발급 실패가 반복되면 rate limit에 걸릴 수 있다. 프로덕션 배포 전에는 `letsencrypt-staging` Issuer로 테스트한다.

셋째, cert-manager가 생성한 Secret의 키 이름이다. cert-manager는 `tls.crt`와 `tls.key`를 생성하므로 Istio Gateway의 기대 형식과 일치한다. mTLS용으로 `ca.crt`도 필요하다면 `Certificate` 리소스에 `isCA: false`를 유지하면서 별도 CA Secret을 관리해야 한다.

### 실무 적용

```bash
# 인증서 상태 확인
kubectl describe certificate api-tls-cert -n istio-system
# STATUS: Ready = 정상, False = 발급 실패

# cert-manager 이벤트 확인
kubectl get events -n istio-system --field-selector reason=Issued

# 현재 인증서 만료일 확인
kubectl get secret api-tls-secret -n istio-system \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | \
  openssl x509 -noout -enddate

# Gateway에 새 인증서가 반영됐는지 확인
istioctl proxy-config secret istio-ingressgateway-xxx -n istio-system
```

인증서 갱신 실패에 대비한 알람 설정도 필요하다. Prometheus의 `certmanager_certificate_expiration_timestamp_seconds` 메트릭으로 만료 7일 전 알람을 설정하면 자동 갱신이 실패했을 때 수동 개입 시간을 확보할 수 있다.

---

## Q6. TCP Gateway를 사용할 때 HTTP Gateway와 달리 적용할 수 없는 Istio 기능은 무엇인가?

### 왜 중요한가?

TCP 프로토콜로 서비스를 노출할 때, 개발자들은 종종 HTTP Gateway와 동일한 Istio 기능을 기대한다. 실제로는 TCP Gateway에서 사용 불가능한 기능이 많다. 이를 모르고 TCP Gateway를 선택하면 나중에 필요한 기능을 추가할 수 없어 설계를 재검토해야 한다.

### 분析

Istio의 풍부한 트래픽 관리 기능 대부분은 HTTP/gRPC 프로토콜을 기반으로 한다. TCP는 L4 레이어 프로토콜이므로 Envoy가 페이로드를 해석할 수 없고, 결과적으로 L7 기능을 제공할 수 없다.

적용 불가 기능 목록이다.

**헤더 기반 라우팅**: HTTP 헤더나 경로를 기반으로 다른 서비스로 라우팅하는 것이 불가능하다. TCP는 포트 번호만으로 라우팅 대상을 결정한다. 카나리 배포나 A/B 테스트를 헤더로 제어하는 패턴이 동작하지 않는다.

**Fault Injection**: HTTP 응답 코드 기반의 장애 주입(abort)과 지연 주입(delay)은 HTTP 전용 기능이다. TCP 레벨에서는 연결 자체를 끊을 수 있지만, 특정 응답 코드를 반환하는 것은 불가능하다.

**재시도(Retry)**: HTTP 재시도는 서버가 5xx를 반환할 때 클라이언트 대신 Envoy가 요청을 재시도하는 기능이다. TCP에서는 응답 상태 코드 개념이 없으므로 재시도를 결정할 기준이 없다.

**요청/응답 메트릭**: Istio는 HTTP 요청 수, 레이턴시, 에러율 같은 L7 메트릭을 자동으로 수집한다. TCP Gateway에서는 바이트 전송량, 연결 수 같은 L4 메트릭만 수집된다. Kiali, Jaeger 같은 Istio 관측성 도구의 HTTP 대시보드가 동작하지 않는다.

**분산 추적**: HTTP 헤더(`x-b3-traceid` 등)를 기반으로 하는 분산 추적이 동작하지 않는다. TCP 연결에는 추적 컨텍스트를 전파할 메커니즘이 없다.

반면 TCP Gateway에서도 사용 가능한 기능이다:

- **mTLS**: TLS 레이어는 L4이므로 TCP Gateway에서도 mTLS가 동작한다
- **연결 풀 제어**: `DestinationRule`의 `connectionPool.tcp` 설정은 TCP에 적용된다
- **Outlier Detection**: TCP 연결 실패 기반의 아웃라이어 감지는 동작한다

### 실무 적용

TCP로 서비스를 노출해야 한다면, 먼저 HTTP 래퍼를 사용할 수 있는지 검토한다. gRPC는 HTTP/2 기반이므로 HTTP Gateway로 노출하면 Istio의 모든 L7 기능을 사용할 수 있다. WebSocket도 HTTP 업그레이드로 시작하므로 HTTP Gateway에서 처리 가능하다.

진짜 TCP 프로토콜이 필요한 경우(PostgreSQL, Redis, 커스텀 바이너리 등)는 TCP Gateway를 쓰되, 관측성 요구사항을 낮춰야 한다. TCP 레벨 메트릭은 `istio_tcp_connections_opened_total`, `istio_tcp_received_bytes_total`로 모니터링한다.

데이터베이스를 TCP Gateway로 노출하는 것은 특별한 이유가 없다면 피하는 것이 좋다. 데이터베이스 트래픽은 일반적으로 클러스터 내부에서만 접근하도록 설계하고, 외부 접근이 필요하면 전용 연결 풀러(PgBouncer, ProxySQL 등)를 사용하는 것이 표준 패턴이다.
