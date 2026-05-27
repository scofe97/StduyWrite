# Ch08. 탐구 질문 — 보안: 통신과 저장소

심화 학습을 위한 탐구 질문 모음이다. 각 질문은 LEARN.md에서 다루지 않은 트레이드오프와 실전 판단 기준을 다룬다.

각 질문에는 세 가지 요소가 있다. **탐구 방향**은 스스로 답을 찾아야 할 세부 질문이고, **직접 해보기**는 실제로 명령을 실행하거나 코드를 작성해 확인하는 실습이며, **조사할 자료**는 출발점이 되는 레퍼런스다. 모든 질문을 다 풀기보다 가장 궁금한 두 개를 골라 깊게 파고드는 것이 효과적이다.

---

## Q1. 대칭 vs 비대칭 암호화: 언제 어느 쪽을 선택하는가?

**배경**: TLS는 두 방식을 함께 쓰지만, 독립적인 설계 결정이 필요한 상황도 있다.

**탐구 방향**:
- 파일 암호화 도구(age, GPG)는 왜 하이브리드 방식을 쓰는가? 비대칭만으로는 왜 부족한가? 파일 크기가 커질수록 RSA 연산 비용이 어떻게 증가하는지 수치로 확인해보자.
- API 서명(JWT RS256 vs HS256)에서 비대칭을 선택하면 무엇이 달라지는가? 마이크로서비스 환경에서 검증 서버 없이 토큰을 검증할 수 있는 이유는 무엇인가? 공개 키를 JWKS 엔드포인트로 배포할 때의 캐시 전략은?
- 데이터베이스 컬럼 레벨 암호화(예: 주민등록번호 필드)에서 대칭 키를 선택하는 이유는? 비대칭으로 컬럼을 암호화하면 어떤 성능 문제가 생기는가?
- Envelope Encryption(봉투 암호화) 패턴은 두 방식의 어떤 장점을 어떻게 결합하는가? DEK(Data Encryption Key)와 KEK(Key Encryption Key)의 역할을 구분해보자.

**직접 해보기**: `openssl speed rsa2048 rsa4096`으로 키 크기별 연산 속도를 측정한 뒤, AES-256 속도와 비교해보자. 차이가 몇 배인가?

**조사할 자료**: AWS KMS Envelope Encryption 문서, JWT 알고리즘 선택 가이드(auth0)

---

## Q2. TLS 1.3이 TLS 1.2보다 나은 점은 무엇인가?

**배경**: 많은 레거시 시스템이 TLS 1.2를 사용한다. 1.3으로 업그레이드할 실질적 이유가 있는가?

**탐구 방향**:
- RTT 감소: 1.2는 2-RTT, 1.3은 1-RTT — 실제 레이턴시 차이는 얼마나 되는가? 0-RTT(Early Data)의 replay attack 위험은 어떻게 다루는가? 어떤 요청 타입에서만 0-RTT를 허용해야 안전한가?
- 취약한 암호 스위트 제거: 1.3에서 RSA 키 교환이 사라진 이유. PFS(Perfect Forward Secrecy)가 왜 필수가 되었는가? 과거 트래픽을 녹화해 두었다가 나중에 개인 키가 탈취되면 무슨 일이 생기는가?
- 핸드셰이크 암호화: 1.3에서 Certificate 메시지가 암호화되어 전송되는 것이 프라이버시에 어떤 의미가 있는가? SNI(Server Name Indication)는 여전히 평문인 문제를 ECH(Encrypted Client Hello)가 어떻게 해결하려 하는가?
- 이미 TLS 1.2를 쓰는 환경에서 1.3을 강제할 때 주의할 구형 클라이언트나 라이브러리는 무엇인가? Java 8 초기 버전, OpenSSL 1.0.x 등 구체적인 사례를 확인해보자.

**직접 해보기**: `openssl s_client -connect example.com:443 -tls1_3 2>/dev/null | grep "Protocol"` 로 실제 협상된 TLS 버전을 확인해보자. 그 다음 `-tls1_2`로 바꾸면 어떻게 달라지는가?

**조사할 자료**: RFC 8446 (TLS 1.3), Cloudflare TLS 1.3 블로그 포스트, ECH(Encrypted Client Hello) 초안

---

## Q3. 인증서 만료를 막는 자동 갱신 전략은 어떻게 설계하는가?

**배경**: certbot의 cron 하나로 충분한가? 대규모 인프라에서는 어떤 추가 장치가 필요한가?

