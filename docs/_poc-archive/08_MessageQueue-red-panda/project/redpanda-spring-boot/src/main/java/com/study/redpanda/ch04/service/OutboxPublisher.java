package com.study.redpanda.ch04.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.study.redpanda.ch04.command.BookFlightCommand;
import com.study.redpanda.ch04.command.BookHotelCommand;
import com.study.redpanda.ch04.command.CancelFlightCommand;
import com.study.redpanda.ch04.domain.OutboxEvent;
import com.study.redpanda.ch04.event.mapper.TripSagaEventMapper;
import com.study.redpanda.ch04.repository.OutboxEventRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.domain.PageRequest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

/**
 * Outbox 폴링 CDC 발행자
 *
 * Outbox 테이블에 저장된 미발행 이벤트를 주기적으로 폴링하여
 * Kafka로 발행한다. 이를 통해 DB TX와 Kafka 발행의 최종 일관성을 보장한다.
 *
 * <h3>발행 흐름</h3>
 * <pre>
 * 1. 500ms마다 미발행 이벤트 50건 조회 (ORDER BY id ASC → 순서 보장)
 * 2. JSON payload → ObjectMapper.readValue() → 도메인 Command
 * 3. 도메인 Command → TripSagaEventMapper.toAvro() → Avro SpecificRecord
 * 4. kafkaTemplate.executeInTransaction() → Kafka 동기 전송
 * 5. 성공 → published=true, publishedAt=now 마킹
 * 6. 실패 → 미발행 유지, 다음 폴링에서 자동 재시도
 * </pre>
 *
 * <h3>정리 스케줄</h3>
 * 5분마다 1시간 이전 발행 완료 레코드를 삭제하여 테이블 비대화를 방지한다.
 *
 * <h3>executeInTransaction() 사용 이유</h3>
 * {@code ch04KafkaTemplate}에 {@code transactional.id}가 설정되어 있어
 * {@code @KafkaListener} 외부에서 Kafka TX를 사용하려면 명시적으로
 * {@code executeInTransaction()}을 호출해야 한다.
 *
 * <h3>Debezium CDC 대안</h3>
 * 폴링 방식 대신 Debezium PostgreSQL CDC Connector를 사용하면
 * WAL(Write-Ahead Log)을 통해 실시간으로 outbox 변경을 감지할 수 있다.
 * <pre>
 * // Debezium Outbox Event Router 설정 예시
 * {
 *   "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
 *   "database.hostname": "localhost",
 *   "database.port": "5432",
 *   "database.dbname": "redpanda_db",
 *   "table.include.list": "public.ch04_outbox_event",
 *   "transforms": "outbox",
 *   "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
 *   "transforms.outbox.table.field.event.key": "message_key",
 *   "transforms.outbox.table.field.event.payload": "payload",
 *   "transforms.outbox.route.topic.replacement": "${routedByValue}",
 *   "transforms.outbox.table.fields.additional.placement": "topic:header:topic"
 * }
 * </pre>
 */
@Component
@Slf4j
public class OutboxPublisher {

    private static final int BATCH_SIZE = 50;

    private final OutboxEventRepository outboxEventRepository;
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final ObjectMapper objectMapper;

    public OutboxPublisher(
            OutboxEventRepository outboxEventRepository,
            @Qualifier("ch04KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            ObjectMapper objectMapper) {
        this.outboxEventRepository = outboxEventRepository;
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
    }

    // ─── 폴링 발행 (500ms마다) ────────────────────────────────────────

    // @Scheduled(fixedDelay = 500)
    public void publishPendingEvents() {
        List<OutboxEvent> events = outboxEventRepository.findByPublishedFalseOrderByIdAsc(
                PageRequest.of(0, BATCH_SIZE));

        for (OutboxEvent event : events) {
            publishEvent(event);
        }
    }

    /**
     * 개별 이벤트를 Kafka로 발행한다.
     *
     * JSON payload를 도메인 Command로 역직렬화한 뒤 Avro로 변환하여 전송한다.
     * 실패 시 published=false 상태를 유지하여 다음 폴링에서 재시도한다.
     */
    private void publishEvent(OutboxEvent event) {
        try {
            Object avroRecord = deserializeAndConvertToAvro(event);

            kafkaTemplate.executeInTransaction(ops -> {
                try {
                    ops.send(event.getTopic(), event.getMessageKey(), avroRecord).get();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Interrupted while sending to Kafka", e);
                } catch (java.util.concurrent.ExecutionException e) {
                    throw new RuntimeException("Failed to send to Kafka", e.getCause());
                }
                return null;
            });

            event.setPublished(true);
            event.setPublishedAt(Instant.now());
            outboxEventRepository.save(event);

            log.info("Outbox event published: id={}, topic={}, aggregateId={}, commandType={}",
                    event.getId(), event.getTopic(), event.getAggregateId(), event.getCommandType());

        } catch (Exception e) {
            log.error("Outbox event publish failed (will retry): id={}, topic={}, aggregateId={}, error={}",
                    event.getId(), event.getTopic(), event.getAggregateId(), e.getMessage(), e);
        }
    }

    /**
     * JSON payload → 도메인 Command → Avro SpecificRecord
     *
     * commandType에 따라 적절한 Command 클래스로 역직렬화한 뒤
     * TripSagaEventMapper.toAvro()로 Avro 레코드로 변환한다.
     */
    private Object deserializeAndConvertToAvro(OutboxEvent event) throws Exception {
        String json = event.getPayload();

        return switch (event.getCommandType()) {
            case "BookFlightCommand" -> {
                BookFlightCommand cmd = objectMapper.readValue(json, BookFlightCommand.class);
                yield TripSagaEventMapper.toAvro(cmd);
            }
            case "BookHotelCommand" -> {
                BookHotelCommand cmd = objectMapper.readValue(json, BookHotelCommand.class);
                yield TripSagaEventMapper.toAvro(cmd);
            }
            case "CancelFlightCommand" -> {
                CancelFlightCommand cmd = objectMapper.readValue(json, CancelFlightCommand.class);
                yield TripSagaEventMapper.toAvro(cmd);
            }
            default -> throw new IllegalArgumentException(
                    "Unknown command type: " + event.getCommandType());
        };
    }

    // ─── 정리 스케줄 (5분마다) ────────────────────────────────────────

    /**
     * 발행 완료된 오래된 레코드를 삭제하여 테이블 비대화를 방지한다.
     * 1시간 이전에 발행 완료된 레코드만 삭제한다.
     */
    // @Scheduled(fixedDelay = 300_000)
    @Transactional
    public void cleanupPublishedEvents() {
        Instant threshold = Instant.now().minus(1, ChronoUnit.HOURS);
        int deleted = outboxEventRepository.deletePublishedBefore(threshold);
        if (deleted > 0) {
            log.info("Outbox cleanup: deleted {} published events older than 1 hour", deleted);
        }
    }
}
