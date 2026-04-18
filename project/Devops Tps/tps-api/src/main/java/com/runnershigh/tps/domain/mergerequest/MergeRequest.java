package com.runnershigh.tps.domain.mergerequest;

import com.runnershigh.tps.domain.common.BaseEntity;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;

/**
 * Merge Request 도메인 객체
 *
 * <p>Git 저장소의 Merge Request(Pull Request) 정보를 나타냅니다.</p>
 *
 * <h2>용어 정리</h2>
 * <ul>
 *   <li><strong>GitHub</strong>: Pull Request (PR)</li>
 *   <li><strong>GitLab</strong>: Merge Request (MR)</li>
 *   <li><strong>Bitbucket</strong>: Pull Request (PR)</li>
 * </ul>
 *
 * <p>본 시스템에서는 MergeRequest로 통일합니다.</p>
 */
@Getter
@Setter
@NoArgsConstructor
public class MergeRequest extends BaseEntity {

    private UUID repositoryId;
    private String externalId;
    private Integer number;
    private String title;
    private String description;
    private MergeRequestStatus status;
    private String sourceBranch;
    private String targetBranch;
    private String authorName;
    private String authorEmail;
    private String url;
    private String mergedAt;
    private String closedAt;

    @Builder
    public MergeRequest(UUID repositoryId, String externalId, Integer number,
                        String title, String description, MergeRequestStatus status,
                        String sourceBranch, String targetBranch,
                        String authorName, String authorEmail, String url,
                        String mergedAt, String closedAt) {
        super();
        this.repositoryId = repositoryId;
        this.externalId = externalId;
        this.number = number;
        this.title = title;
        this.description = description;
        this.status = status != null ? status : MergeRequestStatus.OPEN;
        this.sourceBranch = sourceBranch;
        this.targetBranch = targetBranch;
        this.authorName = authorName;
        this.authorEmail = authorEmail;
        this.url = url;
        this.mergedAt = mergedAt;
        this.closedAt = closedAt;
    }

    public boolean isOpen() {
        return this.status == MergeRequestStatus.OPEN;
    }

    public boolean isMerged() {
        return this.status == MergeRequestStatus.MERGED;
    }

    public boolean isClosed() {
        return this.status == MergeRequestStatus.CLOSED;
    }
}
