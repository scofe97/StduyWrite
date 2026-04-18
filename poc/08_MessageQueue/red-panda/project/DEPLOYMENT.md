# Redpanda K8s 배포 레퍼런스

폐쇄망 K8s 클러스터에 Redpanda를 배포한 실제 경험을 정리한 문서다.
로컬 docker-compose와 달리, K8s 환경에서는 네트워크, 스토리지, 이미지 관리 등 추가 고려사항이 많다.

---

## 1. 배포 환경 개요

| 항목 | 값 |
|------|-----|
| K8s 버전 | v1.28+ |
| 네트워크 | 폐쇄망 (인터넷 불가) |
| 레지스트리 | Harbor (내부 미러링) |
| 스토리지 | NFS + hostPath |
| 아키텍처 | amd64 |

폐쇄망이므로 모든 이미지는 Harbor에 미리 미러링해야 한다.

---

## 2. 사전 준비

### 이미지 미러링

인터넷 접근 가능한 환경에서 이미지를 pull → Harbor에 push:

```bash
# Redpanda
docker pull --platform linux/amd64 docker.redpanda.com/redpandadata/redpanda:v25.3.6
docker tag docker.redpanda.com/redpandadata/redpanda:v25.3.6 harbor.example.com/redpanda/redpanda:v25.3.6
docker push harbor.example.com/redpanda/redpanda:v25.3.6

# Console
docker pull --platform linux/amd64 docker.redpanda.com/redpandadata/console:v3.5.1
docker tag docker.redpanda.com/redpandadata/console:v3.5.1 harbor.example.com/redpanda/console:v3.5.1
docker push harbor.example.com/redpanda/console:v3.5.1
```

### amd64 아키텍처 확인

Redpanda는 ARM을 공식 지원하지 않는다. 반드시 `--platform linux/amd64` 또는 digest 지정으로 amd64 이미지를 사용해야 한다.

```bash
# 이미지 아키텍처 확인
docker inspect harbor.example.com/redpanda/redpanda:v25.3.6 | jq '.[0].Architecture'
# → "amd64"
```

---

## 3. Helm Chart 배포

### Chart 정보

| 항목 | 값 |
|------|-----|
| Chart | redpanda/redpanda |
| Chart 버전 | v3.3.0 |
| App 버전 | v25.3.6 |

### 설치

```bash
# Helm repo 추가 (인터넷 환경에서 chart 다운로드 후 폐쇄망 전달)
helm repo add redpanda https://charts.redpanda.com
helm pull redpanda/redpanda --version 3.3.0

# 폐쇄망에서 설치
helm install redpanda ./redpanda-3.3.0.tgz \
  --namespace redpanda --create-namespace \
  -f custom-values.yaml
```

### custom-values.yaml 핵심 설정

```yaml
image:
  repository: harbor.example.com/redpanda/redpanda
  tag: v25.3.6

console:
  image:
    repository: harbor.example.com/redpanda/console
    tag: v3.5.1

resources:
  cpu:
    cores: 1
  memory:
    container:
      max: 2Gi
    redpanda:
      memory: 1536Mi

storage:
  persistentVolume:
    enabled: true
    size: 20Gi
    storageClass: "redpanda-hostpath"

external:
  enabled: true
  type: NodePort
  addresses:
    - 10.255.17.176
```

---

## 4. 배포 중 발생한 이슈 + 해결책

### Issue 1: NFS AIO 호환성

**증상**: Redpanda가 NFS 볼륨에서 시작 실패. `AIO` (Asynchronous I/O) 관련 에러.

**원인**: Redpanda는 Direct I/O를 사용하는데, NFS는 이를 지원하지 않는다.

**해결**: hostPath 스토리지로 전환.

```yaml
# StorageClass 생성
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: redpanda-hostpath
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

# PV 생성
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redpanda-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/redpanda
  storageClassName: redpanda-hostpath
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - worker-node-1
```

### Issue 2: ARM 이미지 Pull 실패

