# [Spring MSA] 05-6. 응용/도메인 서비스와 표현영역

주제: Spring MSA

- 참고
    
    

# 응용 서비스와 표현 영역

---

<aside>
💡 **NOTE**

> *앞서서는 도메인의 구성요소와 JPA를 이용한 레포지토리 구현 방법에 대해 주로 다루었다. 하지만 **도메인 영역만 잘 만든다고 끝나는 것이 아니다.***
> 

![Untitled](%5BSpring%20MSA%5D%2005-6%20%EC%9D%91%EC%9A%A9%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20%ED%91%9C%ED%98%84%EC%98%81%EC%97%AD/Untitled.png)

도메인이 제 기능을 하기위해서는 사용자와 도메인을 연결해주는 매개체가 필요하다.

- 표현영역 : 사용자의 요청을 해석한다. (컨트롤러)
- 응용영역 : 사용자가 원하는 기능을 제공한다. (서비스)
</aside>

## 응용 서비스의 역할

<aside>
✍️ **NOTE**

> ***응용 서비스**는 **사용자가 요청한 기능을 실행**하고, **기능을 처리하기 위해 도메인 객체**를 사용한다.*
> 

응용 서비스의 주요 역할은 도메인 객체를 사용해서 사용자의 요청을 처리하는 것이므로, 표현 영역 입장에서 보았을 때 응용 서비스는 도메인 영역과 표현 영역을 연결해주는 창구이다.

```java
public Result doSomeFunc(SomeReq req) {
    // 1. 리포지터리에서 어그리게이트를 구한다.
    SomeAgg agg = someAggRepository.findById(req.getId());
    checkNull(agg);

    // 2. 애그리거트의 도메인 기능을 실행한다.
    agg.doFunc(req.getValue());

    // 3. 결과를 리턴한다.
    return createSuccessResult(agg);
}
```

```java
public Result doSomeCreation(CreateSomeReq req) {
    // 1. 데이터 중복 등 데이터가 유효한지 검사한다.
    validate(req);

    // 2. 어그리게이트를 생성한다.
    SomeAgg newAgg = createSome(req);

    // 3. 리포지터리에 어그리게이트를 저장한다.
    someAggRepository.save(newAgg);

    // 4. 결과를 리턴한다.
    return createSuccessResult(newAgg);
}
```

- **응용 서비스**가 복잡하다면 응용 서비스에서 **도메인 로직의 일부를 구현하고 있을 가능성이 높다.**
    - 서비스가 도메인 로직을 일부 구현한다면 코드 중복, 로직 분산 등 코드품질에 좋지않다.
    - 응용 서비스는 트랜잭션, 접근 제어, 이벤트 처리등도 담당한다.

### 도메인 로직 넣지 않기

도메인 로직은 도메인 영역에 위치해야하고 응용 서비스는 도메인 로직을 구현하지 않는다.

이를 알아보기 위해서 암호변경을 예시로 들어보자

```java
public class ChangePasswordService {

    public void changePassword(String memberId, String oldPw, String newPw) {
        Member member = memberRepository.findById(memberId); // 회원검색
        checkMemberExists(member); // 회원이 존재하는가?
        member.changePassword(oldPw, newPw); // 암호변경
    }

    // ... (potentially more methods and fields)
}
```

- Mebere 애그리거트와 관련된 레포지토리를 이용해서 도메인 객체간의 실행흐름 제어한다.

```java
public class Member {

    public void changePassword(String oldPw, String newPw) {
        if (!matchPassword(oldPw)) throw new BadPasswordException(); // 패스워드 검사
        setPassword(newPw);
    }

    // 현재 암호화 일치하는지 검사 (해당 로직이 서비스에 있으면 안됨!)
    public boolean matchPassword(String pwd) {
        return passwordEncoder.matches(pwd);
    }

    private void setPassword(String newPw) {
        if (isEmpty(newPw)) throw new IllegalArgumentException("no new password");
        this.password = newPw;
    }

    // ... (potentially more methods and fields)
}
```

