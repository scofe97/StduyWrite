# DDD 참고

주제: Spring Study

```markdown
# DDD 패키지 구조 가이드

## 개요

이 프로젝트는 **도메인 주도 설계(Domain-Driven Design, DDD)** 패턴을 적용하여 구성된 Spring Boot 애플리케이션입니다. 각 도메인은 명확한 경계를 가지며, CQRS(Command Query Responsibility Segregation) 패턴과 이벤트 소싱 패턴을 적용하여 설계되었습니다.

## 패키지 구조 개요

```
src/main/java/com/myshop/
├── ShopApplication.java          # 메인 애플리케이션 클래스
├── common/                       # 공통 도메인 및 인프라스트럭처
├── member/                       # 회원 도메인
├── order/                        # 주문 도메인
├── catalog/                      # 상품 카탈로그 도메인
├── board/                        # 게시판 도메인
├── admin/                        # 관리자 도메인
├── eventstore/                   # 이벤트 저장소
├── lock/                         # 분산 락 관리
├── integration/                  # 외부 시스템 통합
└── springconfig/                 # Spring 설정
```

## 도메인별 패키지 구조

### 1. Member (회원) 도메인

```
member/
├── command/                      # 명령(Command) 처리
│   ├── domain/                  # 도메인 모델
│   └── application/             # 애플리케이션 서비스
├── query/                       # 조회(Query) 처리
│   ├── MemberData.java         # 조회용 데이터 객체
│   ├── MemberDataDao.java      # 데이터 접근 객체
│   ├── MemberDataSpecs.java    # 조회 조건 스펙
│   └── MemberQueryService.java # 조회 서비스
└── infra/                       # 인프라스트럭처
```

**역할:**
- 회원 가입, 수정, 차단 등 명령 처리
- 회원 정보 조회 및 검색
- CQRS 패턴으로 명령과 조회를 분리

### 2. Order (주문) 도메인

```
order/
├── command/                      # 명령 처리
│   ├── domain/                  # 도메인 모델
│   └── application/             # 애플리케이션 서비스
├── query/                       # 조회 처리
├── ui/                          # 사용자 인터페이스
└── infra/                       # 인프라스트럭처
```

**역할:**
- 주문 생성, 취소, 배송 등 명령 처리
- 주문 내역 조회
- 주문 상태 관리

### 3. Catalog (상품 카탈로그) 도메인

```
catalog/
├── command/                      # 명령 처리
│   └── domain/                  # 도메인 모델
├── query/                       # 조회 처리
├── ui/                          # 사용자 인터페이스
└── NoCategoryException.java     # 도메인 예외
```

**역할:**
- 상품 등록, 수정, 카테고리 관리
- 상품 검색 및 조회
- 카탈로그 관리

### 4. Board (게시판) 도메인

```
board/
└── domain/                      # 도메인 모델
```

**역할:**
- 게시글 작성, 수정, 삭제
- 게시판 관리

### 5. Admin (관리자) 도메인

```
admin/
└── ui/                          # 관리자 인터페이스
```

**역할:**
- 주문 관리 및 처리
- 시스템 관리 기능

## 공통 패키지 구조

### 1. Common (공통)

```
common/
├── model/                       # 공통 도메인 모델
│   ├── Address.java            # 주소 값 객체
│   ├── Email.java              # 이메일 값 객체
│   ├── EmailSet.java           # 이메일 집합 값 객체
│   └── Money.java              # 금액 값 객체
├── event/                       # 이벤트 처리
│   ├── Event.java              # 이벤트 인터페이스
│   ├── Events.java             # 이벤트 컬렉션
│   ├── EventStoreHandler.java  # 이벤트 저장소 핸들러
│   └── EventsConfiguration.java # 이벤트 설정
├── jpa/                        # JPA 관련 공통 기능
│   ├── EmailSetConverter.java  # 이메일 집합 변환기
│   ├── MoneyConverter.java     # 금액 변환기
│   ├── Rangeable.java          # 범위 조회 인터페이스
│   ├── SpecBuilder.java        # 스펙 빌더
│   └── ...
├── ui/                         # 공통 UI 컴포넌트
├── ValidationError.java         # 검증 오류
├── ValidationErrorException.java # 검증 오류 예외
└── VersionConflictException.java # 버전 충돌 예외
```

**역할:**
- 모든 도메인에서 공통으로 사용되는 값 객체
- 이벤트 처리 인프라스트럭처
- JPA 관련 공통 기능
- 공통 예외 처리

### 2. EventStore (이벤트 저장소)

```
eventstore/
├── api/                        # 이벤트 저장소 API
├── infra/                      # 이벤트 저장소 구현
└── ui/                         # 이벤트 저장소 UI
```

**역할:**
- 도메인 이벤트의 영속성 관리
- 이벤트 소싱 패턴 구현
- 이벤트 히스토리 조회

### 3. Lock (분산 락)

```
lock/
├── LockManager.java            # 락 관리자 인터페이스
├── SpringLockManager.java      # Spring 기반 락 관리자
├── LockData.java               # 락 데이터
├── LockId.java                 # 락 식별자
└── ...                         # 락 관련 예외들
```

**역할:**
- 동시성 제어
- 분산 환경에서의 락 관리
- 주문 처리 시 동시 주문 방지

### 4. Integration (통합)

```
integration/
├── EventForwarder.java         # 이벤트 전달자
├── EventSender.java            # 이벤트 발송자
├── OffsetStore.java            # 오프셋 저장소
└── infra/                      # 통합 인프라스트럭처
```

**역할:**
- 외부 시스템과의 이벤트 동기화
- 메시지 브로커 연동
- 배치 처리 및 스트림 처리

### 5. SpringConfig (Spring 설정)

```
springconfig/
├── security/                   # 보안 설정
└── web/                        # 웹 설정
```

**역할:**
- Spring Security 설정
- 웹 애플리케이션 설정
- 보안 정책 적용

## DDD 패턴 적용 사항

### 1. CQRS (Command Query Responsibility Segregation)
- **Command**: `command/` 패키지에서 도메인 명령 처리
- **Query**: `query/` 패키지에서 데이터 조회 처리
- 명령과 조회의 책임을 명확히 분리

### 2. 이벤트 소싱 (Event Sourcing)
- `eventstore/` 패키지를 통한 이벤트 저장
- `common/event/` 패키지의 이벤트 처리 인프라
- 도메인 상태 변경을 이벤트로 기록

### 3. 계층화 아키텍처
- **Domain Layer**: `domain/` 패키지
- **Application Layer**: `application/` 패키지
- **Infrastructure Layer**: `infra/` 패키지
- **UI Layer**: `ui/` 패키지

### 4. 값 객체 (Value Objects)
- `common/model/` 패키지의 불변 객체들
- `Address`, `Email`, `Money` 등 도메인 개념 표현

### 5. 도메인 서비스
- 각 도메인의 `application/` 패키지
- 도메인 로직 조율 및 트랜잭션 관리

## 개발 가이드라인

### 1. 새로운 도메인 추가 시
```
newdomain/
├── command/
│   ├── domain/                 # 도메인 모델
│   └── application/            # 애플리케이션 서비스
├── query/                      # 조회 서비스
├── ui/                         # 사용자 인터페이스
└── infra/                      # 인프라스트럭처
```

### 2. 도메인 간 의존성
- 도메인 간 직접 의존성 금지
- 이벤트를 통한 느슨한 결합
- 공통 패키지 활용

### 3. 예외 처리
- 도메인별 예외는 해당 도메인 패키지에 정의
- 공통 예외는 `common` 패키지에 정의
- `ValidationErrorException` 등 공통 예외 활용

### 4. 이벤트 처리
- 도메인 이벤트는 `common/event/Event` 인터페이스 구현
- 이벤트 저장소를 통한 영속성 관리
- 이벤트 기반 비동기 처리

## 결론

이 패키지 구조는 DDD의 핵심 원칙을 잘 반영하고 있습니다:

1. **도메인 경계 명확화**: 각 도메인이 독립적인 패키지로 구성
2. **CQRS 패턴**: 명령과 조회의 명확한 분리
3. **이벤트 소싱**: 도메인 상태 변경의 이벤트 기반 추적
4. **계층화**: 도메인, 애플리케이션, 인프라스트럭처의 명확한 분리
5. **공통 인프라**: 재사용 가능한 공통 기능의 체계적 관리

이러한 구조를 통해 도메인 로직의 명확성, 코드의 유지보수성, 그리고 시스템의 확장성을 확보할 수 있습니다.

```

