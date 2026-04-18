# 11. 토픽 거버넌스와 GitOps 운영

GitOps 기반 토픽 자동화, 가드레일 정책 강제, 토픽 수명주기 관리. 토픽 네이밍/파티셔닝은 [10-topic-design.md](./10-topic-design.md) 참조.

---

## 1. 왜 거버넌스가 실패하는가

### 1.1 "거버넌스 극장(Governance Theater)" — Conduktor의 분석

거버넌스가 실패하는 패턴은 조직 간에 놀라울 정도로 일관적이다:

1. **문서화된 네이밍 컨벤션** → "급해서 나중에 고치려고 했는데..." → 6개월 뒤 100개의 비표준 토픽
2. **보존 정책 30일 설정** → 30초 만에 소비되는 데이터인데 "혹시 몰라서..." → 디스크 비용 폭증
3. **Replication Factor 1** → 프로덕션에서! "데모 후에 올리려고..." → 브로커 장애 시 데이터 유실

**근본 원인**: 인간이 기억하는 것에 의존하는 거버넌스는, 인간이 잊을 때 실패한다. 코드 리뷰에서 토픽 설정을 놓치는 것은 리뷰어의 잘못이 아니라, 시스템이 잡아내지 못하는 것이 문제다.

### 1.2 가드레일(Guardrails) vs 가이드라인(Guidelines)

**가이드라인 (실패하는 접근):**
- 위키에 "RF=3 사용하세요" 문서화
- 코드 리뷰에서 확인 (놓치기 쉬움)
- 포스트모템에서 "다음부터 주의합시다"

**가드레일 (성공하는 접근):**
- RF < 3인 토픽 생성 요청을 시스템이 **자동 거부**
- 네이밍 규칙 위반 시 CI/CD 파이프라인 **자동 실패**
- 스키마 호환성 검사 **자동 실행**

**성공 지표**: 정책 위반 인시던트가 0에 수렴해야 한다. 개발자가 정책 위반 시 즉시 피드백을 받고, 도움 요청 없이 스스로 수정할 수 있어야 한다. 이것이 "가드레일"의 본질이다.

---

## 2. GitOps 기반 토픽 관리

토픽 설정을 Git 저장소에서 선언적으로 관리하고, CI/CD 파이프라인을 통해 클러스터에 적용하는 방식이다. 인프라를 코드로 관리하는 IaC(Infrastructure as Code) 원칙을 토픽 관리에 적용한 것이다.

### 2.1 중앙집중형 (Centralized Repository)

모든 팀의 토픽 정의를 하나의 저장소에서 관리한다:

```
kafka-topics-repo/
├── README.md
├── policies/
│   └── topic-policy.yaml        # 조직 전체 정책
├── teams/
│   ├── order-team/
│   │   ├── topics.yaml          # 토픽 정의
│   │   └── schemas/             # Avro/Protobuf 스키마
│   ├── payment-team/
│   │   ├── topics.yaml
│   │   └── schemas/
│   └── inventory-team/
│       ├── topics.yaml
│       └── schemas/
└── .github/
    └── workflows/
        ├── validate.yml          # PR 시 검증
        └── apply.yml             # 머지 시 적용
```

**장점**: 전체 토픽 현황을 한 곳에서 파악할 수 있고, 일관된 정책을 강제하기 쉬우며, PR 리뷰로 변경을 통제할 수 있다.

**단점**: 모든 팀이 같은 저장소에 PR을 올리므로 병목이 될 수 있고, 팀 자율성이 제한된다.

### 2.2 분산형 (Decentralized)

각 서비스 저장소에서 해당 서비스가 소유하는 토픽만 관리한다:

```
order-service-repo/
├── src/
├── kafka/
│   ├── topics.yaml              # 이 서비스가 소유하는 토픽만
│   └── schemas/
└── .github/
    └── workflows/
        └── kafka-apply.yml       # 공통 GitHub Action 호출
```

