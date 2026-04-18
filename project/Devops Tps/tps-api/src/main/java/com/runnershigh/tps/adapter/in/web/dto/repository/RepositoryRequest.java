package com.runnershigh.tps.adapter.in.web.dto.repository;

import com.runnershigh.tps.domain.repository.BranchStrategyType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.UUID;

public class RepositoryRequest {

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Create {
        @NotNull(message = "Project ID is required")
        private UUID projectId;

        @NotNull(message = "Connection ID is required")
        private UUID connectionId;

        @NotBlank(message = "Repository name is required")
        private String name;

        @NotBlank(message = "Git URL is required")
        private String gitUrl;

        private String defaultBranch;
        private BranchStrategyType strategyType;
        private String metadata;
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Update {
        private String name;
        private String defaultBranch;
        private BranchStrategyType strategyType;
        private String metadata;
    }
}
