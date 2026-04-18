# Ch04. 구조적 CI/CD 패턴 — 탐구 질문

> 이 문서는 LEARN.md를 읽은 뒤 더 깊이 파고들 질문들을 담는다.
> 각 질문은 단순 복습이 아닌, 실제 설계 결정에서 맞닥뜨리는 트레이드오프를 다룬다.

---

## Q1. Monorepo vs Polyrepo 의사결정 기준

**질문**: 팀이 Monorepo로 전환하거나 Polyrepo를 유지해야 하는 구체적인 신호는 무엇인가?

**탐구 방향**:
- Polyrepo 유지 신호: 서비스 간 배포 주기가 완전히 독립적, 팀 간 기술 스택이 다름(Java vs Go), 각 서비스의 Git 히스토리가 수백만 커밋 규모
- Monorepo 전환 신호: "공유 라이브러리를 업데이트하면 모든 서비스 PR을 열어야 한다", 의존성 버전 불일치로 인한 런타임 오류 반복, 코드 리뷰가 여러 저장소를 오가며 맥락이 단절됨
- Git 성능 한계: Monorepo가 수십만 파일을 넘어가면 `git status`조차 느려짐 → `git sparse-checkout`이나 Virtual File System(VFS for Git)이 필요해지는 임계점은 어디인가?
- 하이브리드: 핵심 공유 라이브러리만 Monorepo, 서비스는 Polyrepo로 유지하는 구조의 장단점은?

**검증 실험**: 실제 팀에서 Polyrepo → Monorepo 전환 사례(Google, Meta)에서 전환 비용과 이후 효과를 정량적으로 측정한 자료를 찾아볼 것

**후속 질문**: Monorepo 전환 후 기존 Polyrepo 저장소 히스토리를 `git filter-repo`로 병합하는 과정에서 커밋 저자 정보와 태그가 유실되는 문제를 어떻게 방지하는가?

**심화 참고**: Nx 공식 문서 "Integrated Monorepo vs Package-Based" 비교 및 Microsoft의 "Scalar" Git 가상화 프로젝트 사례

---

## Q2. Nx affected 빌드의 내부 동작 원리

**질문**: `nx affected`는 어떻게 "이 파일이 변경되면 저 서비스에 영향을 준다"고 판단하는가?

**탐구 방향**:
- 프로젝트 그래프 생성: Nx는 `project.json`의 `implicitDependencies`와 실제 `import` 구문을 분석하여 유향 의존성 그래프(DAG)를 구성함
- 변경 감지: `git diff --name-only {base}...{head}`로 변경 파일 목록 추출 → 각 파일이 속하는 Nx 프로젝트 판별
- 역방향 탐색: 변경된 프로젝트를 루트로, 그래프를 역방향(consumers 방향)으로 BFS/DFS 탐색하여 영향받는 프로젝트 목록 생성
- `namedInputs`의 역할: `production` 입력에서 테스트 파일을 제외하면, 테스트 파일만 변경되어도 빌드 캐시가 무효화되지 않음 — 어떤 파일이 어떤 target의 캐시 키에 포함되는지 제어하는 메커니즘
- 함정: `tsconfig.json`이나 `package.json`이 변경되면 모든 프로젝트가 affected로 마킹됨 → `sharedGlobals`와 `ignoredFiles` 설정으로 범위를 좁히는 전략은?

**검증 실험**: `nx graph` 명령으로 프로젝트 그래프를 시각화하고, 특정 파일을 변경했을 때 `nx show projects --affected`로 어떤 프로젝트가 포함되는지 예측과 비교할 것

**후속 질문**: Nx Cloud의 분산 캐시는 CI 러너가 여러 머신에 분산되어 있을 때도 동일한 task 결과를 공유하는가? 캐시 키 충돌(다른 환경에서 동일 해시 생성)이 발생할 수 있는 조건은 무엇인가?

**심화 참고**: Nx 공식 문서 "How Caching Works" — task hash 계산 방식과 `inputs`/`outputs` 설정이 캐시 적중률에 미치는 영향 분석

---

