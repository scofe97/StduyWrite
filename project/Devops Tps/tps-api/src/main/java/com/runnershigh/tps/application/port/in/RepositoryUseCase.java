package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.repository.BranchStrategyType;
import com.runnershigh.tps.domain.repository.Repository;

import java.util.List;
import java.util.UUID;

/**
 * Repository 도메인의 인바운드 포트 (Use Case)
 *
 * <p>Git 저장소를 관리하는 유스케이스를 정의합니다.
 * 저장소는 반드시 Connection(Git Provider 연결)에 속해야 합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * RepositoryController (Adapter-In)
 *           │
 *           ▼
 *   RepositoryUseCase (Port-In) ◀── 현재 위치
 *           │
 *           ▼
 *   RepositoryService (구현체)
 *           │
 *           ▼
 *   RepositoryRepository (Port-Out)
 * </pre>
 *
 * <h2>도메인 관계</h2>
 * <pre>
 * Project ──┬── Connection (Git Provider 연결)
 *           │        │
 *           │        └── Repository (Git 저장소) ◀── 현재 도메인
 *           │                  │
 *           │                  └── Branch (Git 브랜치)
 *           │
 *           └── Repository (직접 연결)
 * </pre>
 *
 * @see com.runnershigh.tps.application.service.RepositoryService
 * @see com.runnershigh.tps.adapter.in.web.RepositoryController
 */
public interface RepositoryUseCase {

    /**
     * 새로운 Git 저장소를 등록합니다.
     *
     * <h3>처리 흐름</h3>
     * <pre>
     * 1. Git URL 파싱 (protocol, host, owner, repo 분리)
     * 2. Repository 도메인 객체 생성
     * 3. RepositoryRepository.save() 호출
     * 4. 생성된 Repository 반환
     * </pre>
     *
     * <h3>Git URL 파싱 예시</h3>
     * <pre>
     * https://github.com/owner/repo.git
     * ↓ 파싱
     * protocol: https
     * host: github.com
     * owner: owner
     * repo: repo
     * </pre>
     *
     * @param command 저장소 등록에 필요한 정보를 담은 Command 객체
     * @return 생성된 Repository 도메인 객체
     * @see CreateRepositoryCommand
     */
    Repository createRepository(CreateRepositoryCommand command);

    /**
     * 저장소 정보를 수정합니다.
     *
     * <p>수정 가능한 항목: 이름, 기본 브랜치, 브랜치 전략, 메타데이터</p>
     * <p>Git URL(host, owner, repo)은 수정 불가합니다.</p>
     *
     * @param id      수정할 저장소의 UUID
     * @param command 수정할 정보를 담은 Command 객체
     * @return 수정된 Repository 도메인 객체
     * @throws IllegalArgumentException 저장소를 찾을 수 없는 경우
     */
    Repository updateRepository(UUID id, UpdateRepositoryCommand command);

    /**
     * 저장소 상세 정보를 조회합니다.
     *
     * @param id 조회할 저장소의 UUID
     * @return Repository 도메인 객체
     * @throws IllegalArgumentException 저장소를 찾을 수 없는 경우
     */
    Repository getRepository(UUID id);

    /**
     * 모든 저장소를 조회합니다.
     *
     * @return 전체 저장소 목록
     */
    List<Repository> getAllRepositories();

    /**
     * 특정 프로젝트의 모든 저장소를 조회합니다.
     *
     * <p>하나의 프로젝트는 여러 저장소를 가질 수 있으며,
     * 각 저장소는 서로 다른 Connection을 사용할 수 있습니다.</p>
     *
     * @param projectId 프로젝트 UUID
     * @return 해당 프로젝트의 저장소 목록
     */
    List<Repository> getRepositoriesByProjectId(UUID projectId);

    /**
     * 특정 Connection(Git Provider 연결)의 모든 저장소를 조회합니다.
     *
     * <p>하나의 Connection은 여러 저장소를 관리할 수 있습니다.
     * (예: 회사 GitLab 연결 → 여러 프로젝트 저장소)</p>
     *
     * @param connectionId Connection UUID
     * @return 해당 연결의 저장소 목록
     */
    List<Repository> getRepositoriesByConnectionId(UUID connectionId);

    /**
     * 저장소를 삭제합니다.
     *
     * <p><strong>주의:</strong> 저장소를 삭제하면 해당 저장소의
     * 모든 Branch도 함께 삭제됩니다 (CASCADE).</p>
     *
     * <p><strong>참고:</strong> 실제 Git Provider의 저장소는 삭제되지 않으며,
     * TPS 시스템에서의 등록만 해제됩니다.</p>
     *
     * @param id 삭제할 저장소의 UUID
     * @throws IllegalArgumentException 저장소를 찾을 수 없는 경우
     */
    void deleteRepository(UUID id);

    /**
     * 저장소를 Git Provider와 동기화합니다.
     *
     * <h3>처리 흐름</h3>
     * <pre>
     * 1. 저장소 상태를 SYNCING으로 변경
     * 2. Git-API(Go)로 Kafka 메시지 발행 (향후 구현)
     * 3. Git Provider에서 브랜치 목록, 최신 커밋 등 조회
     * 4. 성공 시 ACTIVE, 실패 시 ERROR로 상태 변경
     * 5. lastSyncAt 타임스탬프 업데이트
     * </pre>
     *
     * <p><strong>현재 상태:</strong> Git-API 연동 전이므로 상태만 변경</p>
     *
     * @param id 동기화할 저장소의 UUID
     * @return 동기화된 Repository (status: ACTIVE, lastSyncAt 업데이트)
     * @throws IllegalArgumentException 저장소를 찾을 수 없는 경우
     */
    Repository syncRepository(UUID id);

    /**
     * 저장소 생성 Command
     *
     * <p>새로운 Git 저장소 등록에 필요한 정보를 캡슐화합니다.</p>
     *
     * @param projectId     저장소가 속할 프로젝트 UUID
     * @param connectionId  사용할 Connection UUID (Git Provider 연결)
     * @param name          저장소 표시 이름 (예: "백엔드 API")
     * @param gitUrl        Git 저장소 URL (예: "https://github.com/owner/repo.git")
     * @param defaultBranch 기본 브랜치 (예: "main", "master")
     * @param strategyType  브랜치 전략 (GIT_FLOW, GITHUB_FLOW, TRUNK_BASED)
     * @param metadata      추가 메타데이터 (JSON 형식)
     * @see BranchStrategyType
     */
    record CreateRepositoryCommand(
            UUID projectId,
            UUID connectionId,
            String name,
            String gitUrl,
            String defaultBranch,
            BranchStrategyType strategyType,
            String metadata
    ) {}

    /**
     * 저장소 수정 Command
     *
     * <p>저장소 정보 수정에 사용됩니다. null 필드는 수정하지 않습니다.</p>
     *
     * @param name          수정할 저장소 이름 (null이면 변경 없음)
     * @param defaultBranch 수정할 기본 브랜치 (null이면 변경 없음)
     * @param strategyType  수정할 브랜치 전략 (null이면 변경 없음)
     * @param metadata      수정할 메타데이터 (null이면 변경 없음)
     */
    record UpdateRepositoryCommand(
            String name,
            String defaultBranch,
            BranchStrategyType strategyType,
            String metadata
    ) {}
}
