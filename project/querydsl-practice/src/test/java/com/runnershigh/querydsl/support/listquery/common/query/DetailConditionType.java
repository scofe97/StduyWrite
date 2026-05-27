package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.Arrays;

import com.runnershigh.querydsl.support.listquery.common.exception.InvalidListQueryException;

public enum DetailConditionType {
    T,
    S,
    R,
    G,
    D;

    public static DetailConditionType from(String type) {
        return Arrays.stream(values())
            .filter(value -> value.name().equals(type))
            .findFirst()
            .orElseThrow(() -> new InvalidListQueryException("Unsupported detail condition type: " + type));
    }
}
