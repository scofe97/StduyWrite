# Promtail → Alloy 전환 가이드

> 작성일: 2026-03-09 | 최종 수정: 2026-03-12
> TPS(Trombone) 개발 환경 모니터링 스택 대상
> 전제 지식: `tps-manifest-argocd-구조-분석.md`

---

## 1. TPS 인프라에서 Promtail의 현재 구현

### 배포 위치

- **네임스페이스**: `trb-mgm` (모니터링 전용)
- **배포 방식**: DaemonSet (모든 K8s 노드에 1개씩 배포)
- **클러스터**: Master 3 + Worker 5 = 총 8개 노드에서 실행

### 역할 (로그 수집 파이프라인)

```
[각 노드의 컨테이너]
    ↓ /var/log/containers/*.log (파일 tail)
[Promtail DaemonSet]
    ↓ push (HTTP/gRPC)
[Loki 3.1.0]
    ↓ 데이터소스
[Grafana 11.4.0] → 대시보드/LogQL 검색
```

Promtail이 각 노드에서 컨테이너 로그 파일을 tail하여 Loki로 전송한다. Grafana에서 LogQL을 사용하여 로그를 검색/시각화하고, 별도의 메트릭 수집은 Prometheus + Node-Exporter가 담당한다.

### 모니터링 스택 전체 구성 (trb-mgm, 21 Pods)

| 컴포넌트 | 버전 | 역할 | 배포 방식 |
|---------|------|------|----------|
| Prometheus | 3.1.0 | 메트릭 수집 | StatefulSet (kube-prometheus-stack) |
| Loki | 3.1.0 | 로그 저장/쿼리 | StatefulSet |
| Grafana | 11.4.0 (chart 8.8.2) | 시각화 | Deployment |
| AlertManager | - | 알림 | Deployment |
| Node-Exporter | - | 서버 메트릭 | DaemonSet (8 pods) |
| **Promtail** | 2.9.2 | 로그 수집 | DaemonSet (8 pods) |

### Promtail이 하는 일 (구체적)

1. **로그 파일 발견**: `/var/log/containers/` 경로에서 컨테이너 로그 파일을 자동 발견
2. **K8s 메타데이터 부착**: Pod명, 네임스페이스, 라벨 등을 로그에 자동 태깅
3. **로그 파싱/필터링**: 정규식 기반 파이프라인으로 로그 가공 가능
4. **Loki 전송**: 가공된 로그를 Loki API로 push
5. **포지션 추적**: 재시작 시 이전 위치부터 이어서 수집 (positions.yaml)

---

## 2. Promtail vs Grafana Alloy 비교

### Alloy란?

Grafana Alloy는 Grafana Labs의 차세대 통합 관측성 에이전트로, OpenTelemetry Collector를 기반으로 구축되었다. Promtail(로그)과 Grafana Agent(메트릭/트레이스)를 하나로 통합한 도구다.

### 핵심 차이점

| 항목 | Promtail | Grafana Alloy |
|------|----------|---------------|
| **범위** | 로그 수집만 | 로그 + 메트릭 + 트레이스 + 프로파일링 |
| **프로토콜** | Loki 전용 push | OTLP(OpenTelemetry) + Loki + Prometheus |
| **설정 형식** | YAML (promtail.yml) | HCL (River 문법, alloy config) |
| **로그 수집 방식** | 파일 tail (/var/log/containers/) | K8s API 직접 사용 (더 안정적) |
| **에이전트 통합** | Promtail 단독 | Node-Exporter, Promtail, Agent 역할 통합 가능 |
| **상태** | **EOL 2026-03-02** | 활발한 개발 (신기능은 Alloy에만) |
| **변환 도구** | - | `alloy convert --source-format=promtail` 제공 |

### Alloy 전환의 장점

1. **EOL 대응 (필수)**: Promtail은 2026년 3월 2일 EOL — 보안 패치, 버그 수정이 중단되었다
2. **에이전트 통합**: Promtail + Node-Exporter를 Alloy 하나로 대체할 수 있어 DaemonSet 수가 감소한다
3. **OpenTelemetry 호환**: OTLP 네이티브 지원으로 벤더 락인을 탈피하고, 향후 Jaeger/Tempo 등 트레이싱 추가가 용이하다
4. **K8s API 기반 수집**: 파일 tail 대신 K8s API를 사용하여 더 안정적으로 로그를 수집한다
5. **향후 기능**: 새로운 로깅 기능은 Alloy에만 추가된다 (Loki 3.4부터 Promtail 코드가 Alloy로 머지)
6. **커뮤니티/지원**: 공식 Helm chart, 활발한 커뮤니티, Grafana Labs 직접 지원이 제공된다

### Alloy 전환의 단점/리스크

