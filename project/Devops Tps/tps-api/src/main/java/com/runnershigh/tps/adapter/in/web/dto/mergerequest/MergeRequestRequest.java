package com.runnershigh.tps.adapter.in.web.dto.mergerequest;

import com.runnershigh.tps.domain.mergerequest.MergeRequestStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;

/**
 * MergeRequest API 요청 DTO
 */
public class MergeRequestRequest {

    /**
     * MR 목록 조회 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class ListMergeRequests {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private MergeRequestStatus status;
    }

    /**
     * MR 상세 조회 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class GetMergeRequest {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        @NotNull(message = "number is required")
        private Integer number;
    }

    /**
     * MR 생성 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class CreateMergeRequest {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        @NotBlank(message = "title is required")
        private String title;

        private String description;

        @NotBlank(message = "sourceBranch is required")
        private String sourceBranch;

        @NotBlank(message = "targetBranch is required")
        private String targetBranch;
    }

    /**
     * MR 머지 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class MergeMergeRequest {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        @NotNull(message = "number is required")
        private Integer number;

        private String commitMessage;
        private boolean squash = false;
    }
}
