package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.branchcomparison.BranchComparisonRequest;
import com.runnershigh.tps.adapter.in.web.dto.branchcomparison.BranchComparisonResponse;
import com.runnershigh.tps.application.port.in.BranchComparisonUseCase;
import com.runnershigh.tps.domain.branchcomparison.CleanupResult;
import com.runnershigh.tps.domain.branchcomparison.MergedBranchInfo;
import com.runnershigh.tps.domain.branchcomparison.StaleBranchInfo;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * 브랜치 비교 API Controller
 *
 * <p>브랜치 비교, 머지된 브랜치 조회, 브랜치 정리 API를 제공합니다.</p>
 */
@RestController
@RequestMapping("/v1/branches")
@RequiredArgsConstructor
@Tag(name = "Branch Comparison API", description = "브랜치 비교 및 관리 API")
public class BranchComparisonController {

    private final BranchComparisonUseCase branchComparisonUseCase;

    // ========================================
    // 브랜치 비교
    // ========================================

    @GetMapping("/{connectionId}/compare")
    @Operation(summary = "브랜치 비교", description = "두 브랜치를 비교합니다.")
    public BranchComparisonResponse.Comparison compareBranches(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자") @RequestParam String namespace,
            @Parameter(description = "저장소 이름") @RequestParam String repository,
            @Parameter(description = "기준 브랜치") @RequestParam String base,
            @Parameter(description = "비교 브랜치") @RequestParam String compare) {

        BranchComparisonUseCase.CompareBranchesQuery query =
                new BranchComparisonUseCase.CompareBranchesQuery(
                        connectionId, namespace, repository, base, compare);

        BranchComparisonUseCase.ComparisonResult result = branchComparisonUseCase.compareBranches(query);
        return BranchComparisonResponse.Comparison.from(result);
    }

    @PostMapping("/compare")
    @Operation(summary = "브랜치 비교 (POST)", description = "두 브랜치를 비교합니다.")
    public BranchComparisonResponse.Comparison compareBranchesPost(
            @Valid @RequestBody BranchComparisonRequest.CompareBranches request) {

        BranchComparisonUseCase.CompareBranchesQuery query =
                new BranchComparisonUseCase.CompareBranchesQuery(
                        request.getConnectionId(),
                        request.getNamespace(),
                        request.getRepository(),
                        request.getBase(),
                        request.getCompare());

        BranchComparisonUseCase.ComparisonResult result = branchComparisonUseCase.compareBranches(query);
        return BranchComparisonResponse.Comparison.from(result);
    }

    // ========================================
    // 커밋 차이
    // ========================================

    @GetMapping("/{connectionId}/compare/commits")
    @Operation(summary = "커밋 차이 조회", description = "두 브랜치 간 커밋 차이를 조회합니다.")
    public BranchComparisonResponse.CommitsDiff listCommitsDiff(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자") @RequestParam String namespace,
            @Parameter(description = "저장소 이름") @RequestParam String repository,
            @Parameter(description = "기준 브랜치") @RequestParam String base,
            @Parameter(description = "비교 브랜치") @RequestParam String compare,
            @Parameter(description = "페이지 번호") @RequestParam(defaultValue = "1") int page,
            @Parameter(description = "페이지 크기") @RequestParam(defaultValue = "30") int perPage) {

        BranchComparisonUseCase.ListCommitsDiffQuery query =
                new BranchComparisonUseCase.ListCommitsDiffQuery(
                        connectionId, namespace, repository, base, compare, page, perPage);

        BranchComparisonUseCase.CommitDiffResult result = branchComparisonUseCase.listCommitsDiff(query);
        return BranchComparisonResponse.CommitsDiff.from(result);
    }

    @PostMapping("/compare/commits")
    @Operation(summary = "커밋 차이 조회 (POST)", description = "두 브랜치 간 커밋 차이를 조회합니다.")
    public BranchComparisonResponse.CommitsDiff listCommitsDiffPost(
            @Valid @RequestBody BranchComparisonRequest.ListCommitsDiff request) {

        BranchComparisonUseCase.ListCommitsDiffQuery query =
                new BranchComparisonUseCase.ListCommitsDiffQuery(
                        request.getConnectionId(),
                        request.getNamespace(),
                        request.getRepository(),
                        request.getBase(),
                        request.getCompare(),
                        request.getPage(),
                        request.getPerPage());

        BranchComparisonUseCase.CommitDiffResult result = branchComparisonUseCase.listCommitsDiff(query);
        return BranchComparisonResponse.CommitsDiff.from(result);
    }

