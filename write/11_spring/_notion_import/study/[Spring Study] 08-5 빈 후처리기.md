# [Spring Study] 08-5. 빈 후처리기

주제: Spring Study
연관 노트: [Spring Study] 03-4. 빈 생명주기(@Post, @Destroy) /스코프 (https://www.notion.so/Spring-Study-03-4-Post-Destroy-164d98dd212346a4a8bb1c1beba7408e?pvs=21)

- 참고
    
    [[AOP] 빈 후처리기(BeanPostProccessor)와AnnotationAwareAspectJAutoProxyCreator](https://ttl-blog.tistory.com/864)
    
    [[Spring] 스프링이 제공하는 빈 후처리기](https://hyuuny.tistory.com/94)
    

# Bean 후처리기(BeanPostProcessor)

---

<aside>
💡 **NOTE**

> ***스프링 Bean 후처리기**를 사용하면 스프링 컨테이너에 Bean을 등록하기 직전에 Bean을 조작하거나, 완전히 다른 객체로 바꿔칠 수 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled.png)

Bean 후처리기의 주요 기능은 다음과 같습니다.

1. Bean 조작: 생성된 Bean의 속성을 변경하거나 특정 메소드를 호출할 수 있습니다.
2. 객체 바꿔치기: 생성된 Bean 대신에 완전히 다른 객체를 반환하여 스프링 컨테이너에 등록할 수 있습니다.

스프링은 `CommonAnnotationBeanPostProcessor`라는 Bean 후처리기를 자동으로 등록하며, 이를 통해서 스프링 생명주기 애노테이션을 지원합니다.

- ex) `@PostConstruct`, `@PreDestroy`, `@Resource`

Bean 후처리기를 테스트 하기 위해 **A 객체**를 **B 객체**로 바꿔치는 예제코드를 작성해보겠습니다.

```java
@Slf4j
public class A {
    public void helloA() {
        log.info("hello A");
    }
}

@Slf4j
public class B {
    public void helloB() {
        log.info("hello B");
    }
}
```

```java
@Test
void beanPostProcessorTest(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(BasicConfig.class);

    // A는 Bean으로 등록된다.
    A beanA = applicationContext.getBean("beanA", A.class);

    // B는 Bean으로 등록되지 않는다.
    Assertions.assertThrows(NoSuchBeanDefinitionException.class,
            () -> applicationContext.getBean(B.class));
}

@Slf4j
@Configuration
static class BasicConfig {
		// A만 등록한다.
    @Bean(name = "beanA")
    public A a() {
        return new A();
    }
}
```

```java
@Slf4j
static class AToBPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        log.info("beanName={} bean={}", beanName, bean);
        if (bean instanceof A) {
            return new B();
        }
        return bean;
    }
}
```

```java
@Test
void beanPostProcessorTest(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(BasicConfig.class);

    // B는 Bean으로 등록된다.
    B beanB = applicationContext.getBean("beanA", B.class);

    // A는 Bean으로 등록되지 않는다. (바꿔치기됨)
    Assertions.assertThrows(NoSuchBeanDefinitionException.class,
            () -> applicationContext.getBean(A.class));
}

@Slf4j
@Configuration
static class BasicConfig {
    @Bean(name = "beanA")
    public A a() {
        return new A();
    }

    @Bean
    public AToBPostProcessor helloPostProcessor() {
        return new AToBPostProcessor();
    }
}
```

</aside>

## Bean  후처리기 프록시 적용

<aside>
✍️ **NOTE**

> ***스프링 Bean 후처리기**를 사용해 실제 객체 대신 프록시 객체를 스프링 빈으로 등록해봅시다!*
> 

![빈 후처리기 프로세스](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled%201.png)

빈 후처리기 프로세스

```java
@Slf4j
static class PackageLogTraceProxyPostProcessor implements BeanPostProcessor {
    private final String basePackage;
    private final Advisor advisor;

    public PackageLogTraceProxyPostProcessor(String basePackage, Advisor advisor) {
        this.basePackage = basePackage;
        this.advisor = advisor;
    }
    
    // 빈 초기화 이후 프록시 적용
    @Override
    public Object postProcessAfterInitialization(Object bean,
                                                 String beanName
    ) throws BeansException {
        log.info("param beanName={} bean={}", beanName, bean.getClass());

        // 프록시 적용 대상 여부 체크(패키지 경로 체크)
        // 프록시 적용 대상이 아니면 원본을 그대로 반환
        String packageName = bean.getClass().getPackageName();
        if (!packageName.startsWith(basePackage)) {
            return bean;
        }

        // 프록시 대상이면 프록시를 만들어서 반환
        ProxyFactory proxyFactory = new ProxyFactory(bean);
        proxyFactory.addAdvisor(advisor);
        Object proxy = proxyFactory.getProxy();
        log.info("create proxy: target={} proxy={}", bean.getClass(), proxy.getClass());
        return proxy;
    }
}
```

- `PackageLogTraceProxyPostProcessor`는 특정 패키지 내의 Bean들에 대해 프록시를 적용합니다. 이때 프록시 팩토리를 사용하여 Advisor를 적용합니다.
- 현재는 A,B는 프록시가 적용되며, Pointcut은 A에만 적용되도록 설정한다.

```java
@Slf4j
@Configuration
static class BasicConfig {
    @Bean(name = "beanA")
    public A a() {
        return new A();
    }

    @Bean(name = "beanB")
    public B b() {
        return new B();
    }

    @Bean
    public PackageLogTraceProxyPostProcessor packageLogTraceProxyPostProcessor() {
        return new PackageLogTraceProxyPostProcessor("com.example.study.aop", getAdvisor());
    }

    private Advisor getAdvisor() {
        AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
        aspectJPointcut.setExpression("within(com.example.study.aop.BeanPostProcessorTest.A)");

        return new DefaultPointcutAdvisor(aspectJPointcut, new TimeAdvice());
    }
}
```

```java
@Test
void beanPostProcessorTest2(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(BasicConfig.class);

    // A는 프록시로 등록된다.
    A proxyA = applicationContext.getBean(A.class);
    proxyA.helloA();

    // B는 프록시로 등록되지 않는다.
    B beanB = applicationContext.getBean(B.class);
    beanB.helloB();
}
```

![Untitled](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled%202.png)

</aside>

# 스프링이 제공하는 빈 후처리기

---

<aside>
💡 **NOTE**

> *스프링 부트는 자동 설정으로 `AnnotationAwareAspectAutoProxyCreator`라는 Bean 후처리기가 스프링 빈에 자동으로 등록됩니다. 이 Bean 후처리기는 자동으로 Proxy를 생성해주는 역할을 해줍니다.*
> 

```groovy
implementation 'org.springframework.boot:spring-boot-starter-aop'
```

![위로 계속 올라가면 BeanProcessor를 구현받고 있는걸 확인할 수 있다.](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled%203.png)

위로 계속 올라가면 BeanProcessor를 구현받고 있는걸 확인할 수 있다.

</aside>

## 자동 프록시 생성기 - AutoProxyCreator

<aside>
✍️ **NOTE**

![프록시 흐름](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled%204.png)

프록시 흐름

```java
@Slf4j
@Configuration
@EnableAspectJAutoProxy // 실제 스프링부트에서는 필요없음(자동등록)
static class BasicConfig {
    @Bean(name = "beanA")
    public A a() {
        return new A();
    }

    @Bean(name = "beanB")
    public B b() {
        return new B();
    }

		// Advisor 빈등록(자동 빈후처리기가 찾아서 등록함)
		// A 클래스 등록
    @Bean
    public Advisor timeAdvisor(){
        AspectJExpressionPointcut aspectJPointcut = new AspectJExpressionPointcut();
        aspectJPointcut.setExpression("within(com.example.study.aop.BeanPostProcessorTest.A)");

        return new DefaultPointcutAdvisor(aspectJPointcut, new TimeAdvice());
    }
}
```

```java
@Test
void autoProxyTest(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(BasicConfig.class);

    // A는 프록시로 등록된다.
    A proxyA = applicationContext.getBean(A.class);
    proxyA.helloA();

    // B는 프록시로 등록되지 않는다.
    B beanB = applicationContext.getBean(B.class);
    beanB.helloB();
}
```

![Untitled](%5BSpring%20Study%5D%2008-5%20%EB%B9%88%20%ED%9B%84%EC%B2%98%EB%A6%AC%EA%B8%B0/Untitled%205.png)

- 빈 후처리기를 등록하지 않아도, 자동으로 등록된 빈 후처리기가 `A`를 프록시로 만들어주었습니다.
</aside>