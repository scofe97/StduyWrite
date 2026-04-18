# Redis Streams 상세 가이드

## 1. 개요

Redis Streams는 **Redis 5.0 (2018)**에 도입된 데이터 구조로, Apache Kafka와 유사한 **로그 기반 메시지 스트리밍**을 제공한다.

### 1.1 핵심 특징

| 특징 | 설명 |
|------|------|
| **메시지 영속성** | 메시지가 명시적으로 삭제될 때까지 보존 |
| **Consumer Group** | 여러 Consumer가 분산 처리 |
| **메시지 ID** | 자동 생성되는 고유 ID (타임스탬프 기반) |
| **ACK 메커니즘** | 메시지 처리 확인 가능 |
| **재처리** | 특정 위치부터 다시 읽기 가능 |

### 1.2 Pub/Sub vs Streams

| 항목 | Pub/Sub | Streams |
|------|---------|---------|
| **메시지 보존** | 없음 (Fire-and-Forget) | 있음 (TTL까지) |
| **재처리** | 불가능 | 가능 |
| **Consumer Group** | 없음 | 있음 |
| **ACK** | 없음 | 있음 |
| **순서 보장** | 보장 안됨 | 보장됨 |
| **지연시간** | ~0.1ms | ~0.15ms |

---

## 2. 기본 구조

### 2.1 Stream 데이터 구조

```
Stream: mystream
┌──────────────────────────────────────────────────────────────┐
│ Entry ID          │ Fields                                   │
├──────────────────────────────────────────────────────────────┤
│ 1526569495631-0   │ {"sensor_id": "1234", "temp": "19.8"}    │
│ 1526569495631-1   │ {"sensor_id": "1234", "temp": "20.1"}    │
│ 1526569495632-0   │ {"sensor_id": "5678", "temp": "21.5"}    │
└──────────────────────────────────────────────────────────────┘
         ↑
    타임스탬프-시퀀스
```

### 2.2 Entry ID 형식

```
<millisecondsTime>-<sequenceNumber>

예: 1526569495631-0
    └─────┬─────┘ └┬┘
    Unix 밀리초   시퀀스 번호 (같은 밀리초 내 순서)
```

---

## 3. 핵심 명령어

### 3.1 메시지 추가 (XADD)

```redis
# 자동 ID 생성
XADD mystream * sensor_id 1234 temperature 19.8

# 수동 ID 지정
XADD mystream 1526569495631-0 sensor_id 1234 temperature 19.8

# 최대 길이 제한 (약 1000개 유지)
XADD mystream MAXLEN ~ 1000 * sensor_id 1234 temperature 19.8
```

### 3.2 메시지 읽기 (XREAD)

```redis
# 특정 ID 이후 메시지 읽기
XREAD STREAMS mystream 1526569495631-0

# 새 메시지만 읽기 ($ = 최신)
XREAD STREAMS mystream $

# 블로킹 읽기 (최대 5초 대기)
XREAD BLOCK 5000 STREAMS mystream $

# 여러 Stream 동시 읽기
XREAD STREAMS stream1 stream2 0 0
```

### 3.3 범위 읽기 (XRANGE / XREVRANGE)

```redis
# 전체 범위
XRANGE mystream - +

# 특정 범위
XRANGE mystream 1526569495631-0 1526569495632-0

# 최신 10개
XREVRANGE mystream + - COUNT 10
```

### 3.4 메시지 삭제 (XDEL / XTRIM)

```redis
# 특정 메시지 삭제
XDEL mystream 1526569495631-0

# 길이 제한 (정확히 1000개)
XTRIM mystream MAXLEN 1000

# 길이 제한 (약 1000개, 효율적)
XTRIM mystream MAXLEN ~ 1000

# 특정 ID 이전 삭제
XTRIM mystream MINID 1526569495631-0
```

---

## 4. Consumer Group

### 4.1 Consumer Group이란?

Consumer Group은 **여러 Consumer가 하나의 Stream을 분산 처리**할 수 있게 해주는 기능이다.

