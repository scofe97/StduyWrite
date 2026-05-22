# DDD vs CRUD

주제: Spring Study

# 순수 DDD vs 전통 Layered‑CRUD (MyBatis) — 상세 비교

## 1. 패키지 구조

### 전통 Layered‑CRUD

```
com.example.ticket
├─ controller          # ① HTTP 요청 진입점: DTO를 받아 Service 호출
│   └─ TicketController.java
├─ service             # ② 비즈니스 로직 + 트랜잭션 관리
│   └─ TicketService.java
├─ repository          # ③ MyBatis Mapper: SQL ↔ 도메인 모델 매핑
│   └─ TicketMapper.java
├─ model               # ④ 도메인 POJO: Entity와 DTO 구분 없음
│   └─ Ticket.java
└─ dto                 # ⑤ 요청/응답 구조 정의
    └─ TicketDto.java
```

- **특징**: 계층별로 코드가 물리적으로 분리되지만, 각 계층 안에서는 역할이 모호하게 섞이기 쉽습니다.

### 순수 DDD (Event Sourcing 없음, MyBatis)

```
com.example.ticket                «Bounded Context»
├─ domain                        # 핵심 비즈니스 규칙 캡슐화
│   ├─ model                     # Aggregate + Value Object
│   │   └─ Ticket.java           # 불변 생성·행위 메서드 포함
│   └─ repository                # 도메인 저장소 인터페이스
│       └─ TicketRepository.java
│
├─ infrastructure
│   └─ persistence
│       ├─ MyBatisTicketRepository.java  # 인터페이스 구현
│       └─ TicketMapper.java             # MyBatis XML/Annotation
│
├─ application                  # 유즈케이스 оркест레이션
│   ├─ command                   # Write 전용 DTO
│   │   └─ CreateTicketCommand.java
│   └─ service                   # Application Service
│       └─ TicketApplicationService.java
│
└─ presentation                # REST / GraphQL 등 I/O
    └─ TicketController.java
```

- **특징**: 각 레이어가 책임에 따라 엄격히 분리되어 있으며, 도메인(model) 레이어엔 절대 DB나 외부 의존이 없습니다.

---

## 2. 도메인 규칙 (Business Rules)

### 2‑A. Layered‑CRUD

```java
// service/TicketService.java
@Service
public class TicketService {
    private final TicketMapper mapper;

    @Transactional
    public Long create(String title, boolean highPriority) {
        // 1) 검증 로직
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("제목은 필수입니다");
        }
        // 2) 우선순위 기반 상태 결정
        String status = highPriority ? "URGENT" : "OPEN";
        // 3) 도메인 모델 사용
        Ticket t = new Ticket();
        t.setTitle(title);
        t.setStatus(status);
        // 4) DB 저장
        mapper.insert(t);
        return t.getId();
    }
}
```

- **단점**: 검증, 상태 결정, 모델 생성, 저장이 한 메서드에 섞여 있어 **단일 책임 원칙(SRP)** 위반. 규칙 변경 시 테스트·유지 보수가 어렵습니다.

### 2‑B. 순수 DDD

**Aggregate 개념**

- Aggregate는 관련 도메인 객체들을 하나의 **일관된 트랜잭션 경계**로 묶는 단위입니다.
- Aggregate Root인 `Ticket`을 통해서만 내부 상태를 변경하여 **일관성 규칙**을 안전하게 유지합니다.

```java
// domain/model/Ticket.java
public class Ticket {
    private final TicketId id;
    private final String title;
    private Status status;

    public enum Status { OPEN, URGENT, CLOSED }

    private Ticket(TicketId id, String title, Status status) {
        this.id = id;
        this.title = title;
        this.status = status;
    }

    public static Ticket create(String title, boolean highPriority, IdGenerator gen) {
        // 1) 검증 로직
        if (title == null || title.isBlank()) {
            throw new DomainException("TITLE_REQUIRED");
        }
        // 2) 식별자 생성
        TicketId id = new TicketId(gen.next());
        // 3) 상태 결정
        Status s = highPriority ? Status.URGENT : Status.OPEN;
        return new Ticket(id, title, s);
    }

    // getter만 제공 → 외부에서 상태 변경 불가
    public TicketId getId()    { return id; }
    public String   getTitle() { return title; }
    public Status   getStatus(){ return status; }
}

```

- **장점**: 비즈니스 규칙이 `Aggregate` 내부에 모여 있어 **모델 단위 테스트**가 간단해집니다.
    - 외부에서 임의 상태 변경 불가 → 불변성, 일관성 보장.
    - 상태 전이는 `start()`, `proceed()`, `complete()`, `close()` 메서드를 통해서만 가능합니다.

## 3. 식별자 생성 (Identifier Generation)

### 3‑A. Layered‑CRUD

```java
// model/Ticket.java
public class Ticket {
    private Long id;        // DB에서 @GeneratedValue로 생성
    private String title;
    private String status;
    // getter/setter...
}

// repository/TicketMapper.java
@Mapper
public interface TicketMapper {
    @Insert("INSERT INTO ticket(title,status) VALUES(#{title},#{status})")
    @Options(useGeneratedKeys=true, keyProperty="id")
    void insert(Ticket ticket);
}

```

