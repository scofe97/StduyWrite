---
title: 11_spring/03_network/resilience — Resilience4j 회복탄력성 시리즈
tags: [moc, resilience4j, circuit-breaker, retry, bulkhead, rate-limiter, spring-boot]
status: draft
source:
  - https://resilience4j.readme.io/
  - https://github.com/resilience4j/resilience4j
related:
  - ../README.md
  - ../webflux/01-05.에러 처리와 재시도.md
  - ../../../04_messaging/05_ConsistencyPattern/05-05.Backoff 전략 비교와 선택.md
updated: 2026-05-28
---

# resilience — Resilience4j 회복탄력성 시리즈

---

> 외부 시스템 호출은 *언젠가는* 실패합니다. 네트워크 일시 단절, 외부 API 응답 지연, 다운스트림 장애. 이 *부분 실패* 가 *내 시스템 전체 장애* 로 전파되지 않게 차단하는 장치가 *회복탄력성 패턴* 입니다. Spring HTTP 호출 (RestClient · WebClient · OpenFeign) 에 *Resilience4j* 를 입혀 5가지 패턴 (Circuit Breaker · Retry · Bulkhead · Rate Limiter · Time Limiter) 을 적용하는 방법을 5편으로 정리합니다.

## 왜 별도 묶음인가

`webflux/01-05.에러 처리와 재시도.md` 가 *WebClient 의 retry 한 줄* 을 다룹니다. 그것만으로 *재시도 폭주*, *서킷이 열렸을 때의 분기*, *동시 호출 격리*, *속도 제한* 까지 답하지 못합니다. Spring 자체 retry 추상화는 *재시도* 만 다루고 *다른 회복탄력성 패턴* 은 별도 라이브러리가 답입니다.

Resilience4j 가 그 자리의 *de facto 표준* 입니다. Spring Cloud Circuit Breaker 의 디폴트 구현이며, Spring Boot 3.x 와 자동 구성이 표준화되어 있습니다. 본 묶음은 *5가지 모듈을 각자 한 편* 으로 풀어, 면접에서 *Half-Open 전이는 언제 발생하는가*, *Semaphore Bulkhead 와 ThreadPool Bulkhead 의 차이는 무엇인가*, *Retry 와 Circuit Breaker 의 데코레이터 순서가 왜 중요한가* 같은 질문에 답할 수 있는 수준까지 끌어올립니다.

## 학습 순서

1편 *개요* → 2~5편 *모듈별 깊이* 순서로 읽습니다. 1편이 끝나면 *5가지 모듈이 어디서 갈리고 어떻게 조합하는가* 의 골격이 잡힙니다. 2~5편은 *각 모듈 한 편씩* 입니다.

| # | 문서 | 다루는 핵심 질문 |
|---|------|----------------|
| 01-01 | Resilience4j 개요 — 5가지 모듈과 도입 결정 | 5가지 모듈이 각자 어떤 장애 형태에 답하는가, 조합 순서와 데코레이터 패턴 |
| 01-02 | Circuit Breaker 상세 — 상태 전이와 Sliding Window | CLOSED·OPEN·HALF_OPEN 전이, count-based vs time-based 윈도우, slow call 분리 |
| 01-03 | Retry — exponential backoff·jitter·재시도 폭주 방지 | 백오프 알고리즘, jitter 가 푸는 문제, retry × Circuit Breaker 조합 순서 |
| 01-04 | Bulkhead — Semaphore vs ThreadPool 격리 | 두 구현체의 자원 모델, 동기·비동기 적합성, 장애 전파 차단 모델 |
| 01-05 | Rate Limiter & Time Limiter — 트래픽 제어와 타임아웃 | token bucket 모델, 클라이언트 측 vs 서버 측 제한, TimeLimiter 의 thread 모델 |

## 경계 기준

본 폴더는 *Resilience4j 라이브러리 자체* 와 *Spring Boot 통합* 만 다룹니다. 다른 자리는 다음과 같이 갈립니다.

| 영역 | 다루는 것 | 위치 |
|------|---------|------|
| 본 폴더 (`resilience/`) | Resilience4j 5가지 모듈, Spring Boot 자동 구성, Annotation 통합 | 여기 |
| WebClient 에러·재시도 | `Mono.retryWhen` 의 retry backoff 한정 | [`../webflux/01-05.에러 처리와 재시도.md`](../webflux/01-05.에러%20처리와%20재시도.md) |
| Kafka Consumer Backoff | Spring Kafka `BackOff` 정책 (FixedBackOff·ExponentialBackOff) | [`../../../04_messaging/05_ConsistencyPattern/05-05.Backoff 전략 비교와 선택.md`](../../../04_messaging/05_ConsistencyPattern/05-05.Backoff%20전략%20비교와%20선택.md) |
| 메시징 측 Poison Message | DLT 흡수의 한계, 격리 큐 패턴 | [`06-01.Poison Message 처리`](../../../04_messaging/05_ConsistencyPattern/06-01.Poison%20Message%20처리%20—%20DLT%20흡수의%20한계와%20격리%20큐.md) |
| 메시징 측 Retry Storm | 백오프 jitter, 동시성 제한, 컨슈머 측 서킷 | [`06-02.Retry Storm 방지`](../../../04_messaging/05_ConsistencyPattern/06-02.Retry%20Storm%20방지%20—%20백오프%20jitter·동시성%20제한·서킷.md) |
| Istio 측 회복탄력성 | 인프라 레벨 retry·timeout·circuit-breaking | [`../../../08_cloud/service-mesh/11-03.Istio 레질리언스.md`](../../../08_cloud/service-mesh/11-03.Istio%20레질리언스.md) |

> Istio 와 Resilience4j 는 *같은 패턴을 다른 레이어* 에서 적용합니다. Istio 가 *인프라 계층* 에서, Resilience4j 가 *애플리케이션 계층* 에서. 둘은 보완 관계입니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.2.x ~ 3.4.x | resilience4j-spring-boot3 |
| Resilience4j | 2.2.x | functional 패턴, decorator API |
| Java | 17 / 21 | virtual thread 21+ 에서 Bulkhead 영향 있음 |

## 사전 지식

본 카테고리는 다음을 가정합니다.

1. WebClient 또는 RestClient 로 외부 HTTP 호출을 짜본 경험이 있습니다. 없으면 [`../webflux/01-01.WebClient 입문과 RestTemplate·RestClient 비교.md`](../webflux/01-01.WebClient%20입문과%20RestTemplate·RestClient%20비교.md) 가 시작점.
2. Spring Boot 자동 구성·`application.yml` 외부 설정의 동작을 압니다. 모르면 [`../../07_autoconfig/`](../../07_autoconfig/) 가 시작점.
3. `CompletableFuture` 의 비동기 모델을 한 줄로 답할 수 있습니다. Bulkhead·TimeLimiter 의 ThreadPool 모드 이해에 필요.
