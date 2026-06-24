---
title: Jenkins 학습 도메인 허브 (MOC)
tags: [moc, jenkins, ci-cd, pipeline, operations, roadmap]
status: draft
related:
  - ../README.md
  - 01_core/README.md
  - 02_security/README.md
  - 03_agent/README.md
  - 04_api/README.md
  - 05_operations/README.md
  - 06_infra/README.md
  - 07_engine/README.md
updated: 2026-06-25
---

# Jenkins 학습 도메인 허브 (MOC)

---

> "Jenkinsfile 을 잘 쓰는 사람" 에서 멈추지 말고, Jenkins 를 하나의 **운영 플랫폼**으로 이해하는 것이 이 묶음의 목표입니다. Jenkins 는 오래된 도구처럼 보이지만, 권한·Secret·Agent·Plugin·JVM·배포 전략이 얽힌 운영 시스템으로 바라봐야 제대로 다룰 수 있습니다. 이 문서는 7개 서브 폴더(110편)를 *학습 주제* 축으로 다시 묶은 지도입니다.

## 대주제 — 세 능력 축

Jenkins 전문가는 세 능력을 함께 갖춰야 합니다. 이 세 축이 7개 폴더를 관통하는 대주제입니다.

1. **Pipeline 을 잘 작성하는 능력** — Declarative 구조, 재현 가능한 빌드, 안전한 Credential 주입. 주로 [01_core/](01_core/README.md) 와 [02_security/](02_security/README.md) 가 답합니다.
2. **Jenkins 를 안정적으로 운영하는 능력** — Controller/Agent 구조, 내구성, Plugin·JVM·백업·장애 대응. [03_agent/](03_agent/README.md) · [05_operations/](05_operations/README.md) · [07_engine/](07_engine/README.md) 가 답합니다.
3. **조직의 CI/CD 표준을 설계하는 능력** — Shared Library, 폴더 권한, 외부 도구 통합, GitOps 배포, API 자동화. [04_api/](04_api/README.md) 와 [06_infra/](06_infra/README.md) 가 답합니다.

"Pipeline 몇 줄로 끝나는 도구" 가 아니라, 위 세 능력이 맞물려야 한 사람이 Jenkins 를 책임질 수 있습니다.

## 학습 지도 — 주제 → 폴더 크로스워크

전문가 로드맵의 학습 주제를 기존 7폴더에 매핑한 표입니다. *커버* 열은 우리 자료가 그 주제를 얼마나 다루는지입니다 — ✅ 충분 / △ 부분 / ❌ 미작성.

| # | 학습 주제 | 담당 폴더 | 커버 |
|---|----------|----------|:----:|
| 1 | 기본 구조 (Controller·Agent·Executor·Queue·Label) | [01_core/](01_core/README.md) | ✅ |
| 2 | Pipeline (Declarative·Scripted·step·stage·post) | [01_core/](01_core/README.md) | ✅ |
| 3 | Jenkinsfile 작성 (재현성·실패 추적·withCredentials) | [01_core/](01_core/README.md) · [02_security/](02_security/README.md) | ✅ |
| 4 | Shared Library (vars·src·resources·Trusted) | [05_operations/](05_operations/README.md) | ✅ |
| 5 | Agent 운영 (Static·SSH·Inbound·Docker·K8s) | [03_agent/](03_agent/README.md) | ✅ |
| 6 | 보안 (인증·인가·Matrix·Script Approval·Agent→Controller) | [02_security/](02_security/README.md) | ✅ |
| 7 | Credential (Scope·withCredentials·Masking 한계) | [02_security/](02_security/README.md) · [04_api/](04_api/README.md) | ✅ |
| 8 | Plugin 관리 (의존성·LTS 호환·CasC catalog) | [06_infra/](06_infra/README.md) · [07_engine/](07_engine/README.md) | △ |
| 9 | 운영 관리 (Backup·Restore·Upgrade·Log·Disk) | [05_operations/](05_operations/README.md) | △ |
| 10 | JVM 튜닝 (Xmx·G1GC·Heap·Thread dump) | [06_infra/](06_infra/README.md) | △ |
| 11 | 빌드 도구 (Gradle·SonarQube·Kaniko·SBOM·Trivy) | [03_agent/](03_agent/README.md) · [06_infra/](06_infra/README.md) | ✅ |
| 12 | Docker / Kubernetes 연동 (Pod Template·RBAC·Kaniko) | [03_agent/](03_agent/README.md) | ✅ |
| 13 | 배포 전략 (Blue-Green·Canary·GitOps·ArgoCD) | [06_infra/](06_infra/README.md) | ✅ |
| 14 | 장애 대응 (Queue 적체·UI 느림·Thread dump 루틴) | [05_operations/](05_operations/README.md) · [06_infra/](06_infra/README.md) | ❌ |
| 15 | API / 자동화 (Crumb·Token·Webhook·CLI) | [04_api/](04_api/README.md) | ✅ |
| 16 | 성능·스케일링 (Controller 부하·동적 Agent·discard) | [06_infra/](06_infra/README.md) · [07_engine/](07_engine/README.md) | ✅ |

