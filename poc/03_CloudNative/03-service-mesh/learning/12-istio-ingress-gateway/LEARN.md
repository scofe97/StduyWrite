# Ch12. Istio Ingress Gateway

> 📌 **핵심 요약**: Ingress Gateway는 외부 트래픽이 서비스 메시로 진입하는 첫 번째 문이다. Kubernetes Ingress가 단순한 HTTP 라우팅만 제공한다면, Istio Gateway는 TLS 종료, SNI 기반 멀티 호스트, TCP 프록시까지 처리한다. Gateway 리소스로 "어떤 포트와 호스트를 열것인가"를 정의하고, VirtualService로 "어느 백엔드로 보낼 것인가"를 연결하는 이분법적 설계가 핵심이다.

---

## 🎯 학습 목표

1. Gateway 리소스와 VirtualService의 역할 분리를 설명하고 두 리소스를 연결하는 방법을 작성할 수 있다
2. TLS 모드(SIMPLE, MUTUAL, PASSTHROUGH)를 구별하고 각 상황에 적합한 모드를 선택할 수 있다
3. SNI(Server Name Indication) 원리를 이해하고 단일 Gateway로 여러 도메인을 서빙하는 설정을 작성한다
4. HTTP 트래픽을 HTTPS로 리다이렉트하는 VirtualService 규칙을 구성할 수 있다
5. TCP Gateway를 사용해 비-HTTP 프로토콜을 메시에 노출하는 방법을 이해한다
6. Istio Gateway API와 Kubernetes Gateway API의 차이를 구별하고 선택 기준을 설명할 수 있다

---

## 1. Ingress Gateway의 역할

### 1.1 외부 트래픽 진입점으로서의 Gateway

서비스 메시 내부에서 Pod 간 통신은 사이드카 프록시(Envoy)가 자동으로 처리한다. 그러나 클러스터 외부에서 들어오는 트래픽은 다르다. 외부 요청은 메시 바깥에서 시작하므로 사이드카가 없다. 이 진입 지점을 담당하는 컴포넌트가 Ingress Gateway Envoy 프록시다.

Istio는 `istio-system` 네임스페이스에 `istio-ingressgateway`라는 Deployment를 배포한다. 이 Pod는 사이드카가 아닌 독립 Envoy 프록시로, Kubernetes Service(LoadBalancer 타입)에 연결되어 외부 IP를 가진다. 외부 트래픽은 LoadBalancer → Gateway Pod → 서비스 메시 내부 Pod 순으로 흐른다.

```
외부 클라이언트
      │
      ▼
LoadBalancer Service (istio-ingressgateway)
      │
      ▼
Ingress Gateway Pod (Envoy)
      │
      ▼
내부 서비스 Pod (사이드카 Envoy)
```

Kubernetes Ingress와 비교하면 차이가 명확하다. Ingress는 HTTP/HTTPS만 처리하고 TLS 옵션이 제한적이다. Istio Gateway는 HTTP, HTTPS, TLS, TCP, mTLS를 모두 처리하며, VirtualService와 결합하면 헤더 기반 라우팅, 트래픽 미러링, 장애 주입도 가능하다.

### 1.2 Istio Gateway API vs Kubernetes Gateway API

이름이 비슷해서 혼동하기 쉽지만 완전히 다른 API다. Istio Gateway API는 Istio가 자체적으로 정의한 CRD이며, `networking.istio.io/v1` 그룹에 속하는 `Gateway`와 `VirtualService` 리소스로 구성된다. 오랜 기간 사용된 안정적인 API로, 대부분의 Istio 예제와 공식 문서가 이를 기반으로 한다.

Kubernetes Gateway API는 Kubernetes SIG-Network에서 정의한 표준 API다. `gateway.networking.k8s.io` 그룹에 속하며, `GatewayClass`, `Gateway`, `HTTPRoute`, `TCPRoute` 등으로 구성된다. Istio는 이 표준 API의 구현체로도 동작할 수 있다. 즉, Kubernetes Gateway API 리소스를 작성하면 Istio가 이를 해석해 Envoy 설정을 생성한다.

| 항목 | Istio Gateway API | Kubernetes Gateway API |
|------|-------------------|----------------------|
| API 그룹 | `networking.istio.io/v1` | `gateway.networking.k8s.io` |
| 트래픽 수신 리소스 | `Gateway` | `Gateway` (동명) |
| 라우팅 리소스 | `VirtualService` | `HTTPRoute`, `TCPRoute` |
| 이식성 | Istio 전용 | 멀티 구현체 지원 |
| 성숙도 | GA, 안정 | GA (v1.0 이후) |
| Fault Injection | 지원 | 미지원 (확장 필요) |

