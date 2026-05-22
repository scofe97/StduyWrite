# [Spring MSA] 05-8. 도메인 모델과 바운디드 컨텍스트 경계

주제: Spring MSA

- 참고
    
    

# 도메인 모델과 바운디드 컨텍스트 경계

---

<aside>
✍️ **NOTE**

처음 도메인 모델을 만들 때 빠지기 쉬운 함정이 도메인을 완벽하게 표현하는 단일 모델을 만드는 시도를 하는것이다. 하지만 1장에서 언급한것처럼 도메인은 다시 여러 하위 도메인으로 구분되기 때문에 1개의 모델로 여러 하위 도메인을 모두 표현하려면 모든 하위 도메인에 맞지 않는 모델을 만들게된다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled.png)

상품이라는 모델을 생각해보자

- 카탈로그에서 상품, 재고관리에서 상품, 주문에서 상품, 배송에서 상품은 이름만 같지 실제로 의미하는것이 다르다.
    - 카탈로그에서의 상품은 상품 이미지, 상품명, 상품 가격, 옵션 목록 정보위주
    - 재고 관리에서의 상품은 실존하는 개별 객체를 추적하기 위한 목적으로 사용한다.

논리적으로 같은 존재처럼 보여도 하위 도메인에 따라 다른 용어를 사용하는 경우도 있다.

- 시스템을 사용하는 사람을 회원 도메인에서는 회원이라고 부르지만, 주문 도메인에서는 주문자라고 부르고, 배송도메인에서는 보내는사람이라고 부른다.
- 모델은 특정한 컨텍스트(문맥) 하에서 완전한 의미를 가진다. 같은 제품이라도 각 컨텍스트에서의 의미가 서로 다르다
- 이렇게 구분되는 경계를 갖는 컨텍스트를 DDD에서는 바운디드 컨텍스트라고 부른다.
</aside>

## 바운디드 컨텍스트

<aside>
✍️ **NOTE**

바운디드 컨텍스트는 모델의 경계를 결쳐 결정하며 1개의 바운디드 컨텍스트는 논리적으로 1개의 모델을 가진다.  **( 1(바운디드 컨텍스트) - 1(모델) )**

- 바운디드 컨텍스트는 용어를 기준으로 구분한다.
- 카탈로그 컨텍스트와 재고 컨텍스트는 서로 다른 용어를 사용하므로 이 용어를 기준으로 컨텍스트를 분리할 수 있다.

하위 도메인과 바운디드 컨텍스트가 일대일 관계를 가지면 좋겠지만 현실은 그렇지 않을때가 많다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%201.png)

- ex) 주문 하위 도메인이라도 주문을 처리하는 팀과 복잡한 결제 금액 계산 로직을 구현하는 팀이 따로 있다고 해보자.
    - 주문 하위 도메인에 주문 바운디드 컨텍스트와 결제 금액 계산 바운디드 컨텍스트가 존재가하게된다.
- 규모자 작은 기업은 전체 시스템을 1개팀에서 구현한다.
    - ex) 소규모 쇼핑몰은 1개의 웹애플리케이션으로 온라인 쇼핑을 서비스하며 하나의 시스템에서 회원, 카탈로그, 재고, 구매, 결제 금액과 관련된 모든 기능을 제공한다.

여러 하위 도메인을 하나의 바운디드 컨텍스트에서 개발할때 주의할 점은 하위 도메인 모델이 섞이지 않도록 하는것이다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%202.png)

- 1개 프로젝트에서 각 하위 도메인의 모델이 위치하면 아무래도 전체 하위 도메인을 위한 단일 모델을 만들고 싶은 유횩에 빠지기 쉽다.
- 비록 1개의 바운디드 컨텍스트가 여러 하위 도메인을 포함하더라도 하위 도메인마다 구분되는 패키지를 갖도록 구현해야 하며, 이렇게 함으로써 하위 도메인을 위한 모델이 서로 뒤섞이지 ㅇ낳고 하위 도메인마다 바운디드 컨텍스트를 갖는 효과를 낼 수 있다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%203.png)

</aside>

## 바운디드 컨텍스트 구현

