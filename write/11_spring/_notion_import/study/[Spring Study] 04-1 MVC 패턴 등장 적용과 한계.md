# [Spring Study] 04-1. MVC 패턴 등장 / 적용과 한계

주제: Spring Study
연관 노트: 아키텍쳐 & 대규모 시스템 설계] 06. 소프트웨어 아키텍쳐 패턴 (https://www.notion.so/06-a8475f529f8c403383558ea8b1068718?pvs=21)

- 참고
    
    [Controller, Service, Repository 가 무엇일까?](https://velog.io/@jybin96/Controller-Service-Repository-가-무엇일까)
    
    [](https://github.com/backend-sprout/spring-mvc-1/blob/main/03%20%EC%84%9C%EB%B8%94%EB%A6%BF%2C%20JSP%2C%20MVC%20%ED%8C%A8%ED%84%B4/01%20%ED%9A%8C%EC%9B%90%20%EA%B4%80%EB%A6%AC%20%EC%9B%B9%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98.md.md)
    
    [spring-mvc-1/03 MVC 패턴 적용.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/03%20%EC%84%9C%EB%B8%94%EB%A6%BF%2C%20JSP%2C%20MVC%20%ED%8C%A8%ED%84%B4/03%20MVC%20%ED%8C%A8%ED%84%B4%20%EC%A0%81%EC%9A%A9.md)
    
    [구현하며 이해하는 Spring MVC](https://liltdevs.tistory.com/m/189)
    

# MVC(**Model View Controller)**

---

<aside>
💡 **NOTE**

> ***MVC 패턴은 컨트롤러(Controller)와 뷰(View)라는 영역으로 서로 역할을 나누는 것을 말한다.***
> 

![MVC 패턴 이전 → 비즈니스 로직과 뷰 로직이 합쳐져 있다.](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled.png)

MVC 패턴 이전 → 비즈니스 로직과 뷰 로직이 합쳐져 있다.

![MVC 패턴 1 → Controller(비즈니스 로직) / View(뷰 로직)을 분리했다.](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled%201.png)

MVC 패턴 1 → Controller(비즈니스 로직) / View(뷰 로직)을 분리했다.

![MVC 패턴 2 → 기존 Controller를  
Controller는 HTTP 요청 / Service는 비즈니스 로직으로 분리](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled%202.png)

MVC 패턴 2 → 기존 Controller를  
Controller는 HTTP 요청 / Service는 비즈니스 로직으로 분리

![MVC 패턴2 세부내용](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled%203.png)

MVC 패턴2 세부내용

![MVC 패턴2 흐름](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled%204.png)

MVC 패턴2 흐름

![Untitled](%5BSpring%20Study%5D%2004-1%20MVC%20%ED%8C%A8%ED%84%B4%20%EB%93%B1%EC%9E%A5%20%EC%A0%81%EC%9A%A9%EA%B3%BC%20%ED%95%9C%EA%B3%84/Untitled%205.png)

- **Controller**
    - HTTP 요청을 받아서 **파라미터를 검증**하고, **비즈니스 로직을 실행**한다.
    - `Model`과 `View` 사이의 데이터 전달 역할
    - 자바에서 `Controller`는 `Servlet`을 사용하게 된다.
- **Model**
    - `View`에 출력할 데이터를 담아둔다
    - `Controller`로 부터 `View`가 필요한 데이터를 담는다.
    - `View`는 화면을 렌더링 하는 일에 집중할 수 있다
- **View**
    - `Model`에 담겨있는 데이터를 사용해서 그리는 일에만 집중한다
- **Service**
    - `Controller`에서 넘어온 요청을 받아 알맞은 정보를 가공해서 보냄
    - 비즈니스 로직 수행, `DAO`를 이용해 결과값 받음
- **DAO**
    - Mysql 서버에 접근하여 SQL문을 실행할 수 있는 객체
</aside>

# **MVC 패턴 적용** ⭐

---

<aside>
💡 **NOTE**

> ***아래와 같은 구조로 MVC 패턴을 적용해보자!***
> 
- **Controller**
    - 서블릿
- **View**
    - JSP
- **Model**
    - HttpServletRequest 객체
    - request는 내부에 데이터 저장소를 가지고 있다.
        - `request.setAttribute()`
        - `request.getAttribute()`
</aside>

## **회원 등록 폼 이동**

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "mvcMemberFormServlet", urlPatterns = "/servlet-mvc/members/new-form")
public class MvcMemberFormServlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String viewPath = "/WEB-INF/views/new-form.jsp";
        **RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);**
    }
}
```

- **/WEB-INF**
    - /WEB-INF 폴더는 외부에서 접근할 수 없도록 설정되어 있는 폴더이다
    - 해당 폴더에 접근하려면 애플리케이션 내부적으로 즉 `Servlet`을 통해 접근해야 함
- **redirect vs foward**
    - **redirect**
        - 클라이언트에 응답이 나갔다가 클라이언트가 redirect 경로로 다시 요청한다
        - 클라이언트가 인지할 수 있고, URL도 실제로 변경됨
    - **foward**
        - 서버 내부에서 일어나는 호출이기 때문에 클라이언트가 알지못한다.
</aside>

## **회원 저장**

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "mvcMemberSaveServlet", urlPatterns = "/servlet-mvc/members/save")
public class MvcMemberSaveServlet extends HttpServlet {
    private MemberRepository memberRepository = MemberRepository.getInstance();

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Member 저장 
        String username = request.getParameter("username");
        int age = Integer.parseInt(request.getParameter("age"));
        Member member = new Member(username, age);
        memberRepository.save(member);
        
        // Model에 데이터를 보관
        **request.setAttribute("member", member);**
        
        // 특정 URL로 forward
        String viewPath = "/WEB-INF/views/save-result.jsp";
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

- `Model`은 `HttpServletRequest`의 `request` 객체를 사용하는 것이다
    - `request`에서 `setAttribute()`를 사용해 데이터 저장하고 `View`에 전달
    - `View`에서는 `request.getAttribute()`를 사용해서 데이터 꺼냄
</aside>

## 회원 목록 조회

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "mvcMemberListServlet", urlPatterns = "/servlet-mvc/members")
public class MvcMemberListServlet extends HttpServlet {
    private MemberRepository memberRepository = MemberRepository.getInstance();
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 회원 목록 조회 
        List<Member> members = memberRepository.findAll();
        
        // Model에 데이터를 보관 
        **request.setAttribute("members", members);**
        
        // 특정 URL로 forward
        String viewPath = "/WEB-INF/views/members.jsp";
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

- **Model** 역할인 HttpServletRequest request 객체는 다양한 데이터 타입을 지원한다
    - List<Member> members와 같은 컬렉션 타입도 보관할 수 있다.
</aside>

# **MVC 컨트롤러의 단점**

---

<aside>
💡 **NOTE**

> ***MVC 패턴을 적용함으로써 비즈니스 로직과 뷰 로직이 분리가 되었다.
하지만 여러 컨트롤러를 봤을 때 중복된 코드가 많고, 필요하지 않는 코드가 많이보인다***
> 

```java
@WebServlet(name = "mvcMemberFormServlet", urlPatterns = "/servlet-mvc/members/new-form")
public class MvcMemberFormServlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String viewPath = "/WEB-INF/views/new-form.jsp";
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

