---
title: franz-go — kgo·kadm·컨슈머 lag
tags: [go, kafka, franz-go, kgo, kadm, consumer-lag]
status: draft
source:
  - https://github.com/twmb/franz-go/blob/v1.22.2/README.md
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0
---

# franz-go — kgo·kadm·컨슈머 lag

---

> franz-go 는 순수 Go 로 만든 Kafka 클라이언트이고, 컨슈머 lag 은 `kadm` 이 그룹의 커밋 오프셋과 파티션 끝 오프셋의 차이로 계산해 줍니다. 임시 참고 문서이며 정본은 나중에 따로 만듭니다.

## 1. kgo 클라이언트와 kadm 의 lag

> `kgo` 가 발행과 소비를 맡고, 같은 클라이언트를 `kadm.NewClient` 에 넘기면 그룹 상태와 lag 을 조회하는 관리 API 가 생깁니다.

### 풀려는 문제

Kafka 를 Go 로 쓸 때는 두 가지가 필요합니다. 하나는 발행하고 소비하는 클라이언트이고, 다른 하나는 소비가 얼마나 밀렸는지 보는 도구입니다.

lag 이 없으면 소비자가 살아 있는데도 처리가 뒤처지는 상황을 알 수 없습니다. 모니터링 대시보드가 Kafka 소비 지연을 보여 주려면 브로커에서 그룹의 커밋 위치와 끝 위치를 직접 읽어 빼야 합니다.

franz-go README 는 프로젝트를 한 문장으로 소개합니다.

> "Franz-go is an all-encompassing Apache Kafka client fully written in Go."

기능 목록에는 "Written in pure Go (no wrapper lib for a C library or other bindings)" 도 있습니다.

패키지는 역할별로 나뉩니다. README 의 설명은 다음과 같습니다.

- `kgo`: "The main client is located in the package `github.com/twmb/franz-go/pkg/kgo`"
- `kadm`: "A high-level admin package with many helper types to make cluster administration easy"
- `kmsg`: "The raw-protocol package is released from `pkg/kmsg`"
- `kfake`: README 에는 나오지 않으며 패키지 문서가 가짜 브로커로 소개합니다. 테스트 쪽 사용은 같은 폴더의 테스트 대역 문서에서 다룹니다.

이 문서가 쓴 버전은 Go 1.25.1, franz-go v1.22.2, kadm v1.19.0 입니다. `kadm` 은 별도 모듈이라 버전이 따로 붙습니다.

### 클라이언트 생성과 발행

`kgo.NewClient` 는 옵션을 받아 클라이언트를 만듭니다. 문서에 따르면 브로커 연결은 요청을 보낼 때 처음 만들어집니다. 문서는 "Connections to brokers are lazily created only when requests are written to them." 라고 적습니다. 그래서 `NewClient` 가 성공해도 브로커가 살아 있다는 뜻은 아닙니다.

`NewClient` 는 토픽 메타데이터를 주기적으로 갱신하는 고루틴도 띄웁니다. 그래서 쓰고 난 클라이언트는 `Close` 로 닫아야 합니다.

`ProduceSync` 는 모든 레코드가 발행될 때까지 기다린 뒤 돌아오는 동기 발행입니다. 문서는 "This function produces all records and waits for them all to be produced before returning." 라고 적습니다. 결과의 오류는 `FirstErr()` 로 확인합니다.

```go
prod, err := kgo.NewClient(
	kgo.SeedBrokers(brokers...),
	kgo.DefaultProduceTopic("orders"),
)
if err != nil {
	return err
}
defer prod.Close()

rec := &kgo.Record{Value: []byte("hello")}
if err := prod.ProduceSync(ctx, rec).FirstErr(); err != nil {
	return err
}
```

### 컨슈머 그룹과 커밋

