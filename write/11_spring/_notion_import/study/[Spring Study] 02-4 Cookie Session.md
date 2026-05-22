# [Spring Study] 02-4. Cookie / Session

주제: Spring Study

- 참고
    
    

# Cookie **🍪**

---

## Cookie 생성

<aside>
✍️ **NOTE**

![서버에서 쿠키를 생성해서 응답에 넣어줌](%5BSpring%20Study%5D%2002-4%20Cookie%20Session/Untitled.png)

서버에서 쿠키를 생성해서 응답에 넣어줌

```java
**Cookie idCookie = new Cookie("memberId", String.valueOf(loginMember.getId()));**
response.**addCookie(idCookie);**
```

</aside>

## Cookie 사용

<aside>
✍️ **NOTE**

![쿠키 저장소에 있는 쿠키 사용](%5BSpring%20Study%5D%2002-4%20Cookie%20Session/Untitled%201.png)

쿠키 저장소에 있는 쿠키 사용

![모든 요청에 쿠키는 포함되어 있음](%5BSpring%20Study%5D%2002-4%20Cookie%20Session/Untitled%202.png)

모든 요청에 쿠키는 포함되어 있음

```java
@GetMapping("/")
public String homeLogin(**@CookieValue(name = "memberId", required = false) Long memberId**, Model model) {

    if (memberId == null) {
        return "home";
    }

    // 로그인
    Member loginMember = memberRepository.findById(memberId);
    if (loginMember == null) return "home";

    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

</aside>

## Cookie 삭제

<aside>
✍️ **NOTE**

![쿠키 제거](%5BSpring%20Study%5D%2002-4%20Cookie%20Session/Untitled%203.png)

쿠키 제거

```java
private void expireCookie(HttpServletResponse response, String cookieName) {
    Cookie cookie = new Cookie(cookieName, null);
    **cookie.setMaxAge(0);**
    response.addCookie(cookie);
}
```

</aside>

# Session

---

## Session **생성**

<aside>
✍️ **NOTE**

![쿠키 값으로 UUID값이 넘어감](%5BSpring%20Study%5D%2002-4%20Cookie%20Session/Untitled%204.png)

쿠키 값으로 UUID값이 넘어감

```java
/**
* 세션 생성
*/
public void createdSession(Object value, HttpServletResponse response){
  // 세션 id를 생성하고, 값을 세션에 저장
  String sessionId = UUID.randomUUID().toString();
  **sessionStore.put(sessionId, value);** // value에 로그인회원 정보 들어감

  // 쿠키 생성
  **Cookie mySessionCookie = new Cookie(SESSION_COOKIE_NAME, sessionId);**
  response.addCookie(mySessionCookie);
}
```

</aside>

## Session 조회/사용

<aside>
✍️ **NOTE**

```java
/**
 * 세션 조회
 */
public Object getSession(HttpServletRequest request){
    **Cookie sessionCookie = findCookie(request, SESSION_COOKIE_NAME);**

    if(sessionCookie == null){
        return null;
    }

    return sessionStore.get(sessionCookie.getValue());
}
```

```java
// 세션 관리자를 통해 세션을 생성하고, 회원데이터 보관 (로그인)
sessionManager.createdSession(loginMember, response);

// 세션 관리자에 저장된 회원 정보 조회(페이지 이동)
Member member = (Member) sessionManager.getSession(request);
```

</aside>

## Session 삭제

<aside>
✍️ **NOTE**

```java
/**
* 세션 만료
*/
public void expire(HttpServletRequest request){
  Cookie sessionCookie = findCookie(request, SESSION_COOKIE_NAME);
  if(sessionCookie != null){
      sessionStore.remove(sessionCookie.getValue());
  }
}
```

</aside>

## Session - HttpSession

<aside>
✍️ **NOTE**

> ***HttpSession ⇒ SessionManager와 같은 방식으로 동작***
> 

```java
HttpSession session = **request.getSession();**
// 세션에 로그인 회원정보 보관
**session.setAttribute(SessionConst.LOGIN_MEMBER, loginMember);**
```

```java
// @GetMapping("/")
public String homeLoginV3(HttpServletRequest request, Model model) {

    **HttpSession session = request.getSession(false);**
    if(session == null){
        return "home";
    }

    // 세션 관리자에 저장된 회원 정보 조회
    **Member loginMember = (Member) session.getAttribute(SessionConst.LOGIN_MEMBER);**

    // 세션에 회원 데이터가 없으면 home
    if (loginMember == null) return "home";

    // 세션이 유지되면 로그인으로 이동
    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

- `true` →세션이 없으면 생성한다
- `false` → 세션이 없다면 null을 반환한다
</aside>

## Session - **@SessionAttribute**

<aside>
✍️ **NOTE**

```java
@GetMapping("/")
public String homeLoginV3Spring(**@SessionAttribute(name = SessionConst.LOGIN_MEMBER, required = false) Member loginMember**, Model model) {

    // 세션에 회원 데이터가 없으면 home
    if (loginMember == null) return "home";

    // 세션이 유지되면 로그인으로 이동
    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

---

- **[참고]**
    
    ```java
    server.servlet.session.tracking-modes=cookie
    ```
    
    - 웹 브라우저가 쿠키를 지원하지 않는 경우를 대비해 URL로 세션을 최초에 보내줌
    - url이 아닌 쿠키로만 세션을 유지하려면 application.properties에 값추가
</aside>