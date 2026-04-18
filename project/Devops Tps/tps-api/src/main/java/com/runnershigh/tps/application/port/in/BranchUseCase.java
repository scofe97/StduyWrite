package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;

import java.util.List;
import java.util.UUID;

/**
 * Branch 도메인의 인바운드 포트 (Use Case)
 *
 * <p>Git 브랜치를 관리하는 유스케이스를 정의합니다.
 * 브랜치는 반드시 Repository에 속해야 합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * BranchController (Adapter-In)
 *         │
 *         ▼
 *   BranchUseCase (Port-In) ◀── 현재 위치
 *         │
 *         ▼
 *   BranchService (구현체)
 *         │
 *         ▼
 *   BranchRepository (Port-Out)
 * </pre>
 *
 * <h2>브랜치 타입별 역할 (Git Flow 기준)</h2>
 * <pre>
 * MAIN     ─── 프로덕션 릴리스 브랜치
 * DEVELOP  ─── 개발 통합 브랜치
 * FEATURE  ─── 기능 개발 브랜치 (feature/*)
 * RELEASE  ─── 릴리스 준비 브랜치 (release/*)
 * HOTFIX   ─── 긴급 수정 브랜치 (hotfix/*)
 * </pre>
 *
 * @see com.runnershigh.tps.application.service.BranchService
 * @see com.runnershigh.tps.adapter.in.web.BranchController
 */
public interface BranchUseCase {

    /**
     * 새로운 브랜치를 생성합니다.
     *
     * <h3>처리 흐름</h3>
     * <pre>
     * 1. Branch 도메인 객체 생성
     * 2. BranchType 결정 (명시적 지정 또는 브랜치명에서 추론)
     * 3. Git-API(Go)로 Kafka 메시지 발행 (향후 구현)
     * 4. Git Provider에서 실제 브랜치 생성
     * 5. 생성된 Branch 반환
     * </pre>
     *
     * <h3>브랜치 타입 추론 규칙</h3>
     * <pre>
     * main, master         → MAIN
     * develop, dev         → DEVELOP
     * feature/*            → FEATURE
     * release/*            → RELEASE
     * hotfix/*             → HOTFIX
     * 그 외                → FEATURE (기본값)
     * </pre>
     *
     * @param command 브랜치 생성에 필요한 정보를 담은 Command 객체
     * @return 생성된 Branch 도메인 객체
     * @see CreateBranchCommand
     */
    Branch createBranch(CreateBranchCommand command);

    /**
     * 브랜치 정보를 수정합니다.
     *
     * <p>수정 가능한 항목: 브랜치 타입, 보호 설정, 메타데이터</p>
     * <p>브랜치명은 수정 불가합니다 (Git에서 rename 필요).</p>
     *
     * @param id      수정할 브랜치의 UUID
     * @param command 수정할 정보를 담은 Command 객체
     * @return 수정된 Branch 도메인 객체
     * @throws IllegalArgumentException 브랜치를 찾을 수 없는 경우
     */
    Branch updateBranch(UUID id, UpdateBranchCommand command);

    /**
     * 브랜치 상세 정보를 조회합니다.
     *
     * @param id 조회할 브랜치의 UUID
     * @return Branch 도메인 객체
     * @throws IllegalArgumentException 브랜치를 찾을 수 없는 경우
     */
    Branch getBranch(UUID id);

    /**
     * 특정 저장소의 모든 브랜치를 조회합니다.
     *
     * @param repositoryId 저장소 UUID
     * @return 해당 저장소의 브랜치 목록
     */
    List<Branch> getBranchesByRepositoryId(UUID repositoryId);

    /**
     * 특정 저장소에서 특정 상태의 브랜치를 조회합니다.
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>ACTIVE 브랜치만 조회 → 현재 활성 브랜치</li>
     *   <li>MERGED 브랜치 조회 → 병합 완료된 브랜치</li>
     *   <li>STALE 브랜치 조회 → 정리가 필요한 오래된 브랜치</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @param status       브랜치 상태 (ACTIVE, MERGED, DELETED, STALE)
     * @return 해당 상태의 브랜치 목록
     * @see BranchStatus
     */
    List<Branch> getBranchesByRepositoryIdAndStatus(UUID repositoryId, BranchStatus status);

