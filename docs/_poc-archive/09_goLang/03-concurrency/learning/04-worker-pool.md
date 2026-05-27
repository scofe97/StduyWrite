# Worker Pool 패턴 학습

동시성 패턴을 활용한 워커 풀과 작업 분산을 학습합니다.

---

## 학습 목표

- Worker pool 구현
- errgroup을 사용한 에러 처리
- Semaphore 패턴으로 동시성 제한
- Fan-out/Fan-in 패턴

---

## 1. Worker Pool 개념

### Worker Pool이란?
고정된 수의 워커(goroutine)가 작업 큐에서 작업을 가져와 처리하는 패턴입니다.

```
[작업 큐] → [Worker 1] ↘
           [Worker 2] → [결과]
           [Worker 3] ↗
```

### 왜 필요한가?
- **리소스 제한**: 무제한 goroutine 생성 방지
- **백프레셔**: 시스템 과부하 방지
- **예측 가능성**: 동시 실행 수 제어

### 기본 구현
```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- job * 2  // 작업 처리
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // 워커 3개 시작
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // 작업 전송
    for j := 1; j <= 9; j++ {
        jobs <- j
    }
    close(jobs)

    // 결과 수집
    for a := 1; a <= 9; a++ {
        <-results
    }
}
```

---

## 2. errgroup

### golang.org/x/sync/errgroup
```bash
go get golang.org/x/sync/errgroup
```

고루틴 그룹 관리 및 에러 수집을 위한 패키지입니다.

### 기본 사용법
```go
import "golang.org/x/sync/errgroup"

func main() {
    g, ctx := errgroup.WithContext(context.Background())

    urls := []string{"url1", "url2", "url3"}

    for _, url := range urls {
        url := url  // 클로저 캡처
        g.Go(func() error {
            return fetch(ctx, url)
        })
    }

    // 모든 goroutine 완료 대기, 첫 번째 에러 반환
    if err := g.Wait(); err != nil {
        log.Fatal(err)
    }
}
```

### 특징
- 첫 번째 에러 발생 시 context 취소
- 모든 goroutine 완료 대기
- 에러 수집 및 반환

---

## 3. Semaphore

### golang.org/x/sync/semaphore
```bash
go get golang.org/x/sync/semaphore
```

동시 실행 수를 제한하는 패키지입니다.

### 기본 사용법
```go
import "golang.org/x/sync/semaphore"

func main() {
    ctx := context.Background()
    sem := semaphore.NewWeighted(3)  // 동시 3개 제한

    for i := 0; i < 10; i++ {
        // 슬롯 획득 (블로킹)
        sem.Acquire(ctx, 1)

        go func(i int) {
            defer sem.Release(1)  // 슬롯 반환
            process(i)
        }(i)
    }
}
```

### 채널로 구현한 세마포어
```go
sem := make(chan struct{}, 3)  // 버퍼 3개 = 동시 3개

for i := 0; i < 10; i++ {
    sem <- struct{}{}  // 슬롯 획득
    go func(i int) {
        defer func() { <-sem }()  // 슬롯 반환
        process(i)
    }(i)
}
```

---

## 4. Fan-out/Fan-in 패턴

### Fan-out
하나의 입력을 여러 goroutine으로 분산합니다.

```go
func fanOut(input <-chan int, n int) []<-chan int {
    outputs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}
```

### Fan-in
여러 채널의 결과를 하나로 합칩니다.

```go
func fanIn(inputs ...<-chan int) <-chan int {
    output := make(chan int)
    var wg sync.WaitGroup

    for _, ch := range inputs {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                output <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(output)
    }()

    return output
}
```

---

## 프로젝트 구조

```
03-worker-pool/
├── STUDY.md           # 이 파일
├── README.md          # 개요
├── go.mod
├── pool/              # 워커 풀 구현
├── patterns/          # Fan-out/Fan-in 패턴
├── crawler/           # 웹 크롤러 예제
└── practices/         # 실습 디렉토리
```

---

## 과제

### 과제 1: 기본 워커 풀
`practices/01-simple-worker/main.go`에서 기본 워커 풀을 구현하세요.

### 과제 2: errgroup 에러 처리
`practices/02-errgroup/main.go`에서 errgroup으로 에러를 처리하세요.

### 과제 3: Semaphore 동시성 제한
`practices/03-semaphore/main.go`에서 동시 실행 수를 제한하세요.

### 과제 4: Fan-out/Fan-in
`practices/04-fan-out-in/main.go`에서 Fan-out/Fan-in 패턴을 구현하세요.

---

## 참조 자료

### 📚 Learning Go, 2nd Edition
- **12_Concurrency_in_Go.md**: 고루틴, 채널, select, WaitGroup
- **14_The_Context.md**: 워커 취소, 타임아웃 처리
- **09_Errors.md**: errgroup과 에러 수집 패턴
