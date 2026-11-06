---
title: Go 테스트 대역 — 시간 주입·fake clientset·miniredis·kfake
tags: [go, testing, synctest, client-go, miniredis, kfake, franz-go]
status: draft
source:
  - https://go.dev/blog/testing-time
  - https://pkg.go.dev/testing/synctest@go1.25.0
  - https://pkg.go.dev/k8s.io/client-go@v0.37.2/kubernetes/fake
  - https://pkg.go.dev/k8s.io/client-go@v0.37.2/testing
  - https://github.com/alicebob/miniredis/blob/v2.35.0/README.md
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kfake@v0.0.0-20261022190701-123ec885bc97
  - https://github.com/twmb/franz-go/blob/123ec885bc97/pkg/kfake/skipped_features
updated: 2026-11-06
---

# Go 테스트 대역 — 시간 주입·fake clientset·miniredis·kfake

---

> 시계, Kubernetes API, Redis, Kafka를 진짜 대신 가짜로 바꿔 테스트를 빠르고 결정적으로 만들 수 있지만, 가짜마다 흉내 내지 못하는 부분이 정해져 있습니다. 임시 참고 문서이며 정본은 나중에 따로 만듭니다.

## 1. 테스트 대역 네 가지

> 시간은 인터페이스 주입이나 `testing/synctest` 로, 외부 시스템은 같은 프로토콜을 말하는 인메모리 가짜(fake clientset, miniredis, kfake)로 바꿉니다.

### 풀려는 문제

외부 의존을 그대로 두면 단위 테스트가 느리거나 불안정해집니다. 대표적인 네 가지가 있습니다.

- 시간: `time.Sleep(time.Minute)` 이 든 재시도 로직은 테스트 하나에 1분이 걸립니다.
- Kubernetes API: 진짜 클러스터가 있어야 컨트롤러 로직을 시험할 수 있습니다.
- Redis: 서버를 띄우지 않으면 캐시 코드를 시험할 수 없습니다.
- Kafka: 브로커를 띄우지 않으면 발행·소비 코드를 시험할 수 없습니다.

Go 블로그는 시간 의존 테스트를 이렇게 정리합니다. "Tests that use real time are always slow or flaky." 기다림이 짧으면 불안정하고, 길면 느리다는 뜻입니다.

이 문서가 쓴 버전은 Go 1.25.1, client-go v0.37.2, miniredis v2.40.0, go-redis v9.23.0, franz-go v1.22.2 입니다. kfake 는 franz-go 와 따로 버전이 붙는 모듈이며 이 문서는 `v0.0.0-20261022190701-123ec885bc97` 을 썼습니다.

### 시간 주입과 synctest

가장 오래된 방법은 시계를 인터페이스로 받는 것입니다. 운영에서는 진짜 시계를, 테스트에서는 `Sleep` 이 가짜 시간을 앞으로만 보내는 시계를 넣습니다.

```go
type Clock interface {
	Now() time.Time
	Sleep(d time.Duration)
}

type realClock struct{}

func (realClock) Now() time.Time        { return time.Now() }
func (realClock) Sleep(d time.Duration) { time.Sleep(d) }

type fakeClock struct{ now time.Time }

func (f *fakeClock) Now() time.Time        { return f.now }
func (f *fakeClock) Sleep(d time.Duration) { f.now = f.now.Add(d) }

// Poll 은 check 가 참이 될 때까지 every 간격으로 최대 max 번 확인합니다.
func Poll(c Clock, check func() bool, every time.Duration, max int) (int, bool) {
	for i := 1; i <= max; i++ {
		if check() {
			return i, true
		}
		c.Sleep(every)
	}
	return max, false
}

func TestPollWithFakeClock(t *testing.T) {
	// Given — 세 번째 확인에서 참이 되는 조건과 가짜 시계
	clk := &fakeClock{now: time.Unix(0, 0)}
	calls := 0
	check := func() bool { calls++; return calls == 3 }

	// When — 1분 간격으로 폴링
	n, ok := Poll(clk, check, time.Minute, 10)

	// Then — 실제로는 안 기다리고 가짜 시계만 2분 흘렀다
	if !ok || n != 3 || clk.Now().Sub(time.Unix(0, 0)) != 2*time.Minute {
		t.Fatalf("n=%d ok=%v now=%v", n, ok, clk.Now())
	}
}
```