**증상**: `exec format error` — 컨테이너가 바로 CrashLoop.

**원인**: 멀티 아키텍처 매니페스트에서 ARM 이미지가 pull됨.

**해결**: amd64 digest를 직접 지정하거나, `--platform linux/amd64`로 미러링.

```bash
# digest 확인
docker manifest inspect docker.redpanda.com/redpandadata/redpanda:v25.3.6 \
  | jq '.manifests[] | select(.platform.architecture=="amd64") | .digest'
```

### Issue 3: Console CrashLoop

**증상**: Console Pod가 반복적으로 재시작.

**원인**: Schema Registry 환경변수 미설정.

**해결**: Console 환경변수에 Schema Registry URL 추가.

```yaml
console:
  config:
    kafka:
      brokers:
        - redpanda.redpanda.svc.cluster.local:9093
      schemaRegistry:
        enabled: true
        urls:
          - http://redpanda.redpanda.svc.cluster.local:8081
```

### Issue 4: Internal Listener 포트 충돌

**증상**: 외부에서 Kafka API 접근 불가.

**원인**: Internal/External 리스너가 같은 포트 사용.

**해결**: External 리스너에 별도 NodePort 설정.

```yaml
listeners:
  kafka:
    port: 9093          # Internal
    external:
      default:
        port: 9094      # External container port
        nodePort: 31092  # NodePort
  schemaRegistry:
    port: 8081
    external:
      default:
        port: 8084
        nodePort: 30081
  admin:
    port: 9644
    external:
      default:
        port: 9645
        nodePort: 30644
```

### Issue 5: PVC Pending

**증상**: PVC가 Pending 상태에서 멈춤.

**원인**: StorageClass가 지정되지 않아 기본 NFS provisioner를 사용.

**해결**: `storageClassName`을 명시적으로 지정.

```yaml
storage:
  persistentVolume:
    storageClass: "redpanda-hostpath"
```

---

## 5. 리소스 스펙

| 항목 | Requests | Limits |
|------|----------|--------|
| CPU | 1 core | 1 core |
| Memory | 1.5GiB | 2GiB |
| Storage | 20GiB (hostPath) | - |

Redpanda의 `--memory` 플래그는 Requests 기준(1536M)으로 설정하고,
컨테이너 Limits는 여유를 두어 2GiB로 설정한다.

---

## 6. 접속 정보

### Internal (Pod/Service 간 통신)

| 프로토콜 | 주소 |
|----------|------|
| Kafka | `redpanda.redpanda.svc.cluster.local:9093` |
| Schema Registry | `redpanda.redpanda.svc.cluster.local:8081` |
| Admin API | `redpanda.redpanda.svc.cluster.local:9644` |

### External (NodePort)

| 프로토콜 | 주소 |
|----------|------|
| Kafka | `10.255.17.176:31092` |
| Schema Registry | `10.255.17.176:30081` |
| Admin API | `10.255.17.176:30644` |
| Console | `10.255.17.176:30080` |

### rpk 연결 테스트

```bash
# Internal (Pod 내부)
rpk cluster info --brokers redpanda.redpanda.svc.cluster.local:9093

# External
rpk cluster info --brokers 10.255.17.176:31092
```

---

## 7. Spring Boot 연결 방법

`application.yml`에서 프로파일로 분기한다:

| 프로파일 | bootstrap-servers | 용도 |
|----------|------------------|------|
| `local` | `localhost:19092` | docker-compose 로컬 개발 |
| `dev` | `10.255.17.176:31092` | K8s 클러스터 연결 |

```bash
# 로컬 개발
./gradlew bootRun --args='--spring.profiles.active=local'

# K8s 클러스터 연결
./gradlew bootRun --args='--spring.profiles.active=dev'
```

`dev` 프로파일에서는 Schema Registry URL도 추가 설정된다:
- `spring.kafka.properties.schema.registry.url=http://10.255.17.176:30081`

상세 설정은 [`application.yml`](redpanda-spring-boot/src/main/resources/application.yml) 참조.
