package com.runnershigh.tps.adapter.in.web.dto.mergerequest;

import com.runnershigh.tps.domain.mergerequest.MergeRequest;
import com.runnershigh.tps.domain.mergerequest.MergeRequestStatus;

import java.util.List;
import java.util.UUID;

/**
 * MergeRequest API 응답 DTO
 */
public class MergeRequestResponse {

    /**
     * MR 상세 정보 응답
     */
    public record MergeRequestDetail(
        UUID id,
        UUID repositoryId,
        String externalId,
        Integer number,
        String title,
        String description,
        MergeRequestStatus status,
        String sourceBranch,
        String targetBranch,
        String authorName,
        String authorEmail,
        String url,
        String mergedAt,
        String closedAt,
        String createdAt,
        String updatedAt
    ) {
        public static MergeRequestDetail from(MergeRequest mr) {
            return new MergeRequestDetail(
                mr.getId(),
                mr.getRepositoryId(),
                mr.getExternalId(),
                mr.getNumber(),
                mr.getTitle(),
                mr.getDescription(),
                mr.getStatus(),
                mr.getSourceBranch(),
                mr.getTargetBranch(),
                mr.getAuthorName(),
                mr.getAuthorEmail(),
                mr.getUrl(),
                mr.getMergedAt(),
                mr.getClosedAt(),
                mr.getCreatedAt() != null ? mr.getCreatedAt().toString() : null,
                mr.getUpdatedAt() != null ? mr.getUpdatedAt().toString() : null
            );
        }
    }

    /**
     * MR 목록 응답
     */
    public record MergeRequestList(
        List<MergeRequestSummary> mergeRequests,
        int totalCount
    ) {
        public static MergeRequestList from(List<MergeRequest> mergeRequests) {
            return new MergeRequestList(
                mergeRequests.stream()
                    .map(MergeRequestSummary::from)
                    .toList(),
                mergeRequests.size()
            );
        }
    }

    /**
     * MR 요약 정보
     */
    public record MergeRequestSummary(
        String externalId,
        Integer number,
        String title,
        MergeRequestStatus status,
        String sourceBranch,
        String targetBranch,
        String authorName,
        String url
    ) {
        public static MergeRequestSummary from(MergeRequest mr) {
            return new MergeRequestSummary(
                mr.getExternalId(),
                mr.getNumber(),
                mr.getTitle(),
                mr.getStatus(),
                mr.getSourceBranch(),
                mr.getTargetBranch(),
                mr.getAuthorName(),
                mr.getUrl()
            );
        }
    }
}
