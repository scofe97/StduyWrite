package com.runnershigh.modulith.runner.internal;

import com.runnershigh.modulith.runner.Runner;
import com.runnershigh.modulith.runner.RunnerRegisteredEvent;
import com.runnershigh.modulith.runner.activity.RegisterResult;
import com.runnershigh.modulith.runner.activity.RegisterRunnerActivity;
import com.runnershigh.modulith.runner.activity.RegisterRunnerCommand;
import com.runnershigh.modulith.runner.port.RunnerRepository;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 러너 서비스 - Activity Interface 구현체
 *
 * <p>internal 패키지에 위치하여 외부 모듈에서 직접 접근할 수 없습니다.
 * 외부에서는 Activity Interface를 통해서만 접근합니다.
 *
 * <pre>
 * [Controller] → [RegisterRunnerActivity(Interface)] ← [RunnerService(구현)]
 * </pre>
 */
@Service
class RunnerService implements RegisterRunnerActivity {

    private final RunnerRepository runnerRepository;
    private final ApplicationEventPublisher eventPublisher;

    RunnerService(RunnerRepository runnerRepository, ApplicationEventPublisher eventPublisher) {
        this.runnerRepository = runnerRepository;
        this.eventPublisher = eventPublisher;
    }

    /**
     * 러너 등록 - 메인 플로우
     *
     * <pre>
     * [비즈니스 플로우]
     * 1. 이메일 중복 확인 (Action)
     * 2. 러너 생성 (Action)
     * 3. 등록 이벤트 발행 (Action)
     * </pre>
     */
    @Override
    @Transactional
    public RegisterResult register(RegisterRunnerCommand command) {
        // Action 1: 이메일 중복 확인
        if (!isEmailAvailable(command.email())) {
            return new RegisterResult.Failure(
                    "이미 등록된 이메일입니다: " + command.email(),
                    RegisterResult.Failure.FailureType.DUPLICATE_EMAIL
            );
        }

        try {
            // Action 2: 러너 생성 및 저장
            Runner runner = Runner.create(command.name(), command.email());
            Runner saved = runnerRepository.save(runner);

            // Action 3: 등록 이벤트 발행
            eventPublisher.publishEvent(
                    new RunnerRegisteredEvent(saved.getId(), saved.getEmail())
            );

            return new RegisterResult.Success(saved.getId(), saved.getName());

        } catch (IllegalArgumentException e) {
            return new RegisterResult.Failure(
                    e.getMessage(),
                    RegisterResult.Failure.FailureType.INVALID_DATA
            );
        } catch (Exception e) {
            return new RegisterResult.Failure(
                    "시스템 오류가 발생했습니다",
                    RegisterResult.Failure.FailureType.SYSTEM_ERROR
            );
        }
    }

    /**
     * 이메일 사용 가능 여부 확인 (Action)
     */
    @Override
    @Transactional(readOnly = true)
    public boolean isEmailAvailable(String email) {
        return !runnerRepository.existsByEmail(email.toLowerCase());
    }
}
