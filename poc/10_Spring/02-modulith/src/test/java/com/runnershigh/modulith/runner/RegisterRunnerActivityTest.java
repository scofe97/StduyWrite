package com.runnershigh.modulith.runner;

import com.runnershigh.modulith.runner.activity.RegisterResult;
import com.runnershigh.modulith.runner.activity.RegisterRunnerActivity;
import com.runnershigh.modulith.runner.activity.RegisterRunnerCommand;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.event.ApplicationEvents;
import org.springframework.test.context.event.RecordApplicationEvents;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * 러너 등록 Activity 테스트
 *
 * <p>Activity Interface를 통한 비즈니스 플로우 테스트입니다.
 * 내부 구현(RunnerService)이 아닌 공개 인터페이스를 테스트합니다.
 */
@SpringBootTest
@RecordApplicationEvents
class RegisterRunnerActivityTest {

    @Autowired
    private RegisterRunnerActivity registerActivity;

    @Autowired
    private ApplicationEvents events;

    @Nested
    @DisplayName("러너 등록")
    class Register {

        @Test
        @DisplayName("성공 - 유효한 정보로 등록하면 Success 반환")
        void success() {
            // Given
            var command = new RegisterRunnerCommand("홍길동", "hong@test.com");

            // When
            RegisterResult result = registerActivity.register(command);

            // Then
            assertThat(result).isInstanceOf(RegisterResult.Success.class);

            var success = (RegisterResult.Success) result;
            assertThat(success.runnerId()).isNotNull();
            assertThat(success.name()).isEqualTo("홍길동");
        }

        @Test
        @DisplayName("성공 - 등록 시 RunnerRegisteredEvent 발행")
        void publishesEvent() {
            // Given
            var command = new RegisterRunnerCommand("이벤트테스트", "event@test.com");

            // When
            registerActivity.register(command);

            // Then
            long eventCount = events.stream(RunnerRegisteredEvent.class).count();
            assertThat(eventCount).isGreaterThanOrEqualTo(1);
        }

        @Test
        @DisplayName("실패 - 중복 이메일로 등록하면 DUPLICATE_EMAIL 반환")
        void failWhenDuplicateEmail() {
            // Given - 먼저 등록
            var firstCommand = new RegisterRunnerCommand("첫번째", "duplicate@test.com");
            registerActivity.register(firstCommand);

            // When - 같은 이메일로 다시 등록
            var secondCommand = new RegisterRunnerCommand("두번째", "duplicate@test.com");
            RegisterResult result = registerActivity.register(secondCommand);

            // Then
            assertThat(result).isInstanceOf(RegisterResult.Failure.class);

            var failure = (RegisterResult.Failure) result;
            assertThat(failure.type()).isEqualTo(RegisterResult.Failure.FailureType.DUPLICATE_EMAIL);
        }
    }

    @Nested
    @DisplayName("이메일 사용 가능 여부 확인")
    class IsEmailAvailable {

        @Test
        @DisplayName("사용 가능한 이메일이면 true 반환")
        void returnsTrueForAvailableEmail() {
            // When
            boolean available = registerActivity.isEmailAvailable("new-email@test.com");

            // Then
            assertThat(available).isTrue();
        }

        @Test
        @DisplayName("이미 등록된 이메일이면 false 반환")
        void returnsFalseForExistingEmail() {
            // Given
            var command = new RegisterRunnerCommand("기존러너", "existing@test.com");
            registerActivity.register(command);

            // When
            boolean available = registerActivity.isEmailAvailable("existing@test.com");

            // Then
            assertThat(available).isFalse();
        }
    }

    @Nested
    @DisplayName("Command 유효성 검증")
    class CommandValidation {

        @Test
        @DisplayName("null 이름으로 Command 생성 시 예외 발생")
        void throwsWhenNameIsNull() {
            assertThatThrownBy(() -> new RegisterRunnerCommand(null, "test@test.com"))
                    .isInstanceOf(NullPointerException.class)
                    .hasMessageContaining("name");
        }

        @Test
        @DisplayName("빈 이름으로 Command 생성 시 예외 발생")
        void throwsWhenNameIsBlank() {
            assertThatThrownBy(() -> new RegisterRunnerCommand("  ", "test@test.com"))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("빈 값");
        }

        @Test
        @DisplayName("잘못된 이메일 형식으로 Command 생성 시 예외 발생")
        void throwsWhenEmailIsInvalid() {
            assertThatThrownBy(() -> new RegisterRunnerCommand("테스트", "invalid-email"))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이메일");
        }
    }

    @Nested
    @DisplayName("Sealed Interface 패턴 매칭")
    class SealedInterfacePatternMatching {

        @Test
        @DisplayName("switch 표현식으로 결과 처리")
        void handleResultWithSwitch() {
            // Given
            var command = new RegisterRunnerCommand("패턴매칭", "pattern@test.com");

            // When
            RegisterResult result = registerActivity.register(command);

            // Then - switch 표현식 사용
            String message = switch (result) {
                case RegisterResult.Success s ->
                        "등록 성공: " + s.name() + " (ID: " + s.runnerId() + ")";
                case RegisterResult.Failure f ->
                        "등록 실패: " + f.reason() + " [" + f.type() + "]";
            };

            assertThat(message).startsWith("등록 성공");
        }
    }
}