그룹 소비는 `kgo.ConsumerGroup` 으로 켭니다. 같은 그룹 이름을 쓰는 클라이언트들이 파티션을 나눠 맡습니다. 기본 동작을 알아 두어야 합니다. 문서는 "when group consuming, the default is to autocommit every 5s." 라고 적고, 자동 커밋은 직전에 poll 한 것까지만 커밋한다고 설명합니다.

자동 커밋이 이전 poll 만 커밋하므로 최소 한 번 처리(at-least-once)가 보장됩니다. 대신 리밸런스 중에 중복 처리가 생길 수 있습니다. 종료할 때는 마지막으로 동기 커밋을 한 번 해야 합니다. 문서가 직접 이렇게 권합니다. 종료 후에는 다시 poll 하지 않고 자동 커밋을 기다리지도 않기 때문입니다.

처리가 끝난 뒤에만 커밋하고 싶으면 `DisableAutoCommit` 으로 자동 커밋을 끄고 `CommitUncommittedOffsets` 를 호출합니다. 문서는 권장 패턴을 "have a poll / process / commit loop" 로 적습니다. 리밸런스 도중 내가 더는 소유하지 않는 파티션에 커밋하는 문제는 `BlockRebalanceOnPoll` 로 막을 수 있습니다. 이 옵션을 켜면 `AllowRebalance` 를 호출할 때까지 리밸런스가 미뤄집니다.

```go
func Consume(ctx context.Context, brokers []string, group, topic string, handle func(*kgo.Record) error) error {
	cl, err := kgo.NewClient(
		kgo.SeedBrokers(brokers...),
		kgo.ConsumerGroup(group),
		kgo.ConsumeTopics(topic),
		kgo.DisableAutoCommit(),
		kgo.BlockRebalanceOnPoll(),
	)
	if err != nil {
		return err
	}
	defer cl.Close()

	for {
		fetches := cl.PollFetches(ctx)
		if errors.Is(fetches.Err0(), context.Canceled) || fetches.IsClientClosed() {
			return ctx.Err()
		}
		if errs := fetches.Errors(); len(errs) > 0 {
			return errs[0].Err
		}
		var herr error
		fetches.EachRecord(func(r *kgo.Record) {
			if herr == nil {
				herr = handle(r)
			}
		})
		if herr != nil {
			cl.AllowRebalance()
			return herr
		}
		if err := cl.CommitUncommittedOffsets(ctx); err != nil {
			cl.AllowRebalance()
			return err
		}
		cl.AllowRebalance()
	}
}
```

`PollFetches` 의 문서는 파티션 오류를 모두 확인하라고 강조합니다. 문서는 "It is important to check all partition errors in the returned fetches." 라고 적습니다. 위 예제가 `fetches.Errors()` 를 확인하는 이유입니다.

### 컨슈머 lag 계산

lag 은 파티션 끝 오프셋에서 그룹이 커밋한 오프셋을 뺀 값입니다. `kadm` 의 `GroupMemberLag` 문서는 이를 "the lag between a group member's current offset commit and the current end offset" 이라고 정의합니다. 끝 오프셋은 Kafka 용어로 high watermark 입니다. `ListEndOffsets` 문서가 "In Kafka terms, this returns high watermarks." 라고 연결해 줍니다.

가장 쉬운 방법은 `Client.Lag` 입니다. 문서는 이 함수를 lag 계산에 필요한 여러 요청을 묶은 지름길로 설명합니다.

```go
adm := kadm.NewClient(prod) // kgo 클라이언트를 그대로 넘깁니다.
lags, err := adm.Lag(ctx, "g1")
if err != nil {
	return err
}
l := lags["g1"]
if err := l.Error(); err != nil { // 그룹별 오류는 값 안에 들어 있습니다.
	return err
}
fmt.Println(l.Lag.Total()) // 그룹 전체 lag
```

`Lag` 가 돌려주는 값은 그룹 이름을 키로 하는 맵입니다. 그룹을 설명하지 못했거나 오프셋을 가져오지 못했다면 해당 그룹 값의 `DescribeErr`, `FetchErr` 에 오류가 담깁니다. 그래서 함수의 `err` 가 `nil` 이어도 그룹별로 `Error()` 를 확인해야 합니다.