    /**
     * 특정 저장소에서 특정 타입의 브랜치를 조회합니다.
     *
     * <h3>사용 예시</h3>
     * <ul>
     *   <li>FEATURE 타입 조회 → 현재 개발 중인 기능 브랜치</li>
     *   <li>RELEASE 타입 조회 → 릴리스 준비 중인 브랜치</li>
     *   <li>HOTFIX 타입 조회 → 긴급 수정 브랜치</li>
     * </ul>
     *
     * @param repositoryId 저장소 UUID
     * @param type         브랜치 타입 (MAIN, DEVELOP, FEATURE, RELEASE, HOTFIX)
     * @return 해당 타입의 브랜치 목록
     * @see BranchType
     */
    List<Branch> getBranchesByRepositoryIdAndType(UUID repositoryId, BranchType type);

    /**
     * 브랜치를 삭제합니다.
     *
     * <p><strong>주의:</strong> 보호된 브랜치(isProtected=true)는
     * 삭제하기 전에 보호 설정을 해제해야 합니다.</p>
     *
     * <p><strong>참고:</strong> 실제 Git Provider의 브랜치 삭제는
     * Git-API(Go)를 통해 처리됩니다 (향후 구현).</p>
     *
     * @param id 삭제할 브랜치의 UUID
     * @throws IllegalArgumentException 브랜치를 찾을 수 없는 경우
     */
    void deleteBranch(UUID id);

    /**
     * 브랜치 상태를 변경합니다.
     *
     * <h3>상태 전이 다이어그램</h3>
     * <pre>
     * [생성] → ACTIVE → MERGED (병합됨)
     *              │
     *              ├──→ DELETED (삭제됨)
     *              │
     *              └──→ STALE (오래된 브랜치)
     * </pre>
     *
     * @param id     상태를 변경할 브랜치의 UUID
     * @param status 새로운 상태
     * @return 상태가 변경된 Branch
     * @throws IllegalArgumentException 브랜치를 찾을 수 없는 경우
     * @see BranchStatus
     */
    Branch updateBranchStatus(UUID id, BranchStatus status);

    /**
     * 브랜치의 최신 커밋 SHA를 업데이트합니다.
     *
     * <p>Git Provider 동기화 또는 Webhook 이벤트 수신 시
     * 브랜치의 최신 커밋 정보를 업데이트합니다.</p>
     *
     * <p>커밋 업데이트 시 브랜치 상태가 자동으로 ACTIVE로 변경됩니다.</p>
     *
     * @param id        커밋을 업데이트할 브랜치의 UUID
     * @param commitSha 최신 커밋 SHA (40자 해시)
     * @return 커밋이 업데이트된 Branch
     * @throws IllegalArgumentException 브랜치를 찾을 수 없는 경우
     */
    Branch updateCommit(UUID id, String commitSha);

    /**
     * 브랜치 생성 Command
     *
     * <p>새로운 브랜치 생성에 필요한 정보를 캡슐화합니다.</p>
     *
     * @param repositoryId     브랜치가 속할 저장소 UUID
     * @param name             브랜치명 (예: "feature/user-auth", "release/v1.0.0")
     * @param branchType       브랜치 타입 (null이면 브랜치명에서 추론)
     * @param sourceBranchName 분기 원본 브랜치명 (예: "develop", "main")
     * @param isProtected      브랜치 보호 설정 (true면 삭제/강제푸시 방지)
     * @param metadata         추가 메타데이터 (JSON 형식)
     * @see BranchType
     */
    record CreateBranchCommand(
            UUID repositoryId,
            String name,
            BranchType branchType,
            String sourceBranchName,
            boolean isProtected,
            String metadata
    ) {}

    /**
     * 브랜치 수정 Command
     *
     * <p>브랜치 정보 수정에 사용됩니다. null 필드는 수정하지 않습니다.</p>
     *
     * @param name        수정할 브랜치명 (null이면 변경 없음) - 현재 미지원
     * @param branchType  수정할 브랜치 타입 (null이면 변경 없음)
     * @param isProtected 수정할 보호 설정
     * @param metadata    수정할 메타데이터 (null이면 변경 없음)
     */
    record UpdateBranchCommand(
            String name,
            BranchType branchType,
            boolean isProtected,
            String metadata
    ) {}
}
