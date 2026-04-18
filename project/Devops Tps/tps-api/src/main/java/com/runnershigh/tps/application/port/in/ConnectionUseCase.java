package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ProviderType;

import java.util.List;
import java.util.UUID;

/**
 * Connection 도메인의 인바운드 포트 (Use Case)
 *
 * <p>Git Provider(GitHub, GitLab, Bitbucket) 연결을 관리하는 유스케이스를 정의합니다.
 * Controller(Adapter-In)가 이 인터페이스에 의존하며, ConnectionService가 구현합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * Controller (Adapter-In)
 *      │
 *      ▼
 * ConnectionUseCase (Port-In) ◀── 현재 위치
 *      │
 *      ▼
 * ConnectionService (구현체)
 * </pre>
 *
 * <h2>사용 예시</h2>
 * <pre>{@code
 * // Controller에서 UseCase 호출
 * @RequiredArgsConstructor
 * public class ConnectionController {
 *     private final ConnectionUseCase connectionUseCase;
 *
 *     public ApiResponse<ConnectionResponse> create(ConnectionRequest.Create request) {
 *         CreateConnectionCommand command = new CreateConnectionCommand(...);
 *         Connection connection = connectionUseCase.createConnection(command);
 *         return ApiResponse.success(ConnectionResponse.from(connection));
 *     }
 * }
 * }</pre>
 *
 * @see com.runnershigh.tps.application.service.ConnectionService
 * @see com.runnershigh.tps.adapter.in.web.ConnectionController
 */
public interface ConnectionUseCase {

    /**
     * 새로운 Git Provider 연결을 생성합니다.
     *
     * <p>연결 생성 시 초기 상태는 {@code PENDING}이며,
     * {@link #testConnection(UUID)}을 통해 연결 테스트 후 {@code ACTIVE}로 변경됩니다.</p>
     *
     * <h3>처리 흐름</h3>
     * <pre>
     * 1. Command → Connection 도메인 객체 생성
     * 2. ConnectionRepository.save() 호출
     * 3. 생성된 Connection 반환 (status: PENDING)
     * </pre>
     *
     * @param command 연결 생성에 필요한 정보를 담은 Command 객체
     * @return 생성된 Connection 도메인 객체 (status: PENDING)
     * @see CreateConnectionCommand
     */
    Connection createConnection(CreateConnectionCommand command);

    /**
     * 기존 연결 정보를 수정합니다.
     *
     * <p>변경하지 않을 필드는 Command에서 null로 전달합니다.
     * null이 아닌 필드만 업데이트됩니다.</p>
     *
     * @param id      수정할 연결의 UUID
     * @param command 수정할 정보를 담은 Command 객체 (null 필드는 무시)
     * @return 수정된 Connection 도메인 객체
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     * @see UpdateConnectionCommand
     */
    Connection updateConnection(UUID id, UpdateConnectionCommand command);

    /**
     * 연결 상세 정보를 조회합니다.
     *
     * @param id 조회할 연결의 UUID
     * @return Connection 도메인 객체
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     */
    Connection getConnection(UUID id);

    /**
     * 특정 프로젝트의 모든 연결을 조회합니다.
     *
     * <p>하나의 프로젝트는 여러 Git Provider 연결을 가질 수 있습니다.
     * (예: GitHub 연결 + 회사 GitLab 연결)</p>
     *
     * @param projectId 프로젝트 UUID
     * @return 해당 프로젝트의 연결 목록 (생성일 기준 내림차순)
     */
    List<Connection> getConnectionsByProjectId(UUID projectId);

    /**
     * 특정 Provider 타입의 모든 연결을 조회합니다.
     *
     * <p>전체 시스템에서 특정 Provider를 사용하는 연결 현황 파악에 사용됩니다.</p>
     *
     * @param providerType Provider 타입 (GITHUB, GITLAB, BITBUCKET)
     * @return 해당 타입의 연결 목록
     * @see ProviderType
     */
    List<Connection> getConnectionsByProviderType(ProviderType providerType);