```
                    ┌── Consumer A (메시지 1, 3, 5)
Stream ──► Group ──┼── Consumer B (메시지 2, 4, 6)
                    └── Consumer C (메시지 7, 8, 9)
```

### 4.2 핵심 개념

| 개념 | 설명 |
|------|------|
| **Consumer Group** | 논리적 Consumer 집합 |
| **Consumer** | Group 내 개별 처리자 |
| **PEL** | Pending Entries List (처리 중인 메시지 목록) |
| **Last Delivered ID** | 그룹에 마지막으로 전달된 메시지 ID |

### 4.3 Consumer Group 생성

```redis
# Stream 시작부터 읽기
XGROUP CREATE mystream mygroup 0 MKSTREAM

# 새 메시지만 읽기
XGROUP CREATE mystream mygroup $ MKSTREAM

# 그룹 삭제
XGROUP DESTROY mystream mygroup
```

### 4.4 그룹에서 메시지 읽기 (XREADGROUP)

```redis
# 새 메시지 읽기 (> = 아직 전달 안된 메시지)
XREADGROUP GROUP mygroup consumer1 STREAMS mystream >

# 블로킹 읽기
XREADGROUP GROUP mygroup consumer1 BLOCK 5000 STREAMS mystream >

# 배치 읽기 (최대 10개)
XREADGROUP GROUP mygroup consumer1 COUNT 10 STREAMS mystream >

# 처리 중인 내 메시지 다시 읽기
XREADGROUP GROUP mygroup consumer1 STREAMS mystream 0
```

### 4.5 메시지 확인 (XACK)

```redis
# 단일 메시지 확인
XACK mystream mygroup 1526569495631-0

# 여러 메시지 확인
XACK mystream mygroup 1526569495631-0 1526569495632-0
```

**XACK의 중요성**:
- ACK된 메시지는 PEL에서 제거됨
- ACK하지 않으면 메시지가 다시 전달될 수 있음
- 메모리 효율성을 위해 처리 후 반드시 ACK

### 4.6 Pending 메시지 확인 (XPENDING)

```redis
# 그룹의 Pending 요약
XPENDING mystream mygroup

# 상세 정보 (최대 10개)
XPENDING mystream mygroup - + 10

# 특정 Consumer의 Pending
XPENDING mystream mygroup - + 10 consumer1
```

### 4.7 메시지 소유권 이전 (XCLAIM)

```redis
# 1분 이상 Pending된 메시지를 다른 Consumer로 이전
XCLAIM mystream mygroup consumer2 60000 1526569495631-0

# JUSTID 옵션 (메시지 내용 없이 ID만)
XCLAIM mystream mygroup consumer2 60000 1526569495631-0 JUSTID
```

### 4.8 자동 클레임 (XAUTOCLAIM) - Redis 6.2+

```redis
# 1분 이상 Pending된 메시지 자동 클레임
XAUTOCLAIM mystream mygroup consumer2 60000 0-0 COUNT 10
```

---

## 5. Redis 8.2+ 새로운 명령어

### 5.1 XACKDEL

메시지를 ACK하면서 동시에 삭제:

```redis
# ACK + 삭제를 원자적으로 수행
XACKDEL mystream mygroup 1526569495631-0
```

### 5.2 XDELEX

여러 Consumer Group이 모두 처리한 메시지만 삭제:

```redis
# 모든 그룹이 처리한 메시지 삭제
XDELEX mystream 1526569495631-0
```

---

## 6. 큐 패턴

### 6.1 Fanout Queue (브로드캐스트)

모든 Consumer가 동일한 메시지를 받음:

```
Producer ──► Stream ──► Consumer A (모든 메시지)
                   ├──► Consumer B (모든 메시지)
                   └──► Consumer C (모든 메시지)
```

```redis
# 각 Consumer가 독립적으로 읽기
XREAD STREAMS mystream $
```

### 6.2 Round Robin Queue (분산 처리)

