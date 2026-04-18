package com.runnershigh.tps.domain.branch;

import lombok.Getter;

@Getter
public enum BranchType {
    MAIN("main", "Production branch"),
    DEVELOP("develop", "Development integration branch"),
    FEATURE("feature", "Feature development branch"),
    RELEASE("release", "Release preparation branch"),
    HOTFIX("hotfix", "Production bug fix branch");

    private final String prefix;
    private final String description;

    BranchType(String prefix, String description) {
        this.prefix = prefix;
        this.description = description;
    }

    public static BranchType fromBranchName(String branchName) {
        if (branchName == null) {
            return FEATURE;
        }
        if (branchName.equals("main") || branchName.equals("master")) {
            return MAIN;
        }
        if (branchName.equals("develop") || branchName.equals("dev")) {
            return DEVELOP;
        }
        if (branchName.startsWith("feature/")) {
            return FEATURE;
        }
        if (branchName.startsWith("release/")) {
            return RELEASE;
        }
        if (branchName.startsWith("hotfix/")) {
            return HOTFIX;
        }
        return FEATURE;
    }
}