```java
package com.myshop.order.command.domain;

import com.myshop.common.event.Events;
import com.myshop.common.jpa.MoneyConverter;
import com.myshop.common.model.Money;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Order 도메인 모델
 * 
 * DDD에서 Order는 주문이라는 비즈니스 개념을 표현하는 애그리게이트 루트입니다.
 * 
 * 주요 특징:
 * 1. 애그리게이트 루트: 주문과 관련된 모든 엔티티를 관리
 * 2. 불변성 보장: 생성 후 주요 속성 변경 불가
 * 3. 도메인 이벤트 발행: 상태 변경 시 관련 이벤트 발행
 * 4. 비즈니스 규칙 검증: 주문 생성 및 변경 시 규칙 검증
 * 
 * JPA 매핑:
 * - 테이블명: purchase_order (도메인 모델과 테이블명이 다름)
 * - 접근 방식: 필드 접근 (AccessType.FIELD)
 * - 버전 관리: 낙관적 락을 위한 @Version 사용
 */
@Entity
@Table(name = "purchase_order")  // 도메인 모델명과 테이블명이 다른 경우
@Access(AccessType.FIELD)        // 필드 기반 접근 방식 사용
public class Order {
    
    /**
     * 주문 번호 - 애그리게이트 루트의 식별자
     * @EmbeddedId: 복합 키를 값 객체로 표현
     */
    @EmbeddedId
    private OrderNo number;

    /**
     * 버전 정보 - 낙관적 락을 위한 JPA @Version
     * 동시 수정 시 데이터 일관성 보장
     */
    @Version
    private long version;

    /**
     * 주문자 정보 - 값 객체로 표현
     * @Embedded: 복합 값 객체를 단일 컬럼으로 매핑
     */
    @Embedded
    private Orderer orderer;

    /**
     * 주문 상품 목록 - 값 객체 컬렉션
     * @ElementCollection: 값 객체 리스트를 별도 테이블로 매핑
     * @CollectionTable: 매핑할 테이블 정보 지정
     * @OrderColumn: 리스트의 순서 정보 저장
     * 
     * 도메인 모델: OrderLine 리스트 (비즈니스 개념)
     * 테이블 구조: order_line 테이블 (물리적 저장 구조)
     */
    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(name = "order_line", joinColumns = @JoinColumn(name = "order_number"))
    @OrderColumn(name = "line_idx")
    private List<OrderLine> orderLines;

    /**
     * 총 주문 금액 - Money 값 객체
     * @Convert: 커스텀 컨버터를 사용하여 Money 객체를 DB에 저장
     */
    @Convert(converter = MoneyConverter.class)
    @Column(name = "total_amounts")
    private Money totalAmounts;

    /**
     * 배송 정보 - 값 객체로 표현
     */
    @Embedded
    private ShippingInfo shippingInfo;

    /**
     * 주문 상태 - 열거형으로 표현
     * @Enumerated(EnumType.STRING): 문자열로 저장하여 가독성 향상
     */
    @Column(name = "state")
    @Enumerated(EnumType.STRING)
    private OrderState state;

    /**
     * 주문 일시 - 주문 생성 시점
     */
    @Column(name = "order_date")
    private LocalDateTime orderDate;

    /**
     * JPA를 위한 기본 생성자
     * protected로 설정하여 외부에서 직접 생성 방지
     */
    protected Order() {
    }

    /**
     * 주문 생성 생성자
     * 
     * DDD 원칙:
     * 1. 생성 시점에 모든 필수 정보 검증
     * 2. 생성 완료 후 도메인 이벤트 발행
     * 3. 불변 객체 생성 보장
     * 
     * @param number 주문 번호
     * @param orderer 주문자
     * @param orderLines 주문 상품 목록
     * @param shippingInfo 배송 정보
     * @param state 초기 주문 상태
     */
    public Order(OrderNo number, Orderer orderer, List<OrderLine> orderLines,
                 ShippingInfo shippingInfo, OrderState state) {
        setNumber(number);
        setOrderer(orderer);
        setOrderLines(orderLines);
        setShippingInfo(shippingInfo);
        this.state = state;
        this.orderDate = LocalDateTime.now();
        
        // 도메인 이벤트 발행 - 주문 생성 완료를 외부에 알림
        Events.raise(new OrderPlacedEvent(number.getNumber(), orderer, orderLines, orderDate));
    }

    /**
     * 주문 번호 설정 - 생성자에서만 호출
     * null 검증을 통한 불변성 보장
     */
    private void setNumber(OrderNo number) {
        if (number == null) throw new IllegalArgumentException("no number");
        this.number = number;
    }

    /**
     * 주문자 설정 - 생성자에서만 호출
     */
    private void setOrderer(Orderer orderer) {
        if (orderer == null) throw new IllegalArgumentException("no orderer");
        this.orderer = orderer;
    }

    /**
     * 주문 상품 목록 설정 및 총 금액 계산
     * 
     * 비즈니스 규칙:
     * 1. 최소 1개 이상의 상품이 있어야 함
     * 2. 상품 목록 변경 시 총 금액 자동 재계산
     */
    private void setOrderLines(List<OrderLine> orderLines) {
        verifyAtLeastOneOrMoreOrderLines(orderLines);
        this.orderLines = orderLines;
        calculateTotalAmounts();
    }

    /**
     * 주문 상품 목록 검증 - 비즈니스 규칙
     */
    private void verifyAtLeastOneOrMoreOrderLines(List<OrderLine> orderLines) {
        if (orderLines == null || orderLines.isEmpty()) {
            throw new IllegalArgumentException("no OrderLine");
        }
    }

    /**
     * 총 주문 금액 계산 - 도메인 로직
     * 주문 상품들의 금액을 합산하여 계산
     */
    private void calculateTotalAmounts() {
        this.totalAmounts = new Money(orderLines.stream()
                .mapToInt(x -> x.getAmounts().getValue()).sum());
    }

    /**
     * 배송 정보 설정
     */
    private void setShippingInfo(ShippingInfo shippingInfo) {
        if (shippingInfo == null) throw new IllegalArgumentException("no shipping info");
        this.shippingInfo = shippingInfo;
    }

    // Getter 메서드들 - 도메인 모델의 상태 조회

    public OrderNo getNumber() {
        return number;
    }

    public long getVersion() {
        return version;
    }

    public Orderer getOrderer() {
        return orderer;
    }

    public Money getTotalAmounts() {
        return totalAmounts;
    }

    public ShippingInfo getShippingInfo() {
        return shippingInfo;
    }

    public OrderState getState() {
        return state;
    }

    /**
     * 배송 정보 변경
     * 
     * 비즈니스 규칙:
     * 1. 아직 배송되지 않은 주문만 변경 가능
     * 2. 변경 완료 후 도메인 이벤트 발행
     * 
     * @param newShippingInfo 새로운 배송 정보
     */
    public void changeShippingInfo(ShippingInfo newShippingInfo) {
        verifyNotYetShipped();
        setShippingInfo(newShippingInfo);
        Events.raise(new ShippingInfoChangedEvent(number, newShippingInfo));
    }

    /**
     * 주문 취소
     * 
     * 비즈니스 규칙:
     * 1. 아직 배송되지 않은 주문만 취소 가능
     * 2. 취소 완료 후 도메인 이벤트 발행
     */
    public void cancel() {
        verifyNotYetShipped();
        this.state = OrderState.CANCELED;
        Events.raise(new OrderCanceledEvent(number.getNumber()));
    }

    /**
     * 배송 전 상태 검증
     * @throws AlreadyShippedException 이미 배송된 경우
     */
    private void verifyNotYetShipped() {
        if (!isNotYetShipped())
            throw new AlreadyShippedException();
    }

    /**
     * 아직 배송되지 않은 상태인지 확인
     * @return true: 배송 전, false: 배송 완료
     */
    public boolean isNotYetShipped() {
        return state == OrderState.PAYMENT_WAITING || state == OrderState.PREPARING;
    }

    public List<OrderLine> getOrderLines() {
        return orderLines;
    }

    /**
     * 버전 일치 여부 확인 - 낙관적 락 검증
     * @param version 비교할 버전
     * @return true: 일치, false: 불일치
     */
    public boolean matchVersion(long version) {
        return this.version == version;
    }

    /**
     * 배송 시작
     * 
     * 비즈니스 규칙:
     * 1. 배송 가능한 상태여야 함
     * 2. 배송 시작 후 도메인 이벤트 발행
     */
    public void startShipping() {
        verifyShippableState();
        this.state = OrderState.SHIPPED;
        Events.raise(new ShippingStartedEvent(number.getNumber()));
    }

    /**
     * 배송 가능 상태 검증
     */
    private void verifyShippableState() {
        verifyNotYetShipped();
        verifyNotCanceled();
    }

    /**
     * 취소되지 않은 상태 검증
     * @throws OrderAlreadyCanceledException 이미 취소된 경우
     */
    private void verifyNotCanceled() {
        if (state == OrderState.CANCELED) {
            throw new OrderAlreadyCanceledException();
        }
    }
}

```

