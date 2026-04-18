package com.runnershigh.tps.application.service;

import com.runnershigh.tps.application.port.in.ContentsUseCase;
import com.runnershigh.tps.application.port.out.ConnectionRepository;
import com.runnershigh.tps.application.port.out.GitProviderPort;
import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.TreeEntry;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * Contents 도메인 서비스
 *
 * <p>Git 저장소의 파일/디렉토리 조회 기능을 제공합니다.</p>
 *
 * <h2>주요 기능</h2>
 * <ul>
 *   <li>파일/디렉토리 내용 조회</li>
 *   <li>전체 파일 트리 조회</li>
 * </ul>
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ContentsService implements ContentsUseCase {

    private final GitProviderPort gitProviderPort;
    private final ConnectionRepository connectionRepository;

    @Override
    public ContentEntry getContents(GetContentsQuery query) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(query.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + query.connectionId()));

        // Git Provider를 통해 콘텐츠 조회
        return gitProviderPort.getContents(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.path(),
                query.ref()
        );
    }

    @Override
    public List<TreeEntry> getTree(GetTreeQuery query) {
        // 연결 정보 검증
        Connection connection = connectionRepository.findById(query.connectionId())
                .orElseThrow(() -> new IllegalArgumentException("Connection not found: " + query.connectionId()));

        // Git Provider를 통해 트리 조회
        return gitProviderPort.getTree(
                query.connectionId(),
                query.namespace(),
                query.repository(),
                query.ref(),
                query.recursive()
        );
    }
}
