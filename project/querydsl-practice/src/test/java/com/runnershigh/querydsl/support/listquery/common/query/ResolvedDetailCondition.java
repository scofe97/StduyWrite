package com.runnershigh.querydsl.support.listquery.common.query;

import java.time.LocalDateTime;
import java.util.List;

public record ResolvedDetailCondition<C extends Enum<C> & ListQueryColumn>(
    DetailConditionType type,
    C column,
    String value,
    List<String> valueList,
    LocalDateTime startDateTime,
    LocalDateTime endDateTime
) {
}
