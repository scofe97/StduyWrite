# Redis Pub/Sub 상세 가이드

## 1. 개요

Redis Pub/Sub는 **발행-구독(Publish-Subscribe)** 메시징 패러다임을 구현한 기능으로, 실시간 메시지 브로드캐스트에 사용된다.

### 1.1 핵심 특징

| 특징 | 설명 |
|------|------|
| **Fire-and-Forget** | 메시지를 보내고 잊음 (보존 없음) |
| **실시간** | 초저지연 메시지 전달 (~0.1ms) |
| **브로드캐스트** | 모든 구독자에게 동시 전달 |
| **패턴 구독** | 와일드카드 채널 구독 지원 |
| **At-Most-Once** | 최대 한 번 전달 (유실 가능) |

### 1.2 동작 방식

```
                     ┌── Subscriber A (news.*)
Publisher ──► Channel ──┼── Subscriber B (news.sports)
    │                  └── Subscriber C (news.weather)
    │
    └── 메시지 전송 후 즉시 완료 (보존 없음)
```

---

## 2. 기본 명령어

### 2.1 채널 구독 (SUBSCRIBE)

```redis
# 단일 채널 구독
SUBSCRIBE news

# 여러 채널 구독
SUBSCRIBE news sports weather

# 구독 후 클라이언트는 메시지 수신 대기 상태
```

**구독 응답 형식**:
```
1) "subscribe"      # 메시지 타입
2) "news"           # 채널 이름
3) (integer) 1      # 현재 구독 중인 채널 수
```

### 2.2 패턴 구독 (PSUBSCRIBE)

```redis
# 와일드카드 패턴 구독
PSUBSCRIBE news.*           # news.sports, news.weather 등
PSUBSCRIBE user.*.login     # user.123.login, user.456.login 등
PSUBSCRIBE *                # 모든 채널

# 지원 패턴
# * : 임의의 문자열
# ? : 임의의 단일 문자
# [abc] : 문자 클래스
```

### 2.3 메시지 발행 (PUBLISH)

```redis
# 채널에 메시지 발행
PUBLISH news "Breaking: Redis 8.4 released!"

# 반환값: 메시지를 받은 구독자 수
(integer) 3
```

### 2.4 구독 해제

```redis
# 특정 채널 구독 해제
UNSUBSCRIBE news

# 모든 채널 구독 해제
UNSUBSCRIBE

# 패턴 구독 해제
PUNSUBSCRIBE news.*
```

### 2.5 채널 정보 확인 (PUBSUB)

```redis
# 활성 채널 목록
PUBSUB CHANNELS

# 패턴과 일치하는 채널
PUBSUB CHANNELS news.*

# 채널별 구독자 수
PUBSUB NUMSUB news sports weather

# 패턴 구독 수
PUBSUB NUMPAT
```

---

## 3. Pub/Sub의 한계

### 3.1 메시지 유실 가능성

```
┌─────────────────────────────────────────────────────────────┐
│                    Fire-and-Forget 문제                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Publisher ──► Channel ──► (Subscriber 없음)                │
│                    │                                        │
│                    └── 메시지 유실! (보존 없음)               │
│                                                             │
│  Publisher ──► Channel ──► Subscriber (연결 끊김)           │
│                    │                                        │
│                    └── 메시지 유실! (재전송 없음)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 주요 한계점

| 한계 | 설명 | 대안 |
|------|------|------|
| **메시지 비보존** | 구독자 없으면 메시지 유실 | Streams 사용 |
| **ACK 없음** | 전달 확인 불가 | Streams 사용 |
| **순서 미보장** | 메시지 순서 보장 안됨 | Streams/List 사용 |
| **재처리 불가** | 놓친 메시지 복구 불가 | Streams 사용 |
| **구독 상태 제한** | 구독 중 다른 명령 실행 제한 | RESP3 사용 |

### 3.3 클러스터 확장성 문제

```
┌─────────────────────────────────────────────────────────────┐
│               Cluster에서 Pub/Sub 확장 문제                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  일반 Pub/Sub:                                              │
│  - PUBLISH가 모든 클러스터 노드에 브로드캐스트                 │
│  - 노드 수 증가 → 네트워크 트래픽 선형 증가                   │
│  - 확장성: 음의 방향으로 확장!                               │
│                                                             │
│  예: 10노드, 1GB/s 대역폭, 1KB 메시지                        │
│      → 최대 ~12,500 RPS 제한                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Sharded Pub/Sub (Redis 7.0+)

### 4.1 개요

**Sharded Pub/Sub**는 클러스터 확장성 문제를 해결하기 위해 Redis 7.0에서 도입되었다.

### 4.2 동작 방식

```
일반 Pub/Sub:
  PUBLISH ──► 모든 노드에 브로드캐스트

Sharded Pub/Sub:
  SPUBLISH ──► 채널 슬롯 담당 노드(Shard)에만 전달
```

### 4.3 명령어

```redis
# Sharded 채널 구독
SSUBSCRIBE news.sports

# Sharded 채널 발행
SPUBLISH news.sports "Goal!"

# Sharded 구독 해제
SUNSUBSCRIBE news.sports

# Sharded 채널 정보
PUBSUB SHARDCHANNELS
PUBSUB SHARDNUMSUB news.sports
```

### 4.4 장점

