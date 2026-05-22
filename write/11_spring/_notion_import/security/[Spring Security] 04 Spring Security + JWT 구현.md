# [Spring Security] 04. Spring Security + JWT 구현

주제: Spring Security

- 참고
    
    [Spring Security + JWT 을 구현해보자!](https://velog.io/@limsubin/Spring-Security-JWT-을-구현해보자)
    
    [[Spring Security] Spring Security와 JWT를 사용하여 사용자 인증 구현하기(Spring Boot 3.0.0 이상)](https://colabear754.tistory.com/171)
    
    [[Spring Security] 내부 구조 살펴보기 (1) - 사용자를 기술하는 UserDetails](https://velog.io/@platinouss/Spring-Security-사용자를-기술하는-UserDetails)
    
    [[Spring Security] 내부 구조 살펴보기 (2) - Authentication의 Filter, Manager, Provider](https://velog.io/@platinouss/Spring-Security-Authentication의-Filter-Manager-Provider)
    
    [[Spring Security] 기본 API 및 Filter 이해(1)](https://gong-story.tistory.com/34)
    

# Spring Security + JWT

---

<aside>
💡 **NOTE**

> ***JWT를 구현하기 위해선 어떤것이 필요한가?***
> 

```groovy
implementation "io.jsonwebtoken:jjwt-api:0.11.5"
runtimeOnly "io.jsonwebtoken:jjwt-impl:0.11.5"
runtimeOnly "io.jsonwebtoken:jjwt-jackson:0.11.5"
```

</aside>

## Security에서 JWT 적용흐름

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled.png)

![Autentication 객체를 만든 뒤, AuthenticationManager에게 인증역할을 위힘한다!](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled%201.png)

Autentication 객체를 만든 뒤, AuthenticationManager에게 인증역할을 위힘한다!

- JWT 토큰이 유효하다면, Security하다는 인증정차를 검증해줄 수 있는 커스텀 Filter를 만든다!
- 해당 Filter를 **UsernamePasswordAuthenticationFilter** 앞에서 해당 요청에 대한 인증책임 절차를 진행시킨다!

### UsernamePasswordAuthenticationFilter

- **ID/Password**를 사용하는 Form기반 유저 인증을 처리하는 역할
- **Authentication(인증 객쳬)**를 만들어서 ID/PW를 저장하고, **AuthenticationManager**에게 인증처리를 맡긴다.
- 최종적으로 인증객체를 **SecurityContext**에 저장한다.
</aside>

## JWT Token 생성

<aside>
✍️ **NOTE**

![JWT 토큰의 3가지요소](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled%202.png)

JWT 토큰의 3가지요소

```java
// Jwt에 사용되는 key, 만료시간
private final String secretKey;
private final long tokenValidityInSeconds;

public String generateToken(User user) {
    Date now = new Date();
    return Jwts.builder()
						// header 등록
            .setHeader(createHeader())

						// payload - clain 등록
            .setClaims(createClaims(user))
						// payload - iat(생성시간) 등록
            .setIssuedAt(now)
						// payload -> exp(만료시간) 등록
            .setExpiration(new Date(now.getTime()+ Duration.ofHours(3).toMillis()))

						// 해싱 알고리즘과 시크릿키 등록
            .signWith(SignatureAlgorithm.HS256, jwtProperties.getSecret())
            .compact();
}

// Header
private Map<String, Object> createHeader() {
        Map<String, Object> header = new HashMap<>();
        header.put("typ", "JWT");
        header.put("alg", "HS256"); // 해시 256 암호화
        return header;
  }

// Payload
private Map<String, Object> createClaims(Member member) {
    Map<String, Object> claims = new HashMap<>();
    claims.put("id", member.getMemberId());
    claims.put("email", member.getEmail());
    claims.put("name", member.getMemberName());
    return claims;
}
```

</aside>

## JWT Token 검증

<aside>
✍️ **NOTE**

```java
public boolean validToken(String token) {
    try {
        Jwts.parserBuilder()
                .setSigningKey(secretKey.getBytes())
                .build()
                .parseClaimsJws(token);
        return true;

    } catch (io.jsonwebtoken.security.SecurityException | MalformedJwtException e) {
        // 유효하지 않은 구성의 JWT 토큰
        log.info("잘못된 JW 서명이다.");
    } catch (ExpiredJwtException e) {
        // 만료된 JWT 토큰
        log.info("만료된 JWT 토큰이다.");
    } catch (UnsupportedJwtException e) {
        // 지원되지 않은 형식이거나 구성의 JWT
        log.info("지원되지 않는 JWT 토큰이다.");
    } catch (IllegalArgumentException e) {
        // 잘못된 JWT
        log.info("JWT 토큰이 잘못되었다.");
    }

    return false;
}
```

</aside>

## JWT 토큰 → Authentication 변환

<aside>
✍️ **NOTE**

[Spring boot 3.0.6, Spring security 6, jwt적용 및 인증, 예외 처리](https://velog.io/@joypeb/Spring-boot-3.0.6-Spring-security-6-jwt적용-및-인증-예외-처리)

버전이 올라가면서 특이한게 config에서 인증이 필요한 리소스를 설정해도 
필터는 모든 동작에대해 동작한다.(JWT 인증이 필요없어도 동작을한다)

```java
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final TokenProvider tokenProvider;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        String token = parseBearerToken(request);

        // 토큰값이 유요하다면 검증을 시작한다.
        if (token != null && tokenProvider.validToken(token)) {

            // 토큰 검증 (인증객체 생성)
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

```java
public Authentication getAuthentication(String token) {
    Claims claims = Jwts.parserBuilder()
            .setSigningKey(secretKey.getBytes())
            .build()
            .parseClaimsJws(token)
            .getBody();

    // Authentication(인증) 구현체, (사용자 -, 비밀번호, 권한)
    return new UsernamePasswordAuthenticationToken(Member.from(claims), token, List.of(new SimpleGrantedAuthority("USER")));
}
```

</aside>

## JWT 토큰을 사용한 사용자인

<aside>
✍️ **NOTE**

```java
@DeleteMapping("/{postId}")
public ResponseEntity<?> postRemove(@AuthenticationPrincipal Member member, @PathVariable("postId") Long postId) {}
```

```java
public Authentication getAuthentication(String token) {
    Claims claims = Jwts.parserBuilder()
            .setSigningKey(secretKey.getBytes())
            .build()
            .parseClaimsJws(token)
            .getBody();

    // Authentication(인증) 구현체, (사용자 -, 비밀번호, 권한)
    return new UsernamePasswordAuthenticationToken(Member.from(claims), token, List.of(new SimpleGrantedAuthority("USER")));
}
```

</aside>

# Spring Security + JWT (방법2)

---

<aside>
💡 **NOTE**

> ***JWT를 구현하기 위해선 어떤것이 필요한가?***
> 

```groovy
// https://mvnrepository.com/artifact/com.auth0/java-jwt
implementation group: 'com.auth0', name: 'java-jwt', version: '4.2.1'
```

```java
/*
 * SECRET 노출되면 안된다. (클라우드AWS - 환경변수, 파일에 있는 것을 읽을 수도 있고!!)
 * 리플래시 토큰 (X)
 */
public interface JwtVO {
    public static final String SECRET = "메타코딩"; // HS256 (대칭키)
    public static final int EXPIRATION_TIME = 1000 * 60 * 60 * 24 * 7; // 일주일
    public static final String TOKEN_PREFIX = "Bearer ";
    public static final String HEADER = "Authorization";
}
```

</aside>

## JWT Token 생성

<aside>
✍️ **NOTE**

![인증로직 → UserDetailService (DB의 유저 정보 획득) → User의 정보확인 → 결과를 AuthenticationFilter에 전달 , 세부정보가 Context에 저장.](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled%203.png)

인증로직 → UserDetailService (DB의 유저 정보 획득) → User의 정보확인 → 결과를 AuthenticationFilter에 전달 , 세부정보가 Context에 저장.

![JWT 토큰의 3가지요소](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled%202.png)

JWT 토큰의 3가지요소

```java
@Getter
@RequiredArgsConstructor
public class LoginUser implements UserDetails {

    private final User user;

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
				// 권한추가
        Collection<GrantedAuthority> authorities = new ArrayList<>();
        authorities.add(() -> "ROLE_" + user.getRole());
        return authorities;
    }

    @Override
    public String getPassword() {
        return user.getPassword();
    }

    @Override
    public String getUsername() {
        return user.getUsername();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
```

```java
@Service
public class LoginService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    // 시큐리티로 로그인이 될때, 시큐리티가 loadUserByUsername() 실행해서 username을 체크!!
    // 없으면 오류, 있으면 정상적으로 시큐리티 컨텍스트 내부 세션에 로그인된 세션이 만들어진다.
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {

        User userPS = userRepository.findByUsername(username).orElseThrow(
                () -> new InternalAuthenticationServiceException("인증 실패"));
        return new LoginUser(userPS);
    }

}
```

```java
@Slf4j
public class JwtProcess {

    // 토큰 생성
    public static String create(LoginUser loginUser) {
        String jwtToken = JWT.create()
                .withSubject("bank")
                .withExpiresAt(new Date(System.currentTimeMillis() + JwtVO.EXPIRATION_TIME))
                .withClaim("id", loginUser.getUser().getId())
                .withClaim("role", loginUser.getUser().getRole() + "")
                .sign(Algorithm.HMAC512(JwtVO.SECRET));
        return JwtVO.TOKEN_PREFIX + jwtToken;
    }

    // 토큰 검증 
		// return 되는 LoginUser 객체를 강제로 시큐리티 세션에 직접 주입할 예정
    public static LoginUser verify(String token) {
				// 시크릿 복호화
        DecodedJWT decodedJWT = JWT.require(Algorithm.HMAC512(JwtVO.SECRET))
					.build()
					.verify(token);

        Long id = decodedJWT.getClaim("id").asLong();
        String role = decodedJWT.getClaim("role").asString();
        User user = User.builder()
						.id(id)
						.role(UserEnum.valueOf(role))
						.build();
        LoginUser loginUser = new LoginUser(user);

        return loginUser;
    }
}
```

</aside>

## JWT 토큰필터 생성

<aside>
✍️ **NOTE**

![UsernamePasswordAuthenticationFilter  흐름도](%5BSpring%20Security%5D%2004%20Spring%20Security%20+%20JWT%20%EA%B5%AC%ED%98%84/Untitled%204.png)

UsernamePasswordAuthenticationFilter  흐름도

```java
public class JwtAuthenticationFilter extends UsernamePasswordAuthenticationFilter {

    private final Logger log = LoggerFactory.getLogger(getClass());
    private AuthenticationManager authenticationManager;

		// 인증 관리자를 설정하고, 로그인 처리 URL을 설정
    public JwtAuthenticationFilter(AuthenticationManager authenticationManager) {
        super(authenticationManager);

        setFilterProcessesUrl("/api/login");
        this.authenticationManager = authenticationManager;
    }

    // 로그인 시도를 처리한다.
		// 사용자가 제공한 로그인 정보 DTO를 받아, UsernamePasswordAuthenticationToken 생성
		// 이를 AuthenticationManager에 전달하여 인증시도
    @Override
    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response)
            throws AuthenticationException {
        log.debug("디버그 : attemptAuthentication 호출됨");
        try {
            ObjectMapper om = new ObjectMapper();
            LoginReqDto loginReqDto = om.readValue(request.getInputStream(), LoginReqDto.class);

            // 강제 로그인
            UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(
                    loginReqDto.getUsername(), loginReqDto.getPassword());

            // UserDetailsService의 loadUserByUsername 호출하며 인증과정 시작
            // JWT를 쓴다 하더라도, 컨트롤러 진입을 하면 시큐리티의 권한체크, 인증체크의 도움을 받을 수 있게 세션을 만든다.
            // 이 세션의 유효기간은 request하고, response하면 끝!!
            Authentication authentication = authenticationManager.authenticate(authenticationToken);

            return authentication;
        } catch (Exception e) {
						// InternalAuthenticationServiceException -> config에서 설정한 예외를 호출한다.
            // unsuccessfulAuthentication 호출함
            throw new InternalAuthenticationServiceException(e.getMessage());
        }
    }

    // 로그인 실패 (attemptAuthentication 실패)
    @Override
    protected void unsuccessfulAuthentication(HttpServletRequest request, HttpServletResponse response,
            AuthenticationException failed) throws IOException, ServletException {
        CustomResponseUtil.fail(response, "로그인실패", HttpStatus.UNAUTHORIZED);
    }

		// 로그인 성공 (attemptAuthentication 성공)
    @Override
    protected void successfulAuthentication(HttpServletRequest request, HttpServletResponse response, FilterChain chain,
            Authentication authResult) throws IOException, ServletException {
        log.debug("디버그 : successfulAuthentication 호출됨");

				// 인증 정보를 토대로 JWT토큰 생성하고 반환
        LoginUser loginUser = (LoginUser) authResult.getPrincipal();
        String jwtToken = JwtProcess.create(loginUser);
        response.addHeader(JwtVO.HEADER, jwtToken);

        LoginRespDto loginRespDto = new LoginRespDto(loginUser.getUser());
        CustomResponseUtil.success(response, loginRespDto);
    }

}
```

- `/api/login` URL을 통해 필터가 활성화된다.
- 사용자의 ID/PW를 활용해서 **UsernamePasswordAuthenticationToken**을 생성하고, 이를 **AuthenticationManager**에 전달하여 인증하고 JWT 토큰을 생성한다.

```java
/*
 * 모든 주소에서 동작함 (토큰 검증)
 */
public class JwtAuthorizationFilter extends BasicAuthenticationFilter {
    private final Logger log = LoggerFactory.getLogger(getClass());

    public JwtAuthorizationFilter(AuthenticationManager authenticationManager) {
        super(authenticationManager);
    }

    // JWT 토큰 헤더를 추가하지 않아도 해당 필터는 통과는 할 수 있지만, 결국 시큐리티단에서 세션 값 검증에 실패함.
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        if (isHeaderVerify(request, response)) {
            // 토큰이 존재함
            log.debug("디버그 : 토큰이 존재함");

            String token = request.getHeader(JwtVO.HEADER).replace(JwtVO.TOKEN_PREFIX, "");
            LoginUser loginUser = JwtProcess.verify(token);
            log.debug("디버그 : 토큰이 검증이 완료됨");

            // 임시 세션 (UserDetails 타입 or username)
            Authentication authentication = new UsernamePasswordAuthenticationToken(loginUser, null,
                    loginUser.getAuthorities()); // id, role 만 존재
            SecurityContextHolder.getContext().setAuthentication(authentication);
            log.debug("디버그 : 임시 세션이 생성됨");
        }
        chain.doFilter(request, response);
    }

    private boolean isHeaderVerify(HttpServletRequest request, HttpServletResponse response) {
        String header = request.getHeader(JwtVO.HEADER);
        if (header == null || !header.startsWith(JwtVO.TOKEN_PREFIX)) {
            return false;
        } else {
            return true;
        }
    }
}
```

- 현재 JWT토큰을 사용하므로 세션데이터가 없으므로, JWT값이 헤더에 존재하면 임시 세션을 생성해서 넣어준다.
- 임시 세션은 Spring Security의 **SecurityContextHolder**에 저장한다.
</aside>