<aside>
✍️ **NOTE**

바운디드 컨텍스트가 도메인 모델만 포함하는것은 아니다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%204.png)

- 도메인 기능을 사용자에게 제공하는데 필요한 표현/응용/인프라스트럭쳐 영역을 모두포함한다.
- 도메인 모델의 데이터 구조가 바뀌면 DB테이블 스키마도 함께 변경해야 하므로 테이블도 바운디드 컨텍스트에 포함된다.

표현영역은 HTML 페이지 / Rest API를 제공할수도 있다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%205.png)

- 모든 바운디드 컨텍스트를 반드시 도메인 주도로 개발할 필요는 없다.
- 상품의 리뷰는 복잡한 도메인 로직을 갖지 않기 때문에 CRUD 방식으로 구현해도 된다.
- 서비스 - DAO 구조를 사용하면 도메인 기능이 서비스에 흩어지게 되지만 기능 자체가 단순하면 서비스-DAO CRUD 방식을 사용해도 된다고 생각한다.

하나의 바운디드 컨텍스트에 두 방식을 혼합해서 사용할 수도 있다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%206.png)

- ex) CQRS 패턴(Command Query Responsibility Segregation)
- 상태를 변경하는 명령 기능과 내용을 조회하는 쿼리 기능을 위한 모델을 구분하는 패턴이다.

바운디드 컨텍스트가 반드시 사용자에게 보여지는 UI를 가지고 있어야 하는 것은 아니다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%207.png)

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%208.png)

- 상품의 상제 벙보를 보여주는 페이지를 생각해보자
- 웹 브라우저는 바운디드 컨텍스트를 통해 상세 정보를 읽은다음, 리뷰 바운디드 컨텍스트의 Rest API를 직접 호출해서 로딩한 JSON 데이터를 가공해서 록을 보여줄 수도 있다.
</aside>

## 바운디드 컨텍스트간 통합

<aside>
✍️ **NOTE**

온라인 쇼핑 사이트에서 매출 중대를 위해 카탈로그 하위 도메인에 개인호 ㅏ추천 기능을 도입했다고 가정해보자

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%209.png)

- 기존 카탈로그 시스템을 개발하던 팀과 별도로 추천 시스템을 담당하는 팀이 새로 생겨, 이 팀에서 주도적으로 추천 시스템을 만들기로 한다.
- 카탈로그 하위 도메인에는 기존 카탈로그를 위한 바운디드 컨텍스트와 추천 기능을 위한 바운디드 컨텍스트가 생긴다.
- 두 팀이 관련된 바운디드 컨텍스트를 개발하면 자연스럽게 두 바운디드 컨텍스트 간 통합이 발생한다.
    - 사용자가 제품 상세 페이지를 볼 때, 보고 있는 유사한 상품 목록을 보여준다.

사용자가 카탈로그 바운디드 컨텍스트에 추천 제품 목록을 요청하면 카탈로그 바운디드 컨텍스트는 추천 바운디드 컨텍스트로부터 추천 정보를 읽어와 추천 제품 목록을 제공한다.

- 카탈로그 - 컨텍스트와 추천 컨텍스트의 도메인 모델은 서로 다르다.
    - 카탈그는 제품을 중심으로 도메인 모델을 구현한다,
    - 추천은 추천 연산을 위한 모델을 구현한다.

카탈로그 시스템은 추천 시스템으로부터 추천 데이터를 받아오지만, 카탈로그 시스템에서는 추천의 도메인 모델을 사용하기보다는 카탈로그 도메인 모델을 사용해서 추천 상품을 표현해야 한다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2010.png)

- 도메인 서비스를 구현할 클래스는 인프라스트럭쳐 영역에 위치한다.
- 이 클래스는 외부 시스템과의 연동을 처리하고 외부 시스템의 모델과 현재 도메인 모델간의 변환을 책임진다.
- 위의 그림에서 REST API가 제공하는 데이터는 추천 시스템을 기반으로 하므로, API 응답은 카탈로그 도메인 모델과 일치하지 않는 데이터를 보낸다.

ReSystemClient는 REST API로부터 데이터를 읽어와 카탈로그 도메인에 맞는 상품 모델로 변환한다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2011.png)

