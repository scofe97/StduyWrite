# 05. Error Handling & DLQ

> **이론**: `02-fundamentals/05-core-features.md`
> **Spring 대응**: `03-spring-boot-integration/05-dlq-strategy.md`
> **이 문서**: Go에서 에러 분류, 재시도, DLQ 라우팅 구현에 집중.

## 목표

- 에러 분류 (재시도 가능 vs 불가능)
- 재시도 로직 구현 (지수 백오프)
- Dead Letter Queue 라우팅
- Go의 에러 처리 관용구 활용

## 에러 분류

모든 에러를 동일하게 처리하면 안 된다. 일시적 네트워크 장애는 재시도로 해결되지만, JSON 파싱 에러는 100번 재시도해도 실패한다. Spring의 `DefaultErrorHandler` + `@RetryableTopic`이 자동으로 분류하는 것을, Go에서는 직접 구현한다.

```go
package errors

import (
    "encoding/json"
    "errors"
    "net"
)

type ErrorKind int

const (
    Retryable    ErrorKind = iota // 재시도 가능 (네트워크, 타임아웃)
    NonRetryable                  // 재시도 불가 (역직렬화, 검증 실패)
    Fatal                         // 즉시 중단 (인증 실패, 설정 오류)
)

// 비즈니스 에러 타입 정의
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed: %s - %s", e.Field, e.Message)
}

func ClassifyError(err error) ErrorKind {
    if err == nil {
        return Retryable // 사용 안 함
    }
    // context 취소는 재시도 불가 (애플리케이션 종료)
    if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) {
        return Fatal
    }
    // 검증 에러 → 재시도 불가
    var validErr *ValidationError
    if errors.As(err, &validErr) {
        return NonRetryable
    }
    // JSON 파싱 에러 → 재시도 불가
    var jsonErr *json.SyntaxError
    if errors.As(err, &jsonErr) {
        return NonRetryable
    }
    var jsonTypeErr *json.UnmarshalTypeError
    if errors.As(err, &jsonTypeErr) {
        return NonRetryable
    }
    // 네트워크 타임아웃 → 재시도 가능
    var netErr net.Error
    if errors.As(err, &netErr) && netErr.Timeout() {
        return Retryable
    }
    // 기본: 재시도 가능으로 처리 (보수적)
    return Retryable
}
```

## 재시도 (지수 백오프)

```go
package retry

import (
    "context"
    "fmt"
    "log"
    "time"
)

type Config struct {
    MaxAttempts int
    InitialWait time.Duration
    MaxWait     time.Duration
    Multiplier  float64
}

func DefaultConfig() Config {
    return Config{
        MaxAttempts: 3,
        InitialWait: 100 * time.Millisecond,
        MaxWait:     5 * time.Second,
        Multiplier:  2.0,
    }
}

// Do executes fn with exponential backoff retry.
// Returns nil on success, or the last error after exhausting retries.
func Do(ctx context.Context, cfg Config, fn func() error) error {
    wait := cfg.InitialWait
    var lastErr error

    for attempt := 1; attempt <= cfg.MaxAttempts; attempt++ {
        lastErr = fn()
        if lastErr == nil {
            return nil
        }

        kind := ClassifyError(lastErr)
        if kind == NonRetryable || kind == Fatal {
            return fmt.Errorf("non-retryable error on attempt %d: %w", attempt, lastErr)
        }

        if attempt == cfg.MaxAttempts {
            break
        }

        log.Printf("retry %d/%d after %v: %v", attempt, cfg.MaxAttempts, wait, lastErr)
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-time.After(wait):
        }

        // 지수 증가 + 상한
        wait = time.Duration(float64(wait) * cfg.Multiplier)
        if wait > cfg.MaxWait {
            wait = cfg.MaxWait
        }
    }

    return fmt.Errorf("max retries (%d) exceeded: %w", cfg.MaxAttempts, lastErr)
}
```

## DLQ 라우팅

Spring의 `@RetryableTopic(dltStrategy=...)` 에 해당하는 패턴을 수동 구현한다. DLQ 레코드에는 원본 정보와 실패 사유를 헤더로 포함시켜, 나중에 원인 파악과 재처리가 가능하게 한다.

