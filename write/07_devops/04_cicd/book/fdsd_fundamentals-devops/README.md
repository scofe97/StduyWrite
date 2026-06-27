---
title: Fundamentals of DevOps and Software Delivery 정독 인덱스
tags: [devops, cicd, deployment, iac, orchestration, networking, security, monitoring, study-index, moc]
status: draft
source:
  - 《Fundamentals of DevOps and Software Delivery》
related:
  - ../../README.md
  - ../cicd_cicd-patterns/README.md
updated: 2026-06-28
---


# Fundamentals of DevOps and Software Delivery 정독 인덱스
> 《Fundamentals of DevOps and Software Delivery》의 장 단위 정독 노트 인덱스입니다 — 04_cicd 폴더의 첫 번째 정독 대상 책

이 폴더는 단행본 《Fundamentals of DevOps and Software Delivery》의 정독 노트를 모읍니다. 소프트웨어 딜리버리의 전체 라이프사이클 — 배포, 인프라를 코드로 관리하기(IaC), 오케스트레이션, 버전 관리·빌드·테스트, CI/CD, 다중 팀·환경, 네트워킹, 보안, 데이터 저장, 모니터링, 그리고 DevOps의 미래 — 을 실무 관점에서 훑는 책입니다. 상위 [`04_cicd/`](../../README.md) 폴더가 책별로 정독 노트를 모으는 컨벤션을 따르되, 책 구분을 ch 누적 번호가 아니라 **책 전용 폴더**(`fdsd_fundamentals-devops/`)로 합니다. 폴더명 `fdsd`는 **F**undamentals of **D**evOps and **S**oftware **D**elivery에서 왔고, 같은 폴더의 《CI/CD Design Patterns》(`cicd`)와 출처가 섞이지 않게 구분합니다.

파일명은 `{장 번호}-{편 순번}.{제목}.md` 형식입니다. 앞 번호는 책의 실제 장 번호(01~11)이고, 뒤 번호는 그 장을 여러 편으로 쪼갠 순번입니다. 책 구분의 1차 기준은 각 노트의 `source` 필드입니다.

> **톤·시각화는 합니다체 + 핵심 요약 SVG 1장 + Mermaid를 씁니다.** 합니다체 본문에 각 편마다 `_assets/`의 요약 SVG 1장을 도입부에 `![설명](./_assets/{슬러그}.svg)`로 **임베드**하고, 흐름·상태전이가 자연스러운 곳에 Mermaid를 더합니다. 상위 writing 스킬 SSOT를 따릅니다.



## 정독 대상 책

| 항목 | 내용 |
|------|------|
| 제목 | Fundamentals of DevOps and Software Delivery |
| 구성 | 11장 (배포 → IaC → 오케스트레이션 → 버전·빌드·테스트 → CI/CD → 다중 팀·환경 → 네트워킹 → 보안 → 데이터 → 모니터링 → 미래) |
| 관점 | 실무 중심, "Minimum Effective Dose"·"아프면 더 자주 하라" 같은 점진 도입 원칙 |

> 저자·출판사·ISBN·출판 연도·예제 코드 저장소는 원문 판권면을 확인하는 시점에 보강합니다.



## 장 ↔ 정독 노트 매핑

진척 컬럼: ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

각 장의 제목·핵심 키워드는 원본 소스(`docs/05_DevOps/Fundamentals of DevOps and Software Delivery/`)의 장 제목·핵심 요약에서 읽어 적었습니다. 세부 노트는 해당 장을 합니다체로 재작성하는 시점에 채웁니다 — 본문을 재작성하기 전에는 장 세부를 추측해 채우지 않습니다.

| 장 | 제목 | 노트 | 진척 |
|----|------|------|------|
| 1장 | How to Deploy Your App (앱 배포 방법) | — | ◻ 서버 배포·클라우드 기본·PaaS→IaaS·DevOps 점진 도입·Minimum Effective Dose |
| 2장 | How to Manage Your Infrastructure as Code (인프라를 코드로 관리) | — | ◻ ClickOps의 한계·IaC 4범주(ad hoc·구성 관리·서버 템플릿·프로비저닝)·자동화/문서화/버전 관리 |
| 3장 | How to Manage Your Apps by Using Orchestration Tools (오케스트레이션) | — | ◻ 오케스트레이션 10대 문제·서버/VM/컨테이너/서버리스 4유형·스케줄링·롤백·오토스케일·서비스 통신 |
| 4장 | How to Version, Build, and Test Your Code (버전·빌드·테스트) | — | ◻ Git/GitHub·빌드 시스템(npm)·자동화 테스트·TDD·변경에 대한 자신감 |
| 5장 | How to Set Up CI/CD (CI/CD 설정) | — | ◻ CI 원칙·trunk-based·self-testing build·feature toggle·machine user vs OIDC·배포 전략 6종·GitOps·GitHub Actions |
| 6장 | How to Work with Multiple Teams and Environments (다중 팀·환경) | — | ◻ 분할 정복·환경 분리·코드베이스를 라이브러리/서비스로 분할·독립 관리 |
| 7장 | How to Set Up Networking (네트워킹 설정) | — | ◻ 퍼블릭(IP·DNS)·프라이빗(VPC)·접근(SSH·VPN·Zero Trust)·서비스 통신(Service Discovery·gRPC·Service Mesh) |
| 8장 | How to Secure Communication and Storage (통신·저장소 보안) | — | ◻ "직접 만들지 말라"·검증된 알고리즘(AES-GCM·ChaCha20·RSA-OAEP)·Encryption at Rest/in Transit·Secrets Manager·Let's Encrypt·Argon2id |
| 9장 | How to Store Data (데이터 저장) | — | ◻ 사용 사례별 저장소(관계형·캐시·객체·문서·컬럼형·메시지 큐·이벤트 스트림)·복제·파티셔닝·3-2-1 백업 |
| 10장 | How to Monitor Your Systems (시스템 모니터링) | — | ◻ 로그·메트릭·이벤트·알림 4요소·구조화 JSON·메트릭 5유형·관측 가능성·분산 추적·블레임리스 포스트모템 |
| 11장 | The Future of DevOps and Software Delivery (미래) | — | ◻ 추상화 상승·Infrastructureless·Generative AI(코딩 어시스턴트·RAG)·Secure by Default·Platform Engineering(IDP) |

> 미작성 장은 합니다체 재작성에 착수할 때 비로소 노트를 만듭니다. 빈 노트 사전 생성은 하지 않습니다. 각 장은 원문 분량을 보고 분할안을 먼저 제안한 뒤 작성합니다.



## 작성 규칙

- 원본 `docs/05_DevOps/Fundamentals of DevOps and Software Delivery/NN_*.md`의 본문 사실·예시·수치를 보존하면서 한다체 → 합니다체로 변환하고 구조를 재편합니다.
- 도입부에 요약 SVG 1장을 임베드하고(`_assets/NN-MM.{english-slug}.svg`), 흐름·상태전이에 Mermaid를 더합니다.
- 작성 후 인간화 점검과 빈 줄 구조 규칙을 통과시킵니다.