**장점**: 팀 자율성이 높고, 서비스 코드와 토픽 설정이 같은 저장소에서 버전 관리된다.

**단점**: 전체 현황 파악이 어렵고, 네이밍 규칙 강제를 위해 별도 도구(정책 서버, Webhook)가 필요하다.

### 2.3 Java 코드(NewTopic) vs YAML 선언적 관리

Spring Boot 환경에서 토픽을 관리하는 방법은 크게 두 가지다. `NewTopic` Bean으로 애플리케이션 코드에서 생성하는 방식과, YAML 파일로 선언하고 외부 도구(Jikkou, Terraform 등)로 적용하는 방식이다.

**Java 코드 방식 (NewTopic Bean):**

```java
@Configuration
public class KafkaTopicConfig {
    @Bean
    public NewTopic orderCreatedTopic() {
        return TopicBuilder.name("orders.order.created")
            .partitions(12)
            .replicas(3)
            .config(TopicConfig.RETENTION_MS_CONFIG, "604800000")
            .build();
    }
}
```

애플리케이션이 기동할 때 `KafkaAdmin`이 브로커에 토픽이 없으면 생성한다. 이미 존재하면 **파티션 수 증가만** 반영하고, 설정 변경이나 파티션 감소는 무시한다.

**YAML 선언적 방식 (Jikkou 예시):**

```yaml
apiVersion: 'kafka.jikkou.io/v1beta2'
kind: 'KafkaTopic'
metadata:
  name: 'orders.order.created'
spec:
  partitions: 12
  replicas: 3
  configs:
    retention.ms: '604800000'
```

`jikkou apply`로 적용하면 토픽 생성·설정 변경·삭제까지 모두 처리한다.

**비교:**

| 기준 | Java NewTopic | YAML + 외부 도구 |
|------|--------------|-----------------|
| 토픽 생성 | 앱 기동 시 자동 | CI/CD 파이프라인에서 적용 |
| 설정 변경 | 제한적 (파티션 증가만) | 전체 설정 변경 가능 |
| 토픽 삭제 | 불가 (Bean 제거해도 토픽 유지) | 가능 (선언에 없으면 삭제) |
| 정책 강제 | 불가 (각 서비스가 자유롭게 설정) | 가능 (validate 단계에서 차단) |
| 환경별 분기 | Profile/조건부 Bean | Jinja 템플릿, 환경별 YAML |
| 변경 이력 | Git 커밋 (코드 내 분산) | Git 커밋 (토픽 전용 저장소) |
| 멀티 서비스 현황 파악 | 각 서비스 코드를 뒤져야 함 | 한 저장소에서 전체 파악 |
| Dry-run | 불가 | 가능 (`--dry-run`으로 미리 확인) |

**실무 권장: 병행 사용**

소규모 팀이라면 NewTopic Bean만으로 충분하다. 하지만 서비스가 10개를 넘고 토픽이 50개를 넘으면, "어떤 서비스가 어떤 토픽을 만들었는지" 추적이 어려워진다. 이 시점에서 YAML 선언적 관리로 전환하되, 기존 NewTopic Bean은 **문서화 목적으로 유지**하는 팀도 있다.

```java
// 토픽 생성은 Jikkou가 담당. Bean은 문서화 + IDE 자동완성 용도.
// 실제 생성/변경은 kafka-topics-repo에서 관리
@Bean
public NewTopic orderCreatedTopic() {
    return TopicBuilder.name("orders.order.created")
        .partitions(12).replicas(3).build();
}
```

프로덕션에서는 `auto.create.topics.enable=false`와 함께 YAML 기반 관리를 사용하고, NewTopic Bean은 개발 환경 편의 또는 토픽 설정의 코드 내 문서화 역할로 남기는 것이 현실적이다.

---

## 3. 도구 비교

