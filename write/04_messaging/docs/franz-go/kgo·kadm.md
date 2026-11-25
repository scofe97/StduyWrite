---
title: kgo·kadm
tags: [go, kafka, franz-go, kgo, kadm, consumer-lag, consumer-group, kfake]
status: draft
source:
  - https://raw.githubusercontent.com/twmb/franz-go/v1.22.2/README.md
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0
  - https://raw.githubusercontent.com/twmb/franz-go/v1.22.2/pkg/kgo/config.go
  - https://raw.githubusercontent.com/twmb/franz-go/pkg/kadm/v1.19.0/pkg/kadm/groups.go
  - https://github.com/twmb/franz-go/tree/123ec885bc97/pkg/kfake
related:
  - ../README.md
  - ../../04_BrokerArchitecture/06-02.AdminClient 설정·컨슈머그룹·클러스터.md
  - ../../04_BrokerArchitecture/01-05.오프셋 커밋 API.md
created: 2026-11-25
updated: 2026-11-25
---

# kgo·kadm

---

> franz-go 는 순수 Go 로 만든 Kafka 클라이언트입니다. `kgo` 는 발행과 소비를 맡고 `kadm` 은 그룹의 커밋 오프셋과 파티션 끝 오프셋의 차이로 컨슈머 lag 을 계산합니다.

## 핵심 요약

> 그룹 소비의 기본값은 5초마다 자동 커밋이라서 처리가 끝난 뒤에만 커밋하려면 자동 커밋을 끄고 직접 커밋합니다. lag 은 `kadm` 의 `Client.Lag` 한 번으로 얻고 함수의 `err` 와 그룹별 `Error()` 를 둘 다 확인합니다.

Kafka 에서 오프셋 커밋과 lag 의 개념은 Java 클라이언트 기준으로 [06-02 §3](../../04_BrokerArchitecture/06-02.AdminClient%20설정·컨슈머그룹·클러스터.md)과 [01-05](../../04_BrokerArchitecture/01-05.오프셋%20커밋%20API.md)가 다룹니다. 이 편은 같은 개념을 Go 클라이언트의 옵션과 함수로 옮겨 보입니다.

Kafka 를 Go 로 쓸 때는 두 가지가 필요합니다. 하나는 발행하고 소비하는 클라이언트이고, 다른 하나는 소비가 얼마나 밀렸는지 보는 도구입니다. lag 이 없으면 소비자가 살아 있는데도 처리가 뒤처지는 상황을 알 수 없습니다.

이 편의 코드는 franz-go v1.22.2 와 `kadm` v1.19.0 기준입니다. 두 모듈의 `go.mod` 는 Go 1.26.0 이상을 요구합니다. 툴체인 자동 전환을 막은 Go 1.25.1 에서 `go get` 하면 `requires go >= 1.26.0` 오류가 났습니다. 로컬 확인은 Go 1.26.10 에서 했습니다.



## 1. 클라이언트 생성과 발행

> `kgo.NewClient` 는 브로커에 바로 연결하지 않으며 쓰고 난 클라이언트는 `Close` 로 닫아야 합니다. 발행은 `ProduceSync` 로 결과를 기다립니다.

### 패키지 구성과 버전

franz-go 는 모듈 하나가 아니라 패키지별로 나뉩니다. README 는 각 패키지의 역할을 다음처럼 소개합니다[^readme].

- `kgo`: 발행과 소비를 맡는 주 클라이언트입니다.
- `kadm`: 클러스터 관리를 쉽게 하는 상위 관리 패키지입니다.
- `kmsg`: 프로토콜의 요청·응답 타입을 그대로 다루는 저수준 패키지입니다.
- `kfake`: 테스트용 가짜 브로커입니다. README 에는 없고 패키지 문서가 그렇게 소개합니다[^kfake]. 테스트 쪽 사용은 [Go 테스트 대역](../../../99_ETC/2026-11-06_책에%20없는%20Go·K8s%20개념%20모음/Go%20테스트%20대역%20—%20시간%20주입·fake%20clientset·miniredis·kfake.md) 문서가 다룹니다.

`kadm` 과 `kfake` 는 별도 모듈이라 버전이 따로 붙습니다. 이 편은 `kgo` v1.22.2 와 `kadm` v1.19.0 을 썼습니다.

