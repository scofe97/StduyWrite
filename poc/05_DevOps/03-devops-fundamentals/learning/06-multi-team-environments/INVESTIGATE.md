# Ch06. 멀티 팀과 환경 관리 - 점검 질문

LEARN.md의 내용을 얼마나 이해했는지 확인하는 질문들이다. 단순 암기가 아닌 실제 트레이드오프를 설명할 수 있어야 한다.

---

## Q1. Terraform Workspace vs 디렉토리 분리 전략

**질문**: Terraform으로 멀티 환경을 관리할 때, Workspace 방식과 디렉토리 분리 방식(environments/dev, environments/prod) 중 어떤 상황에서 무엇을 선택해야 하는가?

**핵심 포인트**
- Workspace는 동일한 코드로 여러 state를 유지 — 코드 중복은 없지만 환경 간 코드가 완전히 동일해야 한다는 제약이 생긴다
- 디렉토리 분리는 환경별로 다른 모듈 버전이나 완전히 다른 리소스 구성을 허용한다 — 유연성이 높지만 변경 시 여러 디렉토리를 동기화해야 한다
- `terraform.workspace` 변수 남용은 코드 복잡도를 올린다 — 조건 분기가 많아지면 디렉토리 분리가 더 명확할 수 있다
- Workspace는 state 백엔드 설정이 필수 — 로컬 state는 팀 협업에 적합하지 않다
- 실무에서는 "모듈화 + 디렉토리 분리"가 Workspace보다 더 널리 쓰이는 이유를 설명할 수 있어야 한다
- Workspace 이름은 `terraform.workspace` 변수로 접근하지만, CI/CD에서는 브랜치 이름과 workspace 이름을 어떻게 매핑할지 규칙이 필요하다

**심화 질문**: Terraform Cloud/Enterprise의 Workspace와 오픈소스 Terraform CLI의 Workspace는 개념이 어떻게 다른가?

---

## Q2. Kubernetes RBAC 최소 권한 설계

**질문**: CI/CD 파이프라인이 K8s 클러스터에 배포할 때, ServiceAccount에 부여할 최소 권한 집합을 어떻게 결정하는가? ClusterRole 대신 Role을 쓰는 이유는 무엇인가?

**핵심 포인트**
- `ClusterRole`은 모든 네임스페이스에 걸쳐 권한을 부여한다 — CI/CD 파이프라인이 ClusterRole을 가지면 타 팀의 리소스에도 접근 가능하다
- `Role`은 특정 네임스페이스에만 적용 — 팀별 네임스페이스 구조에서 Role이 격리 경계를 유지하는 핵심이다
- `verbs: ["*"]`는 절대 금지 — get/list/watch/create/update/patch 각각의 의미를 알고 필요한 것만 열어야 한다
- `kubectl auth can-i --list --as=system:serviceaccount:alpha:team-alpha-deployer`로 실제 권한을 검증할 수 있다
- Secrets의 경우 read-only도 신중해야 한다 — External Secrets Operator나 Vault Agent Injector를 쓰면 파이프라인이 Secret 값을 직접 볼 필요가 없다
- 권한 설계 후 주기적으로 `kubectl auth can-i` 감사를 자동화하면 권한 드리프트(처음엔 적절했으나 시간이 지나 과도해진 권한)를 감지할 수 있다

**심화 질문**: 여러 팀이 같은 클러스터를 쓸 때, 네임스페이스 간 통신이 필요한 경우(예: 공유 모니터링 스택)에는 RBAC를 어떻게 설계해야 하는가?

---

## Q3. 환경별 시크릿 관리: Vault vs Sealed Secrets

**질문**: Kubernetes 환경에서 시크릿을 GitOps 방식으로 관리하려 할 때, HashiCorp Vault와 Sealed Secrets(Bitnami)의 트레이드오프는 무엇인가?

**핵심 포인트**
- Sealed Secrets는 암호화된 상태로 Git에 저장 가능 — 복호화 키(private key)가 클러스터 안에만 있어 Git 유출이 일어나도 안전하다
- Vault는 중앙 집중식 — 동적 시크릿(DB 자격증명 자동 생성), 접근 감사 로그, TTL 기반 자동 만료를 제공한다
- Sealed Secrets는 운영이 단순하지만 클러스터별로 다른 키를 가진다 — 멀티 클러스터 환경에서 동기화가 복잡해진다
- Vault는 운영 복잡도가 높다 — Vault 자체의 HA 구성, 언시일(unseal) 관리, 백업 정책이 필요하다
- External Secrets Operator는 Vault/AWS Secrets Manager/GCP Secret Manager를 K8s Secret으로 동기화하는 미들웨어 — 벤더 의존 없이 유연한 선택이 가능하다
- AWS IRSA(IAM Roles for Service Accounts)나 GCP Workload Identity를 활용하면 장기 자격증명 없이 클라우드 시크릿 서비스에 접근할 수 있다

**심화 질문**: Sealed Secrets의 복호화 키를 분실했을 때 복구 방법은? 이를 방지하기 위해 운영에서 어떤 절차를 지켜야 하는가?

---

## Q4. Feature Branch 환경 (Ephemeral Environments)

**질문**: PR이 열릴 때마다 임시 환경(preview environment)을 자동 생성하고, PR이 닫히면 삭제하는 패턴의 장단점과 구현 방법은 무엇인가?

