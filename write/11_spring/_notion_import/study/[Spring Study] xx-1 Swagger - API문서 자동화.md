# [Spring Study] xx-1. Swagger - API문서 자동화

주제: Spring Study

- 참고
    
    [[SpringBoot] Swagger 설정하기](https://velog.io/@gillog/SpringBoot-Swagger-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0)
    
    [[Spring / TIL] SpringBoot 버전 3.X.X에 Swagger적용하기](https://resilient-923.tistory.com/414)
    
    [[Spring Boot] Springdoc 라이브러리를 통한 Swagger 적용](https://colabear754.tistory.com/99)
    
    [[Spring] 스웨거(Swagger) 설정](https://sm-code.tistory.com/entry/Spring-스웨거Swagger-설정)
    
    [[Spring Boot] Swagger를 활용한 API 문서 자동화](https://gaga-kim.tistory.com/entry/Spring-Boot-Swagger%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-API-%EB%AC%B8%EC%84%9C-%EC%9E%90%EB%8F%99%ED%99%94)
    
    [Spring Boot 프로젝트(Gradle) 에서의 Swagger 3.0.0 설정 방법](https://velog.io/@kijrary/Spring-Boot-프로젝트Gradle-에서의-Swagger-3.0.0-설정-방법)
    

# Swagger란 무엇인가?

---

<aside>
💡 **NOTE**

> ***Swagger ⇒** **서버로 요청되는 URL 리스트**를 **HTML화면으로 문서화 및 테스트 할 수 있는 라이브러리**이다.*
> 

[http://144.24.171.248:8081/swagger-ui/index.html#/](http://144.24.171.248:8081/swagger-ui/index.html#/)

예시 사이트

- 간단하게 이야기하자면 **Swagger**는 API Spec 문서이다.
- API를 엑셀이나, 가이드 문서를 통해 관리하는건 주기적인 업데이트가 필요하기 떄문에 관리가 쉽지 않고 시간이 오래걸린다.
</aside>

## build.gradle 추가

<aside>
✍️ **NOTE**

```groovy
// 스프링 3.x 이상
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.0.2'

// 스프링 3.x 미만
implementation 'io.springfox:springfox-boot-starter:3.0.0'
implementation 'io.springfox:springfox-swagger-ui:3.0.0'
```

- 스프링 부트가 2.x버전이라도 왠만하면 **springdoc-openapi-ui를 사용하는걸 권장한다.**
    - springfox는 2020년 7월기준으로 업데이트를 멈추었기 때문
    - `@Configuration`을 하지 않아도 자동으로 생성된다!
</aside>

## SwaggerConfig - Annotaion

<aside>
✍️ **NOTE**

```java
@OpenAPIDefinition(
        servers = @Server(url = "https://wantedonboarding.duckdns.org/"),
        info = @Info(title = "Couple App", description = "couple app api명세", version = "v1"),
        security = @SecurityRequirement(name = "Bearer"))
@SecurityScheme(
        name = "Bearer",
        type = SecuritySchemeType.HTTP,
        scheme = "bearer",
        bearerFormat = "JWT",
        in = SecuritySchemeIn.HEADER,
        paramName = "Authorization"
)
@RequiredArgsConstructor
@Configuration
public class SwaggerConfig {

    @Bean
    public GroupedOpenApi chatOpenApi() {
        String[] paths = {"/**"};

        return GroupedOpenApi.builder()
                .group("COUPLE API v1") // 스웨거 그룹이름
                .pathsToMatch(paths) // 스웨거 적용 API 경로
                .build();
    }
}
```

- **구버전 코드**
    
    ```java
    @Configuration
    @EnableWebMvc
    public class SwaggerConfig {
    
        private ApiInfo swaggerInfo() {
            return new ApiInfoBuilder()
                    .title("SAMPLE API")
                    .description("SAMPLE API Docs")
                    .version("1.0")
                    .build();
        }
    
        @Bean
        public Docket swaggerApi() {
            return new Docket(DocumentationType.SWAGGER_2)
                    .consumes(getConsumeContentTypes())
                    .produces(getProduceContentTypes())
                    .apiInfo(swaggerInfo())
                    .select()
                    .apis(RequestHandlerSelectors.basePackage("kr.co.sample"))
                    .paths(PathSelectors.any())
                    .build()
                    .useDefaultResponseMessages(false);
        }
    
        private Set<String> getConsumeContentTypes() {
            Set<String> consumes = new HashSet<>();
            consumes.add("application/json;charset=UTF-8");
            consumes.add("application/x-www-form-urlencoded");
            return consumes;
        }
    
        private Set<String> getProduceContentTypes() {
            Set<String> produces = new HashSet<>();
            produces.add("application/json;charset=UTF-8");
            return produces;
        }
    }
    ```
    

![실제 사용가능한 Annotation 종류](%5BSpring%20Study%5D%20xx-1%20Swagger%20-%20API%EB%AC%B8%EC%84%9C%20%EC%9E%90%EB%8F%99%ED%99%94/Untitled.png)

실제 사용가능한 Annotation 종류

- **@OpenAPiDefinition**
    - server
        - API 서버의 URL 설정
    - info
        - API의 기본 정보를 설명한다.
    - security
        - API의 보안 요구 사항을 정의한다.
- **@SecurityScheme**
    - name
        - 보안 체계의 이름
    - type
        - 보안 체계의 유형(ex HTTP, OAuth2, API Key ..)
    - scheme
        - 보안 체계의 구조 (ex bearer)
    - in
        - 보안 파라미터가 어디에 위치하는가?
    - paramName
        - 보안 파라미터의 이름
</aside>

## Controller - **Annotations**

<aside>
✍️ **NOTE**

```java
@Tag(name = "회원가입/로그인 API")
@RestController
@RequestMapping("/auth")
// ...
public class AuthController {

    private final AuthService authService;

    @Operation(summary = "회원가입")
    @PostMapping("/signup")
    public ResponseEntity<?> authSignUp(@Valid @RequestBody SignUpRequest signUpRequest) {}
```

</aside>