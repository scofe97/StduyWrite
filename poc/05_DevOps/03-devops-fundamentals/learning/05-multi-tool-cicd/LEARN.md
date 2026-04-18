# Ch05. 멀티 도구 CI/CD 구축

**핵심 질문**: "GitHub Actions로 파이프라인을 처음부터 어떻게 구축하는가?"

---

## 🎯 학습 목표

1. CI/CD 도구들의 아키텍처 차이를 이해하고 상황에 맞는 도구를 선택할 수 있다.
2. GitHub Actions의 workflow, job, step, runner 구조를 설명할 수 있다.
3. OIDC 인증 방식을 활용해 정적 시크릿 없이 클라우드에 배포하는 파이프라인을 작성할 수 있다.
4. Matrix 전략으로 멀티 버전 테스트와 캐싱을 적용해 빌드 시간을 단축할 수 있다.
5. GitOps 패턴과 ArgoCD의 Pull-based 배포 방식을 이해하고, Push-based 방식과 차이를 비교할 수 있다.
6. ApplicationSet을 사용해 멀티 환경(dev/staging/prod) 배포를 선언적으로 관리할 수 있다.

---

## 1. CI/CD 도구 선택

CI/CD 도구는 "어디에서 실행되느냐"와 "무엇을 자동화하느냐"에 따라 적합한 선택이 달라진다. 비용, 유지보수 부담, 기존 인프라와의 통합 여부를 함께 고려해야 한다.

| 항목 | GitHub Actions | GitLab CI | Jenkins | CircleCI |
|------|---------------|-----------|---------|---------|
| **호스팅** | SaaS (GitHub) | SaaS/Self-hosted | Self-hosted | SaaS |
| **설정 방식** | YAML (저장소 내) | YAML (.gitlab-ci.yml) | Groovy (Jenkinsfile) | YAML (.circleci/config.yml) |
| **Runner** | GitHub-hosted / Self-hosted | GitLab Runner | Jenkins Agent | CircleCI Runner |
| **무료 티어** | 월 2,000분 (퍼블릭 무제한) | 월 400분 | 없음 (인프라 비용) | 월 6,000분 |
| **플러그인 생태계** | Marketplace (수천 개 Action) | 내장 기능 중심 | 1,800+ 플러그인 | Orbs |
| **OIDC 지원** | 네이티브 지원 | 네이티브 지원 | 플러그인 필요 | 지원 |
| **적합한 상황** | GitHub 저장소 사용 팀 | GitLab 전체 플랫폼 사용 팀 | 복잡한 온프레미스 파이프라인 | 빠른 SaaS 시작 |

GitHub Actions의 가장 큰 장점은 저장소와의 통합이다. 코드와 파이프라인 정의가 같은 저장소에 있어 리뷰, 히스토리 추적, 브랜치별 파이프라인 관리가 자연스럽다. Jenkins는 복잡한 엔터프라이즈 파이프라인에 강하지만 유지보수 오버헤드가 크다 — Jenkins 실습은 `runners-high/poc/05_DevOps/01-jenkins/`를 참고한다.

---

## 2. GitHub Actions 아키텍처

GitHub Actions는 네 가지 계층 구조로 동작한다. 이 계층을 이해하면 파이프라인을 설계할 때 "어디에 무엇을 놓아야 하는가"를 직관적으로 결정할 수 있다.

```
Workflow (.github/workflows/*.yml)
  └── Job (병렬/순차 실행 단위, 독립된 VM/Container)
        └── Step (순차 실행 단위, 같은 파일시스템 공유)
              └── Action (재사용 가능한 Step 단위)
```

**Workflow**: 특정 이벤트(push, pull_request, schedule 등)에 반응해 실행되는 자동화 단위다. `.github/workflows/` 디렉토리에 YAML 파일로 정의한다.

**Job**: 독립된 실행 환경(runner)에서 돌아가는 Step들의 묶음이다. 기본적으로 Job들은 병렬 실행되며, `needs` 키워드로 의존 관계를 설정하면 순차 실행이 가능하다. Job 사이에는 파일시스템이 공유되지 않으므로, 빌드 결과물을 다음 Job으로 전달할 때는 `actions/upload-artifact`와 `actions/download-artifact`를 사용한다.