    /**
     * 활성 상태(ACTIVE)인 모든 연결을 조회합니다.
     *
     * <p>실제 Git 작업에 사용 가능한 연결 목록을 조회합니다.
     * PENDING, INACTIVE, FAILED 상태의 연결은 제외됩니다.</p>
     *
     * @return 활성 상태 연결 목록
     */
    List<Connection> getActiveConnections();

    /**
     * 연결을 삭제합니다.
     *
     * <p><strong>주의:</strong> 연결을 삭제하면 해당 연결을 사용하는
     * 모든 Repository도 함께 삭제됩니다 (CASCADE).</p>
     *
     * @param id 삭제할 연결의 UUID
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     */
    void deleteConnection(UUID id);

    /**
     * 연결을 활성화합니다.
     *
     * <p>비활성화(INACTIVE) 상태의 연결을 다시 활성화합니다.
     * 연결 테스트 없이 즉시 ACTIVE 상태로 변경됩니다.</p>
     *
     * @param id 활성화할 연결의 UUID
     * @return 활성화된 Connection (status: ACTIVE)
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     */
    Connection activateConnection(UUID id);

    /**
     * 연결을 비활성화합니다.
     *
     * <p>활성 연결을 일시적으로 비활성화합니다.
     * 비활성화된 연결은 Git 작업에 사용되지 않습니다.</p>
     *
     * @param id 비활성화할 연결의 UUID
     * @return 비활성화된 Connection (status: INACTIVE)
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     */
    Connection deactivateConnection(UUID id);

    /**
     * Git Provider 연결을 테스트합니다.
     *
     * <h3>처리 흐름</h3>
     * <pre>
     * 1. 연결 상태를 TESTING으로 변경
     * 2. Git-API(Go)로 Kafka 메시지 발행 (향후 구현)
     * 3. Provider API 호출하여 인증 확인
     * 4. 성공 시 ACTIVE, 실패 시 FAILED로 상태 변경
     * </pre>
     *
     * <p><strong>현재 상태:</strong> Git-API 연동 전이므로 항상 true 반환</p>
     *
     * @param id 테스트할 연결의 UUID
     * @return 연결 테스트 성공 여부
     * @throws IllegalArgumentException 연결을 찾을 수 없는 경우
     */
    boolean testConnection(UUID id);

    /**
     * 연결 생성 Command
     *
     * <p>새로운 Git Provider 연결 생성에 필요한 정보를 캡슐화합니다.</p>
     *
     * @param projectId    연결이 속할 프로젝트 UUID
     * @param providerType Provider 타입 (GITHUB, GITLAB, BITBUCKET)
     * @param name         연결 식별 이름 (예: "회사 GitHub", "팀 GitLab")
     * @param baseUrl      API Base URL (Self-hosted의 경우 필수, Cloud는 null 가능)
     * @param apiToken     인증 토큰 (Personal Access Token 등)
     * @param metadata     추가 메타데이터 (JSON 형식, 예: {"org": "my-org"})
     */
    record CreateConnectionCommand(
            UUID projectId,
            ProviderType providerType,
            String name,
            String baseUrl,
            String apiToken,
            String metadata
    ) {}

    /**
     * 연결 수정 Command
     *
     * <p>연결 정보 수정에 사용됩니다. null 필드는 수정하지 않습니다.</p>
     *
     * @param name     수정할 연결 이름 (null이면 변경 없음)
     * @param baseUrl  수정할 Base URL (null이면 변경 없음)
     * @param apiToken 수정할 API 토큰 (null이면 변경 없음)
     * @param metadata 수정할 메타데이터 (null이면 변경 없음)
     */
    record UpdateConnectionCommand(
            String name,
            String baseUrl,
            String apiToken,
            String metadata
    ) {}
}