```java
# MyBatis를 사용한 도메인 모델과 테이블 객체 매핑 예시

## 개요

MyBatis는 SQL 중심의 ORM 프레임워크로, JPA와 달리 SQL을 직접 작성하여 도메인 모델과 테이블 간의 매핑을 처리합니다. 이를 통해 더 세밀한 제어와 성능 최적화가 가능합니다.

## 1. 기본 매핑 구조

### 1.1 도메인 모델
```java
// Order 도메인 모델
public class Order {
    private OrderNo number;           // 복합 키
    private Orderer orderer;          // 주문자 정보
    private List<OrderLine> orderLines; // 주문 상품 목록
    private Money totalAmounts;       // 총 금액
    private OrderState state;         // 주문 상태
    private LocalDateTime orderDate;  // 주문 일시
    private long version;             // 버전 정보
    
    // 생성자, 메서드들...
}

// OrderNo 값 객체
public class OrderNo {
    private final String number;
    private final String type;
    
    public OrderNo(String number, String type) {
        this.number = number;
        this.type = type;
    }
    
    // getter 메서드들...
}

// Orderer 값 객체
public class Orderer {
    private final MemberId memberId;
    private final Name name;
    private final Email email;
    
    // 생성자, getter 메서드들...
}

// Money 값 객체
public class Money {
    private final int value;
    private final Currency currency;
    
