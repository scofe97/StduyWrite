# Redis Sorted Set 기반 큐 상세 가이드

## 1. 개요

Redis Sorted Set(ZSET)은 **스코어(Score)** 기반으로 정렬된 고유 멤버 집합으로, **우선순위 큐**, **지연 큐**, **대기열 시스템**에 적합하다.

### 1.1 핵심 특징

| 특징 | 설명 |
|------|------|
| **스코어 기반 정렬** | 자동으로 스코어 순 정렬 |
| **고유 멤버** | 중복 불가 (멱등성) |
| **범위 쿼리** | 스코어 범위로 조회 가능 |
| **O(log N)** | 삽입, 삭제, 조회 모두 로그 시간 |

### 1.2 내부 구조

```
Sorted Set = Hash Table + Skip List

Hash Table: O(1) ZSCORE, ZREM by key
Skip List:  O(log N) ZADD, ZRANK, ZRANGE
```

### 1.3 사용 사례

| 사용 사례 | Score 활용 |
|----------|-----------|
| **우선순위 큐** | 우선순위 값 |
| **지연 큐** | 실행 예정 타임스탬프 |
| **대기열 시스템** | 대기열 진입 시간 |
| **Rate Limiter** | 요청 타임스탬프 |
| **리더보드** | 점수 |

---

## 2. 기본 명령어

### 2.1 요소 추가 (ZADD)

```redis
# 단일 추가
ZADD queue 100 "task1"

# 여러 개 추가
ZADD queue 200 "task2" 300 "task3"

# 옵션
ZADD queue NX 100 "task1"  # 존재하지 않을 때만
ZADD queue XX 150 "task1"  # 존재할 때만 (스코어 업데이트)
ZADD queue GT 200 "task1"  # 새 스코어가 클 때만
ZADD queue LT 50 "task1"   # 새 스코어가 작을 때만
```

### 2.2 요소 조회

```redis
# 스코어 범위 조회 (오름차순)
ZRANGEBYSCORE queue -inf +inf

# 특정 스코어 범위
ZRANGEBYSCORE queue 100 200

# 현재 시간 이전 (지연 큐용)
ZRANGEBYSCORE queue -inf 1704067200

# 스코어와 함께 조회
ZRANGEBYSCORE queue -inf +inf WITHSCORES

# 개수 제한
ZRANGEBYSCORE queue -inf +inf LIMIT 0 10

# 내림차순 조회
ZREVRANGEBYSCORE queue +inf -inf
```

### 2.3 요소 제거 (Pop)

```redis
# 최소 스코어 요소 제거 (Redis 5.0+)
ZPOPMIN queue

# 여러 개 제거
ZPOPMIN queue 3

# 최대 스코어 요소 제거
ZPOPMAX queue

# 블로킹 버전 (Redis 5.0+)
BZPOPMIN queue 5   # 5초 대기
BZPOPMAX queue 5

# 특정 요소 제거
ZREM queue "task1"

# 스코어 범위로 제거
ZREMRANGEBYSCORE queue -inf 100
```

### 2.4 순위/스코어 확인

```redis
# 순위 확인 (0부터 시작)
ZRANK queue "task1"     # 오름차순 순위
ZREVRANK queue "task1"  # 내림차순 순위

# 스코어 확인
ZSCORE queue "task1"

# 개수 확인
ZCARD queue

# 스코어 범위 내 개수
ZCOUNT queue 100 200
```

---

## 3. 우선순위 큐 (Priority Queue)

### 3.1 개념

```
┌─────────────────────────────────────────────────────────────┐
│                    우선순위 큐                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Score = 우선순위 (낮을수록 먼저 처리)                        │
│                                                             │
│  ZADD priority_queue 1 "critical_task"   # 최우선           │
│  ZADD priority_queue 5 "normal_task"     # 보통             │
│  ZADD priority_queue 10 "low_task"       # 낮음             │
│                                                             │
│  처리 순서: critical → normal → low                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 구현

```redis
# 작업 추가 (우선순위별)
ZADD tasks 1 '{"id":"t1","type":"critical"}'
ZADD tasks 5 '{"id":"t2","type":"normal"}'
ZADD tasks 10 '{"id":"t3","type":"low"}'

# 가장 높은 우선순위 작업 처리
ZPOPMIN tasks
```

### 3.3 Python 구현

```python
import redis
import json

r = redis.Redis()

class PriorityQueue:
    def __init__(self, name):
        self.name = name

    def push(self, task, priority):
        """작업 추가 (priority가 낮을수록 먼저 처리)"""
        r.zadd(self.name, {json.dumps(task): priority})

    def pop(self, timeout=0):
        """가장 높은 우선순위 작업 가져오기"""
        if timeout > 0:
            result = r.bzpopmin(self.name, timeout)
            if result:
                return json.loads(result[1])
        else:
            result = r.zpopmin(self.name)
            if result:
                return json.loads(result[0][0])
        return None

    def peek(self):
        """제거 없이 확인"""
        result = r.zrange(self.name, 0, 0)
        if result:
            return json.loads(result[0])
        return None

    def size(self):
        return r.zcard(self.name)

