package com.runnershigh.tps.domain.branchcomparison;

import java.util.List;

/**
 * 브랜치 정리 결과 도메인 객체
 */
public record CleanupResult(
    List<String> deleted,
    List<String> skipped,
    List<String> failed,
    boolean dryRun
) {}