    public Money(int value) {
        this.value = value;
        this.currency = Currency.KRW;
    }
    
    // getter 메서드들...
}
```

### 1.2 테이블 구조
```sql
-- 주문 테이블
CREATE TABLE purchase_order (
    order_number VARCHAR(50) NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    member_id VARCHAR(50) NOT NULL,
    member_name VARCHAR(100) NOT NULL,
    member_email VARCHAR(200) NOT NULL,
    total_amounts INT NOT NULL,
    state VARCHAR(20) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    version BIGINT NOT NULL,
    PRIMARY KEY (order_number, order_type)
);

-- 주문 상품 테이블
CREATE TABLE order_line (
    order_number VARCHAR(50) NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    line_idx INTEGER NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (order_number, order_type, line_idx),
    FOREIGN KEY (order_number, order_type) REFERENCES purchase_order(order_number, order_type)
);
```

## 2. MyBatis 매퍼 인터페이스

### 2.1 OrderMapper 인터페이스
```java
public interface OrderMapper {
    
    /**
     * 주문 저장
     */
    void insertOrder(Order order);
    
    /**
     * 주문 상품 저장
     */
    void insertOrderLines(Order order);
    
    /**
     * 주문 조회
     */
    Order selectOrder(OrderNo orderNo);
    
    /**
     * 주문 상품 목록 조회
     */
    List<OrderLine> selectOrderLines(OrderNo orderNo);
    
