# [Spring MSA] xx. 이벤트, CQRS 설계

주제: Spring MSA

- 참고
    
    [김명재, Myeongjae Kim](https://myeongjae.kim/blog/2022/02/03/fundamental-cqrs)
    

# 이벤트

---

<aside>
✍️ **NOTE**

쇼핑몰에서 구매를 취소하면 환불을 처리해야 한다. 

- 이떄 환불 기능을 실행하는 주체는 주문 도메인 엔티티가 될 수 있다.
- 도메인 객체에서 환불 기능을 실행하려면 다음 코드처럼 환불 기능을 제공하는 도메인 서비스를 파라미터로 전달받고 취소 도메인 기능에서 도메인 서비스를 실행하게 된다.

```java
// 도메인 구현
public class Order {

	// 주문 서비스를 사용하여 주문 도메인 서비스를 파라미터로 전달받음
	public void cancel(RefundService refundService) {
	    verifyNotYetShipped();
	    this.state = OrderState.CANCELED;
	
	    this.refundStatus = State.REFUND_STARTED;
	    try {
	        refundService.refund(getPaymentId());
	        this.refundStatus = State.REFUND_COMPLETED;
	    } catch (Exception ex) {
	        // 예외 처리 로직
	    }
	}
}
...

// 서비스 구현
public class CancelOrderService {
    private RefundService refundService;

    @Transactional
    public void cancel(OrderNo orderNo) {
        Order order = findOrder(orderNo);
        order.cancel();

        order.refundStarted();
        try {
            refundService.refund(order.getPaymentId());
            order.refundCompleted();
        } catch (Exception ex) {
            // 예외 처리 로직
        }
    }

    ...
}
```

보통 결제 시스템은 외부에 존재하므로 RefundService는 외부에 결제 시스템이 제공하는 환불 서비스를 호출한다. 이때 3가지 문제가 발생할 수 있다.

1. 외부 서비스가 정살이 아닐 경우 트랜잭션 처리를 어떻게 해야하는가?
    - 환불에 실패했으므로, 주문 취소 트랜잭션을 롤백하는건 맞아 보인다.
    - 하지만 반드시 롤백해야 하는건 아니다. 주문은 취소 상태로 변경하고 환불만 나중에 시도하는 방식으로 처리할수도 있다.
2. 외부 시스템 응답 시간이 길어지면 성능에 문제가 생긴다.
    - 환불 처리 기능이 30초가 걸리면 주문 취소 기능은 30초만큼 대기시간이 증가한다.
    
    ```java
    @Transactional
    public void cancel(OrderNo orderNo) {
        Order order = findOrder(orderNo);
        order.cancel();
    
        order.refundStarted();
        try {
    				// 외부 서비스 성능에 직접적으로 영향을 받는다.
            refundService.refund(order.getPaymentId());
            order.refundCompleted();
        } catch(Exception ex) {
            // 예외 처리 로직
        }
    }
    ```
    
3. 도메인 객체에 서비스를 전달하면 추갖거인 설계상 문제가 나타날 수 있다.
    - ex) 주문 로직과 결제 로직이 섞이게 된다.
    
    ```java
    public class Order {
        public void cancel(RefundService refundService) {
    				// 주문 로직
            verifyNotYetShipped();
            this.state = OrderState.CANCELED;
    
    				// 결제 로직
            this.refundStatus = State.REFUND_STARTED;
            try {
                refundSvc.refund(getPaymentId());
                this.refundStatus = State.REFUND_COMPLETED;
            } catch(Exception ex) {
                // 예외 처리 로직
            }
        }
    }
    ```
    
    - Order는 주문을 표현하는 도메인 객체인데 결제 도메인의 환불 로직과 뒤섞이게 된다.
    - 이는 환불기능이 변경되면 Order도 영향을 받게된다는 의미이다.

이러한 문제들이 발생한 이유는 주문 바운디드 컨텍스트 - 결제 바운디드 컨텍스트 간의 결합이 강하기 때문이다.

- 주문이 결제와 강하게 결합되어서 서로 영향을 받게 되는 것이다.
- 이런 강한 결합을 없앨 수 있는 시스템이 이벤트이다.
</aside>

## 이벤트 개요

<aside>
✍️ **NOTE**

Event는 과거에 벌어진 어떤 것을 의미한다.

- 사용자가 암호를 변경함 → 암호변경 이벤트
- 주문을 취소함 → 주문취소 이벤트

도메인 모델에서도 도메인의 상태 변경을 이벤트로 표현할 수 있다.

- ~할 때, ~가 발생하면, 만약 ~하면과 같은 요구사항은 도메인의 상태 변경과 관련된 경우가 많고 이런 요구사항을 이벤트를 이용해서 구현할 수 있다.