`kfake` 는 태그가 없어 의사 버전 `v0.0.0-20261022190701-123ec885bc97` 을 썼습니다.

README 는 프로젝트를 Go 만으로 쓴 Kafka 클라이언트로 소개합니다. C 라이브러리 래퍼가 아니라고도 적습니다[^readme]. 성능 우월성은 저자의 주장이고 이 편은 측정하지 않았습니다. 열어 본 franz-go README 는 두 라이브러리를 이름으로 비교하지 않습니다. sarama 나 confluent-kafka-go 와의 차이는 두 라이브러리의 문서를 열어 보지 않았으므로 쓰지 않습니다.

### 연결과 고루틴

`NewClient` 는 옵션을 검증해 클라이언트를 만들 뿐입니다. 브로커 연결은 요청을 처음 보낼 때 만들어집니다[^newclient]. 그래서 `NewClient` 가 성공해도 브로커가 살아 있다는 뜻은 아닙니다.

`NewClient` 는 토픽 메타데이터를 주기적으로 갱신하는 고루틴도 띄웁니다[^newclient].

`Close` 는 그룹을 떠나고 모든 연결과 고루틴을 닫으므로 클라이언트를 다 쓰면 호출합니다[^close].

### 동기 발행

`ProduceSync` 는 넘긴 레코드가 모두 발행될 때까지 기다린 뒤 돌아옵니다[^producesync]. 결과의 오류는 `FirstErr()` 로 확인합니다. 이 함수는 코드 조각이라 `ctx` 와 `brokers` 는 호출하는 쪽에서 받습니다.

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



## 2. 컨슈머 그룹과 커밋

> 그룹 소비는 `kgo.ConsumerGroup` 으로 켜며 기본 동작은 5초마다 직전에 poll 한 것까지만 커밋하는 자동 커밋입니다. 처리 뒤 커밋은 자동 커밋을 끄고 직접 합니다.

### 자동 커밋의 기본 동작

같은 그룹 이름을 쓰는 클라이언트들이 파티션을 나눠 맡습니다. 그룹 소비의 기본값은 5초마다 하는 자동 커밋입니다[^group]. 자동 커밋은 직전에 poll 한 것까지만 커밋합니다. poll 을 한 번만 했다면 아무것도 커밋되지 않습니다.

이 방식은 최소 한 번 처리(at-least-once)를 보장합니다. 대신 리밸런스 중에 중복 처리가 생길 수 있습니다. 종료할 때는 마지막으로 동기 커밋을 한 번 하라고 문서가 직접 권합니다. 종료 뒤에는 다시 poll 하지 않고 자동 커밋을 기다리지도 않기 때문입니다[^group].

### 처리 뒤에만 커밋하기

처리가 끝난 뒤에만 커밋하려면 `DisableAutoCommit` 으로 자동 커밋을 끄고 `CommitUncommittedOffsets` 를 호출합니다. 문서가 권하는 패턴은 poll, 처리, 커밋 순서의 반복입니다[^commit].

