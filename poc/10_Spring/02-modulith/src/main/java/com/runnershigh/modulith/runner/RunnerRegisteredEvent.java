package com.runnershigh.modulith.runner;

import java.time.Instant;

/**
 * 러너 등록 완료 이벤트 (Domain Event)
 *
 * <p>러너 등록이 완료되면 발행됩니다.
 * 다른 모듈에서 이 이벤트를 구독하여 후속 작업을 수행할 수 있습니다.
 *
 * <p>사용 예시 (다른 모듈에서 구독):
 * <pre>{@code
 * @ApplicationModuleListener
 * void on(RunnerRegisteredEvent event) {
 *     // 환영 이메일 발송
 *     // 초기 활동 기록 생성
 * }
 * }</pre>
 *
 * @param runnerId     등록된 러너 ID
 * @param email        러너 이메일
 * @param occurredAt   이벤트 발생 시각
 */
public record RunnerRegisteredEvent(
        Long runnerId,
        String email,
        Instant occurredAt
) {
    public RunnerRegisteredEvent(Long runnerId, String email) {
        this(runnerId, email, Instant.now());
    }
}
