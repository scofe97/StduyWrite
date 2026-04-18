package com.study.redpanda.ch04.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.study.redpanda.avro.trip.TripFlightBooked;
import com.study.redpanda.avro.trip.TripFlightBookingFailed;
import com.study.redpanda.avro.trip.TripFlightCancelled;
import com.study.redpanda.avro.trip.TripHotelBooked;
import com.study.redpanda.avro.trip.TripHotelBookingFailed;
import com.study.redpanda.ch04.command.BookFlightCommand;
import com.study.redpanda.ch04.command.BookHotelCommand;
import com.study.redpanda.ch04.command.CancelFlightCommand;
import com.study.redpanda.ch04.domain.OutboxEvent;
import com.study.redpanda.ch04.domain.SagaState;
import com.study.redpanda.ch04.domain.SagaStatus;
import com.study.redpanda.ch04.domain.SagaStep;
import com.study.redpanda.ch04.event.FlightBooked;
import com.study.redpanda.ch04.event.FlightBookingFailed;
import com.study.redpanda.ch04.event.FlightCancelled;
import com.study.redpanda.ch04.event.HotelBooked;
import com.study.redpanda.ch04.event.HotelBookingFailed;
import com.study.redpanda.ch04.event.mapper.TripSagaEventMapper;
import com.study.redpanda.ch04.repository.OutboxEventRepository;
import com.study.redpanda.ch04.repository.SagaStateRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.github.f4b6a3.uuid.UuidCreator;

import java.time.Instant;
import java.time.LocalDate;

/**
 * Trip SAGA Orchestrator — 중앙 조율자
 *
 * <h3>Transactional Outbox 패턴</h3>
 *
 * Command를 Kafka로 직접 전송하지 않고, DB outbox 테이블에 저장한다.
 * SagaState와 OutboxEvent가 동일 DB 트랜잭션 내에서 커밋되므로
 * Dual-Write 불일치가 원천적으로 불가능하다.
 *
 * <pre>
 * ┌─────────────────────────────────────────────────────┐
 * │ 단일 DB TX (@Transactional)                         │
 * │  1. sagaStateRepository.save(state)                 │
 * │  2. outboxEventRepository.save(outboxEvent)         │
 * │  → 원자적 커밋: 둘 다 성공 or 둘 다 롤백             │
 * └─────────────────────────────────────────────────────┘
 *
 * ┌─────────────────────────────────────────────────────┐
 * │ OutboxPublisher (별도 폴링 프로세스)                  │
 * │  - 500ms마다 미발행 이벤트 조회                       │
 * │  - JSON → Avro 변환 → Kafka 전송                    │
 * │  - 전송 성공 → published=true 마킹                   │
 * └─────────────────────────────────────────────────────┘
 * </pre>
 *
 * <h3>정상 플로우</h3>
 * startSaga() → BookFlightCommand → onFlightBooked() → BookHotelCommand → onHotelBooked() → COMPLETED
 *
 * <h3>보상 플로우</h3>
 * onHotelBookingFailed() → CancelFlightCommand → onFlightCancelled() → COMPENSATED
 */
@Service
@Slf4j
public class TripSagaOrchestrator {

    private final SagaStateRepository sagaStateRepository;
    private final OutboxEventRepository outboxEventRepository;
    private final ObjectMapper objectMapper;

    // ─── 토픽 상수 ────────────────────────────────────────────────────────

    // Command 토픽 (Orchestrator → Service)
    static final String FLIGHT_COMMAND_TOPIC = "chapter4.commands.flight";
    static final String HOTEL_COMMAND_TOPIC = "chapter4.commands.hotel";

    // Event 토픽 (Service → Orchestrator) — 이벤트 타입별 분리
    static final String FLIGHT_BOOKED_TOPIC = "chapter4.events.flight-booked";
    static final String FLIGHT_BOOKING_FAILED_TOPIC = "chapter4.events.flight-booking-failed";
    static final String FLIGHT_CANCELLED_TOPIC = "chapter4.events.flight-cancelled";
    static final String HOTEL_BOOKED_TOPIC = "chapter4.events.hotel-booked";
    static final String HOTEL_BOOKING_FAILED_TOPIC = "chapter4.events.hotel-booking-failed";

