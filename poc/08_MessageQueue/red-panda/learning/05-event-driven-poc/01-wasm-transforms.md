# 09. WASM Data Transforms (브로커 내 데이터 변환)

Redpanda 브로커 내부에서 WebAssembly(WASM)로 데이터를 변환. JavaScript/TypeScript로 PII 마스킹, 필터링 구현.

## 왜 WASM Transforms인가?

### 기존 방식의 문제점: 데이터 핑퐁

```
Producer → Broker (raw data) → Consumer (transform) → Broker (cleaned data)
  1ms         1ms                   50ms                    1ms
```

**문제점**:
- **지연시간 증가**: 50ms+ 추가 지연
- **네트워크 비용**: 동일 데이터를 두 번 전송
- **복잡도 증가**: 별도의 Consumer 애플리케이션 관리
- **확장성 문제**: Consumer 인스턴스 추가 관리 필요

### WASM Transforms 방식: 브로커 내 변환

```
Producer → Redpanda Broker (WASM Transform 내장) → Consumer
  1ms              2ms                                 1ms
```

**장점**:
- **지연시간 감소**: < 2ms
- **네트워크 비용 절감**: 한 번만 전송
- **운영 간소화**: 별도의 Consumer 불필요
- **자동 확장**: Redpanda 클러스터와 함께 확장

### GA (Generally Available) 상태

Redpanda WASM Transforms는 Redpanda 24.3부터 정식(GA) 기능으로 제공됩니다.

## 지원 언어 및 SDK

### 공식 SDK 지원 언어

| 언어 | SDK | 사용 사례 |
|------|-----|-----------|
| **JavaScript/TypeScript** | `@redpanda-data/transform-sdk` | 빠른 프로토타입, JSON 처리 |
| **Go** | `github.com/redpanda-data/redpanda/transform-sdk-go` | 고성능, 타입 안전성 |
| **Rust** | `redpanda-transform-sdk` | 최고 성능, 메모리 효율성 |

## 적합한 사용 사례

WASM Transforms는 **stateless(무상태)** 변환에 적합합니다.

### ✅ 적합한 사용 사례

| 사용 사례 | 설명 | 예시 |
|-----------|------|------|
| **필터링** | 특정 조건의 이벤트만 통과 | `status != "CANCELLED"` |
| **마스킹** | PII(개인정보) 필드 숨김 | 전화번호 `010-****-1234` |
| **변환** | 데이터 포맷 변경 | JSON → Avro, CSV → JSON |
| **필드 추출** | 필요한 필드만 선택 | `{id, name}`만 추출 |
| **라우팅** | 내용 기반 토픽 분기 | VIP 고객 → 별도 토픽 |

### ❌ 부적합한 사용 사례 (대안 필요)

| 사용 사례 | 이유 | 대안 |
|-----------|------|------|
| **집계(Aggregation)** | 상태 저장 필요 | Kafka Streams, Flink |
| **조인(Join)** | 여러 스트림 결합 | Kafka Streams, Flink |
| **윈도우 연산** | 시간 기반 상태 관리 | Kafka Streams, Flink |
| **외부 API 호출** | 네트워크 I/O 차단 | Redpanda Connect |
| **데이터베이스 조회** | 외부 상태 저장소 접근 | Redpanda Connect |

## 실습 시나리오: 주문 이벤트 PII 마스킹

### 원본 이벤트 (raw-orders 토픽)

```json
{
  "orderId": "ORD-20260206-001",
  "customerId": "CUST-12345",
  "items": [
    { "productId": "PROD-001", "quantity": 2, "price": 50000 }
  ],
  "totalAmount": 100000,
  "status": "PENDING",
  "customerInfo": {
    "name": "홍길동",
    "phone": "010-1234-5678",
    "email": "hong@example.com",
    "address": "서울시 강남구 테헤란로 123"
  },
  "createdAt": "2026-02-06T10:30:00Z"
}
```

### 변환 후 이벤트 (cleaned-orders 토픽)

