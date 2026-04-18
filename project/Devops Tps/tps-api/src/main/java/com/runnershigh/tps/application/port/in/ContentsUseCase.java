package com.runnershigh.tps.application.port.in;

import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.TreeEntry;

import java.util.List;
import java.util.UUID;

/**
 * Contents 도메인의 인바운드 포트 (Use Case)
 *
 * <p>Git 저장소 내 파일/디렉토리 조회 기능을 정의합니다.</p>
 *
 * <h2>Hexagonal Architecture에서의 역할</h2>
 * <pre>
 * Controller (Adapter-In)
 *      │
 *      ▼
 * ContentsUseCase (Port-In) ◀── 현재 위치
 *      │
 *      ▼
 * ContentsService (구현체)
 *      │
 *      ▼
 * GitProviderPort (Port-Out) → gRPC 서버
 * </pre>
 */
public interface ContentsUseCase {

    /**
     * 특정 경로의 파일/디렉토리 내용을 조회합니다.
     *
     * <h3>동작 방식</h3>
     * <ul>
     *   <li><strong>디렉토리</strong>: 하위 항목 목록 반환</li>
     *   <li><strong>파일</strong>: 파일 내용(base64) + 메타데이터 반환</li>
     * </ul>
     *
     * @param query 조회 요청 정보
     * @return 파일/디렉토리 콘텐츠 정보
     */
    ContentEntry getContents(GetContentsQuery query);

    /**
     * 저장소의 전체 파일 트리를 조회합니다.
     *
     * <p>사이드바 파일 트리 표시에 사용됩니다.
     * recursive=true로 호출하면 전체 트리를 한 번에 가져옵니다.</p>
     *
     * @param query 트리 조회 요청 정보
     * @return 트리 항목 목록
     */
    List<TreeEntry> getTree(GetTreeQuery query);

    /**
     * 파일/디렉토리 조회 Query
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자 (owner/org)
     * @param repository   저장소 이름
     * @param path         경로 (빈 문자열은 루트)
     * @param ref          브랜치/태그/커밋 (null이면 기본 브랜치)
     */
    record GetContentsQuery(
            UUID connectionId,
            String namespace,
            String repository,
            String path,
            String ref
    ) {
        public GetContentsQuery {
            if (path == null) path = "";
        }
    }

    /**
     * 트리 조회 Query
     *
     * @param connectionId 연결 ID
     * @param namespace    저장소 소유자
     * @param repository   저장소 이름
     * @param ref          브랜치/태그/커밋
     * @param recursive    전체 트리 조회 여부
     */
    record GetTreeQuery(
            UUID connectionId,
            String namespace,
            String repository,
            String ref,
            boolean recursive
    ) {}
}
