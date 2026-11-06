---
title: 최신값만 전달하는 채널 — 버퍼 1·drop-oldest
tags: [go, channel, select, concurrency, drop-oldest]
status: draft
source:
  - https://go.dev/ref/spec  # (2026-11-06 확인)
  - https://go.dev/blog/pipelines
  - https://pkg.go.dev/sync@go1.25.0#Cond
  - https://pkg.go.dev/sync/atomic@go1.25.0#Value
  - https://pkg.go.dev/context@go1.25.0
updated: 2026-11-06
---

# 최신값만 전달하는 채널 — 버퍼 1·drop-oldest

---

> 느린 소비자에게 옛 값을 쌓지 않으려면 버퍼 1짜리 채널과 뮤텍스로 감싼 drop-oldest 발행 함수를 씁니다. 임시 참고 문서이며 정본은 나중에 따로 만듭니다.

## 1. 버퍼 1 채널과 drop-oldest

> 채널 버퍼를 1로 두고 발행자가 꽉 찬 버퍼의 옛 값을 꺼내 버린 뒤 새 값을 넣으면, 발행자는 막히지 않고 소비자는 항상 최신 값을 받습니다.

### 풀려는 문제

센서 값, 화면 상태, 설정 스냅샷처럼 새 값이 나오면 옛 값은 의미가 없는 데이터가 있습니다. 이런 값을 보통 채널로 보내면 두 가지 중 하나가 깨집니다.

- 버퍼 없는 채널: 소비자가 느리면 발행자가 `send` 에서 막혀 생산 쪽까지 느려집니다. 명세는 "A send on an unbuffered channel can proceed if a receiver is ready." 라고 적습니다.
- 버퍼 큰 채널: 발행자는 막히지 않지만 소비자는 오래된 값부터 차례로 읽습니다. 지금 시점의 값을 보려고 해도 큐에 쌓인 옛 값을 먼저 비워야 합니다.

원하는 동작은 "발행은 절대 막히지 않고, 읽을 때는 가장 최근 값만 보인다" 입니다. 이를 drop-oldest 라고 부릅니다. 버퍼가 가득 찼을 때 가장 오래된 값을 버리는 정책이라는 뜻입니다.

### 동작 원리

명세는 버퍼 채널의 규칙을 이렇게 적습니다. 용량이 있으면 버퍼가 차지 않은 동안 `send` 가 막히지 않습니다. 명세는 "communication succeeds without blocking if the buffer is not full (sends) or not empty (receives)" 라고 적습니다. 용량이 1이면 값 하나가 들어 있을 때 다음 `send` 는 막힙니다.

여기에 `select` 의 `default` 를 붙이면 막히는 대신 다른 일을 할 수 있습니다. 명세의 `select` 실행 규칙은 "Otherwise, if there is a default case, that case is chosen." 입니다. 어느 통신도 진행할 수 없을 때만 `default` 로 넘어간다는 뜻입니다.

두 규칙을 합치면 발행 함수의 순서가 나옵니다.

1. `select` 로 비막힘 `send` 를 시도합니다. 버퍼가 비어 있으면 성공하고 끝납니다.
2. 실패하면 `select` 로 비막힘 `receive` 를 시도해 옛 값을 꺼내 버립니다. 그 사이 소비자가 먼저 가져갔다면 `default` 로 빠집니다.
3. 1번으로 돌아가 다시 넣습니다.

### 뮤텍스가 필요한 이유

위 순서를 발행자 한 개만 쓰면 뮤텍스가 필요 없습니다. 발행자가 둘 이상이면 2번과 3번 사이에 다른 발행자가 끼어들어 버퍼를 다시 채울 수 있습니다. 이때 3번을 막히는 `send` (`ch <- v`) 로 쓰면, 먼저 비웠던 발행자가 가득 찬 버퍼 앞에서 소비자가 읽어 줄 때까지 막힙니다.

이 현상은 데이터 경쟁(data race)이 아니라 막힘입니다. 채널 연산은 그 자체로 동기화되므로 `go test -race` 는 이 문제를 잡지 않습니다. 이 문서의 실험에서 아래의 뮤텍스 없는 변형은 발행자 4개, 각 10만 번 발행으로 3번 모두 3초 안에 끝나지 않았습니다.

