package com.runnershigh.modulith.runner;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * 러너 도메인 엔티티 단위 테스트
 *
 * <p>순수 도메인 로직 테스트 - 외부 의존성 없음
 */
class RunnerTest {

    @Nested
    @DisplayName("러너 생성")
    class Create {

        @Test
        @DisplayName("유효한 정보로 생성하면 BEGINNER 레벨로 시작")
        void createsWithBeginnerLevel() {
            // When
            Runner runner = Runner.create("홍길동", "hong@test.com");

            // Then
            assertThat(runner.getName()).isEqualTo("홍길동");
            assertThat(runner.getEmail()).isEqualTo("hong@test.com");
            assertThat(runner.getLevel()).isEqualTo(RunnerLevel.BEGINNER);
            assertThat(runner.getRegisteredAt()).isNotNull();
        }

        @Test
        @DisplayName("이메일은 소문자로 정규화됨")
        void normalizesEmail() {
            // When
            Runner runner = Runner.create("테스트", "Test@Example.COM");

            // Then
            assertThat(runner.getEmail()).isEqualTo("test@example.com");
        }

        @Test
        @DisplayName("이름 앞뒤 공백 제거")
        void trimsName() {
            // When
            Runner runner = Runner.create("  홍길동  ", "test@test.com");

            // Then
            assertThat(runner.getName()).isEqualTo("홍길동");
        }

        @Test
        @DisplayName("null 이름으로 생성 시 예외 발생")
        void throwsWhenNameIsNull() {
            assertThatThrownBy(() -> Runner.create(null, "test@test.com"))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이름");
        }

        @Test
        @DisplayName("빈 이름으로 생성 시 예외 발생")
        void throwsWhenNameIsBlank() {
            assertThatThrownBy(() -> Runner.create("   ", "test@test.com"))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이름");
        }

        @Test
        @DisplayName("유효하지 않은 이메일로 생성 시 예외 발생")
        void throwsWhenEmailIsInvalid() {
            assertThatThrownBy(() -> Runner.create("홍길동", "invalid"))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이메일");
        }
    }

    @Nested
    @DisplayName("레벨 승급")
    class Promote {

        @Test
        @DisplayName("BEGINNER → INTERMEDIATE로 승급")
        void promotesFromBeginnerToIntermediate() {
            // Given
            Runner runner = Runner.create("테스트", "test@test.com");
            assertThat(runner.getLevel()).isEqualTo(RunnerLevel.BEGINNER);

            // When
            RunnerLevel newLevel = runner.promote();

            // Then
            assertThat(newLevel).isEqualTo(RunnerLevel.INTERMEDIATE);
            assertThat(runner.getLevel()).isEqualTo(RunnerLevel.INTERMEDIATE);
        }

        @Test
        @DisplayName("전체 승급 경로: BEGINNER → INTERMEDIATE → ADVANCED → ELITE")
        void fullPromotionPath() {
            // Given
            Runner runner = Runner.create("테스트", "test@test.com");

            // When & Then
            assertThat(runner.promote()).isEqualTo(RunnerLevel.INTERMEDIATE);
            assertThat(runner.promote()).isEqualTo(RunnerLevel.ADVANCED);
            assertThat(runner.promote()).isEqualTo(RunnerLevel.ELITE);
        }

        @Test
        @DisplayName("ELITE에서 승급해도 ELITE 유지")
        void staysAtElite() {
            // Given
            Runner runner = Runner.create("테스트", "test@test.com");
            runner.setLevel(RunnerLevel.ELITE);

            // When
            RunnerLevel newLevel = runner.promote();

            // Then
            assertThat(newLevel).isEqualTo(RunnerLevel.ELITE);
        }
    }

    @Nested
    @DisplayName("레벨 직접 설정")
    class SetLevel {

        @Test
        @DisplayName("관리자가 레벨 직접 설정 가능")
        void canSetLevelDirectly() {
            // Given
            Runner runner = Runner.create("테스트", "test@test.com");

            // When
            runner.setLevel(RunnerLevel.ADVANCED);

            // Then
            assertThat(runner.getLevel()).isEqualTo(RunnerLevel.ADVANCED);
        }

        @Test
        @DisplayName("null 레벨 설정 시 예외 발생")
        void throwsWhenLevelIsNull() {
            // Given
            Runner runner = Runner.create("테스트", "test@test.com");

            // When & Then
            assertThatThrownBy(() -> runner.setLevel(null))
                    .isInstanceOf(IllegalArgumentException.class);
        }
    }
}
