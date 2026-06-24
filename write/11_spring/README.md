---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - ../README.md
  - ../03_architecture/README.md
  - ../04_messaging/README.md
  - ../05_data/README.md
updated: 2026-06-25
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
| [08_transaction/](08_transaction/) | 트랜잭션 집계 MOC — 본체는 [`05_data/jpa/04-01`](../05_data/jpa/04-01.스프링%20트랜잭션.md)에 두고, Spring 관점에서 비어 있던 격리 수준·@Transactional 테스트 2편만 보강 (2026-05-29 MOC+2편) |
| [09_validation/](09_validation/) | 입력 검증 — 수동 검증·BindingResult / Bean Validation·그룹 / 커스텀 ConstraintValidator. 옛 02_data-binding 의 단일 편을 분할·확장 (2026-05-29 MOC+3편) |

> Boot 자체(auto-config/Properties/Profile)는 [`07_autoconfig/`](07_autoconfig/), 내장 톰캣은 [`01_core/02-02`](01_core/), 액츄에이터·메트릭은 [`06_observability/05_SpringActuator/`](../06_observability/05_SpringActuator/) 에 정식 문서로 작성됐다(2026-05-25, 김영한 스프링 부트 강의 기반). 노션 import raw 는 [`_notion_import/`](_notion_import/) 에 있으며, 재작성이 끝난 묶음부터 위 표에 행을 추가한다.

### 예정 카테고리

도메인 결합도가 큰 주제(메시징·영속성)는 기존 위치 그대로 두고, Spring 본질 영역에 신설할 후보만 여기에 둔다. 현재 검토 중인 후보는 없다. 신설 시점은 second-brain-harness §4.4 — 최소 5편 확보 시 신설, 미만이면 기존 카테고리 하위에서 시작 — 을 따른다.

> 2026-05-29 — 검토하던 `08_transaction` 과 `09_validation` 을 신설 완료했다. 두 건 모두 당초 명분이 실제 자산과 어긋나 방향을 정정했다. ① `08_transaction`: 트랜잭션 본체(추상화·동기화·AOP·전파·락)는 이미 [`05_data/jpa/04-01`](../05_data/jpa/04-01.스프링%20트랜잭션.md)·`04-01b`·`04-02` 에 final 로 있어, 본체를 새로 쓰지 않고 집계 MOC + 격리 수준·테스트 2편만 보강했다. ② `09_validation`: "6~8편 분량" 이라 적었지만 실제로는 `02_data-binding/02-01` 단일 편(583줄)이 거의 전 범위를 다루고 있었다. 그래서 그 단일 편을 수동 검증·Bean Validation 두 편으로 분할해 옮기고, 목차에 없던 커스텀 `ConstraintValidator` 1편만 신규로 보강했다(분할 2 + 신규 1).

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



## Spring 딥다이브 전체 지도

위의 "카테고리별 배치"가 *어떤 폴더에 무엇이 있나*를, "학습 경로 추천"이 *어떤 순서로 읽나*를 답한다면, 이 절은 *Spring 본질을 어디까지 깊게 파야 하는가*를 답한다. Spring을 깊게 판다는 것은 어노테이션을 더 많이 외우는 일이 아니라, `@Autowired`가 왜 주입되는지·`@Transactional`이 왜 실패하는지·`@RequestBody`가 어디서 변환되는지·AutoConfiguration이 왜 켜지는지·테스트가 왜 느려지는지·운영에서 health가 왜 내려가는지를 설명할 수 있게 되는 일이다. 아래는 그 전체 범위를 24개 대주제로 펼친 뒤 7개 학습 단계로 묶고, 각 대주제의 핵심 키워드를 이미 쓴 문서·아직 안 쓴 갭과 연결한 지도다.

한 문장으로 줄이면 이렇다.

> Spring Container가 Bean을 만들고, Proxy가 부가기능을 감싸고, DispatcherServlet이 요청을 흘려보내고, TransactionManager가 DB 경계를 관리하고, Boot AutoConfiguration이 설정을 조립하며, Actuator와 Test가 운영성과 검증 가능성을 열어준다.

