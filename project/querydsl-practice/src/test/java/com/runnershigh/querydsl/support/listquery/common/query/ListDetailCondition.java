package com.runnershigh.querydsl.support.listquery.common.query;

import java.util.List;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class ListDetailCondition {

    private String type;
    private String column;
    private String value;
    private List<String> valueList;
    private String startDate;
    private String endDate;
}
