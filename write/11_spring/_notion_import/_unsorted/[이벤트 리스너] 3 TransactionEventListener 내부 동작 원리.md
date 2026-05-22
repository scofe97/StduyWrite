# [이벤트 리스너] 3. TransactionEventListener 내부 동작 원리

주제: 분산 시스템

# TransactionEventListener 내부 동작 원리

---

```java
┌─────────────────────────────────────────────────────────────────┐
│ 1. 이벤트 발행                                                     │
│    applicationEventPublisher.publishEvent(event)                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 이벤트 가로채기(Spring이 자동으로)                                  │
│    EventPublicationInterceptor catches event                    │
│    → Checks if transaction is active                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. 트랜잭션용 리스너 등록(트랜잭션이 끝날 때 Spring이 불러준다고 약속          │
│    ApplicationListenerMethodTransactionalAdapter                │
│    → Wraps @TransactionalEventListener method                   │
│    → Registers with TransactionSynchronizationManager           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 비즈니스 로직 실행 + 트랜잭션 종료                                   │
│    Business logic executes                                      │
│    → Commit or Rollback occurs                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 트랜잭션 콜백 실행                                                │
│    AbstractPlatformTransactionManager                           │
│    → triggerBeforeCommit() for BEFORE_COMMIT                    │
│    → triggerAfterCommit() for AFTER_COMMIT                      │
│    → triggerAfterCompletion() for AFTER_ROLLBACK/COMPLETION     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 실제 리스너 메서드 실행                                            │
│    ApplicationListenerMethodTransactionalAdapter                │
│    → Filters by Phase                                           │
│    → Invokes actual listener method                             │
└─────────────────────────────────────────────────────────────────┘
```

## ThreadLocal

ThreadLocal은 각 스레드가 자신만의 독립적인 변수 사본을 가지는 저장소 입니다.

```java
ThreadLocal<String> name = new ThreadLocal<>();
name.set("스레드A");  // 스레드A에서만 보임
```

- static변수라도 다른 스레드와 공유되지 않습니다.
- 트랜잭션 이벤트리스너는 스레드별로 독립적인 트랜잭션을 가져야하므로, 스레드별로 분리하기 위해 스레드 로컬을 사용합니다.

## ThreadSynchronization

```java
// org.springframework.transaction.support.TransactionSynchronization
public interface TransactionSynchronization extends Ordered, Flushable {

    /** 완료 상태 코드 */
    int STATUS_COMMITTED = 0;
    int STATUS_ROLLED_BACK = 1;
    int STATUS_UNKNOWN = 2;

    /**
     * 트랜잭션 일시 중지 시 호출
     */
    default void suspend() {
    }

    /**
     * 트랜잭션 재개 시 호출
     */
    default void resume() {
    }

    /**
     * 트랜잭션 커밋 전 호출
     * - BEFORE_COMMIT Phase가 이 시점에 실행됨
     * - 예외 발생 시 전체 트랜잭션 롤백
     */
    default void beforeCommit(boolean readOnly) {
    }

    /**
     * 트랜잭션 완료 전 호출 (커밋 또는 롤백 전)
     */
    default void beforeCompletion() {
    }

    /**
     * 트랜잭션 커밋 후 호출
     * - AFTER_COMMIT Phase가 이 시점에 실행됨
     * - 예외 발생해도 트랜잭션은 이미 커밋됨
     */
    default void afterCommit() {
    }

    /**
     * 트랜잭션 완료 후 호출 (커밋 또는 롤백 후)
     * - AFTER_COMPLETION Phase가 이 시점에 실행됨
     * - AFTER_ROLLBACK Phase도 이 시점에 실행됨
     *
     * @param status 완료 상태 (STATUS_COMMITTED, STATUS_ROLLED_BACK, STATUS_UNKNOWN)
     */
    default void afterCompletion(int status) {
    }
}
```

## ThreadSynchinoizationManger