1. **설정 형식 변경**: YAML → HCL(River) 문법 학습이 필요하여 팀 러닝 커브가 존재한다
2. **메트릭명 변경**: Promtail 메트릭과 Alloy 메트릭명이 다르므로 기존 대시보드/알람을 수정해야 한다
3. **리소스 사용량**: 통합 에이전트이므로 Promtail보다 메모리/CPU를 약간 더 사용할 수 있다
4. **변환 도구 한계**: `alloy convert`가 복잡한 설정을 100% 변환하지 못할 수 있어 수동 검증이 필요하다
5. **테스트 부담**: 프로덕션 적용 전 로그 누락 여부를 확인하는 충분한 테스트가 필요하다
6. **폐쇄망 이슈**: TPS는 폐쇄망이므로 Alloy 이미지를 Harbor에 미러링하고 Helm chart를 수정해야 한다

---

## 3. 실무 사례

### Big Bang (미국 국방부 DevSecOps)

Promtail → Alloy 전환을 완료하고 ADR로 문서화했다. "Promtail EOL + 통합 에이전트로 복잡도 감소"가 전환 이유였으며, 로그 수집 기능을 유지하면서 에이전트 수를 줄이는 데 성공했다.

### SUSE Communities

Grafana Alloy Part 1으로 Promtail 대체 가이드를 공개했다. 설정 변환 도구가 있지만 복잡한 파이프라인은 수동 조정이 필요하다는 점을 강조한다.

### Medium 실무 사례 (Sofyan Saputra, 2025-12)

K8s 환경에서 Promtail → Alloy DaemonSet 마이그레이션을 수행했다. K8s API 기반 수집이 파일 tail보다 안정적이었으나, 메트릭 이름 변경으로 인해 Grafana 대시보드 업데이트가 필요했다.

---

## 4. 클러스터 실태 vs Git 저장소 불일치 (2026-03-12 조사)

Alloy 전환 작업에 앞서 클러스터를 조사한 결과, Git 저장소의 App-of-Apps 구조와 실제 배포 상태 사이에 불일치가 확인되었다. 이 불일치를 먼저 해소하지 않으면 ArgoCD 전환 시 예상치 못한 다운그레이드가 발생할 수 있다.

### 4-1. ArgoCD Application 현황

ArgoCD에 `trb-mgm`, `trb-oss` 루트 Application이 **등록되어 있지 않다**. Git에는 `dev/trb-mgm-application.yaml`, `dev/trb-oss-application.yaml`이 존재하지만, `kubectl apply`로 적용된 적이 없거나 적용 후 삭제된 상태다.

현재 ArgoCD에 등록된 Application은 `context-hub-*` (6개), `trb-app` (1개), 그리고 환경별 배포 Application(`mjy-*`, `oss-*`, `thk-*`)뿐이다.

즉, trb-mgm(모니터링)과 trb-oss(OSS 도구) 네임스페이스의 서비스들은 **ArgoCD App-of-Apps가 아닌 직접 `helm install`로 배포**된 상태다.

### 4-2. 서비스별 버전 불일치

| 서비스 | 클러스터 실제 | Git 차트 | 불일치 |
|--------|-------------|---------|--------|
| **Loki** | `grafana/loki:3.1.0` | appVersion v2.6.1 (chart 2.16.0) | **Major 버전 불일치** |
| **Promtail** | DaemonSet 8 pods 활성 | `values-dev.yaml`에서 `enabled: false` | **Git은 비활성, 클러스터는 활성** |
| **Grafana** | `grafana:11.4.0` (chart 8.8.2) | `values-dev.yaml`에서 tag 11.2.0 | 마이너 버전 차이 |
| **Prometheus** | kube-prometheus-stack 전체 구성 | - | 미확인 |

### 4-3. Loki 상세 불일치

가장 심각한 불일치는 Loki다.

**클러스터 실제 설정** (Secret `loki`에서 추출):
```yaml
schema_config:
  configs:
  - schema: v13              # Loki 3.x 스키마
    store: tsdb               # TSDB 스토리지 (3.x 전용)
    from: "2020-10-24"
    object_store: s3
storage_config:
  aws:
    s3: http://admin:cloud1234@minio.trb-oss.svc.cluster.local:9000/loki
  tsdb_shipper:               # TSDB shipper (3.x 전용)
    active_index_directory: /data/loki/index
compactor:
  retention_enabled: true
  retention_delete_delay: 2h
```

**Git 차트 설정** (`values-dev.yaml`):
```yaml
loki:
  config:
    common:
      storage:
        s3:
          access_key_id: loki
          endpoint: http://minio.trb-oss.svc.cluster.local:9000
          secret_access_key: ZwMGEo...  # (마스킹)
    limits_config:
      retention_period: 168h
```

핵심 차이:
1. **스키마**: 클러스터는 `v13`(TSDB), Git 차트는 v2.6.1 기본값(boltdb-shipper) → 스키마 다운그레이드 시 데이터 접근 불가
2. **스토리지**: 클러스터는 `tsdb_shipper`, Git은 구 방식
3. **MinIO 인증**: 클러스터와 Git의 access_key/secret_key가 다름
4. **Promtail**: 클러스터에서는 DaemonSet 8대 실행 중이지만, Git `values-dev.yaml`에서는 `promtail.enabled: false`

### 4-4. 전환 전 해소 방안 (옵션 A 채택)

Git 차트를 클러스터 현재 상태에 맞춰 업데이트한 뒤, ArgoCD Application을 등록하여 기존 Helm release를 인계받는다.

