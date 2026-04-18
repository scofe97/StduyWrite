# Ch19. Ingress & Gateway API 점검 질문

## Q1: Ingress Controller가 없으면 Ingress 리소스가 무용지물인 이유

**질문**: Kubernetes 클러스터에 Ingress 리소스를 생성했는데 아무런 효과가 없다. Ingress Controller가 존재하지 않기 때문이다. 이 둘의 관계를 설명하고, Ingress Controller의 역할을 상세히 서술하라.

**핵심 포인트**:

- **Ingress 리소스는 선언(declaration)일 뿐이다**: `kind: Ingress`를 `kubectl apply`로 생성하면 Kubernetes API에 오브젝트가 저장된다. 그러나 이 오브젝트는 "이런 규칙으로 트래픽을 라우팅해 달라"는 의도를 표현한 것이지, 실제 트래픽 처리를 수행하는 것이 아니다. Deployment가 선언되면 Deployment Controller가 Pod를 생성하듯, Ingress가 선언되면 Ingress Controller가 리버스 프록시를 설정해야 한다. Controller가 없으면 선언만 API에 남아 있고 아무 일도 일어나지 않는다.

- **Ingress Controller의 정체**: Ingress Controller는 두 가지 역할을 합친 것이다. (1) **Kubernetes Controller**: API를 Watch하여 Ingress 리소스 변경을 감지하고, 변경 시 프록시 설정을 업데이트하는 제어 루프. (2) **리버스 프록시/로드밸런서**: 실제 외부 트래픽을 수신하여 백엔드 Service로 전달하는 네트워크 프록시(NGINX, Envoy, HAProxy 등). 즉, Ingress Controller = "Ingress 리소스를 감시하는 Controller" + "트래픽을 처리하는 프록시 서버"다.

- **Controller가 없을 때의 증상**: Ingress 리소스를 생성해도 `kubectl get ingress`에서 `ADDRESS` 필드가 비어 있거나 `<pending>` 상태다. 외부에서 접근해도 연결이 거부(Connection Refused)된다. `kubectl describe ingress`에서도 특별한 이벤트가 없다. 왜냐하면 이 리소스를 읽고 처리할 Controller 자체가 존재하지 않기 때문이다. 일반 Kubernetes 오브젝트(ConfigMap 등)처럼 API에 저장만 되어 있을 뿐이다.

- **ingressClassName의 역할**: Kubernetes 1.18+에서는 `spec.ingressClassName` 필드로 어떤 Ingress Controller가 이 Ingress를 처리할지 명시한다. 클러스터에 여러 Ingress Controller(NGINX + Traefik)가 설치되어 있을 때, `ingressClassName: nginx`로 지정하면 NGINX Controller만 이 Ingress를 처리한다. 지정하지 않으면 `ingressclass.kubernetes.io/is-default-class: "true"` 어노테이션이 있는 IngressClass의 Controller가 처리한다. IngressClass가 없거나 default가 지정되지 않으면 어떤 Controller도 처리하지 않는다.

- **Deployment와의 비유**: Deployment를 만들면 Deployment Controller가 ReplicaSet을 생성하고, ReplicaSet Controller가 Pod를 생성한다. 이 Controller들은 kube-controller-manager에 내장되어 있으므로 "별도 설치" 없이 동작한다. 반면 Ingress Controller는 kube-controller-manager에 포함되어 있지 않다. Kubernetes가 "어떤 리버스 프록시를 써야 하는지" 미리 결정하지 않았기 때문이다. NGINX를 쓸지, Traefik을 쓸지, Envoy를 쓸지는 클러스터 운영자가 선택해야 한다.

- **minikube에서의 실제 확인**: `minikube addons enable ingress`를 실행하기 전에 Ingress를 만들면 ADDRESS가 비어 있다. addon을 활성화하면 NGINX Ingress Controller Pod가 `ingress-nginx` 네임스페이스에 생성되고, 기존 Ingress를 자동으로 감지하여 ADDRESS를 할당한다. Controller가 처음 시작할 때 Kubernetes API에 대해 List 요청을 보내 모든 기존 Ingress를 가져오기 때문이다 (List-Watch 패턴의 List 단계).

