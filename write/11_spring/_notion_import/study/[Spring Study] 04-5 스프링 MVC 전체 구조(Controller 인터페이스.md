# [Spring Study] 04-5. 스프링 MVC 전체 구조(Controller 인터페이스, 뷰 리졸버) ⭐

주제: Spring Study

- 참고
    
    [[Spring MVC] Dispatcher Servlet 이란? -(FrontController패턴 포함)](https://devmoony.tistory.com/102)
    
    [Reflection, 프론트 컨트롤러 패턴, DI](https://charactermail.tistory.com/432)
    
    [](https://github.com/backend-sprout/spring-mvc-1/blob/main/05%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/01%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0.md)
    
    [spring-mvc-1/02 핸들러 매핑과 핸들러 어댑터.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/05%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/02%20%ED%95%B8%EB%93%A4%EB%9F%AC%20%EB%A7%A4%ED%95%91%EA%B3%BC%20%ED%95%B8%EB%93%A4%EB%9F%AC%20%EC%96%B4%EB%8C%91%ED%84%B0.md)
    
    [spring-mvc-1/03 뷰 리졸버.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/05%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/03%20%EB%B7%B0%20%EB%A6%AC%EC%A1%B8%EB%B2%84.md)
    

# **스프링 MVC 전체 구조**

---

<aside>
💡 **NOTE**

> ***직접 만든 MVC 프레임워크 와 스프링 MVC 프레임워크의 구조는 아래와 같다.***
> 

![직접 만든 MVC 프레임워크](%5BSpring%20Study%5D%2004-5%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0(Controller%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4/Untitled.png)

직접 만든 MVC 프레임워크

![스프링 MVC 프레임워크](%5BSpring%20Study%5D%2004-5%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0(Controller%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4/Untitled%201.png)

스프링 MVC 프레임워크

</aside>

# **DispathcerServlet**

---

<aside>
💡 **NOTE**

> ***스프링 MVC도 프론트 컨트롤러 패턴으로 구현되어 있다
스프링 MVC의 FrontController → DispatcherServlet***
> 

![DispatcherServlet 구조](%5BSpring%20Study%5D%2004-5%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0(Controller%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4/Untitled%202.png)

DispatcherServlet 구조

- DispathcerServlet도 HttpServlet을 상속받아서 사용하며 Servlet으로서 동작한다
- 스프링 부트는 `DispatcherServlet`을 `Servelt`으로 자동으로 등록하면서 모든경로( urlPatterns=”/”)에 대해서 맵핑한다
</aside>

## **요청 흐름**

<aside>
✍️ **NOTE**

1. Servlet이 호출되면 HttpServlet이 제공하는 service()가 호출된다
2. 스프링 MVC는 DispathcerServlet의 부모인 FrameworkServlet에서 `service()`를 overriding 해두었다
3. FrameworkServlet.service()를 시작으로 여러 메서드가 호출되면서 DispatcherServlet.doDispatch()가 호출된다.

### **DispatcherServlet.doDispatch() 핵심 로직 분석**

```java
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
    HttpServletRequest processedRequest = request;
    HandlerExecutionChain mappedHandler = null;
    ModelAndView mv = null;
    
		// 1. 핸들러 조회
   mappedHandler = getHandler(processedRequest);
    if (mappedHandler == null) {
        noHandlerFound(processedRequest, response);
        return;
    }
    
		// 2. 핸들러 어댑터 조회( 핸들러 처리할 수 있는 어댑터)
    HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());  

    // 3. 핸들러 어댑터 실행
		// 4. 핸들러 어댑터를 통해 핸들러 실행
		// 5. ModelAndView 반환
    mv = ha.handle(processedRequest, response, mappedHandler.getHandler());     

    processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);
}
    
private void processDispatchResult(HttpServletRequest request, HttpServletResponse response, HandlerExecutionChain mappedHandler, ModelAndView mv, Exception exception) throws Exception {
     // 뷰 렌더링 호출
		render(mv, request, response); 
}

protected void render(ModelAndView mv, HttpServletRequest request, HttpServletResponse response) throws Exception {
    View view;

		// 6. 뷰 리졸버를 통해서 뷰 찾기
		// 7. View 반환
    String viewName = mv.getViewName();
    view = resolveViewName(viewName, mv.getModelInternal(), locale, request);  
 
		 // 8. 뷰 렌더링
    view.render(mv.getModelInternal(), request, response); 
```

1. 핸들러 조회  : 핸들러 매핑을 통해 요청 URL에 매핑된 핸들러(컨트롤러)를 조회함
2. 핸들러 어댑터 조회 : 핸들러를 실행할 수 있는 핸들러 어댑터 조회한다
3. 핸들러 어댑터 실행
4. 핸들러 실행
5. ModelAndVIew 반환 : 핸들러 어댑터는 핸들러가 반환하는 정보를 `ModelAndView`로 변환해서 반환 (`ModelView` 생각)
6. viewResolver 호출 
7. View 반환 : `viewResolver`는 `view`의 논리 이름을 물리 이름으로 변경하고 렌더링 역할을 담당하는 `view` 객체를 반환한다
`Jsp`의 경우 `InternalResourceView(JstlView)`를 반환하는데, 내부에 `foward() 로직`이 존재
8. View 렌더링 : view를 통해서 view를 렌더링함
</aside>

## **인터페이스 살펴보기**

<aside>
✍️ **NOTE**

> ***인터페이스들만 구현해서 DispatcherServlet에 등록하면 자신만의 Controller를 만들 수도 있다!***
> 
- **핸들러 매핑:**
    - `org.springframework.web.servlet.HandlerMapping`
- **핸들러 어댑터:**
    - `org.springframework.web.servlet.HandlerAdapter`
- **뷰 리졸버:**
    - `org.springframework.web.servlet.ViewResolver`
- **뷰:**
    - `org.springframework.web.servlet.View`
</aside>

# **Controller 인터페이스**

---

<aside>
💡 **NOTE**

> ***Controller 인터페이스는 @Controller 어노테이션과 전혀 다르다!***
> 
- **Controller 인터페이스**
    - 과거 버전의 스프링 컨트롤러 인터페이스
- 빈의 이름으로 URL을 매핑할 것이다.
</aside>

## Controller 인터페이스

<aside>
✍️ **NOTE**

```java
// 스프링 빈 이름을 URL에 맞추었다.
@Component("/springmvc/old-controller")
public class OldController implements Controller {

    @Override
    public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response) throws Exception {
        System.out.println("OldController.handleRequest");
        return null;
    }

}
```

- **컨트롤러가 호출되려면 다음 2가지가 필요하다**
    - `HandlerMapping(핸들러 매핑)`
        - 핸들러 매핑에서 컨트롤러를 찾을 수 있어야함
        - 스프링 빈의 이름으로 핸들러를 찾을 수 있는 핸들러 매핑이 필요하다
    - `HandlerAdapter(핸들러 어댑터)`
        - 핸들러 매핑을 통해서 찾은 핸들러를 실행할 수 있는 핸들러 어댑터가 필요하다
        - Contorller 인터페이스를 실행할 수 있는 핸들러 어댑터를 찾고 실행해야 한다

![핸들러 맵핑/어댑터의 우선순위](%5BSpring%20Study%5D%2004-5%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0(Controller%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4/Untitled%203.png)

핸들러 맵핑/어댑터의 우선순위

- 핸들러 매핑도, 핸들러 어댑터도 모두 순서대로 찾고 없다면 다음 순서로 넘어간다
    - url을 기준으로 RequestMappingHandlerMapping에서 찾는데 없다?
    - BeanNameUrlHandleMapping에서 찾음

1. **Handler Mapping으로 조회**
    1. HandlerMapping을 순서대로 실행해서 핸들러 찾음
    2. 하지만 지금 버전(옛날기준) 빈 이름으로 찾는데 성공하고 핸들러 OldController 반환
2. **Handler Adapter 조회**
    1. HandlerAdapter의 supports()를 호출
    2. SimpleControllerHandlerAdapter가 Controller 인터페이스를 지원하므로 대상이됨
3. **Handler Adapter 실행**
    1. DispatcherServlet이 조회한 SimpleControllerHandlerAdapter를 실행하면서 핸들러 정보를 함께 넘겨준다
    2. SimpleControllerHandlerAdapter는 OldController를 내부에서 실행하고 결과반환

---

- **정리**
    - **`OldController`를 실행하면 다음과 같이 사용됨**
        - `HandlerMapping = BeanNameUrlHandlerMapping`
        - `HandlerAdapter = SimpleControllerHandlerAdapter`
    - **@RequestMapping**
        - 가장 우선순위가 높은 핸들러 매핑과 핸들러 어댑터는 `RequestMappingHandlerMapping`, `RequestMappingHandlerAdapter` 이다
        - 이것이 바로 지금 실무에서 사용하는 어노테이션 기반의 컨트롤러를 지원하는 매핑과 어댑터이다.
</aside>

# **뷰 리졸버 설정**

---

<aside>
💡 **NOTE**

```java
@Component("/springmvc/old-controller")
public class OldController implements Controller {

    @Override
    public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response) throws Exception {
    System.out.println("OldController.handleRequest");
        return new ModelAndView("new-form");
    }
}
```

- 위 코드를 기준으로 실제 접근시 Whiteable Error Page가 나오고 콘솔에 `OldController.handleRequest`가 호출된다
- 즉 이전에 만들었던 `ViewResolver`와 같은 동작이 **Spring MVC 내부적으로 이루어지지 않았다는 이야기다**

```java
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

- 위와 같은 설정을 추가하면 그제서야 동작하는데 이유가 뭘까?

- 스프링 부트는 `InternalResourceViewResolver`라는 뷰 리졸버를 자동으로 등록하는데 이때 `application.properties`에 등록한 `spring.mvc.view.prefix`, `spring.mvc.view.suffix` 설정 정보를 사용해서 등록한다.
- 사실 이 부분은 스프링 부트의 `AutoConfiguration`으로 인해 적용되는 것이기에 스프링 레거시를 사용하면 별도의 빈을 등록하고 적용시켜줘야 한다

---

- **[참고]**
    - `return new ModelAndView("/WEB-INF/views/new-form.jsp");`
    - 이와 같이 전체경로를 주면 동작을 하긴한다 (권장하지 않음)
</aside>

## **뷰 리졸버 동작 방식**

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Study%5D%2004-5%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20%EC%A0%84%EC%B2%B4%20%EA%B5%AC%EC%A1%B0(Controller%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4/Untitled%204.png)

- 위 코드가 기반이기에 InterResourceViewResolver가 등록된 것이다
- 즉 다른 템플릿에 대한 라이브러리를 의존 받으면 다른 Resolver가 등록된다.

1. **Handler Adapter 호출**
    1. 핸들러 어댑터를 통해 new-form이라는 논리-뷰 이름을 얻음
2. **ViewResolver 호출**
    1. new-form 이라는 뷰 이름으로 `viewResolver`를 순서대로 호출한다
    2. `BeanNameViewResolver`는 new-form이라는 이름의 스프링 빈으로 등록된 뷰를 찾는다 (만약 없다면 `InternalResourceViewResolver`를 호출)
3. **InternalResourceVIewResolver**
    1. JSP와 관련된 뷰 리졸버로 JSP와 관련된 InternalResourceView 반환
4. **뷰 - InternalResourceView**
    1. `InternalResourceView`는 JSP처럼 포워드 `forward()`를 호출해서 처리할 수 있는 경우에 사용한다.
5.  **view.render()**
    1. `view.render()`가 호출되고 `InternalResourceView` 는 `forward()`를 사용해서 JSP를 실행한다.`InternalResourceView`를 기준으로는 `renderMergeOuputModel()` 메서드다.

---

- **[참고]**
    - 다른 뷰는 실제 뷰를 렌더링하지만 JSP의 경우 foward()를 통해서 해당 JSP로 이동(실행)해야 렌더링이 된다
        - JSP를 제외한 나머지 뷰 템플릿들은 foward()과정 없이 바로 렌더링됨
    - Thymeleaf 뷰 템플릿을 사용하면 `ThymeleafViewResolver` 를 등록해야 한다.
    최근에는 라이브러리만 추가하면 스프링 부트가 이런 작업도 모두 자동화해준다.
</aside>