# Redpanda WASM Data Transforms - PII 마스킹

브로커 내부에서 WebAssembly로 데이터를 변환하는 실습 프로젝트.

## 아키텍처

```
Producer → [raw-orders] → WASM Transform (브로커 내부) → [cleaned-orders] → Consumer
                              ↑
                       PII 마스킹 (< 2ms)
                       - 이름: 홍길동 → 홍**
                       - 전화: 010-1234-5678 → 010-****-5678
                       - 이메일: hong@ex.com → ho**@ex.com
                       - 주소: 서울시... → ***
```

## 사전 조건

- Redpanda v24.3+ (WASM Transforms GA)
- Node.js 18+
- rpk CLI

## 실행 방법

### 1. Redpanda 시작 (WASM 활성화)

```bash
cd ../
docker compose -f docker-compose-wasm.yml up -d
```

### 2. 토픽 생성

```bash
rpk topic create raw-orders -p 3 --brokers localhost:19092
rpk topic create cleaned-orders -p 3 --brokers localhost:19092
```

### 3. Transform 빌드 및 배포

```bash
npm install
npm run build

rpk transform deploy \
  --name pii-masking \
  --input-topic raw-orders \
  --output-topic cleaned-orders \
  --file dist/transform.wasm \
  --brokers localhost:19092
```

### 4. 테스트

```bash
# 단위 테스트
npm test

# 수동 테스트: 원본 이벤트 발행
rpk topic produce raw-orders --brokers localhost:19092 <<EOF
{"orderId":"ORD-001","customerInfo":{"name":"홍길동","phone":"010-1234-5678","email":"hong@example.com","address":"서울시 강남구"}}
EOF

# 마스킹된 이벤트 확인
rpk topic consume cleaned-orders --brokers localhost:19092 --num 1
# → {"orderId":"ORD-001","customerInfo":{"name":"홍**","phone":"010-****-5678","email":"ho**@example.com","address":"***"}}
```

### 5. 모니터링

```bash
rpk transform list --brokers localhost:19092
rpk transform describe pii-masking --brokers localhost:19092
```

## 참고 자료

- [Redpanda Data Transforms 공식 문서](https://docs.redpanda.com/current/develop/data-transforms/)
- [Transform SDK - JavaScript/TypeScript](https://www.npmjs.com/package/@redpanda-data/transform-sdk)
- [Transform SDK - Go](https://github.com/redpanda-data/redpanda/tree/dev/src/transform-sdk/go/transform)
- [학습 문서](../../learning/05-event-driven-poc/09-wasm-transforms.md)
