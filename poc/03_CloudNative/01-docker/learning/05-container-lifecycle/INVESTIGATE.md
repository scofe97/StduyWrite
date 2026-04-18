# Ch05. Container Lifecycle - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. PID 1 프로세스의 좀비 프로세스 수거(reaping) 실패와 해결책은?

### 왜 이 질문이 중요한가

컨테이너 내부에서 첫 번째 프로세스가 PID 1을 할당받으며, 전통적인 Linux의 init 프로세스 역할을 수행해야 한다. 많은 애플리케이션이 PID 1로 설계되지 않았기 때문에 자식 프로세스 관리를 제대로 하지 못한다. 좀비 프로세스 누적은 프로세스 테이블 고갈로 이어져 새로운 프로세스 생성을 차단할 수 있다.

### 답변

**좀비 프로세스 발생 원리**

자식 프로세스가 종료되면 커널은 즉시 메모리를 해제하지만 프로세스 테이블 엔트리는 유지한다. 부모 프로세스가 `wait()` 시스템 콜을 호출하여 종료 상태를 읽을 때까지 좀비 상태로 남는다.

```bash
# 좀비 프로세스 확인
$ ps aux | grep defunct
root  1234  0.0  0.0      0     0 ?        Z    10:00   0:00 [sleep] <defunct>
```

**PID 1의 특별한 책임**

1. **고아 프로세스 입양**: 부모가 먼저 죽은 프로세스는 PID 1이 부모가 됨
2. **좀비 수거**: 입양한 프로세스가 종료되면 `wait()` 호출하여 수거
3. **신호 처리**: 기본 신호 핸들러가 없어 명시적 구현 필요

**문제 발생 시나리오**

```dockerfile
# 나쁜 예: 쉘 스크립트가 PID 1
FROM ubuntu:22.04
CMD ["/bin/sh", "-c", "while true; do sleep 1 & done"]
# 백그라운드 sleep 프로세스들이 좀비로 누적
```

```bash
# 실행 후 1시간 뒤
$ docker exec myapp ps aux | grep defunct | wc -l
3600  # 매 초마다 1개씩 누적
```

**해결 방법**

**1. tini 사용** (권장):
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "app.py"]
```

**2. Docker --init 플래그**:
```bash
$ docker run --init myapp
# Docker가 tini-static을 자동 주입
```

**3. 애플리케이션 코드에서 처리** (Go):
```go
package main
import (
    "os"
    "os/signal"
    "syscall"
)

func main() {
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGCHLD)

    go func() {
        for range sigChan {
            var wstatus syscall.WaitStatus
            syscall.Wait4(-1, &wstatus, syscall.WNOHANG, nil)
        }
    }()

    // 메인 로직
}
```

### 실무 적용

**시나리오: Celery worker 좀비 프로세스 누적**

증상:
```bash
$ docker exec celery ps aux | grep defunct
# 100개 이상의 <defunct> 프로세스

$ cat /proc/sys/kernel/pid_max
32768
$ pgrep -c celery
31000  # 거의 한계
```

해결:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y tini && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["celery", "-A", "tasks", "worker"]
```

검증:
```bash
# 24시간 후
$ docker exec celery ps aux | grep -c defunct
0
```

---

## Q2. SIGTERM을 받은 컨테이너의 graceful shutdown 패턴은?

### 왜 이 질문이 중요한가

Docker는 `docker stop` 실행 시 SIGTERM을 보내고 10초(기본값) 후 SIGKILL을 보낸다. 애플리케이션이 SIGTERM을 처리하지 않으면 진행 중인 요청이 중단되고, 데이터베이스 트랜잭션이 롤백되며, 파일 쓰기가 손상될 수 있다.

### 답변

**Graceful Shutdown 핵심 단계**

1. **신호 수신**: SIGTERM/SIGINT 캐치
2. **새 요청 거부**: 헬스체크 실패 → 로드밸런서 제외
3. **진행 중 작업 완료**: 타임아웃 내 현재 요청 마무리
4. **리소스 정리**: DB 연결, 파일 디스크립터 정리
5. **종료**: exit(0)

**언어별 구현**

**Go:**
```go
package main
import (
    "context"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    srv := &http.Server{Addr: ":8080"}

    go func() {
        srv.ListenAndServe()
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGTERM, syscall.SIGINT)
    <-quit

    log.Println("Shutting down...")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Forced shutdown:", err)
    }
}
```