**Step**: 같은 Job 안의 Step들은 동일한 파일시스템을 공유한다. 따라서 이전 Step에서 생성한 파일을 다음 Step에서 바로 사용할 수 있다.

**Runner**: Job이 실행되는 가상 머신이다. GitHub이 제공하는 hosted runner(ubuntu-latest, windows-latest, macos-latest)와 사용자가 직접 운영하는 self-hosted runner로 나뉜다 — runner 상세는 INVESTIGATE.md Q1 참조.

```mermaid
graph TD
    A[이벤트: push to main] --> B[Workflow 트리거]
    B --> C[Job: lint-test]
    B --> D[Job: build]
    C --> E[Step: Checkout]
    C --> F[Step: Setup Node]
    C --> G[Step: Run lint]
    C --> H[Step: Run tests]
    D --> I[Step: Checkout]
    D --> J[Step: Docker build]
    D --> K[Step: Docker push]
    C -->|needs| L[Job: deploy]
    D -->|needs| L
    L --> M[Step: ArgoCD sync]
    L --> N[Step: Slack notify]

    style A fill:#e8f4f8,stroke:#2196F3,color:#333
    style L fill:#e8f5e9,stroke:#4CAF50,color:#333
```

---

## 3. 전체 GitHub Actions CI/CD 파이프라인

아래는 실제 프로덕션에 가까운 파이프라인이다. OIDC 인증, Matrix 전략, 캐싱, 조건부 배포, 실패 알림을 모두 포함한다.

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# OIDC 토큰 발급을 위한 최소 권한 설정
# 정적 AWS 시크릿 대신 임시 토큰으로 인증한다
permissions:
  id-token: write   # OIDC JWT 발급 허용
  contents: read
  packages: write   # GHCR 이미지 푸시 허용

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  NODE_VERSION_DEFAULT: "20"

jobs:
  # ──────────────────────────────────────────────
  # Job 1: Lint & Test (Matrix 전략으로 멀티 버전 검증)
  # ──────────────────────────────────────────────
  lint-test:
    name: Lint & Test (Node ${{ matrix.node-version }})
    runs-on: ubuntu-latest
    # Matrix: Node 18, 20, 22 세 버전을 병렬로 테스트
    # 한 버전에서 실패해도 다른 버전은 계속 실행된다
    strategy:
      fail-fast: false
      matrix:
        node-version: ["18", "20", "22"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          # cache: npm은 package-lock.json 해시를 키로 캐싱한다
          # 의존성이 바뀌지 않으면 install을 건너뛰어 수십 초를 절약한다
          cache: "npm"

      - name: Install dependencies
        run: npm ci  # npm install 대신 ci를 사용해 lock file 준수

      - name: Run lint
        run: npm run lint

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb

      # 테스트 커버리지 리포트를 아티팩트로 보존
      - name: Upload coverage report
        if: matrix.node-version == env.NODE_VERSION_DEFAULT
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
          retention-days: 7

    # 통합 테스트용 PostgreSQL 서비스 컨테이너
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_USER: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

  # ──────────────────────────────────────────────
  # Job 2: Docker 이미지 빌드 & 푸시
  # ──────────────────────────────────────────────
  build-push:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    needs: lint-test  # 테스트 통과 후에만 이미지를 빌드한다
    outputs:
      # 다음 Job(deploy)에서 이미지 태그를 참조하기 위해 output으로 전달
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        # Buildx는 BuildKit 기반으로 레이어 캐싱과 멀티 플랫폼 빌드를 지원한다

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}  # 자동 발급 토큰, 별도 설정 불필요

      - name: Extract Docker metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            # PR: pr-{번호}
            type=ref,event=pr
            # main 브랜치: latest + SHA 짧은 해시
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
            type=sha,prefix=sha-,format=short

      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}  # PR에서는 push 안 함
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          # GitHub Actions 캐시를 Docker 레이어 캐싱에 활용
          # 변경되지 않은 레이어는 재빌드하지 않아 빌드 시간이 단축된다
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  # ──────────────────────────────────────────────
  # Job 3: 배포 (main 브랜치 push 시에만 실행)
  # ──────────────────────────────────────────────
  deploy:
    name: Deploy to Kubernetes
    runs-on: ubuntu-latest
    needs: [lint-test, build-push]
    # main 브랜치에 직접 push될 때만 배포한다
    # PR 빌드에서 실수로 배포되는 것을 방지하는 안전장치다
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
      - name: Checkout GitOps repository
        uses: actions/checkout@v4
        with:
          repository: my-org/gitops-config  # 인프라 설정 저장소
          token: ${{ secrets.GITOPS_TOKEN }}

      # AWS OIDC 인증 — 정적 AWS_ACCESS_KEY_ID/SECRET 없이 임시 자격증명 발급
      # GitHub → AWS IAM OIDC Provider → AssumeRoleWithWebIdentity → 임시 토큰
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-deploy
          aws-region: ap-northeast-2
          # 토큰 유효 기간: 최대 1시간, 파이프라인 완료 후 자동 만료

      - name: Update image tag in GitOps repo
        run: |
          # GitOps: 이미지 태그를 코드로 변경하면 ArgoCD가 자동으로 감지해 배포한다
          NEW_TAG="sha-$(echo ${{ github.sha }} | cut -c1-7)"
          sed -i "s|image: .*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${NEW_TAG}|" \
            apps/my-app/overlays/production/kustomization.yaml
          git config user.email "github-actions@github.com"
          git config user.name "GitHub Actions"
          git commit -am "chore: update my-app image to ${NEW_TAG}"
          git push

  # ──────────────────────────────────────────────
  # Job 4: 실패 알림 (어떤 Job이든 실패하면 실행)
  # ──────────────────────────────────────────────
  notify-failure:
    name: Notify on Failure
    runs-on: ubuntu-latest
    needs: [lint-test, build-push, deploy]
    # 선행 Job 중 하나라도 실패했을 때만 실행
    if: failure()

    steps:
      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Pipeline failed on `${{ github.ref_name }}`",
              "attachments": [{
                "color": "danger",
                "fields": [
                  {"title": "Repository", "value": "${{ github.repository }}", "short": true},
                  {"title": "Commit", "value": "${{ github.sha }}", "short": true},
                  {"title": "Triggered by", "value": "${{ github.actor }}", "short": true},
                  {"title": "Run URL", "value": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}", "short": false}
                ]
              }]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 4. 파이프라인용 Dockerfile (멀티 스테이지 빌드)

