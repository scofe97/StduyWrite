package com.runnershigh.querydsl.support.listquery.common.query;

public record ResolvedSortCondition<C extends Enum<C> & ListQueryColumn>(
    C column,
    SortDirection direction
) {
}
