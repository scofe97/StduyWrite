# [Spring Study] 01-4. 객체지향 원리 적용(DI, IoC) ⭐

주제: Spring Study
연관 노트: [Spring MSA] 05-3. 도메인 영역의 주요 구성요소 (https://www.notion.so/Spring-MSA-05-3-ded45d69c00c436bb488af56d9f3e05e?pvs=21)

- 참고
    
    [4. 객체 지향 원리 적용 - 관심사의 분리](https://gdlovehush.tistory.com/462)
    
    [[백엔드] 스프링 핵심 원리 기본편 정리](https://velog.io/@yssgood/백엔드-스프링-핵심-원리-기본편-정리)
    

# 관심사의 분리

---

<aside>
💡 **NOTE**

> ***애플리케이션을 하나의 공연이라고 생각해보자!***
> 

![왜 Service(클라이언트)가 직접 구현체를 정하고 있는가?](%5BSpring%20Study%5D%2001-4%20%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9(DI,%20IoC)%20%E2%AD%90/Untitled.png)

왜 Service(클라이언트)가 직접 구현체를 정하고 있는가?

- 각각의 인터페이스를 배역이라 생각하자 여기서 배역은 누가 정해주는가?
    - **배우**들이 직접 정하는가? → 아니다 **감독**이 정해야한다
- **배우는 배역만 수행하고, 공연 기획자가 나와서 배우를 지정하자!**
</aside>

## **AppConfig의 등장 (DI 컨테이너)**

<aside>
✍️ **NOTE**

> ***애플리케이션의 전체 동작 방식을 구성(config)하기 위해, 구현 객체를 생성하고 연결하는 책임을 가지는 별도의 설정 클래스를 만든다***
> 

![AppConfig가 어떤 객체가 구현되어야 하는지 결정해줌! ⇒ 의존관계 주입(DI)](%5BSpring%20Study%5D%2001-4%20%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9(DI,%20IoC)%20%E2%AD%90/Untitled%201.png)

AppConfig가 어떤 객체가 구현되어야 하는지 결정해줌! ⇒ 의존관계 주입(DI)

- **별도의 AppConfig를 사용함으로써 OCP와 DIP 원칙을 지킬수 있다.**

```java
public class AppConfig {
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }
    
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
    
    public DiscountPolicy discountPolicy() {
        return new RateDiscountPolicy();
    }
}
```

```java
public class OrderServiceImpl implements OrderService {
    private final MemberRepository memberRepository;
    private final DiscountPolicy discountPolicy;
    
    public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
        this.memberRepository = memberRepository;
        ths.discountPolicy = discountPolicy;
    }
}
```

```java
public class OrderApp {

    public static void main(String[] args) {
        AppConfig appConfig = new AppConfig();
        OrderService orderService = appConfig.orderService();

        Long memberId = 1L;
        Member member = new Member(memberId, "memberA", Grade.VIP
        Order order = orderService.createOrder(memberId, "itemA", 20000);

        System.out.println("order = " + order);
    }
}
```

- 비즈니스 로직상 **DiscountPolicy 인터페이스의 구현 객체로 다른 클래스가 추가되어도**, **구성 영역인 AppConfig에서 수정**하므로, 사용 영역의 어떠한 코드 변경없이 확장한다.
</aside>

# **의존 관계 주입(IoC, DI, 컨테이너)**

---

## IoC(Inversion of Control) - 제어의 역전

<aside>
✍️ **NOTE**

> ***프로그램의 제어 흐름을 직접 제어하는 것이 아니라 외부에서 관리하는 것!***
> 
- 기존 프로그램은 클라이언트 구현 객체가 스스로 필요한 서버 구현 객체를 생성하고, 연결하고 실행했다.
    - 한마디로 구현 객체가 프로그램의 제어 흐름을 스스로 조종했다.
- 반면에 AppConfig가 등장한 이후에는 구현 객체는 자신의 로직을 실행하는 역할만 당한한다.
    - **프로그램의 제어 흐름은 AppConfig가 한다**
</aside>

## **DI (Dependency Injection) - 의존 관계 주입**

<aside>
✍️ **NOTE**

> ***애플리케이션 실행 시점(런타임)에 외부에서 실제 구현 객체를 생성하고 클라이언트에 전달해서 연결되는 것을 의존 관계 주입(DI)라고 한다!***
> 

![어떤 서비스를 의존하고 있는지 알 수 있음 (정적 클래스 의존)](%5BSpring%20Study%5D%2001-4%20%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9(DI,%20IoC)%20%E2%AD%90/Untitled%202.png)

어떤 서비스를 의존하고 있는지 알 수 있음 (정적 클래스 의존)

![어떤 객체를 참조할지 실행시점에 알 수 있음 (동적 클래스 의존)](%5BSpring%20Study%5D%2001-4%20%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9(DI,%20IoC)%20%E2%AD%90/Untitled%203.png)

어떤 객체를 참조할지 실행시점에 알 수 있음 (동적 클래스 의존)

- **의존 관계 주입(DI) 장점**
    - 클라이언트 코드를 변경하지 않고, 호출하는 대상의 타입을 변경할 수 있다.
    - 클래스 의존 관계를 변경하지 않고, 동적인 객체 인스턴스 의존 관계를 쉽게 변경할 수 있다.
</aside>

## DI / IoC 컨테이너 스프링 전환

<aside>
✍️ **NOTE**

> ***DI / IoC 컨테이너 ⇒ AppConfig처럼 객체를 생성하고 관리하면서 의존 관계를 연결해주는 것!***
> 

```java
@Configuration
public class AppConfig {
    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
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

```java
public class OrderApp {

    public static void main(String[] args) {
//        AppConfig appConfig = new AppConfig();
//        OrderService orderService = appConfig.orderService();

        ApplicationContext applicationContext = new AnnotationConfigApplicationContext(AppConfig.class);
        
        OrderService orderService = applicationContext.getBean("orderService", OrderService.class);

        Long memberId = 1L;
        Order order = orderService.createOrder(memberId, "itemA", 20000);

        System.out.println("order = " + order);
    }
}
```

</aside>

## 프레임워크 vs 라이브러리

<aside>
✍️ **NOTE**

- **프레임워크**
    - **내가 작성한 코드를 제어하지 않고, 대신 실행해준다**
    - jUnit은 자신만의 라이프사이클이 존재하며, 내 코드를 그 안에 넣어 실행하는 것
- **라이브러리**
    - **내가 작성한 코드가 직접 제어의 흐름을 담당한다**
</aside>