```java
[스레드 A 시작]
   │
   ├── @Transactional → initSynchronization() 
   │     → synchronizations.set(new LinkedHashSet<>())
   │
   ├── publishEvent(...) → registerSynchronization(MyListener)
   │     → synchronizations.get().add(MyListener)
   │
   ├── DB 작업 완료 → commit()
   │     → getSynchronizations() → [MyListener]
   │     → triggerAfterCommit() → MyListener 실행
   │
   └── clearSynchronization() → ThreadLocal 제거
```

```java
// 각 스레드마다 독립적인 트랜잭션 컨텍스트
Thread-1: synchronizations = [Listener1, Listener2, Listener3]
Thread-2: synchronizations = [Listener4, Listener5]
Thread-3: synchronizations = [Listener6]

// 스레드 간 간섭 없음
```

```java
// org.springframework.transaction.support.TransactionSynchronizationManager
public abstract class TransactionSynchronizationManager {

    // ThreadLocal 저장소: 현재 스레드의 트랜잭션 동기화 리스너 목록
    private static final ThreadLocal<Set<TransactionSynchronization>> synchronizations =
        new NamedThreadLocal<>("Transaction synchronizations");

    // 현재 트랜잭션 이름
    private static final ThreadLocal<String> currentTransactionName =
        new NamedThreadLocal<>("Current transaction name");

    // 트랜잭션 활성화 여부
    private static final ThreadLocal<Boolean> actualTransactionActive =
        new NamedThreadLocal<>("Actual transaction active");

    /**
     * 트랜잭션 동기화 등록
     */
    public static void registerSynchronization(TransactionSynchronization synchronization) {
        Assert.notNull(synchronization, "TransactionSynchronization must not be null");
        Set<TransactionSynchronization> synchs = synchronizations.get();
        
        if (synchs == null) {
            throw new IllegalStateException("Transaction synchronization is not active");
        }
        synchs.add(synchronization);
    }

    /**
     * 등록된 모든 동기화 리스너 조회 (정렬됨)
     */
    public static List<TransactionSynchronization> getSynchronizations() {
        Set<TransactionSynchronization> synchs = synchronizations.get();
        
        if (synchs == null) {
            throw new IllegalStateException("Transaction synchronization is not active");
        }

        // @Order를 고려한 정렬
        List<TransactionSynchronization> sortedSynchs = new ArrayList<>(synchs);
        OrderComparator.sort(sortedSynchs);
        return Collections.unmodifiableList(sortedSynchs);
    }

    /**
     * 트랜잭션 동기화 초기화
     */
    public static void initSynchronization() {
        if (synchronizations.get() != null) {
            throw new IllegalStateException("Cannot activate transaction synchronization - already active");
        }
        synchronizations.set(new LinkedHashSet<>());
    }

    /**
     * 트랜잭션 동기화 정리
     */
    public static void clearSynchronization() {
        synchronizations.remove();
    }
}
```

- ThreadLocal을 통해서 각 스레드마다 독립적인 트랜잭션 컨텍스트를 유지합니다.
- Set 자료구조를 통해 하나의 트랜잭션에 여러 리스너가 등록 가능합니다.
- @Order 기반으로 실행 순서가 제어됩니다.

## ApplicationListenerMethodTransactionalAdapter

@TransactionalEventListener를 TransactionSynchronization으로 변환

