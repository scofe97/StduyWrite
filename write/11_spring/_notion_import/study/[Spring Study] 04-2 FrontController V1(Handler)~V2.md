# [Spring Study] 04-2. FrontController V1(Handler)~V2( View 분리)

주제: Spring Study

- 참고
    
    [spring-mvc-1/01 프론트 컨트롤러 - V1.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/04%20MVC%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%20%EB%A7%8C%EB%93%A4%EA%B8%B0/01%20%ED%94%84%EB%A1%A0%ED%8A%B8%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20-%20V1.md)
    
    [spring-mvc-1/02 프론트 컨트롤러 - V2.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/04%20MVC%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%20%EB%A7%8C%EB%93%A4%EA%B8%B0/02%20%ED%94%84%EB%A1%A0%ED%8A%B8%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20-%20V2.md)
    

# **프론트 컨트롤러**

---

<aside>
💡 **NOTE**

> ***FrontController + HandlerMapping 도입***
> 

![**`FrontController` 도입 전**](%5BSpring%20Study%5D%2004-2%20FrontController%20V1(Handler)~V2/Untitled.png)

**`FrontController` 도입 전**

- 각각의 `Controller`에 공통된 코드들이 많다는 문제가 있다
- 이로 인해 중복이 발생하고 코드의 변경이 필요할 때 유지보주성이 떨어진다는 문제가 발생한다.

![**`FrontController` 도입 후**](%5BSpring%20Study%5D%2004-2%20FrontController%20V1(Handler)~V2/Untitled%201.png)

**`FrontController` 도입 후**

- 각 컨트롤러 앞단에 `FrontController`를 두어 공통 로직을 `FrontController`에서 처리하도록 한다,

### **FrontController 패턴 특징**

---

- **[참고]**
    - Spring의 웹 MVC와 `FrontController`
        - Spring 웹 MVC의 핵심도 바로 `FrontController`다
        - Spring 웹 MVC의 `DispatcherServlet`이 `FrontController` 패턴으로 구현 됨
</aside>

## **FrontController 패턴 특징**

<aside>
✍️ **NOTE**

> ***FrontController 하나로 클라이언트의 요청을 받음!***
> 
- FrontController가 요청에 맞는 컨트롤러를 찾아서 호출
- 공통 처리 가능 FrontControllr를 제외한 **나머지 Controller는 Servlet을 사용하지 않음**
</aside>

# **FrontController - V1**

---

<aside>
💡 **NOTE**

> ***앞의 MVC 패턴과 대표적인 차이점은 요청 url을 통해 알맞은 Handler (Controller)를 찾아와서 실행을 시킨다***
> 

![맵핑정보(Handler)를 조회해서  컨트롤러를 실행시킴](%5BSpring%20Study%5D%2004-2%20FrontController%20V1(Handler)~V2/Untitled%202.png)

맵핑정보(Handler)를 조회해서  컨트롤러를 실행시킴

- 이러한 과정에서 URL과 매핑된 `Handler` 를 저장하는 공간을 `Handler Mapping`이라고 부른다 즉 `Handler Mapping`으로부터 `Handler` 를 조회해서 알맞은 `Handler (Controller)`를 실행하는 과정이다.
</aside>

## **V1 - FrontController**

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "frontControllerServletV1", urlPatterns = "/front-controller/v1/*")
public class FrontControllerServletV1 extends HttpServlet {

		// URI를 맵핑할 Handler 저장소
    private Map<String, ControllerV1> **controllerMap** = new HashMap<>();

