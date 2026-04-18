package com.study.redpanda.ch04;

import com.study.redpanda.ch04.domain.SagaState;
import com.study.redpanda.ch04.domain.SagaStatus;
import com.study.redpanda.ch04.domain.SagaStep;
import com.study.redpanda.ch04.repository.ProcessedCommandRepository;
import com.study.redpanda.ch04.repository.SagaStateRepository;
import com.study.redpanda.ch04.service.TripSagaOrchestrator;
import com.study.redpanda.ch04.service.TripSagaRecoveryScheduler;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.support.TransactionTemplate;

import java.time.Instant;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

/**
 * Ch04 SAGA Orchestration 통합 테스트
 *
 * 로컬 docker-compose 인프라(Redpanda + PostgreSQL)를 사용하여
 * 정상 플로우, 실패+보상, 타임아웃 시나리오를 End-to-End 검증한다.
 *
 * 사전 조건: docker-compose up -d (Redpanda + PostgreSQL 실행 상태)
 *
 * 테스트 시나리오:
 * 1. 정상 플로우: 항공 성공 → 호텔 성공 → COMPLETED
 * 2. Step 1 실패: departure="FAIL" → FAILED (보상 없음)
 * 3. Step 2 실패: hotelName="FAIL" → 항공 취소 → COMPENSATED
 * 4. 타임아웃: Step 2 무응답 → 스케줄러가 보상 트리거 → COMPENSATED
 * 5. 멱등성: 동일 Command 재전송 시 중복 처리 방지 검증
 */
