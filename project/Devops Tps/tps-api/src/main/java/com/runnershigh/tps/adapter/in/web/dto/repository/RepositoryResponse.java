package com.runnershigh.tps.adapter.in.web.dto.repository;

import com.runnershigh.tps.domain.repository.BranchStrategyType;
import com.runnershigh.tps.domain.repository.Repository;
import com.runnershigh.tps.domain.repository.RepositoryStatus;

import java.time.LocalDateTime;
import java.util.UUID;

public record RepositoryResponse(
    UUID id,
    UUID projectId,
    UUID connectionId,
    String name,
    String gitUrl,
    String gitHost,
    String gitOwner,
    String gitRepo,
    String defaultBranch,
    BranchStrategyType strategyType,
    RepositoryStatus status,
    LocalDateTime lastSyncAt,
    String metadata,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {
    public static RepositoryResponse from(Repository repository) {
        return new RepositoryResponse(
            repository.getId(),
            repository.getProjectId(),
            repository.getConnectionId(),
            repository.getName(),
            repository.getFullUrl(),
            repository.getGitHost(),
            repository.getGitOwner(),
            repository.getGitRepo(),
            repository.getDefaultBranch(),
            repository.getStrategyType(),
            repository.getStatus(),
            repository.getLastSyncAt(),
            repository.getMetadata(),
            repository.getCreatedAt(),
            repository.getUpdatedAt()
        );
    }
}
