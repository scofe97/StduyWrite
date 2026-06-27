---
title: CI/CD 공통 개념 로드맵 — 도구를 관통하는 키워드 원문
tags: [moc, cicd, ci-cd, roadmap, keywords, jenkins, woodpecker, concourse, tekton, argo, rundeck, dagger]
status: reference
related:
  - README.md
updated: 2026-06-28
---

# CI/CD 공통 개념 로드맵 — 도구를 관통하는 키워드 원문

---

> Jenkins, Woodpecker, Concourse, Rundeck, Tekton, Argo Workflows, Argo CD, Forgejo/Gitea Actions, Dagger 같은 도구들을 관통하는 공통 개념을 **빠짐없이** 옮긴 원문 기록입니다. 도구별 심화는 각 도구 폴더(`02_Jenkins/` 등)가 맡고, 이 문서는 "도구 이름이 바뀌어도 남는 것"의 SSOT입니다. 핵심은 하나입니다 — CI/CD 도구는 결국 "무엇을, 언제, 어디서, 어떤 권한으로, 어떤 순서로 실행하고, 그 결과를 어떻게 기록하고 다음 단계로 넘길 것인가"를 다루는 시스템입니다.

핵심은 하나입니다.

```text
CI/CD 도구는 결국
“무엇을, 언제, 어디서, 어떤 권한으로, 어떤 순서로 실행하고,
그 결과를 어떻게 기록하고 다음 단계로 넘길 것인가”
를 다루는 시스템이다.
```

---

# 1. 큰 지도

먼저 전체 구조를 이렇게 잡으면 좋습니다.

```text
CI/CD 시스템 공통 구조

사용자 / Git / Webhook / API
        ↓
Trigger
        ↓
Pipeline Definition
        ↓
Scheduler / Queue
        ↓
Runner / Agent / Worker
        ↓
Step / Task 실행
        ↓
Artifact / Image / Report 생성
        ↓
Deploy Target 반영
        ↓
Log / Status / Audit / Notification
```

도구마다 이름은 다르지만 뼈대는 거의 같습니다.

| 공통 개념 | Jenkins               | Woodpecker        | Concourse         | Tekton              | Rundeck           | Argo CD        |
| ----- | --------------------- | ----------------- | ----------------- | ------------------- | ----------------- | -------------- |
| 실행 정의 | Job / Jenkinsfile     | Pipeline YAML     | Pipeline YAML     | Pipeline / Task     | Job               | Application    |
| 실행 단위 | Stage / Step          | Step              | Job / Task / Step | TaskRun / Step      | Step / Node Step  | Sync Operation |
| 실행 노드 | Agent                 | Agent             | Worker            | Pod                 | Node / Runner     | Controller     |
| 수동 실행 | Build with Parameters | Manual/CLI/API 계열 | Trigger Job       | PipelineRun 생성      | Run Job + Options | Sync           |
| 변수    | Parameters / env      | env / secrets     | vars / params     | params / workspaces | options           | parameters는 약함 |
| 산출물   | Artifact              | Artifact / volume | Resource output   | Result / Workspace  | Log / output      | Desired state  |
| 배포    | shell/plugin          | shell/image       | task/resource     | task/pod            | command/plugin    | GitOps sync    |

---

# 2. Control Plane / Data Plane

## 개념

CI/CD 시스템은 보통 두 부분으로 나뉩니다.

```text
Control Plane
  - 작업을 받는다
  - 큐에 넣는다
  - 상태를 관리한다
  - 로그와 결과를 저장한다
  - 권한을 판단한다

Data Plane
  - 실제 명령을 실행한다
  - build/test/deploy를 수행한다
  - Docker, kubectl, ssh, gradle 등을 실행한다
```

Jenkins로 보면:

```text
Jenkins Controller = Control Plane
Jenkins Agent      = Data Plane
```

Woodpecker로 보면:

```text
Woodpecker Server = Control Plane
Woodpecker Agent  = Data Plane
```

Kubernetes 계열로 보면:

```text
Controller = Control Plane
Pod        = Data Plane
```

## 학습 키워드

| 키워드         | 설명                                      |
| ----------- | --------------------------------------- |
| Controller  | 전체 작업 상태를 조율하는 중심                       |
| Server      | UI/API/Queue/DB를 가진 서버                  |
| Agent       | 실제 job을 수행하는 실행자                        |
| Runner      | GitHub Actions/Gitea/Forgejo 계열의 실행자    |
| Worker      | Concourse 계열의 실행자                       |
| Executor    | 구체적인 실행 방식. shell, docker, kubernetes 등 |
| Queue       | 실행 대기열                                  |
| Scheduler   | 어떤 runner에게 작업을 줄지 결정                   |
| Heartbeat   | runner가 살아 있는지 확인                       |
| Lease       | runner에게 작업을 임시 할당하는 권한                 |
| Concurrency | 동시에 실행 가능한 작업 수                         |

## 토이프로젝트 구현 아이디어

처음에는 이렇게 만들면 됩니다.

```text
ci-server
  ├─ POST /jobs/{jobId}/run
  ├─ job_run 테이블에 PENDING 저장
  ├─ worker가 polling
  ├─ RUNNING으로 변경
  ├─ shell command 실행
  └─ SUCCESS/FAILED 저장
```

핵심 DB 모델:

```sql
job
job_run
job_step_run
runner
runner_heartbeat
```

---

# 3. Pipeline Definition

## 개념

Pipeline Definition은 “무엇을 어떤 순서로 실행할지”를 정의한 문서입니다.

예를 들면:

```yaml
pipeline:
  stages:
    - build
    - test
    - package
    - deploy
```

Jenkins는 Jenkinsfile, Woodpecker/Concourse/Tekton은 YAML, Dagger는 코드, Rundeck은 Job 정의를 사용합니다.

## 핵심 구성요소

| 개념       | 설명                                         |
| -------- | ------------------------------------------ |
| Pipeline | 전체 자동화 흐름                                  |
| Workflow | Pipeline과 비슷한 말. GitHub Actions 계열에서 자주 사용 |
| Stage    | 논리적 구간. build/test/deploy                  |
| Job      | 독립 실행 단위                                   |
| Step     | 실제 명령 실행 단위                                |
| Task     | 재사용 가능한 실행 단위                              |
| Command  | shell command                              |
| Script   | 여러 command 묶음                              |
| DAG      | 순차가 아니라 의존성 그래프로 실행                        |
| Matrix   | 여러 버전/환경 조합으로 반복 실행                        |

## 순차 Pipeline

```text
build → test → docker-build → deploy
```

## DAG Pipeline

```text
          ┌─ unit-test
build ────┤
          └─ integration-test
                  ↓
              docker-build
                  ↓
                deploy
```

## 학습 키워드

| 키워드                 | 중요도 | 설명                        |
| ------------------- | --: | ------------------------- |
| Sequential Pipeline |  높음 | 가장 기본적인 순차 실행             |
| DAG Execution       |  높음 | 병렬 실행, 의존성 처리             |
| Fan-out             |  중간 | 하나의 작업이 여러 작업으로 분기        |
| Fan-in              |  중간 | 여러 작업 완료 후 하나로 합류         |
| Conditional Step    |  높음 | 조건부 실행                    |
| Failure Strategy    |  높음 | 실패 시 중단/계속/재시도            |
| Matrix Build        |  중간 | JDK 17/21, OS별 테스트        |
| Template            |  높음 | 공통 pipeline 재사용           |
| Reusable Task       |  높음 | build, deploy 같은 task 재사용 |

## 토이프로젝트 구현 아이디어

처음에는 순차 실행만 구현합니다.

```yaml
name: spring-api-deploy

steps:
  - name: build
    command: "./gradlew clean build"

  - name: test
    command: "./gradlew test"

  - name: deploy
    command: "ssh app01 'systemctl restart app'"
```

그 다음 DAG를 추가합니다.

```yaml
steps:
  - name: build
  - name: unit-test
    needs: [build]
  - name: integration-test
    needs: [build]
  - name: package
    needs: [unit-test, integration-test]
```

---

# 4. Trigger

## 개념

Trigger는 Pipeline을 시작시키는 사건입니다.