    /**
     * 주문 상태 업데이트
     */
    void updateOrderState(@Param("orderNo") OrderNo orderNo, 
                         @Param("state") OrderState state,
                         @Param("version") long version);
    
    /**
     * 배송 정보 업데이트
     */
    void updateShippingInfo(@Param("orderNo") OrderNo orderNo,
                           @Param("shippingInfo") ShippingInfo shippingInfo,
                           @Param("version") long version);
}
```

## 3. MyBatis XML 매퍼

### 3.1 OrderMapper.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.myshop.order.infra.persistence.OrderMapper">
    
    <!-- 결과 맵 정의 -->
    <resultMap id="OrderResultMap" type="com.myshop.order.command.domain.Order">
        <!-- 복합 키 매핑 -->
        <id property="number" column="order_number" javaType="com.myshop.order.command.domain.OrderNo">
            <result property="number" column="order_number"/>
            <result property="type" column="order_type"/>
        </id>
        
        <!-- 값 객체 매핑 -->
        <association property="orderer" javaType="com.myshop.order.command.domain.Orderer">
            <constructor>
                <arg column="member_id" javaType="com.myshop.member.command.domain.MemberId"/>
                <arg column="member_name" javaType="com.myshop.common.model.Name"/>
                <arg column="member_email" javaType="com.myshop.common.model.Email"/>
            </constructor>
        </association>
        
        <!-- Money 값 객체 매핑 -->
        <association property="totalAmounts" javaType="com.myshop.common.model.Money">
            <constructor>
                <arg column="total_amounts" javaType="int"/>
            </constructor>
        </association>
        
        <!-- 기본 필드 매핑 -->
        <result property="state" column="state" 
                javaType="com.myshop.order.command.domain.OrderState"/>
        <result property="orderDate" column="order_date" 
                javaType="java.time.LocalDateTime"/>
        <result property="version" column="version" javaType="long"/>
    </resultMap>
    
    <!-- OrderLine 결과 맵 -->
    <resultMap id="OrderLineResultMap" type="com.myshop.order.command.domain.OrderLine">
        <constructor>
            <arg column="product_id" javaType="com.myshop.catalog.command.domain.ProductId"/>
            <arg column="quantity" javaType="int"/>
            <arg column="price" javaType="com.myshop.common.model.Money"/>
        </constructor>
    </resultMap>
    
    <!-- 주문 저장 -->
    <insert id="insertOrder" parameterType="com.myshop.order.command.domain.Order">
        INSERT INTO purchase_order (
            order_number, order_type, 
            member_id, member_name, member_email,
            total_amounts, state, order_date, version
        ) VALUES (
            #{number.number}, #{number.type},
            #{orderer.memberId.value}, #{orderer.name.value}, #{orderer.email.value},
            #{totalAmounts.value}, #{state}, #{orderDate}, #{version}
        )
    </insert>
    
    <!-- 주문 상품 저장 -->
    <insert id="insertOrderLines" parameterType="com.myshop.order.command.domain.Order">
        INSERT INTO order_line (
            order_number, order_type, line_idx, 
            product_id, quantity, price
        ) VALUES 
        <foreach collection="orderLines" item="line" index="index" separator=",">
            (
                #{number.number}, #{number.type}, #{index},
                #{line.productId.value}, #{line.quantity}, #{line.amounts.value}
            )
        </foreach>
    </insert>
    
    <!-- 주문 조회 -->
    <select id="selectOrder" resultMap="OrderResultMap">
        SELECT 
            order_number, order_type,
            member_id, member_name, member_email,
            total_amounts, state, order_date, version
        FROM purchase_order 
        WHERE order_number = #{number.number} AND order_type = #{number.type}
    </select>
    
    <!-- 주문 상품 목록 조회 -->
    <select id="selectOrderLines" resultMap="OrderLineResultMap">
        SELECT 
            product_id, quantity, price
        FROM order_line 
        WHERE order_number = #{number.number} AND order_type = #{number.type}
        ORDER BY line_idx
    </select>
    
    <!-- 주문 상태 업데이트 (낙관적 락) -->
    <update id="updateOrderState">
        UPDATE purchase_order 
        SET state = #{state}, version = version + 1
        WHERE order_number = #{orderNo.number} 
          AND order_type = #{orderNo.type}
          AND version = #{version}
    </update>
    
    <!-- 배송 정보 업데이트 -->
    <update id="updateShippingInfo">
        UPDATE purchase_order 
        SET 
            shipping_address = #{shippingInfo.address.value},
            shipping_message = #{shippingInfo.message.value},
            version = version + 1
        WHERE order_number = #{orderNo.number} 
          AND order_type = #{orderNo.type}
          AND version = #{version}
    </update>
    
</mapper>
```