**탐구 방향**:
- 갱신 실패 감지: certbot이 조용히 실패할 수 있는 경우(DNS 오류, 80포트 차단, Rate Limit 초과)를 어떻게 감지하는가? `--post-hook`과 `--deploy-hook`의 차이는 무엇이고, 실패 시 알람을 보내는 `--pre-hook` 패턴은?
- 만료 모니터링: Prometheus `ssl_certificate_expiry` 메트릭, Datadog SSL 모니터, 또는 간단한 cron + openssl 스크립트 중 어느 방식이 적합한 상황은? 30일 전, 14일 전, 7일 전 단계별 알람 설계를 생각해보자.
- Kubernetes 환경: cert-manager가 자동으로 처리하는 갱신 흐름은 어떻게 작동하는가? `Certificate` 리소스와 `CertificateRequest` 리소스의 관계는? 갱신된 인증서가 Pod에 자동으로 반영되려면 어떤 추가 설정이 필요한가?
- 와일드카드 인증서(`*.example.com`)는 웹루트 방식으로 발급이 불가능하다. DNS-01 챌린지를 사용할 때 자동화 방법(Route53 플러그인, Cloudflare 플러그인)과 IAM 최소 권한 설정은?
- 인증서 핀닝(Certificate Pinning)을 적용한 모바일 앱이 있을 때 인증서 교체가 미치는 영향과 대응 전략은? HPKP가 왜 폐기되었는지도 함께 조사해보자.

**직접 해보기**: `echo | openssl s_client -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -enddate` 를 cron에 등록해 만료일을 슬랙 알람으로 보내는 10줄짜리 쉘 스크립트를 작성해보자.

**조사할 자료**: cert-manager 공식 문서, certbot DNS 플러그인 목록, Let's Encrypt Rate Limits 문서

---

## Q4. 시크릿 로테이션 자동화에서 무엇이 가장 어려운가?

**배경**: AWS Secrets Manager의 자동 로테이션 버튼을 누르면 끝인가? 실전에서는 그렇지 않다.

**탐구 방향**:
- Double Write 문제: 로테이션 중 일부 앱 인스턴스는 구버전 시크릿을, 일부는 신버전을 사용하는 윈도우가 생긴다. Secrets Manager의 AWSPENDING/AWSCURRENT/AWSPREVIOUS 버전 레이블이 이 문제를 어떻게 다루는가? "즉시 삭제" 대신 AWSPREVIOUS를 일정 기간 유지하는 이유는?
- 커넥션 풀: DB 패스워드가 교체되었는데 앱이 이전 자격증명으로 맺은 커넥션 풀을 계속 유지한다. 어떤 감지 및 재연결 전략이 필요한가? HikariCP의 `keepaliveTime`과 `maxLifetime` 설정이 여기서 어떤 역할을 하는가?
- 외부 API 키: AWS가 관리하지 않는 서드파티 API 키(Stripe, Twilio)의 로테이션은 어떻게 자동화하는가? 커스텀 Lambda 로테이션 함수를 작성할 때 반드시 구현해야 하는 네 단계(createSecret, setSecret, testSecret, finishSecret)는 무엇인가?
- 로테이션 실패 알람: Lambda 로테이션 함수가 실패하면 어디서 확인할 수 있는가? CloudWatch Metric Filter로 로테이션 실패를 감지하고 SNS 알람을 보내는 설정을 직접 만들어보자.

**직접 해보기**: AWS CLI로 테스트용 시크릿을 생성하고, `aws secretsmanager rotate-secret --secret-id test/rotate-demo` 를 실행한 뒤 버전 레이블(AWSPENDING → AWSCURRENT)이 어떻게 전이되는지 `list-secret-version-ids`로 관찰해보자.

**조사할 자료**: AWS 블로그 "Rotate secrets for Amazon RDS", Vault Dynamic Secrets 문서, AWS Lambda 로테이션 함수 템플릿

---

## Q5. Zero Trust 보안 모델은 DevOps 워크플로에 어떤 변화를 가져오는가?

**배경**: "네트워크 안에 있으면 안전하다"는 전제를 버리는 Zero Trust는 실제로 무엇을 바꾸는가?

