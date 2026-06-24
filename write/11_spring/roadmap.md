---
title: Spring 딥다이브 로드맵 — 섹션별 키워드 원문
tags: [moc, spring, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# Spring 딥다이브 로드맵 — 섹션별 키워드 원문

---

> "Spring Boot 로 API 를 만들 줄 아는 개발자" 에서 "Spring 이 왜 그렇게 동작하는지 설명하고, 장애·성능·테스트·트랜잭션까지 설계할 수 있는 개발자" 로 가는 것이 목표입니다. 이 문서는 제공받은 Spring 딥다이브 로드맵 원문을 **섹션별로 빠짐없이** 옮긴 기록입니다. 폴더 배치·학습 경로·보유 문서 매핑은 [README.md](README.md) 가 맡고, 이 문서는 "각 섹션이 원래 무엇을 다루라고 했는가" 의 SSOT 입니다.

## 1. Spring 딥다이브 전체 지도

깊게 판다면 아래 순서가 좋습니다.

```text
1. Spring Core / IoC Container
2. Bean 등록과 생명주기
3. 의존성 주입과 순환 참조
4. ApplicationContext와 BeanFactory
5. BeanPostProcessor / BeanFactoryPostProcessor
6. AOP와 Proxy
7. @Transactional 내부 구조
8. Spring MVC 요청 처리 흐름
9. ArgumentResolver / MessageConverter
10. Exception Handling
11. Validation / Data Binding / Type Conversion
12. Configuration / Profile / Externalized Config
13. Spring Boot Auto Configuration
14. Spring Boot Starter 구조
15. Data Access / Transaction / MyBatis 연동
16. Event / TransactionalEventListener
17. Async / Scheduling / ThreadPool
18. Cache Abstraction
19. Spring Security
20. Actuator / Observability
21. Spring Test
22. Spring 애플리케이션 성능 튜닝
23. Spring 아키텍처 설계 패턴
24. Spring 운영 장애 분석
```

한 문장으로 줄이면: Spring Container 가 Bean 을 만들고, Proxy 가 부가기능을 감싸고, DispatcherServlet 이 요청을 흘려보내고, TransactionManager 가 DB 경계를 관리하고, Boot AutoConfiguration 이 설정을 조립하며, Actuator 와 Test 가 운영성과 검증 가능성을 열어줍니다.

## 2. 1단계: Spring Core / IoC Container

반드시 알아야 할 것:

```text
IoC
DI
Bean
BeanDefinition
BeanFactory
ApplicationContext
DefaultListableBeanFactory
Component Scan
@Configuration
@Bean
@Component
@Service
@Repository
@Controller
@Autowired
Constructor Injection
Qualifier
Primary
Lazy
Scope
Singleton
Prototype
```

깊게 볼 질문: @Service 는 언제 BeanDefinition 으로 변환되는가 / Bean 객체는 언제 실제로 생성되는가 / 싱글톤 Bean 은 어디에 캐싱되는가 / @Autowired 는 생성자 주입과 필드 주입에서 어떻게 다르게 동작하는가 / @Configuration 클래스는 왜 일반 클래스와 다르게 처리되는가 / @Bean 메서드를 직접 호출하면 정말 같은 Bean 이 반환되는가.

핵심 내부 흐름: ClassPath Scan → BeanDefinition 생성 → BeanFactory 에 등록 → BeanFactoryPostProcessor 실행 → Bean 인스턴스 생성 → 의존성 주입 → BeanPostProcessor before → InitializingBean/@PostConstruct → BeanPostProcessor after → Singleton Bean 캐싱. Spring 은 처음부터 객체를 만드는 게 아니라 먼저 BeanDefinition 이라는 설계도를 만들고 그 설계도로 객체를 조립합니다.

## 3. 2단계: Bean 생명주기

학습 키워드:

```text
Bean Lifecycle
Instantiation
Dependency Injection
Aware Interface
BeanNameAware
ApplicationContextAware
InitializingBean
DisposableBean
@PostConstruct
@PreDestroy
initMethod
destroyMethod
SmartInitializingSingleton
SmartLifecycle
```

생명주기 흐름: BeanDefinition 로딩 → Bean 인스턴스 생성 → 의존성 주입 → Aware 계열 콜백 → BeanPostProcessor before initialization → @PostConstruct → InitializingBean.afterPropertiesSet() → initMethod → BeanPostProcessor after initialization → 사용 → @PreDestroy → DisposableBean.destroy() → destroyMethod.

실무 질문: 초기화 시점에 외부 API 를 호출해도 되는가 / Bean 생성 중 예외가 나면 전체 애플리케이션이 뜨지 않는가 / @PostConstruct 에서 트랜잭션이 적용되는가 / ApplicationReadyEvent 와 @PostConstruct 는 무엇이 다른가 / SmartLifecycle 은 언제 쓰는가. @PostConstruct 에서 너무 많은 일을 하면 부팅이 무거워집니다.

## 4. 3단계: AOP 와 Proxy

`@Transactional`·`@Async`·`@Cacheable`·Method Security 는 대부분 프록시 기반으로 이해할 수 있습니다.

반드시 알아야 할 것:

```text
AOP
Aspect
Advice
Pointcut
JoinPoint
Advisor
Proxy
JDK Dynamic Proxy
CGLIB Proxy
Target Object
Self Invocation
Proxy Chain
Method Interceptor
```

핵심 질문: @Transactional 은 왜 private 메서드에 잘 맞지 않는가 / 같은 클래스 내부에서 `this.someMethod()` 를 호출하면 왜 트랜잭션이 안 걸리는가 / 인터페이스가 있으면 JDK Proxy, 없으면 CGLIB Proxy 가 쓰이는 이유는 / 프록시는 Bean 생성 과정 중 언제 만들어지는가 / 여러 AOP 가 걸리면 실행 순서는 어떻게 정해지는가.

가장 중요한 함정 — Self Invocation: `outer()` 가 같은 객체 내부의 `@Transactional inner()` 를 직접 호출하면 프록시를 거치지 않아 트랜잭션이 기대처럼 동작하지 않습니다. Spring 초급자와 중급자를 가르는 문턱입니다.

## 5. 3단계 보강: AOP 와 Weaving

Spring AOP 는 보통 "진짜 바이트코드 위빙" 이 아니라 "런타임 프록시 기반 AOP" 로 동작합니다. AspectJ 는 컴파일 타임 또는 로드 타임에 클래스 자체를 엮는 위빙을 할 수 있습니다. 위빙은 부가기능 코드인 Aspect 를 실제 대상 코드에 엮는 과정입니다.

추가 키워드:

```text
Weaving
Compile-time Weaving
Post-compile Weaving
Load-time Weaving
Runtime Proxy-based AOP
AspectJ
Spring AOP vs AspectJ
@EnableLoadTimeWeaving
aspectjWeaving
spring-aspects.jar
```

Weaving 방식 4가지:

1. **Compile-time Weaving** — 컴파일할 때 Aspect 가 대상 클래스에 엮인다(`ajc`). 대상 클래스 바이트코드 자체가 변경됨, 강력하지만 빌드 구성이 복잡.
2. **Post-compile Weaving** — 이미 컴파일된 `.class`/`.jar` 에 나중에 AspectJ weaver 로 엮는다. 소스 없이 라이브러리·기존 산출물에 부가기능을 넣을 수 있음.
3. **Load-time Weaving (LTW)** — 클래스가 JVM 에 로딩되는 순간 Java Agent / ClassFileTransformer 로 엮는다. `@EnableLoadTimeWeaving`, `@EnableLoadTimeWeaving(aspectjWeaving = ENABLED)` 로 활성화.
4. **Runtime Proxy-based AOP** — Spring AOP 의 일반적 방식. 클래스 파일을 바꾸지 않고 Proxy 객체를 생성해 Client 가 Proxy 를 호출하면 Advice 실행 후 Target 호출.

Runtime Proxy 방식의 제약: self-invocation 문제 · private 메서드 AOP 적용 어려움 · final 클래스/메서드 제약 · Spring Bean 이 아닌 객체에는 적용 어려움 · 메서드 실행 join point 중심.

| 구분 | Spring AOP | AspectJ |
|------|-----------|---------|
| 기본 방식 | 런타임 프록시 | 실제 위빙 |
| 적용 시점 | 런타임 Bean 프록시 생성 시 | 컴파일 타임 / 로드 타임 |
| 대상 | 주로 Spring Bean | 거의 모든 Java 객체 |
| 바이트코드 변경 | 일반적으로 없음 | 있음 |
| private 메서드 | 적용 어려움 | 가능 |
| 생성자 join point | 제한적 | 가능 |
| field 접근 join point | 제한적 | 가능 |
| 설정 난이도 | 낮음 | 높음 |
| 실무 사용성 | 일반적인 Spring 앱에 적합 | 프레임워크/라이브러리/깊은 계측에 적합 |

`@Transactional` 도 기본은 프록시 기반이지만 AspectJ 모드를 쓰면 weaving 기반으로 동작할 수 있습니다(`spring-aspects.jar` + LTW 또는 CTW 필요). 실무 우선순위: ① Spring AOP 는 기본 프록시 기반 → ② self-invocation 문제 → ③ @Transactional·@Async·@Cacheable 이 프록시 기반 → ④ AspectJ 는 실제 weaving 으로 더 넓게 개입 → ⑤ LTW 는 강력하지만 운영/빌드 복잡도가 있어 신중히. 가장 좋은 실험은 같은 로직을 순수 메서드 호출 / Spring AOP @Around / AspectJ LTW 세 방식으로 구현해보는 것입니다.

## 6. 4단계: @Transactional 딥다이브

반드시 알아야 할 것:

```text
PlatformTransactionManager
DataSourceTransactionManager
JpaTransactionManager
TransactionInterceptor
TransactionAttribute
TransactionSynchronizationManager
Propagation
Isolation
Rollback Rule
readOnly
timeout
Checked Exception
Unchecked Exception
```

Propagation: REQUIRED · REQUIRES_NEW · NESTED · SUPPORTS · NOT_SUPPORTED · MANDATORY · NEVER. Isolation: DEFAULT · READ_UNCOMMITTED · READ_COMMITTED · REPEATABLE_READ · SERIALIZABLE.

실무 질문: @Transactional 은 어느 계층에 두는 게 좋은가 / Service 가 다른 Service 를 호출할 때 트랜잭션은 어떻게 전파되는가 / REQUIRES_NEW 는 정말 독립 트랜잭션인가 / 예외를 catch 하면 rollback 이 되는가 / checked exception 에서는 왜 기본 rollback 이 안 되는가 / readOnly=true 는 성능 최적화인가 안전장치인가 / MyBatis 에서 Spring 트랜잭션은 어떻게 연결되는가.

꼭 실험할 것: REQUIRES_NEW 감사 로그 + 주문 rollback 시 주문 데이터는 rollback 되는가 / 감사 데이터는 commit 되는가 / AuditService 를 같은 클래스 내부 메서드로 옮기면 어떻게 되는가 / 예외 catch 위치에 따라 결과가 바뀌는가. 트랜잭션은 문서로만 배우지 않고 DB 에 데이터를 넣고 실패시키며 손으로 확인합니다.

## 7. 5단계: Spring MVC 요청 처리 흐름

반드시 알아야 할 것:

```text
DispatcherServlet
HandlerMapping
HandlerAdapter
HandlerMethodArgumentResolver
HttpMessageConverter
ModelAndView
ViewResolver
HandlerExceptionResolver
Filter
Interceptor
ControllerAdvice
RestControllerAdvice
```

요청 흐름: Client Request → Servlet Filter → DispatcherServlet → HandlerMapping → HandlerAdapter → ArgumentResolver → Controller Method → ReturnValueHandler → HttpMessageConverter → Response.

실무 질문: Filter 와 Interceptor 는 무엇이 다른가 / ArgumentResolver 는 언제 쓰는가 / @RequestBody 는 누가 JSON 을 객체로 바꾸는가 / @ResponseBody 는 누가 객체를 JSON 으로 바꾸는가 / ControllerAdvice 는 어느 시점에 개입하는가 / Validation 실패는 어떤 Exception 으로 올라오는가.

깊게 실험할 것: Custom ArgumentResolver · Custom Annotation 으로 로그인 사용자 주입 · Custom HandlerInterceptor · Global Exception Handler · HttpMessageConverter 동작 확인 · Filter 에서 request body 를 읽었을 때 문제 확인. `@CurrentUser` 같은 커스텀 애너테이션 + ArgumentResolver 를 직접 만들면 MVC 가 더 이상 검은 상자가 아닙니다.

## 8. 6단계: Validation / Binding / Conversion

반드시 알아야 할 것:

```text
Bean Validation
@Valid
@Validated
BindingResult
MethodArgumentNotValidException
ConstraintViolationException
Validator
DataBinder
WebDataBinder
Converter
Formatter
PropertyEditor
ConversionService
```

실무 질문: @Valid 와 @Validated 는 무엇이 다른가 / RequestBody 검증 실패와 RequestParam 검증 실패는 예외가 같은가 / Enum 변환 실패는 어디서 처리되는가 / 날짜 포맷은 어디서 통제하는가 / 비즈니스 검증과 입력값 검증은 어디서 나누는가.

추천 구조: Controller(형식·필수값·타입 검증) → Application Service(유스케이스·상태·권한 검증) → Domain Component(도메인 규칙 검증). 검증은 문지기입니다 — 모든 것을 판단하면 병목, 아무것도 판단하지 않으면 성이 무너집니다.

## 9. 7단계: Spring Boot Auto Configuration

반드시 알아야 할 것:

```text
SpringApplication
AutoConfiguration
@EnableAutoConfiguration
@SpringBootApplication
Condition
@ConditionalOnClass
@ConditionalOnMissingBean
@ConditionalOnProperty
@ConfigurationProperties
Binder
Starter
spring.factories
AutoConfiguration.imports
Environment
PropertySource
Profile
```

실무 질문: 왜 의존성만 추가했는데 Bean 이 자동 등록되는가 / 내가 만든 Bean 이 있으면 Boot 기본 Bean 은 왜 등록되지 않는가 / application.yml 값은 언제 객체에 바인딩되는가 / Profile 별 설정은 어떤 우선순위로 적용되는가 / Auto Configuration 이 너무 많이 켜질 때 어떻게 추적하는가.

꼭 해볼 프로젝트 — 나만의 Spring Boot Starter: autoconfigure 모듈(AutoConfiguration·Properties·Client) + starter 모듈(의존성 모음). 자동 설정은 따뜻한 난로지만 내부를 모르면 불씨가 어디서 시작됐는지 모릅니다.

## 10. 8단계: Configuration / Properties

반드시 알아야 할 것:

```text
Environment
PropertySource
application.yml
application-{profile}.yml
@ConfigurationProperties
@Value
Profile
ConfigData
Environment Variable
Command Line Argument
Relaxed Binding
```

추천: `@ConfigurationProperties(prefix = "app.order")` record + `@EnableConfigurationProperties`. `@Value` 가 나쁜 건 아니지만 설정이 많아질수록 `@ConfigurationProperties` 가 구조화·테스트·문서화에 유리합니다.

## 11. 9단계: Data Access / MyBatis / Transaction

반드시 알아야 할 것:

```text
DataSource
HikariCP
SqlSessionFactory
SqlSessionTemplate
Mapper Proxy
DataSourceTransactionManager
TransactionSynchronizationManager
Connection Binding
MyBatis Executor
Batch Executor
Mapper XML
Dynamic SQL
```

실무 질문: MyBatis Mapper 는 어떻게 인터페이스만으로 동작하는가 / SqlSessionTemplate 은 왜 thread-safe 한가 / @Transactional 이 걸리면 Connection 은 어디에 묶이는가 / 같은 트랜잭션 안에서 여러 Mapper 호출은 같은 Connection 을 쓰는가 / Batch Executor 는 언제 쓰는가 / select 후 update 사이에 lock 이 필요한가.

핵심 연결: Spring @Transactional → TransactionInterceptor → DataSourceTransactionManager → Connection 획득 → TransactionSynchronizationManager 에 Connection 바인딩 → MyBatis SqlSessionTemplate 이 같은 Connection 사용 → commit/rollback → Connection 반환. 이 흐름을 이해하면 "왜 트랜잭션이 안 먹지?" 의 절반이 해결됩니다.

## 12. 10단계: Event / TransactionalEventListener

반드시 알아야 할 것:

```text
ApplicationEventPublisher
ApplicationEvent
@EventListener
@TransactionalEventListener
TransactionPhase
BEFORE_COMMIT
AFTER_COMMIT
AFTER_ROLLBACK
AFTER_COMPLETION
Synchronous Event
Asynchronous Event
```

실무 질문: 이 이벤트는 같은 트랜잭션 안에서 처리되어야 하는가 / 리스너 실패가 원래 로직 실패로 이어져야 하는가 / AFTER_COMMIT 에서 실패하면 보상 처리는 어떻게 하는가 / 비동기 이벤트에서 MDC/traceId 는 유지되는가.

추천 기준: 같은 트랜잭션에서 반드시 성공 → 직접 메서드 호출 / 트랜잭션 성공 이후 부가 작업 → `@TransactionalEventListener(AFTER_COMMIT)` / 실패해도 원 요청을 막지 않아야 함 → Outbox 또는 비동기 이벤트 / 서비스 간 전달 → Kafka 같은 메시징.

## 13. 11단계: Async / Scheduling / ThreadPool

반드시 알아야 할 것:

```text
@Async
@EnableAsync
TaskExecutor
ThreadPoolTaskExecutor
@Scheduled
@EnableScheduling
TaskScheduler
fixedRate
fixedDelay
cron
MDC Propagation
Exception Handling
```

실무 질문: 기본 executor 를 그대로 쓰고 있지는 않은가 / 스레드 풀이 고갈되면 어떻게 되는가 / @Async 메서드 예외는 어디로 가는가 / @Scheduled 작업이 여러 인스턴스에서 동시에 실행되어도 되는가 / 스케줄러에 분산락이 필요한가. 운영에서 스레드는 작은 강입니다 — 흐름을 만들 수 있지만 둑이 없으면 범람합니다.

## 14. 12단계: Cache Abstraction

반드시 알아야 할 것:

```text
CacheManager
@Cacheable
@CachePut
@CacheEvict
Cache Key
TTL
Local Cache
Distributed Cache
Caffeine
Redis
Cache Stampede
Cache Penetration
Cache Invalidation
```

실무 질문: 캐시 키는 안정적인가 / 캐시 무효화 시점은 명확한가 / 트랜잭션 rollback 시 캐시가 먼저 갱신되지는 않는가 / 여러 인스턴스에서 local cache 를 써도 되는가 / TTL 은 왜 그 값인가. 캐시는 성능의 단비이지만 정합성의 그림자를 만듭니다.

## 15. 13단계: Spring Security

반드시 알아야 할 것:

```text
SecurityFilterChain
FilterChainProxy
SecurityContext
SecurityContextHolder
Authentication
Principal
GrantedAuthority
AuthenticationManager
AuthenticationProvider
UserDetailsService
PasswordEncoder
AuthorizationManager
Method Security
CSRF
CORS
Session
JWT
OAuth2 Resource Server
```

실무 질문: 인증과 인가는 어디서 나뉘는가 / JWT 검증은 어느 필터에서 수행되는가 / SecurityContext 는 ThreadLocal 기반인가 / 비동기 실행 시 SecurityContext 는 유지되는가 / URL 권한과 Method 권한 중 어디에 정책을 둘 것인가.

## 16. 14단계: Actuator / 운영 기능

반드시 알아야 할 것:

```text
spring-boot-starter-actuator
HealthIndicator
Readiness
Liveness
Metrics
Micrometer
Prometheus Endpoint
Info Endpoint
Loggers Endpoint
Custom HealthIndicator
Custom Meter
```

실무 endpoint: `/actuator/health` · `/health/readiness` · `/health/liveness` · `/metrics` · `/prometheus` · `/loggers` · `/info`.

실무 질문: DB 장애가 readiness 에 반영되는가 / 외부 API 장애를 health down 으로 볼 것인가 / 운영에서 actuator endpoint 가 과도하게 노출되어 있지는 않은가 / 커스텀 비즈니스 metric 을 만들 수 있는가 / 장애 시 log level 을 동적으로 바꿀 수 있는가.

## 17. 15단계: Spring Test

반드시 알아야 할 것:

```text
JUnit 5
Mockito
AssertJ
@SpringBootTest
@WebMvcTest
@DataJdbcTest
@MybatisTest
@MockBean 계열
TestContext Framework
ApplicationContext Caching
@Transactional Test
MockMvc
WebTestClient
TestRestTemplate
Testcontainers
```

실무 질문: 이 테스트는 Spring Context 가 꼭 필요한가 / 단위 테스트로 충분한가 / @SpringBootTest 를 남용하고 있지는 않은가 / 테스트마다 ApplicationContext 가 새로 떠서 느려지지 않는가 / @Transactional 테스트의 rollback 때문에 실제 운영 흐름과 달라지지 않는가 / MockMvc 테스트에서 Filter/Security 를 포함할 것인가.

추천 테스트 피라미드: Domain/Component 단위 테스트 → Application Service 통합 테스트 → Mapper/Repository 테스트 → Controller Slice 테스트 → 전체 SpringBootTest → E2E/Smoke Test.

## 18. 추천 프로젝트

- **프로젝트 1 — Mini Spring Container**: @Component 스캔 흉내 · BeanDefinition 등록 · 생성자 주입 · 싱글톤 캐시 · BeanPostProcessor 흉내 · @PostConstruct 흉내. (Spring 이 객체를 어떻게 만들고 보관하는지, DI 가 왜 중심인지)
- **프로젝트 2 — Transaction Lab**: REQUIRED · REQUIRES_NEW · NESTED · self-invocation · checked/unchecked exception · catch 후 rollback · rollbackFor · readOnly · timeout · MyBatis Mapper 호출 을 (상황→예상→실제→이유→관련 컴포넌트) 로 정리.
- **프로젝트 3 — Spring MVC Internal Lab**: Custom Filter · Interceptor · ArgumentResolver · ReturnValueHandler · HttpMessageConverter · ControllerAdvice · ProblemDetail 기반 에러 응답.
- **프로젝트 4 — Custom Spring Boot Starter**: 공통 로깅 · 요청 traceId · 표준 에러 응답 · 감사 로그 · 공통 ObjectMapper · 공통 WebMvcConfigurer · 공통 Actuator HealthIndicator. (AutoConfiguration · Conditional · ConfigurationProperties · Starter 구조)
- **프로젝트 5 — Production-ready Spring Template**: Layered Architecture · Global Exception Handling · Validation · Actuator · Health Check · Structured Logging · TraceId · Spring Security 기본 · MyBatis · Transaction · Testcontainers · Dockerfile · Jenkinsfile.

## 19. 딥다이브 학습 순서 (7단계)

1단계 Core: IoC · DI · BeanDefinition · ApplicationContext · Bean Lifecycle · Component Scan · @Configuration → "Spring 이 객체를 어떻게 만들고 주입하는지 설명할 수 있다".

2단계 Proxy/AOP/Transaction: JDK Proxy · CGLIB · AOP · @Transactional · TransactionManager · Propagation · Rollback · Self Invocation → "@Transactional 이 안 먹는 이유를 설명하고 고칠 수 있다".

3단계 Web MVC: DispatcherServlet · Filter · Interceptor · ArgumentResolver · MessageConverter · ExceptionResolver · Validation → "HTTP 요청이 Controller 까지 도달하고 응답이 나가는 과정을 설명할 수 있다".

4단계 Boot: SpringApplication · AutoConfiguration · Conditional · ConfigurationProperties · Profile · Starter → "의존성 하나 추가했을 때 왜 기능이 자동으로 켜지는지 설명할 수 있다".

5단계 Data/Transaction/MyBatis: DataSource · HikariCP · SqlSessionTemplate · Mapper Proxy · TransactionSynchronizationManager · Connection Binding → "Spring 트랜잭션과 MyBatis 가 같은 Connection 을 공유하는 흐름을 설명할 수 있다".

6단계 운영 Spring: Actuator · HealthIndicator · Micrometer · Logging · ThreadPool · Graceful Shutdown · Cache · Security → "Spring 애플리케이션을 운영 환경에서 관측하고 안전하게 종료할 수 있다".

7단계 Test: MockMvc · @SpringBootTest · Slice Test · TestContext Cache · Transactional Test · Testcontainers → "빠르고 신뢰할 수 있는 Spring 테스트 전략을 설계할 수 있다".

## 20. 최종 압축 키워드

```text
Spring Core
IoC Container
Dependency Injection
BeanDefinition
BeanFactory
ApplicationContext
DefaultListableBeanFactory
Component Scan
Bean Lifecycle
BeanPostProcessor
BeanFactoryPostProcessor
FactoryBean
Aware Interfaces
ApplicationEventPublisher
AOP
JDK Dynamic Proxy
CGLIB Proxy
Advisor
MethodInterceptor
Self Invocation
Weaving
Compile-time Weaving
Load-time Weaving
AspectJ
@Transactional
PlatformTransactionManager
TransactionInterceptor
TransactionSynchronizationManager
Propagation
Isolation
Rollback Rules
Spring MVC
DispatcherServlet
HandlerMapping
HandlerAdapter
HandlerMethodArgumentResolver
HandlerMethodReturnValueHandler
HttpMessageConverter
HandlerExceptionResolver
Filter
Interceptor
ControllerAdvice
Validation
DataBinder
ConversionService
Spring Boot
SpringApplication
AutoConfiguration
Conditional
ConfigurationProperties
Profile
Environment
PropertySource
Starter
Externalized Configuration
DataSource
HikariCP
MyBatis
SqlSessionTemplate
Mapper Proxy
Spring Event
@TransactionalEventListener
Async
TaskExecutor
Scheduling
Cache Abstraction
Spring Security
SecurityFilterChain
SecurityContext
Authentication
Authorization
Actuator
HealthIndicator
Micrometer
Prometheus
Spring Test
MockMvc
TestContext Framework
ApplicationContext Caching
Testcontainers
```

## 결론

Spring 을 깊게 판다는 것은 어노테이션을 더 많이 외우는 일이 아니라, @Autowired 가 왜 주입되는지 · @Transactional 이 왜 실패하는지 · @RequestBody 가 어디서 변환되는지 · AutoConfiguration 이 왜 켜지는지 · 테스트가 왜 느려지는지 · 운영에서 health 가 왜 내려가는지 에 답할 수 있게 되는 일입니다.

추천 학습 프로젝트 조합: Mini Spring Container → Transaction Lab → Spring MVC Internal Lab → Custom Spring Boot Starter → Production-ready Spring Template.

## 출처

- [Spring Framework Documentation](https://docs.spring.io/spring-framework/reference/index.html)
- [Core Technologies](https://docs.spring.io/spring-framework/reference/core.html)
- [Aspect Oriented Programming with Spring](https://docs.spring.io/spring-framework/reference/core/aop.html)
- [AOP Concepts](https://docs.spring.io/spring-framework/reference/core/aop/introduction-defn.html)
- [Using AspectJ with Spring Applications](https://docs.spring.io/spring-framework/reference/core/aop/using-aspectj.html)
- [Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)
- [Using @Transactional](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)
- [Spring Web MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- [Externalized Configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Spring Security](https://docs.spring.io/spring-security/reference/index.html)
- [Spring Security Architecture](https://docs.spring.io/spring-security/reference/servlet/architecture.html)
- [Production-ready Features](https://docs.spring.io/spring-boot/reference/actuator/index.html)
- [Testing](https://docs.spring.io/spring-framework/reference/testing.html)
