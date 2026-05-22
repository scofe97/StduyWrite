# [이벤트 리스너] 1. TransactionEventListener vs EventListener

주제: 분산 시스템

- 참고
    
    https://github.com/spring-projects/spring-framework/blob/main/spring-tx/src/main/java/org/springframework/transaction/support/TransactionSynchronization.java
    
    https://github.com/spring-projects/spring-framework/blob/main/spring-tx/src/main/java/org/springframework/transaction/event/TransactionalApplicationListenerSynchronization.java
    

# 이벤트 기반 아키텍쳐

이벤트는 시스템에서 발생한 의미 있는 상태 변화를 나타냅니다.

```tsx
// 이벤트 클래스
public class UserCreatedEvent {
    private final User user;

    public UserCreatedEvent(User user) {
        this.user = user;
    }
}
```

```tsx
// 이벤트 발행 (Publisher)
@Service
public class UserService {
    private final ApplicationEventPublisher eventPublisher;

    public User createUser(String name) {
        User user = userRepository.save(new User(name));
        eventPublisher.publishEvent(new UserCreatedEvent(user));
        return user;
    }
}

// 이벤트 리스닝 (Listener)
@Component
public class UserEventListener {
    @EventListener
    public void handleUserCreated(UserCreatedEvent event) {
        System.out.println("User created: " + event.getUser().getName());
    }
}
```

# 리스너 종류

---

| **항목** | **@EventListener** | **@TransactionalEventListener** |
| --- | --- | --- |
| **실행 시점** | 이벤트 발행 즉시 | 트랜잭션 Phase에 따라 |
| **트랜잭션 컨텍스트** | 발행자와 동일 | 독립적 |
| **롤백 영향** | 이미 실행됨 | Phase에 따라 다름 |
| **주요 사용 사례** | 로깅, 모니터링 | 외부 API, 이메일 전송 |

## @EventListner

- 이벤트가 발행되는 즉시 동기적으로 실행됩니다.
- 트랜잭션과 무관하게 실행되며, 발행지와 동일한 트랜잭션 컨텍스트에서 실행

```tsx
@EventListener
public void handleEvent(UserCreatedEvent event) {
    // 이벤트 발행 즉시 실행
    // 트랜잭션이 커밋되기 전에 실행됨
    // 트랜잭션이 롤백되어도 이미 실행된 상태
}
```

```tsx
Service.createUser()
  ├─ userRepository.save()
  ├─ eventPublisher.publishEvent()  ← 이벤트 발행
  │   └─ @EventListener 실행 ★      ← 즉시 실행 (트랜잭션 내부)
  └─ 트랜잭션 커밋
```

### 사용 사례

- 즉시 실행이 필요한 로직
- 트랜잭션 커밋 여부와 무관한 로직

## @TranscationEventListener

- 트랜잭션 특정 Phase에서 실행하며, 트랜잭션 상태에 따라 조건부로 실행됩니다.
- 발행자 트랜잭션과 독립적으로 실행 가능합니다.

```tsx
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void handleEvent(UserCreatedEvent event) {
    // 트랜잭션이 성공적으로 커밋된 후에 실행
    // 외부 API 호출, 이메일 전송 등에 안전
}
```

```tsx
Service.createUser()
  ├─ userRepository.save()
  ├─ eventPublisher.publishEvent()  ← 이벤트 발행
  │   (리스너는 아직 실행되지 않음)
  └─ 트랜잭션 커밋
      └─ @TransactionalEventListener 실행 ★  ← 커밋 후 실행
```

### 사용 사례

- 트랜잭션 커밋 후에만 실행해야 하는 로직
- 외부 시스템 연동(이메일, 알림 전송, API 호출)

# TranscationEventListenr 종류 및 실행 순서

```tsx
1. Service 메서드 시작
2. DB 작업 (save/update/delete)
3. eventPublisher.publishEvent()
   └─ @EventListener 실행 ★ (즉시)
   
4. @TransactionalEventListener(BEFORE_COMMIT) 실행 ★
5. 트랜잭션 커밋
6. @TransactionalEventListener(AFTER_COMMIT) 실행 ★
7. @TransactionalEventListener(AFTER_COMPLETION) 실행 ★
```

```tsx
1. Service 메서드 시작
2. DB 작업 (save/update/delete)
3. eventPublisher.publishEvent()
   └─ @EventListener 실행 ★ (즉시)
4. 예외 발생
5. 트랜잭션 롤백
6. @TransactionalEventListener(AFTER_ROLLBACK) 실행 ★
7. @TransactionalEventListener(AFTER_COMPLETION) 실행 ★
```

