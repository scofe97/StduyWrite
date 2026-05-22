# [Spring Study] 04-4. FrontController V5(Adapter 추가)

주제: Spring Study

- 참고
    
    [spring-mvc-1/05 프론트 컨트롤러 - V5.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/04%20MVC%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%20%EB%A7%8C%EB%93%A4%EA%B8%B0/05%20%ED%94%84%EB%A1%A0%ED%8A%B8%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20-%20V5.md)
    

# FrontController **- V5**

---

<aside>
💡 **NOTE**

> ***어떤 상황에서는 V4로 개발하고 어떤 상황에서는 V3방식으로 개발하려고 하면 어떻게 해야할까? → 메서드 시그니처와 상관없이 FrontController와 호환되는 어댑터로 해결***
> 

![**다양한 형태의 인터페이스를 지원하기 위한 `Adapter 패턴`을 접목시킨것이 V5 모델이다**](%5BSpring%20Study%5D%2004-4%20FrontController%20V5(Adapter%20%EC%B6%94%EA%B0%80)/Untitled.png)

**다양한 형태의 인터페이스를 지원하기 위한 `Adapter 패턴`을 접목시킨것이 V5 모델이다**

- **핸들러 어댑터**
    - 중간에 추가도니 어댑터 이름은 핸들러 어댑터이다.
    - 핸들러 어댑터는 연결한 `Controller 메서드` 시그니처에 따라 코드를 알맞게 정의해주는 역할을 한다
- **핸들러**
    - `Controller` 이름을 더 넓은 범위의 핸들러로 변경했다
    - `Controller` 의 개념 뿐만 아니라 어떠한 것이든 해당하는 종류의 어댑터만 있으면 다 처리가 가능하기 때문
</aside>

### FrontController **V5** 코드

<aside>
✍️ **NOTE**

```java
@WebServlet(name = "frontControllerServletV5", urlPatterns ="/front-controller/v5/*" )
public class FrontControllerServletV5 extends HttpServlet {
    private final Map<String, Object> handlerMappingMap = new HashMap<>();
    private final List<MyHandlerAdapter> handlerAdapters = new ArrayList<>();

    public FrontControllerServletV5() {
        initHandlerMappingMap();
        initHandlerAdapters();
    }

		// 여기서 링크에따른 핸들러 조회
    private void **initHandlerMappingMap**() {
        handlerMappingMap.put("/front-controller/v5/v3/members/new-form", new MemberFormControllerV3());
        handlerMappingMap.put("/front-controller/v5/v3/members/save", new MemberSaveControllerV3());
        handlerMappingMap.put("/front-controller/v5/v3/members", new MemberListControllerV3());

        // V4 추가
        handlerMappingMap.put("/front-controller/v5/v4/members/new-form", new MemberFormControllerV3());
        handlerMappingMap.put("/front-controller/v5/v4/members/save", new MemberSaveControllerV3());
        handlerMappingMap.put("/front-controller/v5/v4/members", new MemberListControllerV3());
    }

		// 어댑터 초기화
    private void initHandlerAdapters() {
        handlerAdapters.add(new ControllerV3HandlerAdapter());
        handlerAdapters.add(new ControllerV4HandlerAdapter());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        Object handler = getHandler(request);

        if(handler == null){
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
                                                                                              
        **MyHandlerAdapter adapter = getHandlerAdapter(handler);**

        **ModelView mv = adapter.handle(request, response, handler);**

        String viewName = mv.getViewName();
        MyView view = viewResolver(viewName);

        view.render(mv.getModel(), request, response);
    }

		// 핸들러가 어댑터에 맞는게 있는가 확인
    private MyHandlerAdapter getHandlerAdapter(Object handler) {
        for (MyHandlerAdapter adapter : handlerAdapters) {
            if(adapter.supports(handler)){
                return adapter;
            }
        }

        throw new IllegalArgumentException("handler adapter를 찾을 수 없습니다." + handler);
    }

    private Object getHandler(HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        return handlerMappingMap.get(requestURI);
    }

    private MyView viewResolver(String viewName) {
        return new MyView("/WEB-INF/views/" + viewName + ".jsp");
    }
}
```

- `HandlerMappiong`
    - URL과 매팽되는 핸들러를 조회
- `HandlerAdapter 목록`
    - 핸들러와 알맞는 인터페이스를 지원하는 `HandlerAdapter`를 불러와 실행한다
- `HandlerAdapter`
    - 결과로 반환될 `ModelView`를 통해 모델을 세팅하고 View 렌더링을 진행한다
</aside>

### **MyHandlerAdapter** 코드

<aside>
✍️ **NOTE**

```java
public interface MyHandlerAdapter {
		// 사용가능 여부
    boolean supports(Object handler);

		// ModelView를 반환시킨다
    ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler) throws ServletException, IOException;
}
```

```java
public class ControllerV3HandlerAdapter implements MyHandlerAdapter {

    @Override
    **public boolean supports(Object handler)** {
        return (handler instanceof ControllerV3);
    }

    @Override
    **public ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler)** throws ServletException, IOException {
        ControllerV3 controller = (ControllerV3) handler;
        return controller.process(paramMap(request));
    }

    private Map<String, String> paramMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }
}
```

```java
public class ControllerV4HandlerAdapter implements MyHandlerAdapter {
    @Override
    **public boolean supports(Object handler)** {
        return (handler instanceof ControllerV4);
    }

    @Override
    **public ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler)** throws ServletException, IOException {
        ControllerV4 controller = (ControllerV4) handler;

        Map<String, String> paramMap = createParamMap(request);
        Map<String, Object> model = new HashMap<>();

        String viewName = controller.process(paramMap, model);

        ModelView mv = new ModelView(viewName);
        mv.setModel(model);

        return mv;
    }

    private Map<String, String> createParamMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }

}
```

- **핸들러 어댑터 인터페이스**
    - `Controller`마다 사용하는 시그니처가 달라 구현하는 로직은 다르지만, 최소 수준의 공통 규약을 정해 `FrontController`에서 일관된 로직을 작성할 수 있도록 도와준다.

- **사용 가능 유무 판단 메서드**
    - `boolean support(Object handler)`
    - 어댑터가 해당 Controller(handler)를 처리할 수 있는지 판단하는 메서드
    
- **Controller 로직 실행을 위한 메서드**
    - `ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler)`
    - 어댑터는 실제 컨트롤러를 호출하고, 그 결과로 `ModelView` 반환
    - 실제 `Controller`가 `ModelView`를 반환하지 못하면 어댑터가 만들어서라도 반환해줌
    - 이전에는 `FrontController`가 실제로 `Controller`를 호출했지만 이제는 이 어댑터를 통해서 실제로 `Controller`가 호출됨
</aside>