| 단계 | 대주제 | 보유 문서 | 갭(미작성) |
|------|--------|----------|-----------|
| 1 | Core / IoC / Bean 생명주기 (대주제 1~5) | [01_core/01-01](01_core/01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) · [01-02](01_core/01-02.Spring과%20디자인%20패턴.md) | BeanPostProcessor / BeanFactoryPostProcessor 내부 흐름, 순환 참조 전용편 |
| 2 | AOP / Proxy / Weaving (대주제 6) | [05_aop/01-01](05_aop/01-01.횡단%20관심사와%20AOP%20—%20프록시로%20풀어내기.md) · [01-03](05_aop/01-03.템플릿·콜백과%20ThreadLocal%20—%20AOP%20등장%20직전의%20두%20시도.md) · [01-04](05_aop/01-04.어노테이션%20기반%20AOP%20응용%20—%20@Async·@Cacheable·@Retryable.md) | **Weaving 4종(CTW·Post-compile·LTW·Runtime) + Spring AOP vs AspectJ + `@EnableLoadTimeWeaving` 실험** |
| 3 | @Transactional (대주제 7) | 본체 [../05_data/jpa/04-01](../05_data/jpa/04-01.스프링%20트랜잭션.md) · [04-01b](../05_data/jpa/04-01b.트랜잭션%20전파%20활용.md), [08_transaction/01-01](08_transaction/01-01.트랜잭션%20격리%20수준%20—%20Spring%20관점.md) · [01-02](08_transaction/01-02.@Transactional%20테스트%20가드.md), [06_events/01-02](06_events/01-02.트랜잭션%20전파%20조합%20—%20죽은%20트랜잭션과%20REQUIRES_NEW.md) | MyBatis ↔ Spring 트랜잭션 Connection 바인딩 전용편 |
| 4 | Spring MVC / 요청 처리 (대주제 8~10) | [01_core/03-01](01_core/03-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) · [03-02](01_core/03-02.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md), [02_data-binding/01-01](02_data-binding/01-01.HTTP%20요청·응답과%20메시지%20컨버터.md), [01_core/04-01](01_core/04-01.WebFlux%20서버%20—%20리액티브%20스택과%20어노테이션%20모델.md) · [04-02](01_core/04-02.WebFlux%20함수형%20엔드포인트%20—%20RouterFunction과%20HandlerFunction.md) | Custom ArgumentResolver / ReturnValueHandler 실습편 |
| 5 | Validation / Binding / Conversion (대주제 11) | [02_data-binding/](02_data-binding/) (5편), [09_validation/](09_validation/) (3편) | Converter / Formatter / ConversionService 전용편 |
| 6 | Spring Boot 자동구성·외부설정 (대주제 12~14) | [07_autoconfig/](07_autoconfig/) (7편) | (충분) |
| 7 | 운영·연동·테스트 (대주제 15~24) | Event [06_events/](06_events/) (4편), Async/Scheduling [05_aop/01-02](05_aop/01-02.스프링%20스케줄링%20—%20@Scheduled에서%20Quartz까지.md)·01-04, Test [04_testing/](04_testing/) (9편), Data [../05_data/](../05_data/), Security [../10_security/](../10_security/), Actuator [../06_observability/05_SpringActuator/](../06_observability/05_SpringActuator/) | **Cache Abstraction 전용편**(현재 @Cacheable 일부만), MyBatis 연동 전용편, 성능 튜닝·장애 분석편 |

각 대주제의 핵심 키워드는 다음과 같다. 학습 노트나 프롬프트에 그대로 넣어 진도 체크용으로 쓸 수 있다.

### 1단계 — Spring Core / IoC Container

- **1. Spring Core / IoC Container** — IoC · DI · Bean · BeanDefinition · BeanFactory · ApplicationContext · DefaultListableBeanFactory · Component Scan · @Configuration · @Bean · @Component · @Service · @Repository · @Controller · @Autowired · Constructor Injection · Qualifier · Primary · Lazy · Scope · Singleton · Prototype
- **2. Bean 등록과 생명주기** — Bean Lifecycle · Instantiation · Dependency Injection · Aware Interface · BeanNameAware · ApplicationContextAware · InitializingBean · DisposableBean · @PostConstruct · @PreDestroy · initMethod · destroyMethod · SmartInitializingSingleton · SmartLifecycle · ApplicationReadyEvent
- **3. 의존성 주입과 순환 참조** — 생성자 주입 · 필드 주입 · 순환 참조(circular reference) · @Lazy 우회
- **4. ApplicationContext와 BeanFactory** — ApplicationContext · BeanFactory · BeanDefinition 설계도 · 싱글톤 캐싱
- **5. BeanPostProcessor / BeanFactoryPostProcessor** — BeanPostProcessor · BeanFactoryPostProcessor · before/after initialization · FactoryBean

