package com.runnershigh.tps.domain.branchcomparison;

import lombok.Builder;
import lombok.Getter;

/**
 * 머지된 브랜치 정보 도메인 객체
 */
@Getter
@Builder
public class MergedBranchInfo {
    private final String name;
    private final String mergedAt;
    private final String mergedBy;
    private final String lastCommitSha;
    private final String mergedInto;
}