## 4. 복잡한 쿼리 예시

### 4.1 동적 쿼리를 사용한 주문 검색
```xml
<!-- OrderQueryMapper.xml -->
<mapper namespace="com.myshop.order.query.OrderQueryMapper">
    
    <!-- 주문 검색 결과 맵 -->
    <resultMap id="OrderSummaryResultMap" type="com.myshop.order.query.OrderSummary">
        <id property="orderNumber" column="order_number"/>
        <result property="ordererName" column="member_name"/>
        <result property="totalAmount" column="total_amounts"/>
        <result property="state" column="state"/>
        <result property="orderDate" column="order_date"/>
    </resultMap>
    
    <!-- 동적 쿼리를 사용한 주문 검색 -->
    <select id="searchOrders" resultMap="OrderSummaryResultMap">
        SELECT 
            order_number, member_name, total_amounts, state, order_date
        FROM purchase_order po
        <where>
            <if test="ordererId != null">
                AND po.member_id = #{ordererId}
            </if>
            <if test="state != null">
                AND po.state = #{state}
            </if>
            <if test="startDate != null">
                AND po.order_date >= #{startDate}
            </if>
            <if test="endDate != null">
                AND po.order_date &lt;= #{endDate}
            </if>
            <if test="minAmount != null">
                AND po.total_amounts >= #{minAmount}
            </if>
            <if test="maxAmount != null">
                AND po.total_amounts &lt;= #{maxAmount}
            </if>
        </where>
        ORDER BY po.order_date DESC
        <if test="limit != null">
            LIMIT #{limit}
        </if>
    </select>
    
    <!-- 주문 통계 조회 -->
    <select id="getOrderStatistics" resultType="com.myshop.order.query.OrderStatistics">
        SELECT 
            COUNT(*) as totalOrders,
            SUM(total_amounts) as totalAmount,
            AVG(total_amounts) as averageAmount,
            COUNT(CASE WHEN state = 'PAYMENT_WAITING' THEN 1 END) as waitingPayment,
            COUNT(CASE WHEN state = 'PREPARING' THEN 1 END) as preparing,
            COUNT(CASE WHEN state = 'SHIPPED' THEN 1 END) as shipped,
            COUNT(CASE WHEN state = 'CANCELED' THEN 1 END) as canceled
        FROM purchase_order
        <where>
            <if test="startDate != null">
                AND order_date >= #{startDate}
            </if>
            <if test="endDate != null">
                AND order_date &lt;= #{endDate}
            </if>
        </where>
    </select>
    
</mapper>
```