- Member 애그리거트는 암호를 변경하기전에 기존 암호를 올바르게 입력했는가 검사한다.
- 이와같이 기존 암호를 입력했는지 확인하는 로직은 **도메인 로직이므로 서비스에 구현하면 안된다.**
    - 코드의 응집성이 떨어지고, 여러 응용서비스에서 동일한 도메인 로직을 작성할 위험이 있다.
</aside>

## 응용 서비스의 구현

<aside>
✍️ **NOTE**

> ***응용 서비스는 Controller와 Domain의 매개체 역할을** 하는데 이는 디자인패턴의 **facade**(파사드)와 같은 역할을 한다.*
> 

응용 서비스 자체는 복잡한 로직이 없으므로 구현은 어렵지 않다. 이 절에서는 응용 서비스를 구현할 떄 몇가지 고려할 사항과 트랜잭션과 같은 구현 기술의 연동에 대해 살펴본다.

### 응용 서비스의 크기

회원(Member)에 대해서 생각해보자. 

```java
public class MemberService {
    // 각 기능을 구현하는 데 필요한 리포지터리, 도메인 서비스 필드 추가
    private MemberRepository memberRepository;
    private Notifier notifier;

    public void join(MemberJoinRequest joinRequest) {
        // ... implementation ...
    }

    public void changePassword(String memberId, String curPw, String newPw) {
        Member member = findExistingMember(memberId);
        member.changePassword(curPw, newPw);
    }

    public void initializePassword(String memberId) {
        Member member = findExistingMember(memberId);
        String newPassword = member.initializePassword();
        notifier.notifyNewPassword(member, newPassword);
    }

    public void leave(String memberId, String curPw) {
        Member member = findExistingMember(memberId);
        member.leave();
    }

    // 각 기능의 동일 로직에 대한 구현 코드 중복을 줄일 제네릭
    private Member findExistingMember(String memberId) {
        Member member = memberRepository.findById(memberId);
        if (member == null) {
            throw new NoMemberException(memberId);
        }
        return member;
    }

    // ... additional methods and fields ...
}
```

회원 가입, 탈퇴, 암호변경, 비밀번호 초기화와 같은 기능구현을 위해 도메인 모델을 사용한다. 이 경우 응용 서비스는 보통 2가지 방법으로 구현된다.

1. 1개의 응용 서비스 클래스에 모두 구현
2. 구분되는 기능별로 서비스 클래스 따로 구현

각 기능에 동일한 로직을 위한 코드 중복을 제거하기 쉽다는 것이 장점이라면 한 서비스 클래스의 크기(코드 라인)이 커지는 점과 관련 없는 코드가 뒤섞이는게 단점이다.

- **initializePassword()** 함수의 Notifier는 암호변경의 **changePassword()**와는 관계없다.

기존의 큰 서비스에서 비밀번호 변경에 대한 내용을 다루는 서비스를 분리했다.

```java
// 공통로직 (해당 멤버가 존재하는가?)
public final class MemberServiceHelper {

    public static Member findExistingMember(MemberRepository repo, String memberId) {
        Member member = repo.findById(memberId);
        if (member == null) {
            throw new NoMemberException(memberId);
        }
        return member;
    }
}

import static com.myshop.member.application.MemberServiceHelper.*;

// 서비스 분리
public class ChangePasswordService {
    private MemberRepository memberRepository;

    public void changePassword(String memberId, String curPw, String newPw) {
        Member member = findExistingMember(memberRepository, memberId);
        member.changePassword(curPw, newPw);
    }

    // ...
}
```

- 각 기능마다 동일한 로직을 구현해야하는 경우, 여러 클래스에 중복해서 동일한 코드를 구현할 가능성이 있다.
- 이 경우 별도로 클래스에 로직을 구현해서 코드가 중복되는걸 막자.

### 응용 서비스의 인터페이스와 클래스

```java
public interface ChangePasswordService {
    public void changePassword(String memberId, String curPw, String newPw);
}

public class ChangePasswordServiceImpl implements ChangePasswordService {
    //구현
}
```

인터페이스가 필요한 몇 가지 상황이 있는데 그 중 하나는 구현 클래스가 여러개인 경우이다.

