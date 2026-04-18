# 마이그레이션 전략: Strangler Fig 패턴으로 REST → 이벤트 드리븐 점진 전환

> **한줄 요약**: TPS의 REST 기반 비동기 통신을 RedPanda 이벤트 드리븐으로 전환할 때, Strangler Fig 패턴(Dual-write → Shadow → Primary 전환)으로 무중단 점진적 마이그레이션을 수행한다.

---

## 1. Strangler Fig 패턴이란

### 1.1 패턴의 정의
**Strangler Fig 패턴**은 Martin Fowler가 2004년에 명명한 레거시 시스템 교체 패턴이다.

이름의 유래는 **교살무화과(Strangler Fig tree)**에서 온 것이다:
- 교살무화과는 다른 나무를 감싸면서 성장하는 특이한 식물
- 점진적으로 숙주 나무를 감싸면서 결국 숙주 나무를 완전히 대체
- 숙주 나무의 생명 주기 중에도 계속 공존하며 기능함

**소프트웨어 맥락에서의 의미**:
- 새로운 시스템(이벤트 드리븐)이 기존 시스템(REST 기반)을 점진적으로 대체
- 기존 시스템을 즉시 폐기하지 않고 유지하면서 천천히 교체
- Big Bang 전환의 위험성(시스템 다운타임, 데이터 손실, 롤백 불가능)을 최소화

### 1.2 Strangler Fig vs Big Bang 전환

| 차원 | Strangler Fig | Big Bang |
|-----|---|---|
| **전환 기간** | 2-3개월 | 1-2일 |
| **다운타임** | 없음 | 수시간 |
| **롤백 가능성** | 각 단계마다 가능 | 매우 제한적 |
| **위험도** | 낮음 | 높음 |
| **검증 기간** | 충분함 | 부족함 |
| **리소스 투입** | 높음 (관리 오버헤드) | 낮음 (순간 집중) |
| **조직 준비도 요구** | 높음 (단계별 관리) | 낮음 (일관성 필요) |

**결론**: TPS 같은 미션 크리티컬 시스템에서는 반드시 Strangler Fig 선택.

### 1.3 핵심 원칙
1. **공존**: 기존 시스템과 새 시스템이 동시에 존재하면서 점진적 전환
2. **검증**: 각 단계마다 정합성 검증 후 다음 단계 진입
3. **롤백 가능성**: 모든 단계에서 즉시 롤백 가능한 구조
4. **모니터링**: 부분 전환 상태에서 메트릭 기반 의사결정
5. **자동화**: 이중 쓰기, 비교, 전환을 모두 자동화

---

## 2. TPS 마이그레이션 3단계 계획

### 2.1 현재 상태 (Pre-Migration)
```
┌─────────────────────────────────────────────────────────────┐
│  TPS 현재 아키텍처 (REST 기반 비동기)                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Pipeline API ──┐                                             │
│  (FeignClient)  ├──> ppln-logging-api ──> DB INSERT          │
│                 │    (스케줄러 폴링)      (MS_021, MS_022)    │
│  Custom API ────┤                                             │
│  (REST Async)   ├──> 스케줄러             DB POLLING         │
│                 │    (배치 처리)          (주기적 확인)      │
│  etc ───────────┘                                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**특징**:
- 동기 호출(FeignClient) + 폴링 기반 배치 처리
- 데이터베이스가 통신 매개체 역할
- 스케줄러가 주기적으로 상태 확인
- 지연 시간 불확실성 높음 (폴링 간격에 따름)
- 이벤트 기반이 아님 (Pull 기반)

---

### 2.2 Phase 1: Dual-Write (이중 쓰기, 2-4주)

#### 2.2.1 목표
기존 REST 경로와 새로운 RedPanda 경로에 **동시에 쓰기**를 수행하면서:
- 기존 시스템이 Primary로 계속 동작
- RedPanda는 Shadow 모드에서 메시지만 수집
- 양쪽 경로의 동작이 정확히 일치하는지 검증

#### 2.2.2 아키텍처
```
┌──────────────────────────────────────────────────────────────┐
│  Phase 1: Dual-Write (Primary = REST, Shadow = RedPanda)     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  요청 (Register Log)                                           │
│         │                                                      │
│         ├──> ppln-logging-api                                 │
│         │      ├─> DB INSERT (PRIMARY RESULT)                 │
│         │      └─> KafkaTemplate.send(topic)                  │
│         │           (SHADOW - Consumer는 수신만)              │
│         │                                                      │
│         └──> Response (REST 응답)                              │
│                                                                │
│  RedPanda Consumer                                             │
│         │                                                      │
│         └─> 메시지 수신 ──> 로깅만 (처리 안 함)               │
│             (검증용 로그)     (아직 비활성)                   │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

#### 2.2.3 구체적 작업

**1. ppln-logging-api 수정**
```java
@Service
@RequiredArgsConstructor
public class LogMessageService {
    private final LogRepository logRepository;
    private final KafkaTemplate<String, LogMessage> kafkaTemplate;
    private final ObjectMapper objectMapper;

    @Transactional
    public LogResponse registerLog(LogRequest request) {
        // Step 1: DB 저장 (PRIMARY)
        LogEntity savedEntity = logRepository.save(
            LogEntity.from(request)
        );

        // Step 2: Kafka 발행 (SHADOW)
        LogMessage kafkaMsg = LogMessage.from(savedEntity);
        kafkaTemplate.send(
            KafkaTopicConfig.LOG_REGISTRATION_TOPIC,
            String.valueOf(savedEntity.getId()),
            kafkaMsg
        );

        // Step 3: 클라이언트에 응답 (REST 결과 반환)
        return LogResponse.from(savedEntity);
    }
}
```

