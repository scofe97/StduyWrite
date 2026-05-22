# [Spring Study] 01-3. 예제를 통한 스프링 핵심 원리 이해

주제: Spring Study

- 참고
    
    [[백엔드] 스프링 핵심 원리 기본편 정리](https://velog.io/@yssgood/백엔드-스프링-핵심-원리-기본편-정리)
    
    [3. 예제 프로젝트 만들기](https://gdlovehush.tistory.com/459?category=993329)
    

# 프로젝트 생성

---

<aside>
💡 **NOTE**

> *지금은 스프링 없는 **순수한 자바로만 개발을 진행**한다는 점을 꼭 기억하자! 스프링 관련은 한참 뒤에 등장한다.*
> 

![Untitled](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled.png)

- **Intelij Gradle 대신에 자바 직접 실행**
    
    ![Untitled](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%201.png)
    
    - Build and run using: IntelliJ IDEA
    - Run tests using: IntelliJ IDEA
    - 다음과 같이 변경함녀 InteliJ가 자바를 바로 실행해서 실행속도가 더 빠르다.
</aside>

# **비즈니스 요구사항과 설계**

---

<aside>
💡 **NOTE**

> ***회원은 상품을 주문할 수 있고, 회원 등급에 따라 할인을 받을 수 있다!***
> 

![전체 클래스 다이어그램](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%202.png)

전체 클래스 다이어그램

</aside>

## 회원 도메인 개발

<aside>
✍️ **NOTE**

![회원 저장소의 구현체가 여러가지가 존재한다.](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%203.png)

회원 저장소의 구현체가 여러가지가 존재한다.

```java
public class MemberServiceImpl implements MemberService {

    **private final MemberRepository memberRepository = new MemoryMemberRepository();**

    @Override
    public void join(Member member) {
        memberRepository.save(member);
    }

    @Override
    public Member findMemeber(Long memberId) {
        return memberRepository.findById(memberId);
    }
}
```

</aside>

## 주문과 할인 도메인 설계

<aside>
✍️ **NOTE**

![고정 할인, 퍼센트 할인 정책중 하나를 선택](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%204.png)

고정 할인, 퍼센트 할인 정책중 하나를 선택

```java
public class OrderServiceImpl implements OrderService{

    private final MemberRepository memberRepository = new MemoryMemberRepository();
    private final DiscountPolicy discountPolicy = new FixDiscountPolicy();

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}
```

</aside>

## 현재 구조의 문제점 ⭐

<aside>
✍️ **NOTE**

> ***현재 방식은 SOLID의 OCP와 DIP 원칙에 어긋난다!***
> 

```java
public class OrderServiceImpl implements OrderService {
//  private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
    private final DiscountPolicy discountPolicy = new RateDiscountPolicy();
}
```

- **DIP 위반 이유**
    
    ![Service가 DiscountPolicy(인터페이스)와 RateDiscountPolicy(구현체) 둘다 의존중](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%205.png)
    
    Service가 DiscountPolicy(인터페이스)와 RateDiscountPolicy(구현체) 둘다 의존중
    

- **OCP 위반이유**
    
    ![FixDiscountPolicy → RateDiscountPolicy로 변경하려면 Service의 코드도 변경해야함!](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%206.png)
    
    FixDiscountPolicy → RateDiscountPolicy로 변경하려면 Service의 코드도 변경해야함!
    
</aside>

## 해법 ⭐

<aside>
✍️ **NOTE**

> ***해결방법은 아래와 같이, 오로지 클래스가 인터페이스에만 의존하도록 해준다.***
> 

![우리가 원했던 구조](%5BSpring%20Study%5D%2001-3%20%EC%98%88%EC%A0%9C%EB%A5%BC%20%ED%86%B5%ED%95%9C%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%95%B5%EC%8B%AC%20%EC%9B%90%EB%A6%AC%20%EC%9D%B4%ED%95%B4/Untitled%207.png)

우리가 원했던 구조

```java
public class OrderServiceImpl implements OrderService {
    private final DiscountPolicy discountPolicy;
}
```

- 이 상황에서는 누군가가 클라이언트인 `OrderServiceImpl`에 `DiscountPolicy`의 구현 객체를 대신 생성하고 주입해주어야 한다..

**⇒ AppConfig의 등장배경!**

</aside>