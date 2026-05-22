# [Spring Study] 02-2. Servlet

주제: Spring Study

- 참고
    
    [[JSP] 서블릿(Servlet)이란?](https://mangkyu.tistory.com/14)
    
    [[서블릿/JSP] 서블릿의 초기화 과정 및 초기화 방법](https://dololak.tistory.com/47)
    
    [[Spring] Spring MVC - Servlet, Servlet Container, Spring Container 에 대해](https://velog.io/@choidongkuen/Spring-Spring-MVC-Servlet-Servlet-Container-란)
    

# Servlet

---

<aside>
💡 **NOTE**

> `*Servlet`은 웹 서버에서 실행됩니다. 웹 서버는 클라이언트로부터 HTTP 요청을 받아 해당 요청을 적절한 `Servlet`에 전달합니다. `Servlet`은 이를 처리하여 결과를 웹 서버에 반환하고, 웹 서버는 이를 클라이언트에게 전송합니다.*
> 

`Servlet`은 Java 웹 애플리케이션의 핵심 컴포넌트로, HTTP 요청을 처리하고 동적 웹 컨텐츠를 생성하는데 아주 중요한 개념입니다. `Servlet`의 주요 기능은 다음과 같습니다.

- **세션 관리**: 클라이언트 - 서버 간의 상태를 유지할 수 있습니다.
- **쿠키 관리**: 클라이언트의 쿠키를 읽고 작성할 수 있습니다.
- **멀티스레딩 지원**: 각 요청마다 새로운 스레드가 생성되어 병렬 처리됩니다.
- **필터**: 요청과 응답을 가로채어 전후처리를 할 수 있습니다.

### Servlet 동작흐름

![1. Servlet 클래스가 로드되고, init() 메서드 호출로 인스턴스를 초기화한다.](%5BSpring%20Study%5D%2002-2%20Servlet/Untitled.png)

1. Servlet 클래스가 로드되고, init() 메서드 호출로 인스턴스를 초기화한다.

![2. Request / Response를 간단한 메서드(doGet(), doPost())를 호출해서 처리합니다.](%5BSpring%20Study%5D%2002-2%20Servlet/Untitled%201.png)

2. Request / Response를 간단한 메서드(doGet(), doPost())를 호출해서 처리합니다.

</aside>

## Servlet 컨테이너

<aside>
✍️ **NOTE**

> ***Servlet 컨테이너**는 Servlet의 실행 환경을 제공하는 서버 컴포넌트 입니다. Java Servlet API를 구현하여 Servlet의 생명주기 관리 및, HTTP 요청을 처리하며 대표적으로 Apache Tomcat, Jetty등이 있습니다.*
> 

![서블릿 컨테이너 (Servlet 객체는 기본적으로 싱글톤으로 관리됩니다.)](%5BSpring%20Study%5D%2002-2%20Servlet/Untitled%202.png)

서블릿 컨테이너 (Servlet 객체는 기본적으로 싱글톤으로 관리됩니다.)

![Servlet 컨테이너 동작흐름](%5BSpring%20Study%5D%2002-2%20Servlet/Untitled%203.png)

Servlet 컨테이너 동작흐름

### Servlet 컨테이너의 역할

1. 생명주기 관리
    - 초기화: 서블릿 인스턴스를 생성하고 초기화 메서드 init() 호출
    - 종료: 종료 메서드 destroy() 호출하여 자원해제
2. 요청과 응답 처리
    - 요청(HttpServletRequest), 응답(HttpServletResponse) 변환 및 생성
    - 적절한 Servlet 메서드를 호출하여 요청을 처리하고 응답을 작성합니다.
3. 서블릿 매핑
    
    ```xml
    <servlet>
        <servlet-name>HelloServlet</servlet-name>
        <servlet-class>com.example.HelloServlet</servlet-class>
    </servlet>
    
    <servlet-mapping>
        <servlet-name>HelloServlet</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
    ```
    
    - URL 패턴을 사용하여 요청을 특정 Servlet에 맵핑합니다.
    - 맵핑 정보는 web.xml에 있습니다.
4. 보안 관리
    - 인증, 권한 부여, 데이터 암호화등을 할 수 있습니다,
    - 보안 설정은 web.xml에서 설정할 수 있습니다.
5. 세션 관리
    - 클라이언트-서버 간의 Session을 관리하며, 클라이언트의 상태를 유지하고 SessionID를 통해 각 클라이언트를 식별할 수 있습니다.
</aside>

## **Servlet 컨테이너 - Servlet**

<aside>
✍️ **NOTE**

```java
@WebServlet("/myServlet")
public class MyServlet extends HttpServlet {

    @Override
    public void init() throws ServletException {
        // 서블릿 초기화 로직
        System.out.println("Servlet is being initialized");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 세션 관리
        HttpSession session = req.getSession();
        Integer visitCount = (Integer) session.getAttribute("visitCount");
        if (visitCount == null) {
            visitCount = 1;
        } else {
            visitCount++;
        }
        session.setAttribute("visitCount", visitCount);

        // 응답 작성
        resp.setContentType("text/html");
        resp.getWriter().write("<h1>Welcome to MyServlet</h1>");
        resp.getWriter().write("<p>Visit Count: " + visitCount + "</p>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // POST 요청 처리
        String name = req.getParameter("name");
        resp.setContentType("text/html");
        resp.getWriter().write("<h1>Hello, " + name + "!</h1>");
    }

    @Override
    public void destroy() {
        // 서블릿 종료 로직
        System.out.println("Servlet is being destroyed");
    }
}
```

</aside>

## **Servlet 컨테이너 - Lisenter**

<aside>
✍️ **NOTE**

```java
@WebListener
public class MyListener implements ServletContextListener, HttpSessionListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        // 서블릿 컨텍스트 초기화 이벤트 처리
        System.out.println("ServletContext initialized");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        // 서블릿 컨텍스트 종료 이벤트 처리
        System.out.println("ServletContext destroyed");
    }

    @Override
    public void sessionCreated(HttpSessionEvent se) {
        // 세션 생성 이벤트 처리
        System.out.println("Session created: " + se.getSession().getId());
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        // 세션 종료 이벤트 처리
        System.out.println("Session destroyed: " + se.getSession().getId());
    }
}

```

- `Listenr`는 서블릿 컨테이너의 특정 이벤트를 감지하고 처리하는 클래스입니다.
    - ex) Session 생성 및 소멸, 서블릿 컨텍스트 초기화 및 종료 이벤트
</aside>

## **Servlet 컨테이너 - 보안설정**

<aside>
✍️ **NOTE**

```xml
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">

    <!-- 보안 설정 -->
    <security-constraint>
        <web-resource-collection>
            <web-resource-name>Protected Area</web-resource-name>
            <url-pattern>/secure/*</url-pattern>
        </web-resource-collection>
        <auth-constraint>
            <role-name>USER</role-name>
        </auth-constraint>
    </security-constraint>

    <login-config>
        <auth-method>BASIC</auth-method>
        <realm-name>MyServletRealm</realm-name>
    </login-config>

    <security-role>
        <role-name>USER</role-name>
    </security-role>

</web-app>
```

</aside>

# **HttpServletRequest**

---

<aside>
💡 **NOTE**

> `*HttpServletRequest`는 HTTP 요청 정보를 캡슐화 합니다. 이를 통해 서버는 클라이언트가 보낸 데이터 (form, 요청 파라미터, 헤더 등)에 접근할 수 있습니다.*
> 

`HttpServletRequest`의 주요 기능은 다음과 같습니다.

1. 요청 파라미터 접근
2. 헤더 정보 접근
3. 세션 관리
4. 요청 속성 관리
5. 요청 정보 제공
</aside>

## **요청 파라미터 접근**

<aside>
✍️ **NOTE**

```java
@WebServlet("/requestParameter")
public class RequestParameterServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        
        // 요청 파라미터 접근
        String name = req.getParameter("name");
        if (name == null || name.isEmpty()) {
            name = "Guest";
        }

        // ...
    }
}
```

</aside>

## **헤더 정보 접근**

<aside>
✍️ **NOTE**

```java
@WebServlet("/requestHeader")
public class HeaderInfoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 헤더 정보 접근
        String userAgent = req.getHeader("User-Agent");

        // 응답 작성
        resp.setContentType("text/html");
        resp.getWriter().write("<h1>Your User-Agent: " + userAgent + "</h1>");

        // 모든 헤더 출력
        Enumeration<String> headerNames = req.getHeaderNames();
        
        // ...
    }
}
```

</aside>

## **세션 관리**

<aside>
✍️ **NOTE**

```java
@WebServlet("/requestSession")
public class SessionManagementServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 세션 조회
        HttpSession session = req.getSession();
        Integer visitCount = (Integer) session.getAttribute("visitCount");
        if (visitCount == null) {
            visitCount = 1;
        } else {
            visitCount++; // 방문마다 +1
        }
        
        // 세션 수정
        session.setAttribute("visitCount", visitCount);

        // ...
    }
}
```

</aside>

## **요청 속성 관리**

<aside>
✍️ **NOTE**

```java
@WebServlet("/requestAttribute")
public class RequestAttributeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 요청 속성 설정
        req.setAttribute("greeting", "Hello, World!");

        // 요청 속성 읽기
        String greeting = (String) req.getAttribute("greeting");

        // ...
    }
}
```

- 요청 속성(attribute)의 활용 사례는 다음과 같습니다.
    1. 포워딩(Fowarding), 인클루딩(Including)
    2. 임시 데이터 저장
    3. 데이터 전달
</aside>

## **요청 정보 제공**

<aside>
✍️ **NOTE**

```java
public class RequestInfoServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 요청 정보 제공
        String requestURI = req.getRequestURI();
        String clientIP = req.getRemoteAddr();
        String method = req.getMethod();
        String protocol = req.getProtocol();

        // ...
    }
}
```

</aside>

# **HttpServletResponse**

---

<aside>
💡 **NOTE**

> `*HttpServletResponse` 객체는 서블릿이 클라이언트에게 응답을 작성할 때 사용되며 응답 상태 코드, 헤더, 바디 등의 설정을 관리할 수 있습니다.*
> 

`HttpServletRequest`의 주요 기능은 다음과 같습니다.

1. 상태 코드 설정
2. 응답 헤더 설정
3. 응답 바디 작성
</aside>

## 상태 코드 설정

<aside>
✍️ **NOTE**

```java
@WebServlet("/statusExample")
public class StatusExampleServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 200 OK 상태 코드 설정
        resp.setStatus(HttpServletResponse.SC_OK);
        resp.getWriter().write("Status set to 200 OK");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 404 Not Found 상태 코드와 에러 메시지 전송
        resp.sendError(HttpServletResponse.SC_NOT_FOUND, "Resource not found");
    }
}
```

</aside>

## 응답 헤더 설정

<aside>
✍️ **NOTE**

```java
@WebServlet("/headerExample")
public class HeaderExampleServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 응답 헤더 설정
        resp.setHeader("Content-Type", "text/html");
        resp.setHeader("Custom-Header", "CustomHeaderValue");

        // 응답 바디 작성
        resp.getWriter().write("<h1>Headers set</h1>");
        resp.getWriter().write("<p>Check the response headers for 'Content-Type' and 'Custom-Header'.</p>");
    }
}
```

</aside>

## **응답 바디 작성**

<aside>
✍️ **NOTE**

```java
@WebServlet("/responseBodyExample")
public class ResponseBodyExampleServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 응답의 콘텐츠 타입 설정
        resp.setContentType("text/html");

        // 텍스트 응답 바디 작성
        resp.getWriter().write("<h1>This is a response body example</h1>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 바이너리 응답 바디 작성
        resp.setContentType("application/octet-stream");
        resp.setHeader("Content-Disposition", "attachment; filename=\"example.bin\"");
        
        ServletOutputStream outputStream = resp.getOutputStream();
        outputStream.write(new byte[]{0x01, 0x02, 0x03, 0x04});
        outputStream.flush();
        outputStream.close();
    }
}
```

</aside>