현재 시점에서 대부분의 실무 환경은 Istio Gateway API를 사용한다. 신규 프로젝트이고 멀티 컨트롤러 이식성이 중요하다면 Kubernetes Gateway API를 고려할 수 있으나, Istio 특화 기능(fault injection, mirror 등)을 활용하려면 Istio 전용 확장이 필요하다.

### 1.3 Gateway + VirtualService 리소스 관계

Gateway 리소스만으로는 트래픽이 내부 서비스에 도달하지 않는다. Gateway는 포트와 호스트를 "열어주는" 역할만 하며, 실제 라우팅은 VirtualService가 담당한다. 두 리소스를 연결하는 고리는 VirtualService의 `gateways` 필드다.

```
Gateway 리소스                     VirtualService 리소스
─────────────────────────────     ──────────────────────────────────
spec.servers:                     spec.gateways:
  - port: 80                        - my-gateway   ← Gateway 이름 참조
    hosts:                         spec.hosts:
      - "*.example.com"               - "api.example.com"
```

VirtualService의 `hosts`는 Gateway의 `hosts`와 일치하거나 그 하위 집합이어야 한다. Gateway가 `*.example.com`을 허용한다면 VirtualService는 `api.example.com`이나 `www.example.com`을 지정할 수 있다. 매칭이 맞지 않으면 요청이 라우팅되지 않고 404가 반환된다.

---

## 2. 기본 HTTP 라우팅

### 2.1 Gateway 리소스 정의 (포트, 호스트)

Gateway 리소스는 Envoy 프록시가 수신(listen)할 포트, 프로토콜, 허용할 호스트를 정의한다. 어떤 Envoy 프록시에 이 설정을 적용할지는 `selector` 레이블로 지정한다.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway   # istio-ingressgateway Pod에 적용
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*.example.com"       # 와일드카드 호스트 허용
```

`selector`는 Gateway를 적용할 Envoy 프록시를 선택한다. `istio: ingressgateway`는 기본 인그레스 게이트웨이 Pod를 선택한다. 역할별로 분리된 Gateway를 운영할 때는 별도 Deployment와 Service를 만들고 다른 레이블을 사용한다.

`hosts`의 와일드카드 패턴은 조심해서 사용해야 한다. `"*"`는 모든 호스트를 허용하는데, 이는 보안상 좋지 않다. 가능하면 실제 도메인 패턴을 명시하는 것이 좋다.

### 2.2 VirtualService로 서비스 연결

Gateway 뒤에서 실제 라우팅을 처리하는 VirtualService를 작성한다. `gateways` 필드로 위에서 정의한 Gateway를 참조하면, 외부 트래픽을 내부 서비스로 연결할 수 있다.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-vs
  namespace: default
spec:
  hosts:
  - "api.example.com"
  gateways:
  - istio-system/my-gateway   # namespace/name 형식
  http:
  - match:
    - uri:
        prefix: /v1
    route:
    - destination:
        host: api-service      # 쿠버네티스 Service 이름
        port:
          number: 8080
  - route:
    - destination:
        host: api-service
        port:
          number: 8080
```

`gateways` 필드에 `namespace/name` 형식으로 참조한다. 같은 네임스페이스라면 이름만 써도 된다. `mesh`라는 특수 값을 추가하면 외부 Gateway 트래픽과 메시 내부 트래픽 모두에 이 VirtualService를 적용할 수 있다.

VirtualService 없이 Gateway만 있으면 요청이 들어와도 라우팅 대상이 없어 `404`나 `503`이 반환된다. Gateway는 "문을 연다", VirtualService는 "어디로 안내한다"고 이해하면 된다.

### 2.3 호스트 기반 라우팅과 SNI

단일 IP(LoadBalancer)에서 여러 도메인을 서빙하는 것은 흔한 요구사항이다. HTTP에서는 `Host` 헤더를 보고 라우팅하면 된다. 하나의 Gateway에 여러 호스트를 정의하고, 각 호스트에 대응하는 VirtualService를 작성하면 된다.

```yaml
# Gateway: 두 호스트 모두 수신
spec:
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "api.example.com"
    - "web.example.com"

---
# VirtualService for api.example.com
spec:
  hosts:
  - "api.example.com"
  gateways:
  - my-gateway
  http:
  - route:
    - destination:
        host: api-service

---
# VirtualService for web.example.com
spec:
  hosts:
  - "web.example.com"
  gateways:
  - my-gateway
  http:
  - route:
    - destination:
        host: web-service
```

