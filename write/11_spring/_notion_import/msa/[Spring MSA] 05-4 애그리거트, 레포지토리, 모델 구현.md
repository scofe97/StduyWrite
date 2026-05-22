# [Spring MSA] 05-4. 애그리거트, 레포지토리, 모델 구현

주제: Spring MSA

- 참고
    
    

# 애그리거트

---

<aside>
✍️ **NOTE**

> ***애그리거트는 위에서 말한 복잡한 도메인을 쉬운 단위로 묶기위해서 사용하는 방법이다.***
> 

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled.png)

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%201.png)

수백 개의 테이블을 **하나의 ERD에 모두 표시하면 개별 테이블 간의 관계를 파악하기 매우 어렵습니다.**

주요 도메인 요소간의 관계를 파악하는 것은 확장성이 떨어지는 것을 의미하며, 상위 수준에서 모델이 어떻게 엮여 있는지 알아야 전체 모델을 망가뜨리지 않으면서 추가 요구사항을 모델에 반영할 수 있습니다. 세부적인 모델만 이해한 상태에서 코드를 수정하는 것은 꺼려지기 때문입니다.

- **애그리거트** 단위를 통해 일관성을 관리하기 때문에 도메인을 보다 단순한 구조로 만들어줍니다.
- **애그리거트**는 관련된 모델을 하나로 모았기 때문에, 애그리거트에 속한 객체는 유사하거나 동일한 라이프 사이클을 가집니다.
    - 예시) Order을 생성하면 OrderLine, Orderer와 같은 객체들은 한 번에 생성됩니다.
- **애그리거트**는 경계를 가지며, 각 애그리거트 내에서만 관리가 가능합니다.

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%202.png)

밀접해보이는 도메인이 꼭 같은 애그리거트로 묶이지는 않는다.

- 처음 도메인 모델을 만들면 큰 애그리거트로 보이는 것들이 많지만, 도메인에 대한 경험이 생기고 이해할수록 애그리거트는 점점 작아진다.
</aside>

## 애그리거트 루트

<aside>
✍️ **NOTE**

> ***애그리거트 루트는 애그리거트의 대표 Entity이다!***
> 

![애그리거트 = 완전한 1개의 도메인 모델을 표현 ⇒ **레포지터리도 애그리거트 단위로 존재**](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%203.png)

애그리거트 = 완전한 1개의 도메인 모델을 표현 ⇒ **레포지터리도 애그리거트 단위로 존재**

애그리거트는 외부에서 애그리거트에 속한 객체를 변경하면 안된다.

```java
ShippingInfo si = order.getShippingInfo();
si.setAddress(newAddress); // 외부에서 이렇게 변경하면 일관성이 깨진다.
													 // ShippingInfo가 불변이면, 이 코드는 컴파일 에
```

- Set메서드를 공개범위로 만들지 말자
- 밸류 타입은 불변으로 구현하자

**트랜잭션은 작을수록 좋습니다.** (1개의 테이블을 잠그는 것과 3개의 테이블을 잠그는 것은 성능에서 차이가 발생합니다.) **하나의 트랜잭션은 하나의 애그리거트만 수정해야 합니다.**

- 만약 한 트랜잭션에서 2개 이상의 애그리거트를 수정해야 한다면, 애그리거트에서 직접 수정하지 말고, 응용서비스에서 두 애그리거트를 수정하도록 구현합니다.
- 도메인 이벤트를 사용하면 한 트랜잭션에서 1개의 애그리거트를 수정하면서도 동기나 비동기로 다른 애그리거트의 상태를 변경하는 코드를 작성할 수 있습니다.

애그리거트는 완전한 1개의 도메인 모델을 표현합니다. 레포지터리도 애그리거트 단위로 존재합니다.

- Order와 OrderLine을 물리적으로 별도의 DB 테이블에 저장한다 해도, 각 레포지터리를 각각 만들지 않습니다. (JPA를 통해 레포지토리 구현은 이후 자세히 다룰 예정입니다.)
</aside>

## ID를 이용한 애그리거트 참조

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%204.png)

애그리거트간의 참조는 필드를 통해 쉽게 구현할 수 있다.  

- 주문에 속해있는 **Orderer**는 **Meber** 필드를 통해 **Member**를 조회할 수 있다.

애그리거트를 직접 참조할 수 있을때 발생하는 문제점이 존재한다. 

```java
// 다른 애그리거트의 상태를 변경하는 것은 의존 결합도를 높인다.
orderer.getMember().changeAddress(newShippingInfo.getAddrss());
```

