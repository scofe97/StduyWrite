# Ch02. Infrastructure as Code — INVESTIGATE

심화 탐구 질문 모음. 각 질문은 LEARN.md의 개념을 실제 운영 맥락으로 확장한다.

---

## Q1. 선언적 IaC와 명령적 IaC는 언제 어떤 것을 선택하는가?

**질문**: Terraform(선언적)과 Bash(명령적)는 어떤 상황에서 각각이 더 나은 선택인가? 선언적 방식이 항상 우월한가?

**핵심 포인트**

- 선언적 방식은 "최종 상태"만 기술하므로 코드가 짧고 의도가 명확하다 — 하지만 내부 실행 순서를 제어할 수 없다
- 명령적 방식은 순서가 중요한 작업(A를 먼저 만든 후 B를 B의 ID로 연결)에서 직접 제어가 가능하다
- Terraform도 `depends_on`으로 순서를 강제할 수 있지만, 복잡해질수록 코드가 지저분해진다
- 선언적 도구의 drift detection: 현재 인프라 상태가 코드와 달라졌을 때 자동 감지 (`tofu plan`의 핵심 가치)
- 명령적 스크립트는 drift를 감지하지 못한다 — 스크립트를 다시 돌려도 "이미 됐는가"를 직접 확인해야 한다
- 실용적 결론: 인프라 리소스 생성/관리는 선언적(Terraform), 복잡한 커스텀 로직이나 일회성 마이그레이션은 명령적(Bash)

**심화 질문**: Terraform `for_each`와 `count`는 선언적 방식에서 반복을 어떻게 처리하는가? 두 방식의 state 관리 차이는 무엇인가?

---

## Q2. Terraform State는 왜 위험하고 어떻게 안전하게 관리하는가?

**질문**: tfstate 파일이 손상되거나 충돌하면 어떤 일이 생기는가? 팀 환경에서 state를 안전하게 관리하는 전략은 무엇인가?

**핵심 포인트**

- tfstate는 Terraform이 "현재 클라우드 상태"를 추적하는 유일한 기록 — 삭제되면 기존 리소스를 "모른다"고 판단해 재생성 시도
- 두 사람이 동시에 `apply`하면 state 충돌 → 같은 리소스 중복 생성 또는 한쪽 변경 유실
- 해결책 1 — **원격 백엔드**: S3에 state 저장, DynamoDB로 잠금(lock) → 동시 apply 방지
- 해결책 2 — **State 분리**: 환경(dev/staging/prod)별, 컴포넌트(network/compute/data)별로 state 파일 분리 → 한 팀의 실수가 전체에 영향 없음
- `tofu state list` / `tofu state show` / `tofu state mv` — state 직접 조작 명령, 잘못 쓰면 orphan 리소스 발생
- tfstate에는 DB 패스워드 같은 민감 정보가 평문으로 포함될 수 있음 → S3 암호화 + 접근 제어 필수
- Terraform Cloud / Atlantis: state 관리 + PR 기반 plan/apply 워크플로를 제공하는 플랫폼

**심화 질문**: `terraform import`로 기존 리소스를 state에 가져올 때 어떤 위험이 있는가? ClickOps로 만든 리소스를 IaC로 편입하는 절차는?

---

## Q3. Ansible과 Terraform의 역할 경계는 어디인가?

**질문**: 두 도구 모두 "인프라를 코드로 관리"한다고 하는데, 실제 프로젝트에서 어디까지를 Terraform이, 어디서부터를 Ansible이 담당해야 하는가?

**핵심 포인트**

- **Terraform**: 클라우드 API로 리소스 생성 — EC2 인스턴스, RDS, S3 버킷, IAM 역할은 Terraform 영역
- **Ansible**: 서버 OS 수준 관리 — 패키지 설치, 서비스 설정, 파일 배포, 사용자 관리는 Ansible 영역
- 경계가 모호한 영역: EC2 user_data(Terraform) vs Ansible provisioner — user_data는 일회성, Ansible은 반복 적용 가능
- Terraform Ansible provisioner(`local-exec`, `remote-exec`)는 anti-pattern에 가깝다 — state와 연동되지 않아 재실행이 어렵다
- 현실적 패턴: Terraform이 EC2를 만들고 IP를 output으로 내보내면, Ansible이 해당 IP를 inventory로 받아 설정 적용
- Packer와의 관계: Packer+Ansible로 AMI를 굽고, Terraform이 그 AMI ID를 data source로 참조해 EC2 생성

**심화 질문**: Kubernetes 환경에서는 Ansible의 역할이 어떻게 바뀌는가? 컨테이너가 서버 설정 관리를 대체할 수 있는가?

---

## Q4. Packer로 Immutable Infrastructure를 어떻게 구현하는가?

**질문**: Immutable Infrastructure가 무엇이고, Packer AMI 기반 배포가 mutable 서버 방식과 비교해 어떤 운영상 차이를 만드는가?

