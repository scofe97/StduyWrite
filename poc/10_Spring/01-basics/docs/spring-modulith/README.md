# Spring Modulith 학습 가이드

## 학습 목표

1. Spring Modulith의 핵심 개념 이해
2. Internal Service (Activity) 패턴 구현
3. 기존 계층형 아키텍처와 비교 분석

---

## 1. Spring Modulith란?

**모놀리식 애플리케이션 내에서 논리적 모듈 경계를 정의하고 강제하는 프레임워크**

### 핵심 가치

```
Monolith ──────────────────────────────────► Microservices
           │                           │
           │     Spring Modulith       │
           │    (중간 단계, 점진적)      │
           └───────────────────────────┘
```

- MSA의 **장점** (명확한 경계, 느슨한 결합)
- Monolith의 **장점** (단순한 배포, 낮은 운영 비용)

### 기존 방식의 문제

```java
// ❌ 기존: 패키지 간 무분별한 참조
com.example.order.OrderService
    → com.example.payment.internal.PaymentValidator  // 내부 클래스 직접 참조
    → com.example.user.repository.UserRepository     // 리포지토리 직접 참조
```

```java
// ✅ Modulith: 공개 API만 참조
com.example.order.OrderService
    → com.example.payment.PaymentService  // 공개 API만
    → com.example.user.UserService        // 공개 API만
```

---

## 2. 모듈 구조

### 패키지 = 모듈

```
com.example.app/
│
├── order/                      # Order 모듈
│   ├── OrderService.java       # ✅ 공개 API
│   ├── Order.java              # ✅ 공개 도메인
│   ├── OrderCreated.java       # ✅ 공개 이벤트
│   └── internal/               # ❌ 외부 접근 불가
│       ├── CreateOrderActivity.java
│       ├── OrderRepository.java
│       └── OrderValidator.java
│
├── payment/                    # Payment 모듈
│   ├── PaymentService.java
│   └── internal/
│       └── ...
│
└── Application.java
```

### 접근 규칙

| 위치 | 다른 모듈에서 접근 |
|------|-------------------|
| 모듈 루트 (`order/`) | ✅ 가능 |
| internal 패키지 | ❌ 불가 |

---

## 3. Internal Service (Activity) 패턴

### 왜 Activity라고 부르는가?

- **Activity** = 하나의 비즈니스 액션/유스케이스
- 각 Activity는 **단일 책임**을 가짐
- Facade(공개 Service)가 Activity를 조합

### 구조

```
┌─────────────────────────────────────────────┐
│                  Module                      │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │         OrderService (Facade)        │   │  ← 외부 공개
│  │  - create(), cancel(), update()      │   │
│  └──────────────┬──────────────────────┘   │
│                 │                           │
│        ┌────────┼────────┐                 │
│        ▼        ▼        ▼                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Create   │ │ Cancel   │ │ Update   │   │  ← internal
│  │ Order    │ │ Order    │ │ Order    │   │
│  │ Activity │ │ Activity │ │ Activity │   │
│  └──────────┘ └──────────┘ └──────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Facade vs Activity 역할

| 구분 | Facade (OrderService) | Activity (CreateOrderActivity) |
|------|----------------------|-------------------------------|
| 위치 | 모듈 루트 | internal 패키지 |
| 역할 | 진입점, 라우팅 | 실제 비즈니스 로직 |
| 복잡도 | 단순 위임 | 복잡한 로직 |
| 트랜잭션 | 선택적 | 주로 여기서 관리 |
| 테스트 | 통합 테스트 | 단위 테스트 |

---

## 4. 이벤트 기반 모듈 간 통신

### 강한 결합 (❌ 피해야 함)

```java
// Order 모듈이 Payment 모듈 내부를 직접 호출
@Service
public class OrderService {
    private final PaymentProcessor processor;  // Payment internal 클래스

    public void complete(Order order) {
        processor.process(order);  // 직접 호출 = 강한 결합
    }
}
```

### 이벤트 기반 (✅ 권장)

```java
// Order 모듈: 이벤트 발행
@Service
public class OrderService {
    private final ApplicationEventPublisher events;

    public void complete(Order order) {
        // 비즈니스 로직 수행
        events.publishEvent(new OrderCompleted(order.getId()));
    }
}

// Payment 모듈: 이벤트 수신
@Service
public class PaymentEventHandler {

    @ApplicationModuleListener
    public void on(OrderCompleted event) {
        // 결제 처리
    }
}
```

### 이벤트 흐름

```
Order 모듈                     Payment 모듈
    │                              │
    │  OrderCompleted 이벤트        │
    ├─────────────────────────────►│
    │                              │
    │         (느슨한 결합)          │
```

---

## 5. 모듈 검증

### 아키텍처 테스트

```java
@Test
void 모듈_구조_검증() {
    ApplicationModules modules = ApplicationModules.of(Application.class);
    modules.verify();  // 위반 시 테스트 실패
}
```

### 검증 항목

- internal 패키지 외부 참조 여부
- 순환 의존성 존재 여부
- 모듈 간 허용되지 않은 의존성

---

## 6. 의존성 설정

### build.gradle

```groovy
dependencies {
    // Spring Modulith
    implementation 'org.springframework.modulith:spring-modulith-starter-core'

    // 테스트
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test'

    // 문서화 (선택)
    testImplementation 'org.springframework.modulith:spring-modulith-docs'
}

dependencyManagement {
    imports {
        mavenBom 'org.springframework.modulith:spring-modulith-bom:1.3.1'
    }
}
```

---

## 다음 단계

1. **[EXERCISES.md](./EXERCISES.md)** - 실습 과제
2. **[COMPARISON.md](./COMPARISON.md)** - 장단점 비교

---

## 참고 자료

- [Spring Modulith 공식 문서](https://docs.spring.io/spring-modulith/reference/)
- [Spring Modulith GitHub](https://github.com/spring-projects/spring-modulith)
- [코딩하는오후 - Spring Modulith 리팩토링](https://www.youtube.com/@codingpm)
