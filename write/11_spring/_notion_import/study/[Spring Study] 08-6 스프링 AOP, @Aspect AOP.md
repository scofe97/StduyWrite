# [Spring Study] 08-6. 스프링 AOP, @Aspect AOP

주제: Spring Study
연관 노트: [Spring Study] 05-4. HTTP Message Converter, RequestMappingHandlerAdapter (https://www.notion.so/Spring-Study-05-4-HTTP-Message-Converter-RequestMappingHandlerAdapter-cea9762b9b12471f96bd29d4eb4795c7?pvs=21)

- 참고
    
    [@Aspect AOP](https://velog.io/@coconenne/Aspect-AOP)
    
    [[AOP] @Aspect](https://ttl-blog.tistory.com/865)
    
    [[Spring] @Aspect AOP](https://hyuuny.tistory.com/96)
    
    [스프링 AOP 구현](https://velog.io/@coconenne/스프링-AOP-구현)
    

# 스프링 AOP(Aspect-Oriented Programming)

---

<aside>
💡 **NOTE**

> ***AOP**는 부가기능을 핵심 기능에서 분리하고 한 곳에서 관리하여 모듈화하고, 부가 기능을 어디에 적용할지 선택하는 기능을 제공합니다.*
> 

![핵심 기능 - 비즈니스 로직
부가 기능 - 횡단 관심사(AOP)](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled.png)

핵심 기능 - 비즈니스 로직
부가 기능 - 횡단 관심사(AOP)

![로그 추적 로직(횡단 관심사) 추가](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%201.png)

로그 추적 로직(횡단 관심사) 추가

![Untitled](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%202.png)

AOP에서 부가 기능(Advice)과 이를 어디에(Pointcut) 적용할지 정의한 모듈을 `Aspect`라고 합니다. 

`AspectJ` 프레임워크는 AOP의 대표적인 구현 프레임워크이며 스프링 AOP는 `AspectJ`의 문법을 사용하여 일부 기능만 제공합니다. `AspectJ`는 다양한 방법을 제공하지만 복잡하고, 실무에서는 스프링 AOP만 알아도 대부분의 문제를 해결할 수 있습니다.

</aside>

## Aop 적용 방식

<aside>
✍️ **NOTE**

### 컴파일 시점

소스 코드를 컴파일할 때 부가기능 로직을 추가하며, 특별한 컴파일러가 필요합니다.

![.java → .class 시점에서 **부가 기능 로직을 추가합니다.**](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%203.png)

.java → .class 시점에서 **부가 기능 로직을 추가합니다.**

### 클래스 로딩 시점

Java를 실행하면 Java언어는 .class 파일을 JVM 내부의 클래스 로더에 보관하며, 이때 .class 파일을 조작한뒤 JVM에 올리는 방식입니다. (Java Instrumentation 참고)

![JVM에 올라가기전에 추가합니다.](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%204.png)

JVM에 올라가기전에 추가합니다.

### 런타임 시점(Spring AOP)

자바가 실행된 후, Proxy를 적용해 부가 기능을 적용하며, 스프링 AOP가 사용하는 방식입니다.

![빈 후처리기를 통해 적용](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%205.png)

빈 후처리기를 통해 적용

</aside>

# **스프링 AOP 구현 - @Aspect 프록시**

---

<aside>
💡 **NOTE**

> *스프링에서 프록시를 적용하기 위해서는 Advisor를 만들어 스프링 Bean으로 등록하면 됩니다. 스프링은 `@Aspect` 애노테이션으로 매우 편리하게 `Advisor`를 편하게 만들 수 있도록 지원해줍니다.*
> 

![@Aspect를 사용하는 구조](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%206.png)

@Aspect를 사용하는 구조

```java
@Slf4j
@Component
@Aspect
public class TimeAdviceAspect {

    @Around("within(com.example.study.aop.AutoProxyConfig.A)")
    public Object invoke(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("TimeProxy 실행");

        long startTime = System.currentTimeMillis();
        Object proceed = joinPoint.proceed(); // target 없이 메서드 호출
        long endTime = System.currentTimeMillis();

        long resultTime = endTime - startTime;
        log.info("TimeProxy 종료 resultTime={}", resultTime);

        return proceed;
    }
}
```

![Untitled](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%207.png)

</aside>

## 자동 프록시 생성시(@Aspect)

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%208.png)

- `@Aspect`를 보고 `Advisor`로 변환해서 저장한다.
- `Advisor`를 기반으로 프록시를 생성한다.

![Untitled](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%209.png)

![Untitled](%5BSpring%20Study%5D%2008-6%20%EC%8A%A4%ED%94%84%EB%A7%81%20AOP,%20@Aspect%20AOP/Untitled%2010.png)

</aside>

## 포인트컷 분리  & 조합

<aside>
✍️ **NOTE**

```java
@Slf4j
@Aspect
public class AspectV3 {

    // hello.aop.order 패키지와 하위 패키지
    @Pointcut("execution(* hello.aop.order..*(..))")
    private void allOrder(){} // pointcut signature

    // 클래스 이름 패턴이 *Service
    @Pointcut("execution(* *..*Service.*(..))")
    private void allService(){}

    // hello.aop.order 패키지와 하위패키지 이면서 클래스 이름 패턴이 Service인 경우
    @Around("allOrder() && allService()")
    public Object doTransaction(ProceedingJoinPoint joinPoint) throws Throwable {

        try{
            log.info("[트랜잭션 시작] {}", joinPoint.getSignature());
            Object result = joinPoint.proceed();
            log.info("[트랜잭션 시작] {}", joinPoint.getSignature());

            return result;
        }catch (Exception e){
            log.info("[트랜잭션 롤백] {}", joinPoint.getSignature());
            throw e;
        }finally {
            log.info("[리소스 릴리즈] {}", joinPoint.getSignature());
        }
    }
}
```

- 포인트컷은 `&&`, `||`, `!` 조합이 가능하다.
</aside>

## 외부 포인트컷 참조

<aside>
✍️ **NOTE**

```java
public class Pointcuts {

    // hello.aop.order 패키지와 하위 패키지
    @Pointcut("execution(* hello.aop.order..*(..))")
    public void allOrder(){} // pointcut signature

    // 클래스 이름 패턴이 *Service
    @Pointcut("execution(* *..*Service.*(..))")
    public void allService(){}

    // allOrder && allService
    @Pointcut("allOrder() && allService()")
    public void orderAndService() {}
}
```

```java
@Slf4j
@Aspect
public class AspectV4Pointcut {

    @Around("hello.aop.order.aop.Pointcuts.allOrder()")
    public Object doLog(ProceedingJoinPoint joinPoint) throws  Throwable {
        log.info("[log] {}", joinPoint.getSignature());
        return joinPoint.proceed();
    }

    // hello.aop.order 패키지와 하위패키지 이면서 클래스 이름 패턴이 Service인 경우
    @Around("hello.aop.order.aop.Pointcuts.orderAndService()")
    public Object doTransaction(ProceedingJoinPoint joinPoint) throws Throwable {

        try{
            log.info("[트랜잭션 시작] {}", joinPoint.getSignature());
            Object result = joinPoint.proceed();
            log.info("[트랜잭션 시작] {}", joinPoint.getSignature());

            return result;
        }catch (Exception e){
            log.info("[트랜잭션 롤백] {}", joinPoint.getSignature());
            throw e;
        }finally {
            log.info("[리소스 릴리즈] {}", joinPoint.getSignature());
        }
    }
}
```

- `@Around`에 패키지명을 포함한 클래스 이름과 포인트컷 시그니처를 모두 지정하면 된다.
- 포인트컷을 여러 어드바이스에서 함께 사용할 때 유용하다.
</aside>

## 어드바이스 순서 지정하기(@Order)

<aside>
✍️ **NOTE**

```java
@Slf4j
public class AspectV5Order {

    @Aspect
    @Order(2)
    public static class LogAspect{
        @Around("hello.aop.order.aop.Pointcuts.allOrder()")
        public Object doLog(ProceedingJoinPoint joinPoint) throws  Throwable {
            log.info("[log] {}", joinPoint.getSignature());
            return joinPoint.proceed();
        }
    }

    @Aspect
    @Order(1)
    public static class TxAspect{
        // hello.aop.order 패키지와 하위패키지 이면서 클래스 이름 패턴이 Service인 경우
        @Around("hello.aop.order.aop.Pointcuts.orderAndService()")
        public Object doTransaction(ProceedingJoinPoint joinPoint) throws Throwable {

            try{
                log.info("[트랜잭션 시작] {}", joinPoint.getSignature());
                Object result = joinPoint.proceed();
                log.info("[트랜잭션 커밋] {}", joinPoint.getSignature());

                return result;
            }catch (Exception e){
                log.info("[트랜잭션 롤백] {}", joinPoint.getSignature());
                throw e;
            }finally {
                log.info("[리소스 릴리즈] {}", joinPoint.getSignature());
            }
        }
    }

}
```

- 어드바이스는 기본적으로 순서를 보장하지 않는다.
- **순서를 지정하고 싶으면** `@Aspect` **적용 단위로** `@Order` **애노테이션을 적용해야 한다.**
    - 단 `@Order`는 어드바이스 단위가 아닌 클래스 단위로 지정이 가능하다.
    - 그래서 내부에 `static class`구조로 분리해서 사용한다.
    - `@Order`는 숫자가 작을수록 먼저 실행된다.
</aside>