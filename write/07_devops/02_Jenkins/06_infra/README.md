---
title: Jenkins 인프라 계획·배포·통합·확장·AI활용·CI설계 학습 MOC
tags: [moc, jenkins, infra, planning, capacity, well-architected, iac, terraform, jcasc, helm, integration, github, sonarqube, artifactory, scaling, azure-vm-agents, ai, llm, chatgpt, ci-design, docker-registry]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../03_agent/README.md
  - ../05_operations/README.md
updated: 2026-05-31
---

# Jenkins 인프라 계획·배포·통합·확장·AI활용·CI설계 학습 MOC

---

> Jenkins를 "어떻게 쓰는가"가 아니라 "어떻게 계획하고 배포하고, 외부 CI 도구와 통합하고, 확장하고, 하나의 CI 파이프라인으로 설계하는가"를 다루는 묶음입니다. 본 묶음을 끝내면 controller 사양을 근거 있게 산정하고, 5가지 배포 형태를 Well-Architected 6 pillars로 평가하며, Terraform·JCasC·Helm으로 Jenkins를 코드로 재현 가능하게 배포하고, GitHub·SonarQube·Artifactory를 동일한 4단계로 연결하며, VM·K8s 동적 Agent로 수평 확장하고, LLM으로 파이프라인 초안을 짜되 반드시 검증하며, 이 모든 조각을 스테이지 순서가 있는 하나의 CI 파이프라인으로 설계하는 흐름을 한 번에 설명할 수 있습니다.

## 왜 한 폴더로 묶었는가

01_core~05_operations가 "Jenkins를 어떻게 쓰는가"(파이프라인·Agent·API·내구성)에 집중한다면, 06_infra는 그 앞단인 "Jenkins 자체를 어떻게 세우는가"를 다룹니다. 용량 산정·배포 형태 선택·IaC 배포는 코드를 작성하기 전 인프라 설계 단계의 결정이고, 한 번 굳으면 바꾸기 어렵습니다. 세 주제는 결국 *처음 한 번을 제대로 세운다*는 같은 목적을 가집니다 — 용량 산정이 "얼마나 큰 서버가 필요한가"에, 배포 평가가 "어디에 어떤 방식으로 올릴까"에, IaC가 "그 결정을 어떻게 코드로 재현할까"에 답합니다. 한 폴더에 두면 "Jenkins를 진지하게 배포하려면 무엇을 먼저 정해야 하는가"의 답이 한 페이지에 잡힙니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 06 계획·배포 | 06-00 | [점검 — 핵심 질문과 답 (계획·배포)](06-00.점검.핵심%20질문과%20답%20%28계획%C2%B7배포%29.md) | 06장 진입 전·후 자가 점검 |
| 06 계획·배포 | 06-01 | [Jenkins 서버 용량 산정과 시스템 요구사항](06-01.Jenkins%20서버%20용량%20산정과%20시스템%20요구사항.md) | controller 자원 소비, CPU·RAM·디스크 추정식, 포트, JVM 튜닝 |
| 06 계획·배포 | 06-02 | [배포 시나리오와 Well-Architected 평가](06-02.배포%20시나리오와%20Well-Architected%20평가.md) | serverless·container·VM·bare metal, 6 pillars 평가, use-case 매핑 |
| 06 계획·배포 | 06-03 | [IaC로 Jenkins 배포 — Terraform·JCasC·Helm](06-03.IaC로%20Jenkins%20배포%20%E2%80%94%20Terraform%C2%B7JCasC%C2%B7Helm.md) | 재현성, JCasC 3종 파일, Terraform 흐름, K8s vs VM 선택 |
| 06 통합 | 06-04 | [GitHub 연동 — 플러그인·PAT·웹훅](06-04.GitHub%20연동%20%E2%80%94%20플러그인%C2%B7PAT%C2%B7웹훅.md) | GitHub 플러그인, PAT 스코프(admin:repo_hook·repo), 크레덴셜 2종, Test Connection |
| 06 통합 | 06-05 | [SonarQube 연동 — 정적분석 게이트](06-05.SonarQube%20연동%20%E2%80%94%20정적분석%20게이트.md) | SonarQube Helm 배포, Scanner 플러그인, analysis token, Quality Gate |
| 06 통합 | 06-06 | [Artifactory 연동 — 아티팩트 저장소](06-06.Artifactory%20연동%20%E2%80%94%20아티팩트%20저장소.md) | Artifactory Helm 배포(OSS), user·permission, JFrog 플러그인 설정 |
| 06 통합 | 06-07 | [외부 도구 통합 4단계 비교](06-07.외부%20도구%20통합%204단계%20비교.md) | 공통 4단계, 도구별 토큰 경로·크레덴셜 타입 차이, 전역 설정이 마지막인 이유 |
| 06 확장 | 06-08 | [클라우드 VM 동적 Agent — Azure VM Agents 플러그인](06-08.클라우드%20VM%20동적%20Agent%20%E2%80%94%20Azure%20VM%20Agents%20플러그인.md) | VM vs K8s on-demand, service principal 인증, retention 3전략, 이미지 캐싱 |
| 06 AI 활용 | 06-09 | [AI로 파이프라인 초안 짜기 — Describe·Run·Troubleshoot·Refine](06-09.AI로%20파이프라인%20초안%20짜기%20%E2%80%94%20Describe%C2%B7Run%C2%B7Troubleshoot%C2%B7Refine.md) | LLM 4단계 협업 루프, 요구사항 기술, 환경 추측 오류, AI 코드 검증 의무 |
| 06 CI 설계 | 06-10 | [CI 파이프라인 전체 설계 — 스테이지 순서·Docker 레지스트리·인증](06-10.CI%20파이프라인%20전체%20설계%20%E2%80%94%20스테이지%20순서%C2%B7Docker%20레지스트리%C2%B7인증.md) | 7스테이지 순서·이유, webhook 트리거, Artifactory Docker 레지스트리, Kaniko 인증 Secret |

