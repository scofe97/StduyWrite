# Event-Driven PoC (Redpanda 전용): Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. WASM Transform의 성능 한계 — 어떤 변환이 브로커 내부 실행에 적합한가?

### 왜 이 질문이 중요한가

WASM Transforms는 "브로커 내부에서 실행"이라는 아이디어 자체가 매력적이지만, 브로커는 원래 메시지 라우팅에 최적화된 프로세스다. 면접에서 "언제 WASM Transform을 쓰고 언제 외부 Consumer를 쓰겠느냐"라고 물으면, 단순히 지연시간만 비교해서 답하면 얕은 답변이 된다. 실무에서는 브로커 CPU를 WASM이 점유할 때 파티션 전체 처리량이 함께 낮아지는 문제를 직접 겪게 된다.

### 답변

WASM Transform은 Redpanda 브로커 스레드 풀에서 직접 실행된다. 브로커는 I/O 스레드와 CPU 스레드를 엄격하게 분리(Seastar 기반)하고 있어, WASM 실행이 CPU 스레드를 오래 점유하면 같은 코어에 할당된 파티션의 produce/consume 레이턴시가 올라간다.

**적합한 변환 (CPU 소모 낮음, 결과가 결정적)**
- PII 필드 마스킹 (특정 키의 값을 `***`로 교체)
- 필드 추가/제거 (JSON 구조 변환)
- 타입 변환 (문자열 → 숫자, 날짜 포맷 정규화)
- 토픽 라우팅 (조건에 따라 출력 토픽 선택)

**부적합한 변환 (CPU 소모 높거나 I/O 필요)**
- 외부 API 호출 (HTTP 조회로 필드 보강) — WASM 샌드박스에서 네트워크 I/O 불가
- 복잡한 집계 (윈도우 합산, 조인) — 상태 저장 불가, 메시지 단위 처리만 허용
- 이미지/바이너리 인코딩 변환 — CPU 집약적이어서 브로커 처리량 저하
- ML 추론 — 모델 로딩 자체가 메모리/CPU 예산 초과

**설정 예시 — 메모리 한계 명시**

```yaml
# rpk transform deploy 시 리소스 제한
transforms:
  - name: pii-masker
    input_topic: raw-events
    output_topics: [clean-events]
    # 브로커 기본 제한: 함수당 메모리 2MB, 실행 시간 제한 있음
    # 복잡한 로직은 Redpanda Connect로 분리
```

결론적으로 WASM Transform은 "메시지 하나를 받아 즉시 변환하여 내보내는" 순수 함수형 변환에만 사용해야 한다. 상태, 외부 I/O, 높은 CPU 소모가 필요하면 Redpanda Connect 또는 외부 Consumer를 써야 한다.

---

## Q2. WASM vs Redpanda Connect — 브로커 내 변환과 외부 파이프라인 선택 기준

### 왜 이 질문이 중요한가

Redpanda는 WASM Transforms와 Connect(구 Benthos) 두 가지 변환 수단을 제공한다. 면접에서 "Redpanda에서 데이터 변환을 어떻게 구성하겠냐"라는 질문에 둘 다 안다는 사실을 보여주려면, 각각의 운영 단위(브로커 프로세스 vs 독립 프로세스)가 다르다는 점에서 출발해서 선택 기준을 설명해야 한다.

### 답변

| 기준 | WASM Transform | Redpanda Connect |
|------|----------------|-----------------|
| 실행 위치 | 브로커 내부 (인프라 추가 없음) | 독립 프로세스 (별도 배포 필요) |
| 외부 I/O | 불가 (샌드박스) | 가능 (HTTP, DB, S3 등 200+ 커넥터) |
| 상태 저장 | 불가 (메시지 단위) | 가능 (캐시, 집계 윈도우) |
| 레이턴시 | 브로커 처리 경로와 동일 (낮음) | 네트워크 홉 추가 (약간 높음) |
| 확장 | 파티션 수에 따라 자동 | 인스턴스 수동 확장 필요 |
| 장애 격리 | 브로커와 운명 공유 | 파이프라인 장애가 브로커에 무영향 |

**선택 규칙**
- 마스킹·필드 변환·라우팅처럼 외부 의존성 없는 변환 → WASM Transform
- 외부 API 조회, DB Lookup, S3 싱크, 복잡한 집계 → Redpanda Connect
- 장애 격리가 중요한 프로덕션 파이프라인 → Redpanda Connect (브로커 영향 차단)

**Redpanda Connect 파이프라인 예시 (HTTP Enrich)**

```yaml
input:
  kafka_franz:
    seed_brokers: [localhost:9092]
    topics: [raw-events]

pipeline:
  processors:
    - http:
        url: https://geo-api.internal/lookup
        verb: GET
    - mapping: |
        root = this
        root.geo = content().string()

output:
  kafka_franz:
    seed_brokers: [localhost:9092]
    topic: enriched-events
```