**Python:**
```python
import signal
import sys
import atexit

shutdown_flag = False

def shutdown_handler(signum, frame):
    global shutdown_flag
    print("Received SIGTERM, graceful shutdown...")
    shutdown_flag = True

def cleanup():
    print("Cleaning up resources...")
    # DB 연결 종료 등

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)
atexit.register(cleanup)

while not shutdown_flag:
    process_task()
```

**Node.js:**
```javascript
const express = require('express');
const app = express();
const server = app.listen(3000);

let isShuttingDown = false;

app.get('/health', (req, res) => {
    if (isShuttingDown) {
        res.status(503).send('Shutting down');
    } else {
        res.status(200).send('OK');
    }
});

process.on('SIGTERM', () => {
    console.log('SIGTERM received...');
    isShuttingDown = true;

    server.close(() => {
        console.log('HTTP server closed');
        db.end(() => {
            process.exit(0);
        });
    });

    setTimeout(() => {
        console.error('Forced shutdown');
        process.exit(1);
    }, 30000);
});
```

**Docker 설정**

```yaml
# docker-compose.yml
services:
  api:
    image: myapi
    stop_grace_period: 45s  # SIGKILL까지 45초 대기
```

### 실무 적용

**시나리오: Kubernetes 롤링 업데이트 중 5xx 에러**

문제:
```javascript
// 기존 코드 (SIGTERM 미처리)
app.listen(3000);
// docker stop 시 즉시 종료 → 진행 중 요청 실패
```

해결:
```javascript
let activeConnections = 0;

app.use((req, res, next) => {
    activeConnections++;
    res.on('finish', () => activeConnections--);
    next();
});

process.on('SIGTERM', () => {
    console.log(`Shutdown: ${activeConnections} active connections`);
    server.close(() => {
        console.log('All connections closed');
        process.exit(0);
    });
});
```

Kubernetes 설정:
```yaml
spec:
  containers:
  - name: api
    lifecycle:
      preStop:
        exec:
          command: ["/bin/sh", "-c", "sleep 5"]
  terminationGracePeriodSeconds: 60
```

결과:
- 롤링 업데이트 중 5xx 에러 0건
- 평균 종료 시간 3초
- 로그에서 "active connections: 0" 확인

---

## Q3. docker stop의 타임아웃과 restart policy의 상호작용은?

### 왜 이 질문이 중요한가

재시작 정책은 컨테이너의 자가 치유 능력을 결정한다. 잘못된 정책은 장애를 악화시킬 수 있다. 설정 오류로 계속 실패하는 컨테이너가 `always` 정책으로 무한 재시작되면 시스템 리소스를 낭비한다.

### 답변

**4가지 재시작 정책**

| 정책 | 동작 | 사용 시나리오 |
|------|------|--------------|
| **no** | 재시작 안함 | 일회성 작업, 테스트 |
| **on-failure[:max]** | exit code ≠ 0만 재시작 | 일시적 오류 복구 |
| **always** | 항상 재시작 | 프로덕션 서비스 |
| **unless-stopped** | 수동 중지 제외 재시작 | 유지보수 고려 |

**always vs unless-stopped**

```bash
# always 정책
$ docker run -d --restart=always redis
$ docker stop redis
$ sudo systemctl restart docker
$ docker ps
# redis 다시 시작됨 ✅

# unless-stopped 정책
$ docker run -d --restart=unless-stopped redis
$ docker stop redis
$ sudo systemctl restart docker
$ docker ps
# redis 시작 안됨 ❌
```

**재시작 간격 (Exponential Backoff)**

- 첫 재시작: 즉시
- 두 번째: 1초
- 세 번째: 2초
- 네 번째: 4초
- 최대: 1분

**정책 변경**

```bash
# 실행 중인 컨테이너 정책 변경
$ docker update --restart=unless-stopped myapp

# 확인
$ docker inspect myapp --format '{{.HostConfig.RestartPolicy.Name}}'
unless-stopped
```

### 실무 적용

**시나리오 1: DB 마이그레이션 실패 루프**

문제:
```bash
$ docker run -d --restart=always \
  -e DB_HOST=postgres \
  myapp
# postgres 미준비 → 계속 재시작 → CPU 급증
```

해결:
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      retries: 5

  app:
    image: myapp
    depends_on:
      postgres:
        condition: service_healthy
    restart: on-failure
