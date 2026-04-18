package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.application.port.out.BranchRepository;
import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
@RequiredArgsConstructor
public class BranchPersistenceAdapter implements BranchRepository {

    private final BranchMapper branchMapper;

    @Override
    public Branch save(Branch branch) {
        branchMapper.insert(branch);
        return branch;
    }

    @Override
    public Branch update(Branch branch) {
        branch.updateTimestamp();
        branchMapper.update(branch);
        return branch;
    }

    @Override
    public Optional<Branch> findById(UUID id) {
        return Optional.ofNullable(branchMapper.findById(id));
    }

    @Override
    public List<Branch> findByRepositoryId(UUID repositoryId) {
        return branchMapper.findByRepositoryId(repositoryId);
    }

    @Override
    public List<Branch> findByRepositoryIdAndStatus(UUID repositoryId, BranchStatus status) {
        return branchMapper.findByRepositoryIdAndStatus(repositoryId, status);
    }

    @Override
    public List<Branch> findByRepositoryIdAndType(UUID repositoryId, BranchType type) {
        return branchMapper.findByRepositoryIdAndType(repositoryId, type);
    }

    @Override
    public Optional<Branch> findByRepositoryIdAndName(UUID repositoryId, String name) {
        return Optional.ofNullable(branchMapper.findByRepositoryIdAndName(repositoryId, name));
    }

    @Override
    public void deleteById(UUID id) {
        branchMapper.deleteById(id);
    }

    @Override
    public void deleteByRepositoryId(UUID repositoryId) {
        branchMapper.deleteByRepositoryId(repositoryId);
    }

    @Override
    public boolean existsById(UUID id) {
        return branchMapper.countById(id) > 0;
    }
}
