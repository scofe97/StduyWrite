# [Spring MSA] 04-1.  MSA통신방법(OpenFeign)

주제: Spring MSA

- 참고
    
    [[Spring] Spring Boot3.2에 새롭게 추가될 RestClient](https://mangkyu.tistory.com/303)
    
    [Microservice 간 통신 (RestTemplate, FeignClient, ErrorDecoder 예외처리), 데이터 동기화 문제](https://m.blog.naver.com/qjawnswkd/222326922628)
    
    [msaschool - msaschool](https://www.msaschool.io/operation/integration/integration-two/)
    
    [[Spring] OpenFeign이란? OpenFeign 소개 및 사용법](https://mangkyu.tistory.com/278)
    
    [Spring - OpenFeign](https://backtony.tistory.com/74)
    
    [FeignClient에서 read timeout 발생 시 주의사항 (w/ Retry, RetryableException)](https://hungseong.tistory.com/92)
    
    [[Spring] OpenFeign에 Resilence4J 서킷 브레이커 적용하는 방법과 예시 및 주의사항](https://mangkyu.tistory.com/289)
    

# **OpenFeign**

---

<aside>
💡 **NOTE**

> `*OpenFeign`은 Declarative(선언적인) HTTP Client 도구로써, 외부 API 호출을 HTTP 요청 코드를 직접 작성하지 않고도 REST API를 호출할 수 있습니다.*
> 

`OpenFeign`은 Spring Cloud 기반의 기술이므로 Spring Cloud에 대한 의존성이 필요합니다.

```groovy
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-openfeign'
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:2022.0.3"
    }
}
```

```java
@SpringBootApplication
@EnableFeignClients // 추가!
public class FeignClientApplication {

    public static void main(String[] args) {
        SpringApplication.run(FeignClientApplication.class, args);
    }
}
```

```java
// 선언적 방식(어노테이션 추가로 쉽게 사용)
@FeignClient(name = "github-client", url = "https://api.github.com")
public interface GitHubClient {
    
    @GetMapping("/users/{username}")
    GitHubUser getUser(@PathVariable("username") String username);
    
}

@Getter
class GitHubUser {
    private String login;
    private String name;
    private String blog;
}
```

OpenFeign은 다음과 같은 특징이 있습니다.

1. **선언적 접근**: 인터페이스를 통해 Rest API를 정의합니다.
2. **로드 밸런싱**: `Spring Cloud LoadBalancer`와 통합하여 클라이언트측 로드밸런싱 지원
3. **Fallback**: `Resilience4j`와 같은 라이브러리를 통해 장애 복구(fallback) 기능을 제공합니다.
4. **일관된 설정**: Spring의 다른 구성 요소와 통합하여 일관된 설정 관리가 가능합니다.
</aside>

## OpenFeign 설정(타임아웃, 재시도, 로깅)

<aside>
✍️ **NOTE**

> `*OpenFeign`의 설정은 `yaml`과 `Java config`로 할 수 있습니다.*
> 

```yaml
spring:
  cloud:
    openfeign:
      enabled: true  # OpenFeign 기능 활성화

feign:
  client:
    config:
      default:
        connectTimeout: 1000    # 기본 클라이언트의 연결 타임아웃 (밀리초 단위)
        readTimeout: 3000      # 기본 클라이언트의 읽기 타임아웃 (밀리초 단위)
        loggerLevel: FULL       # 기본 클라이언트의 로깅 레벨 설정
        
      # 클라이언트별 설정도 가능
      githubClient:
        connectTimeout: 1000    # GitHub 클라이언트의 연결 타임아웃 (밀리초 단위)
        readTimeout: 3000       # GitHub 클라이언트의 읽기 타임아웃 (밀리초 단위)
        loggerLevel: FULL       # GitHub 클라이언트의 로깅 레벨 설정

logging:
  level:
    com.example: DEBUG         # 예시 패키지의 로그 레벨
    feign:
      Logger: FULL             # Feign 로거의 전역 로깅 레벨 설정

```

```java
@Configuration // 생략가능
public class FeignConfig {

    @Bean
    public Request.Options requestOptions() {
        // Connection timeout: 1000ms, Read timeout: 3000ms
        return new Request.Options(1000, 3000);
    }

    @Bean
    public Retryer retryer() {
        // Period: 1000ms, Max period: 1000ms, Max attempts: 3
        return new Retryer.Default(1000, 1000, 1);
    }

    @Bean
    Logger.Level feignLoggerLevel() {
        // Set the log level to FULL for detailed logging
        return Logger.Level.FULL;
    }
}
```

### 타임아웃

```yaml
feign:
  client:
    config:
      default:
        connectTimeout: 5000    # 기본 클라이언트의 연결 타임아웃 (밀리초 단위)
        readTimeout: 10000      # 기본 클라이언트의 읽기 타임아웃 (밀리초 단위)
      githubClient:
        connectTimeout: 3000    # GitHub 클라이언트의 연결 타임아웃 (밀리초 단위)
        readTimeout: 6000       # GitHub 클라이언트의 읽기 타임아웃 (밀리초 단위)
```

```java
@Configuration
public class FeignConfig {

    @Bean
    public Request.Options requestOptions() {
		    // Connection timeout: 5000ms, Read timeout: 10000ms
        return new Request.Options(5000, 10000);
    }
}
```

### 재시도 설정

```java
@Configuration
public class FeignConfig {

    @Bean
    public Retryer retryer() {
        return new Retryer.Default(1000, 2000, 3); // Period: 1000ms, Max period: 2000ms, Max attempts: 3
    }
}
```

### 로그 설정

```yaml
logging:
  level:
    com.example: DEBUG # 예시 패키지의 로그 레벨
    feign:
      Logger: FULL     # Feign 로거의 로그 레벨을 FULL로 설정
```

```java
@Configuration
public class FeignConfig {

    @Bean
    Logger.Level feignLoggerLevel() {
		    // Set the log level to FULL for detailed logging
        return Logger.Level.FULL;
    }
}
```

- Logger의 이름은 전체 인터페이스 이름이며, 4가지 로그 레벨수준을 제공한다.
    - `NONE`: 로깅하지 않음
    - `BASIC`: 요청 메소드와 URI와 응답 상태와 실행시간만 로깅한다.
    - `HEADERS`: 요청과 응답 헤더와 함께 기본 정보들을 남긴다.
    - `FULL`: 요청과 응답에 대한 헤더와 바디, 메타데이터를 남긴다.
</aside>