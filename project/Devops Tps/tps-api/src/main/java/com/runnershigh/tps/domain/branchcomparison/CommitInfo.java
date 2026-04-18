package com.runnershigh.tps.domain.branchcomparison;

import lombok.Builder;
import lombok.Getter;

/**
 * 간략한 커밋 정보 도메인 객체
 */
@Getter
@Builder
public class CommitInfo {
    private final String sha;
    private final String message;
    private final String authorName;
    private final String authorEmail;
    private final String date;
}
