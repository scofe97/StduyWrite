package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.branchcomparison.*;

import java.util.List;
import java.util.UUID;

/**
 * 브랜치 비교 도메인의 인바운드 포트 (Use Case)
 *
 * <p>브랜치 간 비교, 머지된 브랜치 조회, 브랜치 정리 기능을 정의합니다.</p>
 */
public interface BranchComparisonUseCase {

    /**
     * 두 브랜치를 비교합니다.
     *
     * @param query 비교 요청 정보
     * @return 브랜치 비교 결과
     */
    ComparisonResult compareBranches(CompareBranchesQuery query);

    /**
     * 두 브랜치 간 커밋 차이를 조회합니다.
     *
     * @param query 조회 요청 정보
     * @return 커밋 차이 결과
     */
    CommitDiffResult listCommitsDiff(ListCommitsDiffQuery query);

    /**
     * 머지된 브랜치 목록을 조회합니다.
     *
     * @param query 조회 요청 정보
     * @return 머지된 브랜치 목록
     */
    List<MergedBranchInfo> listMergedBranches(ListMergedBranchesQuery query);

    /**
     * Stale 브랜치 목록을 조회합니다.
     *
     * @param query 조회 요청 정보
     * @return Stale 브랜치 목록
     */
    List<StaleBranchInfo> listStaleBranches(ListStaleBranchesQuery query);

    /**
     * 브랜치를 정리합니다.
     *
     * @param command 정리 명령
     * @return 정리 결과
     */
    CleanupResult cleanupBranches(CleanupBranchesCommand command);

    // ========================================
    // Query & Command DTOs
    // ========================================

    /**
     * 브랜치 비교 Query
     */
    record CompareBranchesQuery(
            UUID connectionId,
            String namespace,
            String repository,
            String base,
            String compare
    ) {}

    /**
     * 커밋 차이 조회 Query
     */
    record ListCommitsDiffQuery(
            UUID connectionId,
            String namespace,
            String repository,
            String base,
            String compare,
            int page,
            int perPage
    ) {
        public ListCommitsDiffQuery {
            if (page <= 0) page = 1;
            if (perPage <= 0) perPage = 30;
        }
    }

    /**
     * 머지된 브랜치 조회 Query
     */
    record ListMergedBranchesQuery(
            UUID connectionId,
            String namespace,
            String repository,
            String base
    ) {
        public ListMergedBranchesQuery {
            if (base == null || base.isEmpty()) base = "main";
        }
    }

    /**
     * Stale 브랜치 조회 Query
     */
    record ListStaleBranchesQuery(
            UUID connectionId,
            String namespace,
            String repository,
            int staleDays
    ) {
        public ListStaleBranchesQuery {
            if (staleDays <= 0) staleDays = 30;
        }
    }

    /**
     * 브랜치 정리 Command
     */
    record CleanupBranchesCommand(
            UUID connectionId,
            String namespace,
            String repository,
            boolean dryRun,
            List<String> excludePatterns,
            int staleDays,
            boolean includeMerged,
            boolean includeStale
    ) {
        public CleanupBranchesCommand {
            if (staleDays <= 0) staleDays = 30;
            if (excludePatterns == null) excludePatterns = List.of();
        }
    }

    // ========================================
    // Result DTOs
    // ========================================

    /**
     * 브랜치 비교 결과
     */
    record ComparisonResult(
            BranchComparison comparison,
            DiffStat diffStat
    ) {}

    /**
     * 커밋 차이 결과
     */
    record CommitDiffResult(
            List<CommitInfo> commits,
            int totalCount
    ) {}
}
