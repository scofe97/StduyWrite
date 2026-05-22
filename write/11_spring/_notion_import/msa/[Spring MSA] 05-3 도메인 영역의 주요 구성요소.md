# [Spring MSA] 05-3. 도메인 영역의 주요 구성요소

주제: Spring MSA
연관 노트: [Spring Study] 01-4. 객체지향 원리 적용(DI, IoC) ⭐ (https://www.notion.so/Spring-Study-01-4-DI-IoC-4b53046a707f4c18a1acb6f82fb9428d?pvs=21)

- 참고
    
    

# 도메인 영역의 주요 구성요소

---

<aside>
💡 **NOTE**

> ***도메인 영역의 모델은 도메인의 주요 개념을 표현하며 핵심 로직을 구현한다. 도메인 영역을 구성하는 요소는 다음과같다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled.png)

</aside>

## 엔티티(Entity)

<aside>
✍️ **NOTE**

> ***Entity는 고유의 식별자를 가지는 자신의 고유 개념을 표현한다.***
> 

![orderNumber는 일종의 PK이다.](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%201.png)

orderNumber는 일종의 PK이다.

```java
public class Order {
    private String orderNumber;
		// ...

    @Override
    public boolean equals(Object obj){
        if(this == obj) return true;
        if(obj == null) return false;
        if(obj.getClass() != Order.class) return false;
        Order other = (Order) obj;
        
        if(this.orderNumber == null) return false;
        return this.orderNumber.equals(other.orderNumber);
    }
    
    @Override
    public int hashCode(){
        final int prime = 31;
        int result = 1;
        result = prime * result + ((orderNumber == null) ? 0 : orderNumber.hashCode());
        return result;
    }
}
```

### **⚠️ Domain의 Entity는 DB의 Entity와는 다른 개념이다.**

가장 큰 차이점은 도메인 모델은 **데이터와 함께 도메인 기능을 제공한다.**

```java
public class Order {
    
    // 주문 도메인 모델의 데이터
    private OrderNo number;
    private Orderer orderer;
    private ShippingInfo shippingInfo;

    // 도메인 모델 엔티티는 도메인 기능도 함께 제공
    public void changeShippingInfo(ShippingInfo shippingInfo) {
       // ...
    }
}
```

- 도메인 모델의 엔티티는 테이블 엔티티라기 보다는 데이터와 기능을 함께 제공하는 객체!

또 다른 차이점은 도메인 모델의 엔티티는 2개 이상의 데이터가 개념적으로 하나인 경우 배률 타입을 이용해서 표현할 수 있다.

![Untitled](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%202.png)

- 왼쪽 테이블의 경우 주문자(Orderer) 개념이 드러나지 않고, 오른쪽은 주문자 데이터를 별도 테이블에 저장했지만 이는 테이블 엔티티에 가까우며 밸류 타입의 의미가 드러나지 않는다.

```java
public class Orderer {
	
		// Orderer는 밸류타임으로 주문자 이름 + 이메일 포함
		// 이는 2개 이상의 데이터가 같이 쓰인다.
		private String name;
		private String email;
}
```

- 반면 도메인 모델의 Orderer는 주문자라는 개념을 잘 반영하므로 도메인을 보다 잘 이해할 수 있도록 돕는다.
</aside>

## 밸류(Value)

<aside>
✍️ **NOTE**

> ***Value는 고유의 식별자를 갖지 않는 객체로 주로 개념적으로 하나인 값을 표현할때 사용한다***
> 

```java
public class ShippingInfo {

		// 받는 사람
    private String receiverName;
		private String receiverPhoneNumber;

		// 주소
		private String shippingAddress1;
		private String shippingAddress2;
		private String shippingZipcode;
}
```

```java
public class Receiver {

    private String name;
    private String phone;

    public Receiver(String name, String phone) {
        this.name = name;
        this.phone = phone;
    }

		// ..
}
```

