---
title: Spring WebClient 학습 MOC
tags: [moc, spring, spring-boot, webclient, reactive, web]
status: final
source:
  - https://docs.spring.io/spring-framework/reference/web-reactive.html
  - https://docs.spring.io/spring-framework/reference/integration/rest-clients.html
  - https://projectreactor.io/docs/netty/release/reference/
related:
  - ../README.md
  - ../../05_data/querydsl/README.md
updated: 2026-05-09
---

# Spring WebClient 학습 MOC

---

> Spring Framework 6.2 / Spring Boot 3.3+ 환경에서 외부 HTTP 호출을 다루는 학습자가 공식 문서의 유스케이스를 한 번에 훑고, TPS `operator/ticket/approval` 모듈의 실제 어댑터 코드까지 같이 읽도록 묶은 11편이다. RestTemplate 대체로 WebClient를 처음 잡은 사람부터, 운영 코드의 `.block()` 호출 한 줄을 두고 고민하는 사람까지를 대상으로 한다.



## 왜 별도 묶음인가

> Spring HTTP 클라이언트가 한 종류였다면 이 묶음은 필요가 없다. 그런데 6.2 시점에서는 RestTemplate, RestClient, WebClient 세 가지가 동시에 살아 있고, 어느 쪽을 골라야 하는지부터가 학습 비용의 상당 부분을 차지한다.

RestTemplate은 6.0 이후 maintenance mode에 들어갔다. 새 기능이 추가되지 않고, 새 프로젝트에서는 권장되지 않는다. 그렇다고 모든 호출을 비동기 Reactor 파이프라인으로 옮기는 것이 정답이냐 하면 그것도 아니다. 6.1에서 등장한 `RestClient`가 동기 호출의 자리를 차지하면서, WebClient는 "비동기·스트리밍·고동시성"에 집중하는 분업 구조가 만들어졌다.

본 묶음은 그 분업이 왜 그렇게 갈렸는지를 첫 챕터에서 정리한 다음, WebClient를 골랐을 때 마주치는 빌드·요청·응답·에러·필터·multipart·테스트의 7개 영역을 공식 문서 순서대로 따라간다. 마지막에는 TPS `ApprovalUrlAdapter`를 꺼내, 위 7개 영역이 한 클래스에서 어떻게 엮이는지 풀어 본다.



## 학습 순서

> 1장은 일상 호출에 필요한 기본기, 2장은 운영 코드에서 자주 만나는 변형이다. 11편을 순서대로 따라가면 면접 질문 8개에 답할 수 있는 수준이 목표다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [입문과 RestTemplate·RestClient 비교](01-01.WebClient%20입문과%20RestTemplate·RestClient%20비교.md) | 등장 동기, 세 클라이언트 결정 트리, 6.0/6.1/6.2의 변화 |
| 01-02 | [빌드와 인프라 설정](01-02.WebClient%20빌드와%20인프라%20설정.md) | `Builder`, `ExchangeStrategies`, codec 한도, ConnectionProvider, HttpClient 타임아웃 |
| 01-03 | [요청 빌딩 (URI·헤더·본문)](01-03.요청%20빌딩%20(URI·헤더·본문).md) | `uri()` 두 형태, `headers(Consumer)`, `bodyValue` vs `body(BodyInserters)` |
| 01-04 | [응답 처리](01-04.응답%20처리%20(retrieve와%20exchangeToMono).md) | `retrieve` vs `exchangeToMono` 결정 트리, `bodyToMono`/`bodyToFlux`, `toEntity` |
| 01-05 | [에러 처리와 재시도](01-05.에러%20처리와%20재시도.md) | `onStatus`, `WebClientResponseException`, Reactor `Retry.backoff`, 멱등성 |
| 01-06 | [ExchangeFilterFunction](01-06.ExchangeFilterFunction.md) | 필터 인터페이스, 로깅·인증·MDC, OAuth2 통합 개요 |
| 02-01 | [Multipart와 파일 업·다운로드](02-01.Multipart와%20파일%20업·다운로드.md) | `MultipartBodyBuilder`, `ByteArrayResource` 익명 override, 다운로드 트레이드오프 |
| 02-02 | [동기·비동기 결정](02-02.동기·비동기%20결정%20(block%20안티패턴).md) | `.block()` 허용/금지 영역, RestClient 대체 시점, MVC 통합 |
| 02-03 | [테스트](02-03.테스트%20(MockWebServer와%20WebTestClient).md) | OkHttp `MockWebServer`, `WebTestClient.bindToServer`, 필터 단위 테스트 |
| 02-04 | [TPS ApprovalUrlAdapter 사례 분석](02-04.실무%20사례%20-%20TPS%20ApprovalUrlAdapter.md) | Hexagonal port, 호출 시점 codecs, 동적 메타 호출, multipart 평탄화, `.block()`, 예외 wrap |

처음 보는 학습자는 01-01부터 순서대로 따라간다. RestTemplate에서 옮겨 오는 입장이라면 01-01과 01-04(응답 처리)부터 보고 02-02(동기 결정)에서 본인 코드와 비교하는 흐름이 빠르다. multipart 업로드만 급하다면 02-01과 02-04로 직행해도 된다.



## 환경과 버전

