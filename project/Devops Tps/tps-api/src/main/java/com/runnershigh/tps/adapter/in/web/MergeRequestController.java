package com.runnershigh.tps.adapter.in.web;

import com.runnershigh.tps.adapter.in.web.dto.mergerequest.MergeRequestRequest;
import com.runnershigh.tps.adapter.in.web.dto.mergerequest.MergeRequestResponse;
import com.runnershigh.tps.application.port.in.MergeRequestUseCase;
import com.runnershigh.tps.domain.mergerequest.MergeRequest;
import com.runnershigh.tps.domain.mergerequest.MergeRequestStatus;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * MergeRequest API Controller
 *
 * <p>Git 저장소의 Merge Request(Pull Request) 관리 API를 제공합니다.</p>
 *
 * <h2>API 목록</h2>
 * <ul>
 *   <li>GET  /v1/merge-requests/{connectionId}/list - MR 목록 조회</li>
 *   <li>GET  /v1/merge-requests/{connectionId}/{number} - MR 상세 조회</li>
 *   <li>POST /v1/merge-requests/list - MR 목록 조회 (POST)</li>
 *   <li>POST /v1/merge-requests/get - MR 상세 조회 (POST)</li>
 *   <li>POST /v1/merge-requests/create - MR 생성</li>
 *   <li>POST /v1/merge-requests/merge - MR 머지</li>
 * </ul>
 */
@RestController
@RequestMapping("/v1/merge-requests")
@RequiredArgsConstructor
@Tag(name = "MergeRequest API", description = "Merge Request(Pull Request) 관리 API")
public class MergeRequestController {

    private final MergeRequestUseCase mergeRequestUseCase;

    // ========================================
    // GET 방식 API
    // ========================================

    @GetMapping("/{connectionId}/list")
    @Operation(summary = "MR 목록 조회", description = "저장소의 Merge Request 목록을 조회합니다.")
    public MergeRequestResponse.MergeRequestList listMergeRequests(
            @PathVariable UUID connectionId,
            @Parameter(description = "저장소 소유자 (owner/workspace)")
            @RequestParam String namespace,
            @Parameter(description = "저장소 이름")
            @RequestParam String repository,
            @Parameter(description = "상태 필터 (OPEN, CLOSED, MERGED, DRAFT)")
            @RequestParam(required = false) MergeRequestStatus status) {

        MergeRequestUseCase.ListMergeRequestsQuery query = new MergeRequestUseCase.ListMergeRequestsQuery(
                connectionId,
                namespace,
                repository,
                status
        );

        List<MergeRequest> mergeRequests = mergeRequestUseCase.listMergeRequests(query);
        return MergeRequestResponse.MergeRequestList.from(mergeRequests);
    }

    @GetMapping("/{connectionId}/{number}")
    @Operation(summary = "MR 상세 조회", description = "특정 Merge Request의 상세 정보를 조회합니다.")
    public MergeRequestResponse.MergeRequestDetail getMergeRequest(
            @PathVariable UUID connectionId,
            @PathVariable Integer number,
            @Parameter(description = "저장소 소유자 (owner/workspace)")
            @RequestParam String namespace,
            @Parameter(description = "저장소 이름")
            @RequestParam String repository) {

        MergeRequestUseCase.GetMergeRequestQuery query = new MergeRequestUseCase.GetMergeRequestQuery(
                connectionId,
                namespace,
                repository,
                number
        );

        MergeRequest mergeRequest = mergeRequestUseCase.getMergeRequest(query);
        return MergeRequestResponse.MergeRequestDetail.from(mergeRequest);
    }

    // ========================================
    // POST 방식 API
    // ========================================

    @PostMapping("/list")
    @Operation(summary = "MR 목록 조회 (POST)", description = "저장소의 Merge Request 목록을 조회합니다. (Body 전송)")
    public MergeRequestResponse.MergeRequestList listMergeRequestsPost(
            @Valid @RequestBody MergeRequestRequest.ListMergeRequests request) {

        MergeRequestUseCase.ListMergeRequestsQuery query = new MergeRequestUseCase.ListMergeRequestsQuery(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getStatus()
        );

        List<MergeRequest> mergeRequests = mergeRequestUseCase.listMergeRequests(query);
        return MergeRequestResponse.MergeRequestList.from(mergeRequests);
    }

    @PostMapping("/get")
    @Operation(summary = "MR 상세 조회 (POST)", description = "특정 Merge Request의 상세 정보를 조회합니다. (Body 전송)")
    public MergeRequestResponse.MergeRequestDetail getMergeRequestPost(
            @Valid @RequestBody MergeRequestRequest.GetMergeRequest request) {

        MergeRequestUseCase.GetMergeRequestQuery query = new MergeRequestUseCase.GetMergeRequestQuery(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getNumber()
        );

        MergeRequest mergeRequest = mergeRequestUseCase.getMergeRequest(query);
        return MergeRequestResponse.MergeRequestDetail.from(mergeRequest);
    }

    @PostMapping("/create")
    @Operation(summary = "MR 생성", description = "새로운 Merge Request를 생성합니다.")
    public MergeRequestResponse.MergeRequestDetail createMergeRequest(
            @Valid @RequestBody MergeRequestRequest.CreateMergeRequest request) {

        MergeRequestUseCase.CreateMergeRequestCommand command = new MergeRequestUseCase.CreateMergeRequestCommand(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getTitle(),
                request.getDescription(),
                request.getSourceBranch(),
                request.getTargetBranch()
        );

        MergeRequest mergeRequest = mergeRequestUseCase.createMergeRequest(command);
        return MergeRequestResponse.MergeRequestDetail.from(mergeRequest);
    }

    @PostMapping("/merge")
    @Operation(summary = "MR 머지", description = "Merge Request를 머지합니다.")
    public MergeRequestResponse.MergeRequestDetail mergeMergeRequest(
            @Valid @RequestBody MergeRequestRequest.MergeMergeRequest request) {

        MergeRequestUseCase.MergeMergeRequestCommand command = new MergeRequestUseCase.MergeMergeRequestCommand(
                request.getConnectionId(),
                request.getNamespace(),
                request.getRepository(),
                request.getNumber(),
                request.getCommitMessage(),
                request.isSquash()
        );

        MergeRequest mergeRequest = mergeRequestUseCase.mergeMergeRequest(command);
        return MergeRequestResponse.MergeRequestDetail.from(mergeRequest);
    }
}