뮤텍스로 "비우고 넣기" 전체를 감싸면 발행자끼리 직렬화되어 이 틈이 사라집니다. 소비자는 뮤텍스를 쓰지 않고 읽기만 하므로 소비자가 끼어들어도 안전합니다. 소비자는 값을 꺼내기만 할 수 있어서, 비운 뒤에는 늘 자리가 있기 때문입니다. 위 순서에서 3번을 `for` 반복의 재시도로 쓴 것은 이 가정이 깨져도 막히지 않게 하는 보험입니다.

### 최소 예제

일반 제네릭 래퍼입니다. 발행자 4개가 동시에 4,000번 발행하고, 1ms 쉬는 느린 소비자가 읽습니다.

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// Latest 는 가장 최근 값 하나만 보관하는 채널 래퍼입니다.
type Latest[T any] struct {
	mu sync.Mutex // 발행자끼리 "비우고 넣기" 를 직렬화합니다.
	ch chan T
}

func NewLatest[T any]() *Latest[T] {
	return &Latest[T]{ch: make(chan T, 1)}
}

// Publish 는 버퍼가 차 있으면 옛 값을 버리고 v 를 넣습니다. 절대 막히지 않습니다.
func (l *Latest[T]) Publish(v T) {
	l.mu.Lock()
	defer l.mu.Unlock()
	for {
		select {
		case l.ch <- v:
			return
		default:
		}
		select {
		case <-l.ch: // 옛 값을 꺼내 버립니다.
		default: // 그 사이 소비자가 먼저 가져갔습니다.
		}
	}
}

// C 는 소비자가 읽는 쪽입니다.
func (l *Latest[T]) C() <-chan T { return l.ch }

func main() {
	l := NewLatest[int]()

	var wg sync.WaitGroup
	for p := 0; p < 4; p++ { // 발행자 4개가 동시에 발행합니다.
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < 1000; i++ {
				l.Publish(p*1000 + i)
			}
		}()
	}

	done := make(chan struct{})
	received := 0
	go func() { // 느린 소비자입니다.
		defer close(done)
		for {
			select {
			case <-l.C():
				received++
				time.Sleep(time.Millisecond)
			case <-time.After(50 * time.Millisecond):
				return
			}
		}
	}()

	wg.Wait()
	<-done
	fmt.Println("발행 4000, 수신", received)
}
```

Go 1.25.1 에서 `go vet` 과 `go run -race` 를 통과했고 출력은 `발행 4000, 수신 4` 였습니다. 수신 횟수는 실행마다 다릅니다. 소비자가 느릴수록 건너뛰는 값이 늘어나는 것이 이 패턴의 의도된 동작입니다.

뮤텍스를 뺀 변형은 이렇게 막힙니다.

```go
func publish(ch chan int, v int) {
	select {
	case ch <- v:
	default:
		select {
		case <-ch:
		default:
		}
		ch <- v // 다른 발행자가 그 사이 채웠다면 여기서 영원히 막힙니다.
	}
}
```

### 대안과 비교

세 가지 대안은 "값을 전달하는 것" 과 "새 값이 왔다고 알리는 것" 중 어느 쪽을 맡는지가 서로 다릅니다.

- `sync.Cond`: 값과 조건 변수를 직접 관리합니다. `Wait` 는 락을 풀고 잠들었다가 깨어나면 락을 다시 잡으므로, 호출하는 쪽이 `for` 로 조건을 다시 검사해야 합니다. 문서는 단순한 경우 `Cond` 보다 채널이 낫다고 적습니다. 문서에는 "users will be better off using channels than a Cond" 라는 문장이 있습니다. `Broadcast` 는 채널 닫기에, `Signal` 은 채널로 보내기에 대응합니다.
- `atomic.Value` 또는 `atomic.Pointer[T]`: 최신 값을 락 없이 저장하고 읽습니다. 소비자는 값이 바뀌었는지 알림을 받지 못하므로 주기적으로 읽어야 합니다. 값이 바뀔 때마다 깨어나야 한다면 채널이나 `Cond` 가 필요합니다. `atomic.Value` 는 같은 구체 타입만 `Store` 할 수 있고, 일관되지 않은 타입이나 `Store(nil)` 은 panic 입니다.
- `context`: 취소 신호와 마감 시각, 요청 범위 값을 전달하는 도구입니다. 문서는 범위를 "carries deadlines, cancellation signals, and other request-scoped values" 로 정합니다. 연속으로 갱신되는 데이터를 나르는 용도가 아니므로 이 패턴의 대안이 아닙니다. 대신 이 패턴의 소비자 루프를 멈출 때 `ctx.Done()` 를 같은 `select` 에 넣어 함께 씁니다.

선택 기준은 다음과 같습니다. 읽을 때만 최신 값이 필요하면 `atomic.Pointer[T]` 가 가장 단순합니다. 새 값이 올 때마다 소비자를 깨워야 하면 이 문서의 버퍼 1 채널이 맞습니다. 여러 소비자를 한꺼번에 깨워야 하면 `Cond.Broadcast` 를 씁니다. 버퍼 1 채널은 값 하나를 소비자 한 명만 받기 때문입니다.

`Cond` 와 `atomic.Pointer` 를 쓴 짧은 예도 `go vet` 과 `go run -race` 를 통과했습니다.

```go
type Snapshot struct{ N int }