> 모든 코드 예제는 다음 조합에서 검증한다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | 3.3.0 (2024-05) 이후 LTS 라인 |
| Spring Framework | 6.2.x | RestClient 정식 도입(6.1) + JdkClientHttpConnector 안정화 |
| Java | 17+ | 21까지 호환 |
| Reactor Netty | 1.1.x | `HttpClient`, `ConnectionProvider`, `EventLoopGroup` |
| Reactor Core | 3.6.x | `Mono`, `Flux`, `Retry.backoff` |
| Jakarta | jakarta.* | `javax` 네임스페이스 미사용 |

3.3 이전 환경에서도 본문 코드 대부분이 동작한다. 차이가 큰 부분(예: `JdkClientHttpConnector`, 일부 `ExchangeFilterFunction` 헬퍼)은 챕터 본문에 ⚠️ 박스로 별도 표기한다.



## 사전 지식

> 이 묶음은 다음을 안다고 가정한다.

1. Reactive Streams의 네 인터페이스(`Publisher`/`Subscriber`/`Subscription`/`Processor`)가 무엇을 하는지 한 문장으로 설명할 수 있다.
2. `Mono`와 `Flux`의 차이를 구독 횟수와 방출 개수 기준으로 말할 수 있다.
3. Spring Boot 프로젝트에 `spring-boot-starter-webflux` 의존성을 추가할 수 있다.
4. Lambda와 메서드 참조(`String::isEmpty` 같은) 표기를 읽을 수 있다.

위 항목 중 막히는 부분이 있다면 [`spring/`](../README.md) 직접 하위와 Reactor 공식 가이드를 먼저 보고 돌아오는 편이 빠르다. WebFlux 핸들러·라우팅 등 서버 측 영역은 본 묶음에서 다루지 않는다(별도 묶음 예정).



## 면접 대비 체크리스트

> 11편을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 한다.

1. 6.2 시점에서 RestTemplate·RestClient·WebClient 중 어느 것을 어떤 기준으로 고르는가? `RestClient`가 등장한 이후 WebClient의 역할은 어떻게 좁혀졌는가?
2. `WebClient.Builder`만 빈으로 받고 호출 시점에 `build()`하는 패턴은 빈으로 완성된 `WebClient`를 받는 것과 비교해 어떤 트레이드오프를 가지는가?
3. `retrieve()`와 `exchangeToMono()`는 언제 갈리는가? `exchange`를 직접 쓸 때 책임지는 것은 무엇인가?
4. `onStatus`와 `onErrorResume`은 어떤 계층에서 동작하는가? `WebClientResponseException`이 뜨면 어디서 잡는 것이 깔끔한가?
5. `ExchangeFilterFunction.ofRequestProcessor`로 본문 로깅을 추가할 때 흔히 빠지는 함정은 무엇인가?
6. multipart 업로드에서 `ByteArrayResource`를 익명 클래스로 감싸 `getFilename()`을 override하는 이유는 무엇인가?
7. `.block()`이 허용되는 영역과 금지되는 영역을 구분할 수 있는가? Reactor thread에서 `.block()`을 호출하면 어떤 일이 일어나는가?
8. `Retry.backoff(maxAttempts, minBackoff)`에 `.transientErrors(true)`를 붙이는 의미는 무엇인가? POST 호출에 재시도를 거는 것이 안전한가?

각 질문에 막히면 표 우측의 챕터를 다시 본다.



## TPS 인용 매핑

> 02-* 챕터들은 TPS `operator` 모듈(commit `b8de25e7`)의 어댑터 코드를 발췌한다. 어느 챕터가 어느 라인을 인용하는지 미리 정리한다.

| 챕터 | 인용 위치 | 패턴 |
|------|----------|------|
| 01-02 | `ApprovalUrlAdapter.java:72-73` | `WebClient.Builder` + `codecs(maxInMemorySize)` 호출 시점 빌드 |
| 01-03 | `ApprovalUrlAdapter.java:102-108` | 동적 `method(httpMethod)` + `headers(Consumer)` + `uri(...)` |
| 01-04 | `ApprovalUrlAdapter.java:175` | `.retrieve().bodyToMono(TpsResponse.class).block()` |
| 01-05 | `ApprovalUrlAdapter.java:177-190` + `ApprovalUrlInvocationException` | 응답코드 검증 후 도메인 예외 wrap |
| 01-06 | `ApprovalUrlAdapter.java:170-173` | 필터 미사용, 호출부 직접 로깅의 한계 |
| 02-01 | `ApprovalUrlAdapter.java:113-158` | `MultipartBodyBuilder` + `ByteArrayResource` 익명 + `flattenAndAppend` |
| 02-02 | `ApprovalUrlAdapter.java:75-176` | `for` 루프 + `.block()` 순차 실행, RestClient 후보 분석 |
| 02-04 | 어댑터 전체 + `ApprovalUrlPort` + `ApprovalUrlInvocationException` | 6요소 종합 풀이 |

원본 파일 경로: `tps-gitlab2/operator/ticket/src/main/java/org/okestro/tps/operator/ticket/approval/`



## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [QueryDSL 학습 MOC](../../05_data/querydsl/README.md) — 같은 묶음 형태(12편)의 톤·구조 모델
- [Spring Framework Reference — WebClient](https://docs.spring.io/spring-framework/reference/web-reactive/webclient.html) — 본 묶음이 따라가는 공식 문서 진입점
- [Reactor Netty Reference](https://projectreactor.io/docs/netty/release/reference/) — `HttpClient`/`ConnectionProvider` 튜닝 근거
