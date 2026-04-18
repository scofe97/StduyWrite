package com.runnershigh.tps.adapter.in.web.dto.branch;

import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.UUID;

public class BranchRequest {

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Create {
        @NotNull(message = "Repository ID is required")
        private UUID repositoryId;

        @NotBlank(message = "Branch name is required")
        private String name;

        private BranchType branchType;
        private String sourceBranchName;
        private boolean isProtected;
        private String metadata;
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Update {
        private String name;
        private BranchType branchType;
        private boolean isProtected;
        private String metadata;
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UpdateStatus {
        @NotNull(message = "Status is required")
        private BranchStatus status;
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UpdateCommit {
        @NotBlank(message = "Commit SHA is required")
        private String commitSha;
    }
}