**절차:**
1. Git 차트 버전 업데이트 — loki subchart를 3.x 호환 버전으로 교체, values-dev.yaml에 클러스터 실제 설정 반영
2. 로컬 렌더링 테스트 — `helm template`으로 클러스터 실제 리소스와 diff 비교
3. ArgoCD Application 등록 — `kubectl apply -f dev/trb-mgm-application.yaml`
4. Sync & 검증 — ArgoCD UI에서 OutOfSync diff 확인, Healthy/Synced 도달

**주의**: ArgoCD가 기존 `helm install`로 만든 리소스를 인계받으려면, ArgoCD가 렌더링하는 결과물이 기존 리소스와 일치해야 한다. 차이가 크면 리소스를 삭제 후 재생성할 수 있다.

---

## 5. 전환 전략

### 단계별 접근

| Phase | 작업 | 상태 |
|-------|------|------|
| Phase 0 | **Git 차트 ↔ 클러스터 버전 정합** (섹션 4 해소) | 완료 (2026-03-13) |
| Phase 1 | Alloy 이미지를 Harbor에 미러링 | 완료 |
| Phase 2 | Helm 차트 구성 (`helm-charts/alloy/values-dev.yaml` 작성) | 완료 |
| Phase 3 | ArgoCD Application 등록 → Alloy 배포 | 완료 (2026-03-13) |
| Phase 4 | 검증 후 Promtail 제거 | 완료 (2026-03-13) |

### 확인 필요 사항 (2026-03-09 개발계 조사 완료)

- [x] 현재 Promtail 설정 확인 → **변환 복잡도: 낮음** (기본 `kubernetes-pods` job 1개, `cri: {}` 파싱만, 커스텀 pipeline 없음)
- [x] Grafana 대시보드에서 Promtail 메트릭 사용 여부 → **미사용** (대시보드/알람에 `promtail_` 메트릭 참조 없음)
- [x] AlertManager 규칙에서 Promtail 관련 알림 존재 여부 → **없음**
- [x] 클러스터 vs Git 불일치 조사 → **Loki major 버전 불일치 확인** (섹션 4)

---

## 6. 현황 조사 결과 (2026-03-09)

### 6-1. 배포 정보

| 항목 | 값 |
|------|-----|
| DaemonSet명 | `loki-promtail` |
| Promtail 버전 | `2.9.2` |
| Helm chart | `promtail-6.15.3` (loki-stack으로 배포) |
| 이미지 | `nexus.okestro-k8s.com:55000/trombone/docker.io/grafana/promtail:2.9.2` |
| 설정 저장소 | **Secret** `loki-promtail` (ConfigMap 아님) |
| Pod 상태 | 8/8 Running, 135일 가동, 재시작 0~1회 |
| Loki 엔드포인트 | `http://loki:3100/loki/api/v1/push` |

### 6-2. Pod 분포 (전체 8개 노드)

| Pod | 노드 | 상태 |
|-----|------|------|
| loki-promtail-qv55s | master-1 | Running (재시작 1회) |
| loki-promtail-l4jfp | master-2 | Running |
| loki-promtail-wmk5t | master-3 | Running |
| loki-promtail-qpxsg | worker-1 | Running (재시작 1회) |
| loki-promtail-qprd9 | worker-2 | Running |
| loki-promtail-4mmvf | worker-3 | Running |
| loki-promtail-6cb7x | worker-4 | Running |
| loki-promtail-2hw6b | worker-5 | Running |

### 6-3. 실제 Promtail 설정 (Secret에서 추출)

```yaml
server:
  log_level: info
  log_format: logfmt
  http_listen_port: 3101

clients:
  - url: http://loki:3100/loki/api/v1/push

positions:
  filename: /run/promtail/positions.yaml

scrape_configs:
  - job_name: kubernetes-pods
    pipeline_stages:
      - cri: {}
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # app, instance, component 라벨 추출 (K8s 표준 라벨 매핑)
      # namespace, pod, container, node_name 라벨 부착
      # job = namespace/app 형태로 조합
      # __path__ = /var/log/pods/*<pod_uid>/<container_name>/*.log

limits_config: {}
tracing:
  enabled: false
```

**전환 난이도 판단: 낮음** — 설정이 Helm chart 기본값에 가깝다. 커스텀 `pipeline_stages`가 `cri: {}` 하나뿐이고, `relabel_configs`도 표준 K8s 메타데이터 매핑만 사용한다. `alloy convert` 자동 변환이 거의 100% 가능한 수준이다.

> **설정 추출 명령어**: `kubectl -n trb-mgm get secret loki-promtail -o jsonpath='{.data.promtail\.yaml}' | base64 -d`

---

## 7. 실행 절차 (Phase 3)

Phase 0(Git-클러스터 버전 정합)이 완료된 후 실행한다. Phase 0 상세 절차는 아래와 같다.

### Phase 0 상세: Git 저장소 정합

#### 0-1. Git 인증 정보 업데이트

ArgoCD가 Bitbucket 저장소를 클론할 때 사용하는 계정/토큰이 `values-*.yaml`의 `repository` 블록에 평문으로 저장되어 있다. 담당자 변경 시 아래 **8개 파일**을 모두 수정해야 한다.

