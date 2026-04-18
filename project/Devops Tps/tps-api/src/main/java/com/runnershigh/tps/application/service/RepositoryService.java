package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.RepositoryUseCase;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.application.port.out.RepositoryRepository;
import com.runnershigh.tps.domain.repository.BranchStrategyType;
import lombok.extern.slf4j.Slf4j;
import com.runnershigh.tps.domain.repository.Repository;
import com.runnershigh.tps.domain.repository.RepositoryStatus;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class RepositoryService implements RepositoryUseCase {

    private final RepositoryRepository repositoryRepository;
    private final GitProviderPort gitProviderPort;

    // Pattern to parse Git URLs: https://github.com/owner/repo.git or git@github.com:owner/repo.git
    private static final Pattern HTTPS_URL_PATTERN = Pattern.compile(
            "^(https?)://([^/]+)/([^/]+)/([^/]+?)(?:\\.git)?$"
    );
    private static final Pattern SSH_URL_PATTERN = Pattern.compile(
            "^git@([^:]+):([^/]+)/([^/]+?)(?:\\.git)?$"
    );

    @Override
    public Repository createRepository(CreateRepositoryCommand command) {
        GitUrlInfo urlInfo = parseGitUrl(command.gitUrl());

        Repository repository = Repository.builder()
                .projectId(command.projectId())
                .connectionId(command.connectionId())
                .name(command.name())
                .gitProtocol(urlInfo.protocol())
                .gitHost(urlInfo.host())
                .gitOwner(urlInfo.owner())
                .gitRepo(urlInfo.repo())
                .defaultBranch(command.defaultBranch() != null ? command.defaultBranch() : "main")
                .strategyType(command.strategyType() != null ? command.strategyType() : BranchStrategyType.GIT_FLOW)
                .status(RepositoryStatus.ACTIVE)
                .metadata(command.metadata())
                .build();

        Repository savedRepository = repositoryRepository.save(repository);

        // Git Flow 전략일 때 develop 브랜치 자동 생성
        if (savedRepository.getStrategyType() == BranchStrategyType.GIT_FLOW) {
            ensureDevelopBranch(savedRepository, command.connectionId());
        }

        return savedRepository;
    }

    /**
     * Git Flow 전략에서 develop 브랜치가 없으면 main에서 생성합니다.
     */
    private void ensureDevelopBranch(Repository repository, UUID connectionId) {
        String developBranch = "develop";
        String namespace = repository.getGitOwner();
        String repo = repository.getGitRepo();

        try {
            // develop 브랜치 존재 확인
            gitProviderPort.getBranch(connectionId, namespace, repo, developBranch);
            log.info("develop branch already exists for repository: {}/{}", namespace, repo);
        } catch (Exception e) {
            // 브랜치가 없으면 main에서 생성
            try {
                gitProviderPort.createBranch(
                        connectionId,
                        namespace,
                        repo,
                        developBranch,
                        repository.getDefaultBranch()  // main 브랜치에서 분기
                );
                log.info("Created develop branch for repository: {}/{}", namespace, repo);
            } catch (Exception createException) {
                log.warn("Failed to create develop branch for repository: {}/{}. Error: {}",
                        namespace, repo, createException.getMessage());
                // 브랜치 생성 실패는 저장소 등록을 막지 않음 (경고만 로깅)
            }
        }
    }

    @Override
    public Repository updateRepository(UUID id, UpdateRepositoryCommand command) {
        Repository repository = getRepository(id);

        if (command.name() != null) {
            repository.setName(command.name());
        }
        if (command.defaultBranch() != null) {
            repository.setDefaultBranch(command.defaultBranch());
        }
        if (command.strategyType() != null) {
            repository.setStrategyType(command.strategyType());
        }
        if (command.metadata() != null) {
            repository.setMetadata(command.metadata());
        }

        return repositoryRepository.update(repository);
    }

    @Override
    @Transactional(readOnly = true)
    public Repository getRepository(UUID id) {
        return repositoryRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Repository not found: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Repository> getAllRepositories() {
        return repositoryRepository.findAll();
    }

    @Override
    @Transactional(readOnly = true)
    public List<Repository> getRepositoriesByProjectId(UUID projectId) {
        return repositoryRepository.findByProjectId(projectId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Repository> getRepositoriesByConnectionId(UUID connectionId) {
        return repositoryRepository.findByConnectionId(connectionId);
    }

    @Override
    public void deleteRepository(UUID id) {
        if (!repositoryRepository.existsById(id)) {
            throw new IllegalArgumentException("Repository not found: " + id);
        }
        repositoryRepository.deleteById(id);
    }

    @Override
    public Repository syncRepository(UUID id) {
        Repository repository = getRepository(id);
        repository.markAsSyncing();
        repositoryRepository.update(repository);

        // TODO: Implement actual sync with Git provider
        // For now, simulate successful sync
        repository.markAsSynced();
        return repositoryRepository.update(repository);
    }

    private GitUrlInfo parseGitUrl(String gitUrl) {
        Matcher httpsMatcher = HTTPS_URL_PATTERN.matcher(gitUrl);
        if (httpsMatcher.matches()) {
            return new GitUrlInfo(
                    httpsMatcher.group(1),
                    httpsMatcher.group(2),
                    httpsMatcher.group(3),
                    httpsMatcher.group(4)
            );
        }

        Matcher sshMatcher = SSH_URL_PATTERN.matcher(gitUrl);
        if (sshMatcher.matches()) {
            return new GitUrlInfo(
                    "ssh",
                    sshMatcher.group(1),
                    sshMatcher.group(2),
                    sshMatcher.group(3)
            );
        }

        throw new IllegalArgumentException("Invalid Git URL format: " + gitUrl);
    }

    private record GitUrlInfo(String protocol, String host, String owner, String repo) {}
}
