---
title: Jenkins 인프라 계획·배포 학습 MOC
tags: [moc, jenkins, infra, planning, capacity, well-architected, iac, terraform, jcasc, helm]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../03_agent/README.md
  - ../05_operations/README.md
updated: 2026-05-31
---

# Jenkins 인프라 계획·배포 학습 MOC

---

> Jenkins를 "어떻게 쓰는가"가 아니라 "어떻게 계획하고 배포하고 운영하는가"를 다루는 묶음입니다. 본 묶음을 끝내면 controller 사양을 근거 있게 산정하고, 5가지 배포 형태를 Well-Architected 6 pillars로 평가하며, Terraform·JCasC·Helm으로 Jenkins를 코드로 재현 가능하게 배포하는 흐름을 한 번에 설명할 수 있습니다.

## 왜 한 폴더로 묶었는가

01_core~05_operations가 "Jenkins를 어떻게 쓰는가"(파이프라인·Agent·API·내구성)에 집중한다면, 06_infra는 그 앞단인 "Jenkins 자체를 어떻게 세우는가"를 다룹니다. 용량 산정·배포 형태 선택·IaC 배포는 코드를 작성하기 전 인프라 설계 단계의 결정이고, 한 번 굳으면 바꾸기 어렵습니다. 세 주제는 결국 *처음 한 번을 제대로 세운다*는 같은 목적을 가집니다 — 용량 산정이 "얼마나 큰 서버가 필요한가"에, 배포 평가가 "어디에 어떤 방식으로 올릴까"에, IaC가 "그 결정을 어떻게 코드로 재현할까"에 답합니다. 한 폴더에 두면 "Jenkins를 진지하게 배포하려면 무엇을 먼저 정해야 하는가"의 답이 한 페이지에 잡힙니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 06 계획·배포 | 06-00 | [점검 — 핵심 질문과 답 (계획·배포)](06-00.점검.핵심%20질문과%20답%20%28계획%C2%B7배포%29.md) | 06장 진입 전·후 자가 점검 |
| 06 계획·배포 | 06-01 | [Jenkins 서버 용량 산정과 시스템 요구사항](06-01.Jenkins%20서버%20용량%20산정과%20시스템%20요구사항.md) | controller 자원 소비, CPU·RAM·디스크 추정식, 포트, JVM 튜닝 |
| 06 계획·배포 | 06-02 | [배포 시나리오와 Well-Architected 평가](06-02.배포%20시나리오와%20Well-Architected%20평가.md) | serverless·container·VM·bare metal, 6 pillars 평가, use-case 매핑 |
| 06 계획·배포 | 06-03 | [IaC로 Jenkins 배포 — Terraform·JCasC·Helm](06-03.IaC로%20Jenkins%20배포%20%E2%80%94%20Terraform%C2%B7JCasC%C2%B7Helm.md) | 재현성, JCasC 3종 파일, Terraform 흐름, K8s vs VM 선택 |

용량부터 보려면 06-01, 배포 형태 결정이 먼저면 06-02, 코드화 구현이 급하면 06-03부터 진입합니다. 세 편은 06-01(얼마나) → 06-02(어디에) → 06-03(어떻게 코드로) 순으로 자연스럽게 이어집니다.

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

> 세 편을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. controller가 빌드를 직접 돌리지 않는데도 CPU·RAM 산정이 중요한 이유는? 책 추정식(요청÷250, agent×3)의 한계는?
2. controller가 쓰는 네 포트(8080·443·50000·22)는 각각 무엇이며, 50000이 막히면 어떤 증상이 납니까?
3. 5가지 배포 형태를 6 pillars로 평가하면 어디가 종합 최적이고, bare metal은 무엇을 포기합니까?
4. JCasC 배포 3종 파일(jenkins.yaml·plugins.txt·override.conf)의 역할과 처리 순서는? 순서를 어기면?
5. `terraform init·plan·apply`는 각각 무엇을 하며, K8s Helm 배포와 VM Terraform 배포를 가르는 기준은?

각 질문에 막히면 해당 절로 돌아갑니다.
