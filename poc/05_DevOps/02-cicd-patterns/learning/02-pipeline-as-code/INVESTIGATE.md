# Ch02. INVESTIGATE — Pipeline as Code와 실행 모델

탐구 질문에 스스로 답하며 이해를 검증한다. 답변은 자유 형식으로 작성하되, 핵심 판단 근거를 포함할 것.

---

## Q1. Declarative vs Scripted Pipeline 트레이드오프

**질문**: Declarative 모델이 Scripted보다 항상 나은가? 어떤 상황에서 Scripted를 선택해야 하는가?

<답변 공간>

힌트: 동적 스테이지 생성, 외부 시스템에서 설정을 읽는 경우, Groovy 함수 재사용을 고려해보자.
Declarative는 구조가 강제되기 때문에 유효성 검사가 쉽지만, `script {}` 블록 없이는 루프나 복잡한 조건을 표현하기 어렵다.
Scripted는 Groovy의 전체 표현력을 활용할 수 있어 "이번 빌드에서 변경된 서비스만 테스트" 같은 동적 파이프라인이 가능하지만, 샌드박스 제한(Jenkins 스크립트 승인)과 디버깅 복잡성을 감수해야 한다.

판단 기준:
- 정적이고 예측 가능한 파이프라인 → Declarative
- 동적 파이프라인 (외부 매니페스트, 변경 파일 기반 선택적 실행) → Scripted 또는 Hybrid

</답변 공간>

---

## Q2. GitHub Actions vs GitLab CI 선택 기준

**질문**: 새 프로젝트를 시작할 때 두 도구 중 하나를 선택해야 한다면 어떤 기준으로 결정하는가?

<답변 공간>

힌트: 저장소 위치(GitHub/GitLab), 보안 정책(self-hosted 요구), 팀의 기존 경험, 레지스트리/이슈 트래커 통합 수준을 고려하자.

GitHub Actions의 강점: Marketplace의 방대한 Actions 생태계, OIDC로 클라우드 인증, PR 리뷰와 워크플로의 자연스러운 통합.
GitLab CI의 강점: GitLab 자체 Container Registry, Environments UI(배포 이력/롤백), Security Scanning(SAST/DAST)이 플랫폼에 내장. Self-managed 인스턴스에서 완전한 제어.

결정 트리: GitLab에 저장소가 있다면 GitLab CI가 자연스러운 선택이다. GitHub 저장소라면 GitHub Actions. 양쪽을 모두 사용하는 조직이라면 파이프라인 정의 언어(YAML 형식)가 달라 포팅 비용이 발생한다 — 이것이 두 플랫폼을 혼용할 때의 실질적인 비용이다.

</답변 공간>

---

## Q3. Pipeline 코드의 테스트 가능성 확보

**질문**: 파이프라인 코드가 "테스트 가능하다"는 것은 구체적으로 무엇을 의미하는가? 어떤 도구로 검증하는가?

<답변 공간>

힌트: `act` (GitHub Actions 로컬 실행), `gitlab-ci-local` (GitLab CI 로컬 실행), YAML 스키마 검증, 파이프라인 린트를 각각 어느 시점에 사용하는지 정리해보자.

세 수준의 검증:
1. **문법 검증**: GitHub Actions는 `.github/workflows/` YAML을 JSON Schema로 검증 (VS Code 플러그인 또는 `yamllint`). GitLab은 `gitlab-ci lint` API 엔드포인트.
2. **로컬 실행**: `act`로 GitHub Actions를 Docker에서 로컬 실행 (실제 Actions runner 환경과 100% 동일하지 않지만 빠른 피드백). `gitlab-ci-local`로 GitLab CI job 로컬 실행.
3. **통합 검증**: 브랜치에서 실제 CI 실행 후 결과 확인.

파이프라인 테스트의 한계: 외부 서비스(AWS, Kubernetes 클러스터) 의존 단계는 로컬 테스트가 어렵다. 이 경우 mock 환경(localstack for AWS, kind for K8s)을 사용하거나, 해당 단계만 실제 CI에서 검증한다.

</답변 공간>

---

## Q4. DAG 기반 실행 모델의 이점

**질문**: 모든 파이프라인을 병렬로 실행하면 되지 않는가? DAG가 필요한 이유는 무엇인가?

<답변 공간>

힌트: 빌드 결과물이 테스트의 입력이 되는 경우, 스테이징 배포 전에 반드시 이미지 빌드가 완료되어야 하는 경우를 떠올려보자.

DAG는 "의존성이 있는 것은 순서를 강제하고, 의존성이 없는 것은 병렬로 실행"하는 모델이다. 완전한 병렬 실행이 불가능한 이유는 데이터 흐름 때문이다. 테스트는 빌드 결과물을 입력으로 받고, 배포는 테스트를 통과한 이미지를 입력으로 받는다. 이 의존 관계를 무시하고 병렬 실행하면 "빌드가 완료되기 전에 배포가 시작되는" 레이스 컨디션이 발생한다.

