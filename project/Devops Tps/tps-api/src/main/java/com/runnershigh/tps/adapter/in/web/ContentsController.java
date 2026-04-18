package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.contents.ContentsRequest;
import com.runnershigh.tps.adapter.in.web.dto.contents.ContentsResponse;
import com.runnershigh.tps.application.port.in.ContentsUseCase;
import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.TreeEntry;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * Contents API Controller
 *
 * <p>Git 저장소의 파일/디렉토리 조회 API를 제공합니다.</p>
 *
 * <h2>API 목록</h2>
 * <ul>
 *   <li>GET /v1/repositories/{repoId}/tree - 파일 트리 조회</li>
 *   <li>GET /v1/repositories/{repoId}/contents - 파일/디렉토리 내용 조회</li>
 * </ul>
 */
@RestController
@RequestMapping("/v1/repositories")
@RequiredArgsConstructor
@Tag(name = "Contents API", description = "Git 저장소 파일 탐색 API")
public class ContentsController {

    private final ContentsUseCase contentsUseCase;

    @GetMapping("/{connectionId}/tree")
    @Operation(summary = "파일 트리 조회", description = "저장소의 전체 파일 트리를 조회합니다.")
    public ContentsResponse.TreeResponse getTree(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자 (owner/workspace)")
            @RequestParam String namespace,
            @Parameter(description = "저장소 이름")
            @RequestParam String repository,
            @Parameter(description = "브랜치/태그/커밋 SHA (기본: 기본 브랜치)")
            @RequestParam(required = false) String ref,
            @Parameter(description = "전체 트리 조회 여부")
            @RequestParam(required = false, defaultValue = "false") boolean recursive) {

        ContentsUseCase.GetTreeQuery query = new ContentsUseCase.GetTreeQuery(
                connectionId,
                namespace,
                repository,
                ref,
                recursive
        );

        List<TreeEntry> entries = contentsUseCase.getTree(query);
        return ContentsResponse.TreeResponse.from(entries);
    }

    @GetMapping("/{connectionId}/contents")
    @Operation(summary = "파일/디렉토리 내용 조회", description = "특정 경로의 파일 또는 디렉토리 내용을 조회합니다.")
    public ContentsResponse.Content getContents(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자 (owner/workspace)")
            @RequestParam String namespace,
            @Parameter(description = "저장소 이름")
            @RequestParam String repository,
            @Parameter(description = "파일/디렉토리 경로 (빈값은 루트)")
            @RequestParam(required = false, defaultValue = "") String path,
            @Parameter(description = "브랜치/태그/커밋 SHA")
            @RequestParam(required = false) String ref) {

        ContentsUseCase.GetContentsQuery query = new ContentsUseCase.GetContentsQuery(
                connectionId,
                namespace,
                repository,
                path,
                ref
        );

        ContentEntry content = contentsUseCase.getContents(query);
        return ContentsResponse.Content.from(content);
    }

    @PostMapping("/tree")
    @Operation(summary = "파일 트리 조회 (POST)", description = "저장소의 전체 파일 트리를 조회합니다. (Body 전송)")
    public ContentsResponse.TreeResponse getTreePost(
            @Valid @RequestBody ContentsRequest.GetTree request) {

        ContentsUseCase.GetTreeQuery query = new ContentsUseCase.GetTreeQuery(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getRef(),
                request.isRecursive()
        );

        List<TreeEntry> entries = contentsUseCase.getTree(query);
        return ContentsResponse.TreeResponse.from(entries);
    }

    @PostMapping("/contents")
    @Operation(summary = "파일/디렉토리 내용 조회 (POST)", description = "특정 경로의 파일 또는 디렉토리 내용을 조회합니다. (Body 전송)")
    public ContentsResponse.Content getContentsPost(
            @Valid @RequestBody ContentsRequest.GetContents request) {

        ContentsUseCase.GetContentsQuery query = new ContentsUseCase.GetContentsQuery(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getPath(),
                request.getRef()
        );

        ContentEntry content = contentsUseCase.getContents(query);
        return ContentsResponse.Content.from(content);
    }
}
