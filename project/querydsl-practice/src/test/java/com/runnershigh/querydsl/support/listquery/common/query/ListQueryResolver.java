package com.runnershigh.querydsl.support.listquery.common.query;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import com.runnershigh.querydsl.support.listquery.common.exception.InvalidListQueryException;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class ListQueryResolver {

    private static final String SEARCH_MODE_ALL = "ALL";
    private static final String SEARCH_MODE_DETAIL = "DTL";

    public <C extends Enum<C> & ListQueryColumn> ResolvedListQuery<C> resolve(
        ListQueryRequest request,
        ListQueryPolicy<C> policy
    ) {
        ListQueryRequest actualRequest = request == null ? new ListQueryRequest() : request;

        int page = resolvePage(actualRequest.getPage());
        int size = resolveSize(actualRequest.getSize(), policy.getDefaultPageSize());
        long offset = (long) (page - 1) * size;

        return new ResolvedListQuery<>(
            page,
            size,
            size,
            offset,
            resolveSearchCondition(actualRequest.getSearchObj(), policy),
            resolveSortCondition(actualRequest.getSortObj(), policy)
        );
    }

    private int resolvePage(Integer page) {
        if (page == null || page < 1) {
            return 1;
        }
        return page;
    }

    private int resolveSize(Integer size, int defaultSize) {
        if (size == null || size < 1) {
            return defaultSize;
        }
        return size;
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedSearchCondition<C> resolveSearchCondition(
        ListSearchRequest searchRequest,
        ListQueryPolicy<C> policy
    ) {
        if (searchRequest == null) {
            return null;
        }

        String columnName = trimToNull(searchRequest.getColumn());
        if (columnName == null) {
            if (!hasSearchInput(searchRequest)) {
                return null;
            }
            throw new InvalidListQueryException("Search mode is required");
        }

        if (SEARCH_MODE_ALL.equals(columnName)) {
            return resolveAllSearchCondition(searchRequest, policy);
        }

        if (SEARCH_MODE_DETAIL.equals(columnName)) {
            return resolveDetailSearchCondition(searchRequest, policy);
        }

        throw new InvalidListQueryException("Unsupported search mode: " + columnName);
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedSearchCondition<C> resolveAllSearchCondition(
        ListSearchRequest searchRequest,
        ListQueryPolicy<C> policy
    ) {
        String keyword = trimToNull(searchRequest.getSearchValue());
        if (keyword == null) {
            return null;
        }

        if (policy.getGlobalSearchColumns().isEmpty()) {
            throw new InvalidListQueryException("Global search columns are not configured");
        }

        return new ResolvedSearchCondition<>(keyword, true, null, Collections.emptyList());
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedSearchCondition<C> resolveDetailSearchCondition(
        ListSearchRequest searchRequest,
        ListQueryPolicy<C> policy
    ) {
        List<ResolvedDetailCondition<C>> detailConditions = resolveDetailConditions(searchRequest.getDetail(), policy);
        if (detailConditions.isEmpty()) {
            return null;
        }

        return new ResolvedSearchCondition<>(null, false, null, detailConditions);
    }

    private boolean hasSearchInput(ListSearchRequest searchRequest) {
        if (trimToNull(searchRequest.getSearchValue()) != null) {
            return true;
        }

        if (searchRequest.getDetail() == null || searchRequest.getDetail().isEmpty()) {
            return false;
        }

        for (ListDetailCondition detailCondition : searchRequest.getDetail()) {
            if (hasDetailSearchInput(detailCondition)) {
                return true;
            }
        }

        return false;
    }

    private boolean hasDetailSearchInput(ListDetailCondition detailCondition) {
        if (detailCondition == null) {
            return false;
        }

        if (trimToNull(detailCondition.getValue()) != null
            || trimToNull(detailCondition.getStartDate()) != null
            || trimToNull(detailCondition.getEndDate()) != null) {
            return true;
        }

        if (detailCondition.getValueList() == null) {
            return false;
        }

        return detailCondition.getValueList().stream()
            .map(this::trimToNull)
            .anyMatch(StringUtils::hasText);
    }

    private <C extends Enum<C> & ListQueryColumn> List<ResolvedDetailCondition<C>> resolveDetailConditions(
        List<ListDetailCondition> detailConditions,
        ListQueryPolicy<C> policy
    ) {
        if (detailConditions == null || detailConditions.isEmpty()) {
            return Collections.emptyList();
        }

        List<ResolvedDetailCondition<C>> resolvedConditions = new ArrayList<>();

        for (ListDetailCondition detailCondition : detailConditions) {
            if (detailCondition == null) {
                continue;
            }

            String columnName = trimToNull(detailCondition.getColumn());
            if (columnName == null) {
                throw new InvalidListQueryException("Detail condition column is required");
            }

            C column = policy.requireColumn(columnName, "Unsupported detail condition column");
            DetailConditionType conditionType = DetailConditionType.from(trimToNull(detailCondition.getType()));
            Set<DetailConditionType> allowedTypes = policy.getAllowedDetailConditionTypes()
                .getOrDefault(column, Collections.emptySet());

            if (!allowedTypes.contains(conditionType)) {
                throw new InvalidListQueryException(
                    "Detail condition type %s is not allowed for column %s".formatted(conditionType, columnName)
                );
            }

            ResolvedDetailCondition<C> resolvedCondition = resolveDetailCondition(detailCondition, column, conditionType);
            if (resolvedCondition != null) {
                resolvedConditions.add(resolvedCondition);
            }
        }

        return resolvedConditions;
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedDetailCondition<C> resolveDetailCondition(
        ListDetailCondition detailCondition,
        C column,
        DetailConditionType conditionType
    ) {
        return switch (conditionType) {
            case T -> resolveTextCondition(detailCondition, column, conditionType);
            case S, R, G -> resolveMultiValueCondition(detailCondition, column, conditionType);
            case D -> resolveDateCondition(detailCondition, column, conditionType);
        };
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedDetailCondition<C> resolveTextCondition(
        ListDetailCondition detailCondition,
        C column,
        DetailConditionType conditionType
    ) {
        String value = trimToNull(detailCondition.getValue());
        if (value == null) {
            return null;
        }

        return new ResolvedDetailCondition<>(
            conditionType,
            column,
            value,
            Collections.emptyList(),
            null,
            null
        );
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedDetailCondition<C> resolveMultiValueCondition(
        ListDetailCondition detailCondition,
        C column,
        DetailConditionType conditionType
    ) {
        List<String> valueList = detailCondition.getValueList() == null
            ? Collections.emptyList()
            : detailCondition.getValueList().stream()
                .map(this::trimToNull)
                .filter(StringUtils::hasText)
                .toList();

        if (valueList.isEmpty()) {
            return null;
        }

        return new ResolvedDetailCondition<>(
            conditionType,
            column,
            null,
            valueList,
            null,
            null
        );
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedDetailCondition<C> resolveDateCondition(
        ListDetailCondition detailCondition,
        C column,
        DetailConditionType conditionType
    ) {
        LocalDate startDate = parseDate(detailCondition.getStartDate(), "startDate");
        LocalDate endDate = parseDate(detailCondition.getEndDate(), "endDate");

        if (startDate == null && endDate == null) {
            return null;
        }

        if (startDate != null && endDate != null && endDate.isBefore(startDate)) {
            throw new InvalidListQueryException("endDate must not be before startDate");
        }

        return new ResolvedDetailCondition<>(
            conditionType,
            column,
            null,
            Collections.emptyList(),
            startDate == null ? null : startDate.atStartOfDay(),
            endDate == null ? null : LocalDateTime.of(endDate, LocalTime.of(23, 59, 59))
        );
    }

    private <C extends Enum<C> & ListQueryColumn> ResolvedSortCondition<C> resolveSortCondition(
        ListSortRequest sortRequest,
        ListQueryPolicy<C> policy
    ) {
        String columnName = sortRequest == null ? null : trimToNull(sortRequest.getColumn());

        if (sortRequest == null
            || columnName == null
            || sortRequest.getDirection() == null) {
            return new ResolvedSortCondition<>(policy.getDefaultSortColumn(), policy.getDefaultSortDirection());
        }

        C column = policy.requireColumn(columnName, "Unsupported sort column");
        if (!policy.getSortableColumns().contains(column)) {
            throw new InvalidListQueryException("Sorting is not allowed for column: " + columnName);
        }

        return new ResolvedSortCondition<>(column, sortRequest.getDirection());
    }

    private String trimToNull(String value) {
        if (!StringUtils.hasText(value)) {
            return null;
        }
        return value.trim();
    }

    private LocalDate parseDate(String value, String fieldName) {
        String trimmedValue = trimToNull(value);
        if (trimmedValue == null) {
            return null;
        }

        try {
            return LocalDate.parse(trimmedValue);
        } catch (DateTimeParseException exception) {
            throw new InvalidListQueryException("Invalid date format for %s: %s".formatted(fieldName, trimmedValue));
        }
    }
}