```java
public class Address {

    private String zipCode;
    private String address1;
    private String address2;

    public Address(String zipCode, String address1, String address2) {
        this.zipCode = zipCode;
        this.address1 = address1;
        this.address2 = address2;
    }

		// ..
}
```

![결론적으로 밸류타입은 코드 가독성을 향상시킨다.](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%203.png)

결론적으로 밸류타입은 코드 가독성을 향상시킨다.

밸류타입이 꼭 2개 이상의 데이터를 가져야 하는것은 아니다. (int와 같은 타입을 Money 객체로 표현) 또한 밸류타입 내부에 해당 밸류타입에서 사용할 메소드를 정의할 수 있다.

**밸류 객체의 데이터는 변경 기능을 제공하지 않는(불변)을 선호한다.**

- 안전한 코드를 작성할 수 있기 때문!
</aside>

## 애그리거트

<aside>
✍️ **NOTE**

> ***애그리거트는 상위 수준에서 모델을 보며 전체 모델의 관계와 개별모델을 이해하는데 도움을 준다.***
> 

![Untitled](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%204.png)

- 점 하나하나가 모두 도메인이며 도메인이 많아질수록 점점 복잡해진다.
- 지도에서 먼저 축소해서 큰틀을 본다음 확대하는 시나리오를 생각하면 된다. 이와 비슷하게 도메인 모델도 개별 객체뿐만 아니라 상위 수준에서 모델을 볼 수 있어야 한다.
- 애그리거트를 사용하면 개별 객체가 아닌 관련 객체를 묶어서 도메인 모델을 이해하고 관리할 수 있다.

![Untitled](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%205.png)

애그리거트는 군집에 속한 객체를 관리하는 **루트 엔티티를 가진다**.

- 루트 엔티티는 애그리거트에 속해 있는 **엔티티**와 **밸류 객체**를 사용해서 애그리거트가 구현해야할 기능을 제공한다.
- 애그리거트를 사용하는 코드는 애그리거트 루트가 제공하는 기능을 실행하고 애그리거트 루트를 통해서 간접적으로 애그리거트 내의 다른 엔티티와 밸류 객체에 접근한다.
- ex) 주문 애그리거트는 **Order를 통하지 않고 ShippongInfo를 변경할 수 있는 방법을 제공하지 않는다.**
- 즉 배송지를 변경하려면 루트 엔티티인 Order를 사용해야 하므로 배송지 정보를 변경할 때에는 **Order가 구현한 도메인 로직을 항상 따르게 된다.**
</aside>

## 레포지토리

<aside>
✍️ **NOTE**

> ***엔티티나 밸류가 요구사항에서 도출되는 도메인 모델이라면 레포지토리는 구현을 위한 도메인 모델이다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-3%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%98%81%EC%97%AD%EC%9D%98%20%EC%A3%BC%EC%9A%94%20%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C/Untitled%206.png)

```java
public interface OrderRepository extends Repository<Order, OrderNo> {
    Optional<Order> findById(OrderNo id);

		// Order 단위
    void save(Order order);

    default OrderNo nextOrderNo() {
        int randomNo = ThreadLocalRandom.current().nextInt(900000) + 100000;
        String number = String.format("%tY%<tm%<td%<tH-%d", new Date(), randomNo);
        return new OrderNo(number);
    }
}

@Service
public class CancelOrderService {
    private OrderRepository orderRepository;
    private CancelPolicy cancelPolicy;

    public CancelOrderService(OrderRepository orderRepository,
                              CancelPolicy cancelPolicy) {
        this.orderRepository = orderRepository;
        this.cancelPolicy = cancelPolicy;
    }

    @Transactional
    public void cancel(OrderNo orderNo, Canceller canceller) {
        Order order = orderRepository.findById(orderNo)
                .orElseThrow(() -> new NoOrderException());

        if (!cancelPolicy.hasCancellationPermission(order, canceller)) {
            throw new NoCancellablePermission();
        }
        order.cancel();
    }

}
```

레포지토리의 경우 대상을 찾고 저장하는 단위가 애거리트 루트 엔티티인 Order임을 알 수 있다.

</aside>