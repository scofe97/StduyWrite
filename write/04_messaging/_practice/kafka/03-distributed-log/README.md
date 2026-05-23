# 03 - Distributed Log 실습

Kafka를 분산 로그로 이해하기 위한 실습입니다.

## 관련 이론

- [Chapter 4: Kafka as a Distributed Log](../../../docs/08_MessageQueue/Kafka/04_Kafka_as_a_Distributed_Log.md)

## 실습 환경

```bash
# 멀티 브로커 환경 시작 (상위 디렉토리에서)
cd /path/to/kafka-messaging
docker-compose -f docker-compose-multi.yml up -d

# 컨테이너 접속
docker exec -it kafka1 /bin/bash

# 실습 폴더 이동
cd /labs/03-distributed-log
chmod +x *.sh
```

## 실습 목차

| 스크립트 | 학습 내용 |
|----------|----------|
| `01-create-topics.sh` | 다양한 토픽 생성 |
| `02-key-partition-demo.sh` | Key 기반 파티셔닝, 순서 보장 |
| `03-consumer-group-demo.sh` | Consumer Group 동작 원리 |
| `04-offset-management.sh` | Offset 관리 및 리셋 |
| `05-replication-demo.sh` | 복제와 Leader-Follower 구조 |
| `06-cleanup.sh` | 실습 리소스 정리 |

## 핵심 개념

### 1. Offset
- 파티션 내 메시지의 고유 위치
- 0부터 시작, 메시지마다 1씩 증가
- `__consumer_offsets` 토픽에 저장

### 2. Key와 파티션
```
partition = hash(key) % partition_count
```
- Key 없음: Round-Robin 분배 → 순서 보장 안됨
- Key 있음: 같은 Key = 같은 파티션 → 순서 보장

### 3. Consumer Group
- 같은 Group: 파티션을 나눠서 소비 (부하 분산)
- 다른 Group: 독립적으로 모든 데이터 소비

### 4. 복제 (Replication)
- Leader: 모든 읽기/쓰기 담당
- Follower: Leader 데이터 복제, 대기
- ISR: 동기화된 복제본 목록

## 실습 순서

```bash
# 1. 토픽 생성
./01-create-topics.sh

# 2. Key 파티셔닝 확인
./02-key-partition-demo.sh

# 3. Consumer Group 테스트
./03-consumer-group-demo.sh

# 4. Offset 관리
./04-offset-management.sh

# 5. 복제 확인
./05-replication-demo.sh

# 6. 정리
./06-cleanup.sh
```

## 주요 명령어

```bash
# 토픽 목록
kafka-topics --list --bootstrap-server kafka1:9092

# 토픽 상세
kafka-topics --describe --topic <topic> --bootstrap-server kafka1:9092

# Consumer Group 상태
kafka-consumer-groups --describe --group <group> --bootstrap-server kafka1:9092

# Offset 리셋
kafka-consumer-groups --reset-offsets \
    --group <group> \
    --topic <topic> \
    --to-earliest \
    --execute \
    --bootstrap-server kafka1:9092
```
