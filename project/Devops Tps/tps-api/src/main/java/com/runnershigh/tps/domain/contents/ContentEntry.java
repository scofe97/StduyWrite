package com.runnershigh.tps.domain.contents;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

/**
 * 콘텐츠 엔트리 도메인 객체
 *
 * <p>Git 저장소 내 파일 또는 디렉토리의 내용을 나타냅니다.</p>
 *
 * <h2>사용 예시</h2>
 * <ul>
 *   <li><strong>디렉토리</strong>: entries 필드에 하위 항목 목록 포함, content는 null</li>
 *   <li><strong>파일</strong>: content 필드에 파일 내용 포함 (base64), entries는 null</li>
 * </ul>
 */
@Getter
@Builder
public class ContentEntry {

    private final ContentType type;
    private final String name;
    private final String path;
    private final Long size;
    private final String content;
    private final String encoding;
    private final String sha;
    private final List<ContentEntry> entries;

    public boolean isFile() {
        return type == ContentType.FILE;
    }

    public boolean isDirectory() {
        return type == ContentType.DIRECTORY;
    }
}
