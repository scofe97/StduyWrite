package com.runnershigh.tps.adapter.out.persistence;

import com.runnershigh.tps.application.port.out.RepositoryRepository;
import com.runnershigh.tps.domain.repository.Repository;
import com.runnershigh.tps.domain.repository.RepositoryStatus;
import lombok.RequiredArgsConstructor;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@org.springframework.stereotype.Repository
@RequiredArgsConstructor
public class RepositoryPersistenceAdapter implements RepositoryRepository {

    private final RepositoryMapper repositoryMapper;

    @Override
    public Repository save(Repository repository) {
        repositoryMapper.insert(repository);
        return repository;
    }

    @Override
    public Repository update(Repository repository) {
        repository.updateTimestamp();
        repositoryMapper.update(repository);
        return repository;
    }

    @Override
    public Optional<Repository> findById(UUID id) {
        return Optional.ofNullable(repositoryMapper.findById(id));
    }

    @Override
    public List<Repository> findByProjectId(UUID projectId) {
        return repositoryMapper.findByProjectId(projectId);
    }

    @Override
    public List<Repository> findByConnectionId(UUID connectionId) {
        return repositoryMapper.findByConnectionId(connectionId);
    }

    @Override
    public List<Repository> findByStatus(RepositoryStatus status) {
        return repositoryMapper.findByStatus(status);
    }

    @Override
    public Optional<Repository> findByProjectIdAndName(UUID projectId, String name) {
        return Optional.ofNullable(repositoryMapper.findByProjectIdAndName(projectId, name));
    }

    @Override
    public void deleteById(UUID id) {
        repositoryMapper.deleteById(id);
    }

    @Override
    public boolean existsById(UUID id) {
        return repositoryMapper.countById(id) > 0;
    }

    @Override
    public List<Repository> findAll() {
        return repositoryMapper.findAll();
    }
}
