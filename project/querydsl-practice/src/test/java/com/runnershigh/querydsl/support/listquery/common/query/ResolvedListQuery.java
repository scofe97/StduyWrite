package com.runnershigh.querydsl.support.listquery.common.query;

public record ResolvedListQuery<C extends Enum<C> & ListQueryColumn>(
    int page,
    int size,
    int limit,
    long offset,
    ResolvedSearchCondition<C> searchQuery,
    ResolvedSortCondition<C> sortQuery
) {
}
