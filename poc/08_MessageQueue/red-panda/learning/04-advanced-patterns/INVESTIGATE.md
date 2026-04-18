# Advanced Patterns: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. mTLS는 얼마나 느려지는가? 성능 오버헤드를 어떻게 관리하는가?

### 왜 이 질문이 중요한가

TLS를 도입하면 "얼마나 느려지냐"는 질문은 보안 설계 리뷰에서 반드시 나온다. 단순히 "느려진다"고 답하면 부족하고, 핸드셰이크 비용과 세션 재사용 전략, 그리고 인증서 만료가 프로덕션 장애로 이어지는 실제 사례를 함께 설명할 수 있어야 한다.

### 답변

**TLS 핸드셰이크 비용**은 연결 수립 시점에만 발생한다. TLS 1.3 기준 1-RTT(기존 2-RTT에서 개선)이며, RSA 4096보다 ECDSA P-256이 CPU 부담이 약 10배 적다. 한 번 맺은 연결은 세션 키를 재사용하므로, 연결이 유지되는 동안의 추가 비용은 AES-GCM 암호화 오버헤드(대략 5~10%)뿐이다.

실무에서 더 위험한 문제는 **인증서 만료**다. 인증서가 만료되면 브로커와 클라이언트 연결이 일제히 끊기고 클러스터 전체가 중단된다. 이를 막으려면 만료 30일 전 자동 갱신을 강제해야 한다.

```bash
# cert-manager (K8s) — 만료 30일 전 자동 갱신
apiVersion: cert-manager.io/v1
kind: Certificate
spec:
  renewBefore: 720h  # 30일
  duration: 8760h    # 1년

# 인증서 만료 모니터링 (Prometheus alert)
- alert: CertExpiringSoon
  expr: (x509_cert_expiry - time()) / 86400 < 30
  labels:
    severity: warning
```

**세션 재사용**으로 핸드셰이크 빈도를 줄이는 것도 중요하다. Kafka 클라이언트는 기본적으로 연결을 유지(keep-alive)하므로, 불필요한 연결 끊김을 방지하는 것만으로도 TLS 오버헤드를 최소화할 수 있다.

---

## Q2. 멀티테넌트 환경에서 SASL + ACL을 어떻게 설계하는가?

### 왜 이 질문이 중요한가

팀이 늘어나고 서비스가 많아질수록 "누가 어떤 토픽에 쓸 수 있는가"를 체계적으로 관리해야 한다. 면접에서는 단순 설정 방법보다 "왜 그 구조로 설계했는가"를 묻는다. ACL이 폭발적으로 늘어나는 문제와 서비스 계정 기반 설계를 설명할 수 있어야 한다.

### 답변

멀티테넌트 설계의 핵심은 **인증(SASL)과 인가(ACL)를 분리**하고, 사람이 아닌 **서비스 계정** 단위로 권한을 부여하는 것이다.

```
팀 A 서비스      →  service-account: payments-producer
                    ACL: WRITE on topic:payments-*

팀 B 서비스      →  service-account: analytics-consumer
                    ACL: READ on topic:payments-*, consumer-group:analytics-*
```

실제 설정 흐름은 다음과 같다.

```bash
# 1. SASL 사용자(서비스 계정) 생성
rpk acl user create payments-producer --password "$SECRET"

# 2. 토픽 접근 ACL 부여 (와일드카드로 팀 네임스페이스 단위 관리)
rpk acl create \
  --allow-principal User:payments-producer \
  --operation write \
  --topic "payments-*"

# 3. 컨슈머 그룹 ACL (읽기에는 그룹 권한도 필요)
rpk acl create \
  --allow-principal User:analytics-consumer \
  --operation read \
  --topic "payments-*" \
  --group "analytics-*"
```

**ACL 폭발 문제**는 토픽명에 팀 접두사(`payments-`, `inventory-`)를 강제하고 와일드카드 ACL을 사용함으로써 억제한다. 서비스마다 토픽마다 ACL을 개별 등록하면 수백 개로 늘어나 운영이 불가능해진다. 토픽 네이밍 컨벤션과 ACL 설계는 함께 결정해야 한다.

---

