package com.runnershigh.tps.adapter.in.web.dto.connection;

import com.runnershigh.tps.domain.connection.Connection;
import com.runnershigh.tps.domain.connection.ConnectionStatus;
import com.runnershigh.tps.domain.connection.ProviderType;

import java.time.LocalDateTime;
import java.util.UUID;

public record ConnectionResponse(
    UUID id,
    UUID projectId,
    ProviderType providerType,
    String name,
    String baseUrl,
    ConnectionStatus status,
    String metadata,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {
    public static ConnectionResponse from(Connection connection) {
        return new ConnectionResponse(
            connection.getId(),
            connection.getProjectId(),
            connection.getProviderType(),
            connection.getName(),
            connection.getBaseUrl(),
            connection.getStatus(),
            connection.getMetadata(),
            connection.getCreatedAt(),
            connection.getUpdatedAt()
        );
    }
}
