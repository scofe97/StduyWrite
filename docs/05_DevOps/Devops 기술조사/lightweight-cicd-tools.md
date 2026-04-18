# CI/CD 도구 비교 가이드

이 문서에서는 Jenkins를 포함한 다양한 CI/CD 도구들을 비교하고 정리한다.

---

## 1. Jenkins

### 1.1 개요

- **언어**: Java
- **라이선스**: MIT
- **메모리**: 1~4GB (플러그인에 따라 증가)
- **URL**: https://www.jenkins.io/

### 1.2 특징

- 가장 오래되고 널리 사용되는 CI/CD 도구
- 1,800개 이상의 플러그인 생태계
- Pipeline as Code (Jenkinsfile) 지원
- 거의 모든 도구와 연동 가능
- Blue Ocean UI로 현대적 인터페이스 제공

### 1.3 장단점

| 장점 | 단점 |
|------|------|
| 풍부한 플러그인 생태계 | 무거움 (JVM 기반) |
| 레퍼런스가 많음 | 설정이 복잡함 |
| 유연한 커스터마이징 | 플러그인 의존성 관리 어려움 |
| 대규모 프로젝트에 적합 | UI/UX가 구식 |
| 한국어 자료 풍부 | 보안 취약점 관리 필요 |

### 1.4 Jenkinsfile 예시

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
    post {
        always {
            junit '**/target/surefire-reports/*.xml'
        }
    }
}
```

### 1.5 언제 Jenkins를 선택하나?

- 복잡한 빌드 파이프라인이 필요할 때
- 다양한 툴과의 연동이 필수일 때
- 온프레미스 환경에서 완전한 제어가 필요할 때
- 레거시 시스템과의 호환성이 중요할 때
- 팀에 Jenkins 경험자가 있을 때

---

## 2. 한국에서 많이 쓰는 CI/CD 도구

### 2.1 GitHub Actions

- **특징**: GitHub에 내장된 CI/CD
- **가격**: Public 무료, Private는 월 2,000분 무료 후 유료
- **메모리**: SaaS (관리 불필요)
- **인기 이유**: GitHub 사용률 높음, 설정 간단, Marketplace 풍부

```yaml
# .github/workflows/build.yml
name: Build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Build with Gradle
        run: ./gradlew build
```

### 2.2 GitLab CI/CD

- **특징**: GitLab에 내장, 강력한 DevOps 플랫폼
- **가격**: Self-hosted 무료, SaaS는 플랜별
- **메모리**: Runner ~200MB
- **인기 이유**: 올인원 DevOps, 보안 기능 내장, 한국 기업 도입 증가

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  image: maven:3.8-openjdk-17
  script:
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
  only:
    - main
```

### 2.3 ArgoCD

- **특징**: Kubernetes용 GitOps CD 도구
- **메모리**: ~500MB
- **인기 이유**: GitOps 표준, 선언적 배포, K8s 환경 필수 도구화

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 2.4 AWS CodePipeline / CodeBuild

- **특징**: AWS 네이티브 CI/CD
- **가격**: 파이프라인당 월 $1, 빌드 분당 과금
- **인기 이유**: AWS 사용 기업 많음, 다른 AWS 서비스와 연동 용이

```yaml
# buildspec.yml
version: 0.2
phases:
  install:
    runtime-versions:
      java: corretto17
  build:
    commands:
      - ./gradlew build
artifacts:
  files:
    - target/*.jar
```

### 2.5 Azure DevOps

- **특징**: Microsoft의 DevOps 플랫폼
- **가격**: 5명까지 무료, 이후 유료
- **인기 이유**: MS/Azure 환경에서 선호, 올인원 플랫폼

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: Maven@3
    inputs:
      mavenPomFile: 'pom.xml'
      goals: 'clean package'
```

### 2.6 한국 시장 점유율 (체감 기준)

| 순위 | 도구 | 주요 사용처 |
|------|------|------------|
| 1 | Jenkins | 대기업, 금융권, 공공기관 |
| 2 | GitHub Actions | 스타트업, 중소기업, 오픈소스 |
| 3 | GitLab CI | 보안 중시 기업, 대기업 일부 |
| 4 | ArgoCD | K8s 도입 기업 (CD 전용) |
| 5 | AWS CodePipeline | AWS 올인 기업 |
| 6 | Azure DevOps | MS 파트너, .NET 환경 |

---

## 3. 경량 Self-hosted 옵션

### 3.1 Drone CI

- **언어**: Go
- **특징**: 컨테이너 네이티브 설계, YAML 기반 파이프라인 (`.drone.yml`)
- **연동**: GitHub, GitLab, Gitea, Bitbucket 등
- **메모리**: ~100MB
- **장점**: 매우 가볍고 빠름, 설정이 간단함
- **단점**: Enterprise 기능은 유료

```yaml
# .drone.yml 예시
kind: pipeline
type: docker
name: default

steps:
  - name: build
    image: maven:3.8-openjdk-17
    commands:
      - mvn clean package
