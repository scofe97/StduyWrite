package com.study.redpanda.ch03.event.mapper;

import com.study.redpanda.avro.saga.SagaInventoryReleased;
import com.study.redpanda.avro.saga.SagaInventoryReservationFailed;
import com.study.redpanda.avro.saga.SagaInventoryReserved;
import com.study.redpanda.avro.saga.SagaOrderCreated;
import com.study.redpanda.avro.saga.SagaOrderItem;
import com.study.redpanda.avro.saga.SagaPaymentCompleted;
import com.study.redpanda.avro.saga.SagaPaymentFailed;
import com.study.redpanda.avro.saga.SagaPaymentRefunded;
import com.study.redpanda.avro.saga.SagaShippingFailed;
import com.study.redpanda.avro.saga.SagaShippingRequested;
import com.study.redpanda.ch03.event.InventoryReleased;
import com.study.redpanda.ch03.event.InventoryReservationFailed;
import com.study.redpanda.ch03.event.InventoryReserved;
import com.study.redpanda.ch03.event.OrderCreated;
import com.study.redpanda.ch03.event.PaymentCompleted;
import com.study.redpanda.ch03.event.PaymentFailed;
import com.study.redpanda.ch03.event.PaymentRefunded;
import com.study.redpanda.ch03.event.ShippingFailed;
import com.study.redpanda.ch03.event.ShippingRequested;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

/**
 * 도메인 레코드 ↔ Avro 생성 클래스 변환 매퍼
 *
 * - toAvro(): 도메인 레코드 → Avro SpecificRecord (Kafka 전송용)
 * - toDomain(): Avro SpecificRecord → 도메인 레코드 (비즈니스 로직용)
 *
 * Instant ↔ String: Instant.toString() / Instant.parse()
 * BigDecimal ↔ String: toPlainString() / new BigDecimal(str)
 */
public class SagaEventMapper {

    private SagaEventMapper() {}

    // ─── OrderCreated ────────────────────────────────────────────────────────

    public static SagaOrderCreated toAvro(OrderCreated domain) {
        List<SagaOrderItem> avroItems = domain.items().stream()
                .map(item -> SagaOrderItem.newBuilder()
                        .setProductId(item.productId())
                        .setProductName(item.productName())
                        .setQuantity(item.quantity())
                        .setPrice(item.price().toPlainString())
                        .build())
                .toList();

        return SagaOrderCreated.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setCustomerId(domain.customerId())
                .setItems(avroItems)
                .setTotalAmount(domain.totalAmount().toPlainString())
                .build();
    }

    public static OrderCreated toDomain(SagaOrderCreated avro) {
        List<OrderCreated.OrderItem> items = avro.getItems().stream()
                .map(item -> new OrderCreated.OrderItem(
                        item.getProductId().toString(),
                        item.getProductName().toString(),
                        item.getQuantity(),
                        new BigDecimal(item.getPrice().toString())))
                .toList();

        return new OrderCreated(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getCustomerId().toString(),
                items,
                new BigDecimal(avro.getTotalAmount().toString()));
    }

    // ─── InventoryReserved ───────────────────────────────────────────────────

    public static SagaInventoryReserved toAvro(InventoryReserved domain) {
        return SagaInventoryReserved.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setReservationIds(domain.reservationIds())
                .build();
    }

    public static InventoryReserved toDomain(SagaInventoryReserved avro) {
        List<String> ids = avro.getReservationIds().stream()
                .map(Object::toString)
                .toList();
        return new InventoryReserved(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                ids);
    }

    // ─── InventoryReservationFailed ──────────────────────────────────────────

    public static SagaInventoryReservationFailed toAvro(InventoryReservationFailed domain) {
        return SagaInventoryReservationFailed.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setReason(domain.reason())
                .setFailedItems(domain.failedItems())
                .build();
    }

    public static InventoryReservationFailed toDomain(SagaInventoryReservationFailed avro) {
        List<String> failedItems = avro.getFailedItems().stream()
                .map(Object::toString)
                .toList();
        return new InventoryReservationFailed(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getReason().toString(),
                failedItems);
    }

    // ─── PaymentCompleted ────────────────────────────────────────────────────

    public static SagaPaymentCompleted toAvro(PaymentCompleted domain) {
        return SagaPaymentCompleted.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setTransactionId(domain.transactionId())
                .setAmount(domain.amount().toPlainString())
                .build();
    }

    public static PaymentCompleted toDomain(SagaPaymentCompleted avro) {
        return new PaymentCompleted(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getTransactionId().toString(),
                new BigDecimal(avro.getAmount().toString()));
    }

    // ─── PaymentFailed ───────────────────────────────────────────────────────

    public static SagaPaymentFailed toAvro(PaymentFailed domain) {
        return SagaPaymentFailed.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setReason(domain.reason())
                .setErrorCode(domain.errorCode())
                .build();
    }

    public static PaymentFailed toDomain(SagaPaymentFailed avro) {
        return new PaymentFailed(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getReason().toString(),
                avro.getErrorCode().toString());
    }

    // ─── ShippingRequested ───────────────────────────────────────────────────

    public static SagaShippingRequested toAvro(ShippingRequested domain) {
        return SagaShippingRequested.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setTrackingNumber(domain.trackingNumber())
                .build();
    }

    public static ShippingRequested toDomain(SagaShippingRequested avro) {
        return new ShippingRequested(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getTrackingNumber().toString());
    }

    // ─── ShippingFailed ──────────────────────────────────────────────────────

    public static SagaShippingFailed toAvro(ShippingFailed domain) {
        return SagaShippingFailed.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setReason(domain.reason())
                .build();
    }

    public static ShippingFailed toDomain(SagaShippingFailed avro) {
        return new ShippingFailed(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getReason().toString());
    }

    // ─── InventoryReleased ───────────────────────────────────────────────────

    public static SagaInventoryReleased toAvro(InventoryReleased domain) {
        return SagaInventoryReleased.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setReservationIds(domain.reservationIds())
                .build();
    }

    public static InventoryReleased toDomain(SagaInventoryReleased avro) {
        List<String> ids = avro.getReservationIds().stream()
                .map(Object::toString)
                .toList();
        return new InventoryReleased(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                ids);
    }

    // ─── PaymentRefunded ─────────────────────────────────────────────────────

    public static SagaPaymentRefunded toAvro(PaymentRefunded domain) {
        return SagaPaymentRefunded.newBuilder()
                .setOrderId(domain.orderId())
                .setCorrelationId(domain.correlationId())
                .setTimestamp(domain.timestamp().toString())
                .setTransactionId(domain.transactionId())
                .setAmount(domain.amount().toPlainString())
                .build();
    }

    public static PaymentRefunded toDomain(SagaPaymentRefunded avro) {
        return new PaymentRefunded(
                avro.getOrderId().toString(),
                avro.getCorrelationId().toString(),
                Instant.parse(avro.getTimestamp().toString()),
                avro.getTransactionId().toString(),
                new BigDecimal(avro.getAmount().toString()));
    }
}
