package com.runnershigh.modulith.runner.internal;

import com.runnershigh.modulith.runner.Runner;
import com.runnershigh.modulith.runner.RunnerLevel;
import com.runnershigh.modulith.runner.port.RunnerRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 인메모리 러너 저장소 - Repository Port 구현체
 *
 * <p>개발 및 테스트용 인메모리 구현입니다.
 * 프로덕션에서는 JPA 구현체로 교체할 수 있습니다.
 *
 * <p>internal 패키지에 위치하여 외부에서 직접 접근할 수 없습니다.
 */
@Repository
class InMemoryRunnerRepository implements RunnerRepository {

    private final Map<Long, Runner> storage = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    @Override
    public Runner save(Runner runner) {
        if (runner.getId() == null) {
            runner.setId(idGenerator.getAndIncrement());
        }
        storage.put(runner.getId(), runner);
        return runner;
    }

    @Override
    public Optional<Runner> findById(Long id) {
        return Optional.ofNullable(storage.get(id));
    }

    @Override
    public Optional<Runner> findByEmail(String email) {
        return storage.values().stream()
                .filter(runner -> runner.getEmail().equalsIgnoreCase(email))
                .findFirst();
    }

    @Override
    public boolean existsByEmail(String email) {
        return storage.values().stream()
                .anyMatch(runner -> runner.getEmail().equalsIgnoreCase(email));
    }

    @Override
    public List<Runner> findByLevel(RunnerLevel level) {
        return storage.values().stream()
                .filter(runner -> runner.getLevel() == level)
                .toList();
    }

    @Override
    public List<Runner> findAll() {
        return List.copyOf(storage.values());
    }

    // 테스트용 초기화 메서드
    void clear() {
        storage.clear();
        idGenerator.set(1);
    }
}