- **특징**: 식별자가 DB 저장 시점에 결정되므로, 코드 내에선 ID가 없을 수 있습니다.

### 3‑B. 순수 DDD

```java
// domain/model/TicketId.java
public record TicketId(Long value) {}

// domain/repository/IdGenerator.java
public interface IdGenerator { Long next(); }

// 생성 시점에 ID 발급
TicketId id = new TicketId(gen.next());

```

- **장점**: 식별자를 애플리케이션에서 생성하여, **저장 전후가 동일한 도메인 객체**로 다룰 수 있습니다.

---

## 4. 저장소 (Repository)

### 4‑A. Layered‑CRUD

```java
// repository/TicketMapper.java
@Mapper
public interface TicketMapper {
    void insert(Ticket ticket);
    Ticket findById(Long id);
}

```

- **단순 매핑**: SQL과 모델 간 1:1 매핑, 비즈니스 로직 없음.

### 4‑B. 순수 DDD

```java
// domain/repository/TicketRepository.java
public interface TicketRepository {
    void save(Ticket ticket);
    Optional<Ticket> findById(TicketId id);
}

// infrastructure/persistence/MyBatisTicketRepository.java
@Repository
public class MyBatisTicketRepository implements TicketRepository {
    private final TicketMapper mapper;

    @Override
    public void save(Ticket ticket) {
        // VO→Map 변환 등 매핑 로직 캡슐화
        mapper.insert(new TicketEntity(ticket));
    }

    @Override
    public Optional<Ticket> findById(TicketId id) {
        TicketEntity e = mapper.findById(id.value());
        return e == null
            ? Optional.empty()
            : Optional.of(e.toDomain());
    }
}

```

- **장점**: 도메인 로직은 인터페이스만 참조, 구현체 교체·테스트 더 쉽습니다.

---

## 5. 서비스 책임 (Service Responsibility)

### 5‑A. Layered‑CRUD

```java
// service/TicketService.java
@Service
public class TicketService {
    private final TicketMapper mapper;
    private final NotificationClient client;

    @Transactional
    public Long createAndNotify(String title) {
        // domain 로직 + 외부 호출 혼합
        Ticket t = new Ticket();
        t.setTitle(title);
        t.setStatus("OPEN");
        mapper.insert(t);
        client.sendAlert(t.getId());
        return t.getId();
    }
}

```

- **단점**: 외부 통신·비즈니스·트랜잭션이 한 곳에 있어 책임 과다.

### 5‑B. 순수 DDD

```java
// application/service/TicketApplicationService.java
@Service
public class TicketApplicationService {
    private final TicketRepository repo;
    private final NotificationService notify;
    private final IdGenerator idGen;

    @Transactional
    public TicketId createAndNotify(CreateTicketCommand cmd) {
        // 1) Aggregate 생성(규칙 포함)
        Ticket t = Ticket.create(cmd.title(), cmd.highPriority(), idGen);
        // 2) 저장
        repo.save(t);
        // 3) 후처리: 도메인 이벤트 또는 직접 호출
        notify.sendAlert(t.getId());
        return t.getId();
    }
}

```

- **장점**: Use‑Case 흐름만 orchestration, 도메인 규칙과 외부 호출 분리.

---

## 6. 변경 이력 (Audit / Change History)

### 6‑A. Layered‑CRUD

```java
// model/Ticket.java
@EntityListeners(AuditingEntityListener.class)
@Entity
public class Ticket {
    @CreatedDate  LocalDateTime createdAt;
    @LastModifiedDate LocalDateTime updatedAt;
    // 상태 변경 시 서비스에서 별도 로그 저장
}

```

- **특징**: 테이블 컬럼에 최신 변경 시간만 유지, 이력 세부 내용 미포함.

### 6‑B. 순수 DDD

```java
// (ES 없음) 도메인 이벤트 예시
public class Ticket {
    private final List<DomainEvent> changes = new ArrayList<>();

    public static Ticket create(...) {
        TicketCreated ev = new TicketCreated(...);
        changes.add(ev);
        return t;
    }
    public List<DomainEvent> changes() { return List.copyOf(changes); }
}

// Application Service
t.changes().forEach(evt -> publisher.publishEvent(evt));

```

- **장점**: 원하는 수준까지 **이벤트로 이력**을 남길 수 있고, 정책 따라 저장·통계 활용 가능.

---

## 7. 요약 비교 테이블

| 구분 | Layered‑CRUD | 순수 DDD |
| --- | --- | --- |
| **도메인 규칙** | 서비스 내부 if‑else 로직 집중 | Aggregate.create() 에 캡슐화 |
| **식별자 생성** | DB @GeneratedKeys | IdGenerator + TicketId VO |
| **저장소** | TicketMapper.insert(...) 직접 호출 | TicketRepository 인터페이스 + Adapter |
| **서비스 책임** | 비즈니스·트랜잭션·외부 호출 혼합 | Application Service = 유즈케이스만 |
| **변경 이력** | Audit 칼럼·로그 | Domain Event 도입 통해 세밀한 이력 관리 |

각 단계별 **책임 분리가 어떻게 달라지는지**, **테스트 및 유지보수성**을 비교해 보시기 바랍니다!