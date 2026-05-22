# [Spring Study] 08-3. JDK 동적 동적 프록시

주제: Spring Study
연관 노트: [Java Study] 03. Class, 리플렉션과 어노테이션 (https://www.notion.so/Java-Study-03-Class-cf5c08d78e584160b38f17bc0a54c496?pvs=21)

- 참고
    
    [AOP(Aspect-Oriented Programming)의 이해와 스프링에서의 적용](https://f-lab.kr/insight/understanding-aop-in-spring)
    
    [☕ 누구나 쉽게 배우는 Dynamic Proxy 다루기](https://inpa.tistory.com/entry/JAVA-☕-누구나-쉽게-배우는-Dynamic-Proxy-다루기)
    
    [[Spring] Spring의 AOP 프록시 구현 방법(JDK 동적 프록시,  CGLib 프록시)과 @EnableAspectJAutoProxy의 proxyTargetClass - (3/3)](https://mangkyu.tistory.com/175)
    
    [동적 프록시 기술](https://velog.io/@coconenne/동적-프록시-기술)
    

# **JAVA 동**적 프록시

---

<aside>
💡 **NOTE**

> *JAVA* *****동적 프록시는 자바 가상 머신(JVM)에서 공싱적으로 지원하는 동적 프록시를 의미하며, 동적 프록시는 Reflect API를 활용해 프록시 클래스를 동적으로 만들어줍니다.*
> 

프록시 패턴은 초기화 지연, 접근 제어, 로깅, 캐싱 등을 추가하려 할 때, 원본 객체를 수정하지 않고 사용하는 디자인 패턴입니다. 이를 통해 개방-폐쇄 원칙 (OCP)을 준수할 수 있습니다. 이로 인해 코드가 유연하게 확장 가능하며, 유지보수가 쉬워집니다.

![Untitled](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled.png)

![InvocationHandler를 통해 프록시 객체를 자동으로 만들어준다.](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%201.png)

InvocationHandler를 통해 프록시 객체를 자동으로 만들어준다.

### 동적 프록시 요소

동적 프록시를 만들기 위해서는 `java.lang.reflect.Proxy` 클래스의 `newProxyInstance()` 메서드를 사용합니다. 이 메서드를 호출하면 따로 프록시 클래스 정의 없이 자동으로 프록시 객체를 등록할 수 있습니다.

```java
@Test
void dynamicA(){
    AInterface target = new AImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

    // 인터페이스 정보로 프록시 생성
    AInterface proxy = (AInterface) Proxy.newProxyInstance(
            AInterface.class.getClassLoader(),
            new Class[]{AInterface.class},
            handler);

    // call()은 인터페이스의 함수
    proxy.call();
}

@Test
void dynamicB(){
    BInterface target = new BImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

    // 인터페이스 정보로 프록시 생성
    com.example.study.aop.BInterface proxy = (BInterface) Proxy.newProxyInstance(
            BInterface.class.getClassLoader(),
            new Class[]{BInterface.class},
            handler);

    // call()은 인터페이스의 함수
    proxy.call();
}
```

1. `ClassLoader loader`: Proxy 클래스를 만드는 클래스 로더입니다. 일반적으로 구현할 인터페이스에 Class Loader를 가져옵니다.
2. `Class<?>[] interfaces`: 프록시 클래스가 구현하고자 하는 인터페이스 목록입니다.
3. `InvocationHandler h`: 프록시 메서드가 호출되었을때 실행되는 메서드입니다.
</aside>

## InvocationHandler 인터페이스

<aside>
✍️ **NOTE**

> `*InvocationHandler` 인터페이스는 `newProxyInstnace()` 메서드의 3번째 매개변수에 들어갈 핸들러 메서드를 정의하는 함수형 인터페이스 입니다.*
> 

`InvocationHandler` 인터페이스의 코드를 확인하면 `invoke()`라는 추상 메서드만 존재합니다. 이 `invoke()` 메서드는 프록시 메서드가 호출될 때 대신 실행되는 메서드입니다.

```java
public interface InvocationHandler {
    Object invoke(Object proxy, Method method, Object[] args) throws Throwable;
}
```

```java
@Slf4j
public class TimeInvocationHandler implements InvocationHandler {

    private final Object target;

    public TimeInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        
				log.info("TimeProxy 실행");
        long startTime = System.currentTimeMillis();
        
        Object result = method.invoke(target, args); // 메서드 실행
        
        long endTime = System.currentTimeMillis();
        long resultTime = endTime - startTime;
        log.info("TimeProxy 종료 resultTime={}", resultTime);

        return result;
    }
}
```

```java
@Slf4j
public class AImpl implements AInterface {
    @Override
    public String call() {
        log.info("A 호출");
        return "a";
    }
}

@Slf4j
public class BImpl implements BInterface {
    @Override
    public String call() {
        log.info("B 호출");
        return "b";
    }
}
```

```java
@Test
void dynamicA(){
    AInterface target = new AImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

		// 인터페이스 정보로 프록시 생성
    AInterface proxy = (AInterface) Proxy.newProxyInstance(AInterface.class.getClassLoader(), 
												new Class[]{AInterface.class}, 
												handler);

		// call()은 인터페이스의 함수
    proxy.call();
}

@Test
void dynamicB(){
    BInterface target = new BImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

		// 인터페이스 정보로 프록시 생성
    BInterface proxy = (BInterface) Proxy.newProxyInstance(BInterface.class.getClassLoader(), 
												new Class[]{BInterface.class}, 
												handler);

		// call()은 인터페이스의 함수
    proxy.call();
}
```

![Untitled](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%202.png)

![동적 프록시 흐름](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%203.png)

동적 프록시 흐름

</aside>

## 동적 프록시 메서드 필터링

<aside>
✍️ **NOTE**

> *위의 예제에서는 타겟 객체의 메서드는 call하나 밖에 없었다. 만약 메서드가 여러개 있는 타겟을 프록시화 하려면 어떻게 해야 하는가?*
> 

```java
public interface CInterface {
    String call();
    void print();
    Integer sum(int a, int b);
}

public class CImpl implements CInterface {
    @Override
    public String call() {
        System.out.println("C 호출");
        return "C 호출";
    }

    @Override
    public void print() {
        System.out.println("CImpl print");
    }

    @Override
    public Integer sum(int a, int b) {
        System.out.println(a+b);
        return a+b;
    }
}

```

```java
@Slf4j
@RequiredArgsConstructor
public class TimeInvocationHandler implements InvocationHandler {

    private final Object target;
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {

        log.info("TimeProxy 실행");

        long startTime = System.currentTimeMillis();
        Object result = method.invoke(target, args);
        long endTime = System.currentTimeMillis();
        long resultTime = endTime - startTime;

        log.info("TimeProxy 종료 resultTime={}", resultTime);

        return result;
    }
}
```

```java
@Test
void dynamicC() {
    CInterface target = new CImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

    CInterface proxy = (CInterface) Proxy.newProxyInstance(
            CInterface.class.getClassLoader(),
            new Class[]{CInterface.class},
            handler
    );

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![모든 메소드에 프록시 핸들러가 적용된다.](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%204.png)

모든 메소드에 프록시 핸들러가 적용된다.

만약 모든 메소드에 적용하지 않고 특정 메소드에만 적용하기 위해서는 method 매개변수의 메서드명을 조건문으로 검사해서 필터링할 수 있다.

```java
@Slf4j
@RequiredArgsConstructor
public class TimeInvocationMethodFilterHandler implements InvocationHandler {

    private final Object target;
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {

				// 메서드 필터링
        if(method.getName().equals("sum")){
            log.info("TimeProxy 실행");

            long startTime = System.currentTimeMillis();
            Object result = method.invoke(target, args);
            long endTime = System.currentTimeMillis();
            long resultTime = endTime - startTime;

            log.info("TimeProxy 종료 resultTime={}", resultTime);

            return result;
        }

        return method.invoke(target, args);
    }
}
```

```java
@Test
void dynamicC2() {
    CInterface target = new CImpl();
    TimeInvocationMethodFilterHandler handler = new TimeInvocationMethodFilterHandler(target);

    CInterface proxy = (CInterface) Proxy.newProxyInstance(
            CInterface.class.getClassLoader(),
            new Class[]{CInterface.class},
            handler
    );

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![sum메서드에만 프록시가 적용된다.](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%205.png)

sum메서드에만 프록시가 적용된다.

</aside>

## 동적 프록시 **제약 사항**

<aside>
✍️ **NOTE**

> *동적 프록시는 반드시 인터페이스를 파라미터로 입력해야 합니다. 프록시를 동적으로 생성하기 위해 인터페이스가 기반으로 사용되기 때문입니다.*
> 

그렇다면 인터페이스 없이 클래스만 있는 경우에는 동적 프록시를 어떻게 적용할 수 있을까요? 이를 위해 자바에서는 CGLIB라는 라이브러리를 사용합니다. 이 라이브러리는 바이트 코드를 조작하여 동적 프록시 기술을 응용하며, JDK를 사용하는 방법보다 동적 프록시 생성을 더 쉽게 할 수 있습니다.

</aside>

# CGLIB(Code Gnenrator Library)

---

<aside>
💡 **NOTE**

> *CGLIB는 JDK의 동적 프록시와 달리 클래스를 대상으로 바이트코드를 조작해 프록시를 생성할 수 있는 라이브러리입니다! 기본 동적 프록시보다 성능이 좋아 스프링 프레임워크에서 기본으로 내장되어 있습니다.*
> 

`CGLIB`를 사용하기 위해서는 `Enhancer` 객체로 프록시 객체를 만들어 `MethodInterceptor` 인터페이스로 프록시 핸들러를 등록해야 합니다.

```java
@Slf4j
@RequiredArgsConstructor
public class MyProxyInterceptor implements MethodInterceptor {

    private final Object target;

    @Override
    public Object intercept(Object obj,         // CGLIB가 적용된 객체
                            Method method,      // 호출된 메서드
                            Object[] args,      // 메서드를 호출하면서 전달된 인수
                            MethodProxy proxy   // 메서드 호출에 사용
    ) throws Throwable {

        log.info("TimeProxy 실행");
        long startTime = System.currentTimeMillis();

        Object result = method.invoke(target, args); // 파라미터로 전달받은 메서드를 invoke로 실행

        long endTime = System.currentTimeMillis();
        long resultTime = endTime - startTime;
        log.info("TimeProxy 종료 resultTime={}", resultTime);

        log.info("targetClass={}", target.getClass());
        log.info("proxyClass={}", proxy.getClass());

        return result;
    }
}

```

```java
public class Subject {
    public void call() {
        System.out.println("서비스 호출");
    }

    public void run() {
        System.out.println("서비스 실행");
    }
}
```

```java
@Test
void cglibTest() {

    // 1. 프록시 등록
    Enhancer enhancer = new Enhancer();
    
    // CGLIB는 구체 클래스를 상속받아서 프록시를 생성한다.
    enhancer.setSuperclass(Subject.class);
    
    // 프록시 핸들러
    enhancer.setCallback(new MyProxyInterceptor((new Subject())));

		// 2. 프록시 생성
    Subject proxy = (Subject) enhancer.create(); // setSuperClass()에 지정한 클래스를 상속받아 프록시 생성

		// 3. 프록시 호출
    proxy.call();
}
```

```java
@Test
void cglibTest2() {
    Subject proxy = (Subject) Enhancer.create(Subject.class, (MethodInterceptor) (o, method, args, methodProxy) -> {
        Subject target = new Subject();

        System.out.println("TimeProxy 실행");
        long startTime = System.nanoTime();

        Object result = method.invoke(target, args); // 파라미터로 전달받은 메서드를 invoke로 실행

        long endTime = System.nanoTime();
        long resultTime = endTime - startTime;
        System.out.println("TimeProxy 종료 resultTime = " + resultTime);

        return result;
    });

    proxy.call();
}
```

![앞에 배웠던 동적 프록시를 CGLIB가 자동으로 해주는거 말곤 크게 차이없음](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%206.png)

앞에 배웠던 동적 프록시를 CGLIB가 자동으로 해주는거 말곤 크게 차이없음

![Untitled](%5BSpring%20Study%5D%2008-3%20JDK%20%EB%8F%99%EC%A0%81%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9D%EC%8B%9C/Untitled%207.png)

</aside>