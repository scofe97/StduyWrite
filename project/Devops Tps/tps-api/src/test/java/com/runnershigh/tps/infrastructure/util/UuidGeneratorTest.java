package com.runnershigh.tps.infrastructure.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CopyOnWriteArrayList;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * UUID v7 생성기 테스트
 *
 * <p>테스트 범위:</p>
 * <ul>
 *   <li>UUID 버전 검증 (v7)</li>
 *   <li>순차성(monotonic) 검증</li>
 *   <li>유니크성 검증</li>
 *   <li>타임스탬프 추출 검증</li>
 *   <li>멀티스레드 안전성 검증</li>
 * </ul>
 */
class UuidGeneratorTest {

    @Nested
    @DisplayName("generate() 메서드")
    class GenerateTests {

        @Test
        @DisplayName("UUID v7 생성 - 버전이 7이어야 함")
        void generate_shouldReturnUuidVersion7() {
            // given & when
            UUID uuid = UuidGenerator.generate();

            // then
            assertThat(uuid.version()).isEqualTo(7);
        }

        @Test
        @DisplayName("UUID v7 생성 - variant가 RFC 4122 형식이어야 함")
        void generate_shouldReturnRfc4122Variant() {
            // given & when
            UUID uuid = UuidGenerator.generate();

            // then
            // variant == 2는 RFC 4122 표준을 의미
            assertThat(uuid.variant()).isEqualTo(2);
        }

        @RepeatedTest(10)
        @DisplayName("UUID v7 생성 - 순차적으로 증가해야 함 (monotonic)")
        void generate_shouldBeMonotonicallyIncreasing() {
            // given
            List<UUID> uuids = new ArrayList<>();

            // when - 100개의 UUID 연속 생성
            for (int i = 0; i < 100; i++) {
                uuids.add(UuidGenerator.generate());
            }

            // then - 모든 UUID가 이전 것보다 커야 함
            for (int i = 1; i < uuids.size(); i++) {
                UUID current = uuids.get(i);
                UUID previous = uuids.get(i - 1);

                assertThat(current.compareTo(previous))
                        .as("UUID[%d] should be greater than UUID[%d]", i, i - 1)
                        .isGreaterThan(0);
            }
        }

        @Test
        @DisplayName("UUID v7 생성 - 모든 UUID가 유니크해야 함")
        void generate_shouldBeUnique() {
            // given
            int count = 10000;
            List<UUID> uuids = new ArrayList<>(count);

            // when
            for (int i = 0; i < count; i++) {
                uuids.add(UuidGenerator.generate());
            }

            // then
            long uniqueCount = uuids.stream().distinct().count();
            assertThat(uniqueCount).isEqualTo(count);
        }

        @Test
        @DisplayName("UUID v7 생성 - 멀티스레드 환경에서도 유니크해야 함")
        void generate_shouldBeUniqueInMultiThreadedEnvironment() throws InterruptedException {
            // given
            int threadCount = 10;
            int uuidsPerThread = 1000;
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            CountDownLatch latch = new CountDownLatch(threadCount);
            List<UUID> allUuids = new CopyOnWriteArrayList<>();

            // when
            for (int i = 0; i < threadCount; i++) {
                executor.submit(() -> {
                    try {
                        for (int j = 0; j < uuidsPerThread; j++) {
                            allUuids.add(UuidGenerator.generate());
                        }
                    } finally {
                        latch.countDown();
                    }
                });
            }

            latch.await();
            executor.shutdown();

            // then
            int expectedTotal = threadCount * uuidsPerThread;
            assertThat(allUuids).hasSize(expectedTotal);

            long uniqueCount = allUuids.stream().distinct().count();
            assertThat(uniqueCount).isEqualTo(expectedTotal);
        }
    }

    @Nested
    @DisplayName("extractTimestamp() 메서드")
    class ExtractTimestampTests {

