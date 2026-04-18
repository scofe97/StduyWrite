package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.repository.RepositoryRequest;
import com.runnershigh.tps.adapter.in.web.dto.repository.RepositoryResponse;
import com.runnershigh.tps.application.port.in.RepositoryUseCase;
import com.runnershigh.tps.domain.repository.Repository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/v1/repositories")
@RequiredArgsConstructor
@Tag(name = "Repository API", description = "Git 저장소 관리 API")
public class RepositoryController {

    private final RepositoryUseCase repositoryUseCase;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "저장소 생성", description = "새로운 Git 저장소를 등록합니다.")
    public RepositoryResponse createRepository(
            @Valid @RequestBody RepositoryRequest.Create request) {

        RepositoryUseCase.CreateRepositoryCommand command = new RepositoryUseCase.CreateRepositoryCommand(
                request.getProjectId(),
                request.getConnectionId(),
                request.getName(),
                request.getGitUrl(),
                request.getDefaultBranch(),
                request.getStrategyType(),
                request.getMetadata()
        );

        Repository repository = repositoryUseCase.createRepository(command);
        return RepositoryResponse.from(repository);
    }

    @PutMapping("/{id}")
    @Operation(summary = "저장소 수정", description = "저장소 정보를 수정합니다.")
    public RepositoryResponse updateRepository(
            @PathVariable UUID id,
            @Valid @RequestBody RepositoryRequest.Update request) {

        RepositoryUseCase.UpdateRepositoryCommand command = new RepositoryUseCase.UpdateRepositoryCommand(
                request.getName(),
                request.getDefaultBranch(),
                request.getStrategyType(),
                request.getMetadata()
        );

        Repository repository = repositoryUseCase.updateRepository(id, command);
        return RepositoryResponse.from(repository);
    }

    @GetMapping
    @Operation(summary = "전체 저장소 목록", description = "모든 저장소를 조회합니다.")
    public List<RepositoryResponse> getAllRepositories() {
        return repositoryUseCase.getAllRepositories()
                .stream()
                .map(RepositoryResponse::from)
                .toList();
    }

    @GetMapping("/{id}")
    @Operation(summary = "저장소 조회", description = "저장소 상세 정보를 조회합니다.")
    public RepositoryResponse getRepository(@PathVariable UUID id) {
        Repository repository = repositoryUseCase.getRepository(id);
        return RepositoryResponse.from(repository);
    }

    @GetMapping("/project/{projectId}")
    @Operation(summary = "프로젝트별 저장소 목록", description = "프로젝트의 모든 저장소를 조회합니다.")
    public List<RepositoryResponse> getRepositoriesByProjectId(@PathVariable UUID projectId) {
        return repositoryUseCase.getRepositoriesByProjectId(projectId)
                .stream()
                .map(RepositoryResponse::from)
                .toList();
    }

    @GetMapping("/connection/{connectionId}")
    @Operation(summary = "연결별 저장소 목록", description = "특정 연결의 모든 저장소를 조회합니다.")
    public List<RepositoryResponse> getRepositoriesByConnectionId(@PathVariable UUID connectionId) {
        return repositoryUseCase.getRepositoriesByConnectionId(connectionId)
                .stream()
                .map(RepositoryResponse::from)
                .toList();
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "저장소 삭제", description = "저장소를 삭제합니다.")
    public void deleteRepository(@PathVariable UUID id) {
        repositoryUseCase.deleteRepository(id);
    }

    @PostMapping("/{id}/sync")
    @Operation(summary = "저장소 동기화", description = "Git Provider에서 저장소 정보를 동기화합니다.")
    public RepositoryResponse syncRepository(@PathVariable UUID id) {
        Repository repository = repositoryUseCase.syncRepository(id);
        return RepositoryResponse.from(repository);
    }
}