용량부터 보려면 06-01, 배포 형태 결정이 먼저면 06-02, 코드화 구현이 급하면 06-03부터 진입합니다. 계획·배포 세 편은 06-01(얼마나) → 06-02(어디에) → 06-03(어떻게 코드로) 순으로 이어집니다. 외부 도구 연동은 06-04~06-06을 도구별로 보고, 06-07 비교표로 공통 4단계를 정리합니다. 06-08은 03_agent의 K8s 동적 Agent와 짝을 이루는 VM 기반 동적 Agent 편으로, 수평 확장의 두 갈래를 비교합니다. 06-09는 LLM으로 파이프라인 초안을 짜는 방법론과 그 검증 의무를 다루며, 06-05·06-06의 플러그인 step과 이어집니다. 06-10은 06-04~06-06과 03_agent Kaniko를 한 순서로 잇는 CI 파이프라인 전체 설계도로, 개별 도구를 배운 뒤 큰 그림을 잡는 마무리 편입니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.4xx 이상 | JCasC, durability 표준 |
| Java | 11 | 책 기준 JVM 튜닝 예시 |
| Terraform | azurerm provider | 예시는 Azure, GCP·AWS도 대응 provider |
| Helm chart | jenkins/jenkins | K8s 배포용 공식 차트 |

> 용량 추정식·6 pillars 점수는 *Learning Continuous Integration with Jenkins 3e*가 제시하는 휴리스틱입니다. Jenkins 공식 보장이 아니므로 설계의 출발점으로만 삼고 실측으로 보정합니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md)의 Controller·Agent 역할 분리와 [`../03_agent/`](../03_agent/README.md)의 K8s 실행 환경을 알고 있습니다.
2. [`../02_security/`](../02_security/README.md)의 JCasC 기본 개념을 한 번이라도 본 적이 있습니다(06-03 진입 조건).
3. 클라우드 VM·컨테이너·Kubernetes의 차이를 개념 수준에서 구분할 수 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md), [`../03_agent/`](../03_agent/README.md)를 먼저 보고 돌아옵니다.

## 면접 대비 체크리스트

> 열 편을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. controller가 빌드를 직접 돌리지 않는데도 CPU·RAM 산정이 중요한 이유는? 책 추정식(요청÷250, agent×3)의 한계는?
2. controller가 쓰는 네 포트(8080·443·50000·22)는 각각 무엇이며, 50000이 막히면 어떤 증상이 납니까?
3. 5가지 배포 형태를 6 pillars로 평가하면 어디가 종합 최적이고, bare metal은 무엇을 포기합니까?
4. JCasC 배포 3종 파일(jenkins.yaml·plugins.txt·override.conf)의 역할과 처리 순서는? 순서를 어기면?
5. `terraform init·plan·apply`는 각각 무엇을 하며, K8s Helm 배포와 VM Terraform 배포를 가르는 기준은?
6. GitHub·SonarQube·Artifactory 통합의 공통 4단계는 무엇이며, "전역 설정"이 항상 마지막인 이유는?
7. secret text와 username&password 크레덴셜은 각각 언제 쓰며, GitHub가 둘 다 쓰는 이유는?
8. VM 동적 Agent와 K8s on-demand는 각각 어떤 워크로드에 유리하며, VM의 retention 3전략(Idle·Pool·Once)은 어떻게 다릅니까?
9. LLM으로 파이프라인을 짤 때 Describe→Run→Troubleshoot→Refine 중 가장 중요한 단계는? AI 생성 코드를 그대로 믿으면 안 되는 이유와 검증 원칙은?
10. CI 파이프라인 스테이지 순서(Clone→Test→SCA→Quality Gate→Build→Publish)에서 SCA·Gate가 Build 앞에 오는 이유는? Artifactory를 Docker 레지스트리로 쓸 때 package type과 Kaniko 인증 Secret의 namespace는?

각 질문에 막히면 해당 절로 돌아갑니다.
