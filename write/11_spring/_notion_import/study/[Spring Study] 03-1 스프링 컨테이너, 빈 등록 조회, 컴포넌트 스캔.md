# [Spring Study] 03-1. 스프링 컨테이너, 빈 등록/조회, 컴포넌트 스캔

주제: Spring Study

- 참고
    
    [7. 스프링 컨테이너 생성 과정](https://gdlovehush.tistory.com/465?category=993329)
    
    [8. 스프링 빈 조회 - 상속 관계](https://gdlovehush.tistory.com/468?category=993329)
    
    [9. 스프링 컨테이너의 다양한 설정 형식 - 자바 코드, XML](https://gdlovehush.tistory.com/469?category=993329)
    
    [12. 컴포넌트 스캔과 의존관계 자동 주입 시작하기](https://gdlovehush.tistory.com/473?category=993329)
    

# 스프링 컨테이너의 생성 및 관리

---

<aside>
💡 **NOTE**

> *스프링 컨테이너는 스프링의 빈(bean) 생성, 관리, 조회 등을 담당하는 객체입니다. 이는 XML 또는 애노테이션 기반의 자바 설정 클래스로 구성될 수 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled.png)

```java
// 스프링 컨테이너 생성
ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfig.class);
```

스프링 컨테이너는 `BeanFactory`와 `ApplicationContext` 두 종류의 인터페이스로 구현되어 있습니다. 일반적으로 스프링 컨테이너는 `ApplicationContext`를 사용합니다.

`BeanFactory`는 스프링의 기본적인 IOC 컨테이너이며 빈의 등록/생성/조회를 관리하며 `getBean()` 메서드를 통해 빈을 인스턴스화 할 수 있습니다.

![BeanDefinition을 통한 Bean생성](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%201.png)

BeanDefinition을 통한 Bean생성

`ApplicationContext`는 BeanFactory의 기능을 상속받아 제공해주며, BeanFactory의 기능 이외의 부가 기능을 제공해줍니다. 아래는 부가 기능의 종류입니다.

![ApplicationContext는 여러 인터페이스를 상속받아서 국제화, 이벤트, 리소스 조회 등의 기능을 제공한다](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%202.png)

ApplicationContext는 여러 인터페이스를 상속받아서 국제화, 이벤트, 리소스 조회 등의 기능을 제공한다

- `MessageSource`(메시지 다국화 인터페이스)
- `ApplicationEvenePublisher`(이벤트 관련 기능)
- `ResourceLoader`(파일, 클래스 등 리소스 조회)
</aside>

## @Configuration 빈 등록

<aside>
✍️ **NOTE**

> *스프링 컨테이너는 스프링 설정 클래스(`@Configuration`)에서 빈을 등록할 수 있습니다. 기본적으로 메서드 이름을 사용하지만 `@Bean(name=”customName”)`으로 명시적으로 부여할 수도 있습니다.*
> 

```java
@Configuration
public class AppConfig {

		// 이름으로 명시가능
    @Bean(name = "memberService")
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(
                memberRepository(),
                discountPolicy()
        );
    }

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }

    @Bean
    public DiscountPolicy discountPolicy() {
        return new RateDiscountPolicy();
    }
}

```

![@Bean이름 - Bean 객체로 저장된다.](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%203.png)

@Bean이름 - Bean 객체로 저장된다.

![AppConfig를 참조해 의존관계를 주입(DI)한다!](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%204.png)

AppConfig를 참조해 의존관계를 주입(DI)한다!

</aside>

## @ComponentScan 빈 등록

<aside>
✍️ **NOTE**

> *스프링은 `@ComponentScan` 어노테이션을 사용해서 지정된 패키지 및 하위 패키지를 탐색하여 `@Component`가 붙은 클래스를 찾아 자동으로 빈에 등록해줍니다.*
> 

```java
@Component
public class MemberServiceImpl implements MemberService {
    private final MemberRepository memberRepository;

		// 자동으로 주입시켜준다.
    @Autowired
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
}

@Component
public class MemoryMemberRepository implements MemberRepository {}
```

스프링 부트를 사용할 경우, 기본적으로 `@SpringBootApplication`이 등록되어 있고, 이 내부에는 `@ComponentScan`이 포함되어 있습니다.

```java
// basePackage: 해당 경로부터 하위 패키지를 모두 검색합니다.
@ComponentScan( basePackages = "hello.core" )

```

![스프링 부트를 실행시키면 자동으로 빈이 등록됨](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%205.png)

스프링 부트를 실행시키면 자동으로 빈이 등록됨

스프링 부트를 실행하면 자동으로 빈이 등록됩니다.

스프링은 다음과 같은 어노테이션도 기본 스캔 대상에 포함합니다. 참고로 각 어노테이션은 내부에 @Component를 가지고 있습니다. 이 어노테이션들은 컴포넌트 스캔의 대상이 되면서 추가적인 기능들을 수행합니다.

- `@Controller`: MVC 컨트롤러로 인식합니다.
- `@Service`: 비즈니스 로직을 처리하는 서비스 레이어로 인식합니다.
- `@Repository` : 데이터 계층의 예외를 스프링 예외로 반환합니다.
- `@Configuration`: 설정 정보로 인식하고, 빈 정의를 담당합니다.
</aside>

## **컨테이너에 등록된 빈 조회**

<aside>
✍️ **NOTE**

```java
@Test
void findApplicationBean(){
  String[] beanDefinitionNames = ac.getBeanDefinitionNames();
  for (String beanDefinitionName : beanDefinitionNames) {

    // Bean의 메타데이터
    BeanDefinition beanDefinition = ac.getBeanDefinition(beanDefinitionName);

    // 내가 등록한 Bean
    // BeanDefinition.ROLE_APPLICATION : 직접 등록한 애플리케이션 빈
    // BeanDefinition.ROLE_INFRASTRUCTURE : 스프링 내부에서 사용하는 빈
    if(beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION){
        Object bean = ac.getBean(beanDefinitionName);
        System.out.println("beanDefinitionName = " + beanDefinitionName + " object = " + bean);
    }
  }
}
```

```java
@Test
void findBean() {
		// 이름 조회
    MemberService memberService = ac
	    .getBean("memberService", MemberService.class);
    assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
    
    // 타입 조회
    MemberService memberService = ac
	    .getBean**(MemberService.class);**
    assertThat(memberService).isInstanceOf**(MemberServiceImpl.class);**
    
    
}
```

### 동일 타입 빈이 2개인 경우

```java
@Configuration
static class SameBeanConfig {

    @Bean
    public MemberRepository memberRepository1() {
        return new MemoryMemberRepository();
    }

    @Bean
    public MemberRepository memberRepository2() {
        return new MemoryMemberRepository();
    }
}
```

```java
@Test
void findBeanByTypeDuplicate(){
    assertThrows(NoUniqueBeanDefinitionException.class,
            () -> ac.getBean(MemberRepository.class));
}
```

![실제 발생에러](%5BSpring%20Study%5D%2003-1%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EB%B9%88%20%EB%93%B1%EB%A1%9D%20%EC%A1%B0%ED%9A%8C,%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%8A%A4%EC%BA%94/Untitled%206.png)

실제 발생에러

```java
@Test
void findBeanByName(){
		// 빈 이름으로 타입을 구분해서 조회한다.
    MemberRepository memberRepository = ac
	    .getBean("memberRepository1",MemberRepository.class);
    assertThat(memberRepository).isInstanceOf(MemberRepository.class);
}
```

```java
@Test
void findAllBeanByType(){
		// getBeansOfType() => Map<이름, 타입> 으로 전체조회
    Map<String, MemberRepository> beansOfType = ac
	    .getBeansOfType(MemberRepository.class);
	    
    for (String key : beansOfType.keySet()) {
        System.out.println("key = " + key + "value = " + beansOfType.get(key));
    }

    System.out.println("beansOfType = " + beansOfType);
    assertThat(beansOfType.size()).isEqualTo(2);
}
```

</aside>