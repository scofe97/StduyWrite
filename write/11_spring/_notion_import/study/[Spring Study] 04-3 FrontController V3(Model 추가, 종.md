# [Spring Study] 04-3. FrontController V3(Model 추가, 종속성 제거)~V4(단순화)

주제: Spring Study

- 참고
    
    [spring-mvc-1/03 프론트 컨트롤러 - V3.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/04%20MVC%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%20%EB%A7%8C%EB%93%A4%EA%B8%B0/03%20%ED%94%84%EB%A1%A0%ED%8A%B8%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20-%20V3.md)
    
    [spring-mvc-1/04 프론트 컨트롤러 - V4.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/04%20MVC%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%20%EB%A7%8C%EB%93%A4%EA%B8%B0/04%20%ED%94%84%EB%A1%A0%ED%8A%B8%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20-%20V4.md)
    

# FrontController - V3

---

<aside>
💡 **NOTE**

> ***Model 추가, ViewModel 추가
HttpServletRequest/HttpServletResp onse Servlet 종속성 코드 제거***
> 

![`Servlet` 종속성 제거를 위해 `Model`를 만들고 `View` 이름까지 전달하는 객체 `ModelView`를 만들어보자!](%5BSpring%20Study%5D%2004-3%20FrontController%20V3(Model%20%EC%B6%94%EA%B0%80,%20%EC%A2%85/Untitled.png)

`Servlet` 종속성 제거를 위해 `Model`를 만들고 `View` 이름까지 전달하는 객체 `ModelView`를 만들어보자!

- **Controller는 HttpServletRequest, HttpServletResponse는 필요하지 않다**
    - Controller는 요청 파라미터 정보만 필요하기에 `Map<String, String>` 객체만 넘겨주면 된다
    - request가 없기에 별도의 Model객체를 만들어서 반환하는 구조로 가지도록 해야한다.
- Controller는 파라미터 데이터를 이용하여 비즈니스 로직을 수행하고 결과값을 ModelView 객체에 `Map<String, String>`형식으로 View 경로와 함께 저장한 후 반환한다.
</aside>

## V3 - FrontController

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "frontControllerServletV3", urlPatterns = "/front-controller/v3/*")
public class FrontControllerServletV3 extends HttpServlet {

    private Map<String, ControllerV3> controllerMap = new HashMap<>();

    public FrontControllerServletV3() {
        controllerMap.put("/front-controller/v3/members/new-form", new MemberFormControllerV3());
        controllerMap.put("/front-controller/v3/members/save", new MemberSaveControllerV3());
        controllerMap.put("/front-controller/v3/members", new MemberListControllerV3());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String requestURI = request.getRequestURI();

        ControllerV3 controller = controllerMap.get(requestURI);
        if (controller == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

				// Controller에서 request의 parameter를 Map으로 전해준다
        ModelView modelView = controller.process(paramMap(request));

				// 이후 Controller에서 ModelView에 경로와 값을 저장하고 반환
        MyView myView = viewResolver(modelView.viewName());

				// 반환받은 ModelView의 viewName으로 render 실행
        myView.render(modelView.model(), request, response);
    }

    private Map<String, String> paramMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }

    private MyView **viewResolver**(String viewName) {
        return new MyView("/WEB-INF/views/" + viewName + ".jsp");
    }
}
```

- **파라미터 데이터 추출 (paramMap)**
    - **`createParamMap()`**
    - `FrontController`에서는 `HttpServletRequest request`를 활용해서 `Map<String, String> paramMap`에 파라미터 이름과 그 값을 매핑하여 저장시키고 있다
    - 생성된 `paramMap`을 `controller`에 주입시켜 `Model`값과 `ViewName`을 가진 `ModelView`를 반환하도록 한다
    - 이때 반환된 `ViewName`은 단순한 경로만을 나타낸다 (prefix와 suffix를 가지 않은 경로)

- **뷰 리졸버 (경로반환)**
    - `MyView view = viewResolve(viewName)`
    - Controller가 반환한 논리 뷰 이름을 실제 물리 뮤 경로로 변경하고 실제 물리 경로가 있는 MyView 객체를 반환한다
        - 논리 뷰 이름 : `members`
        - 물리 뷰 경로 : `/WEB-INF/views/members``.jsp`

- **렌더링 작업 (request값 다 넘기고 이동)**
    - `view.render(mv.getModel(), request, response)`
    - MyView를 통해서 HTML 화면 렌더링
    - MyView의 render()는 Model 정보도 함께 받는다.
    - Model 정보는 내부에서 request.setAttribute()로 담아둔다.
</aside>

## V3 - **MyView**

<aside>
✍️ **NOTE**

```java
public class MyView {
    private String viewPath;

    public MyView(String viewPath) {
        this.viewPath = viewPath;
    }

    public void render(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        RequestDispatcher requestDispatcher = request.getRequestDispatcher(viewPath);
        requestDispatcher.forward(request, response);
    }

    public void **render(Map<String, Object> model, HttpServletRequest request, HttpServletResponse response)** throws ServletException, IOException {
	     // 넘어온 데이터를 전부 request에 넣어줌
			 **modelToRequestAttribute(model, request);**

        RequestDispatcher requestDispatcher = request.getRequestDispatcher(viewPath);
        requestDispatcher.forward(request, response);
    }

    private void modelToRequestAttribute(Map<String, Object> model, HttpServletRequest request) {
        model.forEach((key, value) -> request.setAttribute(key, value));
    }
    
}
```

- MyView는 request.setAttribute를 사용하여 데이터를 저장하고 뷰로 데이터 흐름을 이동시킨다.
</aside>

## V3 - **ModelView**

<aside>
✍️ **NOTE**

```java
public class ModelView {

    private String viewName;
    private Map<String, Object> model = new HashMap<>();

    public ModelView(String viewName) {
        this.viewName = viewName;
    }

    public String getViewName() {
        return viewName;
    }

    public void setViewName(String viewName) {
        this.viewName = viewName;
    }

    public Map<String, Object> getModel() {
        return model;
    }

    public void setModel(Map<String, Object> model) {
        this.model = model;
    }
}
```

</aside>

## V3 - **Controller 인터페이스**

<aside>
✍️ **NOTE**

```java
public interface ControllerV3 {
    ModelView process(Map<String, String> paramMap);
}
```

- 응답 결과로 뷰 이름과 뷰에 전달할 `Model` 데이터를 포함하는 `ModelView` 객체를 반환하면 된다.
</aside>

## V3 - V2 회원저장 코드 비교

<aside>
✍️ **NOTE**

```java
@Override
public MyView process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 데이터 저장
    String username = request.getParameter("username");
    int age = Integer.parseInt(request.getParameter("age"));

    Member member = new Member(username, age);
    memberRepository.save(member);
    
    // Model에 데이터 보관  
    request.setAttribute("member", member);
    
    // View 경로를 저장하는 MyView 반환 
    return new MyView("/WEB-INF/views/save-result.jsp");
}