CI 파이프라인에서 빌드하는 이미지는 멀티 스테이지 빌드를 사용해야 한다. 빌드 도구와 의존성을 최종 이미지에 포함시키지 않아 이미지 크기와 공격 표면을 줄이는 것이 목적이다.

```dockerfile
# Dockerfile

# ── Stage 1: 의존성 설치 ──────────────────────────
# node:20-alpine을 베이스로 사용해 이미지를 작게 유지한다
FROM node:20-alpine AS deps
WORKDIR /app

# package 파일만 먼저 복사 — 소스 코드 변경 시 이 레이어는 캐시를 재사용한다
COPY package*.json ./
RUN npm ci --only=production

# ── Stage 2: 빌드 ─────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci  # 개발 의존성 포함 (타입스크립트 컴파일러 등)
COPY . .
RUN npm run build

# ── Stage 3: 최종 실행 이미지 ─────────────────────
# 빌드 도구 없이 프로덕션 의존성과 빌드 결과물만 포함
FROM node:20-alpine AS runner
WORKDIR /app

# 보안: root가 아닌 전용 사용자로 실행
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# deps 스테이지에서 프로덕션 의존성만 복사
COPY --from=deps /app/node_modules ./node_modules
# builder 스테이지에서 빌드 결과물만 복사
COPY --from=builder /app/dist ./dist

USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

---

## 5. GitOps와 ArgoCD

### GitOps란 무엇인가

GitOps는 Git 저장소를 인프라와 애플리케이션의 "단일 진실 원천"으로 사용하는 운영 방식이다. 클러스터 상태를 직접 변경하는 대신, Git에 원하는 상태를 커밋하면 자동화 도구가 실제 상태를 원하는 상태에 맞게 조정한다. 이 방식의 핵심 이점은 모든 변경이 Git 히스토리로 추적되고, 롤백이 `git revert` 하나로 해결된다는 점이다.

ArgoCD는 Kubernetes를 위한 GitOps 도구다. Git 저장소를 지속적으로 감시하다가 실제 클러스터 상태와 차이가 생기면 자동으로 동기화한다.

### ArgoCD Application 매니페스트

```yaml
# apps/my-app/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-production
  namespace: argocd
  # finalizer: ArgoCD Application 삭제 시 클러스터 리소스도 함께 정리
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/my-org/gitops-config
    targetRevision: main
    path: apps/my-app/overlays/production  # Kustomize overlay 경로

  destination:
    server: https://kubernetes.default.svc
    namespace: my-app-production

  syncPolicy:
    automated:
      prune: true      # Git에서 삭제된 리소스는 클러스터에서도 삭제
      selfHeal: true   # 클러스터 상태가 수동으로 변경되면 Git 상태로 복구
    syncOptions:
      - CreateNamespace=true        # 네임스페이스 없으면 자동 생성
      - PrunePropagationPolicy=foreground  # 의존 리소스부터 순서대로 삭제
      - ApplyOutOfSyncOnly=true     # 변경된 리소스만 적용 (성능 최적화)

  # 동기화 실패 재시도 설정
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m

  # 헬스 체크: 롤링 업데이트가 완료되기 전에 Synced 상태로 전환되지 않도록 한다
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # HPA가 관리하는 replica 수는 drift 무시
```

### ArgoCD ApplicationSet (멀티 환경 관리)

ApplicationSet은 하나의 템플릿으로 여러 환경의 Application을 생성한다. 환경이 추가될 때마다 Application YAML을 별도로 만들 필요가 없다.

```yaml
# apps/my-app/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-app
  namespace: argocd
