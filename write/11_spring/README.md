---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - ../README.md
  - ../03_architecture/README.md
  - ../04_messaging/README.md
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
| [01_core/](01_core/) | Spring 코어 3종 통합 — 컨테이너(IoC/DI·빈 등록·주입·생명주기·스코프·디자인 패턴, 01장)·서블릿(WAS·멀티스레드·쿠키/세션·내장톰캣, 02장)·MVC(FrontController V1~V5·DispatcherServlet·예외 처리, 03장) (2026-05-24 01_container/02_servlet/03_mvc 통합) |
| [02_data-binding/](02_data-binding/) | HTTP 요청·응답·메시지 컨버터·Jackson·파일 업로드·Validation·메시지 국제화 (2026-05-23 4편 묶음) |
| [03_network/](03_network/) | 외부 HTTP 호출 두 갈래 — WebClient(리액티브) 11편 + OpenFeign(선언형) 2편 (2026-05-27 03_webflux → 03_network 재편) |
| [04_testing/](04_testing/) | JUnit5/Mockito/MockMvc/@SpringBootTest/Testcontainers/EmbeddedKafka/ArchUnit/WireMock (2026-05-09 9편 묶음 추가) |
| [05_aop/](05_aop/) | 횡단 관심사·필터/인터셉터·JDK 동적 프록시·프록시 팩토리·빈 후처리기·@Aspect · 템플릿·콜백·ThreadLocal — AOP 등장 직전 · 스프링 스케줄링/Quartz (2026-05-23 3편) |
| [06_events/](06_events/) | 스프링 이벤트 — @EventListener vs @TransactionalEventListener·트랜잭션 Phase·전파 조합·내부 동작·동기/비동기(@Async) (2026-05-24 이벤트 리스너 4편 묶음) |
| [07_autoconfig/](07_autoconfig/) | 스프링 부트 자동 구성·외부 설정 — 스타터/BOM·@AutoConfiguration·@Conditional·커스텀 스타터·외부 설정·@ConfigurationProperties·프로필 (2026-05-25 boot zip 6편 묶음) |

> Boot 자체(auto-config/Properties/Profile)는 [`07_autoconfig/`](07_autoconfig/), 내장 톰캣은 [`01_core/02-02`](01_core/), 액츄에이터·메트릭은 [`06_observability/05_SpringActuator/`](../06_observability/05_SpringActuator/) 에 정식 문서로 작성됐다(2026-05-25, 김영한 스프링 부트 강의 기반). 노션 import raw 는 [`_notion_import/`](_notion_import/) 에 있으며, 재작성이 끝난 묶음부터 위 표에 행을 추가한다.

### 예정 카테고리

다음 묶음을 후속으로 검토 중이다. 도메인 결합도가 큰 주제(메시징·영속성)는 기존 위치 그대로 두고, 아래 두 주제만 Spring 본질 영역에 신설 후보다.

1. **08_transaction** — `@Transactional` 의 전파(Propagation)·격리(Isolation)·readOnly·롤백 규칙·AOP 프록시 함정. 현재 `06_events/` 의 `@TransactionalEventListener` 가 트랜잭션 Phase 만 다루고 있어, 본 묶음이 빠지면 트랜잭션 본체가 비어 있는 상태다.
2. **08_validation 독립화** — 현재 `02_data-binding/` 에 묶여 있는 Bean Validation 분리. 바인딩(요청 본문 → 객체 변환)과 검증(제약 조건 검사)은 DispatcherServlet 파이프라인에서 다른 단계이고, Custom Constraint / Group Validation / `@Validated` vs `@Valid` 만 해도 6~8편 분량이 나온다.

신설 시점은 second-brain-harness §4.4 — 최소 5편 확보 시 신설, 미만이면 기존 카테고리 하위에서 시작 — 을 따른다.

### 도메인별 통합 (다른 카테고리)

| 주제 | 경로 | 다루는 내용 |
|------|------|------------|
| 설계 철학 | [`03_architecture/`](../03_architecture/README.md) "10. 후속 주제" | IoC를 설계 패턴 관점으로, AOP의 Decorator 해석 (예정) |
| 메시징 | [`04_messaging/`](../04_messaging/) | `@KafkaListener`, Producer Config, Error Handler (스프링 부분은 04_BrokerArchitecture·05_ConsistencyPattern 등 주제별로 흡수) |
| 영속성 | [`05_data/`](../05_data/) | [QueryDSL 6.12 학습 묶음](../05_data/querydsl/README.md) (Spring Data JPA, R2DBC, `@Transactional` 예정) |

## 전체 Spring 문서 목록 집계

태그 기반으로 전 카테고리에서 Spring 문서를 집계한다.

```bash
grep -rl "^  - spring$\|tags:.*spring" write/ --include="*.md" | sort
```

결과는 월간 리뷰에서 이 MOC 하단에 스냅샷으로 기록한다.

## 학습 경로 추천

대상자에 따라 진입점이 다르다.

1. **`01_core/`** — Spring 입문자. 컨테이너(IoC/DI·빈 생명주기·스코프, 01장) → 서블릿(WAS·멀티스레드·내장톰캣, 02장) → MVC(FrontController·DispatcherServlet·예외 처리, 03장)를 한 폴더에서 의존 순서대로 묶었다. 요청 한 건이 톰캣에서 컨트롤러까지 도달하는 척추를 한 흐름으로 본다.
2. **`02_data-binding/`** — `01_core/` MVC 다음 단계. DispatcherServlet 이 받은 요청 본문을 객체로 바인딩하고 응답을 직렬화하는 과정 — 메시지 컨버터·파일 업로드·Validation·국제화.
3. **`07_autoconfig/`** — 스프링 부트의 자체 동작. "라이브러리만 넣으면 빈이 생기는" 자동 구성과 "한 번 빌드, 환경마다 다른 설정"을 만드는 외부 설정·프로필. `01_core/` 가 빈을 직접 등록하는 세계라면 여기는 부트가 자동 등록하는 세계다.
4. **`05_aop/`** — 프록시·AOP·스케줄링. 인터셉터·필터로 풀리지 않는 횡단 관심사와 `@Scheduled`·Quartz. `01_core/` 01장의 CGLIB 프록시가 출발점.
5. **`06_events/`** — 스프링 이벤트. `@TransactionalEventListener` 의 Phase·전파 조합·내부 동작. 트랜잭션 경계와 외부 연동 분리를 다룬다.
6. **`03_network/`** — 외부 HTTP 호출. `webflux/` (WebClient 11편) 와 `feign/` (OpenFeign 2편 압축본) 두 갈래. RestTemplate 경험자는 `webflux/01-01` 부터, 신규 MSA 설계자는 `feign/01-01` 부터 진입.
7. **`04_testing/`** — 단위·통합·E2E 전 범위. Spring Boot 3.x 기준.
8. **운영·모니터링** — [`06_observability/05_SpringActuator/`](../06_observability/05_SpringActuator/) 액츄에이터·마이크로미터·프로메테우스로 스프링 앱 메트릭을 노출·시각화.
9. **도메인별** — 본인 관심 영역. 메시징이면 [`04_messaging/`](../04_messaging/), 데이터·ORM 이면 [`05_data/querydsl/`](../05_data/querydsl/), 보안이면 [`10_security/`](../10_security/).

## 이관 진척

`poc/10_Spring/` → 여기로의 이관은 청크 단위로 진행한다. 진척 상태는 `STUDY_INDEX.md` 하단의 이관 표에서 확인한다.
