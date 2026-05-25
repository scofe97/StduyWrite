---
title: 03_ddd — 도메인 주도 설계 시리즈
tags: [moc, architecture, ddd]
status: draft
related:
  - ../README.md
  - ./GAP.md
  - ../../../docs/02_Architecture/02_DDD/
updated: 2026-05-23
---

# 03_ddd — 도메인 주도 설계 시리즈
---
> Evans/Vernon 의 DDD 를 Spring Boot 4.x · Java 25 컨텍스트에서 다시 정리한다. SSOT 는 `docs/02_Architecture/02_DDD/` 13편.

본 시리즈는 4개 절(전략적 설계 · 전술적 설계 · 진화·전환 · 사례·통합) 로 묶인다. CQRS · Event Sourcing 같이 EDD 와 겹치는 주제는 05_edd 가 구현 측을 다루고, 본 시리즈는 모델 의미만 다룬다.

## 절 체계

| 절 | 의미 | 문서 |
|----|------|------|
| 01 | 전략적 설계 — 언어·경계·서브도메인 | 01-01 ~ 01-04 |
| 02 | 전술적 설계 — Aggregate / Entity / VO / Domain Service | 02-01 ~ 02-03 |
| 03 | 진화·전환 — 리팩토링·DB·마이크로서비스 이행 | 03-01 ~ 03-04 |
| 04 | 사례·통합 — 헥사고날·이벤트·CI/CD·AI | 04-01 ~ 04-04 |

## 문서 목록

### 01번대 — 전략적 설계

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 01-01 | [유비쿼터스 언어와 도메인 모델](01-01.유비쿼터스%20언어와%20도메인%20모델.md) | 도메인 언어는 코드에 어떻게 박히는가 | final |
| 01-02 | [전략적 설계와 전술적 패턴](01-02.전략적%20설계와%20전술적%20패턴.md) | Bounded Context 와 Aggregate 결정 기준 | final |
| 01-03 | [도메인 책임 분리와 세부 도메인 식별](01-03.도메인%20책임%20분리와%20세부%20도메인%20식별.md) | sub-domain 과 bounded context 의 차이 | final |
| 01-04 | [Bounded Context 와 Context Map](01-04.Bounded%20Context%20와%20Context%20Map.md) | Context Map 7가지 통신 패턴 | final |

### 02번대 — 전술적 설계

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 02-01 | [Aggregate 설계 규칙](02-01.Aggregate%20설계%20규칙.md) | Root · 트랜잭션 경계 · ID 참조 | final |
| 02-02 | [Entity 와 Value Object](02-02.Entity%20와%20Value%20Object.md) | record · sealed 로 VO 강제 | final |
| 02-03 | [Domain Service, Factory, Repository](02-03.Domain%20Service%2C%20Factory%2C%20Repository.md) | 세 패턴의 책임 분리 | final |

### 03번대 — 진화·전환

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 03-01 | [리팩토링 원칙 — 행동하기 전에 이해하기](03-01.리팩토링%20원칙%20—%20행동하기%20전에%20이해하기.md) | 모델 재발견으로서의 리팩토링 | final |
| 03-02 | [혼돈에서 벗어나기 — 핵심 도메인 식별](03-02.혼돈에서%20벗어나기%20—%20핵심%20도메인%20식별.md) | Core / Supporting / Generic 구분 | final |
| 03-03 | [데이터베이스 리팩토링](03-03.데이터베이스%20리팩토링.md) | Expand–Contract · 듀얼 라이트 | final |
| 03-04 | [모놀리스에서 마이크로서비스로 — 언제, 왜](03-04.모놀리스에서%20마이크로서비스로%20—%20언제%2C%20왜.md) | 분리 의사결정 기준 | final |

### 04번대 — 사례·통합

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 04-01 | [헥사고날 변형 — TPS 결재 도메인 적용 사례](04-01.헥사고날%20변형%20—%20TPS%20결재%20도메인%20적용%20사례.md) | 교과서 헥사고날 변형의 결정 근거 | final |
| 04-02 | [이벤트와 CQRS 통합 — DDD 시점에서](04-02.이벤트와%20CQRS%20통합.md) | Aggregate 가 이벤트를 만드는 이유 | final |
| 04-03 | [DDD 와 CI/CD](04-03.DDD%20와%20CI_CD.md) | Bounded Context 단위 파이프라인 | final |
| 04-04 | [AI 코딩 시대의 DDD](04-04.AI%20코딩%20시대의%20DDD.md) | 구조가 패턴이 된다는 4 원칙 | final |

## SSOT 매핑 / 갭

[`GAP.md`](GAP.md) 가 `docs/02_Architecture/02_DDD/` 13편 ↔ 본 시리즈의 매핑과 미작성 챕터를 박제한다.
