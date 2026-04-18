# Redis List 기반 큐 상세 가이드

## 1. 개요

Redis List는 **연결 리스트(Linked List)** 구조로, 양쪽 끝에서 O(1) 시간에 삽입/삭제가 가능하여 **큐(Queue)** 또는 **스택(Stack)** 구현에 적합하다.

### 1.1 핵심 특징

| 특징 | 설명 |
|------|------|
| **FIFO/LIFO** | 큐(FIFO) 또는 스택(LIFO) 구현 가능 |
| **블로킹 연산** | BRPOP/BLPOP으로 대기 가능 |
| **원자적 연산** | 경쟁 조건 없이 안전한 처리 |
| **간단한 구현** | 최소한의 명령어로 큐 구현 |

### 1.2 List vs Streams 비교

| 항목 | List | Streams |
|------|------|---------|
| **Consumer Group** | 없음 | 있음 |
| **메시지 ID** | 없음 | 자동 생성 |
| **ACK** | 수동 구현 필요 | 내장 |
| **재처리** | 수동 구현 필요 | 내장 |
| **복잡도** | 낮음 | 중간 |
| **적합 용도** | 단순 작업 큐 | 이벤트 스트리밍 |

---

## 2. 기본 명령어

### 2.1 요소 추가

```redis
# 왼쪽(Head)에 추가
LPUSH myqueue "task1"
LPUSH myqueue "task2" "task3"  # 여러 개 동시 추가

# 오른쪽(Tail)에 추가
RPUSH myqueue "task4"
RPUSH myqueue "task5" "task6"

# 존재하는 리스트에만 추가
LPUSHX myqueue "task7"  # myqueue가 없으면 무시
RPUSHX myqueue "task8"
```

### 2.2 요소 제거 (Pop)

```redis
# 왼쪽에서 제거
LPOP myqueue

# 오른쪽에서 제거
RPOP myqueue

# 여러 개 제거 (Redis 6.2+)
LPOP myqueue 3  # 왼쪽에서 3개
RPOP myqueue 3  # 오른쪽에서 3개
```

### 2.3 블로킹 Pop (가장 중요!)

```redis
# 블로킹 왼쪽 Pop (최대 5초 대기)
BLPOP myqueue 5

# 블로킹 오른쪽 Pop
BRPOP myqueue 5

# 여러 큐에서 대기 (우선순위 순서)
BLPOP queue:high queue:medium queue:low 5

# 무한 대기 (타임아웃 0)
BRPOP myqueue 0
```

**블로킹 응답 형식**:
```
1) "myqueue"   # 큐 이름
2) "task1"     # 값
```

### 2.4 리스트 정보

```redis
# 길이 확인
LLEN myqueue

# 범위 조회 (삭제 없이)
LRANGE myqueue 0 -1   # 전체
LRANGE myqueue 0 9    # 처음 10개

# 특정 인덱스 조회
LINDEX myqueue 0      # 첫 번째
LINDEX myqueue -1     # 마지막
```

---

## 3. 큐 패턴

### 3.1 기본 FIFO 큐

```
Producer ──LPUSH──► [Queue] ──RPOP──► Consumer

순서: task1 → task2 → task3
      ↓       ↓       ↓
    처리1   처리2   처리3
```

```redis
# Producer
LPUSH tasks "task1"
LPUSH tasks "task2"
LPUSH tasks "task3"

# Consumer
RPOP tasks  # "task1" 반환
RPOP tasks  # "task2" 반환
RPOP tasks  # "task3" 반환
```

### 3.2 블로킹 Worker 패턴

```redis
# Worker (무한 루프로 대기)
while True:
    result = BRPOP tasks 0  # 무한 대기
    process(result)
```

```python
import redis

r = redis.Redis()

while True:
    # 블로킹 대기 (무한)
    result = r.brpop('tasks', timeout=0)
    if result:
        queue, task = result
        process_task(task)
```

### 3.3 우선순위 큐 패턴

```redis
# 여러 큐를 우선순위 순서로 대기
BRPOP queue:critical queue:high queue:normal queue:low 0

# critical → high → normal → low 순서로 처리
```

```python
import redis

r = redis.Redis()

# 우선순위 순서로 큐 지정
queues = ['queue:critical', 'queue:high', 'queue:normal', 'queue:low']

while True:
    result = r.brpop(queues, timeout=0)
    if result:
        queue, task = result
        print(f"Processing from {queue}: {task}")
```

---

## 4. 신뢰성 있는 큐 (Reliable Queue)

### 4.1 문제점

기본 RPOP의 문제:
```
1. Worker가 RPOP으로 작업 가져옴
2. Worker 처리 중 크래시
3. 작업 유실! (복구 불가)
```

### 4.2 해결책: BRPOPLPUSH / LMOVE

```redis
# BRPOPLPUSH (Redis 6.2 이전)
BRPOPLPUSH tasks processing 0

# LMOVE (Redis 6.2+, 권장)
LMOVE tasks processing RIGHT LEFT

# BLMOVE (블로킹 버전)
BLMOVE tasks processing RIGHT LEFT 0
```

### 4.3 Reliable Queue 패턴

```
┌─────────────────────────────────────────────────────────────┐
│                    Reliable Queue 패턴                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 작업 가져오기 (원자적으로 processing으로 이동)            │
│     LMOVE tasks processing RIGHT LEFT                       │
│                                                             │
│  2. 작업 처리                                               │
│     process_task()                                          │
│                                                             │
│  3. 처리 완료 시                                            │
│     LREM processing 1 "task_data"                          │
│                                                             │
│  4. 실패 시 (크래시 복구)                                    │
│     processing 리스트에서 재처리 또는 tasks로 복구           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Python 구현 예제

```python
import redis
import json
import time