```
argocd-apps/app-of-apps/charts/
├── trb-mgm/
│   ├── values-dev.yaml
│   ├── values-stg.yaml
│   ├── values-prd.yaml
│   └── values-mirae.yaml
└── trb-oss/
    ├── values-dev.yaml
    ├── values-stg.yaml
    ├── values-prd.yaml
    └── values-mirae.yaml
```

각 파일의 `repository:` 블록을 다음으로 변경:

```yaml
repository:
  url: https://bitbucket.org/okestrolab/tps_manifest.git
  branch: main
  username: lee-chanwoong
  password: ATBBVBXPwFPxj2MBVzNXrhZ7NqKQCA54292C  # Bitbucket App Password
```

이 값은 `templates/repository.yaml`이 읽어서 ArgoCD용 Secret(`trb-manifest-repo`)을 생성한다. 인증이 틀리면 ArgoCD가 Git 클론에 실패하여 모든 Application이 Sync 불가 상태가 된다.

#### 0-2. Loki/Promtail 버전 정합

섹션 4의 불일치를 해소한다.

1. `helm-charts/loki-stack/` 의 Loki subchart를 3.x 호환 버전으로 교체
2. `helm-charts/loki-stack/values-dev.yaml`에 클러스터 실제 설정 반영 (schema v13, tsdb, MinIO 인증)
3. `promtail.enabled: true`로 변경 (클러스터 현재 상태와 일치시키기)

#### 0-3. 로컬 Helm 렌더링 검증

Git push 전에 **로컬에서** Helm 렌더링이 정상인지 확인한다. `helm template`은 렌더링만 수행하고 클러스터에 적용하지 않으므로 안전하다. 개발계 master 노드에는 helm CLI가 없으므로 반드시 로컬에서 실행한다.

```bash
cd ~/okestro/tps_manifest

# 테스트 1: App-of-Apps 템플릿 확인
# → trb-mgm 루트 차트가 올바른 ArgoCD Application yaml을 생성하는지
helm template trb-mgm argocd-apps/app-of-apps/charts/trb-mgm \
  -f argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml
```

출력에서 확인할 것:
- `alloy`라는 이름의 Application이 생성되는가
- `source.path`가 `helm-charts/alloy`를 가리키는가
- `valueFiles`에 `values-dev.yaml`이 포함되어 있는가

```bash
# 테스트 2: 실제 차트 렌더링 확인
# → Helm 차트가 유효한 K8s 리소스(DaemonSet, ConfigMap 등)를 생성하는지
helm template alloy helm-charts/alloy \
  -f helm-charts/alloy/values-dev.yaml \
  --namespace trb-mgm
```

출력에서 확인할 것:
- DaemonSet, ConfigMap 등이 정상적으로 생성되는가
- 문법 오류(indentation, 누락된 변수)가 없는가

| 흔한 오류 | 원인 | 해결 |
|-----------|------|------|
| `no template "xxx" associated with template "xxx"` | templates/ 디렉토리에 파일 없음 | 차트 구조 확인 (`Chart.yaml` + `templates/` 필수) |
| `values don't meet the specifications` | values-dev.yaml YAML 형식 오류 | 들여쓰기 확인 |
| `nil pointer evaluating interface {}` | values에 필요한 키 누락 | `values.yaml`과 `values-dev.yaml` 키 대조 |

#### 0-4. ArgoCD 루트 Application 등록

현재 `trb-mgm`, `trb-oss` 루트 Application이 ArgoCD에 **등록되어 있지 않다** (섹션 4-1). 모니터링 서비스들은 직접 `helm install`로 배포된 상태이므로, App-of-Apps를 활성화하려면 루트 Application을 수동 등록해야 한다.

**순서가 중요하다** — ArgoCD가 private Bitbucket 저장소를 클론하려면 인증 Secret이 먼저 존재해야 한다.

```bash
ssh master-1

# Step A: ArgoCD에 Git 저장소 인증 Secret 등록 (최초 1회)
# templates/repository.yaml이 이 역할을 하지만, 루트 App 등록 전에는 렌더링되지 않으므로
# 수동으로 먼저 생성해야 한다 (닭과 달걀 문제)
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: trb-manifest-repo
  namespace: trb-oss
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: https://bitbucket.org/okestrolab/tps_manifest.git
  username: lee-chanwoong
  password: ATBBVBXPwFPxj2MBVzNXrhZ7NqKQCA54292C
EOF

# Step B: 루트 Application 등록
cat <<'EOF' | kubectl apply -f -
kind: Application
apiVersion: argoproj.io/v1alpha1
metadata:
  name: trb-mgm
  namespace: trb-oss
spec:
  destination:
    namespace: trb-mgm
    server: https://kubernetes.default.svc
  project: default
  source:
    helm:
      valueFiles:
      - values-dev.yaml
    path: argocd-apps/app-of-apps/charts/trb-mgm
    repoURL: https://bitbucket.org/okestrolab/tps_manifest.git
EOF
```

> ⚠️ Step A를 건너뛰면 ArgoCD가 Bitbucket을 클론하지 못해 Application이 `ComparisonError` 상태로 멈춘다.

