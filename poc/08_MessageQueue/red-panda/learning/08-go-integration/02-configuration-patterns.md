# 02. Configuration Patterns

> **이론**: `02-fundamentals/03-architecture-deep-dive.md`
> **Spring 대응**: `03-spring-boot-integration/02-configuration-reference.md`
> **이 문서**: Go에서 franz-go 클라이언트 설정 패턴에 집중.

## 목표

- 환경별(dev/staging/prod) 설정 분리 패턴 구현
- TLS/SASL 인증 설정
- 함수형 옵션 패턴의 확장 및 조합

## 함수형 옵션 패턴

Spring Boot는 `application.yml`에 프로퍼티를 나열하고 자동 설정이 클라이언트를 구성한다. Go는 이런 마법이 없다. 대신 franz-go는 함수형 옵션 패턴을 사용하여 타입 안전한 설정을 제공한다.

```go
// Spring: spring.kafka.producer.acks=all
// Go: 함수형 옵션으로 명시적 설정
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.RequiredAcks(kgo.AllISRAcks()),
    kgo.RecordPartitioner(kgo.StickyKeyPartitioner(nil)),
    kgo.ProducerBatchMaxBytes(1_000_000),
    kgo.MaxBufferedRecords(10_000),
)
```

함수형 옵션의 장점은 컴파일 타임에 타입 검사가 이루어진다는 것이다. Spring의 문자열 프로퍼티(`"all"`)와 달리, Go에서는 `kgo.AllISRAcks()`처럼 타입이 보장된다.

## 설정 구조체 + 빌더 패턴

프로젝트가 커지면 설정을 구조화해야 한다. 환경 변수에서 읽어 옵션 슬라이스를 조합하는 패턴을 사용한다.

```go
package kafka

import (
    "crypto/tls"
    "os"
    "strings"

    "github.com/twmb/franz-go/pkg/kgo"
    "github.com/twmb/franz-go/pkg/sasl/plain"
    "github.com/twmb/franz-go/pkg/sasl/scram"
)

type Config struct {
    Brokers       []string
    ConsumerGroup string
    TLSEnabled    bool
    SASLEnabled   bool
    SASLUser      string
    SASLPass      string
    SASLMechanism string // "plain" | "scram-sha-256"
    Profile       string // "local" | "dev" | "prod"
}

func LoadFromEnv() Config {
    brokers := os.Getenv("KAFKA_BROKERS")
    if brokers == "" {
        brokers = "localhost:19092"
    }
    return Config{
        Brokers:       strings.Split(brokers, ","),
        ConsumerGroup: os.Getenv("KAFKA_CONSUMER_GROUP"),
        TLSEnabled:    os.Getenv("KAFKA_TLS_ENABLED") == "true",
        SASLEnabled:   os.Getenv("KAFKA_SASL_ENABLED") == "true",
        SASLUser:      os.Getenv("KAFKA_SASL_USER"),
        SASLPass:      os.Getenv("KAFKA_SASL_PASS"),
        SASLMechanism: os.Getenv("KAFKA_SASL_MECHANISM"),
        Profile:       os.Getenv("APP_PROFILE"),
    }
}

func (c Config) BuildOpts() []kgo.Opt {
    opts := []kgo.Opt{
        kgo.SeedBrokers(c.Brokers...),
    }

    // Consumer Group
    if c.ConsumerGroup != "" {
        opts = append(opts, kgo.ConsumerGroup(c.ConsumerGroup))
    }

    // TLS
    if c.TLSEnabled {
        tlsCfg := &tls.Config{MinVersion: tls.VersionTLS12}
        opts = append(opts, kgo.DialTLSConfig(tlsCfg))
    }

    // SASL
    if c.SASLEnabled {
        switch c.SASLMechanism {
        case "scram-sha-256":
            opts = append(opts, kgo.SASL(
                scram.Auth{User: c.SASLUser, Pass: c.SASLPass}.AsSha256Mechanism(),
            ))
        default: // plain
            opts = append(opts, kgo.SASL(
                plain.Auth{User: c.SASLUser, Pass: c.SASLPass}.AsMechanism(),
            ))
        }
    }

    // 프로파일별 기본 옵션 추가
    opts = append(opts, c.profileOpts()...)

    return opts
}

func (c Config) NewClient(extra ...kgo.Opt) (*kgo.Client, error) {
    opts := append(c.BuildOpts(), extra...)
    return kgo.NewClient(opts...)
}
```

## 프로파일별 설정

Spring의 `application-{profile}.yml` 대신, Go에서는 환경변수와 기본값 조합으로 프로파일을 구현한다.