```json
{
  "orderId": "ORD-20260206-001",
  "customerId": "CUST-12345",
  "items": [
    { "productId": "PROD-001", "quantity": 2, "price": 50000 }
  ],
  "totalAmount": 100000,
  "status": "PENDING",
  "customerInfo": {
    "name": "홍**",
    "phone": "010-****-5678",
    "email": "ho**@example.com",
    "address": "***"
  },
  "createdAt": "2026-02-06T10:30:00Z"
}
```

## JavaScript/TypeScript WASM Transform 구현

### 프로젝트 초기화

```bash
mkdir wasm-transforms && cd wasm-transforms
npm init -y
npm install --save-dev @redpanda-data/transform-sdk typescript
```

### Transform 로직 구현 (src/transform.ts)

```typescript
import { onRecordWritten } from "@redpanda-data/transform-sdk";

onRecordWritten((event, writer) => {
  try {
    const rawValue = event.record.value;
    if (!rawValue) {
      return;
    }

    const textValue = rawValue.text();
    const data = JSON.parse(textValue);

    // PII 마스킹 적용
    if (data.customerInfo) {
      if (data.customerInfo.phone) {
        data.customerInfo.phone = maskPhone(data.customerInfo.phone);
      }

      if (data.customerInfo.address) {
        data.customerInfo.address = "***";
      }

      if (data.customerInfo.name) {
        data.customerInfo.name = maskName(data.customerInfo.name);
      }

      if (data.customerInfo.email) {
        data.customerInfo.email = maskEmail(data.customerInfo.email);
      }
    }

    writer.write({
      ...event.record,
      value: JSON.stringify(data),
    });
  } catch (error) {
    console.error("Transform error:", error);
    writer.write(event.record);
  }
});

function maskPhone(phone: string): string {
  return phone.replace(/(\d{3})-?\d{4}(-?\d{4})/, "$1-****$2");
}

function maskName(name: string): string {
  if (name.length <= 1) return name;
  return name.charAt(0) + "*".repeat(name.length - 1);
}

function maskEmail(email: string): string {
  const [local, domain] = email.split("@");
  if (!domain) return email;

  const visibleLength = Math.max(1, Math.floor(local.length / 2));
  const maskedLocal = local.substring(0, visibleLength) + "**";
  return `${maskedLocal}@${domain}`;
}
```

## WASM Transform 배포 및 관리

### Transform 빌드

```bash
npm run build
```

**출력**:
```
✓ TypeScript compiled successfully
✓ WASM module built: dist/transform.wasm (42KB)
```

### Transform 배포

```bash
rpk transform deploy \
  --name pii-masking-transform \
  --input-topic raw-orders \
  --output-topic cleaned-orders \
  --file dist/transform.wasm
```

**출력**:
```
Transform deployed successfully!

Name:         pii-masking-transform
Input Topic:  raw-orders
Output Topic: cleaned-orders
Status:       RUNNING
```

### Transform 목록 조회

```bash
rpk transform list
```

**출력**:
```
NAME                      INPUT TOPIC   OUTPUT TOPIC    STATUS    DEPLOYED AT
pii-masking-transform     raw-orders    cleaned-orders  RUNNING   2026-02-06 10:30:00
```

### Transform 메트릭 조회

```bash
rpk transform describe pii-masking-transform
```

**출력**:
```
Name:              pii-masking-transform
Status:            RUNNING
Input Topic:       raw-orders
Output Topic:      cleaned-orders
Records Processed: 15,234
Errors:            0
Avg Latency:       1.8ms
Throughput:        500 msg/sec
Memory Usage:      12MB
CPU Usage:         5%
```

## Docker Compose 설정

```yaml
version: '3.8'

services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v25.3.1
    command:
      - redpanda start
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --mode dev-container
      - --set redpanda.data_transforms_enabled=true
      - --set redpanda.data_transforms_per_core_memory_reservation=10485760
      - --set redpanda.data_transforms_per_function_memory_limit=5242880
    ports:
      - "19092:19092"
      - "9644:9644"
    volumes:
      - redpanda-data:/var/lib/redpanda/data

volumes:
  redpanda-data:
```

## Producer와 Consumer 구현