**탐구 방향**:
- VPN 없는 접근: Zero Trust Network Access(ZTNA)에서 개발자가 내부 서비스에 접근하는 방식은 기존 VPN과 어떻게 다른가? Cloudflare Access, Google BeyondCorp 같은 제품이 VPN의 어떤 문제를 해결하는가? 측면 이동(lateral movement) 공격이 VPN 환경에서 쉬운 이유는?
- 서비스 간 신뢰: 마이크로서비스 환경에서 "서비스 A는 서비스 B를 믿어도 되는가?"를 어떻게 판단하는가? mTLS와 SPIFFE/SPIRE가 이 문제를 어떻게 해결하는가? SVID(SPIFFE Verifiable Identity Document)의 구조는?
- CI/CD 파이프라인: 빌드 서버가 프로덕션 시크릿에 접근해야 할 때 Zero Trust 원칙을 어떻게 적용하는가? GitHub Actions에서 OIDC 토큰으로 AWS IAM 역할을 위임받는 흐름을 단계별로 정리해보자. 정적 Access Key 저장 방식과 무엇이 다른가?
- 최소 권한 자동화: IAM Access Analyzer가 실제 사용 패턴을 분석해 최소 권한 정책을 생성하는 방식은? Vault의 Policy as Code(Sentinel)와 어떻게 다른가?

**직접 해보기**: GitHub Actions 워크플로에서 `id-token: write` 권한을 추가하고 OIDC 토큰을 출력해보자. JWT 디코더로 `sub` 클레임이 어떤 형식인지 확인하고, 이 값으로 AWS IAM 신뢰 정책의 `Condition`을 어떻게 구성해야 하는지 작성해보자.

**조사할 자료**: Google BeyondCorp 논문, NIST SP 800-207 (Zero Trust Architecture), SPIFFE 공식 문서, GitHub Actions OIDC 문서

---

## Q6. SOPS vs Sealed Secrets vs Vault: Git에 시크릿을 저장하는 접근법 비교

**배경**: GitOps 워크플로에서 시크릿을 어떻게 다루는가? 세 도구는 서로 다른 철학을 갖는다.

**탐구 방향**:
- SOPS(Secrets OPerationS): 파일 전체가 아닌 값(value)만 암호화해 Git에 커밋한다. KMS/PGP/age 키로 복호화한다. 팀원마다 다른 키로 접근할 수 있는 장점은 `.sops.yaml`의 `creation_rules`로 어떻게 구현되는가? ArgoCD + SOPS 연동 시 복호화 시점은 언제인가?
- Sealed Secrets(Bitnami): Kubernetes 클러스터 안의 컨트롤러만 복호화할 수 있다. `kubeseal`로 암호화한 `SealedSecret`을 Git에 저장하는 방식이다. 클러스터가 삭제되면 복호화 키도 사라지는 위험을 백업 키로 어떻게 관리하는가? 네임스페이스 범위(namespace-scoped)와 클러스터 범위(cluster-scoped) SealedSecret의 차이는?
- Vault + External Secrets Operator: 시크릿 자체는 Git에 없고, Vault 경로 참조만 `ExternalSecret` 리소스로 Git에 저장한다. Vault에서 값을 가져와 Kubernetes `Secret`을 생성하는 흐름에서 토큰 갱신 주기와 캐시 전략은 어떻게 설정하는가?
- 도구 선택 기준: 팀이 3명인 스타트업, 30명의 멀티 클라우드 팀, 온프레미스 Kubernetes 운영 팀 각각에 어떤 도구가 어울리는가? 운영 복잡도와 보안 강도의 트레이드오프를 표로 정리해보자.

**직접 해보기**: SOPS + age 키로 간단한 YAML 파일을 암호화해보자. `age-keygen -o key.txt && sops --encrypt --age $(grep public key.txt | awk '{print $NF}') secret.yaml > secret.enc.yaml` 실행 후 암호화된 파일 구조를 살펴보고, 값(value)만 암호화되고 키(key)는 평문임을 확인하라.

**조사할 자료**: SOPS GitHub README, Bitnami Sealed Secrets 문서, External Secrets Operator 문서, ArgoCD Vault Plugin 문서

---

## 탐구 후 자기 점검

탐구를 마쳤다면 다음 질문에 스스로 답해보자. 답하기 어려운 항목이 있다면 해당 질문으로 돌아가 다시 조사한다.

- [ ] TLS handshake에서 PFS가 보장되는 이유를 세 문장 이내로 설명할 수 있는가?
- [ ] 자신이 운영하는 서비스의 인증서 만료일을 지금 당장 확인할 수 있는가?
- [ ] 코드베이스에서 환경변수로 주입되는 시크릿을 Secrets Manager로 이전하는 마이그레이션 계획을 한 단락으로 작성할 수 있는가?
- [ ] Zero Trust와 기존 경계 보안(Perimeter Security)의 차이를 동료에게 5분 안에 설명할 수 있는가?