DAG의 실질적 이점: 크리티컬 패스를 명확히 드러낸다. "전체 파이프라인이 30분 걸리는데 어디서 시간을 줄일 수 있나?" → DAG에서 크리티컬 패스의 각 노드를 최적화하면 전체 시간이 줄고, 비크리티컬 경로는 최적화해도 전체 시간에 영향 없음을 즉시 알 수 있다.

</답변 공간>

---

## Q5. Argo CD ApplicationSet의 Generator 패턴

**질문**: LEARN.md에서 List Generator를 사용했다. 언제 다른 Generator(Cluster, Git, Matrix)를 선택해야 하는가?

<답변 공간>

힌트: 클러스터가 동적으로 추가/삭제되는 경우, 디렉토리 구조에서 환경을 발견하는 경우, 두 Generator를 조합하는 경우를 구분해보자.

Generator 선택 기준:
- **List Generator**: 환경 목록이 고정적이고 적을 때 (dev/staging/prod). 가장 단순하고 명시적.
- **Cluster Generator**: Argo CD에 등록된 클러스터 목록을 자동으로 읽어 Application 생성. 클러스터가 자주 추가/삭제되는 멀티테넌트 환경에 적합.
- **Git Generator**: Git 저장소의 특정 경로 아래 디렉토리를 스캔해 Application 생성. "새 서비스 디렉토리를 추가하면 자동으로 배포" 패턴 구현 가능.
- **Matrix Generator**: 두 Generator를 조합. 예: 모든 클러스터 × 모든 앱 = 전체 배포 매트릭스.

실무에서는 List가 가장 많이 쓰인다. 과도한 자동화(Git Generator + 자동 동기화)는 실수로 추가된 디렉토리가 배포되는 위험이 있어, 프로덕션 환경에서는 신중해야 한다.

</답변 공간>

---

## Q6. Pipeline as Code의 보안 고려사항

**질문**: 파이프라인 코드가 공개 저장소에 있을 때 시크릿 노출 위험을 어떻게 방지하는가? OIDC가 장기 시크릿보다 나은 이유는 무엇인가?

<답변 공간>

힌트: `secrets.MY_KEY` vs 하드코딩, OIDC 토큰의 수명(단기), AWS STS와 OIDC의 관계, fork PR에서 시크릿 접근 제한을 생각해보자.

시크릿 노출의 세 가지 위험:
1. **하드코딩**: 파이프라인 파일에 API 키를 직접 작성. git history에 영원히 남음.
2. **로그 출력**: `echo $SECRET`으로 시크릿을 로그에 출력. GitHub Actions는 등록된 시크릿을 자동으로 마스킹하지만, 인코딩(base64 등)하면 우회 가능.
3. **Fork PR 공격**: 외부 기여자의 fork에서 PR을 보낼 때 시크릿에 접근할 수 있으면 탈취 가능. GitHub Actions는 fork PR에서 시크릿을 기본 차단.

OIDC가 장기 시크릿보다 안전한 이유: OIDC 토큰은 **요청 시점에 생성되는 단기 자격증명**이다. AWS에 등록된 OIDC 공급자 설정을 통해 GitHub Actions가 발급한 ID 토큰을 AWS STS가 검증하고, 설정된 IAM 역할의 임시 자격증명(15분~1시간)을 발급한다. 장기 Access Key가 저장소에 존재하지 않으므로, 저장소가 탈취되어도 클라우드 자격증명은 안전하다. 또한 OIDC 클레임(`repository`, `ref`, `environment`)으로 어떤 저장소의 어떤 브랜치/환경에서만 역할을 수임할 수 있는지 세밀하게 제한할 수 있다.

실천 원칙: 파이프라인 파일은 공개 저장소에서도 안전하게 공유할 수 있어야 한다. 시크릿은 CI 플랫폼의 비밀 저장소(GitHub Secrets, GitLab Variables)나 외부 Vault에 보관하고, 파이프라인은 참조 이름만 사용한다.

</답변 공간>

---

## 참고

- [GitHub Actions: OIDC로 클라우드 인증](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitLab CI: rules 문법](https://docs.gitlab.com/ee/ci/yaml/#rules)
- [Argo CD: ApplicationSet 컨트롤러](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/)
- [act: GitHub Actions 로컬 실행](https://github.com/nektos/act)
- Ch01 ← Ch02 → Ch03 (테스트 자동화 패턴)
- Jenkins 상세: `05_DevOps/01-jenkins/learning/03-pipeline/LEARN.md`
