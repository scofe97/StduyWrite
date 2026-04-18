package com.runnershigh.modulith.runner;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * 러너 레벨 Value Object 단위 테스트
 */
class RunnerLevelTest {

    @Nested
    @DisplayName("다음 레벨")
    class Next {

        @ParameterizedTest(name = "{0} → {1}")
        @CsvSource({
                "BEGINNER, INTERMEDIATE",
                "INTERMEDIATE, ADVANCED",
                "ADVANCED, ELITE",
                "ELITE, ELITE"
        })
        @DisplayName("각 레벨의 다음 레벨")
        void nextLevel(RunnerLevel current, RunnerLevel expected) {
            assertThat(current.next()).isEqualTo(expected);
        }
    }

    @Nested
    @DisplayName("레벨 비교")
    class Comparison {

        @Test
        @DisplayName("ELITE는 모든 레벨 이상")
        void eliteIsAtLeastAllLevels() {
            assertThat(RunnerLevel.ELITE.isAtLeast(RunnerLevel.BEGINNER)).isTrue();
            assertThat(RunnerLevel.ELITE.isAtLeast(RunnerLevel.INTERMEDIATE)).isTrue();
            assertThat(RunnerLevel.ELITE.isAtLeast(RunnerLevel.ADVANCED)).isTrue();
            assertThat(RunnerLevel.ELITE.isAtLeast(RunnerLevel.ELITE)).isTrue();
        }

        @Test
        @DisplayName("BEGINNER는 BEGINNER 이상만 만족")
        void beginnerComparisons() {
            assertThat(RunnerLevel.BEGINNER.isAtLeast(RunnerLevel.BEGINNER)).isTrue();
            assertThat(RunnerLevel.BEGINNER.isAtLeast(RunnerLevel.INTERMEDIATE)).isFalse();
        }
    }

    @Nested
    @DisplayName("최고 레벨 확인")
    class IsMaxLevel {

        @Test
        @DisplayName("ELITE만 최고 레벨")
        void onlyEliteIsMaxLevel() {
            assertThat(RunnerLevel.BEGINNER.isMaxLevel()).isFalse();
            assertThat(RunnerLevel.INTERMEDIATE.isMaxLevel()).isFalse();
            assertThat(RunnerLevel.ADVANCED.isMaxLevel()).isFalse();
            assertThat(RunnerLevel.ELITE.isMaxLevel()).isTrue();
        }
    }

    @Nested
    @DisplayName("표시명")
    class DisplayName {

        @ParameterizedTest(name = "{0} = {1}")
        @CsvSource({
                "BEGINNER, 초보",
                "INTERMEDIATE, 중급",
                "ADVANCED, 고급",
                "ELITE, 엘리트"
        })
        @DisplayName("한글 표시명")
        void koreanDisplayNames(RunnerLevel level, String expected) {
            assertThat(level.getDisplayName()).isEqualTo(expected);
        }
    }
}
