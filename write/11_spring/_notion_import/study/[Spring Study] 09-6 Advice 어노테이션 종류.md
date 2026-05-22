# [Spring Study] 09-6. Advice 어노테이션 종류

주제: Spring Study

- 참고
    
    [스프링 AOP 구현](https://velog.io/@coconenne/스프링-AOP-구현#스프링-핵심-원리)
    
    [[Spring] Advice 종류](https://hyuuny.tistory.com/100)
    

# **어드바이스 종류**

---

<aside>
💡 **NOTE**

> *스프링 **Advice**에는 `@Around`**이외에도 다양한 방식이 존재한다**.*
> 

![Advice 적용순서](%5BSpring%20Study%5D%2009-6%20Advice%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled.png)

Advice 적용순서

![함수가 성공했을때 나오는 출력순서](%5BSpring%20Study%5D%2009-6%20Advice%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%201.png)

함수가 성공했을때 나오는 출력순서

- 복잡해 보이지만 사실 `@Around`를 제외한 나머지 어드바이스들은 `@Around`가 할 수 있는 일의 일부만 제공할 뿐이다.
    - 단 `@Around`는 `ProceedingJoinPoin`를 사용해서 직접 `proceed()`해줘야 한다.
    - 만약 해주지 않는다면 타겟이 호출되지 않는 치명적인 버그가 발생한다.
    - 나머지는 `JoinPoint`를 사용해서 위와같은 문제를 걱정할 필요가 없으며, 코드를 작성한 의도가 더 명확하게 드러난다.
</aside>

## **JoinPoint와 ProceedingJoinPoint 인터페이스 기능**

<aside>
✍️ **NOTE**

```java
public void orderItem(String itemID) {
    log.info("[orderService] 실행");
    orderRepository.save(itemID);
}
```

![각 함수들의 결과값 출력](%5BSpring%20Study%5D%2009-6%20Advice%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%202.png)

각 함수들의 결과값 출력

[ChatGPT](https://chat.openai.com/share/cefaf04f-0214-46d8-873e-3632998c7ee0)

왜 getTarget()과 getThis()가 같은지에 대한 질문
(쉽게 요약하면 프록시 안거치고 orderRepository.save() 함수를 바로쓰기 때문)

### JoinPoint

- `getArgs()`
    - 메서드 인수 반환
- `getThis()`
    - 프록시 객체 반환
- `getTarget()`
    - 대상 객체를 반환한다.
- `getSignature()`
    - 조언되는 메서드에 대한 설명반환
- `toString()`
    - 조언되는 방법에 대한 유용한 설명반환

### **ProceedingJoinPoint**

- `proceed()`
    - 다음 어드바이스나 타겟을 호출한다.
</aside>

## @Around

<aside>
✍️ **NOTE**

> ***메서드 호출 전후에 수행하며, 조인 포인트 실행 여부 선택, 반환 값 변환, 예외 변환 등이 가능하다.***
> 

```java
@Around("hello.aop.order.aop.Pointcuts.orderAndService()")
public Object doTransaction(ProceedingJoinPoint joinPoint) throws Throwable {

    try {
        // @Before
        log.info("[트랜잭션 시작] {}", joinPoint.getSignature());

        Object result = joinPoint.proceed();

        // @AfterReturning
        log.info("[트랜잭션 커밋] {}", joinPoint.getSignature());
        return result;
    } catch (Exception e) {
        // @AfterThrowing
        log.info("[트랜잭션 롤백] {}", joinPoint.getSignature());
        throw e;
    } finally {
        // @After
        log.info("[리소스 릴리즈] {}", joinPoint.getSignature());
    }
}
```

- `ProceedingJoinPoint`를 사용해야 한다.
- `proceed()`를 통해 대상을 실행해야 하며, 여러번 실행할 수 있다.
</aside>

## @Before

<aside>
✍️ **NOTE**

> ***조인 포인트 실행 이전에 실행된다.***
> 

```java
@Before("hello.aop.order.aop.Pointcuts.orderAndService()")
public void doBefore(JoinPoint joinPoint) {
    log.info("[before] {}", joinPoint.getSignature());
}
```

</aside>

## **@AfterReturning**

<aside>
✍️ **NOTE**

> ***조인 포인트가 정상 완료후 실행된다.***
> 

```java
@AfterReturning(value = "hello.aop.order.aop.Pointcuts.orderAndService()", returning = "result")
public void doReturn(JoinPoint joinPoint, Object result) {
    log.info("[return] {} return={}", joinPoint.getSignature(), result);
}
```

- `returning` 속성에 사용된 이름은 어드바이스 매서드의 매개변수와 이름이 같아야한다.
- `returning`절에 지정된 타입의 값을 반환하는 메서드만 대상으로 실행한다.
    - `Object`타입으로 하면 모든 타입에 대해서 받을수있으므로 무조건 실행한다.
</aside>

## **@AfterThrowing**

<aside>
✍️ **NOTE**

> ***메서드가 예외를 던지는 경우 실행된다.***
> 

```java
@AfterThrowing(value = "hello.aop.order.aop.Pointcuts.orderAndService()", throwing = "ex")
public void doThrowing(JoinPoint joinPoint, Exception ex) {
    log.info("[throwing] {} ex={}", joinPoint.getSignature(), ex);
}
```

- `throwing` 속성에 사용된 이름은 어드바이스 매서드의 매개변수 이름과 일치해야 한다.
- `throwing`절에 지정된 타입과 맞는 예외를 대상으로 실행된다.
</aside>

## **@After**

<aside>
✍️ **NOTE**

> 조인 포인트가 정상 또는 예외에 관계없이 마지막에 실행(finally)된다.
> 

```java
@After(value = "hello.aop.order.aop.Pointcuts.orderAndService()")
public void doAfter(JoinPoint joinPoint) {
    log.info("[after] {}", joinPoint.getSignature());
}
```

- 정상 및 예외 반환 조건을 모두 처리하며, 일반적으로 리소스 해제에 사용한다.
</aside>