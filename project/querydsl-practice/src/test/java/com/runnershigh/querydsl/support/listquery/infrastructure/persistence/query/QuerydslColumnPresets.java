package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import java.time.LocalDateTime;
import java.util.function.BiFunction;
import java.util.function.Function;

import com.runnershigh.querydsl.support.listquery.common.query.ResolvedDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;
import com.querydsl.core.types.dsl.ComparableExpressionBase;
import com.querydsl.core.types.dsl.DateTimeExpression;
import com.querydsl.core.types.dsl.Expressions;
import com.querydsl.core.types.dsl.SimpleExpression;
import com.querydsl.core.types.dsl.StringExpression;

public final class QuerydslColumnPresets {

    private QuerydslColumnPresets() {
    }

    public static <Q> BiFunction<Q, String, Predicate> keywordContains(
        Function<Q, StringExpression> expressionProvider
    ) {
        return (context, keyword) -> contains(expressionProvider.apply(context), keyword);
    }

    public static <Q> BiFunction<Q, String, Predicate> keywordRegexp(
        Function<Q, StringExpression> expressionProvider
    ) {
        return (context, keyword) -> regexp(expressionProvider.apply(context), keyword);
    }

    public static <Q> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailTextContains(
        Function<Q, StringExpression> expressionProvider
    ) {
        return (context, detailCondition) -> contains(expressionProvider.apply(context), detailCondition.value());
    }

    public static <Q> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailTextRegexp(
        Function<Q, StringExpression> expressionProvider
    ) {
        return (context, detailCondition) -> regexp(expressionProvider.apply(context), detailCondition.value());
    }

    public static <Q, T> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailSelection(
        Function<Q, SimpleExpression<T>> expressionProvider,
        Function<String, T> valueConverter
    ) {
        return (context, detailCondition) -> expressionProvider.apply(context).in(
            detailCondition.valueList().stream().map(valueConverter).toList()
        );
    }

    public static <Q> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailDateTimeRange(
        Function<Q, DateTimeExpression<LocalDateTime>> expressionProvider
    ) {
        return (context, detailCondition) -> {
            DateTimeExpression<LocalDateTime> expression = expressionProvider.apply(context);
            BooleanBuilder builder = new BooleanBuilder();

            if (detailCondition.startDateTime() != null) {
                builder.and(expression.goe(detailCondition.startDateTime()));
            }

            if (detailCondition.endDateTime() != null) {
                builder.and(expression.loe(detailCondition.endDateTime()));
            }

            return builder;
        };
    }

    /**
     * Creates a simple CSV-style group filter for {@code DetailConditionType.G}.
     * Use this only when a single value can be translated into a DB predicate such as
     * {@code FIND_IN_SET(value, column) > 0}. More complex semantics should be implemented
     * through {@link QuerydslQueryHooks}.
     */
    public static <Q> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailGroupCsv(
        BiFunction<Q, String, Predicate> valuePredicateFactory
    ) {
        return (context, detailCondition) -> {
            BooleanBuilder builder = new BooleanBuilder();

            for (String value : detailCondition.valueList()) {
                builder.or(valuePredicateFactory.apply(context, value));
            }

            return builder;
        };
    }

    public static <Q> BiFunction<Q, ResolvedDetailCondition<?>, Predicate> detailGroupFindInSet(
        Function<Q, StringExpression> expressionProvider
    ) {
        return detailGroupCsv((context, value) ->
            Expressions.booleanTemplate(
                "function('find_in_set', {0}, {1}) > 0",
                value,
                expressionProvider.apply(context)
            )
        );
    }

    public static <Q> BiFunction<Q, SortDirection, OrderSpecifier<?>> orderByComparable(
        Function<Q, ComparableExpressionBase<?>> expressionProvider
    ) {
        return (context, direction) -> orderBy(expressionProvider.apply(context), direction);
    }

    private static Predicate contains(StringExpression expression, String keyword) {
        return expression.like("%" + escapeLikePattern(keyword) + "%", '\\');
    }

    private static Predicate regexp(StringExpression expression, String keyword) {
        return Expressions.numberTemplate(
            Integer.class,
            "function('regexp_instr', {0}, {1})",
            expression,
            keyword
        ).gt(0);
    }

    private static String escapeLikePattern(String value) {
        if (value == null) {
            return null;
        }
        return value
            .replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_");
    }

    private static OrderSpecifier<?> orderBy(ComparableExpressionBase<?> expression, SortDirection direction) {
        return direction == SortDirection.ASC ? expression.asc() : expression.desc();
    }
}
