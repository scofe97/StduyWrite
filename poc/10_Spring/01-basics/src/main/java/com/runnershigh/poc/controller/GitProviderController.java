package com.runnershigh.poc.controller;

import com.runnershigh.poc.grpc.GitProviderGrpcClient;
import com.runnershigh.poc.grpc.generated.Branch;
import com.runnershigh.poc.grpc.generated.Repository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * Git Provider REST API Controller
 *
 * gRPC 클라이언트를 통해 git-provider 서버와 통신하는 예제
 */
@RestController
@RequestMapping("/api/git")
@RequiredArgsConstructor
public class GitProviderController {

    private final GitProviderGrpcClient gitProviderClient;

    // ========================================
    // Repository Endpoints
    // ========================================

    /**
     * 저장소 목록 조회
     * GET /api/git/repositories?token={githubToken}
     */
    @GetMapping("/repositories")
    public ResponseEntity<List<Map<String, Object>>> listRepositories(
            @RequestParam String token) {

        List<Repository> repositories = gitProviderClient.listRepositories(token);

        List<Map<String, Object>> result = repositories.stream()
                .map(this::repositoryToMap)
                .toList();

        return ResponseEntity.ok(result);
    }

    /**
     * 저장소 상세 조회
     * GET /api/git/repositories/{namespace}/{repo}?token={githubToken}
     */
    @GetMapping("/repositories/{namespace}/{repo}")
    public ResponseEntity<Map<String, Object>> getRepository(
            @PathVariable String namespace,
            @PathVariable String repo,
            @RequestParam String token) {

        Repository repository = gitProviderClient.getRepository(token, namespace, repo);

        if (repository == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(repositoryToMap(repository));
    }

    // ========================================
    // Branch Endpoints
    // ========================================

    /**
     * 브랜치 목록 조회
     * GET /api/git/repositories/{namespace}/{repo}/branches?token={githubToken}
     */
    @GetMapping("/repositories/{namespace}/{repo}/branches")
    public ResponseEntity<List<Map<String, Object>>> listBranches(
            @PathVariable String namespace,
            @PathVariable String repo,
            @RequestParam String token) {

        List<Branch> branches = gitProviderClient.listBranches(token, namespace, repo);

        List<Map<String, Object>> result = branches.stream()
                .map(this::branchToMap)
                .toList();

        return ResponseEntity.ok(result);
    }

    /**
     * 브랜치 상세 조회
     * GET /api/git/repositories/{namespace}/{repo}/branches/{branch}?token={githubToken}
     */
    @GetMapping("/repositories/{namespace}/{repo}/branches/{branch}")
    public ResponseEntity<Map<String, Object>> getBranch(
            @PathVariable String namespace,
            @PathVariable String repo,
            @PathVariable String branch,
            @RequestParam String token) {

        Branch branchInfo = gitProviderClient.getBranch(token, namespace, repo, branch);

        if (branchInfo == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(branchToMap(branchInfo));
    }

    /**
     * 브랜치 생성
     * POST /api/git/repositories/{namespace}/{repo}/branches
     */
    @PostMapping("/repositories/{namespace}/{repo}/branches")
    public ResponseEntity<Map<String, Object>> createBranch(
            @PathVariable String namespace,
            @PathVariable String repo,
            @RequestParam String token,
            @RequestBody CreateBranchRequest request) {

        Branch branch = gitProviderClient.createBranch(
                token, namespace, repo, request.branchName(), request.ref());

        if (branch == null) {
            return ResponseEntity.badRequest().build();
        }

        return ResponseEntity.ok(branchToMap(branch));
    }

    // ========================================
    // Helper Methods
    // ========================================

    private Map<String, Object> repositoryToMap(Repository repo) {
        return Map.of(
                "id", repo.getId(),
                "name", repo.getName(),
                "fullName", repo.getFullName(),
                "description", repo.getDescription(),
                "url", repo.getUrl(),
                "cloneUrl", repo.getCloneUrl(),
                "sshUrl", repo.getSshUrl(),
                "defaultBranch", repo.getDefaultBranch(),
                "private", repo.getPrivate()
        );
    }

    private Map<String, Object> branchToMap(Branch branch) {
        return Map.of(
                "name", branch.getName(),
                "sha", branch.getSha(),
                "protected", branch.getProtected(),
                "isDefault", branch.getIsDefault()
        );
    }

    // ========================================
    // Request DTOs
    // ========================================

    public record CreateBranchRequest(String branchName, String ref) {}
}