# 사용 예
pq = PriorityQueue('my_priority_queue')
pq.push({'id': 1, 'action': 'send_email'}, priority=5)
pq.push({'id': 2, 'action': 'process_payment'}, priority=1)  # 먼저 처리

task = pq.pop()  # process_payment 반환
```

---

## 4. 지연 큐 (Delayed Queue)

### 4.1 개념

```
┌─────────────────────────────────────────────────────────────┐
│                    지연 큐                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Score = 실행 예정 Unix 타임스탬프                           │
│                                                             │
│  현재 시간: 1704067200 (2024-01-01 00:00:00)                │
│                                                             │
│  ZADD delayed 1704067260 "task1"  # 1분 후 실행             │
│  ZADD delayed 1704070800 "task2"  # 1시간 후 실행           │
│                                                             │
│  처리: 현재 시간 이전 스코어의 작업만 가져옴                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 구현

```redis
# 5분 후 실행 작업 추가
ZADD delayed_queue 1704067500 '{"id":"t1","action":"send_reminder"}'

# 현재 시간 이전의 작업 조회
ZRANGEBYSCORE delayed_queue -inf 1704067200 LIMIT 0 10

# 처리할 작업 가져오기 + 제거 (Lua 스크립트로 원자적 처리)
```

### 4.3 Python 구현

```python
import redis
import json
import time

r = redis.Redis()

class DelayedQueue:
    def __init__(self, name):
        self.name = name

    def schedule(self, task, delay_seconds):
        """지연 작업 추가"""
        execute_at = time.time() + delay_seconds
        r.zadd(self.name, {json.dumps(task): execute_at})

    def schedule_at(self, task, execute_timestamp):
        """특정 시간에 실행"""
        r.zadd(self.name, {json.dumps(task): execute_timestamp})

    def get_ready_tasks(self, limit=10):
        """실행 준비된 작업들 가져오기 (원자적)"""
        now = time.time()

        # Lua 스크립트로 원자적 처리
        lua_script = """
        local tasks = redis.call('ZRANGEBYSCORE', KEYS[1], '-inf', ARGV[1], 'LIMIT', 0, ARGV[2])
        if #tasks > 0 then
            redis.call('ZREM', KEYS[1], unpack(tasks))
        end
        return tasks
        """

        result = r.eval(lua_script, 1, self.name, now, limit)
        return [json.loads(t) for t in result]

    def poll(self, interval=1):
        """폴링 방식 처리"""
        while True:
            tasks = self.get_ready_tasks()
            for task in tasks:
                yield task

            if not tasks:
                time.sleep(interval)

# 사용 예
dq = DelayedQueue('delayed_tasks')

# 5분 후 이메일 발송
dq.schedule({'action': 'send_email', 'to': 'user@example.com'}, 300)

# 특정 시간에 알림
dq.schedule_at({'action': 'notify'}, 1704153600)

# 처리
for task in dq.poll():
    process_task(task)
```

---

## 5. 대기열 시스템 (Waiting Queue)

### 5.1 티켓 예매 대기열 패턴

```
┌─────────────────────────────────────────────────────────────┐
│                    대기열 시스템                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Score = 대기열 진입 타임스탬프 (+ 랜덤 tiebreaker)          │
│                                                             │
│  주요 연산:                                                 │
│  - ZADD: 대기열 진입                                        │
│  - ZRANK: 내 순번 확인                                      │
│  - ZPOPMIN: 다음 사람 입장                                  │
│  - ZREM: 대기열 이탈                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Kafka vs Redis 대기열 비교

| 항목 | Kafka | Redis Sorted Set |
|------|-------|------------------|
| **순번 조회** | 불가 | O(log N) ZRANK |
| **중간 이탈** | 불가 | O(log N) ZREM |
| **중복 방지** | 별도 구현 | 자동 (고유 멤버) |
| **확장성** | 우수 | 중간 |
| **복잡도** | 높음 | 낮음 |

### 5.3 Python 구현

```python
import redis
import time
import random

r = redis.Redis()

class WaitingQueue:
    def __init__(self, event_id):
        self.queue_key = f'waiting:{event_id}'
        self.active_key = f'active:{event_id}'

    def enter(self, user_id):
        """대기열 진입"""
        # 스코어 = 타임스탬프 + 랜덤 (동시 진입 시 순서 보장)
        score = time.time() + random.random() / 1000000
        r.zadd(self.queue_key, {user_id: score}, nx=True)

    def get_position(self, user_id):
        """내 순번 확인 (0부터 시작)"""
        rank = r.zrank(self.queue_key, user_id)
        return rank + 1 if rank is not None else None

    def leave(self, user_id):
        """대기열 이탈"""
        r.zrem(self.queue_key, user_id)

    def admit_next(self, count=1):
        """다음 N명 입장 허용"""
        users = r.zpopmin(self.queue_key, count)
        admitted = []
        for user_id, score in users:
            user_id = user_id.decode() if isinstance(user_id, bytes) else user_id
            # 활성 사용자로 이동
            r.sadd(self.active_key, user_id)
            r.expire(self.active_key, 600)  # 10분 세션
            admitted.append(user_id)
        return admitted

    def get_queue_length(self):
        """대기열 길이"""
        return r.zcard(self.queue_key)

    def get_ahead_count(self, user_id):
        """내 앞에 몇 명?"""
        rank = r.zrank(self.queue_key, user_id)
        return rank if rank is not None else -1