```text
Git push
PR 생성
Tag 생성
수동 버튼 클릭
스케줄
Webhook
API 호출
외부 이벤트
```

## Trigger 종류

| Trigger               | 설명                | 예시            |
| --------------------- | ----------------- | ------------- |
| Manual Trigger        | 사용자가 버튼으로 실행      | 운영 배포         |
| Parameterized Trigger | 입력값을 받아 실행        | version=1.2.3 |
| Git Push Trigger      | commit push 시 실행  | CI            |
| PR/MR Trigger         | Pull Request 검증   | 리뷰 전 테스트      |
| Tag Trigger           | release tag 기준 실행 | 운영 배포         |
| Schedule Trigger      | cron 기반 실행        | 매일 새벽 배치      |
| Webhook Trigger       | 외부 시스템 호출         | Jira 승인 후 배포  |
| API Trigger           | REST API로 실행      | 사내 포털에서 실행    |
| Registry Trigger      | image push 감지     | image scan    |
| Event Trigger         | Kafka/Event 기반    | 배포 이벤트 후속 처리  |

## Jenkins의 Build with Parameters와 대응되는 개념

```text
Manual Trigger
+ Input Parameters
+ Default Value
+ Choice Parameter
+ Boolean Parameter
+ Secret Parameter
+ Validation
```

## 학습 키워드

| 키워드                     | 설명                               |
| ----------------------- | -------------------------------- |
| Event Source            | 이벤트 발생지                          |
| Webhook Receiver        | webhook 수신 API                   |
| Debounce                | 짧은 시간에 여러 이벤트가 들어올 때 합치기         |
| Idempotency Key         | 같은 이벤트 중복 실행 방지                  |
| Manual Approval         | 사람이 승인해야 다음 단계 진행                |
| Trigger Policy          | 어떤 branch/tag/environment에서 실행할지 |
| Dry Run                 | 실제 배포 없이 검증만 수행                  |
| Re-run                  | 실패한 작업 재실행                       |
| Re-run from Failed Step | 실패 지점부터 재실행                      |

## 토이프로젝트 구현 아이디어

처음에는 세 가지 trigger만 구현해도 충분합니다.

```text
1. 수동 실행
2. Webhook 실행
3. Cron 실행
```

API 예시:

```http
POST /pipelines/{id}/runs
Content-Type: application/json

{
  "params": {
    "targetEnv": "dev",
    "version": "1.0.3",
    "deployType": "vm"
  }
}
```

---

# 5. Parameter / Variable / Input

## 개념

Parameter는 실행 시 외부에서 넣는 값입니다.
Variable은 pipeline 내부에서 쓰이는 값입니다.

```text
Parameter:
  사용자가 입력한다.

Variable:
  시스템이나 pipeline이 계산하거나 주입한다.
```

예:

```text
SERVICE_NAME=order-api
TARGET_ENV=prod
VERSION=1.2.3
DEPLOY_TYPE=k8s
IMAGE_TAG=20260627-a1b2c3
```

## Parameter 종류

| 종류           | 설명         | 예시                     |
| ------------ | ---------- | ---------------------- |
| String       | 문자열        | version                |
| Choice       | 선택값        | dev/stg/prod           |
| Boolean      | true/false | restart=true           |
| Number       | 숫자         | replica=3              |
| Secret       | 민감값        | token                  |
| File         | 파일 입력      | kubeconfig, env file   |
| Multi Select | 여러 값 선택    | targets=[app01, app02] |
| JSON         | 복잡한 입력     | deployment config      |

## 중요한 설계 포인트

파라미터는 단순 입력값처럼 보이지만, 운영에서는 사고의 문이 됩니다.

| 항목  | 고려사항                        |
| --- | --------------------------- |
| 검증  | prod 배포 시 version 필수        |
| 권한  | prod는 특정 사용자만 가능            |
| 기본값 | dev를 기본값으로 둘지               |
| 선택값 | target server 목록을 동적으로 가져올지 |
| 마스킹 | secret이 로그에 노출되지 않게         |
| 감사  | 누가 어떤 값으로 실행했는지             |
| 재현성 | 같은 값으로 다시 실행 가능한지           |

## 토이프로젝트 구현 아이디어

Parameter Schema를 먼저 만듭니다.

```json
{
  "parameters": [
    {
      "name": "targetEnv",
      "type": "choice",
      "required": true,
      "options": ["dev", "stg", "prod"]
    },
    {
      "name": "version",
      "type": "string",
      "required": true
    },
    {
      "name": "restart",
      "type": "boolean",
      "default": true
    }
  ]
}
```

---

# 6. Secret / Credential

## 개념

CI/CD는 거의 항상 외부 시스템의 열쇠를 다룹니다.

```text
Git token
Docker registry password
SSH private key
Kubeconfig
Cloud access key
Database migration credential
Slack webhook
Vault token
```

## 핵심 키워드

| 키워드                | 설명                                             |
| ------------------ | ---------------------------------------------- |
| Secret Store       | 민감값 저장소                                        |
| Credential Binding | 실행 시 secret을 환경 변수나 파일로 주입                     |
| Masking            | 로그에서 secret을 숨김                                |
| Rotation           | secret 주기적 교체                                  |
| Scoped Secret      | 특정 project/environment에서만 사용                   |
| Protected Secret   | protected branch/tag에서만 사용                     |
| External Secret    | Vault, AWS Secrets Manager, K8s Secret 등 외부 연동 |
| Short-lived Token  | 짧은 수명의 토큰                                      |
| OIDC               | 장기 secret 없이 identity 기반 인증                    |
| Least Privilege    | 최소 권한                                          |

## 주의할 점

가장 흔한 사고는 이것입니다.

```text
echo $TOKEN
kubectl config view
docker login 명령 로그 노출
ssh key 파일 권한 오류
prod kubeconfig를 dev job에서도 사용
```

## 토이프로젝트 구현 아이디어

Secret은 처음부터 암호화까지 완벽히 하려 하지 말고, 개념을 분리합니다.

```text
secret metadata
  - name
  - scope
  - created_by

secret value
  - encrypted_value
```

실행 시에는 이렇게 주입합니다.

```text
step.environment:
  REGISTRY_PASSWORD = fromSecret("harbor-password")
```

---

# 7. Runner / Agent / Worker

## 개념

Runner는 실제 명령을 실행하는 실행자입니다.

```text
서버는 명령하지,
직접 땀 흘려 빌드하지 않는다.
```

좋은 CI/CD 구조는 서버와 실행자를 분리합니다.

```text
Server
  ↓
Queue
  ↓
Runner
  ↓
Shell / Docker / Kubernetes Pod
```

## Runner 실행 방식

| 방식                | 설명             | 장점           | 단점                  |
| ----------------- | -------------- | ------------ | ------------------- |
| Shell Runner      | 호스트 OS에서 직접 실행 | 단순, VM 배포 편함 | 격리 약함               |
| Docker Runner     | 컨테이너에서 실행      | 재현성 좋음       | Docker daemon 보안 주의 |
| Kubernetes Runner | Pod로 실행        | 확장성 좋음       | K8s 지식 필요           |
| SSH Runner        | 원격 서버에 접속해 실행  | VM 배포에 좋음    | credential 관리 필요    |
| Ephemeral Runner  | 실행 후 폐기        | 보안 좋음        | 준비 비용 있음            |

## 핵심 키워드

| 키워드                 | 설명                              |
| ------------------- | ------------------------------- |
| Runner Registration | runner를 server에 등록              |
| Runner Token        | runner 인증 토큰                    |
| Label / Tag         | 어떤 job을 어떤 runner가 받을지          |
| Capability          | runner가 docker/kubectl 등을 지원하는지 |
| Workspace Cleanup   | 실행 후 작업 디렉터리 삭제                 |
| Isolation Boundary  | 실행 격리 경계                        |
| Ephemeral Execution | 매번 깨끗한 환경에서 실행                  |
| Runner Pool         | 여러 runner 묶음                    |
| Autoscaling Runner  | 부하에 따라 runner 증가                |
| Heartbeat           | runner 생존 체크                    |

## 토이프로젝트 구현 아이디어