이 방법은 코드를 시계 인터페이스에 맞춰 고쳐야 한다는 비용이 있습니다. Go 1.25 의 `testing/synctest` 는 코드를 고치지 않고 진짜 `time.Sleep` 을 그대로 두고 시간만 가짜로 만듭니다. 블로그는 이 패키지의 이력을 이렇게 적습니다. "In Go 1.24, we introduced the `testing/synctest` package as an experimental package." 이 패키지는 Go 1.25 에서 정식으로 올라왔습니다.

`synctest.Test` 는 함수를 새 거품(bubble) 안에서 실행합니다. 거품 안의 `time` 패키지는 가짜 시계를 쓰고, 거품 안 고루틴이 모두 막히면 시계가 다음 예약 시각으로 점프합니다.

```go
func TestPollWithSynctest(t *testing.T) {
	synctest.Test(t, func(t *testing.T) {
		// Given — 진짜 time.Sleep 을 쓰는 코드, 거품(bubble) 안의 가짜 시간
		start := time.Now()
		calls := 0
		check := func() bool { calls++; return calls == 3 }

		// When — 1분 간격 폴링을 진짜 시계 구현으로 호출
		n, ok := Poll(realClock{}, check, time.Minute, 10)

		// Then — 거품 안 시간이 정확히 2분 흘렀다
		if !ok || n != 3 || time.Since(start) != 2*time.Minute {
			t.Fatalf("n=%d ok=%v elapsed=%v", n, ok, time.Since(start))
		}
	})
}
```

두 테스트 모두 0.00초에 끝났습니다. `synctest` 의 한계는 "durably blocked" 라는 개념에서 나옵니다. 거품 밖의 일이 풀어 줄 수 있는 막힘은 영구적으로 막힌 것이 아니라서 시계가 점프하지 않습니다.

패키지 문서가 드는 예는 `sync.Mutex` 잠금과 네트워크 입출력입니다. 따라서 진짜 소켓을 쓰는 코드는 거품 안에서 시간이 앞으로 가지 않습니다. 이 한계는 아래 miniredis 와 kfake 를 `synctest` 와 함께 쓸 때 부딪히므로 시간은 인터페이스나 가짜 서버의 시간 조작 기능으로 따로 다룹니다.

### fake clientset

client-go 는 진짜 API 서버 없이 쓸 수 있는 가짜 clientset 을 제공합니다. `fake.NewClientset(objects...)` 는 넘긴 객체를 들고 있다가 조회에 그대로 돌려줍니다. 호출은 기록되어 `cs.Actions()` 로 확인할 수 있습니다.

```go
func TestFakeClientset(t *testing.T) {
	// Given — 파드 하나가 미리 들어 있는 fake clientset
	cs := fake.NewClientset(&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "web", Namespace: "default"}})

	// When — 목록 조회
	list, err := cs.CoreV1().Pods("default").List(context.Background(), metav1.ListOptions{})

	// Then — 넣은 객체가 그대로 나오고, 호출 기록이 남는다
	if err != nil || len(list.Items) != 1 {
		t.Fatalf("err=%v items=%d", err, len(list.Items))
	}
	if got := cs.Actions()[0]; !got.Matches("list", "pods") {
		t.Fatalf("action=%v", got)
	}
}
```

실패를 일으키려면 반응자(reactor)를 끼웁니다. 반응자는 호출이 들어오면 순서대로 확인하는 처리기 체인입니다. 문서는 `PrependReactor` 를 "adds a reactor to the beginning of the chain", `AddReactor` 를 "appends a reactor to the end of the chain" 이라고 적습니다. 앞에 끼운 반응자가 `true` 를 돌려주면 체인이 거기서 끝납니다.

```go
func TestFakeClientsetReactor(t *testing.T) {
	// Given — pods 의 get 호출에 실패를 주입하는 반응자
	cs := fake.NewClientset()
	boom := errors.New("api server down")
	cs.PrependReactor("get", "pods", func(k8stesting.Action) (bool, runtime.Object, error) {
		return true, nil, boom
	})

	// When — 파드 조회
	_, err := cs.CoreV1().Pods("default").Get(context.Background(), "web", metav1.GetOptions{})

	// Then — 주입한 오류가 그대로 돌아온다
	if !errors.Is(err, boom) {
		t.Fatalf("err=%v", err)
	}
}
```

`NewClientset` 과 `NewSimpleClientset` 의 차이는 필드 추적입니다. 문서는 "Compared to NewSimpleClientset, the Clientset returned here supports field tracking and thus server-side apply." 라고 적습니다. 새 코드는 `NewClientset` 을 씁니다.

무엇을 흉내 내지 못하는지는 문서의 문장과 직접 돌려 본 결과로 나뉩니다.