```java
// org.springframework.transaction.event.ApplicationListenerMethodTransactionalAdapter
class ApplicationListenerMethodTransactionalAdapter
        extends ApplicationListenerMethodAdapter
        implements TransactionSynchronization {

		// 트랜잭션 단계
    private final TransactionPhase phase;

		// Phase 추출
    public ApplicationListenerMethodTransactionalAdapter(
            String beanName,
            Class<?> targetClass,
            Method method) {
        super(beanName, targetClass, method);

        // @TransactionalEventListener 어노테이션에서 Phase 추출
        TransactionalEventListener annotation =
            method.getAnnotation(TransactionalEventListener.class);
        this.phase = annotation.phase();
    }

    @Override
    public void onApplicationEvent(ApplicationEvent event) {
        // 트랜잭션이 활성화되어 있는지 확인
        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            // TransactionSynchronization으로 등록
            TransactionSynchronizationManager.registerSynchronization(
                new TransactionSynchronizationEventAdapter(this, event)
            );
        }
        else if (this.annotation.fallbackExecution()) {
            // fallbackExecution=true면 트랜잭션 없이도 실행
            processEvent(event);
        }
    }

    /**
     * BEFORE_COMMIT Phase 처리
     */
    @Override
    public void beforeCommit(boolean readOnly) {
        if (this.phase == TransactionPhase.BEFORE_COMMIT) {
            processEvent(this.event);
        }
    }

    /**
     * AFTER_COMMIT Phase 처리
     */
    @Override
    public void afterCommit() {
        if (this.phase == TransactionPhase.AFTER_COMMIT) {
            processEvent(this.event);
        }
    }

    /**
     * AFTER_ROLLBACK 및 AFTER_COMPLETION Phase 처리
     */
    @Override
    public void afterCompletion(int status) {
        // 롤백된 경우
        if (status == STATUS_ROLLED_BACK) {
            if (this.phase == TransactionPhase.AFTER_ROLLBACK) {
                processEvent(this.event);
            }
            else if (this.phase == TransactionPhase.AFTER_COMPLETION) {
                processEvent(this.event);
            }
        }
        // 커밋된 경우
        else if (status == STATUS_COMMITTED) {
            if (this.phase == TransactionPhase.AFTER_COMPLETION) {
                processEvent(this.event);
            }
        }
    }

    /**
     * 실제 리스너 메서드 호출
     */
    protected void processEvent(ApplicationEvent event) {
        // condition 평가
        if (shouldHandle(event)) {
            // 실제 @TransactionalEventListener 메서드 호출
            invokeListener(event);
        }
    }
}
```

## AbstractPlatformTransactionManger

