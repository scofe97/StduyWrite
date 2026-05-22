# [Spring MSA] 05-7. 애그리거트 트랜잭션 관리

주제: Spring MSA

- 참고
    
    

# 애그리거트 트랜잭션 관리

---

<aside>
💡 **NOTE**

> *하나의 애그리거트를 **두 사용자가 동시에 변경할 때 트랜잭션이 필요합니다.***
> 

![하나의 애그리거트를 동시에 수정한다!](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled.png)

하나의 애그리거트를 동시에 수정한다!

한 주문 애그리거트에 대해 **운영자는 배송상태로 변경**할 떄 **사용자는 배송지 주소를 변경**하면 어떻게 될까?

- 운영자와 고객이 동시에 하나의 주문 애그리거트를 생성하므로 운영자 스레드와 고객 스레드는 같은 주문 애그리거트를 나타내는 다른 객체를 사용하게 됩니다.

운영자와 고객 스레드는 동일한 애그리거트를 사용하지만 물리적으로는 서로 다른 애그리거트 객체를 사용합니다. 따라서 운영자 스레드가 주문 애그리거트 객체를 배송 상태로 변경하더라도, 고객 스레드가 사용하는 주문 애그리거트 객체에는 영향을 주지 않습니다.

- 서로 다른 애그리거트 객체를 사용한다는 것은 주문 애그리거트가 다르다는 것보다는 가져온 **주문 애그리거트가 독립적**이라는 의미입니다.
- 문제는 이 트랜잭션들을 반영하면, 고객은 배송상태를 변경하고 운영자는 배송지를 변경하면서 일관성이 깨집니다. (하나만 반영되기 때문입니다)
</aside>

## 선점 잠금

<aside>
✍️ **NOTE**

> ***선점 잠금**은 먼저 애그리거트를 구한 스레드가 **애그리거트 사용이 끝날 때까지 다른 스레드가 수정하지 못하게 하는 방법**이다.*
> 

![말그대로 먼저 읽은 트랜잭션에서 Lock을 걸어버리는 경우](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%201.png)

말그대로 먼저 읽은 트랜잭션에서 Lock을 걸어버리는 경우

선점 잠금을 구현하는 방법은 다음과 같다.

- DBMS의 for update와 같은 쿼리를 사용
- 스프링 데이터 JPA는 @Lock 애노테이션을 사용

### 선점 잠금과 교착상태

![A와 B가 서로 Lock을 들고 있고 상대방의 Lock을 요구한다.](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%202.png)

A와 B가 서로 Lock을 들고 있고 상대방의 Lock을 요구한다.

이런 문제는 사용자가 많을수록 발생할 가능성이 높고, 잠금을 구할 떄 최대 대기 시간을 지정해야 한다.

스프링 데이터 JPA에서는 QueryHint기능을 사용해서 해결할 수 있다.

</aside>

## 비선점 잠금

<aside>
✍️ **NOTE**

> ***비선점 잠금**은 동시에 접근하는 것을 막는 대신 **변경한 데이터를 실제 DBMS에 반영하는 시점에 가능 여부**를 확인한다!*
> 

![2개의 트랜잭션은 동시에 접근하지 않지만, 수정할때 문제가 생긴다.](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%203.png)

2개의 트랜잭션은 동시에 접근하지 않지만, 수정할때 문제가 생긴다.

선점잠금은 강력해보이지만 모든 트랜잭션 충돌 문제를 해결해주지는 않는다.

- 운영자가 배송지 정보를 조회하고 배송 상태로 변경하는 사이에 고객이 배송지를 변경하는점이 문제의 핵심이다. (이미 조회한 데이터가 고객에 의해 수정된다는 것)

이러한 문제는 선점 잠금 방식으로 해결할 수 없으며 비선점 잠금으로 해결할 수 있다. 비선점 잠금을 구현하기 위해서는 애그리거트에 버전으로 사용할 숫자 타입 프로퍼티를 추가해야 한다.

![Untitled](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%204.png)

```sql
UPDATE aggtable SET version = version + 1, colX = ?, colY = ?
WHERE aggId = ? AND version = 현재버전
```

```java
@Entity
@Table(name = "purchase_order")
@Access(AccessType.FIELD)
public class Order {
    @EmbeddedId
    private OrderNo number;

    @Version
    private long version;

    // ...
}
```

