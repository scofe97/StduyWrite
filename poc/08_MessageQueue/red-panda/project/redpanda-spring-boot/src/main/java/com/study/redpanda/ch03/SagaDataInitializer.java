package com.study.redpanda.ch03;

import com.study.redpanda.ch03.domain.Inventory;
import com.study.redpanda.ch03.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@RequiredArgsConstructor
@Slf4j
public class SagaDataInitializer implements CommandLineRunner {

    private final InventoryRepository inventoryRepository;

    @Override
    @Transactional
    public void run(String... args) {
        if (inventoryRepository.count() > 0) {
            log.info("Ch03 SAGA: Inventory data already exists, skipping initialization");
            return;
        }

        inventoryRepository.save(Inventory.builder()
                .productId("PROD-001").availableQuantity(100).reservedQuantity(0).build());
        inventoryRepository.save(Inventory.builder()
                .productId("PROD-002").availableQuantity(50).reservedQuantity(0).build());
        inventoryRepository.save(Inventory.builder()
                .productId("PROD-003").availableQuantity(200).reservedQuantity(0).build());

        log.info("Ch03 SAGA: Initialized inventory data (3 products)");
    }
}
