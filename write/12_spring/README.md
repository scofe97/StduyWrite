---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - ../README.md
  - ../03_architecture/README.md
  - ../05_messaging/spring/README.md
  - ../06_data/README.md
updated: 2026-05-19
---

# Spring 학습 통합 MOC
---
> Spring 문서는 주제별로 분산 배치된다. 이 페이지가 전 카테고리 집계점이 되어 Spring 공부자의 진입점 역할을 한다.

## 왜 분산 배치인가

`_meta/conventions.md`의 카테고리 결정 원칙은 "주제 중심"이다. Spring Kafka 문서를 `05_messaging/`이 아닌 `12_spring/` 전용 폴더에 두면, "Kafka로 메시징을 구현하는 방법 비교"라는 주제 축이 깨진다. 따라서 도메인 결합도가 큰 Spring 문서(`@KafkaListener`, QueryDSL, Filter Chain 등)는 해당 주제 카테고리에 그대로 두고, 본 페이지가 논리층에서 모든 Spring 문서를 엮는다.

본 폴더(`write/12_spring/`)는 정식 카테고리(번호 12)로 등재되어 Spring 본질 이론 — 프레임워크의 자체 동작을 다루는 — 만 모은다.

## 카테고리별 배치

### 여기 (`12_spring/`) — Spring 본질 이론

| 폴더 | 범위 |
|------|------|
| [04_webflux/](04_webflux/) | Reactive, WebClient, Mono/Flux (2026-05-09 WebClient 11편 묶음 추가) |
| [05_testing/](05_testing/) | JUnit5/Mockito/MockMvc/@SpringBootTest/Testcontainers/EmbeddedKafka/ArchUnit/WireMock (2026-05-09 9편 묶음 추가) |

> 입문(Core/Boot/MVC)·내부 동작(Internals) 영역은 아직 본 폴더에 정식 문서로 없다. 신규 작성 시 위 표에 행을 추가한다.

### 도메인별 통합 (다른 카테고리)

| 주제 | 경로 | 다루는 내용 |
|------|------|------------|
| 설계 철학 | [`03_architecture/`](../03_architecture/README.md) "10. 후속 주제" | IoC를 설계 패턴 관점으로, AOP의 Decorator 해석 (예정) |
| 메시징 | [`05_messaging/spring/`](../05_messaging/spring/) | `@KafkaListener`, Producer Config, Error Handler |
| 영속성 | [`06_data/`](../06_data/) | [QueryDSL 6.12 학습 묶음](../06_data/querydsl/README.md) (Spring Data JPA, R2DBC, `@Transactional` 예정) |

## 전체 Spring 문서 목록 집계

태그 기반으로 전 카테고리에서 Spring 문서를 집계한다.

```bash
grep -rl "^  - spring$\|tags:.*spring" write/ --include="*.md" | sort
```

결과는 월간 리뷰에서 이 MOC 하단에 스냅샷으로 기록한다.

## 학습 경로 추천

본 폴더의 두 묶음은 **이미 Spring을 한 번 써본 사람**을 대상으로 한다.

1. **`04_webflux/`** — WebClient·Reactive. RestTemplate 경험이 있다면 1-1부터 진입.
2. **`05_testing/`** — 단위·통합·E2E 전 범위. Spring Boot 3.x 기준.
3. **도메인별** — 본인 관심 영역. 메시징이면 [`05_messaging/spring/`](../05_messaging/spring/), 데이터·ORM 이면 [`06_data/querydsl/`](../06_data/querydsl/).

Spring 입문(IoC/DI, Boot auto-config, MVC 기초)은 외부 공식 가이드 또는 [`03_architecture/`](../03_architecture/) 의 설계 관점 문서를 먼저 참조한다.

## 이관 진척

`poc/10_Spring/` → 여기로의 이관은 청크 단위로 진행한다. 진척 상태는 `STUDY_INDEX.md` 하단의 이관 표에서 확인한다.
