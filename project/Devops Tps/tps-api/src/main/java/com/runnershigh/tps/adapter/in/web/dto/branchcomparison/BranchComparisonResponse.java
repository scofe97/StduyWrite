package com.runnershigh.tps.adapter.in.web.dto.branchcomparison;

import com.runnershigh.tps.application.port.in.BranchComparisonUseCase;
import com.runnershigh.tps.domain.branchcomparison.*;

import java.util.List;

/**
 * 브랜치 비교 API 응답 DTO
 */
public class BranchComparisonResponse {

    /**
     * 브랜치 비교 결과 응답
     */
    public record Comparison(
        String baseBranch,
        String compareBranch,
        int aheadBy,
        int behindBy,
        String mergeable,
        String mergeStatus,
        String suggestedAction,
        String baseSha,
        String compareSha,
        String mergeBaseSha,
        DiffStatResponse diffStat
    ) {
        public static Comparison from(BranchComparisonUseCase.ComparisonResult result) {
            BranchComparison comparison = result.comparison();
            return new Comparison(
                comparison.getBaseBranch(),
                comparison.getCompareBranch(),
                comparison.getAheadBy(),
                comparison.getBehindBy(),
                comparison.getMergeable() != null ? comparison.getMergeable().name() : null,
                comparison.getMergeStatus(),
                comparison.getSuggestedAction() != null ? comparison.getSuggestedAction().name() : null,
                comparison.getBaseSha(),
                comparison.getCompareSha(),
                comparison.getMergeBaseSha(),
                result.diffStat() != null ? DiffStatResponse.from(result.diffStat()) : null
            );
        }
    }

    /**
     * 변경 통계 응답
     */
    public record DiffStatResponse(
        int filesChanged,
        int additions,
        int deletions
    ) {
        public static DiffStatResponse from(DiffStat diffStat) {
            return new DiffStatResponse(
                diffStat.getFilesChanged(),
                diffStat.getAdditions(),
                diffStat.getDeletions()
            );
        }
    }

    /**
     * 커밋 차이 결과 응답
     */
    public record CommitsDiff(
        List<CommitInfoResponse> commits,
        int totalCount
    ) {
        public static CommitsDiff from(BranchComparisonUseCase.CommitDiffResult result) {
            return new CommitsDiff(
                result.commits().stream().map(CommitInfoResponse::from).toList(),
                result.totalCount()
            );
        }
    }

    /**
     * 커밋 정보 응답
     */
    public record CommitInfoResponse(
        String sha,
        String message,
        String authorName,
        String authorEmail,
        String date
    ) {
        public static CommitInfoResponse from(CommitInfo commitInfo) {
            return new CommitInfoResponse(
                commitInfo.getSha(),
                commitInfo.getMessage(),
                commitInfo.getAuthorName(),
                commitInfo.getAuthorEmail(),
                commitInfo.getDate()
            );
        }
    }

    /**
     * 머지된 브랜치 목록 응답
     */
    public record MergedBranches(List<MergedBranchInfoResponse> branches) {
        public static MergedBranches from(List<MergedBranchInfo> branches) {
            return new MergedBranches(
                branches.stream().map(MergedBranchInfoResponse::from).toList()
            );
        }
    }

    /**
     * 머지된 브랜치 정보 응답
     */
    public record MergedBranchInfoResponse(
        String name,
        String mergedAt,
        String mergedBy,
        String lastCommitSha,
        String mergedInto
    ) {
        public static MergedBranchInfoResponse from(MergedBranchInfo info) {
            return new MergedBranchInfoResponse(
                info.getName(),
                info.getMergedAt(),
                info.getMergedBy(),
                info.getLastCommitSha(),
                info.getMergedInto()
            );
        }
    }

    /**
     * Stale 브랜치 목록 응답
     */
    public record StaleBranches(List<StaleBranchInfoResponse> branches) {
        public static StaleBranches from(List<StaleBranchInfo> branches) {
            return new StaleBranches(
                branches.stream().map(StaleBranchInfoResponse::from).toList()
            );
        }
    }

    /**
     * Stale 브랜치 정보 응답
     */
    public record StaleBranchInfoResponse(
        String name,
        String lastCommitSha,
        String lastCommitDate,
        int daysInactive
    ) {
        public static StaleBranchInfoResponse from(StaleBranchInfo info) {
            return new StaleBranchInfoResponse(
                info.getName(),
                info.getLastCommitSha(),
                info.getLastCommitDate(),
                info.getDaysInactive()
            );
        }
    }

    /**
     * 브랜치 정리 결과 응답
     */
    public record Cleanup(
        List<String> deleted,
        List<String> skipped,
        List<String> failed,
        boolean dryRun
    ) {
        public static Cleanup from(CleanupResult result) {
            return new Cleanup(
                result.deleted(),
                result.skipped(),
                result.failed(),
                result.dryRun()
            );
        }
    }
}
