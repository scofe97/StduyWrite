# 12-system-programming

OS 기초와 시스템 콜을 Go 언어로 실습하며 배우는 학습 프로젝트입니다.

**핵심 원칙**: "시스템 콜을 직접 호출하고 strace로 확인하면 OS가 보인다"

## 구조

```
12-system-programming/
├── learning/
│   ├── 01-syscall-basics.md
│   ├── 02-memory.md
│   ├── 03-network-io.md
│   ├── 04-zero-copy.md
│   ├── 05-netpoll-deep.md
│   └── 06-http-vs-websocket.md
├── practice/
│   ├── 01-syscall-basics/   (3 steps)
│   ├── 02-memory/           (3 steps)
│   ├── 03-network-io/       (3 steps)
│   ├── 04-zero-copy/        (3 steps)
│   └── 05-netpoll-deep/     (3 steps)
├── go.mod
├── go.sum
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 학습 순서

| # | 토픽 | learning | practice | 선수 조건 |
|---|------|----------|----------|----------|
| 1 | System Call Basics | 01 | 01 (3 steps) | 없음 |
| 2 | Memory (mmap) | 02 | 02 (3 steps) | 01 완료 |
| 3 | Zero-Copy | 04 | 04 (3 steps) | 02 완료 |
| 4 | Network I/O | 03, 06 | 03 (3 steps) | 01 완료 |
| 5 | Go netpoll Deep | 05 | 05 (3 steps) | 03, 04 완료 |

## 환경 설정

### Docker 환경 (필수)

strace, epoll 등 Linux 전용 기능을 실습하기 위해 Docker를 사용합니다.

```bash
docker-compose build
docker-compose run --rm lab

# 컨테이너 내부에서 실습
cd practice/01-syscall-basics/step1_open_read
go run main.go

# strace로 시스템 콜 추적
strace -e openat,read,write go run main.go
```

### 의존성

- Go 1.22+
- Docker & Docker Compose
- `golang.org/x/sys/unix` 패키지

## strace 유용한 옵션

```bash
strace -e openat,read,write ./program   # 특정 시스템 콜만
strace -T -e read,write ./program       # 타이밍 포함
strace -c ./program                     # 호출 횟수 통계
strace -f ./program                     # 자식 프로세스 추적
```