runner가 server를 polling하는 구조부터 시작합니다.

```text
runner → GET /runs/next?label=linux
server → job_run 반환
runner → 실행
runner → PATCH /runs/{id}/status
```

나중에 server가 runner로 push하는 구조를 고민해도 됩니다.

---

# 8. Executor

## 개념

Executor는 runner가 실제로 작업을 실행하는 방식입니다.

```text
Runner는 사람이고,
Executor는 손에 든 도구다.
```

## Executor 종류

| Executor                | 설명             | 적합한 작업            |
| ----------------------- | -------------- | ----------------- |
| Shell Executor          | local shell 실행 | VM 배포, 간단한 script |
| Docker Executor         | container에서 실행 | build/test        |
| Kubernetes Executor     | pod로 실행        | 대규모 CI, 격리        |
| SSH Executor            | 원격 host 실행     | VM 운영 작업          |
| Docker Compose Executor | compose 환경 구성  | 통합 테스트            |
| Firecracker/MicroVM     | microVM 격리     | 보안 강화             |
| Nomad Executor          | Nomad job 실행   | Nomad 환경          |

## 설계 포인트

| 항목  | 질문                           |
| --- | ---------------------------- |
| 격리성 | job 간 파일/환경이 섞이지 않는가?        |
| 성능  | 매번 image pull 비용이 큰가?        |
| 보안  | untrusted code를 실행해도 되는가?    |
| 캐시  | dependency cache를 어떻게 공유할까?  |
| 로그  | stdout/stderr를 어떻게 수집할까?     |
| 종료  | timeout/interrupt를 어떻게 처리할까? |

## 토이프로젝트 구현 순서

```text
1. Shell Executor
2. Docker Executor
3. SSH Executor
4. Kubernetes Executor
```

처음부터 Kubernetes Executor를 만들면 배가 산으로 갑니다.
먼저 shell로 작은 불씨를 만들고, 그 다음 컨테이너라는 화덕을 얹는 편이 좋습니다.

---

# 9. Workspace

## 개념

Workspace는 pipeline이 작업하는 디렉터리입니다.

```text
checkout된 source
build 결과물
test report
임시 파일
artifact
```

Jenkins에서 `workspace`, Tekton에서 `workspace`, GitHub Actions에서 working directory 등이 같은 계열입니다.

## 핵심 키워드

| 키워드                  | 설명                  |
| -------------------- | ------------------- |
| Checkout             | Git source 가져오기     |
| Working Directory    | 명령 실행 기준 디렉터리       |
| Clean Workspace      | 이전 파일 제거            |
| Persistent Workspace | step 간 파일 공유        |
| Ephemeral Workspace  | 실행 후 삭제             |
| Volume Mount         | 컨테이너 간 파일 공유        |
| PVC                  | K8s에서 workspace 보존  |
| Cache Directory      | dependency cache 저장 |
| Artifact Directory   | 산출물 저장              |

## 주의할 점

```text
이전 빌드 산출물이 남아서 테스트가 통과하는 경우
secret 파일이 workspace에 남는 경우
Docker build context에 불필요한 파일이 들어가는 경우
step 간 workspace 공유가 안 되는 경우
```

## 토이프로젝트 구현 아이디어

각 job run마다 workspace를 분리합니다.

```text
/workspaces/{pipelineRunId}/
  ├─ source/
  ├─ artifacts/
  ├─ logs/
  └─ tmp/
```

실행 후 정책을 둡니다.

```text
성공 후 삭제
실패 시 7일 보존
artifact는 별도 저장소로 이동
```

---

# 10. Artifact / Report

## 개념

Artifact는 pipeline이 만든 결과물입니다.

```text
JAR
WAR
Docker image metadata
test report
coverage report
SBOM
deployment manifest
log bundle
```

## Artifact 종류

| 종류                     | 예시                    |
| ---------------------- | --------------------- |
| Build Artifact         | app.jar, app.war      |
| Test Report            | JUnit XML             |
| Coverage Report        | Jacoco report         |
| Static Analysis Report | Sonar result          |
| Package                | zip, tar.gz           |
| Container Image        | OCI image             |
| SBOM                   | CycloneDX, SPDX       |
| Provenance             | SLSA attestation      |
| Deployment Manifest    | Helm values, K8s YAML |

## 핵심 키워드

| 키워드                  | 설명                         |
| -------------------- | -------------------------- |
| Artifact Store       | 산출물 저장소                    |
| Retention Policy     | 보관 기간                      |
| Promotion            | dev artifact를 stg/prod로 승격 |
| Immutable Artifact   | 한 번 만든 산출물을 바꾸지 않음         |
| Artifact Fingerprint | 산출물 식별자                    |
| Checksum             | 무결성 확인                     |
| Digest               | OCI image 불변 식별자           |
| Provenance           | 산출물 생성 출처                  |
| SBOM                 | 의존성 목록                     |

## 중요한 원칙

```text
운영 배포 시 다시 빌드하지 않는다.
이미 검증된 artifact를 승격한다.
```

나쁜 흐름:

```text
dev build
stg에서 다시 build
prod에서 다시 build
```

좋은 흐름:

```text
build once
test once
promote same artifact
```

---

# 11. Cache

## 개념

Cache는 반복 빌드 시간을 줄이는 장치입니다.

```text
Gradle cache
Maven repository
npm cache
Docker layer cache
Go build cache
pip cache
```

## 핵심 키워드

| 키워드                | 설명                    |
| ------------------ | --------------------- |
| Dependency Cache   | 의존성 다운로드 재사용          |
| Build Cache        | 컴파일 결과 재사용            |
| Docker Layer Cache | image layer 재사용       |
| Remote Cache       | 여러 runner가 공유하는 cache |
| Cache Key          | cache 식별 기준           |
| Cache Invalidation | cache 무효화             |
| Cache Poisoning    | 악의적/오염된 cache 사용      |
| Read-only Cache    | 보안 강화용 cache          |

## 토이프로젝트 실습

Spring Boot 기준:

```text
1. Gradle cache 없는 빌드 시간 측정
2. Gradle cache 추가
3. Docker layer cache 추가
4. cache key를 build.gradle 기준으로 변경
```

---

# 12. Image Build / Registry

## 개념

컨테이너 시대의 CI/CD는 대부분 image를 중심으로 움직입니다.

```text
source code
  ↓
build artifact
  ↓
container image
  ↓
registry push
  ↓
VM/K8s deploy
```

## 핵심 키워드

| 키워드                | 설명                               |
| ------------------ | -------------------------------- |
| OCI Image          | 표준 컨테이너 이미지 형식                   |
| Dockerfile         | image build 정의                   |
| BuildKit           | 고급 image build 엔진                |
| Kaniko             | Docker daemon 없이 image build     |
| Buildpacks         | Dockerfile 없이 app image 생성       |
| Registry           | image 저장소                        |
| Harbor             | 대표적인 사내 registry                 |
| Image Tag          | 사람이 읽는 버전 라벨                     |
| Image Digest       | 불변 image 식별자                     |
| Image Pull Secret  | private registry 인증              |
| Vulnerability Scan | image 취약점 스캔                     |
| Image Promotion    | dev registry에서 prod registry로 승격 |

## 태그 전략

```text
나쁜 예:
latest

좋은 예:
order-api:1.2.3
order-api:20260627-1430
order-api:git-a1b2c3d
order-api:1.2.3-git-a1b2c3d
```

운영에서는 digest를 같이 기록하는 것이 좋습니다.

```text
image: harbor.local/order-api:1.2.3
digest: sha256:...
```

---

# 13. Deployment Target

## 개념

CI/CD에서 배포 대상은 크게 세 가지입니다.

```text
1. VM
2. Container Runtime
3. Kubernetes
```

## VM 배포

키워드:

| 키워드                | 설명                |
| ------------------ | ----------------- |
| SSH                | 원격 접속             |
| SCP/RSYNC          | 파일 전송             |
| systemd            | 서비스 관리            |
| Tomcat             | WAR 배포            |
| Nginx              | reverse proxy     |
| Health Check       | 배포 후 확인           |
| Rollback Directory | 이전 버전 보관          |
| Symlink Deploy     | current 심볼릭 링크 교체 |
| Blue-Green on VM   | 포트/디렉터리 교체        |
| Ansible            | VM 작업 표준화         |