**심화 질문**: Ingress Controller 없이 Ingress 리소스가 API에 저장만 되어 있으면, 나중에 Controller를 설치했을 때 기존 Ingress가 자동으로 인식되는가? Controller의 List-Watch 패턴에서 초기 List 단계가 이를 어떻게 처리하는가?

---

## Q2: Gateway API의 역할 분리 모델

**질문**: Gateway API가 GatewayClass, Gateway, HTTPRoute를 별도 리소스로 분리한 이유는 무엇이며, 이것이 대규모 조직에서 어떤 운영상의 이점을 제공하는가?

**핵심 포인트**:

- **Ingress의 역할 혼재 문제**: Ingress는 단일 리소스에 TLS 설정(인프라 관심사), 리스닝 포트(운영 관심사), 라우팅 규칙(개발 관심사)이 모두 들어 있다. 50명의 개발자가 같은 Ingress YAML을 수정하면 Git 충돌이 빈번하고, 한 팀의 실수가 다른 팀의 서비스에 영향을 미칠 수 있다. 예를 들어 개발자가 TLS 섹션을 잘못 건드려 전체 도메인의 인증서가 깨지거나, 경로 규칙을 잘못 수정하여 다른 팀의 트래픽을 가로챌 수 있다.

- **GatewayClass (인프라 관리자 담당)**: "어떤 Controller 구현체를 사용할지" 결정한다. 조직 전체 수준에서 한 번 결정하는 것으로, AWS ALB Controller, NGINX Gateway Fabric, Envoy Gateway 중 어떤 것을 표준으로 사용할지 정의한다. 인프라 관리자(CTO, 플랫폼 아키텍트)가 설정하며, 변경 빈도가 매우 낮다. 일반 개발자는 이 리소스를 수정할 권한이 없다.

- **Gateway (클러스터 운영자/플랫폼팀 담당)**: "어떤 포트에서, 어떤 프로토콜로, 어떤 TLS 인증서를 사용하여 트래픽을 수신할지" 정의한다. `listeners` 필드로 HTTP(80), HTTPS(443), TCP(5432) 등의 리스너를 설정하고, `allowedRoutes`로 어떤 네임스페이스의 Route를 허용할지 제어한다. 이는 RBAC과 결합하여 "team-a 네임스페이스는 api.myapp.com 리스너에만 Route를 추가할 수 있다"는 정책을 강제할 수 있다.

- **HTTPRoute (애플리케이션 개발자 담당)**: "내 서비스로 오는 트래픽의 라우팅 규칙"만 정의한다. 개발자는 TLS 인증서나 포트 설정에 신경 쓸 필요 없이, `parentRefs`로 공유 Gateway를 참조하고 자신의 호스트명/경로 규칙만 작성하면 된다. 각 팀이 자신의 네임스페이스에서 독립적으로 Route를 관리하므로 Git 충돌이 발생하지 않고, 다른 팀의 라우팅에 영향을 미칠 수 없다.

- **RBAC 연동 실무**: Kubernetes RBAC Role로 권한을 분리한다. `GatewayClass`는 ClusterRole `infra-admin`만 생성/수정 가능. `Gateway`는 `infra` 네임스페이스의 Role `platform-operator`만 가능. `HTTPRoute`는 각 팀의 네임스페이스에서 해당 팀의 Role `developer`가 생성/수정 가능. 이렇게 하면 개발자가 실수로 Gateway의 TLS 설정을 변경하거나, 다른 팀의 네임스페이스에 Route를 생성하는 것을 원천 차단한다.

- **상태 확인과 디버깅**: Ingress에서는 문제 발생 시 원인을 파악하기 어려웠다 (`status.loadBalancer.ingress` 정도). Gateway API는 각 리소스에 상세한 `Conditions`를 제공한다. Gateway에는 `Accepted`(Controller가 인식했는지), `Programmed`(설정이 적용되었는지). HTTPRoute에는 `Accepted`(Gateway가 수락했는지), `ResolvedRefs`(백엔드 Service가 존재하는지). 조건이 False이면 `reason`과 `message`에서 정확한 원인을 알 수 있다.

