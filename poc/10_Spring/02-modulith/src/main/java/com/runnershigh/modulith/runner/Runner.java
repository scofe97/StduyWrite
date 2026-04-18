package com.runnershigh.modulith.runner;

import java.time.LocalDateTime;

/**
 * 러너 도메인 엔티티
 *
 * <p>비즈니스 로직을 포함하는 Rich Domain Model입니다.
 * 생성과 레벨 관리에 대한 규칙을 캡슐화합니다.
 */
public class Runner {

    private Long id;
    private String name;
    private String email;
    private RunnerLevel level;
    private LocalDateTime registeredAt;

    // JPA를 위한 기본 생성자
    protected Runner() {
    }

    private Runner(String name, String email) {
        this.name = validateName(name);
        this.email = validateEmail(email);
        this.level = RunnerLevel.BEGINNER;
        this.registeredAt = LocalDateTime.now();
    }

    /**
     * 새로운 러너를 생성합니다.
     *
     * @param name  러너 이름
     * @param email 러너 이메일
     * @return 생성된 러너
     * @throws IllegalArgumentException 유효하지 않은 입력
     */
    public static Runner create(String name, String email) {
        return new Runner(name, email);
    }

    /**
     * 다음 레벨로 승급합니다.
     *
     * <p>이미 최고 레벨인 경우 변경되지 않습니다.
     *
     * @return 승급 후 레벨
     */
    public RunnerLevel promote() {
        this.level = this.level.next();
        return this.level;
    }

    /**
     * 레벨을 직접 설정합니다. (관리자 기능)
     *
     * @param newLevel 새로운 레벨
     */
    public void setLevel(RunnerLevel newLevel) {
        if (newLevel == null) {
            throw new IllegalArgumentException("레벨은 null일 수 없습니다");
        }
        this.level = newLevel;
    }

    // ===== Validation =====

    private static String validateName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("이름은 필수입니다");
        }
        String trimmed = name.trim();
        if (trimmed.length() < 2 || trimmed.length() > 50) {
            throw new IllegalArgumentException("이름은 2~50자여야 합니다");
        }
        return trimmed;
    }

    private static String validateEmail(String email) {
        if (email == null || email.isBlank()) {
            throw new IllegalArgumentException("이메일은 필수입니다");
        }
        String normalized = email.trim().toLowerCase();
        if (!normalized.contains("@") || !normalized.contains(".")) {
            throw new IllegalArgumentException("유효하지 않은 이메일 형식입니다");
        }
        return normalized;
    }

    // ===== Getters =====

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public RunnerLevel getLevel() {
        return level;
    }

    public LocalDateTime getRegisteredAt() {
        return registeredAt;
    }

    // 테스트용 ID 설정 (package-private)
    void setId(Long id) {
        this.id = id;
    }
}