핵심 흐름: ClassPath Scan → BeanDefinition 생성 → BeanFactory 등록 → BeanFactoryPostProcessor 실행 → Bean 인스턴스 생성 → 의존성 주입 → BeanPostProcessor before → @PostConstruct·InitializingBean → BeanPostProcessor after → Singleton 캐싱. Spring은 객체를 곧바로 만들지 않고 먼저 **BeanDefinition이라는 설계도**를 만든 뒤 그 설계도로 조립한다.

### 2단계 — AOP / Proxy / Weaving

- **6. AOP와 Proxy** — AOP · Aspect · Advice · Pointcut · JoinPoint · Advisor · Proxy · JDK Dynamic Proxy · CGLIB Proxy · Target Object · Self Invocation · Proxy Chain · MethodInterceptor · ProxyFactory · TargetSource
- **Weaving (위빙)** — Weaving · Compile-time Weaving · Post-compile Weaving · Load-time Weaving(LTW) · Runtime Proxy-based AOP · AspectJ · Spring AOP vs AspectJ · @EnableLoadTimeWeaving · aspectjWeaving · spring-aspects.jar

가장 중요한 문턱은 **Self Invocation**이다. 같은 객체 내부에서 `this.inner()`로 호출하면 프록시를 거치지 않아 `inner()`의 `@Transactional`이 동작하지 않는다. Spring AOP는 기본적으로 런타임 프록시이므로 클래스 파일 자체를 바꾸지 않고, private/final 메서드와 Bean이 아닌 객체에는 적용이 어렵다. 반면 AspectJ는 컴파일 타임·로드 타임에 클래스 자체를 엮는 위빙으로 더 넓은 지점에 개입한다.

### 3단계 — @Transactional

- **7. @Transactional 내부 구조** — PlatformTransactionManager · DataSourceTransactionManager · JpaTransactionManager · TransactionInterceptor · TransactionAttribute · TransactionSynchronizationManager · Propagation(REQUIRED · REQUIRES_NEW · NESTED · SUPPORTS · NOT_SUPPORTED · MANDATORY · NEVER) · Isolation(DEFAULT · READ_UNCOMMITTED · READ_COMMITTED · REPEATABLE_READ · SERIALIZABLE) · Rollback Rule · rollbackFor · readOnly · timeout · Checked/Unchecked Exception

트랜잭션은 문서로만 배우지 않는다. DB에 데이터를 넣고, 실패시키고, 로그를 보며 REQUIRES_NEW가 정말 독립 트랜잭션인지·catch한 예외가 rollback을 막는지·checked exception에서 기본 rollback이 왜 안 되는지를 손으로 확인해야 한다.

### 4단계 — Spring MVC / 요청 처리

- **8. Spring MVC 요청 처리 흐름** — DispatcherServlet · HandlerMapping · HandlerAdapter · ModelAndView · ViewResolver · Filter · Interceptor
- **9. ArgumentResolver / MessageConverter** — HandlerMethodArgumentResolver · HandlerMethodReturnValueHandler · HttpMessageConverter · @RequestBody · @ResponseBody
- **10. Exception Handling** — HandlerExceptionResolver · @ControllerAdvice · @RestControllerAdvice · ProblemDetail

요청 흐름: Client → Servlet Filter → DispatcherServlet → HandlerMapping → HandlerAdapter → ArgumentResolver → Controller → ReturnValueHandler → HttpMessageConverter → Response. Custom ArgumentResolver로 로그인 사용자를 주입해보면 MVC가 더 이상 검은 상자가 아니다.

### 5단계 — Validation / Binding / Conversion

- **11. Validation / Data Binding / Type Conversion** — Bean Validation · @Valid · @Validated · BindingResult · MethodArgumentNotValidException · ConstraintViolationException · Validator · DataBinder · WebDataBinder · Converter · Formatter · PropertyEditor · ConversionService

`@Valid`(RequestBody)와 `@Validated`(RequestParam·그룹) 검증 실패는 올라오는 예외가 다르다. 형식 검증은 Controller, 유스케이스 검증은 Application Service, 도메인 규칙은 Domain Component로 나눈다.

### 6단계 — Spring Boot 자동구성·외부설정

