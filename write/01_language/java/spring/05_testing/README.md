---
title: Spring 테스트 학습 묶음
tags: [moc, spring, spring-boot, testing, junit5, mockito, testcontainers, archunit]
status: final
related:
  - ../README.md
  - ../04_webflux/02-03.테스트 (MockWebServer와 WebTestClient).md
  - ../../../../06_data/spring/querydsl/02-02.테스트와 멀티모듈.md
updated: 2026-05-09
---

# Spring 테스트 학습 묶음

Spring Boot 3.x 기준으로 단위 테스트에서 외부 시스템 E2E까지를 한 줄기로 엮은 학습 시리즈다. 한 챕터씩 따로 읽어도 닫혀 있도록 썼지만, 전체를 순서대로 따라가면 테스트 피라미드의 어느 층이 어떤 결함을 잡는지를 비용·속도·신뢰도 트레이드오프와 함께 손에 익힐 수 있다.



## 이 묶음의 위치

`spring/04_webflux/02-03.테스트` 가 WebClient 한 어댑터의 단위 테스트에 집중한다면, 이 묶음은 **단위 테스트의 모범 작성법부터 시작해 슬라이스·통합·E2E·아키텍처 가드까지 전 계층의 사용법과 함정을 다룬다**. WebClient 챕터를 먼저 읽었다면 이 묶음의 1장(기초)을 빠르게 건너뛸 수 있고, JPA 위주로 들어가는 사람은 `06_data/spring/querydsl/02-02.테스트와 멀티모듈` 과 본 묶음의 02-01을 함께 본다.



## 학습 곡선

읽는 순서 자체가 비용·환경 의존도가 낮은 것에서 높은 것 순이다. 단위 테스트는 컨텍스트를 띄우지 않아 1초 안에 끝나고, 슬라이스 테스트는 Spring 컨텍스트 일부만 띄워 수 초 내 완료된다. 통합 테스트부터는 Testcontainers·EmbeddedKafka 같은 인프라가 함께 뜨면서 수십 초가 들고, 외부 시스템 E2E는 WireMock으로 격리하지 않으면 환경 가용성에 결과가 묶인다. 이 순서를 의식하면 빌드 시간이 폭주하기 전에 어느 층에 테스트를 늘릴지 판단이 선다.



## 챕터 (총 9편, 2장 구성)

### 1장 — 기초: 단위·슬라이스 테스트

| # | 제목 | 핵심 |
|---|------|------|
| 01-01 | [테스트 피라미드와 Spring 테스트 종류](01-01.테스트%20피라미드와%20Spring%20테스트%20종류.md) | 단위/슬라이스/통합/E2E 분류, `*Test`/`*IT`/`*E2ETest` 네이밍, Gradle `test`/`integrationTest` task 분리 |
| 01-02 | [JUnit 5 + AssertJ로 단위 테스트 작성](01-02.JUnit%205%20+%20AssertJ로%20단위%20테스트%20작성.md) | `@DisplayName` 한글 컨벤션, AssertJ fluent API, `Clock.fixed`로 시간 결정성, Logback `ListAppender`로 로그 검증 |
| 01-03 | [Mockito와 MockMvc 슬라이스](01-03.Mockito와%20MockMvc%20슬라이스.md) | BDDMockito `then().should()`, `ArgumentCaptor`, `MockMvcBuilders.standaloneSetup` vs `@WebMvcTest`, `@Nested` 시나리오 그룹화 |
| 01-04 | [@SpringBootTest와 ApplicationContextRunner](01-04.@SpringBootTest와%20ApplicationContextRunner.md) | `webEnvironment` 옵션, `ApplicationContextRunner`로 AutoConfiguration 슬라이스, `@TestConfiguration` + `@EnableAutoConfiguration(exclude=...)` 조립 |

### 2장 — 통합·E2E·가드레일

| # | 제목 | 핵심 |
|---|------|------|
| 02-01 | [Testcontainers와 진짜 DB 통합 테스트](02-01.Testcontainers와%20진짜%20DB%20통합%20테스트.md) | `@Testcontainers`/`@DynamicPropertySource` vs `@ServiceConnection`(Boot 3.1+), init script, Object Mother 시드 |
| 02-02 | [EmbeddedKafka·Testcontainers로 메시징 테스트](02-02.EmbeddedKafka·Testcontainers로%20메시징%20테스트.md) | `@EmbeddedKafka`, DLQ 라우팅, `ErrorHandlingDeserializer`, `@RetryableTopic` 컴파일 가드 |
| 02-03 | [ArchUnit으로 아키텍처 가드레일](02-03.ArchUnit으로%20아키텍처%20가드레일.md) | slices/noClasses DSL, 헥사고날 5룰 베이스라인, false-positive 회피와 점진 도입 |
| 02-04 | [WireMock과 외부 시스템 E2E](02-04.WireMock과%20외부%20시스템%20E2E.md) | `wm.stubFor` 응답 주입, 스케줄러 자동 실행 억제, "stub 미설정 = 호출 안 됨" 음성 검증, `@Transactional` reflection 가드 |
| 02-05 | [TPS 메시징 플로우 종합 E2E](02-05.TPS%20메시징%20플로우%20종합%20E2E.md) | API → Outbox → Kafka → Consumer 풀 흐름, race 흡수 폴링, CloudEvents 헤더, ThreadLocal 누수 방지 |



## 이 묶음의 톤

각 챕터는 다음 4단을 따른다.

1. **왜 이 단계가 필요한가** — 다른 단계로는 잡지 못하는 결함이 무엇인지를 한 문단으로 설명한다.
2. **핵심 API와 어노테이션** — 표나 짧은 코드 예로 결정적 차이를 보인다.
3. **함정과 회피** — Ryuk 비활성으로 인한 컨테이너 누수, schema-registry timeout 30초, ThreadLocal 누수 같은 실제 사고 사례를 정리한다.
4. **TPS 사례** — operator·message-lib·executor 모듈에서 짧게 인용한다. 사내 도메인이 본질이 아닌 인용은 일반화하고, 흐름이 본질인 인용은 그대로 둔다. 종합 챕터(02-05)는 사례 분석에 한 챕터를 통째로 쓴다.



## 관련 문서

- [04_webflux/02-03.테스트 (MockWebServer와 WebTestClient)](../04_webflux/02-03.테스트%20(MockWebServer와%20WebTestClient).md) — WebClient 어댑터 단위 테스트, 본 묶음 1장과 보완 관계
- [06_data/spring/querydsl/02-02.테스트와 멀티모듈](../../../../06_data/spring/querydsl/02-02.테스트와%20멀티모듈.md) — JPA·QueryDSL 멀티모듈 빌드의 테스트 분리, 본 묶음 02-01과 보완 관계
- [Spring 학습 통합 MOC](../README.md) — 전 카테고리 Spring 문서 진입점