```

**시나리오 2: 유지보수 모드 전환**

문제:
```bash
# always 정책
$ docker stop app  # 점검을 위해 중지
# 서버 재부팅 발생
# → app 다시 시작 → 점검 중 DB에 쓰기 ❌
```

해결:
```bash
# unless-stopped 사용
$ docker run -d --restart=unless-stopped app
$ docker stop app
# 재부팅 후에도 중지 상태 유지 ✅
```

**권장사항**

- 프로덕션 서비스: `unless-stopped`
- 인프라 서비스: `always`
- 배치 작업: `on-failure:3`
- 개발/테스트: `no`

---

## Q4. 컨테이너 상태 전이와 디버깅 전략은?

### 왜 이 질문이 중요한가

컨테이너의 상태 전이를 이해하면 디버깅 시 컨테이너가 왜 특정 상태에 머물러 있는지 파악할 수 있다. Exited 상태 컨테이너는 디스크 공간을 차지하므로 정기적으로 정리해야 한다.

### 답변

**상태 다이어그램**

```
     create          start
[X] --------> [Created] --------> [Running]
                  │                   │ │
                  │                   │ └─ pause
                  │                   │    ↓
                  │                   │ [Paused]
                  │                   │    │
                  │                   │ ←──┘ unpause
                  │                   │
                  │ ←─────────────────┘ stop/exit
                  ↓
             [Exited]
                  │
                  │ rm
                  ↓
                [X]
```

**각 상태의 내부 동작**

**Created**:
- 컨테이너 메타데이터 생성 (`/var/lib/docker/containers/<id>/`)
- config.v2.json 저장
- 네트워크/볼륨 미할당
- 프로세스 미시작

**Running**:
1. containerd에게 시작 요청 (gRPC)
2. containerd-shim 프로세스 생성
3. runc가 namespace 생성 (PID, NET, MNT, IPC, UTS)
4. cgroup 설정 적용
5. overlay2 파일시스템 마운트
6. 네트워크 구성 (veth pair)
7. ENTRYPOINT/CMD 실행

**Paused**:
- cgroup freezer 사용
- 모든 프로세스를 `TASK_UNINTERRUPTIBLE` 상태로
- CPU 스케줄링 제외, 메모리 유지
- 네트워크 연결 유지, 패킷 처리 중단

```bash
$ docker pause test
$ cat /sys/fs/cgroup/freezer/docker/<id>/freezer.state
FROZEN
```

**Exited**:
- PID 1에 SIGTERM → 10초 → SIGKILL
- exit code 메타데이터 저장
- namespace 해제
- cgroup 제거
- 네트워크 인터페이스 삭제
- **파일시스템 유지** (로그, 쓰기 레이어)

**Removed**:
- 메타데이터 디렉토리 삭제
- 쓰기 레이어 삭제
- 네트워크/볼륨 연결 해제

### 실무 적용

**시나리오 1: 디스크 공간 부족**

진단:
```bash
$ df -h
# /var 95% 사용

$ docker ps -a --filter "status=exited" | wc -l
500  # 종료된 컨테이너 500개

$ docker ps -a --format "{{.ID}}" | \
  xargs -I {} du -sh /var/lib/docker/containers/{}
# 일부 컨테이너 1GB+ 로그 보유
```

해결:
```bash
# 종료된 컨테이너 제거
$ docker container prune
# 45GB 회복

# 재발 방지
$ cat /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

**시나리오 2: pause를 활용한 무중단 배포**

```bash
# 구 컨테이너 pause (CPU 해제)
$ docker pause old-app

# 신규 컨테이너 헬스체크 대기
$ while [ "$(docker inspect new-app --format='{{.State.Health.Status}}')" != "healthy" ]; do
  sleep 1
done

# 트래픽 전환 후 구 컨테이너 종료
$ docker stop old-app

# 롤백 필요 시 unpause (start보다 빠름)
$ docker unpause old-app
```

---

## Q5. 헬스체크 설계 패턴과 자동 복구 구현은?

### 왜 이 질문이 중요한가

컨테이너가 실행 중이라고 해서 정상 작동하는 것은 아니다. 교착 상태, 메모리 누수, 외부 의존성 장애 등으로 요청을 처리하지 못할 수 있다. 헬스체크는 이러한 "좀비 상태"를 감지하여 자동 복구를 트리거한다.

### 답변

**헬스체크 정의**

Dockerfile:
```dockerfile
FROM nginx:1.23
HEALTHCHECK --interval=30s \
            --timeout=3s \
            --start-period=10s \
            --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

Docker run:
```bash
docker run -d \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  --health-start-period=10s \
  nginx
```

**파라미터**

- `interval`: 헬스체크 간격 (기본 30초)
- `timeout`: 명령 타임아웃 (기본 30초)
- `retries`: 연속 실패 허용 횟수 (기본 3)
- `start-period`: 시작 후 유예 기간 (기본 0초)

**상태 전이**

```
[starting] → (첫 성공) → [healthy]
    ↓                        ↓
(start-period 초과)    (연속 3회 실패)
    ↓                        ↓
