# TPS workflow-api 로깅/트레이싱 현황 분석

> 작성일: 2024-12-22 (Day 1)

## 1. 개요

현재 TPS workflow-api의 로깅 및 트레이싱 현황을 분석하여 개선 포인트를 도출한다.

## 2. 현황 요약

| 항목 | 현재 상태 | 문제점 |
|------|----------|--------|
| 로깅 | Slf4j 기반 | 분산 환경 추적 불가 |
| AOP 트레이싱 | LogAspect (로컬만) | 프로덕션에서 비활성화 |
| 서비스 간 통신 | FeignClient (동기) | 장애 전파, 추적 불가 |
| TraceID | 미적용 | 요청 흐름 추적 불가 |

## 3. 상세 분석

### 3.1 LogAspect.java 분석

**파일 위치**: `infrastructure/support/aop/LogAspect.java`

```java
@Aspect
@Component(value = "LogAspectV3")
@Profile("local")  // 문제점 1: 로컬에서만 동작
@ConditionalOnProperty(name = "trb.release.version", havingValue = "v3.0.5")
@RequiredArgsConstructor
public class LogAspect {
    private final LogTrace logTrace;

    @Pointcut("execution(* org.okestro.tps.api.v3.domain..*.*(..)) && !within(*..mapper..*)")
    public void allComponent(){};

    @Pointcut("execution(* org.okestro.tps.api.v3.application..*.*(..)) && !within(*..mapper..*)")
    public void allService(){};

    @Pointcut("execution(* org.okestro.tps.api.v3.infrastructure.persistence.*.*(..)) && !within(*..mapper..*)")
    public void allPersistence(){};

    @Pointcut("execution(* org.okestro.tps.api.v3.presentation.*.event.*.*(..))")
    public void allEventListener(){};

    @Around("allComponent() || allService() || allPersistence() || allEventListener()")
    public Object logTrace(ProceedingJoinPoint joinPoint) throws Throwable {
        TraceStatus status = logTrace.begin(joinPoint.getSignature().toShortString());
        // 문제점 2: 단일 서비스 내 추적만 가능
        // 문제점 3: 분산 TraceID 개념 없음
    }
}
```

**문제점 상세:**

| 문제 | 설명 | 영향 |
|------|------|------|
| `@Profile("local")` | 로컬 환경에서만 동작 | 운영 환경에서 추적 불가 |
| `TraceStatus` 사용 | 단일 서비스 내 추적만 가능 | 서비스 간 호출 연결 불가 |
| 조건부 활성화 | `v3.0.5` 버전에서만 동작 | 버전별 동작 불일치 |

**추적 범위:**
- `v3.domain..*` - 도메인 레이어
- `v3.application..*` - 애플리케이션 레이어
- `v3.infrastructure.persistence.*` - 영속성 레이어
- `v3.presentation.*.event.*` - 이벤트 리스너

### 3.2 TicketEventPublisher.java 분석

**파일 위치**: `infrastructure/external/ticket/TicketEventPublisher.java`

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class TicketEventPublisher {

    private final TicketPreparationFeignClient feignClient;

    public List<PublishResult> publish(List<TicketPreparationEvent<?>> events) {
        List<AsyncMessageRequest> messageRequests = toAsyncMessageRequests(events);

        return messageRequests.stream()
                .map(this::publishAndGetResult)  // 동기 처리
                .collect(Collectors.toList());
    }

    private PublishResult publishAndGetResult(AsyncMessageRequest request) {
        String eventNo = request.getSpclKey();
        try {
            log.info("Publishing event [{}].", eventNo);
            feignClient.publishEvent(request);  // 동기 FeignClient 호출
            log.info("Event [{}] published successfully.", eventNo);
            return PublishResult.success(eventNo);
        } catch (FeignException e) {
            log.error("Failed to publish event [{}]. Error: {}", eventNo, e.getMessage());
            return PublishResult.failure(eventNo, e.getMessage());
        }
    }
}
```

**문제점 상세:**

| 문제 | 설명 | 영향 |
|------|------|------|
| 동기 호출 | `feignClient.publishEvent()` 응답 대기 | API 응답 지연 |
| 장애 전파 | ppln-logging-api 장애 시 영향 | 티켓 생성 실패 |
| 스레드 점유 | 네트워크 대기 시간 동안 블로킹 | 성능 저하 |
| 단순 예외 처리 | `FeignException`만 처리 | 재시도 로직 없음 |

**호출 흐름:**
```
┌─────────────────┐     동기 호출      ┌──────────────────────┐
│ TcktMngService  │ ───────────────► │ TicketEventPublisher │
└─────────────────┘                   └──────────┬───────────┘
                                                 │
                                            FeignClient
                                            (동기 호출)
                                                 │
                                                 ▼
                                      ┌──────────────────┐
                                      │  ppln-logging-api │
                                      └──────────────────┘
