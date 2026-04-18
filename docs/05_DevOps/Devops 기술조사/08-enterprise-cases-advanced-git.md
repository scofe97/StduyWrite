# 기업 Git 태그 활용 사례 및 CI/CD Git 심화 기술

> **목적**: DevOps Workflow 제품 개발을 위한 실무 사례 학습 및 CI/CD Git 심화 기술 이해
> **작성일**: 2024-12-28

---

## 목차

### Part 1: 기업 기술 블로그 Git 태그 활용 사례
1. [메쉬코리아 (부릉) - Jenkins + ArgoCD](#1-메쉬코리아-부릉---jenkins--argocd)
2. [우아한형제들 (배달의민족) - Git Flow](#2-우아한형제들-배달의민족---git-flow)
3. [뱅크샐러드 - Trunk-Based Development](#3-뱅크샐러드---trunk-based-development)
4. [당근페이 - 승인 기반 배포](#4-당근페이---승인-기반-배포)
5. [SK Devocean - GitHub Actions 자동화](#5-sk-devocean---github-actions-자동화)
6. [PRND (헤이딜러) - Release 자동화](#6-prnd-헤이딜러---release-자동화)

### Part 2: CI/CD에서 활용하는 Git 심화 기술
7. [Git Hooks](#7-git-hooks)
8. [Git Submodules](#8-git-submodules)
9. [Git LFS (Large File Storage)](#9-git-lfs-large-file-storage)
10. [Git Bisect](#10-git-bisect)
11. [Shallow Clone & Sparse Checkout](#11-shallow-clone--sparse-checkout)
12. [Git Worktree](#12-git-worktree)
13. [Signed Commits (GPG)](#13-signed-commits-gpg)
14. [Conventional Commits & Semantic Release](#14-conventional-commits--semantic-release)
15. [Git Attributes](#15-git-attributes)
16. [GitHub/GitLab Webhooks 심화](#16-githubgitlab-webhooks-심화)

### Part 3: 종합 정리
17. [CI/CD Git 기술 체크리스트](#17-cicd-git-기술-체크리스트)

---

# Part 1: 기업 기술 블로그 Git 태그 활용 사례

## 1. 메쉬코리아 (부릉) - Jenkins + ArgoCD

### 배경

메쉬코리아는 Kubernetes 환경에서 MSA를 운영하며, 기존 Bamboo + Spinnaker에서 Jenkins + ArgoCD로 CI/CD 도구를 전환했습니다.

### 태그 활용 방식

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Git Tag    │────▶│  Jenkins    │────▶│    ECR      │
│   Push      │     │  CI Build   │     │  (Docker)   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  K8s 배포   │◀────│  Argo CD    │◀────│ Helm Values │
│             │     │  (GitOps)   │     │  업데이트   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 핵심 포인트

**Git Tag Push 기반 CI 자동화**

```bash
# 개발자가 태그 푸시
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3

# Jenkins가 태그 이벤트 감지 → 빌드 시작
```

**버전 네이밍 컨벤션 통합**

```
v{major}.{minor}.{patch}[-{prerelease}]

예시:
- v1.0.0        → Production 배포
- v1.0.0-rc.1   → Staging 배포
- v1.0.0-dev.1  → Dev 배포
```

**Helm Values 자동 업데이트**

```yaml
# helm-values/production/values.yaml
image:
  repository: ecr.aws/myapp
  tag: v1.2.3  # Jenkins가 자동으로 업데이트
```

### 환경별 배포 전략

| 환경 | Auto Sync | 배포 트리거 |
|------|-----------|------------|
| Dev | ✅ 활성화 | 태그 푸시 즉시 |
| QA | ✅ 활성화 | 태그 푸시 즉시 |
| Production | ❌ 비활성화 | 수동 Sync 버튼 |

### 학습 포인트

1. **태그 컨벤션**: 팀 전체가 동일한 버전 네이밍 규칙 사용
2. **GitOps 분리**: 애플리케이션 코드와 배포 매니페스트 저장소 분리
3. **환경별 제어**: Production은 수동 승인으로 안전성 확보

---

## 2. 우아한형제들 (배달의민족) - Git Flow

### 배경

배달의민족 안드로이드 팀은 2017년 GitHub Flow에서 Git Flow로 브랜치 전략을 전환했습니다.

### Repository 구조

```
┌─────────────────────────────────────────────────────┐
│                 Upstream Repository                  │
│            (github.com/org/project)                 │
└─────────────────────────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│    Origin     │ │    Origin     │ │    Origin     │
│  (Developer A)│ │  (Developer B)│ │  (Developer C)│
└───────────────┘ └───────────────┘ └───────────────┘
            │             │             │
            ▼             ▼             ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│     Local     │ │     Local     │ │     Local     │
│  Repository   │ │  Repository   │ │  Repository   │
└───────────────┘ └───────────────┘ └───────────────┘
```

### Git Flow 워크플로우

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  master ──●────────────────────●────────────────●──▶          │
│           │                    ↑                ↑              │
│           │                    │ (merge)        │ (merge)      │
│           │                    │                │              │
│  release  │            ●───────●                │              │
│           │            ↑       │                │              │
│           │            │       │ (bugfix)       │              │
│           │            │       ▼                │              │
│  develop ─●────●───────●───────●────────────────●──▶          │
│                ↑       ↑                        ↑              │
│                │       │                        │              │
│  feature       ●───────●                        │              │
│                        │                        │              │
│  hotfix                                    ●────●              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 태그 생성 시점

```bash
# QA 완료 후 master 머지 시 태그 생성
git checkout master
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin master --tags

# develop에도 머지 (동기화)
git checkout develop
git merge release/v1.2.0
git push origin develop
```

### 실제 명령어 흐름

```bash
# 1. Feature 브랜치 생성
git checkout develop
git checkout -b feature/user-profile

# 2. 작업 완료 후 develop 머지
git checkout develop
git merge --no-ff feature/user-profile
git push origin develop

# 3. Release 브랜치 생성 (QA 시작)
git checkout -b release/v1.2.0 develop
git push origin release/v1.2.0

# 4. QA 중 버그 수정
git checkout release/v1.2.0
# 버그 수정 작업
git commit -m "fix: resolve login issue"
git push origin release/v1.2.0

# 5. QA 완료 → master 머지 + 태그
git checkout master
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin master --tags

# 6. develop 동기화
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop

# 7. release 브랜치 삭제
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### 학습 포인트

1. **--no-ff 옵션**: 항상 머지 커밋 생성으로 기능 단위 추적
2. **태그 시점**: master 머지 직후 즉시 태그 생성
3. **브랜치 정리**: release 브랜치는 머지 후 삭제

---

## 3. 뱅크샐러드 - Trunk-Based Development

### 배경

뱅크샐러드는 "하루 1000번 배포하는 조직"을 목표로 배포 프로세스를 혁신했습니다.

### 기존 문제점

```
[기존 Git Flow의 문제]

1. 브랜치 복잡성
   - feature, develop, release, hotfix, master 관리 부담
   
2. 배포 주기 길어짐
   - release 브랜치 생성 → QA → 머지까지 시간 소요
   
3. 충돌 증가
   - 장기간 분리된 브랜치는 머지 시 충돌 빈발
```

### Trunk-Based Development 전환

```
[Before: Git Flow]
master ──────────────────────────────────────
         \                    /
develop   ●───●───●───●───●──●
               \     /
feature         ●───●

[After: Trunk-Based]
master ──●───●───●───●───●───●───●───●───●──▶
          ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
          │   │   │   │   │   │   │   │
         PR  PR  PR  PR  PR  PR  PR  PR
```

### 핵심 원칙

```bash
# 1. 모든 작업은 master에서 분기
git checkout master
git checkout -b fix/login-bug

# 2. 짧은 수명의 브랜치 (1-2일 이내)
# 작업 완료
git push origin fix/login-bug

# 3. PR 생성 → 코드 리뷰 → master 머지
# GitHub UI에서 PR 생성
# 최소 1명의 서비스 오너 승인 필요

# 4. 머지 즉시 배포
# master 머지 → CI/CD 자동 트리거 → 배포
```

### 태그 활용 방식

```bash
# Trunk-Based에서는 태그보다 커밋 해시 활용
# 하지만 주요 릴리즈에는 태그 사용

# 예: 주간 릴리즈 마킹
git tag -a release-2024-w52 -m "Weekly release"
git push origin release-2024-w52
```

### Cross Teams, Cross Repositories

```
개발자 A (팀 X)
    │
    ├── Repository A (팀 X 소유) ─ 직접 수정
    ├── Repository B (팀 Y 소유) ─ PR로 기여
    └── Repository C (팀 Z 소유) ─ PR로 기여

→ 팀 경계를 넘어 코드 기여 가능
→ 코드 오너의 리뷰 필수
```

### 학습 포인트

1. **단일 브랜치**: master만 유지, 복잡성 최소화
2. **짧은 PR 주기**: 1-2일 내 머지로 충돌 최소화
3. **자동화 의존**: 테스트 자동화가 필수
4. **태그 최소화**: 커밋 단위 배포로 태그 필요성 감소

---

## 4. 당근페이 - 승인 기반 배포

### 배경

금융 서비스 특성상 자유로운 배포가 불가능하며, 배포 전 승인자의 별도 승인이 필요합니다.

### Git Flow 선택 이유

```
[당근페이가 Git Flow를 선택한 이유]

1. 운영/개발 환경 분리
   - Production 브랜치와 Develop 브랜치 명확히 분리
   
2. Stable 브랜치 관리
   - 언제든 배포 가능한 안정적인 main 브랜치 유지
   
3. 장애 대응
   - main 기준으로 빠른 hotfix 가능
   
4. 팀 친숙도
   - 모두에게 익숙한 브랜치 전략
```

### 정기 배포 프로세스

```
월  화  [수: 정기 배포]  목  금

┌─────────────────────────────────────────────┐
│              수요일 배포 프로세스              │
├─────────────────────────────────────────────┤
│ 1. develop → release 브랜치 생성             │
│ 2. QA 진행                                  │
│ 3. 배포 승인자 리뷰                          │
│ 4. 승인 후 main 머지                         │
│ 5. 태그 생성 (v1.2.0)                       │
│ 6. Production 배포                          │
│ 7. 모니터링                                 │
└─────────────────────────────────────────────┘
```

### 태그 + 승인 워크플로우

```bash
# 1. Release 준비
git checkout -b release/v1.2.0 develop

# 2. 승인 요청 (Slack/Jira 등)
# "[배포 승인 요청] v1.2.0 - 변경사항: ..."

# 3. 승인 완료 후 태그 생성
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Approved release v1.2.0"
git push origin main --tags

# 4. 태그 기반 배포 트리거
# v*.*.* 태그 → Production 배포 파이프라인 실행
```

### 학습 포인트

1. **규제 환경 대응**: 금융/의료 등 승인이 필수인 도메인
2. **정기 배포 주기**: 배포 일정을 고정하여 리소스 집중
3. **태그 = 승인 기록**: 태그에 승인 정보 포함

---

## 5. SK Devocean - GitHub Actions 자동화

### Conventional Commits 기반 자동 태그

```
[Conventional Commits 규칙]

feat:     새로운 기능 → Minor 버전 업 (1.0.0 → 1.1.0)
fix:      버그 수정 → Patch 버전 업 (1.0.0 → 1.0.1)
docs:     문서 수정 → 버전 변경 없음
style:    코드 포맷팅 → 버전 변경 없음
refactor: 리팩토링 → 버전 변경 없음
test:     테스트 추가 → 버전 변경 없음
chore:    빌드/설정 변경 → 버전 변경 없음

BREAKING CHANGE: → Major 버전 업 (1.0.0 → 2.0.0)
```

### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Auto Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Semantic Release
        uses: cycjimmy/semantic-release-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 커밋 → 태그 자동 생성 흐름

```
커밋 메시지                          생성되는 태그
─────────────────────────────────────────────────
feat: add user authentication    →  v1.1.0
fix: resolve login bug           →  v1.1.1
feat: add payment module         →  v1.2.0
fix: fix payment validation      →  v1.2.1
feat!: redesign API (BREAKING)   →  v2.0.0
```

### 자동 생성되는 Release Notes

```markdown
## [1.2.0] - 2024-12-28

### Features
- add user authentication (#123)
- add payment module (#125)

### Bug Fixes
- resolve login bug (#124)
- fix payment validation (#126)

### Contributors
- @developer-a
- @developer-b
```

### 학습 포인트

1. **커밋 메시지 규칙화**: Conventional Commits로 자동화 기반 마련
2. **Semantic Release**: 버전 자동 결정 및 태그 생성
3. **Release Notes 자동화**: 수동 문서 작업 제거

---

## 6. PRND (헤이딜러) - Release 자동화

### 기존 수동 프로세스

```
[Before: 수동 태그 생성]
1. release 브랜치 → main 머지
2. GitHub UI에서 Release 페이지 이동
3. 수동으로 태그 이름 입력
4. Release Notes 작성
5. Publish Release 클릭

→ 매 배포마다 5-10분 소요
→ 실수 가능성 존재
```

### 자동화된 프로세스

```yaml
# .github/workflows/auto-release.yml
name: Auto Create Release

on:
  pull_request:
    types: [closed]
    branches:
      - main
      - master

jobs:
  create-release:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract version from branch name
        id: version
        run: |
          BRANCH_NAME="${{ github.event.pull_request.head.ref }}"
          VERSION=$(echo $BRANCH_NAME | grep -oP 'release/\K[\d.]+')
          echo "version=$VERSION" >> $GITHUB_OUTPUT
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ steps.version.outputs.version }}
          release_name: Release v${{ steps.version.outputs.version }}
          body: |
            ## Changes
            ${{ github.event.pull_request.body }}
          draft: false
          prerelease: false
```

### 워크플로우 상세

```
1. release/1.2.0 브랜치 생성
       │
       ▼
2. PR 생성: release/1.2.0 → main
       │
       ▼
3. PR 본문에 변경사항 작성
       │
       ▼
4. 코드 리뷰 & 승인
       │
       ▼
5. PR 머지 (Merge)
       │
       ▼
6. GitHub Actions 자동 실행
   - 브랜치명에서 버전 추출 (1.2.0)
   - 태그 생성 (v1.2.0)
   - Release 생성
   - Release Notes = PR 본문
```

### 학습 포인트

1. **브랜치명 컨벤션**: `release/x.x.x` 형식으로 버전 정보 포함
2. **PR 본문 활용**: Release Notes를 PR 본문으로 대체
3. **트리거 조건**: PR 머지 시에만 실행

---

# Part 2: CI/CD에서 활용하는 Git 심화 기술

## 7. Git Hooks

### 개념

Git Hooks는 특정 Git 이벤트 발생 시 자동으로 실행되는 스크립트입니다.

```
.git/hooks/
├── pre-commit        # 커밋 전 실행
├── prepare-commit-msg # 커밋 메시지 편집 전
├── commit-msg        # 커밋 메시지 검증
├── post-commit       # 커밋 후 실행
├── pre-push          # 푸시 전 실행
├── pre-receive       # 서버: 푸시 받기 전
├── post-receive      # 서버: 푸시 받은 후
├── update            # 서버: 브랜치별 업데이트 전
└── post-update       # 서버: 업데이트 후
```

### 클라이언트 훅 vs 서버 훅

| 구분 | 클라이언트 훅 | 서버 훅 |
|------|-------------|--------|
| 실행 위치 | 로컬 개발 환경 | Git 서버 (GitHub, GitLab) |
| 용도 | 린트, 테스트, 포맷팅 | 정책 강제, 배포 트리거 |
| 우회 가능 | `--no-verify`로 스킵 가능 | 우회 불가 |
| 예시 | pre-commit, pre-push | pre-receive, post-receive |

### pre-commit 훅 예시

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit hooks..."

# 1. ESLint 실행
echo "Running ESLint..."
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ ESLint failed. Please fix errors before committing."
    exit 1
fi

# 2. 테스트 실행
echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix before committing."
    exit 1
fi

# 3. 민감 정보 체크
echo "Checking for secrets..."
if git diff --cached --name-only | xargs grep -l "API_KEY\|SECRET\|PASSWORD" 2>/dev/null; then
    echo "❌ Potential secrets detected!"
    exit 1
fi

echo "✅ All pre-commit checks passed!"
exit 0
```

### commit-msg 훅 (Conventional Commits 강제)

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Conventional Commits 패턴 검증
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Expected format: <type>(<scope>): <subject>"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo ""
    echo "Example: feat(auth): add login functionality"
    exit 1
fi

echo "✅ Commit message format is valid"
exit 0
```

### pre-push 훅 (브랜치 보호)

```bash
#!/bin/sh
# .git/hooks/pre-push

protected_branches="main master production"
current_branch=$(git rev-parse --abbrev-ref HEAD)

for branch in $protected_branches; do
    if [ "$current_branch" = "$branch" ]; then
        echo "❌ Direct push to $branch is not allowed!"
        echo "Please create a PR instead."
        exit 1
    fi
done

exit 0
```

### Husky를 활용한 Hook 관리

```bash
# Husky 설치
npm install husky --save-dev
npx husky init

# pre-commit 훅 설정
echo "npm run lint && npm test" > .husky/pre-commit

# commit-msg 훅 설정 (commitlint 사용)
npm install @commitlint/cli @commitlint/config-conventional --save-dev
echo "npx commitlint --edit \$1" > .husky/commit-msg
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 
      'refactor', 'test', 'chore', 'revert'
    ]],
    'subject-max-length': [2, 'always', 72]
  }
};
```

### CI/CD에서의 활용

```yaml
# GitHub Actions에서 서버 훅 대체
name: Enforce Commit Convention

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Check commit messages
        uses: wagoid/commitlint-github-action@v5
```

---

## 8. Git Submodules

### 개념

Git Submodules는 하나의 Git 저장소 안에 다른 Git 저장소를 포함시키는 기능입니다.

```
main-project/
├── .git/
├── .gitmodules           # 서브모듈 설정 파일
├── src/
├── libs/
│   ├── shared-utils/     # 서브모듈 (별도 저장소)
│   └── common-ui/        # 서브모듈 (별도 저장소)
└── README.md
```

### 사용 사례

```
[서브모듈 활용 사례]

1. 공통 라이브러리 관리
   - 여러 프로젝트에서 공유하는 유틸리티
   
2. 마이크로서비스 구성
   - 각 서비스를 독립 저장소로 관리
   
3. 벤더 라이브러리
   - 외부 라이브러리를 특정 버전으로 고정
   
4. 문서/설정 분리
   - 설정 파일을 별도 저장소로 관리
```

### 기본 명령어

```bash
# 서브모듈 추가
git submodule add https://github.com/org/shared-utils.git libs/shared-utils

# .gitmodules 파일 생성됨
cat .gitmodules
# [submodule "libs/shared-utils"]
#     path = libs/shared-utils
#     url = https://github.com/org/shared-utils.git

# 서브모듈 포함 클론
git clone --recurse-submodules https://github.com/org/main-project.git

# 기존 클론에서 서브모듈 초기화
git submodule init
git submodule update

# 또는 한 번에
git submodule update --init --recursive
```

### 서브모듈 업데이트

```bash
# 특정 서브모듈 최신화
cd libs/shared-utils
git fetch origin
git checkout main
git pull origin main
cd ../..
git add libs/shared-utils
git commit -m "chore: update shared-utils submodule"

# 모든 서브모듈 최신화
git submodule update --remote --merge

# 특정 브랜치 추적 설정
git config -f .gitmodules submodule.libs/shared-utils.branch develop
```

### CI/CD에서 서브모듈 처리

```yaml
# GitHub Actions
- uses: actions/checkout@v3
  with:
    submodules: recursive  # 서브모듈 포함 체크아웃
    token: ${{ secrets.PAT_TOKEN }}  # Private 서브모듈용

# GitLab CI
variables:
  GIT_SUBMODULE_STRATEGY: recursive

# Jenkins
checkout([
    $class: 'GitSCM',
    extensions: [[$class: 'SubmoduleOption', recursiveSubmodules: true]]
])
```

### 서브모듈 vs 대안 비교

| 방식 | 장점 | 단점 | 적합한 상황 |
|------|------|------|------------|
| **Submodules** | 정확한 버전 고정 | 복잡한 워크플로우 | 안정적인 외부 의존성 |
| **Subtree** | 단일 저장소 유지 | 히스토리 복잡 | 가끔 동기화 필요 |
| **Package Manager** | 간편한 의존성 관리 | 버전 범위 문제 | 라이브러리 의존성 |
| **Monorepo** | 원자적 변경 | 저장소 크기 증가 | 긴밀한 연관 프로젝트 |

---

## 9. Git LFS (Large File Storage)

### 개념

Git LFS는 대용량 파일을 별도 스토리지에 저장하고, Git에는 포인터만 저장하는 확장 기능입니다.

```
[일반 Git]
Repository: 100MB 바이너리 파일 전체 저장
→ 히스토리에 파일 전체가 쌓임
→ clone 시 모든 버전 다운로드

[Git LFS]
Repository: 포인터 파일만 저장 (수백 바이트)
LFS Server: 실제 파일 저장
→ 필요한 버전만 다운로드
```

### 설치 및 설정

```bash
# Git LFS 설치
# macOS
brew install git-lfs

# Ubuntu
sudo apt install git-lfs

# Windows
# Git for Windows에 포함됨

# 저장소에서 LFS 활성화
git lfs install

# 추적할 파일 패턴 지정
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "*.mp4"
git lfs track "models/*.bin"

# .gitattributes 파일 생성됨
cat .gitattributes
# *.psd filter=lfs diff=lfs merge=lfs -text
# *.zip filter=lfs diff=lfs merge=lfs -text
```

### 사용 예시

```bash
# LFS 추적 파일 추가
git add .gitattributes
git add large-model.bin
git commit -m "chore: add ML model"
git push origin main

# LFS 파일 정보 확인
git lfs ls-files

# LFS 파일만 가져오기
git lfs pull

# 특정 파일 패턴만 가져오기
git lfs pull --include="*.bin"
git lfs pull --exclude="*.mp4"
```

### CI/CD에서 LFS 처리

```yaml
# GitHub Actions
- uses: actions/checkout@v3
  with:
    lfs: true  # LFS 파일 체크아웃

# GitLab CI
variables:
  GIT_LFS_SKIP_SMUDGE: "1"  # 선택적 LFS 다운로드

before_script:
  - git lfs pull --include="models/"

# Jenkins
checkout([
    $class: 'GitSCM',
    extensions: [[$class: 'GitLFSPull']]
])
```

### LFS 적용 대상

| 파일 유형 | LFS 권장 여부 | 이유 |
|----------|-------------|------|
| 이미지 (PSD, AI) | ✅ 권장 | 대용량, 바이너리 |
| 동영상 (MP4, MOV) | ✅ 권장 | 매우 대용량 |
| ML 모델 (bin, h5) | ✅ 권장 | 대용량, 자주 변경 |
| 빌드 산출물 | ❌ 비권장 | 저장소에 포함하지 말 것 |
| 문서 (PDF) | ⚠️ 선택적 | 크기에 따라 |
| 소스 코드 | ❌ 비권장 | 텍스트, diff 필요 |

---

## 10. Git Bisect

### 개념

Git Bisect는 이진 탐색을 통해 버그가 도입된 커밋을 찾는 기능입니다.

```
[100개 커밋에서 버그 찾기]

선형 탐색: 최대 100번 확인
이진 탐색: 최대 7번 확인 (log₂100 ≈ 7)

좋음 ─────────────────●───────────────────── 나쁨
                      ↑
               버그 도입 커밋
```

### 수동 Bisect

```bash
# 1. Bisect 시작
git bisect start

# 2. 현재(버그 있음)를 bad로 마킹
git bisect bad

# 3. 정상 작동하던 커밋을 good으로 마킹
git bisect good v1.0.0
# 또는
git bisect good abc1234

# 4. Git이 중간 커밋으로 체크아웃
# Bisecting: 50 revisions left to test after this

# 5. 테스트 후 결과 입력
git bisect good  # 버그 없음
# 또는
git bisect bad   # 버그 있음

# 6. 반복... Git이 범위를 좁혀감
# Bisecting: 25 revisions left...
# Bisecting: 12 revisions left...
# ...

# 7. 범인 커밋 발견
# abc1234 is the first bad commit
# commit abc1234
# Author: developer@example.com
# Date: Mon Dec 25 2024
#
#     feat: add new feature (버그 도입!)

# 8. Bisect 종료
git bisect reset
```

### 자동 Bisect (스크립트 활용)

```bash
# 테스트 스크립트 작성
# test-bug.sh
#!/bin/bash
npm test
exit $?  # 테스트 성공: 0, 실패: 1

# 자동 bisect 실행
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test-bug.sh

# Git이 자동으로 good/bad 판단
# 결과: 버그 도입 커밋 자동 발견
```

### CI/CD에서 활용

```yaml
# 버그 발견 시 자동 bisect (GitHub Actions)
name: Auto Bisect

on:
  workflow_dispatch:
    inputs:
      good_commit:
        description: 'Last known good commit'
        required: true
      test_command:
        description: 'Test command to run'
        default: 'npm test'

jobs:
  bisect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Run bisect
        run: |
          git bisect start
          git bisect bad HEAD
          git bisect good ${{ github.event.inputs.good_commit }}
          git bisect run ${{ github.event.inputs.test_command }}
```

### 실전 팁

```bash
# 특정 경로만 대상으로 bisect
git bisect start -- src/auth/

# Bisect 로그 확인
git bisect log

# 잘못된 마킹 수정
git bisect log > bisect.log
# bisect.log 편집
git bisect replay bisect.log

# 현재 상태를 스킵 (빌드 실패 등)
git bisect skip
```

---

## 11. Shallow Clone & Sparse Checkout

### Shallow Clone

전체 히스토리 대신 최근 커밋만 클론합니다.

```bash
# 최근 1개 커밋만 클론
git clone --depth 1 https://github.com/org/repo.git

# 최근 10개 커밋만 클론
git clone --depth 10 https://github.com/org/repo.git

# 특정 브랜치만 shallow clone
git clone --depth 1 --branch main https://github.com/org/repo.git

# 나중에 히스토리 확장
git fetch --unshallow

# 특정 깊이까지 확장
git fetch --depth 100
```

### Sparse Checkout

저장소의 일부 디렉토리만 체크아웃합니다.

```bash
# 1. Sparse checkout 활성화
git clone --filter=blob:none --sparse https://github.com/org/monorepo.git
cd monorepo

# 2. 필요한 디렉토리만 체크아웃
git sparse-checkout set services/user-service libs/common

# 또는 패턴 추가
git sparse-checkout add services/order-service

# 3. 설정 확인
git sparse-checkout list
# services/user-service
# services/order-service
# libs/common

# 4. 전체 체크아웃으로 복구
git sparse-checkout disable
```

### CI/CD 최적화 활용

```yaml
# GitHub Actions - Shallow Clone
- uses: actions/checkout@v3
  with:
    fetch-depth: 1  # Shallow clone

# 모노레포에서 변경된 서비스만 빌드
- name: Checkout specific service
  run: |
    git sparse-checkout init --cone
    git sparse-checkout set services/${{ matrix.service }}
```

### 효과 비교

```
[전체 클론]
Repository: 2GB
Clone 시간: 5분
Checkout: 전체 파일

[Shallow Clone (depth=1)]
다운로드: ~100MB
Clone 시간: 30초
Checkout: 전체 파일 (최신 버전만)

[Sparse Checkout]
다운로드: 필요한 부분만
Clone 시간: 10초
Checkout: 지정한 디렉토리만
```

---

## 12. Git Worktree

### 개념

Git Worktree는 하나의 저장소에서 여러 브랜치를 동시에 체크아웃할 수 있게 합니다.

```
[일반적인 방식]
repo/
└── (한 번에 하나의 브랜치만)

[Git Worktree]
repo/              # main 브랜치
repo-feature/      # feature 브랜치
repo-hotfix/       # hotfix 브랜치

→ 모두 같은 .git 공유
→ 브랜치 전환 없이 동시 작업
```

### 사용 방법

```bash
# 새 worktree 생성
git worktree add ../repo-feature feature/new-ui
git worktree add ../repo-hotfix hotfix/critical-bug

# 새 브랜치와 함께 생성
git worktree add -b feature/experiment ../repo-experiment

# worktree 목록 확인
git worktree list
# /home/user/repo          abc1234 [main]
# /home/user/repo-feature  def5678 [feature/new-ui]
# /home/user/repo-hotfix   ghi9012 [hotfix/critical-bug]

# worktree 삭제
git worktree remove ../repo-feature

# 또는 디렉토리 삭제 후 정리
rm -rf ../repo-feature
git worktree prune
```

### 활용 사례

```bash
# 1. 긴급 핫픽스 작업
# main에서 기능 개발 중 긴급 버그 발생
git worktree add ../hotfix hotfix/urgent-fix
cd ../hotfix
# 버그 수정 후
git push origin hotfix/urgent-fix
cd ../repo
# 원래 작업 계속

# 2. 코드 리뷰
# 다른 사람의 PR을 로컬에서 확인
git worktree add ../review origin/feature/colleague-work
cd ../review
# 코드 확인, 테스트
cd ../repo
git worktree remove ../review

# 3. 버전별 문서 확인
git worktree add ../v1 v1.0.0
git worktree add ../v2 v2.0.0
# 두 버전 동시에 비교
```

### CI/CD 활용

```bash
# 병렬 빌드를 위한 worktree
#!/bin/bash
BRANCHES=("main" "develop" "release/v1.0")

for branch in "${BRANCHES[@]}"; do
    git worktree add "../build-$branch" "$branch"
    (cd "../build-$branch" && npm install && npm run build) &
done

wait  # 모든 빌드 완료 대기
```

---

## 13. Signed Commits (GPG)

### 개념

GPG 서명을 통해 커밋의 진위를 검증합니다.

```
[서명되지 않은 커밋]
- 누구나 author를 위조할 수 있음
- git config user.email로 변경 가능

[서명된 커밋]
- GPG 키로 암호화 서명
- GitHub에서 "Verified" 배지 표시
- 커밋 작성자 신원 보장
```

### GPG 키 설정

```bash
# 1. GPG 키 생성
gpg --full-generate-key
# RSA and RSA, 4096 bits 선택
# 이메일은 GitHub 계정과 동일하게

# 2. 키 ID 확인
gpg --list-secret-keys --keyid-format=long
# sec   rsa4096/ABC123DEF456 2024-01-01
#       Key fingerprint = ...
# uid   Developer <dev@example.com>

# 3. Git에 서명 키 설정
git config --global user.signingkey ABC123DEF456

# 4. 커밋 시 자동 서명
git config --global commit.gpgsign true

# 5. GitHub에 공개 키 등록
gpg --armor --export ABC123DEF456
# 출력된 키를 GitHub Settings > SSH and GPG keys에 등록
```

### 서명된 커밋/태그 생성

```bash
# 서명된 커밋
git commit -S -m "feat: add secure feature"

# 서명된 태그
git tag -s v1.0.0 -m "Signed release v1.0.0"

# 서명 검증
git log --show-signature
git tag -v v1.0.0
```

### GitHub 브랜치 보호 규칙

```yaml
# 서명된 커밋만 허용
Branch protection rules:
  - Require signed commits: ✅

# 결과:
# - 서명되지 않은 커밋은 push 거부
# - PR 머지 시에도 서명 필요
```

### CI/CD에서 서명

```yaml
# GitHub Actions에서 자동 서명
- name: Import GPG key
  uses: crazy-max/ghaction-import-gpg@v5
  with:
    gpg_private_key: ${{ secrets.GPG_PRIVATE_KEY }}
    passphrase: ${{ secrets.GPG_PASSPHRASE }}
    git_user_signingkey: true
    git_commit_gpgsign: true

- name: Create signed commit
  run: |
    git commit -S -m "chore: automated update"
    git push
```

---

## 14. Conventional Commits & Semantic Release

### Conventional Commits 스펙

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type 종류

| Type | 설명 | SemVer 영향 |
|------|------|------------|
| `feat` | 새로운 기능 | Minor (0.X.0) |
| `fix` | 버그 수정 | Patch (0.0.X) |
| `docs` | 문서 변경 | 없음 |
| `style` | 코드 포맷팅 | 없음 |
| `refactor` | 리팩토링 | 없음 |
| `perf` | 성능 개선 | Patch |
| `test` | 테스트 추가/수정 | 없음 |
| `build` | 빌드 시스템 변경 | 없음 |
| `ci` | CI 설정 변경 | 없음 |
| `chore` | 기타 변경 | 없음 |
| `revert` | 커밋 되돌리기 | 원본에 따름 |

### Breaking Change

```bash
# Footer 방식
git commit -m "feat: change API response format

BREAKING CHANGE: response.data is now response.result"

# Type에 ! 추가 방식
git commit -m "feat!: change API response format"

# 둘 다 Major 버전 업 (X.0.0)
```

### Semantic Release 설정

```javascript
// release.config.js
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/npm',
    '@semantic-release/github',
    '@semantic-release/git'
  ]
};
```

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          persist-credentials: false
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm ci
      
      - name: Semantic Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### 버전 자동 결정 흐름

```
커밋 히스토리:
  feat: add user module        → Minor
  fix: resolve login bug       → Patch
  docs: update README          → 없음
  feat!: redesign API          → Major

현재 버전: v1.2.3

분석 결과:
  - Major change 있음 → Major 버전 업
  
새 버전: v2.0.0
```

---

## 15. Git Attributes

### 개념

`.gitattributes` 파일로 경로별 Git 동작을 커스터마이징합니다.

### 줄 끝 처리 (Line Endings)

```gitattributes
# .gitattributes

# 모든 텍스트 파일 자동 감지
* text=auto

# 특정 파일 강제 LF
*.sh text eol=lf
*.bash text eol=lf
Makefile text eol=lf

# 특정 파일 강제 CRLF
*.bat text eol=crlf
*.ps1 text eol=crlf

# 바이너리 파일 지정
*.png binary
*.jpg binary
*.pdf binary
```

### Diff/Merge 커스터마이징

```gitattributes
# 특정 파일 diff 비활성화
package-lock.json -diff
yarn.lock -diff

# 특정 파일 머지 전략
database.yml merge=ours

# 워드 단위 diff
*.md diff=markdown

# 이미지 diff 도구 지정
*.png diff=exif
```

### 언어별 통계 (Linguist)

```gitattributes
# GitHub 언어 통계에서 제외
docs/* linguist-documentation
vendor/* linguist-vendored
*.min.js linguist-generated

# 언어 강제 지정
*.h linguist-language=C++
```

### Export 제어

```gitattributes
# git archive에서 제외
.gitignore export-ignore
.gitattributes export-ignore
.github/ export-ignore
tests/ export-ignore

# CI/CD에서 배포 패키지 생성 시 유용
```

### CI/CD 활용 예시

```yaml
# 변경된 파일 유형에 따라 다른 작업 수행
- name: Check file types
  run: |
    # .gitattributes에서 바이너리로 지정된 파일 확인
    git check-attr binary -- $(git diff --name-only HEAD~1)
```

---

## 16. GitHub/GitLab Webhooks 심화

### Webhook 이벤트 종류

```
[GitHub Webhook Events]

Push Events:
  - push              # 코드 푸시
  - create            # 브랜치/태그 생성
  - delete            # 브랜치/태그 삭제

Pull Request Events:
  - pull_request      # PR 생성/수정/머지
  - pull_request_review
  - pull_request_review_comment

Issue Events:
  - issues
  - issue_comment

Release Events:
  - release           # 릴리즈 생성

Repository Events:
  - repository
  - fork
  - star
```

### Webhook Payload 구조

```json
// Push Event Payload
{
  "ref": "refs/heads/main",
  "before": "abc123...",
  "after": "def456...",
  "repository": {
    "id": 12345,
    "name": "my-repo",
    "full_name": "org/my-repo"
  },
  "pusher": {
    "name": "developer",
    "email": "dev@example.com"
  },
  "commits": [
    {
      "id": "def456...",
      "message": "feat: add new feature",
      "author": {...},
      "added": ["src/new.js"],
      "modified": ["src/existing.js"],
      "removed": []
    }
  ],
  "head_commit": {...}
}
```

### Webhook 수신 서버 구현

```javascript
// Node.js Express 예시
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Webhook 시크릿 검증
function verifySignature(req) {
  const signature = req.headers['x-hub-signature-256'];
  const hmac = crypto.createHmac('sha256', process.env.WEBHOOK_SECRET);
  const digest = 'sha256=' + hmac.update(JSON.stringify(req.body)).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

app.post('/webhook', (req, res) => {
  // 서명 검증
  if (!verifySignature(req)) {
    return res.status(401).send('Invalid signature');
  }

  const event = req.headers['x-github-event'];
  const payload = req.body;

  switch (event) {
    case 'push':
      handlePush(payload);
      break;
    case 'pull_request':
      handlePullRequest(payload);
      break;
    case 'release':
      handleRelease(payload);
      break;
  }

  res.status(200).send('OK');
});

function handlePush(payload) {
  const branch = payload.ref.replace('refs/heads/', '');
  const commits = payload.commits;
  
  console.log(`Push to ${branch}: ${commits.length} commits`);
  
  // 태그 푸시 감지
  if (payload.ref.startsWith('refs/tags/')) {
    const tag = payload.ref.replace('refs/tags/', '');
    console.log(`New tag: ${tag}`);
    // 배포 트리거
    triggerDeployment(tag);
  }
}

function handleRelease(payload) {
  if (payload.action === 'published') {
    const version = payload.release.tag_name;
    console.log(`Release published: ${version}`);
    triggerDeployment(version);
  }
}
```

### GitLab Webhook 특이사항

```json
// GitLab Push Event (약간 다른 구조)
{
  "object_kind": "push",
  "event_name": "push",
  "ref": "refs/heads/main",
  "checkout_sha": "def456...",
  "project": {
    "id": 12345,
    "name": "my-repo",
    "path_with_namespace": "org/my-repo"
  },
  "commits": [...],
  "total_commits_count": 1
}

// GitLab 헤더
X-Gitlab-Event: Push Hook
X-Gitlab-Token: <secret_token>
```

### Webhook 디버깅

```bash
# ngrok으로 로컬 테스트
ngrok http 3000

# GitHub Webhook 재전송
# Settings > Webhooks > Recent Deliveries > Redeliver

# 로그 확인
# Settings > Webhooks > Recent Deliveries
# - Request headers
# - Request body
# - Response status
# - Response body
```

---

# Part 3: 종합 정리

## 17. CI/CD Git 기술 체크리스트

### 기본 기술

| 기술 | 용도 | 중요도 |
|------|------|--------|
| 브랜치 전략 | 개발 워크플로우 정의 | ⭐⭐⭐ 필수 |
| 태그 | 버전 관리, 배포 트리거 | ⭐⭐⭐ 필수 |
| 머지 전략 | 코드 통합 방식 | ⭐⭐⭐ 필수 |
| Revert/Reset | 롤백 | ⭐⭐⭐ 필수 |

### 자동화 기술

| 기술 | 용도 | 중요도 |
|------|------|--------|
| Git Hooks | 로컬 검증 자동화 | ⭐⭐⭐ 필수 |
| Conventional Commits | 커밋 메시지 표준화 | ⭐⭐⭐ 필수 |
| Semantic Release | 버전/태그 자동화 | ⭐⭐ 권장 |
| Webhooks | CI/CD 트리거 | ⭐⭐⭐ 필수 |

### 최적화 기술

| 기술 | 용도 | 중요도 |
|------|------|--------|
| Shallow Clone | CI 속도 개선 | ⭐⭐ 권장 |
| Sparse Checkout | 모노레포 최적화 | ⭐⭐ 권장 |
| Git LFS | 대용량 파일 관리 | ⭐ 선택적 |

### 고급 기술

| 기술 | 용도 | 중요도 |
|------|------|--------|
| Git Submodules | 의존성 관리 | ⭐ 선택적 |
| Git Worktree | 병렬 작업 | ⭐ 선택적 |
| Git Bisect | 버그 추적 | ⭐ 선택적 |
| Signed Commits | 보안 강화 | ⭐⭐ 권장 |
| Git Attributes | 파일별 설정 | ⭐ 선택적 |

### DevOps Workflow 제품 구현 시 우선순위

```
[1단계: 핵심 기능]
✅ 브랜치 이벤트 감지 (push, merge)
✅ 태그 이벤트 감지 (create, delete)
✅ PR/MR 이벤트 감지
✅ 기본 롤백 지원 (revert)

[2단계: 자동화 기능]
✅ Conventional Commits 파싱
✅ 자동 버전 결정
✅ 자동 태그 생성
✅ Release Notes 생성

[3단계: 최적화 기능]
✅ Shallow Clone 옵션
✅ Sparse Checkout 지원 (모노레포)
✅ Git LFS 지원

[4단계: 고급 기능]
✅ Git Hooks 템플릿 제공
✅ Signed Commits 검증
✅ Bisect 자동화
✅ Submodule 지원
```

---

## 참고 자료

### 기업 기술 블로그

- [메쉬코리아 - CI/CD 도구 및 방법론 도입기](https://mesh.dev/20210208-dev-notes-002-ci-cd/)
- [우아한형제들 - 우린 Git-flow를 사용하고 있어요](https://techblog.woowahan.com/2553/)
- [뱅크샐러드 - 하루에 1000번 배포하는 조직 되기](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/)
- [당근페이 - 매일 배포하는 팀이 되는 여정](https://medium.com/daangn/)
- [SK Devocean - GitHub Action을 이용하여 Release 자동화](https://devocean.sk.com/blog/techBoardDetail.do?ID=164861)

### 공식 문서

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Release](https://semantic-release.gitbook.io/)

---

*이전 문서: [02-git-concepts-tag-rollback-merge.md](./02-git-concepts-tag-rollback-merge.md)*
