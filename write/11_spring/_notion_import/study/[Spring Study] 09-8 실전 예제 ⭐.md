# [Spring Study] 09-8. 실전 예제 ⭐

주제: Spring Study

- 참고
    
    [스프링 AOP - 실전 예제](https://velog.io/@coconenne/스프링-AOP-실전-예제)
    
    [스프링 AOP - 실무 주의사항](https://velog.io/@coconenne/스프링-AOP-실무-주의사항)
    

# **예제 만들기**

---

<aside>
💡 **NOTE**

> ***실제 상황에서 발생할만한 경우를 직접 작성해본다!***
> 
- `@Trace` 애노테이션으로 로그 출력
- `@Retry` 애노테이션으로 예외 발생시 재시도

```java
@Service
@RequiredArgsConstructor
public class ExamService {

    private final ExamRepository examRepository;

    @Trace
    public void request(String itemId) {
        examRepository.save(itemId);
    }
}
```

```java
@Repository
public class ExamRepository {

    private static int seq = 0;

    /**
     * 5번에 1번 실패함..
     */
    @Trace
    @Retry(value = 4)
    public String save(String itemId){

        seq++;
        if (seq % 5 == 0) {
            throw new IllegalStateException("예외 발생");
        }

        return "ok";
    }
}
```

</aside>

## @Trace (로그 출력)

<aside>
✍️ **NOTE**

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Trace {}
```

```java
@Slf4j
@Aspect
public class TraceAspect {

    @Before("@annotation(hello.aop.exam.annotation.Trace)")
    public void doTrace(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        log.info("[trace] {} args={}", joinPoint.getSignature(), args);
    }
}
```

</aside>

## @Retry (재시도)

<aside>
✍️ **NOTE**

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Retry {
    int value() default 3;
}
```

```java
@Slf4j
@Aspect
public class RetryAspect {

    @Around("@annotation(retry)")
    public Object doRetry(ProceedingJoinPoint joinPoint, Retry retry) throws Throwable {
        log.info("[retry] {} retry={}", joinPoint.getSignature(), retry);

        int maxRetry = retry.value();
        Exception exceptionHolder = null;

        for (int retryCount = 1; retryCount <= maxRetry; retryCount++) {
            try{
                log.info("[retry] try count={}/{}", retryCount, maxRetry);
                return joinPoint.proceed();
            } catch (Exception e) {
                exceptionHolder = e;
            }
        }

        throw exceptionHolder;
    }
}
```

</aside>

# **스프링AOP - 실무 주의사항**

---

## **프록시와 내부 호출**

<aside>
✍️ **NOTE**

> *스프링은 프록시 방식의 AOP를 사용하므로, **항상 프록시를 통해서 대상 객체(Target)을 호출해야 한다!***
> 
- 프록시를 거치지 않으면 AOP가 적용되지 않는다.
- 스프링은 의존관계 주입시 항상 프록시 객체를 주입해서, 일반적으로 이러한 문제가 발생하지 않지만 대상 객체의 내부에서 메서드 호출이 프록시를 거치지 않으면 문제가 발생한다.

![실제 target객체에서 호출하기에 internal함수는 AOP가 적용되지 않음.. (external()을 실행시킨 경우임)](%5BSpring%20Study%5D%2009-8%20%EC%8B%A4%EC%A0%84%20%EC%98%88%EC%A0%9C%20%E2%AD%90/Untitled.png)

실제 target객체에서 호출하기에 internal함수는 AOP가 적용되지 않음.. (external()을 실행시킨 경우임)

```java
@Slf4j
@Component
public class CallServiceV0 {

    public void external(){
        log.info("call external");
        internal(); // 내부 메서드 호출 (AOP가 적용되지 않음!)
    }

    public void internal() {
        log.info("call internal"); 
    }
}
```

</aside>

## 프록시 내부 호출 대안 1(자기 자신 주입)

<aside>
✍️ **NOTE**

```java
@Slf4j
@Component
public class CallServiceV1 {

    private CallServiceV1 callServiceV1;

    @Autowired
    public void setCallServiceV1(CallServiceV1 callServiceV1) {
        this.callServiceV1 = callServiceV1;
    }

    public void external(){
        log.info("call external");
        callServiceV1.internal(); // 외부 메서드 호출
    }

    public void internal() {
        log.info("call internal");
    }
}
```

![뭔가 복잡하지만 프록시를 거침..](%5BSpring%20Study%5D%2009-8%20%EC%8B%A4%EC%A0%84%20%EC%98%88%EC%A0%9C%20%E2%AD%90/Untitled%201.png)

뭔가 복잡하지만 프록시를 거침..

- **📌 주의점!**
    - 이러한 주입시 순환 사이클이 만들어지므로 실제로 사용하려면 추가설정을 해줘야한다.
    - `spring.main.allow-circular-references=true`
</aside>

## 프록시 내부 호출 대안 2(**지연 조회**)

<aside>
✍️ **NOTE**

```java
@Slf4j
@Component
public class CallServiceV2 {

    // private final ApplicationContext applicationContext;
    private final ObjectProvider<CallServiceV2> callServiceProvider;

    public CallServiceV2(ObjectProvider<CallServiceV2> callServiceProvider) {
        this.callServiceProvider = callServiceProvider;
    }

    public void external(){
        log.info("call external");
        // CallServiceV2 callServiceV2 = applicationContext.getBean(CallServiceV2.class);
        CallServiceV2 callServiceV2 = callServiceProvider.getObject();
        callServiceV2.internal(); // 외부 메서드 호출
    }

    public void internal() {
        log.info("call internal");
    }
}
```

</aside>

## 프록시 내부 호출 대안 3(**구조 변경**)

<aside>
✍️ **NOTE**

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class CallServiceV3 {

    private final InternalService internalService;

    public void external(){
        log.info("call external");
        internalService.internal(); // 외부 메서드 호출
    }
}
```

```java
@Slf4j
@Component
public class InternalService {
    public void internal() {
        log.info("call internal");
    }
}
```

![외부 메서드를 호출하게 되므로 문제가없어짐](%5BSpring%20Study%5D%2009-8%20%EC%8B%A4%EC%A0%84%20%EC%98%88%EC%A0%9C%20%E2%AD%90/Untitled%202.png)

외부 메서드를 호출하게 되므로 문제가없어짐

</aside>