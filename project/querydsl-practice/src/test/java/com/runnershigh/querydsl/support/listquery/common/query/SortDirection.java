package com.runnershigh.querydsl.support.listquery.common.query;

public enum SortDirection {
    ASC,
    DESC;

    public static SortDirection from(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }

        return SortDirection.valueOf(value.trim());
    }
}
