# 01. Basic Setup & Health Check

> **이론**: `02-fundamentals/01-what-is-event-streaming.md`
> **Spring 대응**: `03-spring-boot-integration/01-basic-setup.md`
> **이 문서**: Go franz-go 환경 구성 및 Redpanda 연결 확인에 집중.

## 목표

- franz-go 클라이언트 설치 및 기본 연결 설정
- Redpanda 브로커 헬스 체크 구현
- Go 프로젝트 구조 확립 (cmd/internal 패턴)

## franz-go 소개

franz-go는 순수 Go로 작성된 Kafka 클라이언트 라이브러리다. CGO 의존성 없이 Kafka 프로토콜을 직접 구현했기 때문에, 크로스 컴파일이 자유롭고 배포가 단순하다.

Spring Boot에서 `spring-kafka`가 Kafka 프로토콜을 추상화하는 것처럼, franz-go는 Go 생태계에서 동일한 역할을 한다. 다만 Spring의 선언적 방식(`@KafkaListener`)과 달리, franz-go는 명시적 폴링 루프를 사용한다. 이 차이가 Go 클라이언트의 핵심 특성이다.

### 왜 franz-go인가?

| 특성 | franz-go | confluent-kafka-go | sarama |
|------|:--------:|:-----------------:|:------:|
| 순수 Go | O | X (CGO/librdkafka) | O |
| 트랜잭션 | 완전 지원 | 완전 지원 | 부분 |
| Schema Registry | 내장 (`pkg/sr`) | 별도 라이브러리 | X |
| API 스타일 | 함수형 옵션 | 설정 맵 | 구조체 |

순수 Go 구현은 빌드 단순성과 배포 용이성을 보장한다. CGO 기반 라이브러리는 librdkafka C 라이브러리에 의존하므로, Docker 이미지 빌드 시 별도 시스템 라이브러리가 필요하고 alpine 이미지에서 문제가 발생할 수 있다.

## 프로젝트 구조

```
08-go-integration/
└── practice/
    ├── go.mod
    ├── go.sum
    ├── cmd/
    │   └── ch01/
    │       └── main.go
    └── internal/
        └── kafka/
            └── client.go
```

Go 프로젝트는 `cmd/` 에 실행 진입점을, `internal/` 에 공유 로직을 두는 관습을 따른다. 챕터별로 `cmd/ch01`, `cmd/ch02` 형태로 독립 실행 파일을 만든다.

### go.mod 초기화

```bash
mkdir -p practice/cmd/ch01 practice/internal/kafka
cd practice
go mod init github.com/yourname/redpanda-go

# franz-go 클라이언트
go get github.com/twmb/franz-go/pkg/kgo
# Admin API
go get github.com/twmb/franz-go/pkg/kadm
```

## 기본 연결

### 클라이언트 생성

franz-go는 함수형 옵션 패턴(`kgo.Opt`)으로 클라이언트를 구성한다. Spring의 `spring.kafka.bootstrap-servers` 프로퍼티 대신 `kgo.SeedBrokers()`를 사용한다.

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/twmb/franz-go/pkg/kgo"
)

func main() {
    client, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
    )
    if err != nil {
        log.Fatalf("클라이언트 생성 실패: %v", err)
    }
    defer client.Close()

    // Ping으로 연결 확인
    if err := client.Ping(context.Background()); err != nil {
        log.Fatalf("브로커 연결 실패: %v", err)
    }
    fmt.Println("Redpanda 연결 성공!")
}
```

### 메타데이터 조회

브로커 상태와 토픽 목록을 확인하는 헬스 체크는 Admin API로 수행한다. `kadm.NewClient(client)`는 기존 kgo.Client를 재사용하므로 별도 연결이 생성되지 않는다.

```go
import "github.com/twmb/franz-go/pkg/kadm"

func healthCheck(client *kgo.Client) error {
    adm := kadm.NewClient(client)

    brokers, err := adm.Brokers(context.Background())
    if err != nil {
        return fmt.Errorf("브로커 조회 실패: %w", err)
    }

    for _, b := range brokers {
        fmt.Printf("Broker %d: %s:%d\n", b.NodeID, b.Host, b.Port)
    }

    topics, err := adm.ListTopics(context.Background())
    if err != nil {
        return fmt.Errorf("토픽 조회 실패: %w", err)
    }

    for name, detail := range topics {
        fmt.Printf("Topic: %s (partitions: %d)\n", name, len(detail.Partitions))
    }
    return nil
}
```

### 토픽 생성

`CreateTopics`의 두 번째 인자는 파티션 수, 세 번째는 복제 팩터다. Redpanda 단일 노드 환경에서는 복제 팩터를 1로 설정한다.

```go
func createTopic(client *kgo.Client, name string, partitions int32) error {
    adm := kadm.NewClient(client)

    resp, err := adm.CreateTopics(context.Background(), partitions, 1, nil, name)
    if err != nil {
        return err
    }
    for _, r := range resp {
        if r.Err != nil {
            return fmt.Errorf("토픽 생성 실패 %s: %w", r.Topic, r.Err)
        }
        fmt.Printf("토픽 생성: %s (partitions=%d)\n", r.Topic, partitions)
    }
    return nil
}
```

### 토픽 삭제

```go
func deleteTopic(client *kgo.Client, name string) error {
    adm := kadm.NewClient(client)
    resp, err := adm.DeleteTopics(context.Background(), name)
    if err != nil {
        return err
    }
    for _, r := range resp {
        if r.Err != nil {
            return fmt.Errorf("토픽 삭제 실패 %s: %w", r.Topic, r.Err)
        }
    }
    return nil
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `spring-boot-starter-kafka` | `go get github.com/twmb/franz-go/pkg/kgo` | 의존성 추가 |
| `spring.kafka.bootstrap-servers` | `kgo.SeedBrokers(...)` | 브로커 주소 |
| `KafkaAdmin` bean | `kadm.NewClient(client)` | Admin 작업 |
| `NewTopic` bean 등록 | `adm.CreateTopics(...)` | 토픽 생성 |
| `KafkaHealthIndicator` | `client.Ping(ctx)` | 헬스 체크 |
| application.yml | 환경변수 + `kgo.Opt` | 설정 방식 |
| `@SpringBootApplication` | `func main()` | 진입점 |

## 실습 TODO

```
TODO 1: go mod init 후 franz-go 의존성 추가
TODO 2: franz-go 클라이언트로 Redpanda 연결 확인 (Ping)
TODO 3: kadm으로 브로커 메타데이터 출력
TODO 4: "go-test-topic" 토픽 생성 (3 파티션)
TODO 5: 토픽 목록 조회 후 출력
```

## 체크포인트

- [ ] `go run ./cmd/ch01` 실행 시 "Redpanda 연결 성공" 출력
- [ ] 브로커 ID, 호스트, 포트 출력 확인
- [ ] 토픽 생성 및 조회 동작 확인
- [ ] `go build ./...` 오류 없이 빌드 성공