**심화 질문**: Gateway API에서 개발자가 생성한 HTTPRoute의 `parentRefs`가 존재하지 않는 Gateway를 참조하면 어떻게 되는가? Route가 "orphaned" 상태가 되는가? 이런 상황을 자동으로 감지하고 알림하는 메커니즘은 무엇인가?

---

## Q3: TLS 종단 위치의 차이

**질문**: TLS 종단을 Ingress(또는 Gateway)에서 하는 것과 Pod에서 직접 하는 것의 차이는 무엇이며, 어떤 경우에 어떤 방식을 선택해야 하는가?

**핵심 포인트**:

- **Ingress에서 TLS 종단 (TLS Termination)**: 클라이언트 → Ingress Controller 구간은 HTTPS(암호화), Ingress Controller → Pod 구간은 HTTP(평문)로 통신한다. Ingress Controller가 인증서를 관리하므로 모든 백엔드 Pod가 개별적으로 인증서를 설정할 필요가 없다. cert-manager를 사용하면 인증서 발급(Let's Encrypt)과 만료 전 자동 갱신까지 완전 자동화된다. 대부분의 웹 서비스에서 이 방식을 사용하며, 클러스터 내부 네트워크는 격리된 환경이므로 평문 통신도 수용 가능하다.

- **Pod에서 TLS 종단 (TLS Passthrough)**: Ingress Controller가 TLS를 복호화하지 않고 암호화된 트래픽을 그대로 Pod에 전달한다. Pod 내의 애플리케이션이 직접 인증서를 사용하여 TLS를 처리한다. Ingress Controller는 TLS ClientHello 메시지의 SNI(Server Name Indication) 필드만 읽고 라우팅하며, 요청 본문(HTTP 헤더, 경로 등)은 읽을 수 없다. NGINX Ingress에서는 `nginx.ingress.kubernetes.io/ssl-passthrough: "true"` 어노테이션으로 설정한다.

- **Ingress TLS 종단의 장점**: (1) **중앙화된 인증서 관리** — 인증서 갱신 시 Ingress Secret만 업데이트하면 됨, 각 Pod 재배포 불필요. cert-manager가 자동으로 처리하므로 운영 부담이 최소. (2) **L7 기능 사용 가능** — TLS가 복호화되어야 HTTP 내용(경로, 헤더, 쿠키)을 읽을 수 있으므로, 경로 기반 라우팅, 헤더 조작, 속도 제한, 인증 등 Ingress Controller의 L7 기능을 활용할 수 있다. (3) **성능 분리** — TLS 핸드셰이크와 암복호화의 CPU 부하를 Ingress Controller가 담당하므로 애플리케이션 Pod의 부하가 줄어든다.

- **Pod TLS 종단(Passthrough)의 장점**: (1) **진정한 End-to-End 암호화** — Ingress Controller도 평문 데이터를 볼 수 없으므로 보안이 극대화된다. PCI-DSS(신용카드), HIPAA(의료) 등 컴플라이언스 요구사항에서 "중간 프록시도 데이터를 읽어서는 안 된다"고 요구하는 경우 필수. (2) **mTLS(상호 TLS)** — 클라이언트 인증서를 Pod가 직접 검증할 수 있다. 서비스 간 인증에 사용되는 mTLS에서 Pod가 직접 인증서를 관리하면 Controller를 신뢰하지 않아도 된다.

- **Pod TLS 종단의 단점**: (1) 각 Pod가 인증서를 관리해야 한다 (Secret 마운트, 갱신 처리, 인증서 만료 모니터링). (2) Ingress Controller의 L7 라우팅 기능을 사용할 수 없다. SNI 기반 호스트 라우팅만 가능하며, 경로 기반 라우팅(`/api/v1`, `/api/v2`)이 불가능하다. (3) 디버깅이 어렵다 — Ingress Controller의 액세스 로그에서 요청 URL, 헤더, 응답 코드를 볼 수 없다.

- **하이브리드 방식 (TLS Re-encryption)**: Ingress Controller에서 TLS를 종단(복호화)하여 L7 기능을 사용하고, Pod으로 보낼 때 다시 새로운 TLS 연결(내부 인증서)을 수립한다. 클러스터 내부 네트워크도 암호화하면서 L7 기능을 사용할 수 있다. Gateway API에서는 `BackendTLSPolicy`로 이를 표준적으로 설정할 수 있다. 단, 암복호화가 두 번 발생하므로 성능 오버헤드가 있다.

**심화 질문**: Service Mesh(Istio, Linkerd)의 사이드카 mTLS와 Ingress TLS 종단의 관계는 무엇인가? Istio를 사용할 때 Ingress에서 TLS를 종단하고, Istio가 Pod 간 mTLS를 처리하면 이중 암호화가 되는가? 이 조합의 보안과 성능 트레이드오프는?

---

## Q4: PathType의 차이와 라우팅 우선순위

**질문**: Ingress에서 `pathType: Exact`, `Prefix`, `ImplementationSpecific`의 동작 차이를 설명하고, 여러 규칙이 겹칠 때의 우선순위를 서술하라.

**핵심 포인트**:

- **Exact**: 경로가 정확히 일치해야 매칭된다. `path: /api`는 `/api`에만 매칭되며, `/api/` (후행 슬래시), `/api/users` (하위 경로), `/API` (대소문자)에는 매칭되지 않는다. 특정 엔드포인트 하나만 노출할 때 사용한다. 예를 들어 건강 확인 엔드포인트 `/healthz`만 외부에 노출하고 싶을 때 Exact를 사용한다.

- **Prefix**: 경로 세그먼트(`/`로 구분) 단위로 접두사 매칭한다. 이것이 가장 중요한 동작 차이인데, **단순 문자열 접두사 매칭이 아니다**. `path: /api`는 `/api`, `/api/`, `/api/users`, `/api/users/123`에 매칭되지만, `/apiV2`, `/api-v2`에는 매칭되지 않는다. 왜냐하면 Prefix 매칭은 `/`로 분리된 세그먼트 단위로 비교하기 때문이다. `/api`는 세그먼트 `api`이고, `/apiV2`는 세그먼트 `apiV2`이므로 다른 세그먼트로 취급된다. 만약 문자열 접두사 매칭이었다면 `/api`는 `/apiV2`에도 매칭되어 예기치 않은 라우팅이 발생했을 것이다.

- **ImplementationSpecific**: 매칭 동작이 Ingress Controller 구현에 따라 달라진다. NGINX에서는 기본적으로 Prefix와 유사하게 동작하지만, 정규식 경로(`~`, `~*`)를 지원하는 Controller도 있다. Traefik에서는 다른 규칙을 적용할 수 있다. 이식성이 없으므로 가능하면 사용하지 않는 것이 좋다. Gateway API에서는 `RegularExpression` PathType을 명시적으로 표준화하여 이 문제를 해결했다.

- **우선순위 규칙**: (1) **Exact가 항상 Prefix보다 우선한다.** `/api`에 대해 Exact와 Prefix 규칙이 모두 있으면 Exact가 승리한다. (2) **Prefix 간에는 가장 긴 경로가 우선한다.** `/api/v1/users`는 `/api`보다 `/api/v1`이 우선하고, `/api/v1/users`가 가장 우선한다. (3) **같은 길이의 Prefix가 매칭되면** 호스트가 명시된 규칙이 와일드카드(`*`)보다 우선한다. (4) **그래도 동점이면** Ingress Controller 구현에 따라 다르다 (보통 생성 순서).

- **실수 사례와 방지**: `path: /`를 Prefix로 설정하면 모든 요청에 매칭된다 (모든 경로는 `/`로 시작하므로). 그러나 "가장 긴 경로 우선" 규칙 덕분에 `/api`가 `/`보다 항상 우선한다. 따라서 `path: /`는 안전한 fallback(기본 백엔드) 규칙으로 사용할 수 있다. 문제가 되는 경우는 `/static`이라는 경로를 Exact로 설정했는데, `/static/css/style.css` 같은 하위 경로가 매칭되지 않아 404가 반환되는 경우다. 정적 파일을 서빙하려면 Prefix를 사용해야 한다.

**심화 질문**: Gateway API의 HTTPRoute에서는 `path.type: RegularExpression`을 표준으로 지원한다. 정규식 경로와 Prefix 경로가 동일한 요청에 매칭될 때 우선순위는 어떻게 결정되는가? Gateway API의 매칭 우선순위 규칙은 Ingress와 어떻게 다른가?

---

## Q5: Gateway API의 다중 프로토콜 지원

**질문**: Ingress는 HTTP/HTTPS만 지원하는데, Gateway API는 TCP, UDP, gRPC를 어떻게 지원하는가? 각 프로토콜을 위한 Route 리소스는 무엇인가?

**핵심 포인트**:

- **Ingress의 HTTP 전용 설계**: Ingress 스펙은 `spec.rules[].http.paths`로 고정되어 있으며, HTTP 요청의 호스트명과 경로만 매칭할 수 있다. TCP 데이터베이스(MySQL 3306), UDP DNS(53), gRPC 서비스를 Ingress로 노출하려면 Controller별 비표준 방법을 써야 한다. 예를 들어 NGINX Ingress에서 TCP 서비스를 노출하려면 `tcp-services`라는 ConfigMap에 `"3306": "default/mysql-service:3306"` 형태로 포트 매핑을 추가해야 하는데, 이는 Ingress 리소스와 완전히 별개의 메커니즘이라 관리 일관성이 없다.

- **Gateway API의 Route 리소스 체계**: Gateway API는 프로토콜별로 별도의 Route 리소스를 정의하여 타입 안전성과 프로토콜별 최적화된 매칭 규칙을 제공한다. (1) **HTTPRoute**: HTTP/HTTPS 트래픽 라우팅. 호스트, 경로, 헤더, 쿼리파라미터, 메서드 매칭 지원. Ingress 대체. (2) **GRPCRoute**: gRPC 트래픽을 gRPC 서비스명(`service`)과 메서드명(`method`)으로 라우팅. 경로 기반이 아닌 gRPC 의미 체계에 맞는 라우팅 제공. (3) **TCPRoute**: TCP 트래픽을 포트 기반으로 라우팅. 데이터베이스(PostgreSQL, MySQL), Redis, 커스텀 TCP 프로토콜에 사용. (4) **TLSRoute**: TLS 패스스루 트래픽을 SNI(Server Name Indication) 기반으로 라우팅. TLS를 종단하지 않고 암호화된 상태로 백엔드에 전달. (5) **UDPRoute**: UDP 트래픽을 포트 기반으로 라우팅. DNS 서버, 게임 서버, VoIP 등에 사용.

- **Gateway의 다중 리스너**: Gateway 리소스에서 여러 리스너를 정의하여 다양한 프로토콜을 동시에 수신할 수 있다. 포트 80에서 HTTP, 포트 443에서 HTTPS, 포트 5432에서 TCP(PostgreSQL), 포트 50051에서 gRPC를 하나의 Gateway에서 모두 수신할 수 있다. 각 리스너는 `allowedRoutes.kinds`로 허용할 Route 종류를 제한한다. 예를 들어 포트 5432 리스너는 TCPRoute만 허용하고, 포트 443 리스너는 HTTPRoute만 허용하도록 설정한다.

- **GRPCRoute의 의미**: gRPC는 HTTP/2 위에서 동작하므로 기술적으로 HTTPRoute로도 라우팅 가능하다. gRPC 요청의 경로는 `/{package}.{ServiceName}/{MethodName}` 형태이므로 HTTPRoute의 Prefix 매칭으로 서비스를 구분할 수 있다. 그러나 GRPCRoute는 gRPC 의미 체계에 맞는 `matches.method.service`와 `matches.method.method` 필드를 제공하여, "UserService의 GetUser 메서드만 다른 백엔드로 보내라" 같은 gRPC 수준의 세밀한 라우팅을 표준으로 지원한다.

- **구현 현황과 성숙도**: HTTPRoute는 대부분의 Gateway API Controller가 지원하며 GA(v1.0) 상태다. GRPCRoute도 v1.1에서 GA가 되었다. TCPRoute, TLSRoute, UDPRoute는 아직 실험적(Experimental) 상태이며, Controller에 따라 지원 수준이 다르다. 2024년 기준 Envoy Gateway, Istio, Kong이 가장 넓은 범위의 Route 타입을 지원한다. 도입 전에 사용 중인 Controller의 conformance test 통과 현황을 확인해야 한다.

**심화 질문**: TCP 수준에서는 요청의 내용을 볼 수 없는데, TCPRoute는 어떤 기준으로 트래픽을 분기하는가? 같은 포트에서 여러 TCP 서비스를 구분할 수 있는가? TLSRoute의 SNI 기반 라우팅은 이 문제를 어떻게 해결하는가?

---

## Q6: 여러 팀이 같은 호스트를 공유할 때의 충돌 해결

**질문**: Gateway API에서 team-a와 team-b가 모두 `api.myapp.com`에 대한 HTTPRoute를 생성하면 충돌이 발생하는가? Gateway API는 이를 어떻게 처리하는가?

**핵심 포인트**:

- **같은 호스트, 다른 경로 (충돌 아님)**: team-a가 `api.myapp.com/users` 경로를, team-b가 `api.myapp.com/orders` 경로를 등록하면 이는 충돌이 아니라 정상적인 경로 분할이다. Gateway Controller는 두 HTTPRoute를 병합(merge)하여 하나의 라우팅 테이블을 생성한다. `/users` 요청은 team-a의 서비스로, `/orders` 요청은 team-b의 서비스로 전달된다. 이것이 Gateway API의 멀티테넌시 설계의 핵심 가치이다.

- **같은 호스트, 같은 경로 (진정한 충돌)**: team-a와 team-b가 모두 `api.myapp.com/api`에 대한 HTTPRoute를 생성하면 진정한 충돌이 발생한다. Gateway API는 이를 해결하기 위해 명확한 우선순위 규칙을 정의한다. (1) 가장 구체적인(긴) 경로가 우선한다. (2) 같은 길이면 Exact가 Prefix보다 우선한다. (3) 여전히 동점이면 생성 시각이 빠른(오래된) Route가 우선한다. (4) 마지막으로 알파벳 순서(namespace/name)가 기준이 된다. 이 결정론적 규칙 덕분에 어떤 Route가 적용될지 예측 가능하다.

- **Gateway의 allowedRoutes로 사전 방지**: 실무에서는 충돌이 발생하기 전에 Gateway의 `allowedRoutes`를 활용하여 각 팀이 관리할 수 있는 호스트를 사전에 분리한다. 예를 들어 Gateway에 두 개의 리스너를 만들고, `api.myapp.com` 리스너는 `namespace selector: team-a`만, `admin.myapp.com` 리스너는 `namespace selector: team-b`만 Route를 생성할 수 있도록 설정한다. 이렇게 하면 team-b가 `api.myapp.com`에 대한 HTTPRoute를 생성해도 Gateway가 수락하지 않는다.

- **HTTPRoute 상태로 충돌 확인**: 충돌 시 "패배한" HTTPRoute의 `status.parents[].conditions`에 구체적인 정보가 기록된다. `Accepted: False`는 Gateway가 Route를 수락하지 않았다는 뜻이며, `reason`과 `message`에서 원인을 알 수 있다. 예를 들어 "RouteConflict: path /api is already claimed by team-a/user-route" 같은 메시지가 기록된다. 개발자는 `kubectl describe httproute`로 자신의 Route가 정상적으로 적용되었는지 확인할 수 있다.

- **Ingress와의 차이**: Ingress에서는 같은 호스트/경로에 대해 여러 Ingress가 존재하면 Controller에 따라 동작이 예측 불가능했다. NGINX Ingress Controller는 Ingress 리소스의 `creationTimestamp`가 빠른 것을 우선하지만, 다른 Controller는 마지막에 업데이트된 것을 적용할 수도 있다. Gateway API는 이 모호함을 명확한 우선순위 규칙으로 표준화하여, Controller 구현과 무관하게 동일한 동작을 보장한다.

**심화 질문**: 여러 Gateway(예: `internal-gateway`, `external-gateway`)가 있을 때 하나의 HTTPRoute가 `parentRefs`에서 두 Gateway를 모두 참조할 수 있는가? 이 경우 같은 서비스가 내부/외부 모두에서 접근 가능해지는데, 이 패턴의 실무 사용 사례는 무엇인가?

---

## Q7: Ingress 어노테이션의 이식성 문제와 Gateway API의 해결 방식

**질문**: NGINX Ingress Controller의 어노테이션 기반 설정이 왜 문제가 되며, Gateway API는 이를 어떻게 해결하는가?

**핵심 포인트**:

- **어노테이션 의존성 문제**: Ingress 스펙 자체는 매우 단순하다 (호스트, 경로, TLS). 실무에서 필요한 기능(속도 제한, 인증, CORS, URL 리라이트, 타임아웃, 프록시 버퍼 크기 등)은 모두 Controller별 어노테이션으로 구현된다. NGINX의 `nginx.ingress.kubernetes.io/limit-rps: "10"`은 Traefik에서 동작하지 않는다. Traefik은 자체 IngressRoute CRD나 미들웨어를 사용한다. 즉, Ingress를 사용하면서도 사실상 특정 Controller에 종속(vendor lock-in)된다.

- **Controller 교체 시의 비용**: 조직이 NGINX에서 Envoy로 마이그레이션하려 할 때, 모든 Ingress 리소스의 어노테이션을 재작성해야 한다. 50개의 서비스에 각각 5~10개의 어노테이션이 있다면 250~500개의 설정을 변환해야 한다. 어노테이션 이름뿐만 아니라 값의 형식, 동작 차이(예: 타임아웃 단위가 초 vs 밀리초)도 확인해야 한다.

- **Gateway API의 표준화 접근**: Gateway API는 자주 사용되는 기능을 스펙에 직접 포함하여 Controller 간 이식성을 보장한다. (1) **트래픽 분할(weight)**: HTTPRoute의 `backendRefs[].weight`로 표준 지원. 어노테이션 불필요. (2) **헤더 기반 라우팅**: `matches[].headers`로 표준 지원. (3) **URL 리라이트**: `filters[].urlRewrite`로 표준 지원. (4) **리다이렉트**: `filters[].requestRedirect`로 표준 지원. (5) **헤더 조작**: `filters[].requestHeaderModifier`로 표준 지원. 이 기능들은 Gateway API를 지원하는 모든 Controller에서 동일하게 동작한다.

- **Policy Attachment 패턴**: 속도 제한, 인증, 재시도 정책 같은 고급 기능은 Controller마다 다를 수 있다. Gateway API는 이를 "Policy Attachment"라는 확장 메커니즘으로 처리한다. 각 Controller가 자체 Policy CRD(예: `BackendTLSPolicy`, `RateLimitPolicy`)를 정의하고, Gateway나 HTTPRoute에 "부착(attach)"한다. 어노테이션과 달리 Policy는 별도의 Kubernetes 리소스이므로 스키마 검증, RBAC, 버전 관리가 가능하다.

- **Conformance Test**: Gateway API는 Controller가 스펙을 올바르게 구현했는지 검증하는 Conformance Test Suite를 제공한다. 각 Controller는 테스트 통과 결과를 공개하며, 사용자는 "이 Controller가 HTTPRoute의 headerMatch를 올바르게 지원하는가?"를 테스트 결과로 확인할 수 있다. Ingress에는 이런 표준 테스트가 없어서 Controller 간 동작 차이를 발견하려면 직접 테스트해야 했다.

**심화 질문**: 어노테이션 기반 설정의 장점도 있다 — 단순하고, 별도 CRD 없이 Ingress 리소스 하나로 모든 설정을 관리할 수 있다. 소규모 팀에서 Ingress + 어노테이션이 Gateway API보다 더 적합한 경우는 언제인가? "YAGNI(You Ain't Gonna Need It)" 원칙을 적용하면 언제 Gateway API로 전환하는 것이 적절한가?
