package com.runnershigh.tps.domain.branchcomparison;

import lombok.Builder;
import lombok.Getter;

/**
 * 변경 통계 도메인 객체
 */
@Getter
@Builder
public class DiffStat {
    private final int filesChanged;
    private final int additions;
    private final int deletions;
}