**핵심 포인트**
- Ephemeral Environment는 QA가 실제 URL로 변경 사항을 검증할 수 있게 한다 — "내 로컬에선 됐는데"를 없애는 효과가 있다
- K8s에서는 PR 번호를 Namespace 이름으로 사용(`pr-1234`)해 완전한 격리 환경을 만들 수 있다
- 비용이 문제다 — PR 환경은 보통 축소된 사이즈로 만들고, 활동 없으면 자동 슬립 또는 삭제 정책이 필요하다
- 데이터베이스 시드 전략이 복잡하다 — 프로덕션 데이터 복제는 개인정보 문제, 빈 DB는 테스트 불편
- Vercel/Railway 같은 플랫폼은 이 기능을 내장 — 직접 구현 대신 플랫폼 레벨에서 해결하는 것도 전략이다
- PR이 닫힐 때 네임스페이스 삭제를 보장하려면 GitHub Actions의 `pull_request` 이벤트 중 `closed` 타입을 트리거로 사용하고, 삭제 실패 시 알림 경보를 추가해야 자원 누수를 막을 수 있다

**심화 질문**: Feature Branch 환경에 외부 서비스(결제, SMS)가 연동될 때, 실제 API를 호출하지 않도록 하는 방법은 무엇인가?

---

## Q5. CODEOWNERS와 PR 리뷰 자동화

**질문**: CODEOWNERS 파일이 있어도 리뷰가 병목이 되는 경우가 많다. CODEOWNERS를 실제로 효과적으로 운영하기 위해 GitHub Branch Protection Rules에서 어떤 설정을 함께 해야 하는가?

**핵심 포인트**
- "Require review from Code Owners" 옵션을 활성화해야 CODEOWNERS가 강제력을 가진다 — 파일만 있어도 리뷰어 추가가 안 되면 우회 가능하다
- 팀 단위(@org/team)로 지정하면 팀원 중 누구든 리뷰해도 통과 — 개인(@user) 지정은 병목을 만든다
- CODEOWNERS는 `.github/CODEOWNERS`, `CODEOWNERS`, `docs/CODEOWNERS` 순서로 검색 — 위치에 따라 적용 범위가 달라진다
- 너무 세밀한 CODEOWNERS는 오히려 속도를 떨어뜨린다 — "모든 파일에 CTO 승인" 같은 설정은 형식이 목적을 잡아먹는 예다
- Draft PR 상태에서는 CODEOWNERS 리뷰 요청을 보류하는 것이 팀 피로도를 줄인다
- 모노레포에서 CODEOWNERS 패턴이 많아지면 순서가 중요하다 — 아래에 있는 규칙이 위의 규칙을 덮어쓰므로, 더 구체적인 패턴을 파일 아래쪽에 배치해야 의도대로 동작한다

**심화 질문**: CODEOWNERS에 지정된 팀원이 퇴사하거나 팀을 이동했을 때 발생하는 문제는 무엇이며, 이를 자동으로 감지하는 방법은?

---

## Q6. 스테이징 환경의 프로덕션 유사성 보장

**질문**: 스테이징 환경이 프로덕션과 다를 때 어떤 종류의 버그가 스테이징을 통과해 프로덕션에서 발견되는가? 유사성을 높이는 데 현실적으로 가장 중요한 요소 세 가지는 무엇인가?

**핵심 포인트**
- 데이터 볼륨 차이 — 스테이징에 레코드 100개, 프로덕션에 100만 개면 인덱스 누락이나 N+1 쿼리가 스테이징에서는 보이지 않는다
- 의존 서비스 버전 차이 — 스테이징에서 DB 마이너 버전이 다르면 특정 SQL 동작이 달라질 수 있다
- 인프라 크기 차이 — 단일 노드 스테이징에서는 분산 시스템의 레이스 컨디션이 재현되지 않는다
- 네트워크 레이턴시 차이 — 스테이징에서 타임아웃이 여유로우면 프로덕션 네트워크 지연으로 인한 실패를 놓친다
- 실제 트래픽 패턴 — 스테이징에 트래픽이 없으면 프로덕션의 동시성 문제가 드러나지 않는다
- 스테이징과 프로덕션의 차이를 명문화한 "환경 유사성 체크리스트"를 팀에서 관리하면, 유사성이 시간이 지나며 낮아지는 드리프트를 정기적으로 점검할 수 있다

**심화 질문**: 프로덕션 데이터를 익명화해 스테이징으로 주기적으로 복사하는 파이프라인을 설계한다면, 어떤 개인정보 처리 고려사항이 필요한가?

---

## 점검 체크리스트

이 챕터의 핵심 개념을 실제로 이해했는지 확인하는 최종 항목이다.

- [ ] `terraform workspace list`로 현재 workspace를 확인하고, 다른 workspace로 전환해 `terraform plan` 결과가 달라지는 것을 설명할 수 있다
- [ ] K8s 클러스터에서 `kubectl auth can-i create deployments --as=system:serviceaccount:alpha:team-alpha-deployer -n alpha`를 실행해 의도한 권한이 적용되었는지 검증할 수 있다
- [ ] `docker compose -f docker-compose.yml -f docker-compose.prod.yml config`로 병합 결과를 확인하고, override 우선순위를 설명할 수 있다
- [ ] CODEOWNERS 파일을 작성하고, Branch Protection Rules에서 "Require review from Code Owners"를 활성화하는 전체 절차를 설명할 수 있다
- [ ] dev/staging/prod 각 환경의 목적과 그 목적 차이가 인프라 설정에 어떻게 반영되는지 한 문단으로 설명할 수 있다
