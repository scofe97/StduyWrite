package com.runnershigh.tps.domain.branch;

import com.runnershigh.tps.domain.common.BaseEntity;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
public class Branch extends BaseEntity {

    private UUID repositoryId;
    private String name;
    private BranchType branchType;
    private BranchStatus status;
    private String sourceBranchName;
    private String latestCommitSha;
    private String metadata;
    private boolean isProtected;

    @Builder
    public Branch(UUID repositoryId, String name, BranchType branchType,
                  BranchStatus status, String sourceBranchName, String latestCommitSha,
                  String metadata, boolean isProtected) {
        super();
        this.repositoryId = repositoryId;
        this.name = name;
        this.branchType = branchType != null ? branchType : BranchType.fromBranchName(name);
        this.status = status != null ? status : BranchStatus.ACTIVE;
        this.sourceBranchName = sourceBranchName;
        this.latestCommitSha = latestCommitSha;
        this.metadata = metadata;
        this.isProtected = isProtected;
    }

    public Branch(UUID id, UUID repositoryId, String name, BranchType branchType,
                  BranchStatus status, String sourceBranchName, String latestCommitSha,
                  String metadata, boolean isProtected) {
        super(id);
        this.repositoryId = repositoryId;
        this.name = name;
        this.branchType = branchType;
        this.status = status;
        this.sourceBranchName = sourceBranchName;
        this.latestCommitSha = latestCommitSha;
        this.metadata = metadata;
        this.isProtected = isProtected;
    }

    public void markAsMerged() {
        this.status = BranchStatus.MERGED;
        updateTimestamp();
    }

    public void markAsDeleted() {
        this.status = BranchStatus.DELETED;
        updateTimestamp();
    }

    public void markAsStale() {
        this.status = BranchStatus.STALE;
        updateTimestamp();
    }

    public void updateCommit(String commitSha) {
        this.latestCommitSha = commitSha;
        this.status = BranchStatus.ACTIVE;
        updateTimestamp();
    }

    public boolean isActive() {
        return this.status == BranchStatus.ACTIVE;
    }

    public boolean isMainBranch() {
        return this.branchType == BranchType.MAIN;
    }

    public boolean isDevelopBranch() {
        return this.branchType == BranchType.DEVELOP;
    }
}