- 구현 클래스가 다수 존재하면, 런타임에 구현 객체를 교체하는 작업이 유용하다.
- 하지만 응용 서비스는 런타임에 교체하는 경우가 거의 없고 한 응용 서비스의 구현 클래스가 2개인 경우도 드물다.

TDD를 즐겨하고, 표현영역부터 개발을 시작한다면, 미리 응용 서비스를 구현할 수 없으므로 응용 서비스의 인터페이스부터 개발할것이다. 표현 영역이 아닌 도메인 영역이나 응용영역의 개발을 먼저 시작하면 응용 서비스 클래스가 먼저 만들어진다. 이렇게되면 Interface가 꼭 필요한가 싶다.

### 메서드 파라미터와 값 리턴

응용 서비스가 제공하는 메서드는 도메인을 이용해서 사용자가 요구한 기능을 실행하는 데 필요한 값을 파라미터로 전달받아야 한다. 

```java
@Controller
@RequestMapping("/member/changePassword")
public class MemberPasswordController {

    // 컨트롤러를 이용해서 요청 서비스에 데이터를 전달하며
    // 프레임워크가 제공하는 기능을 활용하기에 좋음
    @PostMapping()
    public String submit(ChangePasswordRequest changePwdReq) {
        Authentication auth = SecurityContext.getAuthentication();
        changePwdReq.setMemberId(auth.getId());

        try {
            changePasswordService.changePassword(changePwdReq);
        } catch (NoMemberException ex) {
            // 알맞은 예외처리 처리 및 응답
        }

        // ...
    }

    // ...
}
```

- ex) 암호변경 → 회원 ID, 현재 암호, 변경될 암호를 제공받아야한다.
- 이에대해서 따로 파라미터로 받아도되고, 별도의 클래스로 제공받아도 된다.

```java
public class OrderService {

    @Transactional
    public OrderNo placeOrder(OrderRequest orderRequest) {
        OrderNo orderNo = orderRepository.nextId();
        Order order = createOrder(orderNo, orderRequest);
        orderRepository.save(order);

        // 유용 서비스 실행 후 특정 업무에서 필요한 결과 리턴
        return orderNo;
    }

    ...
}
```

- 응용 서비스의 결과를 표현 영역에서 사용해야 하면 응용 서비스 메서드의 결과로 필요한 데이터를 리턴한다.

### 표현 영역에 의존해서는 안된다.

응용 표현의 영역인 HttpServelt이나 HttpSession의 코드를 서비스로 넘겨서는 안된다.

- 응용 영역이 표현 영역에 대해 의존성이 발생해 테스트하기 힘들어진다.
</aside>

## 표현 영역

<aside>
✍️ **NOTE**

> ***표현영역은 응용 서비스가 요구하는 형식으로 변환하고 반환하는 역할을 담당한다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-6%20%EC%9D%91%EC%9A%A9%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20%ED%91%9C%ED%98%84%EC%98%81%EC%97%AD/Untitled%201.png)

- 사용자가 시스템을 사용할 수 있는 흐름을 제공하고 제어한다.
- 사용자의 요청을 알맞은 응용 서비스에 전달하고 결과를 제공한다.
- 사용자의 세션/권한을 관리/검사한다.
</aside>

## 조회 전용 기능과 응용 서비스

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-6%20%EC%9D%91%EC%9A%A9%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20%ED%91%9C%ED%98%84%EC%98%81%EC%97%AD/Untitled%202.png)

```java
public class OrderController {
    private OrderViewDao orderViewDao;

    @RequestMapping("/myorders")
    public String list(ModelMap model) {
        String ordererId = SecurityContext.getAuthentication().getId();
				
				// 그냥 바로 Repo참고 해도 된다는 의미
        List<OrderView> orders = orderViewDao.selectByOrderer(ordererId);
        model.addAttribute("orders", orders);
        return "order/list";
    }

    ...
}
```

</aside>

# 도메인 서비스

---

## 여러 애그리거트가 필요한 기능

<aside>
✍️ **NOTE**

> *도메인 영역의 코드를 작성하다 보면, 하**나의 애그리거트로 기능을 구현할 수 없을 떄가 있다.***
> 

