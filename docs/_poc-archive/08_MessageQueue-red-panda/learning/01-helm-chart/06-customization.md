# 05. Customization

환경별 오버라이드 및 프로덕션 설정

---

## 환경별 Values 파일 구조

```
values.yaml           # 기본값 (변경하지 않음)
values-dev.yaml       # 개발 환경
values-staging.yaml   # 스테이징 환경
values-prod.yaml      # 프로덕션 환경
```

### 배포 시 적용

```bash
# 개발
helm install redpanda . -f values-dev.yaml -n redpanda

# 스테이징
helm install redpanda . -f values-staging.yaml -n redpanda-staging

# 프로덕션
helm install redpanda . -f values-prod.yaml -n redpanda-prod
```

---

## 개발 환경 (values-dev.yaml)

```yaml
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

storage:
  persistentVolume:
    size: 5Gi

tls:
  enabled: false

auth:
  sasl:
    enabled: false

console:
  enabled: true
```

---

## 스테이징 환경 (values-staging.yaml)

```yaml
statefulset:
  replicas: 3
  budget:
    maxUnavailable: 1
  podAntiAffinity:
    type: soft
    topologyKey: kubernetes.io/hostname

resources:
  cpu:
    cores: 2
  memory:
    container:
      max: 4Gi
    redpanda:
      memory: 3Gi

storage:
  persistentVolume:
    size: 20Gi
    storageClass: "standard-ssd"

tls:
  enabled: true
  certs:
    default:
      issuerRef:
        name: letsencrypt-staging
        kind: ClusterIssuer

auth:
  sasl:
    enabled: true
    mechanism: SCRAM-SHA-512

console:
  enabled: true
```

---

## 프로덕션 환경 (values-prod.yaml)

```yaml
statefulset:
  replicas: 5
  budget:
    maxUnavailable: 1
  podAntiAffinity:
    type: hard
    topologyKey: kubernetes.io/hostname

# 존 분산
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule

resources:
  cpu:
    cores: 4
  memory:
    enable_memory_locking: true
    container:
      max: 10Gi
    redpanda:
      memory: 8Gi
      reserveMemory: 1Gi

storage:
  persistentVolume:
    size: 100Gi
    storageClass: "fast-ssd"
  tiered:
    config:
      cloud_storage_enabled: true
      cloud_storage_region: ap-northeast-2
      cloud_storage_bucket: redpanda-tiered-prod
      retention_local_target_bytes: 53687091200  # 50GB

tls:
  enabled: true
  certs:
    default:
      issuerRef:
        name: letsencrypt-prod
        kind: ClusterIssuer

auth:
  sasl:
    enabled: true
    mechanism: SCRAM-SHA-512
    secretRef: redpanda-users  # 외부 Secret

config:
  cluster:
    default_topic_replications: 3
    default_topic_partitions: 6
    log_compression_type: lz4
    enable_rack_awareness: true

monitoring:
  enabled: true
  scrapeInterval: 30s

console:
  enabled: true
  ingress:
    enabled: true
    hosts:
      - host: redpanda-console.example.com
```

---

## 커스텀 설정 패턴

### 1. 환경변수로 Secret 주입

```yaml
# values-prod.yaml
auth:
  sasl:
    enabled: true
    secretRef: redpanda-users  # 미리 생성된 Secret 참조
```

```bash
# Secret 생성
kubectl create secret generic redpanda-users \
  --from-literal=admin=admin-password \
  --from-literal=producer=producer-password \
  -n redpanda
```

### 2. Ingress 설정

```yaml
listeners:
  kafka:
    external:
      enabled: true
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: nlb

console:
  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
    hosts:
      - host: console.example.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - hosts:
          - console.example.com
        secretName: console-tls
```

### 3. 리소스 Quota 대응

```yaml
# 네임스페이스에 ResourceQuota가 있는 경우
resources:
  cpu:
    cores: 2
  memory:
    container:
      max: 4Gi
      min: 2Gi  # 최소값 명시

# requests와 limits 명시적 설정
podTemplate:
  spec:
    containers:
      - name: redpanda
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
```

### 4. Node Selector / Tolerations

```yaml
statefulset:
  nodeSelector:
    dedicated: redpanda
  tolerations:
    - key: dedicated
      operator: Equal
      value: redpanda
      effect: NoSchedule
```

---

## 실습: 환경별 배포

```bash
# 1. 개발 환경 배포
helm install redpanda-dev . \
  -f values-dev.yaml \
  -n redpanda-dev \
  --create-namespace

# 2. 설정 변경 테스트 (dry-run)
helm upgrade redpanda-dev . \
  -f values-dev.yaml \
  --set statefulset.replicas=2 \
  -n redpanda-dev \
  --dry-run

# 3. 변경 적용
helm upgrade redpanda-dev . \
  -f values-dev.yaml \
  --set statefulset.replicas=2 \
  -n redpanda-dev

# 4. 정리
helm uninstall redpanda-dev -n redpanda-dev
kubectl delete ns redpanda-dev
```

---

## 참고

- [Redpanda Production Deployment](https://docs.redpanda.com/current/deploy/deployment-option/self-hosted/kubernetes/k-production-workflow/)
- [Helm Values Files](https://helm.sh/docs/chart_template_guide/values_files/)
