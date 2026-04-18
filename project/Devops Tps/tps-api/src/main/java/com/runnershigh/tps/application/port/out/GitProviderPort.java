package com.runnershigh.tps.application.port.out;

import com.runnershigh.tps.domain.branchcomparison.*;
import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.TreeEntry;
import com.runnershigh.tps.domain.mergerequest.MergeRequest;

import java.util.List;
import java.util.UUID;

/**
 * Git Provider 아웃바운드 포트 (gRPC 클라이언트)
 *
 * <p>git-provider(Go) gRPC 서버와 통신하는 인터페이스입니다.
 * Service가 이 인터페이스에 의존하며, gRPC Adapter가 구현합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * Application Service (Application)
 *         │
 *         ▼
 * GitProviderPort (Port-Out) ◀── 현재 위치
 *         │
 *         ▼
 * GitProviderGrpcAdapter (Adapter-Out)
 *         │
 *         ▼
 *    gRPC Server (git-provider Go)
 * </pre>
 *
 * <h2>설계 의도</h2>
 * <ul>
 *   <li><strong>기술 독립성</strong>: Service가 gRPC에 직접 의존하지 않음</li>
 *   <li><strong>테스트 용이성</strong>: Mock 객체로 쉽게 대체 가능</li>
 *   <li><strong>통신 방식 교체 용이</strong>: gRPC → REST 전환 시 Service 코드 변경 불필요</li>
 * </ul>
 */
public interface GitProviderPort {

    // ========================================
    // Repository Operations
    // ========================================

    /**
     * 원격 저장소 목록을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @return 원격 저장소 목록
     */
    List<RemoteRepository> listRepositories(UUID connectionId);

    /**
     * 특정 원격 저장소를 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자 (owner/org)
     * @param repo         저장소 이름
     * @return 원격 저장소 정보
     */
    RemoteRepository getRepository(UUID connectionId, String namespace, String repo);

    // ========================================
    // Branch Operations
    // ========================================

    /**
     * 원격 브랜치 목록을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @return 브랜치 목록
     */
    List<RemoteBranch> listBranches(UUID connectionId, String namespace, String repo);

    /**
     * 특정 원격 브랜치를 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param branch       브랜치 이름
     * @return 브랜치 정보
     */
    RemoteBranch getBranch(UUID connectionId, String namespace, String repo, String branch);

    /**
     * 원격 브랜치를 생성합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param branch       생성할 브랜치 이름
     * @param ref          기준 ref (브랜치명 또는 SHA)
     * @return 생성된 브랜치 정보
     */
    RemoteBranch createBranch(UUID connectionId, String namespace, String repo, String branch, String ref);

    /**
     * 원격 브랜치를 삭제합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param branch       삭제할 브랜치 이름
     */
    void deleteBranch(UUID connectionId, String namespace, String repo, String branch);

    // ========================================
    // Contents Operations (Phase 1)
    // ========================================

    /**
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param path         경로 (빈 문자열은 루트)
     * @param ref          브랜치/태그/커밋 (null이면 기본 브랜치)
     * @return 파일/디렉토리 콘텐츠 정보
     */
    ContentEntry getContents(UUID connectionId, String namespace, String repo, String path, String ref);

    // ========================================
    // Tree Operations (Phase 2)
    // ========================================

    /**
     * 저장소의 전체 파일 트리를 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param ref          브랜치/태그/커밋
     * @param recursive    전체 트리 조회 여부
     * @return 트리 항목 목록
     */
    List<TreeEntry> getTree(UUID connectionId, String namespace, String repo, String ref, boolean recursive);

    // ========================================
    // MergeRequest Operations (Phase 3)
    // ========================================

    /**
     * Merge Request 목록을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param state        상태 필터 (open, closed, merged, all)
     * @return MR 목록
     */
    List<MergeRequest> listMergeRequests(UUID connectionId, String namespace, String repo, String state);