결제 금액 계산 로직을 생각해보자 다음과 같은 상황에서 총 주문 금액을 책임져야하는 애그리거트는 무엇인가? (각 도메인이 모두 영향을 주는 경우)

- 상품 애그리거트 ⇒ 구매하는 상품의 가격, 배송비
- 주문 애그리거트 ⇒ 상품별 구매 개수
- 할인 쿠폰 애그리거트 ⇒ 쿠폰별로 지정한 할인 금액, 비율에 따라 할인, 조건에 따른 중복사용
- 회원 애그리거트 ⇒ 회원 등급에 따라 추가 할인

하나의 도메인의 책임이라고 보기는 어려운것같다. 그러면 하나의 도메인에 다른 도메인을 일단 모두 들고와서 로직을 처리하도록 해보자.

```java
public class Order {
    // ...
    private Orderer orderer;
    private List<OrderLine> orderLines;
    private List<Coupon> usedCoupons;

    private Money calculatePayAmounts() {
        Money totalAmounts = calculateTotalAmounts();
        // 쿠폰별 할인 금액을 구한다.
        Money discount = 
            coupons.stream()
                   .map(coupon -> calculateDiscount(coupon))
                   .reduce(Money(0), (v1, v2) -> v1.add(v2));
        
        // 회원에 따른 추가 할인을 구한다.
        Money membershipDiscount = 
            calculateDiscount(orderer.getMember().getGrade());
        
        // 실제 결제 금액 계산
        return totalAmounts.minus(discount).minus(membershipDiscount);
    }

    private Money calculateDiscount(Coupon coupon) {
        // orderLines의 각 상품에 대해 쿠폰을 적용해서 할인 금액 계산하는 로직,
        // 쿠폰의 적용 조건 등을 확인하는 코드
        // 정책에 따라 복잡한 if-else와 계산 코드
        // ...
    }

    private Money calculateDiscount(MemberGrade grade) {
        // ...등급에 따라 할인 금액 계산
    }
}
```

이렇게 코드를 작성하는 경우 특별 세일로 1달간 2% 추가 할인을 한다고 가정하자.

- **할인 정책은 주문 애그리거트와 관련 없음에도 결제 금액 계산의 책임떄문에 코드를 수정해야한다.**
- 이렇게 애매한 도메인 기능을 특정 애그리거트에 구현하면 점점 유지보수하기 힘들어진다.
- 이를 해소하는 방법은 도메인 기능을 별도 서비스로 구현하는 거다!
</aside>

## 도메인 서비스

<aside>
✍️ **NOTE**

> *도메인 서비스는 **도메인 영역에 위치한 도메인 로직을 표현할 떄 사용한다.***
> 
- 계산 로직 ⇒ 여러 애그리거트가 필요한 계산 로직, 한 애그리거트가 담당하기엔 복잡한 로직
- 외부 시스템 연동이 필요한 로직 ⇒ 구현하기 위해 타 시스템 사용

### 계산 로직과 도메인 서비스

할인 금액 규칙 계산처럼 한 애그리거트에 넣기 애매한 도메인 개념을 구현하려면 애그리거트에 억지로 넣기보다는 도메인 서비스를 이용해서 도메인 개념을 명시적으로 드러내면 된다.

도메인 영역에 애그리거트나 밸류와 같은 구성요소와 도메인 서비스를 비교할 떄 다른점은 도메인 서비스는 상태 없이 로직만 구현한다는 점이다.

```java
public class DiscountCalculationService {

		// 돈 계산
    public Money calculateDiscountAmounts(
        List<OrderLine> orderLines,
        List<Coupon> coupons,
        MemberGrade grade) {
        
        Money couponDiscount = 
            coupons.stream()
                   .map(coupon -> calculateDiscount(coupon))
                   .reduce(Money(0), (v1, v2) -> v1.add(v2));
        
        Money membershipDiscount = 
            calculateDiscount(orderer.getMember().getGrade());
        
        return couponDiscount.add(membershipDiscount);
    }

    private Money calculateDiscount(Coupon coupon) {
        // ...
    }

    private Money calculateDiscount(MemberGrade grade) {
        // ...
    }
}
```

