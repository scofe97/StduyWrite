# [Spring Security] 02-4. Naver Login

주제: Spring Security

- 참고
    
    [[Spring Security] 8. OAuth2 Naver Login](https://velog.io/@kyu9610/Spring-Security-8.-OAuth2-Naver-Login)
    

# **OAuth2 네이버 로그인**

---

<aside>
💡 **NOTE**

> ***OAuth2 client는 Google, Facebook은 기본적으로 제공해주지만, 네이버/카카오 등 나라마다 대형 포털 사이트를 모두 제공해주지는 않는다!***
> 
- 그 이유는 `getAttributes` 값이 포털 사이트마다 **너무 다양하기 때문이다!**
    - 당장 구글과 페이스북만 보더라도 `provider-id`를 `sub`, `id` 다르게 줌
    - 따라서 기본 제공해주지 않는 포털 사이트를 로그인 하려면 개발문서를 읽어봐야 한다!
    

[NAVER Developers](https://developers.naver.com/main/)

이제는 알아서 등록하고 와라..

- Application > Application 등록 > 애플리케이션 이름 / API설정(네이버로그인) / API서비스환경(웹) > CallBack URL 설정([http://localhost:8080/login/oauth2/code/naver](http://localhost:8080/login/oauth2/code/naver)) 을 하면 앱이 생성된다.
</aside>

## **application.yml 설정**

<aside>
✍️ **NOTE**

```yaml
security:
    oauth2:
      client:
        registration:
          google:
            client-id: /**자신의 client-id**/
            client-secret: /**자신의 client-secret**/
            scope: profile,email

          facebook:
            client-id: /**자신의 client-id**/
            client-secret: /**자신의 client-secret**/
            scope: public_profile,email

          naver:
            client-id: /**자신의 client-id**/
            client-secret: /**자신의 client-secret**/
            scope: name,email
            client-name: Naver
            authorization-grant-type: authorization_code
            redirect-uri: http://localhost:8080/login/oauth2/code/naver

        provider:
          naver:
            authorization-uri: https://nid.naver.com/oauth2.0/authorize
            token-uri: https://nid.naver.com/oauth2.0/token
            user-info-uri: https://openapi.naver.com/v1/nid/me
            user-name-attribute: response #회원 정보를 JSON으로 받는데 response라는 키값으로 네이버가 리턴해줌.
```

- `authorization-grant-type`
    - 어떤 방식으로 인증을 할 것인가?
    - 우리는 기존에 사용하던 권한 코드 부여 방식을 사용하기 때문에 authorization_code를 적어준다.
- `redirect-uri`
    - 로그인 주소를 적는 곳
    - 기존의 구글이나 페이스북은 고정이 되어있었기 때문에 적어주지 않았지만, 네이버는 필요

- `provier`
    
    [네이버 로그인 개발가이드 - LOGIN](https://developers.naver.com/docs/login/devguide/devguide.md#3-4-2-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%97%B0%EB%8F%99-url-%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0)
    
    공식문서 참고하면서 할 것
    
    - `authorization-url`
        - 이 주소로 요청하면, 네이버 로그인이 나온다.
    - `token-uri`
        - 이 주소를 이용하여 토큰을 받을 수 있다.
    - `user-info-uri`
        - 이 주소를 사용하여야 프로필 정보를 받을 수 있다.
</aside>

# **소셜 로그인 구분**

---

## **PrincipalOauth2UserService**

<aside>
✍️ **NOTE**

```java
// 회원가입을 강제로 진행할 예정
OAuth2UserInfo oAuth2UserInfo = null;
if (userRequest.getClientRegistration().getRegistrationId().equals("google")) {
    oAuth2UserInfo = new GoogleUserInfo(oAuth2User.getAttributes());

} else if (userRequest.getClientRegistration().getRegistrationId().equals("facebook")) {
    oAuth2UserInfo = new FacebookUserInfo(oAuth2User.getAttributes());

}  else if (userRequest.getClientRegistration().getRegistrationId().equals("naver")) {
    oAuth2UserInfo = new NaverUserInfo((Map)oAuth2User.getAttributes().get("response"));

} else{
    System.out.println("구글하고 페이스북, 네이버 로그인이 없다고요? 나가");
}
```

- 네이버 로그인으로 들어오면 NaverUserInfo 클래스를 이용하여 처리한다.
- 네이버 로그인은 특이하게 **attributes에서 response라는 attribute를 다시 준다.**
    - 그 이유는 네이버는 attributes안에 response라는 속성에 id, email을 보관하기 때문
</aside>

## **NaverUserInfo**

<aside>
✍️ **NOTE**

```java
@RequiredArgsConstructor
public class NaverUserInfo implements OAuth2UserInfo {

    // {id=~, email=~, name=~} -> response
    private final Map<String, Object> attributes;

    @Override
    public String getProviderId() {
        return (String) attributes.get("id");
    }

    @Override
    public String getProvider() {
        return "naver";
    }

    @Override
    public String getEmail() {
        return (String) attributes.get("email");
    }

    @Override
    public String getName() {
        return (String) attributes.get("name");
    }
}
```

</aside>