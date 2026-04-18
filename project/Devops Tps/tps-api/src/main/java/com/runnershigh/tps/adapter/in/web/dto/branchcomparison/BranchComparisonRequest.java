package com.runnershigh.tps.adapter.in.web.dto.branchcomparison;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.UUID;

/**
 * 브랜치 비교 API 요청 DTO
 */
public class BranchComparisonRequest {

    /**
     * 브랜치 비교 요청
     */
    @Getter
    @Setter
    public static class CompareBranches {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        @NotBlank(message = "base is required")
        private String base;

        @NotBlank(message = "compare is required")
        private String compare;
    }

    /**
     * 커밋 차이 조회 요청
     */
    @Getter
    @Setter
    public static class ListCommitsDiff {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        @NotBlank(message = "base is required")
        private String base;

        @NotBlank(message = "compare is required")
        private String compare;

        private int page = 1;
        private int perPage = 30;
    }

    /**
     * 머지된 브랜치 조회 요청
     */
    @Getter
    @Setter
    public static class ListMergedBranches {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private String base = "main";
    }

    /**
     * Stale 브랜치 조회 요청
     */
    @Getter
    @Setter
    public static class ListStaleBranches {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private int staleDays = 30;
    }

    /**
     * 브랜치 정리 요청
     */
    @Getter
    @Setter
    public static class CleanupBranches {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private boolean dryRun = true;
        private List<String> excludePatterns;
        private int staleDays = 30;
        private boolean includeMerged = false;
        private boolean includeStale = false;
    }
}