| 도구 | 방식 | 특징 | 상태 |
|------|------|------|------|
| **Jikkou** | CLI (Java) | Jinja 템플릿, 커스텀 검증/변환, Redpanda 지원, Stateless | 활발 개발 중 |
| **kafka-gitops** | CLI | Terraform-like plan/apply, ACL 자동 생성, Confluent Cloud 지원 | 유지보수 모드 |
| **Julie** | CLI (Java) | YAML 기반, 계층적 네이밍 강제, 스키마 등록 | 프로젝트 동면 |
| **Strimzi Operator** | K8s CRD | KafkaTopic CRD, GitOps 자연스러움 | 활발 |
| **Redpanda Operator** | K8s CRD | Topic CRD, Redpanda 네이티브 | 활발 |
| **Terraform** | IaC | Confluent/Kafka Provider, 인프라와 통합 | 활발 |
| **Conduktor** | 플랫폼 | 정책 엔진 + GitOps + UI, 상용 | 상용 |
| **Klaw** | 웹 UI | Four Eyes 승인, 셀프서비스 | 오픈소스 |

Redpanda 환경에서는 **Jikkou**가 가장 실용적이다. Stateless 방식이라 별도 상태 저장소가 필요 없고, Redpanda를 네이티브로 지원하며, Jinja 템플릿으로 환경별 설정 분기가 가능하기 때문이다. Kubernetes 환경이라면 **Redpanda Operator**의 Topic CRD가 자연스럽다.

---

## 4. Jikkou 활용

### 4.1 토픽 정의 (YAML)

```yaml
# kafka-topics.yaml
apiVersion: 'kafka.jikkou.io/v1beta2'
kind: 'KafkaTopic'
metadata:
  name: 'order.events.created'
  labels:
    team: 'order-team'
    environment: 'production'
spec:
  partitions: 12
  replicas: 3
  configs:
    min.insync.replicas: 2
    retention.ms: '2592000000'
    cleanup.policy: 'delete'
    compression.type: 'zstd'
---
apiVersion: 'kafka.jikkou.io/v1beta2'
kind: 'KafkaTopic'
metadata:
  name: 'order.customers.state'
  labels:
    team: 'order-team'
spec:
  partitions: 12
  replicas: 3
  configs:
    cleanup.policy: 'compact'
    min.cleanable.dirty.ratio: '0.3'
```

### 4.2 CLI 사용법

```bash
# Dry-run (변경 사항 미리 보기)
jikkou apply --files ./kafka-topics.yaml --dry-run

# 실제 적용
jikkou apply --files ./kafka-topics.yaml

# 출력 예시:
# TASK [CREATE] Create a new topic order.events.created (partitions=12, replicas=3) - CHANGED
# TASK [CREATE] Create a new topic order.customers.state (partitions=12, replicas=3) - CHANGED
# EXECUTION in 2s 661ms
# ok: 0, created: 2, altered: 0, deleted: 0, failed: 0
```

Jikkou는 Terraform의 `plan/apply` 패턴과 유사하게 동작한다. `--dry-run`으로 변경 계획을 먼저 확인하고, 검토 후 실제 적용하는 2단계 워크플로우다.

---

## 5. Redpanda Operator (Kubernetes CRD)

Kubernetes 환경에서는 Topic을 CRD(Custom Resource Definition)로 선언하고, Operator가 실제 클러스터에 반영한다:

```yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Topic
metadata:
  name: order-events-created
  namespace: kafka
spec:
  kafkaApiSpec:
    brokers:
      - redpanda-0.redpanda.kafka.svc.cluster.local:9093
  partitions: 12
  replicationFactor: 3
  additionalConfig:
    cleanup.policy: "delete"
    retention.ms: "2592000000"
    compression.type: "zstd"
    min.insync.replicas: "2"
```

