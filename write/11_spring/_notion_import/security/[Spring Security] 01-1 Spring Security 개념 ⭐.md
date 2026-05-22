# [Spring Security] 01-1. Spring Security 개념 ⭐

주제: Spring Security
연관 노트: [Spring Study] 08-2. 필터와 인터셉터 (https://www.notion.so/Spring-Study-08-2-df2108b46b1c429e83a9c668b85a925f?pvs=21)

- 참고
    
    [스프링부트 회원가입 구현하기](https://ysu96.tistory.com/8)
    
    [Spring Security의 구조(Architecture) 및 처리 과정 알아보기](https://dev-coco.tistory.com/174)
    
    각 필터가 실제로 어떻게 구현되었는가 참각 필터가 어떻게 구현되었는가 참고
    
    [스프링 시큐리티 - 아키텍처 정리](https://devwithpug.github.io/spring/spring-security-1/)
    
    아키텍쳐 참고
    
    [[Java] Spring Boot Security 이해하기 -1 : 5.7.x 버전 구조 및 파일 이해](https://adjh54.tistory.com/91)
    
    Security에서 사용되는 객체
    
    [Spring Security적용을 하려면 Security Filter의 구조를 알아야 한다](https://velog.io/@readnthink/Spring-Security적용을-하려면-Security-Filter의-구조를-알아야-한다)
    
    SecurityFilter 이론
    
    [[Spring Security] Filter란?](https://velog.io/@seongwon97/Spring-Security-Filter란)
    
    SecurityFilter 이론
    
    [스프링 시큐리티 기본 API및 Filter 이해](https://catsbi.oopy.io/c0a4f395-24b2-44e5-8eeb-275d19e2a536)
    
    SecurityFilter 이론
    
    [Spring Security, 제대로 이해하기 - FilterChain](https://gngsn.tistory.com/160)
    
    SecurityFilter 이론
    

# Spring Security

---

<aside>
💡 **NOTE**

> ***애플리케이션 내의 보안 중 사용자에 대한 ‘인증’과 ‘인가’에 대한 처리를 담당하는 프레임워크를 의미한다.***
> 
- **접근 주체(Principal)**
    - 보호된 대상에 접근하는 유저
    
- **인증(Authenticate)**
    - 현재 유저가 누구인지 확인 (ex 로그인)
    - 애플리케이션의 작업을 수행할 수 있는 주체임을 증명한다.
    
- **인가(Authorization)**
    - 현재 유저가 어떤 서비스, 페이지에 접근할 수 있는 권한이 있는지 검사한다.
    
- **권한**
    - 인증된 주체가 애플리케이션의 동작을 수행할 수 있도록 허락되었는지를 결정
    - 권한 승인이 필요한 부분으로 접근하려면 인증 과정을 통해 주체가 증명되어야 한다.
    - 권한 부여에도 두가지 영역이 존재하는데 웹 요청 권한, 메소드 호출 및 도메인 인스턴스에 대한 접근 권한 부여
</aside>

## 스프링 시큐리티 특징과 구조

<aside>
✍️ **NOTE**

> *Client (request) → **Filter** → DispatcherServlet → **Interceptor** → Controller*
> 

![인증관리자(Authentication Manager), 접근 결정 관리자(Access Decision Manager)를 통해 사용자의 리소스 접근을 제어한다.](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled.png)

인증관리자(Authentication Manager), 접근 결정 관리자(Access Decision Manager)를 통해 사용자의 리소스 접근을 제어한다.

- **인증 관리자** ⇒ `UsernamePasswordAuthenticationFilter`
- **접근 결정 관리자** ⇒ `FilterSecurityInterceptor`

- 보안과 관련하여 체계적으로 많은 옵션을 제공하여 편리하게 사용할 수 있다.
- **Filter 기반으로 동작**하여 MVC와 분리하여 동작한다.
- 어노테이션을 통한 간단한 설정
- 기본적으로 **Session & Coockie 방식**으로 인증한다.
</aside>

## ⚠️ **Spring Security 5.7.x 버전에 대한 이슈 사항**

<aside>
✍️ **NOTE**

```java
public class SecurityConfig extends WebSecurityConfigurerAdapter{}
```

- 5.6.x 버전 이하에서는 `WebSecurityConfig` 클래스에서 `WebSecurityConfiguredAdapter`를 상속받아서 사용했다
- **5.7.x 버전부터는 Deprecated되어서 사용이 안됨!**
    - 5.7.x 버전 이상부터는 컴포넌트 기반의 `Configuration`을 구성하는 것으로 권장된다.
</aside>

# Spring Security **Architecture**

---

<aside>
💡 **NOTE**

![전체적인 Spring Security 흐름도](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled%201.png)

전체적인 Spring Security 흐름도

![그냥 참고용.. 봐도 모르겠다](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled%202.png)

그냥 참고용.. 봐도 모르겠다

1. 사용자가 로그인 정보와 함께 인증 요청을 한다 - **Http Request**
2. **AuthenticationFilter**가 요청을 가로채고, 가로챈 정보를 통해 **UsernamePasswordAuthenticationToken**의 인증용 객체를 생성한다.
3. **AuthenticationManager**의 구현체인 **ProviderManager**에게 생성한 **UsernamePasswordToken** 객체를 전달한다.
4. **AuthenticationManager**는 등록된 **AuthenticationProvider**(들)을 조회하여 인증을 요구한다.
5. 실제 DB에서 사용자 인증정보를 가져오는 **UserDetailService**에 사용자 정보를 넘겨준다.
6. 넘겨받은 사용자 정보를 통해 DB에서 찾은 정보인 **UserDetails** 객체를 만든다.
7. **AuthenticationProvier**(들)은 **UserDetails**를 넘겨받고 사용자 정보를 비교한다.
8. 인증이 완료되면 권한 등의 사용자 정보를 담긴 **Authentication** 객체를 반환한다.
9. 다시 최초의 **AuthenticationFilter**에 **Authentication** 객체가 반환된다.
10. **Authentication** 객체를 **SecurityContext**에 저장한다.
    - 사용자 정보를 저장한다는건 Session-Cookie 방식을 사용한다는걸 의미한다.
</aside>

# **Security Filter**

---

<aside>
💡 **NOTE**

> *Clinet -> FilterChain -> **DelegatingFilterProxy (위임처리)** -> **FilterChainProxy** -> **Security Filter(시큐리티 필터 적용!)***
> 

![ServletContainer → SpringContainer, Filter → Dispatcher Servlet](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled%203.png)

ServletContainer → SpringContainer, Filter → Dispatcher Servlet

- Spring Container와 Was 서버간에 Request 요청이 연결되어야 하는데 이를 수행하는 **Filter가 DelegationFilterProxy다.**
- **DelegatingFilterProxy**의 내부에 **FilterChainProxy**라는 위임대상을 가지고 있다.
    - FilterChainProxy는 SpringSecurity에서 제공되는 특수 필터다.
    - **SecurityFilterChain**이라는 이름을 가진 Bean을 호출하여 **SecurityFilter** 역할을 수행한다.
</aside>

## **SecurityFilterChain**

<aside>
✍️ **NOTE**

> ***SecurityFilterChain은 List의 형태로 구성되며, 이 리스트를 AuthenticationFilter라 부른다!***
> 

![SecurityFilterChain 의 수많은 Filter (그냥 개념만 알면된다..)](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled%204.png)

SecurityFilterChain 의 수많은 Filter (그냥 개념만 알면된다..)

![가로버전](%5BSpring%20Security%5D%2001-1%20Spring%20Security%20%EA%B0%9C%EB%85%90%20%E2%AD%90/Untitled%205.png)

가로버전

</aside>