**핵심 포인트**

- **Mutable**: 서버를 유지하면서 위에 변경을 적용 (Ansible 재실행, apt upgrade) — 서버가 쌓인 변경의 역사를 가짐
- **Immutable**: 변경이 필요하면 새 이미지로 새 서버를 만들고 기존 서버를 버림 — 서버는 항상 "신선한" 상태
- Packer로 새 AMI 빌드 → Terraform으로 새 AMI 사용하는 EC2 교체 → 이것이 immutable 배포 사이클
- 장점: 서버 간 drift 없음, 배포 롤백 = 이전 AMI ID로 되돌리기, 프로덕션과 동일한 이미지를 스테이징에서 테스트
- 단점: AMI 빌드 시간(5~15분)이 배포 시간에 추가, 빌드 파이프라인 필요
- Auto Scaling Group + Launch Template: 새 AMI를 Launch Template에 반영하면 신규 인스턴스는 자동으로 새 AMI 사용
- 컨테이너(Docker)도 동일한 immutable 철학 — Dockerfile이 Packer의 역할을 한다

**심화 질문**: Packer 빌드를 CI 파이프라인에 통합할 때, AMI 빌드 실패를 어떻게 감지하고 롤백 전략을 어떻게 설계하는가?

---

## Q5. IaC 코드는 어떻게 테스트하는가?

**질문**: 일반 소프트웨어는 단위 테스트와 통합 테스트가 있다. IaC 코드를 "테스트"한다는 것은 구체적으로 무엇을 검증하는 것인가?

**핵심 포인트**

- **정적 분석**: `tofu validate` (문법), `tflint` (모범 사례, deprecated 리소스), `checkov` / `tfsec` (보안 정책) — 실제 클라우드 호출 없이 빠르게 실행
- **ansible-lint**: Ansible 플레이북 스타일, 보안, idempotency 위반 검사 — 태스크에 `name` 누락, `become` 남용 등을 잡아냄
- **Terratest** (Go): 실제 클라우드에 인프라를 배포하고, HTTP 응답/포트 접근/IAM 정책을 코드로 검증한 후 자동 삭제 — 진정한 통합 테스트
- Terratest는 실제 리소스를 생성하므로 비용과 시간이 발생 → PR마다 실행하기보다 야간 스케줄이나 릴리즈 전 실행
- **모듈 테스트 전략**: Terraform 모듈을 작게 분리하고 각 모듈마다 `examples/` 디렉토리에 테스트용 설정 — `tofu plan`만으로도 기본 검증 가능
- Kitchen-Terraform, Molecule(Ansible용): Terratest 외 대안 도구들
- 테스트 피라미드를 IaC에 적용하면: 정적 분석(많음, 빠름) → plan 검증(중간) → Terratest 통합 테스트(적음, 느림)

**심화 질문**: Security Group이 의도한 포트만 열려 있는지, IAM 정책이 최소 권한 원칙을 따르는지를 자동으로 검증하는 테스트는 어떻게 작성하는가?

---

## Q6. ClickOps에서 IaC로 전환할 때 마이그레이션 전략은 무엇인가?

**질문**: 이미 콘솔로 만들어진 프로덕션 인프라가 있다. 다운타임 없이 IaC로 전환하려면 어떻게 접근해야 하는가?

**핵심 포인트**

- **terraform import**: 기존 리소스를 state에 가져오는 명령 — 리소스를 삭제/재생성하지 않고 Terraform 관리 하에 편입
- import 절차: (1) 기존 리소스의 현재 설정을 콘솔에서 확인 → (2) 동일한 설정의 `.tf` 파일 작성 → (3) `terraform import` 실행 → (4) `tofu plan`에서 변경 없음(no changes) 확인
- 가장 흔한 실수: import 후 plan에서 예상치 못한 변경이 나오는 것 — 콘솔 기본값과 Terraform provider 기본값이 다를 때 발생
- **단계적 전환 전략**: 새로 만드는 리소스부터 IaC로 시작, 기존 리소스는 우선순위에 따라 점진적으로 import
- **전환 우선순위**: 자주 변경되는 리소스부터 → Security Group 규칙, 태그, IAM 정책처럼 변경이 잦은 것이 IaC 효과가 크다
- `terraformer` / `former2`: 기존 AWS 리소스를 스캔해서 Terraform 코드를 자동 생성하는 도구 — 출발점으로 유용하지만 수동 검토 필수
- 전환 중에는 콘솔 변경 금지 정책을 팀에 공지 — IaC와 콘솔이 동시에 인프라를 관리하면 drift가 빠르게 누적

**심화 질문**: 마이그레이션 중 `terraform import`가 실패하거나 state가 손상됐을 때 복구 절차는 무엇인가? state 백업 전략을 어떻게 설계해야 하는가?
