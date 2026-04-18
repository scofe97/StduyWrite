package com.runnershigh.modulith.runner;

/**
 * 러너 레벨 (Value Object)
 *
 * <p>레벨 승급 규칙을 캡슐화합니다.
 *
 * <pre>
 * BEGINNER → INTERMEDIATE → ADVANCED → ELITE
 * </pre>
 */
public enum RunnerLevel {

    /** 초보 러너 */
    BEGINNER("초보", 1),

    /** 중급 러너 */
    INTERMEDIATE("중급", 2),

    /** 고급 러너 */
    ADVANCED("고급", 3),

    /** 엘리트 러너 */
    ELITE("엘리트", 4);

    private final String displayName;
    private final int order;

    RunnerLevel(String displayName, int order) {
        this.displayName = displayName;
        this.order = order;
    }

    /**
     * 다음 레벨을 반환합니다.
     *
     * @return 다음 레벨 (ELITE인 경우 ELITE 유지)
     */
    public RunnerLevel next() {
        return switch (this) {
            case BEGINNER -> INTERMEDIATE;
            case INTERMEDIATE -> ADVANCED;
            case ADVANCED, ELITE -> ELITE;
        };
    }

    /**
     * 현재 레벨이 대상 레벨보다 높거나 같은지 확인합니다.
     *
     * @param other 비교 대상 레벨
     * @return 높거나 같으면 true
     */
    public boolean isAtLeast(RunnerLevel other) {
        return this.order >= other.order;
    }

    /**
     * 최고 레벨인지 확인합니다.
     *
     * @return ELITE면 true
     */
    public boolean isMaxLevel() {
        return this == ELITE;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getOrder() {
        return order;
    }
}
