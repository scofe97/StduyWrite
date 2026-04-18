package com.runnershigh.tps.domain.repository;

import com.runnershigh.tps.domain.common.BaseEntity;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
public class Repository extends BaseEntity {

    private UUID projectId;
    private UUID connectionId;
    private String name;
    private String gitProtocol;
    private String gitHost;
    private String gitOwner;
    private String gitRepo;
    private String defaultBranch;
    private BranchStrategyType strategyType;
    private RepositoryStatus status;
    private LocalDateTime lastSyncAt;
    private String metadata;

    @Builder
    public Repository(UUID projectId, UUID connectionId, String name, String gitProtocol,
                      String gitHost, String gitOwner, String gitRepo, String defaultBranch,
                      BranchStrategyType strategyType, RepositoryStatus status, String metadata) {
        super();
        this.projectId = projectId;
        this.connectionId = connectionId;
        this.name = name;
        this.gitProtocol = gitProtocol != null ? gitProtocol : "https";
        this.gitHost = gitHost;
        this.gitOwner = gitOwner;
        this.gitRepo = gitRepo;
        this.defaultBranch = defaultBranch != null ? defaultBranch : "main";
        this.strategyType = strategyType != null ? strategyType : BranchStrategyType.GIT_FLOW;
        this.status = status != null ? status : RepositoryStatus.ACTIVE;
        this.metadata = metadata;
    }

    public Repository(UUID id, UUID projectId, UUID connectionId, String name, String gitProtocol,
                      String gitHost, String gitOwner, String gitRepo, String defaultBranch,
                      BranchStrategyType strategyType, RepositoryStatus status,
                      LocalDateTime lastSyncAt, String metadata) {
        super(id);
        this.projectId = projectId;
        this.connectionId = connectionId;
        this.name = name;
        this.gitProtocol = gitProtocol;
        this.gitHost = gitHost;
        this.gitOwner = gitOwner;
        this.gitRepo = gitRepo;
        this.defaultBranch = defaultBranch;
        this.strategyType = strategyType;
        this.status = status;
        this.lastSyncAt = lastSyncAt;
        this.metadata = metadata;
    }

    public String getFullUrl() {
        return String.format("%s://%s/%s/%s", gitProtocol, gitHost, gitOwner, gitRepo);
    }

    public String getCloneUrl() {
        return getFullUrl() + ".git";
    }

    public void markAsSyncing() {
        this.status = RepositoryStatus.SYNCING;
        updateTimestamp();
    }

    public void markAsSynced() {
        this.status = RepositoryStatus.ACTIVE;
        this.lastSyncAt = LocalDateTime.now();
        updateTimestamp();
    }

    public void markAsError() {
        this.status = RepositoryStatus.ERROR;
        updateTimestamp();
    }

    public void deactivate() {
        this.status = RepositoryStatus.INACTIVE;
        updateTimestamp();
    }

    public boolean isActive() {
        return this.status == RepositoryStatus.ACTIVE;
    }
}
