# [Spring Security] 02-3. Facebook Login

주제: Spring Security

- 참고
    
    [[Spring Security] 7. OAuth2 Facebook Login](https://velog.io/@kyu9610/Spring-Security-7.-OAuth2-Facebook-Login)
    

# **OAuth2 페이스북 로그인**

---

<aside>
💡 **NOTE**

> ***구글 로그인을 해보았으니, 페이스북 로그인도 쉽게 할 수 있다!***
> 

[Meta for Developers](https://developers.facebook.com/?locale=ko_KR)

들어가서  설정하고 client-id, client-secret 값 받아오자

</aside>

## **application.yml**

<aside>
✍️ **NOTE**

```yaml
security:
    oauth2:
      client:
        registration:
          google:
            client-id: /**자신의 클라이언트 아이디**/
            client-secret: /**자신의 클라이언트 비밀번호**/
            scope: profile,email

          facebook:
            client-id: /**자신의 클라이언트 아이디**/
            client-secret: /**자신의 클라이언트 비밀번호**/
            scope: public_profile,email
```

- 기존의  구글 로그인과 똑같이 구성되어 있다.
- 만들어진 앱에서 `client-id/secre`t를 받아서 적어준다.
- `scope`는 google과 다르게 `public_profile`로 적어주어야 한다.
    - ⚠️ 사이트마다 `scope`값이 다르기 때문에 주의할것!
</aside>

# **구글과 페이스북 로그인 구분**

---

<aside>
💡 **NOTE**

> 이전에 **구글 로그인**을 구현할 떄에 `attributes`에서 `sub`라는 타이틀을 가져온적이 있다.
하지만 **페이스북에서는 sub가 아닌 id를 받아와야하는데 어떻게 해결하는가?**
> 
- 👏 **provider**를 구분하기 위해서 **인터페이스와 클래스를 생성하기로 한다!**
</aside>

## **OAuth2UserInfo.interface**

<aside>
✍️ **NOTE**

```java
public interface OAuth2UserInfo {
    String getProviderId();
    String getProvider();
    String getEmail();
    String getName();
}
```

- provier와 providerId, 이메일, 이름을 반환하는 공통 메서드를 구현한다.
</aside>

## **GoogleUserInfo, FacebookUserInfo**

<aside>
✍️ **NOTE**

### GoogleUserInfo

```java
public class GoogleUserInfo implements OAuth2UserInfo{

    private Map<String,Object> attributes; // getAttributes;

    // 생성자
    public GoogleUserInfo(Map<String,Object> attributes){
        this.attributes = attributes;
    }

    @Override
    public String getProviderId() {
        return (String)attributes.get("sub");
    }

    @Override
    public String getProvider() {
        return "google";
    }

    @Override
    public String getEmail() {
        return (String)attributes.get("email");
    }

    @Override
    public String getName() {
        return (String)attributes.get("name");
    }
}
```

### FacebookUserInfo

```java
public class FacebookUserInfo implements OAuth2UserInfo{
    
		private Map<String,Object> attributes; // getAttributes;

    // 생성자
    public FacebookUserInfo(Map<String,Object> attributes){
        this.attributes = attributes;
    }

    @Override
    public String getProviderId() {
        return (String)attributes.get("id");
    }

    @Override
    public String getProvider() {
        return "facebook";
    }

    @Override
    public String getEmail() {
        return (String)attributes.get("email");
    }

    @Override
    public String getName() {
        return (String)attributes.get("name");
    }
}
```

</aside>

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

} else{
    System.out.println("구글하고 페이스북, 네이버 로그인이 없다고요? 나가");
}

String provider = oAuth2UserInfo.getProvider();// google
String providerId = oAuth2UserInfo.getProviderId();
String username = oAuth2UserInfo + "_" + providerId;
String password = "겟인데어";
String email = oAuth2User.getAttribute("email");
String role = "ROLE_USER";
```

- 인터페이스를 통해서 구글과, 페이스북 둘다 쉽게 정보를 받아올 수 있게했다.
- 이제 이 정보를 활용해서 로그인이 실행되게 하면된다!

```java
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
    System.out.println("userEntity = " + userEntity);
    userRepository.save(userEntity);
}else{
    System.out.println("이미 로그인한적이 있습니다!");
}
```

</aside>