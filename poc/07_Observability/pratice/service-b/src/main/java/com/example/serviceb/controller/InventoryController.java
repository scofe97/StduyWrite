package com.example.serviceb.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/api/inventory")
public class InventoryController {

    private static final Logger log = LoggerFactory.getLogger(InventoryController.class);

    // 간단한 인메모리 재고 저장소
    private final Map<String, Integer> inventory = new ConcurrentHashMap<>();

    public InventoryController() {
        // 초기 재고 설정
        inventory.put("PROD-001", 100);
        inventory.put("PROD-002", 50);
        inventory.put("PROD-003", 0);  // 품절 상품
    }

    @GetMapping("/{productId}")
    public Map<String, Object> checkInventory(@PathVariable String productId) {
        log.info(">>> [INVENTORY] 재고 확인 요청: productId={}", productId);

        // DB 조회 시뮬레이션
        try {
            Thread.sleep(30);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        int stock = inventory.getOrDefault(productId, 0);
        boolean available = stock > 0;

        log.info(">>> [INVENTORY] 재고 확인 결과: productId={}, stock={}, available={}",
                productId, stock, available);

        return Map.of(
            "productId", productId,
            "stock", stock,
            "available", available
        );
    }
}