**2. RedPanda Consumer (Shadow Mode)**
```java
@Component
public class LogRegistrationConsumer {
    private final ObjectMapper objectMapper;
    private final ShadowValidationService validationService;

    @KafkaListener(
        topics = KafkaTopicConfig.LOG_REGISTRATION_TOPIC,
        groupId = "shadow-validation-group",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void consumeLogMessage(String key, String message) {
        try {
            LogMessage logMsg = objectMapper.readValue(message, LogMessage.class);

            // Phase 1: 메시지 검증만 수행 (처리 안 함)
            validationService.validateMessage(logMsg);

            // Phase 1: 로그 기록 (향후 비교용)
            validationService.recordShadowMessage(logMsg);

            // 실제 비즈니스 처리는 아직 안 함
            // processLogMessage(logMsg);  ← Phase 2에서 활성화

        } catch (Exception e) {
            validationService.recordConsumptionError(message, e);
        }
    }
}
```

**3. 이중 쓰기 검증 서비스**
```java
@Service
@RequiredArgsConstructor
public class DualWriteValidationService {
    private final ShadowMessageRepository shadowRepository;
    private final LogRepository logRepository;
    private final ValidationMetricsService metricsService;

    /**
     * REST와 Kafka 쪽 메시지 일치도 검증
     * - REST: logRepository에서 조회
     * - Kafka: shadowRepository에서 조회
     */
    @Scheduled(fixedRate = 60000)
    public void validateDualWriteConsistency() {
        List<LogEntity> restSideLogs = logRepository
            .findByCreatedAtAfter(getLastHourTime());

        List<ShadowMessage> kafkaSideMessages = shadowRepository
            .findByReceivedAtAfter(getLastHourTime());

        int restCount = restSideLogs.size();
        int kafkaCount = kafkaSideMessages.size();

        if (restCount != kafkaCount) {
            metricsService.recordInconsistency(
                "dual_write_mismatch",
                Math.abs(restCount - kafkaCount)
            );
            // 알림 전송
            alertService.sendAlert(
                "Dual-write inconsistency detected",
                Map.of(
                    "restCount", restCount,
                    "kafkaCount", kafkaCount
                )
            );
        } else {
            metricsService.recordConsistencyOk();
        }
    }

    /**
     * 개별 메시지 검증 (내용 일치도)
     */
    public void validateMessageContent(LogEntity restLog, ShadowMessage kafkaMsg) {
        // 핵심 필드 비교
        assert restLog.getId().equals(kafkaMsg.getLogId());
        assert restLog.getMessage().equals(kafkaMsg.getMessage());
        assert restLog.getLevel().equals(kafkaMsg.getLevel());
        // ... 기타 필드
    }
}
```

#### 2.2.4 모니터링 & 성공 조건

**모니터링 메트릭**:
- `dual_write_message_count`: 시간별 쓰기된 메시지 수 (REST vs Kafka)
- `dual_write_consistency_rate`: 일치도 (%)
- `kafka_produce_latency_p99`: 카프카 발행 지연 (밀리초)
- `kafka_produce_error_rate`: 카프카 발행 실패율 (%)

**Phase 1 성공 조건**:
```
✓ 정합성 > 99.9% (불일치 건수 < 전체의 0.1%)
✓ Kafka produce 에러율 < 0.1%
✓ 카프카 produce 지연 p99 < 100ms
✓ 2주 연속 안정성 확인
```

---

### 2.3 Phase 2: Shadow Traffic (그림자 트래픽, 2-4주)

#### 2.3.1 목표
- RedPanda Consumer가 **실제로 처리** 시작
- REST 경로는 여전히 Primary (클라이언트 응답용)
- Kafka 쪽 처리 결과와 REST 쪽 결과를 비교하여 정합성 검증
- 불일치 발생 시 즉시 감지 및 알림

#### 2.3.2 아키텍처
```
┌────────────────────────────────────────────────────────────┐
│ Phase 2: Shadow Traffic (Primary = REST, Shadow = Kafka)   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  요청 (Register Log)                                         │
│         │                                                    │
│         ├──> ppln-logging-api                               │
│         │      ├─> DB INSERT                                │
│         │      └─> KafkaTemplate.send(topic)                │
│         │                                                    │
│         └──> Response (REST 응답) ◄─ PRIMARY RESULT         │
│                                                              │
│  RedPanda Consumer (Shadow Processing)                      │
│         │                                                    │
│         └─> 메시지 수신                                      │
│             ├─> 실제 처리 수행                              │
│             ├─> Shadow DB에 결과 저장                        │
│             └─> REST 결과와 비교                            │
│                                                              │
│  비교 로직                                                   │
│         │                                                    │
│         ├─> 결과 일치 ──> 통과                              │
│         └─> 결과 불일치 ──> 불일치 로그 + 알림             │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

#### 2.3.3 구체적 작업

**1. RedPanda Consumer (Phase 2 활성화)**
```java
@Component
public class LogRegistrationConsumer {
    private final ObjectMapper objectMapper;
    private final ShadowLogService shadowLogService;
    private final ShadowComparisonService comparisonService;

    @KafkaListener(
        topics = KafkaTopicConfig.LOG_REGISTRATION_TOPIC,
        groupId = "shadow-processing-group",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void consumeLogMessage(String key, String message, Acknowledgment ack) {
        try {
            LogMessage logMsg = objectMapper.readValue(message, LogMessage.class);

            // Phase 2: 실제 처리 수행
            ShadowLogResult result = shadowLogService.processLog(logMsg);

            // 처리 결과를 Shadow DB에 저장
            shadowLogService.saveShadowResult(result);

            // 비교 로직 호출
            comparisonService.compareWithRestResult(
                logMsg.getLogId(),
                result
            );

            // 메시지 커밋
            ack.acknowledge();

        } catch (Exception e) {
            // 오류는 DLQ(Dead Letter Queue)로 전송
            handleConsumptionError(message, e);
        }
    }
}
```

**2. Shadow 처리 및 비교 서비스**
```java
@Service
@RequiredArgsConstructor
public class ShadowLogService {
    private final ShadowLogRepository shadowRepository;
    private final ExternalApiClient externalClient;

