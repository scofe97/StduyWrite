package com.runnershigh.querydsl.support.listquery.common.query;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@NoArgsConstructor
public class ListSortRequest {

    @Setter
    private String column;
    private SortDirection direction;

    public void setDirection(Object direction) {
        if (direction == null) {
            this.direction = null;
            return;
        }

        if (direction instanceof SortDirection sortDirection) {
            this.direction = sortDirection;
            return;
        }

        if (direction instanceof String directionValue) {
            this.direction = SortDirection.from(directionValue);
            return;
        }

        throw new IllegalArgumentException("Unsupported sort direction type: " + direction.getClass().getName());
    }
}