r = redis.Redis()

def reliable_worker():
    while True:
        # 1. 원자적으로 작업 가져오기
        task = r.blmove('tasks', 'processing', 0, 'RIGHT', 'LEFT')

        if task:
            try:
                # 2. 작업 처리
                process_task(json.loads(task))

                # 3. 처리 완료 - processing에서 제거
                r.lrem('processing', 1, task)

            except Exception as e:
                # 4. 실패 시 - 다시 tasks로 복구 (선택적)
                r.lmove('processing', 'tasks', 'LEFT', 'LEFT')
                print(f"Task failed, returned to queue: {e}")

def recover_stale_tasks(timeout_seconds=300):
    """오래된 processing 작업 복구"""
    # processing 리스트의 모든 항목 확인
    tasks = r.lrange('processing', 0, -1)

    for task in tasks:
        task_data = json.loads(task)
        # 타임스탬프 기반 타임아웃 체크
        if time.time() - task_data.get('timestamp', 0) > timeout_seconds:
            # tasks로 다시 이동
            r.lmove('processing', 'tasks', 'LEFT', 'LEFT')
```

---

## 5. 고급 패턴

### 5.1 작업 결과 저장 패턴

```python
import redis
import json
import uuid

r = redis.Redis()

# Producer
def submit_task(data):
    task_id = str(uuid.uuid4())
    task = {
        'id': task_id,
        'data': data,
        'timestamp': time.time()
    }
    r.lpush('tasks', json.dumps(task))
    return task_id

def get_result(task_id, timeout=30):
    """결과 대기"""
    result = r.brpop(f'result:{task_id}', timeout)
    if result:
        return json.loads(result[1])
    return None

# Consumer/Worker
def worker():
    while True:
        result = r.brpop('tasks', 0)
        if result:
            task = json.loads(result[1])
            task_id = task['id']

            # 처리
            output = process(task['data'])

            # 결과 저장 (30초 후 자동 삭제)
            r.lpush(f'result:{task_id}', json.dumps(output))
            r.expire(f'result:{task_id}', 30)
```

### 5.2 Rate Limiting 패턴

```python
import redis
import time

r = redis.Redis()

def rate_limited_worker(max_per_second=10):
    """초당 최대 처리량 제한"""
    interval = 1.0 / max_per_second

    while True:
        start = time.time()

        result = r.brpop('tasks', 1)  # 1초 타임아웃
        if result:
            process_task(result[1])

        # Rate limiting
        elapsed = time.time() - start
        if elapsed < interval:
            time.sleep(interval - elapsed)
```

### 5.3 Dead Letter Queue 패턴

```python
import redis
import json

r = redis.Redis()

MAX_RETRIES = 3

def worker_with_dlq():
    while True:
        task_json = r.blmove('tasks', 'processing', 0, 'RIGHT', 'LEFT')

        if task_json:
            task = json.loads(task_json)
            retries = task.get('retries', 0)

            try:
                process_task(task)
                r.lrem('processing', 1, task_json)

            except Exception as e:
                r.lrem('processing', 1, task_json)

                if retries < MAX_RETRIES:
                    # 재시도 카운트 증가 후 다시 큐에 추가
                    task['retries'] = retries + 1
                    r.lpush('tasks', json.dumps(task))
                else:
                    # Dead Letter Queue로 이동
                    task['error'] = str(e)
                    r.lpush('tasks:dlq', json.dumps(task))
```

---

## 6. 성능 특성

### 6.1 시간 복잡도

| 명령어 | 시간 복잡도 | 설명 |
|--------|-----------|------|
| LPUSH/RPUSH | O(1) | 단일 요소 |
| LPUSH/RPUSH (N개) | O(N) | N개 요소 |
| LPOP/RPOP | O(1) | 단일 요소 |
| LLEN | O(1) | |
| LINDEX | O(N) | N = 인덱스 |
| LRANGE | O(S+N) | S = 시작, N = 범위 |
| LREM | O(N) | N = 리스트 길이 |

### 6.2 Best Practices

```
✅ BRPOP/BLPOP 사용 (폴링 방지)
✅ 타임아웃 적절히 설정
✅ 여러 큐 우선순위 활용
✅ LMOVE로 신뢰성 확보
✅ 리스트 크기 모니터링

❌ 바쁜 폴링 (CPU 낭비)
❌ LINDEX로 전체 순회 (O(N))
❌ 무한정 리스트 증가
❌ 단순 RPOP만 사용 (유실 위험)
```

---

## 7. Streams로 마이그레이션

### 7.1 마이그레이션 이유

```
List → Streams 전환 고려 시점:

✅ Consumer Group 필요
✅ 메시지 ID/추적 필요
✅ ACK 메커니즘 필요
✅ 메시지 재처리 필요
✅ 여러 Consumer 분산 처리
```

### 7.2 비교

| 기능 | List | Streams |
|------|------|---------|
| 메시지 추가 | LPUSH | XADD |
| 메시지 읽기 | RPOP | XREAD |
| 블로킹 읽기 | BRPOP | XREAD BLOCK |
| Consumer Group | 수동 구현 | XGROUP |
| ACK | 수동 구현 | XACK |

---

## 8. 참고 자료

- [Redis Lists 공식 문서](https://redis.io/docs/latest/develop/data-types/lists/)
- [BLPOP 문서](https://redis.io/docs/latest/commands/blpop/)
- [LMOVE 문서](https://redis.io/docs/latest/commands/lmove/)
- [Reliable Queue 패턴](https://redis.io/docs/latest/commands/rpoplpush/)