    public TripSagaOrchestrator(
            SagaStateRepository sagaStateRepository,
            OutboxEventRepository outboxEventRepository,
            ObjectMapper objectMapper) {
        this.sagaStateRepository = sagaStateRepository;
        this.outboxEventRepository = outboxEventRepository;
        this.objectMapper = objectMapper;
    }

    // ─── SAGA 시작 ────────────────────────────────────────────────────────

    /**
     * SAGA 시작: SagaState 생성 → OutboxEvent(BookFlightCommand) 저장
     *
     * <p>트랜잭션 경계:
     * <ul>
     *   <li>단일 DB TX: SagaState INSERT + OutboxEvent INSERT → 원자적 커밋</li>
     *   <li>Kafka 발행은 OutboxPublisher가 비동기로 처리</li>
     * </ul>
     *
     * @return sagaId (SAGA 인스턴스 식별자)
     */
    @Transactional
    public String startSaga(String tripId, String departure, String arrival,
                            LocalDate travelDate, String hotelName,
                            LocalDate checkIn, LocalDate checkOut) {
        String sagaId = UuidCreator.getTimeOrderedEpoch().toString();

        SagaState state = SagaState.builder()
                .sagaId(sagaId)
                .tripId(tripId)
                .currentStep(SagaStep.FLIGHT_BOOKING)
                .status(SagaStatus.STARTED)
                .departure(departure)
                .arrival(arrival)
                .travelDate(travelDate)
                .hotelName(hotelName)
                .checkIn(checkIn)
                .checkOut(checkOut)
                .stepStartedAt(Instant.now())
                .build();
        sagaStateRepository.save(state);

        log.info("SAGA started: sagaId={}, tripId={}", sagaId, tripId);

        // Step 1: 항공 예약 요청 → Outbox에 저장 (동일 DB TX)
        BookFlightCommand cmd = BookFlightCommand.builder()
                .tripId(tripId)
                .sagaId(sagaId)
                .departure(departure)
                .arrival(arrival)
                .travelDate(travelDate)
                .build();

        saveOutboxEvent(FLIGHT_COMMAND_TOPIC, sagaId, "BookFlightCommand", cmd);

        return sagaId;
    }

    // ─── Step 1 완료: 항공 예약 성공 ────────────────────────────────────

    /**
     * 항공 예약 완료 이벤트 수신 → SagaState 업데이트 → OutboxEvent(BookHotelCommand) 저장
     *
     * <p>트랜잭션 경계:
     * <ul>
     *   <li>Kafka TX: 컨테이너가 시작 → consumer offset 커밋</li>
     *   <li>DB TX: @Transactional → SagaState UPDATE + OutboxEvent INSERT 원자적</li>
     * </ul>
     */
    @KafkaListener(
            topics = FLIGHT_BOOKED_TOPIC,
            groupId = "trip-saga-orchestrator",
            containerFactory = "ch04KafkaListenerContainerFactory")
    @Transactional
    public void onFlightBooked(TripFlightBooked avroEvent) {
        FlightBooked event = TripSagaEventMapper.toDomain(avroEvent);

        log.info("SAGA step received: sagaId={}, event=FlightBooked, reservationId={}",
                event.sagaId(), event.reservationId());

        SagaState state = getSagaState(event.sagaId());

        if (state.getStatus() != SagaStatus.STARTED) {
            log.warn("Invalid state for FlightBooked: sagaId={}, status={}",
                    event.sagaId(), state.getStatus());
            return;
        }

        // 상태 업데이트: Step 1 완료 → Step 2 진행
        state.setCurrentStep(SagaStep.HOTEL_BOOKING);
        state.setStatus(SagaStatus.IN_PROGRESS);
        state.setFlightReservationId(event.reservationId());
        state.setStepStartedAt(Instant.now());
        sagaStateRepository.save(state);

        log.info("SAGA step completed: sagaId={}, step=FLIGHT_BOOKING, next=HOTEL_BOOKING",
                event.sagaId());

        // Step 2: 호텔 예약 요청 → Outbox에 저장 (동일 DB TX)
        BookHotelCommand cmd = BookHotelCommand.builder()
                .tripId(event.tripId())
                .sagaId(event.sagaId())
                .hotelName(state.getHotelName())
                .checkIn(state.getCheckIn())
                .checkOut(state.getCheckOut())
                .build();

        saveOutboxEvent(HOTEL_COMMAND_TOPIC, event.sagaId(), "BookHotelCommand", cmd);
    }

