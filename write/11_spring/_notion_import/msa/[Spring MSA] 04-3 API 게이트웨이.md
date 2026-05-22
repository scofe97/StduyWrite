# [Spring MSA] 04-3. API 게이트웨이

주제: Spring MSA

- 참고
    
    [msaschool - msaschool](https://www.msaschool.io/operation/architecture/architecture-one/)
    
    [What is an API Gateway? How Does it Work?](https://www.wallarm.com/what/the-concept-of-an-api-gateway)
    
    [API 게이트웨이 패턴과 클라이언트-마이크로 서비스 간 직접 통신 - .NET](https://learn.microsoft.com/ko-kr/dotnet/architecture/microservices/architect-microservice-container-applications/direct-client-to-microservice-communication-versus-the-api-gateway-pattern)
    
    [마이크로서비스 구축을 위한 API Gateway 패턴 사용하기](https://nginxstore.com/blog/api-gateway/마이크로서비스-구축을-위한-api-gateway-패턴-사용하기/#5)
    
    [Spring Cloud Gateway](https://docs.spring.io/spring-cloud-gateway/docs/4.0.9/reference/html/)
    
    [[Spring Cloud] Spring Cloud Gateway - 기본 개념](https://velog.io/@mrcocoball2/Spring-Cloud-Spring-Cloud-Gateway-기본-개념)
    
    [[Spring] Spring Cloud Gateway(스프링 클라우드 게이트웨이) 공식 문서 간단히 살펴보기 및 리서치 후기](https://mangkyu.tistory.com/230)
    

# Api Gateway

---

<aside>
💡 **NOTE**

> *API Gateway는 API 서버 앞단에서 모든 API 서버들의 엔드포인트를 단일화하여 묶어주고 API에 대한 인증/인가 기능에따라 여러 서버로 라우팅 하는 기능을 담당할 수 있습니다.*
> 

API 게이트웨이는 **ESB(Enterprise Service Bus)**에서부터 시작되었습니다. ESB가 SOAP/XML 웹서비스 기반의 많은 기능을 가지는 구조였다면, API 게이트웨이는 JSON/REST 기반의 최소한의 기능을 처리하는 경량화 서비스입니다.

![단일 진입점](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled.png)

단일 진입점

- 보안, 로깅, 속도제한과 같은 횡단 관심사의 기능을 독립적으로 배치할 수 있고, 모든 MSA 호출에 대한 필터와 라우터 역할을 한다.
- 단일 정책 시행 시점(PEP, Policy Enforcement Point)역할을 하는 서비스게이트 웨이를 통해 클라이언트는 요청한다.
- 모든 서비스 호출이 게이트웨이를 통과하는 만큼 지표 수집이 원활하다.
</aside>

## **API Gateway + BFF 패턴**

<aside>
✍️ **NOTE**

> *API Gateway 계층에서 API Gateway를 여러 개로 분할하면서 서로 다른 이기종의 클라이언트 앱 또는 비즈니스 로직 요청에 대해 응답을 처리하는 패턴을 BFF(Backend for Frontend)패턴이라 합니다.*
> 

![각 플랫폼에 BFF 적용](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%201.png)

각 플랫폼에 BFF 적용

![API Gateway를 여러개 두는 구조](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%202.png)

API Gateway를 여러개 두는 구조

- 프론트엔드와 백엔드 사이의 중개 역할을 하며, 클라이언트가 직접 마이크로서비스와 통신하지 ㅇ낳아도 됩니다.
- 클라이언트가 변경될 때마다 백엔드 로직을 업데이트하지 않고 BFF를 수정하면 된다.
</aside>

## API Gateway의 동작

<aside>
✍️ **NOTE**

> *API Gateway는 내부에서*
> 

![unnamed.webp](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/unnamed.webp)

![API Gateway 핵심 동작](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%203.png)

API Gateway 핵심 동작

- 서비스 디스커버리(Eureka Service)는 서비스 검색 및 등록이외의 작업은 하지 못합니다.
- 콘텐츠 캐시, 로그 수집과 같은 공통로직을 쉽게 구현할 수 있습니다.
</aside>

# **Spring Cloud Gateway**

---

<aside>
💡 **NOTE**

> *Spring Cloud Gateway는 스프링 리액터에 기반한 게이트웨이로 Circuit Breaker 서비스와도 통합되는 등 Spring Api Gateway를 개발하는데 매우 유용하다!*
> 

![Spring Cloud Gateway구조](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%204.png)

Spring Cloud Gateway구조

- `Route`: 고유 ID + 목적지 URI +  Predicate + Filter로 구성되며 Predicate + Filter의 묶음이자 라우팅이 될 규칙이다.
- `Predicate`: 주어진 요청이 주어진 조건을 충족하는지 테스트하는 구성 요소이며, 하나 이상의 조건자를 정할 수 있습니다.(만약 Predicate에 매칭되지 않으면 404로 응답합니다.)
- `Filter & Filter Chain`: Gateway를 통해 들어오는 요청/응답에 대한 전후처리를 담당합니다.

```yaml
[
  {
	  # 매칭
	  "predicate": "Paths: [/accounts/**], match trailing slash: true",
	  "metadata": {
	    "management.port": "8080"
	  },
	  "route_id": "ReactiveCompositeDiscoveryClient_ACCOUNTS",
	  
	  # 세그먼트 추출 & 응답헤더에 X-ResponseTime 추가
	  "filters": [
	    "[[RewritePath /accounts/?(?<remaining>.*) = '/${remaining}'], order = 1]"
	  ],
	  
	  # 로드 밸런서 이름이 ACCOUNTS 서비스 라우팅
	  "uri": "lb://ACCOUNTS",
	  "order": 0
  },
]
```

```bash
# Gateway Enpoint/account ~ (predicate검사확인)
POST http://localhost:8072/accounts/api/create
GET http://localhost:8072/accounts/api/fetch?mobileNumber=4354437687
```

</aside>

## Spring API Gateway 설정

<aside>
✍️ **NOTE**

```groovy
dependencies {
		implementation 'org.springframework.cloud:spring-cloud-starter-gateway'
	
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'org.springframework.cloud:spring-cloud-starter-config'
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-client'
    
    // ...
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:2023.0.1"
    }
}
```

[https://github.com/eazybytes/microservices-config](https://github.com/eazybytes/microservices-config)

```yaml
spring:
  application:
    name: "gatewayserver"

  config:
    import: "optional:configserver:http://localhost:8071/" # 유레카 관련설정 

	# Gateway 설정
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true # 서비스 디스커버리를 통한 라우트 생성이 활성
          lower-case-service-id: true # 서비스 ID를 모두 소문자로 처리하여 라우트를 생성
          

# Actuator 활성화       
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    gateway:
      enabled: true
  info:
    env:
      enabled: true

info:
  app:
    name: "gatewayserver"
    description: "Eazy Bank Gateway Server Application"
    version: "1.0.0" 
```

</aside>

## 게이트웨이 필터

<aside>
✍️ **NOTE**

> *Spring Cloud Gateway는 `RouteLocater` 빈을 정의하여 특정 경로에 대한 요청을 처리하는 방법을 지정할 수 있습니다.*
> 

아래의 코드는 특정 경로로 들어오는 요청을 적절한 서비스로 전달하며, 이 과정에서 경로 재작성과 응답헤더 추가와 같은 필터 작업을 수행할 수 있습니다.

```java
@Bean
public RouteLocator eazyBankRouteConfig(RouteLocatorBuilder routeLocatorBuilder) {

	  // 사용자 정의 라우팅 필터
    return routeLocatorBuilder.routes()
            .route(p -> p
                    .path("/eazybank/accounts/**")
                    .filters(f -> f
				                    .rewritePath("/eazybank/accounts/(?<segment>.*)", "/${segment}")
                            .addResponseHeader("X-Response-Time", LocalDateTime.now().toString()))
                    .uri("lb://ACCOUNTS"))
                    
            .route(p -> p
                    .path("/eazybank/loans/**")
                    .filters(f -> f
				                    .rewritePath("/eazybank/loans/(?<segment>.*)", "/${segment}")
                            .addResponseHeader("X-Response-Time", LocalDateTime.now().toString()))
                    .uri("lb://LOANS"))
                    
            .route(p -> p
                    .path("/eazybank/cards/**")
                    .filters(f -> f
				                    .rewritePath("/eazybank/cards/(?<segment>.*)", "/${segment}")
                            .addResponseHeader("X-Response-Time", LocalDateTime.now().toString()))
                    .uri("lb://CARDS")).build();
}
```

- 필터의 경우에는 경로 재작성, 헤더, 파라미터 추가 등 다양한 작업을 수행할 수 있습니다.
- `f.rewritePath` 흐름도
    1. `/eazybank/accounts/details/123` 요청
    2. `/eazybank/accounts/(?<segment>.*)` 매칭
    3. ‘`segment`’는 `details/123`로 매칭
    4. `/eazybank/accounts/details/123` ⇒ `/details/123` 재작성하여 전송

```java
@Configuratio
public class FilterConfig {

    @Bea
    public RouteLocator gatewayRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
            // 경로가 '/first-service/**'로 시작하는 모든 요청을 매치
            .route(r -> r.path("/first-service/**")
            // 요청/응답 필터작업(헤더 추가)
            .filters(f -> f
                .addRequestHeader("first-request", "first-request-header")
                .addResponseHeader("first-response", "first-response-header"))
            // 요청을 localhost의 8081 포트로 전달
            .uri("http://localhost:8081/"))
            
            // 경로가 '/second-service/**'로 시작하는 모든 요청을 매치
            .route(r -> r.path("/second-service/**")
            .filters(f -> f
                .addRequestHeader("second-request", "second-request-header")
                .addResponseHeader("second-response", "second-response-header"))
            .uri("http://localhost:8082/"))
		        .build();
    }
}
```

```yaml
sping:
	cloud:
	  gateway:
	    routes:
	      # 첫 번째 서비스의 라우트를 정의합니다.
	      - id: first-service # 라우트 ID
	        uri: http://localhost:8081/ # 라우트가 포워딩할 서비스의 URI
	        predicates:
	          - Path=/first-service/** # '/first-service'로 시작하는 모든 경로를 매치하는 조건
	        filters:
	          - AddRequestHeader=first-request, first-request-header2
	          - AddResponseHeader=first-response, first-response-header
	          
	      # 두 번째 서비스의 라우트를 정의합니다.
	      - id: second-service # 라우트 ID
	        uri: http://localhost:8082/ # 라우트가 포워딩할 서비스의 URI
	        predicates:
	          - Path=/second-service/** # '/second-service'로 시작하는 모든 경로를 매치하는 조건
	        filters:
	          - AddRequestHeader=second-request, second-request-header2
	          - AddResponseHeader=second-response, second-response-header2
```

</aside>

## 게이트웨이 커스텀 필터

<aside>
✍️ **NOTE**

> *Spring Cloud Gateway는 `RouteLocater` 빈을 정의하여 특정 경로에 대한 요청을 처리하는 방법을 지정할 수 있습니다.*
> 

### 커스텀 필터

커스텀 필터를 만들어서 API Gateway에 적용할수 있습니다.

```java
@Component
// 이 클래스는 사용자 정의 게이트웨이 필터 팩토리를 정의합니다.
// AbstractGatewayFilterFactory를 상속받음으로써
// Spring Cloud Gateway의 필터 팩토리로 사용될 수 있습니다.
public class CustomFilter extends AbstractGatewayFilterFactory<CustomFilter.Config> {
    // Config는 AbstractGatewayFilterFactory에 사용되는 구성 타입입니다.
    public CustomFilter() {
        super(Config.class);
    }

    // 필터의 동작을 정의합니다.
    @Override
    public GatewayFilter apply(Config config) {
        // Custom Pre Filter. JWT 인증을 수행할 수 있다고 가정합니다.
        return (exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest();
            ServerHttpResponse response = exchange.getResponse();

            // 요청 URI와 함께 프리 필터 동작을 로깅합니다.
            log.info("Custom PRE filter: request uri -> {}", request.getId());

            // 필터 체인을 통해 요청을 다음 필터 또는 서비스로 전달합니다.
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                // Custom Post Filter. 오류에 따라 에러 응답 핸들러를 호출할 수 있다고 가정합니다.
                // 응답 코드와 함께 포스트 필터 동작을 로깅합니다.
                log.info("Custom POST filter: response code -> {}", response.getStatusCode());
            }));
        };
    }

    // 필터 구성을 위한 내부 클래스입니다.
    public static class Config {
        // 필터 구성을 위한 설정 값들을 정의할 수 있습니다.
    }
}
```

```yaml
routes:
  - id: first-service
    uri: http://localhost:8081/
    predicates:
      - Path=/first-service/**
    filters:
      - CustomFilter

  - id: second-service
    uri: http://localhost:8082/
    predicates:
      - Path=/second-service/**
    filters:
      - name: CustomFilter
      - name: LoggingFilter
        args:
          baseMessage: Hi, there.
          preLogger: true
          postLogger: true
```

### 글로벌 필터(default-filters)

커스텀 필터와 달리, 직접 등록할 필요없이 전역적으로 설정됩니다.

```java
// 이 클래스는 전역 게이트웨이 필터로 작동하며, 모든 라우트에 적용됩니다.
@Component
public class GlobalFilter extends AbstractGatewayFilterFactory<GlobalFilter.Config> {
    // 기본 생성자에서 Config 클래스를 슈퍼클래스 생성자에 전달합니다.
    public GlobalFilter() {
        super(Config.class);
    }

    // apply 메소드는 게이트웨이 필터 인스턴스를 반환합니다.
    @Override
    public GatewayFilter apply(Config config) {
        // 람다 표현식을 사용하여 GatewayFilter의 동작을 정의합니다.
        return (exchange, chain) -> {
            // HTTP 요청과 응답 객체를 가져옵니다.
            ServerHttpRequest request = exchange.getRequest();
            ServerHttpResponse response = exchange.getResponse();

            // 구성에 따라 로깅할 기본 메시지를 출력합니다.
            log.info("Global Filter baseMessage: {}", config.getBaseMessage());

            // preLogger 구성이 true일 때, 요청 시작을 로깅합니다.
            if (config.isPreLogger()) {
                log.info("Global Filter Start: request id -> {}", request.getId());
            }

            // 체인의 다음 필터에 요청을 전달하고, 요청 처리가 끝나면 응답을 로깅합니다.
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                // postLogger 구성이 true일 때, 응답 완료를 로깅합니다.
                if (config.isPostLogger()) {
                    log.info("Global Filter End: response code -> {}", response.getStatusCode());
                }
            }));
        };
    }

    // Config는 필터 구성을 위한 정적 내부 클래스입니다.
    @Data // 롬복 라이브러리의
    public static class Config {
        // 기본 메시지, 프리 로깅, 포스트 로깅 활성화 여부를 위한 필드입니다.
        private String baseMessage;
        private boolean preLogger;
        private boolean postLogger;
    }
}
```

```yaml
# Spring Cloud Gateway의 전역 설정입니다.
cloud:
  gateway:
    # 모든 라우트에 기본적으로 적용될 필터를 정의합니다.
    default-filters:
      - name: GlobalFilter # 사용할 필터의 이름입니다. (Bean의 이름과 동일해야함)
        args: # 필터에 전달할 인자들입니다.
          baseMessage: Spring Cloud Gateway GlobalFilter # 로그에 출력할 기본 메시지입니다.
          preLogger: true # 요청 시작시 로그를 남길지 여부를 설정합니다.
          postLogger: true # 응답 완료시 로그를 남길지 여부를 설정합니다.
          
    # 정의된 라우트들입니다.
    routes:
			#...
```

### 로깅 필터

```java
// @Component 어노테이션으로 클래스를 스프링 빈으로 등록합니다.
// @Slf4j는 Lombok 라이브러리의 어노테이션으로 로그를 위한 Slf4j 로거를 제공합니다.
@Component
@Slf4j
public class LoggingFilter extends AbstractGatewayFilterFactory<LoggingFilter.Config> {
    // LoggingFilter의 생성자입니다. Config.class를 상위 클래스의 생성자로 전달합니다.
    public LoggingFilter() { 
        super(Config.class); 
    }

    // apply 메소드는 GatewayFilter를 반환합니다. 이 메소드는 실제 필터 로직을 정의합니다.
    @Override
    public GatewayFilter apply(Config config) {
        // 람다 표현식을 사용하여 GatewayFilter의 동작을 정의합니다.
        return (exchange, chain) -> {
            // HTTP 요청과 응답 객체를 가져옵니다.
            ServerHttpRequest request = exchange.getRequest();
            ServerHttpResponse response = exchange.getResponse();

            // 구성에 따라 로깅할 기본 메시지를 출력합니다.
            log.info("Logging filter baseMessage: " + config.getBaseMessage());

            // preLogger가 true로 설정된 경우, 요청 정보를 로깅합니다.
            if (config.isPreLogger()) {
                log.info("Logging PRE filter: request uri -> {}", request.getURI());
            }

            // 체인의 다음 필터에 요청을 전달하고, 요청 처리가 끝나면 응답을 로깅합니다.
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                // postLogger가 true로 설정된 경우, 응답 정보를 로깅합니다.
                if (config.isPostLogger()) {
                    log.info("Logging fPOST filter: response code -> {}", response.getStatusCode());
                }
            }));
        };
    }
}
```

</aside>

## 스프링 게이트 웨이 로드밸런스

<aside>
✍️ **NOTE**

![1. Api Gateway
2. Service Discovery
3. Service](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%205.png)

1. Api Gateway
2. Service Discovery
3. Service

```yaml
eureka:
	client:
		register-with-eureka: true
		fetch-registry: true
		service-url:
			defaultZone: http://localhost:8761/euraka

sping:
	cloud:
	  gateway:
	    routes:
	      - id: first-service # 첫 번째 서비스의 고유 ID
	        uri: lb://MY-FIRST-SERVICE # 'MY-FIRST-SERVICE'를 가리키는 로드밸런서를 사용하는 서비스 URI
	        predicates:
	          - Path=/first-service/** # '/first-service'로 시작하는 모든 경로를 매칭하는 조건
	          	
	      - id: second-service # 두 번째 서비스의 고유 ID
	        uri: lb://MY-SECOND-SERVICE # 'MY-SECOND-SERVICE'를 가리키는 로드밸런서를 사용하는 서비스 URI
	        predicates:
	          - Path=/second-service/** # '/second-service'로 시작하는 모든 경로를 매칭하는 조건

```

</aside>

![Untitled](%5BSpring%20MSA%5D%2004-3%20API%20%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4/Untitled%206.png)

Gateway 서버 내에서 커스텀 필터를 생성하고 있습니다. 주된 목적은 외부 요청이 게이트웨이 서버에 도착하면, 고유한 correlation ID를 생성하고 이 ID를 다른 마이크로서비스로 전달한 후, 클라이언트에게 응답을 보낼 때 응답 헤더에 이 ID를 포함시키는 것입니다. 이를 통해 요청이 마이크로서비스 네트워크 내에서 어떻게 이동했는지 추적할 수 있습니다.

**RequestTraceFilter:**

- 외부에서 들어오는 요청마다 고유한 correlation ID를 생성합니다.
- 이미 correlation ID가 존재하는 경우, 새로 생성하지 않습니다.
- **`GlobalFilter`** 인터페이스를 구현하고 **`Order`** 어노테이션을 사용하여 필터 실행 순서를 지정합니다.

**ResponseTraceFilter:**

- 마이크로서비스로부터 받은 응답에 correlation ID를 추가합니다.
- **`@Configuration`** 어노테이션과 **`@Bean`** 어노테이션을 사용하여 커스텀 글로벌 필터를 정의합니다.

**FilterUtility:**

- 요청과 응답 필터에서 공통으로 사용되는 로직을 처리합니다.
- correlation ID의 존재 여부를 확인하고, 있으면 해당 값을 반환합니다.

**Spring Cloud Gateway에서의 로그 설정:**

- **`application.yml`** 파일에서 로그 레벨을 **`debug`**로 설정하여, 개발 중에 디버그 로그를 출력할 수 있도록 설정합니다.

이번 강의에서는 Gateway 서버에서 전달하는 요청 헤더를 개별 마이크로서비스가 받아들이는 방법을 구현했습니다. 이를 통해 마이크로서비스는 Gateway가 생성한 correlation ID를 포함하여, 요청이 마이크로서비스 네트워크를 거치는 과정을 추적할 수 있게 됩니다. 이는 마이크로서비스 아키텍처에서 중요한 추적 기능을 제공합니다.

**주요 단계:**

1. **Controller 변경:** **`AccountsController`**와 **`CustomerController`**와 같은 마이크로서비스 내의 Controller에 **`@RequestHeader`** 어노테이션을 추가하여 Gateway에서 전달하는 **`easybank-correlation-id`** 헤더를 수신합니다.
2. **Logger 추가:** 각 마이크로서비스에 로거를 추가하여 correlation ID와 함께 로그를 남깁니다.
3. **Feign Client 수정:** **`LoansFeignClient`**와 **`CardsFeignClient`** 인터페이스를 수정하여 **`@RequestHeader`** 어노테이션으로 correlation ID를 받도록 변경합니다.
4. **Service 구현 변경:** **`CustomerServiceImpl`**와 같은 서비스 구현에서 correlation ID를 받아서 다른 마이크로서비스로 전달합니다.
5. **YAML 파일 수정:** **`application.yml`** 파일에서 **`logging.level.com.eazybytes.*`** 속성을 **`debug`**로 설정하여, 마이크로서비스의 로그 레벨을 debug로 지정합니다.

이 모든 변경 사항을 통해, 마이크로서비스 간의 요청이 어떻게 전달되고 처리되는지 더 잘 이해하고 추적할 수 있게 됩니다. 디버깅 및 모니터링을 위한 훌륭한 기초를 제공합니다.

**포스트맨 검증:**

- Postman을 사용하여 **`fetchCustomerDetails`** API를 호출하면, 마이크로서비스가 Gateway에서 전달한 correlation ID를 받고, 로그를 남긴 후 클라이언트에게 응답을 보냅니다.
- 응답 헤더에서 **`EasyBank-correlationId`**를 확인할 수 있으며, 로그 파일에서도 이 ID를 검색하여 요청이 처리된 경로를 확인할 수 있습니다.

```java
// FilterUtility 클래스는 HTTP 헤더와 관련된 유틸리티 메서드를 제공하는 컴포넌트입니다.
@Component
public class FilterUtility {

    // 상수로 정의된 correlation ID의 키 값입니다.
    public static final String CORRELATION_ID = "eazybank-correlation-id";

    // 요청 헤더에서 correlation ID를 추출하는 메서드입니다.
    public String getCorrelationId(HttpHeaders requestHeaders) {
        // 헤더에서 correlation ID를 가져옵니다.
        if (requestHeaders.get(CORRELATION_ID) != null) {
            List<String> requestHeaderList = requestHeaders.get(CORRELATION_ID);
            // 첫 번째 correlation ID를 반환합니다.
            return requestHeaderList.stream().findFirst().get();
        } else {
            // 헤더가 없으면 null을 반환합니다.
            return null;
        }
    }

    // 주어진 이름과 값으로 요청 헤더를 설정하는 메서드입니다.
    public ServerWebExchange setRequestHeader(ServerWebExchange exchange, String name, String value) {
        // 요청 객체를 변경하여 새 헤더를 추가합니다.
        return exchange.mutate().request(exchange.getRequest().mutate().header(name, value).build()).build();
    }

    // correlation ID를 요청 헤더에 설정하는 메서드입니다.
    public ServerWebExchange setCorrelationId(ServerWebExchange exchange, String correlationId) {
        // setRequestHeader를 호출하여 correlation ID를 설정합니다.
        return this.setRequestHeader(exchange, CORRELATION_ID, correlationId);
    }
}
```

```java
// 응답 트레이스를 위한 필터 구성을 정의하는 클래스입니다.
@Configuration
public class ResponseTraceFilter {

    // 로깅을 위한 Logger 객체입니다.
    private static final Logger logger = LoggerFactory.getLogger(ResponseTraceFilter.class);

    // FilterUtility 인스턴스를 자동 주입합니다.
    @Autowired
    FilterUtility filterUtility;

    // 응답 처리 후 실행되는 글로벌 필터를 빈으로 등록합니다.
    @Bean
    public GlobalFilter postGlobalFilter() {
        return (exchange, chain) -> {
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                // 요청 헤더를 가져옵니다.
                HttpHeaders requestHeaders = exchange.getRequest().getHeaders();
                // correlation ID를 추출합니다.
                String correlationId = filterUtility.getCorrelationId(requestHeaders);
                // 로그에 correlation ID를 기록합니다.
                logger.debug("Updated the correlation id to the outbound headers: {}", correlationId);
                // 응답 헤더에 correlation ID를 추가합니다.
                exchange.getResponse().getHeaders().add(filterUtility.CORRELATION_ID, correlationId);
            }));
        };
    }
}
```

```java

// 요청 트레이스를 위한 글로벌 필터 구현입니다.
@Component
public class RequestTraceFilter implements GlobalFilter {

    // 로깅을 위한 Logger 객체입니다.
    private static final Logger logger = LoggerFactory.getLogger(RequestTraceFilter.class);

    // FilterUtility 인스턴스를 자동 주입합니다.
    @Autowired
    FilterUtility filterUtility;

    // 요청을 처리하는 필터 메서드입니다.
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // 요청 헤더를 가져옵니다.
        HttpHeaders requestHeaders = exchange.getRequest().getHeaders();
        // correlation ID가 존재하는지 확인합니다.
        if (isCorrelationIdPresent(requestHeaders)) {
            // correlation ID가 있으면 로그에 기록합니다.
            logger.debug("eazyBank-correlation-id found in RequestTraceFilter : {}",
                    filterUtility.getCorrelationId(requestHeaders));
        } else {
            // correlation ID가 없으면 새로 생성합니다.
            String correlationID = generateCorrelationId();
            // 생성된 correlation ID를 요청 헤더에 설정합니다.
            exchange = filterUtility.setCorrelationId(exchange, correlationID);
            // 로그에 새로 생성된 correlation ID를 기록합니다.
            logger.debug("eazyBank-correlation-id generated in RequestTraceFilter : {}", correlationID);
        }
        // 요청을 계속 처리합니다.
        return chain.filter(exchange);
    }

    // 요청 헤더에서 correlation ID의 존재 여부를 확인하는 메서드입니다.
    private boolean isCorrelationIdPresent(HttpHeaders requestHeaders) {
        return filterUtility.getCorrelationId(requestHeaders) != null;
    }

    // 새로운 correlation ID를 생성하는 메서드입니다.
    private String generateCorrelationId() {
        // UUID를 사용하여 유일한 ID를 생성합니다.
        return java.util.UUID.randomUUID().toString();
    }
}
```