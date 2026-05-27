# Redpanda Helm Chart: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. values.yaml로 해결 안 되는 경우, 어떻게 Chart를 커스터마이징하는가

### 왜 이 질문이 중요한가

Helm 차트를 사용하다 보면 values.yaml에 노출되지 않은 Kubernetes 필드(예: 특정 initContainer 추가, sidecar 주입, SecurityContext 세부 설정)가 필요한 상황이 반드시 생긴다. "우리 환경에 맞게 바꾸고 싶은데 values에 없다"는 질문은 실무에서 흔하고, 면접에서는 Helm의 확장 메커니즘에 대한 이해도를 검증하는 데 자주 등장한다.

### 답변

values.yaml은 차트 개발자가 의도적으로 노출한 표면만 제어할 수 있다. 이를 넘어설 때 세 가지 접근법을 순서대로 검토한다.

**방법 1: `--set` 또는 추가 values 파일로 미공개 경로 접근**

템플릿 내부에서 `.Values.statefulset.podTemplate` 같은 경로를 통해 임의 Kubernetes spec을 통과시켜 주는 경우, 깊은 경로를 직접 지정할 수 있다.

```bash
# sidecar 컨테이너 추가 (차트가 extraContainers 필드를 지원하는 경우)
helm upgrade redpanda . -f values-prod.yaml \
  --set 'statefulset.extraContainers[0].name=fluent-bit' \
  --set 'statefulset.extraContainers[0].image=fluent/fluent-bit:3.0'
```

**방법 2: Kustomize로 Chart 출력에 패치 적용**

차트가 원하는 필드를 전혀 노출하지 않는다면, `helm template`으로 매니페스트를 생성한 뒤 Kustomize `strategic merge patch`로 필드를 덧붙인다.

```bash
helm template redpanda . -f values-prod.yaml > base/all.yaml
# kustomization.yaml 에서 patchesStrategicMerge로 initContainer 추가
```

**방법 3: Chart Fork 또는 Subchart Wrapper**

장기적으로 다수의 비표준 변경이 필요하다면 차트를 fork하거나, 사내 wrapper 차트를 만들어 원본 차트를 dependency로 포함시키고 templates/ 에서 추가 리소스를 선언한다. 업스트림 업그레이드 시 merge 비용이 발생하는 트레이드오프가 있다.

---

## Q2. Redpanda는 왜 Deployment가 아닌 StatefulSet을 사용하는가

### 왜 이 질문이 중요한가

StatefulSet과 Deployment의 차이는 K8s 기초 면접 단골 질문이지만, Kafka/Redpanda 같은 분산 스토리지 시스템에 적용하면 이유가 훨씬 구체적이고 설득력 있게 설명할 수 있다. "왜 상태 저장 서비스는 StatefulSet이어야 하는가"는 설계 판단력을 묻는 질문이다.

### 답변

Redpanda의 각 브로커는 세 가지 이유로 안정적인 정체성이 필요하다.

**1. 안정적인 네트워크 ID**: StatefulSet은 `redpanda-0`, `redpanda-1` 같이 예측 가능한 Pod 이름과 헤드리스 서비스 DNS를 보장한다. Raft 합의 프로토콜에서 각 노드는 서로의 주소를 알아야 하며, Deployment의 임의 Pod 이름으로는 이 요구를 충족할 수 없다.

**2. 안정적인 스토리지 바인딩**: StatefulSet의 `volumeClaimTemplates`는 Pod 재스케줄 시에도 동일 PVC(`datadir-redpanda-0`)를 재연결한다. Deployment + 단일 PVC로는 여러 Pod이 같은 볼륨을 공유하거나 데이터를 잃는 문제가 생긴다.

**3. 순서 보장 업그레이드/롤아웃**: `maxUnavailable: 1` 설정과 결합하면 한 번에 하나씩 브로커를 재시작하여 Raft quorum을 유지하면서 Rolling Upgrade를 수행할 수 있다.

```yaml
# values.yaml — StatefulSet 제어 핵심 필드
statefulset:
  replicas: 3
  updateStrategy:
    type: RollingUpdate
  budget:
    maxUnavailable: 1   # quorum(2/3) 유지하며 한 노드씩 교체
```

Deployment를 사용하면 위 세 조건을 직접 구현해야 하므로 StatefulSet이 Redpanda의 유일한 현실적 선택지다.

---

## Q3. Helm vs Redpanda Operator — 어떤 상황에서 무엇을 선택하는가