흐름:

```text
build jar
  ↓
scp app.jar
  ↓
systemctl stop
  ↓
replace jar
  ↓
systemctl start
  ↓
health check
```

## Container 배포

키워드:

| 키워드                      | 설명             |
| ------------------------ | -------------- |
| Docker Compose           | VM 위 컨테이너 배포   |
| Docker Context           | 원격 Docker host |
| Container Restart Policy | 재시작 정책         |
| Network                  | 컨테이너 네트워크      |
| Volume                   | 데이터 볼륨         |
| Image Pull               | 새 image 가져오기   |
| Compose Project          | 서비스 묶음         |
| Rolling Compose          | 직접 구현 필요       |

흐름:

```text
docker pull
docker compose up -d
docker compose ps
health check
```

## Kubernetes 배포

키워드:

| 키워드            | 설명                  |
| -------------- | ------------------- |
| Deployment     | 무상태 app 배포          |
| StatefulSet    | 상태 있는 app           |
| Service        | 네트워크 진입점            |
| Ingress        | HTTP 라우팅            |
| ConfigMap      | 설정                  |
| Secret         | 민감 설정               |
| Namespace      | 격리 단위               |
| ServiceAccount | Pod 권한              |
| RBAC           | 권한                  |
| Rollout        | 점진 교체               |
| Helm           | chart 기반 배포         |
| Kustomize      | overlay 기반 manifest |
| Argo CD        | GitOps sync         |
| Argo Rollouts  | canary/blue-green   |

흐름:

```text
image push
  ↓
manifest image tag 변경
  ↓
kubectl apply / helm upgrade
  ↓
rollout status
  ↓
health check
```

---

# 14. Environment / Promotion

## 개념

CI/CD는 환경을 다룹니다.

```text
local
dev
qa
stg
prod
```

단순히 서버 주소만 다른 것이 아닙니다.
권한, 승인, secret, replica, resource, 배포 전략이 모두 달라집니다.

## 핵심 키워드

| 키워드                   | 설명                        |
| --------------------- | ------------------------- |
| Environment           | dev/stg/prod              |
| Promotion             | 다음 환경으로 승격                |
| Approval Gate         | 승격 전 승인                   |
| Freeze Window         | 배포 금지 시간                  |
| Environment Lock      | 같은 환경 동시 배포 방지            |
| Config Drift          | 환경 간 설정 차이                |
| Variable Scope        | 환경별 변수                    |
| Secret Scope          | 환경별 secret                |
| Progressive Promotion | dev → stg → canary → prod |

## 좋은 흐름

```text
build once
  ↓
dev deploy
  ↓
stg promotion
  ↓
approval
  ↓
prod deploy
```

## 토이프로젝트 구현 아이디어

배포 환경 테이블을 둡니다.

```sql
environment
- id
- name
- type
- requires_approval
- deploy_strategy
- locked
```

---

# 15. Approval / Gate

## 개념

Gate는 다음 단계로 넘어가기 전 멈추는 지점입니다.

```text
build
  ↓
test
  ↓
approval gate
  ↓
prod deploy
```

## Gate 종류

| 종류                 | 설명             |
| ------------------ | -------------- |
| Manual Approval    | 사람이 승인         |
| Quality Gate       | 테스트/정적분석 기준 충족 |
| Security Gate      | 취약점 기준 충족      |
| Change Ticket Gate | 변경관리 티켓 승인     |
| Time Window Gate   | 배포 가능 시간 확인    |
| Dependency Gate    | 다른 시스템 상태 확인   |
| Observability Gate | 배포 후 지표 확인     |

## 학습 키워드

| 키워드                  | 설명            |
| -------------------- | ------------- |
| Approver             | 승인자           |
| Approval Policy      | 승인 규칙         |
| Separation of Duties | 요청자와 승인자 분리   |
| Timeout              | 일정 시간 후 자동 만료 |
| Reject               | 반려            |
| Re-approve           | 수정 후 재승인      |
| Audit                | 승인 이력         |
| Change Management    | 변경관리 연동       |

## 토이프로젝트 구현 아이디어

```text
deploy-prod step 전에 WAITING_APPROVAL 상태로 멈춤
승인 API 호출 시 다음 step 실행
반려 시 pipeline FAILED 또는 REJECTED
```

상태:

```text
PENDING
RUNNING
WAITING_APPROVAL
APPROVED
REJECTED
SUCCESS
FAILED
```

---

# 16. Deployment Strategy

## 개념

배포는 단순히 새 버전을 올리는 일이 아닙니다.
트래픽과 위험을 어떻게 다룰지의 문제입니다.

## 전략

| 전략             | 설명                |   난이도 |
| -------------- | ----------------- | ----: |
| Recreate       | 기존 종료 후 새 버전 시작   |    낮음 |
| Rolling Update | 순차 교체             |    중간 |
| Blue-Green     | 두 환경 중 하나로 전환     |    중간 |
| Canary         | 일부 트래픽만 신규 버전     |    높음 |
| Shadow         | 실제 트래픽 복제, 응답은 버림 |    높음 |
| A/B Test       | 사용자 그룹별 분기        |    높음 |
| Feature Flag   | 배포와 기능 공개 분리      | 중간~높음 |

## 핵심 키워드

| 키워드                  | 설명           |
| -------------------- | ------------ |
| Rollout              | 새 버전 반영 과정   |
| Rollback             | 이전 버전 복구     |
| Traffic Shifting     | 트래픽 비율 조정    |
| Health Probe         | 정상성 검사       |
| Readiness Probe      | 트래픽 받을 준비 여부 |
| Liveness Probe       | 살아 있는지       |
| Analysis             | 메트릭 기반 판단    |
| Error Budget         | 허용 가능한 실패 범위 |
| SLO                  | 서비스 목표       |
| Progressive Delivery | 점진 배포        |

---

# 17. State Machine

## 개념

CI/CD 시스템은 상태 기계입니다.

```text
PENDING
  ↓
QUEUED
  ↓
RUNNING
  ↓
SUCCESS / FAILED / CANCELED
```

배포와 승인을 포함하면 더 복잡해집니다.

```text
CREATED
  ↓
VALIDATING
  ↓
QUEUED
  ↓
RUNNING
  ↓
WAITING_APPROVAL
  ↓
DEPLOYING
  ↓
VERIFYING
  ↓
SUCCESS
```

## 핵심 상태

| 상태               | 의미         |
| ---------------- | ---------- |
| CREATED          | 실행 요청 생성   |
| PENDING          | 아직 준비 전    |
| QUEUED           | 실행 대기      |
| ASSIGNED         | runner에 할당 |
| RUNNING          | 실행 중       |
| WAITING_APPROVAL | 승인 대기      |
| SKIPPED          | 조건에 의해 건너뜀 |
| SUCCESS          | 성공         |
| FAILED           | 실패         |
| CANCELED         | 사용자 취소     |
| TIMEOUT          | 제한시간 초과    |
| UNKNOWN          | 상태 확인 불가   |

## 토이프로젝트에서 중요한 것

상태 전이를 막아야 합니다.

```text
SUCCESS → RUNNING 불가
FAILED → RUNNING 불가, 단 retry는 새 run 생성
WAITING_APPROVAL → SUCCESS 불가
```

상태 전이 테이블을 명시하면 좋습니다.

---

# 18. Retry / Timeout / Cancel

## 개념

실패는 예외가 아니라 정상 경로입니다.

CI/CD는 반드시 실패를 다뤄야 합니다.

## 핵심 키워드

| 키워드                    | 설명               |
| ---------------------- | ---------------- |
| Retry                  | 재시도              |
| Max Retry              | 최대 재시도 횟수        |
| Backoff                | 재시도 간격 증가        |
| Exponential Backoff    | 지수 증가            |
| Timeout                | 최대 실행 시간         |
| Cancellation           | 사용자 취소           |
| Interrupt              | 실행 중인 process 중단 |
| Graceful Stop          | 안전한 종료           |
| Force Kill             | 강제 종료            |
| Retry from Failed Step | 실패 step부터 재시작    |
| Idempotent Step        | 재실행해도 안전한 step   |

