# [Spring Study] 08-4. 프록시 팩토리, Pointcut, Advice, Advisor ⭐

주제: Spring Study

- 참고
    
    [스프링이 지원하는 프록시](https://velog.io/@coconenne/a4vk148t)
    
    [[Spring] 프록시 팩토리(ProxyFactory)](https://yejun-the-developer.tistory.com/7)
    
    [6.6 ProxyFactory를 사용하여 프로그래밍 방식으로 AOP 프록시 만들기 by sh](https://wannaqueen.gitbook.io/spring5/spring-5.0/6-spring-aop-api/6.6)
    

# 프록시 팩토리(ProxyFactory)

---

<aside>
💡 **NOTE**

> ***프록시 팩토리**를 사용하는 경우 JDK 동적 프록시와, CGLIB 프록시 중 적절한 방법을 자동으로 선택해서 생성할 수 있습니다.*
> 

![ProxyFactory를 사용하면 JDK 동적프록시, CGLIB 중 하나를 알아서 판단하고 사용한다.](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled.png)

ProxyFactory를 사용하면 JDK 동적프록시, CGLIB 중 하나를 알아서 판단하고 사용한다.

**JDK 동적프록시**는 `InvocationHandler`를 **CGLIB**는 `MethodInterceptor`를 구현해야 했다. 그렇다면 프록시 팩토리도 각각을 따로 만들어서 제공하는가?

스프링은 이 문제를 해결하기 위해 `Adivce`라는 개념을 도입했습니다. 개발자는 앞의 두 객체를 신경쓰지 않고 Advice를 만들면 됩니다. 프록시 팩토리를 사용하면 `Advice`를 호출하는 적용 `InvocationHandler`, `MethodInterceptor`를 내부에서 만들어 줍니다.

![Advice를 통해 단순화해준다.](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%201.png)

Advice를 통해 단순화해준다.

![Advice 구조](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%202.png)

Advice 구조

```java
@Slf4j
public class TimeAdvice implements MethodInterceptor {

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        log.info("TimeProxy 실행");

        long startTime = System.currentTimeMillis();
        Object proceed = invocation.proceed() // target 없이 메서드 호출
        long endTime = System.currentTimeMillis();

        long resultTime = endTime - startTime;
        log.info("TimeProxy 종료 resultTime={}", resultTime);

        return proceed;
    }
}
```

```java
@Test
void advice(){
		// 실제 구현객체
    AInterface target = new AImpl();
    
    // 프록시 팩토리 생성(타겟 설정, 어드바이스 추가)
    ProxyFactory proxyFactory = new ProxyFactory(target);
    proxyFactory.addAdvice(new TimeAdvice());
    
    proxyFactory.setProxyTargetClass(true); // 무조건 CGLIB 사용

		// 프록시 생성
    AInterface proxy = (AInterface) proxyFactory.getProxy();
    
	  // 호출
    proxy.call();
    
    log.info("targetClass={}", target.getClass());
    log.info("proxyClass={}", proxy.getClass());
}
```

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%203.png)

스프링 부트는 AOP를 적용할 때 기본적으로 `proxyTargetClass=true`로 설정하고, 이를 통해 인터페이스가 있어도 항상 CGLIB를 사용하여 구체 클래스를 기반으로 프록시를 생성합니다.

- 자세한 이유는 이후에 설명하겠습니다.
</aside>

# Pointcut, Advice, Advisor

---

<aside>
💡 **NOTE**

![Pointcut, Advice, Advisor 관계도](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%204.png)

Pointcut, Advice, Advisor 관계도

- `Pointcut`: 어디에 부가 기능을 적용할지, 어디에 부가 기능을 적용하지 않을지 판단하는 필터로직
    - 주로 클래스와 메서드 이름으로 필터링한다.
- `Advice`: 프록시가 호출하는 부가 기능이며, 단순하게 프록시 로직이라고 생각하면 된다.
- `Advisor`: `Pointcut + Advice` 개념이라 생각하면 된다.

스프링 AOP는 역할과 책임을 명확히 분리합니다. `Pointcut`은 대상 여부를 확인하는 필터 역할만 담당하고 `Adivce`는 부가 기능 로직만 담당합니다. 이 둘을 합쳐서 `Advisor`가 이루어집니다.

![동작 흐름도](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%205.png)

동작 흐름도

```java
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
@Test
void advisorTest1(){
		// 타겟 생성
    CInterface target = new CImpl();

		// 프록시 팩토리 생성 & advisor 생성
    ProxyFactory proxyFactory = new ProxyFactory(target);
    DefaultPointcutAdvisor advisor =
            new DefaultPointcutAdvisor(Pointcut.TRUE, new TimeAdvice());

		// Advisor 등록
    proxyFactory.addAdvisor(advisor);
    CInterface proxy = (CInterface) proxyFactory.getProxy();

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![결과](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%206.png)

결과

</aside>

## Pointcut 직접 구현하기

<aside>
✍️ **NOTE**

> `*Pointcut.TRUE`의 경우 모든 메서드에 프록시를 적용하게 됩니다. `Pointcut`을 만들어서 `call()` 메서드에만 프록시가 적용되게 해봅시다.*
> 

```java
static class MyPointcut implements Pointcut {
    @Override
    public ClassFilter getClassFilter() {
        return ClassFilter.TRUE;
    }

    @Override
    public MethodMatcher getMethodMatcher() {
        return null;
    }
}

static class MyMethodMatcher implements MethodMatcher{
    private String matchName = "save";

    // 적용여부
    @Override
    public boolean matches(Method method, Class<?> targetClass) {
        boolean result = method.getName().equals(matchName);
        return result;
    }

    // 런타임 시점에 수행되는지 여부
    @Override
    public boolean isRuntime() {
        return false;
    }

    // 매개변수를 포함하여 런타임시점 매칭여부
    @Override
    public boolean matches(Method method, Class<?> targetClass, Object... args) {
        throw  new UnsupportedOperationException(); // 지원하지 않음
    }
}
```

```java
@Test
void advisorTest2() {
		// 타겟 생성
    CInterface target = new CImpl();

		// 프록시 팩토리 생성 & advisor 생성
    ProxyFactory proxyFactory = new ProxyFactory(target);
    DefaultPointcutAdvisor advisor =
            new DefaultPointcutAdvisor(new MyPointcut(), new TimeAdvice());

		// Advisor 등록
    proxyFactory.addAdvisor(advisor);
    CInterface proxy = (CInterface) proxyFactory.getProxy();

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%207.png)

</aside>

## 스프링 제공 Pointcut

<aside>
✍️ **NOTE**

> *스프링은 다양한 Pointcut을 기본으로 제공합니다.*
> 

```java
@Test
void advisorTest3() {
    CInterface target = new CImpl();

		// 메소드 이름 Pointcut
    NameMatchMethodPointcut namePointcut = new NameMatchMethodPointcut();
    namePointcut.setMappedNames("call");

		// 정규식 Pointcut
    JdkRegexpMethodPointcut regexPointcut = new JdkRegexpMethodPointcut();
    regexPointcut.setPattern(".*sum.*");
    
    // 어노테이션 Pointcut
    AnnotationMatchingPointcut annotationPointcut = new AnnotationMatchingPointcut(MyAnnotation.class);

		// AspectJ Pointcut(적용)
    AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
    aspectJPointcut.setExpression("execution(* com.example.study..*(..))");

    ProxyFactory proxyFactory = new ProxyFactory(target);
    DefaultPointcutAdvisor advisor =
            new DefaultPointcutAdvisor(aspectJPointcut, new TimeAdvice());

    proxyFactory.addAdvisor(advisor);
    CInterface proxy = (CInterface) proxyFactory.getProxy();

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%208.png)

</aside>

## 여러개의 Advisor 적용하기

<aside>
✍️ **NOTE**

> *프록시에 여러 Advisor를 적용할수도 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%209.png)

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%2010.png)

```java
@Test
void advisorTest4() {
    // proxy -> advisor2 -> advisor1 -> target
    CInterface target = new CImpl();

    NameMatchMethodPointcut namePointcut = new NameMatchMethodPointcut();
    namePointcut.setMappedNames("call");

    JdkRegexpMethodPointcut regexPointcut = new JdkRegexpMethodPointcut();
    regexPointcut.setPattern(".*sum.*");

    ProxyFactory proxyFactory = new ProxyFactory(target);
    
    // Advisor 여러개 등록
    DefaultPointcutAdvisor advisor1 =
            new DefaultPointcutAdvisor(namePointcut, new TimeAdvice());
    DefaultPointcutAdvisor advisor2 =
            new DefaultPointcutAdvisor(regexPointcut, new TimeAdvice());

		// 여러개의 Advisor 등록
    proxyFactory.addAdvisor(advisor1);
    proxyFactory.addAdvisor(advisor2);
    CInterface proxy = (CInterface) proxyFactory.getProxy();

    proxy.call();
    proxy.sum(1, 2);
    proxy.print();
}
```

![Untitled](%5BSpring%20Study%5D%2008-4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%ED%8C%A9%ED%86%A0%EB%A6%AC,%20Pointcut,%20Advice,%20Adv/Untitled%2011.png)

</aside>

## 프록시 팩토리 문제점

<aside>
✍️ **NOTE**

1. **너무 많은 설정**
    - MVC 3개 클래스에 적용하는것만 해도 코드량이 상당한데 만약 100개가 넘어간다면..?
    - 최근에는 스프링 빈을 등록하는것이 귀찮아 컴포넌트 스캔까지 사용하는데 직접 등록하고 프록시를 적용하는건 너무 힘들다.

1. **컴포넌트 스캔**
    - **컴포넌트 스캔을 사용하는 경우는 프록시 적용이 불가능하다.**
    - 실제 객체를 컴포넌트 스캔으로 스프링 컨테이너에 이미 빈으로 등록을 다 해버린 상태이기 때문
    - **지금까지 학습한 프록시를 적용하려면 실제 객체가 아닌 프록시를 빈으로 등록**해야 한다.

**⇒ 위의 2문제를 해결하는 것이 이후 설명할 빈 후처리기!**

</aside>