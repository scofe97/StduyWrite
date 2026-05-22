# DDD Aggregate 패턴

주제: Spring Study

# DDD Aggregate 패턴 & 설계 가이드

**예시 도메인**: 티켓(Ticket) → 워크플로우 인스턴스(WorkflowInstance) → 워크플로우 인스턴스 스텝(WorkflowInstanceStep)

Aggregate는 **도메인 모델의 일관성을 보장하기 위한 경계(Boundary)** 입니다. 하나의 Aggregate Root를 통해 내부 엔티티/값 객체 파생 작업을 수행하며, 외부에서는 Aggregate Root만 참조합니다.

---

## 1. 패키지 구조 제안

```
com.example.ticketflow
├─ domain
│   ├─ model
│   │   ├─ Ticket.java                       # Aggregate Root
│   │   ├─ WorkflowInstance.java            # 내부 엔티티
│   │   └─ WorkflowInstanceStep.java        # 내부 값 객체
│   └─ exception
│       └─ DomainException.java             # 공통 도메인 예외
│
├─ application
│   └─ service
│       └─ TicketApplicationService.java    # 유즈케이스(티켓 실행/종료)
│
├─ infrastructure
│   └─ persistence
│       ├─ MyBatisTicketRepository.java     # 도메인 저장소 구현체
│       └─ TicketMapper.java                # MyBatis Mapper
│
└─ presentation
    └─ TicketController.java                # REST API

```

---

## 2. 도메인 모델

### 2.1. 값 객체: WorkflowInstanceStep

```java
public class WorkflowInstanceStep {
    private final int sequence;         // 단계 번호
    private final String name;          // 단계 이름
    private StepStatus status;          // 처리 상태

    public enum StepStatus { PENDING, COMPLETED, FAILED }

    public WorkflowInstanceStep(int sequence, String name) {
        this.sequence = sequence;
        this.name = name;
        this.status = StepStatus.PENDING;
    }

    public void complete() {
        if (status != StepStatus.PENDING) {
            throw new DomainException("STEP_NOT_PENDING");
        }
        this.status = StepStatus.COMPLETED;
    }

    // 게터만 제공
    public int getSequence()     { return sequence; }
    public String getName()      { return name; }
    public StepStatus getStatus(){ return status; }
}

```

### 2.2. 내부 엔티티: WorkflowInstance

```java
public class WorkflowInstance {
    private final String id;                           // 식별자
    private final List<WorkflowInstanceStep> steps;    // 1:N 관계
    private InstanceStatus status;

    public enum InstanceStatus { CREATED, RUNNING, FAILURE, COMPLETED }

    public WorkflowInstance(String id, List<String> stepNames) {
        this.id = id;
        this.status = InstanceStatus.CREATED;
        this.steps = IntStream.range(0, stepNames.size())
            .mapToObj(i -> new WorkflowInstanceStep(i+1, stepNames.get(i)))
            .toList();
    }

    public void start() {
        if (status != InstanceStatus.CREATED) {
            throw new DomainException("INVALID_STATE_TO_START");
        }
        this.status = InstanceStatus.RUNNING;
    }

    public void processFirstStep() {
        if (steps.isEmpty()) throw new DomainException("NO_STEPS_DEFINED");
        steps.get(0).complete();  // 첫 번째 스텝만 처리
    }

    public void fail() {
        this.status = InstanceStatus.FAILURE;
    }

    // 게터만 제공
    public String getId()        { return id; }
    public InstanceStatus getStatus() { return status; }
    public List<WorkflowInstanceStep> getSteps() { return List.copyOf(steps); }
}

```

### 2.3. Aggregate Root: Ticket

```java
public class Ticket {
    private final String id;                          // VO로 분리 가능
    private TicketStatus status;
    private final WorkflowInstance workflow;

    public enum TicketStatus { NEW, EXECUTING, CLOSED }

    public Ticket(String id, List<String> stepNames) {
        this.id = id;
        this.status = TicketStatus.NEW;
        this.workflow = new WorkflowInstance(id + "_wf", stepNames);
    }

    /** 티켓 실행 */
    public void execute() {
        // 1) 실행 가능 검증
        if (status != TicketStatus.NEW) {
            throw new DomainException("TICKET_NOT_NEW");
        }
        // 2) 상태 변경
        this.status = TicketStatus.EXECUTING;
        // 3) 워크플로우 시작 및 이력
        workflow.start();
        // 4) 첫 스텝 처리 및 이력
        workflow.processFirstStep();
    }

    /** 티켓 종료 */
    public void close() {
        // 1) 종료 가능 검증
        if (status != TicketStatus.EXECUTING) {
            throw new DomainException("TICKET_NOT_EXECUTING");
        }
        // 2) 상태 변경
        this.status = TicketStatus.CLOSED;
    }

    // 게터만 제공
    public String getId()       { return id; }
    public TicketStatus getStatus() { return status; }
    public WorkflowInstance getWorkflowInstance() { return workflow; }
}

```

---

## 3. Application Service (유즈케이스)

```java
@Service
@RequiredArgsConstructor
public class TicketApplicationService {
    private final TicketRepository repo;
    private final ExternalApiClient apiClient;

    @Transactional
    public void executeTicket(String id) {
        Ticket ticket = repo.findById(id).orElseThrow();
        ticket.execute();        // Aggregate 단일 책임
        repo.save(ticket);       // 변경된 상태·이력 저장
        apiClient.notifyExecution(id);  // 후속 외부 호출
    }

    @Transactional
    public void closeTicket(String id) {
        Ticket ticket = repo.findById(id).orElseThrow();
        ticket.close();
        repo.save(ticket);
        apiClient.notifyClosure(id);
    }
}

```

---

## 4. DDD 설계 가이드라인

1. **Aggregate Root**: 외부에서 접근 가능한 단일 진입점
    - 내부 상태 변경은 Aggregate Root 메서드를 통해서만 수행
    - 다른 Aggregate와는 ID로만 참조, 내부 엔티티 노출 금지
2. **Entity vs Value Object**
    - **Entity**: 식별자(ID)로 구분, 장기간 생명주기 (Ticket, WorkflowInstance)
    - **Value Object**: 식별자가 없고 불변(WorkflowInstanceStep)
3. **Domain Service**: 특정 비즈니스 로직이 Aggregate에 속하지 않을 때
    - 예: `PaymentService.processPayment(ticket)` 같은 로직은 별도의 도메인 서비스
4. **Factory**: 복잡한 Aggregate 생성 로직 캡슐화
    - 생성자가 복잡하면 `TicketFactory` 클래스로 추출
5. **Repository Interface**: 도메인 레이어에 인터페이스만 두고, 인프라 구현 분리
    - `interface TicketRepository { findById, save }`
6. **Domain Event**: 중요한 상태변경을 이벤트로 발행하여 추적 및 연계
    - 예: `TicketStartedEvent`, `WorkflowStepCompletedEvent`
7. **Ubiquitous Language**: 코드·팀 문서에서 도메인 용어 통일
    - 클래스명, 메서드명, 변수명에 도메인 용어 사용
8. **Bounded Context**: 각 도메인(`ticketflow`)를 명확히 분리
    - Context Mapping으로 통합 시 경계 정의
9. **Anti-Corruption Layer**: 외부 시스템 연동 시 도메인 모델 오염 방지
    - Adapter 패키지를 통해 변환

---

문의사항이나 더 깊은 예제가 필요하시면 언제든 알려주세요!