spec:
  # List generator: 환경 목록을 직접 정의
  generators:
    - list:
        elements:
          - env: dev
            cluster: https://dev-cluster.example.com
            namespace: my-app-dev
            autoSync: "true"
            imageTag: develop
          - env: staging
            cluster: https://staging-cluster.example.com
            namespace: my-app-staging
            autoSync: "true"
            imageTag: staging
          - env: production
            cluster: https://prod-cluster.example.com
            namespace: my-app-production
            autoSync: "false"  # 프로덕션은 수동 승인 후 동기화
            imageTag: latest

  template:
    metadata:
      name: "my-app-{{env}}"
      namespace: argocd
    spec:
      project: default
      source:
        repoURL: https://github.com/my-org/gitops-config
        targetRevision: main
        path: "apps/my-app/overlays/{{env}}"
      destination:
        server: "{{cluster}}"
        namespace: "{{namespace}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: "{{autoSync}}" == "true"
```

---

## 6. Push-based vs Pull-based CD

CD 방식은 배포 트리거의 방향에 따라 두 가지로 나뉜다. 어떤 방식이 낫다기보다 팀의 보안 요구사항과 운영 복잡도에 따라 선택이 달라진다.

| 비교 항목 | Push-based (GitHub Actions 직접 배포) | Pull-based (ArgoCD GitOps) |
|----------|--------------------------------------|---------------------------|
| **작동 방식** | CI 파이프라인이 kubectl/helm으로 클러스터에 직접 배포 | ArgoCD가 Git을 감시하다가 변경 감지 시 동기화 |
| **클러스터 접근** | 외부(CI 서버)에서 클러스터에 접근 | 클러스터 내부 에이전트가 외부 Git에 접근 |
| **보안** | CI 서버에 클러스터 자격증명 저장 필요 | 클러스터 자격증명이 외부에 노출되지 않음 |
| **드리프트 감지** | 없음 (배포 후 수동 변경을 감지 못함) | selfHeal로 자동 감지 및 복구 |
| **롤백** | 이전 파이프라인 재실행 또는 수동 | `git revert` 후 자동 동기화 |
| **오프라인 클러스터** | 배포 불가 | 가능 (내부에서 Git 폴링) |
| **복잡도** | 낮음 (파이프라인만) | 높음 (ArgoCD 별도 운영) |
| **적합한 상황** | 소규모 팀, 빠른 시작 | 멀티 클러스터, 강한 보안 요구사항 |

---

## 7. Bad vs Good: 수동 배포 vs 자동화 파이프라인

### Bad: 수동 배포 스크립트

```bash
# deploy.sh — 절대 이렇게 하지 말 것
# 문제 1: 자격증명이 스크립트에 하드코딩될 위험
# 문제 2: 누가 언제 어떤 버전을 배포했는지 추적 불가
# 문제 3: 테스트 없이 배포, 장애 발생 시 원인 추적 어려움
# 문제 4: 로컬 환경에 따라 결과가 달라짐 ("내 컴퓨터에서는 됐는데...")

