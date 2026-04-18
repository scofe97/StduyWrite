package com.runnershigh.tps.application.port.out;

import com.runnershigh.tps.domain.repository.Repository;
import com.runnershigh.tps.domain.repository.RepositoryStatus;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Repository 도메인의 아웃바운드 포트 (Repository)
 *
 * <p>Git 저장소 엔티티의 영속성 작업을 정의하는 인터페이스입니다.
 * Service가 이 인터페이스에 의존하며, PersistenceAdapter가 구현합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * RepositoryService (Application)
 *         │
 *         ▼
 * RepositoryRepository (Port-Out) ◀── 현재 위치
 *         │
 *         ▼
 * RepositoryPersistenceAdapter (Adapter-Out)
 *         │
 *         ▼
 * RepositoryMapper (MyBatis)
 *         │
 *         ▼
 *    PostgreSQL
 * </pre>
 *
 * <h2>도메인 관계</h2>
 * <pre>
 * Connection ──────┐
 *                  │
 *                  ▼
 *            Repository ◀── 현재 도메인
 *                  │
 *                  ▼
 *              Branch
 * </pre>
 *
 * <h2>주요 제약조건</h2>
 * <ul>
 *   <li>저장소는 반드시 Connection에 속해야 함</li>
 *   <li>프로젝트 내 저장소 이름은 유일해야 함 (UNIQUE INDEX)</li>
 *   <li>삭제 시 하위 Branch도 CASCADE 삭제됨</li>
 * </ul>
 *
 * @see com.runnershigh.tps.adapter.out.persistence.RepositoryPersistenceAdapter
 * @see com.runnershigh.tps.adapter.out.persistence.RepositoryMapper
 */
public interface RepositoryRepository {

    /**
     * 새로운 Repository를 저장합니다.
     *
     * <p>저장 전 Repository의 id, createdAt, updatedAt이 자동 설정됩니다.</p>
     *
     * <h3>DB 제약조건</h3>
     * <ul>
     *   <li>project_id + name 조합은 유일해야 함</li>
     *   <li>connection_id는 유효한 Connection을 참조해야 함</li>
     * </ul>
     *
     * @param repository 저장할 Repository 도메인 객체
     * @return 저장된 Repository (id가 할당됨)
     */
    Repository save(Repository repository);

    /**
     * 기존 Repository를 수정합니다.
     *
     * <p>수정 전 updatedAt이 자동으로 갱신됩니다.</p>
     *
     * @param repository 수정할 Repository 도메인 객체
     * @return 수정된 Repository
     */
    Repository update(Repository repository);

    /**
     * ID로 Repository를 조회합니다.
     *
     * @param id 조회할 Repository의 UUID
     * @return Repository를 담은 Optional (없으면 Optional.empty())
     */
    Optional<Repository> findById(UUID id);

    /**
     * 프로젝트 ID로 Repository 목록을 조회합니다.
     *
     * <p>하나의 프로젝트는 여러 저장소를 가질 수 있으며,
     * 각 저장소는 서로 다른 Connection(Git Provider)을 사용할 수 있습니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>프로젝트 대시보드에서 저장소 목록 표시</li>
     *   <li>프로젝트별 저장소 관리 화면</li>
     * </ul>
     *
     * @param projectId 프로젝트 UUID
     * @return 해당 프로젝트의 Repository 목록
     */
    List<Repository> findByProjectId(UUID projectId);

    /**
     * Connection ID로 Repository 목록을 조회합니다.
     *
     * <p>하나의 Connection(Git Provider 연결)은 여러 저장소를 관리할 수 있습니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>Connection 삭제 전 영향받는 저장소 확인</li>
     *   <li>특정 Git Provider의 저장소 목록 조회</li>
     * </ul>
     *
     * @param connectionId Connection UUID
     * @return 해당 Connection의 Repository 목록
     */
    List<Repository> findByConnectionId(UUID connectionId);

    /**
     * 상태로 Repository 목록을 조회합니다.
     *
     * <h3>상태별 의미</h3>
     * <ul>
     *   <li>ACTIVE: 정상 운영 중인 저장소</li>
     *   <li>INACTIVE: 비활성화된 저장소</li>
     *   <li>SYNCING: 동기화 진행 중</li>
     *   <li>ERROR: 동기화 오류 발생</li>
     * </ul>
     *
     * @param status Repository 상태
     * @return 해당 상태의 Repository 목록
     * @see RepositoryStatus
     */
    List<Repository> findByStatus(RepositoryStatus status);

    /**
     * 프로젝트 ID와 이름으로 Repository를 조회합니다.
     *
     * <p>프로젝트 내에서 저장소 이름은 유일해야 하므로,
     * 이 메서드는 최대 1개의 결과를 반환합니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>저장소 이름 중복 검사</li>
     *   <li>이름 기반 저장소 조회</li>
     * </ul>
     *
     * @param projectId 프로젝트 UUID
     * @param name      저장소 이름
     * @return Repository를 담은 Optional (없으면 Optional.empty())
     */
    Optional<Repository> findByProjectIdAndName(UUID projectId, String name);

    /**
     * ID로 Repository를 삭제합니다.
     *
     * <p><strong>주의:</strong> 해당 Repository의 모든 Branch도
     * CASCADE로 함께 삭제됩니다.</p>
     *
     * <p><strong>참고:</strong> 실제 Git Provider의 저장소는 삭제되지 않으며,
     * TPS 시스템에서의 등록만 해제됩니다.</p>
     *
     * @param id 삭제할 Repository의 UUID
     */
    void deleteById(UUID id);

    /**
     * ID로 Repository 존재 여부를 확인합니다.
     *
     * <p>전체 데이터를 조회하지 않고 COUNT로 빠르게 확인합니다.</p>
     *
     * @param id 확인할 Repository의 UUID
     * @return 존재하면 true, 없으면 false
     */
    boolean existsById(UUID id);

    /**
     * 모든 Repository를 조회합니다.
     *
     * @return 전체 Repository 목록
     */
    List<Repository> findAll();
}
