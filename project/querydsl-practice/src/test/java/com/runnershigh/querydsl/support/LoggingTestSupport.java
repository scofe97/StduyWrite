package com.runnershigh.querydsl.support;

import com.runnershigh.querydsl.config.DataSourceProxyConfig;
import com.runnershigh.querydsl.config.DbInfoPrinter;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Import;

@TestConfiguration
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import({DataSourceProxyConfig.class, DbInfoPrinter.class})
public class LoggingTestSupport {
}
