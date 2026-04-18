# 아키텍처 패턴 비교 분석

실습 완료 후 각 패턴의 장단점을 직접 평가하세요.

---

## 비교 대상

| 패턴 | 설명 |
|------|------|
| **계층형 (Layered)** | Controller → Service → Repository |
| **Modulith + Activity** | Module → Facade → Activity → Repository |
| **Clean Architecture** | Controller → UseCase → Entity → Gateway |

---

## 1. 계층형 아키텍처 (기존 방식)

### 구조

```
com.example/
├── controller/
│   ├── OrderController.java
│   └── PaymentController.java
├── service/
│   ├── OrderService.java
│   └── PaymentService.java
├── repository/
│   ├── OrderRepository.java
│   └── PaymentRepository.java
└── domain/
    ├── Order.java
    └── Payment.java
```

### 특징

```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;  // 직접 의존
    private final UserService userService;        // 직접 의존

    public Order createOrder(OrderRequest req) {
        // 모든 로직이 한 메서드에
        User user = userService.findById(req.getUserId());
        Order order = new Order(user, req.getItems());
        orderRepository.save(order);
        paymentService.process(order);  // 강한 결합
        return order;
    }
}
```

### 평가 체크리스트

실습 후 직접 평가하세요:

| 항목 | 점수 (1-5) | 메모 |
|------|-----------|------|
| 이해 용이성 | ☐ | |
| 새 기능 추가 편의성 | ☐ | |
| 테스트 작성 용이성 | ☐ | |
| 모듈 경계 명확성 | ☐ | |
| 의존성 관리 | ☐ | |
| 코드 재사용성 | ☐ | |

---

## 2. Modulith + Activity 패턴

### 구조

```
com.example/
├── order/
│   ├── Order.java              # 공개
│   ├── OrderService.java       # Facade
│   ├── OrderCreated.java       # 이벤트
│   └── internal/
│       ├── CreateOrderActivity.java
│       ├── OrderRepository.java
│       └── OrderValidator.java
└── payment/
    ├── PaymentService.java
    └── internal/
        └── PaymentEventHandler.java  # 이벤트 구독
```

### 특징

```java
// Facade - 단순 라우팅
@Service
public class OrderService {
    private final CreateOrderActivity createOrder;

    public Order create(OrderRequest req) {
        return createOrder.execute(req);  // 위임만
    }
}

// Activity - 실제 로직
@Service
class CreateOrderActivity {
    private final OrderRepository repository;
    private final ApplicationEventPublisher events;

    @Transactional
    Order execute(OrderRequest req) {
        Order order = Order.create(req);
        repository.save(order);
        events.publishEvent(new OrderCreated(order.getId()));
        return order;
    }
}

// 다른 모듈 - 이벤트 구독
@Service
class PaymentEventHandler {
    @ApplicationModuleListener
    void on(OrderCreated event) {
        // 결제 처리 (느슨한 결합)
    }
}
```

### 평가 체크리스트

실습 후 직접 평가하세요:

| 항목 | 점수 (1-5) | 메모 |
|------|-----------|------|
| 이해 용이성 | ☐ | |
| 새 기능 추가 편의성 | ☐ | |
| 테스트 작성 용이성 | ☐ | |
| 모듈 경계 명확성 | ☐ | |
| 의존성 관리 | ☐ | |
| 코드 재사용성 | ☐ | |

---

## 3. 직접 비교 분석

### 파일 수 비교

| 기능 | 계층형 | Modulith |
|------|--------|----------|
| 주문 생성 | ~3개 | ~5개 |
| 주문 취소 추가 | +1 메서드 | +1 Activity |
| 결제 연동 | 직접 의존 | 이벤트 핸들러 |

**직접 계산해보세요**:
- 계층형 총 파일 수: ___개
- Modulith 총 파일 수: ___개

---

### 의존성 방향

**계층형**:
```
Order ──────► Payment ──────► User
  │              │
  └──────────────┴────► Repository
```

**Modulith**:
```
Order ─── Event ───► Payment
  │                    │
  ▼                    ▼
Repository          Repository
(isolated)          (isolated)
```

---

### 변경 영향 범위

**시나리오**: Payment 로직 변경 시

| 패턴 | 영향 범위 |
|------|----------|
| 계층형 | OrderService, PaymentService, 관련 테스트 전체 |
| Modulith | PaymentEventHandler만 (Order 모듈 무관) |

**직접 실험**: 실습 코드에서 Payment 로직을 변경하고 영향 범위를 확인하세요.

---

## 4. 장단점 정리

### 계층형 아키텍처

| 장점 | 단점 |
|------|------|
| 직관적, 학습 곡선 낮음 | 모듈 경계 불명확 |
| 파일 수 적음 | Service 비대화 |
| 설정 간단 | 테스트 시 많은 Mock 필요 |
| | 순환 의존성 발생 쉬움 |

### Modulith + Activity

| 장점 | 단점 |
|------|------|
| 명확한 모듈 경계 | 초기 설정 복잡 |
| 느슨한 결합 (이벤트) | 파일 수 증가 |
| Activity 단위 테스트 용이 | 학습 곡선 있음 |
| MSA 전환 용이 | 이벤트 추적 어려움 |
| 강제되는 아키텍처 규칙 | 디버깅 복잡도 증가 |

---

## 5. 적용 판단 기준

### Modulith가 적합한 경우

- [ ] 팀 규모 3명 이상, 도메인별 분리 필요
- [ ] 모놀리스 → MSA 점진적 전환 계획
- [ ] 명확한 도메인 경계가 존재
- [ ] 장기 유지보수 예상

### 계층형이 적합한 경우

- [ ] 소규모 프로젝트, 빠른 MVP
- [ ] 1-2명 개발, 도메인 단순
- [ ] MSA 전환 계획 없음
- [ ] 팀 학습 비용 최소화 필요

---

## 6. 실습 후 결론

직접 작성하세요:

### 내가 느낀 장점

```
1.
2.
3.
```

### 내가 느낀 단점

```
1.
2.
3.
```

### 실무 적용 여부

```
적용하겠다 / 적용하지 않겠다

이유:


```

### 추가 학습이 필요한 부분

```
1.
2.
```

---

## 참고: 더 깊이 학습하려면

| 주제 | 키워드 |
|------|--------|
| 이벤트 소싱 | Event Sourcing, CQRS |
| 헥사고날 아키텍처 | Ports & Adapters |
| DDD | Bounded Context, Aggregate |
| MSA 전환 | Strangler Fig Pattern |
