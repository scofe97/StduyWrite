# DDD 모델 작성

주제: Spring Study

## 1. 값 객체 (Value Object)

> “값 객체는 변화하지 않는 순간의 기억이다.”
> 

### 정의

- **식별자 없이**, 그 **속성 값 자체(Value)**로 동등성을 판단하는 객체
- 불변성(Immutable)을 지녀 재사용과 비교가 쉽다

### 특징

- **동등성(equals)**: 모든 속성이 같으면 같은 객체
- **불변성**: 속성은 `final`로 선언해 생성 이후 변경 불가
- **가치 표현**: `Money`, `Address`, `Period`처럼 그 자체로 의미 완성

### 장점

1. **안정성**: 한 번 만들어지면 상태 변화가 없어 스레드 안전
2. **단순비용 최적화**: 동일 값이면 재사용 가능
3. **의미 명료**: 비즈니스 개념이 코드에 직관적으로 드러남

### 단점

1. **조합 비용**: 속성이 많아지면 생성자 또는 팩토리 메서드가 복잡
2. **불변성 관리**: Java에서는 매번 새 객체 생성이 필요해 GC 부담

### 예제 코드

```java
package com.example.domain;

import java.util.Objects;

// 금액을 표현하는 값 객체
public final class Money {
    private final long amount;      // 최소 단위 통화(예: 센트)
    private final String currency;  // "KRW", "USD" 등

    private Money(long amount, String currency) {
        this.amount   = amount;
        this.currency = Objects.requireNonNull(currency);
    }

    // 생성 팩토리 메서드
    public static Money of(long amount, String currency) {
        return new Money(amount, currency);
    }

    public long getAmount() { return amount; }
    public String getCurrency() { return currency; }

    // 값 더하기
    public Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("통화 단위가 다릅니다.");
        }
        return new Money(amount + other.amount, currency);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Money m)) return false;
        return amount == m.amount && currency.equals(m.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }

    @Override
    public String toString() {
        return String.format("%d %s", amount, currency);
    }
}

```

---

## 2. 엔티티 (Entity)

> “엔티티는 시간 속에 자신만의 정체성을 새긴 존재이다.”
> 

### 정의

- *고유 식별자(ID)**를 바탕으로 동등성을 판단하는 객체
- 라이프사이클(생성·변경·삭제)에 따라 상태가 변할 수 있음

### 특징

- **ID 기반 동등성**: `equals`/`hashCode`는 일반적으로 `id`만으로 구현
- **상태 변화**: 비즈니스 로직에 따라 속성 값이 변경될 수 있음
- **영속성 매핑**: RDB 테이블의 PK와 매핑

### 장점

1. **명확한 참조**: 식별자를 통해 여러 곳에서 안전하게 참조
2. **유연한 변화 관리**: 상태 변화 이력을 추적·관리 가능
3. **풍부한 행위(Behavior)**: 데이터뿐 아니라 로직도 담아낼 수 있음

### 단점

1. **동시성 이슈**: 상태 변경 시 동시성·락 관리를 고민해야 함
2. **비즈니스 로직 복잡도**: 상태 전이에 따른 유효성 검사 코드가 늘어남

### 예제 코드

```java
package com.example.domain;

import java.util.Objects;

// 고객을 표현하는 엔티티
public class Customer {
    private final Long id;      // 고유 식별자
    private String name;        // 변경 가능
    private Address address;    // 값 객체

    public Customer(Long id, String name, Address address) {
        this.id      = Objects.requireNonNull(id);
        this.name    = Objects.requireNonNull(name);
        this.address = Objects.requireNonNull(address);
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public Address getAddress() { return address; }

    // 고객 이름 변경 로직
    public void changeName(String newName) {
        if (newName == null || newName.isBlank()) {
            throw new IllegalArgumentException("이름은 비어 있을 수 없습니다.");
        }
        this.name = newName;
    }

    // 주소 업데이트
    public void updateAddress(Address newAddress) {
        this.address = Objects.requireNonNull(newAddress);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Customer c)) return false;
        return id.equals(c.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

```

> 부록: Address 값 객체
> 

```java
package com.example.domain;

import java.util.Objects;

public final class Address {
    private final String street;
    private final String city;
    private final String zipcode;

    public Address(String street, String city, String zipcode) {
        this.street  = Objects.requireNonNull(street);
        this.city    = Objects.requireNonNull(city);
        this.zipcode = Objects.requireNonNull(zipcode);
    }

    // getters 생략…

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Address a)) return false;
        return street.equals(a.street)
            && city.equals(a.city)
            && zipcode.equals(a.zipcode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(street, city, zipcode);
    }
}

```