할인 계산 서비스를 사용하는 주체는 애그리거트 또는 응용 서비스가 될 수도 있다.

```java
public class Order {

    public void calculateAmounts(
        DiscountCalculationService disCalSvc, 
        MemberGrade grade) {

        Money totalAmounts = getTotalAmounts();
        Money discountAmounts = 
            disCalSvc.calculateDiscountAmounts(this.orderLines, this.coupons, grade);
        this.paymentAmounts = totalAmounts.minus(discountAmounts);
    }

    // ...
}
```

```java
public class OrderService {
    private DiscountCalculationService discountCalculationService;

    @Transactional
    public OrderNo placeOrder(OrderRequest orderRequest) {
        OrderNo orderNo = orderRepository.nextId();
        Order order = createOrder(orderNo, orderRequest);
        orderRepository.save(order);
        // 유용 서비스 실행 후 필요한 업무에서 필요한 결과 리턴
        return orderNo;
    }

    private Order createOrder(OrderNo orderNo, OrderRequest orderReq) {
        Member member = findMember(orderReq.getOrdererId());
        Order order = new Order(orderNo, orderReq.getOrderLines(),
                                orderReq.getCoupons(), createOrderer(member),
                                orderReq.getShippingInfo());

        order.calculateAmounts(this.discountCalculationService,
                               member.getGrade());
        return order;
    }

    // ...
}
```

### 도메인 서비스 객체를 애그리거트에 주입하지 않기

```java
public class Order {
    @Autowired
    private DiscountCalculationService discountCalculationService;

    // ...
}
```

도메인 객체는 필드로 구성된 데이터와 메서드를 이용해서 개념적으로 하나인 모델을 표현한다.

모델의 데이터를 담는 필드는 모델에서 중요한 구성요소다. 그런데 discountCalculationService 필드는 데이터 자체와 관련이 없다.

또 ORder가 제공하는 모든 기능에서 discountCalculationService를 필요로하는 것도 아니다.

일부 기능을 위해서 굳이 도메인 서비스를 에그리거트에 채우는건 욕심에 불과하다.

### 외부 시스템 연동과 도메인 서비스

```java
// 권한을 가졌는가?
public interface SurveyPermissionChecker {
    boolean hasUserCreationPermission(String userId);
}

// 서비스주입하고 사용
public class CreateSurveyService {
    private SurveyPermissionChecker permissionChecker;

    public Long createSurvey(CreateSurveyRequest req) {
        validate(req);
        // 도메인 서비스를 이용해서 의사 시스템 권한을 확인
        if (!permissionChecker.hasUserCreationPermission(req.getRequestorId())) {
            throw new NoPermissionException();
        }
        // ...
    }
}
```

외부시스템이나 타 도메인과의 연동 기능도 도메인 서비스가 될 수 있다.

- 설문조사 시스템, 사용자 역할 관리 시스템이 분리되어있다고 하자
- 설문 조사 시스템은 설문 조사를 생성할 때 사용자가 생성 권한을 가진 역할인지 확인하기 위해 역할 관리 시스템과 연동해야한다.

### 도메인 서비스의 패키지 위치

![Untitled](%5BSpring%20MSA%5D%2005-6%20%EC%9D%91%EC%9A%A9%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20%ED%91%9C%ED%98%84%EC%98%81%EC%97%AD/Untitled%203.png)

도메인 서비스는 도메인 로직을 표현하므로 다른 도메인 구성요소와 동일하게 위치한다.

- domain 하위에 너무 많아지면 model, service, repository와 같이 분리하자.

### 도메인 서비스의 인터페이스와 클래스

![Untitled](%5BSpring%20MSA%5D%2005-6%20%EC%9D%91%EC%9A%A9%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20%ED%91%9C%ED%98%84%EC%98%81%EC%97%AD/Untitled%204.png)

도메인 서비스의 로직이 고정되어 있지 않은 경우, 인터페이스로 구현하고 이를 구현할 클래스를 둘 수 있다. 이때는 인프라스트럭쳐 영역에 두자

</aside>