[unhealthy] ←────────────────┘
```

**상태 확인**

```bash
$ docker ps --format "table {{.Names}}\t{{.Status}}"
# NAMES    STATUS
# web      Up 5 minutes (healthy)
# db       Up 2 hours (unhealthy)

$ docker inspect web --format='{{json .State.Health}}' | jq
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [...]
}
```

**자동 재시작 구현**

Docker는 unhealthy 상태에서 자동 재시작하지 않는다. Autoheal 사용:

```bash
$ docker run -d \
  --name autoheal \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  willfarrell/autoheal
```

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 10s
      timeout: 3s
      retries: 3

  autoheal:
    image: willfarrell/autoheal
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

**헬스체크 모범 사례**

1. **경량 체크** (3초 이내):
```dockerfile
# 좋은 예
HEALTHCHECK CMD curl -f http://localhost/health || exit 1

# 나쁜 예
HEALTHCHECK CMD python -c "import app; app.full_test()"
```

2. **외부 의존성 포함**:
```python
@app.route('/health')
def health():
    try:
        db.execute('SELECT 1')
        redis.ping()
        return 'OK', 200
    except Exception as e:
        return str(e), 503
```

3. **start-period 충분히**:
```dockerfile
# Java 애플리케이션 (60초 초기화)
HEALTHCHECK --start-period=90s \
            --interval=10s \
  CMD curl -f http://localhost:8080/actuator/health
```

### 실무 적용

**시나리오: 메모리 누수로 응답 지연**

헬스체크 구현:
```javascript
app.get('/health', async (req, res) => {
    const start = Date.now();
    try {
        await db.query('SELECT 1');
        const duration = Date.now() - start;

        // 1초 이상이면 unhealthy
        if (duration > 1000) {
            return res.status(503).send(`Slow: ${duration}ms`);
        }
        res.status(200).send('OK');
    } catch (err) {
        res.status(503).send(err.message);
    }
});
```

Autoheal 배포:
```yaml
services:
  api:
    build: .
    # healthcheck는 Dockerfile에 정의

  autoheal:
    image: willfarrell/autoheal
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - AUTOHEAL_INTERVAL=10
```

결과:
```bash
# 메모리 누수 → unhealthy
$ docker ps
# api  Up 2 minutes (unhealthy)

# 10초 후 autoheal이 재시작
$ docker ps
# api  Up 5 seconds (health: starting)
```

---

## Q6. 컨테이너 로깅 드라이버 선택 기준과 중앙화 전략은?

### 왜 이 질문이 중요한가

기본 JSON-file 드라이버는 로그 로테이션 미설정 시 디스크를 가득 채운다. 중앙화된 로그 수집 시스템과 통합하려면 적절한 드라이버를 선택해야 하며, 각 드라이버는 성능, 안정성, 검색 기능에서 트레이드오프가 있다.

### 답변

**주요 로깅 드라이버**

| 드라이버 | 저장 위치 | docker logs | 중앙화 |
|---------|----------|-------------|--------|
| **json-file** | 로컬 파일 | ✅ | ❌ |
| **syslog** | syslog 서버 | ❌ | ✅ |
| **journald** | systemd journal | ✅ (프록시) | 추가 설정 |
| **fluentd** | Fluentd | ❌ | ✅ |

**json-file (기본)**

장점:
- 설정 불필요
- docker logs 사용 가능
- 외부 의존성 없음

단점:
- 로그 로테이션 필수
- 중앙화 불가
- 컨테이너 삭제 시 손실

설정:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "compress": "true"
  }
}
```

**syslog**

장점:
- 표준 프로토콜
- 네트워크 전송
- SIEM 통합

단점:
- UDP 사용 시 손실 가능
- docker logs 사용 불가
- syslog 서버 장애 시 유실

설정:
```bash
docker run -d \
  --log-driver syslog \
  --log-opt syslog-address=tcp://192.168.1.100:514 \
  --log-opt tag="{{.Name}}" \
  nginx
```

**journald**

장점:
- systemd 통합
- 구조화된 로그
- 자동 로테이션

단점:
- systemd 환경 필요
- docker logs 느림
- 추가 전송 설정 필요

사용:
```bash
docker run -d --log-driver journald nginx

# 조회
journalctl CONTAINER_NAME=nginx -f
```

**fluentd**

장점:
- 500+ 플러그인
- 비동기 전송
- 로그 변환/필터링
- 버퍼링

단점:
- Fluentd 데몬 필요
- docker logs 불가
- 네트워크 장애 시 버퍼 크기만큼만 보호

