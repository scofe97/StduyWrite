package com.runnershigh.tps.application.port.out;

import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Branch 도메인의 아웃바운드 포트 (Repository)
 *
 * <p>Git 브랜치 엔티티의 영속성 작업을 정의하는 인터페이스입니다.
 * Service가 이 인터페이스에 의존하며, PersistenceAdapter가 구현합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * BranchService (Application)
 *         │
 *         ▼
 * BranchRepository (Port-Out) ◀── 현재 위치
 *         │
 *         ▼
 * BranchPersistenceAdapter (Adapter-Out)
 *         │
 *         ▼
 * BranchMapper (MyBatis)
 *         │
 *         ▼
 *    PostgreSQL
 * </pre>
 *
 * <h2>도메인 관계</h2>
 * <pre>
 * Repository (상위)
 *      │
 *      └── Branch ◀── 현재 도메인
 *           ├── MAIN
 *           ├── DEVELOP
 *           ├── FEATURE/*
 *           ├── RELEASE/*
 *           └── HOTFIX/*
 * </pre>
 *
 * <h2>주요 제약조건</h2>
 * <ul>
 *   <li>브랜치는 반드시 Repository에 속해야 함</li>
 *   <li>저장소 내 브랜치 이름은 유일해야 함 (UNIQUE INDEX)</li>
 *   <li>Repository 삭제 시 Branch도 CASCADE 삭제됨</li>
 * </ul>
 *
 * @see com.runnershigh.tps.adapter.out.persistence.BranchPersistenceAdapter
 * @see com.runnershigh.tps.adapter.out.persistence.BranchMapper
 */
public interface BranchRepository {

    /**
     * 새로운 Branch를 저장합니다.
     *
     * <p>저장 전 Branch의 id, createdAt, updatedAt이 자동 설정됩니다.</p>
     *
     * <h3>DB 제약조건</h3>
     * <ul>
     *   <li>repository_id + name 조합은 유일해야 함</li>
     *   <li>repository_id는 유효한 Repository를 참조해야 함</li>
     * </ul>
     *
     * @param branch 저장할 Branch 도메인 객체
     * @return 저장된 Branch (id가 할당됨)
     */
    Branch save(Branch branch);

    /**
     * 기존 Branch를 수정합니다.
     *
     * <p>수정 전 updatedAt이 자동으로 갱신됩니다.</p>
     *
     * @param branch 수정할 Branch 도메인 객체
     * @return 수정된 Branch
     */
    Branch update(Branch branch);

    /**
     * ID로 Branch를 조회합니다.
     *
     * @param id 조회할 Branch의 UUID
     * @return Branch를 담은 Optional (없으면 Optional.empty())
     */
    Optional<Branch> findById(UUID id);

    /**
     * 저장소 ID로 Branch 목록을 조회합니다.
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>저장소의 전체 브랜치 목록 표시</li>
     *   <li>브랜치 관리 화면</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @return 해당 저장소의 Branch 목록
     */
    List<Branch> findByRepositoryId(UUID repositoryId);

    /**
     * 저장소 ID와 상태로 Branch 목록을 조회합니다.
     *
     * <h3>상태별 활용</h3>
     * <ul>
     *   <li>ACTIVE: 현재 활성 브랜치 (작업 가능)</li>
     *   <li>MERGED: 병합 완료된 브랜치 (정리 대상)</li>
     *   <li>DELETED: 삭제된 브랜치 (히스토리 용도)</li>
     *   <li>STALE: 오래된 브랜치 (정리 권장)</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @param status       브랜치 상태
     * @return 해당 저장소에서 특정 상태의 Branch 목록
     * @see BranchStatus
     */
    List<Branch> findByRepositoryIdAndStatus(UUID repositoryId, BranchStatus status);

    /**
     * 저장소 ID와 타입으로 Branch 목록을 조회합니다.
     *
     * <h3>타입별 활용</h3>
     * <ul>
     *   <li>MAIN: 프로덕션 릴리스 브랜치</li>
     *   <li>DEVELOP: 개발 통합 브랜치</li>
     *   <li>FEATURE: 현재 개발 중인 기능들</li>
     *   <li>RELEASE: 릴리스 준비 중인 버전들</li>
     *   <li>HOTFIX: 긴급 수정 브랜치들</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @param type         브랜치 타입
     * @return 해당 저장소에서 특정 타입의 Branch 목록
     * @see BranchType
     */
    List<Branch> findByRepositoryIdAndType(UUID repositoryId, BranchType type);

    /**
     * 저장소 ID와 이름으로 Branch를 조회합니다.
     *
     * <p>저장소 내에서 브랜치 이름은 유일하므로,
     * 이 메서드는 최대 1개의 결과를 반환합니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>브랜치 이름 중복 검사</li>
     *   <li>이름 기반 브랜치 조회 (Git Webhook 처리 등)</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @param name         브랜치 이름
     * @return Branch를 담은 Optional (없으면 Optional.empty())
     */
    Optional<Branch> findByRepositoryIdAndName(UUID repositoryId, String name);

    /**
     * ID로 Branch를 삭제합니다.
     *
     * <p><strong>주의:</strong> 보호된 브랜치(isProtected=true)도
     * 이 메서드로 삭제됩니다. 보호 검증은 Service 레이어에서 수행해야 합니다.</p>
     *
     * @param id 삭제할 Branch의 UUID
     */
    void deleteById(UUID id);

    /**
     * 저장소의 모든 Branch를 삭제합니다.
     *
     * <p>Repository 삭제 시 CASCADE 대신 명시적으로 호출하거나,
     * 저장소 초기화 시 사용됩니다.</p>
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>저장소 재동기화 전 기존 브랜치 정리</li>
     *   <li>테스트 데이터 정리</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     */
    void deleteByRepositoryId(UUID repositoryId);

    /**
     * ID로 Branch 존재 여부를 확인합니다.
     *
     * <p>전체 데이터를 조회하지 않고 COUNT로 빠르게 확인합니다.</p>
     *
     * @param id 확인할 Branch의 UUID
     * @return 존재하면 true, 없으면 false
     */
    boolean existsById(UUID id);
}