Consumer Group으로 메시지 분산:

```
Producer ──► Stream ──► Group ──► Consumer A (메시지 1, 4)
                            ├──► Consumer B (메시지 2, 5)
                            └──► Consumer C (메시지 3, 6)
```

```redis
# Consumer Group 사용
XREADGROUP GROUP mygroup consumer1 STREAMS mystream >
```

---

## 7. 실전 예제

### 7.1 주문 처리 시스템

```redis
# 1. Stream 및 Consumer Group 생성
XGROUP CREATE orders order-processors $ MKSTREAM

# 2. 주문 추가 (Producer)
XADD orders * order_id ORD-001 user_id U-123 amount 50000

# 3. 주문 처리 (Consumer)
XREADGROUP GROUP order-processors worker1 BLOCK 5000 COUNT 1 STREAMS orders >

# 4. 처리 완료 확인
XACK orders order-processors 1526569495631-0
```

### 7.2 Python 예제

```python
import redis

r = redis.Redis()

# Consumer Group 생성
try:
    r.xgroup_create('mystream', 'mygroup', id='0', mkstream=True)
except redis.exceptions.ResponseError:
    pass  # 그룹이 이미 존재

# Producer
r.xadd('mystream', {'event': 'user_login', 'user_id': '123'})

# Consumer
while True:
    messages = r.xreadgroup(
        groupname='mygroup',
        consumername='worker1',
        streams={'mystream': '>'},
        count=10,
        block=5000
    )

    for stream, entries in messages:
        for entry_id, data in entries:
            # 메시지 처리
            print(f"Processing: {data}")

            # ACK
            r.xack('mystream', 'mygroup', entry_id)
```

---

## 8. 성능 및 Best Practices

### 8.1 성능 특성

| 항목 | 수치 |
|------|------|
| **처리량** | 수천~수만 msg/s |
| **지연시간** | ~0.15ms |
| **메모리** | 메시지당 약 100-200 bytes 오버헤드 |

### 8.2 Best Practices

```
✅ 배치 읽기 사용 (COUNT 옵션)
✅ 처리 후 즉시 XACK
✅ MAXLEN으로 Stream 크기 제한
✅ BLOCK 옵션으로 폴링 최소화
✅ NOACK 사용 시 주의 (메시지 유실 가능)

❌ 단일 메시지씩 읽기 (비효율)
❌ ACK 없이 방치 (메모리 누수)
❌ 무한정 Stream 증가 (메모리 부족)
```

### 8.3 메모리 관리

```redis
# Stream 정보 확인
XINFO STREAM mystream

# Stream 길이 확인
XLEN mystream

# 주기적 트리밍
XTRIM mystream MAXLEN ~ 10000
```

---

## 9. Kafka와 비교

| 항목 | Redis Streams | Apache Kafka |
|------|--------------|--------------|
| **처리량** | 수천~수만/s | 수십만/s |
| **지연시간** | ~0.15ms | ~수십ms |
| **메시지 보존** | 인메모리 (선택적 디스크) | 디스크 |
| **파티셔닝** | 없음 | 있음 |
| **Consumer Group** | 있음 | 있음 |
| **운영 복잡도** | 낮음 | 높음 |
| **적합 규모** | 소~중규모 | 대규모 |

### 9.1 Redis Streams 선택 시점

```
✅ 이미 Redis 인프라 사용 중
✅ 소~중규모 이벤트 처리
✅ 낮은 운영 복잡도 필요
✅ 초저지연 필수
✅ 간단한 Consumer Group 패턴
```

---

## 10. 참고 자료

- [Redis Streams 공식 문서](https://redis.io/docs/latest/develop/data-types/streams/)
- [XREADGROUP 문서](https://redis.io/docs/latest/commands/xreadgroup/)
- [XACK 문서](https://redis.io/docs/latest/commands/xack/)
- [Consumer Groups 튜토리얼](https://www.infoworld.com/article/2257824/how-to-use-consumer-groups-in-redis-streams.html)