```java
public class RecSysClient implements ProductRecommendationService {
    private ProductRepository productRepository;

    @Override
    public List<Product> getRecommendationsOf(ProductId id) {
        List<RecommendationItem> items = getRecItems(id.getValue());
        return toProducts(items);
    }

		// 외부 추천시스템을 통해 데이터 가져
    private List<RecommendationItem> getRecItems(String itemId) {
        // externalRecClient는 외부 추천 시스템을 위한 클라이언트라고 가정
        return externalRecClient.getRecs(itemId);
    }

		// Catalog -> Product 변환
    private List<Product> toProducts(List<RecommendationItem> items) {
        return items.stream()
                    .map(item -> toProductId(item.getItemId()))
                    .map(prodId -> productRepository.findById(prodId))
                    .collect(toList());
    }

    private ProductId toProductId(String itemId) {
        return new ProductId(itemId);
    }

    ...
}
```

- getRecItems() 메서드에 사용하는 externalRecClient는 외부 추천 시스템에 연결할 떄 사용하는 클라이언트로써 팀에서 배포한 추천 시스템을 관리하는 모듈이라 가정하자.
- toProduct()를 통해서 카탈로그 도메인의 Product 모델로 변환하는 작업을 처리한다.

REST API를 호출하는 것은 두 바운디드 컨텍스트를 직접 통합하는 방식이다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2012.png)

- 직접 통합하는 방식 이외에 간접적으로 통합하는 방법이 있는데 대표적으로 메세지 큐가 있다.
- 추천 시스템은 사용자가 조회한 상품 이력이나 구매 이력과 같은 사용자 활동 이력을 필요로하는데 이 내역을 메시지 큐를 사용할 수 있다.
- 메세지큐는 비동기로 메세지를 처리하기 때문에 카탈로그 바운디드 컨텍스트는 메시지를 큐에 추가한뒤에 추천 바운디드 컨텍스트가 메시지를 처리할 떄 까지 기다리지 않고 바로 이어서 자신의 처리를 계속한다.

추천 바운디드 컨텍스트는 큐에서 이력 메시지를 읽어와 추천을 계산하는데 사용한다. 이것은 두 바운디드 컨텍스트가 사용할 메시지의 데이터 구조를 맞춰야 함을 의미한다.

- 각각의 바운디드 컨텍스트를 담당하는 팀은 서로 만나서 주고받을 데이터 형식에 대해 협의해야 한다.
- 메시지 시스템을 카탈로그 측에서 관리하고 있다면 큐에 담기는 메시지는 그림과 같다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2013.png)

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2014.png)

어떤 도메인 관점에서 모델을 사용하느냐에 따라 두 바운디드 컨텍스트의 구현 코드가 달라진다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2015.png)

```java
// 상품 조회 관련 로그 기록 코드
public class ViewLogService {
    private MessageClient messageClient;

    public void appendViewLog(String memberId, String productId, Date time) {

				// 카탈로그 도메인 기준
        messageClient.send(new ViewLog(memberId, productId, time));

				// 추천 시스템을 기준
				messageClient.send(new ActivityLog(memberId, productId, time));
    }
    // ...
}

// messageClient
public class RabbitMQClient implements MessageClient {
    private RabbitTemplate rabbitTemplate;

		// 카탈로그 도메인 기준
    @Override
    public void send(ViewLog viewLog) {
        // 카프카나 기준으로 작성된 메시지큐로 메시지를 전송
        rabbitTemplate.convertAndSend(logQueueName, viewLog);
    }

		// 추천 시스템 기준
		@Override
    public void send(ActivityLog activityLog) {
        // 카프카나 기준으로 작성된 메시지큐로 메시지를 전송
        rabbitTemplate.convertAndSend(logQueueName, activityLog);
    }

}
```

- 이러한 구조는 메시지큐를 누가 제공하느냐에 따라 데이터 구조가 결정된다.
- ex) 카탈로그가 큐에 데이터를 제공하는 입장이면 카탈로그 도메인을 따른다.

### 마이크로서비스와 바운디드 컨텍스트

