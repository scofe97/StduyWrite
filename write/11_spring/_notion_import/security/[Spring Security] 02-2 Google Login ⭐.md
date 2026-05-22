# [Spring Security] 02-2. Google Login ⭐

주제: Spring Security

- 참고
    
    [[Spring Security] 5. OAuth2 Google Login ①](https://velog.io/@kyu9610/Spring-Security-5.-OAuth2Google-Login)
    
    [[Spring Security] 6. OAuth2 Google Login ②](https://velog.io/@kyu9610/Spring-Security-6.-OAuth2-Google-Login)
    
    [[Spring Security] OAuth 구글 로그인하기](https://lotuus.tistory.com/79)
    
    구글 클라우드 플랫폼 과정설명
    
    [](https://velog.io/@jyleedev/AuthenticationPrincipal-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%A0%95%EB%B3%B4-%EB%B0%9B%EC%95%84%EC%98%A4%EA%B8%B0)
    
    [[Spring Security] 스프링 시큐리티로 OAuth 로그인 구현하기](https://blogshine.tistory.com/400)
    

# **Google Login 설정!**

---

<aside>
💡 **NOTE**

> ***구글 OAuth로그인을 위해서는 먼저 구글 클라우드 플랫폼에 가서 설정을 해주어야 한다!***
> 
</aside>

## 구글 클라우드 플랫폼

<aside>
✍️ **NOTE**

[Google 클라우드 플랫폼](https://console.cloud.google.com/apis/dashboard?hl=ko&project=principal-rope-376914&supportedpurview=project)

- 자세한 과정은 참고링크에 걸어두었으니, 핵심만 소개한다.

### 승인된 리디렉션

![Untitled](%5BSpring%20Security%5D%2002-2%20Google%20Login%20%E2%AD%90/Untitled.png)

- 승인된 리디렉션 URI에 "**http://**localhost:8080**/login/oauth2/code/google**"을 입력한다.
- 밑줄친 부분은 정해진 내용이라 바꾸면 안된다! ([공식문서](https://docs.spring.io/spring-security/reference/servlet/oauth2/login/core.html) 참조)

### 클라이언트 ID, 클라이언트 비밀번호

![잘 기억해두자 나중에 쓴다.](%5BSpring%20Security%5D%2002-2%20Google%20Login%20%E2%AD%90/Untitled%201.png)

잘 기억해두자 나중에 쓴다.

</aside>

## **OAuth2 설정**

<aside>
✍️ **NOTE**

### build.gradle > dependency 추가

```java
implementation 'org.springframework.boot:spring-boot-starter-oauth2-client:2.6.2'
```

### yaml 추가

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: 30818697785-7oraok4rh34lkjuig9deo0tcttcsi6vv.apps.googleusercontent.com
            client-secret: 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
            scope:
            - email
            - profile
```

- client-id와 client-secret값에 구글 클라우드 플랫폼에서 얻어왔던 정보를 입력한다!

### SecurityConfig 수정

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    // ...

    http.oauth2Login()
            .loginPage("/loginForm")		// 인증이 필요한 URL에 접근하면 /loginForm으로 이동
            .defaultSuccessUrl("/")			// 로그인 성공하면 "/" 으로 이동
            .failureUrl("/loginForm")		// 로그인 실패 시 /loginForm으로 이동
            .userInfoEndpoint()			// 로그인 성공 후 사용자정보를 가져온다
            .userService(principalOauth2UserService);	//사용자정보를 처리할 때 사용한다
    return http.build();
}
```

| `.oauth2Login()` | OAuth2기반으로 로그인 할 경우의 설정을 추가할 수 있다.OAuth2LoginConfigurer를 불러온다 |
| --- | --- |
| `.loginPage(String url)` | 로그인 페이지 경로를 호출한다. |
| `.defaultSuccessUrl(String url)` | 로그인 성공 시 url로 이동한다. |
| `.failureUrl(String url)` | 로그인 실패 시 url로 이동한다. |
| `.userInfoEndpoint()` | 로그인 성공 후 사용자 정보를 가져온다 |
| `.userService(Class)` | userInfoEndpoint()로 가져온 사용자 정보를 처리할 때 사용g한다. |
</aside>

# **Google Login 후처리**

---

<aside>
💡 **NOTE**

> ***구글 로그인이 정상적으로 처리가되면 다음의 과정을 진행해야 한다.***
> 
1. **코드받기(인증)**
    - 구글에 정상적으로 로그인했다고 인증이 되었다.
2. **엑세스 토근받기**
    - 사용자 정보에 접근할 권한이 생긴다.
3. **사용자 프로필 정보 가져오기**
4. **정보를 통해서 회원가입**
    - 추가정보가 필요할 시에는 받아야 한다.
</aside>

## **PrincipalDetails**

<aside>
✍️ **NOTE**

> ***일반 로그인 사용자(폼 로그인)**와 **OAuth2 로그인** 사용자 모두 `Principal`를 객체로 받기 위해서 `UserDetails`와 `OAuth2User` 둘다 구현받고 생성자를 추가한다!*
> 

![원래는 UserDetails와 OAuth2User의 타입이 달라서 명시해주기 어려웠다.](%5BSpring%20Security%5D%2002-2%20Google%20Login%20%E2%AD%90/Untitled%202.png)

원래는 UserDetails와 OAuth2User의 타입이 달라서 명시해주기 어려웠다.

### Authentication

![인증에 성공한 유저는 Authentication 객체를 만들어 정보를 채운다.](%5BSpring%20Security%5D%2002-2%20Google%20Login%20%E2%AD%90/Untitled%203.png)

인증에 성공한 유저는 Authentication 객체를 만들어 정보를 채운다.

### **@AuthenticationPrincipal**

- 세션 정보 UserDetails에 접근할 수 있는 어노테이션
- **전체코드**
    
    ```java
    @Data
    public class PrincipalDetails implements UserDetails, OAuth2User {
    
        private User user;
        private Map<String, Object> attributes;
    
        // 일반 시큐리티 로그인시 사용
        public PrincipalDetails(User user) {
            this.user = user;
        }
    
        // OAuth2.0 로그인시 사용
        public PrincipalDetails(User user, Map<String, Object> attributes) {
            this.user = user;
            this.attributes = attributes;
        }
    
        // 해당 User의 권한을 리턴하는 곳
        @Override
        public Collection<? extends GrantedAuthority> getAuthorities() {
            Collection<GrantedAuthority> collect = new ArrayList<>();
            collect.add(() -> {
                return user.getRole();
            });
            return collect;
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
            // 우리 사이트 1년동안 로그인안하면 휴먼계정으로 변한다
            // 로그인한 날짜가 마지막 로그인 시간 1년초과하면 false
    
            return true;
        }
    
        @Override
        public Map<String, Object> getAttributes() {
            return attributes;
        }
    
        @Override
        public String getName() {
            return null;
        }
    }
    ```
    
</aside>

## **OAuth2UserService**

<aside>
✍️ **NOTE**

> `*DefaultOAuthUserService`는 OAuth2로그인 시 `loadUserByUsername`메서드로 로그인한 **유저가 DB에 저장되어있는지를 찾는다!***
> 
- **OAuth2**로 로그인하는 사용자는 회원가입을 거치지 않기 때문에, DB에 유저가 없다면 자동으로 회원가입 처리해준다!
- 유저가 있다면 `Authentication`(**OAuth2**를 구현한 PrincipalDetails)를 반환하여 `SecurityContextHolder`에 저장할 수 있게 한다.
- **전체코드**
    
    ```java
    @Service
    @RequiredArgsConstructor
    public class PrincipalOauth2UserService extends DefaultOAuth2UserService {
    
        private final UserRepository userRepository;
    
        // 구글로 부터 받은 userRequest 데이터에 대한 후처리되는 함수
        // 함수 종료시 @AuthenticationPrincipal 어노테이션이 만들어진다.
        @Override
        public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
            // 구글로 부터 받은 userRequest 데이터에 대한 후처리가 되는 함수
            // userRequest = org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest@485cfb01
            System.out.println("userRequest = " + userRequest);
            System.out.println("userRequest.getClientRegistration = " + userRequest.getClientRegistration());
            System.out.println("userRequest.getAccessToken = " + userRequest.getAccessToken());
            System.out.println("loadUser = " + super.loadUser(userRequest).getAttributes());
    
    //                userRequest = org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest@13eded25
    //                userRequest.getClientRegistration = ClientRegistration{registrationId='google',
    //                    clientId='30818697785-7oraok4rh34lkjuig9deo0tcttcsi6vv.apps.googleusercontent.com',
    //                    clientSecret='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',
    //                    clientAuthenticationMethod=org.springframework.security.oauth2.core.ClientAuthenticationMethod@4fcef9d3,
    //                    uthorizationGrantType=org.springframework.security.oauth2.core.AuthorizationGrantType@5da5e9f3,
    //                    redirectUri='{baseUrl}/{action}/oauth2/code/{registrationId}',
    //                    scopes=[email, profile],
    //                    providerDetails=org.springframework.security.oauth2.client.registration.ClientRegistration$ProviderDetails@3d18c3e0,
    //                    clientName='Google'}
    //                userRequest.getAccessToken = org.springframework.security.oauth2.core.OAuth2AccessToken@378b1437
    //                loadUser = {sub=114477815481377286595,
    //                    name=심보현[부울경_2반_E205]팀원,
    //                    given_name=심보현[부울경_2반_E205]팀원,
    //                    picture=https://lh3.googleusercontent.com/a/AEdFTp7sA6LZmEpbsfNlnMc4Y-2tIZz19V-n4oEog3aQ=s96-c,
    //                    email=tscofet@gmail.com,
    //                    email_verified=true,
    //                    locale=ko}
    
            // username = google_sub
            // password = 암호화
            // email = email
            // role = ROLE_USER
            // provider = google
            // providerId = sub
    
            OAuth2User oAuth2User = super.loadUser(userRequest);
            // 구글 로긍니 버튼 클릭 -> 구글 로그인 창 -> 로그인을 완료 -> code를 리턴(Oauth-CLient라이브러리) -> AccessToken 요청
            // userRequest 정보 -> 회원프로필 받아야함(loadUser 함수) -> 구글로부터 회원 프로필 받아준다.
    
            String provider = userRequest.getClientRegistration().getClientId();// google
            String providerId = oAuth2User.getAttribute("sub");
            String username = provider + "_" + providerId;
            String password = "겟인데어";
            String email = oAuth2User.getAttribute("email");
            String role = "ROLE_USER";
    
            User userEntity = userRepository.findByUsername(username);
    
            if (userEntity == null) {
                // 유저가 없으므로 강제로 회원가입 시킴
                userEntity = User.builder()
                        .username(username)
                        .password(password)
                        .email(email)
                        .role(role)
                        .provider(provider)
                        .providerId(providerId)
                        .build();
                userRepository.save(userEntity);
            }else{
                System.out.println("이미 로그인한적이 있습니다!");
            }
    
            // 정보를 토대로 강제로 회원가입 진행하기
            return new PrincipalDetails(userEntity, oAuth2User.getAttributes());
        }
    }
    ```
    

### 참고

```java
//인증서버(구글)의 정보를 가져온다
userRequest.getClientRegistration();
	결과 : ClientRegistration{
              registrationId='google', 
              clientId='~', 
              clientSecret='~', 
              clientAuthenticationMethod=org.springframework.security.oauth2.core.ClientAuthenticationMethod@4fcef9d3, 
              authorizationGrantType=org.springframework.security.oauth2.core.AuthorizationGrantType@5da5e9f3, 
              redirectUri='{baseUrl}/{action}/oauth2/code/{registrationId}', 
              scopes=[profile, email], 
              providerDetails=org.springframework.security.oauth2.client.registration.ClientRegistration$ProviderDetails@5b8ec6e5, 
              clientName='Google'
          }

//인증 토큰값을 가져온다
userRequest.getAccessToken().getTokenValue();
	결과 : Tokenvalue~~

//유저의 정보를 가져온다
super.loadUser(userRequest).getAttributes();
	결과 : {
              sub=~(PK 같은거), 
              name=~, 
              given_name=~, 
              family_name=~, 
              picture=~, 
              email=~, 
              email_verified=true, 
              locale=ko
          }
```

</aside>