package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.BranchUseCase;
import com.runnershigh.tps.application.port.out.BranchRepository;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.application.port.out.RepositoryRepository;
import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;
import com.runnershigh.tps.domain.repository.Repository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class BranchService implements BranchUseCase {

    private final BranchRepository branchRepository;
    private final RepositoryRepository repositoryRepository;
    private final GitProviderPort gitProviderPort;

    @Override
    public Branch createBranch(CreateBranchCommand command) {
        // Check for duplicate branch name in repository
        branchRepository.findByRepositoryIdAndName(command.repositoryId(), command.name())
                .ifPresent(existing -> {
                    throw new IllegalArgumentException("Branch already exists: " + command.name());
                });

        // Get repository info for Git provider call
        Repository repository = repositoryRepository.findById(command.repositoryId())
                .orElseThrow(() -> new IllegalArgumentException("Repository not found: " + command.repositoryId()));

        // Determine the source ref (branch or commit SHA)
        String sourceRef = command.sourceBranchName();
        if (sourceRef == null || sourceRef.isEmpty()) {
            sourceRef = repository.getDefaultBranch();
        }

        // Create branch on remote Git provider (GitHub, GitLab, etc.)
        GitProviderPort.RemoteBranch remoteBranch = null;
        try {
            log.info("Creating branch '{}' on remote Git provider from ref '{}'", command.name(), sourceRef);
            remoteBranch = gitProviderPort.createBranch(
                    repository.getConnectionId(),
                    repository.getGitOwner(),
                    repository.getGitRepo(),
                    command.name(),
                    sourceRef
            );
            log.info("Successfully created branch '{}' on remote. SHA: {}", command.name(), remoteBranch.sha());
        } catch (Exception e) {
            log.error("Failed to create branch '{}' on remote Git provider: {}", command.name(), e.getMessage());
            throw new RuntimeException("Failed to create branch on remote: " + e.getMessage(), e);
        }

        // Save to local database
        Branch branch = Branch.builder()
                .repositoryId(command.repositoryId())
                .name(command.name())
                .branchType(command.branchType() != null ? command.branchType() : BranchType.fromBranchName(command.name()))
                .status(BranchStatus.ACTIVE)
                .sourceBranchName(command.sourceBranchName())
                .isProtected(command.isProtected())
                .latestCommitSha(remoteBranch != null ? remoteBranch.sha() : null)
                .metadata(command.metadata())
                .build();

        return branchRepository.save(branch);
    }

    @Override
    public Branch updateBranch(UUID id, UpdateBranchCommand command) {
        Branch branch = getBranch(id);

        if (command.name() != null) {
            branch.setName(command.name());
        }
        if (command.branchType() != null) {
            branch.setBranchType(command.branchType());
        }
        branch.setProtected(command.isProtected());
        if (command.metadata() != null) {
            branch.setMetadata(command.metadata());
        }

        return branchRepository.update(branch);
    }

    @Override
    @Transactional(readOnly = true)
    public Branch getBranch(UUID id) {
        return branchRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Branch not found: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Branch> getBranchesByRepositoryId(UUID repositoryId) {
        return branchRepository.findByRepositoryId(repositoryId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Branch> getBranchesByRepositoryIdAndStatus(UUID repositoryId, BranchStatus status) {
        return branchRepository.findByRepositoryIdAndStatus(repositoryId, status);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Branch> getBranchesByRepositoryIdAndType(UUID repositoryId, BranchType type) {
        return branchRepository.findByRepositoryIdAndType(repositoryId, type);
    }

    @Override
    public void deleteBranch(UUID id) {
        Branch branch = getBranch(id);

        if (branch.isProtected()) {
            throw new IllegalStateException("Cannot delete protected branch: " + branch.getName());
        }

        branchRepository.deleteById(id);
    }

    @Override
    public Branch updateBranchStatus(UUID id, BranchStatus status) {
        Branch branch = getBranch(id);

        switch (status) {
            case MERGED -> branch.markAsMerged();
            case DELETED -> branch.markAsDeleted();
            case STALE -> branch.markAsStale();
            case ACTIVE -> {
                branch.setStatus(BranchStatus.ACTIVE);
                branch.updateTimestamp();
            }
        }

        return branchRepository.update(branch);
    }

    @Override
    public Branch updateCommit(UUID id, String commitSha) {
        Branch branch = getBranch(id);
        branch.updateCommit(commitSha);
        return branchRepository.update(branch);
    }
}