### 이벤트 관련 구성요소

도메인 모델에 이벤트를 도입하려면 4개의 구성요소가 필요하다.

![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled.png)

1. 이벤트
2. 이벤트 생성 주체
    - 엔티티, 밸류, 도메인 서비스와 같은 도메인 객체
    - 도메인 객체는 도메인 로직을 실행하면 상태가 바뀌면서 관련 이벤트를 발생시킨다.
3. 이벤트 디스패쳐 (퍼블리셔)
    - 이벤트 생성 주체와 이벤트 핸들러를 연결해주는 것이 이벤트 디스패쳐다.
    - 이벤트 생성 주체는 이벤트를 생성해서 디스패쳐에 이벤트를 전달한다.
    - 디스패쳐는 해당 이벤트를 처리할 수 있는 핸들러에 이벤트를 전파한다.
4. 이벤트 핸들러 (구독자)
    - 이벤트 생성 주체가 발생한 이벤트에 반응한다.
    - 이벤트 핸들러는 생성 주체가 발생한 이벤트를 전달받아 이벤트에 담긴 데이터로 원하는 기능을 실행시킨다.

### 이벤트의 구성

이벤트는 발생한 이벤트에 대한 정보를 담는다. 이 정보는 다음을 포함한다.

- 이벤트 종류 : 클래스 이름
- 이벤트 발생 시간
- 추가 데이터 : 주문번호, 신규 배송지 정보 등..

배송지를 변경하는 이벤트를 생각해보자. 이 이벤트를 위한 클래스는 다음과 같다.

```java
public class ShippingInfoChangedEvent {
    private String orderNumber;
    private long timestamp;
    private ShippingInfo newShippingInfo;

    // 생성자, getter
}
```

- 클래스 이름을 보면 Changed라는 과거 시제를 사용했다. 이벤트는 현재 기준으로 과거에 벌어진것을 표현하기 때문에 과거 시제를 사용한다.

```java
public class Order {
    public void changeShippingInfo(ShippingInfo newShippingInfo) {
        verifyNotYetShipped();
        setShippingInfo(newShippingInfo);
        Events.raise(new ShippingInfoChangedEvent(number, newShippingInfo));
    }

    // ...
}
```

이 이벤트를 발생하는 주체는 Order 애그리거트다.

- Order 애그리거트의 배송지 변경 기능을 구현한 메서드는 다음 코드처럼 배송지 정보를 변경한 뒤에 이 이벤트를 발생시킬 것이다.
- 이 코드에서 Events.raise()는 디스패쳐를 통해 이벤트를 전파하는 기능을 제공한다.

ShippingInfoChangedEvent를 처리하는 핸들러는 디스패쳐로부터 이벤트를 전달받아 필요한 작업을 수행한다.

```java
public class ShippingInfoChangedHandler {

    @EventListener(ShippingInfoChangedEvent.class)
    public void handle(ShippingInfoChangedEvent evt) {
        shippingInfoSynchronizer.sync(
            evt.getOrderNumber(),
            evt.getNewShippingInfo()
        );
    }

    // ...
}
```

### 이벤트 용도

이벤트 용도는 크게 2가지로 나뉜다.

1. 트리거
    
    ![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled%201.png)
    
    - 도메인의 상태가 바뀔때 다른 후처리가 필요하면 후처리를 실행하기 위한 트리거로 이벤트를 사용할 수 있다.
        - 주문 에서는 주문 취소 이벤트를 트리거로 사용할 수 있다.
        - 예매 결과를 통지할 때도 완료 이벤트를 발생시키고 SMS를 발송하는 방식으로 구현할 수 있다.

1. 서로 다른 시스템 간의 동기
    - 배송지를 변경하면 외부 배송 서비스에 바뀐 배송지 정보를 전송해야 한다.
    - 주문 도메인은 배송지 변경 이벤트를 발생 시키고 이벤트 핸들러는 외부 배송 서비스와 배송지 정보를 동기화 할 수 있다.

### 이벤트의 장점

이벤트를 사용하면 도메인 로직이 섞이는 것을 방지할 수 있다.

![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled%202.png)

```java
public class Order {

		// 기본 로직
    public void cancel(RefundService refundService) {
        verifyNotYetShipped();
        this.state = OrderState.CANCELED;

				// 환불 도메인을 위한 로직을 작성해야함
        this.refundStatus = State.REFUND_STARTED;
        try {
            refundSvc.refund(getPaymentId());
            this.refundStatus = State.REFUND_COMPLETED;
        } catch(Exception ex) {
            // 예외 처리 로직
        }
    }

		// 이벤트 로직 (이벤트로 서로 다른 도메인 로직이 섞이지 않음)
		public void cancel() {
        verifyNotYetShipped();
        this.state = OrderState.CANCELED;
        Events.raise(new OrderCanceledEvent(number.getNumber()));
    }
}
```

