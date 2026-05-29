---
title: Spring 트랜잭션 학습 MOC
tags: [moc, spring, transaction, transactional, isolation, propagation, testing]
status: draft
source:
  - https://docs.spring.io/spring-framework/reference/data-access/transaction.html
related:
  - ../README.md
  - ../../05_data/jpa/04-01.스프링 트랜잭션.md
  - ../06_events/README.md
updated: 2026-05-29
---

# Spring 트랜잭션 학습 MOC

---

> 트랜잭션의 본질 — `PlatformTransactionManager` 추상화, 스레드 동기화, AOP 프록시, 전파(Propagation), 락 — 은 영속성 도메인인 [`05_data/`](../../05_data/) 에 이미 정리돼 있습니다. 본 묶음은 그 자산을 옮겨 오지 않고 *Spring 관점으로 한 자리에 모으는 집계점* 이며, 거기서 비어 있던 두 조각 — 격리 수준(Isolation)의 Spring 적용과 `@Transactional` 테스트 — 만 보강합니다.


## 이 묶음의 자리 — 본체는 05_data, 여기는 집계와 보강

트랜잭션은 도메인 결합도가 큰 주제입니다. `@Transactional` 한 줄은 영속성 계층(JPA·JDBC)과 떼어 설명하기 어렵고, 그래서 본체 문서는 [`05_data/jpa/`](../../05_data/jpa/) 에 자리잡는 편이 자연스럽습니다. 같은 내용을 `11_spring/` 에 다시 쓰면 두 곳이 어긋나는 순간 어느 쪽이 옳은지 알 수 없게 됩니다.

그래서 본 묶음은 본체를 복제하지 않습니다. 흩어진 트랜잭션 문서가 어디에 있는지를 지도로 모으고, 그 지도에서 *Spring 관점에서만 비어 있던* 두 편 — 격리 수준의 `@Transactional` 적용, 그리고 테스트에서의 트랜잭션 — 을 채웁니다. 본체를 보고 싶으면 지도의 링크를 따라가고, Spring 적용 각도가 궁금하면 본 묶음의 두 편을 봅니다.

## 트랜잭션 지도

> 트랜잭션 관련 문서가 어느 자리에 있는지 한눈에 모았습니다. *기존(SSOT)* 은 그 주제의 정본이 사는 자리이고, *신규* 가 본 묶음에서 보강한 편입니다.

| 주제 | 위치 | 구분 |
|------|------|------|
| 추상화·동기화·AOP·전파 본체 | [`05_data/jpa/04-01`](../../05_data/jpa/04-01.스프링%20트랜잭션.md) | 기존(SSOT) |
| 전파 실무 시나리오 (회원+로그) | [`05_data/jpa/04-01b`](../../05_data/jpa/04-01b.트랜잭션%20전파%20활용.md) | 기존 |
| 낙관적·비관적 락 (`@Version`·`@Lock`) | [`05_data/jpa/04-02`](../../05_data/jpa/04-02.낙관적%20비관적%20락.md) | 기존 |
| 격리 수준·이상현상 (DB 이론) | [`05_data/sql/04-02`](../../05_data/sql/04-02.동시성제어와%20락.md) · [`theory/01-04`](../../05_data/theory/01-04.트랜잭션과%20격리%20수준.md) | 기존(SSOT) |
| `@TransactionalEventListener` Phase·전파 | [`06_events/`](../06_events/README.md) | 기존 |
| **격리 수준 — Spring 적용** | [`01-01`](01-01.트랜잭션%20격리%20수준%20—%20Spring%20관점.md) | 신규 |
| **`@Transactional` 테스트 가드** | [`01-02`](01-02.@Transactional%20테스트%20가드.md) | 신규 |

## 학습 순서 추천

> 본체를 먼저 읽고 본 묶음으로 넘어오는 순서가 자연스럽습니다. 트랜잭션을 처음 보는 단계라면 1번부터, 격리·테스트만 보강하려면 2~3번으로 직행합니다.

1. [`05_data/jpa/04-01`](../../05_data/jpa/04-01.스프링%20트랜잭션.md) — 추상화·동기화·AOP 자기호출 함정·전파를 한 번에. 본 묶음의 전제입니다.
2. [`01-01` 격리 수준 — Spring 관점](01-01.트랜잭션%20격리%20수준%20—%20Spring%20관점.md) — `@Transactional(isolation=...)` 이 DB 격리에 어떻게 얹히는지, 같은 코드가 MySQL 과 PostgreSQL 에서 왜 다르게 도는지.
3. [`01-02` @Transactional 테스트 가드](01-02.@Transactional%20테스트%20가드.md) — 테스트의 자동 롤백이 왜 프로덕션과 의미가 다른지, 자기호출·전파 함정을 테스트로 어떻게 노출시키는지.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-data-jpa` 가 `JpaTransactionManager` 자동 구성 |
| Spring Framework | 6.2.x | `@Transactional`·`TransactionDefinition`·TestContext 트랜잭션 |
| Java | 17+ | |
| 격리 검증 DB | MySQL 8 / PostgreSQL 16 | 기본 격리 수준이 달라 §3 비교에 사용 |

## 관련 문서

- [Spring 통합 MOC](../README.md) — Spring 학습 문서 전체 진입점
- [스프링 트랜잭션 (추상화·동기화·AOP·전파)](../../05_data/jpa/04-01.스프링%20트랜잭션.md) — 본 묶음이 전제하는 본체 문서
- [스프링 이벤트와 두 리스너](../06_events/01-01.스프링%20이벤트와%20두%20리스너%20—%20@EventListener%20vs%20@TransactionalEventListener.md) — 트랜잭션 Phase 와 이벤트의 결합
- [Spring 공식 — Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)
