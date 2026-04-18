package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import io.github.resilience4j.circuitbreaker.CallNotPermittedException;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import jakarta.annotation.PostConstruct;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Ch02 C8: Circuit Breaker 연동
 *
 * 외부 서비스 호출을 Circuit Breaker로 감싸서:
 * - CLOSED: 정상 호출
 * - OPEN: 즉시 실패 (블로킹 없음 → poll() 간격 유지 → 리밸런싱 방지)
 * - HALF_OPEN: 일부 요청으로 복구 확인
 *
 * Circuit Breaker가 없으면 외부 API 타임아웃(30초+)으로 poll() 간격 초과 → 리밸런싱 폭풍
 */
@Slf4j
@Component
public class CircuitBreakerConsumer {

    @Getter
    private final CircuitBreakerRegistry circuitBreakerRegistry;

    @Getter
    private CircuitBreaker circuitBreaker;

    @Getter
    private volatile CountDownLatch successLatch = new CountDownLatch(1);

    @Getter
    private volatile CountDownLatch failureLatch = new CountDownLatch(1);

    @Getter
    private final AtomicInteger successCount = new AtomicInteger(0);

    @Getter
    private final AtomicInteger failureCount = new AtomicInteger(0);

    @Getter
    private final AtomicInteger circuitOpenCount = new AtomicInteger(0);

    // 외부 서비스 장애 시뮬레이션
    @Getter
    private volatile boolean externalServiceDown = false;

    public CircuitBreakerConsumer() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
                .failureRateThreshold(50)           // 실패율 50% 이상 → OPEN
                .slidingWindowSize(4)                // 최근 4건 기준
                .minimumNumberOfCalls(4)             // 최소 4건 호출 후 판단
                .waitDurationInOpenState(Duration.ofSeconds(5))  // OPEN 후 5초 대기
                .permittedNumberOfCallsInHalfOpenState(2)        // HALF_OPEN에서 2건 시도
                .build();

        this.circuitBreakerRegistry = CircuitBreakerRegistry.of(config);
        this.circuitBreaker = circuitBreakerRegistry.circuitBreaker("external-service");
    }

    @PostConstruct
    public void init() {
        circuitBreaker.getEventPublisher()
                .onStateTransition(event -> log.info("CircuitBreaker 상태 전이: {}",
                        event.getStateTransition()));
    }

    public void reset(int successCount, int failureCount) {
        this.successLatch = new CountDownLatch(successCount);
        this.failureLatch = new CountDownLatch(failureCount);
        this.successCount.set(0);
        this.failureCount.set(0);
        this.circuitOpenCount.set(0);
        this.externalServiceDown = false;
    }

    public void setExternalServiceDown(boolean down) {
        this.externalServiceDown = down;
    }

    @KafkaListener(
            id = "circuit-breaker-listener",
            topics = "chapter2.circuit-test",
            groupId = "circuit-test-group"
    )
    public void consume(@Payload OrderEvent event, Acknowledgment ack) {
        log.info("CircuitBreakerConsumer: orderId={}, circuitState={}",
                event.getOrderId(), circuitBreaker.getState());

        try {
            // Circuit Breaker로 외부 서비스 호출을 감싼다
            String result = circuitBreaker.executeSupplier(() -> callExternalService(event));
            successCount.incrementAndGet();
            successLatch.countDown();
            log.info("처리 성공: orderId={}, result={}", event.getOrderId(), result);
            ack.acknowledge();
        } catch (CallNotPermittedException e) {
            // Circuit OPEN 상태 — 외부 서비스를 호출하지 않고 즉시 차단된 경우
            // 블로킹 없이 밀리초 수준으로 실패 → poll() 간격 유지 → 리밸런싱 방지
            circuitOpenCount.incrementAndGet();
            failureCount.incrementAndGet();
            failureLatch.countDown();
            log.info("Circuit OPEN — 즉시 차단 (블로킹 없음): orderId={}", event.getOrderId());
            // OPEN 상태에서는 ack하지 않음 → 복구 후 재처리 가능
            // 실무에서는 nack + DLT 또는 pause 연동이 일반적
        } catch (RuntimeException e) {
            // 외부 서비스 호출은 했지만 실패한 경우 (CLOSED/HALF_OPEN 상태)
            failureCount.incrementAndGet();
            failureLatch.countDown();
            log.info("외부 서비스 호출 실패: orderId={}, error={}", event.getOrderId(), e.getMessage());
            ack.acknowledge();
            // 실무에서는 재시도 전략(C5/C6)과 병행
        }
    }

    /**
     * 외부 서비스 호출 시뮬레이션
     * externalServiceDown=true이면 예외 발생 (API 장애 상황)
     */
    private String callExternalService(OrderEvent event) {
        if (externalServiceDown) {
            throw new RuntimeException("External service unavailable");
        }
        return "OK:" + event.getOrderId();
    }
}