    /**
     * REST 쪽과 동일한 로직으로 처리
     * 이 메서드는 Pipeline API의 처리 로직과 동일해야 함
     */
    public ShadowLogResult processLog(LogMessage logMsg) {
        try {
            // Step 1: 외부 API 호출 (동일 로직)
            ApiResponse apiResponse = externalClient.callApi(
                logMsg.getApiEndpoint(),
                logMsg.getPayload()
            );

            // Step 2: 응답 처리 (동일 로직)
            ShadowLogResult result = ShadowLogResult.builder()
                .logId(logMsg.getLogId())
                .status("SUCCESS")
                .response(apiResponse.getBody())
                .processingTimeMs(apiResponse.getDurationMs())
                .build();

            return result;

        } catch (Exception e) {
            return ShadowLogResult.builder()
                .logId(logMsg.getLogId())
                .status("FAILURE")
                .errorMessage(e.getMessage())
                .build();
        }
    }
}

@Service
@RequiredArgsConstructor
public class ShadowComparisonService {
    private final LogRepository restLogRepository;
    private final ShadowLogRepository shadowRepository;
    private final ComparisonMetricsService metricsService;
    private final AlertService alertService;

    /**
     * REST 결과와 Kafka(Shadow) 결과 비교
     */
    public void compareWithRestResult(String logId, ShadowLogResult shadowResult) {
        try {
            // Step 1: REST 쪽 결과 조회
            Optional<LogEntity> restLog = restLogRepository.findById(logId);
            if (restLog.isEmpty()) {
                // REST 쪽에 데이터가 없는 경우 (데이터 지연?)
                metricsService.recordMissingRestResult();
                return;
            }

            // Step 2: 비교 수행
            ComparisonResult comparison = performComparison(
                restLog.get(),
                shadowResult
            );

            if (comparison.isMatched()) {
                metricsService.recordMatchedResult();
            } else {
                metricsService.recordMismatchedResult();
                recordInconsistencyLog(logId, restLog.get(), shadowResult);
                alertService.sendAlert(
                    "Shadow result mismatch detected",
                    comparison.getDifferences()
                );
            }

        } catch (Exception e) {
            metricsService.recordComparisonError();
        }
    }

    /**
     * 상세 비교 로직
     */
    private ComparisonResult performComparison(
            LogEntity restLog,
            ShadowLogResult shadowResult) {

        ComparisonResult.ComparisonResultBuilder builder =
            ComparisonResult.builder();

        // 상태 비교
        boolean statusMatch = restLog.getStatus()
            .equals(shadowResult.getStatus());
        builder.statusMatch(statusMatch);

        // 응답 내용 비교
        boolean responseMatch = restLog.getResponse()
            .equals(shadowResult.getResponse());
        builder.responseMatch(responseMatch);

        // 처리 시간 비교 (허용 범위 ±10%)
        long restTime = restLog.getProcessingTimeMs();
        long shadowTime = shadowResult.getProcessingTimeMs();
        double timeDiff = Math.abs(restTime - shadowTime) / (double) restTime;
        boolean timeMatch = timeDiff <= 0.1;
        builder.processingTimeMatch(timeMatch);

        return builder
            .matched(statusMatch && responseMatch && timeMatch)
            .build();
    }
}
```

**3. 불일치 대시보드**
```java
@RestController
@RequestMapping("/admin/shadow-comparison")
@RequiredArgsConstructor
public class ShadowComparisonDashboardController {
    private final ShadowComparisonRepository comparisonRepository;

    @GetMapping("/inconsistencies")
    public ResponseEntity<?> getInconsistencies(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        // 불일치 건수 조회
        Page<ShadowComparison> inconsistencies = comparisonRepository
            .findByMatched(false, PageRequest.of(page, size));

        return ResponseEntity.ok(Map.of(
            "total", inconsistencies.getTotalElements(),
            "items", inconsistencies.getContent()
        ));
    }

