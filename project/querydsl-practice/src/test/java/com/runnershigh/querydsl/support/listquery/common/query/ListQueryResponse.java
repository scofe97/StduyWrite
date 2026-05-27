package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.List;
import java.util.function.Function;

import lombok.Getter;

@Getter
public class ListQueryResponse<T> {

    private final int itemSize;
    private final int pageSize;
    private final int totalItemSize;
    private final List<T> data;

    private ListQueryResponse(int itemSize, int totalItemSize, List<T> data) {
        this.itemSize = itemSize;
        this.totalItemSize = totalItemSize;
        this.data = data;
        this.pageSize = calculatePageSize(itemSize, totalItemSize);
    }

    public static <T> ListQueryResponse<T> of(int itemSize, int totalItemSize, List<T> data) {
        return new ListQueryResponse<>(itemSize, totalItemSize, data);
    }

    public <R> ListQueryResponse<R> mapData(Function<T, R> mapper) {
        return ListQueryResponse.of(
            itemSize,
            totalItemSize,
            data.stream().map(mapper).toList()
        );
    }

    private static int calculatePageSize(int itemSize, int totalItemSize) {
        if (itemSize < 1) {
            return 0;
        }
        return (totalItemSize + itemSize - 1) / itemSize;
    }
}