구매 취소 로직에 이벤트를 적용함으로써 환불 로직이 없어졌다.

환불 실행 로직은 주문 취소 이벤트를 받는 이벤트 핸들러로 이동하고 이벤트를 사용하여 주문 도메인에서 결제 도메인으로의 의존을 제거했다.

</aside>

## 이벤트, 핸들러, 디스패쳐 구현

<aside>
✍️ **NOTE**

실제 이벤트와 관련된 코드를 스프링으로 구현해보자

- 이벤트 클래스 : 이벤트를 표현한다.
- 디스패쳐 : 스프링이 제공하는 ApplicationEventPublisher를 이용한다.
- Events : 이벤트를 발생한다. 이벤트 발행을위해 ApplicationEventPublisher를 사용
- 이벤트 핸들러 : 이벤트를 수신해서 처리한다.

### 이벤트 클래스

이벤트 자체를 위한 상위 타입은 존재하지 않는다. 원하는 클래스를 이벤트로 사용하면된다.

```java
public abstract class Event {
    private long timestamp;

    public Event() {
        this.timestamp = System.currentTimeMillis();
    }

    public long getTimestamp() {
        return timestamp;
    }

}
```

```java
public class OrderCanceledEvent extends Event {
    private String orderNumber;

    public OrderCanceledEvent(String number) {
        super();
        this.orderNumber = number;
    }

    public String getOrderNumber() {
        return orderNumber;
    }
}
```

- 단 이벤트를 식별하기 위해 클래스의 이름을 과거 시제로 사용하자.

### Events 클래스와 ApplicationEventPublisher

이벤트 발행과 출판을 위해 스프링이 제공하는 ApplicationEvnetPublisher를 사용한다.

- 스프링 컨테이너는 ApplicationEventPublisher도 된다.
- Events 클래스는 ApplicationEventPublisher를 사용해서 이벤트를 발생시키도록 구현한다.

```java
@Configuration
public class EventsConfiguration {
    @Autowired
    private ApplicationContext applicationContext;

    @Bean
    public InitializingBean eventsInitializer() {
        return () -> Events.setPublisher(applicationContext);
    }
}
```

```java
public class Events {
    private static ApplicationEventPublisher publisher;

    static void setPublisher(ApplicationEventPublisher publisher) {
        Events.publisher = publisher;
    }

    public static void raise(Object event) {
        if (publisher != null) {
            publisher.publishEvent(event);
        }
    }
}
```

- Events 클래스의 raise() 메서드는 ApplicationEventPublisher가 제공하는 publishEvent() 메서드를 이용해서 이벤트를 발생시킨다.
- eventsInitializer() 메서드는 initializingBean 타입 객체를 빈으로 설정한다.
    - 이 타입은 스프링 빈 객체를 초기화할 떄 사용하는 인터페이스로, 이 기능을 사용해서 Events 클래스를 초기화 했다.

### 흐름 정리

![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled%203.png)

</aside>

## 동기/비동기 이벤트 처리 문제

<aside>
✍️ **NOTE**

### 동기 이벤트 처리

이벤트를 사용해서 커플링 문제는 해소했지만 아직 외부 서비스에 영향을 받는 문제가 남아있다.

```java

```

- 해당 코드에서 외부 환불 서비스와 연동한다고 가정해보자, 만약 외부 활불 기능이 갑자기 느려지면 cancle() 메서드도 함께 느려진다.
- 이것은 외부 서비스의 성능 저하가 바로 내 시스템의 성능 저하로 연결된다는것을 의미한다.
- 또한 트랜잭션도 문제가 되는데, 환불로직에서 예외가 발생하면 cancel() 메서드의 트랜잭션을 롤백해야하는가? 만약 롤백하면 구매취소 기능이 실패하게 되는것과 같다.
    - 생각해볼만한 가정은 서비스에 실패했다고 반드시 롤백해야하는가?
    - 구매 자체 취소자체는 처리하고 환불만 재처리하거나 수동으로 처리해보자
    - 외부 시스템과의 연동을 동기로 처리할 떄 발생하는 성능과 트랜잭션 범위 문제를 해소하는 방법은 비동기로 처리하거나 이벤트와 트랜잭션을 연계하는것이다!

### 비동기 이벤트 처리

