---
title: 03_ddd — SSOT 커버리지 갭
tags: [meta, ddd, coverage]
status: draft
related:
  - ./README.md
  - ../../../docs/02_Architecture/02_DDD/
updated: 2026-05-28
---

# 03_ddd — SSOT 커버리지 갭
---
> `docs/02_Architecture/02_DDD/` 13편 ↔ 본 시리즈 매핑. 2026-05-28 시점에 본 시리즈 14편 모두 5블록 보강 완료 (학습 목표 + Mermaid 2개 + 실제 사례 + 면접 Q&A/정답).

## SSOT ↔ 본 시리즈 매핑

| SSOT (docs/02_DDD) | 본 시리즈 | 상태 |
|-------------------|----------|------|
| 01_Evolution_of_Domain_Driven_Design | 01-01 유비쿼터스 언어와 도메인 모델 (흡수) | final |
| 02_Understanding_Complexity_Problem_Solution_Space | 01-03 도메인 책임 분리 (흡수) | final |
| 03_Strategic_Patterns | 01-02 전략적 설계와 전술적 패턴, 01-04 Bounded Context 와 Context Map | final x2 |
| 04_Tactical_Patterns | 02-01 Aggregate 설계 규칙, 02-02 Entity 와 VO, 02-03 Domain Service·Factory·Repository | final x3 |
| 05_Introducing_Refactoring_Principles | 03-01 리팩토링 원칙 | final |
| 06_Transitioning_from_Chaos | 03-02 혼돈에서 벗어나기 | final |
| 07_Integrating_Events_with_CQRS | 04-02 이벤트와 CQRS 통합 (구현은 04_edd) | final |
| 08_Refactoring_the_Database | 03-03 데이터베이스 리팩토링 | final |
| 09_DDD_Patterns_for_CI_CD | 04-03 DDD 와 CI/CD | final |
| 10_Transition_to_Microservices | 03-04 모놀리스에서 마이크로서비스로 | final |
| 11_Dealing_with_Events_and_Their_Evolution | 05_edd/02-05 이벤트 진화 다루기 (위임) | draft (TBD, 04_edd 측) |
| 12_Orchestrating_Complexity | 05_edd/03-02 Choreography vs Orchestration (위임) | draft (TBD, 04_edd 측) |
| 13_DDD_for_AI_Coding | 04-04 AI 코딩 시대의 DDD | final |

## 본 시리즈에만 있는 문서 (SSOT 외 보강)

- **04-01 헥사고날 변형 — TPS 결재 도메인 적용 사례**: 사내 사례 중심으로 작성된 final 문서. Evans/Vernon 원전에는 없는 변형 결정 근거를 다룹니다.

## 보강 작업 이력

2026-05-28 일괄 보강 완료 (4 Stage):

- Stage 1 — 01-01 ~ 01-04 (전략적 설계 4편)
- Stage 2 — 02-01 ~ 02-03 (전술적 설계 3편)
- Stage 3 — 03-01 ~ 03-04 (진화·전환 4편)
- Stage 4 — 04-01 ~ 04-04 (사례·통합 4편) + README + 본 GAP

각 final 문서가 *학습 목표 + Mermaid 2개 이상 + 실제 사례(원전·본인 코드) + 면접 Q&A + 정답 (자답 후 펼치기)* 5블록을 갖춥니다. 산문은 합니다체 ≥30 / 한다체 0 / AI 강조어 0 검증 게이트를 통과했습니다.

## 다음 후속 작업

- 05_edd 측 매핑 항목 (11_, 12_) 의 본 시리즈 위임 부분 작성.
- `_review/` 폴더 운영 시작 (writing §12 간격 반복) — 본 시리즈 면접 Q&A 를 SSOT 로 회차별 자답 기록.