```java
// org.springframework.transaction.support.AbstractPlatformTransactionManager
public abstract class AbstractPlatformTransactionManager
        implements PlatformTransactionManager {

    /**
     * 커밋 처리
     */
    private void processCommit(DefaultTransactionStatus status) {
        try {
            boolean beforeCompletionInvoked = false;

            try {
                boolean unexpectedRollback = false;

                // 1. beforeCommit 콜백 호출
                prepareForCommit(status);
                triggerBeforeCommit(status);  // ← BEFORE_COMMIT 실행

                // 2. beforeCompletion 콜백 호출
                triggerBeforeCompletion(status);
                beforeCompletionInvoked = true;

                // 3. 실제 커밋 수행
                if (status.hasSavepoint()) {
                    status.releaseHeldSavepoint();
                }
                else if (status.isNewTransaction()) {
                    doCommit(status);  // ← 실제 DB 커밋
                }

                // 4. afterCommit 콜백 호출
                triggerAfterCommit(status);  // ← AFTER_COMMIT 실행
            }
            catch (UnexpectedRollbackException ex) {
                // 예기치 않은 롤백 발생
                triggerAfterCompletion(status, TransactionSynchronization.STATUS_ROLLED_BACK);
                throw ex;
            }
            catch (TransactionException ex) {
                // 커밋 실패 시 롤백
                if (isRollbackOnCommitFailure()) {
                    doRollbackOnCommitException(status, ex);
                }
                else {
                    triggerAfterCompletion(status, TransactionSynchronization.STATUS_UNKNOWN);
                }
                throw ex;
            }
            catch (RuntimeException | Error ex) {
                if (!beforeCompletionInvoked) {
                    triggerBeforeCompletion(status);
                }
                doRollbackOnCommitException(status, ex);
                throw ex;
            }

            // 5. afterCompletion 콜백 호출
            try {
                triggerAfterCompletion(status, TransactionSynchronization.STATUS_COMMITTED);
                // ← AFTER_COMPLETION 실행 (커밋 성공 시)
            }
            finally {
                cleanupAfterCompletion(status);
            }
        }
        finally {
            cleanupAfterCompletion(status);
        }
    }

    /**
     * 롤백 처리
     */
    private void processRollback(DefaultTransactionStatus status, boolean unexpected) {
        try {
            boolean unexpectedRollback = unexpected;

            try {
                // 1. beforeCompletion 콜백 호출
                triggerBeforeCompletion(status);

                // 2. 실제 롤백 수행
                if (status.hasSavepoint()) {
                    status.rollbackToHeldSavepoint();
                }
                else if (status.isNewTransaction()) {
                    doRollback(status);  // ← 실제 DB 롤백
                }
                else {
                    // 중첩 트랜잭션의 경우 rollback-only 마킹
                    if (status.hasTransaction()) {
                        doSetRollbackOnly(status);
                    }
                }
            }
            catch (RuntimeException | Error ex) {
                triggerAfterCompletion(status, TransactionSynchronization.STATUS_UNKNOWN);
                throw ex;
            }

            // 3. afterCompletion 콜백 호출
            triggerAfterCompletion(status, TransactionSynchronization.STATUS_ROLLED_BACK);
            // ← AFTER_ROLLBACK 및 AFTER_COMPLETION 실행 (롤백 시)
        }
        finally {
            cleanupAfterCompletion(status);
        }
    }

    /**
     * beforeCommit 콜백 실행
     */
    protected final void triggerBeforeCommit(DefaultTransactionStatus status) {
        if (status.isNewSynchronization()) {
            TransactionSynchronizationUtils.triggerBeforeCommit(
                status.isReadOnly()
            );
        }
    }

    /**
     * afterCommit 콜백 실행
     */
    protected final void triggerAfterCommit(DefaultTransactionStatus status) {
        if (status.isNewSynchronization()) {
            TransactionSynchronizationUtils.triggerAfterCommit();
        }
    }

    /**
     * afterCompletion 콜백 실행
     */
    protected final void triggerAfterCompletion(
            DefaultTransactionStatus status,
            int completionStatus) {
        if (status.isNewSynchronization()) {
            List<TransactionSynchronization> synchronizations =
                TransactionSynchronizationManager.getSynchronizations();

            TransactionSynchronizationUtils.invokeAfterCompletion(
                synchronizations,
                completionStatus
            );
        }
    }
}
```

## 상세 동작 과정

### 1. 이벤트 발행

```java
// UserService.java
@Transactional
public User createUser(String name, String email) {
    User user = userRepository.save(new User(name, email));

    // 이벤트 발행
    applicationEventPublisher.publishEvent(new UserCreatedEvent(user));
    // ↓
    // Spring의 ApplicationEventMulticaster가 이벤트를 수신
    // ↓
    // 모든 등록된 ApplicationListener에게 이벤트 전파

    return user;
}
```

### 2. @TransactionalEventListener 감지 및 등록

```java
// ApplicationListenerMethodTransactionalAdapter
@Override
public void onApplicationEvent(ApplicationEvent event) {
    // 1. 트랜잭션 활성화 확인
    if (TransactionSynchronizationManager.isSynchronizationActive()) {

        // 2. TransactionSynchronization 생성 및 등록
        TransactionSynchronizationManager.registerSynchronization(
            new TransactionSynchronizationEventAdapter(this, event, this.phase)
        );

        // ↓
        // ThreadLocal<Set<TransactionSynchronization>>에 저장됨
        // synchronizations.get().add(synchronization);
    }
}
```

### 3. 트랜잭션 커밋 시 콜백 실행

