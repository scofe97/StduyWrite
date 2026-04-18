package com.runnershigh.poc.grpc;

import com.runnershigh.poc.grpc.generated.*;
import io.grpc.StatusRuntimeException;
import lombok.extern.slf4j.Slf4j;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

/**
 * Git Provider gRPC 클라이언트
 *
 * grpc-client-spring-boot-starter를 사용한 gRPC 클라이언트 예제
 *
 * 설정 방법:
 * 1. application.yml에서 grpc.client.{name}.address 설정
 * 2. @GrpcClient 어노테이션으로 stub 주입
 */
@Slf4j
@Service
public class GitProviderGrpcClient {

    /**
     * gRPC Stub 주입
     * - "git-provider"는 application.yml의 grpc.client.git-provider와 매핑
     * - BlockingStub: 동기 호출용
     * - FutureStub: 비동기 호출용 (ListenableFuture 반환)
     * - Stub: 스트리밍용
     */
    @GrpcClient("git-provider")
    private GitServiceGrpc.GitServiceBlockingStub gitServiceStub;

    // ========================================
    // Repository Operations
    // ========================================

    /**
     * 저장소 목록 조회
     */
    public List<Repository> listRepositories(String githubToken) {
        try {
            // Provider 설정 생성
            ProviderConfig config = ProviderConfig.newBuilder()
                    .setGithub(GitHubConfig.newBuilder()
                            .setToken(githubToken)
                            .build())
                    .build();

            // gRPC 호출
            ListRepositoriesRequest request = ListRepositoriesRequest.newBuilder()
                    .setProvider(config)
                    .build();

            ListRepositoriesResponse response = gitServiceStub.listRepositories(request);

            log.info("Successfully fetched {} repositories", response.getRepositoriesCount());
            return response.getRepositoriesList();

        } catch (StatusRuntimeException e) {
            log.error("gRPC call failed: {}", e.getStatus(), e);
            return Collections.emptyList();
        }
    }

    /**
     * 저장소 상세 조회
     */
    public Repository getRepository(String githubToken, String namespace, String repoName) {
        try {
            ProviderConfig config = ProviderConfig.newBuilder()
                    .setGithub(GitHubConfig.newBuilder()
                            .setToken(githubToken)
                            .build())
                    .build();

            GetRepositoryRequest request = GetRepositoryRequest.newBuilder()
                    .setProvider(config)
                    .setNamespace(namespace)
                    .setRepository(repoName)
                    .build();

            GetRepositoryResponse response = gitServiceStub.getRepository(request);

            log.info("Successfully fetched repository: {}", response.getRepository().getFullName());
            return response.getRepository();

        } catch (StatusRuntimeException e) {
            log.error("gRPC call failed: {}", e.getStatus(), e);
            return null;
        }
    }

    // ========================================
    // Branch Operations
    // ========================================

    /**
     * 브랜치 목록 조회
     */
    public List<Branch> listBranches(String githubToken, String namespace, String repoName) {
        try {
            ProviderConfig config = ProviderConfig.newBuilder()
                    .setGithub(GitHubConfig.newBuilder()
                            .setToken(githubToken)
                            .build())
                    .build();

            ListBranchesRequest request = ListBranchesRequest.newBuilder()
                    .setProvider(config)
                    .setNamespace(namespace)
                    .setRepository(repoName)
                    .build();

            ListBranchesResponse response = gitServiceStub.listBranches(request);

            log.info("Successfully fetched {} branches", response.getBranchesCount());
            return response.getBranchesList();

        } catch (StatusRuntimeException e) {
            log.error("gRPC call failed: {}", e.getStatus(), e);
            return Collections.emptyList();
        }
    }

    /**
     * 브랜치 상세 조회
     */
    public Branch getBranch(String githubToken, String namespace, String repoName, String branchName) {
        try {
            ProviderConfig config = ProviderConfig.newBuilder()
                    .setGithub(GitHubConfig.newBuilder()
                            .setToken(githubToken)
                            .build())
                    .build();

            GetBranchRequest request = GetBranchRequest.newBuilder()
                    .setProvider(config)
                    .setNamespace(namespace)
                    .setRepository(repoName)
                    .setBranch(branchName)
                    .build();

            GetBranchResponse response = gitServiceStub.getBranch(request);

            log.info("Successfully fetched branch: {}", response.getBranch().getName());
            return response.getBranch();

        } catch (StatusRuntimeException e) {
            log.error("gRPC call failed: {}", e.getStatus(), e);
            return null;
        }
    }

    /**
     * 브랜치 생성
     */
    public Branch createBranch(String githubToken, String namespace, String repoName,
                               String newBranchName, String ref) {
        try {
            ProviderConfig config = ProviderConfig.newBuilder()
                    .setGithub(GitHubConfig.newBuilder()
                            .setToken(githubToken)
                            .build())
                    .build();

            CreateBranchRequest request = CreateBranchRequest.newBuilder()
                    .setProvider(config)
                    .setNamespace(namespace)
                    .setRepository(repoName)
                    .setBranch(newBranchName)
                    .setRef(ref)
                    .build();

            CreateBranchResponse response = gitServiceStub.createBranch(request);

            log.info("Successfully created branch: {}", response.getBranch().getName());
            return response.getBranch();

        } catch (StatusRuntimeException e) {
            log.error("gRPC call failed: {}", e.getStatus(), e);
            return null;
        }
    }
}
