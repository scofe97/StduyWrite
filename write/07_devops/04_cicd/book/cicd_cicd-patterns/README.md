---
title: CI/CD Design Patterns 정독 인덱스
tags: [cicd, ci-cd, design-pattern, gof, deployment-strategy, anti-pattern, ddd, study-index, moc]
status: draft
source:
  - 《CI/CD Design Patterns》
related:
  - ../../README.md
  - ../fdsd_fundamentals-devops/README.md
updated: 2026-06-28
---


# CI/CD Design Patterns 정독 인덱스
> 《CI/CD Design Patterns》의 장 단위 정독 노트 인덱스입니다 — 04_cicd 폴더의 두 번째 정독 대상 책

이 폴더는 단행본 《CI/CD Design Patterns》의 정독 노트를 모읍니다. GoF 디자인 패턴의 렌즈로 CI/CD를 다시 보는 책으로, 패턴의 기원(Christopher Alexander → GoF)부터 구조·행위·생성 패턴, 배포 전략, 규제 산업의 DDD 적용, 감사·평가, AI 통합, 그리고 안티패턴까지 이어집니다. 상위 [`04_cicd/`](../../README.md) 폴더가 책별로 정독 노트를 모으는 컨벤션을 따르되, 책 구분을 ch 누적 번호가 아니라 **책 전용 폴더**(`cicd_cicd-patterns/`)로 합니다. 폴더명 `cicd`는 책 제목에서 왔고, 같은 폴더의 《Fundamentals of DevOps and Software Delivery》(`fdsd`)와 출처가 섞이지 않게 구분합니다.

파일명은 `{장 번호}-{편 순번}.{제목}.md` 형식입니다. 앞 번호는 책의 실제 장 번호(01~14)이고, 뒤 번호는 그 장을 여러 편으로 쪼갠 순번입니다. 책 구분의 1차 기준은 각 노트의 `source` 필드입니다.

> **톤·시각화는 합니다체 + 핵심 요약 SVG 1장 + Mermaid를 씁니다.** 합니다체 본문에 각 편마다 `_assets/`의 요약 SVG 1장을 도입부에 `![설명](./_assets/{슬러그}.svg)`로 **임베드**하고, 흐름·상태전이가 자연스러운 곳에 Mermaid를 더합니다. 상위 writing 스킬 SSOT를 따릅니다.



## 정독 대상 책

| 항목 | 내용 |
|------|------|
| 제목 | CI/CD Design Patterns |
| 구성 | 14장 (기초 → 패턴 유형 → 테스트·배포 → 비즈니스 정렬 → 구조 패턴 → 배포 전략 → 행위 패턴 → 규제 DDD → 생성 패턴 → 클라우드 → 감사·평가 → 고급·AI → 안티패턴 → 부록) |
| 관점 | GoF 디자인 패턴(생성·구조·행위)을 CI/CD 파이프라인 설계에 매핑 |

> 저자·출판사·ISBN·출판 연도·예제 코드 저장소는 원문 판권면을 확인하는 시점에 보강합니다.



## 장 ↔ 정독 노트 매핑

진척 컬럼: ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

각 장의 제목·핵심 키워드는 원본 소스(`docs/05_DevOps/CICD Pattern/`)의 파일명·핵심 요약에서 읽어 적었습니다. 세부 노트는 해당 장을 합니다체로 재작성하는 시점에 채웁니다 — 본문을 재작성하기 전에는 장 세부를 추측해 채우지 않습니다.

| 장 | 제목 | 노트 | 진척 |
|----|------|------|------|
| 1장 | Foundations of CI/CD Design Patterns (기초) | — | ◻ 디자인 패턴 기원(GoF)·CI/CD 관계·Push/Pull 배포 모델·테스트 피라미드/다이아몬드·Rolling/Blue-Green/Canary 개념 |
| 2장 | Types of CI/CD Design Patterns and Components (유형·구성요소) | — | ◻ Pipeline as Code(PaC)·Infrastructure as Code(IaC)·순차/병렬 실행·도구별 PaC 구현(Jenkins·GitLab·GitHub Actions) |
| 3장 | Advancing CI/CD Testing to Deployment (테스트→배포) | — | ◻ 테스트 자동화 패턴 적용·아티팩트 관리 전략·배포 유형·브랜칭 전략 |
| 4장 | Business Outcome Alignment with CI/CD (비즈니스 정렬) | — | ◻ OKR 기반 목표 설정·DORA 메트릭 측정·조직 차원 CI/CD 도입 확대 |
| 5장 | Exploring Structural CI/CD Design Patterns (구조 패턴) | — | ◻ Monorepo vs Polyrepo·파이프라인 의존성 관리·도구/코드/모듈화·RBAC 접근 제어 |
| 6장 | Deployment Strategies for Structural Patterns (구조 패턴 배포 전략) | — | ◻ 5대 배포 전략(Blue-Green·Canary·Feature Toggle·A/B·Dark Launch)·CI/CD 단계별 데이터 신호·CDEvents |
| 7장 | Understanding Behavioral Design Patterns for CI/CD (행위 패턴) | — | ◻ 10대 행위 패턴(Chain of Responsibility·Command·Observer·Strategy 등)·AI 기반 관찰성·BDD |
| 8장 | Domain Driven Design Patterns for Regulated Sectors (규제 DDD) | — | ◻ Bounded Context·Ubiquitous Language·RBAC/ABAC·GDPR/HIPAA/PCI DSS 규제 준수 파이프라인 |
| 9장 | Applying Creational CI/CD Design Patterns (생성 패턴) | — | ◻ Factory Method·Abstract Factory·Singleton·Prototype·Builder·클라우드 네이티브 확장성/복원력·컨테이너화 |
| 10장 | Deployment Strategies — Creational CI/CD with Cloud Providers (클라우드) | — | ◻ Landing Zone·Singleton 표준화(저장소/파이프라인/IaC)·Blue-Green/Canary/Rolling·Team Topologies |
| 11장 | Auditing and Assessment of Design Patterns (감사·평가) | — | ◻ 평가 vs 감사 차이·Shift-Left 감사·Quality Gate 자동화·성숙도 모델 |
| 12장 | Advanced CI/CD Design Patterns and Use Cases (고급·AI) | — | ◻ ML·생성형 AI 통합·자가 학습 CI/CD·실시간 유틸리티 기반 패턴·AI 주도 미래 로드맵 |
| 13장 | Exploring Anti-Patterns for CI/CD Design Pattern Deployments (안티패턴) | — | ◻ 7대 안티패턴 인식·회피·최적 패턴 선택·플랫폼 엔지니어링 시너지 |
| 14장 | Appendix — Knowledge Test and Case Studies (부록) | — | ◻ 15개 퀴즈 지식 점검·3가지 실제 케이스 스터디·전체 복습 |

> 미작성 장은 합니다체 재작성에 착수할 때 비로소 노트를 만듭니다. 빈 노트 사전 생성은 하지 않습니다. 각 장은 원문 분량을 보고 분할안을 먼저 제안한 뒤 작성합니다.



## 작성 규칙

- 원본 `docs/05_DevOps/CICD Pattern/NN_*.md`의 본문 사실·예시·수치를 보존하면서 한다체 → 합니다체로 변환하고 구조를 재편합니다.
- 도입부에 요약 SVG 1장을 임베드하고(`_assets/NN-MM.{english-slug}.svg`), 흐름·상태전이에 Mermaid를 더합니다.
- 작성 후 인간화 점검과 빈 줄 구조 규칙을 통과시킵니다.