| 항목 | 일반 Pub/Sub | Sharded Pub/Sub |
|------|-------------|-----------------|
| **메시지 전파** | 모든 노드 | Shard 내 노드만 |
| **확장성** | 음의 방향 | 선형 확장 |
| **네트워크 부하** | 높음 | 낮음 |

---

## 5. 사용 사례

### 5.1 적합한 사용 사례

```
✅ 실시간 알림/푸시
   - 채팅 메시지 알림
   - 라이브 스코어 업데이트
   - 실시간 가격 변동

✅ 캐시 무효화
   - 분산 캐시 동기화
   - 설정 변경 브로드캐스트

✅ 실시간 대시보드
   - 모니터링 메트릭
   - 로그 스트리밍

✅ 이벤트 브로드캐스트
   - 사용자 온라인/오프라인 상태
   - 시스템 상태 알림
```

### 5.2 부적합한 사용 사례

```
❌ 메시지 보장 필요
   → Streams 또는 RabbitMQ 사용

❌ 작업 큐
   → List 또는 Streams 사용

❌ 이벤트 소싱
   → Streams 또는 Kafka 사용

❌ 트랜잭션 메시징
   → RabbitMQ 사용
```

---

## 6. 실전 예제

### 6.1 Python 예제

**Publisher**:
```python
import redis

r = redis.Redis()

# 메시지 발행
r.publish('news', 'Breaking: Redis 8.4 released!')
r.publish('news.sports', 'Team A wins championship!')
```

**Subscriber**:
```python
import redis

r = redis.Redis()
pubsub = r.pubsub()

# 채널 구독
pubsub.subscribe('news')
pubsub.psubscribe('news.*')

# 메시지 수신 루프
for message in pubsub.listen():
    if message['type'] in ('message', 'pmessage'):
        print(f"Channel: {message['channel']}")
        print(f"Data: {message['data']}")
```

### 6.2 WebSocket 연동 패턴

```
┌─────────┐    WebSocket    ┌─────────┐    Pub/Sub    ┌─────────┐
│ Client  │ ◄─────────────► │  Server │ ◄───────────► │  Redis  │
└─────────┘                 └─────────┘                └─────────┘
     │                           │                          │
     │ 1. WebSocket 연결          │                          │
     │─────────────────────────►│                          │
     │                           │ 2. SUBSCRIBE channel     │
     │                           │─────────────────────────►│
     │                           │                          │
     │                           │ 3. PUBLISH (다른 서버)    │
     │                           │◄─────────────────────────│
     │ 4. WebSocket 메시지        │                          │
     │◄─────────────────────────│                          │
```

### 6.3 캐시 무효화 예제

```python
import redis

# Publisher (캐시 업데이트 시)
def invalidate_cache(key):
    r = redis.Redis()
    r.publish('cache:invalidate', key)

# Subscriber (각 애플리케이션 서버)
def listen_invalidation():
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe('cache:invalidate')

    for message in pubsub.listen():
        if message['type'] == 'message':
            key = message['data'].decode()
            local_cache.delete(key)
```

---

## 7. RESP3와 Pub/Sub

### 7.1 기존 제한 (RESP2)

```
구독 상태에서:
❌ 일반 명령어 실행 불가
✅ SUBSCRIBE / UNSUBSCRIBE만 가능
✅ PSUBSCRIBE / PUNSUBSCRIBE만 가능
```

### 7.2 RESP3 개선

```
구독 상태에서:
✅ 모든 명령어 실행 가능
✅ 푸시 메시지와 응답 구분
```

```redis
# RESP3 핸드셰이크
HELLO 3

# 이후 구독 중에도 다른 명령 실행 가능
SUBSCRIBE news
GET mykey  # 가능!
```

---

## 8. 성능 특성

### 8.1 지연시간

| 항목 | 수치 |
|------|------|
| **평균 지연시간** | ~0.1ms |
| **P99 지연시간** | ~0.5ms |
| **Streams 대비** | 0.05ms 빠름 |

### 8.2 처리량

| 환경 | 처리량 |
|------|--------|
| **단일 노드** | 수십만 msg/s |
| **클러스터 (일반)** | 노드 증가 시 감소 |
| **클러스터 (Sharded)** | 선형 확장 |

---

## 9. Streams vs Pub/Sub 선택 가이드

```
┌─────────────────────────────────────────────────────────────┐
│                      선택 가이드                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Q: 메시지 유실이 허용되는가?                                │
│  ├─ YES → Pub/Sub 고려                                     │
│  └─ NO → Streams 사용                                      │
│                                                             │
│  Q: 메시지 재처리가 필요한가?                                │
│  ├─ YES → Streams 사용                                     │
│  └─ NO → Pub/Sub 고려                                      │
│                                                             │
│  Q: Consumer Group이 필요한가?                              │
│  ├─ YES → Streams 사용                                     │
│  └─ NO → Pub/Sub 고려                                      │
│                                                             │
│  Q: 초저지연이 최우선인가?                                   │
│  ├─ YES → Pub/Sub 사용 (~0.1ms)                            │
│  └─ NO → Streams 사용 (~0.15ms)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. 참고 자료

- [Redis Pub/Sub 공식 문서](https://redis.io/docs/latest/develop/pubsub/)
- [Sharded Pub/Sub](https://redis.io/docs/latest/develop/pubsub/#sharded-pubsub)
- [Pub/Sub 확장성 분석](https://ably.com/blog/scaling-pub-sub-with-websockets-and-redis)
