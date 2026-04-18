package com.example.servicea.config;

/**
 * 수동 TraceID 전파 설정 (학습용) - 비활성화됨
 *
 * feign-micrometer 라이브러리 사용으로 대체
 *
 * 학습 포인트:
 * - 수동 헤더 추가: TraceID 전파 O, 클라이언트 Span X
 * - 라이브러리 사용: TraceID 전파 O, 클라이언트 Span O
 */
// @Configuration  // 비활성화
public class ManualTracingFeignConfig {
    // 라이브러리 방식 사용으로 주석 처리
}
