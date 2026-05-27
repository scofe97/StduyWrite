package com.runnershigh.querydsl.support.listquery.common.query;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class ListQueryRequest {

    private Integer page;
    private Integer size;
    private ListSearchRequest searchObj;
    private ListSortRequest sortObj;
}