		// 생성자에 Handler를 저장한다.
    public FrontControllerServletV1() {
        controllerMap.put("/front-controller/v1/members/new-form", new MemberFormControllerV1());
        controllerMap.put("/front-controller/v1/members/save", new MemberSaveControllerV1());
        controllerMap.put("/front-controller/v1/members", new MemberListControllerV1());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("FrontControllerServletV1.service");

        // /front-controller/v1/members
        **String requestURI = request.getRequestURI();**

        ControllerV1 controller = controllerMap.get(requestURI);
        if(controller == null){
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        controller.process(request, response);
    }
}
```

```java
public class MemberFormControllerV1 implements ControllerV1 {
    @Override
    public void process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String viewPath = "/WEB-INF/views/new-form.jsp";
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

- **controllMap 객체에 URI 패턴을 등록한다!**
    - `urlPatterns = "/front-controller/v1/*"`
    - 패턴 매칭으로 `/front-controller/v1` 를 포함한 모든 하위 요청을 이 서블릿에서 처리한다.
    - ex) `/front-controller/v1` , `/front-controller/v1/a` , `/front-controller/v1/a/b`
    
- **service()**
    - 핸들러 매핑에서 URI를 조회해서 실제 호출할 Controller를 `ControllerMap`에서 찾는다
        - 만약 없다면 404(SC_NOT_FOUNT) 상태 코드 반환
        - Controller를 찾았다면 `controller.process(request, response)` 실행
</aside>

# **FrontController - V2**

---

<aside>
💡 **NOTE**

> ***View 관련 로직 별도의 객체로 분리한다!***
> 

![V2 구조는 V1구조에서 View와 관련된 로직을 `View 객체(MyView)`로 분리시킨 구조다.](%5BSpring%20Study%5D%2004-2%20FrontController%20V1(Handler)~V2/Untitled%203.png)

V2 구조는 V1구조에서 View와 관련된 로직을 `View 객체(MyView)`로 분리시킨 구조다.

```java
String viewPath = "/WEB-INF/views/new-form.jsp";
RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
dispatcher.forward(request, response);
```

- 모든 Controller들은 로직을 수행한 후 특정 VIew로 흐름을 이동하기 위해 이와 같은 코드를 작성했다.
- 그러나 위와 같은 코드가 모든 Controller에 존재하기에 중복이 발생하고 이로인해 유지보수에 어려움이 생겼다.
    - (경로나 형식이 바뀐다면 모든 Controller의 코드를 일일히 수정해줘야 한다는 문제가 발생한다)
- 이를 **해결하기 위해, View 관련 로직을 별도의 객체(MyView)로 분리하는 방법을 고안해냈고 이를 활용한게 V2이다.**
</aside>

## **V2 - FrontController**

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "frontControllerServletV2", urlPatterns = "/front-controller/v2/*")
public class FrontControllerServletV2 extends HttpServlet {

    private Map<String, ControllerV2> controllerMap = new HashMap<>();

    public FrontControllerServletV2() {
        controllerMap.put("/front-controller/v2/members/new-form", new MemberFormControllerV2());
        controllerMap.put("/front-controller/v2/members/save", new MemberSaveControllerV2());
        controllerMap.put("/front-controller/v2/members", new MemberListControllerV2());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        // /front-controller/V2/members
        String requestURI = request.getRequestURI();

        ControllerV2 controller = controllerMap.get(requestURI);
        if(controller == null){
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        MyView view = controller.process(request, response);
        view.render(request, response);
    }
}
```

- V1과 크게 변하지는 않았지만 `view.render(request, response)`를 통해 데이터 흐름을 이동시키고 있다
- 즉 `MyView view` **객체를 활용해 중복된 코드를 줄이고 역할을 위임시켰다.**
</aside>

## **V2 -** MyView

<aside>
✍️ **NOTE**

```java
public class MyView {
    private String viewPath;

    public MyView(String viewPath) {
        this.viewPath = viewPath;
    }

    public void **render**(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

- `MyView` 클래스는 `View`와 관련된 로직만을 수행하는 객체이다
- 저장하고 있는 경로를 통해 데이터 흐름을 넘기는 작업을 하며, 여기서 구현되어 있지 않지만, 때에 따라 `prefix`와 `suffix`를 분리하여 공통으로 관리할 수 있다.
</aside>

## **V2 - ControllerV2**

<aside>
✍️ **NOTE**

```java
public class MemberFormControllerV2 implements ControllerV2 {
    @Override
    public MyView process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        return new MyView("/WEB-INF/views/new-form.jsp");
    }
}
```

- View와 관련된 로직은 MyView에서 처리하므로 경로를 넘겨주어 반환시키도록 변환
</aside>

## **V2 - V1 회원등록 폼 비교**

<aside>
✍️ **NOTE**

```java
// V1 
@Override
public void process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    String viewPath = "/WEB-INF/views/new-form.jsp";
    RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
    dispatcher.forward(request, response);
}

// V2
@Override
public MyView process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    return new MyView("/WEB-INF/views/new-form.jsp");
}
```

</aside>