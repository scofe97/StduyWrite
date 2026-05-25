---
title: 스프링 이벤트 학습 MOC
tags: [moc, spring, spring-boot, event, transactional-event-listener, async]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../05_aop/README.md
updated: 2026-05-24
---

# 스프링 이벤트 학습 MOC
---

> 스프링의 `ApplicationEvent` 기능은 한 객체의 상태 변화를 다른 객체에 느슨하게 알리는 인프라입니다. 본 묶음은 그 이벤트 기능을 두 축으로 따라갑니다. 하나는 *언제* 실행되는가(트랜잭션 Phase), 다른 하나는 *어느 스레드에서* 실행되는가(동기/비동기)입니다. 단순 `@EventListener` 부터 시작해 `@TransactionalEventListener` 의 Phase·전파 함정·내부 동작·비동기 분리까지, 실무에서 한 번씩 데이게 되는 지점을 미리 짚습니다.

## 왜 별도 묶음인가

스프링 이벤트는 AOP도 MVC도 아닌 독립 주제입니다. `DispatcherServlet` 흐름(`01_core/`)이나 횡단 관심사(`05_aop/`)와 달리, 이벤트는 *발행자와 구독자를 떼어 놓는* 한 가지 관심사에 집중합니다. 그런데 이 단순해 보이는 기능이 트랜잭션과 만나는 순간 "커밋 후에 실행했더니 DB 쓰기가 사라진다", "비동기로 돌렸더니 트랜잭션이 끊긴다" 같은 함정이 줄줄이 나옵니다. 그 함정들을 한 흐름으로 엮어야 어느 도구가 어느 자리를 메우는지 헷갈리지 않습니다.

## 학습 순서

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [스프링 이벤트와 두 리스너 — @EventListener vs @TransactionalEventListener](01-01.스프링%20이벤트와%20두%20리스너%20—%20@EventListener%20vs%20@TransactionalEventListener.md) | 이벤트 기반 분리, 두 리스너의 실행 시점 차이, 트랜잭션 Phase 4종, fallbackExecution·condition |
| 01-02 | [트랜잭션 전파 조합 — 죽은 트랜잭션과 REQUIRES_NEW](01-02.트랜잭션%20전파%20조합%20—%20죽은%20트랜잭션과%20REQUIRES_NEW.md) | AFTER_COMMIT + REQUIRED의 DB 쓰기 손실, REQUIRES_NEW 해법, Spring 6.2/Boot 3.5 fail-fast 검증 |
| 01-03 | [@TransactionalEventListener 내부 동작 원리](01-03.@TransactionalEventListener%20내부%20동작%20원리.md) | TransactionSynchronization 콜백, ThreadLocal 등록소, 어댑터의 발행 시 등록 → 커밋 시 트리거 |
| 01-04 | [동기와 비동기 이벤트 — @Async와 보상 트랜잭션](01-04.동기와%20비동기%20이벤트%20—%20@Async와%20보상%20트랜잭션.md) | 동기 vs @Async 트랜잭션·예외·성능 비교, 보상 트랜잭션 4전략, 선택 기준 |

처음 보는 학습자는 01-01 부터 순서대로 따라가면 됩니다. 01-01이 "언제 실행되는가"의 전체 지도를 그리고, 01-02가 그 위에서 가장 자주 데는 함정(죽은 트랜잭션)을 짚으며, 01-03이 그 함정이 왜 생기는지를 내부 코드로 설명합니다. 01-04는 축을 "어느 스레드인가"로 바꿔 비동기 처리와 보상을 다룹니다. 실무에서 함정만 빠르게 확인하려면 01-02부터 봐도 됩니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Framework | 6.2.x | `@TransactionalEventListener` 검증 로직 포함 |
| Spring Boot | 3.5.x | fail-fast 검증(01-02 §3) 기준 |
| Java | 17+ | `switch` 표현식(01-03 예제) 사용 |

## 사전 지식

> 본 묶음은 다음을 안다고 가정합니다.

1. `@Transactional` 의 전파(propagation) 개념 — 특히 `REQUIRED` 와 `REQUIRES_NEW` 의 차이를 한 문장으로 설명할 수 있습니다.
2. `ApplicationContext` 가 빈을 관리하고 `ApplicationEventPublisher` 를 제공한다는 사실 — 막히면 [`../01_core/01-01`](../01_core/01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) §4 를 봅니다.
3. `ThreadLocal` 이 스레드별 독립 저장소라는 점 — 막히면 [`../05_aop/01-03`](../05_aop/01-03.템플릿·콜백과%20ThreadLocal%20—%20AOP%20등장%20직전의%20두%20시도.md) §5 를 봅니다.

## 면접 대비 체크리스트

> 네 편을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. `@EventListener` 와 `@TransactionalEventListener` 는 무엇이 다른가? 이메일 전송을 어느 쪽에 둬야 안전한가?
2. 트랜잭션 Phase 네 종류와 각 실행 시점은? `AFTER_COMMIT` 이 기본값인 이유는?
3. `@TransactionalEventListener(AFTER_COMMIT)` 에서 `@Transactional(REQUIRED)` 로 DB를 저장하면 왜 사라지는가? 해법은?
4. "발행은 트랜잭션 안인데 실행은 커밋 후"가 어떻게 가능한가? `TransactionSynchronization` 의 역할은?
5. `@Async` 리스너가 발행자 트랜잭션에 참여하지 못하는 이유는? 그래서 무엇이 필요한가?

각 질문에 막히면 해당 편의 본문으로 돌아갑니다.

## 원본 학습 자료

본 묶음은 노션 학습 노트(`_notion_import/_unsorted/` 의 이벤트 리스너 1~3편 + 스프링 이벤트 동기/비동기)를 통합 재작성한 산출물입니다. 원본은 재작성 완료 후 제거됐고, 이력은 [`../_notion_import/README.md`](../_notion_import/README.md) 에 있습니다.

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [`../01_core/`](../01_core/) — `ApplicationEventPublisher` 가 속한 컨테이너의 부가 기능
- [`../05_aop/`](../05_aop/) — `@Async`·`@Scheduled` 가 의지하는 AOP 프록시
- [TransactionalEventListener (Spring Framework API)](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/event/TransactionalEventListener.html) — 공식 레퍼런스