ArgoCD나 FluxCD와 결합하면 Git 저장소의 YAML 변경이 자동으로 클러스터에 반영된다. 이것이 진정한 GitOps다 — Git이 단일 진실 소스(Single Source of Truth)가 되고, 클러스터 상태가 항상 Git과 일치한다.

---

## 6. GitHub Actions CI/CD 파이프라인

PR 생성 시 검증(validate + dry-run)을 수행하고, main 머지 시 실제 적용하는 전체 파이프라인이다:

```yaml
# .github/workflows/kafka-topics.yml
name: Kafka Topics Management

on:
  pull_request:
    paths: ['kafka/**']
  push:
    branches: [main]
    paths: ['kafka/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - name: Install Jikkou
        run: # Jikkou 설치 (curl + unzip + chmod)

      - name: Validate topic definitions
        run: jikkou validate --files kafka/topics/

      - name: Custom policy checks
        run: |
          python scripts/validate-naming.py kafka/topics/
          python scripts/validate-partitions.py kafka/topics/

      - name: Dry-run (Plan)
        env:
          JIKKOU_KAFKA_BOOTSTRAP_SERVERS: ${{ secrets.KAFKA_BOOTSTRAP_SERVERS }}
        run: jikkou apply --files kafka/topics/ --dry-run 2>&1 | tee plan.txt

      - name: Comment PR with plan
        # PR에 plan 결과를 코멘트로 추가 (actions/github-script@v7)

  apply:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      # validate job과 동일한 Jikkou 설치

      - name: Apply topic changes
        env:
          JIKKOU_KAFKA_BOOTSTRAP_SERVERS: ${{ secrets.KAFKA_BOOTSTRAP_SERVERS }}
        run: jikkou apply --files kafka/topics/
```

이 파이프라인의 핵심은 **PR 단계에서 dry-run 결과를 코멘트로 남기는 것**이다. 리뷰어가 "어떤 토픽이 생성/변경/삭제되는지"를 PR에서 바로 확인할 수 있어, Terraform의 plan 출력과 동일한 경험을 제공한다.

---

## 7. 정책 자동 강제 (Policy Enforcement)

### 7.1 정책 정의 (Conduktor 스타일)

```yaml
# topic-policy.yaml
apiVersion: kafka.conduktor.io/v1
kind: KafkaTopicPolicy
metadata:
  name: production-topic-policy
spec:
  rules:
    - type: ReplicationFactor
      min: 3
    - type: Partitions
      min: 3
      max: 48
    - type: RetentionMs
      min: 86400000       # 최소 1일
      max: 7776000000     # 최대 90일
    - type: TopicNamePattern
      pattern: "^[a-z]+-[a-z]+\\.[a-z]+\\.[a-z-]+$"
    - type: MinInsyncReplicas
      min: 2
```

### 7.2 자체 검증 스크립트 (Python)

조직 고유 규칙(네이밍, 파티션, 복제 팩터)을 CI에서 코드로 강제한다:

```python
#!/usr/bin/env python3
# scripts/validate-naming.py
import yaml, sys, re

NAMING_PATTERN = re.compile(r'^[a-z]+\.[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$')
MIN_REPLICAS, MIN_PARTITIONS, MAX_PARTITIONS = 3, 3, 48
errors = []

for filepath in sys.argv[1:]:
    with open(filepath) as f:
        for doc in yaml.safe_load_all(f):
            if not (doc and doc.get('kind') == 'KafkaTopic'):
                continue
            name, spec = doc['metadata']['name'], doc['spec']

            if not NAMING_PATTERN.match(name):
                errors.append(f"[{name}] 네이밍 규칙 위반 (패턴: team.domain.entity)")
            if spec.get('replicas', 1) < MIN_REPLICAS:
                errors.append(f"[{name}] 복제 팩터 {spec['replicas']} < {MIN_REPLICAS}")
            p = spec.get('partitions', 1)
            if not (MIN_PARTITIONS <= p <= MAX_PARTITIONS):
                errors.append(f"[{name}] 파티션 수 {p} 범위 밖 [{MIN_PARTITIONS}, {MAX_PARTITIONS}]")

if errors:
    print("정책 위반 발견:")
    for e in errors: print(f"  - {e}")
    sys.exit(1)
print("모든 토픽이 정책을 준수합니다.")
```

