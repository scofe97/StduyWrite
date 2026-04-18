# Ch07. 네트워킹 기초 — INVESTIGATE

> 이 파일은 LEARN.md를 읽은 후 스스로 답을 찾아가는 탐구 질문 모음이다.
> 검색, 실습, 공식 문서를 통해 답을 작성하라.

---

## Q1. Public vs Private Subnet의 차이와 NAT Gateway의 역할

Public Subnet과 Private Subnet의 기술적 차이는 무엇인가? Route Table에서 차이를 확인하라.

- Public Subnet의 Route Table에는 `0.0.0.0/0 → IGW`가 있다. Private Subnet에는 무엇이 있는가?
- `map_public_ip_on_launch = true`를 설정하지 않으면 Public Subnet에 올려도 인터넷에서 접근이 안 될 수 있다. 왜인가?
- NAT Gateway가 Private Subnet의 아웃바운드 트래픽을 처리하는 흐름을 단계별로 설명하라 (앱 서버 → NAT GW → IGW → 인터넷).
- NAT Gateway는 왜 Public Subnet에 위치해야 하는가? Private Subnet에 두면 어떤 문제가 생기는가?
- NAT Gateway는 비용이 발생한다. 시간당 요금 외에 데이터 전송 요금도 있다. 대안으로 NAT Instance를 사용하는 경우의 트레이드오프는 무엇인가?
- 멀티 AZ 구성에서 NAT Gateway를 AZ마다 하나씩 두는 이유는 무엇인가? 단일 NAT Gateway로 모든 AZ를 처리하면 어떤 위험이 생기는가?

**탐구 방향**: AWS NAT Gateway 요금 페이지, OpenTofu `aws_nat_gateway` 리소스 문서

---

## Q2. DNS TTL 설정과 장애 시 영향

TTL은 캐시 유효 시간이다. 이 값이 장애 복구 속도에 직접 영향을 미친다.

- 현재 `app.example.com`의 TTL이 3600초(1시간)로 설정되어 있다. 서버 IP를 변경하면 전 세계 DNS 캐시가 새 IP를 반영하는 데 최대 얼마나 걸리는가?
- 블루-그린 배포에서 DNS 전환을 사용한다고 가정하자. 배포 48시간 전에 TTL을 60초로 낮춰야 한다는 이유를 설명하라.
- TTL을 항상 60초로 낮게 유지하면 안 되는 이유는 무엇인가? DNS 서버 부하와 Resolver 캐시 관점에서 설명하라.
- Route53의 ALIAS 레코드는 TTL을 직접 설정할 수 없다. AWS가 내부적으로 어떻게 처리하는가?
- Negative TTL(NXDOMAIN 응답의 캐시 시간)은 어디서 설정하는가? 잘못 설정하면 어떤 문제가 생기는가?
- Route53 헬스체크와 DNS Failover를 함께 구성할 때 TTL이 낮아야 하는 이유를 설명하라. 헬스체크 간격과 TTL의 권장 관계는 무엇인가?

**탐구 방향**: `dig +trace` 출력에서 각 레코드의 TTL 값 관찰, RFC 2308 (Negative Caching)

---

## Q3. L4 vs L7 로드밸런싱 선택 기준

로드밸런서는 어느 레이어에서 동작하느냐에 따라 할 수 있는 것과 비용이 달라진다.

- L4 로드밸런서(AWS NLB)와 L7 로드밸런서(AWS ALB)의 라우팅 결정 기준 차이를 설명하라.
- L4는 헬스체크를 TCP 연결 성공으로 판단한다. L7은 HTTP 200 응답으로 판단한다. 어떤 상황에서 L4 헬스체크가 "통과"했지만 실제 서비스는 장애 상태일 수 있는가?
- gRPC, WebSocket 같은 긴 연결(long-lived connection)을 다룰 때 L4와 L7 중 어느 것이 유리한가? 이유는?
- nginx upstream의 `least_conn` 알고리즘이 `round-robin`보다 유리한 시나리오는 어떤 경우인가?
- AWS ALB에서 경로 기반 라우팅(`/api/*`는 API 서버, `/static/*`는 S3)을 구성하려면 L4로는 불가능하다. 그 이유를 OSI 모델 관점에서 설명하라.
- Sticky Session(세션 고정)을 L4와 L7에서 각각 어떻게 구현하는가? ALB의 `stickiness` 쿠키 방식과 NLB의 소스 IP 고정 방식의 차이는 무엇인가?