## Q3. Reusable Workflow의 한계와 대안

**질문**: GitHub Actions Reusable Workflow가 해결하지 못하는 상황은 무엇이며, 그때 어떤 대안을 선택해야 하는가?

**탐구 방향**:
- 한계 1 — 중첩 불가: Reusable Workflow를 호출하는 워크플로우는 다른 Reusable Workflow를 호출할 수 없음(1단계 중첩만 허용, 2024년 기준 최대 4단계로 완화). 복잡한 파이프라인 트리가 필요하면 Composite Actions가 대안
- 한계 2 — secrets 전달: 호출자가 명시적으로 `secrets: inherit` 또는 개별 secret을 전달해야 함. 피호출자가 "알아서 읽기"는 불가 → secret 관리 복잡도 증가
- 한계 3 — 조건부 실행: 피호출 워크플로우 내부에서 `if:` 조건이 호출자의 컨텍스트를 참조하기 어려움
- Composite Actions vs Reusable Workflow: 전자는 step 수준 재사용(job 분리 없음), 후자는 job 수준 재사용(별도 러너). 언제 어떤 것을 선택할 것인가?
- 대안 — Action as Code: 모든 로직을 Docker Action이나 JavaScript Action으로 구현하면 any CI 도구에서 재사용 가능. 하지만 관리 오버헤드 증가

**검증 실험**: 동일한 빌드 로직을 Reusable Workflow, Composite Action, 쉘 스크립트 세 가지로 구현하고 각각의 디버깅 경험과 재사용성을 비교할 것

**후속 질문**: Reusable Workflow를 다른 조직의 저장소에서 호출(`uses: other-org/workflows/.github/workflows/build.yml@main`)할 때 보안 검토 항목은 무엇인가? 서드파티 워크플로우가 secrets를 탈취하는 공격 벡터는 어떻게 차단하는가?

---

## Q4. 파이프라인 RBAC 설계 원칙

**질문**: 파이프라인 RBAC를 설계할 때 권한을 너무 세분화하면 오히려 역효과가 나는 이유는 무엇이며, 적절한 세분화 수준을 어떻게 결정하는가?

**탐구 방향**:
- 최소 권한 원칙(Principle of Least Privilege)을 파이프라인에 적용: 개발자는 dev 배포만, SRE는 prod 배포까지 — 이 경계를 어떻게 코드로 강제하는가?
- GitHub Environments의 Required Reviewers: 승인자 그룹을 코드가 아닌 UI로 설정하면 감사 추적이 어려워짐. 승인 설정도 Terraform으로 코드화하는 방법은?
- 긴급 배포(Break Glass): 정상 승인 프로세스를 우회해야 하는 인시던트 상황에서 어떤 예외 경로를 마련하고, 그 사용을 어떻게 감사하는가?
- 역할 폭발(Role Explosion) 안티패턴: 역할이 너무 세분화되면 "누가 무엇을 할 수 있는가"를 파악하기 어려워짐 → 역할 수를 최소화하면서도 필요한 격리를 달성하는 설계 원칙은?
- RBAC vs ABAC: 역할 기반이 아닌 속성 기반(배포 시간대, 변경 크기, 위험 점수)으로 동적 승인 요구 수준을 결정하는 패턴

**검증 실험**: 실제 인시던트 사례에서 파이프라인 권한 설정이 복구 시간에 미친 영향(너무 엄격해서 지연 vs 너무 느슨해서 실수)을 분석할 것

**후속 질문**: GitHub Environment의 Required Reviewers 설정을 Terraform(`github_repository_environment` 리소스)으로 관리할 때, 리뷰어 팀 멤버십이 변경되면 IaC 상태 드리프트가 발생한다. 이 드리프트를 감지하고 수정하는 워크플로우를 어떻게 설계하는가?

---

## Q5. Adapter 패턴으로 CI 도구 교체 비용 최소화

**질문**: 빌드 로직을 쉘 스크립트로 추상화할 때 생기는 새로운 문제(스크립트 테스트, 크로스 플랫폼 호환성)를 어떻게 관리하는가?

