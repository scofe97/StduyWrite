# Stage 02: Topics and Messages

Kafka 토픽과 메시지 구조 심화 학습

## 학습 내용

- 메시지 구조 (Timestamp, Key, Value, Headers)
- 데이터 포맷 (JSON, Avro, Protobuf)
- 메시지 타입 (States, Deltas, Events, Commands)
- Key 기반 파티셔닝과 순서 보장

## 관련 이론

- [Chapter 3: Exploring Kafka Topics and Messages](../../../docs/08_MessageQueue/Kafka/03_Exploring_Kafka_Topics_and_Messages.md)

## 실습 환경

```bash
# Key가 있는 메시지 생산
kafka-console-producer \
    --topic products.prices.changelog \
    --property "parse.key=true" \
    --property "key.separator=:" \
    --bootstrap-server localhost:9092

# Key와 Value 함께 소비
kafka-console-consumer \
    --topic products.prices.changelog \
    --from-beginning \
    --property "print.key=true" \
    --property "key.separator=:" \
    --bootstrap-server localhost:9092
```

## 다음 단계

- [03-distributed-log](../03-distributed-log/): 분산 로그와 복제