등록 후 확인:
```bash
# 루트 Application 상태
kubectl -n trb-oss get application trb-mgm

# 자식 Application 생성 확인 (loki, prometheus, alloy 등)
kubectl -n trb-oss get applications
```

#### 0-4-1. Sync 동작 이해 (루트 vs 자식)

루트 Application(`trb-mgm-application.yaml`)에는 `syncPolicy`가 **없다**. 즉 루트는 수동 Sync다. 반면 자식 Application들(loki, prometheus, alloy)은 `values-dev.yaml`의 `syncPolicy.automated`를 상속받으므로 자동 Sync다.

```
루트 Application (trb-mgm) — 수동 Sync
    ↓ UI에서 Sync 버튼 → 자식 Application 생성/업데이트
자식 Application (loki, alloy 등) — 자동 Sync
    ↓ helm-charts/* 변경 시 자동 배포
```

**처음 등록 후 반드시 루트를 1회 수동 Sync해야 자식 Application들이 생성된다.** 그 이후 자식들은 자동 Sync이므로 `helm-charts/*` 내부 변경(values, 차트 버전 등)은 Git push만으로 반영된다.

단, 자식 Application 자체를 추가/삭제하는 변경(예: `templates/alloy.yaml` 신규 생성, `values-dev.yaml`에 `alloy.enabled` 블록 추가)은 **루트 차트의 렌더링 결과가 바뀌는 것**이므로 루트를 다시 Sync해야 한다.

#### 0-4-2. FAQ: Loki 차트를 새 버전으로 교체하고 push하면?

> **Q: Loki subchart를 3.x로 갈아끼우고 push하면, 루트를 다시 등록해야 하나?**

아니다. 루트를 **재등록할 필요는 없다**. 변경 위치에 따라 동작이 다르다:

| 변경 위치 | 예시 | 루트 Sync 필요? |
|----------|------|---------------|
| `helm-charts/loki-stack/` 내부 | 차트 교체, values 수정, 버전 업 | **불필요** — 자식 `loki` Application이 자동 감지 |
| `charts/trb-mgm/templates/` | 새 Application 템플릿 추가/삭제 | **필요** — 루트 렌더링 결과가 변경됨 |
| `charts/trb-mgm/values-dev.yaml` | `alloy.enabled` 추가, `helmPath` 변경 | **필요** — 루트 렌더링 결과가 변경됨 |

Loki subchart 교체는 `helm-charts/loki-stack/` 내부 변경이므로, 이미 존재하는 자식 `loki` Application이 자동으로 변경을 감지하고 Sync한다. 루트 재등록이나 수동 Sync는 불필요하다.

#### 0-4-3. FAQ: 기존 `helm install` 리소스와 ArgoCD 자동 Sync 충돌

> **Q: 기존 Loki는 `helm install`로 직접 밀어 넣은 건데, ArgoCD가 자동 Sync하면 기존 리소스를 삭제하고 Git 버전으로 다시 만드나?**

**상황에 따라 다르다.**

ArgoCD는 Sync 시 Git 차트를 렌더링한 결과물을 "원하는 상태"로 보고, 클러스터의 현재 상태와 비교한다.

**Case 1: Git 렌더링 결과 ≈ 클러스터 현재 상태** (차이가 적음)
- ArgoCD가 기존 리소스를 **인계(adopt)** 한다
- 삭제/재생성 없이 라벨(`app.kubernetes.io/managed-by: Helm` → ArgoCD 관리)만 업데이트
- 서비스 중단 없음

**Case 2: Git 렌더링 결과 ≠ 클러스터 현재 상태** (차이가 큼)
- ArgoCD가 클러스터를 Git 상태로 맞추려고 **리소스를 수정/삭제 후 재생성**
- `prune: true`이므로 Git에 없는 리소스는 삭제됨
- `selfHeal: true`이므로 클러스터를 수동으로 되돌려도 ArgoCD가 다시 Git 상태로 강제함
- **서비스 중단 가능**

현재 Loki는 **Case 2에 해당한다** — 클러스터는 3.1.0(schema v13, TSDB), Git 차트는 2.6.1(boltdb-shipper)이므로 렌더링 결과가 완전히 다르다.

**따라서 Sync 전에 반드시:**
1. Git 차트를 클러스터 버전에 맞춰 업데이트 (Phase 0-2)
2. `helm template`으로 렌더링 결과를 클러스터 실제 리소스와 diff 비교 (Phase 0-3)
3. diff가 최소화된 상태에서 Sync

이 순서를 지키지 않고 현재 Git 상태 그대로 Sync하면, ArgoCD가 Loki 3.1.0을 2.6.1로 다운그레이드하려 시도하여 **데이터 접근 불가** 사고가 발생할 수 있다.

> ⚠️ **핵심 원칙**: ArgoCD 첫 Sync 전에 Git 렌더링 결과와 클러스터 실제 상태의 diff를 0에 가깝게 만들어야 안전하다. Sync 버튼을 누르기 전에 ArgoCD UI에서 OutOfSync diff를 반드시 확인할 것.

