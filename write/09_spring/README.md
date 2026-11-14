---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - spring-keywords.md
  - ../README.md
  - ../03_architecture/README.md
  - ../04_messaging/README.md
  - ../05_data/README.md
updated: 2026-11-14
---

# Spring 학습 통합 MOC

> Spring 본질 이론과 프레임워크 자체 동작을 다루며, 전 카테고리 Spring 문서의 집계점 역할을 합니다.



## 경계 기준

이 저장소의 카테고리 결정 원칙은 "주제 중심"입니다. Spring Kafka 문서를 `04_messaging/`이 아닌 `09_spring/` 전용 폴더에 두면, "Kafka로 메시징을 구현하는 방법 비교"라는 주제 축이 깨집니다. 따라서 도메인 결합도가 큰 Spring 문서(`@KafkaListener`, QueryDSL, Filter Chain 등)는 해당 주제 카테고리에 그대로 두고, 본 페이지가 논리층에서 모든 Spring 문서를 엮습니다.

본 폴더(`write/09_spring/`)는 프레임워크의 자체 동작을 다루는 Spring 본질 이론만 모읍니다.

도메인별 통합 대상 카테고리 경계는 다음과 같습니다.

| 주제 | 경로 | 다루는 내용 |
|------|------|------------|
| 설계 철학 | [`03_architecture/`](../03_architecture/README.md) "10. 후속 주제" | IoC를 설계 패턴 관점으로, AOP의 Decorator 해석 (예정) |
| 메시징 | [`04_messaging/`](../04_messaging/) | `@KafkaListener`, Producer Config, Error Handler (스프링 부분은 04_BrokerArchitecture·05_ConsistencyPattern 등 주제별로 흡수) |
| 영속성 | [`05_data/`](../05_data/) | [QueryDSL 6.12 학습 묶음](../05_data/03_persistence/querydsl/README.md) (Spring Data JPA, R2DBC, `@Transactional` 예정) |

- Boot 자체는 [`07_autoconfig/`](07_autoconfig/), 내장 톰캣은 [`01_core/02-02`](01_core/), 액츄에이터·메트릭은 `06_observability/05_SpringActuator/`에 정식 문서로 작성되었습니다.
- 트랜잭션 본체는 [`05_data/03_persistence/jpa/04-01`](../05_data/03_persistence/jpa/04-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md)에 두고, 검증은 [`02_data-binding/`](02_data-binding/)에서 다룹니다.
- 도메인 결합도가 큰 주제는 기존 위치 그대로 두고, Spring 본질 영역에 신설할 후보만 여기에 둡니다.
- 현재 검토 중인 신설 후보는 없습니다. 신설 시점은 최소 5편 확보 시 신설, 미만이면 기존 카테고리 하위에서 시작한다는 기준을 따릅니다.



## 키워드

### spring-keywords.md