파티션 단위로 보려면 `GroupLag` 의 `Sorted()` 나 `Lookup(topic, partition)` 을 씁니다. 각 항목 `GroupMemberLag` 에는 `Commit`, `End`, `Lag` 필드가 있고, 오류가 있으면 `Lag` 은 -1 이 되고 `Err` 가 채워집니다. 토픽별 합계는 `TotalByTopic()` 입니다.

직접 계산하려면 `FetchOffsets(ctx, group)` 로 커밋 오프셋을, `ListEndOffsets(ctx, topics...)` 로 끝 오프셋을 읽어 뺍니다. 아래 테스트는 kfake 가짜 브로커에 10건을 발행하고 그룹 컨슈머가 4건을 커밋한 뒤, 두 방법이 모두 6을 돌려주는지 확인합니다.

```go
func TestConsumerLag(t *testing.T) {
	// Given — 파티션 1개 토픽에 10건을 발행하고, 그룹 컨슈머가 4건만 읽어 커밋한 상태
	c, err := kfake.NewCluster(kfake.NumBrokers(1), kfake.SeedTopics(1, "orders"))
	if err != nil {
		t.Fatal(err)
	}
	defer c.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
	defer cancel()

	prod, err := kgo.NewClient(kgo.SeedBrokers(c.ListenAddrs()...), kgo.DefaultProduceTopic("orders"))
	if err != nil {
		t.Fatal(err)
	}
	defer prod.Close()
	for i := 0; i < 10; i++ {
		rec := &kgo.Record{Value: []byte(fmt.Sprintf("m%d", i))}
		if err := prod.ProduceSync(ctx, rec).FirstErr(); err != nil {
			t.Fatal(err)
		}
	}

	cons, err := kgo.NewClient(
		kgo.SeedBrokers(c.ListenAddrs()...),
		kgo.ConsumerGroup("g1"),
		kgo.ConsumeTopics("orders"),
		kgo.DisableAutoCommit(),
	)
	if err != nil {
		t.Fatal(err)
	}
	defer cons.Close()

	got := 0
	for got < 4 {
		fs := cons.PollRecords(ctx, 4-got)
		if err := fs.Err(); err != nil {
			t.Fatal(err)
		}
		got += fs.NumRecords()
	}
	if err := cons.CommitUncommittedOffsets(ctx); err != nil {
		t.Fatal(err)
	}

	// When — kadm 으로 그룹 lag 계산
	adm := kadm.NewClient(prod)
	lags, err := adm.Lag(ctx, "g1")
	if err != nil {
		t.Fatal(err)
	}

	// Then — 끝 오프셋 10 − 커밋 4 = 6
	l := lags["g1"]
	if err := l.Error(); err != nil {
		t.Fatal(err)
	}
	if total := l.Lag.Total(); total != 6 {
		t.Fatalf("total lag=%d", total)
	}

	// 같은 값을 손으로 계산: 커밋 오프셋과 끝 오프셋을 따로 읽어 뺀다.
	commits, err := adm.FetchOffsets(ctx, "g1")
	if err != nil {
		t.Fatal(err)
	}
	ends, err := adm.ListEndOffsets(ctx, "orders")
	if err != nil {
		t.Fatal(err)
	}
	cm, _ := commits.Lookup("orders", 0)
	end, _ := ends.Lookup("orders", 0)
	if manual := end.Offset - cm.At; manual != 6 {
		t.Fatalf("manual lag=%d", manual)
	}
}
```

이 테스트와 앞의 `Consume` 함수는 `go vet` 과 `go test -race` 를 통과했습니다. 테스트가 쓴 `kfake` 는 가짜 브로커라서, 진짜 브로커에서의 값이 같다는 보장은 아닙니다.

### 흔한 함정