HTTPS에서 여러 도메인을 서빙하려면 SNI가 필요하다. TLS 핸드셰이크는 HTTP 헤더보다 먼저 일어나므로, 서버는 클라이언트가 어떤 도메인으로 접속했는지 TLS 레벨에서 알아야 올바른 인증서를 제시할 수 있다. SNI는 ClientHello 메시지에 도메인 이름을 포함시켜 서버가 적절한 인증서를 선택하게 한다.

---

## 3. Gateway TLS 보안

### 3.1 SIMPLE 모드 (서버 TLS)

SIMPLE 모드는 가장 일반적인 HTTPS 설정이다. 서버만 인증서를 제시하고, 클라이언트는 별도 인증서 없이 서버를 신뢰하면 된다. 브라우저가 HTTPS로 서버에 접속하는 일반적인 방식이 SIMPLE 모드다.

인증서는 Kubernetes Secret에 저장하고, Gateway에서 참조한다. Secret의 키는 `tls.crt`(인증서)와 `tls.key`(개인 키) 형식이어야 한다.

```yaml
# Secret 생성
kubectl create secret tls my-tls-secret \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem \
  -n istio-system

---
# Gateway TLS 설정
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: my-tls-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: my-tls-secret   # Secret 이름
    hosts:
    - "api.example.com"
```

`credentialName`은 인그레스 게이트웨이와 같은 네임스페이스(istio-system)의 Secret을 참조한다. 인증서를 다른 네임스페이스의 Secret에서 참조하고 싶다면 `cacert`나 `privateKey` 필드로 직접 경로를 지정해야 하는데, 이는 권장 방식이 아니다.

### 3.2 MUTUAL 모드 (상호 TLS/mTLS)

MUTUAL 모드는 서버뿐만 아니라 클라이언트도 인증서를 제시해야 하는 양방향 TLS다. 주로 B2B API나 내부 시스템 간 통신처럼 클라이언트 신원을 검증해야 하는 상황에서 사용한다.

```yaml
spec:
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: MUTUAL
      credentialName: my-tls-secret        # 서버 인증서
      # CA 인증서는 Secret에 ca.crt 키로 포함되어야 함
    hosts:
    - "api.example.com"
```

MUTUAL 모드에서 Secret은 `tls.crt`, `tls.key` 외에 `ca.crt`(클라이언트 인증서를 서명한 CA 인증서)도 포함해야 한다. 클라이언트는 이 CA가 서명한 인증서를 제시해야 접속이 허용된다. CA 인증서 검증에 실패하면 TLS 핸드셰이크 단계에서 연결이 거부된다.

클라이언트 인증서가 없는 curl 요청은 다음과 같이 실패한다:

```bash
# 실패: 클라이언트 인증서 없음
curl https://api.example.com/
# SSL handshake failed: certificate required

# 성공: 클라이언트 인증서 제공
curl --cert client.crt --key client.key \
     --cacert ca.crt \
     https://api.example.com/
```

### 3.3 PASSTHROUGH 모드 (앱에서 TLS 처리)

PASSTHROUGH 모드는 Gateway가 TLS를 종료하지 않고, 암호화된 트래픽을 그대로 백엔드 서비스로 전달한다. TLS 핸드셰이크와 인증서 관리를 애플리케이션이 직접 처리하고 싶을 때 사용한다.

```yaml
spec:
  servers:
  - port:
      number: 443
      name: tls
      protocol: TLS
    tls:
      mode: PASSTHROUGH
    hosts:
    - "api.example.com"
```

PASSTHROUGH에서는 `credentialName`이 없다. Gateway는 TLS 내용을 보지 않고 SNI 정보만 읽어 라우팅 결정을 내린 뒤, 암호화된 패킷을 그대로 백엔드로 넘긴다. VirtualService는 `tls` 섹션을 사용해 SNI 기반으로 라우팅한다.

```yaml
# PASSTHROUGH 라우팅 VirtualService
spec:
  hosts:
  - "api.example.com"
  gateways:
  - my-gateway
  tls:
  - match:
    - port: 443
      sniHosts:
      - "api.example.com"
    route:
    - destination:
        host: api-service
        port:
          number: 443
```

