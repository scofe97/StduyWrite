# [Spring Study] 07-1. 서블릿 예외 처리

주제: Spring Study

- 참고
    
    [[Spring MVC] [2] 8. 예외 처리와 오류 페이지](https://velog.io/@dbsrud11/Spring-MVC-2-8.-%EC%98%88%EC%99%B8-%EC%B2%98%EB%A6%AC%EC%99%80-%EC%98%A4%EB%A5%98-%ED%8E%98%EC%9D%B4%EC%A7%80)
    

# **서블릿 예외 처리**

---

<aside>
💡 **NOTE**

> *웹 애플리케이션에서는 각 요청이 별도의 스레드에서 처리되며, 예외가 발생해 처리되지 않는다면 최종적으로 WAS까지 전달됩니다. 그렇기 때문에 WAS는 이 예외를 어떻게 처리해야할지 결정해야 합니다.*
> 

오류가 발생하면 기본적으로 `/error`로 에러 요청을 다시 전달하도록 WAS(톰캣)를 설정했으며, 톰캣은 500, 404 등의 오류 코드가 발생하면 오류 페이지를 제공하여 어떤 예외가 발생했는지 알려줄 수 있습니다.

```java
@GetMapping("/error-404")
public void error404(HttpServletResponse response) throws IOException {
    response.sendError(404, "404 오류!"); // 상태코드, 에러 메시지
}

@GetMapping("/error-500")
public void error500(HttpServletResponse response) throws IOException {
    response.sendError(500, "내부 서버 오류");
}
```

![톰캣이 제공하는 기본 500에러 페이지](%5BSpring%20Study%5D%2007-1%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC/Untitled.png)

톰캣이 제공하는 기본 500에러 페이지

- `sendError()`를 호출하면, 서블릿 컨테이너는 관련된 HTTP 상태코드에 따른 기본 오류 페이지를 보여줍니다.
</aside>

## **오류 화면 제공**

<aside>
✍️ **NOTE**

> *스프링 부트의 `WebServerCustomizer` 인터페이스를 구현하면 오류 상황에 대한 맞춤형 예외 페이지를 손쉽게 설정할 수 있습니다.*
> 

```java
@Component
public class WebServerCustomizer implements WebServerFactoryCustomizer<ConfigurableWebServerFactory> {

    @Override
    public void customize(ConfigurableWebServerFactory factory) {
		    // 예외 페이지 등록 (404, 500)
        ErrorPage errorPage404 = new ErrorPage(HttpStatus.NOT_FOUND, "/error-page/404");
        ErrorPage errorPage500 = new (HttpStatus.INTERNAL_SERVER_ERROR, "/error-page/500");

				// 특정 예외의 페이지 등록
        ErrorPage errorPageEx = new (RuntimeException.class, "/error-page/500");

				// 페이지 등록
        factory.addErrorPages(errorPage404, errorPage500, errorPageEx);
    }
}
```

- 서블릿은 `Exception`이 발생하여 서블릿 밖으로 전달되거나 `response.sendError()`가 호출되었을 때, 상황에 맞는 오류 처리 기능을 제공합니다.
- 서블릿은 `Exception`이 밖으로 전달되거나 `response.sendError()`가 호출되었을 때 설정된 오류 페이지를 찾습니다.

```java
@Slf4j
@Controller
public class ErrorPageController {

    //RequestDispatcher 상수로 정의되어 있음
    public static final String ERROR_EXCEPTION = "javax.servlet.error.exception";
    public static final String ERROR_EXCEPTION_TYPE = "javax.servlet.error.exception_type";
    public static final String ERROR_MESSAGE = "javax.servlet.error.message";
    public static final String ERROR_REQUEST_URI = "javax.servlet.error.request_uri";
    public static final String ERROR_SERVLET_NAME = "javax.servlet.error.servlet_name";
    public static final String ERROR_STATUS_CODE = "javax.servlet.error.status_code";

    @RequestMapping("/error-page/404")
    public String errorPage404(HttpServletRequest request, HttpServletResponse response) {
        log.info("errorPage 404");
        printErrorInfo(request);
        return "error-page/404";
    }

    @RequestMapping("/error-page/500")
    public String errorPage500(HttpServletRequest request, HttpServletResponse response) {
        log.info("errorPage 500");
        printErrorInfo(request);
        return "error-page/500";
    }

    private void printErrorInfo(HttpServletRequest request){
        log.info("ERROR_EXCEPTION: {}", request.getAttribute(ERROR_EXCEPTION));
        log.info("ERROR_EXCEPTION_TYPE: {}", request.getAttribute(ERROR_EXCEPTION_TYPE));
        log.info("ERROR_MESSAGE: {}", request.getAttribute(ERROR_MESSAGE));
        log.info("ERROR_REQUEST_URI: {}", request.getAttribute(ERROR_REQUEST_URI));
        log.info("ERROR_SERVLET_NAME: {}", request.getAttribute(ERROR_SERVLET_NAME));
        log.info("ERROR_STATUS_CODE: {}", request.getAttribute(ERROR_STATUS_CODE));
        log.info("dispatchType = {}", request.getDispatcherType());
    }
}
```

![Untitled](%5BSpring%20Study%5D%2007-1%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC/Untitled%201.png)

</aside>

# **스프링 부트 예외 처리**

---

<aside>
💡 **NOTE**

> *스프링 부트는 앞서 진행한 오류 페이지 설정을 간소화하기 위해 `WebServerCustomizer` 인터페이스와 `BasicErrorController`를 사용하여 오류 처리 메커니즘을 제공합니다.*
> 

스프링 부트는 모든 오류를 처리하는 `/error` 경로를 자동으로 설정하며, 이를 위해 `ErrorMvcAutoConfiguration` 클래스가 내부적으로 오류 페이지를 자동으로 등록합니다.

```java
@Configuration(proxyBeanMethods = false)
@EnableWebMvc
public class ErrorMvcAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean(value = ErrorController.class, search = SearchStrategy.CURRENT)
    public BasicErrorController basicErrorController(ErrorAttributes errorAttributes) {
        return new BasicErrorController(errorAttributes);
    }

    // 여기서는 기본적인 ErrorController를 빈으로 등록하는 방법을 보여줍니다.
    // 실제 구현에서는 오류 페이지의 경로 설정, 커스텀 오류 뷰의 등록 등 추가적인 설정이 포함됩니다.
}
```

`BasicErrorController`는 모든 오류 처리를 담당하는 컨트롤러이며, `/error` 경로에 매핑되어, 오류 발생시 해당 경로로 리다이렉트되어 처리합니다.

![스프링에 기본으로 내장된 BasicErrorController](%5BSpring%20Study%5D%2007-1%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC/Untitled%202.png)

스프링에 기본으로 내장된 BasicErrorController

![Untitled](%5BSpring%20Study%5D%2007-1%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC/Untitled%203.png)

`BasicErrorController`는 아래의 정보를 모델에 담아 뷰에 전달합니다. 그러나 클라이언트에게 너무 많은 예외 정보를 노출하는 것은 바람직하지 않으므로, 정보 노출에 대한 설정을 할 수 있습니다.

```java
* timestamp: Fri Feb 05 00:00:00 KST 2021
* status: 400
* error: Bad Request
* exception: org.springframework.validation.BindException
* trace: 예외 trace
* message: Validation failed for object='data'. Error count: 1
* errors: Errors(BindingResult)
* path: 클라이언트 요청 경로 (`/hello`)
```

```java
server.error.include-exception=true
server.error.include-message=on_param
server.error.include-stacktrace=on_param
server.error.include-binding-errors=on_param
```

- `never` : 사용하지 않음
- `always` : 항상 사용
- `on_param` : 파라미터가 있을 때 사용

스프링 부트의 `WebMvcAutoConfiguration`를 통해 스프링은 예외 발생 시에 자동으로 `BasicErrorController`로 에러 처리 요청이 전달됩니다. 이 때 요청이 다시 `/error`로 전달됨을 주목해봅시다.

```yaml
# 예외 전달흐름
WAS(톰캣) -> 필터 -> 서블릿(디스패처 서블릿) -> 인터셉터 -> 컨트롤러

# 컨트롤러 예외 발생
컨트롤러(예외발생) -> 인터셉터 -> 서블릿(디스패처 서블릿) -> 필터 -> WAS(톰캣)

# 전체 흐름
# 최종적으로 BasicErrorController 호출
# 필터, 인터셉터, 디스패쳐 서블릿이 중복적으로 호출된다.
WAS(톰캣) -> 필터 -> 서블릿(디스패처 서블릿) -> 인터셉터 -> 컨트롤러
-> 컨트롤러(예외발생) -> 인터셉터 -> 서블릿(디스패처 서블릿) -> 필터 -> WAS(톰캣)
-> WAS(톰캣) -> 필터 -> 서블릿(디스패처 서블릿) -> 인터셉터 -> 컨트롤러(BasicErrorController)
```

- 기본적인 에러 처리는 결국 에러 컨트롤러를 한 번 더 호출하는 것입니다.
- 이 과정에서 `Filter`와 `Interceptor`가 중복 호출되는데, `Filter`의 경우 서블릿의 `DispatcherType` 요청 타입에 따라서 제어가 가능합니다. 하지만 `Interceptor`는 스프링의 기술이므로 제어가 불가능합니다.
</aside>

## 필터, 인터셉터 중복호출 방지

<aside>
✍️ **NOTE**

> `*Filter`는 서블릿 기술이므로, `Filter` 등록 시에는 호출될 `DispatcherType`을 설정할 수 있습니다. 기본적으로 `REQUEST`의 경우에만 호출되므로, 예외 발생 시의 중복 호출을 방지할 수 있습니다.*
> 

![중복호출 ](%5BSpring%20Study%5D%2007-1%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC/Untitled%204.png)

중복호출 

`Filter`의 경우 기본적으로 `REQEUST` 타입이 적용되어 중복호출이 되지 않지만, 실제로 중복흐름이 발생하는지 확인하는지 확인하려면 `DispatcherType`의 `ERROR`값을 추가로 등록해주면 됩니다.

```java
public enum DispatcherType {
    REQUEST, // 클라이언트 요청
    ERROR  , // 오류 요청
    FORWARD, // 서블릿에서 다른 서블릿 요청
    INCLUDE, // 서블릿에서 다른 서블릿이나 JSP결과 포함
    ASYNC    // 비동기 서블릿 호출
}
```

```java
@Configuration
public class WebConfig{

    @Bean
    public FilterRegistrationBean<Filter> logFilter(){
        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();

				// DispatcherType - Request, Error 추가
        filterRegistrationBean.setDispatcherTypes(DispatcherType.ERROR, DispatcherType.REQUEST);

        return filterRegistrationBean;
    }
}
```

`Interceptor`는 스프링이 제공하는 기능으로, `DispatcherType`과 함께 항상 호출됩니다. 따라서 `Interceptor`의 경우, 오류 페이지로 이동하는 URL 패턴을 제외하면 중복 호출을 방지할 수 있습니다.

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

		// 인터셉터 등록
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LogInterceptor())
                .order(1)
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/css/**", "/*.ico"
                        , "/error", "/error-page/**" //오류 페이지 경로
                );
    }
}
```

</aside>