package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import java.time.LocalDateTime;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;

import com.runnershigh.querydsl.support.listquery.common.query.DetailConditionType;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;
import com.querydsl.core.types.dsl.ComparableExpressionBase;
import com.querydsl.core.types.dsl.DateTimeExpression;
import com.querydsl.core.types.dsl.SimpleExpression;
import com.querydsl.core.types.dsl.StringExpression;

public final class QueryColumnBindingBuilder<Q> {

    private BiFunction<Q, String, Predicate> keywordFactory;
    private final Map<DetailConditionType, BiFunction<Q, ResolvedDetailCondition<?>, Predicate>> detailFactories =
        new EnumMap<>(DetailConditionType.class);
    private BiFunction<Q, SortDirection, OrderSpecifier<?>> orderFactory;

    private QueryColumnBindingBuilder() {
    }

    public static <Q> QueryColumnBindingBuilder<Q> builder() {
        return new QueryColumnBindingBuilder<>();
    }

    public QueryColumnBindingBuilder<Q> keyword(BiFunction<Q, String, Predicate> keywordFactory) {
        this.keywordFactory = keywordFactory;
        return this;
    }

    public QueryColumnBindingBuilder<Q> keywordContains(Function<Q, StringExpression> expressionProvider) {
        return keyword(QuerydslColumnPresets.keywordContains(expressionProvider));
    }

    public QueryColumnBindingBuilder<Q> keywordRegexp(Function<Q, StringExpression> expressionProvider) {
        return keyword(QuerydslColumnPresets.keywordRegexp(expressionProvider));
    }

    public QueryColumnBindingBuilder<Q> detail(
        DetailConditionType detailConditionType,
        BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailFactory
    ) {
        detailFactories.put(detailConditionType, detailFactory);
        return this;
    }

    public QueryColumnBindingBuilder<Q> detailTextContains(Function<Q, StringExpression> expressionProvider) {
        return detail(DetailConditionType.T, QuerydslColumnPresets.detailTextContains(expressionProvider));
    }

    public QueryColumnBindingBuilder<Q> detailTextRegexp(Function<Q, StringExpression> expressionProvider) {
        return detail(DetailConditionType.T, QuerydslColumnPresets.detailTextRegexp(expressionProvider));
    }

    public <T> QueryColumnBindingBuilder<Q> detailSelection(
        Function<Q, SimpleExpression<T>> expressionProvider,
        Function<String, T> valueConverter
    ) {
        BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailFactory =
            QuerydslColumnPresets.detailSelection(expressionProvider, valueConverter);
        detailFactories.put(DetailConditionType.S, detailFactory);
        detailFactories.put(DetailConditionType.R, detailFactory);
        return this;
    }

    public QueryColumnBindingBuilder<Q> detailDateTimeRange(Function<Q, DateTimeExpression<LocalDateTime>> expressionProvider) {
        return detail(DetailConditionType.D, QuerydslColumnPresets.detailDateTimeRange(expressionProvider));
    }

    public QueryColumnBindingBuilder<Q> detailGroupCsv(BiFunction<Q, String, Predicate> valuePredicateFactory) {
        return detail(DetailConditionType.G, QuerydslColumnPresets.detailGroupCsv(valuePredicateFactory));
    }

    public QueryColumnBindingBuilder<Q> detailGroupFindInSet(Function<Q, StringExpression> expressionProvider) {
        return detail(DetailConditionType.G, QuerydslColumnPresets.detailGroupFindInSet(expressionProvider));
    }

    public QueryColumnBindingBuilder<Q> order(BiFunction<Q, SortDirection, OrderSpecifier<?>> orderFactory) {
        this.orderFactory = orderFactory;
        return this;
    }

    public QueryColumnBindingBuilder<Q> orderByComparable(Function<Q, ComparableExpressionBase<?>> expressionProvider) {
        return order(QuerydslColumnPresets.orderByComparable(expressionProvider));
    }

    public QueryColumnBinding<Q> build() {
        return new QueryColumnBinding<>(keywordFactory, Map.copyOf(detailFactories), orderFactory);
    }
}