## 5. 값 객체 변환기 (TypeHandler)

### 5.1 Money TypeHandler
```java
public class MoneyTypeHandler extends BaseTypeHandler<Money> {
    
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, Money parameter, JdbcType jdbcType) 
            throws SQLException {
        ps.setInt(i, parameter.getValue());
    }
    
    @Override
    public Money getNullableResult(ResultSet rs, String columnName) throws SQLException {
        Integer value = rs.getInt(columnName);
        return value != null ? new Money(value) : null;
    }
    
    @Override
    public Money getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        Integer value = rs.getInt(columnIndex);
        return value != null ? new Money(value) : null;
    }
    
    @Override
    public Money getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        Integer value = cs.getInt(columnIndex);
        return value != null ? new Money(value) : null;
    }
}
```

### 5.2 OrderState TypeHandler
```java
public class OrderStateTypeHandler extends BaseTypeHandler<OrderState> {
    
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, OrderState parameter, JdbcType jdbcType) 
            throws SQLException {
        ps.setString(i, parameter.name());
    }
    
    @Override
    public OrderState getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String value = rs.getString(columnName);
        return value != null ? OrderState.valueOf(value) : null;
    }
    
    @Override
    public OrderState getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        String value = rs.getString(columnIndex);
        return value != null ? OrderState.valueOf(value) : null;
    }
    
    @Override
    public OrderState getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        String value = cs.getString(columnIndex);
        return value != null ? OrderState.valueOf(value) : null;
    }
}
```

## 6. MyBatis 설정

### 6.1 MyBatis 설정 파일
```xml
<!-- mybatis-config.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    
    <!-- 타입 별칭 설정 -->
    <typeAliases>
        <typeAlias alias="Order" type="com.myshop.order.command.domain.Order"/>
        <typeAlias alias="OrderLine" type="com.myshop.order.command.domain.OrderLine"/>
        <typeAlias alias="OrderState" type="com.myshop.order.command.domain.OrderState"/>
        <typeAlias alias="Money" type="com.myshop.common.model.Money"/>
    </typeAliases>
    
    <!-- 타입 핸들러 설정 -->
    <typeHandlers>
        <typeHandler handler="com.myshop.common.mybatis.MoneyTypeHandler"/>
        <typeHandler handler="com.myshop.order.infra.persistence.OrderStateTypeHandler"/>
    </typeHandlers>
    
    <!-- 환경 설정 -->
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/myshop"/>
                <property name="username" value="root"/>
                <property name="password" value="password"/>
            </dataSource>
        </environment>
    </environments>
    
    <!-- 매퍼 설정 -->
    <mappers>
        <mapper resource="mapper/OrderMapper.xml"/>
        <mapper resource="mapper/OrderQueryMapper.xml"/>
    </mappers>
    
</configuration>
```

