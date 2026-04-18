package com.runnershigh.tps.domain.connection;

import com.runnershigh.tps.domain.common.BaseEntity;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
public class Connection extends BaseEntity {

    private UUID projectId;
    private ProviderType providerType;
    private String name;
    private String baseUrl;
    private String apiToken;
    private ConnectionStatus status;
    private String metadata;

    @Builder
    public Connection(UUID projectId, ProviderType providerType, String name,
                      String baseUrl, String apiToken, ConnectionStatus status, String metadata) {
        super();
        this.projectId = projectId;
        this.providerType = providerType;
        this.name = name;
        this.baseUrl = baseUrl;
        this.apiToken = apiToken;
        this.status = status != null ? status : ConnectionStatus.PENDING;
        this.metadata = metadata;
    }

    public Connection(UUID id, UUID projectId, ProviderType providerType, String name,
                      String baseUrl, String apiToken, ConnectionStatus status, String metadata) {
        super(id);
        this.projectId = projectId;
        this.providerType = providerType;
        this.name = name;
        this.baseUrl = baseUrl;
        this.apiToken = apiToken;
        this.status = status;
        this.metadata = metadata;
    }

    public void activate() {
        this.status = ConnectionStatus.ACTIVE;
        updateTimestamp();
    }

    public void deactivate() {
        this.status = ConnectionStatus.INACTIVE;
        updateTimestamp();
    }

    public void markAsFailed() {
        this.status = ConnectionStatus.FAILED;
        updateTimestamp();
    }

    public void markAsTesting() {
        this.status = ConnectionStatus.TESTING;
        updateTimestamp();
    }

    public boolean isActive() {
        return this.status == ConnectionStatus.ACTIVE;
    }

    public String getEffectiveBaseUrl() {
        if (baseUrl != null && !baseUrl.isEmpty()) {
            return baseUrl;
        }
        return providerType.getDefaultApiUrl();
    }
}
