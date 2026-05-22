# [Spring Security] 02-1. OAuth2.0 개념이해 ⭐

주제: Spring Security

- 참고
    
    [[Spring Security] 5. OAuth2 Google Login ①](https://velog.io/@kyu9610/Spring-Security-5.-OAuth2Google-Login)
    
    [OAuth 2.0 개념 총 정리](https://charming-kyu.tistory.com/36)
    
    [[Spring Security] 동작방법 및 Form, OAuth 로그인하기 (Feat.Thymeleaf 타임리프)](https://lotuus.tistory.com/78)
    
    [[OAuth2] 동작과정](https://lotuus.tistory.com/83)
    

# **OAuth2(Open Authorization 2.0, OAuth2)**

---

<aside>
💡 **NOTE**

> ***인증을 위한 개방형 표준 프로토콜이다!***
> 

![인증과정 흐름](%5BSpring%20Security%5D%2002-1%20OAuth2%200%20%EA%B0%9C%EB%85%90%EC%9D%B4%ED%95%B4%20%E2%AD%90/Untitled.png)

인증과정 흐름

- 이 프로토콜에서는 Third-Party 프로그램에게 리소스 소유자를 대신하여 **리소스 서버에서 제공하는 자원에 대한 접근 권한을 위임하는 방식**을 제공한다.
- 구글, 페이스북, 카카오, 네이버 등에서 제공하는 **간편 로그인 기능도 OAuth2 프로토콜 기반의 사용자 인증 기능을 제공**한다.
</aside>

## **역할**

<aside>
✍️ **NOTE**

### Resource Owner

- **리소스 소유자**를 의미한다.
- 본인의 정보에 접근할 수 있는 자격을 승인하는 주체이다. ex(구글 로그인을 할 사용자)
- 클라이언트를 인증(Authorizie)하는 역할을 수행하고, 인증이 완료되면, 동의를 통해 권한 획득 자격을 클라이언트에게 부여한다.

### Client

- **Resource Owner**의 리소스를 사용하조가 접근 요청을 하는 **어플리케이션**

### Resource Server

- **Resource Owner**의 정보가 저장되어 있는 서버

### Authorization Server

- 권한 서버
- **인증/인가를 수행하는 서버**로, 클라이언트의 접근 자격을 확인하고 **Access Token을 발급**하여 권한을 부여하는 역할을 수행한다.
</aside>

## **주요 용어**

<aside>
✍️ **NOTE**

### Authentitaction(인증)

- 인증, **접근 자격이 있는지 검증**하는 단계

### Authorization(인가)

- **자원에 접근할 권한을 부여**하고 리소스 접근 권한이 담긴 Access Token을 제공한다.

### Access Token

- 리소스 서버에게서 리소스 소유자의 정보를 획득할 때 사용되는 만료 기간이 있는 Token

### Refresh Token

- **Access Token** 만료시 이를 재발급 받기위한 용도로 사용하는 Token
</aside>

## 흐름

<aside>
✍️ **NOTE**

1. 아이디, 비밀번호를 가진 요청이 들어온다.
2. **Form 로그인**이면 `UserDetailService`의 `loadUserByUsername` 메서드가 실행되고,
**OAuth2 로그인**이면 `OAuth2UserService`의 `loadUserByUsername` 메서드가 실행된다.
3. `loadUserByUsername` 메서드는 **“이런 정보가 들어왔는데 혹시 회원이야?” 라고 묻는 메서드**다.
= `loadUserByUsername`에서는 회원을 찾아주는 로직을 구현!
4. 이때, 회원정보는 **Form 로그인**이면 `UserDetails`타입으로, **OAuth2 로그인**이면 `OAuth2User` 타입으로 반환해준다.
5. `UserDetails` 또는 `OAuth2User`를 반환하면 Spring에서 알아서 Session에 저장해준다.
    
    
</aside>