```

### 3.3 FeignClient 현황

workflow-api에서 사용 중인 FeignClient 목록 (4개):

#### 3.3.1 TicketPreparationFeignClient

```java
@FeignClient(
    name = "pipeline-integration-feign",
    url = "${trb.services.ppln-logging-api.url}/ppln-logging/api",
    configuration = FeignConfig.class
)
public interface TicketPreparationFeignClient {
    @PostMapping("/v3/message/register")
    TpsResponse<Void> publishEvent(@RequestBody @Valid AsyncMessageRequest publishRequest);
}
```

| 항목 | 값 |
|------|-----|
| 대상 서비스 | ppln-logging-api |
| 용도 | 이벤트 발행 |
| 엔드포인트 | `/v3/message/register` |

#### 3.3.2 PipelineIntgrtdClient

```java
@FeignClient(
    name = "pipeline-integration-feign",
    url = "${trb.services.pipeline-api.url}/pipeline/api/ticket-integration/v2",
    configuration = FeignConfig.class
)
public interface PipelineIntgrtdClient {
    @PostMapping("/{ticketNo}/reset")
    TpsResponse<Void> resetTicket(...);

    @PostMapping("/{ticketNo}/create")
    TpsResponse<Void> createTicket(...);

    @PostMapping("/{ticketNo}/remove")
    TpsResponse<TcktRemoveResult> removeTicket(...);