#### 0-5. 기존 Helm release 인계 주의

ArgoCD가 기존 `helm install`로 만든 리소스를 인계받으려면, ArgoCD Application이 렌더링하는 결과물이 기존 클러스터 리소스와 **일치**해야 한다. 차이가 크면 ArgoCD가 리소스를 삭제 후 재생성하여 서비스 중단이 발생할 수 있다.

```bash
# 인계 전: 로컬 렌더링 결과와 클러스터 실제 리소스를 비교
helm template loki helm-charts/loki-stack \
  -f helm-charts/loki-stack/values-dev.yaml \
  --namespace trb-mgm > /tmp/rendered.yaml

# 클러스터 실제 리소스 추출 (SSH)
kubectl -n trb-mgm get statefulset loki -o yaml > /tmp/actual.yaml

# diff 비교 — 차이가 적을수록 안전
diff /tmp/rendered.yaml /tmp/actual.yaml
```

ArgoCD 등록 후 UI에서 OutOfSync diff를 확인하고, 예상 밖 차이가 있으면 `values-dev.yaml`을 조정하여 diff를 줄인 뒤 sync한다.

---

### Step 1. 현재 상태 확인

```bash
ssh master-1

# Promtail 상태 확인 — 8개 노드 모두 Running이어야 함
kubectl -n trb-mgm get pods -l app.kubernetes.io/name=promtail

# Alloy가 아직 없는지 확인 — "No resources found" 예상
kubectl -n trb-mgm get pods -l app.kubernetes.io/name=alloy

# ArgoCD에 등록된 Application 목록
kubectl -n trb-oss get applications
```

### Step 2. ArgoCD Application 템플릿 생성

**경로**: `argocd-apps/app-of-apps/charts/trb-mgm/templates/alloy.yaml`

기존 `loki-stack.yaml`을 복제하여 3곳만 수정한다: `metadata.name`, `if` 조건의 키, `helmPath` 참조.

```yaml
{{- if .Values.alloy.enabled }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: alloy
  namespace: trb-oss
spec:
  destination:
    namespace: {{ .Values.application.destination.namespace }}
    server: {{ .Values.application.destination.server }}
  project: {{ .Values.application.project }}
  source:
    helm:
      valueFiles:
        {{- range .Values.application.helm.valuesFiles }}
        - {{ . | quote }}
        {{- end }}
    path: {{ .Values.alloy.helmPath }}
    repoURL: {{ .Values.repository.url }}
    targetRevision: {{ .Values.repository.branch }}
  syncPolicy:
    {{- .Values.application.syncPolicy | toYaml | nindent 4 }}
{{- end }}
```

### Step 3. values-dev.yaml에 alloy 항목 추가

**경로**: `argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml`

```yaml
# 기존 (수정하지 않음)
loki:
  enabled: true
  helmPath: helm-charts/loki-stack

prometheus:
  enabled: true
  helmPath: helm-charts/kube-prometheus-stack

# 신규 추가
alloy:
  enabled: true
  helmPath: helm-charts/alloy
```

### Step 4. Git 커밋 및 Push

```bash
cd ~/okestro/tps_manifest

git add argocd-apps/app-of-apps/charts/trb-mgm/templates/alloy.yaml
git add argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml

git commit -m "feat: Alloy ArgoCD Application 등록 (Promtail EOL 대응)"
git push origin main
```

**주의**: 이 단계에서는 Alloy만 추가한다. Promtail 비활성화(`promtail.enabled: false`)는 Alloy 정상 동작 확인 후에 진행해야 로그 수집 공백이 없다.

### Step 5. ArgoCD 배포 확인

```bash
# alloy Application이 생성되었는지 확인
kubectl -n trb-oss get applications alloy

# 예상: Synced / Healthy
```

ArgoCD UI(`https://argocd.dev.trb.com`)에서 `trb-mgm` → 자식 Application 목록에 `alloy` 확인.

### Step 6. DaemonSet & Pod 검증

```bash
# DaemonSet 확인 — DESIRED = CURRENT = READY = 8
kubectl -n trb-mgm get daemonset -l app.kubernetes.io/name=alloy

# Pod 상태 확인 — 모든 노드에 1개씩 Running
kubectl -n trb-mgm get pods -l app.kubernetes.io/name=alloy -o wide

# Pod 로그 확인 — 에러 없이 수집 시작 메시지가 보여야 함
kubectl -n trb-mgm logs -l app.kubernetes.io/name=alloy --tail=20
```

| 증상 | 원인 | 해결 |
|------|------|------|
| `ImagePullBackOff` | Harbor에 이미지가 없거나 태그 불일치 | `values-dev.yaml`의 `image.registry`, `image.tag` 확인 |
| `CrashLoopBackOff` | River 설정 문법 오류 | `kubectl logs`로 에러 메시지 확인, ConfigMap 내용 점검 |
| DESIRED < 8 | tolerations 누락으로 master 노드 제외 | `values-dev.yaml`에 master 노드 toleration 추가 |
| Loki 전송 실패 | `loki.write` 엔드포인트 주소 오류 | `http://loki:3100` 접근 가능한지 `kubectl exec`로 확인 |

