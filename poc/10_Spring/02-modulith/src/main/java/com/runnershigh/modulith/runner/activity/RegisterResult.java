package com.runnershigh.modulith.runner.activity;

/**
 * 러너 등록 결과 (Sealed Interface)
 *
 * <p>Success와 Failure 두 가지 결과만 허용합니다.
 * switch 표현식에서 패턴 매칭으로 처리할 수 있습니다.
 *
 * <pre>{@code
 * RegisterResult result = activity.register(command);
 * return switch (result) {
 *     case Success s -> ResponseEntity.ok(s);
 *     case Failure f -> ResponseEntity.badRequest().body(f.reason());
 * };
 * }</pre>
 */
public sealed interface RegisterResult
        permits RegisterResult.Success, RegisterResult.Failure {

    /**
     * 등록 성공 결과
     *
     * @param runnerId 생성된 러너 ID
     * @param name     러너 이름
     */
    record Success(Long runnerId, String name) implements RegisterResult {
    }

    /**
     * 등록 실패 결과
     *
     * @param reason 실패 사유
     * @param type   실패 유형
     */
    record Failure(String reason, FailureType type) implements RegisterResult {

        public enum FailureType {
            /** 이미 존재하는 이메일 */
            DUPLICATE_EMAIL,
            /** 유효하지 않은 입력 데이터 */
            INVALID_DATA,
            /** 시스템 오류 */
            SYSTEM_ERROR
        }
    }
}
