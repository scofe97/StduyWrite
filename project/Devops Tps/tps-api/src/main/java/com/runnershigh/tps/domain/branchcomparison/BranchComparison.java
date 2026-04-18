package com.runnershigh.tps.domain.branchcomparison;

import lombok.Builder;
import lombok.Getter;

/**
 * 브랜치 비교 결과 도메인 객체
 */
@Getter
@Builder
public class BranchComparison {
    private final String baseBranch;
    private final String compareBranch;
    private final int aheadBy;
    private final int behindBy;
    private final MergeableState mergeable;
    private final String mergeStatus;
    private final SuggestedAction suggestedAction;
    private final String baseSha;
    private final String compareSha;
    private final String mergeBaseSha;
}