@SpringBootTest
@ActiveProfiles("local")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class TripSagaIntegrationTest {

    /** ch04 SAGA에서 사용하는 토픽 목록 (auto_create_topics_enabled=false 대응) */
    private static final List<String> REQUIRED_TOPICS = List.of(
            "chapter4.commands.flight",
            "chapter4.commands.hotel",
            "chapter4.events.flight-booked",
            "chapter4.events.flight-booking-failed",
            "chapter4.events.flight-cancelled",
            "chapter4.events.hotel-booked",
            "chapter4.events.hotel-booking-failed"
    );

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Autowired
    private TripSagaOrchestrator orchestrator;

    @Autowired
    private TripSagaRecoveryScheduler recoveryScheduler;

    @Autowired
    private SagaStateRepository sagaStateRepository;

    @Autowired
    private ProcessedCommandRepository processedCommandRepository;

    @Autowired
    private ApplicationContext applicationContext;

    private static boolean topicsCreated = false;

    /**
     * 테스트 실행 전 필요한 토픽을 사전 생성한다.
     * auto_create_topics_enabled=false 환경에서 토픽 미존재로 인한 실패를 방지.
     */
    @BeforeEach
    void ensureTopicsExist() throws Exception {
        if (topicsCreated) return;

        try (AdminClient admin = AdminClient.create(
                Map.of(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers))) {
            Set<String> existing = admin.listTopics().names().get(10, TimeUnit.SECONDS);
            List<NewTopic> toCreate = REQUIRED_TOPICS.stream()
                    .filter(t -> !existing.contains(t))
                    .map(t -> new NewTopic(t, 1, (short) 1))
                    .collect(Collectors.toList());
            if (!toCreate.isEmpty()) {
                admin.createTopics(toCreate).all().get(10, TimeUnit.SECONDS);
            }
        }
        topicsCreated = true;
    }

    // ─── Test 1: 정상 플로우 ─────────────────────────────────────────────────

    /**
     * CTP 체인 전체 검증:
     *   startSaga() → BookFlightCommand → FlightBooked
     *     → BookHotelCommand → HotelBooked → COMPLETED
     */
    @Test
    @Order(1)
    @DisplayName("정상 플로우: 항공 성공 → 호텔 성공 → COMPLETED")
    void 정상플로우_항공성공_호텔성공_COMPLETED() {
        // Given
        String tripId = "TRIP-" + UUID.randomUUID().toString().substring(0, 8);

        // When
        String sagaId = orchestrator.startSaga(
                tripId, "ICN", "NRT",
                LocalDate.of(2026, 3, 15),
                "Tokyo Hotel",
                LocalDate.of(2026, 3, 15),
                LocalDate.of(2026, 3, 18));

        // Then
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(1, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    SagaState state = sagaStateRepository.findById(sagaId).orElseThrow();
                    assertThat(state.getStatus()).isEqualTo(SagaStatus.COMPLETED);
                    assertThat(state.getFlightReservationId()).startsWith("FLT-");
                    assertThat(state.getHotelReservationId()).startsWith("HTL-");
                    assertThat(state.getCompletedAt()).isNotNull();
                });
    }

    // ─── Test 2: Step 1 실패 ─────────────────────────────────────────────────

    /**
     * departure="FAIL" → FlightBookingFailed → FAILED
     * Step 1 실패이므로 보상할 대상 없음
     */
    @Test
    @Order(2)
    @DisplayName("Step 1 실패: departure=FAIL → FAILED (보상 없음)")
    void Step1실패_항공실패_보상없이_FAILED() {
        // Given
        String tripId = "TRIP-FAIL1-" + UUID.randomUUID().toString().substring(0, 8);

        // When
        String sagaId = orchestrator.startSaga(
                tripId, "FAIL", "NRT",
                LocalDate.of(2026, 3, 15),
                "Tokyo Hotel",
                LocalDate.of(2026, 3, 15),
                LocalDate.of(2026, 3, 18));

        // Then
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(1, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    SagaState state = sagaStateRepository.findById(sagaId).orElseThrow();
                    assertThat(state.getStatus()).isEqualTo(SagaStatus.FAILED);
                    assertThat(state.getFailedStep()).isEqualTo("FLIGHT_BOOKING");
                    assertThat(state.getFailureReason()).contains("FAIL");
                    assertThat(state.getFlightReservationId()).isNull();
                });
    }

    // ─── Test 3: Step 2 실패 → 보상 ──────────────────────────────────────────

    /**
     * hotelName="FAIL" → HotelBookingFailed
     *   → COMPENSATING → CancelFlightCommand → FlightCancelled → COMPENSATED
     */
    @Test
    @Order(3)
    @DisplayName("Step 2 실패: hotelName=FAIL → 항공 취소 → COMPENSATED")
    void Step2실패_호텔실패_항공취소_COMPENSATED() {
        // Given
        String tripId = "TRIP-FAIL2-" + UUID.randomUUID().toString().substring(0, 8);

        // When
        String sagaId = orchestrator.startSaga(
                tripId, "ICN", "NRT",
                LocalDate.of(2026, 3, 15),
                "FAIL",
                LocalDate.of(2026, 3, 15),
                LocalDate.of(2026, 3, 18));

        // Then
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(1, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    SagaState state = sagaStateRepository.findById(sagaId).orElseThrow();
                    assertThat(state.getStatus()).isEqualTo(SagaStatus.COMPENSATED);
                    assertThat(state.getFailedStep()).isEqualTo("HOTEL_BOOKING");
                    assertThat(state.getFailureReason()).contains("FAIL");
                    assertThat(state.getFlightReservationId()).startsWith("FLT-");
                    assertThat(state.getHotelReservationId()).isNull();
                    assertThat(state.getCompletedAt()).isNotNull();
                });
    }

    // ─── Test 4: 타임아웃 → 보상 ─────────────────────────────────────────────

    /**
     * HOTEL_BOOKING 단계에서 서비스가 무응답인 상황을 시뮬레이션한다.
     *
     * stepStartedAt을 3분 전으로 설정한 SagaState를 DB에 직접 생성하고,
     * 스케줄러를 수동 호출하여 타임아웃 감지 → 보상 플로우를 검증한다.
     *
     * 흐름:
     *   checkTimeouts() → COMPENSATING → CancelFlightCommand
     *     → FlightCommandHandler → FlightCancelled
     *       → Orchestrator.onFlightCancelled() → COMPENSATED
     */
    @Test
    @Order(4)
    @DisplayName("타임아웃: Step 2 무응답 → 스케줄러가 보상 트리거 → COMPENSATED")
    void Step2타임아웃_스케줄러_보상트리거_COMPENSATED() {
        // Given: HOTEL_BOOKING에서 3분째 멈춘 SAGA (2분 타임아웃 초과)
        String sagaId = UUID.randomUUID().toString();
        String tripId = "TRIP-TIMEOUT-" + sagaId.substring(0, 8);

        SagaState stalledSaga = SagaState.builder()
                .sagaId(sagaId)
                .tripId(tripId)
                .currentStep(SagaStep.HOTEL_BOOKING)
                .status(SagaStatus.IN_PROGRESS)
                .departure("ICN")
                .arrival("NRT")
                .travelDate(LocalDate.of(2026, 3, 15))
                .hotelName("Stalled Hotel")
                .checkIn(LocalDate.of(2026, 3, 15))
                .checkOut(LocalDate.of(2026, 3, 18))
                .flightReservationId("FLT-TIMEOUT-01")
                .stepStartedAt(Instant.now().minus(3, ChronoUnit.MINUTES))
                .build();
        sagaStateRepository.save(stalledSaga);

        // When: 타임아웃 스케줄러 수동 실행
        recoveryScheduler.checkTimeouts();

        // Then: 타임아웃 감지 → COMPENSATING → 항공 취소 → COMPENSATED
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(1, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    SagaState state = sagaStateRepository.findById(sagaId).orElseThrow();
                    assertThat(state.getStatus()).isEqualTo(SagaStatus.COMPENSATED);
                    assertThat(state.getFailureReason()).contains("Timeout");
                    assertThat(state.getFailedStep()).isEqualTo("HOTEL_BOOKING");
                    assertThat(state.getCompletedAt()).isNotNull();
                });
    }

    // ─── Test 5: 멱등성 검증 ─────────────────────────────────────────────────

    /**
     * 정상 플로우 완료 후, ProcessedCommand 테이블에 기록이 남아 있는지 확인한다.
     * Handler가 동일 (sagaId, commandType)으로 재처리를 시도하면 스킵된다.
     */
    @Test
    @Order(5)
    @DisplayName("멱등성: 정상 플로우 후 ProcessedCommand 기록 존재 확인")
    void 멱등성_ProcessedCommand_기록확인() {
        // Given: 정상 플로우 실행
        String tripId = "TRIP-IDEM-" + UUID.randomUUID().toString().substring(0, 8);

        String sagaId = orchestrator.startSaga(
                tripId, "ICN", "LAX",
                LocalDate.of(2026, 4, 1),
                "LA Hotel",
                LocalDate.of(2026, 4, 1),
                LocalDate.of(2026, 4, 5));

        // When: SAGA 완료 대기
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(1, TimeUnit.SECONDS)
                .untilAsserted(() -> {
                    SagaState state = sagaStateRepository.findById(sagaId).orElseThrow();
                    assertThat(state.getStatus()).isEqualTo(SagaStatus.COMPLETED);
                });

        // Then: ProcessedCommand에 BOOK_FLIGHT, BOOK_HOTEL 기록 확인
        // tryAcquire()는 @Modifying INSERT 쿼리이므로 TransactionTemplate으로 감싸야 함
        TransactionTemplate txTemplate = new TransactionTemplate(
                applicationContext.getBean("transactionManager", org.springframework.transaction.PlatformTransactionManager.class));

        int bookFlightDup = txTemplate.execute(status ->
                processedCommandRepository.tryAcquire(sagaId, "BOOK_FLIGHT", Instant.now()));
        int bookHotelDup = txTemplate.execute(status ->
                processedCommandRepository.tryAcquire(sagaId, "BOOK_HOTEL", Instant.now()));

        assertThat(bookFlightDup).isZero();  // 이미 처리됨 → 0
        assertThat(bookHotelDup).isZero();   // 이미 처리됨 → 0
    }
}