## 7. 서비스 레이어에서의 사용

### 7.1 OrderRepository 구현
```java
@Repository
public class OrderRepository {
    
    private final OrderMapper orderMapper;
    private final OrderQueryMapper orderQueryMapper;
    
    public OrderRepository(OrderMapper orderMapper, OrderQueryMapper orderQueryMapper) {
        this.orderMapper = orderMapper;
        this.orderQueryMapper = orderQueryMapper;
    }
    
    /**
     * 주문 저장
     */
    public void save(Order order) {
        orderMapper.insertOrder(order);
        orderMapper.insertOrderLines(order);
    }
    
    /**
     * 주문 조회
     */
    public Order findById(OrderNo orderNo) {
        Order order = orderMapper.selectOrder(orderNo);
        if (order != null) {
            List<OrderLine> orderLines = orderMapper.selectOrderLines(orderNo);
            // OrderLine을 Order에 설정하는 로직 필요
        }
        return order;
    }
    
    /**
     * 주문 상태 업데이트
     */
    public boolean updateState(OrderNo orderNo, OrderState newState, long version) {
        int updatedRows = orderMapper.updateOrderState(orderNo, newState, version);
        return updatedRows > 0;
    }
    
    /**
     * 주문 검색
     */
    public List<OrderSummary> searchOrders(OrderSearchCriteria criteria) {
        return orderQueryMapper.searchOrders(criteria);
    }
}
```

## 8. JPA vs MyBatis 비교

### 8.1 JPA 방식
```java
// JPA: 자동 매핑, 객체 중심
@Entity
@Table(name = "purchase_order")
public class Order {
    @EmbeddedId
    private OrderNo number;
    
    @Embedded
    private Orderer orderer;
    
    @ElementCollection
    private List<OrderLine> orderLines;
}

// 사용: 간단한 저장/조회
orderRepository.save(order);
Order found = orderRepository.findById(orderNo);
```

### 8.2 MyBatis 방식
```java
// MyBatis: SQL 중심, 세밀한 제어
public interface OrderMapper {
    void insertOrder(Order order);
    Order selectOrder(OrderNo orderNo);
}

// 사용: SQL 직접 제어
orderMapper.insertOrder(order);
Order found = orderMapper.selectOrder(orderNo);
```

## 9. 장단점 분석

### 9.1 MyBatis 장점
- **SQL 제어**: 복잡한 쿼리와 성능 최적화 가능
- **유연성**: 도메인 모델과 테이블 구조의 자유로운 매핑
- **성능**: N+1 문제 등 JPA의 성능 이슈 회피
- **학습 곡선**: SQL 지식만 있으면 사용 가능

### 9.2 MyBatis 단점
- **복잡성**: 매핑 설정과 SQL 관리의 복잡성
- **보일러플레이트**: 반복적인 CRUD 코드 작성 필요
- **타입 안전성**: 컴파일 타임 타입 검증 부족
- **유지보수**: SQL 변경 시 여러 파일 수정 필요

## 10. 사용 가이드라인

### 10.1 MyBatis 사용 시기
1. **복잡한 쿼리**: 다중 테이블 조인, 서브쿼리 등
2. **성능 최적화**: 인덱스 활용, 쿼리 튜닝 필요
3. **레거시 시스템**: 기존 SQL 활용 필요
4. **팀 역량**: SQL 전문성 보유

### 10.2 JPA 사용 시기
1. **단순한 CRUD**: 기본적인 데이터 조작
2. **빠른 개발**: 프로토타입 및 초기 개발
3. **도메인 중심**: 비즈니스 로직 중심 설계
4. **팀 역량**: 객체지향 설계 역량 보유

## 결론

MyBatis는 SQL 중심의 접근 방식으로 도메인 모델과 테이블 간의 복잡한 매핑을 처리할 수 있습니다. 특히:

1. **복잡한 쿼리 처리**: 동적 쿼리, 복합 조인 등
2. **성능 최적화**: SQL 레벨에서의 세밀한 제어
3. **유연한 매핑**: 도메인 모델과 테이블 구조의 자유로운 연결

하지만 이는 더 많은 설정과 SQL 관리 작업을 요구하므로, 프로젝트의 요구사항과 팀의 역량을 고려하여 선택해야 합니다.

```