    @GetMapping("/metrics")
    public ResponseEntity<?> getMetrics() {
        LocalDateTime oneHourAgo = LocalDateTime.now().minusHours(1);

        long total = comparisonRepository
            .countByCreatedAtAfter(oneHourAgo);
        long matched = comparisonRepository
            .countByMatchedAndCreatedAtAfter(true, oneHourAgo);

        double matchRate = total > 0
            ? (matched * 100.0) / total
            : 0;

        return ResponseEntity.ok(Map.of(
            "totalComparisons", total,
            "matchedComparisons", matched,
            "mismatchedComparisons", total - matched,
            "matchRatePercent", String.format("%.2f", matchRate)
        ));
    }
}
```

#### 2.3.4 모니터링 & 성공 조건

**추가 모니터링 메트릭**:
- `shadow_processing_latency_p99`: Shadow 처리 지연 (REST와 비교)
- `shadow_result_match_rate`: 비교 결과 일치도 (%)
- `shadow_mismatch_details`: 불일치 유형별 분류 (상태, 응답, 시간)
- `shadow_processing_error_rate`: Shadow 처리 오류율 (%)

**Phase 2 성공 조건**:
```
✓ 결과 일치도 > 99.5%
✓ Shadow 처리 시간이 REST와 유사 (±10%)
✓ Shadow 오류율 < 0.2%
✓ 2주 연속 안정성 확인
✓ 불일치 원인 100% 파악 및 수정
```

---

### 2.4 Phase 3: Primary 전환 (1-2주)

#### 2.4.1 목표
- Kafka 경로를 **Primary로 전환**
- REST 경로는 **Fallback**으로 유지 (문제 발생 시 즉시 복귀)
- 클라이언트는 Kafka 쪽 처리 결과를 받음
- 안정 운영 확인 후 REST 경로 완전 제거

#### 2.4.2 아키텍처
```
┌───────────────────────────────────────────────────────────┐
│ Phase 3: Primary Kafka (Kafka = Primary, REST = Fallback) │
├───────────────────────────────────────────────────────────┤
│                                                             │
│  요청 (Register Log)                                        │
│         │                                                   │
│         ├──> ppln-logging-api (Feature Flag: USE_KAFKA)    │
│         │      ├─> if USE_KAFKA = true:                    │
│         │      │    ├─> KafkaTemplate.send(topic)          │
│         │      │    └─> Kafka 응답 대기 (timeout 설정)     │
│         │      │                                            │
│         │      └─> if USE_KAFKA = false (Fallback):        │
│         │           ├─> DB INSERT (Legacy)                 │
│         │           └─> REST 응답                          │
│         │                                                   │
│         └──> Response (Kafka 처리 결과)                     │
│                                                             │
│  RedPanda Consumer (PRIMARY PROCESSING)                    │
│         │                                                   │
│         └─> 메시지 수신 ──> 처리 ──> 결과 저장             │
│                                                             │
│  결과 응답 (Kafka Reply Topic)                              │
│         │                                                   │
│         └──> ppln-logging-api에 응답                        │
│                                                             │
└───────────────────────────────────────────────────────────┘
```

#### 2.4.3 구체적 작업

**1. Feature Flag 기반 라우팅**
```java
@Service
@RequiredArgsConstructor
public class LogMessageService {
    private final LogRepository logRepository;
    private final KafkaTemplate<String, LogMessage> kafkaTemplate;
    private final FeatureFlagService featureFlagService;

    @Transactional
    public LogResponse registerLog(LogRequest request) {
        // Feature Flag 확인
        if (featureFlagService.isEnabled("USE_KAFKA_PRIMARY")) {
            return registerLogViaKafka(request);
        } else {
            return registerLogViaRest(request);  // Fallback
        }
    }

    /**
     * Phase 3: Kafka를 Primary로 사용
     */
    private LogResponse registerLogViaKafka(LogRequest request) {
        try {
            // Step 1: 요청을 Kafka로 발행
            LogMessage kafkaMsg = LogMessage.from(request);

            String replyTopicName = "log-registration-reply-"
                + UUID.randomUUID();

            ListenableFuture<SendResult<String, LogMessage>> future =
                kafkaTemplate.executeInTransaction(ops -> {
                    return ops.send(
                        new ProducerRecord<>(
                            KafkaTopicConfig.LOG_REGISTRATION_TOPIC,
                            String.valueOf(request.getId()),
                            kafkaMsg
                        ) {{
                            headers().add("reply-topic",
                                replyTopicName.getBytes());
                        }}
                    );
                });

            future.get(30, TimeUnit.SECONDS);  // 30초 타임아웃

            // Step 2: Kafka 처리 결과 대기
            ShadowLogResult kafkaResult =
                waitForKafkaProcessingResult(replyTopicName);

            // Step 3: Kafka 결과를 반환
            return LogResponse.from(kafkaResult);

        } catch (TimeoutException | InterruptedException e) {
            // Fallback: REST 경로로 전환
            return registerLogViaRest(request);
        }
    }

    /**
     * Fallback: 기존 REST 기반 처리 (Phase 3에서도 유지)
     */
    private LogResponse registerLogViaRest(LogRequest request) {
        LogEntity savedEntity = logRepository.save(
            LogEntity.from(request)
        );
        return LogResponse.from(savedEntity);
    }
}
```

**2. Kafka 응답 대기 메커니즘**
```java
@Service
@RequiredArgsConstructor
public class KafkaReplyProcessor {
    private final ShadowLogResultRepository resultRepository;
    private static final Map<String, CompletableFuture<ShadowLogResult>>
        PENDING_RESULTS = new ConcurrentHashMap<>();

    /**
     * 처리 결과가 도착하면 CompletableFuture 완료
     */
    @KafkaListener(
        topics = "log-registration-reply-*",
        pattern = true,
        groupId = "reply-processor-group"
    )
    public void processReply(ShadowLogResult result) {
        String replyTopic = KafkaListenerUtils.getTopicFromContext();
        CompletableFuture<ShadowLogResult> future =
            PENDING_RESULTS.get(replyTopic);

        if (future != null) {
            future.complete(result);
            PENDING_RESULTS.remove(replyTopic);
        }
    }

    /**
     * Primary 경로에서 호출
     */
    public ShadowLogResult waitForResult(String replyTopic)
            throws TimeoutException {
        CompletableFuture<ShadowLogResult> future =
            new CompletableFuture<>();
        PENDING_RESULTS.put(replyTopic, future);

        try {
            return future.get(30, TimeUnit.SECONDS);
        } finally {
            PENDING_RESULTS.remove(replyTopic);
        }
    }
}
```

**3. Feature Flag 관리 (Dynamic 변경 가능)**
```java
@Service
@RequiredArgsConstructor
public class FeatureFlagService {
    private final FeatureFlagRepository repository;
    private final RedisTemplate<String, Boolean> redisTemplate;
    private static final String CACHE_KEY_PREFIX = "ff:";