이 스크립트의 가치는 **CI에서 실행된다는 점**이다. 개발자가 정책을 모르거나 잊어도, PR을 올리는 순간 자동으로 검증된다.

---

## 8. 토픽 문서화

### 8.1 토픽 카탈로그 (Topic Registry)

규모가 커지면 **토픽 카탈로그**(토픽 레지스트리)를 운영한다. 어떤 팀이 어떤 토픽을 소유하고, 누가 소비하며, 어떤 스키마를 사용하는지를 한 곳에서 관리하는 것이다. AsyncAPI 명세가 이 역할을 할 수 있다.

```yaml
# topic-catalog.yaml (또는 AsyncAPI 명세)
topics:
  orders.order.created:
    owner: order-team
    partitions: 6
    retention: 7d
    schema: OrderCreated (Avro, v3)
    consumers:
      - payment-service
      - notification-service
      - analytics-pipeline
    classification: internal
    created: 2025-06-15
```

토픽 카탈로그의 가치는 "이 토픽에 대해 알아야 할 모든 것"을 한 곳에 모으는 것이다. `rpk topic describe`로 설정은 확인할 수 있지만, 소유 팀·소비자 목록·데이터 분류는 카탈로그 없이 알 수 없다.

### 8.3 Redpanda Console Git 기반 문서화

Redpanda Console은 Git 저장소의 Markdown 파일을 토픽 문서로 자동 표시한다 (토픽명 = 파일명):

```yaml
# Redpanda Console 설정
console:
  topicDocumentation:
    enabled: true
    git:
      enabled: true
      repository:
        url: https://github.com/myorg/kafka-topic-docs.git
      branch: main
      baseDirectory: docs/topics
      refreshInterval: 10m
```

### 8.4 토픽 문서 템플릿

권장 템플릿 (토픽명 = 파일명):

```markdown
# {토픽명}

## 소유 팀
{팀명} (@{팀 슬랙 핸들})

## 설명
{토픽의 목적과 발행되는 이벤트/엔티티 설명}

## 스키마
- Format: Avro / Protobuf / JSON
- Subject: {스키마 레지스트리 subject명}
- 호환성: BACKWARD / FORWARD / FULL

## 메시지 키
`{키 필드}` ({타입}) — {파티셔닝 의도 설명}

## 컨슈머 그룹
| 그룹 ID | 소유 팀 | 용도 |
|---------|---------|------|
| ... | ... | ... |

## 설정
- Partitions: {수}
- Retention: {기간}
- Cleanup Policy: delete / compact
- Compression: {알고리즘}

## 관련 토픽
- `{토픽명}.DLT` — Dead Letter Topic
- `{후속 토픽}` — {관계 설명}

## 변경 이력
| 날짜 | 변경 | PR |
|------|------|-----|
| ... | ... | ... |
```

이 문서화의 핵심 가치는 **토픽의 "왜"를 기록하는 것**이다. 설정값은 `rpk topic describe`로 확인할 수 있지만, "왜 파티션이 12개인지", "어떤 팀이 소비하는지"는 문서 없이 알 수 없다.

---

## 9. 토픽 수명주기 관리

### 9.1 수명주기 단계

```
┌──────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐
│ 제안/승인  │───→│ 활성 운영  │───→│ Deprecated │───→│   삭제    │
└──────────┘    └──────────┘    └────────────┘    └──────────┘
    PR 생성        모니터링         마이그레이션        유예기간 후
    정책 검증       스키마 진화      안내/지원          안전 삭제
    CI 검증         파티션 조정
```