## 배포에서 재시도 주의

빌드는 재시도해도 비교적 안전합니다.

```text
./gradlew build
```

하지만 배포는 재시도 시 위험합니다.

```text
DB migration
서비스 재시작
트래픽 전환
파일 삭제
```

그래서 배포 step은 멱등성을 고민해야 합니다.

```text
같은 version을 다시 배포해도 안전한가?
이미 실행된 migration을 다시 실행하지 않는가?
이미 생성된 Kubernetes resource를 다시 apply해도 괜찮은가?
```

---

# 19. Concurrency / Lock

## 개념

동시에 실행되면 안 되는 작업이 있습니다.

```text
prod 배포 2개 동시 실행
같은 VM에 두 서비스 동시 restart
DB migration 동시 실행
같은 namespace helm upgrade 동시 실행
```

## 핵심 키워드

| 키워드               | 설명              |
| ----------------- | --------------- |
| Concurrency Limit | 동시 실행 제한        |
| Environment Lock  | 특정 환경 잠금        |
| Resource Lock     | 특정 리소스 잠금       |
| Mutex             | 하나만 실행          |
| Semaphore         | N개까지 실행         |
| Queue Group       | 같은 그룹은 순차 실행    |
| Cancel Previous   | 이전 실행 취소 후 새 실행 |
| Skip Duplicate    | 같은 작업이면 새 실행 생략 |

## 토이프로젝트 구현 아이디어

```sql
deployment_lock
- lock_key
- owner_run_id
- acquired_at
- expires_at
```

예:

```text
lock_key = prod:order-api
```

---

# 20. Observability

## 개념

CI/CD도 운영 시스템입니다.
그러므로 관측 가능해야 합니다.

## 관측 대상

| 대상     | 예시                      |
| ------ | ----------------------- |
| Log    | step stdout/stderr      |
| Metric | 성공률, 평균 빌드 시간           |
| Trace  | pipeline run 전체 흐름      |
| Event  | queued, started, failed |
| Audit  | 누가 실행/승인/취소했는지          |

## 핵심 키워드

| 키워드            | 설명                  |
| -------------- | ------------------- |
| Structured Log | JSON 형태 로그          |
| Log Streaming  | 실행 중 실시간 로그         |
| Log Masking    | secret 숨김           |
| Metrics        | 실행 시간, 실패율          |
| Tracing        | pipeline 단계 추적      |
| Span           | 각 step 단위 추적        |
| Correlation ID | 여러 시스템 로그 연결        |
| Build URL      | 실행 결과 링크            |
| Notification   | Slack/email/webhook |
| Alert          | 실패/지연 알림            |
| SLI/SLO        | CI/CD 자체의 신뢰성 지표    |

## 좋은 지표

```text
pipeline_success_rate
pipeline_duration_seconds
queue_wait_time_seconds
runner_busy_ratio
deployment_frequency
change_failure_rate
mean_time_to_recovery
```

DORA metric도 연결됩니다.

| DORA 지표               | 의미              |
| --------------------- | --------------- |
| Deployment Frequency  | 배포 빈도           |
| Lead Time for Changes | 변경이 운영에 반영되는 시간 |
| Change Failure Rate   | 배포 실패율          |
| MTTR                  | 장애 복구 시간        |

---

# 21. Audit / Governance

## 개념

CI/CD는 권한 있는 행동을 자동화합니다.
따라서 감사가 중요합니다.

## 기록해야 할 것

| 항목       | 예시                |
| -------- | ----------------- |
| Who      | 누가 실행했는가          |
| When     | 언제 실행했는가          |
| What     | 어떤 pipeline/job인가 |
| Params   | 어떤 파라미터인가         |
| Commit   | 어떤 commit인가       |
| Artifact | 어떤 산출물인가          |
| Target   | 어디에 배포했는가         |
| Approval | 누가 승인했는가          |
| Result   | 성공/실패             |
| Logs     | 실행 로그             |

## 핵심 키워드

| 키워드               | 설명                         |
| ----------------- | -------------------------- |
| Audit Log         | 감사 로그                      |
| Traceability      | commit → build → deploy 추적 |
| Change Request    | 변경 요청                      |
| Deployment Record | 배포 이력                      |
| Immutable Log     | 수정 불가능한 로그                 |
| Retention         | 보관 기간                      |
| Compliance        | 규정 준수                      |
| RBAC              | 역할 기반 권한                   |
| SoD               | 요청자/승인자 분리                 |

---

# 22. Permission / RBAC

## 개념

누가 무엇을 할 수 있는가의 문제입니다.

## 권한 예시

| 권한             | 설명        |
| -------------- | --------- |
| View Pipeline  | 조회        |
| Run Pipeline   | 실행        |
| Cancel Run     | 취소        |
| Approve Deploy | 승인        |
| Edit Pipeline  | 파이프라인 수정  |
| Manage Secret  | secret 관리 |
| Deploy Dev     | dev 배포    |
| Deploy Prod    | prod 배포   |
| Admin Runner   | runner 관리 |

## 핵심 키워드

| 키워드               | 설명           |
| ----------------- | ------------ |
| User              | 사용자          |
| Group             | 그룹           |
| Role              | 역할           |
| Permission        | 권한           |
| Project Scope     | 프로젝트 단위 권한   |
| Environment Scope | 환경 단위 권한     |
| Secret Scope      | secret 접근 범위 |
| Service Account   | 자동화 계정       |
| Token Scope       | 토큰 권한 범위     |
| Impersonation     | 대리 실행        |

## 운영에서 중요한 질문

```text
개발자가 prod 배포 버튼을 누를 수 있는가?
승인자와 실행자가 같아도 되는가?
runner가 prod secret을 읽을 수 있는가?
dev pipeline에서 prod kubeconfig를 볼 수 있는가?
```

---

# 23. Plugin / Extension / Integration

## 개념

CI/CD 도구는 혼자 일하지 않습니다.

```text
Git
Issue Tracker
Registry
Cloud
Kubernetes
Secret Manager
Chat
Monitoring
Approval System
```

이들을 연결하는 방식이 확장 모델입니다.

## 확장 방식

| 방식               | 설명                   | 예시                   |
| ---------------- | -------------------- | -------------------- |
| Plugin           | 제품 내부 확장             | Jenkins plugin       |
| Container Plugin | 특정 image로 step 실행    | Woodpecker/Drone     |
| Resource Type    | 외부 상태를 resource로 모델링 | Concourse            |
| Action           | 재사용 가능한 workflow 단위  | GitHub/Gitea/Forgejo |
| Task Catalog     | 재사용 task             | Tekton               |
| Webhook          | 외부 HTTP 호출           | Slack/Jira           |
| CLI Wrapper      | CLI를 step에서 실행       | kubectl, helm        |
| SDK              | 코드로 pipeline 작성      | Dagger               |

## 좋은 확장 모델의 조건

```text
도구 내부 API에 너무 강하게 묶이지 않는다.
실행 환경이 재현 가능하다.
버전 고정이 가능하다.
보안 경계가 명확하다.
장애가 전체 시스템을 무너뜨리지 않는다.
```

---

# 24. GitOps

## 개념

GitOps는 배포 상태의 원천을 Git으로 두는 방식입니다.

```text
Git repository = Desired State
Cluster        = Live State
Controller     = Reconcile
```

## 핵심 키워드

| 키워드                   | 설명                   |
| --------------------- | -------------------- |
| Desired State         | Git에 선언된 원하는 상태      |
| Live State            | 실제 클러스터 상태           |
| Reconciliation        | 둘을 맞추는 과정            |
| Drift                 | Git과 실제 상태 차이        |
| Sync                  | Git 상태를 cluster에 반영  |
| Rollback              | Git revert로 복구       |
| Manifest Repo         | 배포 manifest 저장소      |
| App of Apps           | Argo CD app 관리 패턴    |
| Image Updater         | image tag 자동 갱신      |
| Pull-based Deployment | cluster가 Git을 보고 당겨감 |

## CI/CD와의 분리

```text
CI:
  build
  test
  image push
  manifest update

CD:
  Git 변경 감지
  cluster sync
  health check
  rollback
```

