package com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query;

import com.runnershigh.querydsl.support.listquery.common.query.ListQueryColumn;

public interface QueryColumnBindingRegistry<C extends Enum<C> & ListQueryColumn, Q> {

    QueryColumnBinding<Q> get(C column);
}