```go
func (c Config) profileOpts() []kgo.Opt {
    switch c.Profile {
    case "prod":
        return []kgo.Opt{
            kgo.RequiredAcks(kgo.AllISRAcks()),
            kgo.RecordRetries(5),
            kgo.ProducerBatchMaxBytes(1_000_000),
            kgo.MaxBufferedRecords(50_000),
        }
    case "dev":
        return []kgo.Opt{
            kgo.RequiredAcks(kgo.LeaderAck()),
            kgo.RecordRetries(2),
            kgo.ProducerBatchMaxBytes(500_000),
        }
    default: // local
        return []kgo.Opt{
            kgo.RequiredAcks(kgo.LeaderAck()),
            kgo.RecordRetries(1),
        }
    }
}
```

## TLS/SASL 인증

Redpanda Cloud 또는 프로덕션 환경에서는 TLS + SASL 인증이 필수다.

```go
import (
    "crypto/tls"
    "github.com/twmb/franz-go/pkg/sasl/plain"
    "github.com/twmb/franz-go/pkg/sasl/scram"
)

// SASL/PLAIN
plainAuth := plain.Auth{User: "user", Pass: "pass"}.AsMechanism()

// SASL/SCRAM-SHA-256 (Redpanda 기본 권장)
scramAuth := scram.Auth{User: "user", Pass: "pass"}.AsSha256Mechanism()

// SASL/SCRAM-SHA-512
scram512Auth := scram.Auth{User: "user", Pass: "pass"}.AsSha512Mechanism()

client, err := kgo.NewClient(
    kgo.SeedBrokers("broker:9092"),
    kgo.DialTLSConfig(&tls.Config{MinVersion: tls.VersionTLS12}),
    kgo.SASL(scramAuth),
)
```

## 로깅 통합

franz-go는 `kgo.WithLogger()`로 내부 로그를 커스텀 로거에 연결할 수 있다. 프로덕션에서는 구조화된 로거(zerolog, zap)와 통합하는 것이 일반적이다.

```go
import (
    "fmt"
    "os"

    "github.com/rs/zerolog"
    "github.com/twmb/franz-go/pkg/kgo"
)

type zerologAdapter struct {
    logger zerolog.Logger
}

func (z *zerologAdapter) Level() kgo.LogLevel { return kgo.LogLevelInfo }

func (z *zerologAdapter) Log(level kgo.LogLevel, msg string, keyvals ...any) {
    var event *zerolog.Event
    switch level {
    case kgo.LogLevelError:
        event = z.logger.Error()
    case kgo.LogLevelWarn:
        event = z.logger.Warn()
    case kgo.LogLevelDebug:
        event = z.logger.Debug()
    default:
        event = z.logger.Info()
    }
    for i := 0; i+1 < len(keyvals); i += 2 {
        event = event.Interface(fmt.Sprint(keyvals[i]), keyvals[i+1])
    }
    event.Msg(msg)
}

// 사용
logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.WithLogger(&zerologAdapter{logger: logger}),
)
```

## Consumer 전용 옵션

Consumer는 Producer와 다른 옵션 집합이 필요하다. 같은 Config에서 용도별로 옵션을 분리한다.

```go
func (c Config) ConsumerOpts(topics ...string) []kgo.Opt {
    opts := c.BuildOpts()
    opts = append(opts,
        kgo.ConsumeTopics(topics...),
        kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
    )
    return opts
}

func (c Config) ProducerOpts() []kgo.Opt {
    opts := c.BuildOpts()
    opts = append(opts,
        kgo.RecordPartitioner(kgo.StickyKeyPartitioner(nil)),
        kgo.ProducerBatchCompression(kgo.SnappyCompression()),
    )
    return opts
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `application-{profile}.yml` | 환경변수 + `profileOpts()` | 프로파일 |
| `spring.kafka.properties.*` | `kgo.Opt` 슬라이스 | 설정 전달 |
| `spring.kafka.ssl.*` | `kgo.DialTLSConfig(...)` | TLS |
| `spring.kafka.security.protocol=SASL_SSL` | `kgo.SASL(mechanism)` | 인증 |
| `DefaultKafkaProducerFactory` | `config.NewClient(opts...)` | 팩토리 |
| `@ConfigurationProperties` | `LoadFromEnv()` | 설정 바인딩 |
| Spring 자동 설정 | 명시적 옵션 조합 | Go는 마법 없음 |

## 실습 TODO

```
TODO 1: Config 구조체 + LoadFromEnv() 구현
TODO 2: BuildOpts()로 클라이언트 생성 → Ping 확인
TODO 3: APP_PROFILE=dev/prod 환경변수로 프로파일 분기 확인
TODO 4: zerolog 어댑터 연결 후 내부 로그 출력 확인
TODO 5: ConsumerOpts / ProducerOpts 분리 후 각각 클라이언트 생성
```

## 체크포인트

- [ ] 환경변수 변경만으로 브로커 주소 전환 가능
- [ ] APP_PROFILE=prod → AllISRAcks 설정 적용 확인
- [ ] APP_PROFILE=dev → LeaderAck 설정 적용 확인
- [ ] zerolog으로 franz-go 내부 로그 출력 확인