`PollFetches` 도중 리밸런스가 일어나면 내가 더는 소유하지 않는 파티션에 커밋할 수 있습니다. `BlockRebalanceOnPoll` 을 켜면 `AllowRebalance` 를 호출할 때까지 리밸런스가 미뤄집니다[^block]. 아래 `Consume` 은 두 옵션을 함께 쓴 소비 루프입니다. 완전한 프로그램이 아니라 함수 하나입니다.

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
			cl.AllowRebalance()
			return ctx.Err()
		}
		if errs := fetches.Errors(); len(errs) > 0 {
			cl.AllowRebalance()
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

`PollFetches` 의 문서는 반환된 fetches 의 파티션 오류를 모두 확인하라고 강조합니다[^poll]. 위 예제가 `fetches.Errors()` 를 확인하는 이유입니다.

`return` 하는 모든 길에서 `AllowRebalance` 를 먼저 부르는 데에는 이유가 있습니다. `BlockRebalanceOnPoll` 을 켜고 poll 한 클라이언트의 `Close` 는 리밸런스를 자동으로 허용하지 않습니다[^close]. `Close` 는 그룹을 떠나는 일이고, 그룹을 떠나면 리밸런스가 일어나기 때문입니다.

취소 경로의 `AllowRebalance` 를 빼고 돌려 보면 `Consume` 이 돌아오지 않았습니다. 컨텍스트를 취소하고 15초를 기다렸는데도 `defer cl.Close()` 에서 멈춰 있었습니다. 같은 코드에 `AllowRebalance` 를 더하자 취소 직후 `context canceled` 로 돌아왔습니다. 두 실행 모두 `kfake` 가짜 브로커에서 한 결과입니다.

### 커밋 옵션의 함정

`DisableAutoCommit` 만 켜고 `OnPartitionsRevoked` 를 쓰지 않으면 중복 처리가 생깁니다. 문서가 든 예는 이렇습니다. 멤버 A 가 파티션 0 을 오프셋 30 까지 처리했는데 커밋은 4 에 머물렀습니다. 리밸런스로 파티션이 멤버 B 에게 넘어가면 B 는 4 부터 다시 처리합니다.

더 나쁜 경우도 문서에 있습니다. B 가 오프셋 50 을 커밋한 뒤 A 가 뒤늦게 30 을 커밋하면 B 의 커밋이 되감깁니다[^disable]. 중복 처리가 괜찮은 워크로드라면 `OnPartitionsRevoked` 는 필수가 아니라고 문서가 덧붙입니다.

`BlockRebalanceOnPoll` 에도 대가가 있고 문서가 이 상충 관계를 직접 적습니다[^block]. 처리가 오래 걸리면 그룹 멤버가 리밸런스 타임아웃을 넘겨 그룹에서 쫓겨날 수 있습니다.

문서는 레코드를 빨리 처리하라고 권합니다. 처리가 느리면 `PollFetches` 대신 `PollRecords` 로 한 번에 받는 양을 제한하라고 권합니다[^block]. 이 옵션을 켜면 sarama 의 기본 동작과 비슷해진다고도 적습니다.



## 3. kadm 으로 컨슈머 lag 계산

> lag 은 파티션 끝 오프셋에서 그룹이 커밋한 오프셋을 뺀 값이며 `Client.Lag` 가 필요한 요청을 묶어 계산해 줍니다. 그룹별 오류는 반환값 안에 들어 있습니다.

### lag 의 정의와 끝 오프셋

`kadm` 의 `GroupMemberLag` 는 그룹 멤버의 현재 오프셋 커밋과 현재 끝 오프셋의 차이로 lag 을 정의합니다[^gml]. 끝 오프셋은 Kafka 용어로 high watermark 입니다. `ListEndOffsets` 문서가 이 대응을 직접 적습니다[^listend].

### Client.Lag 로 한 번에 계산

가장 쉬운 방법은 `Client.Lag` 입니다. 이 함수는 그룹 설명, 커밋 오프셋 조회, 시작 오프셋 조회, 끝 오프셋 조회를 부르고 그 결과로 lag 을 계산합니다[^lag]. `kadm.NewClient` 에는 `kgo` 클라이언트를 그대로 넘깁니다.

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

반환값은 그룹 이름을 키로 하는 맵입니다. 그룹을 설명하지 못했거나 커밋 오프셋을 가져오지 못했으면 해당 그룹 값의 `DescribeErr`, `FetchErr` 에 오류가 담깁니다. 그래서 함수의 `err` 가 `nil` 이어도 그룹별 `Error()` 를 확인해야 합니다. 맵 전체에서 첫 오류를 보려면 `lags.Error()` 를, 오류가 없는지만 보려면 `lags.Ok()` 를 씁니다[^lag].

파티션 단위로 보려면 `GroupLag` 의 `Sorted()` 나 `Lookup(topic, partition)` 을 씁니다. 각 항목 `GroupMemberLag` 는 `Commit`, `End`, `Lag` 필드를 갖습니다. 커밋 조회나 끝 오프셋 조회에 오류가 있으면 `Lag` 은 -1 이 되고 `Err` 에 그 오류가 담깁니다[^gml]. 토픽별 합계는 `TotalByTopic()` 입니다.

### 손으로 계산하기

`FetchOffsets` 로 커밋 오프셋을, `ListEndOffsets` 로 끝 오프셋을 읽어 빼도 같은 값이 나옵니다. 두 함수는 `(ctx, group)` 과 `(ctx, topics...)` 를 받습니다.

아래 테스트는 `kfake` 가짜 브로커에 10건을 발행하고 그룹 컨슈머가 4건을 커밋합니다. 그 뒤 두 방법이 모두 6 을 돌려주는지 확인합니다.

테스트 파일에는 `context`, `fmt`, `testing`, `time` 과 `kadm`, `kfake`, `kgo` 패키지를 import 해야 합니다.

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

이 테스트와 앞의 `Consume` 함수와 `Lag` 호출부는 Go 1.26.10 에서 `go vet` 을 통과했습니다. 테스트는 `go test -race` 도 통과했습니다. `kfake` 는 한 프로세스 안에서 도는 가짜 브로커라서 컨테이너를 띄우지 않았습니다. 진짜 브로커에서 같은 값이 나온다는 보장은 아닙니다.

### lag 을 읽을 때의 함정

- 커밋이 없는 파티션의 lag 은 로그 시작 오프셋 때문에 과대 계산될 수 있습니다. 문서의 예는 이렇습니다. 끝 오프셋 30, 시작 오프셋 10 에 아직 커밋이 없으면 실제 lag 은 20 입니다. `CalculateGroupLag` 는 30 을 알려 줍니다. `CalculateGroupLagWithStartOffsets` 는 20 을 돌려줍니다[^start]. `Client.Lag` 는 시작 오프셋을 항상 함께 계산하므로 이 문제가 없습니다.
- 그룹이 Empty 상태이면 멤버가 `nil` 입니다. 이때 lag 은 토픽의 모든 파티션에 대해 계산됩니다. 할당된 토픽은 전부 소비될 대상으로 간주됩니다[^gml].
- 함수의 `err` 만 확인하고 그룹별 `Error()` 를 건너뛰는 실수가 있습니다. 위 예제처럼 둘 다 확인합니다.
- lag 은 얼마나 밀렸는지이지 처리가 되고 있는지가 아닙니다. 커밋이 멈춘 그룹의 lag 은 계속 커집니다. 소비는 하는데 커밋만 못 하는 경우와 소비 자체가 멈춘 경우는 lag 숫자로 가를 수 없습니다. 커밋 시각이나 처리 로그를 함께 봅니다.



## 참고 자료

[^readme]: franz-go README (v1.22.2). <https://raw.githubusercontent.com/twmb/franz-go/v1.22.2/README.md>
[^kfake]: Go `kfake` 패키지 문서와 소스. <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kfake> · <https://github.com/twmb/franz-go/tree/123ec885bc97/pkg/kfake>
[^newclient]: `kgo.NewClient` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#NewClient>
[^producesync]: `Client.ProduceSync` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#Client.ProduceSync>
[^group]: `kgo.ConsumerGroup` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#ConsumerGroup>
[^commit]: `Client.CommitUncommittedOffsets` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#Client.CommitUncommittedOffsets>
[^block]: `kgo.BlockRebalanceOnPoll` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#BlockRebalanceOnPoll>
[^close]: `Client.Close` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#Client.Close>
[^poll]: `Client.PollFetches` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#Client.PollFetches>
[^disable]: `kgo.DisableAutoCommit` (kgo v1.22.2). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2#DisableAutoCommit>
[^gml]: `kadm.GroupMemberLag` (kadm v1.19.0). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0#GroupMemberLag>
[^listend]: `Client.ListEndOffsets` (kadm v1.19.0). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0#Client.ListEndOffsets>
[^lag]: `Client.Lag` 와 `DescribedGroupLags` (kadm v1.19.0). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0#Client.Lag> · 호출 순서는 소스 <https://raw.githubusercontent.com/twmb/franz-go/pkg/kadm/v1.19.0/pkg/kadm/groups.go> 의 `Lag` 를 읽어 확인했습니다. 시그니처와 문장은 모듈 v1.22.2, kadm v1.19.0 을 내려받아 `go doc` 으로도 대조했습니다.
[^start]: `kadm.CalculateGroupLagWithStartOffsets` (kadm v1.19.0). <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0#CalculateGroupLagWithStartOffsets>
