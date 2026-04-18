package com.runnershigh.tps.infrastructure.util;

import com.fasterxml.uuid.Generators;
import com.fasterxml.uuid.impl.TimeBasedEpochGenerator;

import java.util.UUID;

/**
 * UUID v7 생성 유틸리티
 *
 * <p>UUID v7은 시간 기반 순차 UUID로, B-Tree 인덱스 성능을 크게 향상시킵니다.</p>
 *
 * <h2>UUID v7 구조 (RFC 9562)</h2>
 * <pre>
 * |  unix_ts_ms (48bit)  | ver | rand_a | var | rand_b |
 * |<----- 시간순 정렬 ----->|
 *
 * 예: 018d5e90-1234-7abc-8def-0123456789ab
 *     ^^^^^^^^
 *     Unix timestamp (밀리초)
 * </pre>
 *
 * <h2>성능 이점</h2>
 * <ul>
 *   <li><strong>B-Tree 인덱스</strong>: 항상 끝에 삽입 → 페이지 분할 없음</li>
 *   <li><strong>INSERT 성능</strong>: UUID v4 대비 약 3-4배 향상</li>
 *   <li><strong>시간 범위 쿼리</strong>: id 자체로 시간 필터링 가능</li>
 *   <li><strong>정렬 효율</strong>: 자연스러운 시간순 정렬</li>
 * </ul>
 *
 * <h2>UUID v4 vs UUID v7 비교</h2>
 * <pre>
 * UUID v4 (랜덤):
 *   - 122비트 랜덤
 *   - 정렬 불가능
 *   - 인덱스 삽입 시 랜덤 위치 → 페이지 분할 빈번
 *
 * UUID v7 (순차):
 *   - 48비트 타임스탬프 + 74비트 랜덤
 *   - 시간순 정렬 가능
 *   - 인덱스 삽입 시 항상 끝 → 페이지 분할 없음
 * </pre>
 *
 * <h2>Thread Safety</h2>
 * <p>내부 생성기는 thread-safe하며, 동일 밀리초 내에서도
 * monotonic(단조 증가) 순서를 보장합니다.</p>
 *
 * @see <a href="https://www.rfc-editor.org/rfc/rfc9562">RFC 9562 - UUIDs</a>
 * @see <a href="https://github.com/cowtowncoder/java-uuid-generator">java-uuid-generator</a>
 */
public final class UuidGenerator {

    /**
     * Thread-safe UUID v7 생성기 (싱글톤)
     *
     * <p>TimeBasedEpochGenerator는 UUID v7(RFC 9562)을 생성합니다.
     * 밀리초 내에서도 monotonic 순서를 보장합니다.</p>
     */
    private static final TimeBasedEpochGenerator GENERATOR =
            Generators.timeBasedEpochGenerator();

    private UuidGenerator() {
        // 유틸리티 클래스 - 인스턴스화 방지
    }

    /**
     * UUID v7 생성
     *
     * <p>시간 기반 순차 UUID를 생성합니다.
     * 생성된 UUID는 시간순으로 자연스럽게 정렬됩니다.</p>
     *
     * <h3>사용 예시</h3>
     * <pre>{@code
     * UUID id = UuidGenerator.generate();
     * // 018d5e90-1234-7abc-8def-0123456789ab
     * }</pre>
     *
     * @return 시간 기반 순차 UUID (version 7)
     */
    public static UUID generate() {
        return GENERATOR.generate();
    }

    /**
     * UUID v7에서 생성 시간 추출
     *
     * <p>UUID v7의 상위 48비트에서 Unix 타임스탬프(밀리초)를 추출합니다.</p>
     *
     * <h3>사용 예시</h3>
     * <pre>{@code
     * UUID uuid = UuidGenerator.generate();
     * long timestamp = UuidGenerator.extractTimestamp(uuid);
     * Instant created = Instant.ofEpochMilli(timestamp);
     * }</pre>
     *
     * <h3>활용</h3>
     * <ul>
     *   <li>엔티티 생성 시간 확인 (createdAt 없이도 가능)</li>
     *   <li>시간 범위 쿼리 최적화</li>
     *   <li>디버깅 및 감사 로그</li>
     * </ul>
     *
     * @param uuid UUID v7
     * @return Unix timestamp (밀리초)
     * @throws IllegalArgumentException uuid가 null인 경우
     */
    public static long extractTimestamp(UUID uuid) {
        if (uuid == null) {
            throw new IllegalArgumentException("UUID must not be null");
        }
        // UUID v7: 상위 48비트가 Unix 타임스탬프 (밀리초)
        return uuid.getMostSignificantBits() >>> 16;
    }

    /**
     * UUID가 v7 형식인지 확인
     *
     * @param uuid 확인할 UUID
     * @return UUID v7이면 true
     */
    public static boolean isVersion7(UUID uuid) {
        return uuid != null && uuid.version() == 7;
    }
}
