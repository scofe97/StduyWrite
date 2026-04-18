package com.runnershigh.tps.application.port.out;

import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ConnectionStatus;
import com.runnershigh.tps.domain.connection.ProviderType;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Connection 도메인의 아웃바운드 포트 (Repository)
 *
 * <p>Connection 엔티티의 영속성 작업을 정의하는 인터페이스입니다.
 * Service가 이 인터페이스에 의존하며, PersistenceAdapter가 구현합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * ConnectionService (Application)
 *         │
 *         ▼
 * ConnectionRepository (Port-Out) ◀── 현재 위치
 *         │
 *         ▼
 * ConnectionPersistenceAdapter (Adapter-Out)
 *         │
 *         ▼
 * ConnectionMapper (MyBatis)
 *         │
 *         ▼
 *    PostgreSQL
 * </pre>
 *
 * <h2>설계 의도</h2>
 * <ul>
 *   <li><strong>기술 독립성</strong>: Service가 MyBatis에 직접 의존하지 않음</li>
 *   <li><strong>테스트 용이성</strong>: Mock 객체로 쉽게 대체 가능</li>
 *   <li><strong>기술 교체 용이</strong>: MyBatis → JPA 전환 시 Service 코드 변경 불필요</li>
 * </ul>
 *
 * <h2>구현체</h2>
 * <ul>
 *   <li>{@link com.runnershigh.tps.adapter.out.persistence.ConnectionPersistenceAdapter} - 운영 구현체</li>
 *   <li>테스트 시에는 Mock 또는 InMemory 구현체 사용</li>
 * </ul>
 *
 * @see com.runnershigh.tps.adapter.out.persistence.ConnectionPersistenceAdapter
 * @see com.runnershigh.tps.adapter.out.persistence.ConnectionMapper
 */
public interface ConnectionRepository {

    /**
     * 새로운 Connection을 저장합니다.
     *
     * <p>저장 전 Connection의 id, createdAt, updatedAt이 자동 설정됩니다.</p>
     *
     * <h3>MyBatis SQL</h3>
     * <pre>
     * INSERT INTO connections (id, project_id, provider_type, name, ...)
     * VALUES (#{id}, #{projectId}, #{providerType}, #{name}, ...)
     * </pre>
     *
     * @param connection 저장할 Connection 도메인 객체
     * @return 저장된 Connection (id가 할당됨)
     */
    Connection save(Connection connection);

    /**
     * 기존 Connection을 수정합니다.
     *
     * <p>수정 전 updatedAt이 자동으로 갱신됩니다.</p>
     *
     * <h3>MyBatis SQL</h3>
     * <pre>
     * UPDATE connections SET
     *     name = #{name}, base_url = #{baseUrl}, ...
     * WHERE id = #{id}
     * </pre>
     *
     * @param connection 수정할 Connection 도메인 객체
     * @return 수정된 Connection
     */
    Connection update(Connection connection);

    /**
     * ID로 Connection을 조회합니다.
     *
     * <h3>MyBatis SQL</h3>
     * <pre>
     * SELECT * FROM connections WHERE id = #{id}
     * </pre>
     *
     * @param id 조회할 Connection의 UUID
     * @return Connection을 담은 Optional (없으면 Optional.empty())
     */
    Optional<Connection> findById(UUID id);

    /**
     * 프로젝트 ID로 Connection 목록을 조회합니다.
     *
     * <p>하나의 프로젝트는 여러 Git Provider 연결을 가질 수 있습니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>프로젝트 설정 화면에서 연결 목록 표시</li>
     *   <li>Repository 등록 시 사용 가능한 Connection 목록 조회</li>
     * </ul>
     *
     * @param projectId 프로젝트 UUID
     * @return 해당 프로젝트의 Connection 목록 (생성일 기준 내림차순)
     */
    List<Connection> findByProjectId(UUID projectId);

    /**
     * Provider 타입으로 Connection 목록을 조회합니다.
     *
     * <p>전체 시스템에서 특정 Provider를 사용하는 연결 현황 파악에 사용됩니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>관리자 대시보드에서 GitHub 연결 통계</li>
     *   <li>특정 Provider 장애 시 영향받는 연결 파악</li>
     * </ul>
     *
     * @param providerType Provider 타입 (GITHUB, GITLAB, BITBUCKET)
     * @return 해당 타입의 Connection 목록
     */
    List<Connection> findByProviderType(ProviderType providerType);

    /**
     * 상태로 Connection 목록을 조회합니다.
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>FAILED 상태 조회 → 연결 문제 해결 필요</li>
     *   <li>PENDING 상태 조회 → 테스트 대기 중인 연결</li>
     *   <li>TESTING 상태 조회 → 현재 테스트 진행 중인 연결</li>
     * </ul>
     *
     * @param status Connection 상태
     * @return 해당 상태의 Connection 목록
     * @see ConnectionStatus
     */
    List<Connection> findByStatus(ConnectionStatus status);

    /**
     * 활성 상태(ACTIVE)인 Connection 목록을 조회합니다.
     *
     * <p>실제 Git 작업에 사용 가능한 연결만 조회합니다.
     * {@code findByStatus(ConnectionStatus.ACTIVE)}와 동일하지만,
     * 자주 사용되므로 별도 메서드로 제공합니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>Repository 등록 시 선택 가능한 연결 목록</li>
     *   <li>Git 작업 실행 시 사용할 연결 검증</li>
     * </ul>
     *
     * @return 활성 상태 Connection 목록
     */
    List<Connection> findActiveConnections();

    /**
     * ID로 Connection을 삭제합니다.
     *
     * <p><strong>주의:</strong> 해당 Connection을 사용하는 모든 Repository도
     * CASCADE로 함께 삭제됩니다.</p>
     *
     * <h3>MyBatis SQL</h3>
     * <pre>
     * DELETE FROM connections WHERE id = #{id}
     * </pre>
     *
     * @param id 삭제할 Connection의 UUID
     */
    void deleteById(UUID id);

    /**
     * ID로 Connection 존재 여부를 확인합니다.
     *
     * <p>전체 데이터를 조회하지 않고 COUNT로 빠르게 확인합니다.</p>
     *
     * <h3>MyBatis SQL</h3>
     * <pre>
     * SELECT COUNT(*) FROM connections WHERE id = #{id}
     * </pre>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>삭제 전 존재 여부 확인</li>
     *   <li>중복 생성 방지 검증</li>
     * </ul>
     *
     * @param id 확인할 Connection의 UUID
     * @return 존재하면 true, 없으면 false
     */
    boolean existsById(UUID id);
}