    // ─── Step 2 완료: 호텔 예약 성공 → SAGA 완료 ────────────────────────

    /**
     * 호텔 예약 완료 이벤트 수신 → SAGA COMPLETED
     *
     * <p>트랜잭션: DB TX(SagaState UPDATE) + Kafka TX(consumer offset 커밋)
     */
    @KafkaListener(
            topics = HOTEL_BOOKED_TOPIC,
            groupId = "trip-saga-orchestrator",
            containerFactory = "ch04KafkaListenerContainerFactory")
    @Transactional
    public void onHotelBooked(TripHotelBooked avroEvent) {
        HotelBooked event = TripSagaEventMapper.toDomain(avroEvent);

        log.info("SAGA step received: sagaId={}, event=HotelBooked, reservationId={}",
                event.sagaId(), event.reservationId());

        SagaState state = getSagaState(event.sagaId());

        if (state.getStatus() != SagaStatus.IN_PROGRESS) {
            log.warn("Invalid state for HotelBooked: sagaId={}, status={}",
                    event.sagaId(), state.getStatus());
            return;
        }

        // SAGA 완료
        state.setCurrentStep(SagaStep.COMPLETED);
        state.setStatus(SagaStatus.COMPLETED);
        state.setHotelReservationId(event.reservationId());
        state.setCompletedAt(Instant.now());
        sagaStateRepository.save(state);

        log.info("SAGA completed: sagaId={}, tripId={}, flightReservationId={}, hotelReservationId={}",
                event.sagaId(), event.tripId(),
                state.getFlightReservationId(), event.reservationId());
    }

    // ─── Step 1 실패: 항공 예약 실패 → FAILED (보상 불필요) ──────────────

    /**
     * 항공 예약 실패 → SAGA 바로 FAILED
     *
     * Step 1에서 실패했으므로 이전에 성공한 단계가 없다.
     * 보상할 것이 없으므로 바로 FAILED 상태로 전이한다.
     *
     * <p>트랜잭션: DB TX(SagaState UPDATE) + Kafka TX(consumer offset 커밋)
     */
    @KafkaListener(
            topics = FLIGHT_BOOKING_FAILED_TOPIC,
            groupId = "trip-saga-orchestrator",
            containerFactory = "ch04KafkaListenerContainerFactory")
    @Transactional
    public void onFlightBookingFailed(TripFlightBookingFailed avroEvent) {
        FlightBookingFailed event = TripSagaEventMapper.toDomain(avroEvent);

        log.warn("SAGA step failed: sagaId={}, event=FlightBookingFailed, reason={}",
                event.sagaId(), event.reason());

        SagaState state = getSagaState(event.sagaId());

        if (state.getStatus() != SagaStatus.STARTED) {
            log.warn("Invalid state for FlightBookingFailed: sagaId={}, status={}",
                    event.sagaId(), state.getStatus());
            return;
        }

        // Step 1 실패 → 보상 없이 바로 FAILED
        state.setStatus(SagaStatus.FAILED);
        state.setFailureReason(event.reason());
        state.setFailedStep("FLIGHT_BOOKING");
        sagaStateRepository.save(state);

        log.error("SAGA failed at Step 1 (no compensation needed): sagaId={}, tripId={}",
                event.sagaId(), event.tripId());
    }

    // ─── Step 2 실패: 호텔 예약 실패 → 보상 시작 ──────────────────────