- 다른 애거리거트의 상태를 쉽게 변경할 수 있게 된다는 점이다.
- 애그리거트를 직접 참조하면 성능에 관련해서 고민을 해야한다. (즉시 vs 지연 로딩)
- 확장성이 떨어진다. (각 애그리거트가 다른 DB를 사용하는 경우, 단순히 JPA만으로 안됨)

3번째 문제를 해결하기 위해서는, **ID를 통해 다른 애그리거트를 참조하는것이 좋다.** 

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%205.png)

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%206.png)

- 하지만 다른 애그리거트를 ID로 참조하면 참조하는 여러 애그리거트를 읽을 때 조회 속도가 문제될수 있다.
- 예를들어 주문 목록을 보여주려면 상품 애거리거트와 회원 애그리거트를 함께 읽어야 하는데, 이를 처리할 때 다음과 같이 각 주문마다 **상품과 회원 애그리거트를 읽어온다고 해보자.**
    
    ```java
    List<Order> orders = orders = orderRepository.findByOrderer(ordererId);
    
    // order 도메인에서 상품을 N번꺼내게됨.
    List<OrderView> dtos = orders.stream()
    	.map(order -> {
    			ProductId prodId = order.getOrderLines().get(0).getProductId();
    			Product product = productRepository.findById(prodId);
    			return new OrderView(order, member, product);
    	}).collect(toList());
    ```
    
    - N개의 대상을 조회할 때, 1번의 쿼리로 N개를 읽어오고 이에 연관된 데이터를 가져오는 쿼리를 N번 실행합니다. (N+1번의 문제)
    - ID를 이용한 애그리거트 참조는 지연로딩과 유사한 효과를 가져오지만, 이로 인해 N+1 조회 문제와 같은 문제가 발생할 수 있습니다. ⇒ **이로 인해 쿼리의 증가로 인해 조회 속도가 느려지는 문제가 발생합니다.**
    - 가장 쉬운 해결책은 객체 참조 방식으로 변경하고, 즉시 로딩을 사용하도록 설정을 변경하는 것입니다. (하지만 이로 인해 이전에 언급한 문제가 다시 발생할 수 있음)

**ID 참조를 통해 N + 1 문제를 방지하려면 조회 전용 쿼리를 사용하면 됩니다.**

```java
public List<OrderView> selectByOrderer(String ordererId) {
    // JPQL 쿼리를 문자열로 생성
    String selectQuery =
        "select new com.myshop.order.application.dto.OrderView(o, m, p) " +
        "from Order o join o.orderLines ol, Member m, Product p " +
        "where o.orderer.memberId.id = :ordererId " + // 주문자 ID로 필터링
        "and o.orderer.memberId = m.id " + // 주문자와 멤버 ID 연결
        "and index(ol) = 0 " + // orderLines의 첫 번째 요소를 선택
        "and ol.productId = p.id " + // orderLine의 제품 ID와 제품 ID 연결
        "order by o.number.number desc"; // 주문 번호 내림차순으로 정렬

    // 문자열로 생성된 쿼리를 실행하기 위한 TypedQuery 객체 생성
    TypedQuery<OrderView> query =
        em.createQuery(selectQuery, OrderView.class);

    // 쿼리 파라미터 설정 (주문자 ID)
    query.setParameter("ordererId", ordererId);

    // 쿼리 실행 및 결과 목록 반환
    return query.getResultList();
}
```

- Join이 포함된 쿼리가 더 복잡할지언정, DB의 성능의 주요문제중 하나인 라운드 트립(조회빈도)를 해결하기 때문에 일반적으로 더 효율적이다.
</aside>

## 애그리거트 간 집합 연관

<aside>
✍️ **NOTE**

> ***애그리거트간 1-N , N-1 모델을 구현할때는 N+1문제를 회파하기 위해  N-1을 주로 사용하자.***
> 

```java
public List<Product> getProduct(int page, int size){
	List<Product> sortedProducts = sortById(products);
	return sortedProducts.subList((page-1) * size, page * size);
}
```

이 코드를 실제 데이터베이스 관리 시스템(DBMS)에 적용하면, 특정 카테고리에 속한 모든 Product들을 조회할 수 있습니다.

- 하지만, 제품의 수가 수만 개에 이른다면, 매번 실행할 때마다 처리 속도가 상당히 느려지는 문제가 발생할 수 있습니다. 이런 성능 문제를 감안할 때, 개념적으로는 **1-N 관계가 존재할지라도, 실제 구현에서는 이를 반영하지 않는 것이 좋습니다.**

카테고리에 속한 제품들을 찾아야 할 필요가 있을 때는, 제품을 기준으로 하여 해당 제품이 속한 카테고리와의 **N-1 관계**를 이용해 조회하는 것이 훨씬 효율적입니다.

