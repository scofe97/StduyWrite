package com.runnershigh.modulith.runner.activity;

import java.util.Objects;

/**
 * 러너 등록 명령 (Input)
 *
 * <p>불변 객체로, 생성 시 유효성 검증을 수행합니다.
 *
 * @param name  러너 이름 (필수)
 * @param email 러너 이메일 (필수)
 */
public record RegisterRunnerCommand(
        String name,
        String email
) {
    public RegisterRunnerCommand {
        Objects.requireNonNull(name, "name은 필수입니다");
        Objects.requireNonNull(email, "email은 필수입니다");

        if (name.isBlank()) {
            throw new IllegalArgumentException("name은 빈 값일 수 없습니다");
        }
        if (!email.contains("@")) {
            throw new IllegalArgumentException("유효하지 않은 이메일 형식입니다");
        }
    }
}
