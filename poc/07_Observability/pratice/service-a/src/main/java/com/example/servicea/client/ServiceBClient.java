package com.example.servicea.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient(name = "service-b", url = "http://localhost:8071")
public interface ServiceBClient {

    @GetMapping("/api/message")
    String getMessage();
}