- 애그리거트를 수정할때마다 버전으로 사용할 프로퍼티 값이 1씩 증가한다.

![최종적인 흐름도](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%205.png)

최종적인 흐름도

```java
@Controller
public class OrderAdminController {
    private StartShippingService startShippingService;

    @PostMapping("/startShipping")
    public String startShipping(StartShippingRequest startReq) {
        try {
            startShippingService.startShipping(startReq);
            return "shippingStarted";
        } catch(OptimisticLockingFailureException | VersionConflictException ex) {
            // 트랜잭션 충돌
            return "startShippingTxConflict";
        }
    }

    ...
}
```

```java
public void startShipping(StartShippingRequest req) {
    Order order = orderRepository.findById(new OrderNo(req.getOrderNumber()));
    checkOrder(order);

    if (!order.matchVersion(req.getVersion())) {
        throw new VersionConflictException();
    }
    order.startShipping();
}
```

응용 서비스에 전달할 요청 데이터는 사용자가 전송한 버전 값을 포함한다. 이제 서비스에서 트랜잭션의 예와가 발생한다면, **OptimisticLockingFaulureException예외**가 발생한다. 

Controller에서 이 예외가 발생했는지에 따라 트랜잭션 충돌이 일어났는지 확인할 수 있다.

- **OptimisticLockingFailureException**  ⇒ 누군가 동시에 수정했다.
    - JPA에서 발생시키는 예외로 실제 SQL쿼리 동작시 발생한다.
- **VersionConflictException** ⇒ 누군가 애그리거트를 수정했다.
    - 애플리케이션 코드에서 발생하는 예외로,

### 강제 버전 증가

애그리거트에 애그리거트 루트 외에 다른 엔티티가 존재하는데 긴으 실행 도중 루트가 아닌 다른 엔티티의 값만 변경된다고 하자. (이 경우 JPA는 루트 엔티티의 버전 값을 증가시키지 않는다.)

그런데 이런 JPA특징은 애그리거트 관점에서 보면 문제가 된다. 비록 루트 엔티티의 값이 바뀌지 않았더라도 논리적으로 애그리거트의 구성요소중 일부 값이 바뀌면 애그리거트는 바뀐것이기 떄문이다,

JPA는 이런 문제를 해결하기 위해서 @Lock을 제공하면서, 트랜잭션 종료시점에 버전값 증가 처리르한다.

</aside>

## 오프라인 비선점 잠금

<aside>
✍️ **NOTE**

> ***오프라인 선점 잠금 방식**은 여러 트랜잭션에 걸쳐서 동시 변경을 막는 방식이다.*
> 

![아틀라시안의 컨플루언스는 문서를 편집할 떄 누군가 먼저 편집을 하는 중이면 다른 사용자가 문서를 수정하고 있다는 문구를 보여준다.](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%206.png)

아틀라시안의 컨플루언스는 문서를 편집할 떄 누군가 먼저 편집을 하는 중이면 다른 사용자가 문서를 수정하고 있다는 문구를 보여준다.

이러한 방식은 단순한 선점/비선점 잠금 방식으로는 구현할 수 없으며, 이떄 필요한 것이 오프라인 선점 잠금 방식이다

단일 트랜잭션에서 동시 변경을 막는 선점 잠금 방식과 달리 오프라인 선점 잠금은 여러 트랜잭션에 걸쳐 동시 변경을 막는다. 

![Untitled](%5BSpring%20MSA%5D%2005-7%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B4%80%EB%A6%AC/Untitled%207.png)

- 1번째 트랜잭션을 시작할때 오프라인 잠금을 선점, 마지막 트랜잭션에서 해제한다.
- 이 잠금을 해제하기 전까지 다른 사용자는 잠금을 구할 수 없다. 그러므로 이 잠금은 무조건적으로 유효시간을 가져야한다.
- 단순히 유효시간을 만료해버리면, A가 만료시간이 1초가 지난후 3번과정을 수행한다고 가정해보자
    - 사용자 A는 잠금이 없으므로 수정에 실패하게 된다.
    - 이러한 상황을 만들지 않으려면 일정 주기로 유효시간을 증가시켜야한다.

이후 내용은 오프라인 선점 잠금을 구현하기 위한 코드들을 다루지만, 당장은 필요하지 않으므로 생략한다.

</aside>