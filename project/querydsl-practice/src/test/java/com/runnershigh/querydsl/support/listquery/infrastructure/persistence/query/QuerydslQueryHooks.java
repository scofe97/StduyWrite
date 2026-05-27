package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import com.runnershigh.querydsl.support.listquery.common.query.ListQueryColumn;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;

public interface QuerydslQueryHooks<C extends Enum<C> & ListQueryColumn, Q> {

    default Predicate basePredicate(Q context) {
        return null;
    }

    default Predicate keywordPredicate(Q context, C column, String keyword) {
        return null;
    }

    default Predicate detailPredicate(Q context, ResolvedDetailCondition<C> detailCondition) {
        return null;
    }

    default OrderSpecifier<?> orderSpecifier(Q context, C column, SortDirection direction) {
        return null;
    }

    static <C extends Enum<C> & ListQueryColumn, Q> QuerydslQueryHooks<C, Q> noop() {
        return new QuerydslQueryHooks<>() {
        };
    }
}