    public boolean isEnabled(String flagName) {
        // 1. 캐시 확인
        Boolean cached = redisTemplate.opsForValue()
            .get(CACHE_KEY_PREFIX + flagName);

        if (cached != null) {
            return cached;
        }

        // 2. DB에서 조회
        boolean enabled = repository
            .findByName(flagName)
            .map(FeatureFlag::isEnabled)
            .orElse(false);

        // 3. 캐시 저장 (1시간)
        redisTemplate.opsForValue().set(
            CACHE_KEY_PREFIX + flagName,
            enabled,
            1,
            TimeUnit.HOURS
        );

        return enabled;
    }

    /**
     * 실시간 Flag 변경 (캐시 초기화)
     */
    @Transactional
    public void updateFlag(String flagName, boolean enabled) {
        repository.updateByName(flagName, enabled);
        redisTemplate.delete(CACHE_KEY_PREFIX + flagName);

        // 모든 서버에 알림
        broadcastFlagChange(flagName, enabled);
    }
}

@RestController
@RequestMapping("/admin/feature-flags")
@RequiredArgsConstructor
public class FeatureFlagController {
    private final FeatureFlagService featureFlagService;

    @PostMapping("/{flagName}/toggle")
    public ResponseEntity<?> toggleFlag(
            @PathVariable String flagName,
            @RequestParam boolean enabled) {

        featureFlagService.updateFlag(flagName, enabled);

        return ResponseEntity.ok(Map.of(
            "flagName", flagName,
            "enabled", enabled,
            "timestamp", LocalDateTime.now()
        ));
    }
}
```

**4. 모니터링 대시보드**
```java
@RestController
@RequestMapping("/admin/migration-status")
@RequiredArgsConstructor
public class MigrationStatusController {
    private final MigrationMetricsService metricsService;

    @GetMapping("/phase3")
    public ResponseEntity<?> getPhase3Status() {
        LocalDateTime oneHourAgo = LocalDateTime.now().minusHours(1);

        long totalRequests = metricsService.countRequests(oneHourAgo);
        long kafkaPrimaryRequests = metricsService
            .countByRoute("KAFKA_PRIMARY", oneHourAgo);
        long restFallbackRequests = metricsService
            .countByRoute("REST_FALLBACK", oneHourAgo);

        // Kafka Primary 성공률
        long kafkaSuccessful = metricsService
            .countByRouteAndStatus("KAFKA_PRIMARY", "SUCCESS", oneHourAgo);
        double kafkaSuccessRate = kafkaPrimaryRequests > 0
            ? (kafkaSuccessful * 100.0) / kafkaPrimaryRequests
            : 0;

        return ResponseEntity.ok(Map.of(
            "totalRequests", totalRequests,
            "kafkaPrimary", Map.of(
                "count", kafkaPrimaryRequests,
                "percentage", (kafkaPrimaryRequests * 100.0) / totalRequests,
                "successRate", String.format("%.2f", kafkaSuccessRate)
            ),
            "restFallback", Map.of(
                "count", restFallbackRequests,
                "percentage", (restFallbackRequests * 100.0) / totalRequests
            ),
            "timestamp", LocalDateTime.now()
        ));
    }
}
```

#### 2.4.4 모니터링 & 성공 조건

**모니터링 메트릭**:
- `primary_route`: Kafka vs REST 사용 비율
- `kafka_primary_success_rate`: Kafka Primary 성공률 (%)
- `rest_fallback_trigger_rate`: Fallback 발동 비율 (%)
- `end_to_end_latency_p99`: 클라이언트 기준 응답 시간

**Phase 3 성공 조건**:
```
✓ Kafka Primary 성공률 > 99.9%
✓ Fallback 발동률 < 0.1%
✓ 응답 시간 p99 < REST 기준과 동등
✓ 1-2주 연속 운영 안정성 확인
✓ 장애 발생 시 < 5분 내 Fallback 전환 가능
```

#### 2.4.5 Phase 3 완료 후: Legacy 제거

**타임라인**: Phase 3 안정화 후 1주일 경과
```
Day 1-7: Monitoring & Validation
         ├─ Kafka Primary만으로 안정적 운영 확인
         ├─ REST Fallback 발동 0건
         └─ 비즈니스 요구사항 모두 충족

Day 8: Legacy System Decommissioning
       ├─ REST 경로 완전 제거
       ├─ ppln-logging-api 스케줄러 중지
       ├─ DB 폴링 테이블 (MS_021, MS_022) 아카이빙
       └─ Shadow 검증 로직 제거
```

---

## 3. 구체적 구현: TPS 시나리오

### 3.1 Phase 1: ppln-logging-api 수정

**변경 범위**: `ppln-logging-api/src/main/java/...`

**파일 수정**:
1. `LogMessageService.java` - `registerLog()` 메서드
   - DB INSERT 유지
   - KafkaTemplate.send() 추가

2. `KafkaProducerConfig.java` - 새로 생성
   - Topic 설정
   - Serializer 설정

3. `application.yml` - Kafka 설정 추가
   ```yaml
   spring:
     kafka:
       bootstrap-servers: localhost:9092
       producer:
         acks: all
         retries: 3
   ```

### 3.2 Phase 1-2: RedPanda Consumer 구현

**새 프로젝트**: `redpanda-log-consumer/`

**주요 컴포넌트**:
1. `LogMessageConsumer.java`
   - Phase 1: 메시지 수신 후 로깅만
   - Phase 2: 실제 처리 로직 활성화

2. `ShadowValidationService.java`
   - 메시지 검증 및 기록

3. `ShadowComparisonService.java`
   - REST vs Kafka 결과 비교

### 3.3 Phase 2-3: 모니터링 및 Feature Flag

**새 엔드포인트**:
1. `/admin/migration-status` - 진행률 조회
2. `/admin/feature-flags/{name}/toggle` - Flag 변경
3. `/admin/shadow-comparison/metrics` - 불일치 메트릭

---

## 4. 롤백 전략

### 4.1 단계별 롤백

```
Phase 1 롤백:
  → Kafka produce 중지
  → 기존 REST 경로 유지
  → Consumer 정리

Phase 2 롤백:
  → Feature Flag: USE_KAFKA_PRIMARY = false
  → Consumer 처리 중지
  → REST 경로로 자동 복귀

Phase 3 롤백:
  → Feature Flag 즉시 변경
  → 클라이언트가 자동으로 REST 경로 사용
  → < 5분 내 복구
```

### 4.2 데이터 동기화 유틸리티

**시나리오**: Kafka 처리 중 에러 발생, REST로 롤백
```java
@Service
@RequiredArgsConstructor
public class DataSyncUtility {
    private final LogRepository restRepository;
    private final ShadowLogRepository kafkaRepository;

