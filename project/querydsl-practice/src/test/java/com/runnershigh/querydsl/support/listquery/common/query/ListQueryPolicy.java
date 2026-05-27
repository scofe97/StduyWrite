package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.Arrays;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

import com.runnershigh.querydsl.support.listquery.common.exception.InvalidListQueryException;

public interface ListQueryPolicy<C extends Enum<C> & ListQueryColumn> {

    Class<C> getColumnType();

    Set<C> getGlobalSearchColumns();

    Map<C, Set<DetailConditionType>> getAllowedDetailConditionTypes();

    Set<C> getSortableColumns();

    C getDefaultSortColumn();

    SortDirection getDefaultSortDirection();

    default int getDefaultPageSize() {
        return 15;
    }

    @Deprecated(since = "2026-04-28")
    default Set<C> getKeywordSearchColumns() {
        return getGlobalSearchColumns();
    }

    default C getTieBreakerSortColumn() {
        return null;
    }

    default SortDirection getTieBreakerSortDirection() {
        return SortDirection.DESC;
    }

    default C resolveColumn(String inputName) {
        return getColumnMap().get(inputName);
    }

    private Map<String, C> getColumnMap() {
        return Arrays.stream(getColumnType().getEnumConstants())
            .collect(Collectors.toMap(ListQueryColumn::getInputName, Function.identity()));
    }

    default C requireColumn(String inputName, String messagePrefix) {
        C column = resolveColumn(inputName);
        if (column == null) {
            throw new InvalidListQueryException(messagePrefix + ": " + inputName);
        }
        return column;
    }
}