**탐구 방향**: AWS ALB vs NLB 비교 문서, nginx `upstream` 지시어 공식 문서

---

## Q4. nginx reverse proxy에서 필수 헤더 (X-Forwarded-For, X-Real-IP)

Reverse Proxy 뒤의 백엔드는 클라이언트 IP를 어떻게 알 수 있는가?

- nginx 없이 클라이언트가 직접 백엔드에 접근하면 `request.remoteAddr`는 클라이언트 IP다. nginx를 통하면 무엇이 되는가?
- `X-Forwarded-For` 헤더는 쉼표로 구분된 IP 목록을 담을 수 있다. 여러 프록시를 거쳤을 때 어떤 순서로 IP가 쌓이는가? 실제 클라이언트 IP는 몇 번째에 있는가?
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`에서 `$proxy_add_x_forwarded_for` 변수의 동작을 설명하라. 기존 헤더가 있을 때와 없을 때 각각 어떻게 처리하는가?
- 악의적인 클라이언트가 `X-Forwarded-For: 1.2.3.4` 헤더를 요청에 직접 포함하면 어떻게 되는가? 이를 방어하려면 nginx 설정에서 어떻게 해야 하는가? (`real_ip_header`, `set_real_ip_from`)
- Spring Boot에서 `server.forward-headers-strategy=native` 설정의 역할을 설명하라.
- ALB 뒤에 nginx가 있는 2단 프록시 구성에서 `X-Forwarded-For`에 신뢰할 수 없는 IP가 추가될 수 있다. ALB가 삽입하는 IP와 클라이언트가 조작한 IP를 어떻게 구분하는가?

**탐구 방향**: nginx `ngx_http_realip_module` 문서, Spring Boot 프록시 헤더 처리 문서

---

## Q5. VPC Peering vs Transit Gateway

여러 VPC를 연결해야 할 때 두 가지 선택지가 있다. 언제 무엇을 쓰는가?

- VPC Peering은 두 VPC를 1:1로 연결한다. VPC A, B, C가 있을 때 모두 연결하려면 몇 개의 Peering 연결이 필요한가? VPC가 10개라면?
- VPC Peering은 전이적 라우팅(transitive routing)을 지원하지 않는다. A-B Peering, B-C Peering이 있어도 A에서 C로 직접 통신이 안 되는 이유를 설명하라.
- Transit Gateway는 허브-앤-스포크 모델로 동작한다. 어떻게 전이적 라우팅 문제를 해결하는가?
- Transit Gateway의 단점은 무엇인가? (비용, 레이턴시 관점)
- 동일 계정 내 2개의 VPC를 연결할 때 VPC Peering이 더 나은 선택인 경우는 언제인가?
- Transit Gateway Route Table을 분리하면 VPC 간 격리 정책을 세밀하게 제어할 수 있다. 개발/스테이징/프로덕션 VPC를 같은 TGW에 연결하면서도 개발↔프로덕션 직접 통신을 차단하는 구성 방법을 설명하라.

**탐구 방향**: AWS Transit Gateway 요금, VPC Peering 한계 공식 문서

---

## Q6. mTLS와 서비스 간 통신 보안

일반 TLS는 클라이언트가 서버를 검증한다. mTLS는 서버도 클라이언트를 검증한다. 이것이 마이크로서비스 환경에서 왜 중요한가?

- 일반 TLS로 HTTPS를 사용하면 서버 신원은 보장된다. 하지만 어떤 보안 위협이 여전히 남는가? (내부 네트워크의 악성 서비스가 API를 호출하는 시나리오)
- mTLS에서 클라이언트 인증서는 어떻게 발급하고 갱신하는가? 수동 관리의 문제점은 무엇인가?
- Linkerd와 Istio가 mTLS를 자동화하는 방법을 설명하라. 개발자가 별도로 설정할 것이 있는가?
- SPIFFE/SPIRE가 해결하는 문제는 무엇인가? "워크로드 신원(workload identity)"이란 개념을 IP 기반 신원과 비교하여 설명하라.
- nginx에서 mTLS를 수동으로 구성하려면 어떤 지시어가 필요한가? (`ssl_verify_client`, `ssl_client_certificate`)
- 인증서 만료 직전에 자동 갱신하지 못했을 때 서비스 간 통신이 전면 중단된다. Cert-Manager가 이 문제를 해결하는 방식과 갱신 실패를 감지하는 모니터링 방법을 설명하라.

**탐구 방향**: SPIFFE 공식 문서, Linkerd Ch07 (mTLS), `runners-high/poc/03_CloudNative/03-service-mesh/learning/` Ch04

---

## Q7. CDN과 엣지 네트워킹

CDN은 콘텐츠를 사용자에게 가까운 서버에서 제공한다. 단순 캐시 이상의 역할을 한다.

- CDN의 PoP(Point of Presence)과 오리진 서버의 관계를 설명하라. 캐시 미스(cache miss)가 발생했을 때 트래픽 흐름은 어떻게 되는가?
- CloudFront의 캐시 동작은 `Cache-Control` 헤더와 CloudFront 캐시 정책 중 어느 것이 우선하는가? 오리진이 `Cache-Control: no-store`를 반환해도 CloudFront가 캐시할 수 있는가?
- CDN을 사용할 때 캐시 무효화(cache invalidation)가 필요한 상황은 어떤 경우인가? CloudFront에서 파일 경로별 무효화와 버전 파라미터(`?v=2`) 방식의 트레이드오프를 설명하라.
- 엣지 컴퓨팅(CloudFront Functions, Lambda@Edge)은 CDN 엣지에서 코드를 실행한다. 오리진 서버에서 실행하는 것과 비교했을 때 적합한 사용 사례와 제약 조건은 무엇인가?
- CDN이 DDoS 방어에 기여하는 원리를 설명하라. 오리진 IP가 노출되면 CDN 방어가 우회될 수 있다. 이를 방지하는 방법은 무엇인가?
- 지역 차단(Geo-Restriction)과 지역 라우팅(Geo-Routing)의 차이를 설명하라. Route53 지리적 라우팅과 CloudFront 지역 차단을 함께 사용하는 시나리오를 제시하라.

**탐구 방향**: CloudFront 캐시 정책 문서, Lambda@Edge vs CloudFront Functions 비교, AWS Shield

---

## 자가 점검 체크리스트

아래 항목에 답할 수 있으면 이 챕터를 이해한 것이다.

- [ ] Private Subnet 인스턴스가 인터넷으로 아웃바운드 요청을 보내는 경로를 그림으로 그릴 수 있다
- [ ] 배포 전날 DNS TTL을 낮추는 이유와 되돌려야 하는 시점을 설명할 수 있다
- [ ] `/api/v1/users` 경로의 요청만 특정 Target Group으로 보내려면 어떤 로드밸런서가 필요한지 고를 수 있다
- [ ] nginx 설정에서 클라이언트 IP 위조 공격을 방어하는 설정을 작성할 수 있다
- [ ] VPC가 5개일 때 Full-mesh Peering 개수와 Transit Gateway 연결 개수를 계산할 수 있다
- [ ] 서비스 메시 없이 mTLS를 수동으로 구현할 때 발생하는 운영 부담을 설명할 수 있다
- [ ] CDN 캐시 무효화 비용을 최소화하는 정적 자산 배포 전략을 설명할 수 있다
