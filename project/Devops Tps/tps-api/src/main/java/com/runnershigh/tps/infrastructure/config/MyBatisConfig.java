package com.runnershigh.tps.infrastructure.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("com.runnershigh.tps.adapter.out.persistence")
public class MyBatisConfig {
}
