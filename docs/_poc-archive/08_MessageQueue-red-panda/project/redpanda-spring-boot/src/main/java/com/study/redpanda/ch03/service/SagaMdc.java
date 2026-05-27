package com.study.redpanda.ch03.service;

import org.slf4j.MDC;

/**
 * SAGA 분산 추적용 MDC 유틸리티
 *
 * Choreography에서는 이벤트가 여러 서비스를 거치므로, correlationId를 MDC에 넣어
 * 모든 로그에 자동으로 포함시킨다. 이렇게 하면 Kibana/Grafana에서
 * correlationId로 검색하면 4개 서비스의 로그가 시간순으로 나열된다.
 *
 * 사용 패턴:
 * SagaMdc.set(correlationId, orderId);
 * try { ... } finally { SagaMdc.clear(); }
 *
 * logback 패턴: %d{HH:mm:ss.SSS} [%thread] %-5level [cid=%X{correlationId}][oid=%X{orderId}] %logger - %msg%n
 */
public final class SagaMdc {

    public static final String CORRELATION_ID = "correlationId";
    public static final String ORDER_ID = "orderId";

    private SagaMdc() {}

    public static void set(String correlationId, String orderId) {
        MDC.put(CORRELATION_ID, correlationId);
        MDC.put(ORDER_ID, orderId);
    }

    public static void clear() {
        MDC.remove(CORRELATION_ID);
        MDC.remove(ORDER_ID);
    }
}
