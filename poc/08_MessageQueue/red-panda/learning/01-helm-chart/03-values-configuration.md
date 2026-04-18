# 02. Values Configuration

values.yaml 상세 분석 및 주요 설정 옵션

---

## 설정 구조 개요

```yaml
# values.yaml 주요 섹션
statefulset:     # Pod/Replica 설정
resources:       # CPU/Memory 리소스
storage:         # 스토리지 설정
listeners:       # 네트워크 리스너
tls:             # TLS 설정
auth:            # 인증 설정
config:          # Redpanda 내부 설정
console:         # Console UI 설정
monitoring:      # 모니터링 설정
```

---

## 1. 클러스터 설정 (statefulset)

```yaml
statefulset:
  replicas: 3                    # 브로커 수
  updateStrategy:
    type: RollingUpdate
  budget:
    maxUnavailable: 1            # 최대 동시 비가용 Pod

  # Pod Anti-Affinity
  podAntiAffinity:
    type: hard                   # soft | hard
    topologyKey: kubernetes.io/hostname
```

### replicas 권장값

| 환경 | replicas | 이유 |
|------|----------|------|
| 개발 | 1 | 리소스 절약 |
| 스테이징 | 3 | 프로덕션 유사 환경 |
| 프로덕션 | 3+ (홀수) | Raft 합의 위해 홀수 권장 |

---

## 2. 리소스 설정 (resources)

```yaml
resources:
  cpu:
    cores: 1                     # vCPU 코어 수
    overprovisioned: false       # 오버프로비저닝 허용
  memory:
    enable_memory_locking: false
    container:
      max: 2.5Gi                 # 컨테이너 전체 메모리
      min: null
    redpanda:
      memory: 2Gi                # Redpanda 프로세스 전용
      reserveMemory: 200Mi       # OS/기타용 예약
```

### 메모리 계산

```
container.max = redpanda.memory + redpanda.reserveMemory + 여유분

예: container.max 2.5Gi = redpanda 2Gi + reserve 200Mi + 300Mi 여유
```

### 환경별 권장값

| 환경 | CPU | Memory (container) | Memory (redpanda) |
|------|-----|-------------------|-------------------|
| 개발 | 0.5 | 1Gi | 512Mi |
| 스테이징 | 2 | 4Gi | 3Gi |
| 프로덕션 | 4+ | 10Gi+ | 8Gi+ |

---

## 3. 스토리지 설정 (storage)

```yaml
storage:
  persistentVolume:
    enabled: true
    size: 20Gi
    storageClass: ""             # 기본 StorageClass 사용
    labels: {}
    annotations: {}

  # Tiered Storage
  tiered:
    mountType: none              # none | hostPath | emptyDir | persistentVolume
    config:
      cloud_storage_enabled: false
      cloud_storage_region: ""
      cloud_storage_bucket: ""
```

### StorageClass 선택

```yaml
# SSD 사용 권장
storage:
  persistentVolume:
    storageClass: "fast-ssd"     # 또는 gp3, pd-ssd 등
```

---

## 4. 리스너 설정 (listeners)

```yaml
listeners:
  kafka:
    port: 9092
    tls:
      enabled: false
      cert: default
  admin:
    port: 9644
    tls:
      enabled: false
  schemaRegistry:
    port: 8081
    enabled: true
    tls:
      enabled: false
  http:
    port: 8082                   # Pandaproxy
    enabled: true
```

### 포트 요약

| 리스너 | 포트 | 용도 |
|--------|------|------|
| kafka | 9092 | Kafka 클라이언트 연결 |
| admin | 9644 | Admin API, 메트릭 |
| schemaRegistry | 8081 | Schema Registry API |
| http | 8082 | HTTP Proxy (REST) |

---

## 5. TLS 설정 (tls)

```yaml
tls:
  enabled: false
  certs:
    default:
      caEnabled: true
      secretRef:
        name: ""                 # 기존 Secret 사용 시
      issuerRef:                 # cert-manager 사용 시
        name: ""
        kind: ClusterIssuer
```

### cert-manager 연동

```yaml
tls:
  enabled: true
  certs:
    default:
      issuerRef:
        name: letsencrypt-prod
        kind: ClusterIssuer
```

---

## 6. 인증 설정 (auth)

```yaml
auth:
  sasl:
    enabled: false
    mechanism: SCRAM-SHA-512     # SCRAM-SHA-256 | SCRAM-SHA-512
    users:
      - name: admin
        password: ""             # Secret으로 관리 권장
        mechanism: SCRAM-SHA-512
```

### Secret으로 비밀번호 관리

```yaml
auth:
  sasl:
    enabled: true
    secretRef: redpanda-users    # 기존 Secret 참조
```

---

## 7. Redpanda 내부 설정 (config)

```yaml
config:
  cluster: {}                    # 클러스터 레벨 설정
  node: {}                       # 노드 레벨 설정
  tunable: {}                    # 튜닝 가능한 설정
```

### 주요 cluster 설정

```yaml
config:
  cluster:
    default_topic_replications: 3
    default_topic_partitions: 3
    enable_rack_awareness: false
    log_compression_type: producer   # none | gzip | snappy | lz4 | zstd
```

---

## 8. values-dev.yaml 예시

```yaml
# 개발환경용 최소 설정
statefulset:
  replicas: 1
  budget:
    maxUnavailable: 1

resources:
  cpu:
    cores: 0.5
  memory:
    container:
      max: 1Gi
    redpanda:
      memory: 512Mi
      reserveMemory: 100Mi

storage:
  persistentVolume:
    enabled: true
    size: 5Gi

console:
  enabled: true
```

---

## 실습

```bash
cd /Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda

# 전체 기본값 확인
helm show values .

# 특정 섹션 확인
helm show values . | yq '.resources'
helm show values . | yq '.listeners'

# 설정 병합 확인 (dry-run)
helm template test . -f values-dev.yaml | head -200

# 값 검증
helm lint . -f values-dev.yaml
```

---

## 참고

- [Redpanda Helm Configuration](https://docs.redpanda.com/current/reference/helm-configuration/)
