package com.study.redpanda.cqrs.config;

import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import lombok.experimental.UtilityClass;
import org.apache.avro.specific.SpecificRecord;

import java.util.Map;

/**
 * CQRS Kafka Streams 공통 Serde 팩토리
 *
 * PostsStreamTopology와 FollowsStreamTopology에서 동일한 Avro Serde 생성 로직이
 * 중복되어 있었다. 이 유틸리티 클래스로 추출하여 한 곳에서 관리한다.
 */
@UtilityClass
public class CqrsSerdeFactory {

    /**
     * Avro SpecificRecord 값 Serde 생성.
     *
     * specific.avro.reader=true로 설정하여 GenericRecord가 아닌
     * 생성된 구체 타입(PostCreated, PostLiked 등)으로 역직렬화한다.
     *
     * configure()의 isKey 파라미터는 Schema Registry subject 이름을 결정한다.
     * - isKey=false → subject suffix "-value" (예: topic-RecordName, value용)
     * - isKey=true  → subject suffix "-key"   (예: topic-RecordName, key용)
     * Schema Registry는 subject 단위로 호환성을 관리하므로 key/value subject가 분리되어야 한다.
     * 또한 isKey 값에 따라 Confluent 직렬화기가 읽는 설정 prefix도 달라진다:
     * - isKey=false → value.subject.name.strategy 등
     * - isKey=true  → key.subject.name.strategy 등
     *
     * 이 프로젝트에서는 key가 String(postId, followerId)이므로 Serdes.String()을 사용하고,
     * Avro Serde는 value 전용(isKey=false)으로만 생성한다.
     *
     * @param schemaRegistryUrl Schema Registry 주소
     * @return 구성 완료된 SpecificAvroSerde (value용)
     */
    public static <T extends SpecificRecord> SpecificAvroSerde<T> createAvroValueSerde(
            String schemaRegistryUrl) {
        SpecificAvroSerde<T> serde = new SpecificAvroSerde<>();
        serde.configure(
                Map.of(
                        "schema.registry.url", schemaRegistryUrl,
                        "specific.avro.reader", true
                ),
                false  // isKey=false → value serde (subject에 "-value" suffix 적용)
        );
        return serde;
    }
}