## BEFORE_COMMIT

```tsx
@TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
public void beforeCommit(UserCreatedEvent event) {
    // 트랜잭션 커밋 직전에 실행
    // 아직 트랜잭션이 활성화된 상태
}
```

- 트랜잭션이 커밋되기 직전에 실행하며, 트랜잭션이 아직 활성화된 상태입니다.
- DB 변경사항이 아직 커밋되지 않아, eventListener에서 예외발생 시 전체 트랜잭션이 롤백됩니다.

## AFTER_COMMIT(기본 값)

```tsx
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void afterCommit(UserCreatedEvent event) {
    // 트랜잭션 커밋 후 실행
    // 데이터가 안전하게 저장된 상태
}
```

- 트랜잭션이 성공적으로 커밋된 후 실행됩니다.
- eventListener를 호출한 트랜잭션은 이미 종료된 상태이며, DB에 반영된 상태입니다.
- eventListerner에서 예외가 발생해도 트랜잭션에는 영향이 없습니다.

## AFTER_ROLLBACK

```tsx
@TransactionalEventListener(phase = TransactionPhase.AFTER_ROLLBACK)
public void afterRollback(UserCreatedEvent event) {
    // 트랜잭션 롤백 후 실행
    // 보상 트랜잭션 또는 에러 처리
}
```

- 트랜잭션이 롤백된 후 실행되며, DB 변경사항이 모두 취소된 상태에서 발동하빈다.
- 예외 발생 시 보상 로직 실행을 위해 사용됩니다.

## AFTER_COMPLETION

```tsx
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMPLETION)
public void afterCompletion(UserCreatedEvent event) {
    // 트랜잭션 완료 후 실행 (커밋/롤백 무관)
}
```

- 트랜잭션이 완료된 후 실행됩니다. (커밋 또는 롤백 상관없이)
- 항상 실행됩니다.

# 주요 속성

---

### FallbackException(트랜잭션 이벤트 리스너 전용)

| 값 | 동작 | 권장 여부 |
| --- | --- | --- |
| `false` (기본값) | 트랜잭션 있을 때만 실행 | **권장** |
| `true` | 트랜잭션 없으면 즉시 실행 | 제한적 사용 |

```java
@Service
public class UserService {

    @Transactional
    public void createUser() {
        publish(new UserEvent()); // ✅ AFTER_COMMIT에 실행
    }

    public void nonTxMethod() {
        publish(new UserEvent()); // fallbackExecution=false → 무시됨
    }
}
```

### condition

Spring Expression Language로 이벤트 처리 여부를 동적으로 결정합니다.

```java
condition = "#event.속성 == 값"
```

| 목적 | SpEL 표현식 | 예시 |
| --- | --- | --- |
| 숫자 비교 | `#event.amount > 1000000` | 고액 주문 |
| 객체 속성 | `#event.user.age >= 18` | 성인 사용자 |
| Enum 비교 | `#event.status == T(OrderStatus).COMPLETED` | 완료 상태 |
| 논리 연산 | `#event.amount > 100000 && #event.paymentMethod == 'CARD'` | 복합 조건 |
| 컬렉션 | `#event.items.size() > 5` | 대량 주문 |
| 포함 여부 | `#event.tags.contains('VIP')` | VIP 고객 |
| 메서드 호출 | `#event.isEligibleForDiscount()` | 비즈니스 로직 위임 |
| 정규식 | `#event.email matches '.*@company\\.com'` | 회사 이메일 |
| Null 체크 | `#event.oldValue != null` | 변경 전후 비교 |
| Bean 참조 | `@env.getProperty('feature.enabled') == 'true'` | 기능 플래그 |

```java
@TransactionalEventListener(
    phase = TransactionPhase.AFTER_COMMIT,
    condition = "#event.customer.vip && #event.totalAmount > 1000000"
)
public void notifyVipLargeOrder(OrderCreatedEvent event) {
    // VIP + 100만원 초과
}
```

```java
@TransactionalEventListener(
    phase = TransactionPhase.AFTER_ROLLBACK,
    condition = "#event.retryCount < 3 && #event.errorType != 'CARD_INVALID'",
    fallbackExecution = false
)
public void scheduleRetry(PaymentFailedEvent event) {
    // 재시도 가능 조건
}
```