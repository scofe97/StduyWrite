# [Spring Study] 07-2. 스프링 예외처리(HandlerExceptionResolver)

주제: Spring Study

- 참고
    
    [[Spring] 스프링의 다양한 예외 처리 방법(ExceptionHandler, ControllerAdvice 등) 완벽하게 이해하기 - (1/2)](https://mangkyu.tistory.com/204)
    
    [[Spring MVC] [2] 9. API 예외 처리](https://velog.io/@dbsrud11/Spring-MVC-2-9.-API-%EC%98%88%EC%99%B8-%EC%B2%98%EB%A6%AC)
    

# 스프링이 제공하는 예외처리

---

<aside>
💡 **NOTE**

> *Java에서 기본적인 예외처리는 try-catch이지만, Spring은 에러 처리라는 공통 관심사를 메인 로직으로부터 분리하는 예외 처리 방식인 `HandlerExceptionResolver` 인터페이스를 만들었습니다.*
> 

`HandlerExceptionResolver`는 대부분 발생한 Exception을 잡아내고, HTTP 상태나 응답 메시지를 설정합니다. 이로 인해, 웹 애플리케이션 서버(WAS)는 해당 요청을 정상적인 응답으로 인식하게 되고, 복잡한 WAS의 에러 전달이 발생하지 않습니다.

```java
public interface HandlerExceptionResolver {
    ModelAndView resolveException(HttpServletRequest request, 
											            HttpServletResponse response, 
											            Object handler, 
											            Exception ex);
}
```

'`handler`'라는 Object 타입은 예외가 발생한 컨트롤러 객체를 가리킵니다. 예외가 발생하면, 디스패처 서블릿까지 전달되며, 적절한 예외 처리를 위한 `HandlerExceptionResolver` 구현체들이 빈으로 등록되어 관리됩니다.

- `ExceptionHandler`, `ResponseStatus`, `DefaultHandler` 순서의 우선순위를 가지게 됩니다.

적용 가능한 구현체를 찾아 예외 처리를 하게 되는데, 대표적으로 4가지가 있습니다:

1. `DefaultErrorAttribute`: 에러 속성을 저장하나, 직접 예외를 처리하지는 않습니다.
2. `ExceptionHandlerExceptionResolver`: `Controller`나 `ControllerAdvice`에 있는 `ExceptionHandler`를 통해 에러 응답을 처리합니다.
3. `ResponseStatusExceptionResolver`: HTTP 상태 코드를 지정하는 `@ResponseStatus` 또는 `ResponseStatusException`을 처리합니다.
4. `DefaultHandlerExceptionResovler`: 스프링 내부에서 발생하는 기본 예외들을 처리합니다.

Spring은 다음과 같은 도구들로 `ExceptionResolver`를 동작시켜 에러를 처리할 수 있습니다.

1. `@ResponseStatus`
2. `ResponseStatusException`
3. `@ExceptionHandler`
4. `@ControllerAdivce`, `@RestControllerAdvice`
</aside>

## **HandlerExceptionResolver 생성**

<aside>
💡 **NOTE**

> `*HandlerExceptionResolver`는 API에서 발생하는 예외를 효과적으로 관리할 수 있습니다. 이를 통해 다른 HTTP 상태 코드를 지정하거나 사용자 정의 오류 메시지를 전달할 수 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%2007-2%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%98%88%EC%99%B8%EC%B2%98%EB%A6%AC(HandlerExceptionResol/Untitled.png)

![Untitled](%5BSpring%20Study%5D%2007-2%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%98%88%EC%99%B8%EC%B2%98%EB%A6%AC(HandlerExceptionResol/Untitled%201.png)

```java
@GetMapping("/java-error")
public ResponseEntity<String> getError(){
    throw new RuntimeException();
}
```

```java
@Slf4j
public class MyHandlerExceptionResolver implements HandlerExceptionResolver {

    @Override
    public ModelAndView resolveException(HttpServletRequest request,
                                         HttpServletResponse response,
                                         Object handler,
                                         Exception ex)
    {
        // RuntimeException 예외 발생시 200으로 상태코드 변경(원래는 500)
        if (ex instanceof RuntimeException) {
            log.info("RuntimeException을 200코드로 변경");
            response.setStatus(HttpServletResponse.SC_OK);
            return new ModelAndView();
        }
        return null;
    }
}
```

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

		// ExceptionHandler 등록
    @Override
    public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
        resolvers.add(new MyHandlerExceptionResolver());
    }
}
```

- `configureHandlerExceptionResolvers()`는 스프링이 기본으로 제공하는 `ExceptionResolver`를 제거하므로, `extendHandlerExceptionResolvers`를 사용하는 것이 좋습니다.
- 실제로는 직접 구현하지 않고, 스프링이 제공하는 `ExceptionResovlver`를 주로 사용합니다.
</aside>

## @**ResponseStatus**

<aside>
✍️ **NOTE**

> `*@ResponseStatus`는 특정 예외에 대해 직접 지정된 HTTP 상태코드로 응답할 수 있게 해줍니다.*
> 

```java
@ResponseStatus(code = HttpStatus.BAD_REQUEST, reason = "잘못된 요청 오류")
public class BadRequestException extends RuntimeException {}
```

```java
throw new ResponseStatusException(HttpStatus.NOT_FOUND, "error.bad", new IllegalArgumentException());
```

</aside>

## **ResponseStatusException**

<aside>
✍️ **NOTE**

> *@ResponseStatus를 붙여줄 수 없는 경우, ResponseStatusException을 활용해서 예외처리를 해줄 수 있습니다.*
> 

```java
@GetMapping("/status-exception")
public ResponseEntity<?> getStatusException() {
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Item Not Found");
}
```

- `ResponseStatus`와 동일하게 `ResponseStatusExceptionResolver`가 에러를 처리합니다.
- 하지만 여러 한계점들이 존재해 실제로 `@ExceptionHandler`가 가장 많이 쓰인다.
    - 예외가 WAS까지 전달된다.
    - 예외 처리 코드가 중복될 수 있다.
</aside>

## **@ExceptionHandler** ⭐

<aside>
✍️ **NOTE**

> `*ExceptionHandler`는 특정 컨트롤러 내에서 발생할 수 있는 예외를 처리하기 위해 사용되며, 예외 처리로직을 컨트롤러내에서 직접 정의할 수 있습니다.*
> 

```java
@RestController
public class ExceptionHandlingController {

    // IllegalArgumentException 처리
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<String> handleIllegalArgument(IllegalArgumentException e) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
    }

    // UserException 처리
    @ExceptionHandler(UserException.class)
    public ResponseEntity<String> handleUserException(UserException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
    }

    // 모든 Exception 처리
    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleException(Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("An error occurred");
    }

    @GetMapping("/test")
    public String test(@RequestParam(required = false) String param) {
        // 로직..
    }
}
```

- `@ControllerAdivce`나 `@Controller` 어노테이션 내부의 메소드에 추가해야 동작합니다.
- `@ExceptionHandler`에 등록된 예외 클래스와 파라미터로 받는 예외 클래스가 다른경우 컴파일 시점에 예외가 발생하지 않고, 런타임 시점에 예외가 발생한다.
</aside>

## **@ControllerAdvice, @RestControllerAdvice**

<aside>
💡 **NOTE**

> `*@ControllerAdvice`는 모든 컨트롤러에 걸쳐 공통의 예외 처리, 데이터 바인딩 설정 등을 적용할 수 있게 해주는 어노테이션입니다. 간단히 설명하면 컨트롤러와 예외를 분리시키기 위해 등장했다고 생각하면 됩니다.*
> 

`@ControllerAdvice`는 대상으로 지정한 여러 컨트롤러에 `@ExceptionHandler`, `@InitBinder` 기능을 부여해주는 역할을 합니다.

```java
@RestControllerAdvice(basePackages = "hello.exception.api")
public class ExControllerAdvice {

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptioHandler(IllegalArgumentException.class)
    public ErrorResult illegalExHandler(IllegalArgumentException e){
        log.error("[exceptionHandler] ex", e);
        return new ErrorResult("BAD", e.getMessage());
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResult> userExHandler(UserException e){
        log.error("[exceptionHandler ex", e);
        ErrorResult errorResult = new ErrorResult("USER-EX", e.getMessage());
        return new ResponseEntity(errorResult, HttpStatus.BAD_REQUEST);
    }

    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler
    public ErrorResult exHandler(Exception e){
        log.error("[exceptionHandler] ex", e);
        return new ErrorResult("EX", "내부오류");
    }
}
```

- `@RestControllerAdvice`는 `@ControllerAdvice`와 같고 `@ResponseBody`가 추가된 것입니다.

```java
// @RestController 어노테이션 범위에 지정
@ControllerAdvice(annotations = RestController.class)
public class ExampleAdvice1 {}

// 특정 패키지 범위
@ControllerAdvice("org.example.controllers")
public class ExampleAdvice2 {}

// 특정 클래스 범위
@ControllerAdvice(assignableTypes = {ControllerInterface.class,
        AbstractController.class})
public class ExampleAdvice3 {}
```

</aside>