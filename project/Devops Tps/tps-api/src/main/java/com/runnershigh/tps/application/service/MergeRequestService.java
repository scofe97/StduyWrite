package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.MergeRequestUseCase;
import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.mergerequest.MergeRequest;
import com.runnershigh.tps.domain.mergerequest.MergeRequestStatus;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * MergeRequest 도메인 서비스
 *
 * <p>Git 저장소의 Merge Request(Pull Request) 관리 기능을 제공합니다.</p>
 *
 * <h2>주요 기능</h2>
 * <ul>
 *   <li>MR 목록 조회</li>
 *   <li>MR 상세 조회</li>
 *   <li>MR 생성</li>
 *   <li>MR 머지</li>
 * </ul>
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MergeRequestService implements MergeRequestUseCase {

    private final GitProviderPort gitProviderPort;
    private final ConnectionRepository connectionRepository;

    @Override
    public List<MergeRequest> listMergeRequests(ListMergeRequestsQuery query) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(query.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + query.connectionId()));

        // 상태를 문자열로 변환
        String state = convertStatusToString(query.status());

        // Git Provider를 통해 MR 목록 조회
        return gitProviderPort.listMergeRequests(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                state
        );
    }

    @Override
    public MergeRequest getMergeRequest(GetMergeRequestQuery query) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(query.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + query.connectionId()));

        // Git Provider를 통해 MR 상세 조회
        return gitProviderPort.getMergeRequest(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.number()
        );
    }

    @Override
    @Transactional
    public MergeRequest createMergeRequest(CreateMergeRequestCommand command) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(command.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + command.connectionId()));

        // Git Provider를 통해 MR 생성
        return gitProviderPort.createMergeRequest(
                command.connectionId(),
                command.namespace(),
                command.repository(),
                command.title(),
                command.description(),
                command.sourceBranch(),
                command.targetBranch()
        );
    }

    @Override
    @Transactional
    public MergeRequest mergeMergeRequest(MergeMergeRequestCommand command) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(command.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + command.connectionId()));

        // Git Provider를 통해 MR 머지
        return gitProviderPort.mergeMergeRequest(
                command.connectionId(),
                command.namespace(),
                command.repository(),
                command.number(),
                command.commitMessage(),
                command.squash()
        );
    }

    /**
     * MergeRequestStatus를 Provider API 상태 문자열로 변환
     */
    private String convertStatusToString(MergeRequestStatus status) {
        if (status == null) {
            return "all";
        }
        return switch (status) {
            case OPEN -> "open";
            case MERGED -> "merged";
            case CLOSED -> "closed";
            case DRAFT -> "draft";
        };
    }
}
