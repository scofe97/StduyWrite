package com.runnershigh.tps.adapter.in.web.dto.branch;

import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;

import java.time.LocalDateTime;
import java.util.UUID;

public record BranchResponse(
    UUID id,
    UUID repositoryId,
    String name,
    BranchType branchType,
    BranchStatus status,
    String sourceBranchName,
    String latestCommitSha,
    boolean isProtected,
    String metadata,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {
    public static BranchResponse from(Branch branch) {
        return new BranchResponse(
            branch.getId(),
            branch.getRepositoryId(),
            branch.getName(),
            branch.getBranchType(),
            branch.getStatus(),
            branch.getSourceBranchName(),
            branch.getLatestCommitSha(),
            branch.isProtected(),
            branch.getMetadata(),
            branch.getCreatedAt(),
            branch.getUpdatedAt()
        );
    }
}
