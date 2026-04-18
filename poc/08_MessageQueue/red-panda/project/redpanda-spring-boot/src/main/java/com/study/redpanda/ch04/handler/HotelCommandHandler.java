package com.study.redpanda.ch04.handler;

import com.study.redpanda.avro.trip.TripBookHotelCommand;
import com.study.redpanda.ch04.command.BookHotelCommand;
import com.study.redpanda.ch04.event.HotelBooked;
import com.study.redpanda.ch04.event.HotelBookingFailed;
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
 * 호텔 서비스 Command Handler
 *
 * <p>클래스 레벨 {@code @KafkaListener} + 메서드 레벨 {@code @KafkaHandler}로
 * Avro 타입별 자동 디스패치한다. 호텔 토픽에는 BookHotelCommand 1종만 있으므로
 * 단일 핸들러로 처리.
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
        topics = "chapter4.commands.hotel",
        groupId = "hotel-command-handler",
        containerFactory = "ch04KafkaListenerContainerFactory")
public class HotelCommandHandler {

    private final ProcessedCommandRepository processedCommandRepository;

    static final String HOTEL_BOOKED_TOPIC = "chapter4.events.hotel-booked";
    static final String HOTEL_BOOKING_FAILED_TOPIC = "chapter4.events.hotel-booking-failed";

    /**
     * 호텔 예약 처리
     *
     * 실패 시뮬레이션: hotelName이 "FAIL"이면 예약 실패
     */
    @KafkaHandler
    @SendTo
    @Transactional
    public Message<?> handleBookHotel(TripBookHotelCommand avroCmd) {
        BookHotelCommand cmd = TripSagaEventMapper.toDomain(avroCmd);
        log.info("Processing BookHotelCommand: sagaId={}, tripId={}, hotel={}",
                cmd.sagaId(), cmd.tripId(), cmd.hotelName());

        if (!acquireIdempotency(cmd.sagaId(), "BOOK_HOTEL")) {
            return null;  // 중복 → 응답 발행 안 함
        }

        if ("FAIL".equalsIgnoreCase(cmd.hotelName())) {
            HotelBookingFailed failed = new HotelBookingFailed(
                    cmd.tripId(), cmd.sagaId(), Instant.now(),
                    "Hotel booking failed: " + cmd.hotelName() + " is fully booked");
            log.warn("Hotel booking FAILED: sagaId={}", cmd.sagaId());
            return toMessage(HOTEL_BOOKING_FAILED_TOPIC, cmd.sagaId(),
                    TripSagaEventMapper.toAvro(failed));
        }

        String reservationId = "HTL-" + UUID.randomUUID().toString().substring(0, 8);
        HotelBooked booked = new HotelBooked(
                cmd.tripId(), cmd.sagaId(), Instant.now(), reservationId);
        log.info("Hotel booked: sagaId={}, reservationId={}", cmd.sagaId(), reservationId);
        return toMessage(HOTEL_BOOKED_TOPIC, cmd.sagaId(),
                TripSagaEventMapper.toAvro(booked));
    }

    @KafkaHandler(isDefault = true)
    public void handleUnknown(Object record) {
        log.warn("Unknown command type on hotel topic: {}", record.getClass().getName());
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
