package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.mergerequest.MergeRequest;
import com.runnershigh.tps.domain.mergerequest.MergeRequestStatus;

import java.util.List;
import java.util.UUID;

/**
 * MergeRequest 도메인의 인바운드 포트 (Use Case)
 *
 * <p>Merge Request(Pull Request) 관리 기능을 정의합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * Controller (Adapter-In)
 *      │
 *      ▼
 * MergeRequestUseCase (Port-In) ◀── 현재 위치
 *      │
 *      ▼
 * MergeRequestService (구현체)
 *      │
 *      ├──▶ MergeRequestRepository (Port-Out) → DB
 *      └──▶ GitProviderPort (Port-Out) → gRPC 서버
 * </pre>
 */
public interface MergeRequestUseCase {

    /**
     * 저장소의 Merge Request 목록을 조회합니다.
     *
     * @param query 조회 요청 정보
     * @return Merge Request 목록
     */
    List<MergeRequest> listMergeRequests(ListMergeRequestsQuery query);

    /**
     * 특정 Merge Request를 조회합니다.
     *
     * @param query 조회 요청 정보
     * @return Merge Request 상세 정보
     */
    MergeRequest getMergeRequest(GetMergeRequestQuery query);

    /**
     * 새로운 Merge Request를 생성합니다.
     *
     * @param command 생성 명령
     * @return 생성된 Merge Request
     */
    MergeRequest createMergeRequest(CreateMergeRequestCommand command);

    /**
     * Merge Request를 머지합니다.
     *
     * @param command 머지 명령
     * @return 머지된 Merge Request
     */
    MergeRequest mergeMergeRequest(MergeMergeRequestCommand command);

    /**
     * MR 목록 조회 Query
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repository   저장소 이름
     * @param status       상태 필터 (null이면 전체)
     */
    record ListMergeRequestsQuery(
            UUID connectionId,
            String namespace,
            String repository,
            MergeRequestStatus status
    ) {}

    /**
     * MR 상세 조회 Query
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repository   저장소 이름
     * @param number       MR 번호
     */
    record GetMergeRequestQuery(
            UUID connectionId,
            String namespace,
            String repository,
            Integer number
    ) {}

    /**
     * MR 생성 Command
     *
     * @param connectionId  연결 ID
     * @param namespace     저장소 소유자
     * @param repository    저장소 이름
     * @param title         제목
     * @param description   설명
     * @param sourceBranch  소스 브랜치
     * @param targetBranch  타겟 브랜치
     */
    record CreateMergeRequestCommand(
            UUID connectionId,
            String namespace,
            String repository,
            String title,
            String description,
            String sourceBranch,
            String targetBranch
    ) {}

    /**
     * MR 머지 Command
     *
     * @param connectionId   연결 ID
     * @param namespace      저장소 소유자
     * @param repository     저장소 이름
     * @param number         MR 번호
     * @param commitMessage  커밋 메시지 (선택적)
     * @param squash         스쿼시 머지 여부
     */
    record MergeMergeRequestCommand(
            UUID connectionId,
            String namespace,
            String repository,
            Integer number,
            String commitMessage,
            boolean squash
    ) {}
}