```java
public List<Product> getProductCategory(Long categoryId, int page, int size){
	Category category = categoryRepository.findById(categoryId);
	
	checkCategory(category);

	List<Product> product = // JPA 쿼리로 특정 데이터만 뽑아옴!
			productRepository.findByCategoryId(category.getId(), page, size);

	int totalCount = productRepository.countByCategoryId(category.getId());

	return new Page(page, size, totalCount, products);
```

</aside>

## 애그리거트를 팩토리로 사용하기

<aside>
✍️ **NOTE**

> ***고객에 특정 상점을 여러 차례 신고해서 해당 상점이 더 이상 물건을 등록하지 못하도록 차단한 상태라고 가정해보자***
> 

```java
public class RegisterProductService {
    public ProductId registerNewProduct(NewProductRequest req) {
        Store store = storeRepository.findById(req.getStoreId());

        // 상점이 null이면 예외를 던집니다.
        checkNull(store)

        // 상점이 차단(blocked)되었으면 예외를 던집니다. (도메인 로직 노출)
        if (store.isBlocked()) {
            throw new StoreBlockedException();
        }

        ProductId id = productRepository.nextId();
        Product product = new Product(id, store.getId(), ...);
        productRepository.save(product);
        return id;
    }
    ...
}
```

- 상품 등록 기능을 구현한 서비스는 차단 상태가 아닌 경우에만 구현할 수 있다.
- 도메인 로직 처리(Store가 Product를 생성할 수 있는지 판단)하는 로직이 노출되었다. 이는 도메인 로직인데 서비스에서 구현된것
- 이를 별도의 클래스로 만들 수있으나, 애그리거트에 구현할 수도 있다.

```java
public class RegisterProductService {

    public ProductId registerNewProduct(NewProductRequest req) {
        Store store = storeRepository.findById(req.getStoreId());
        checkNull(store);

        ProductId id = productRepository.nextId();
        Product product = store.createProduct(id, ...생략);
        productRepository.save(product);
        return id;
    }
    // ...
}
```

```java
public class Store {
    public Product createProduct(ProductId newProductId, ProductInfo pi) {
        // 만약 상점이 차단된 경우, StoreBlockedException을 던진다.
        if (isBlocked()) throw new StoreBlockedException();

        // 상점이 차단되지 않은 경우, 새로운 Product 인스턴스를 생성하여 반환한다.
        return ProductFactory.create(newProductId, getId(), pi);
    }
}
```

</aside>

# JPA 레포지토리 구현

---

<aside>
💡 **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%207.png)

레포지토리 구현 클래스는 인프라 영역에 위치해야한다. (JPA는 어차피 자동생성이니 크게 신경쓰지마라)

</aside>

## 매핑 구현

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%208.png)

**애그리거트 루트 엔티티** 

- @Entity

**밸류 , 밸류 타입 프로퍼티**

- @Embeddable, @Embedded

### AttributeConverter 이용한 밸류 맵핑처리

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%209.png)

```java
@Converter(autoApply = true)
public class MoneyConverter implements AttributeConverter<Money, Integer> {

    @Override
    public Integer convertToDatabaseColumn(Money money) {
        // Money 객체가 null이 아니라면, money의 값을 가져와 데이터베이스 컬럼으로 변환
        return money == null ? null : money.getValue();
    }

    @Override
    public Money convertToEntityAttribute(Integer value) {
        // 데이터베이스 컬럼 값이 null이 아니라면, 해당 값을 사용하여 Money 객체를 생성
        return value == null ? null : new Money(value);
    }
}

@Converter(converter = MoneyConverter.class)
private Money totalAmounts;
```

### 밸류 컬렉션  : 별도의 테이블 매핑

![Untitled](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%2010.png)

```java
@Entity
@Table(name = "purchase_order")
public class Order {
    @EmbeddedId
    private OrderNo number;
    // ... other fields ...

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "order_line", joinColumns = @JoinColumn(name = "order_number"))
    @OrderColumn(name = "line_idx")
    private List<OrderLine> orderLines;
    // ... other fields ...
}

@Embeddable
public class OrderLine {
    @Embedded
    private ProductId productId;

    @Column(name = "price")
    private Money price;

    @Column(name = "quantity")
    private int quantity;

    @Column(name = "amounts")
    private Money amounts;
    // ... other fields ...
}
```

### 밸류 컬랙션 : 1개 컬럼 맵핑

도메인 모델에는 이메일 주소 목록을 Set으로 보관하고 DB에는 1개 컬럼에 콤마로 구분해서 저장한다

