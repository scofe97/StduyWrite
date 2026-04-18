# 12. Schema Registry & Avro

> **이론**: `02-fundamentals/11-schema-registry.md`
> **Spring 대응**: `03-spring-boot-integration/15-schema-registry-strategy.md`
> **이 문서**: Go에서 franz-go/sr + hamba/avro를 사용한 Schema Registry 연동에 집중.

## 목표

- franz-go/pkg/sr로 Schema Registry 연동
- hamba/avro로 Avro 직렬화/역직렬화
- 스키마 진화 및 호환성 관리
- Spring Boot 프로젝트와 Avro 스키마 공유

## franz-go Schema Registry 클라이언트

franz-go는 `pkg/sr` 패키지로 Schema Registry 클라이언트를 내장하고 있다. Redpanda는 Schema Registry를 자체 내장하므로 별도 컨테이너가 필요 없다. Confluent Schema Registry와 동일한 REST API를 제공하여 Spring Boot 프로젝트와 동일한 Registry를 공유할 수 있다.

```go
import "github.com/twmb/franz-go/pkg/sr"

func newSchemaRegistry() (*sr.Client, error) {
    return sr.NewClient(sr.URLs("http://localhost:18081"))
}
```

## Avro 직렬화 (hamba/avro)

Java의 Avro 생성 클래스(`specific.avro.reader=true`) 대신 Go에서는 구조체 필드에 `avro` 태그를 붙여 매핑한다. Avro는 schema index 기반으로 매핑하므로 필드 순서는 `.avsc` 스키마 파일 기준이다.

```go
import "github.com/hamba/avro/v2"

const orderSchemaJSON = `{
    "type": "record",
    "name": "Order",
    "namespace": "com.example",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "customerId", "type": "string"},
        {"name": "amount", "type": "double"},
        {"name": "status", "type": {"type": "enum", "name": "OrderStatus",
            "symbols": ["PENDING", "CONFIRMED", "CANCELLED"]}}
    ]
}`

type Order struct {
    ID         string  `avro:"id"`
    CustomerID string  `avro:"customerId"`
    Amount     float64 `avro:"amount"`
    Status     string  `avro:"status"`
}

func marshalAvro(order Order) ([]byte, error) {
    schema, err := avro.Parse(orderSchemaJSON)
    if err != nil {
        return nil, err
    }
    return avro.Marshal(schema, order)
}

func unmarshalAvro(data []byte) (Order, error) {
    schema, err := avro.Parse(orderSchemaJSON)
    if err != nil {
        return Order{}, err
    }
    var order Order
    err = avro.Unmarshal(schema, data, &order)
    return order, err
}
```

## Schema Registry 통합

### Serde (Serializer/Deserializer)

franz-go/sr의 `Serde`는 Schema Registry에서 ID를 조회하여 메시지 앞에 5바이트 매직 헤더(`0x00` + 4바이트 schema ID)를 자동으로 붙이고 제거한다. Confluent 호환 포맷이므로 Spring Boot 프로젝트와 상호 운용된다.

```go
func setupSerde(rcl *sr.Client) (*sr.Serde, error) {
    var serde sr.Serde

    // 스키마 등록
    schema, err := rcl.CreateSchema(context.Background(), "orders-value", sr.Schema{
        Schema: orderSchemaJSON,
        Type:   sr.TypeAvro,
    })
    if err != nil {
        return nil, fmt.Errorf("스키마 등록 실패: %w", err)
    }

    // Serde에 타입 등록
    avroSchema, _ := avro.Parse(orderSchemaJSON)
    serde.Register(
        schema.ID,
        Order{},
        sr.EncodeFn(func(v any) ([]byte, error) {
            return avro.Marshal(avroSchema, v)
        }),
        sr.DecodeFn(func(b []byte, v any) error {
            return avro.Unmarshal(avroSchema, b, v)
        }),
    )

    return &serde, nil
}
```

### Producer with Avro

```go
func produceAvro(client *kgo.Client, serde *sr.Serde, order Order) error {
    value, err := serde.Encode(order)
    if err != nil {
        return fmt.Errorf("avro 직렬화 실패: %w", err)
    }

    results := client.ProduceSync(context.Background(), &kgo.Record{
        Topic: "orders",
        Key:   []byte(order.ID),
        Value: value,
    })
    return results.FirstErr()
}
```

### Consumer with Avro

