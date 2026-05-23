---
title: Spring AOP 학습 MOC
tags: [moc, spring, spring-boot, aop, aspect, proxy]
status: draft
source:
  - https://docs.spring.io/spring-framework/reference/core/aop.html
  - https://docs.spring.io/spring-framework/reference/core/aop-api.html
related:
  - ../README.md
  - ../03_mvc/
  - ../08_exception-handling/
updated: 2026-05-23
---

# Spring AOP 학습 MOC

---

> 로깅·트랜잭션·인증 같은 "횡단 관심사" 가 어떻게 자바 표준 동적 프록시에서 출발해 Spring `@Aspect` AOP 까지 정돈됐는지를 한 흐름으로 묶은 학습 묶음입니다. Spring AOP 를 처음 접하는 사람부터, `@Around` 를 쓰면서도 내부에서 무엇이 일어나는지 설명이 막히는 사람까지가 대상입니다.

## 왜 별도 묶음인가

`@Transactional` 한 줄, `@Async` 한 줄, `@Cacheable` 한 줄. Spring 을 쓰면서 가장 자주 마주치는 이 세 어노테이션은 모두 AOP 위에 서 있습니다. 그런데 "어노테이션을 붙이면 동작한다" 만 알고 있으면, 같은 클래스에서 호출했더니 `@Transactional` 이 안 먹는다거나, `@Cacheable` 이 동작 안 한다는 문제를 만났을 때 원인을 짚지 못합니다.

본 묶음은 AOP 가 단계적으로 발전한 다섯 지점(횡단 관심사 → JDK 동적 프록시 → ProxyFactory → 빈 후처리기 → `@Aspect`)을 그대로 따라가면서, 각 단계가 이전 단계의 어떤 불편함을 해결했는지를 묻습니다. 마지막에는 실무에서 가장 자주 만나는 함정(internal call, proxy-target-class)을 정리합니다.

## 학습 순서

> 핵심 1편이 횡단 관심사 등장부터 `@Aspect` 까지를 압축하고, 01-03 이 그 직전 단계로서 객체지향 패턴 두 가지의 한계를 보여 줍니다. 01-02 는 같은 폴더에 두는 별 주제(스프링 스케줄링)로, 횡단 관심사와는 직접 관계가 없습니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [횡단 관심사와 AOP — 프록시로 풀어내기](01-01.횡단%20관심사와%20AOP%20—%20프록시로%20풀어내기.md) | 횡단 관심사 / Filter·Interceptor 한계 / JDK·CGLIB 동적 프록시 / ProxyFactory / 빈 후처리기 / `@Aspect` / Pointcut 표현식 / Advice 5종 / internal call / proxy-target-class |
| 01-03 | [템플릿·콜백과 ThreadLocal — AOP 등장 직전의 두 시도](01-03.템플릿·콜백과%20ThreadLocal%20—%20AOP%20등장%20직전의%20두%20시도.md) | 템플릿 메서드 패턴 / 콜백 패턴 (`JdbcTemplate`·`TransactionTemplate` 의 뿌리) / `ThreadLocal` 상태 격리와 누수 / 세 도구의 공통 한계 — *호출부 협조 강제* / AOP 가 가져온 전환 |
| 01-02 | [스프링 스케줄링 — @Scheduled에서 Quartz까지](01-02.스프링%20스케줄링%20—%20@Scheduled에서%20Quartz까지.md) | 배치 vs 스케줄러 / `@Scheduled` / `ThreadPoolTaskScheduler` / Quartz 4구성 / JobStore(RAM·JDBC) / Trigger(Simple·Cron) / Cluster 모드 / Stateful Job / 결정 트리 |