### 왜 이 질문이 중요한가

Redpanda는 공식 Helm 차트 외에 Kubernetes Operator도 제공한다. "왜 Helm을 쓰는가, Operator는 언제 쓰는가"는 운영 철학과 팀 역량에 대한 판단을 요구하는 질문으로, 시니어 엔지니어 면접에서 자주 나온다.

### 답변

두 접근법의 핵심 차이는 "누가 Day-2 운영을 책임지는가"이다.

| 관점 | Helm | Operator |
|------|------|----------|
| 업그레이드 | 수동 `helm upgrade` | Controller가 자동 감지 후 실행 |
| 클러스터 상태 인식 | 없음 (K8s 리소스만 관리) | Redpanda API 호출로 건강 상태 확인 |
| 토픽/ACL 관리 | values.yaml 밖의 일 | CRD로 선언 가능 |
| 학습 비용 | 낮음 | CRD 구조 + Controller 로직 이해 필요 |

**Helm을 선택하는 상황**: 팀이 K8s에 익숙하고 Redpanda 전용 운영 자동화가 불필요할 때, 또는 GitOps(ArgoCD/Flux)로 Chart를 직접 관리하는 파이프라인이 이미 있을 때. 설정 변경의 감사 추적이 values 파일 diff로 충분할 때.

**Operator를 선택하는 상황**: 브로커 수 자동 조정, 롤링 업그레이드 중 quorum 체크, 토픽·사용자를 CRD로 선언하는 GitOps가 필요할 때. 운영 인력이 부족하고 자동화 수준이 높아야 할 때.

결론적으로 Helm은 "단순하고 예측 가능한 배포"에, Operator는 "지능적인 Day-2 자동화"에 적합하다. 두 도구를 혼용하면 충돌이 발생할 수 있으므로 하나를 선택해 일관되게 유지하는 것이 원칙이다.

---

## Q4. 프로덕션 Redpanda 클러스터의 리소스 산정 기준은 무엇인가

### 왜 이 질문이 중요한가

"얼마나 줘야 하나요?"는 설계 리뷰와 인프라 비용 승인 요청 때 반드시 나오는 질문이다. 막연하게 "많이 주면 좋다"가 아니라, 처리량과 보존량을 기준으로 역산하는 방법을 설명할 수 있어야 한다.

### 답변

Redpanda 리소스 산정은 세 축(CPU, Memory, Disk)을 독립적으로 계산한다.

**CPU**: Redpanda는 Seastar 기반 thread-per-core 모델이므로 코어 수가 처리량과 직결된다. 공식 가이드는 브로커당 최소 4 vCPU(프로덕션)를 권장한다. 처리량이 브로커당 500 MB/s를 넘는다면 8 vCPU부터 시작한다.

```yaml
resources:
  cpu:
    cores: 4        # 프로덕션 최소값
    overprovisioned: false  # thread-per-core 정확도 유지
```

**Memory**: `container.max = redpanda.memory + reserveMemory`. Redpanda 메모리는 페이지 캐시와 내부 버퍼에 쓰인다. 브로커당 8 GiB redpanda 메모리(container 10 GiB)를 출발점으로 잡고, 토픽 파티션 수가 많다면 늘린다(파티션 하나당 약 1 MB 오버헤드).

```yaml
resources:
  memory:
    enable_memory_locking: true  # 스왑 방지 (프로덕션 필수)
    container:
      max: 10Gi
    redpanda:
      memory: 8Gi
      reserveMemory: 1Gi
```

**Disk**: `보존 기간 × 초당 입력량 × 복제 팩터`. 예를 들어 1 GB/s 입력, 3x 복제, 7일 보존이면 브로커당 약 `(1 GB/s × 86400 × 7) / 3 ≈ 200 TB`가 필요하다. 이 수치가 현실적이지 않다면 Tiered Storage(S3/GCS)를 도입해 로컬 디스크는 핫 데이터만 유지한다.

```yaml
storage:
  persistentVolume:
    size: 100Gi          # 로컬 핫 데이터만
    storageClass: fast-ssd
  tiered:
    config:
      cloud_storage_enabled: true
      retention_local_target_bytes: 53687091200  # 로컬 50GB 상한
```

노드 수는 Raft quorum 특성상 홀수(3, 5)를 유지하고, 가용 영역(AZ)에 `topologySpreadConstraints`로 균등 분산하는 것이 이중 장애 시나리오에서 quorum 손실을 막는 기본 원칙이다.
