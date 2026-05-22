# [Spring Security] 01-3. 실습 - form 회원가입

주제: Spring Security

- 참고
    
    [스프링 시큐리티를 이용한 회원가입 구현하기](https://velog.io/@jincrates/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%8B%9C%ED%81%90%EB%A6%AC%ED%8B%B0%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EB%B0%8F-%EB%A1%9C%EA%B7%B8%EC%9D%B8)
    
    [[Spring Security] 3. Spring Security 회원가입](https://velog.io/@kyu9610/Spring-Security-3.-Spring-Security-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85)
    

# **시큐리티 로그인, 회원가입**

---

<aside>
💡 **NOTE**

> ***시큐리티를 이용해서 회원가입을하고 로그인을 한다!***
> 
</aside>

## 회원가입, 컨트롤러 및 화면구성

<aside>
✍️ **NOTE**

### controller

```java
@GetMapping("/joinForm")
public String joinForm() {
    return "joinForm";
}

@PostMapping("/join")
public String join(User user) {
    System.out.println(user);

    user.setRole("ROLE_USER");
    String rawPassword = user.getPassword();
    String encPassword = bCryptPasswordEncoder.encode(rawPassword);
    user.setPassword(encPassword);

		// 회원가입 잘됨. 비밀번호 : 1234 => 시큐리티로 로그인할 수 없음 ( 패스워드가 암호화 되지 않아서)
    userRepository.save(user); 
    return "redirect:/loginForm";
}
```

### joinForm

![Untitled](%5BSpring%20Security%5D%2001-3%20%EC%8B%A4%EC%8A%B5%20-%20form%20%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85/Untitled.png)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원가입 페이지</title>
</head>
<body>
<h1>회원가입 페이지</h1>
<hr/>
<form action="/join" method="post">
    <input type="text" name="username" placeholder="Username"/> <br/>
    <input type="password" name="password" placeholder="Password"/> <br/>
    <input type="email" name="email" placeholder="Email"/> <br/>
    <button>회원가입</button>
</form>
</body>
</html>
```

</aside>

# **로그인, 권한처리**

---

<aside>
💡 **NOTE**

> ***로그인을 구현하기 위해서 auth 패키지를 생성한다!***
> 
- **auth패키지는 Spring Security가 로그인을 진행하고 완료가되면 Security Session을 만들어준다.**
- **Session**에 들어가는 정보 **Object**가 정해져있는데, 이것이 바로 **Authentication 객체**여야 한다.
- 즉 **Spring Security ⇒ Authentiaction ⇒ UserDetails** 객체 이렇게 구성된다.
</aside>

## 로그인, 컨트롤러 및 화면구성

<aside>
✍️ **NOTE**

### controller

```java
@GetMapping("/loginForm")
public String loginForm() {
    return "loginForm";
}
```

### loginForm

![Untitled](%5BSpring%20Security%5D%2001-3%20%EC%8B%A4%EC%8A%B5%20-%20form%20%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85/Untitled%201.png)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>로그인 페이지</title>
</head>
<body>
<h1>로그인 페이지</h1>
<hr/>
<!-- 시큐리티는 x-www-form-url-encoded 타입만 인식 -->
<form action="/login" method="post">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <button>로그인</button>
</form>
<a href="/joinForm">회원가입을 아직 하지 않으셨나요?</a>
</body>
</html>
```

</aside>

## **PrincipalDetails**

<aside>
✍️ **NOTE**

> ***UserDetails 객체를 상속받으면 스프링 시큐리티의 고유한 세션저장소에 저장을 할 수 있게 된다!***
> 

```java
@RequiredArgsConstructor
public class PrincipalDetails implements UserDetails {

    private final User user;

    // 해당 User의 권한을 리턴하는 곳
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        Collection<GrantedAuthority> collect = new ArrayList<>();
        collect.add(()->{ return user.getRole();});
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
}
```

- 스프링 시큐리티가 대신 로그인을 해주는 대신 패스워드를 가로채기 한다.
- 이렇게 된 PricipaDetails 타입을 Authentication객체 안에 넣는다.
</aside>

## **PrincipalDetailsService**

<aside>
✍️ **NOTE**

> *인증 시, DB에서 **User**를 찾고 **UserDetails**로 반환하는 **loadUserByUsername 메서드를 갖는다.***
> 

```java
// 시큐리티 설정에서 loginProcessingUrl("/login")
// login 요청이 오면 자동으로 UserDetailService 타입으로 Ioc 되어있는 loadUserByUserName 함수가 실행
@Service
@RequiredArgsConstructor
public class PrincipalDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    // 시큐리티 session = Authentication(내부 UserDetails) = UserDetails
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        System.out.println("username = " + username);
        User userEntity = userRepository.findByUsername(username);

        if (userEntity != null) {
            return new PrincipalDetails(userEntity);
        }
        return null;
    }
}
```

- **Authentication**객체를 생성하기 위해서 **PrincipalDetailsService class**를 생성한다.
- **UserDetailsService**를 상속하여 정의한다.
- **로그인 요청이 오면** 자동으로 **loadUserByUsername**함수가 실행되도록 정의되어 있다.
- 이 때 매개변수로 받는 **String username은 html에서 정의된 input type의 name과 동일해야 한다!**
</aside>

## 권한처리

<aside>
✍️ **NOTE**

> ***User의 정보에는 ROLE이라는 변수가 있으며, 이 권한에 따라 사용자가 들어갈 수 있는 페이지를 처리할 수 있다.***
> 

![각 유저는 권한이 다르다.](%5BSpring%20Security%5D%2001-3%20%EC%8B%A4%EC%8A%B5%20-%20form%20%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85/Untitled%202.png)

각 유저는 권한이 다르다.

### EnableWebSecurity

```java
@Configuration
@EnableWebSecurity // 스프링 시큐리티 필터가 스프링 필터체인에 등록된다!
@EnableGlobalMethodSecurity(securedEnabled = true, prePostEnabled = true)
// secure 어노테이션 활성화, preAuthorize, postAUthorize 활성화
public class SecurityConfig { ... }
```

```java
@Secured("ROLE_ADMIN")
@GetMapping("/info")
public @ResponseBody String info(){
    return "개인정보";
}
```

### EnableGlobalMethodSecurity

```java
@Configuration
@EnableWebSecurity // 스프링 시큐리티 필터가 스프링 필터체인에 등록된다!
@EnableGlobalMethodSecurity(securedEnabled = true, prePostEnabled = true)
// secure 어노테이션 활성화, preAuthorize, postAUthorize 활성화
public class SecurityConfig { ... }
```

```java
@PreAuthorize("hasRole('ROLE_MANAGER') or hasRole('ROLE_ADMIN')")
@GetMapping("/data")
public @ResponseBody String data(){
    return "데이터정보";
}
```

</aside>