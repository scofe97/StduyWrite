# [Spring Study] 09-7. Pointcut 어노테이션 종류

주제: Spring Study

- 참고
    
    [스프링 AOP - 포인트컷](https://velog.io/@coconenne/스프링-AOP-포인트컷)
    
    [[Spring] AOP Pointcut execution](https://hyuuny.tistory.com/101)
    

# **포인트컷 지시자 종류**

---

<aside>
💡 **NOTE**

> ***포인트컷 표현식**은 `execution`같은 **포인트컷 지시자(Pointcut Designator)** 줄여서 PCD라고 한다.*
> 

![AspectJExpressionPointcut은 포인트컷 표현식을 처리해주는 클래스! (자세히 보면 위에 Pointcut을 받음)](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled.png)

AspectJExpressionPointcut은 포인트컷 표현식을 처리해주는 클래스! (자세히 보면 위에 Pointcut을 받음)

- **execution (사실 이것만 알아도 됨!)** ✅
    - 메소드 실행 조인 포인트를 매칭한다.
    - 스프링 AOP에서 가장 많이 사용하고, 기능도 복잡하다.
- `within`
    - exectuion에서 타입 부분만 사용한다고 보면된다.
- `args`
    - 인자가 주어진 타입의 인스턴스인 조인 포인트로 매칭한다.
- `this`
    - 스프링 빈 객체(스프링 AOP 프록시)를 대상으로 하는 조인 포인트
- `target`
    - Target 객체(스프링 AOP 프록시가 가르키는 실제 대상)을 대상으로하는 조인 포인트
- `@target`
    - 실행 객체의 클래스에 주어진 타입의 애노테이션이 있는 조인 포인트
- `@within`
    - 주어진 애노테이션이 있는 타입 내 조인 포인트
- `@annotaion`
    - 메서드가 주어진 애노테이션을 가지고 있는 조인포인트를 매칭
- `@args`
    - 전달된 실제 인수의 런타임 타입이 주어진 타입의 애노테이션을 갖는 조인 포인트
- `bean`
    - 스프링 전용 포인트컷 지시자
    - 빈의 이름으로 포인트컷을 지정한다.

- 여러 지시자중, `execution`을 가장 많이 사용하고, 나머지는 잘 사용하지 않으니 execution을 중점적으로 학습하자!
</aside>

## AspectJ Pointcut 표현식

<aside>
✍️ **NOTE**

> `*AspectJExpressionPointcut`을 사용하면, 정밀한 `Pointcut`을 설정할 수 있습니다.*
> 

```java
// A만 적용됩니다.
@Bean
public Advisor timeAdvisor(TimeAdvice timeAdvice) {
    AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
    aspectJPointcut.setExpression("within(com.example.study.aop.AutoProxyConfig.A)");
    return new DefaultPointcutAdvisor(aspectJPointcut, timeAdvice);
}

// A,B 둘다 적용됩니다.
@Bean
public Advisor timeAdvisor2(TimeAdvice timeAdvice) {
    AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
    aspectJPointcut.setExpression("execution(* com.example.study.aop.AutoProxyConfig..*(..))");
    return new DefaultPointcutAdvisor(aspectJPointcut, timeAdvice);
}

// A,B 둘다 적용되지 않습니다.
@Bean
public Advisor timeAdvisor3(TimeAdvice timeAdvice) {
    AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
    aspectJPointcut.setExpression("execution(* hello.proxy.app.test..*(..))");
    return new DefaultPointcutAdvisor(aspectJPointcut, timeAdvice);
}
```

![Untitled](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%201.png)

### AspectJ Pointcut 표현식

- `execution`: 메서드 실행(join point)에 대한 매칭을 정의한다.
    - `modifiers-pattern`: 메서드의 접근 제어자(public, private 등)
    - `ret-type-pattern`: 메서드의 반환 타입
    - `declaring-type-pattern`: 메서드를 선언한 타입(클래스)
    - `name-pattern`: 메서드 이름 패턴
    - `param-pattern`: 메서드의 파라미터 패턴
    - `throws-pattern`: 메서드가 던질 수 있는 예외
- `within`: 특정 타입에 대한 매칭을 정의한다.
</aside>

## **execution** ⭐

<aside>
✍️ **NOTE**

```java
execution(접근제어자? 반환타입 선언타입?메서드이름(파라미터) 예외?)
```

- 메소드 실행 조인 포인트를 매칭한다.
- `?`는 생략할 수 있다.
- `*`같은 패턴을 지정할 수 있다.

```java
// 가장 정확하게 매칭하는 방법
@Test
void exactMatch() {
    pointcut.setExpression("execution(public String hello.aop.member.MemberServiceImpl.hello(String))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 가장 생략한 방법
@Test
void allMatch() {
    pointcut.setExpression("execution(* *(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

- **매칭 조건**
    - 접근 제어자? : `public`
    - 반환타입 : `String`
    - 선언타입?: `hello.aop.member.MemberServiceImpl`
    - 메서드: `hello`
    - 파라미터: `(String)`
    - 예외?: 생략

```java
// 메서드 이름패턴으로 조회
@Test
void nameMatchStar1() {
    pointcut.setExpression("execution(* hel*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 메서드 이름패턴으로 조회
@Test
void nameMatchStar2() {
    pointcut.setExpression("execution(* *el*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

```java
// 패키지 이름패턴으로 조회
@Test
void packageExactMatch2() {
    pointcut.setExpression("execution(* hello.aop.member.*.*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 패키지 이름패턴으로 조회
@Test
void packageExactSubPackage2() {
    pointcut.setExpression("execution(* hello.aop..*.*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

- `.` : 정확하게 해당 위치의 패키지
- `..` : 해당 위치의 패키지와 그 하위 패키지도 포함한다.

```java
// 타입 조회
@Test
void typeExactMatch() {
    pointcut.setExpression("execution(* hello.aop.member.MemberServiceImpl.*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 부모타입 조회
@Test
void typeExactMatchSuperType() {
    pointcut.setExpression("execution(* hello.aop.member.MemberService.*(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

```java
// String 타입의 파라미터 허용
// (String)
@Test
void argsMatch() {
    pointcut.setExpression("execution(* *(String))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 파라미터가 없는 경우
// ()
@Test
void argsMatchNoArgs() {
    pointcut.setExpression("execution(* *())");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isFalse();
}

// 정확하게 하나의 파라미터 허용, 모든 타입 허용
// (XXX)
@Test
void argsMatchStar() {
    pointcut.setExpression("execution(* *(*))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 모든 파라미터 타입과 개수 허용
// (), (XXX), (XXX, XXX)
@Test
void argsMatchAll() {
    pointcut.setExpression("execution(* *(..))");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

</aside>

## **within**

<aside>
✍️ **NOTE**

> ***execution에서 타입 부분만 사용한다. (별로 안씀)***
> 

```java
@Test
void withinExact() {
    pointcut.setExpression("within(hello.aop.member.MemberServiceImpl)");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}

// 클래스 패턴매칭
@Test
void withinStar() {
    pointcut.setExpression("within(hello.aop.member.*Service*");
    Assertions.assertThat(pointcut.matches(helloMethod, MemberServiceImpl.class)).isTrue();
}
```

</aside>

## **args**

<aside>
✍️ **NOTE**

> ***execution에서 인자값만 사용한다. (별로 안씀)***
> 

```java
// exection -> 메서드의 시그니처로 판단 (정적)
// args -> 런타임에 전달된 인수로 판단 (동적)
@Test
void argsVsExecution(){
    // Args
    Assertions.assertThat(pointcut("args(String)")
            .matches(helloMethod, MemberServiceImpl.class)).isTrue();
    Assertions.assertThat(pointcut("args(java.io.Serializable)") // Serializable은 String의 부모타입중 하나
            .matches(helloMethod, MemberServiceImpl.class)).isTrue();
    Assertions.assertThat(pointcut("args(Object)")
            .matches(helloMethod, MemberServiceImpl.class)).isTrue();

    // Execution
    Assertions.assertThat(pointcut("execution(* *(String))")
            .matches(helloMethod, MemberServiceImpl.class)).isTrue();
    Assertions.assertThat(pointcut("execution(* *(java.io.Serializable))")
            .matches(helloMethod, MemberServiceImpl.class)).isFalse();
    Assertions.assertThat(pointcut("execution(* *(Object))")
            .matches(helloMethod, MemberServiceImpl.class)).isFalse();
}
```

</aside>

## **@target, @within**

<aside>
✍️ **NOTE**

> ***특정 조건의 애노테이션이 있는지 확인한다!***
> 

![@target → 인스턴스의 모든 메서드를 조인 포인트로 적용
@within → 해당 타입 내의 메서드만 조인 포인트로 사용](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%202.png)

@target → 인스턴스의 모든 메서드를 조인 포인트로 적용
@within → 해당 타입 내의 메서드만 조인 포인트로 사용

```java
@Around("execution(* hello.aop..*(..)) && @target(hello.aop.member.annotation.ClassAop)")
public Object atTarget(ProceedingJoinPoint joinPoint) throws Throwable {
    log.info("[@target] {}", joinPoint.getSignature());
    return joinPoint.proceed();
}

//@within: 선택된 클래스 내부에 있는 메서드만 조인 포인트로 선정, 부모 타입의 메서드는적용되지 않음
@Around("execution(* hello.aop..*(..)) && @within(hello.aop.member.annotation.ClassAop)")
public Object atWithin(ProceedingJoinPoint joinPoint) throws Throwable {
    log.info("[@within] {}", joinPoint.getSignature());
    return joinPoint.proceed();
}
```

![target은 상위 타입까지 log가 나오지만, within은 안나옴](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%203.png)

target은 상위 타입까지 log가 나오지만, within은 안나옴

- `execution`을 사용하는 이유는 `@target`의 경우 실행 시점에 일어나는 포인트컷 적용 여부도 결국 프록시가 있어야 실행 시점에 판단할 수 있다.
- 프록시를 생성하는 시점은 스프링 컨테이너가 만들어지는 애플리케이션 로딩 시점에 적용할 수 있으며, `@target`과 같은 포인트컷 지시자가 있으면 스프링은 모든 스프링 빈에 AOP를 적용하려고 시도한다.
- 내부에서 사용하는 빈 중에는 `final`로 지정된 빈들도 있기 때문에 오류가 생길 수 있어, 프록시 적용 대상을 축소하는 표현식을 사용한다.
</aside>

## **@annotation, @args**

<aside>
✍️ **NOTE**

> ***메서드가 주어진 애노테이션을 가지고 매칭한다.***
> 

```java
@Override
@MethodAop("test value")
public String hello(String param) {
    return "ok";
}
```

```java
@Aspect
static class AtAnnotationAspect{
  @Around("@annotation(hello.aop.member.annotation.MethodAop)")
  public Object doAtAnnotation(ProceedingJoinPoint joinPoint) throws Throwable {
      log.info("[@annotation] {}", joinPoint.getSignature());
      return joinPoint.proceed();
  }
}
```

```java
@args(test.Check)
```

- `@args`는 파라미터에 애노테이션이 있으면 검색하는 용도
</aside>

## **bean**

<aside>
✍️ **NOTE**

> ***스프링 빈 이름으로 포인트컷을 매칭한다!***
> 

```java
@Aspect
static class BeanAspect {
    @Around("bean(orderSerivce) || bean(*Repository)")
    public Object doLog(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("[bean] {}", joinPoint.getSignature());
        return joinPoint.proceed();
    }
}
```

</aside>

## **매개변수 전달**

<aside>
✍️ **NOTE**

> ***위에서 사용한 개념들을 스프링의 Advice에 매개변수로 사용할 수 있다!***
> 

```java
@Pointcut("execution(* hello.aop.member..*.*(..))")
private void allMember() {
}

@Around("allMember()")
public Object logArgs1(ProceedingJoinPoint joinPoint) throws Throwable {
    Object arg1 = joinPoint.getArgs()[0];
    log.info("[logArgs1]{}, arg={}", joinPoint.getSignature(), arg1);
    return joinPoint.proceed();
}

@Around("allMember() && args(arg, ..)")
public Object logArgs2(ProceedingJoinPoint joinPoint, Object arg) throws Throwable {
    log.info("[logArgs2]{}, arg={}", joinPoint.getSignature(), arg);
    return joinPoint.proceed();
}

@Before("allMember() && args(arg, ..)")
public void logArgs3(String arg) {
    log.info("[logArgs3]{}, arg={}", arg);
}

@Before("allMember() && this(obj)")
public void thisArgs(JoinPoint joinPoint, MemberService obj){
    log.info("[this]{}, obj={}", joinPoint.getThis(), obj.getClass());
}

@Before("allMember() && target(obj)")
public void targetArgs(JoinPoint joinPoint, MemberService obj){
    log.info("[target]{}, obj={}", joinPoint.getThis(), obj.getClass());
}

@Before("allMember() && @target(annotation)")
public void atTarget(JoinPoint joinPoint, ClassAop annotation){
    log.info("[@target]{}, obj={}", joinPoint.getSignature(), annotation);
}

@Before("allMember() && @within(annotation)")
public void atWithin(JoinPoint joinPoint, ClassAop annotation){
    log.info("[@within]{}, obj={}", joinPoint.getSignature(), annotation);
}

@Before("allMember() && @annotation(annotation)")
public void atWithin(JoinPoint joinPoint, MethodAop annotation){
    log.info("[@annotation]{}, annotationValue={}", joinPoint.getSignature(), annotation.value());
}
```

</aside>

## **this, target**

<aside>
✍️ **NOTE**

![JDK 동적 프록시 → proxy(this)의 impl을 찾을 수 없음](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%204.png)

JDK 동적 프록시 → proxy(this)의 impl을 찾을 수 없음

![CGLIB → proxy(this)의 impl을 찾을 수 있음!](%5BSpring%20Study%5D%2009-7%20Pointcut%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EC%A2%85%EB%A5%98/Untitled%205.png)

CGLIB → proxy(this)의 impl을 찾을 수 있음!

- `this`
    - 스프링 빈 객체(스프링 AOP 프록시)를 대상으로 하는 조인 포인트
- `target`
    - target 객체(스프링 AOP 프록시가 가르키는 실제 대상)을 대상으로 하는 조인 포인트
</aside>