// V3
@Override
public ModelView process(Map<String, String> paramMap) {

		// Request의 데이터를 꺼내서 작업
    String username = paramMap.get("username");
    int age = Integer.parseInt(paramMap.get("age"));

    Member member = new Member(username, age);
    memberRepository.save(member);

		// 반환값을 가지고 ModelView 생성이후 반환
    ModelView modelView = new ModelView("save-result");
    modelView.getModel().put("member", member);
    return modelView;
}
```

- 응답 결과로 뷰 이름과 뷰에 전달할 Model 데이터를 포함하는 ModelView 객체를 반환하면 된다.
</aside>

# FrontController - V4

---

<aside>
💡 **NOTE**

> ***단순하고 실용적인 컨트롤러***
> 

![기본 V3와 매우 비슷한 구조이지만, `Controller`에게 파라미터 정보는 물론 `Model`정보까지 넘겨준다](%5BSpring%20Study%5D%2004-3%20FrontController%20V3(Model%20%EC%B6%94%EA%B0%80,%20%EC%A2%85/Untitled%201.png)

기본 V3와 매우 비슷한 구조이지만, `Controller`에게 파라미터 정보는 물론 `Model`정보까지 넘겨준다

- V3 Controller는 Servlet 종속성을 제거하고 View 경로의 중복을 제거하는 등 잘 설계된  Controller다
- 좋은 프레임워크는 아키텍쳐도 중요하지만, 개발자가 단순하고 편리하게 사용할 수 있어야 한다.
    - **v3를 변형해서 개발자가 편리하게 개발하도록 설계한다.**
</aside>

## V4 - **FrontController**

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "frontControllerServletV4", urlPatterns = "/front-controller/v4/*")
public class FrontControllerServletV4 extends HttpServlet {

    private Map<String, ControllerV4> controllerMap = new HashMap<>();

    public FrontControllerServletV4() {
        controllerMap.put("/front-controller/v4/members/new-form", new MemberFormControllerV4());
        controllerMap.put("/front-controller/v4/members/save", new MemberSaveControllerV4());
        controllerMap.put("/front-controller/v4/members", new MemberListControllerV4());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String requestURI = request.getRequestURI();
        ControllerV4 controller = controllerMap.get(requestURI);
        if (controller == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        Map<String, String> paramMap = paramMap(request); // 파라미터 값들
        Map<String, Object> model = new HashMap<>(); // 여기다 데이터 담음
        String viewName = controller.process(paramMap, model); // 주소만 반환

        MyView myView = viewResolver(viewName);
        myView.render(model, request, response);
    }

    private Map<String, String> paramMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }

    private MyView viewResolver(String viewName) {
        return new MyView("/WEB-INF/views/" + viewName + ".jsp");
    }
}
```

- `FrontController`에서 `Map<String, Object> model = new HashMap<>();` 을 통해 모델 객체를 생성한다 (request 역활)
- 기존과는 다르게 `Controller`에게 모델을 넘겨주어 `Controller`에서 모델에 값을 넣는 방식으로 취한다.
- 또한 `Controller`는 `View` 경로만 반환하면 되므로 이를 이용해 `ViewResolver`도 손쉽게 호출 가능하게 한다.
</aside>

## V4 - V3 **회원 저장 비교**

<aside>
✍️ **NOTE**

```java
// V3
@Override
public ModelView process(Map<String, String> paramMap) {
    String username = paramMap.get("username");
    int age = Integer.parseInt(paramMap.get("age"));

    Member member = new Member(username, age);
    memberRepository.save(member);

    ModelView mv = new ModelView("save-result");
    mv.getModel().put("member", member);
    return mv;
}

// V4
@Override
public String process(Map<String, String> paramMap, Map<String, Object> model) {
    String username = paramMap.get("username");
    int age = Integer.parseInt(paramMap.get("age"));

    Member member = new Member(username, age);
    memberRepository.save(member);

    model.put("member", member);
    return "save-result";
}
```

</aside>