# Kafka Performance 실습

## 시작

```bash
docker exec -it kafka1 /bin/bash
cd /labs/05-performance
```

## 실습 순서

| 스크립트 | 설명 |
|---------|------|
| `01-create-topic.sh` | 성능 테스트 토픽 생성 |
| `02-producer-perf-baseline.sh` | Producer 기본 성능 |
| `03-producer-perf-batch.sh` | 배치 최적화 |
| `04-producer-perf-compress.sh` | 압축 추가 |
| `05-consumer-perf.sh` | Consumer 기본 성능 |
| `06-consumer-perf-optimized.sh` | Consumer 최적화 |
| `07-compare-all.sh` | 전체 비교 |
| `08-cleanup.sh` | 정리 |

## 핵심 명령어

```bash
# Producer 성능 테스트
kafka-producer-perf-test \
    --topic TOPIC \
    --num-records 100000 \
    --record-size 1000 \
    --throughput -1 \
    --producer-props bootstrap.servers=kafka1:9092

# Consumer 성능 테스트
kafka-consumer-perf-test \
    --topic TOPIC \
    --messages 100000 \
    --bootstrap-server kafka1:9092
```

## 권장 설정

| 설정 | 권장값 | 효과 |
|------|--------|------|
| `batch.size` | 100KB~1MB | Throughput ↑ |
| `linger.ms` | 10ms | Throughput ↑ |
| `compression.type` | lz4/zstd | 네트워크/디스크 ↓ |
| `fetch.min.bytes` | 1MB | Consumer Throughput ↑ |