### Step 7. Grafana LogQL 검증

```
브라우저: https://grafana.dev.trb.com
Explore → Loki 데이터소스 선택
```

```logql
# 1. 최근 5분간 trb-app 네임스페이스 로그가 수집되는지
{namespace="trb-app"} | line_format "{{.log}}"

# 2. 특정 서비스 로그 확인
{namespace="trb-app", app="tps-api"}

# 3. 로그 볼륨 확인 — 그래프가 0이 아니어야 함
count_over_time({namespace=~".+"}[1m])
```

Promtail과 Alloy가 동시에 동작하면 동일 로그가 2번 수집된다. 검증 기간에는 오히려 양쪽을 비교할 수 있어 유용하다. 라벨(`namespace`, `pod`, `container`, `app`)이 양쪽에서 동일하게 붙는지 확인한다.

### Step 8. Promtail 제거 (Phase 4)

Alloy 정상 동작 확인 후 진행한다.

```yaml
# helm-charts/loki-stack/values-dev.yaml
promtail:
  enabled: false    # true → false
```

```bash
git add helm-charts/loki-stack/values-dev.yaml
git commit -m "chore: Promtail 비활성화 (Alloy 전환 완료)"
git push origin main
```

ArgoCD sync 후 Promtail DaemonSet이 자동 삭제된다.

잔여 리소스 확인:
```bash
kubectl -n trb-mgm get all,secret,sa -l app.kubernetes.io/name=promtail
kubectl get clusterrole,clusterrolebinding -l app.kubernetes.io/name=promtail

# 잔여 있으면 정리
kubectl -n trb-mgm delete secret loki-promtail 2>/dev/null
kubectl delete clusterrole loki-promtail 2>/dev/null
kubectl delete clusterrolebinding loki-promtail 2>/dev/null
kubectl -n trb-mgm delete sa loki-promtail 2>/dev/null
```

---

## 8. 롤백 절차

### Alloy에 문제가 있을 때

```bash
cd ~/okestro/tps_manifest
git revert HEAD
git push origin main
# ArgoCD sync → alloy Application 삭제 → Alloy DaemonSet 삭제
```

### Promtail을 이미 제거한 후 Alloy가 실패할 때

```yaml
# helm-charts/loki-stack/values-dev.yaml에서 promtail.enabled: true로 변경
```

```bash
git add helm-charts/loki-stack/values-dev.yaml
git commit -m "rollback: Promtail 재활성화 (Alloy 장애 대응)"
git push origin main
```

**롤백 소요 시간**: Git push → ArgoCD 감지(최대 3분) → sync 실행(1~2분) = 약 5분 이내. 급한 경우 ArgoCD UI에서 수동 sync를 트리거하면 더 빠르다.

---

## 9. Alloy 설정 상세

### 9-1. River 문법 핵심 개념

Alloy는 YAML 대신 **River**라는 HCL 기반 설정 언어를 사용한다. Terraform의 HCL과 유사하여 인프라 엔지니어에게 익숙한 문법이다.

```river
// Promtail YAML의 scrape_configs에 해당
loki.source.kubernetes "pods" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [loki.process.pipeline.receiver]
}

// Promtail YAML의 pipeline_stages에 해당
loki.process "pipeline" {
  stage.docker {}
  stage.labels {
    values = { app = "" }
  }
  forward_to = [loki.write.default.receiver]
}

// Promtail YAML의 clients에 해당
loki.write "default" {
  endpoint {
    url = "http://loki.trb-mgm.svc:3100/loki/api/v1/push"
  }
}
```

### 9-2. YAML → River 매핑

| Promtail YAML | Alloy River | 설명 |
|---------------|-------------|------|
| `scrape_configs[].job_name` | `loki.source.kubernetes "이름"` | 로그 소스 정의 |
| `pipeline_stages` | `loki.process` 안의 `stage.*` | 로그 가공 파이프라인 |
| `clients[].url` | `loki.write` 안의 `endpoint.url` | Loki 전송 대상 |
| `positions.filename` | 자동 관리 | Alloy가 내부적으로 처리 |
| 계층 구조 (들여쓰기) | 블록 + `forward_to` 체이닝 | 데이터 흐름이 명시적 |

River의 핵심 개념은 **forward_to 체이닝**이다. 각 컴포넌트가 다음 컴포넌트로 데이터를 명시적으로 전달하므로, 데이터 파이프라인의 흐름이 YAML보다 직관적으로 보인다.

```
[loki.source.kubernetes] --forward_to--> [loki.process] --forward_to--> [loki.write]
     (로그 발견)                            (로그 가공)                    (Loki 전송)
```

### 9-3. 설정 변환 도구

```bash
# 외부 네트워크에서 Alloy 바이너리 다운로드
curl -LO https://github.com/grafana/alloy/releases/download/v1.6.1/alloy-linux-amd64.zip

# 설정 변환 실행
alloy convert --source-format=promtail --output=alloy-config.alloy promtail.yaml

# 변환 결과 검증 (dry-run)
alloy run --dry-run alloy-config.alloy
```

### 9-4. 대시보드/알람 메트릭 (조사 완료: 수정 불필요)

