# [Spring MSA] 05-1. 도메인이란?

주제: Spring MSA

- 참고
    
    [[도메인 주도 개발 시작하기] 01. 도메인 모델 시작하기](https://be-developer.tistory.com/66)
    
    [유비쿼터스 언어(UBIQUITOUS LANGUAGE)](https://loopstudy.tistory.com/334)
    

# 도메인이란 무엇인가?

---

<aside>
💡 **NOTE**

> ***도메인은 해결하고자 하는 문제(요구사항)의 영역 또는 집합이다!***
> 

![도메인은 여러 하위 도메인으로 구성되고, 모두 구현하지 않아도 된다.](%5BSpring%20MSA%5D%2005-1%20%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%B4%EB%9E%80/Untitled.png)

도메인은 여러 하위 도메인으로 구성되고, 모두 구현하지 않아도 된다.

하나의 하위 도메인은 다른 하위 도메인과 연동하여 완전한 기능을 제공한다.

- ex) 쇼핑몰에서는 주문, 결제 도메인이 존재한다.

여러가지 도메인들이 상호작용하며, 비즈니스 도메인별로 나누어 설계하는 것이 도메인 주도 설계이다.

</aside>

## 도메인 모델

<aside>
✍️ **NOTE**

> ***도메인 모델이란 특정 도메인을 개념적으로 표현한 것이다!***
> 

![주문 도메인 모델(클래스) ⇒ 상품 구매수, 배송지, 결제 수단 등을 가진 객체모델](%5BSpring%20MSA%5D%2005-1%20%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%B4%EB%9E%80/Untitled%201.png)

주문 도메인 모델(클래스) ⇒ 상품 구매수, 배송지, 결제 수단 등을 가진 객체모델

![도메인 모델(상태) ⇒ 다이어 그램을 통한 표현](%5BSpring%20MSA%5D%2005-1%20%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%B4%EB%9E%80/Untitled%202.png)

도메인 모델(상태) ⇒ 다이어 그램을 통한 표현

**클래스 다이어그램**이나, **상태 다이어그램**과 같은 UML 표기법이외에도 다른 방법을 사용할 수 있다.

**도메인 모델 설계 시 주의점**

- 도메인에 따라 용어 의미가 결정되므로 여러 하위 도메인을 하나의 다이어그램에서 모델링하면 안된다.
- 모델의 각 구성요소는 특정 도메인으로 한정될 때 비로소 의미가 완전해지기 때문에 각 하위 도메인마다 별도로 모델을 만들어야 한다.

```java
public class Order {
    private OrderState state;
    private ShippingInfo shippingInfo;
    
    public void changeShippingInfo(ShippingInfo newShipInfo){
				// 변경가능 여부 확인
        if(isShippingChangeable()){
            throw new IllegalStateException("현재 상태로 변경이 불가능하다. " + state);
        }

				// 배송정보 변경
        this.shippingInfo = newShipInfo;
    }
    
    private boolean isShippingChangeable(){
				// 주문상태가 배송이전인 상태
        return state == OrderState.PAYMENT_WAITING || state == OrderState.PREPARING;
    }
}

public enum OrderState {
    PAYMENT_WAITING, PREPARING, SHIPPED, DELIVERING, DELIVERY_COMPLETED, CANCELED
}
```

- 주문 도메인 ⇒ **‘출고 전에 배송지를 변경할 수 있다’** , **‘주문 취소는 배송 전에만 할 수 있다’** 라는 규칙을 구현한 코드가 도메인 계층에 위치한다.
- 이런 도메인 규칙을 객체 지향 기법으로 구현하는 패턴이 **도메인 모델 패턴**이다.

### 개념 모델과 구현 모델

- 개념 모델은 순수하게 문제를 분석한 결과물이다.
- 데이터베이스, 트랜잭션 처리, 성능, 구현 기술을 고려하지 않기 때문에 있는 그대로는 사용할 수 없다. (그래서 **개념 모델** → **구현 모델** 변환 작업이 필요)
- 따라서 처음부터 완벽한 개념 모델보다는, 전반적인 개요를 알 수 있는 수준으로 개념 모델을 작성해야 한다.
</aside>

## 도메인 모델 도출

<aside>
✍️ **NOTE**

> ***도메인 모델링은 핵심 구성요소, 규칙, 기능을 찾는것이 기본이고 이것은 요구사항에서 출발한다!***
> 
- **주문 도메인과 관련 요구사항**
    - 최소 한 종류 이상의 상품을 주문해야 한다.
    - 한 상품을 1개 이상 주문 할 수 있다.
    - 주문할 때 배송지 정보를 반드시 저장해야 한다.
    - 배송지 정보는 받는 사람 이름, 전화번호, 주소로 구성된다.
    - 출고를 하면 배송지를 변경할 수 없다.
    - 출고 전에 주문을 취소할 수 있다.
    - 고객이 결제를 완료하기 전에는 상품을 준비하지 않는다.
    

위의 요구사항을 가지고 **주문 도메인 모델**을 더 구체화 시켜보자.

![앞서 설명했던 Order의 모델정보](%5BSpring%20MSA%5D%2005-1%20%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%B4%EB%9E%80/Untitled%201.png)

앞서 설명했던 Order의 모델정보

```java
public class Order {
	public void changeShipped() { ... } // 배송지 변경
	public void changeShippingInfo(ShippingInfo newShipping) { ... } // 배송상태 변경
	public void cancel() { ... } // 주문취소
	public void completePayment() { ... } // 결제완료
}
```

```java
public class OrderLine {
	private Product product; // 상품
	private int price; // 1개 가격
	private int quantity; // 구매개수
	private int amount; // 총 가격
}
```

```java
public class Order {
	// 주문은 여러개의 주문상품 정보를 가진다. (1대N)
	private List<OrderLine> orderLines;
	private int totalAmounts;

	private void setOrderLines(List<OrderLine> orderLines) { ... } // 주문상품 리스트 설정
	private void verifyAtLeastOneOrMoeOrderLines(List<OrderLine> orderLines) { ... } // 최소 1개이상의 주문상품이 있는지 검증
	private void calculateTotalAmounts() { ... } // 주문상품의 총가격
}
```

</aside>

## 도메인 모델에 set메서드 넣지 않기

<aside>
✍️ **NOTE**

> ***set 메서드는 도메인의 핵심 개념이나 의도를 코드에서 사라지게 하고, 도메인 객체를 생성할 때 온전치 않은 상태로 생성할 수 있으므로 자제하는것이 좋다.***
> 
- 생성자로 필요한 것을 모두 받은다음, 생성자 호출 시점에서 데이터 검증을 하는것이 안전하다.
- set 메서드를 사용한다면 private를 사용해서 내부에서만 사용하자.

### DTO의 get/set 메서드

- 표현 - 도메인 계층끼리 데이터를 주고받을때 사용하는 데이터 구조이다.
- 과거에는 DTO에 set메서드가 필요했지만, 최근에는 다른 방법을 지원하므로 불변객체로 만들자.
</aside>

## 도메인 용어와 유비쿼터스 언어

<aside>
✍️ **NOTE**

> ***유비쿼터스 언어 ⇒ 프로젝트 관계자가 모두 이해하는 공통된 용어를 사용하자!***
> 

![개발 컨벤션으로 작성한다.](%5BSpring%20MSA%5D%2005-1%20%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%B4%EB%9E%80/Untitled%203.png)

개발 컨벤션으로 작성한다.

```java
public OrderState {
	STEP1, STEP2, STEP3, STEP4, STEP5, STEP6
}
```

```java
public OrderState {
	PAYMENT_WAITING, PREPARING, SHIPPED, DELIVERING, DELIVERY_COMPLETED;
}
```

</aside>