    /**
     * 호텔 예약 실패 → COMPENSATING → OutboxEvent(CancelFlightCommand) 저장
     *
     * Step 2에서 실패했으므로 Step 1(항공)을 역순으로 보상해야 한다.
     * SagaState에 저장된 flightReservationId로 취소 Command를 생성한다.
     *
     * <p>트랜잭션: DB TX(SagaState UPDATE + OutboxEvent INSERT 원자적) + Kafka TX(consumer offset 커밋)
     */
    @KafkaListener(
            topics = HOTEL_BOOKING_FAILED_TOPIC,
            groupId = "trip-saga-orchestrator",
            containerFactory = "ch04KafkaListenerContainerFactory")
    @Transactional
    public void onHotelBookingFailed(TripHotelBookingFailed avroEvent) {
        HotelBookingFailed event = TripSagaEventMapper.toDomain(avroEvent);

        log.warn("SAGA step failed: sagaId={}, event=HotelBookingFailed, reason={}",
                event.sagaId(), event.reason());

        SagaState state = getSagaState(event.sagaId());

        if (state.getStatus() != SagaStatus.IN_PROGRESS) {
            log.warn("Invalid state for HotelBookingFailed: sagaId={}, status={}",
                    event.sagaId(), state.getStatus());
            return;
        }

        // COMPENSATING 상태로 전이
        state.setStatus(SagaStatus.COMPENSATING);
        state.setFailureReason(event.reason());
        state.setFailedStep("HOTEL_BOOKING");
        sagaStateRepository.save(state);

        log.info("SAGA compensation started: sagaId={}, cancelling flight reservationId={}",
                event.sagaId(), state.getFlightReservationId());

        // 보상: 항공 예약 취소 → Outbox에 저장 (동일 DB TX)
        CancelFlightCommand cmd = CancelFlightCommand.builder()
                .tripId(event.tripId())
                .sagaId(event.sagaId())
                .reservationId(state.getFlightReservationId())
                .build();

        saveOutboxEvent(FLIGHT_COMMAND_TOPIC, event.sagaId(), "CancelFlightCommand", cmd);
    }

    // ─── 보상 완료: 항공 취소 성공 → COMPENSATED ──────────────────────

    /**
     * 항공 취소 완료 → SAGA COMPENSATED (보상 완료)
     *
     * 보상이 모두 끝났으므로 SAGA를 COMPENSATED 상태로 마무리한다.
     * COMPENSATED는 "실패했지만 일관성은 복구되었다"는 의미이다.
     *
     * <p>트랜잭션: DB TX(SagaState UPDATE) + Kafka TX(consumer offset 커밋)
     */
    @KafkaListener(
            topics = FLIGHT_CANCELLED_TOPIC,
            groupId = "trip-saga-orchestrator",
            containerFactory = "ch04KafkaListenerContainerFactory")
    @Transactional
    public void onFlightCancelled(TripFlightCancelled avroEvent) {
        FlightCancelled event = TripSagaEventMapper.toDomain(avroEvent);

        log.info("SAGA compensation received: sagaId={}, event=FlightCancelled, reservationId={}",
                event.sagaId(), event.reservationId());

        SagaState state = getSagaState(event.sagaId());

        if (state.getStatus() != SagaStatus.COMPENSATING) {
            log.warn("Invalid state for FlightCancelled: sagaId={}, status={}",
                    event.sagaId(), state.getStatus());
            return;
        }

        // 보상 완료 → COMPENSATED
        state.setStatus(SagaStatus.COMPENSATED);
        state.setCompletedAt(Instant.now());
        sagaStateRepository.save(state);

        log.info("SAGA compensated: sagaId={}, tripId={} (flight {} cancelled, hotel was not booked)",
                event.sagaId(), event.tripId(), event.reservationId());
    }

    // ─── 내부 헬퍼 ───────────────────────────────────────────────────────

    /**
     * Command를 Outbox 테이블에 JSON으로 저장한다.
     *
     * 호출 메서드의 @Transactional 범위 내에서 실행되므로
     * SagaState.save()와 동일 DB TX에서 커밋된다.
     */
    private void saveOutboxEvent(String topic, String sagaId,
                                  String commandType, Object command) {
        try {
            OutboxEvent event = OutboxEvent.builder()
                    .aggregateId(sagaId)
                    .topic(topic)
                    .messageKey(sagaId)
                    .commandType(commandType)
                    .payload(objectMapper.writeValueAsString(command))
                    .published(false)
                    .build();
            outboxEventRepository.save(event);
        } catch (JsonProcessingException e) {
            throw new IllegalStateException(
                    "Failed to serialize command: " + commandType, e);
        }
    }

    private SagaState getSagaState(String sagaId) {
        return sagaStateRepository.findById(sagaId)
                .orElseThrow(() -> new IllegalStateException("SagaState not found: " + sagaId));
    }
}
