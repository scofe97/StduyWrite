# [Spring Study] 05-4. HTTP Message Converter, RequestMappingHandlerAdapter

주제: Spring Study
연관 노트: [Spring Study] 08-6. 스프링 AOP, @Aspect AOP (https://www.notion.so/Spring-Study-08-6-AOP-Aspect-AOP-c731d4cf1b294dab881ba3deb3f976bf?pvs=21)

- 참고
    
    [spring-mvc-1/13 요청 매핑 헨들러 어뎁터 구조.md at main · backend-sprout/spring-mvc-1](https://github.com/backend-sprout/spring-mvc-1/blob/main/06%20%EC%8A%A4%ED%94%84%EB%A7%81%20MVC%20-%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5/13%20%EC%9A%94%EC%B2%AD%20%EB%A7%A4%ED%95%91%20%ED%97%A8%EB%93%A4%EB%9F%AC%20%EC%96%B4%EB%8E%81%ED%84%B0%20%EA%B5%AC%EC%A1%B0.md)
    

# HTTP 메시지 컨버터

---

<aside>
💡 **NOTE**

> *HTTP 메시지 컨버터는 클라이언트로부터 받은 HTTP 요청의 본문을 컨트롤러가 처리할 수 있는 자바 객체로 변환하거나, 반환된 객체를 HTTP 응답의 본문으로 바꾸는데 사용됩니다.*
> 

HTTP 데이터를 읽고, HTTP 응답 데이터를 쓰는 컨버터의 어노테이션인 `@RequestBody`, `@ResponseBody`가 대표적이며, 해당 어노테이션들이 붙으면 `HttpMessageConverter`가 데이터 변환을 담당하게 됩니다.

- `@RequestBody`: HTTP 요청 본문의 데이터가 메서드 파라미터로 변환됩니다.
- `@ResponseBody`: 메서드에서 반환된 값이 HTTP 응답 본문에 직접 쓰입니다.

```java
public interface HttpMessageConverter<T> {

    boolean canRead(Class<?> clazz, @Nullable MediaType mediaType);

    boolean canWrite(Class<?> clazz, @Nullable MediaType mediaType);

    List<MediaType> getSupportedMediaTypes();

    T read(Class<? extends T> clazz, HttpInputMessage inputMessage) throws IOException, HttpMessageNotReadableException;

    void write(T t, @Nullable MediaType contentType, HttpOutputMessag outputMessage) throws IOException, HttpMessageNotWritableException;

}
```

스프링에서 제공하는 주요 HTTP 메시지 컨버터는 다음과 같습니다.

1. `ByteArrayHttpMessageConverter`
2. `StringHttpMessageConverter`
3. `MappingJackson2HttpMessageConverter`
</aside>

## **HTTP 메시지 컨버터의 작동 방식**

<aside>
✍️ **NOTE**

> *HTTP 요청/응답에서 사용되는 데이터의 읽기 및 쓰기 작업을 처리하는데 사용되며, 이전에 설명한 `Converter`와 다른 인터페이스를 구현하지만 개념은 동일합니다.*
> 

### HTTP 요청 데이터 읽기

- 컨트롤러에서 `@RequestBody`, `HttpEntity`를 사용하는 컨트롤러에서 HTTP 요청이 들어오면, 해당 데이터 타입과 `Content-Type`을 지원하는지 확인합니다. (`canRead()` 호출)
- 지원되면 `read()` 메서드가 호출되어 요청 데이터가 객체로 반환됩니다.

### HTTP 응답 데이터 쓰기

- 컨트롤러에서 `@ResponseBody`나 `HttpEntity`를 통해 데이터를 반환할 때, 해당 데이터 타입과 클라이언트의 Accpe 헤더를 지원하는지 확인합니다. (`canWrite()` 호출)
- 지원되면 `write()` 메서드가 호출되어 객체 데이터가 HTTP 응답 메시지 바디에 쓰입니다.
</aside>

# RequestMappingHandlerAdapter 구조

---

<aside>
💡 **NOTE**

> `*RequestMappingHandlerAdapter`는 스프링 MVC에서 `@RequestMapping` 어노테이션을 처리하며. 요청이 들어올 때 해당 요청을 처리할 수 있는 가장 적합한 메서드를 결정합니다.*
> 

![HTTP 메시지 컨버터는 4번에서 사용됨 (디스패쳐 서블릿 - 핸들러 사이)](%5BSpring%20Study%5D%2005-4%20HTTP%20Message%20Converter,%20Reques/Untitled.png)

HTTP 메시지 컨버터는 4번에서 사용됨 (디스패쳐 서블릿 - 핸들러 사이)

![Untitled](%5BSpring%20Study%5D%2005-4%20HTTP%20Message%20Converter,%20Reques/Untitled%201.png)

</aside>

## **ArgumentResolver**

<aside>
✍️ **NOTE**

> *스프링은 `HandlerMethodArgumentResolver` 인페이스를 통해 컨트롤러 메소드의 파라미터를 동적으로 처리합니다. 이 인터페이스의 구현체는 특정 타입의 파라미터를 지원하는지 확인하고, 지원한다면 필요한 객체를 생성합니다.*
> 

아래의 코드는 `Session` 정보에서 유저의 정보를 추출해서 자동으로 `MemberResponseStatus` 객체를 생성해주는 작업입니다.

```java
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface SignIn {}
```

```java
@Slf4j
public class SignInArgumentResolver implements HandlerMethodArgumentResolver {

		// 해당 파라미터를 지원하는가?
    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        boolean hasLoginAnnotation = parameter.hasParameterAnnotation(SignIn.class); // @Login이 있는가?
        boolean hasMemberType = MemberResponseStatus.class.isAssignableFrom(parameter.getParameterType()); // MemberResponseStatus가 있는가?

        return hasLoginAnnotation && hasMemberType;
    }

		// 파라미터를 지원한다면 실제 객체를 생성
    @Override
    public Object resolveArgument(MethodParameter parameter,
                                  ModelAndViewContainer mavContainer,
                                  NativeWebRequest webRequest,
                                  WebDataBinderFactory binderFactory) throws Exception {

        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest(); // 원본 HTTP 요청
        HttpSession session = request.getSession(false); // 현재 Session을 가져온다.

				// session에 저장된 유저객체가 없다면 Null 반환
        if(session == null || session.getAttribute(Const.SIGNIN_MEMBER) == null) {
            log.info("not login member {}",  session);
            return null;
        }

				// 저장된 객체가 있다면 저장된 객체 반환
        log.info("login member {}", session.getAttribute(Const.SIGNIN_MEMBER));
        return session.getAttribute(Const.SIGNIN_MEMBER);
    }
}
```

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        resolvers.add(new SignInArgumentResolver());
    }
}
```

```java
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final MemberService memberService;

		// 4. @SignIn 사용
    @GetMapping("/status")
    public ResponseEntity<?> memberStatus(@SignIn MemberResponseStatus member){
        return new ResponseEntity<>(member, HttpStatus.OK);
    }
    
    
    @PostMapping("/signIn")
    public ResponseEntity<?> memberSignIn(@Valid @RequestBody MemberRequestSignInDto memberRequestSignInDto,
                                          HttpSession httpSession){

        MemberResponseStatus signInMember = memberService.signIn(memberRequestSignInDto);
        log.info("signMember : {}", signInMember);
        httpSession.setAttribute(Const.SIGNIN_MEMBER, signInMember);
        return new ResponseEntity<>(signInMember, HttpStatus.OK);
    }
}
```

</aside>

## **ReturnValueHandler**

<aside>
✍️ **NOTE**

> `*ReturnValueHandler`는 컨트롤러에서 반환된 값이 어떻게 HTTP 응답에 매핑될지를 처리합니다. 만약 문자열을 반환할 경우, 뷰 이름 혹은 `ResponeBody`가 붙은경우 JSON 형식으로 직렬화되어 Respone 본문에 포함될 수 있습니다.*
> 

[Return Values :: Spring Framework](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/return-types.html)

스프링은 다양한 `ReturnValudeHandler`를 지원하며 대표적인 예시는 다음과 같습니다.

- ex) `ModelAndView`, `@ResponseBody`, `HttpEntity`, `String`

```java
public class CustomReturnValueHandler implements HandlerMethodReturnValueHandler {

    @Override
    public boolean supportsReturnType(MethodParameter returnType) {
        // 특정 조건에 따라 처리 가능 여부를 결정 (예: MyResponse 타입인 경우만 처리)
        return MyResponse.class.isAssignableFrom(returnType.getParameterType());
    }

    @Override
    public void handleReturnValue(
            Object returnValue, 
            MethodParameter returnType,
            ModelAndViewContainer mavContainer,
            ServerHttpRequest request,
            ServerHttpResponse response) throws Exception {

        // 반환값을 처리하고 응답 설정
        if (returnValue instanceof MyResponse) {
            MyResponse myResponse = (MyResponse) returnValue;
            // 반환 객체를 JSON 문자열로 변환 (여기서는 예시로 단순 문자열 사용)
            String json = "{\"message\": \"" + myResponse.getMessage() + "\"}";
            response.getBody().write(json.getBytes());

            // ModelAndView 진행 방지
            mavContainer.setRequestHandled(true);
        }
    }
}
```

</aside>