이 파이프라인에서 외부 HTTP 조회가 포함되어 있어 WASM으로는 구현이 불가능하다. 이처럼 "외부 의존성 유무"가 두 수단을 가르는 가장 명확한 기준이다.

---

## Q3. Iceberg Topics의 실시간성 — flush 주기와 쿼리 지연 사이 트레이드오프

### 왜 이 질문이 중요한가

Iceberg Topics를 "실시간 데이터 레이크하우스"라고 부르지만, Iceberg 파일 포맷(Parquet)의 특성상 데이터를 즉시 읽을 수는 없다. 면접에서 "Iceberg Topics로 실시간 대시보드를 만들 수 있냐"라고 물으면, flush 주기와 쿼리 지연 사이의 관계를 구체적인 수치로 설명할 수 있어야 한다.

### 답변

Redpanda Iceberg Topics는 토픽에 쓰인 메시지를 주기적으로 Parquet 파일로 플러시하고 Iceberg 메타데이터(manifest)를 업데이트한다. Spark나 Trino 같은 쿼리 엔진은 메타데이터를 먼저 읽고 나서 Parquet 파일을 스캔하기 때문에, 플러시 전 데이터는 쿼리에 노출되지 않는다.

**flush 주기 설정과 지연 관계**

```yaml
# redpanda.yaml 또는 토픽 설정
redpanda:
  iceberg_target_snapshot_interval_ms: 30000  # 30초마다 스냅샷
  iceberg_snapshot_ms: 10000                   # 10초 플러시 (최소 단위)
```

- `iceberg_snapshot_ms: 10000` → 쿼리 지연 10~20초 (플러시 직후 쿼리 시 다음 플러시까지 대기 가능)
- `iceberg_snapshot_ms: 60000` → 쿼리 지연 최대 60초, 파일 수 감소로 S3 비용 절감

**실무 선택 기준**

| 시나리오 | 권장 설정 | 이유 |
|----------|-----------|------|
| 분 단위 실시간 대시보드 | 10~30초 플러시 | 수용 가능한 지연, 파일 수 증가 감수 |
| 시간 단위 배치 분석 | 5~10분 플러시 | 파일 수 최소화, S3 비용 절감 |
| 초 단위 실시간 알림 | Iceberg Topics 부적합 → Consumer 사용 | Parquet 구조상 초 단위 불가 |

결국 Iceberg Topics는 "분 단위 준실시간 분석"과 "별도 파이프라인 없는 배치 분석"을 동시에 해결하는 데 가장 적합하고, 초 단위 SLA가 필요한 알림이나 이상 탐지는 별도 Consumer로 처리해야 한다.

---

## Q4. Iceberg 통합 시 스키마 진화 — Avro 스키마 변경이 Iceberg 테이블에 미치는 영향

### 왜 이 질문이 중요한가

Redpanda에서 Avro로 직렬화된 메시지를 Iceberg Topics로 저장할 때, Schema Registry의 스키마 버전이 바뀌면 Iceberg 테이블 컬럼도 연동되어야 한다. 이 연동이 자동으로 되는지, 어떤 변경은 안전하고 어떤 변경은 Iceberg 테이블을 깨뜨리는지를 모르면 프로덕션에서 데이터 유실 또는 쿼리 실패가 발생한다.

### 답변

Redpanda Iceberg Topics는 Schema Registry와 연동하여 Avro 스키마를 Iceberg 스키마로 변환한다. Avro의 스키마 호환성 규칙과 Iceberg의 스키마 진화 규칙이 다르기 때문에, 호환 가능한 Avro 변경이더라도 Iceberg 테이블에서는 주의가 필요한 경우가 있다.

**Avro 변경 유형별 Iceberg 영향**

| Avro 변경 | Avro 호환성 | Iceberg 영향 |
|-----------|------------|-------------|
| 필드 추가 (default 있음) | BACKWARD 호환 | Iceberg 컬럼 추가 — 안전 |
| 필드 제거 (default 있던 것) | FORWARD 호환 | Iceberg 컬럼 null 처리 — 기존 데이터 유지 |
| 필드 타입 변경 (int→long) | 호환 불가 | Iceberg 타입 충돌 — 파이프라인 중단 위험 |
| 필드 이름 변경 | 호환 불가 | Iceberg에서 구 컬럼 + 신 컬럼 동시 존재 가능 |

**안전한 스키마 진화 전략**

```json
// 기존 스키마 (v1)
{"name": "user_id", "type": "string"}

// 안전한 변경: 필드 추가 + default 필수
{"name": "user_id",  "type": "string"},
{"name": "user_tier","type": ["null","string"], "default": null}  // nullable + default null
```

필드 이름을 바꿔야 할 때는 구 필드를 deprecated로 두고 신 필드를 추가한 뒤, Iceberg 테이블에서 구 컬럼 데이터를 마이그레이션 후 제거하는 2단계 전략을 써야 한다. 타입 변경은 스키마 호환성 자체가 깨지므로 새 토픽 + 새 Iceberg 테이블로 마이그레이션하는 것이 유일한 안전한 방법이다.