이 분리는 Kubernetes 운영에서 매우 중요합니다.

---

# 25. Supply Chain Security

## 개념

현대 CI/CD는 단순 자동화가 아닙니다.
소프트웨어 공급망 보안의 관문입니다.

## 핵심 키워드

| 키워드                  | 설명                         |
| -------------------- | -------------------------- |
| SAST                 | 정적 보안 분석                   |
| DAST                 | 동적 보안 분석                   |
| Dependency Scan      | 의존성 취약점 검사                 |
| Container Scan       | image 취약점 검사               |
| Secret Scan          | 코드 내 secret 검사             |
| SBOM                 | 의존성 목록                     |
| Signing              | artifact/image 서명          |
| Cosign               | container image signing 도구 |
| SLSA                 | 공급망 보안 성숙도 모델              |
| Provenance           | 산출물 생성 경로 증명               |
| Policy as Code       | 배포 정책 코드화                  |
| Admission Controller | K8s 배포 시 정책 검사             |

## 좋은 흐름

```text
source
  ↓
test
  ↓
dependency scan
  ↓
image build
  ↓
image scan
  ↓
sign image
  ↓
generate SBOM
  ↓
deploy only signed image
```

---

# 26. Database Migration

## 개념

애플리케이션 배포에서 DB 변경은 가장 위험한 부분입니다.

## 핵심 키워드

| 키워드                     | 설명               |
| ----------------------- | ---------------- |
| Migration               | schema 변경        |
| Flyway/Liquibase        | migration 도구     |
| Backward Compatibility  | 구버전 앱과 호환        |
| Expand-Contract         | 안전한 schema 변경 전략 |
| Pre-deploy Migration    | 앱 배포 전 migration |
| Post-deploy Migration   | 앱 배포 후 migration |
| Rollback Script         | 되돌리기 script      |
| Data Migration          | 데이터 변환           |
| Lock Timeout            | DDL lock 문제      |
| Zero Downtime Migration | 무중단 DB 변경        |

## CI/CD에서 중요한 질문

```text
DB migration은 어느 단계에서 실행할까?
실패하면 앱 배포도 중단할까?
운영 DB migration은 승인자를 둘까?
migration 결과를 어떻게 기록할까?
rollback 가능한 변경인가?
```

---

# 27. 테스트 전략

## CI/CD 도구 학습에서 테스트도 같이 봐야 합니다.

| 테스트              | 설명              |
| ---------------- | --------------- |
| Unit Test        | 빠른 단위 테스트       |
| Integration Test | DB/Kafka/API 연동 |
| Contract Test    | 서비스 간 계약 검증     |
| E2E Test         | 사용자 흐름 검증       |
| Smoke Test       | 배포 후 최소 확인      |
| Performance Test | 성능              |
| Chaos Test       | 장애 주입           |
| Rollback Test    | 복구 검증           |

## pipeline 배치

```text
commit
  ↓
unit test
  ↓
integration test
  ↓
image build
  ↓
deploy dev
  ↓
smoke test
  ↓
approval
  ↓
deploy prod
```

---

# 28. Notification / Event

## 개념

Pipeline 결과는 사람과 시스템에게 알려야 합니다.

## 알림 대상

| 대상            | 내용         |
| ------------- | ---------- |
| Slack/Teams   | 성공/실패 알림   |
| Email         | 승인 요청      |
| Jira/Redmine  | 티켓 상태 변경   |
| Kafka         | 내부 이벤트 발행  |
| Webhook       | 외부 시스템 후처리 |
| Monitoring    | 배포 이벤트 주입  |
| Incident Tool | 실패 시 장애 대응 |

## 이벤트 예시

```json
{
  "eventType": "DEPLOYMENT_SUCCEEDED",
  "service": "order-api",
  "env": "prod",
  "version": "1.2.3",
  "commit": "a1b2c3d",
  "actor": "bohyun",
  "timestamp": "2026-06-27T12:00:00Z"
}
```

## 핵심 키워드

| 키워드                   | 설명               |
| --------------------- | ---------------- |
| Webhook               | HTTP 이벤트 전송      |
| Event Bus             | Kafka 등으로 이벤트 발행 |
| Callback URL          | 외부 시스템 응답        |
| Notification Template | 메시지 템플릿          |
| Subscription          | 이벤트 구독           |
| Dead Letter           | 실패 이벤트 보관        |
| Retry Policy          | 알림 재시도           |

---

# 29. Configuration as Code

## 개념

CI/CD 설정도 코드로 관리해야 합니다.

```text
UI에서 클릭해 만든 설정은
처음엔 빠르지만 나중엔 기억나지 않는다.
```

## 핵심 키워드

| 키워드                   | 설명               |
| --------------------- | ---------------- |
| Pipeline as Code      | pipeline을 코드로 관리 |
| Configuration as Code | 서버 설정도 코드화       |
| Job DSL               | job 정의 코드화       |
| YAML Workflow         | YAML 기반 workflow |
| Versioning            | 설정 변경 이력         |
| Review                | pipeline 변경 리뷰   |
| Template Repository   | 공통 템플릿           |
| Policy Repository     | 정책 저장소           |
| Drift                 | 실제 설정과 코드 차이     |

## 좋은 구조

```text
app-repo
  ├─ src/
  ├─ build.gradle
  ├─ Dockerfile
  └─ ci.yml

deploy-repo
  ├─ dev/
  ├─ stg/
  └─ prod/
```

---

# 30. Tool별 핵심 키워드 정리

## Jenkins

```text
Controller
Agent
Executor
Job
Pipeline
Jenkinsfile
Declarative Pipeline
Scripted Pipeline
Groovy CPS
Shared Library
Plugin
Credential
Build with Parameters
Workspace
Artifact
Freestyle Job
Folder
Node Label
Post Action
```

## Woodpecker

```text
Server
Agent
Pipeline
Step
Backend
Docker Backend
Kubernetes Backend
Secret
Environment
Forge
Webhook
Plugin as Container
Matrix
Volume
Workspace
```

## Concourse

```text
Web
Worker
Team
Pipeline
Resource
Resource Type
Job
Plan
Task
Get
Put
Trigger
fly CLI
Var
Credential Manager
Containerized Task
```

## Rundeck

```text
Project
Job
Option
Node
Node Executor
Workflow
Step
Node Step
Command Step
Dispatch
ACL
Runbook
Ad-hoc Command
Schedule
Execution History
```

## Tekton

```text
Task
TaskRun
Pipeline
PipelineRun
Step
Workspace
Param
Result
ServiceAccount
Trigger
EventListener
PipelineResource
Resolver
Catalog
```

## Argo Workflows

```text
Workflow
WorkflowTemplate
CronWorkflow
DAG
Steps
Template
Artifact
Parameter
Executor
Archive
RetryStrategy
Synchronization
```

## Argo CD

```text
Application
AppProject
Repository
Manifest
Desired State
Live State
Sync
Health
Drift
Reconciliation
Rollback
App of Apps
Sync Wave
Hook
```

## Dagger

```text
Engine
Module
Function
Container
Directory
Cache
Secret
Service Binding
SDK
Pipeline as Code
Portable CI Logic
```

## Forgejo/Gitea Actions

```text
Workflow
Job
Step
Runner
Action
workflow_dispatch
Inputs
Secrets
Context
Event
Matrix
Artifact
```

---

# 31. 학습 로드맵

## Level 1. CI/CD 기본 뼈대

학습 개념:

```text
Pipeline
Stage
Job
Step
Runner
Workspace
Log
Status
Manual Trigger
Parameter
```

토이프로젝트:

```text
웹에서 버튼 클릭
  ↓
파라미터 입력
  ↓
shell command 실행
  ↓
로그 실시간 출력
  ↓
성공/실패 저장
```

---

## Level 2. Spring Boot Build/Test

학습 개념:

```text
Gradle Lifecycle
Test Report
Artifact
Cache
Environment Variable
Secret Masking
```

토이프로젝트:

```text
Git repo URL 입력
  ↓
clone
  ↓
./gradlew clean test build
  ↓
JUnit report 저장
  ↓
JAR artifact 저장
```