```java
public class EmailSet {
    private Set<Email> emails = new HashSet<>();

    public EmailSet(Set<Email> emails) {
        this.emails.addAll(emails);
    }

    public Set<Email> getEmails() {
        return Collections.unmodifiableSet(emails);
    }
}

public class EmailSetConverter implements AttributeConverter<EmailSet, String> {
    @Override
    public String convertToDatabaseColumn(EmailSet attribute) {
        if (attribute == null) return null;
        return attribute.getEmails().stream()
                .map(email -> email.getAddress())
                .collect(Collectors.joining(","));
    }

    @Override
    public EmailSet convertToEntityAttribute(String dbData) {
        if (dbData == null) return null;
        String[] emails = dbData.split(",");
        Set<Email> emailSet = Arrays.stream(emails)
                .map(value -> new Email(value))
                .collect(Collectors.toSet());
        return new EmailSet(emailSet);
    }
}
```

### 밸류를 이용한 ID 맵핑

식별자라는 의미를 부각시키기 위해 식별자 자체를 밸류 타입으로 만들 수 있다.

```java
@Entity
@Table(name = "purchase_order")
public class Order {
    @EmbeddedId
    private OrderNo number;
    // ... other fields ...
}

@Embeddable
public class OrderNo implements Serializable {
    @Column(name = "order_number")
    private String number;
    // ... other fields ...
}
```

- OrderNo, MemberId등이 이를위한 밸류타입의 예시이다.

### 별도 테이블에 저장하는 밸류 맵핑

![Aritcle Content의 경우, Article과 연결하기 위해 ID가 있을뿐 식별자가 필요한건 아니다.](%5BSpring%20MSA%5D%2005-4%20%EC%95%A0%EA%B7%B8%EB%A6%AC%EA%B1%B0%ED%8A%B8,%20%EB%A0%88%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC,%20%EB%AA%A8%EB%8D%B8%20%EA%B5%AC%ED%98%84/Untitled%2011.png)

Aritcle Content의 경우, Article과 연결하기 위해 ID가 있을뿐 식별자가 필요한건 아니다.

애그리거트에서 루트 엔티티를 뺸 나머지 구성요소는 대부분 밸류이다. 만약 다른 엔티티가 있다면 진짜 엔티티인지 의심해봐야 한다.

밸류가 아니라 엔티티가 확실하다면 해당 엔티티가 다른 애거리거트는 아닌지 확인해야 한다. 특히 자신만의 독자적인 라이프 사이클을 가진다면 구분될 확률이 높다.

단 개념적으로 밸류여도 구현 기술의 한계로 Entity를 사용해야 할 때도 있다. 이런 경우 변경 메소드를 제공하지 않아야한다. 또한 삭제규칙와, 여러 규칙을 추가한다.

```java
@Entity
@Table(name = "product")
public class Product {
    @EmbeddedId
    private ProductId id;
    private String name;
    @Convert(converter = MoneyConverter.class)
    private Money price;
    private String detail;

    @OneToMany(
        cascade = {CascadeType.PERSIST, CascadeType.REMOVE},
        orphanRemoval = true
    )
    @JoinColumn(name = "product_id")
    @OrderColumn(name = "list_idx")
    private List<Image> images = new ArrayList<>();

    // ...

    public void changeImages(List<Image> newImages) {
        images.clear();
        images.addAll(newImages);
    }
}
```

</aside>

## 애그리거트 로딩 전략

<aside>
✍️ **NOTE**

> ***JPA 맵핑을 설정할때 가장 중요한건 애그리거트에 속한 객체가 모두 모여야 완전한 하나가 된다는 것이다.***
> 

즉 다음과 같이 애그리거트 루트를 로딩하면 루트에 속한 모든 객체가 완전한 상태여야 함을 의미한다.

```java
Proudct product = productRepositroy.findById(id);
```

- 데이터를 조회할 때, 애그리거트가 완전한 상태임을 보장하기 위해 **즉시 로딩 방식**을 사용하는 것이 일반적입니다. 이는 `FetchType.EAGER` 설정을 통해 맵핑된 관계를 즉시 로딩으로 설정하는 것을 의미합니다. 그러나 이 방법을 사용하면 때때로 **성능 문제가 발생**할 수 있습니다.
- 대부분의 애플리케이션에서는 **조회 기능의 사용 빈도가 매우 높습니다.** 이 경우, 상태 변경을 위해 지연 로딩을 사용하면 발생하는 추가 쿼리의 지연 시간은 일반적으로 크게 문제되지 않습니다.
- 결론은, 애그리거트의 특성에 따라 적절히 지연 로딩과 즉시 로딩을 설정하는 것이 중요합니다.
</aside>