    @PostMapping("/{ticketNo}/complete")
    TpsResponse<TcktCompleteResult> completeTicket(...);
}
```

| 항목 | 값 |
|------|-----|
| 대상 서비스 | pipeline-api |
| 용도 | 티켓 연계 (초기화/등록/삭제/완료) |
| 엔드포인트 | `/ticket-integration/v2/*` |

#### 3.3.3 CommonFeignClient

```java
@RefreshScope
@FeignClient(name = "common-feign", url = "${trb.services.common-api.url}/common/api/")
public interface CommonFeignClient {
    @GetMapping("/taskUser/v1/user/select_list/taskCd/{taskCd}")
    TpsResponse<List<UserDto>> selectMappingUserByTaskCd(@PathVariable("taskCd") String taskCd);
}
```

| 항목 | 값 |
|------|-----|
| 대상 서비스 | common-api |
| 용도 | 업무코드별 사용자 조회 |
| 엔드포인트 | `/taskUser/v1/user/select_list/*` |

#### 3.3.4 PmsFeignClient

```java
@RefreshScope
@FeignClient(name = "pms-feign", url = "${trb.services.pms-api.url}/pms/api/", configuration = FeignConfig.class)
public interface PmsFeignClient {
    @GetMapping("/requirement/v1/select_list/{bizCd}/by_misn_id")
    TpsResponse<List<ReqmntDto>> selectRequirementListByMisnIdList(...);

    @GetMapping("/user/v1/select_list/member/{bizCd}")
    TpsResponse<List<MemberDto>> selectProjectMemberList(...);
}
```

| 항목 | 값 |
|------|-----|
| 대상 서비스 | pms-api |
| 용도 | 요구사항/프로젝트 멤버 조회 |
| 엔드포인트 | `/requirement/*`, `/user/*` |

### 3.4 FeignClient 공통 문제점

| 문제 | 설명 |
|------|------|
| 동기 방식 | 모든 호출이 응답 대기 필요 |
| Circuit Breaker 미적용 | 장애 서비스 호출 계속 시도 |
| TraceID 전파 없음 | 서비스 간 요청 추적 불가 |
| Fallback 없음 | 장애 시 대체 로직 없음 |

## 4. 서비스 간 통신 구조

```
                         ┌─────────────────┐
                         │  workflow-api   │
                         │     (8089)      │
                         └────────┬────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ppln-logging   │     │   pipeline-api  │     │   common-api    │
│      -api       │     │     (8085)      │     │                 │
│                 │     │                 │     │                 │
│ - 이벤트 발행   │     │ - 티켓 연계     │     │ - 사용자 조회   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │    pms-api      │
                                                │                 │
                                                │ - 요구사항 조회 │
                                                │ - 멤버 조회     │
                                                └─────────────────┘
```

## 5. 현재 상태 평가

| 항목 | 점수 | 상태 | 설명 |
|------|------|------|------|
| 분산 트레이싱 | 0% | ❌ | TraceID 없음, 로컬에서만 AOP 동작 |
| 비동기 처리 | 0% | ❌ | 모든 FeignClient 동기 호출 |
| 장애 격리 | 0% | ❌ | Circuit Breaker 없음 |
| 로그 통합 | 30% | ⚠️ | 로그는 있으나 연관 분석 불가 |

## 6. 개선 방향

### 6.1 분산 트레이싱 도입 (Week 1)

**목표:** Micrometer Tracing + Zipkin 기반 추적 시스템 구축

```java
// 개선된 LogAspect (제안)
@Aspect
@Component
public class DistributedLogAspect {
    private final Tracer tracer;

    @Around("allService()")
    public Object logWithTrace(ProceedingJoinPoint joinPoint) throws Throwable {
        Span currentSpan = tracer.currentSpan();
        String traceId = currentSpan != null ?
            currentSpan.context().traceId() : "N/A";

        MDC.put("traceId", traceId);
        log.info("[{}] Starting: {}", traceId, joinPoint.getSignature());

        try {
            return joinPoint.proceed();
        } finally {
            log.info("[{}] Completed: {}", traceId, joinPoint.getSignature());
            MDC.clear();
        }
    }
}
```

**필요 의존성:**
```gradle
implementation 'io.micrometer:micrometer-tracing-bridge-brave'
implementation 'io.zipkin.reporter2:zipkin-reporter-brave'
```

### 6.2 FeignClient TraceID 전파

Spring Boot 3.x + Micrometer Tracing 조합 시 자동 전파:

```yaml
# application.yml
management:
  tracing:
    sampling:
      probability: 1.0  # 개발 환경에서 100% 샘플링
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans
```

### 6.3 비동기 전환 (Week 2-3)

```java
// 현재 (동기)
feignClient.publishEvent(request);

// 개선 (비동기 - Kafka)
kafkaTemplate.send("ticket-events", event);
```

## 7. 예상 개선 효과

| 개선 항목 | 현재 | 개선 후 |
|----------|------|--------|
| 장애 추적 시간 | 수십 분 | 수 분 |
| 서비스 간 추적 | 불가 | 가능 (TraceID) |
| 로그 통합 조회 | 개별 서비스 접근 | 중앙화 (Zipkin UI) |
| 장애 격리 | 불가 | 가능 (비동기 전환 시) |

## 8. 다음 단계

| 일차 | 작업 |
|------|------|
| Day 2 | Zipkin Docker 환경 구성 |
| Day 3 | Micrometer Tracing 의존성 추가 실험 |
| Day 4 | FeignClient TraceID 전파 확인 |
| Day 5 | LogAspect 개선안 구현 및 테스트 |

## 9. 참고 파일 위치

```
workflow-api/src/main/java/org/okestro/tps/api/v3/
├── infrastructure/
│   ├── support/aop/
│   │   └── LogAspect.java              # 현재 AOP 로깅
│   └── external/
│       ├── client/                      # FeignClient 정의
│       │   ├── CommonFeignClient.java
│       │   ├── PmsFeignClient.java
│       │   ├── PipelineIntgrtdClient.java
│       │   └── TicketPreparationFeignClient.java
│       └── ticket/
│           └── TicketEventPublisher.java    # 이벤트 발행
└── application/
    ├── service/ticket/                  # 티켓 서비스
    └── event/                           # 이벤트 리스너
```
