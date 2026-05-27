# 05 - Go netpoll Deep Dive

Go 런타임의 네트워크 I/O 처리 방식을 깊이 이해합니다. 고루틴이 블로킹처럼 보이지만 실제로는 논블로킹으로 동작하는 원리를 체험합니다.

## 소크라테스 질문

실습을 시작하기 전에 다음 질문들을 생각해보세요.

### 질문 1: Go의 conn.Read()가 블로킹처럼 보이는데 어떻게 수천 연결을 처리?

> **힌트**: 고루틴은 OS 스레드가 아닙니다.
>
> 생각해볼 점:
> - 고루틴이 I/O 대기 중일 때 무슨 일이 일어나나요?
> - M:N 스케줄링이란?
> - 블로킹 API + 논블로킹 구현 = ?

### 질문 2: Goroutine이 I/O 대기 중일 때 OS 스레드도 대기하나?

> **힌트**: Go 런타임의 역할을 생각해보세요.
>
> 생각해볼 점:
> - GOMAXPROCS=1일 때 여러 연결을 처리할 수 있을까요?
> - "파킹(parking)"이란?
> - netpoll이 언제 고루틴을 깨우나요?

### 질문 3: GOMAXPROCS와 네트워크 성능의 관계는?

> **힌트**: CPU-bound vs I/O-bound
>
> 생각해볼 점:
> - I/O 대기 중인 고루틴은 CPU를 사용하나요?
> - GOMAXPROCS를 늘리면 네트워크 성능이 선형으로 증가할까요?
> - 어떤 상황에서 GOMAXPROCS가 중요할까요?

## 참고 문서

- [05_Go_System_Integration.md](../../docs/05_Go_System_Integration.md) - Go netpoll 심층
- [03_OS_Fundamentals.md](../../docs/03_OS_Fundamentals.md) - 스케줄링 기초

## 실습 단계

### Step 1: 고루틴 I/O의 실제 동작

**목표**: 블로킹 API가 논블로킹으로 구현되는 것 확인

**위치**: `step1_goroutine_io/main.go`

**핵심 개념**:
- 고루틴 상태: running, runnable, waiting
- I/O 대기 시 고루틴은 "waiting" 상태
- OS 스레드는 다른 고루틴 실행

**검증 방법**:
```bash
# GOMAXPROCS=1로 여러 연결 처리
GOMAXPROCS=1 go run main.go

# 고루틴 상태 확인
GODEBUG=schedtrace=1000 go run main.go
```

---

### Step 2: RawConn으로 저수준 소켓 제어

**목표**: Go의 net 패키지와 raw 시스템 콜 혼합 사용

**위치**: `step2_rawconn/main.go`

**핵심 개념**:
- net.TCPConn.SyscallConn() - raw fd 접근
- RawConn.Control() - 소켓 옵션 설정
- RawConn.Read/Write() - 저수준 I/O

**검증 방법**:
```bash
go run main.go

# strace로 확인
strace -e socket,setsockopt,epoll_ctl go run main.go
```

---

### Step 3: 성능 벤치마크

**목표**: GOMAXPROCS와 연결 수에 따른 성능 측정

**위치**: `step3_benchmark/main.go`

**핵심 개념**:
- 동시 연결 처리량 측정
- GOMAXPROCS 영향 분석
- 고루틴 오버헤드 이해

**검증 방법**:
```bash
# 다양한 GOMAXPROCS로 벤치마크
GOMAXPROCS=1 go run main.go
GOMAXPROCS=2 go run main.go
GOMAXPROCS=4 go run main.go

# 프로파일링
go run main.go -cpuprofile=cpu.prof
go tool pprof cpu.prof
```

## 완료 체크리스트

- [ ] Step 1: GOMAXPROCS=1로 다중 연결 처리 확인
- [ ] Step 1: GODEBUG=schedtrace로 스케줄링 확인
- [ ] Step 2: RawConn으로 소켓 fd 접근
- [ ] Step 2: 저수준 소켓 옵션 설정
- [ ] Step 3: GOMAXPROCS별 성능 차이 측정
- [ ] Step 3: 동시 연결 수에 따른 성능 변화 확인
- [ ] 소크라테스 질문 3개 모두 답변 가능

## 핵심 인사이트

(실습 완료 후 작성하세요)

1. Go의 M:N 스케줄링의 핵심은...
2. netpoll이 고루틴을 깨우는 시점은...
3. GOMAXPROCS 튜닝의 핵심은...