### 9.2 Deprecated 토픽 관리

토픽을 즉시 삭제하면 알지 못하는 컨슈머가 장애를 겪을 수 있다. 따라서 "Deprecated → 유예기간 → 삭제"의 3단계를 거쳐야 한다:

```java
// 토픽 deprecated 표시 (커스텀 설정 메타데이터)
@Bean
public NewTopic deprecatedTopic() {
    return TopicBuilder.name("legacy.orders.v1")
        .partitions(6)
        .replicas(3)
        .config("x.deprecated", "true")
        .config("x.deprecated-since", "2025-06-01")
        .config("x.migration-target", "order.events.created")
        .config("x.removal-date", "2025-09-01")
        .build();
}
```

`x.` 접두사 설정은 Kafka/Redpanda가 무시하지만, 관리 도구와 문서화 시스템에서 읽을 수 있다. 이를 통해 "이 토픽은 언제까지 사용 가능하고, 대체 토픽이 무엇인지"를 선언적으로 표현한다.

### 9.3 사용하지 않는 토픽 탐지

```bash
# Redpanda/Kafka에서 컨슈머 그룹 활동 확인
rpk group list

# 특정 토픽의 컨슈머 그룹 확인
rpk topic describe legacy.orders.v1

# 최근 N일간 produce/consume 활동이 없는 토픽 찾기
# (Prometheus + Grafana 대시보드 또는 스크립트)
```

Prometheus 메트릭 `kafka_server_BrokerTopicMetrics_MessagesInPerSec`이 0인 토픽을 30일간 모니터링하면, 사용하지 않는 토픽을 자동으로 식별할 수 있다.

---

## 10. 운영 체크리스트

### 주간
- [ ] Consumer Lag 추이 확인 (> 10,000이면 조사)
- [ ] DLT 메시지 검토 및 처리/삭제
- [ ] 디스크 사용량 확인 (Tiered Storage 전환 검토)

### 월간
- [ ] 사용하지 않는 토픽 식별 (0 produce/consume)
- [ ] 파티션 불균형(skew) 확인 (> 20%면 키 재설계)
- [ ] 보존 정책 적절성 검토

### 분기
- [ ] 네이밍 컨벤션 준수 감사
- [ ] 스키마 호환성 모드 검토 (BACKWARD → FULL 전환 검토)
- [ ] ACL/접근 제어 검토
- [ ] Deprecated 토픽 마이그레이션 상태 확인
- [ ] 토픽 문서 최신화 확인

---

## 체크포인트

| # | 질문 | 확인 |
|---|------|------|
| 1 | 가이드라인과 가드레일의 차이를 설명할 수 있는가? | |
| 2 | GitOps 중앙집중형과 분산형의 장단점을 비교할 수 있는가? | |
| 3 | Jikkou dry-run → apply 워크플로우를 설명할 수 있는가? | |
| 4 | CI/CD 파이프라인에서 정책 검증이 어떻게 동작하는지 설명할 수 있는가? | |
| 5 | 토픽 수명주기의 4단계를 설명하고, Deprecated 관리 방법을 제시할 수 있는가? | |

---

## 참고 자료

- Conduktor Blog, "Kafka Governance: Guardrails Over Guidelines" (2025)
- Conduktor Blog, "Automate Kafka Configuration at Scale with GitOps" (2024)
- SPOUD, "Tools for managing Kafka topics in CI/CD pipelines" — Jikkou, Julie, Strimzi 비교 (2024)
- Confluent Blog, "GitOps For Kafka Admins: CI/CD Pipeline With CfK"
- Confluent Developer, "Build an Event Streaming Platform with GitOps" (Terraform + GitHub Actions)
- Jikkou GitHub — https://github.com/streamthoughts/jikkou
- kafka-gitops GitHub — https://github.com/devshawn/kafka-gitops
- Redpanda Docs, "Enable Topic Documentation in Console"
