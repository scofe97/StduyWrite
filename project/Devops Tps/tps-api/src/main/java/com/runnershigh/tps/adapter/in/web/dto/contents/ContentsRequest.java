package com.runnershigh.tps.adapter.in.web.dto.contents;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;

/**
 * Contents API 요청 DTO
 */
public class ContentsRequest {

    /**
     * 파일/디렉토리 내용 조회 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class GetContents {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private String path = "";
        private String ref;
    }

    /**
     * 트리 조회 요청
     */
    @Getter
    @Setter
    @NoArgsConstructor
    public static class GetTree {
        @NotNull(message = "connectionId is required")
        private UUID connectionId;

        @NotBlank(message = "namespace is required")
        private String namespace;

        @NotBlank(message = "repository is required")
        private String repository;

        private String ref;
        private boolean recursive = false;
    }
}