MSA가 단순 유행을 지나 많은 기업에서 MSA 아키텍쳐를 채용하고 있다.

마이크로 서비스는 애플리케이션을 작은 서비스로 나누어 개발하는 아키텍쳐 스타일이며, 개별 서비스를 독립된 프로세스로 실행하고 각 서비스가 REST API 메시징을 이용해서 통신하는 구조를 가진다.

이런 마이크로서비스의 특징은 바운디드 컨텍스트와 어울린다.

각 바운디드 컨텍스트는 모델의 경께를 형성하는데 바운디드 컨텍스트를 마이크로서비스로 구현하면 자연스럽게 컨텍스트별로 모델이 분리된다.

코드로 생각하면 마이크로서비스마다 프로젝트를 생성하므로 바운디드 컨텍스트별로 프로젝트를 만들게된다.

별도 프로세스로 개발한 바운디드 컨텍스트는 독립적으로 배포하고 모니터링하며 확장되는데 이 역시 마이크로 서비스가 갖는 특징이다.

</aside>

## 바운디드 컨텍스트 간 관계

<aside>
✍️ **NOTE**

바운디드 컨텍스트는 어떤 식으로 든 연결되기 떄문에 두 바운디드 컨텍스트는 다양한 방식으로 관계를 가진다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2016.png)

- 가장 대표적인 관계는 API를 제공하는 REST API이다.
- 그림과 같이 하류 컴포넌트인 카탈로그는 상류 컴포넌트인 추천 컨텍스트가 제공하는 데이터와 기능에 의존한다.
    - 카탈로그 → 추천 상품을 보여주기 위해 추천 바운디드 컨텍스트가 제공하는 데이터 + 기능에 의존한다.

상류 컴포넌트는 하류 컴포넌트가 사용할 수 있는 통신 프로토콜을 정의하고 이를 공개한다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2017.png)

- ex) 추천 시스템은 하류 컴포넌트가 사용할 수 있는 REST API 혹은 프로토콜 버퍼와 같은 것을 이용해서 서비스를 제공할 수 있다.
- 상류팀의 고객인 하류 팀이 다수 존재하면 상류팀은 여러 하류팀의 요구사항을 수용할 수 있는 API를 만들고 이를 서비스 형태로 공개해서 서비스의 일관성을 유지할 수 있다.
    - 이런 서비스를 공개 호스트 서비스(OPEN HOST SERVICE)라고 한다.

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2018.png)

상류 컴포넌트의 서비스는 상류 바운디드 컨텍스트의 도메인 모델을 따른다. 따라서 하류 컴포넌트는 상류 서비스의 모델이 자신의 도메인 모델에 영향을 주지 않도록 보호하는 완충지대를 다시 만들어야 한다.

두 바운디드 컨텍스트가 같은 모델을 경유하는 경우도 있다.

- ex) 운영자를 위한 주문관리 도구를 개발하는 팀과 고객을 위한 주문 서비스를 개발하는 팀이 다르다고 가정하자.
- 두팀은 주문을 표현하는 모델을 공유함으로써 주문과 관련된 중복 설계를 막을 수 있다.
    - 이러한 공유하는 모델을 공유 커널이라 부른다.
- 공유 커널의 장점은 중복을 줄여주지만, 여러팀이 하나의 모델을 사용하기때문에 하노ㅉㄱ에서 임의로 변경하면 안된다.

마지막으로 볼 관계는 독립 방식(SEPARATE WAY)이다.

- 그냥 서로 통합하지 않은 방식이며, 독립적으로 개발한다.
- 독립 방식에서 두 바운디드 컨텍스트 간의 통합은 수동으로 이루어진다

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2019.png)

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2020.png)

</aside>

## 컨텍스트 맵

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-8%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%B0%94%EC%9A%B4%EB%94%94%EB%93%9C%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B2%BD%EA%B3%84/Untitled%2021.png)

개별 바운디드 컨텍스트에 매몰되면 전체를 보지 못하므로, 전체 비즈니스를 조망할 수 있는 컨텍스트 맵을 만든다.

- OHS → 오픈 호스트 서비스
- ACL → 안티코럽션 계층

</aside>