    /**
     * 특정 Merge Request를 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param number       MR 번호
     * @return MR 상세 정보
     */
    MergeRequest getMergeRequest(UUID connectionId, String namespace, String repo, Integer number);

    /**
     * Merge Request를 생성합니다.
     *
     * @param connectionId  연결 ID
     * @param namespace     저장소 소유자
     * @param repo          저장소 이름
     * @param title         제목
     * @param description   설명
     * @param sourceBranch  소스 브랜치
     * @param targetBranch  타겟 브랜치
     * @return 생성된 MR
     */
    MergeRequest createMergeRequest(UUID connectionId, String namespace, String repo,
                                     String title, String description,
                                     String sourceBranch, String targetBranch);

    /**
     * Merge Request를 머지합니다.
     *
     * @param connectionId   연결 ID
     * @param namespace      저장소 소유자
     * @param repo           저장소 이름
     * @param number         MR 번호
     * @param commitMessage  커밋 메시지
     * @param squash         스쿼시 머지 여부
     * @return 머지된 MR
     */
    MergeRequest mergeMergeRequest(UUID connectionId, String namespace, String repo,
                                    Integer number, String commitMessage, boolean squash);

    // ========================================
    // Branch Comparison Operations (Phase 1.2)
    // ========================================

    /**
     * 두 브랜치를 비교합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param base         기준 브랜치
     * @param compare      비교 브랜치
     * @return 브랜치 비교 결과
     */
    BranchComparisonResult compareBranches(UUID connectionId, String namespace, String repo,
                                           String base, String compare);

    /**
     * 두 브랜치 간 커밋 차이를 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param base         기준 브랜치
     * @param compare      비교 브랜치
     * @param page         페이지 번호
     * @param perPage      페이지 당 개수
     * @return 커밋 목록
     */
    CommitDiffResult listCommitsDiff(UUID connectionId, String namespace, String repo,
                                      String base, String compare, int page, int perPage);

    /**
     * 머지된 브랜치 목록을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param base         기준 브랜치
     * @return 머지된 브랜치 목록
     */
    List<MergedBranchInfo> listMergedBranches(UUID connectionId, String namespace, String repo, String base);

    /**
     * Stale 브랜치 목록을 조회합니다.
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repo         저장소 이름
     * @param staleDays    비활성 기준 일수
     * @return Stale 브랜치 목록
     */
    List<StaleBranchInfo> listStaleBranches(UUID connectionId, String namespace, String repo, int staleDays);

    /**
     * 브랜치를 정리합니다.
     *
     * @param connectionId    연결 ID
     * @param namespace       저장소 소유자
     * @param repo            저장소 이름
     * @param dryRun          드라이 런 여부
     * @param excludePatterns 제외 패턴
     * @param staleDays       비활성 기준 일수
     * @param includeMerged   머지된 브랜치 포함
     * @param includeStale    Stale 브랜치 포함
     * @return 정리 결과
     */
    CleanupResult cleanupBranches(UUID connectionId, String namespace, String repo,
                                   boolean dryRun, List<String> excludePatterns,
                                   int staleDays, boolean includeMerged, boolean includeStale);

    // ========================================
    // DTOs for Remote Entities
    // ========================================

    /**
     * 브랜치 비교 결과 DTO
     */
    record BranchComparisonResult(
            BranchComparison comparison,
            DiffStat diffStat
    ) {}

    /**
     * 커밋 차이 결과 DTO
     */
    record CommitDiffResult(
            List<CommitInfo> commits,
            int totalCount
    ) {}

    /**
     * 원격 저장소 정보 DTO
     */
    record RemoteRepository(
            String id,
            String name,
            String fullName,
            String description,
            String url,
            String cloneUrl,
            String sshUrl,
            String defaultBranch,
            boolean isPrivate
    ) {}

    /**
     * 원격 브랜치 정보 DTO
     */
    record RemoteBranch(
            String name,
            String sha,
            boolean isProtected,
            boolean isDefault
    ) {}
}
