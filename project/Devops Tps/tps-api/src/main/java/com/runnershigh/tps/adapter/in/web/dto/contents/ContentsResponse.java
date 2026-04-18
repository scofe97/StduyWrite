package com.runnershigh.tps.adapter.in.web.dto.contents;

import com.runnershigh.tps.domain.contents.ContentEntry;
import com.runnershigh.tps.domain.contents.ContentType;
import com.runnershigh.tps.domain.contents.TreeEntry;

import java.util.List;

/**
 * Contents API 응답 DTO
 */
public class ContentsResponse {

    /**
     * 트리 엔트리 응답
     */
    public record Tree(
        String path,
        String type,
        String sha,
        Long size,
        String mode
    ) {
        public static Tree from(TreeEntry entry) {
            // Convert Git types to frontend-friendly types
            String frontendType = switch (entry.getType()) {
                case "blob" -> "FILE";
                case "tree" -> "DIRECTORY";
                default -> entry.getType().toUpperCase();
            };

            return new Tree(
                entry.getPath(),
                frontendType,
                entry.getSha(),
                entry.getSize(),
                entry.getMode()
            );
        }
    }

    /**
     * 콘텐츠 엔트리 응답
     */
    public record Content(
        ContentType type,
        String name,
        String path,
        Long size,
        String sha,
        String content,
        String encoding,
        List<Content> entries
    ) {
        public static Content from(ContentEntry entry) {
            List<Content> childEntries = null;
            if (entry.getEntries() != null) {
                childEntries = entry.getEntries().stream()
                    .map(Content::from)
                    .toList();
            }

            return new Content(
                entry.getType(),
                entry.getName(),
                entry.getPath(),
                entry.getSize(),
                entry.getSha(),
                entry.getContent(),
                entry.getEncoding(),
                childEntries
            );
        }
    }

    /**
     * 트리 조회 응답
     */
    public record TreeResponse(List<Tree> entries) {
        public static TreeResponse from(List<TreeEntry> entries) {
            return new TreeResponse(
                entries.stream().map(Tree::from).toList()
            );
        }
    }
}