```java
// AbstractPlatformTransactionManager.processCommit()

try {
    // 1. BEFORE_COMMIT Phase 실행
    triggerBeforeCommit(status);
    // ↓
    // TransactionSynchronizationUtils.triggerBeforeCommit()
    // ↓
    // synchronizations.forEach(sync -> sync.beforeCommit(readOnly));
    // ↓
    // ApplicationListenerMethodTransactionalAdapter.beforeCommit()
    // ↓
    // if (this.phase == BEFORE_COMMIT) processEvent(event);

    // 2. 실제 커밋
    doCommit(status);

    // 3. AFTER_COMMIT Phase 실행
    triggerAfterCommit(status);
    // ↓
    // synchronizations.forEach(sync -> sync.afterCommit());
    // ↓
    // ApplicationListenerMethodTransactionalAdapter.afterCommit()
    // ↓
    // if (this.phase == AFTER_COMMIT) processEvent(event);
}
finally {
    // 4. AFTER_COMPLETION Phase 실행 (커밋 성공 시)
    triggerAfterCompletion(status, STATUS_COMMITTED);
    // ↓
    // synchronizations.forEach(sync -> sync.afterCompletion(STATUS_COMMITTED));
    // ↓
    // ApplicationListenerMethodTransactionalAdapter.afterCompletion(STATUS_COMMITTED)
    // ↓
    // if (this.phase == AFTER_COMPLETION) processEvent(event);
}
```

### 4. 트랜잭션 롤백 시 콜백 실행

```java
// AbstractPlatformTransactionManager.processRollback()

try {
    // 1. 실제 롤백
    doRollback(status);
}
finally {
    // 2. AFTER_ROLLBACK 및 AFTER_COMPLETION Phase 실행
    triggerAfterCompletion(status, STATUS_ROLLED_BACK);
    // ↓
    // synchronizations.forEach(sync -> sync.afterCompletion(STATUS_ROLLED_BACK));
    // ↓
    // ApplicationListenerMethodTransactionalAdapter.afterCompletion(STATUS_ROLLED_BACK)
    // ↓
    // if (this.phase == AFTER_ROLLBACK) processEvent(event);
    // if (this.phase == AFTER_COMPLETION) processEvent(event);
}
```

# 실습

---

## 어노테이션 사용

```java
/**
 * 사용자 서비스
 * 트랜잭션 이벤트를 발행하는 비즈니스 로직
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final ApplicationEventPublisher eventPublisher;

    /**
     * 사용자 생성 - REQUIRED 전파 레벨
     */
    @Transactional
    public User createUser(String name, String email) {
        log.info("[Service] Creating user: name={}, email={}", name, email);

        User user = User.builder()
                .name(name)
                .email(email)
                .status(User.UserStatus.ACTIVE)
                .build();

        User savedUser = userRepository.save(user);
        log.info("[Service] User saved with ID: {}", savedUser.getId());

        // 이벤트 발행
        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));
        log.info("[Service] UserCreatedEvent published");

        return savedUser;
    }

    /**
     * 사용자 생성 (예외 발생) - 롤백 테스트용
     */
    @Transactional
    public User createUserWithException(String name, String email) {
        log.info("[Service] Creating user with exception: name={}, email={}", name, email);

        User user = User.builder()
                .name(name)
                .email(email)
                .status(User.UserStatus.ACTIVE)
                .build();

        User savedUser = userRepository.save(user);
        log.info("[Service] User saved with ID: {}", savedUser.getId());

        // 이벤트 발행
        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));
        log.info("[Service] UserCreatedEvent published");

        // 강제로 예외 발생 - 롤백 유도
        throw new RuntimeException("Intentional exception for rollback test");
    }

    /**
     * 사용자 수정
     */
    @Transactional
    public User updateUser(Long userId) {
        log.info("[Service] Updating user: userId={}", userId);

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId));

        user.activate();
        User updatedUser = userRepository.save(user);

        eventPublisher.publishEvent(new UserUpdatedEvent(updatedUser));
        log.info("[Service] UserUpdatedEvent published");

        return updatedUser;
    }

    /**
     * 사용자 삭제
     */
    @Transactional
    public void deleteUser(Long userId) {
        log.info("[Service] Deleting user: userId={}", userId);

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId));

        eventPublisher.publishEvent(new UserDeletedEvent(user));
        log.info("[Service] UserDeletedEvent published");

        userRepository.delete(user);
    }

    /**
     * 새로운 트랜잭션으로 사용자 생성 - REQUIRES_NEW 전파 레벨
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public User createUserInNewTransaction(String name, String email) {
        log.info("[Service][NEW_TX] Creating user in new transaction: name={}, email={}", name, email);

        User user = User.builder()
                .name(name)
                .email(email)
                .status(User.UserStatus.ACTIVE)
                .build();

        User savedUser = userRepository.save(user);
        log.info("[Service][NEW_TX] User saved with ID: {}", savedUser.getId());

        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));
        log.info("[Service][NEW_TX] UserCreatedEvent published");

        return savedUser;
    }

    /**
     * 트랜잭션 없이 사용자 생성
     */
    public User createUserWithoutTransaction(String name, String email) {
        log.info("[Service][NO_TX] Creating user without transaction: name={}, email={}", name, email);

        User user = User.builder()
                .name(name)
                .email(email)
                .status(User.UserStatus.ACTIVE)
                .build();

        User savedUser = userRepository.save(user);
        log.info("[Service][NO_TX] User saved with ID: {}", savedUser.getId());

        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));
        log.info("[Service][NO_TX] UserCreatedEvent published");

        return savedUser;
    }
}

```