        @Test
        @DisplayName("타임스탬프 추출 - 현재 시간과 일치해야 함")
        void extractTimestamp_shouldReturnValidTimestamp() {
            // given
            long before = System.currentTimeMillis();
            UUID uuid = UuidGenerator.generate();
            long after = System.currentTimeMillis();

            // when
            long extracted = UuidGenerator.extractTimestamp(uuid);

            // then
            assertThat(extracted).isBetween(before, after);
        }

        @Test
        @DisplayName("타임스탬프 추출 - null UUID는 예외 발생")
        void extractTimestamp_shouldThrowExceptionForNull() {
            // given & when & then
            assertThatThrownBy(() -> UuidGenerator.extractTimestamp(null))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessage("UUID must not be null");
        }

        @Test
        @DisplayName("타임스탬프 추출 - 순서대로 생성된 UUID는 타임스탬프도 순서대로")
        void extractTimestamp_shouldBeOrderedForSequentialUuids() throws InterruptedException {
            // given
            UUID uuid1 = UuidGenerator.generate();
            Thread.sleep(10); // 10ms 대기
            UUID uuid2 = UuidGenerator.generate();

            // when
            long timestamp1 = UuidGenerator.extractTimestamp(uuid1);
            long timestamp2 = UuidGenerator.extractTimestamp(uuid2);

            // then
            assertThat(timestamp2).isGreaterThan(timestamp1);
        }
    }

    @Nested
    @DisplayName("isVersion7() 메서드")
    class IsVersion7Tests {

        @Test
        @DisplayName("UUID v7 확인 - v7이면 true")
        void isVersion7_shouldReturnTrueForV7() {
            // given
            UUID uuidV7 = UuidGenerator.generate();

            // when
            boolean result = UuidGenerator.isVersion7(uuidV7);

            // then
            assertThat(result).isTrue();
        }

        @Test
        @DisplayName("UUID v7 확인 - v4이면 false")
        void isVersion7_shouldReturnFalseForV4() {
            // given
            UUID uuidV4 = UUID.randomUUID();

            // when
            boolean result = UuidGenerator.isVersion7(uuidV4);

            // then
            assertThat(result).isFalse();
        }

        @Test
        @DisplayName("UUID v7 확인 - null이면 false")
        void isVersion7_shouldReturnFalseForNull() {
            // given & when
            boolean result = UuidGenerator.isVersion7(null);

            // then
            assertThat(result).isFalse();
        }
    }

    @Nested
    @DisplayName("성능 특성")
    class PerformanceTests {

        @Test
        @DisplayName("대량 생성 시 B-Tree 친화적 순서 유지")
        void generate_shouldMaintainBTreeFriendlyOrder() {
            // given
            List<UUID> uuids = new ArrayList<>();

            // when - 1000개 생성
            for (int i = 0; i < 1000; i++) {
                uuids.add(UuidGenerator.generate());
            }

            // then - 정렬 없이도 이미 정렬되어 있어야 함
            List<UUID> sorted = new ArrayList<>(uuids);
            sorted.sort(UUID::compareTo);

            assertThat(uuids).isEqualTo(sorted);
        }

        @Test
        @DisplayName("UUID v7은 시간 범위 쿼리에 활용 가능")
        void generate_shouldSupportTimeRangeQueries() throws InterruptedException {
            // given - 시작 시간 기록
            long queryStart = System.currentTimeMillis();
            Thread.sleep(5);

            // 일부 UUID 생성
            List<UUID> targetUuids = new ArrayList<>();
            for (int i = 0; i < 10; i++) {
                targetUuids.add(UuidGenerator.generate());
            }

            Thread.sleep(5);
            long queryEnd = System.currentTimeMillis();

            // when - 생성된 UUID의 타임스탬프 확인
            for (UUID uuid : targetUuids) {
                long timestamp = UuidGenerator.extractTimestamp(uuid);

                // then - 모든 UUID가 쿼리 범위 내에 있어야 함
                assertThat(timestamp).isBetween(queryStart, queryEnd);
            }
        }
    }
}
