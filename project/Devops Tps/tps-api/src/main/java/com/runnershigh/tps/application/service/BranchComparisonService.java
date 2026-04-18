package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.BranchComparisonUseCase;
import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.domain.branchcomparison.CleanupResult;
import com.runnershigh.tps.domain.branchcomparison.MergedBranchInfo;
import com.runnershigh.tps.domain.branchcomparison.StaleBranchInfo;
import com.runnershigh.tps.domain.connection.Connection;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 브랜치 비교 도메인 서비스
 *
 * <p>브랜치 간 비교, 머지된 브랜치 조회, 브랜치 정리 기능을 제공합니다.</p>
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class BranchComparisonService implements BranchComparisonUseCase {

    private final GitProviderPort gitProviderPort;
    private final ConnectionRepository connectionRepository;

    @Override
    public ComparisonResult compareBranches(CompareBranchesQuery query) {
        validateConnection(query.connectionId());

        GitProviderPort.BranchComparisonResult result = gitProviderPort.compareBranches(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.base(),
                query.compare()
        );

        return new ComparisonResult(result.comparison(), result.diffStat());
    }

    @Override
    public CommitDiffResult listCommitsDiff(ListCommitsDiffQuery query) {
        validateConnection(query.connectionId());

        GitProviderPort.CommitDiffResult result = gitProviderPort.listCommitsDiff(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.base(),
                query.compare(),
                query.page(),
                query.perPage()
        );

        return new CommitDiffResult(result.commits(), result.totalCount());
    }

    @Override
    public List<MergedBranchInfo> listMergedBranches(ListMergedBranchesQuery query) {
        validateConnection(query.connectionId());

        return gitProviderPort.listMergedBranches(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.base()
        );
    }

    @Override
    public List<StaleBranchInfo> listStaleBranches(ListStaleBranchesQuery query) {
        validateConnection(query.connectionId());

        return gitProviderPort.listStaleBranches(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.staleDays()
        );
    }

    @Override
    @Transactional
    public CleanupResult cleanupBranches(CleanupBranchesCommand command) {
        validateConnection(command.connectionId());

        return gitProviderPort.cleanupBranches(
                command.connectionId(),
                command.namespace(),
                command.repository(),
                command.dryRun(),
                command.excludePatterns(),
                command.staleDays(),
                command.includeMerged(),
                command.includeStale()
        );
    }

    private Connection validateConnection(java.util.UUID connectionId) {
        return connectionRepository.findById(connectionId)
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + connectionId));
    }
}