학습 동선은 두 가지로 갈립니다. AOP 의 *왜* 부터 차근차근 본다면 01-03 → 01-01 순으로 진입해, 객체지향 패턴의 한계를 먼저 보고 AOP 가 그 한계를 어떻게 푸는지를 이어 읽습니다. AOP 어노테이션을 이미 써 본 입장이라면 01-01 §3·§5 로 직진한 뒤 01-03 으로 뒤돌아 *왜 굳이 동적 프록시인가* 의 동기만 확인해도 됩니다. `@Transactional` 의 internal call 문제로 디버깅 중이라면 01-01 §9 로 직행합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-aop` 가 `AnnotationAwareAspectJAutoProxyCreator` 자동 등록 |
| Spring Framework | 6.2.x | AspectJ 표현식 `execution`·`@annotation` 등 지원 |
| Java | 17+ | `Proxy.newProxyInstance` 표준 API |
| AspectJ | 1.9.x (런타임 표현식 평가) | 컴파일 시점 위빙은 미사용, 런타임 프록시만 사용 |

Spring Boot 의 기본값 `spring.aop.proxy-target-class=true` 가 적용되어 CGLIB 기반 프록시가 만들어진다는 점만 유의하면, 본문 코드는 대부분 환경에서 그대로 동작합니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. Spring 의 `@Bean`, `@Component`, `@Autowired` 가 무엇을 하는지 한 문장으로 설명할 수 있습니다.
2. Java 인터페이스와 구현 클래스의 차이를 알고, 다형성으로 인터페이스 타입으로 객체를 받을 수 있습니다.
3. Reflection API 의 존재(`Method`, `Class.forName`)를 들어 본 적이 있습니다. (몰라도 본문에서 보충 가능)
4. Spring MVC 의 `DispatcherServlet`·`HandlerInterceptor` 가 어디에 위치하는지 대략 알고 있습니다.

위 항목 중 막히는 부분이 있으면 [`spring/`](../README.md) 의 다른 묶음(`01_container/`, `03_mvc/`)을 먼저 보고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 1편을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 합니다.

1. 횡단 관심사가 Filter·Interceptor 로 해결되지 않는 영역은 무엇이며, 왜 AOP 가 필요한가?
2. JDK 동적 프록시와 CGLIB 의 차이는? 각각 어떤 제약을 가지는가?
3. `Pointcut`, `Advice`, `Advisor` 의 관계를 한 문장으로 설명할 수 있는가?
4. Spring Boot 에서 AOP 가 자동으로 적용되는 메커니즘은?
5. `@Around` 와 `@Before` 의 차이, 그리고 `@Around` 만 위험한 이유는?
6. `execution` 과 `args` 가 같은 파라미터 패턴 같지만 다른 점은?
7. internal call 문제가 발생하는 이유와 대안 세 가지는?

각 질문에 막히면 1편 본문의 해당 절을 다시 봅니다.

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [Spring MVC — FrontController 에서 DispatcherServlet 까지](../03_mvc/01-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) — Interceptor 가 어디서 끼어드는지 비교
- [예외 처리 — 서블릿에서 @ControllerAdvice 까지](../08_exception-handling/01-01.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md) — `@ControllerAdvice` 가 AOP 와 어떻게 연결되는지 확인
- [Spring Framework Reference — AOP](https://docs.spring.io/spring-framework/reference/core/aop.html) — 본 묶음이 따라가는 공식 문서
- [Spring Framework Reference — AOP APIs](https://docs.spring.io/spring-framework/reference/core/aop-api.html) — `ProxyFactory`·`Advisor` API 의 1차 자료

## 후속 편 계획

> 본 묶음은 1편으로 시작했고, 다음 두 방향으로 확장할 예정입니다.

- **트랜잭션 AOP** — `@Transactional` 이 어떤 `Advisor` 로 등록되며, propagation·rollbackFor 옵션이 프록시 안에서 어떻게 해석되는지 추적합니다.
- **응용 패턴** — `@Async`, `@Cacheable`, `@Retryable` 같은 어노테이션 기반 AOP 가 모두 같은 빈 후처리기 메커니즘 위에 서 있는 사실을 비교 정리합니다.
