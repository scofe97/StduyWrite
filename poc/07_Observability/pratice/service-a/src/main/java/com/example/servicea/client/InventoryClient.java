package com.example.servicea.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.Map;

@FeignClient(name = "inventory-service", url = "http://localhost:8071")
public interface InventoryClient {

    @GetMapping("/api/inventory/{productId}")
    Map<String, Object> checkInventory(@PathVariable("productId") String productId);
}