- 문서: "without applying any validations and/or defaults" 라고 적혀 있고, "It shouldn't be considered a replacement for a real clientset" 라고 경고합니다.
- 직접 확인(v0.37.2): 이름과 컨테이너가 없는 파드를 `GenerateName` 만 주고 만들면 오류 없이 만들어졌고 `Name`, `UID`, `ResourceVersion` 이 모두 비어 있었습니다. 같은 이름으로 두 번 만들면 `already exists` 가 났습니다.
- 문서에 없고 확인하지 않은 것: RBAC, 어드미션 웹훅, 감시(watch) 이벤트의 정확한 순서 보장.

### miniredis

miniredis 는 순수 Go 로 만든 Redis 테스트 서버입니다. README 는 목적을 한 문장으로 밝힙니다.

> "Sometimes you want to test code which uses Redis, without making it a full-blown integration test."

실제 TCP 로 말하므로 go-redis 같은 평범한 클라이언트를 코드 수정 없이 붙일 수 있습니다.

```go
func TestMiniredisTTL(t *testing.T) {
	// Given — 인메모리 Redis 와 클라이언트, TTL 10초 키
	m := miniredis.RunT(t)
	rdb := redis.NewClient(&redis.Options{Addr: m.Addr()})
	ctx := context.Background()
	if err := rdb.Set(ctx, "k", "v", 10*time.Second).Err(); err != nil {
		t.Fatal(err)
	}

	// When — TTL 이 자동으로 줄지 않으므로 직접 11초 앞으로 보냄
	m.FastForward(11 * time.Second)

	// Then — 키가 만료되었다
	n, err := rdb.Exists(ctx, "k").Result()
	if err != nil || n != 0 {
		t.Fatalf("exists=%d err=%v", n, err)
	}
}
```

시간과 관련해서 가장 중요한 규칙은 TTL 이 저절로 줄지 않는다는 점입니다. README 는 이렇게 적습니다. "Since miniredis is intended to be used in unittests TTLs don't decrease automatically." 모든 TTL 은 `m.FastForward(d)` 로 직접 줄입니다. 줄어서 0 이하가 된 키는 지워집니다.

`SetTime()` 도 있습니다. README 에 따르면 `SetTime()` 은 `TIME` 명령이 돌려주는 값을 정하고, 이 값은 `FastForward` 로는 바뀌지 않고 `SetTime` 으로만 바뀝니다.

흉내 내지 못하는 부분은 README 가 "Commands which will probably not be implemented:" 아래에 적습니다. v2.35.0 README 에서는 `CLUSTER (all)` 아래 `CLUSTER *`, 그리고 `DUMP`, `MIGRATE`, `FUNCTION`, `SAVE`, `SHUTDOWN` 이 거기에 있습니다.

다만 `CLUSTER` 전체가 빠진 것은 아닙니다. 구현 목록의 Cluster 절에 `CLUSTER SLOTS`·`CLUSTER KEYSLOT`·`CLUSTER NODES` 가 있고, v2.40.0 에는 `CLUSTER SHARDS` 도 더해졌습니다. v2.40.0 은 `DUMP` 도 구현 목록으로 옮겼으며 문자열 키만 다룹니다. 서버 `INFO` 와 `COMMAND` 는 일부만 구현되어 있다고 나옵니다. `CLUSTER` 의 나머지 하위 명령이나 영속성이 동작에 영향을 주는 코드는 miniredis 로 시험할 수 없습니다.

### kfake

kfake 는 franz-go 저장소의 가짜 Kafka 브로커입니다. 패키지 문서는 "Package kfake provides a fake Kafka broker for testing." 한 줄로 시작하고, `Cluster` 를 "a mock Kafka broker cluster" 라고 부릅니다. 실제 Kafka 프로토콜로 말하는 브로커를 프로세스 안에서 띄우므로 `kgo` 클라이언트를 그대로 붙입니다.

```go
func TestKfakeProduceConsume(t *testing.T) {
	// Given — 브로커 1대, 파티션 1개짜리 토픽 "events"
	c, err := kfake.NewCluster(kfake.NumBrokers(1), kfake.SeedTopics(1, "events"))
	if err != nil {
		t.Fatal(err)
	}
	defer c.Close()
	cl, err := kgo.NewClient(
		kgo.SeedBrokers(c.ListenAddrs()...),
		kgo.ConsumeTopics("events"),
		kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
	)
	if err != nil {
		t.Fatal(err)
	}
	defer cl.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// When — 한 건 발행 후 읽기
	if err := cl.ProduceSync(ctx, &kgo.Record{Topic: "events", Value: []byte("hello")}).FirstErr(); err != nil {
		t.Fatal(err)
	}
	fetches := cl.PollFetches(ctx)

	// Then — 같은 값이 돌아온다
	if err := fetches.Err(); err != nil {
		t.Fatal(err)
	}
	got := fetches.Records()
	if len(got) != 1 || string(got[0].Value) != "hello" {
		t.Fatalf("records=%v", got)
	}
}
```

