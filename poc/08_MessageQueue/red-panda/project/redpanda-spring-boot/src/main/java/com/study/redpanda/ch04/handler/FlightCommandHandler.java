package com.study.redpanda.ch04.handler;

import com.study.redpanda.avro.trip.TripBookFlightCommand;
import com.study.redpanda.avro.trip.TripCancelFlightCommand;
import com.study.redpanda.ch04.command.BookFlightCommand;
import com.study.redpanda.ch04.command.CancelFlightCommand;
import com.study.redpanda.ch04.event.FlightBooked;
import com.study.redpanda.ch04.event.FlightBookingFailed;
import com.study.redpanda.ch04.event.FlightCancelled;
import com.study.redpanda.ch04.event.mapper.TripSagaEventMapper;
import com.study.redpanda.ch04.repository.ProcessedCommandRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.Message;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.UUID;

/**
 * 항공 서비스 Command Handler
 *
 * <p>클래스 레벨 {@code @KafkaListener} + 메서드 레벨 {@code @KafkaHandler}로
 * Avro 타입별 자동 디스패치한다. instanceof 분기 없이 Spring이 역직렬화된 타입으로 라우팅.
 *
 * <p>{@code @SendTo}로 응답 이벤트를 발행한다. 반환된 {@link Message}의
 * {@code KafkaHeaders.TOPIC} 헤더가 실제 대상 토픽을 결정하므로,
 * 성공/실패에 따라 동적으로 토픽을 선택할 수 있다.
 * → kafkaTemplate 직접 의존 제거.
 *
 * <p>트랜잭션: Kafka TX(컨테이너) + DB TX(@Transactional) 이중 구조.
 * 멱등성 INSERT(DB)와 이벤트 발행(Kafka)이 독립 커밋되므로 Dual-Write 가능성 있음.
 * Recovery Scheduler가 타임아웃 기반으로 보상.
 */
@Component
@Slf4j
@RequiredArgsConstructor
@KafkaListener(
        topics = "chapter4.commands.flight",
        groupId = "flight-command-handler",
        containerFactory = "ch04KafkaListenerContainerFactory")
public class FlightCommandHandler {

    private final ProcessedCommandRepository processedCommandRepository;

    static final String FLIGHT_BOOKED_TOPIC = "chapter4.events.flight-booked";
    static final String FLIGHT_BOOKING_FAILED_TOPIC = "chapter4.events.flight-booking-failed";
    static final String FLIGHT_CANCELLED_TOPIC = "chapter4.events.flight-cancelled";

    /**
     * 항공 예약 처리
     *
     * 실패 시뮬레이션: departure가 "FAIL"이면 예약 실패
     */
    @KafkaHandler
    @SendTo
    @Transactional
    public Message<?> handleBookFlight(TripBookFlightCommand avroCmd) {
        BookFlightCommand cmd = TripSagaEventMapper.toDomain(avroCmd);
        log.info("Processing BookFlightCommand: sagaId={}, tripId={}, {} → {}",
                cmd.sagaId(), cmd.tripId(), cmd.departure(), cmd.arrival());

        if (!acquireIdempotency(cmd.sagaId(), "BOOK_FLIGHT")) {
            return null;  // 중복 → 응답 발행 안 함
        }

        if ("FAIL".equalsIgnoreCase(cmd.departure())) {
            FlightBookingFailed failed = new FlightBookingFailed(
                    cmd.tripId(), cmd.sagaId(), Instant.now(),
                    "Flight booking failed: no available flights from " + cmd.departure());
            log.warn("Flight booking FAILED: sagaId={}", cmd.sagaId());
            return toMessage(FLIGHT_BOOKING_FAILED_TOPIC, cmd.sagaId(),
                    TripSagaEventMapper.toAvro(failed));
        }

        String reservationId = "FLT-" + UUID.randomUUID().toString().substring(0, 8);
        FlightBooked booked = new FlightBooked(
                cmd.tripId(), cmd.sagaId(), Instant.now(), reservationId);
        log.info("Flight booked: sagaId={}, reservationId={}", cmd.sagaId(), reservationId);
        return toMessage(FLIGHT_BOOKED_TOPIC, cmd.sagaId(),
                TripSagaEventMapper.toAvro(booked));
    }

    /**
     * 항공 예약 취소 (보상)
     */
    @KafkaHandler
    @SendTo
    @Transactional
    public Message<?> handleCancelFlight(TripCancelFlightCommand avroCmd) {
        CancelFlightCommand cmd = TripSagaEventMapper.toDomain(avroCmd);
        log.info("Processing CancelFlightCommand: sagaId={}, reservationId={}",
                cmd.sagaId(), cmd.reservationId());

        if (!acquireIdempotency(cmd.sagaId(), "CANCEL_FLIGHT")) {
            return null;
        }

        FlightCancelled cancelled = new FlightCancelled(
                cmd.tripId(), cmd.sagaId(), Instant.now(), cmd.reservationId());
        log.info("Flight cancelled: sagaId={}, reservationId={}", cmd.sagaId(), cmd.reservationId());
        return toMessage(FLIGHT_CANCELLED_TOPIC, cmd.sagaId(),
                TripSagaEventMapper.toAvro(cancelled));
    }

    @KafkaHandler(isDefault = true)
    public void handleUnknown(Object record) {
        log.warn("Unknown command type on flight topic: {}", record.getClass().getName());
    }

    // ─── 내부 헬퍼 ───────────────────────────────────────────────────────

    private boolean acquireIdempotency(String sagaId, String commandType) {
        int acquired = processedCommandRepository.tryAcquire(sagaId, commandType, Instant.now());
        if (acquired == 0) {
            log.info("Duplicate {} skipped: sagaId={}", commandType, sagaId);
            return false;
        }
        return true;
    }

    private Message<?> toMessage(String topic, String key, Object payload) {
        return MessageBuilder.withPayload(payload)
                .setHeader(KafkaHeaders.TOPIC, topic)
                .setHeader(KafkaHeaders.KEY, key)
                .build();
    }
}