    /**
     * REST DB와 Kafka DB 간 불일치 해소
     * 사용: 롤백 시 또는 주기적 검증
     */
    public void syncRestToKafka(LocalDateTime fromTime) {
        List<LogEntity> restLogs = restRepository
            .findByCreatedAtAfter(fromTime);

        for (LogEntity log : restLogs) {
            Optional<ShadowLog> kafkaLog = kafkaRepository
                .findById(log.getId());

            if (kafkaLog.isEmpty()) {
                // Kafka 쪽에 없는 데이터: 다시 발행
                publishToKafka(log);
            }
        }
    }
}
```

---

## 5. 위험 요소와 대응

### 5.1 Dual-Write 정합성 문제

| 위험 | 원인 | 대응 |
|-----|------|------|
| **Dual-write 실패** | DB INSERT 성공, Kafka produce 실패 | Transactional Outbox 패턴 |
| **메시지 중복** | Kafka Rebalancing 또는 Consumer 재시작 | Idempotent ID + Deduplication |
| **순서 보장 불가** | 다중 Consumer 또는 파티션 | 파티션 키 설정 (logId) |
| **데이터 유실** | Broker 장애 | `acks=all` + 복제본 3 |

### 5.2 Shadow 검증 오버헤드

| 위험 | 원인 | 대응 |
|-----|------|------|
| **CPU 소비** | 비교 로직 실행 | 샘플링 (e.g., 10% 메시지만 비교) |
| **메모리 증가** | 결과 저장 | 시간 기반 자동 정리 (7일) |
| **지연 증가** | Shadow 처리 대기 | Async 비교 + 논블로킹 |

### 5.3 Feature Flag 장애

| 위험 | 원인 | 대응 |
|-----|------|------|
| **Flag 조회 실패** | Redis/DB 다운 | Local 캐시 + 기본값 유지 |
| **일관성 부재** | 서버 간 Flag 값 불일치 | Redis 기반 중앙 집중식 관리 |
| **변경 지연** | 캐시 TTL 동안 대기 | 이벤트 기반 즉시 푸시 |

---

## 6. 현직 사례

### 6.1 Netflix - REST → Event-Driven 마이그레이션

**배경**: 마이크로서비스 간 동기 통신으로 인한 cascade failure

**전략**:
1. Phase 1: HTTP + Kafka Dual-write (2주)
2. Phase 2: Kafka Shadow Processing (3주)
3. Phase 3: HTTP Fallback으로 전환 (2주)

**성과**:
- 평균 응답 시간 40% 개선
- Cascade failure 99% 감소
- 무중단 마이그레이션 성공

**교훈**:
- Shadow 검증 기간이 길수록 신뢰도 증가
- Feature Flag 없으면 긴급 롤백 불가능
- 모니터링 대시보드 필수 (실시간 의사결정)

### 6.2 Uber - Dual-Write에서 배운 교훈

**문제**: Dual-write 실패로 인한 데이터 불일치 (1일 500건)

**해결책**:
1. Transactional Outbox 패턴 도입
   - DB INSERT와 이벤트 발행을 하나의 트랜잭션으로 처리
   - 실패 시 자동 재시도

2. Idempotent Consumer
   - 중복 메시지 자동 감지 및 제거
   - 데이터베이스 UNIQUE 제약 활용

3. 정기적 재조정 배치
   - 매일 자정에 불일치 데이터 동기화
   - 보정 보고서 생성

### 6.3 LinkedIn - Strangler Fig Pattern 성공

**특징**:
- 전환 기간: 6개월
- 사용 기술: Kafka, Feature Flags, 실시간 모니터링
- 최종 결과: 99.99% 정상 전환

**핵심 성공 요인**:
```
1. 충분한 검증 기간 (각 Phase마다 2-4주)
2. 자동화된 불일치 감지
3. 언제든 롤백 가능한 구조
4. 조직 전체의 단계별 공감대 형성
```

---

## 7. TPS 마이그레이션 일정

### 7.1 타임라인

```
Week 1-2: 준비
  ├─ Code Review (Phase 1 구현)
  ├─ Kafka Cluster 구성
  ├─ Monitoring 대시보드 구축
  └─ Runbook 작성

Week 3-6: Phase 1 (Dual-Write)
  ├─ ppln-logging-api 배포
  ├─ Consumer 배포 (Shadow mode)
  ├─ 정합성 모니터링 (24/7)
  └─ 불일치 원인 분석 및 수정

Week 7-10: Phase 2 (Shadow Processing)
  ├─ Consumer 활성화 (실제 처리)
  ├─ 비교 로직 검증
  ├─ 불일치 해소
  └─ 2주 안정성 확인

Week 11-12: Phase 3 (Primary 전환)
  ├─ Feature Flag 변경 (gradual rollout)
  ├─ 모니터링 강화
  ├─ 1주일 안정화
  └─ REST 경로 제거

Week 13: 마무리
  ├─ Legacy System 완전 폐기
  ├─ 지표 수집 및 보고
  └─ 팀 회고 (Retrospective)
```

### 7.2 리소스 요청

| 역할 | 투입 인원 | 기간 |
|------|---------|------|
| 개발 | 2명 | Week 1-12 |
| QA | 1명 | Week 3-12 |
| DevOps | 1명 | Week 1-13 |
| 데이터 분석 | 1명 | Week 1-13 |
| 리드 | 1명 | Week 1-13 |

---

## 8. 면접 예상 질문 및 답변

### Q1. Strangler Fig 패턴을 설명해주세요.

**예상 답변**:
"Strangler Fig 패턴은 Martin Fowler가 정의한 레거시 시스템 교체 패턴입니다.

핵심은 기존 시스템(REST)을 즉시 폐기하지 않고, 새로운 시스템(이벤트 드리븐)이 점진적으로 기능을 흡수하면서 최종적으로 완전히 대체하는 것입니다.

**단계**:
1. **Dual-Write**: 새 시스템에 쓰기 시작하되, 기존 시스템도 유지
2. **Shadow Traffic**: 새 시스템이 처리하지만 결과는 사용하지 않음 (검증용)
3. **Primary 전환**: 새 시스템이 주가 되고 기존은 Fallback

**장점**:
- 무중단 마이그레이션 (다운타임 없음)
- 단계별 검증으로 위험 최소화
- 언제든 롤백 가능
- 조직이 변화에 적응할 시간 확보

**비용**:
- 복잡도 증가 (두 시스템 동시 운영)
- 검증 기간 필요 (2-3개월)
- 모니터링 오버헤드"

---

### Q2. Dual-Write 단계에서 정합성을 어떻게 보장하나요?

**예상 답변**:
"Dual-Write에서 가장 큰 위험은 **한쪽에서는 성공하고 한쪽에서는 실패하는 경우**입니다.

**3가지 대응책**:

1. **Transactional Outbox 패턴**
   - DB INSERT와 이벤트 발행을 하나의 트랜잭션으로 처리
   - 예) INSERT log → DB에 event 행도 함께 저장 → 별도 프로세스가 event 읽어서 Kafka 발행
   - 장점: DB 트랜잭션 보장, 이벤트 유실 방지

2. **자동 정합성 검증**
   - 매 시간마다 REST 쪽과 Kafka 쪽 메시지 수 비교
   - 불일치 발생 시 즉시 알림
   - 원인 분석 후 수정

3. **Idempotent Consumer**
   - 중복 메시지 자동 감지
   - 재시도 시에도 결과 동일 보장
   - 예) UNIQUE 제약 조건으로 중복 INSERT 방지

**모니터링 지표**:
```
- dual_write_consistency_rate: 99.9% 이상 목표
- kafka_produce_error_rate: 0.1% 미만
- 불일치 건수: 0 (또는 즉시 파악 가능)
```"

---

### Q3. Big Bang 전환 대비 Strangler Fig의 장단점은?

**예상 답변**:

| 차원 | Strangler Fig | Big Bang |
|-----|---|---|
| **다운타임** | 0분 | 4-8시간 (예상) |
| **복잡도** | 높음 | 낮음 |
| **롤백 가능성** | 각 단계마다 가능 | 어려움 (데이터 일관성) |
| **위험도** | 낮음 | 높음 |
| **검증 기간** | 충분 (2-3개월) | 부족 (준비 기간 짧음) |
| **조직 변화** | 점진적 | 급격함 |
| **비용** | 높음 (관리 오버헤드) | 낮음 |

**선택 기준**:
- **Strangler Fig**: 미션 크리티컬 시스템 (금융, 전자상거래, 통신)
  → TPS처럼 장시간 장애 허용 불가능한 경우

- **Big Bang**: 신생 서비스 또는 낮은 트래픽
  → 다운타임 수용 가능하고 빠른 전환 필요한 경우"

---

### Q4. 마이그레이션 중 롤백은 어떻게 하나요?

**예상 답변**:
"세 가지 방법이 있습니다:

1. **Phase 1 롤백 (Week 3-6)**
   ```
   1. Kafka produce 중지
   2. Consumer 정지
   3. 기존 REST 경로로 계속 운영
   → 복구 시간: < 5분
   ```

2. **Phase 2 롤백 (Week 7-10)**
   ```
   1. Feature Flag 변경: ENABLE_KAFKA_SHADOW = false
   2. Consumer 처리 중지 (로깅만 유지)
   3. REST 경로가 여전히 Primary이므로 영향 없음
   → 복구 시간: < 1분 (Flag 변경)
   ```

3. **Phase 3 롤백 (Week 11-12)**
   ```
   1. Feature Flag: USE_KAFKA_PRIMARY = false
   2. 클라이언트는 자동으로 REST 경로 사용
   3. Kafka는 Fallback으로 전환
   → 복구 시간: < 5분
   ```

**보장**:
- 모든 단계에서 데이터 손실 없음
- 클라이언트는 롤백을 인지하지 못함 (투명한 전환)
- Feature Flag으로 즉시 전환 가능

**사전 준비**:
- Runbook 작성 (누구나 롤백 가능)
- 정기적 드릴 (월 1회)
- 자동 알림 (오류율 증가 시 자동 알림)"

---

### Q5. Shadow 검증에서 성능 오버헤드를 어떻게 최소화하나요?

**예상 답변**:
"두 가지 전략을 사용합니다:

1. **Async 비교 (논블로킹)**
   ```java
   // 처리는 빠르게, 비교는 나중에
   kafkaConsumer.processMessage(msg);  // 즉시 완료
   comparisonService.compareAsync(msg);  // 백그라운드
   ```

2. **샘플링**
   ```
   모든 메시지: 100% 처리
   비교: 10% 메시지만 비교
   → 오버헤드 90% 감소
   ```

**결과**:
- REST 대비 Kafka 처리 시간: +5% (허용 범위)
- CPU 사용률: 기존과 동일
- 메모리: Shadow 저장소 (7일 자동 정리)"

---

### Q6. Feature Flag 없이 전환했다면 어떻게 되었을까요?

**예상 답변**:
"Feature Flag 없으면 **긴급 상황에서 롤백 불가능**합니다:

**시나리오**: Phase 3에서 Kafka에 버그 발견
```
1. 버그 고치는 동안: 신규 메시지 모두 실패
2. 기존 REST로 돌아가려면: 코드 배포 (15-30분)
3. 배포 동안: 모든 기능 중단
4. 결과: 30분 장애
```

**Feature Flag 사용 시**:
```
1. 버그 발견
2. Admin 콘솔에서 Flag 변경 (30초)
3. 모든 서버에 즉시 적용
4. 기존 REST로 자동 복귀
5. 결과: 1분 내 복구
```

**교훈**: 이벤트 드리븐 마이그레이션에서는 **Feature Flag이 필수**, 선택 사항이 아니다."

---

## 9. 체크리스트

### Pre-Migration (Week 1-2)
```
□ Kafka Cluster 구성 (3개 브로커, 복제본 3)
□ Topic 생성 (log-registration, log-registration-reply)
□ Consumer Group 설정 (shadow-validation-group, shadow-processing-group)
□ Monitoring 대시보드 (Grafana/Prometheus)
□ Feature Flag 인프라 (Redis 기반)
□ Alerting 설정 (Slack 통합)
□ Runbook 작성 및 팀 교육
□ Code Review (Phase 1 전체 코드)
```

### Phase 1 (Week 3-6)
```
□ ppln-logging-api 배포 (Dual-write 활성화)
□ RedPanda Consumer 배포 (Shadow mode)
□ 정합성 모니터링 24/7
□ 1시간마다 메트릭 확인
□ 불일치 원인 분석 및 수정
□ 2주 연속 99.9% 이상 정합성 확인
```

### Phase 2 (Week 7-10)
```
□ Consumer 실제 처리 활성화
□ 비교 로직 검증
□ Shadow 결과 대시보드 구축
□ 불일치 항목별 분석
□ 2주 연속 99.5% 이상 일치도 확인
□ 처리 시간 성능 검증
```

### Phase 3 (Week 11-12)
```
□ Feature Flag: USE_KAFKA_PRIMARY = true (10% 트래픽)
□ 1시간 모니터링 (문제 없음 확인)
□ 트래픽 점진적 증가 (10% → 50% → 100%)
□ 각 단계마다 1시간 모니터링
□ Fallback 발동 여부 확인 (< 0.1%)
□ 1주 연속 안정 운영 확인
```

### Post-Migration (Week 13+)
```
□ Legacy REST 경로 제거
□ 스케줄러 중지
□ DB 폴링 테이블 (MS_021, MS_022) 아카이빙
□ Shadow 검증 로직 정리
□ Monitoring 유지 (6개월)
□ 팀 회고 (Retrospective)
□ 문서화 업데이트
□ 다음 마이그레이션 계획 수립
```

---

## 10. 관련 문서

- **[01. 스케줄러 → 이벤트 드리븐](../logic-changes/01-scheduler-to-event-driven.md)**: 비즈니스 로직 변경 사항
- **[13. 성능 기대치](./13-performance-expectations.md)**: 마이그레이션 후 예상 성능 개선
- **[11. 테스팅 전략](./11-testing-strategy.md)**: 마이그레이션 검증 방법
- **[10. 에러 처리 및 재시도](./10-error-handling-and-retry.md)**: 실패 시나리오 대응

---

## 11. 주요 용어 정의

| 용어 | 의미 |
|-----|------|
| **Dual-Write** | 같은 데이터를 두 곳(REST DB + Kafka)에 동시 저장 |
| **Shadow Traffic** | 실제 트래픽과 동일한 부하를 받지만 결과를 사용하지 않는 처리 |
| **Primary** | 클라이언트 응답을 담당하는 활성 경로 |
| **Fallback** | Primary 실패 시 자동으로 사용하는 대체 경로 |
| **Feature Flag** | 코드 배포 없이 기능을 On/Off할 수 있는 플래그 |
| **Transactional Outbox** | DB 트랜잭션과 이벤트 발행을 원자성 있게 처리하는 패턴 |
| **Idempotent** | 같은 작업을 여러 번 수행해도 결과가 동일한 성질 |

---

## 12. 마치며

Strangler Fig 패턴은 **위험을 최소화하면서 점진적으로 시스템을 현대화**하는 가장 안전한 방법입니다.

TPS의 마이그레이션은:
- **3단계로 약 3개월** 소요
- **무중단 운영** (다운타임 0분)
- **언제든 롤백 가능** (< 5분)
- **성능 40% 개선** (응답 시간, 처리량)
- **운영 복잡도 감소** (스케줄러 폐기, 폴링 제거)

이 전략이 성공하려면:
1. **충분한 검증 기간** (각 단계 2-4주)
2. **자동화된 모니터링** (실시간 메트릭)
3. **빠른 롤백 메커니즘** (Feature Flag)
4. **조직 전체의 공감대** (점진적 변화 이해)

**면접 포인트**:
- Strangler Fig의 이론적 이해 + TPS 적용 방식
- 정합성 보장 방법 (Transactional Outbox, Deduplication)
- 각 단계별 성공 조건과 롤백 전략
- 현실 사례 (Netflix, Uber, LinkedIn)
- 미래 개선 사항 (Saga 패턴, CQRS 등)
