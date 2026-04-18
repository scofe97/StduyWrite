package com.example.serviceb.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ApiController {

    private static final Logger log = LoggerFactory.getLogger(ApiController.class);

    @GetMapping("/message")
    public String getMessage() {
        log.info(">>> Service-B: /api/message 요청 받음");

        // 비즈니스 로직 시뮬레이션 (50ms 딜레이)
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        log.info(">>> Service-B: 응답 반환");
        return "Greetings from Service-B!";
    }

    @GetMapping("/health")
    public String health() {
        return "Service-B is healthy!";
    }
}