회원 가입 신청을 하면 검증을 위해 이메일을 보내는 서비스가 많다. 회원 가입 신청을 하자마자 바로 내 메일함에 검증 이메일이 도착할 필요는 없다. 이메일이 몇 초 뒤에 도착해도 문제되지 않는다. 10~20초 후에 도착해도 되고, 받지못하면 다시 받게 해주면된다.

- 비슷하게 주문을 취소하자마자 결제를 취소하지 않아도된다. 수십 초 내에 결제 취소가 이루어지면된다.
- 이렇게 우리가 구현해야하는 것중 A → B 가 꼭 연속적일 필요가 없다.
- B를 실패하면 일정간격으로 재시도하거나 수동처리해도 상관없는 경우가 있다.

A하면 일정 시간 안에 B하라는 A하면 이벤트로 볼수도 있다.

- ex) 회원가입 신청을하면 인증 이메일을 보내라

이벤트를 비동기로 구현하는 방법은 다양한데 이글에서는 4가지 방식으로 구현한다.

1. 로컬 핸들러 비동기 실행
2. 메시지 큐를 사용하기
3. 이벤트 저장소, 이벤트 포워더 사용하기
4. 이벤트 저장소와 이벤트 제공 API 사용하기

### 로컬 핸들러 비동기 실행

이벤트 핸들러를 비동기로 실행하는 방법은 핸들러를 별도 스레드로 실행하는것이다.

- Spring의 @Async 애노테이션을 사용하면 손쉽게 가동할 수 있다.
    
    ```java
    @SpringBootApplication
    @EnableAsync // 설정추가
    public class ShopApplication {
    
        public static void main(String[] args) {
            SpringApplication.run(ShopApplication.class, args);
        }
    }
    
    @Service
    public class OrderCanceledEventHandler {
    
        @Async // 비동기실행
        @EventListener(OrderCanceledEvent.class)
        public void handle(OrderCanceledEvent event) {
            refundService.refund(event.getOrderNumber());
        }
    }
    ```
    

### 메시징 시스템을 이용한 비동기 구현

카프카 혹은 래빗 MQ와 같은 메시징 시스템을 사용해서 구현할 수도 있다. 메시지 큐는 이벤트를 메시지 리스너에 전달하고, 메시지 리스너는 알맞은 이벤트 핸들러를 이용해서 이벤트를 처리한다.

![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled%204.png)

- 이때 이벤트를 메시지 큐에 저장하는 과정과 메시지 큐에서 이벤트를 읽어와 처리하는 과정은 별도 스레드나 프로세스로 처리한다.
- 필요하다면 이벤트를 발생시키는 도메인 기능과, 메시지 큐에 이벤트를 저장하는 절차를 하나의 트랜잭션으로 묶어야 한다.  이를 위해 글로벌 트랜잭션이 필요하다.
    - 글로벌 트랜잭션을 사용하면 안전하게 이벤트를 큐에 전달할 수 있지만 반대로 글로벌 트랜잭션으로 인해 전체 성능이 떨어진다.
- 메시지 큐를 사용하면 발생시키는 주체와 핸들러가 별도 프로세스에서 동작한다.
    - 이벤트 발생 JVM과 처리 JVM이 다르다는 것을 의미한다.
- 메시징 시스템은 글로벌 트랜잭션 지원과 함께 클러스터와 고가용성을 지원하므로 안정적으로 메시지를 전달할 수 있다.

### 이벤트 저장소를 이용한 비동기 처리

- 생략
</aside>

## 이벤트 적용시 고려사항

<aside>
✍️ **NOTE**

이벤트를 구현할 떄 고려할 점이 있다. (추후 다룬다.)

</aside>

# CQRS

---

<aside>
✍️ **NOTE**

[axon & spring boot를 이용해 CQRS & event sourcing 패턴 사용하기](https://velog.io/@dvmflstm/axon-spring-boot를-이용해-CQRS-event-sourcing-패턴-사용하기)

[https://www.youtube.com/watch?v=xf0kXMTFJm8&ab_channel=최범균](https://www.youtube.com/watch?v=xf0kXMTFJm8&ab_channel=최범균)

![Untitled](%5BSpring%20MSA%5D%20xx%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%20CQRS%20%EC%84%A4%EA%B3%84/Untitled%205.png)

명령과 쿼리를 나눈다. (Command Query)

- 명령 ⇒ 시스템 데이터를 변경
- 쿼리 ⇒ 시스템 데이터 조

책임 분리 (Responsibility Segregation)

- 책임 ⇒ 구성 요소(모델)의 역할
    - 클래스/함수
    - 모듈/패키지
    - 웹서버/DB
- 분리
    - 역할에 따라 구성 요소 나누는것

</aside>