# 사용 예
wq = WaitingQueue('concert_2024')

# 대기열 진입
wq.enter('user_123')
wq.enter('user_456')

# 내 순번 확인
print(f"Your position: {wq.get_position('user_456')}")

# 입장 허용 (관리자)
admitted = wq.admit_next(10)
print(f"Admitted: {admitted}")
```

### 5.4 Lua 스크립트 (원자적 처리)

```lua
-- admit_users.lua
-- 대기열에서 N명을 원자적으로 활성 세션으로 이동

local queue_key = KEYS[1]
local active_key = KEYS[2]
local count = tonumber(ARGV[1])
local session_ttl = tonumber(ARGV[2])

local users = redis.call('ZPOPMIN', queue_key, count)
local admitted = {}

for i = 1, #users, 2 do
    local user_id = users[i]
    redis.call('SADD', active_key, user_id)
    table.insert(admitted, user_id)
end

if #admitted > 0 then
    redis.call('EXPIRE', active_key, session_ttl)
end

return admitted
```

---

## 6. Rate Limiter (Sliding Window)

### 6.1 개념

```
┌─────────────────────────────────────────────────────────────┐
│                Sliding Window Rate Limiter                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Score = 요청 타임스탬프                                     │
│  Member = 요청 고유 ID                                       │
│                                                             │
│  1. 오래된 요청 제거 (윈도우 밖)                              │
│  2. 현재 윈도우 내 요청 수 확인                               │
│  3. 제한 미만이면 새 요청 추가                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 구현

```python
import redis
import time
import uuid

r = redis.Redis()

class SlidingWindowRateLimiter:
    def __init__(self, key, max_requests, window_seconds):
        self.key = key
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self):
        """요청 허용 여부 확인 및 기록"""
        now = time.time()
        window_start = now - self.window_seconds

        pipe = r.pipeline()

        # 1. 윈도우 밖 요청 제거
        pipe.zremrangebyscore(self.key, '-inf', window_start)

        # 2. 현재 요청 수 확인
        pipe.zcard(self.key)

        # 3. 새 요청 추가 (임시)
        request_id = str(uuid.uuid4())
        pipe.zadd(self.key, {request_id: now})

        # 4. TTL 설정
        pipe.expire(self.key, self.window_seconds)

        results = pipe.execute()
        current_count = results[1]

        if current_count >= self.max_requests:
            # 초과 - 방금 추가한 요청 제거
            r.zrem(self.key, request_id)
            return False

        return True

    def get_remaining(self):
        """남은 요청 수"""
        now = time.time()
        window_start = now - self.window_seconds
        r.zremrangebyscore(self.key, '-inf', window_start)
        current = r.zcard(self.key)
        return max(0, self.max_requests - current)

# 사용 예: IP당 분당 100회 제한
limiter = SlidingWindowRateLimiter('rate:192.168.1.1', 100, 60)

if limiter.is_allowed():
    process_request()
else:
    return_429_too_many_requests()
```

---

## 7. 성능 특성

### 7.1 시간 복잡도

| 명령어 | 시간 복잡도 |
|--------|-----------|
| ZADD | O(log N) |
| ZREM | O(log N) |
| ZSCORE | O(1) |
| ZRANK | O(log N) |
| ZRANGE | O(log N + M) |
| ZRANGEBYSCORE | O(log N + M) |
| ZPOPMIN/MAX | O(log N × M) |
| ZCARD | O(1) |

### 7.2 메모리 사용량

```
Sorted Set ≈ 100 bytes/element 오버헤드

- Skip List 포인터
- Hash Table 엔트리
- Score (double)
```

### 7.3 Best Practices

```
✅ 적절한 TTL 설정 (메모리 관리)
✅ Lua 스크립트로 원자적 처리
✅ LIMIT 옵션으로 결과 제한
✅ 멱등성 활용 (중복 방지)

❌ 전체 범위 조회 (ZRANGE 0 -1)
❌ 무한정 크기 증가
❌ 비원자적 다중 연산 (경쟁 조건)
```

---

## 8. 참고 자료

- [Redis Sorted Sets 공식 문서](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
- [ZADD 문서](https://redis.io/docs/latest/commands/zadd/)
- [ZPOPMIN 문서](https://redis.io/docs/latest/commands/zpopmin/)
- [지연 메시지 시스템 구현](https://www.sirotin.ca/2025/01/10/building-a-delayed-message-system-with-redis-and-fastapi/)