설정:
```bash
docker run -d \
  --log-driver fluentd \
  --log-opt fluentd-address=localhost:24224 \
  --log-opt tag="docker.{{.Name}}" \
  nginx
```

**선택 기준**

```
환경별 선택
├─ 개발/테스트 → json-file
├─ 단일 서버
│  ├─ systemd → journald
│  └─ Unix → syslog
└─ 클러스터
   ├─ 기존 SIEM → syslog
   ├─ ELK/EFK → fluentd
   └─ AWS → awslogs
```

### 실무 적용

**시나리오 1: 디스크 공간 부족**

문제:
```bash
$ df -h /var
# /var 100%

$ find /var/lib/docker/containers/ -name "*-json.log" -exec du -h {} \; | sort -hr
# 15GB container1-json.log
```

즉시 조치:
```bash
$ truncate -s 0 /var/lib/docker/containers/<id>/<id>-json.log
```

영구 해결:
```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

**시나리오 2: ELK 스택 통합**

Fluentd 설정:
```conf
<source>
  @type forward
  port 24224
</source>

<match docker.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
```

Docker Compose:
```yaml
services:
  fluentd:
    image: fluent/fluentd:v1.14
    ports:
      - "24224:24224"

  app:
    image: myapp
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: docker.app
```

---

## Q7. cgroup v2의 리소스 제한과 한계 도달 시 동작은?

### 왜 이 질문이 중요한가

리소스 제한은 noisy neighbor 문제를 방지하는 핵심이다. 제한 도달 시 동작을 모르면 성능 저하 원인을 파악하기 어렵다. 메모리 제한 초과는 OOM Kill을 발생시키지만, CPU 제한 초과는 throttling만 일으킨다.

### 답변

**CPU 제한**

설정:
```bash
$ docker run -d --cpus="1.5" nginx
# cpu.max = "150000 100000" (150ms per 100ms)
```

한계 도달 시:
- Throttling 발생 (프로세스 대기 큐)
- 처리 시간 증가, 종료 안됨

확인:
```bash
$ docker stats --no-stream test
# CPU %가 한계에서 멈춤

$ cat /sys/fs/cgroup/system.slice/docker-<id>.scope/cpu.stat
# nr_throttled: 5000
# throttled_time: 25000000000
```

**메모리 제한**

설정:
```bash
$ docker run -d -m 512m --memory-swap 512m nginx
# memory.max = 536870912
```

한계 도달 시:

Phase 1: 메모리 압박
```bash
$ cat /sys/fs/cgroup/.../memory.pressure
# some avg10=2.50  # 2.5% 시간 동안 메모리 확보 대기
```

Phase 2: OOM Kill
- OOM Killer가 메모리 최다 사용 프로세스 종료
- PID 1 종료 → 컨테이너 종료
- Exit code: 137 (SIGKILL)

```bash
$ docker inspect test --format '{{.State.OOMKilled}}'
true

$ dmesg | grep -i oom
# Memory cgroup out of memory: Killed process 12345
```

**I/O 제한**

설정:
```bash
$ docker run -d \
  --device-read-bps /dev/sda:10mb \
  --device-write-bps /dev/sda:5mb \
  nginx
```

한계 도달 시:
- I/O 요청 큐에 대기
- read()/write() 블로킹
- 쿼리/로그 쓰기 느림

**PID 제한**

```bash
$ docker run -d --pids-limit 100 nginx
```

한계 도달 시:
- fork() 시스템 콜이 EAGAIN 반환
- 새 프로세스/스레드 생성 불가
- 기존 프로세스는 계속 실행

### 실무 적용

**시나리오: Java OOM Kill 반복**

진단:
```bash
$ docker inspect myapp --format '{{.HostConfig.Memory}}'
536870912  # 512MB

$ docker stats myapp
# MEM: 510MB / 512MB

$ docker inspect myapp --format '{{.State.OOMKilled}}'
true
```

근본 원인:
```bash
$ docker exec myapp java -XX:+PrintFlagsFinal -version | grep HeapSize
# MaxHeapSize = 2147483648  # 2GB!
```

해결:
```dockerfile
FROM eclipse-temurin:17-jre
COPY app.jar /app.jar
ENTRYPOINT ["java", \
  "-XX:+UseContainerSupport", \
  "-XX:MaxRAMPercentage=75.0", \
  "-jar", "/app.jar"]
```

검증:
```bash
$ docker exec myapp java -XX:+PrintFlagsFinal | grep HeapSize
# MaxHeapSize = 402653184  # 384MB (512MB * 0.75)

# 24시간 후
$ docker ps
# myapp  Up 24 hours (healthy)
```