export KUBECONFIG=~/.kube/config  # 로컬 kubeconfig 의존
docker build -t myapp:latest .
docker push myapp:latest
kubectl set image deployment/myapp myapp=myapp:latest
echo "배포 완료!"  # 실제로 성공했는지 확인하지 않음
```

### Good: GitHub Actions 자동 파이프라인

위 섹션 3의 파이프라인이 수동 배포와 다른 핵심 포인트:
- 모든 배포는 Git 커밋과 연결되어 추적 가능하다.
- OIDC로 임시 자격증명을 사용해 정적 시크릿 노출 위험이 없다.
- 테스트 통과 후에만 배포가 진행된다(`needs: lint-test`).
- 실패 시 즉시 팀에 알림이 전송된다.
- PR에서는 빌드만 하고 배포하지 않는다(`if: github.ref == 'refs/heads/main'`).

---

## 8. CI/CD 파이프라인 전체 흐름

```mermaid
graph LR
    A[개발자 push] --> B[GitHub Actions 트리거]
    B --> C{PR인가?}
    C -->|PR| D[lint + test + build only]
    C -->|main push| E[lint + test]
    E --> F[Docker build & push]
    F --> G[GitOps 저장소 이미지 태그 업데이트]
    G --> H[ArgoCD 변경 감지]
    H --> I{환경}
    I -->|dev/staging| J[자동 동기화]
    I -->|production| K[수동 승인 후 동기화]
    J --> L[Kubernetes 배포]
    K --> L
    D --> M{실패?}
    E --> M
    F --> M
    M -->|실패| N[Slack 알림]

    style A fill:#e3f2fd,stroke:#1976D2,color:#333
    style L fill:#e8f5e9,stroke:#388E3C,color:#333
    style N fill:#ffebee,stroke:#D32F2F,color:#333
    style K fill:#fff3e0,stroke:#F57C00,color:#333
```

---

## 교차 참조

- **Jenkins 기초**: `runners-high/poc/05_DevOps/01-jenkins/learning/` — Jenkinsfile, Shared Library, Agent 설정
- **Kubernetes 배포**: `runners-high/poc/03_CloudNative/02-kubernetes/learning/` — Deployment, Service, Kustomize
- **Docker 멀티 스테이지 빌드**: `runners-high/poc/03_CloudNative/01-docker/learning/` — Ch07 Dockerfile 최적화
- **보안 (OIDC)**: INVESTIGATE.md Q2 — OIDC 인증이 정적 시크릿보다 나은 이유 상세

---

## 핵심 요약

| 개념 | 한 줄 설명 |
|------|-----------|
| **GitHub Actions** | 저장소와 통합된 이벤트 기반 CI/CD, YAML로 정의 |
| **OIDC 인증** | 정적 시크릿 없이 임시 자격증명으로 클라우드 인증 |
| **Matrix 전략** | 여러 버전/환경 조합을 병렬로 테스트 |
| **GitOps** | Git을 단일 진실 원천으로 삼아 선언적으로 인프라를 관리 |
| **ArgoCD** | Git 변경을 감지해 Kubernetes 클러스터를 자동 동기화하는 Pull-based CD 도구 |
| **ApplicationSet** | 하나의 템플릿으로 멀티 환경 Application을 생성하는 ArgoCD 확장 |
| **Push-based CD** | CI 파이프라인이 직접 클러스터에 배포, 설정 간단하지만 자격증명 외부 노출 |
| **Pull-based CD** | 클러스터 내 에이전트가 Git을 감시해 동기화, 보안 강하고 드리프트 자동 복구 |
| **멀티 스테이지 빌드** | 빌드 도구를 최종 이미지에서 제외해 이미지 크기와 공격 표면을 줄임 |

---

## 다음 챕터 예고

Ch06에서는 멀티 팀 환경에서 파이프라인을 어떻게 조직화하는지 다룬다. 팀마다 독립적인 파이프라인을 유지하면서도 공통 워크플로우를 재사용하는 방법, 그리고 환경별 배포 승인 프로세스를 설계하는 방식을 살펴본다.