키워드 파일: [spring-keywords.md](spring-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 컨테이너와 빈 | 7편 | — |
| 2단계 · 프록시와 AOP | 4편 | — |
| 3단계 · 요청 처리 | 11편 | — |
| 4단계 · 트랜잭션과 이벤트 | 4편 | — |
| 5단계 · 부트가 조립하는 세계 | 8편 | — |
| 6단계 · 외부 통신과 회복탄력성 | 11편 | — |
| 7단계 · 비동기와 실시간 | 8편 | — |
| 8단계 · 보안과 운영 | 0편 | 필터 체인이 먼저다 · 인증과 사용자 · 비밀번호 · 엔드포인트 인가 · 액츄에이터 엔드포인트 · Micrometer 와 메트릭 |
| 9단계 · 테스트와 배포 | 10편 | — |



## 하위 폴더·문서 목록

| 폴더 | 편수 | 범위 |
|------|------|------|
| [01_core/](01_core/) | 8편 | Spring 코어 3종 통합 — 컨테이너(IoC/DI·빈 등록·주입·생명주기·스코프·디자인 패턴, 01장)·서블릿(WAS·멀티스레드·쿠키/세션·내장톰캣, 02장)·MVC(FrontController V1~V5·DispatcherServlet·예외 처리·WebFlux, 03~04장) |
| [02_data-binding/](02_data-binding/) | 5편 | HTTP 요청·응답·메시지 컨버터·Jackson·파일 업로드·Validation·메시지 국제화 |
| [03_network/](03_network/) | 37편 | 외부·실시간 통신 다섯 갈래 — WebClient(`webflux/` 10편)·OpenFeign(`feign/` 5편)·Reactor Netty 전송 엔진(`reactive-net/` 7편)·SSE/WebSocket/STOMP 실시간(`realtime/` 10편)·회복탄력성(`resilience/` 5편) |
| [04_testing/](04_testing/) | 9편 | JUnit5/Mockito/MockMvc/@SpringBootTest/Testcontainers/EmbeddedKafka/ArchUnit/WireMock |
| [05_aop/](05_aop/) | 4편 | 횡단 관심사·필터/인터셉터·JDK 동적 프록시·프록시 팩토리·빈 후처리기·@Aspect · 템플릿·콜백·ThreadLocal — AOP 등장 직전 · 스프링 스케줄링/Quartz · @Async·@Cacheable·@Retryable |
| [06_events/](06_events/) | 4편 | 스프링 이벤트 — @EventListener vs @TransactionalEventListener·트랜잭션 Phase·전파 조합·내부 동작·동기/비동기(@Async) |
| [07_autoconfig/](07_autoconfig/) | 7편 | 스프링 부트 자동 구성·외부 설정 — 스타터/BOM·@AutoConfiguration·@Conditional·커스텀 스타터·외부 설정·@ConfigurationProperties·프로필 |



## 학습 경로 추천

대상자에 따라 진입점이 다릅니다.

1. **`01_core/`**: Spring 입문자를 위한 출발점입니다. 컨테이너(IoC/DI·빈 생명주기·스코프, 01장) → 서블릿(WAS·멀티스레드·내장톰캣, 02장) → MVC(FrontController·DispatcherServlet·예외 처리, 03장)를 의존 순서대로 묶었습니다. 요청 한 건이 톰캣에서 컨트롤러까지 도달하는 척추를 한 흐름으로 봅니다.
2. **`02_data-binding/`**: `01_core/` MVC 다음 단계입니다. DispatcherServlet이 받은 요청 본문을 객체로 바인딩하고 응답을 직렬화하는 과정을 다룹니다. 메시지 컨버터, 파일 업로드, Validation, 국제화를 포함합니다.
3. **`07_autoconfig/`**: 스프링 부트의 자체 동작을 다룹니다. 라이브러리만 넣으면 빈이 생기는 자동 구성과 환경마다 다른 설정을 만드는 외부 설정·프로필을 설명합니다. `01_core/`가 빈을 직접 등록하는 세계라면 여기는 부트가 자동 등록하는 세계입니다.
4. **`05_aop/`**: 프록시와 AOP 및 스케줄링을 다룹니다. 인터셉터나 필터로 풀리지 않는 횡단 관심사와 `@Scheduled`·Quartz를 설명합니다. `01_core/` 01장의 CGLIB 프록시가 출발점입니다.
5. **`06_events/`**: 스프링 이벤트를 다룹니다. `@TransactionalEventListener`의 Phase와 전파 조합 및 내부 동작을 다룹니다. 트랜잭션 경계와 외부 연동 분리를 다룹니다.
6. **`03_network/`**: 외부 통신과 실시간 통신을 다룹니다. 클라이언트 두 갈래(`webflux/` WebClient, `feign/` OpenFeign)와 전송 엔진(`reactive-net/`), 실시간 통신(`realtime/` SSE·WebSocket·STOMP), 회복탄력성(`resilience/`)을 포함합니다. RestTemplate 경험자는 `webflux/01-01`부터, 신규 MSA 설계자는 `feign/01-01`부터 진입합니다.
7. **`04_testing/`**: 단위 테스트부터 통합·E2E 테스트까지 전 범위를 다룹니다. Spring Boot 3.x 기준입니다.
8. **운영·모니터링**: `06_observability/05_SpringActuator/` 액츄에이터, 마이크로미터, 프로메테우스로 스프링 앱 메트릭을 노출하고 시각화합니다.
9. **도메인별**: 특정 도메인은 해당 카테고리로 진입합니다. 메시징은 [`04_messaging/`](../04_messaging/), 데이터와 ORM은 [`05_data/03_persistence/querydsl/`](../05_data/03_persistence/querydsl/)입니다.



## Spring 딥다이브 전체 지도

위의 "하위 폴더·문서 목록"이 어떤 폴더에 무엇이 있는지를, "학습 경로 추천"이 어떤 순서로 읽는지를 답한다면, 이 절은 Spring 본질을 어디까지 깊게 파야 하는가를 답합니다. 읽는 순서는 [Spring 학습 로드맵](spring-keywords.md)이 정합니다. 컨테이너, 프록시, 요청 처리, 트랜잭션을 지나 부트, 통신, 보안, 운영, 테스트까지 9단계입니다. 각 단계와 짝을 맞춰 보유 문서와 미작성 갭을 연결한 네비게이션입니다.

Spring Container가 Bean을 만들고 Proxy가 부가 기능을 감쌉니다. DispatcherServlet이 요청을 흘려보내고 TransactionManager가 DB 경계를 관리합니다. Boot AutoConfiguration이 설정을 조립하며 Actuator와 Test가 운영성과 검증 가능성을 엽니다.

| 단계 | 대주제 | 진입 문서 | 갭(미작성) |
|------|--------|----------|-----------|
| 1 | Core / IoC / Bean 생명주기 (대주제 1~5) | [01_core/01-01](01_core/01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) · [01-02](01_core/01-02.Spring과%20디자인%20패턴.md) | BeanPostProcessor 내부 흐름, 순환 참조 전용편 |
| 2 | AOP / Proxy / Weaving (대주제 6) | [05_aop/01-01](05_aop/01-01.횡단%20관심사와%20AOP%20—%20프록시로%20풀어내기.md) · [01-03](05_aop/01-03.템플릿·콜백과%20ThreadLocal%20—%20AOP%20등장%20직전의%20두%20시도.md) · [01-04](05_aop/01-04.어노테이션%20기반%20AOP%20응용%20—%20@Async·@Cacheable·@Retryable.md) | Weaving 4종 + Spring AOP vs AspectJ + `@EnableLoadTimeWeaving` 실험 전용편 |
| 3 | @Transactional (대주제 7) | 본체 [../05_data/03_persistence/jpa/04-01](../05_data/03_persistence/jpa/04-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md) · [04-01b](../05_data/03_persistence/jpa/04-01b.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EC%A0%84%ED%8C%8C%20%ED%99%9C%EC%9A%A9.md), [06_events/01-02](06_events/01-02.트랜잭션%20전파%20조합%20—%20죽은%20트랜잭션과%20REQUIRES_NEW.md) | MyBatis ↔ Spring 트랜잭션 Connection 바인딩 전용편 |
| 4 | Spring MVC / 요청 처리 (대주제 8~10) | [01_core/03-01](01_core/03-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) · [03-02](01_core/03-02.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md), [02_data-binding/01-01](02_data-binding/01-01.HTTP%20요청·응답과%20메시지%20컨버터.md), [01_core/04-01](01_core/04-01.WebFlux%20서버%20—%20리액티브%20스택과%20어노테이션%20모델.md) · [04-02](01_core/04-02.WebFlux%20함수형%20엔드포인트%20—%20RouterFunction과%20HandlerFunction.md) | Custom ArgumentResolver / ReturnValueHandler 실습편 |
| 5 | Validation / Binding / Conversion (대주제 11) | [02_data-binding/](02_data-binding/) | Converter / Formatter / ConversionService 전용편 |
| 6 | Spring Boot 자동구성·외부설정 (대주제 12~14) | [07_autoconfig/](07_autoconfig/) | 7편으로 충분 — 신규 후보 없음 |
| 7 | 운영·연동·테스트 (대주제 15~24) | Event [06_events/](06_events/), Async/Scheduling [05_aop/01-02](05_aop/01-02.스프링%20스케줄링%20—%20@Scheduled에서%20Quartz까지.md)·01-04, Test [04_testing/](04_testing/), Data [../05_data/](../05_data/) | Cache Abstraction 전용편, MyBatis 연동 전용편, 성능 튜닝·장애 분석편 |
| 8 | 빌드·패키징·Tomcat 배포 ([로드맵 9단계](spring-keywords.md)) | [01_core/02-02](01_core/02-02.내장%20톰캣과%20SpringApplication%20—%20JAR로%20WAS를%20품다.md) | bootJar vs plain jar·Boot Loader(JarLauncher/WarLauncher)·외부 WAR(SpringBootServletInitializer·providedRuntime)·Layered JAR·Docker layer cache·CI/CD 산출물 관리 전용편 |

단계별 개념 표와 우선순위, 책의 읽을 장은 [로드맵](spring-keywords.md)이 정본입니다. 미작성 갭은 위 표의 "갭" 열에 모았습니다. 코어 영역은 BeanPostProcessor와 순환 참조 전용편, AOP는 Weaving 4종과 AspectJ 실험편을 다룹니다. 데이터와 웹은 MyBatis Connection 바인딩, Custom ArgumentResolver, Converter/ConversionService 편이 후보입니다. 운영과 배포는 Cache Abstraction, 성능 튜닝, Tomcat 배포 전용편을 보강 대상으로 둡니다.
