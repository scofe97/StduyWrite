package com.runnershigh.querydsl.config;

import net.ttddyy.dsproxy.ExecutionInfo;
import net.ttddyy.dsproxy.QueryInfo;
import net.ttddyy.dsproxy.listener.QueryExecutionListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;
import java.util.regex.Pattern;

@Configuration
public class DataSourceProxyConfig {

    private static final Logger log = LoggerFactory.getLogger("SQL");

    private static final Pattern DDL = Pattern.compile(
            "^\\s*(drop|create|alter|truncate)\\b",
            Pattern.CASE_INSENSITIVE
    );

    private static final Pattern KEYWORDS = Pattern.compile(
            "\\b(select|from|where|join|on|order\\s+by|group\\s+by|having"
            + "|insert\\s+into|update|delete|set|values|and|or|not|in|like|as"
            + "|left|right|inner|outer|cross|full|fetch|distinct|union|all"
            + "|case|when|then|else|end|exists|between|is|null|asc|desc"
            + "|limit|offset|with|next|value|for)\\b",
            Pattern.CASE_INSENSITIVE
    );

    @Bean
    public QueryExecutionListener uppercaseSqlListener() {
        return new QueryExecutionListener() {
            @Override
            public void beforeQuery(ExecutionInfo execInfo, List<QueryInfo> queryInfoList) {
            }

            @Override
            public void afterQuery(ExecutionInfo execInfo, List<QueryInfo> queryInfoList) {
                for (QueryInfo qi : queryInfoList) {
                    String raw = qi.getQuery();
                    if (raw == null || raw.isBlank()) {
                        continue;
                    }
                    String compact = raw.replaceAll("\\s+", " ").trim();
                    if (DDL.matcher(compact).find()) {
                        continue;
                    }
                    String upper = KEYWORDS.matcher(compact).replaceAll(m -> m.group().toUpperCase());
                    Integer rows = execInfo.getResult() instanceof Integer i ? i : null;
                    if (rows != null && rows >= 0) {
                        log.info("[{}ms, {} rows] {}", execInfo.getElapsedTime(), rows, upper);
                    } else {
                        log.info("[{}ms] {}", execInfo.getElapsedTime(), upper);
                    }
                }
            }
        };
    }
}
