---
title: Jenkins 전문가 로드맵 — 섹션별 키워드 원문
tags: [moc, jenkins, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# Jenkins 전문가 로드맵 — 섹션별 키워드 원문

---

> "Jenkinsfile 을 잘 쓰는 사람" 에서 멈추지 말고, Jenkins 를 하나의 운영 플랫폼으로 이해해야 합니다. 이 문서는 제공받은 전문가 로드맵 20섹션이 다루는 키워드를 **섹션별로 빠짐없이** 옮긴 원문 기록입니다. 커버 판정·격차는 [README.md](README.md) 의 크로스워크 표가 맡고, 이 문서는 "각 섹션이 원래 무엇을 다루라고 했는가" 의 SSOT 입니다.

## 1. Jenkins 기본 구조

먼저 Jenkins 가 어떻게 움직이는지 알아야 합니다.

### 반드시 알아야 할 개념

| 주제 | 핵심 |
|------|------|
| Controller | Jenkins 의 두뇌. Job 관리, 스케줄링, UI, 설정 저장 |
| Agent / Node | 실제 빌드가 실행되는 작업자 |
| Executor | Agent 안에서 동시에 실행 가능한 작업 슬롯 |
| Workspace | 빌드가 실행되는 디렉터리 |
| Job / Build / Run | 작업 정의와 실행 이력 |
| Queue | 실행 대기열 |
| Label | 특정 Agent 를 선택하는 기준 |
| Plugin | Jenkins 기능 확장 단위 |

깊게 볼 포인트: Controller 는 빌드를 직접 많이 수행하면 안 됩니다. 무거운 작업은 Agent 로 밀어내고, Controller 는 오케스트레이션·상태 관리·UI·스케줄링에 집중해야 합니다.

## 2. Jenkins Pipeline

전문가가 되려면 Freestyle Job 보다 Pipeline as Code 를 중심으로 봐야 합니다.

### 필수 학습

| 주제 | 설명 |
|------|------|
| Declarative Pipeline | `pipeline {}` 기반. 표준화에 좋음 |
| Scripted Pipeline | Groovy 기반. 유연하지만 복잡함 |
| Jenkinsfile | 파이프라인 정의 파일 |
| stage / steps / post | 단계, 실행, 후처리 |
| agent | 어디서 실행할지 결정 |
| environment | 환경 변수 |
| parameters | 파라미터 빌드 |
| when | 조건 분기 |
| input | 수동 승인 |
| parallel | 병렬 실행 |
| retry / timeout | 안정성 제어 |
| stash / unstash | stage 간 파일 전달 |
| archiveArtifacts | 산출물 보관 |
| junit | 테스트 결과 수집 |

Pipeline 의 기본 실행 단위는 `step` 이며, 공식 문서도 step 을 Pipeline 의 가장 기본적인 빌딩 블록으로 설명합니다.

## 3. Jenkinsfile 작성 능력

Jenkinsfile 을 잘 쓰려면 단순 문법보다 운영 중 깨지지 않는 구조를 고민해야 합니다.

좋은 Jenkinsfile 의 기준:

1. 빌드 환경이 재현 가능하다.
2. Credential 이 안전하게 주입된다.
3. 실패 지점이 명확하다.
4. timeout / retry 가 적절하다.
5. 로그가 읽을 수 있다.
6. stage 단위로 원인을 추적할 수 있다.
7. 배포와 빌드가 느슨하게 분리된다.
8. 공통 로직은 Shared Library 로 빠진다.

피해야 할 패턴: `sh "docker login -u ${USER} -p ${PASSWORD}"` 처럼 비밀번호를 직접 넣으면 로그·프로세스 목록에 노출됩니다. `withCredentials` + `--password-stdin` 으로 좁게 감쌉니다. Credential 은 Controller 에 암호화 저장되고 Pipeline 에서는 credential ID 로 다룹니다.

## 4. Shared Library

반복되는 Jenkinsfile 이 많아지면 조직은 무너집니다.

알아야 할 구조: `vars/`, `src/`, `resources/`.

공부할 키워드:

```text
@Library
vars directory
src directory
resources directory
Global Shared Library
Folder-level Library
Trusted Library
Untrusted Library
Script Security Sandbox
libraryResource
```

## 5. Agent 운영

Jenkins 운영의 절반은 Agent 운영입니다.

### Agent 유형

| 방식 | 특징 |
|------|------|
| Static Agent | VM/서버에 상시 Agent 설치 |
| SSH Agent | SSH 로 접속해 실행 |
| Inbound Agent | Agent 가 Controller 로 접속 |
| Docker Agent | 컨테이너 안에서 빌드 |
| Kubernetes Agent | Pod 를 동적으로 생성 |
| Windows Agent | bat/powershell 기반 실행 |

전문가가 봐야 할 질문: 빌드가 Controller 에서 돌고 있지는 않은가 / Agent workspace 가 계속 쌓이고 있지는 않은가 / Agent 별 toolchain 버전이 다르지는 않은가 / 동적 Agent 실패 시 원인을 추적할 수 있는가 / Docker socket 을 Agent 에 그대로 노출하고 있지는 않은가 / Kubernetes Agent Pod template 이 표준화되어 있는가.

## 6. Jenkins 보안

Jenkins 는 CI/CD 도구이지만 실제로는 운영 서버로 가는 문입니다.

### 반드시 알아야 할 보안 영역

| 영역 | 설명 |
|------|------|
| Authentication | 로그인 방식 |
| Authorization | 권한 제어 |
| Matrix Authorization | 사용자/그룹별 권한 |
| Folder 권한 | 팀/프로젝트 단위 격리 |
| Credentials | Secret 관리 |
| Script Approval | Groovy 실행 승인 |
| CSRF Crumb | API 호출 보호 |
| Agent → Controller Security | Agent 가 Controller 를 오염시키지 못하게 제한 |
| Plugin 취약점 | 플러그인 업데이트 관리 |
| Audit Log | 누가 무엇을 변경했는지 추적 |

Jenkins 2.326 부터 Agent-to-Controller 보안 시스템을 비활성화·커스터마이즈할 수 없게 변경됐습니다.

특히 조심할 것: Jenkinsfile 에서 secret echo / sh 문자열에 password 직접 삽입 / Docker socket 마운트 / 과도한 Overall·Administer 권한 / 오래된 플러그인 방치 / Script Console 접근 허용 / Controller 에서 빌드 실행 / Job Configure 권한을 너무 넓게 부여.

## 7. Credential 관리

Credential 을 "그냥 등록해서 쓰는 것" 으로 보면 안 됩니다.

알아야 할 것:

```text
Secret Text
Username with Password
SSH Username with Private Key
Secret File
Certificate
Credentials Scope
System / Global / Folder Scope
withCredentials
credentials() helper
Masking 한계
Credential Binding Plugin
```

Declarative 에서는 `environment` 안 `credentials()` helper 로 secret text·username/password·secret file 을 다룰 수 있습니다. 다만 실무에서는 `environment` 에 오래 두기보다 필요한 stage 에서만 `withCredentials` 로 좁게 감싸는 편이 안전합니다.

## 8. Plugin 관리

Jenkins 는 플러그인으로 숨 쉬지만 플러그인으로 병들기도 합니다.

공부할 것:

```text
Plugin dependency
Plugin compatibility
Plugin security advisory
LTS version compatibility
Update center
Pinned plugin
Detached plugin
Configuration as Code와 plugin catalog
```

운영 원칙: 플러그인은 적게 설치한다 / 설치 이유를 문서화한다 / 업데이트 전 staging Jenkins 에서 검증한다 / LTS 업그레이드와 플러그인 업그레이드를 함께 테스트한다 / 안 쓰는 플러그인은 제거한다.

## 9. Jenkins 운영 관리

전문가가 되려면 장애를 봐야 합니다.

### 주요 운영 주제

| 주제 | 봐야 할 것 |
|------|-----------|
| Backup | `$JENKINS_HOME`, Job config, Credentials, Plugin 목록 |
| Restore | 실제 복구 리허설 |
| Upgrade | LTS 업그레이드 전략 |
| Log | System Log, Build Log, Plugin Log |
| Disk | workspace, builds, artifacts, fingerprints |
| Queue | 대기열 지연 |
| Executor | 병목 |
| Thread dump | 멈춤 분석 |
| Heap dump | 메모리 분석 |
| GC log | JVM 튜닝 |
| Metrics | Prometheus, OpenTelemetry, Jenkins exporter |

중요한 디렉터리: `$JENKINS_HOME/` 아래 `config.xml`, `credentials.xml`, `secrets/`, `jobs/`, `nodes/`, `plugins/`, `users/`, `workspace/`, `builds/`, `logs/`. 백업은 `jobs/` 만으로 부족하고 Credentials 복구에는 `secrets/` 도 필요합니다.

## 10. JVM 튜닝

Jenkins 는 Java 애플리케이션입니다. 결국 JVM 위에서 숨을 쉽니다.

알아야 할 JVM 키워드:

```text
-Xms
-Xmx
G1GC
GC log
Heap dump
Thread dump
Metaspace
Safepoint
OutOfMemoryError
High CPU thread 분석
File descriptor
```

봐야 할 증상: UI 가 느리다 / Queue 가 밀린다 / Build log 가 늦게 열린다 / Plugin update 후 CPU 가 높다 / Full GC 가 자주 발생한다 / Thread 가 BLOCKED 상태로 쌓인다.

## 11. 빌드 도구 이해

Jenkins 는 다른 도구를 조율하는 지휘자입니다.

Java/Spring 기준 필수:

```text
Gradle Lifecycle
Maven Lifecycle
JUnit Report
Jacoco Report
SonarQube
Checkstyle / PMD / SpotBugs
Docker build
Kaniko / BuildKit
Harbor / ECR
SBOM
Trivy / Grype
Artifact Repository
Nexus / Artifactory
```

Spring Boot Pipeline 예시 흐름: Checkout → Compile → Unit Test → Integration Test → Static Analysis → Build JAR → Docker Image Build → Image Scan → Push Registry → Deploy Dev → Smoke Test → Approval → Deploy Prod → Notification.

## 12. Docker / Kubernetes 연동

요즘 Jenkins 전문가는 K8s 를 피해가기 어렵습니다.

알아야 할 것:

```text
Docker in Docker
Docker socket mount
Kaniko
BuildKit
Kubernetes Plugin
Pod Template
ServiceAccount
RBAC
Namespace 분리
ImagePullSecret
PVC Workspace
Ephemeral Agent
Resource requests/limits
Node Selector
Toleration
```

전문가 관점 질문: Pod 가 실패했을 때 로그를 어디서 보는가 / workspace 는 사라져도 되는가 / 캐시는 어디에 둘 것인가 / 빌드 이미지 버전은 고정되어 있는가 / ServiceAccount 권한은 최소 권한인가.

## 13. 배포 전략

Jenkins 가 배포까지 담당한다면 배포 전략도 알아야 합니다.

필수 개념:

```text
Rolling Deployment
Blue-Green Deployment
Canary Deployment
Feature Flag
Manual Approval
Rollback
Smoke Test
Health Check
ArgoCD 연동
Helm
Kustomize
GitOps
```

Jenkins 와 GitOps 의 역할 분리 — Jenkins: 빌드·테스트·이미지 생성·이미지 푸시·manifest 변경 PR 생성 / ArgoCD: Kubernetes 배포 상태 동기화·Drift 감지·Rollback. 운영이 커질수록 GitOps 방식이 추적성·복구에 유리합니다.

## 14. 장애 대응 능력

Jenkins 전문가의 진짜 실력은 장애 때 드러납니다.

### 자주 만나는 장애

| 증상 | 의심 지점 |
|------|----------|
| Queue 가 계속 밀림 | Executor 부족, Label 불일치, Agent offline |
| 빌드가 시작 안 됨 | Node 연결 실패, 권한, SCM checkout 지연 |
| Jenkins UI 느림 | GC, 플러그인, 디스크 I/O |
| 빌드 로그가 끊김 | Agent 연결, 네트워크, Remoting 문제 |
| Credential 안 먹힘 | Scope, ID, Folder 권한 |
| 갑자기 Pipeline 실패 | 플러그인 업데이트, Jenkins LTS 변경 |
| Workspace 오염 | cleanWs 누락, 같은 workspace 공유 |
| Docker build 느림 | 캐시 미사용, 레이어 설계 문제 |
| 디스크 꽉 참 | builds, artifacts, workspace, logs 누적 |

장애 분석 루틴 10단계:

1. Jenkins System Log 확인
2. 해당 Job Build Log 확인
3. Queue / Executor 상태 확인
4. Agent online/offline 확인
5. Disk 사용량 확인
6. 최근 플러그인/설정 변경 확인
7. Thread dump 확인
8. GC log 확인
9. 네트워크/SCM/Registry 상태 확인
10. 재현 가능한 최소 Pipeline 작성

## 15. Jenkins API / 자동화

Jenkins 를 운영 플랫폼으로 쓰려면 API 도 알아야 합니다.

학습 키워드:

```text
Remote Access API
Crumb Issuer
API Token
Build with Parameters
Queue API
Job API
Blue Ocean API
Webhook
Generic Webhook Trigger
GitHub/GitLab Webhook
Jenkins CLI
Script Console
```

CSRF 보호가 켜져 있으면 Crumb 처리가 필요할 수 있습니다.

## 16. 성능과 스케일링

Jenkins 가 커지면 가장 먼저 봐야 할 것은 Controller 부하입니다.

체크리스트:

```text
Controller에서 빌드하지 않는다.
Agent를 동적으로 확장한다.
Job 수와 View를 정리한다.
Build discard policy를 설정한다.
Artifact 보관 기간을 제한한다.
불필요한 플러그인을 제거한다.
SCM polling을 줄이고 webhook 기반으로 전환한다.
무거운 Groovy 로직을 Pipeline에 넣지 않는다.
Shared Library도 과도하게 복잡하게 만들지 않는다.
```

## 17. 전문가 로드맵 (숙련도 단계)

1단계 사용자 수준:

```text
Jenkins UI 사용
Job 생성
빌드 실행
로그 확인
파라미터 빌드
간단한 Jenkinsfile 작성
```

2단계 Pipeline 작성자:

```text
Declarative Pipeline
stage/post/when/parallel
credentials 사용
junit/archiveArtifacts
Docker build/push
배포 stage 작성
```

3단계 팀 표준화 담당자:

```text
Shared Library
공통 Jenkinsfile 템플릿
빌드/배포 표준화
Credential scope 설계
폴더 권한 설계
Notification 표준화
```

4단계 Jenkins 운영자:

```text
Controller/Agent 구조 설계
Plugin 관리
Backup/Restore
Upgrade
JVM 튜닝
Queue/Executor 분석
Kubernetes Agent 운영
보안 정책 관리
```

5단계 CI/CD 플랫폼 엔지니어:

```text
GitOps 연동
멀티 테넌시
동적 Agent
표준 빌드 이미지
품질 게이트
SBOM/취약점 스캔
감사 로그
OpenTelemetry/Prometheus 연동
대규모 Job 운영
내부 Developer Platform 연계
```

## 18. 실무 기준 학습 프로젝트

프로젝트 1 — Spring Boot CI Pipeline:

```text
Git checkout
Gradle build
JUnit report
Jacoco report
SonarQube 분석
JAR archive
```

프로젝트 2 — Docker Image Pipeline:

```text
Dockerfile 작성
이미지 빌드
태그 전략
Harbor push
취약점 스캔
build cache 최적화
```

프로젝트 3 — Kubernetes 배포 Pipeline:

```text
K8s Agent Pod
Kaniko build
Helm deploy
Smoke test
Rollback
```

프로젝트 4 — Shared Library:

```text
buildJavaApp()
buildDockerImage()
deployHelm()
notifyResult()
withQualityGate()
```

프로젝트 5 — Jenkins 운영 자동화:

```text
Job DSL
Configuration as Code
Backup/Restore 스크립트
Plugin 목록 관리
권한 매트릭스 설계
```

## 19. 핵심 키워드만 압축

```text
Jenkins Controller/Agent Architecture
Executor, Node, Label, Workspace
Queue Scheduling
Declarative Pipeline
Scripted Pipeline
Jenkinsfile
Pipeline Step, Stage, Post, When, Parallel
Credential Binding
withCredentials
Secret Masking Limitations
Shared Library
vars/src/resources 구조
Trusted vs Untrusted Library
Script Security Sandbox
Plugin Dependency Management
Jenkins LTS Upgrade
Backup and Restore of JENKINS_HOME
Controller JVM Tuning
GC Log, Heap Dump, Thread Dump
Agent-to-Controller Security
Matrix Authorization
Folder-based Permission
CSRF Crumb
Webhook Trigger
Remote Access API
Kubernetes Plugin
Ephemeral Agent
Pod Template
Docker Socket Risk
Kaniko / BuildKit
Artifact Management
JUnit / Jacoco / SonarQube
Build Discard Policy
Workspace Cleanup
Pipeline Retry / Timeout
Manual Approval
Blue-Green / Canary / Rolling Deployment
GitOps with ArgoCD
Observability: Metrics, Logs, Traces
Jenkins Shared Library Testing
Job DSL
Configuration as Code
```

## 20. 가장 중요한 결론

Jenkins 전문가는 세 부류의 능력을 함께 가져야 합니다.

1. Pipeline 을 잘 작성하는 능력
2. Jenkins 를 안정적으로 운영하는 능력
3. 조직의 CI/CD 표준을 설계하는 능력

Jenkins 는 오래된 도구처럼 보이지만 제대로 다루면 여전히 강력합니다. 다만 그 힘은 날카로운 칼과 같아서, Pipeline 몇 줄로 끝나는 도구가 아니라 권한·Secret·Agent·Plugin·JVM·배포 전략이 얽힌 운영 시스템으로 바라봐야 합니다.

## 출처

- [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- [Extending with Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- [Agent → Controller Security Changes in 2.326](https://www.jenkins.io/doc/book/security/controller-isolation/jep-235/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
