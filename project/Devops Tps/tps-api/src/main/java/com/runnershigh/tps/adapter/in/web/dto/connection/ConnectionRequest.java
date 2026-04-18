package com.runnershigh.tps.adapter.in.web.dto.connection;

import com.runnershigh.tps.domain.connection.ProviderType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.UUID;

public class ConnectionRequest {

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Create {
        private UUID projectId;

        @NotNull(message = "Provider type is required")
        private ProviderType providerType;

        @NotBlank(message = "Connection name is required")
        private String name;

        private String baseUrl;
        private String apiToken;
        private String metadata;
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Update {
        private String name;
        private String baseUrl;
        private String apiToken;
        private String metadata;
    }
}