PASSTHROUGH의 장점은 엔드-투-엔드 암호화다. Gateway가 TLS를 종료하지 않으므로 인증서 개인 키가 Gateway에 노출되지 않는다. 단점은 Gateway 레벨에서 HTTP 내용을 볼 수 없으므로 헤더 기반 라우팅, 장애 주입, 트래픽 미러링 등 Istio의 L7 기능을 사용할 수 없다는 점이다.

### 3.4 HTTP → HTTPS 리다이렉트

HTTP로 들어온 요청을 HTTPS로 리다이렉트하는 것은 보안의 기본이다. Istio에서는 Gateway에서 80 포트를 열고, VirtualService에서 리다이렉트 규칙을 정의한다.

```yaml
# Gateway: 80포트와 443포트 모두 정의
spec:
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "api.example.com"
    tls:
      httpsRedirect: true   # 80으로 오면 443으로 리다이렉트
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: my-tls-secret
    hosts:
    - "api.example.com"
```

`httpsRedirect: true`를 설정하면 Gateway는 HTTP 요청에 대해 자동으로 `301 Moved Permanently`를 반환하고, `Location` 헤더에 `https://` URL을 담는다. 별도 VirtualService 없이도 리다이렉트가 동작한다. 리다이렉트 이후의 HTTPS 트래픽 처리는 443 포트 server 설정과 연결된 VirtualService가 담당한다.

---

## 4. 멀티 호스트 서빙

### 4.1 SNI 기반 인증서 분리

단일 Gateway에서 여러 도메인의 HTTPS 트래픽을 처리하려면 도메인마다 다른 인증서를 제공해야 한다. 이것이 SNI가 필요한 이유다. 클라이언트가 TLS 핸드셰이크 시 SNI로 도메인을 알려주면, Gateway는 해당 도메인에 맞는 인증서를 선택해 응답한다.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: multi-host-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https-api
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: api-tls-secret    # api.example.com 인증서
    hosts:
    - "api.example.com"
  - port:
      number: 443
      name: https-web
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: web-tls-secret    # web.example.com 인증서
    hosts:
    - "web.example.com"
```

두 서버 블록이 모두 443 포트를 사용하지만, `hosts`가 다르다. Envoy는 SNI를 보고 `api.example.com`으로 오면 `api-tls-secret` 인증서를, `web.example.com`으로 오면 `web-tls-secret` 인증서를 사용한다. 두 도메인은 동일한 LoadBalancer IP를 공유하지만 각자의 인증서를 가진다.

### 4.2 하나의 Gateway에서 여러 도메인 처리

멀티 호스트 Gateway의 각 도메인은 별도 VirtualService로 라우팅을 정의한다. VirtualService는 네임스페이스를 넘어서 동작할 수 있으므로, 각 팀이 자신의 네임스페이스에서 VirtualService를 관리하고 공유 Gateway를 참조하는 패턴이 가능하다.

```yaml
# 팀 A의 VirtualService (namespace: team-a)
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-routing
  namespace: team-a
spec:
  hosts:
  - "api.example.com"
  gateways:
  - istio-system/multi-host-gateway
  http:
  - route:
    - destination:
        host: api-service.team-a.svc.cluster.local
        port:
          number: 8080

---
# 팀 B의 VirtualService (namespace: team-b)
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: web-routing
  namespace: team-b
spec:
  hosts:
  - "web.example.com"
  gateways:
  - istio-system/multi-host-gateway
  http:
  - route:
    - destination:
        host: web-service.team-b.svc.cluster.local
        port:
          number: 3000
```

이 패턴에서 Gateway는 인프라 팀이 관리하고, 각 애플리케이션 팀은 VirtualService만 관리한다. Gateway 변경 권한이 없어도 라우팅 규칙을 추가할 수 있어 책임 분리가 명확해진다.

---

## 5. TCP 트래픽

### 5.1 TCP 포트 노출

HTTP가 아닌 TCP 기반 프로토콜(MySQL, PostgreSQL, Redis, 커스텀 바이너리 프로토콜 등)도 Istio Gateway로 노출할 수 있다. 포트 번호로만 라우팅이 결정되므로 HTTP처럼 경로나 헤더 기반 조건을 사용할 수 없다.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: tcp-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 31400
      name: tcp
      protocol: TCP
    hosts:
    - "*"
```

TCP Gateway는 `hosts: ["*"]`를 많이 사용한다. TCP 레벨에서는 HTTP `Host` 헤더 같은 식별자가 없으므로 포트 번호가 유일한 라우팅 기준이다.