### Producer (Node.js)

```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'order-producer',
  brokers: ['localhost:19092']
});

const producer = kafka.producer();

async function sendOrder() {
  await producer.connect();

  const order = {
    orderId: `ORD-${Date.now()}`,
    customerId: 'CUST-12345',
    items: [{ productId: 'PROD-001', quantity: 2, price: 50000 }],
    totalAmount: 100000,
    status: 'PENDING',
    customerInfo: {
      name: '홍길동',
      phone: '010-1234-5678',
      email: 'hong@example.com',
      address: '서울시 강남구 테헤란로 123'
    },
    createdAt: new Date().toISOString()
  };

  await producer.send({
    topic: 'raw-orders',
    messages: [{ value: JSON.stringify(order) }]
  });

  console.log('Order sent:', order.orderId);
  await producer.disconnect();
}

sendOrder();
```

### Consumer (Node.js)

```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'analytics-consumer',
  brokers: ['localhost:19092']
});

const consumer = kafka.consumer({ groupId: 'analytics-team' });

async function consumeCleanedOrders() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'cleaned-orders', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const order = JSON.parse(message.value.toString());
      console.log('Received cleaned order:', {
        orderId: order.orderId,
        name: order.customerInfo.name,        // 홍**
        phone: order.customerInfo.phone,      // 010-****-5678
        email: order.customerInfo.email,      // ho**@example.com
        address: order.customerInfo.address   // ***
      });
    }
  });
}

consumeCleanedOrders();
```

## Apache Flink vs WASM Transforms 비교

| 항목 | Redpanda WASM Transforms | Apache Flink |
|------|--------------------------|--------------|
| **배포 복잡도** | ⭐⭐⭐⭐⭐ 단순 | ⭐⭐ 복잡 |
| **지연시간** | < 2ms | 10-50ms |
| **상태 관리** | ❌ Stateless만 | ✅ Stateful 지원 |
| **집계/조인** | ❌ 불가능 | ✅ 가능 |
| **리소스** | 브로커 메모리 공유 | 별도 클러스터 필요 |
| **언어** | JS/TS, Go, Rust | Java, Scala, Python |
| **학습 곡선** | ⭐⭐ 낮음 | ⭐⭐⭐⭐ 높음 |

## 성능 및 제약사항

### 메모리 제한

```yaml
--set redpanda.data_transforms_per_core_memory_reservation=10485760  # 코어당 10MB
--set redpanda.data_transforms_per_function_memory_limit=5242880    # 함수당 5MB
```

**권장사항**:
- Transform 로직을 가볍게 유지 (< 1MB 메모리)
- 큰 객체 생성 지양
- 메모리 누수 방지

### 네트워크 I/O 제한

WASM 환경에서는 외부 네트워크 호출이 **차단**됩니다.

**불가능한 작업**:
- HTTP API 호출
- 데이터베이스 쿼리
- 외부 서비스 연동

**대안**: Redpanda Connect 사용

## 실습 체크리스트

- [ ] Redpanda 클러스터 시작 (WASM Transforms 활성화)
- [ ] TypeScript Transform 프로젝트 초기화
- [ ] PII 마스킹 로직 구현
- [ ] Transform 빌드 (`npm run build`)
- [ ] Transform 배포 (`rpk transform deploy`)
- [ ] Producer로 원본 주문 이벤트 발행
- [ ] Consumer로 마스킹된 이벤트 수신 확인
- [ ] Transform 메트릭 확인
- [ ] Transform 로그 확인
- [ ] Transform 업데이트 및 재배포

## 다음 단계

- **10장**: Redpanda Connect로 외부 시스템 연동
- **11장**: 이벤트 기반 시스템 테스트 전략

## 참고 자료

- [Redpanda Data Transforms 공식 문서](https://docs.redpanda.com/current/develop/data-transforms/)
- [Transform SDK - JavaScript/TypeScript](https://www.npmjs.com/package/@redpanda-data/transform-sdk)
- [Transform SDK - Go](https://github.com/redpanda-data/redpanda/tree/dev/src/transform-sdk/go/transform)
