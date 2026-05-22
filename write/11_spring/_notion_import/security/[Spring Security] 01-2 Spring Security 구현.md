# [Spring Security] 01-2. Spring Security 구현

주제: Spring Security

- 참고
    
    [Spring Security, 제대로 이해하기 - FilterChain](https://gngsn.tistory.com/160)
    
    필터 동작들
    
    [[Spring Boot + Security] SecurityConfig 설정 (Feat. gradle)](https://chlee21.tistory.com/190)
    
    SecurityConfig
    
    [Spring Security, 어렵지 않게 설정하기](https://gngsn.tistory.com/155)
    
    SecurityConfig
    
    [Spring Security Without WebSecurityConfigurerAdapter - JavaTechOnline](https://javatechonline.com/spring-security-without-websecurityconfigureradapter/#Example1_With_WebSecurityConfigurerAdapter)
    
    SecurityConfig
    
    [[Spring Security] 스프링시큐리티 설정값들의 역할과 설정방법(2)](https://kimchanjung.github.io/programming/2020/07/02/spring-security-02/)
    
    httpSecurity 메소드
    
    [Spring Security #1 기본동작](https://jiwondev.tistory.com/244)
    

# Spring Security 환경설정

---

<aside>
💡 **NOTE**

```groovy
implementation 'org.springframework.boot:spring-boot-starter-security'
testImplementation 'org.springframework.security:spring-security-test'
```

![시큐리티 적용시 기본적으로 로그인화면이 나온다.
기본 Username/Password =? user/시스템 로그에 출력됨](%5BSpring%20Security%5D%2001-2%20Spring%20Security%20%EA%B5%AC%ED%98%84/Untitled.png)

시큐리티 적용시 기본적으로 로그인화면이 나온다.
기본 Username/Password =? user/시스템 로그에 출력됨

```yaml
spring:
  security:
    user:
      name: user
      password: 1111
```

</aside>

# SecurityConfig

---

<aside>
💡 **NOTE**

> ***Spring Security의 환경설정을 구성하기 위한 클래스다!***
> 

![HttpSecurity로 대부분 구현한다고 생각하면 된다.](%5BSpring%20Security%5D%2001-2%20Spring%20Security%20%EA%B5%AC%ED%98%84/Untitled%201.png)

HttpSecurity로 대부분 구현한다고 생각하면 된다.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig{

  @Bean // 패스워드 암호화 관련 메소드
  public PasswordEncoder passwordEncoder(){
      return new BCryptPasswordEncoder();
  }

	@Bean // 시큐리티 대부분의 설정을 담당하는 메소드
	public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
			// ...
			return http.build();
	}

	// 이외에도 등록해서 사용하면 된다..
}
```

</aside>

## BCryptPasswordEncoder

<aside>
✍️ **NOTE**

> ***BCrype 인코딩**을 통하여 비밀번호에 대한 암호화를 수행한다.*
> 

![password를 암호화해줌](%5BSpring%20Security%5D%2001-2%20Spring%20Security%20%EA%B5%AC%ED%98%84/Untitled%202.png)

password를 암호화해줌

```java
@Bean // 패스워드 암호화 관련 메소드
public PasswordEncoder passwordEncoder(){
    return new BCryptPasswordEncoder();
}
```

</aside>

## **HttpSecurity**

<aside>
✍️ **NOTE**

> ***스프링시큐리티의 각종 설정은 HttpSecurity로 대부분 하게 된다!***
> 

[Spring Boot 3.1(Spring 6.1) Security Config: 'csrf()' is deprecated and marked for removal](https://velog.io/@letsdev/Spring-Boot-3.1Spring-6.1-Security-Config-csrf-is-deprecated-and-marked-for-removal)

스프링 부트 버전이 올라가면서 작성방식에 차이가 생김

[Spring boot 3.0.6, Spring security 6, jwt적용 및 인증, 예외 처리](https://velog.io/@joypeb/Spring-boot-3.0.6-Spring-security-6-jwt적용-및-인증-예외-처리)

버전이 올라가면서 동작방식이 달라짐

</aside>

## **HttpSecurity -** csrf, 강제, session 적용

<aside>
✍️ **NOTE**

```java
// CORS 처리
http.cors().configuration(configurationSource)

// CSRF 사용
http.csrf(AbstractHttpConfigurer::disable)

// session 사용하지 않으므로 무상태설정
http.sessionManagement(sessionManagement -> sessionManagement
		.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
```

```java
@Configuration
public class CorsConfig {

    @Bean
    public CorsFilter corsFilter() {
				// CORS 설정을 위한 UrlBasedCorsConfigurationSource 객체 생성
				// URL 패턴에따라 CORS 관리를 가능하게 해줌
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();

				// 새로운 CORS 설정을 만들기 위한 CorsConfiguration 객체 생성
        CorsConfiguration config = new CorsConfiguration();

				// 인증 정보 (예: 쿠키, HTTP 인증)를 요청에 포함할지 여부 설정
        config.setAllowCredentials(true);

				// 모든 출처(origin)에서의 요청을 허용하도록 설정 (향후 프론트만)
        config.addAllowedOriginPattern("*");

				// 모든 HTTP 헤더를 요청에 포함할 수 있도록 허용
        config.addAllowedHeader("*");

				// 모든 HTTP 메소드 (GET, POST 등)를 요청에 허용
        config.addAllowedMethod("*");

				// 모든 경로에 대해 이 CORS 설정을 등록
        source.registerCorsConfiguration("/**", config);

        return new CorsFilter(source);
    }
}
```

</aside>

## **HttpSecurity -** 리소스(URL) 접근 권한 설정

<aside>
✍️ **NOTE**

> ***특정 리소스의 접근 허용 또는 특정 권한을 가진 사용자만 접근을 가능하게 할 수 있습니다.***
> 

```java
http.authorizeHttpRequests(authorizeRequest -> authorizeRequest
		// 해당 경로는 모든 권한을 허용한다.
    .requestMatchers(HttpMethod.GET, "/login**", "/web-resources/**", "/actuator/**").permitAll()

		// 해당 경로는 어드민 권한이 있어야한다.
    .requestMatchers(HttpMethod.GET, "/admin/**").hasAnyRole("ADMIN")

		// 해당 경로는 유저 권한이 있어야 한다.
    .requestMatchers(HttpMethod.GET, "/order/**").hasAnyRole("USER")

		// 나머지는 모두 권한이 필요하다.
    .anyRequest().authenticated()
```

- **requestMatchers**
    - 특정 리소스에 대해서 권한을 설정한다.
- **permitAll**
    - 리소스의 접근을 인증절차 없이 허용한다.
- **authenticated**
    - 리소스의 접근을 인증절차를 통해 허용한다.
- **hasAnyRole**
    - 해당 권한을 가진 사용자만 접근을 허용한다.
- **anyRequest**
    - 모든 리소스를 의미하며, anyMatcher로 설정하지 않은 리소스를 말한다.
</aside>

## **HttpSecurity - 로그인처리 설정**

<aside>
✍️ **NOTE**

> ***로그인 FORM 페이지를 이용하여 로그인하는 방식을 사용하려고 할때 여러가지 설정을 할 수 있습니다.***
> 

```java
// Form 로그인을 활용하는경우 (JWT에는 필요없음)
.formLogin(formLogin -> formLogin
        .loginPage("/login")
        .loginProcessingUrl("/loginProc")
        .usernameParameter("userId")
        .passwordParameter("userPw")
        .permitAll())
```

</aside>

## **HttpSecurity -** 커스텀 필드 등록 ⭐

<aside>
✍️ **NOTE**

> ***커스텀 필터를 생성해서 등록할 수 있다!***
> 

```java
.addFilterBefore(jwtAuthenticationFilter, 
	UsernamePasswordAuthenticationFilter.class)
```

```java
@Order(0)
@RequiredArgsConstructor
@Component
@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final TokenProvider tokenProvider;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        String token = parseBearerToken(request);

        // 토큰값이 유요하다면 검증을 시작한다.
        if (token != null && tokenProvider.validToken(token)) {
            // 토큰 검증
            Authentication authentication = tokenProvider.getAuthentication(token);

            // SecurityContextHolder => 인증정보를 담는다.
            SecurityContextHolder.getContext().setAuthentication(authentication);
            log.info("Security Context에 {} 인증 정보를 저장했다", authentication.getPrincipal());
        } else {
            log.info("유효한 JWT 토큰이 없습니다, uri: {}", request.getRequestURI());
        }

        filterChain.doFilter(request, response);
    }

    /**
     * Authorization Bearer 제거(공백포함 7글자)
     * @param request 요청 request
     * @return token (없는경우 null)
     */
    private String parseBearerToken(HttpServletRequest request) {
        return Optional.ofNullable(request.getHeader(HttpHeaders.AUTHORIZATION))
                .filter(token -> token.length() >= 7 && token.substring(0, 7).equalsIgnoreCase("Bearer "))
                .map(token -> token.substring(7))
                .orElse(null);
    }
}
```

- **addFilterBefore**
    - 지정된 필터 앞에 커스텀 필터를 추가한다.
- **addFilterAfter**
    - 지정된 필터 뒤에 커스텀 필터를 추가한다.
- **addFilterAt**
    - 지정된 필터의 순서에 커스텀 필터가 추가된다.
</aside>