---

## Level 3. VM 배포

학습 개념:

```text
SSH
SCP
systemd
Tomcat
Health Check
Rollback
Ansible
Deployment Lock
```

토이프로젝트:

```text
JAR artifact 선택
  ↓
target VM 선택
  ↓
scp 전송
  ↓
systemctl restart
  ↓
/actuator/health 확인
  ↓
실패 시 이전 jar 복구
```

---

## Level 4. Container 배포

학습 개념:

```text
Dockerfile
BuildKit
Image Tag
Registry
Digest
Docker Compose
Image Pull
Container Health
```

토이프로젝트:

```text
Docker image build
  ↓
Harbor push
  ↓
VM에서 docker compose pull
  ↓
docker compose up -d
  ↓
health check
```

---

## Level 5. Kubernetes 배포

학습 개념:

```text
kubectl
Helm
Kustomize
Namespace
ServiceAccount
RBAC
Deployment
Rollout
ConfigMap
Secret
Ingress
```

토이프로젝트:

```text
image push
  ↓
helm values image tag 변경
  ↓
helm upgrade
  ↓
kubectl rollout status
  ↓
pod log 조회
```

---

## Level 6. GitOps

학습 개념:

```text
Desired State
Live State
Reconciliation
Drift
Argo CD
Manifest Repo
Image Tag Update
Rollback by Git Revert
```

토이프로젝트:

```text
CI에서 image push
  ↓
manifest repo의 image tag 변경 commit
  ↓
Argo CD가 자동 sync
  ↓
배포 상태 조회
```

---

## Level 7. 운영 자동화

학습 개념:

```text
Approval
RBAC
Audit
Runbook
Environment Lock
Change Request
Notification
Webhook
Event
```

토이프로젝트:

```text
prod 배포 요청
  ↓
WAITING_APPROVAL
  ↓
승인자 승인
  ↓
배포 실행
  ↓
Slack/Kafka 이벤트 발행
  ↓
감사 로그 저장
```

---

## Level 8. 고급 주제

학습 개념:

```text
DAG Scheduler
Ephemeral Runner
Kubernetes Executor
Autoscaling Runner
Supply Chain Security
SBOM
Image Signing
Policy as Code
OpenTelemetry
DORA Metrics
```

토이프로젝트:

```text
Pipeline DAG 실행기
  ↓
병렬 테스트
  ↓
실패 step부터 재실행
  ↓
image scan
  ↓
signed image만 배포
  ↓
pipeline trace 생성
```

---

# 32. 토이프로젝트 최종 목표 예시

당신이 만든다면 이런 프로젝트가 좋습니다.

```text
Mini Jenkins-Light

기능:
1. Pipeline YAML 등록
2. Manual Trigger
3. Parameter 입력
4. Runner polling
5. Shell executor
6. Docker executor
7. SSH VM deploy
8. Kubernetes deploy
9. Log streaming
10. Secret masking
11. Approval gate
12. Deployment history
13. Webhook notification
14. Argo CD 연동
```

기본 구조:

```text
frontend
  └─ pipeline 실행/로그/승인 UI

backend
  ├─ pipeline 관리
  ├─ run 상태 관리
  ├─ parameter validation
  ├─ queue
  ├─ audit
  └─ webhook

runner
  ├─ shell executor
  ├─ docker executor
  ├─ ssh executor
  └─ k8s executor
```

DB 핵심 테이블:

```text
pipeline
pipeline_version
pipeline_parameter
pipeline_run
pipeline_step_run
runner
runner_heartbeat
secret
environment
deployment
deployment_approval
deployment_lock
audit_log
webhook_event
```

상태 흐름:

```text
CREATED
  ↓
QUEUED
  ↓
ASSIGNED
  ↓
RUNNING
  ↓
WAITING_APPROVAL
  ↓
RUNNING
  ↓
SUCCESS / FAILED / CANCELED / TIMEOUT
```

---

# 33. 가장 중요한 설계 질문

로드맵을 만들 때 아래 질문을 계속 붙잡으면 좋습니다.

```text
1. 이 작업은 누가 실행하는가?
2. 어디서 실행되는가?
3. 어떤 권한으로 실행되는가?
4. 입력값은 무엇인가?
5. secret은 어떻게 주입되는가?
6. 산출물은 어디에 남는가?
7. 실패하면 어떻게 되는가?
8. 재실행해도 안전한가?
9. 누가 승인했는가?
10. 나중에 같은 배포를 추적할 수 있는가?
```

이 질문들이 CI/CD 도구의 심장입니다.
도구 이름은 바뀌어도 이 질문은 오래 남습니다.

결국 CI/CD 학습의 핵심은 Jenkins를 외우는 것이 아니라, **실행·격리·상태·권한·산출물·배포·감사라는 일곱 개의 기둥을 이해하는 것**입니다. 이 기둥을 잡으면 Jenkins, Woodpecker, Concourse, Tekton, Argo, Rundeck은 서로 다른 외투를 입은 같은 계절처럼 보이기 시작합니다.

---

# 부록 A. 독립형 Jenkins-light 도구 선택 — 도구 독립성 분석

> **GitLab CI/CD는 강력하지만 GitLab이라는 큰 성 안으로 들어가는 선택**입니다. "독립적인 Jenkins-light"를 원한다면 GitLab은 1순위에서 내려옵니다. 다만 "독립적"이라는 말은 세 층으로 나눠야 합니다.

```text
1. SCM 독립성
   - GitHub/GitLab/Gitea/Forgejo 등에 덜 묶이는가?

2. 실행기 독립성
   - runner/agent/worker를 VM, Docker, K8s 어디에나 둘 수 있는가?

3. 파이프라인 독립성
   - build/test/deploy 로직이 특정 제품 문법에 과하게 갇히지 않는가?
```

이 기준으로 보면 **Gitea/Forgejo Actions는 완전 독립형 CI가 아닙니다.** 반면 **Woodpecker, Concourse, Rundeck, Dagger** 쪽이 더 독립형에 가깝습니다.

## A-1. Jenkins-light 후보들은 독립적인가?

| 도구                  | SCM 독립성 | 실행 독립성 | 파이프라인 독립성 | 판단                         |
| ------------------- | ------: | -----: | --------: | -------------------------- |
| **Jenkins**         |       5 |      5 |         4 | 기준점                        |
| **Woodpecker**      |       4 |      5 |         4 | 독립형 경량 CI에 가장 가까움          |
| **Concourse**       |       5 |      5 |         4 | SCM보다 resource 중심이라 독립성 높음 |
| **Rundeck**         |       5 |      5 |         3 | CI보다 운영 자동화 독립성 최강         |
| **Dagger**          |       5 |      5 |         5 | 실행 엔진은 독립적, 단 UI/스케줄러 없음   |
| **Forgejo Actions** |       2 |      4 |         3 | Forgejo에 묶임                |
| **Gitea Actions**   |       2 |      4 |         3 | Gitea에 묶임                  |
| **GitLab CI/CD**    |       1 |      4 |         3 | GitLab 종속 큼                |

## A-2. Gitea/Forgejo Actions는 독립적인가?

정확히 말하면 **runner는 독립적이지만, CI control plane은 Gitea/Forgejo에 종속**됩니다. Gitea Actions는 Gitea 자체의 내장 CI/CD 기능이고, job 실행은 Gitea가 직접 하지 않고 `act runner`라는 독립 프로그램에 위임합니다. Forgejo도 구조가 비슷합니다 — `.forgejo/workflows` 파일을 기반으로 CI를 구동하고, 실제 실행은 별도 설치·구성되는 Forgejo Runner가 담당합니다.

```text
Forgejo / Gitea
  ├─ Git repository
  ├─ Actions UI
  ├─ Workflow definition
  └─ Runner에게 작업 전달

Runner
  ├─ Host 실행
  ├─ Docker 실행
  └─ Docker-in-Docker 실행
```