var latest atomic.Pointer[Snapshot]

// 쓰기: latest.Store(&Snapshot{N: 1})
// 읽기: latest.Load().N  (Store 전에는 nil 이므로 nil 검사 필요)

type Box struct {
	mu  sync.Mutex
	c   *sync.Cond
	v   int
	gen uint64
}

func (b *Box) Set(v int) {
	b.mu.Lock()
	b.v = v
	b.gen++
	b.mu.Unlock()
	b.c.Broadcast()
}

func (b *Box) Wait(seen uint64) (int, uint64) {
	b.mu.Lock()
	defer b.mu.Unlock()
	for b.gen == seen { // Wait 는 깨어나도 조건이 참이라는 보장이 없습니다.
		b.c.Wait()
	}
	return b.v, b.gen
}
```

### 흔한 함정

가장 위험한 함정은 모든 이벤트가 필요한 곳에 이 패턴을 쓰는 것입니다. 결제 완료, 주문 접수, 감사 로그처럼 하나라도 빠지면 안 되는 이벤트는 drop-oldest 가 조용히 버립니다. 이 패턴은 "다음 값이 이전 값을 대체한다" 는 의미가 있는 상태 값에만 씁니다.

그 밖의 함정은 다음과 같습니다.

- 뮤텍스를 빼고 마지막 `send` 를 막히는 `ch <- v` 로 쓰기. 위 실험처럼 발행자가 막히는데 `-race` 는 아무것도 보고하지 않습니다.
- 채널을 닫는 책임이 모호함. 닫힌 채널에 `send` 하면 run-time panic 이므로 발행자 쪽이 닫을 때는 뮤텍스 안에서 닫힘 여부를 확인해야 합니다. 이 문서의 예제는 채널을 닫지 않고 소비자가 `ctx` 나 타이머로 끝납니다.
- 소비자가 값을 읽은 뒤 처리 중에 새 값이 오면 그 값은 다음 읽기 때 받습니다. 처리 중 도착한 값을 즉시 보고 싶다면 이 패턴이 아니라 별도 취소 신호를 설계해야 합니다.
- 소비자가 여럿이면 값 하나를 한 소비자만 받습니다. 모두가 같은 최신 값을 봐야 하면 `atomic.Pointer` 로 읽거나 `Cond.Broadcast` 를 씁니다.

### 공식 문서 근거

| 출처 | 확인한 문장 | 이 문서에서 쓴 곳 |
|------|------------|------------------|
| Go 명세 Channel types | "The capacity, in number of elements, sets the size of the buffer in the channel." | 버퍼 용량의 뜻 |
| Go 명세 Channel types | "communication succeeds without blocking if the buffer is not full (sends) or not empty (receives)" | 버퍼 1의 막힘 조건 |
| Go 명세 Select statements | "Otherwise, if there is a default case, that case is chosen." | 비막힘 연산 |
| Go 명세 Send statements | "A send on a closed channel proceeds by causing a run-time panic." | 닫기 함정 |
| Go 블로그 pipelines | "Goroutines are not garbage collected; they must exit on their own." | 막힌 발행자의 위험 |
| `sync.Cond` | "users will be better off using channels than a Cond" | 대안 비교 |
| `atomic.Value` | "A Value provides an atomic load and store of a consistently typed value." | 대안 비교 |
| `context` | "carries deadlines, cancellation signals, and other request-scoped values" | 대안 비교 |

주소는 명세와 블로그가 https://go.dev/ref/spec (2026-11-06 확인) 과 https://go.dev/blog/pipelines 입니다. 패키지 문서는 Go 1.25.0 고정 주소인 https://pkg.go.dev/sync@go1.25.0#Cond, https://pkg.go.dev/sync/atomic@go1.25.0#Value, https://pkg.go.dev/context@go1.25.0 입니다.
