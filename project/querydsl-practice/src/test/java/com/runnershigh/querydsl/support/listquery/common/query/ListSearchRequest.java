package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.List;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class ListSearchRequest {

    private String searchValue;
    private String column;
    private List<ListDetailCondition> detail;
}