| 질문                                           | 답                                    |
| -------------------------------------------- | ------------------------------------ |
| Gitea/Forgejo Actions가 Jenkins처럼 독립 CI 서버인가? | 아니오                                  |
| runner는 독립적으로 VM에 설치 가능한가?                   | 예                                    |
| GitHub Actions처럼 수동 실행 + 입력값이 가능한가?          | Forgejo는 가능                          |
| Git 서버를 바꿔도 그대로 유지 가능한가?                     | 어렵다                                  |
| GitLab 종속을 피하려는 목적에 맞는가?                     | GitLab보다는 가볍지만, Gitea/Forgejo 종속은 생김 |

Forgejo는 `workflow_dispatch`를 통해 UI나 API로 workflow를 수동 실행할 수 있고, `choice`/`boolean`/`number`/`string` 타입의 입력값을 정의할 수 있습니다. Jenkins의 "Build with Parameters"와 비슷합니다.

```yaml
on:
  workflow_dispatch:
    inputs:
      target_env:
        description: "배포 환경"
        required: true
        type: choice
        options:
          - dev
          - stg
          - prod
      version:
        description: "배포 버전"
        required: true
        type: string
      deploy_type:
        description: "배포 유형"
        required: true
        type: choice
        options:
          - vm
          - container
          - k8s
```

## A-3. 더 독립적인 후보

### 1순위: Woodpecker CI

자체 server/agent 구조를 가지고 GitHub·Gitea·Forgejo·GitLab·Bitbucket 등 여러 forge와 연동됩니다. GitLab CI처럼 GitLab에 박혀 있는 구조가 아닙니다. Kubernetes backend는 pipeline step을 독립 Pod로 실행하고, step 간 파일 전달을 위해 임시 PVC를 생성하며, step 단위로 CPU/memory requests/limits를 지정할 수 있습니다.

```text
GitHub / Gitea / Forgejo / GitLab / Bitbucket
  ↓ webhook
Woodpecker Server
  ↓ queue
Woodpecker Agent
  ↓
Docker / Kubernetes / Local backend
```

```yaml
steps:
  build:
    image: eclipse-temurin:21
    commands:
      - ./gradlew clean build

  test:
    image: eclipse-temurin:21
    commands:
      - ./gradlew test

  docker-build:
    image: docker:cli
    commands:
      - docker build -t harbor.local/app/order-api:${CI_COMMIT_SHA} .
      - docker push harbor.local/app/order-api:${CI_COMMIT_SHA}

  deploy-k8s:
    image: bitnami/kubectl
    commands:
      - kubectl set image deployment/order-api order-api=harbor.local/app/order-api:${CI_COMMIT_SHA}
      - kubectl rollout status deployment/order-api
```

다만 Jenkins처럼 UI에서 `VERSION`/`TARGET_ENV`/`DEPLOY_TYPE`을 폼으로 넣는 경험은 상대적으로 약합니다.

### 2순위: Concourse

SCM에 덜 묶입니다. Git도 하나의 resource일 뿐이고, Docker image·S3·time·registry 같은 외부 상태도 resource로 다룹니다.

```text
Resource
  ↓
Job
  ↓
Plan
  ↓
Task
  ↓
Output Resource
```

독립성은 좋지만 Jenkins식 파라미터 빌드 UX는 약합니다. "Jenkins-light"라기보다 **독립적인 pipeline machine**입니다.

### 3순위: Rundeck

CI 도구라기보다 **운영 자동화 / Runbook Automation 도구**입니다. "파라미터 넣고 VM/컨테이너/K8s 배포 실행"에는 매우 잘 맞습니다. Job은 실행 시 required/optional·선택값 목록을 가진 named option을 정의할 수 있고, Kubernetes 플러그인도 제공합니다.

```text
Woodpecker / Concourse
  → build / test / image push

Rundeck
  → 파라미터 기반 배포 / 재시작 / 롤백 / 점검
```

### 4순위: Dagger

CI 서버가 아니라 **pipeline engine**입니다. build·test·ship 자동화를 위한 플랫폼이고, 로컬·CI 서버·클라우드에서 실행될 수 있습니다. 특정 CI 서버 문법에 덜 묶이는 게 장점입니다.

```text
Dagger pipeline
  ├─ local에서 실행
  ├─ Jenkins에서 실행
  ├─ Woodpecker에서 실행
  ├─ GitHub Actions에서 실행
  └─ Concourse에서 실행
```

UI·Job·parameter form·schedule·log browser·credential store를 다 제공하는 도구는 아닙니다. **Jenkinsfile/Groovy를 대체할 수 있는 pipeline logic layer**에 가깝습니다.

## A-4. 빌드/테스트/배포 능력 비교

| 도구              | Build | Test | VM Deploy | Container Deploy | K8s Deploy | 파라미터 UI |
| --------------- | ----: | ---: | --------: | ---------------: | ---------: | ------: |
| Woodpecker      |     5 |    5 |         4 |                5 |          5 |     2.5 |
| Concourse       |     5 |    5 |         3 |                5 |          4 |       2 |
| Rundeck         |   2.5 |  2.5 |         5 |                4 |          4 |       5 |
| Dagger          |     5 |    5 |         4 |                5 |          4 |       1 |
| Forgejo Actions |     4 |    4 |         4 |                4 |          4 |       4 |
| Gitea Actions   |     4 |    4 |         4 |                4 |          4 |     3.5 |
| Jenkins         |     5 |    5 |         5 |                5 |          5 |       5 |

Kubernetes 구성 방식은 보통 셋입니다.

```text
1. Runner/Agent에 kubeconfig를 주고 kubectl/helm 실행

2. Runner/Agent를 Kubernetes 내부에 두고 ServiceAccount 권한으로 실행

3. CI는 image build/push까지만 하고,
   배포는 Argo CD가 GitOps로 수행
```

가장 권장하는 구조는 3번입니다 — CI 도구가 cluster-admin 열쇠를 쥐고 직접 클러스터를 흔드는 일을 줄입니다.

```text
CI 도구
  ├─ build
  ├─ test
  ├─ image push
  └─ manifest repo image tag 변경

Argo CD
  └─ Kubernetes sync
```

## A-5. 추천 아키텍처

### A안: Jenkins-light 단일 도구에 가깝게

```text
Woodpecker
  ├─ build
  ├─ test
  ├─ image build
  ├─ image push
  ├─ VM deploy: ssh / ansible
  └─ K8s deploy: kubectl / helm / manifest update
```

가볍고 독립적이지만 Jenkins식 파라미터 입력 UI가 약합니다.

### B안: Jenkins 역할을 둘로 나누기 (더 실무적)

```text
Woodpecker
  ├─ build
  ├─ test
  └─ image push

Rundeck
  ├─ target_env 입력
  ├─ version 입력
  ├─ deploy_type 입력
  ├─ VM 배포
  ├─ Container 배포
  └─ K8s 배포
```

| Jenkins 역할        | 대체                                 |
| ----------------- | ---------------------------------- |
| CI 빌드/테스트         | Woodpecker                         |
| 이미지 빌드/push       | Woodpecker                         |
| 파라미터 배포 버튼        | Rundeck                            |
| VM 작업             | Rundeck + Ansible                  |
| K8s 배포            | Rundeck → Argo CD / Helm / kubectl |
| 공통 pipeline logic | Dagger 선택 가능                       |

## A-6. 결론

단일 제품으로 고르면:

```text
1순위: Woodpecker
2순위: Concourse
3순위: Forgejo Actions, 단 Forgejo 종속 허용 시
```

운영 현실성까지 보면 **Woodpecker + Rundeck + Argo CD** 조합이 가장 단정합니다. Woodpecker가 빌드와 테스트의 망치라면, Rundeck은 운영자가 누르는 안전한 스위치이고, Argo CD는 Kubernetes의 실제 상태를 조용히 맞추는 항해사입니다. Jenkins 하나가 모두 들고 있던 짐을 세 도구로 나누면, 호환성의 무게는 줄고 각자의 역할은 더 선명해집니다.

> 출처: Gitea Documentation(act runner·overview), Forgejo(Actions administrator guide·reference), Woodpecker CI(forges·kubernetes backend), Concourse CI(resources), Rundeck(job options·kubernetes plugins), Dagger(GitHub repository). 본 부록은 도구 비교의 *현재 시점 스냅샷*이며, 각 도구의 정확한 기능 경계는 공식 문서로 재확인합니다.