## 실제 사용

```java
/**
 * TransactionSynchronizationManager 직접 사용 예제
 *
 * 이 서비스는 @TransactionalEventListener가 내부적으로 어떻게 동작하는지
 * TransactionSynchronizationManager를 직접 사용하여 보여줍니다.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class TransactionSyncDemoService {

    private final UserRepository userRepository;

    /**
     * TransactionSynchronization 직접 등록 예제
     *
     * @TransactionalEventListener가 내부적으로 하는 일:
     * 1. 이벤트 수신 시 TransactionSynchronization 구현체 생성
     * 2. TransactionSynchronizationManager에 등록
     * 3. 트랜잭션 완료 시 콜백 실행
     */
    @Transactional
    public User createUserWithCustomSync(String name, String email) {
        log.info("\n========== TransactionSynchronization 직접 등록 예제 ==========");

        // 1. 트랜잭션 동기화 활성화 확인
        boolean isActive = TransactionSynchronizationManager.isSynchronizationActive();
        log.info("트랜잭션 동기화 활성화: {}", isActive);

        // 2. 현재 트랜잭션 정보 출력
        String txName = TransactionSynchronizationManager.getCurrentTransactionName();
        boolean isReadOnly = TransactionSynchronizationManager.isCurrentTransactionReadOnly();
        log.info("트랜잭션 이름: {}, 읽기전용: {}", txName, isReadOnly);

        // 3. Custom TransactionSynchronization 등록
        // 이것이 @TransactionalEventListener가 내부적으로 하는 일입니다!
        if (isActive) {
            log.info("\n--- TransactionSynchronization 등록 시작 ---");

            // 여러 순서로 등록하여 @Order 동작 확인
            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("Sync-1 (Order=100)", 100)
            );

            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("Sync-2 (Order=1)", 1)
            );

            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("Sync-3 (Order=50)", 50)
            );

            log.info("--- TransactionSynchronization 등록 완료 ---\n");
        }

        // 4. 비즈니스 로직 수행
        log.info("--- 비즈니스 로직 실행 시작 ---");
        User user = User.builder()
            .name(name)
            .email(email)
            .status(User.UserStatus.ACTIVE)
            .build();

        User savedUser = userRepository.save(user);
        log.info("사용자 저장 완료: {}", savedUser.getId());
        log.info("--- 비즈니스 로직 실행 완료 ---\n");

        log.info("--- 트랜잭션 커밋 시작 (콜백 실행 예정) ---");
        return savedUser;

        // 메서드 종료 시 트랜잭션 커밋됨
        // → TransactionSynchronization 콜백들이 @Order 순서대로 실행됨:
        //   1. Sync-2 (Order=1)
        //   2. Sync-3 (Order=50)
        //   3. Sync-1 (Order=100)
    }

    /**
     * 롤백 시 TransactionSynchronization 동작 확인
     */
    @Transactional
    public User createUserWithRollback(String name, String email) {
        log.info("\n========== 롤백 시 TransactionSynchronization 동작 ==========");

        // TransactionSynchronization 등록
        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("RollbackSync", 1)
            );
        }

        // 비즈니스 로직
        User user = User.builder()
            .name(name)
            .email(email)
            .status(User.UserStatus.ACTIVE)
            .build();

        userRepository.save(user);

        // 예외 발생 → 롤백
        log.info("--- 예외 발생: 트랜잭션 롤백 예정 ---");
        throw new RuntimeException("Test rollback");

        // 트랜잭션 롤백됨
        // → afterCompletion(STATUS_ROLLED_BACK) 호출됨
    }

    /**
     * 중첩 트랜잭션에서 TransactionSynchronization 동작 확인
     */
    @Transactional
    public void demonstrateNestedTransaction() {
        log.info("\n========== 중첩 트랜잭션에서 TransactionSynchronization ==========");

        // 외부 트랜잭션에 동기화 등록
        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("OuterSync", 1)
            );
        }

        log.info("--- 외부 트랜잭션에서 사용자 생성 ---");
        User user = User.builder()
            .name("Outer User")
            .email("outer@example.com")
            .status(User.UserStatus.ACTIVE)
            .build();
        userRepository.save(user);

        // 내부 트랜잭션 호출
        log.info("\n--- 내부 트랜잭션 호출 (REQUIRES_NEW) ---");
        createInnerTransaction();

        log.info("\n--- 외부 트랜잭션으로 복귀 ---");
    }

    /**
     * REQUIRES_NEW로 새로운 트랜잭션 시작
     * - 기존 트랜잭션 일시 중지 (suspend)
     * - 새 트랜잭션 완료 후 기존 트랜잭션 재개 (resume)
     */
    @Transactional(propagation = org.springframework.transaction.annotation.Propagation.REQUIRES_NEW)
    public void createInnerTransaction() {
        log.info("--- 새 트랜잭션 시작 (외부 트랜잭션 일시 중지됨) ---");

        // 새 트랜잭션에 동기화 등록
        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(
                new CustomTransactionSynchronization("InnerSync", 1)
            );
        }

        User innerUser = User.builder()
            .name("Inner User")
            .email("inner@example.com")
            .status(User.UserStatus.ACTIVE)
            .build();
        userRepository.save(innerUser);

        log.info("--- 내부 트랜잭션 커밋 예정 ---");
    }

    /**
     * TransactionSynchronizationManager 상태 정보 출력
     */
    public void printTransactionSyncInfo() {
        log.info("\n========== TransactionSynchronizationManager 상태 ==========");

        boolean isActive = TransactionSynchronizationManager.isSynchronizationActive();
        log.info("동기화 활성화: {}", isActive);

        if (isActive) {
            String txName = TransactionSynchronizationManager.getCurrentTransactionName();
            boolean isReadOnly = TransactionSynchronizationManager.isCurrentTransactionReadOnly();
            boolean isActualTxActive = TransactionSynchronizationManager.isActualTransactionActive();

            log.info("트랜잭션 이름: {}", txName);
            log.info("읽기 전용: {}", isReadOnly);
            log.info("실제 트랜잭션 활성화: {}", isActualTxActive);

            // 등록된 동기화 리스너 개수
            try {
                int syncCount = TransactionSynchronizationManager.getSynchronizations().size();
                log.info("등록된 동기화 리스너 개수: {}", syncCount);
            } catch (IllegalStateException e) {
                log.info("등록된 동기화 리스너 개수: 조회 불가 (동기화 비활성)");
            }
        }

        log.info("==========================================================\n");
    }
}
```