```

### 3.2 Woodpecker CI

- **언어**: Go
- **특징**: Drone의 커뮤니티 포크, 완전 오픈소스 (Apache 2.0)
- **메모리**: ~100MB
- **장점**: Drone과 거의 동일한 사용법, 라이선스 이슈 없음
- **단점**: Drone 대비 생태계가 작음
- **URL**: https://woodpecker-ci.org/

```yaml
# .woodpecker.yml 예시
steps:
  build:
    image: gradle:8-jdk17
    commands:
      - gradle build
```

### 3.3 Tekton

- **언어**: Go
- **특징**: Kubernetes 네이티브, CRD 기반 파이프라인 정의
- **환경**: Kubernetes 필수
- **메모리**: ~500MB (컨트롤러)
- **장점**: ArgoCD와 궁합 좋음, 클라우드 네이티브 표준
- **단점**: K8s 없으면 사용 불가, 학습 곡선 존재

```yaml
# Tekton Task 예시
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: build-app
spec:
  steps:
    - name: build
      image: maven:3.8-openjdk-17
      script: |
        mvn clean package
```

### 3.4 Concourse CI

- **언어**: Go
- **특징**: 리소스 기반의 선언적 파이프라인
- **메모리**: ~500MB
- **장점**: 개념이 깔끔함, 파이프라인 시각화 우수
- **단점**: 독특한 개념으로 학습 곡선 있음

```yaml
# pipeline.yml 예시
jobs:
  - name: build
    plan:
      - get: source-code
        trigger: true
      - task: compile
        file: source-code/ci/build.yml
```

### 3.5 GoCD

- **언어**: Java/Ruby
- **특징**: ThoughtWorks 제작, Value Stream Map 기능
- **메모리**: ~1GB
- **장점**: 파이프라인 시각화 뛰어남, 복잡한 워크플로우 지원
- **단점**: 상대적으로 무거움

### 3.6 Agola

- **언어**: Go
- **특징**: 클라우드 네이티브, 런타임 선택 가능 (Docker, K8s, 로컬)
- **메모리**: ~200MB
- **장점**: Gitea/Gogs와 연동 좋음, 유연한 런타임
- **URL**: https://agola.io/

### 3.7 Laminar

- **언어**: Rust
- **특징**: 극도로 가벼움, 단일 바이너리 실행
- **메모리**: ~50MB
- **장점**: 미니멀, 웹 UI 내장, 설치 간단
- **단점**: 기능이 단순함, 복잡한 파이프라인에는 부적합
- **URL**: https://laminar.ohwg.net/

---

## 4. 하이브리드 (에이전트 Self-hosted)

### 4.1 Buildkite

- **특징**: 컨트롤 플레인은 SaaS, 에이전트만 self-hosted
- **에이전트**: Go 바이너리 하나 (~50MB)
- **장점**: 매우 가벼운 설치, 관리 부담 적음
- **단점**: 컨트롤 플레인 의존, 완전한 self-hosted 불가
- **가격**: 소규모 팀 무료 플랜 있음

### 4.2 Cirrus CI

- **특징**: self-hosted 러너 지원, Starlark 스크립트 지원
- **장점**: 설정 간단, 유연한 문법
- **URL**: https://cirrus-ci.org/

---

## 5. Git 서버 내장 CI

### 5.1 Gitea Actions

- **특징**: GitHub Actions 호환 문법, Gitea에 내장
- **러너**: act_runner
- **장점**: 별도 설치 불필요 (Gitea 사용 시), GitHub Actions 경험 활용
- **단점**: Gitea 전용

```yaml
# .gitea/workflows/build.yml
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew build
```

### 5.2 GitLab CI (Self-hosted)

- **특징**: GitLab에 내장된 CI/CD
- **장점**: GitLab과 완벽한 통합
- **단점**: GitLab 전용, 러너 별도 설치 필요

---

## 6. 태스크 러너 / 보조 도구

CI/CD와 조합하거나 단순한 자동화에 사용할 수 있는 도구들.

### 6.1 Task (go-task)

- **언어**: Go
- **특징**: Makefile 대체제, YAML 기반
- **URL**: https://taskfile.dev/

```yaml
# Taskfile.yml
version: '3'
tasks:
  build:
    cmds:
      - go build -o bin/app
  test:
    cmds:
      - go test ./...
```

### 6.2 Just

- **언어**: Rust
- **특징**: 커맨드 러너, Makefile보다 간단한 문법
- **URL**: https://github.com/casey/just

```just
# justfile
build:
    cargo build --release

test:
    cargo test