인그레스 게이트웨이 Service의 `spec.ports`에도 해당 포트가 있어야 한다. Helm 차트나 IstioOperator로 설치했다면 `gateways.istio-ingressgateway.ports`에 포트를 추가해야 한다.

### 5.2 TCP Gateway + VirtualService

TCP VirtualService는 `tcp` 섹션을 사용한다. 매칭 조건은 포트 번호만 사용할 수 있다.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: tcp-echo-vs
  namespace: default
spec:
  hosts:
  - "*"
  gateways:
  - istio-system/tcp-gateway
  tcp:
  - match:
    - port: 31400
    route:
    - destination:
        host: tcp-echo-service
        port:
          number: 9000
```

`tcp` 섹션은 `http`와 달리 `uri`, `headers` 같은 매칭 조건이 없다. 포트 번호와 소스 레이블만 사용 가능하다. TCP 트래픽은 페이로드를 검사하지 않으므로 Istio의 L7 기능(재시도, 장애 주입, 서킷 브레이킹의 HTTP 부분 등)을 사용할 수 없다.

Echo 서버로 TCP Gateway를 테스트하는 방법은 다음과 같다:

```bash
# TCP 연결 테스트
GATEWAY_IP=$(kubectl get svc istio-ingressgateway \
  -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# netcat으로 TCP 연결 후 메시지 전송
echo "Hello TCP Gateway" | nc $GATEWAY_IP 31400
# 에코 서버라면 동일 메시지가 반환된다
```

### 5.3 SNI Passthrough 라우팅

PASSTHROUGH 모드에서 여러 서비스를 SNI 이름으로 구별해 라우팅할 수 있다. 이 방식은 각 서비스가 자체 TLS를 처리하면서도 단일 LoadBalancer 포트를 공유한다.

```yaml
# Gateway: TLS PASSTHROUGH
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: sni-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: tls-passthrough
      protocol: TLS
    tls:
      mode: PASSTHROUGH
    hosts:
    - "service-a.example.com"
    - "service-b.example.com"

---
# VirtualService A: SNI로 service-a 라우팅
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: sni-vs-a
spec:
  hosts:
  - "service-a.example.com"
  gateways:
  - sni-gateway
  tls:
  - match:
    - port: 443
      sniHosts:
      - "service-a.example.com"
    route:
    - destination:
        host: service-a
        port:
          number: 443

---
# VirtualService B: SNI로 service-b 라우팅
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: sni-vs-b
spec:
  hosts:
  - "service-b.example.com"
  gateways:
  - sni-gateway
  tls:
  - match:
    - port: 443
      sniHosts:
      - "service-b.example.com"
    route:
    - destination:
        host: service-b
        port:
          number: 443
```

이 패턴을 "SNI Routing" 또는 "SNI Passthrough"라고 부른다. Gateway는 SNI를 읽어 라우팅하지만, TLS 내용은 보지 않는다. 각 서비스는 자신의 인증서로 클라이언트와 직접 TLS를 맺는다.

---

## 6. 운영 팁

### 6.1 게이트웨이 역할 분리 (전용 Gateway 생성)

기본 `istio-ingressgateway`는 모든 트래픽을 처리하는 공용 게이트웨이다. 인터넷 트래픽과 내부 트래픽을 같은 게이트웨이로 처리하면 보안 정책을 분리하기 어렵다. 역할별로 전용 Gateway를 만드는 것이 권장 패턴이다.

전용 Gateway를 만들려면 새 Deployment와 Service를 만들고 고유 레이블을 부여한다:

```yaml
# 내부 전용 게이트웨이 (internal)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: internal-gateway
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: internal-gateway
  template:
    metadata:
      labels:
        app: internal-gateway
        istio: internal-gateway   # 고유 레이블
      annotations:
        inject.istio.io/templates: gateway  # Gateway injection 템플릿
    spec:
      containers:
      - name: istio-proxy
        image: auto                          # Istio가 자동으로 이미지 채움
```

이 Deployment에 Gateway 리소스를 연결할 때는 `selector.istio: internal-gateway`를 사용한다. 인터넷 Gateway는 `istio: ingressgateway`, 내부 Gateway는 `istio: internal-gateway`로 구별한다.

### 6.2 게이트웨이 주입 (Gateway Injection)

Istio 1.13부터 인그레스 게이트웨이를 위한 새로운 배포 방식인 Gateway Injection이 도입됐다. 기존 방식은 사전에 Gateway 바이너리를 직접 지정했지만, Gateway Injection 방식은 사이드카 주입과 유사하게 Pod에 어노테이션을 추가하면 Istio가 자동으로 Envoy 컨테이너를 주입한다.

```yaml
# Gateway Injection 방식 Deployment
spec:
  template:
    metadata:
      annotations:
        inject.istio.io/templates: "gateway"  # 게이트웨이 템플릿 사용
      labels:
        sidecar.istio.io/inject: "true"       # 주입 활성화
        istio: my-gateway
    spec:
      containers:
      - name: istio-proxy
        image: auto   # Istio가 버전에 맞는 이미지로 채움
```

Gateway Injection의 장점은 Istio 업그레이드 시 게이트웨이 이미지도 자동으로 맞춰진다는 점이다. 별도로 게이트웨이 이미지 버전을 관리할 필요가 없다.

### 6.3 액세스 로그 설정 (Telemetry API)

기본적으로 Istio 인그레스 게이트웨이는 모든 요청의 액세스 로그를 stdout으로 출력한다. Telemetry API로 이 동작을 커스터마이징할 수 있다.

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: gateway-access-log
  namespace: istio-system
spec:
  selector:
    matchLabels:
      istio: ingressgateway
  accessLogging:
  - providers:
    - name: envoy             # 기본 Envoy 액세스 로그
    disabled: false
    filter:
      expression: "response.code >= 400"  # 에러만 로깅
```

`filter.expression`에 CEL(Common Expression Language) 표현식을 사용해 특정 조건의 요청만 로깅하거나, `disabled: true`로 로깅을 완전히 끌 수 있다. 대용량 트래픽 환경에서는 모든 요청을 로깅하면 디스크 I/O와 스토리지 비용이 급증하므로 에러나 느린 요청만 선택적으로 로깅하는 것이 합리적이다.

### 6.4 PILOT_FILTER_GATEWAY_CLUSTER_CONFIG

Istio 컨트롤 플레인은 기본적으로 모든 서비스에 대한 Envoy 설정(cluster config)을 모든 게이트웨이에 전송한다. 서비스가 수백 개 이상인 대규모 클러스터에서는 이로 인해 게이트웨이 Pod의 메모리 사용량이 불필요하게 높아지고, 설정 배포 시간도 길어진다.

`PILOT_FILTER_GATEWAY_CLUSTER_CONFIG=true` 환경 변수를 istiod에 설정하면, 컨트롤 플레인이 각 게이트웨이에서 실제로 사용하는 서비스의 cluster 설정만 전송한다. VirtualService에서 참조하지 않는 서비스는 해당 게이트웨이에서 Envoy cluster가 생성되지 않는다.

```yaml
# IstioOperator로 설정
spec:
  components:
    pilot:
      k8s:
        env:
        - name: PILOT_FILTER_GATEWAY_CLUSTER_CONFIG
          value: "true"
```

이 최적화는 수십 개 이상의 서비스를 가진 클러스터에서 게이트웨이 메모리를 30~60% 줄이는 효과가 있다. 다만 설정 후에는 게이트웨이에서 사용할 서비스가 VirtualService에 명시적으로 포함되어야 라우팅이 동작하므로, 암묵적 cluster 접근에 의존하던 설정을 점검해야 한다.

---

## 📝 핵심 정리

**Gateway 역할 분리**는 Istio 트래픽 관리의 핵심 설계 원칙이다. Gateway는 포트와 호스트를 열어주는 "허가권"이고, VirtualService는 실제 라우팅 규칙이다. 두 리소스를 분리함으로써 인프라 팀과 애플리케이션 팀이 독립적으로 설정을 관리할 수 있다.

**TLS 모드 선택 기준**은 다음과 같다. 일반 웹 서비스는 SIMPLE, 클라이언트 신원 검증이 필요한 B2B API는 MUTUAL, 애플리케이션이 TLS를 직접 관리해야 한다면 PASSTHROUGH를 선택한다. PASSTHROUGH를 선택하면 Istio L7 기능을 포기해야 하므로 신중히 결정해야 한다.

**SNI**는 멀티 호스트 HTTPS 환경에서 빠질 수 없는 개념이다. 단일 IP에서 여러 도메인의 인증서를 서빙하려면 SNI가 필요하고, Istio는 서버 블록을 도메인별로 분리해 각각 다른 `credentialName`을 사용하는 방식으로 구현한다.

**대규모 운영**에서는 `PILOT_FILTER_GATEWAY_CLUSTER_CONFIG`로 불필요한 cluster 설정 전파를 줄이고, 역할별 전용 Gateway 분리로 보안 정책과 스케일링 전략을 독립적으로 관리한다.
