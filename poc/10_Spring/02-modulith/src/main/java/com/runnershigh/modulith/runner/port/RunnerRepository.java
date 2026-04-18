package com.runnershigh.modulith.runner.port;

import com.runnershigh.modulith.runner.Runner;
import com.runnershigh.modulith.runner.RunnerLevel;

import java.util.List;
import java.util.Optional;

/**
 * 러너 저장소 Port (Outbound)
 *
 * <p>Hexagonal Architecture의 Outbound Port입니다.
 * 실제 구현체(JPA, In-Memory 등)는 internal 패키지에 위치합니다.
 *
 * <p>의존성 방향:
 * <pre>
 * [Service] → [Port(Interface)] ← [Adapter(구현체)]
 * </pre>
 */
public interface RunnerRepository {

    /**
     * 러너를 저장합니다.
     *
     * @param runner 저장할 러너
     * @return 저장된 러너 (ID 포함)
     */
    Runner save(Runner runner);

    /**
     * ID로 러너를 조회합니다.
     *
     * @param id 러너 ID
     * @return 러너 (없으면 empty)
     */
    Optional<Runner> findById(Long id);

    /**
     * 이메일로 러너를 조회합니다.
     *
     * @param email 이메일
     * @return 러너 (없으면 empty)
     */
    Optional<Runner> findByEmail(String email);

    /**
     * 이메일 존재 여부를 확인합니다.
     *
     * @param email 이메일
     * @return 존재하면 true
     */
    boolean existsByEmail(String email);

    /**
     * 레벨별 러너 목록을 조회합니다.
     *
     * @param level 러너 레벨
     * @return 해당 레벨의 러너 목록
     */
    List<Runner> findByLevel(RunnerLevel level);

    /**
     * 전체 러너를 조회합니다.
     *
     * @return 전체 러너 목록
     */
    List<Runner> findAll();
}