- **12. Configuration / Profile / Externalized Config** — Environment · PropertySource · application.yml · application-{profile}.yml · @Value · Relaxed Binding · ConfigData · Command Line Argument
- **13. Spring Boot Auto Configuration** — SpringApplication · @EnableAutoConfiguration · @SpringBootApplication · @ConditionalOnClass · @ConditionalOnMissingBean · @ConditionalOnProperty · AutoConfiguration.imports · spring.factories · Binder
- **14. Spring Boot Starter 구조** — Starter · BOM · autoconfigure 모듈 · @ConfigurationProperties · @EnableConfigurationProperties

의존성만 추가했는데 Bean이 자동 등록되는 이유, 내가 만든 Bean이 있으면 Boot 기본 Bean이 `@ConditionalOnMissingBean`으로 비켜서는 이유를 직접 만든 Starter로 확인한다. 설정이 많아지면 `@Value`보다 `@ConfigurationProperties`가 구조화·테스트·문서화에 유리하다.

### 7단계 — 운영·연동·테스트

- **15. Data Access / Transaction / MyBatis** — DataSource · HikariCP · SqlSessionFactory · SqlSessionTemplate · Mapper Proxy · Connection Binding · MyBatis Executor · Batch Executor · Mapper XML · Dynamic SQL
- **16. Event / TransactionalEventListener** — ApplicationEventPublisher · @EventListener · @TransactionalEventListener · TransactionPhase(BEFORE_COMMIT · AFTER_COMMIT · AFTER_ROLLBACK · AFTER_COMPLETION) · Synchronous/Asynchronous Event · Outbox
- **17. Async / Scheduling / ThreadPool** — @Async · @EnableAsync · TaskExecutor · ThreadPoolTaskExecutor · @Scheduled · @EnableScheduling · TaskScheduler · fixedRate · fixedDelay · cron · MDC Propagation · 분산락
- **18. Cache Abstraction** — CacheManager · @Cacheable · @CachePut · @CacheEvict · Cache Key · TTL · Local/Distributed Cache · Caffeine · Redis · Cache Stampede · Cache Penetration · Cache Invalidation
- **19. Spring Security** — SecurityFilterChain · FilterChainProxy · SecurityContext · SecurityContextHolder · Authentication · Principal · GrantedAuthority · AuthenticationManager · AuthenticationProvider · UserDetailsService · PasswordEncoder · AuthorizationManager · Method Security · CSRF · CORS · JWT · OAuth2 Resource Server
- **20. Actuator / Observability** — spring-boot-starter-actuator · HealthIndicator · Readiness · Liveness · Metrics · Micrometer · Prometheus Endpoint · Loggers Endpoint · Custom HealthIndicator · Custom Meter
- **21. Spring Test** — JUnit 5 · Mockito · AssertJ · @SpringBootTest · @WebMvcTest · @DataJdbcTest · @MybatisTest · @MockBean · TestContext Framework · ApplicationContext Caching · @Transactional Test · MockMvc · WebTestClient · TestRestTemplate · Testcontainers
- **22~24. 성능 튜닝 / 아키텍처 설계 패턴 / 운영 장애 분석** — 부팅 비용 · 스레드풀 고갈 · health down 원인 · Layered Architecture · Graceful Shutdown · Structured Logging · TraceId

`@Transactional` → TransactionInterceptor → DataSourceTransactionManager → Connection 획득 → TransactionSynchronizationManager에 바인딩 → MyBatis SqlSessionTemplate이 같은 Connection 사용 → commit/rollback. 이 흐름을 이해하면 "왜 트랜잭션이 안 먹지?"의 절반이 풀린다.

> **심화 실습 후보** — ① Mini Spring Container(BeanDefinition·생성자 주입·싱글톤 캐시 흉내) ② Transaction Lab(REQUIRED·REQUIRES_NEW·NESTED·self-invocation·rollbackFor를 표로 정리) ③ Spring MVC Internal Lab(Custom Filter·Interceptor·ArgumentResolver·ProblemDetail) ④ Custom Spring Boot Starter(AutoConfiguration·Conditional·ConfigurationProperties) ⑤ Production-ready Spring Template(Layered·Global Exception·Actuator·TraceId·Testcontainers). 다섯 개를 만들면 Spring은 더 이상 마법의 숲이 아니다.



## 이관 진척

`poc/10_Spring/` → 여기로의 이관은 청크 단위로 진행한다. 진척 상태는 `STUDY_INDEX.md` 하단의 이관 표에서 확인한다.
