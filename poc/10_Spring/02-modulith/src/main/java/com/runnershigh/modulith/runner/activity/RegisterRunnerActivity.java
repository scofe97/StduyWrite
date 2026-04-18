package com.runnershigh.modulith.runner.activity;

/**
 * 러너 등록 Activity Interface
 *
 * <p>설계 문서의 "러너 등록" Activity Diagram과 1:1 매핑됩니다.
 *
 * <pre>
 * [비즈니스 플로우]
 * 1. 이메일 중복 확인 (Action)
 * 2. 러너 생성 (Action)
 * 3. 등록 이벤트 발행 (Action)
 * </pre>
 *
 * @see RegisterRunnerCommand 입력 명령
 * @see RegisterResult 결과 (Sealed Interface)
 */
public interface RegisterRunnerActivity {

    /**
     * 러너를 등록합니다.
     *
     * @param command 등록에 필요한 정보
     * @return 등록 결과 (Success 또는 Failure)
     */
    RegisterResult register(RegisterRunnerCommand command);

    /**
     * 이메일 사용 가능 여부를 확인합니다.
     *
     * @param email 확인할 이메일
     * @return 사용 가능하면 true
     */
    boolean isEmailAvailable(String email);
}
