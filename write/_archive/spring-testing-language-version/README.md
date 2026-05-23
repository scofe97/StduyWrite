---
title: testing — Spring 테스트 패턴 시리즈
tags: [java, spring, junit5, mockito, testcontainers, kafka-test, wiremock, archunit]
status: final
source:
  - https://tech.kakaopay.com/post/given-test-code/
  - https://tech.kakaopay.com/post/given-test-code-2/
  - https://tech.kakaopay.com/post/mock-test-code/
  - https://tech.kakaopay.com/post/mock-test-code-part-2/
  - https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing
related:
  - ../../../04_messaging/04_BrokerArchitecture/01-08.Kafka 공통 정책 스타터 패턴.md
  - ../../../04_messaging/05_ConsistencyPattern/01-05.Inbox.md
updated: 2026-05-16
---

# Spring 테스트 패턴 시리즈

---

> TPS 코드베이스(`executor`·`message-lib`·`operator` 3개 모듈, 총 **311개 테스트 파일**)에 누적된 스프링 테스트 패턴을 정리한 시리즈다. 카카오페이 기술 블로그 4편(Given Part 1·3, Mock Part 1·2)을 출발점으로 삼아, TPS의 실제 코드를 도메인 언어로 변형해 다룬다.



## 왜 이 시리즈인가

테스트 패턴이 코드 안에 흩어져 있으면 신규 합류자가 *같은 결정을 다시* 한다. `AbstractMariaDbIntegrationTest`가 왜 `@DirtiesContext`를 피하는지, `JenkinsWireMockSupport`가 왜 static WireMockServer를 쓰는지, `EventPublisherTest`가 왜 `ArgumentCaptor`로 검증하는지 — 결정의 *근거*를 묶어 두지 않으면 일관성이 깨진다.

이 시리즈는 그 결정 근거를 한 곳에 모은다. 카카오페이 글이 던지는 두 축을 골격으로 잡는다.

- **Given/When/Then 가독성** (Given Part 1·3): 데이터 셋업은 *검증이 아니다*. 핵심에 집중.
- **Mock 전략과 설계 피드백** (Mock Part 1·2): 테스트가 어렵다 = 설계 개선 신호.



## 시리즈 구성 (9편)

| # | 제목 | 핵심 메시지 |
|---|------|-------------|
| 01-01 | [테스트 철학과 카테고리](01-01.테스트%20철학과%20카테고리.md) | 테스트 코드는 *구현의 첫 사용자*. Unit/Slice/Integration/E2E 분류와 TPS 분포 |
| 01-02 | [Given-When-Then 구조](01-02.Given-When-Then%20구조.md) | 데이터 셋업은 검증이 아니다. BDDMockito·세 가지 지옥·대표 fixture |
| 02-01 | [Unit 테스트 패턴](02-01.Unit%20테스트%20패턴.md) | POJO 테스트, AssertJ, JUnit 5(`@DisplayName`, `@Nested`), `Clock.fixed` |
| 02-02 | [Mock 전략과 설계 피드백](02-02.Mock%20전략과%20설계%20피드백.md) | Mock Server vs `@MockBean` vs `@TestConfiguration` vs `java-test-fixtures`. ArgumentCaptor |
| 03-01 | [Slice 테스트 (@WebMvcTest·@DataJpaTest)](03-01.Slice%20테스트.md) | Slice 어노테이션의 메커니즘. TPS에 거의 없는 이유 |
| 03-02 | [Integration 테스트와 @SpringBootTest](03-02.Integration%20테스트.md) | `@ServiceConnection` + Testcontainers MariaDB. ApplicationContext 재사용 |
| 04-01 | [Kafka·Outbox·Inbox 테스트](04-01.Kafka%20테스트.md) | `@EmbeddedKafka`, Awaitility, `@RetryableTopic` 가드, ArchUnit |
| 04-02 | [WireMock과 E2E 테스트](04-02.WireMock과%20E2E.md) | static WireMockServer, fault injection, concurrency 검증 |
| 05-01 | [Test Fixture와 testFixtures 플러그인](05-01.Test%20Fixture.md) | DomainFixture·DomainIoFixture, ObjectMother, `java-test-fixtures` 결정 트리 |



## 카카오페이 4편 한 줄 요약

이 시리즈가 출발점으로 삼는 원문이다. 각 편 본문에서 *어디서 인용했는지* 명시한다.

| 원문 | 핵심 |
|------|------|
| [Given Part 1](https://tech.kakaopay.com/post/given-test-code/) | 데이터 셋업이 *검증을 가린다*. JSON/`@Sql` 같은 외부 자원으로 분리해 핵심에 집중 |
| [Given Part 3](https://tech.kakaopay.com/post/given-test-code-2/) | *세 가지 지옥*: 파라미터·멀티모듈·Mocking. `DomainFixture`·`java-test-fixtures`로 해결 |
| [Mock Part 1](https://tech.kakaopay.com/post/mock-test-code/) | Mock Server / `@MockBean` / `@TestConfiguration` / `java-test-fixtures` 진화 비교. main에 Mock Bean 등록 금지 |
| [Mock Part 2](https://tech.kakaopay.com/post/mock-test-code-part-2/) | 테스트는 *구현의 첫 사용자*. 책임 분리·외부 의존성 차단·POJO 테스트로 설계가 개선됨 |



## TPS 모듈별 테스트 분포

| 모듈 | 테스트 파일 수 | 비고 |
|------|--------------|------|
| executor | 76 | Jenkins E2E + WireMock + 도메인 단위 테스트 중심 |
| message-lib | 10 | Outbox·Kafka 설정 단위/통합 테스트 |
| operator | 225 | ticket 도메인 중심, Testcontainers MariaDB 다수 |
| **합계** | **311** | |



## 시리즈 읽기 순서

처음 읽는다면 **01-01 → 01-02 → 02-01 → 02-02** 순서가 자연스럽다. 그 뒤는 도메인 관심사에 따라 갈라 읽는다.

- *Spring 통합이 궁금하면*: 03-01 → 03-02
- *Kafka·메시지 큐 테스트가 궁금하면*: 04-01 → 04-02
- *Fixture 재사용이 어려우면*: 05-01

각 편은 *카카오페이 원문 인용 → TPS 코드 인용 → 변형 지점 설명*의 순서로 본다.