개발계 조사 결과, Grafana 대시보드 ConfigMap과 AlertManager 규칙에서 `promtail_` 메트릭을 참조하는 곳이 **없었다**. 향후 모니터링 대시보드 추가 시 참고:

| Promtail 메트릭 | Alloy 메트릭 |
|----------------|-------------|
| `promtail_targets_active_total` | `loki_source_kubernetes_targets` |
| `promtail_sent_entries_total` | `loki_write_sent_entries_total` |
| `promtail_dropped_entries_total` | `loki_write_dropped_entries_total` |

### 9-5. helm-charts/alloy/values-dev.yaml (Phase 2에서 작성 완료)

| 설정 | 값 | 설명 |
|------|-----|------|
| `image.registry` | `harbor.dev.console.trombone.okestro.cloud` | 폐쇄망이므로 Harbor 미러 사용 |
| `image.tag` | `v1.14.0` | Alloy 버전 |
| `controller.type` | `daemonset` | 모든 노드에 1개씩 배포 (Promtail과 동일) |
| `alloy.configMap.content` | River 문법 설정 | discovery → source → process → write 파이프라인 |
| `loki.write.endpoint.url` | `http://loki:3100/loki/api/v1/push` | 기존 Promtail과 동일한 Loki 엔드포인트 |
| `resources.requests` | cpu: 50m, memory: 128Mi | Promtail 대비 유사한 리소스 |
| `crds.create` | `false` | 폐쇄망에서 CRD 자동 생성 비활성화 |

---

## 10. 핵심 개념 보충

### DaemonSet

K8s에서 **모든 노드(또는 특정 노드)에 정확히 1개의 Pod를 배포**하는 워크로드 타입이다. 로그 수집 에이전트는 각 노드의 `/var/log/containers/`를 읽어야 하는데, 이 경로는 해당 노드에서만 접근 가능하기 때문에 DaemonSet이 필수다.

### Loki Push 모델

Prometheus는 Pull 모델(대상을 주기적으로 긁어감)을 사용하지만, Loki는 Push 모델(에이전트가 Loki로 밀어넣음)을 사용한다. Promtail과 Alloy 모두 동일한 API(`/loki/api/v1/push`)로 push하므로, 병렬 배포가 가능하다.

### OpenTelemetry (OTLP)

OTLP는 로그/메트릭/트레이스를 수집하는 벤더 중립 표준 프로토콜이다. Alloy는 OTLP를 지원하므로 향후 분산 트레이싱(Tempo/Jaeger) 도입 시 Alloy 하나로 로그+트레이스를 동시에 수집할 수 있다.

### (선택) Node-Exporter 통합

Alloy는 Prometheus 메트릭도 수집할 수 있으므로, Node-Exporter DaemonSet을 제거하고 Alloy에 통합할 수 있다. 로그 수집 전환이 안정화된 후에 별도로 진행하는 것을 권장한다.

---

## 체크리스트

```
Phase 0: Git-클러스터 버전 정합
□ Git 인증 정보 업데이트 (8개 values 파일 — 아래 상세)
□ loki subchart를 3.x 호환 버전으로 업데이트
□ values-dev.yaml에 클러스터 실제 설정 반영
□ helm template 렌더링 테스트 통과
□ trb-mgm-application.yaml ArgoCD 등록
□ ArgoCD에서 Healthy/Synced 확인

Phase 3: Alloy 배포
□ Promtail 8/8 Running 확인
□ alloy.yaml 템플릿 생성
□ values-dev.yaml에 alloy 블록 추가
□ Git push
□ ArgoCD에서 alloy Application Synced/Healthy
□ Alloy Pod 8/8 Running
□ Grafana LogQL 검증 통과

Phase 4: Promtail 제거
□ promtail.enabled: false push
□ 잔여 ClusterRole/Secret 정리
```

---

## 참고 자료

- [Grafana 공식 마이그레이션 가이드](https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/)
- [Big Bang ADR: Alloy replacing Promtail](https://docs-bigbang.dso.mil/latest/docs/adrs/0004-alloy-replacing-promtail/)
- [K8s 마이그레이션 사례 (Medium)](https://medium.com/@vincenthartmann/migrating-from-promtail-to-grafana-alloy-in-kubernetes-53ce4c5b7556)
- [SUSE: Grafana Alloy Part 1](https://www.suse.com/c/grafana-alloy-part-1-replacing-promtail/)
- [Promtail Is Dead (Elest.io)](https://blog.elest.io/promtail-is-dead-how-to-migrate-your-log-pipeline-to-grafana-alloy-before-it-breaks/)
- [Loki 3.4: Promtail merging into Alloy](https://grafana.com/blog/2025/02/13/grafana-loki-3.4-standardized-storage-config-sizing-guidance-and-promtail-merging-into-alloy/)
- [실무 마이그레이션 사례 (Sofyan)](https://medium.com/@meongbego/how-we-migrated-from-promtail-to-grafana-alloy-5ebc6f5ec256)
- ArgoCD 구조: `tps-manifest-argocd-구조-분석.md`
- Helm 차트 추가: `tps-manifest-helm-차트-추가-가이드.md`