**탐구 방향**:
- 스크립트 테스트: 쉘 스크립트 자체를 테스트하는 도구(bats-core, shellspec)를 사용하면 스크립트 품질을 보장할 수 있음. CI 도구 의존성 제거와 스크립트 복잡도 증가 사이의 균형
- 크로스 플랫폼 함정: macOS의 `sed -i`와 Linux의 `sed -i`는 동작이 다름. `#!/usr/bin/env bash`와 `set -euo pipefail`만으로 해결되지 않는 플랫폼 차이는?
- 대안 — Taskfile vs Makefile: Taskfile은 YAML 기반으로 가독성이 높지만 별도 바이너리 설치 필요. Makefile은 어디서나 동작하지만 문법이 직관적이지 않음. 팀 규모와 도구 표준화 수준에 따른 선택 기준은?
- 컨테이너화된 빌드: 모든 빌드 도구를 Docker 이미지에 패키징하면 `docker run myorg/build-tools:1.0 ./scripts/build.sh` 형태로 완전한 재현성을 보장. 하지만 이미지 관리 오버헤드 발생
- 추상화 수준 결정: 어디까지 추상화할 것인가? 파일 하나당 스크립트 하나 vs 전체 파이프라인을 하나의 CLI 도구로 패키징하는 것의 트레이드오프

**검증 실험**: 현재 GitHub Actions 워크플로우에서 CI 도구 전용 구문(`${{ github.sha }}` 등)을 제거하고 환경변수로 추상화한 뒤, 동일한 스크립트를 GitLab CI에서 실행해볼 것

**후속 질문**: 빌드 스크립트가 복잡해져서 Bash 대신 Go나 Python으로 재작성할 시점의 기준은 무엇인가? Dagger.io처럼 파이프라인 로직 자체를 타입이 있는 언어로 작성하는 접근의 트레이드오프는?

---

## Q6. Monorepo에서 팀 간 빌드 격리

**질문**: Monorepo에서 A팀의 코드 변경이 B팀의 CI를 깨뜨리는 상황을 어떻게 구조적으로 방지하는가?

**탐구 방향**:
- Nx Project Boundaries(태그 기반): `project.json`에 태그를 붙이고 `.eslintrc.json`의 `@nx/enforce-module-boundaries` 규칙으로 허용되지 않은 cross-team import를 빌드 시점에 차단
- CODEOWNERS 파일: `.github/CODEOWNERS`로 디렉토리별 필수 리뷰어를 지정하면, A팀이 B팀 코드를 변경할 때 B팀의 승인이 강제됨
- 공유 라이브러리 변경 프로토콜: 공유 lib 변경은 모든 consumers를 affected 빌드로 검증한 뒤에만 머지 허용. 이 검증을 자동화하는 GitHub Actions 조건은?
- Ownership 메타데이터: `project.json`에 `owner` 필드를 추가하고, affected 빌드 시 해당 팀에게만 Slack 알림을 보내는 파이프라인 설계
- 격리 실패 신호: 특정 팀의 CI가 자신들이 변경하지 않은 코드 때문에 자주 실패하면, 의존성 그래프가 지나치게 결합되어 있다는 신호 — 어떤 메트릭으로 결합도를 측정하는가?

**검증 실험**: `nx graph`로 프로젝트 간 의존성 그래프를 시각화하고, 팀 경계를 넘는 의존성(cross-team edges)의 수를 주기적으로 측정하여 결합도 트렌드를 추적할 것

**후속 질문**: Monorepo에서 팀 A가 팀 B의 라이브러리를 사용하다가 인터페이스 변경을 요청할 때, 변경 제안 → 리뷰 → 마이그레이션을 구조화하는 RFC(Request for Comments) 프로세스를 파이프라인과 어떻게 연동하는가? 예를 들어 deprecation 경고를 CI 린트 단계에서 자동으로 감지하는 방법은?

**심화 참고**: Nx `@nx/enforce-module-boundaries` 규칙의 `allowedExternalImports`와 `bannedExternalImports` 옵션으로 팀 간 의존성 허용 목록을 선언적으로 관리하는 패턴
