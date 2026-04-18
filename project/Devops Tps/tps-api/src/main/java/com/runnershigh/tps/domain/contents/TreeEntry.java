package com.runnershigh.tps.domain.contents;

import lombok.Builder;
import lombok.Getter;

/**
 * 트리 엔트리 도메인 객체
 *
 * <p>Git 저장소의 전체 트리 구조에서 개별 항목을 나타냅니다.
 * 파일 트리 사이드바 표시에 최적화되어 있습니다.</p>
 */
@Getter
@Builder
public class TreeEntry {

    private final String path;
    private final String type;
    private final String sha;
    private final Long size;
    private final String mode;

    public boolean isBlob() {
        return "blob".equals(type);
    }

    public boolean isTree() {
        return "tree".equals(type);
    }
}
