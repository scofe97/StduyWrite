package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import java.util.Map;
import java.util.function.BiFunction;

import com.runnershigh.querydsl.support.listquery.common.query.DetailConditionType;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;

public final class QueryColumnBinding<Q> {

    private final BiFunction<Q, String, Predicate> keywordFactory;
    private final Map<DetailConditionType, BiFunction<Q, ResolvedDetailCondition<?>, Predicate>> detailFactories;
    private final BiFunction<Q, SortDirection, OrderSpecifier<?>> orderFactory;

    public QueryColumnBinding(
        BiFunction<Q, String, Predicate> keywordFactory,
        Map<DetailConditionType, BiFunction<Q, ResolvedDetailCondition<?>, Predicate>> detailFactories,
        BiFunction<Q, SortDirection, OrderSpecifier<?>> orderFactory
    ) {
        this.keywordFactory = keywordFactory;
        this.detailFactories = detailFactories;
        this.orderFactory = orderFactory;
    }

    public boolean supportsKeyword() {
        return keywordFactory != null;
    }

    public boolean supportsDetail(DetailConditionType detailConditionType) {
        return detailFactories.containsKey(detailConditionType);
    }

    public boolean supportsOrder() {
        return orderFactory != null;
    }

    public Predicate buildKeyword(Q context, String keyword) {
        if (keywordFactory == null) {
            throw new IllegalStateException("Keyword factory is not configured for this column binding");
        }
        return keywordFactory.apply(context, keyword);
    }

    public Predicate buildDetail(Q context, ResolvedDetailCondition<?> detailCondition) {
        BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailFactory = detailFactories.get(detailCondition.type());
        if (detailFactory == null) {
            throw new IllegalStateException("Detail factory is not configured for type: " + detailCondition.type());
        }
        return detailFactory.apply(context, detailCondition);
    }

    public OrderSpecifier<?> buildOrder(Q context, SortDirection direction) {
        if (orderFactory == null) {
            throw new IllegalStateException("Order factory is not configured for this column binding");
        }
        return orderFactory.apply(context, direction);
    }
}