```

### 6.3 Dagger

- **언어**: Go (SDK: Go, Python, TypeScript 등)
- **특징**: 파이프라인을 코드로 작성, 로컬/CI 동일 실행
- **장점**: 로컬에서 디버깅 가능, 언어별 SDK 제공
- **URL**: https://dagger.io/

### 6.4 Pueue

- **언어**: Rust
- **특징**: 태스크 큐/스케줄러
- **용도**: 빌드 잡 관리, 병렬 실행

---

## 7. 비교표

### 7.1 전체 도구 비교

| 도구 | 메모리 | K8s 필수 | 설정 복잡도 | 라이선스 | 특징 |
|------|--------|----------|------------|----------|------|
| **Jenkins** | 1~4GB | ❌ | 높음 | MIT | 풍부한 플러그인, 레퍼런스 많음 |
| **GitHub Actions** | SaaS | ❌ | 낮음 | 상용 | GitHub 통합, Marketplace |
| **GitLab CI** | ~200MB | ❌ | 낮음 | MIT/상용 | 올인원 DevOps |
| **ArgoCD** | ~500MB | ✅ | 중간 | Apache 2.0 | GitOps CD 전용 |
| **AWS CodePipeline** | SaaS | ❌ | 중간 | 상용 | AWS 네이티브 |
| **Azure DevOps** | SaaS | ❌ | 중간 | 상용 | MS 생태계 통합 |
| **Drone** | ~100MB | ❌ | 낮음 | 부분 유료 | 심플, 빠른 시작 |
| **Woodpecker** | ~100MB | ❌ | 낮음 | Apache 2.0 | Drone 포크, 완전 무료 |
| **Tekton** | ~500MB | ✅ | 중간 | Apache 2.0 | K8s 네이티브, ArgoCD 연동 |
| **Concourse** | ~500MB | ❌ | 중간 | Apache 2.0 | 선언적, 시각화 좋음 |
| **GoCD** | ~1GB | ❌ | 중간 | Apache 2.0 | Value Stream Map |
| **Agola** | ~200MB | ❌ | 낮음 | Apache 2.0 | Gitea 친화적 |
| **Laminar** | ~50MB | ❌ | 매우 낮음 | GPL-3.0 | 초경량, 미니멀 |
| **Buildkite** | ~50MB | ❌ | 낮음 | 상용 | 에이전트만 설치 |
| **Gitea Actions** | 내장 | ❌ | 낮음 | MIT | GitHub Actions 호환 |

### 7.2 경량 도구 비교 (Jenkins 대안)

| 도구 | 메모리 | 설정 복잡도 | 컨테이너 네이티브 | 추천 환경 |
|------|--------|------------|------------------|----------|
| Woodpecker | ~100MB | 낮음 | ✅ | 범용, Gitea |
| Drone | ~100MB | 낮음 | ✅ | 범용 |
| Laminar | ~50MB | 매우 낮음 | ❌ | 단순 빌드 |
| Agola | ~200MB | 낮음 | ✅ | Gitea/Gogs |
| Tekton | ~500MB | 중간 | ✅ | Kubernetes |
| Concourse | ~500MB | 중간 | ✅ | 복잡한 파이프라인 |

---

## 8. 선택 가이드

### 상황별 추천

| 상황 | 추천 도구 |
|------|----------|
| 복잡한 엔터프라이즈 환경 | Jenkins, GitLab CI |
| GitHub 사용 중 | GitHub Actions |
| GitLab 사용 중 | GitLab CI |
| AWS 올인 환경 | AWS CodePipeline + CodeBuild |
| Azure/.NET 환경 | Azure DevOps |
| 가장 가볍게 시작하고 싶다 | Woodpecker, Laminar |
| Kubernetes 환경이다 | Tekton, ArgoCD |
| ArgoCD를 이미 사용 중이다 | Tekton (CI) + ArgoCD (CD) |
| Gitea를 사용 중이다 | Gitea Actions, Woodpecker, Agola |
| 복잡한 파이프라인 시각화가 필요하다 | Concourse, GoCD |
| 관리 부담을 최소화하고 싶다 | GitHub Actions, Buildkite |
| 로컬에서도 파이프라인 테스트하고 싶다 | Dagger |
| 레거시 시스템 연동이 많다 | Jenkins |

### DevOps GUI 플랫폼 연동 시 고려사항

1. **API 품질**: Drone, Woodpecker, Tekton은 REST API가 잘 정리되어 있음
2. **웹훅 지원**: 대부분 지원하나 Laminar는 제한적
3. **상태 조회**: 파이프라인 실행 상태를 외부에서 조회할 수 있는지 확인
4. **인증**: OAuth, API 토큰 등 인증 방식 확인

---

## 9. 참고 링크

### 주요 도구
- Jenkins: https://www.jenkins.io/
- GitHub Actions: https://github.com/features/actions
- GitLab CI: https://docs.gitlab.com/ee/ci/
- ArgoCD: https://argo-cd.readthedocs.io/

### 경량 대안
- Drone CI: https://www.drone.io/
- Woodpecker CI: https://woodpecker-ci.org/
- Tekton: https://tekton.dev/
- Concourse CI: https://concourse-ci.org/
- GoCD: https://www.gocd.org/
- Agola: https://agola.io/
- Laminar: https://laminar.ohwg.net/
- Buildkite: https://buildkite.com/

### 보조 도구
- Dagger: https://dagger.io/
- Task: https://taskfile.dev/

### 클라우드
- AWS CodePipeline: https://aws.amazon.com/codepipeline/
- Azure DevOps: https://azure.microsoft.com/services/devops/