# 스프링 데이터 JPA를 이용한 조회 기능

---

<aside>
💡 **NOTE**

> ***CQRS, 즉 Command Query Responsibility Segregation은 명령(Command) 모델과 조회(Query) 모델을 분리하는 디자인 패턴입니다. 이 방법론을 시작하기 전에, CQRS의 개념을 간단히 살펴보겠습니다.***
> 
- 명령 모델: 이는 상태를 변경하는 기능을 담당합니다.
    - ex) 회원 가입, 암호 변경과 같은 기능이 여기에 속합니다.
- 조회 모델: 데이터를 조회하는 기능에 초점을 맞춥니다.
    - ex) 주문 목록 확인, 주문 상세 조회 등이 이에 해당합니다.

앞서 언급한 **엔티티**, **애그리거트**, **레포지토리** 등은 주로 상태 변경에 사용됩니다. 이들은 주로 **명령 모델**로 활용됩니다. 반면에 **정렬, 페이징, 검색 조건** 설정과 같은 기능은 **조회 기능**에서 주로 사용됩니다.

이러한 이유로, 이번 장에서는 **레포지토리(도메인 모델에 속한)**와 **DAO(데이터 접근 의미)**라는 용어를 혼용하여 사용합니다.

### Repository vs DAO

```java
public interface ProductDAO {

    Product saveProduct(Product product);

    Product getProduct(String productId);

}

@Service
public class ProductDAOImpl implements ProductDAO {

    private final Logger LOGGER = LoggerFactory.getLogger(ProductDAOImpl.class);

    ProductRepository productRepository;

    @Autowired
    public ProductDAOImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    public Product saveProduct(Product product) {
        LOGGER.info("[saveProduct] product 정보 저장. productId : {}", product.getId());
        Product product1 = productRepository.save(product);
        LOGGER.info("[saveProduct] product 정보 저장완료. productId : {}", product1.getId());
        return product1;
    }

    @Override
    public Product getProduct(String productId) {
        LOGGER.info("[getProduct] product 정보 요청. productId : {}", productId);
        Product product = productRepository.getById(productId);
        LOGGER.info("[getProduct] product 정보 요청 완료. productId : {}", product.getId());
        return product;
    }
}
```

```java
public interface ProductRepository extends JpaRepository<Product, String> {

    /* 쿼리 메소드의 주제 키워드 */

    // 조회
    List<Product> findByName(String name);
    List<Product> queryByName(String name);

    // 존재 유무
    boolean existsByName(String name);

    // 쿼리 결과 개수
    long countByName(String name);

    // 삭제
    void deleteByName(String name);
    long removeByName(String name);

    // 값 개수 제한
    List<Product> findFirst5ByName(String name);
    List<Product> findTop3ByName(String name);
	  //..
}
```

- Repository
    - Entity에 의해 생성된 데이터베이스에 접근하는 메소드를 사용하기 위한 인터페이스
    - Service - DB의 연결고리
- DAO
    - 데이터베이스에 접근하는 객체를 의미 (영속성 레이어)
    - Service가 DB에 연결할 수 있게 해주는 역할
</aside>

## 검색을 위한 스펙

<aside>
✍️ **NOTE**

검색 조건이 고정되어 있고 단순하면 JPA로 바로 구현함녀된다.

하지만 목록 조회와 같은 기능은 다양한 검색조건이 필요할 수 있다. 조합이 증가할수록 find메서드가 증가하기 때문이다. 이 때 사용할 수 있는것이 스펙이다.

스펙은 애그리거트가 특정 조건을 충족하는지 사용하는 인터페이스이다.

```java
public class OrdererSpec implements Specification<Order> {
    private String ordererId;

    public OrdererSpec(String ordererId) {
        this.ordererId = ordererId;
    }

    public boolean isSatisfiedBy(Order agg) {
        return agg.getOrdererId().getMemberId().getId().equals(ordererId);
    }
}
```

```java
public class MemoryOrderRepository implements OrderRepository {
    public List<Order> findAll(Specification<Order> spec) {
        List<Order> allOrders = findAll();
        return allOrders.stream()
                .filter(order -> spec.isSatisfiedBy(order))
                .toList();
    }
    // ...
}

// 클래스 주석을 포함하는 스니펫을 사용하여
Specification<Order> ordererSpec = new OrdererSpec("madiviru5");

// 리포지토리에 전달
List<Order> orders = orderRepository.findAll(ordererSpec);
```

하지만 실제 스펙은 이렇게 구현하지 않는다. 실제 스펙은 스프링 데이터 JPA를 이용해서 구현된다.

</aside>