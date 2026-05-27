package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Supplier;

import com.runnershigh.querydsl.support.listquery.common.exception.InvalidListQueryException;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryColumn;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryPolicy;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryResponse;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedListQuery;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedSearchCondition;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;
import com.querydsl.jpa.JPQLQuery;

public abstract class AbstractQuerydslListQueryRepository<C extends Enum<C> & ListQueryColumn, Q> {

    protected abstract ListQueryPolicy<C> policy();

    protected abstract QueryColumnBindingRegistry<C, Q> registry();

    protected QuerydslQueryHooks<C, Q> hooks() {
        return QuerydslQueryHooks.noop();
    }

    protected Predicate buildPredicate(
        ResolvedListQuery<C> resolvedQuery,
        Q context,
        Predicate baseCondition
    ) {
        BooleanBuilder builder = new BooleanBuilder();

        if (baseCondition != null) {
            builder.and(baseCondition);
        }

        Predicate hookBasePredicate = hooks().basePredicate(context);
        if (hookBasePredicate != null) {
            builder.and(hookBasePredicate);
        }

        ResolvedSearchCondition<C> searchCondition = resolvedQuery.searchQuery();
        if (searchCondition == null) {
            return builder;
        }

        if (searchCondition.hasKeyword()) {
            builder.and(buildKeywordPredicate(searchCondition, context));
        }

        if (searchCondition.hasDetailConditions()) {
            for (ResolvedDetailCondition<C> detailCondition : searchCondition.detailConditions()) {
                builder.and(buildDetailPredicate(detailCondition, context));
            }
        }

        return builder;
    }

    protected OrderSpecifier<?>[] buildOrderSpecifiers(
        ResolvedListQuery<C> resolvedQuery,
        Q context
    ) {
        List<OrderSpecifier<?>> orderSpecifiers = new ArrayList<>();
        orderSpecifiers.add(buildOrderSpecifier(context, resolvedQuery.sortQuery().column(), resolvedQuery.sortQuery().direction()));

        C tieBreakerColumn = policy().getTieBreakerSortColumn();
        if (tieBreakerColumn != null && tieBreakerColumn != resolvedQuery.sortQuery().column()) {
            orderSpecifiers.add(buildOrderSpecifier(context, tieBreakerColumn, policy().getTieBreakerSortDirection()));
        }

        return orderSpecifiers.toArray(OrderSpecifier[]::new);
    }

    protected <T> ListQueryResponse<T> executeListQuery(
        ResolvedListQuery<C> resolvedQuery,
        Supplier<JPQLQuery<Long>> countQuerySupplier,
        Supplier<JPQLQuery<T>> dataQuerySupplier
    ) {
        long totalCount = Optional.ofNullable(countQuerySupplier.get().fetchOne()).orElse(0L);
        if (totalCount == 0L) {
            return ListQueryResponse.of(resolvedQuery.size(), 0, List.of());
        }

        List<T> data = dataQuerySupplier.get()
            .offset(resolvedQuery.offset())
            .limit(resolvedQuery.limit())
            .fetch();

        return ListQueryResponse.of(resolvedQuery.size(), Math.toIntExact(totalCount), data);
    }

    private Predicate buildKeywordPredicate(ResolvedSearchCondition<C> searchCondition, Q context) {
        BooleanBuilder allColumnBuilder = new BooleanBuilder();
        for (C globalSearchColumn : policy().getGlobalSearchColumns()) {
            allColumnBuilder.or(buildKeywordPredicate(context, globalSearchColumn, searchCondition.keyword()));
        }

        return allColumnBuilder;
    }

    private Predicate buildKeywordPredicate(Q context, C column, String keyword) {
        Predicate customPredicate = hooks().keywordPredicate(context, column, keyword);
        if (customPredicate != null) {
            return customPredicate;
        }

        QueryColumnBinding<Q> columnBinding = registry().get(column);
        if (columnBinding == null || !columnBinding.supportsKeyword()) {
            throw new InvalidListQueryException("Keyword search is not implemented for column: " + column.getInputName());
        }

        return columnBinding.buildKeyword(context, keyword);
    }

    private Predicate buildDetailPredicate(ResolvedDetailCondition<C> detailCondition, Q context) {
        Predicate customPredicate = hooks().detailPredicate(context, detailCondition);
        if (customPredicate != null) {
            return customPredicate;
        }

        QueryColumnBinding<Q> columnBinding = registry().get(detailCondition.column());
        if (columnBinding == null || !columnBinding.supportsDetail(detailCondition.type())) {
            throw new InvalidListQueryException(
                "Detail search is not implemented for column/type: %s/%s".formatted(
                    detailCondition.column().getInputName(),
                    detailCondition.type()
                )
            );
        }

        return columnBinding.buildDetail(context, detailCondition);
    }

    private OrderSpecifier<?> buildOrderSpecifier(Q context, C column, SortDirection direction) {
        OrderSpecifier<?> customOrderSpecifier = hooks().orderSpecifier(context, column, direction);
        if (customOrderSpecifier != null) {
            return customOrderSpecifier;
        }

        QueryColumnBinding<Q> columnBinding = registry().get(column);
        if (columnBinding == null || !columnBinding.supportsOrder()) {
            throw new InvalidListQueryException("Ordering is not implemented for column: " + column.getInputName());
        }

        return columnBinding.buildOrder(context, direction);
    }
}
