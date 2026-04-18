package com.example.servicea.controller;

import com.example.servicea.client.ServiceBClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class HelloController {

    private static final Logger log = LoggerFactory.getLogger(HelloController.class);

    private final RestTemplate restTemplate;
    private final ServiceBClient serviceBClient;

    public HelloController(RestTemplate restTemplate, ServiceBClient serviceBClient) {
        this.restTemplate = restTemplate;
        this.serviceBClient = serviceBClient;
    }

    // RestTemplate 방식 (Day 2에서 사용)
    @GetMapping("/hello")
    public String hello() {
        log.info(">>> Service-A: /hello (RestTemplate) 요청 받음");

        String response = restTemplate.getForObject(
            "http://localhost:8071/api/message",
            String.class
        );

        log.info(">>> Service-A: Service-B 응답 = {}", response);
        return "[RestTemplate] Service-A says: Hello! " + response;
    }

    // FeignClient 방식 (Day 3에서 추가)
    @GetMapping("/hello-feign")
    public String helloFeign() {
        log.info(">>> Service-A: /hello-feign (FeignClient) 요청 받음");

        String response = serviceBClient.getMessage();

        log.info(">>> Service-A: Service-B 응답 = {}", response);
        return "[FeignClient] Service-A says: Hello! " + response;
    }

    @GetMapping("/health")
    public String health() {
        return "Service-A is healthy!";
    }
}