```go
package dlq

import (
    "context"
    "fmt"
    "time"

    "github.com/twmb/franz-go/pkg/kgo"
)

type Router struct {
    client   *kgo.Client
    dlqTopic string
}

func NewRouter(client *kgo.Client, originalTopic string) *Router {
    return &Router{
        client:   client,
        dlqTopic: originalTopic + ".DLQ",
    }
}

func (d *Router) Route(ctx context.Context, original *kgo.Record, reason error) error {
    dlqRecord := &kgo.Record{
        Topic: d.dlqTopic,
        Key:   original.Key,
        Value: original.Value,
        // 원본 헤더 유지 + DLQ 메타데이터 추가
        Headers: append(cloneHeaders(original.Headers),
            kgo.RecordHeader{Key: "dlq-reason", Value: []byte(reason.Error())},
            kgo.RecordHeader{Key: "dlq-original-topic", Value: []byte(original.Topic)},
            kgo.RecordHeader{Key: "dlq-original-partition", Value: []byte(fmt.Sprintf("%d", original.Partition))},
            kgo.RecordHeader{Key: "dlq-original-offset", Value: []byte(fmt.Sprintf("%d", original.Offset))},
            kgo.RecordHeader{Key: "dlq-timestamp", Value: []byte(time.Now().UTC().Format(time.RFC3339))},
        ),
    }
    results := d.client.ProduceSync(ctx, dlqRecord)
    return results.FirstErr()
}

func cloneHeaders(headers []kgo.RecordHeader) []kgo.RecordHeader {
    if len(headers) == 0 {
        return nil
    }
    cloned := make([]kgo.RecordHeader, len(headers))
    copy(cloned, headers)
    return cloned
}
```

### 통합: Consumer + 재시도 + DLQ

```go
func consumeWithErrorHandling(
    client *kgo.Client,
    dlqRouter *dlq.Router,
    retryCfg retry.Config,
) {
    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }

        fetches.EachError(func(t string, p int32, err error) {
            log.Printf("fetch error: topic=%s partition=%d err=%v", t, p, err)
        })

        fetches.EachRecord(func(r *kgo.Record) {
            err := retry.Do(ctx, retryCfg, func() error {
                return processRecord(r)
            })
            if err != nil {
                log.Printf("DLQ routing record key=%s: %v", string(r.Key), err)
                if dlqErr := dlqRouter.Route(ctx, r, err); dlqErr != nil {
                    log.Printf("DLQ routing FAILED: %v", dlqErr)
                    // DLQ 전송 실패는 커밋하지 않아 재처리 기회를 유지한다
                    return
                }
            }
        })

        if err := client.CommitUncommittedOffsets(ctx); err != nil {
            log.Printf("커밋 실패: %v", err)
        }
    }
}
```

## DLQ Consumer (재처리)

DLQ 토픽을 소비하여 실패 원인을 분석하거나 수동으로 재처리한다.

```go
func consumeDLQ(client *kgo.Client) {
    ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT)
    defer cancel()

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            originalTopic := getHeader(r, "dlq-original-topic")
            reason := getHeader(r, "dlq-reason")
            timestamp := getHeader(r, "dlq-timestamp")
            log.Printf("[DLQ] original=%s reason=%s at=%s key=%s",
                originalTopic, reason, timestamp, string(r.Key))
        })
    }
}

func getHeader(r *kgo.Record, key string) string {
    for _, h := range r.Headers {
        if h.Key == key {
            return string(h.Value)
        }
    }
    return ""
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `DefaultErrorHandler` | `ClassifyError()` 함수 | 에러 분류 |
| `@RetryableTopic(attempts=3)` | `retry.Do(cfg, fn)` | 재시도 |
| `@RetryableTopic(backoff=@Backoff(...))` | `retry.Config.Multiplier` | 백오프 |
| Dead Letter Topic (DLT) | `dlq.Router.Route()` | DLQ 전송 |
| `DeadLetterPublishingRecoverer` | `dlq.Router` 구조체 | DLQ 라우터 |
| `@DltHandler` | DLQ 토픽 별도 Consumer | DLQ 소비 |
| `@RetryableTopic(dltTopicSuffix=".DLT")` | `originalTopic + ".DLQ"` | DLQ 토픽명 |

## 실습 TODO

```
TODO 1: ErrorKind + ClassifyError() 구현 (JSON 에러, 네트워크 에러 포함)
TODO 2: retry.Do() 지수 백오프 구현 및 단위 테스트
TODO 3: dlq.Router 구현 (헤더에 원본 정보 포함)
TODO 4: 정상/실패 메시지 혼합 전송 → DLQ 라우팅 확인
TODO 5: DLQ 토픽 Consumer로 실패 메시지 및 헤더 출력
```

## 체크포인트

- [ ] 재시도 가능 에러: 최대 3회 재시도 후 DLQ 라우팅
- [ ] 재시도 불가 에러: 즉시 DLQ 라우팅 (재시도 없음)
- [ ] DLQ 레코드에 dlq-reason, dlq-original-topic, dlq-original-offset 헤더 존재
- [ ] 로그에서 재시도 횟수, 백오프 시간 확인
- [ ] DLQ Consumer에서 실패 원인 출력 확인
