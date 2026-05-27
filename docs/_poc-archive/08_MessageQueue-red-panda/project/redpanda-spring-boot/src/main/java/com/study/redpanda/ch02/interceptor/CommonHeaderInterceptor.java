package com.study.redpanda.ch02.interceptor;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerInterceptor;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.slf4j.MDC;

import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Map;

/**
 * Kafka ProducerInterceptor: 모든 메시지에 공통 헤더를 자동 주입한다.
 *
 * Spring 컨텍스트와 독립적이다 (DI 불가).
 * application.yml의 interceptor.classes 설정으로 활성화한다.
 */
@Slf4j
public class CommonHeaderInterceptor implements ProducerInterceptor<String, Object> {

    private static final String SERVICE_NAME = "order-service";

    /**
     * send() 호출 시 브로커 전송 전에 실행된다.
     * 원본 record에 헤더를 추가하여 반환한다.
     */
    @Override
    public ProducerRecord<String, Object> onSend(ProducerRecord<String, Object> record) {
        // 서비스 출처 식별용
        record.headers().add("X-Service-Name",
                SERVICE_NAME.getBytes(StandardCharsets.UTF_8));

        // 전송 시점 기록 (변수로 추출하여 헤더와 로그에 동일한 값 사용)
        String sentAt = Instant.now().toString();
        record.headers().add("X-Sent-At",
                sentAt.getBytes(StandardCharsets.UTF_8));

        // MDC에 traceId가 있으면 분산 추적용 헤더 추가
        String traceId = MDC.get("traceId");
        if (traceId != null) {
            record.headers().add("X-Trace-Id",
                    traceId.getBytes(StandardCharsets.UTF_8));
        }

        log.debug("Interceptor injected headers: X-Service-Name={}, X-Sent-At={}",
                SERVICE_NAME, sentAt);
        return record;
    }

    /**
     * 브로커 ACK 수신 후 호출된다.
     * 메트릭 수집이나 실패 로깅에 사용할 수 있다.
     */
    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
        if (exception != null) {
            log.warn("Interceptor: message send failed", exception);
        }
    }

    @Override
    public void close() {}

    @Override
    public void configure(Map<String, ?> configs) {}
}