</aside>

## **ViewPath에 중복**

<aside>
✍️ **NOTE**

```java
String viewPath = "/WEB-INF/views/new-form.jsp";
```

- 각각의 컨트롤러에서는 데이터 흐름의 이동을 위한 경로 문자열을 가진다.
허나 자세히보면 아래와 같은 중복을 가지는 것을 알 수 있다.
    - **prefix** : /WEB-INF/views/
    - **suffix** : .jsp
- 이러한 중복은 **경로가 바뀌었을 때 모든 ViewPath를 수정해야한다는 단점이 있다**
    - JSP가 아닌 thymeleaf 같은 다른 뷰로 변경한다면 전체 코드를 변경해야 함..
</aside>

## **포워드 중복**

<aside>
✍️ **NOTE**

```java
RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
dispatcher.forward(request, response);
```

- `View`로 **이동하는 코드가 항상 중복 호출되어야 하며 그 모습 또한 동일**하다
- 물론 이 부분을 메서드로 공통화해도 되지만, 해당 메서드도 항상 직접 호출해야 함
</aside>

## **사용하지 않는 코드**

<aside>
✍️ **NOTE**

```java
HttpServletRequest request, HttpServletResponse response
```

- `HttpServletRequest`, `HttpServletResponse` 객체는 사용할 때도 있고, 사용하지 않을 때도 있다
- `HttpServletRequest`, `HttpServletResponse` 클래스는 개발자가 직접 생성하고 다루는 대상이 아니다보니 **테스트 케이스를 작성하기도 어렵다.**
</aside>

## **공통 처리가 어렵다.**

<aside>
✍️ **NOTE**

> ***앞서 말했던 단점들은 전부 공통과 중복이라는 키워드로 설명이 가능하다***
> 
- 공통 기능들은 단순히 메서드로 뽑으면 될 것 같지만, 결과적으로 메서드를 호출하는 것 자체도 중복이다
- 이 문제를 해결하려면 컨트롤러 호출 전에 앞단에서 먼저 공통기능을 처리해야 한다
- 즉 **프론트 컨트롤러(Front Controller) 패턴을 도입하면 이런 문제를 깔끔하게 해결할 수 있다!**
</aside>