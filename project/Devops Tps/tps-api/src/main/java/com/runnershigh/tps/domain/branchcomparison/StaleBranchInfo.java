package com.runnershigh.tps.domain.branchcomparison;

import lombok.Builder;
import lombok.Getter;

/**
 * Stale 브랜치 정보 도메인 객체
 */
@Getter
@Builder
public class StaleBranchInfo {
    private final String name;
    private final String lastCommitSha;
    private final String lastCommitDate;
    private final int daysInactive;
}