세 가지(8 Plugin 관리·9 운영 관리·10 JVM 튜닝)는 △ 부분, 14 장애 대응은 ❌ 로 우리 자료에서 단독 편이 없거나 얕습니다 — 아래 "아직 얕거나 빈 주제" 절에 신규 후보로 정리했습니다. 나머지는 해당 폴더의 README 학습 순서를 따라가면 됩니다.

## 전문가 5단계 로드맵

같은 110편을 *숙련도* 순으로 다시 읽는 경로입니다. 단계가 올라갈수록 "Pipeline 작성" 에서 "플랫폼 설계" 로 넘어갑니다.

| 단계 | 수준 | 핵심 능력 | 주로 보는 폴더 |
|------|------|----------|--------------|
| 1 | 사용자 | UI·Job·빌드 실행·로그·간단한 Jenkinsfile | [01_core/](01_core/README.md) |
| 2 | Pipeline 작성자 | Declarative·stage/post/when/parallel·credentials·Docker build·배포 stage | [01_core/](01_core/README.md) · [02_security/](02_security/README.md) |
| 3 | 팀 표준화 담당자 | Shared Library·공통 템플릿·Credential scope·폴더 권한·Notification 표준 | [05_operations/](05_operations/README.md) · [02_security/](02_security/README.md) |
| 4 | Jenkins 운영자 | Controller/Agent 설계·Plugin 관리·Backup/Restore·Upgrade·JVM 튜닝·K8s Agent | [03_agent/](03_agent/README.md) · [05_operations/](05_operations/README.md) · [07_engine/](07_engine/README.md) |
| 5 | CI/CD 플랫폼 엔지니어 | GitOps·멀티 테넌시·표준 빌드 이미지·품질 게이트·SBOM·감사 로그·Observability | [06_infra/](06_infra/README.md) · [04_api/](04_api/README.md) |

## 아직 얕거나 빈 주제 (격차 백로그)

전문가 로드맵 대비 우리 자료가 비거나 얕은 주제입니다. **기존 110편을 더 쪼개는 게 아니라, 빈 칸을 신규 문서로 채우는** 후보입니다. 당장 작성하지 않고 backlog 로만 둡니다.

| 신규 문서 후보 | 별도 문서인 이유 | 제안 위치 |
|---------------|----------------|----------|
| 장애 대응 runbook (증상 → 의심 지점 표 + 분석 루틴 10단계) | 여러 영역을 가로지르는 횡단 주제라 기존 어느 편에도 들어맞지 않습니다 — 가장 큰 공백 | `05_operations/` 신규 |
| Backup / Restore · LTS Upgrade 절차 | 내구성(01-01) 과는 다른 *운영 절차* 소주제입니다 | `05_operations/` 신규 |
| Jenkins 특화 JVM 튜닝 (Heap · Thread · GC dump 실측) | `06_infra/01-01` 은 용량 *산정* 이지 튜닝이 아닙니다 | `06_infra/` 또는 `07_engine/` 신규 |
| Plugin 수명주기 · 보안 권고 | 여러 편에 흩어진 Plugin 언급을 한곳에 모읍니다 | `06_infra/` 신규 |
| 실무 프로젝트 5종 인덱스 | 학습 프로젝트를 묶는 허브가 없습니다 | 본 README + [_practice/](_practice/) |

## 실무 학습 프로젝트

직접 만들어 보면 위 주제들이 연결됩니다. 각 프로젝트가 어느 폴더의 자료에 기대는지 함께 적습니다.

