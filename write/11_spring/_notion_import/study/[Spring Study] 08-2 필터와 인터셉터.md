# [Spring Study] 08-2. 필터와 인터셉터

주제: Spring Study
연관 노트: [Spring Security] 01-1. Spring Security 개념 ⭐ (https://www.notion.so/Spring-Security-01-1-Spring-Security-42ec449ed49b426caff25e4decf511e5?pvs=21), [Spring Study] 04. 스프링 MVC 흐름 (https://www.notion.so/Spring-Study-04-MVC-75e00aab0b564fd2b6707d4edfb9add4?pvs=21)

- 참고
    
    [[Spring] 필터(Filter) vs 인터셉터(Interceptor) 차이 및 용도 - (1)](https://mangkyu.tistory.com/173)
    
    [Spring Interceptor, 제대로 이해하기](https://gngsn.tistory.com/153)
    
    [[Spring MVC] [2] 7. 로그인 처리2 - 필터, 인터셉터](https://velog.io/@dbsrud11/Spring-MVC-2-7.-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%B2%98%EB%A6%AC2-%ED%95%84%ED%84%B0-%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0)
    
    [[Spring] Filter, Interceptor, AOP](https://velog.io/@soyeon207/Spring-Filter-Interceptor-AOP)
    

# **스프링 필터**

---

<aside>
💡 **NOTE**

> *필터는 디스패쳐 서블릿에 요청이 전달되기 전/후에 URL패턴에 맞는 모든 요청에 대한 부가작업을 처리할 수 있는 기능을 제공합니다.*
> 

디스패쳐 서블릿은 스프링의 가장 앞단에 존재하는 프론트 컨트롤러이므로, 필터는 스프링 범위 밖에서 처리가 되는 것이며 즉 스프링이 아닌 톰캣과 같은 웹 컨테이너에 의해 관리가 됩니다.

![Untitled](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled.png)

- Servlet이 스프링 외부에서 관리되어 스프링에서 관리가 불가능하다고 생각할 수 있지만 이는 이후 DelegatingFilterProxy의 개념을 통해 가능해진다.
</aside>

## 필터 구현 및 등록

<aside>
✍️ **NOTE**

```java
public interface Filter {

		// init: 필터 객체를 초기화하고 서비스에 추가(최초 1번)
    public default void init(FilterConfig filterConfig) throws ServletException {}

		// doFilter: url-pattern에 맞는 모든 HTTP 요청이 디스패쳐 서블릿에 전달되기 전
		// 웹 컨테이너에 의해 실행
    public void doFilter(ServletRequest request, 
										     ServletResponse response,
                         FilterChain chain // 다음 필터 호출
                         ) throws IOException, ServletException;

		// destroy: 필터 객체를 서비스에서 제거하고 자원반환
    public default void destroy() {}
}
```

Filter 실습을 위해 간단한 Log를 찍을 수 있는 LogFilter를 구현합니다. 각 생명주기 별로 log 메서드를 추가해서 어떻게 동작하는지 알아봅시다.

```java
@Slf4j
public class LogFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        log.info("로그: log filter init");
    }

    @Override
    public void doFilter(ServletRequest request, 
                         ServletResponse response, 
                         FilterChain chain
    ) throws IOException, ServletException {
        
        log.info("로그: log filter doFilter");
        HttpServletRequest httpRequest = (HttpServletRequest) request;

        String requestURI = httpRequest.getRequestURI();
        httpRequest.setAttribute("change", "Filter");

        String uuid = UUID.randomUUID().toString();

        log.info("로그: REQUEST [{}][{}]", uuid, requestURI);
        chain.doFilter(request, response);
        log.info("로그: RESPONSE [{}][{}]", uuid, requestURI);
    }

    @Override
    public void destroy() {
        log.info("로그: log filter destroy");
    }
}
```

위에서 생성한 필터를 등록하기 위해 WebConfig의 빈에 추가합니다.

```java
@Configuration
public class WebConfig {

    @Bean
    public FilterRegistrationBean<Filter> logFilter(){
        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
        // 필터 인스턴스 설정
        filterRegistrationBean.setFilter(new LogFilter());
        
        // 필터 실행 순서 설정 (1이면 가장 먼저 실행됨)
        filterRegistrationBean.setOrder(1);
        
        // 필터가 적용될 URL 패턴 설정 (모든 요청에 대해 필터 적용)
        filterRegistrationBean.addUrlPatterns("/*");

        // 필터의 이름 설정
        filterRegistrationBean.setName("LoggingFilter");

        // 필터 활성화 설정 (true로 설정하면 필터 활성화)
        filterRegistrationBean.setEnabled(true);

        return filterRegistrationBean;
    }
}
```

</aside>

## 필터 실습(로그인)

<aside>
✍️ **NOTE**

```java
@Slf4j
public class LoginCheckFilter implements Filter {

    // 인증필터의 URL (해당 경로를 제외하고 필터 적용)
    private static final String[] whiteList= {"/", "/members/add",  "/login", "/logout", "/css/*"};

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        String requestURI = httpRequest.getRequestURI();

        HttpServletResponse httpResponse = (HttpServletResponse) response;

        try{
            log.info("인증 체크 필터 시작 {}", requestURI);

            if(isLoginCheckPath(requestURI)){
                log.info("인증 체크 로직 실행 {}", requestURI);
                HttpSession session = httpRequest.getSession(false);

                if(session == null || session.getAttribute("Login") == null){
                    log.info("미인증 사용자 요청 {}", requestURI);
                    httpResponse.sendRedirect("/login?redirectURL=" + requestURI);
                    return;
                }
            }

            chain.doFilter(request, response);

        }catch (Exception e){
            throw e; // 예외 로깅 가능 하지만, 톰캣까지 예외를 보내주어야함
        }finally {
            log.info("인증 체크 필터 종료 {}", requestURI);
        }
    }

		// 
    private boolean isLoginCheckPath(String requestURI){
        return !PatternMatchUtils.simpleMatch(whiteList, requestURI);
    }
}
```

```java
@Configuration
public class WebConfig {
		// ...		

    @Bean
    public FilterRegistrationBean loginCheckFilter(){
        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setFilter(new LoginCheckFilter());
        filterRegistrationBean.setOrder(2);
        filterRegistrationBean.addUrlPatterㅁns("/*");

        return filterRegistrationBean;
    }
}
```

- 특정 URL을 제외하는 로직이 Filter를 등록할때 작성하지 않은 이유는 FilterRegistrationBean에서 특정 URL을 제외하는 패턴을 설정하는 것을 지원하지 않기 때문입니다.
</aside>

# 스프링 인터셉터

---

<aside>
💡 **NOTE**

> *인터셉터는 필터와 달리 Spring이 제공하는 기술로써, **디스패쳐 서블릿이 컨트롤러를 호출하기 전과 후에 요청과 응답을 참조하거나 가공할 수 있는 기능을 제공합니다.***
> 

디스패처 서블릿은 핸들러 매핑을 통해 적절한 컨트롤러를 찾아 요청하며, 이에 대한 결과로 `HandlerExecutionChain`이라는 실행 체인을 반환합니다. 이 실행 체인에는 1개 이상의 인터셉터가 등록되어 있을 경우, 순차적으로 인터셉터를 거쳐 컨트롤러가 실행됩니다. 인터셉터가 없다면, 컨트롤러는 바로 실행됩니다.

![Untitled](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled%201.png)

</aside>

## 스프링 인터셉터 흐름

<aside>
✍️ **NOTE**

![스프링 인터셉터 흐름](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled%202.png)

스프링 인터셉터 흐름

- 스프링 인터셉터는 `DispatcherServlet` - `Controller` 사이에서 호출됩니다.
- 스프링 인터셉터는 체인으로 구성되며, 중간에 인터셉터를 자유롭게 추가할 수 있습니다.
- 기본적으로 필터보다 더 많은 기능을 제공하며, 대표적으로 URL패턴의 경우 더 세밀하게 설정이 가능합니다.

![Untitled](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled%203.png)

- `afterCompletion`의 경우 예외가 발생해도 항상 호출되므로 finally의 개념을 가집니다.
</aside>

## 인터셉터 구현 및 등록

<aside>
✍️ **NOTE**

```java
public interface HandlerInterceptor {

		// preHandle: 컨트롤러 호출이전 (반환값이 false이면 다음 작업이 막힘)
    default boolean preHandle(HttpServletRequest request, 
													    HttpServletResponse response, 
													    Object handler
													    ) throws Exception {
        return true;
    }

		// postHandle: 컨트롤러 호출이후 
		// ModelAndView 후처리가 가능하나 요즘은 Json을 사용해서 자주 쓰이지 않는다.
    default void postHandle(HttpServletRequest request, 
												    HttpServletResponse response, 
												    Object handler,
                            @Nullable ModelAndView modelAndView
                            ) throws Exception {
    }

		// afterCompletion: 모든 작업이 완료된후 실행
		// 요청 처리중에 사용한 리소스 반환에 자주 사용한다.
    default void afterCompletion(HttpServletRequest request, 
														     HttpServletResponse response, 
														     Object handler,
                                 @Nullable Exception ex
                                 ) throws Exception {
    }
}
```

```java
@Slf4j
public class LogInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {
                             
        String uuid = UUID.randomUUID().toString();

        // Request 속성 지정
        request.setAttribute("change", "Filter");
        request.setAttribute("uuid", uuid);

        // Response Header 조작
        response.setHeader("Change Interceptor Header", "Interceptor");
        response.setHeader("Change Interceptor DateHeader", "Interceptor2");

        log.info("Pre Handle method is Calling: REQUEST [{}][{}]", uuid, request.getRequestURI());
        return true; // true 반환하여 요청 처리 계속
    }

    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler,
                           ModelAndView modelAndView) throws Exception {
                           
        String uuid = (String) request.getAttribute("uuid");
        log.info("Post Handle method is Calling: HANDLED [{}][{}]", uuid, request.getRequestURI());
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex)throws Exception {

        String uuid = (String) request.getAttribute("uuid");
        log.info("Request and Response is completed: RESPONSE [{}][{}]", uuid, request.getRequestURI());
    }
}
```

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    // ...

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 인터셉터 생성 및 등록
        HandlerInterceptor loggingInterceptor = new LogInterceptor();

        registry.addInterceptor(loggingInterceptor)
					      // 모든 요청에 인터셉터 적용
                .addPathPatterns("/**")
                // 로그인과 로그아웃 경로는 제외
                .excludePathPatterns("/login/**", "/logout/**")
                // 인터셉터의 실행 순서 설정
                .order(1);
    }
}
```

</aside>

![Untitled](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled%204.png)

## 실습결과

<aside>
✍️ **NOTE**

![Header값에 관한 수정 혹은 Request에 속성값 추가는 Filter와 Interceptor 2개 모두 큰차이가 없다.](%5BSpring%20Study%5D%2008-2%20%ED%95%84%ED%84%B0%EC%99%80%20%EC%9D%B8%ED%84%B0%EC%85%89%ED%84%B0/Untitled%205.png)

Header값에 관한 수정 혹은 Request에 속성값 추가는 Filter와 Interceptor 2개 모두 큰차이가 없다.

</aside>