```java
/**
 * TransactionSynchronization 인터페이스 직접 구현 예제
 *
 * 이 클래스는 Spring의 트랜잭션 이벤트 리스너가 내부적으로 어떻게 동작하는지
 * TransactionSynchronization 인터페이스를 직접 구현하여 보여줍니다.
 *
 * @TransactionalEventListener는 내부적으로 이 인터페이스를 구현한
 * ApplicationListenerMethodTransactionalAdapter를 사용합니다.
 */
@Slf4j
public class CustomTransactionSynchronization implements TransactionSynchronization, Ordered {

    private final String name;
    private final int order;

    public CustomTransactionSynchronization(String name, int order) {
        this.name = name;
        this.order = order;
        log.info("[{}] TransactionSynchronization created with order={}", name, order);
    }

    @Override
    public int getOrder() {
        return this.order;
    }

    /**
     * 트랜잭션 일시 중지 시 호출
     * - PROPAGATION_REQUIRES_NEW 등으로 새 트랜잭션이 시작될 때
     */
    @Override
    public void suspend() {
        log.info("[{}] suspend() - 트랜잭션 일시 중지", name);
    }

    /**
     * 트랜잭션 재개 시 호출
     * - 일시 중지된 트랜잭션이 다시 활성화될 때
     */
    @Override
    public void resume() {
        log.info("[{}] resume() - 트랜잭션 재개", name);
    }

    /**
     * 트랜잭션 커밋 전 호출
     * - BEFORE_COMMIT Phase와 매핑됨
     * - 예외 발생 시 전체 트랜잭션 롤백
     *
     * @param readOnly 읽기 전용 트랜잭션 여부
     */
    @Override
    public void beforeCommit(boolean readOnly) {
        log.info("[{}] beforeCommit(readOnly={}) - 커밋 직전 (BEFORE_COMMIT Phase)", name, readOnly);
        log.info("[{}]   → 이 시점에 예외가 발생하면 전체 트랜잭션이 롤백됩니다", name);
    }

    /**
     * 트랜잭션 완료 전 호출 (커밋 또는 롤백 전)
     * - cleanup 작업에 사용
     */
    @Override
    public void beforeCompletion() {
        log.info("[{}] beforeCompletion() - 트랜잭션 완료 직전 (커밋/롤백 전)", name);
    }

    /**
     * 트랜잭션 커밋 후 호출
     * - AFTER_COMMIT Phase와 매핑됨
     * - 예외 발생해도 이미 커밋된 데이터는 유지됨
     */
    @Override
    public void afterCommit() {
        log.info("[{}] afterCommit() - 커밋 완료 (AFTER_COMMIT Phase)", name);
        log.info("[{}]   → 이 시점에 예외가 발생해도 데이터는 이미 커밋되었습니다", name);
    }

    /**
     * 트랜잭션 완료 후 호출 (커밋 또는 롤백 후)
     * - AFTER_COMPLETION 및 AFTER_ROLLBACK Phase와 매핑됨
     *
     * @param status 완료 상태
     *               - STATUS_COMMITTED (0): 커밋 성공
     *               - STATUS_ROLLED_BACK (1): 롤백됨
     *               - STATUS_UNKNOWN (2): 상태 불명
     */
    @Override
    public void afterCompletion(int status) {
        String statusStr = switch (status) {
            case STATUS_COMMITTED -> "COMMITTED";
            case STATUS_ROLLED_BACK -> "ROLLED_BACK";
            case STATUS_UNKNOWN -> "UNKNOWN";
            default -> "UNDEFINED";
        };

        log.info("[{}] afterCompletion(status={}) - 트랜잭션 완료", name, statusStr);

        if (status == STATUS_COMMITTED) {
            log.info("[{}]   → AFTER_COMPLETION Phase: 커밋 완료", name);
        } else if (status == STATUS_ROLLED_BACK) {
            log.info("[{}]   → AFTER_ROLLBACK Phase: 롤백됨", name);
            log.info("[{}]   → AFTER_COMPLETION Phase: 롤백으로 완료", name);
        }
    }

    /**
     * flush 호출 시 동작
     * - JPA EntityManager flush 등에서 호출될 수 있음
     */
    @Override
    public void flush() {
        log.info("[{}] flush() - 트랜잭션 flush", name);
    }
}

```