- **Spring Boot CI Pipeline** — checkout → Gradle build → JUnit·Jacoco → SonarQube → JAR archive. 기반: [01_core/](01_core/README.md) · [06_infra/](06_infra/README.md)
- **Docker Image Pipeline** — Dockerfile → 빌드 → 태그 전략 → Harbor push → 취약점 스캔 → 캐시 최적화. 기반: [03_agent/](03_agent/README.md)
- **Kubernetes 배포 Pipeline** — K8s Agent Pod → Kaniko build → Helm deploy → smoke test → rollback. 기반: [03_agent/](03_agent/README.md) · [06_infra/](06_infra/README.md)
- **Shared Library** — `buildJavaApp()` · `buildDockerImage()` · `deployHelm()` · `notifyResult()` · `withQualityGate()`. 기반: [05_operations/](05_operations/README.md)
- **Jenkins 운영 자동화** — Job DSL · Configuration as Code · Backup/Restore 스크립트 · Plugin 목록 관리 · 권한 매트릭스. 기반: [02_security/](02_security/README.md) · [06_infra/](06_infra/README.md)

## 왜 7폴더인가 (구조 결정 기록)

학습 주제는 17개로 나뉘지만 폴더는 7개입니다. 둘은 다른 축이라 1:1 로 맞추지 않습니다 — 주제는 *학습 순서* 축이고, 폴더는 *운영 관심사* 축입니다. 위 크로스워크 표가 보여주듯 주제는 폴더에 여러 개씩 자연스럽게 접힙니다.

폴더를 17개로 늘리지 않는 이유는 두세 편짜리 폴더가 양산돼 오히려 동선이 끊기기 때문입니다(실제로 내구성 2편은 단독 폴더로 두기 적어 `05_operations` 로 합쳤습니다). `06_infra`(26편) 의 CI·CD 묶음을 별도 폴더로 분리하는 안도 검토했지만, 그 폴더 README 가 "Jenkins 자체를 세운다" 는 한 흐름으로 6개 그룹을 묶었고 CI·CD 편들이 같은 폴더의 계획·통합·Job 운영 편을 자주 참조해, 가르면 흐름이 폴더 사이 링크로 끊깁니다. 그래서 *17주제 시야는 이 README 의 크로스워크* 가 제공하고, 폴더 물리 구조는 7개를 유지합니다.

## 환경과 버전

> 본 묶음 전반의 기준 조합입니다. 폴더별 세부 버전은 각 README 를 따릅니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | Pipeline·durability·Agent→Controller 보안 기본 |
| JDK | 17 | Jenkins 2.426+ 권장 런타임 |
| Pipeline 문법 | Declarative 우선 | Scripted 는 비교 목적 |
| Kubernetes | 1.28 이상 | 동적 Agent·PodSecurity 적용 |

> Jenkins 2.326 부터 Agent→Controller 보안 시스템을 비활성화·커스터마이즈할 수 없도록 바뀌었습니다 — Agent 와 Controller 사이 보안 경계를 강제하는 변화입니다(출처: [jenkins.io JEP-235](https://www.jenkins.io/doc/book/security/controller-isolation/jep-235/)). Pipeline 의 가장 기본 빌딩 블록은 `step` 이며(출처: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)), Credential 은 Controller 에 암호화 저장되고 Pipeline 에서는 ID 로만 다룹니다(출처: [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)).

## 핵심 키워드 (압축)

복습·검색용 키워드 묶음입니다.

```text
Controller/Agent Architecture · Executor · Node · Label · Workspace · Queue Scheduling
Declarative / Scripted Pipeline · Jenkinsfile · step·stage·post·when·parallel
Credential Binding · withCredentials · Secret Masking Limitations
Shared Library · vars/src/resources · Trusted vs Untrusted · Script Security Sandbox
Plugin Dependency · LTS Upgrade · Backup/Restore of JENKINS_HOME
Controller JVM Tuning · GC Log · Heap/Thread Dump · Agent-to-Controller Security
Matrix Authorization · Folder Permission · CSRF Crumb · Webhook Trigger · Remote Access API
Kubernetes Plugin · Ephemeral Agent · Pod Template · Docker Socket Risk · Kaniko/BuildKit
Artifact Management · JUnit/Jacoco/SonarQube · Build Discard · Workspace Cleanup
Retry/Timeout · Manual Approval · Blue-Green/Canary/Rolling · GitOps with ArgoCD
Observability (Metrics·Logs·Traces) · Shared Library Testing · Job DSL · Configuration as Code
```