## Q3. OpenTelemetry 샘플링 전략 — Head vs Tail, 무엇을 언제 선택하는가?

### 왜 이 질문이 중요한가

트레이스를 100% 수집하면 스토리지 비용이 폭발하고, 너무 낮은 비율로 샘플링하면 실제 문제를 놓친다. 이 트레이드오프를 이해하고 상황에 맞는 전략을 선택하는 능력은 관찰 가능성 설계의 핵심 역량이다.

### 답변

두 전략의 결정적 차이는 **언제 샘플링 결정을 내리는가**에 있다.

| 전략 | 결정 시점 | 장점 | 단점 |
|------|----------|------|------|
| Head Sampling | 요청 시작 시 | 오버헤드 낮음, 구현 단순 | 에러 트레이스를 버릴 수 있음 |
| Tail Sampling | 전체 트레이스 완료 후 | 에러/느린 요청 100% 보존 | OTel Collector 메모리 필요 |

**Head Sampling 설정 예시** (OTel Collector):

```yaml
# 전체의 10%만 수집
sampler:
  type: traceidratiobased
  ratio: 0.1
```

**Tail Sampling 설정 예시** — 에러와 느린 요청은 반드시 보존:

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors-policy
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-traces-policy
        type: latency
        latency: { threshold_ms: 1000 }
      - name: base-rate-policy
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

실무 권장 패턴은 **Head Sampling 10% + Tail Sampling으로 에러/지연 트레이스 100% 보존**을 조합하는 것이다. Kafka/Redpanda 환경에서는 프로듀서 → 브로커 → 컨슈머로 이어지는 트레이스 컨텍스트를 메시지 헤더로 전파해야 하므로, `traceparent` 헤더 전파 설정을 누락하지 않도록 주의한다.

---

## Q4. Redpanda에서 Quota와 Rate Limiting을 어떻게 설정하는가?

### 왜 이 질문이 중요한가

하나의 프로듀서가 네트워크 대역폭을 독점하면 다른 서비스 전체가 느려진다. 이를 방어하는 Quota 설정을 모르면 멀티테넌트 환경에서 "왜 갑자기 전체 서비스가 느려지는가"를 진단하지 못한다. 면접에서는 설정 방법뿐 아니라 쓰로틀링이 발생했을 때 클라이언트 동작을 설명할 수 있어야 한다.

### 답변

Redpanda의 Quota는 클라이언트 ID 단위로 프로듀서/컨슈머 처리량을 제한한다. 쓰로틀링이 발생하면 브로커가 클라이언트에게 대기 시간(throttle_time_ms)을 응답에 포함해 전달하고, 클라이언트는 그만큼 대기 후 재전송한다. 따라서 클라이언트가 튕기는 것이 아니라 속도가 낮아지는 방식으로 동작한다.

```bash
# 클라이언트 ID "payments-producer"의 프로듀서 처리량을 10MB/s로 제한
rpk cluster config set \
  quota_producer_byte_rate 10485760  # 전역 기본값 (10MB/s)

# 특정 클라이언트에만 적용 (rpk acl quota)
rpk acl quota create \
  --client-id "payments-producer" \
  --producer-byte-rate 5242880   # 5MB/s

# 컨슈머 처리량 제한
rpk acl quota create \
  --client-id "analytics-consumer" \
  --consumer-byte-rate 20971520  # 20MB/s

# 현재 쓰로틀링 여부 확인
rpk cluster metrics | grep throttle
```

**Prometheus 알림 설정** — 쓰로틀링이 지속되면 처리 지연으로 이어지므로 알림이 필수다:

```yaml
- alert: KafkaProducerThrottled
  expr: rate(kafka_producer_throttle_time_avg[5m]) > 100  # 100ms 초과
  labels:
    severity: warning
  annotations:
    summary: "프로듀서 {{ $labels.client_id }} 쓰로틀링 발생"
```

**설계 팁**: Quota는 팀 접두사 기반 클라이언트 ID 컨벤션(`{team}-{service}-{role}`)과 조합해야 관리가 쉽다. 클라이언트 ID가 임의 문자열이면 Quota를 개별 등록해야 하지만, 팀 단위 패턴이 있으면 기본값으로 커버 범위를 넓힐 수 있다.
