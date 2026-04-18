package com.runnershigh.tps.domain.connection;

import lombok.Getter;

@Getter
public enum ProviderType {
    GITHUB("GitHub", "https://api.github.com"),
    GITLAB("GitLab", null),
    BITBUCKET("Bitbucket", "https://api.bitbucket.org/2.0");

    private final String displayName;
    private final String defaultApiUrl;

    ProviderType(String displayName, String defaultApiUrl) {
        this.displayName = displayName;
        this.defaultApiUrl = defaultApiUrl;
    }

    public boolean requiresCustomUrl() {
        return this == GITLAB;
    }
}
