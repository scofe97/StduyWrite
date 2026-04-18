package com.runnershigh.tps.domain.repository;

import lombok.Getter;

@Getter
public enum BranchStrategyType {
    GIT_FLOW("Git Flow", "feature, develop, release, hotfix, main"),
    GITHUB_FLOW("GitHub Flow", "feature, main"),
    TRUNK_BASED("Trunk Based", "feature, main with short-lived branches");

    private final String displayName;
    private final String description;

    BranchStrategyType(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }
}
