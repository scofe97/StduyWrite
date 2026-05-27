package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.List;

public record ResolvedSearchCondition<C extends Enum<C> & ListQueryColumn>(
    String keyword,
    boolean allColumns,
    C column,
    List<ResolvedDetailCondition<C>> detailConditions
) {

    public boolean hasKeyword() {
        return keyword != null;
    }

    public boolean hasDetailConditions() {
        return detailConditions != null && !detailConditions.isEmpty();
    }

    @Deprecated(since = "2026-04-28")
    public boolean allColumns() {
        return allColumns;
    }

    @Deprecated(since = "2026-04-28")
    public C column() {
        return column;
    }
}