접속 주소는 `ListenAddrs()` 로 얻습니다. 문서는 "returns the hostports that the cluster is listening on" 라고 적습니다. 옵션으로는 `NumBrokers`, `SeedTopics`, `DefaultNumPartitions`, `EnableSASL` 같은 것이 있습니다.

패키지 문서에는 지원 범위 목록이 없습니다. 대신 모듈 안의 `skipped_features` 파일이 의도적으로 구현하지 않은 기능을 적어 둡니다. 이 파일은 맨 위에서 "kfake does not implement throttling, and writes are immediate (no replication)" 이라고 밝힙니다. 그 아래에는 다음이 나옵니다.

- 랙 인식 읽기(KIP-392)와 로그 잘림 감지는 구현하지 않았습니다.
- 티어드 스토리지(KIP-405)의 일부 오프셋 조회는 구현하지 않았습니다.
- 공유 그룹 코디네이터 일부(KIP-932)는 구현하지 않았습니다.

복제가 없으므로 브로커 장애 때 리더 전환이나 데이터 유실 같은 동작은 kfake 로 시험할 수 없습니다. 파일 안의 항목은 개발 중에 바뀌므로 지금 쓰는 버전의 파일을 직접 확인합니다.

### 흔한 함정

- fake clientset 이 통과했다고 해서 매니페스트가 클러스터에서 받아들여진다는 뜻은 아닙니다. 검증과 기본값 채움이 없어서 잘못된 객체도 통과합니다. 실제 검증은 통합 테스트나 `envtest` 같은 진짜 API 서버가 맡아야 합니다. (`envtest` 는 이 문서에서 열어 본 문서가 아니므로 이름만 적습니다.)
- miniredis 에서 만료를 기다리는 `time.Sleep` 을 쓰면 테스트가 영원히 통과하지 않습니다. TTL 이 자동으로 줄지 않기 때문입니다. `FastForward` 를 씁니다.
- `synctest` 거품 안에서 진짜 소켓(miniredis·kfake 접속)을 쓰면 시계가 점프하지 않습니다. 문서가 네트워크 입출력을 영구 막힘에서 제외하기 때문입니다.
- `synctest` 는 Go 1.25 부터 정식입니다. Go 1.24 에서는 실험 기능이므로 빌드 환경의 Go 버전을 먼저 확인합니다.
- 가짜는 같은 인터페이스를 흉내 낼 뿐 같은 동시성 동작을 보장하지 않습니다. 순서나 지연에 민감한 버그는 진짜 시스템에서 다시 확인합니다.

### 공식 문서 근거

| 출처 | 확인한 문장 | 이 문서에서 쓴 곳 |
|------|------------|------------------|
| Go 블로그 testing-time | "Tests that use real time are always slow or flaky." | 풀려는 문제 |
| Go 블로그 testing-time | "In Go 1.24, we introduced the `testing/synctest` package as an experimental package." | synctest 버전 |
| `testing/synctest` | "Test executes f in a new bubble." | 거품 개념 |
| `testing/synctest` | "A goroutine which can be unblocked by an event from outside its bubble is not durably blocked." | 시계 점프 한계 |
| client-go fake | "Compared to NewSimpleClientset, the Clientset returned here supports field tracking and thus server-side apply." | NewClientset 선택 |
| client-go fake | "It shouldn't be considered a replacement for a real clientset" | 한계 |
| client-go testing | "PrependReactor adds a reactor to the beginning of the chain." | 반응자 |
| miniredis README | "Since miniredis is intended to be used in unittests TTLs don't decrease automatically." | TTL 규칙 |
| miniredis README | "Commands which will probably not be implemented:" | 못 흉내 내는 명령 |
| kfake 패키지 문서 | "Package kfake provides a fake Kafka broker for testing." | 정의 |
| kfake `skipped_features` | "kfake does not implement throttling, and writes are immediate (no replication)." | 복제 없음 |

miniredis 는 v2.35.0 태그의 README 를 열었고 예제는 v2.40.0 으로 돌렸습니다. kfake 의 `skipped_features` 는 모듈 소스에서 직접 읽었으며 frontmatter 의 주소는 같은 커밋의 GitHub 경로입니다.
