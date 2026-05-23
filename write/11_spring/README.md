---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - ../README.md
  - ../03_architecture/README.md
  - ../04_messaging/spring/README.md
  - ../05_data/README.md
updated: 2026-05-23
---

# Spring 학습 통합 MOC
---
> Spring 문서는 주제별로 분산 배치된다. 이 페이지가 전 카테고리 집계점이 되어 Spring 공부자의 진입점 역할을 한다.

## 왜 분산 배치인가

`_meta/conventions.md`의 카테고리 결정 원칙은 "주제 중심"이다. Spring Kafka 문서를 `04_messaging/`이 아닌 `11_spring/` 전용 폴더에 두면, "Kafka로 메시징을 구현하는 방법 비교"라는 주제 축이 깨진다. 따라서 도메인 결합도가 큰 Spring 문서(`@KafkaListener`, QueryDSL, Filter Chain 등)는 해당 주제 카테고리에 그대로 두고, 본 페이지가 논리층에서 모든 Spring 문서를 엮는다.

본 폴더(`write/11_spring/`)는 정식 카테고리(번호 12)로 등재되어 Spring 본질 이론 — 프레임워크의 자체 동작을 다루는 — 만 모은다.

## 카테고리별 배치

### 여기 (`11_spring/`) — Spring 본질 이론

| 폴더 | 범위 |
|------|------|
| [01_container/](01_container/) | IoC/DI, BeanFactory/ApplicationContext, 빈 등록·주입·생명주기·스코프 (2026-05-23 1편 추가) |
| [02_servlet/](02_servlet/) | WAS·Servlet·멀티 스레드·쿠키/세션·WAR/내장톰캣 부록 (2026-05-23 1편 추가) |
| [03_mvc/](03_mvc/) | MVC 패턴·FrontController V1~V5·DispatcherServlet·PRG·WebMvcConfigurer/CORS 부록 (2026-05-23 1편 추가) |
| [04_data-binding/](04_data-binding/) | HTTP 요청·응답·메시지 컨버터·Jackson·파일 업로드·Validation (2026-05-23 3편 묶음 추가) |
| [04_webflux/](04_webflux/) | Reactive, WebClient, Mono/Flux (2026-05-09 WebClient 11편 묶음 추가) |
| [05_testing/](05_testing/) | JUnit5/Mockito/MockMvc/@SpringBootTest/Testcontainers/EmbeddedKafka/ArchUnit/WireMock (2026-05-09 9편 묶음 추가) |
| [06_aop/](06_aop/) | 횡단 관심사·필터/인터셉터·JDK 동적 프록시·프록시 팩토리·빈 후처리기·@Aspect (2026-05-23 1편) · 스프링 스케줄링/Quartz (2026-05-23 1편 추가) |
| [08_exception-handling/](08_exception-handling/) | 서블릿 예외·BasicErrorController·HandlerExceptionResolver·@ControllerAdvice (2026-05-23 1편 추가) |

> Boot 자체(auto-config/Actuator/Properties) 영역은 아직 본 폴더에 정식 문서로 없다. 노션 import raw 는 [`_notion_import/`](_notion_import/) 에 있으며, 재작성이 끝난 묶음부터 위 표에 행을 추가한다.

### 도메인별 통합 (다른 카테고리)

| 주제 | 경로 | 다루는 내용 |
|------|------|------------|
| 설계 철학 | [`03_architecture/`](../03_architecture/README.md) "10. 후속 주제" | IoC를 설계 패턴 관점으로, AOP의 Decorator 해석 (예정) |
| 메시징 | [`04_messaging/spring/`](../04_messaging/spring/) | `@KafkaListener`, Producer Config, Error Handler |
| 영속성 | [`05_data/`](../05_data/) | [QueryDSL 6.12 학습 묶음](../05_data/querydsl/README.md) (Spring Data JPA, R2DBC, `@Transactional` 예정) |

## 전체 Spring 문서 목록 집계

태그 기반으로 전 카테고리에서 Spring 문서를 집계한다.

```bash
grep -rl "^  - spring$\|tags:.*spring" write/ --include="*.md" | sort
```

결과는 월간 리뷰에서 이 MOC 하단에 스냅샷으로 기록한다.

## 학습 경로 추천

대상자에 따라 진입점이 다르다.

1. **`01_container/`** — Spring 입문자. IoC/DI 가 무엇인지부터 빈 생명주기·스코프 충돌 해결까지 한 편으로 묶여 있다.
2. **`02_servlet/` → `03_mvc/` → `04_data-binding/`** — 웹 계층 토대 3단. WAS·서블릿 → FrontController·DispatcherServlet → HTTP 요청·응답·바인딩·Validation 순.
3. **`06_aop/`** — 프록시·AOP·스케줄링. 인터셉터·필터로 풀리지 않는 횡단 관심사와 `@Scheduled`·Quartz.
4. **`08_exception-handling/`** — MVC 위에서 예외 처리 전 흐름 (서블릿 → BasicErrorController → HandlerExceptionResolver → @ControllerAdvice).
5. **`04_webflux/`** — WebClient·Reactive. RestTemplate 경험이 있다면 01-01 부터 진입.
6. **`05_testing/`** — 단위·통합·E2E 전 범위. Spring Boot 3.x 기준.
7. **도메인별** — 본인 관심 영역. 메시징이면 [`04_messaging/spring/`](../04_messaging/spring/), 데이터·ORM 이면 [`05_data/querydsl/`](../05_data/querydsl/), 보안이면 [`10_security/`](../10_security/).

## 이관 진척

`poc/10_Spring/` → 여기로의 이관은 청크 단위로 진행한다. 진척 상태는 `STUDY_INDEX.md` 하단의 이관 표에서 확인한다.
