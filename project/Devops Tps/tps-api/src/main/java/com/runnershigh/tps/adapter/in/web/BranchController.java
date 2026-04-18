package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.branch.BranchRequest;
import com.runnershigh.tps.adapter.in.web.dto.branch.BranchResponse;
import com.runnershigh.tps.application.port.in.BranchUseCase;
import com.runnershigh.tps.domain.branch.Branch;
import com.runnershigh.tps.domain.branch.BranchStatus;
import com.runnershigh.tps.domain.branch.BranchType;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/v1/branches")
@RequiredArgsConstructor
@Tag(name = "Branch API", description = "Git 브랜치 관리 API")
public class BranchController {

    private final BranchUseCase branchUseCase;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "브랜치 생성", description = "새로운 브랜치를 생성합니다.")
    public BranchResponse createBranch(
            @Valid @RequestBody BranchRequest.Create request) {

        BranchUseCase.CreateBranchCommand command = new BranchUseCase.CreateBranchCommand(
                request.getRepositoryId(),
                request.getName(),
                request.getBranchType(),
                request.getSourceBranchName(),
                request.isProtected(),
                request.getMetadata()
        );

        Branch branch = branchUseCase.createBranch(command);
        return BranchResponse.from(branch);
    }

    @PutMapping("/{id}")
    @Operation(summary = "브랜치 수정", description = "브랜치 정보를 수정합니다.")
    public BranchResponse updateBranch(
            @PathVariable UUID id,
            @Valid @RequestBody BranchRequest.Update request) {

        BranchUseCase.UpdateBranchCommand command = new BranchUseCase.UpdateBranchCommand(
                request.getName(),
                request.getBranchType(),
                request.isProtected(),
                request.getMetadata()
        );

        Branch branch = branchUseCase.updateBranch(id, command);
        return BranchResponse.from(branch);
    }

    @GetMapping("/{id}")
    @Operation(summary = "브랜치 조회", description = "브랜치 상세 정보를 조회합니다.")
    public BranchResponse getBranch(@PathVariable UUID id) {
        Branch branch = branchUseCase.getBranch(id);
        return BranchResponse.from(branch);
    }

    @GetMapping("/repository/{repositoryId}")
    @Operation(summary = "저장소별 브랜치 목록", description = "저장소의 모든 브랜치를 조회합니다.")
    public List<BranchResponse> getBranchesByRepositoryId(@PathVariable UUID repositoryId) {
        return branchUseCase.getBranchesByRepositoryId(repositoryId)
                .stream()
                .map(BranchResponse::from)
                .toList();
    }

    @GetMapping("/repository/{repositoryId}/status/{status}")
    @Operation(summary = "상태별 브랜치 목록", description = "특정 상태의 브랜치를 조회합니다.")
    public List<BranchResponse> getBranchesByStatus(
            @PathVariable UUID repositoryId,
            @PathVariable BranchStatus status) {
        return branchUseCase.getBranchesByRepositoryIdAndStatus(repositoryId, status)
                .stream()
                .map(BranchResponse::from)
                .toList();
    }

    @GetMapping("/repository/{repositoryId}/type/{type}")
    @Operation(summary = "타입별 브랜치 목록", description = "특정 타입의 브랜치를 조회합니다.")
    public List<BranchResponse> getBranchesByType(
            @PathVariable UUID repositoryId,
            @PathVariable BranchType type) {
        return branchUseCase.getBranchesByRepositoryIdAndType(repositoryId, type)
                .stream()
                .map(BranchResponse::from)
                .toList();
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "브랜치 삭제", description = "브랜치를 삭제합니다.")
    public void deleteBranch(@PathVariable UUID id) {
        branchUseCase.deleteBranch(id);
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "브랜치 상태 변경", description = "브랜치의 상태를 변경합니다.")
    public BranchResponse updateBranchStatus(
            @PathVariable UUID id,
            @Valid @RequestBody BranchRequest.UpdateStatus request) {
        Branch branch = branchUseCase.updateBranchStatus(id, request.getStatus());
        return BranchResponse.from(branch);
    }

    @PatchMapping("/{id}/commit")
    @Operation(summary = "브랜치 커밋 업데이트", description = "브랜치의 최신 커밋 SHA를 업데이트합니다.")
    public BranchResponse updateCommit(
            @PathVariable UUID id,
            @Valid @RequestBody BranchRequest.UpdateCommit request) {
        Branch branch = branchUseCase.updateCommit(id, request.getCommitSha());
        return BranchResponse.from(branch);
    }
}
