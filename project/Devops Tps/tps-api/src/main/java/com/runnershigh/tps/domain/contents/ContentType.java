package com.runnershigh.tps.domain.contents;

/**
 * 콘텐츠 타입
 *
 * <p>Git 저장소 내 항목의 유형을 나타냅니다.</p>
 */
public enum ContentType {
    FILE,
    DIRECTORY,
    SYMLINK,
    SUBMODULE
}