- 커밋이 없는 파티션의 lag 은 로그 시작 오프셋 때문에 과대 계산될 수 있습니다. `CalculateGroupLagWithStartOffsets` 의 문서가 예를 듭니다. 끝 오프셋이 30, 시작 오프셋이 10 이고 아직 커밋이 없으면 실제 lag 은 20 인데 `CalculateGroupLag` 는 30 을 알려 줍니다. `Client.Lag` 는 시작 오프셋을 항상 함께 계산하므로 이 문제가 없습니다.
- 그룹이 비어 있는(Empty) 경우 멤버가 `nil` 입니다. `GroupMemberLag` 문서에 따르면 이때 lag 은 토픽의 모든 파티션에 대해 계산되고, 할당된 토픽은 전부 소비될 대상으로 간주됩니다.
- 함수의 `err` 만 확인하고 그룹별 `Error()` 를 건너뛰는 실수가 있습니다. 위 예제처럼 둘 다 확인합니다.
- 자동 커밋을 끄고 리밸런스를 막지 않으면 이미 다른 멤버에게 넘어간 파티션에 커밋해 중복 처리가 생깁니다. `DisableAutoCommit` 문서는 최악의 경우 다른 멤버의 커밋을 되감을 수 있다고 경고합니다.
- `BlockRebalanceOnPoll` 을 켜고 처리가 오래 걸리면 그룹에서 쫓겨날 위험이 있습니다. 문서가 이 상충 관계를 직접 적습니다.
- lag 은 "얼마나 밀렸나" 이지 "처리가 되고 있나" 가 아닙니다. 커밋이 멈춘 그룹의 lag 은 계속 커지므로, 소비는 하는데 커밋만 못 하는 경우와 소비 자체가 멈춘 경우를 구분하려면 커밋 시각이나 처리 로그를 함께 봅니다.

### sarama 및 confluent-kafka-go 와의 차이

이 문서는 두 클라이언트와의 차이를 단정하지 않습니다. 열어 본 franz-go README 는 두 라이브러리를 이름으로 비교하지 않습니다. 비교할 수 있는 확인된 사실은 README 의 "Written in pure Go (no wrapper lib for a C library or other bindings)" 한 줄뿐입니다. 이 문장은 franz-go 가 C 라이브러리 래퍼가 아니라는 사실만 말합니다.

README 는 성능 주장도 합니다.

> "This client is fast, and is consistently among the fastest and most cpu and memory efficient Kafka clients in Go."

이 문장은 저자의 주장이며 이 문서에서 측정으로 검증하지 않았습니다. 두 라이브러리의 README 와 비교 벤치마크는 열지 않았습니다.

### 공식 문서 근거

| 출처 | 확인한 문장 | 이 문서에서 쓴 곳 |
|------|------------|------------------|
| franz-go README | "Franz-go is an all-encompassing Apache Kafka client fully written in Go." | 소개 |
| franz-go README | "Written in pure Go (no wrapper lib for a C library or other bindings)" | 차이 |
| `kgo.NewClient` | "Connections to brokers are lazily created only when requests are written to them." | 클라이언트 생성 |
| `kgo.ProduceSync` | "This function produces all records and waits for them all to be produced before returning." | 발행 |
| `kgo.ConsumerGroup` | "when group consuming, the default is to autocommit every 5s." | 커밋 |
| `kgo.PollFetches` | "It is important to check all partition errors in the returned fetches." | 소비 루프 |
| `kadm.GroupMemberLag` | "the lag between a group member's current offset commit and the current end offset" | lag 정의 |
| `kadm.ListEndOffsets` | "In Kafka terms, this returns high watermarks." | 끝 오프셋 |
| `kadm.CalculateGroupLagWithStartOffsets` | "this function can correctly tell you that the lag is 20, whereas CalculateGroupLag would tell you the lag is 30." | 함정 |

패키지 문서는 https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2 와 https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0 입니다. 시그니처와 문장은 모듈 v1.22.2, kadm v1.19.0 을 내려받아 `go doc` 으로도 대조했습니다.
