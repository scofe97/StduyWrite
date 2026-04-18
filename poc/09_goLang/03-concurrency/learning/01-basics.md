# Stage 04: 동시성 학습 정리

## 1. Goroutine 기초

### 생성
```go
go func() {
    fmt.Println("goroutine에서 실행")
}()
```

### 주의: main이 먼저 끝나면 goroutine도 종료
```go
func main() {
    go fmt.Println("출력 안 될 수도!")
    // main 끝 → 프로그램 종료
}
```

---

## 2. Goroutine vs Thread

| 구분 | Java Thread | Go Goroutine |
|------|-------------|--------------|
| 메모리 | ~1MB 스택 | ~2KB 스택 |
| 생성 비용 | 무거움 (OS 호출) | 가벼움 (Go 런타임) |
| 스케줄링 | OS 커널 | Go 런타임 (M:N) |
| 동시 실행 | 수천 개 한계 | 수십만 개 가능 |

---

## 3. Goroutine 대기 방법

### 방법 1: sync.WaitGroup
```go
var wg sync.WaitGroup

wg.Add(1)
go func() {
    defer wg.Done()
    // 작업
}()

wg.Wait()  // 모든 goroutine 완료 대기
```

### 방법 2: Channel
```go
ch := make(chan string)

go func() {
    ch <- "완료"  // 전송
}()

result := <-ch  // 수신 (블로킹)
```

---

## 4. Channel

### 생성
```go
ch := make(chan int)       // 버퍼 없음
ch := make(chan int, 10)   // 버퍼 10개
```

### 전송/수신
```go
ch <- 42      // 전송
value := <-ch // 수신
```

### 버퍼 없는 채널 vs 버퍼 있는 채널

| 구분 | 버퍼 없음 | 버퍼 있음 |
|------|----------|----------|
| 전송 | 수신자 있어야 진행 | 버퍼 공간 있으면 진행 |
| 동기화 | 동기식 | 비동기식 |
| 용도 | 핸드셰이크 | 작업 큐 |

---

## 5. 병렬 실행 패턴

### 잘못된 방법 (순차 실행)
```go
go func() {
    for _, p := range providers {
        fetchRepos(p, ch)  // 순차!
    }
}()
```

### 올바른 방법 (병렬 실행)
```go
for _, p := range providers {
    go fetchRepos(p, ch)  // 각각 goroutine!
}

// 결과 수신
for i := 0; i < len(providers); i++ {
    result := <-ch
    fmt.Println(result)
}
```

---

## 6. 병렬 실행 효과

```
순차 실행: 1초 + 1.5초 + 1.2초 = 3.7초
병렬 실행: max(1초, 1.5초, 1.2초) = 1.5초
```

---

## 7. 원본 프로젝트 적용

### cmd/server/main.go
```go
func main() {
    go startGRPCServer()    // goroutine
    go startRESTGateway()   // goroutine

    // 시그널 대기 (Graceful shutdown)
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
}
```

gRPC 서버와 REST Gateway를 **동시에** 실행!

---

## 실습 파일

| 파일 | 내용 |
|------|------|
| `gofunc.go` | WaitGroup, Channel, Worker 실험 |
| `fetcher.go` | API 호출 시뮬레이션 |
| `main.go` | 병렬 API 호출 테스트 |

---

## 핵심 정리

1. `go func()` → goroutine 생성
2. `sync.WaitGroup` → 여러 goroutine 대기
3. `chan` → goroutine 간 통신
4. 병렬 실행 → 각각 `go`로 호출
5. 버퍼 채널 → 비동기 큐 역할

---

## 과제

### 과제 1: Goroutine 기초
`practices/01-goroutine-basic/main.go`에서 goroutine을 생성하고 실행해보세요.

### 과제 2: WaitGroup 동기화
`practices/02-waitgroup/main.go`에서 WaitGroup을 사용하여 여러 goroutine을 동기화하세요.

### 과제 3: Channel 기초
`practices/03-channel-basic/main.go`에서 채널로 데이터를 주고받아보세요.

### 과제 4: 병렬 API 호출
`practices/04-parallel-fetch/main.go`에서 여러 API를 병렬로 호출하세요.
