# [Spring Study] 03-3. 의존관계 주입, 조건 및 복수 빈 처리

주제: Spring Study

- 참고
    
    [14. 다양한 의존관계 주입 방법](https://gdlovehush.tistory.com/475?category=993329)
    

# **스프링의 다양한 의존관계 주입 방법**

---

<aside>
💡 **NOTE**

> *스프링 프레임워크는 객체 간의 의존관계를 동적으로 주입(DI)하는 기능을 통해 객체간의 결합도를 낮추고 유연한 코드 관리가 가능해집니다. 스프링에서 의존 관계를 주입하는 방법은 4가지가 있습니다.*
> 

![DI ⇒ 외부에서 객체를 주입](%5BSpring%20Study%5D%2003-3%20%EC%9D%98%EC%A1%B4%EA%B4%80%EA%B3%84%20%EC%A3%BC%EC%9E%85,%20%EC%A1%B0%EA%B1%B4%20%EB%B0%8F%20%EB%B3%B5%EC%88%98%20%EB%B9%88%20%EC%B2%98%EB%A6%AC/Untitled.png)

DI ⇒ 외부에서 객체를 주입

- 생성자 주입
- setter 주입
- 필드 주입
- 일반 메서드 주입
</aside>

## 생성자 주입 ✅

<aside>
✍️ **NOTE**

> *생성자 주입은 클래스의 생성자를 통해 의존성을 주입받습니다.*
> 

```java
@Autowired
public OrderServiceImpl(MemberRepository memberRepository, 
													DiscountPolicy discountPolicy) {
    this.memberRepository = memberRepository;
    this.discountPolicy = discountPolicy;
}
```

- 생성자는 호출 시점에 딱 한 번만 호출되는 것이 보장됩니다.
- 생성사 주입은 객체의 불변성을 보장하고, 의존성 누락을 컴파일 시점에 잡을 수 있어 가장 선호되는 방식입니다.

생성자 주입은 롬복의 `@RequiredArgsConstructor` 어노테이션을 사용해 더 간결하게 생성할 수 있습니다.

```java
@Component
@RequiredArgsConstructor
public class OrderServiceImpl implements OrderService {

    private final MemberRepository memberRepository;
    private final DiscountPolicy discountPolicy;

		// final이 붙은 필드의 생성자가 자동으로 생성됨..
}
```

</aside>

## 수정자(setter) 주입 ❌

<aside>
✍️ **NOTE**

> *수정자 주입은 객체의 필드 값을 변경하는 setter를 통해 주입받습니다. 선택적이거나 변경 가능성이 있는 경우에 사용됩니다.*
> 

```java
@Autowired
public void setMemberRepository(MemberRepository memberRepository){
    this.memberRepository = memberRepository;
}

@Autowired
public void setDiscountPolicy(DiscountPolicy discountPolicy){
    this.discountPolicy = discountPolicy;
}
```

- 선택, 변경 가능성이 있는 의존관계에 사용한다 (거의 없음)
</aside>

## 필드 주입 ❌

<aside>
✍️ **NOTE**

> *필드 주입은 클래스 내부의 필드에 `@Autowired` 어노테이션을 붙여 의존관계를 주입하는 방식입니다.*
> 

```java
@Autowired private MemberRepository memberRepository;
@Autowired private DiscountPolicy discountPolicy;
```

- 코드가 간결하지만 **외부에서 변경이 불가능해서 테스트 하기 힘들다는 치명적인 단점**이 있다.
- `@Autowired`는 스프링의 어노테이션이므로 순수 자바코드로 테스트할 수 없습니다.
</aside>

# **조건에 따른 빈 등록 처리**

---

<aside>
💡 **NOTE**

> *스프링은 자동 주입 대상이 되는 스프링 빈이 없을 경우, 옵션으로 처리하는 방법을 제공해줍니다.*
> 

```java
@Autowired(required = false)
public void setNoBean1(Member noBean1){
    System.out.println("noBean1 = " + noBean1);
}
```

- `@Autowired(required=false)`를 사용하면, 자동 주입 대상이 없는 경우 수정자 메서드 자체가 호출되지 않습니다.

```java
@Autowired
public void setNoBean2(@Nullable Member noBean2){
    System.out.println("noBean2 = " + noBean2);
}
```

- `@Nullable`을 사용하면 자동 주입대상이 없는 경우 자동으로 null이 입력됩니다.

```java
@Autowired
public void setNoBean2(@Nullable Member noBean2){
    System.out.println("noBean2 = " + noBean2);
}
```

- `Optional`을 사용하면 자동 주입대상이 없는 경우 `Optional.empty`가 입력됩니다.
</aside>

# **스프링 빈이 2개 이상일 때 해결 방법**

---

<aside>
💡 **NOTE**

> *스프링 컨테이너에서 동일한 타입의 빈이 2개 이상있는 경우 `NoUniqueBeanDefinitionException` 예외가 발생하게 됩니다. 이를 위해 스프링은 몇가지 해결책을 제공합니다.*
> 

```java
@Component
public class FixDiscountPolicy implements DiscountPolicy {}

@Component
public class RateDiscountPolicy implements DiscountPolicy {}
```

</aside>

## **@Autowired 필드명 매칭**

<aside>
✍️ **NOTE**

```java
// 파라미터 값 변경이전
@Autowired
public OrderServiceImpl(
	MemberRepository memberRepository, 
	DiscountPolicy discountPolicy) {
    this.memberRepository = memberRepository;
    this.discountPolicy = discountPolicy;
}
```

```java
// 파라미터 값 변경이후
@Autowired
public OrderServiceImpl(
	MemberRepository memberRepository,  
	DiscountPolicy rateDiscountPolicy ) { // 필드명 매칭
    this.memberRepository = memberRepository;
    this.discountPolicy = rateDiscountPolicy;
}
```

- 필드 명 매칭의 경우 타입 매칭을 먼저 시도하고 그 결과에 여러 빈이 있을 때 추가로 동작한다.
</aside>

## **@**Qualifier ✅

<aside>
✍️ **NOTE**

> **`*@**Qualifier`는 추가 구분자를 붙여주는 방식입니다.*
> 

```java
@Component
@Qualifier("mainDiscountPolicy")
public class RateDiscountPolicy implements DiscountPolicy {}

@Component
@Qualifier("fixDiscountPolicy")
public class FixDiscountPolicy implements DiscountPolicy {}
```

```java
@Autowired
public OrderServiceImpl(MemberRepository memberRepository,
                        @Qualifier("mainDiscountPolicy") DiscountPolicy discountPolicy) {
    this.memberRepository = memberRepository;
    this.discountPolicy = discountPolicy;
}
```

```java
@Autowired
public DiscountPolicy setDiscountPolicy(@Qualifier("mainDiscountPolicy")
                                        DiscountPolicy discountPolicy) {
    this.discountPolicy = discountPolicy;
}
```

</aside>

## **@Primary**

<aside>
✍️ **NOTE**

> `*@*Primary` *는 우선순위를 정하는 방법입니다.*
> 

```java
@Component
@Primary // 우선순위를 가진다.
public class RateDiscountPolicy implements DiscountPolicy {}

@Component
public class FixDiscountPolicy implements DiscountPolicy {}
```

```java
@Autowired
public OrderServiceImpl(
	MemberRepository memberRepository,  
	DiscountPolicy discountPolicy) {
    this.memberRepository = memberRepository;
    this.discountPolicy = discountPolicy;
}
```

</aside>

## **조회한 빈이 모두 필요한 경우 List, Map에 담기**

<aside>
✍️ **NOTE**

> *스프링은 타입에 따른 의존성 주입뿐만 아니라, 특정 타입의 모든 빈을 수집하여 LIst나 Map으로 반환이 가능합니다.*
> 

```java
private final Map<String , DiscountPolicy> policyMap;
private final List<DiscountPolicy> policies;

public DiscountService(Map<String, DiscountPolicy> policyMap, List<DiscountPolicy> policies) {
    this.policyMap = policyMap;
    this.policies = policies;
    System.out.println("policyMap = " + policyMap);
    System.out.println("policies = " + policies);
}

public int discount(Member member, int price, String discountCode) {
    DiscountPolicy discountPolicy = policyMap.get(discountCode);
    return discountPolicy.discount(member, price);
}
```

</aside>