---

## 3. 애그리게이트 (Aggregate)

> “애그리게이트는 도메인 객체들이 어우러진 하나의 일관성 경계다.”
> 

### 정의

- *하나의 루트 엔티티(Aggregate Root)**와 그에 속한 **자식 객체(Value Object 또는 Entity)**들의 집합
- 외부에서는 **루트만** 직접 참조하고, 내부 객체는 **루트**를 통해서만 접근

### 특징

- **일관성 경계**: 한 애그리게이트 내 트랜잭션은 전부 성공하거나 전부 실패
- **캡슐화**: 내부 구조를 외부에 드러내지 않고, 루트가 유효성·변경을 책임
- **참조 제한**: 다른 애그리게이트는 ID 참조만 허용

### 장점

1. **데이터 무결성 보장**: 트랜잭션 경계가 명확해 일관성 유지
2. **모델 단순화**: 외부에 공개할 인터페이스가 루트 하나로 제한되어 복잡도 감소
3. **캡슐화 강화**: 내부 구현 변경이 외부에 파급되지 않음

### 단점

1. **과도한 경계 설정 위험**: 너무 큰 애그리게이트는 성능 저하·락 경합 유발
2. **작은 단위 트랜잭션 구현 어려움**: 부분 업데이트가 필요한 경우 비효율

### 예제 코드

```java
package com.example.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

// Aggregate Root: 주문
public class Order {
    private final Long id;                 // Aggregate Root 식별자
    private final Customer customer;       // 다른 Aggregate 참조는 ID만 허용하지만, 예제 단순화를 위해 객체 참조
    private final List<OrderItem> items;   // 내부 Value Object 리스트

    public Order(Long id, Customer customer) {
        this.id       = Objects.requireNonNull(id);
        this.customer = Objects.requireNonNull(customer);
        this.items    = new ArrayList<>();
    }

    public Long getId() { return id; }
    public Customer getCustomer() { return customer; }
    public List<OrderItem> getItems() { return Collections.unmodifiableList(items); }

    // 비즈니스 행위: 주문 항목 추가
    public void addItem(String productName, Money unitPrice, int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("수량은 1 이상이어야 합니다.");
        }
        this.items.add(new OrderItem(productName, unitPrice, quantity));
    }

    // 총액 계산
    public Money totalAmount() {
        return items.stream()
            .map(OrderItem::subtotal)
            .reduce(Money.of(0, items.get(0).getUnitPrice().getCurrency()), Money::plus);
    }

    // equals/hashCode는 루트 엔티티의 ID만으로 구현
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order o2)) return false;
        return id.equals(o2.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

// 내부 Value Object: 주문 항목
final class OrderItem {
    private final String productName;
    private final Money unitPrice;
    private final int quantity;

    public OrderItem(String productName, Money unitPrice, int quantity) {
        this.productName = Objects.requireNonNull(productName);
        this.unitPrice   = Objects.requireNonNull(unitPrice);
        this.quantity    = quantity;
    }

    public String getProductName() { return productName; }
    public Money getUnitPrice() { return unitPrice; }
    public int getQuantity() { return quantity; }

    public Money subtotal() {
        return unitPrice.plus(Money.of(unitPrice.getAmount() * (quantity - 1), unitPrice.getCurrency()));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderItem oi)) return false;
        return productName.equals(oi.productName)
            && unitPrice.equals(oi.unitPrice)
            && quantity == oi.quantity;
    }

    @Override
    public int hashCode() {
        return Objects.hash(productName, unitPrice, quantity);
    }
}

```

---

### 맺음말

- **값 객체**는 **불변의 조각**으로, 비즈니스 가치를 표현하는 작은 꽃망울입니다.
- **엔티티**는 **시간의 흐름 속 정체성**을 간직한 나무로, 변화와 생애주기를 견뎌냅니다.
- **애그리게이트**는 이들을 한데 모아 **일관성의 숲**을 이루어, 비즈니스 규칙을 안전하게 지켜냅니다.

도메인 모델링은 단순한 코드 작성을 넘어 비즈니스의 언어로 가치와 규칙을 직조하는 작업입니다. 이 가이드를 통해 실질적인 사고의 틀을 다지고, 자신만의 도메인 정원을 정성껏 가꿔 나가시길 바랍니다.