```go
func consumeAvro(client *kgo.Client, serde *sr.Serde) {
    for {
        fetches := client.PollFetches(context.Background())
        fetches.EachRecord(func(r *kgo.Record) {
            var order Order
            if err := serde.Decode(r.Value, &order); err != nil {
                log.Printf("avro 역직렬화 실패: %v", err)
                return
            }
            fmt.Printf("Order: %+v\n", order)
        })
    }
}
```

## 스키마 공유 전략

Spring Boot 프로젝트와 동일한 `.avsc` 파일을 참조하여 스키마 불일치를 방지한다. 두 프로젝트가 동일한 Schema Registry를 바라보면 런타임에서도 호환성이 보장된다.

```
project/
├── redpanda-spring-boot/src/main/avro/  # Java Avro 스키마
├── redpanda-go/avro/                     # Go에서 같은 .avsc 참조
└── docker-compose.yml                    # 동일 Schema Registry
```

```go
// .avsc 파일에서 스키마 로드
func loadSchema(path string) (avro.Schema, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    return avro.Parse(string(data))
}

// 초기화 시 파일에서 로드
schema, err := loadSchema("avro/order.avsc")
if err != nil {
    log.Fatalf("스키마 로드 실패: %v", err)
}
```

## 스키마 진화

### BACKWARD 호환 변경 (새 필드 + 기본값)

기존 Consumer가 V1 스키마로 디코드할 수 있어야 BACKWARD 호환이다. 새 필드에는 반드시 기본값을 지정한다.

```go
const orderSchemaV2 = `{
    "type": "record",
    "name": "Order",
    "namespace": "com.example",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "customerId", "type": "string"},
        {"name": "amount", "type": "double"},
        {"name": "status", "type": {"type": "enum", "name": "OrderStatus",
            "symbols": ["PENDING", "CONFIRMED", "CANCELLED"]}},
        {"name": "region", "type": "string", "default": "KR"}
    ]
}`

// 호환성 확인 후 등록
func registerWithCompatibilityCheck(rcl *sr.Client, subject, newSchema string) error {
    compatible, err := rcl.CheckCompatibility(context.Background(),
        subject,
        sr.Schema{Schema: newSchema, Type: sr.TypeAvro},
        -1, // latest version
    )
    if err != nil {
        return fmt.Errorf("호환성 확인 실패: %w", err)
    }
    if !compatible.Is {
        return fmt.Errorf("스키마 호환 불가: %s", compatible.Compatibility)
    }

    _, err = rcl.CreateSchema(context.Background(), subject, sr.Schema{
        Schema: newSchema,
        Type:   sr.TypeAvro,
    })
    return err
}
```

### 호환성 레벨 설정

```go
// 주제별 호환성 설정
err := rcl.SetCompatibility(context.Background(),
    sr.SetCompatibility(sr.CompatBackward),
    "orders-value",
)
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `spring-kafka-avro` | `franz-go/pkg/sr` + `hamba/avro` | Avro 통합 |
| `KafkaAvroSerializer` | `serde.Encode()` | 직렬화 |
| `KafkaAvroDeserializer` | `serde.Decode()` | 역직렬화 |
| `schema.registry.url` | `sr.URLs(...)` | Registry URL |
| Gradle avro plugin | 수동 `.avsc` 로드 | 코드 생성 없음 |
| `specific.avro.reader=true` | 구조체 + `avro` 태그 | 타입 매핑 |
| `avro.Parse()` N/A | 파싱 후 캐시 권장 | 성능 |

## 실습 TODO

```
TODO 1: Schema Registry에 Order 스키마 등록
TODO 2: Avro Producer → Consumer 라운드트립
TODO 3: 스키마 V2 등록 + BACKWARD 호환성 확인
TODO 4: Spring Boot Producer → Go Consumer 상호 운용 테스트
TODO 5: .avsc 파일 공유 구조 설정
TODO 6: avro.Parse() 결과 캐싱으로 성능 최적화
```

## 체크포인트

- [ ] Schema Registry에 스키마 등록 확인 (`curl localhost:18081/subjects`)
- [ ] Avro 직렬화/역직렬화 라운드트립 성공
- [ ] V1 Producer → V2 Consumer 호환 동작
- [ ] Spring Boot에서 produce한 Avro 메시지를 Go Consumer로 소비
- [ ] 호환 불가 스키마 변경 시 오류 사전 차단