    // ========================================
    // 머지된 브랜치
    // ========================================

    @GetMapping("/{connectionId}/merged")
    @Operation(summary = "머지된 브랜치 목록", description = "기준 브랜치에 머지된 브랜치 목록을 조회합니다.")
    public BranchComparisonResponse.MergedBranches listMergedBranches(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자") @RequestParam String namespace,
            @Parameter(description = "저장소 이름") @RequestParam String repository,
            @Parameter(description = "기준 브랜치") @RequestParam(defaultValue = "main") String base) {

        BranchComparisonUseCase.ListMergedBranchesQuery query =
                new BranchComparisonUseCase.ListMergedBranchesQuery(
                        connectionId, namespace, repository, base);

        List<MergedBranchInfo> branches = branchComparisonUseCase.listMergedBranches(query);
        return BranchComparisonResponse.MergedBranches.from(branches);
    }

    @PostMapping("/merged")
    @Operation(summary = "머지된 브랜치 목록 (POST)", description = "기준 브랜치에 머지된 브랜치 목록을 조회합니다.")
    public BranchComparisonResponse.MergedBranches listMergedBranchesPost(
            @Valid @RequestBody BranchComparisonRequest.ListMergedBranches request) {

        BranchComparisonUseCase.ListMergedBranchesQuery query =
                new BranchComparisonUseCase.ListMergedBranchesQuery(
                        request.getConnectionId(),
                        request.getNamespace(),
                        request.getRepository(),
                        request.getBase());

        List<MergedBranchInfo> branches = branchComparisonUseCase.listMergedBranches(query);
        return BranchComparisonResponse.MergedBranches.from(branches);
    }

    // ========================================
    // Stale 브랜치
    // ========================================

    @GetMapping("/{connectionId}/stale")
    @Operation(summary = "Stale 브랜치 목록", description = "오래된 브랜치 목록을 조회합니다.")
    public BranchComparisonResponse.StaleBranches listStaleBranches(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자") @RequestParam String namespace,
            @Parameter(description = "저장소 이름") @RequestParam String repository,
            @Parameter(description = "비활성 기준 일수") @RequestParam(defaultValue = "30") int staleDays) {

        BranchComparisonUseCase.ListStaleBranchesQuery query =
                new BranchComparisonUseCase.ListStaleBranchesQuery(
                        connectionId, namespace, repository, staleDays);

        List<StaleBranchInfo> branches = branchComparisonUseCase.listStaleBranches(query);
        return BranchComparisonResponse.StaleBranches.from(branches);
    }

    @PostMapping("/stale")
    @Operation(summary = "Stale 브랜치 목록 (POST)", description = "오래된 브랜치 목록을 조회합니다.")
    public BranchComparisonResponse.StaleBranches listStaleBranchesPost(
            @Valid @RequestBody BranchComparisonRequest.ListStaleBranches request) {

        BranchComparisonUseCase.ListStaleBranchesQuery query =
                new BranchComparisonUseCase.ListStaleBranchesQuery(
                        request.getConnectionId(),
                        request.getNamespace(),
                        request.getRepository(),
                        request.getStaleDays());

        List<StaleBranchInfo> branches = branchComparisonUseCase.listStaleBranches(query);
        return BranchComparisonResponse.StaleBranches.from(branches);
    }

    // ========================================
    // 브랜치 정리
    // ========================================

    @PostMapping("/cleanup")
    @Operation(summary = "브랜치 정리", description = "머지된 브랜치와 오래된 브랜치를 정리합니다.")
    public BranchComparisonResponse.Cleanup cleanupBranches(
            @Valid @RequestBody BranchComparisonRequest.CleanupBranches request) {

        BranchComparisonUseCase.CleanupBranchesCommand command =
                new BranchComparisonUseCase.CleanupBranchesCommand(
                        request.getConnectionId(),
                        request.getNamespace(),
                        request.getRepository(),
                        request.isDryRun(),
                        request.getExcludePatterns(),
                        request.getStaleDays(),
                        request.isIncludeMerged(),
                        request.isIncludeStale());

        CleanupResult result = branchComparisonUseCase.cleanupBranches(command);
        return BranchComparisonResponse.Cleanup.from(result);
    }
}
