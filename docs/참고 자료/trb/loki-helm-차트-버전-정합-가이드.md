# Loki Helm 차트 버전 정합 가이드

> 작성일: 2026-03-13
> TPS(Trombone) 개발 환경 Loki 차트 메타데이터 정합 대상
> 전제 지식: `promtail-to-alloy-전환-가이드.md` 섹션 4

---

## 1. 배경 및 문제 정의

개발계 클러스터의 Loki는 이미 3.1.0으로 운영 중이다. 누군가 subchart의 `values.yaml`에서 이미지 태그와 config(schema v13, tsdb_shipper, MinIO)를 3.1.0에 맞춰 수정했지만, `Chart.yaml` 메타데이터는 v2.6.1로 남겨둔 상태다. 실제 동작에는 문제가 없으나, ArgoCD 도입 시 appVersion 불일치가 혼란을 유발하고 `helm list`에서 잘못된 버전이 표시된다.

### 3계층 버전 현황

| 계층 | 항목 | 현재 값 | 기대 값 | 상태 |
|------|------|---------|---------|------|
| **Chart.yaml** (loki-stack) | `appVersion` | `v2.6.1` | `"3.1.0"` | **불일치** |
| **Chart.yaml** (loki-stack) | `version` | `2.10.0` | `2.10.0` | 유지 |
| **Chart.yaml** (loki subchart) | `appVersion` | `v2.6.1` | `"3.1.0"` | **불일치** |
| **Chart.yaml** (loki subchart) | `version` | `2.16.0` | `2.16.0` | 유지 |
| **values.yaml** (loki subchart) | `image.tag` | `3.1.0` | `3.1.0` | 정합 완료 |
| **values.yaml** (loki subchart) | `schema_config` | v13 / tsdb | v13 / tsdb | 정합 완료 |
| **values.yaml** (loki subchart) | `storage_config` | tsdb_shipper + MinIO | tsdb_shipper + MinIO | 정합 완료 |
| **클러스터** | StatefulSet 이미지 | `grafana/loki:3.1.0` | `grafana/loki:3.1.0` | 정합 완료 |

핵심: **Chart.yaml 2개 파일의 `appVersion`만 수정하면 된다.** values.yaml과 templates는 이미 3.1.0에 맞춰져 있으므로 건드리지 않는다.

---

## 2. 변경 필요 항목

수정 대상은 2개 파일, 각 1줄이다.

### 2-1. `helm-charts/loki-stack/Chart.yaml`

```yaml
# Before
appVersion: v2.6.1

# After
appVersion: "3.1.0"
```

### 2-2. `helm-charts/loki-stack/charts/loki/Chart.yaml`

```yaml
# Before
appVersion: v2.6.1

# After
appVersion: "3.1.0"
```

`version` 필드(차트 자체 버전 2.10.0, 2.16.0)는 변경하지 않는다. `appVersion`은 차트가 배포하는 애플리케이션 버전을 나타내는 메타데이터일 뿐, 실제 배포되는 이미지 태그에 영향을 주지 않는다. 이미지 태그는 `values.yaml`의 `image.tag`가 결정한다.

> `"3.1.0"`에 따옴표를 붙이는 이유: YAML에서 숫자로 파싱되는 것을 방지하기 위함이다. Helm 공식 가이드에서도 appVersion에 문자열 따옴표를 권장한다.

---

## 3. 변경 불필요 항목 근거

### 3-0. Helm subchart values 적용 계층 구조

Helm에서 부모 차트(loki-stack)가 자식 차트(loki)를 포함할 때, values는 여러 계층에서 병합(merge)된다. "어디를 수정해야 하는가"를 판단하려면 이 계층 구조를 이해해야 한다.

#### 값 병합 원리

Helm은 values를 **깊은 병합(deep merge)** 한다. 상위 계층에서 같은 키를 선언하면 하위 계층의 값을 덮어쓰고, 선언하지 않은 키는 하위 계층의 기본값이 그대로 살아남는다.

```
helm install loki helm-charts/loki-stack -f values-dev.yaml
```

이 명령을 실행하면 Helm은 아래 순서로 values를 병합한다:

```
① charts/loki/values.yaml        (subchart 자체 기본값 — 우선순위 가장 낮음)
       ↑ 병합
② values.yaml (loki-stack 루트)   (부모 차트 기본값)
       ↑ 병합
③ values-dev.yaml                 (helm install -f 로 주입 — 우선순위 가장 높음)
```

**핵심**: 상위 계층에서 특정 키를 선언하지 않으면, 하위 계층의 값이 그대로 사용된다. "오버라이드하지 않음 = 기본값 유지"다.

#### loki-stack에서의 실제 흐름

이미지 태그(`loki.image.tag`)를 예로 들면:

```
① charts/loki/values.yaml
   image:
     tag: 3.1.0            ← 여기서 3.1.0 선언

② values.yaml (루트)
   loki:
     enabled: true
     nodeSelector: {}       ← loki.image 키 자체가 없음 → ①의 3.1.0 유지

③ values-dev.yaml
   loki:
     config:
       common: ...          ← loki.image 키 없음 → 여전히 ①의 3.1.0 유지
```

부모 차트에서 subchart 값을 오버라이드할 때는 **subchart 이름을 키로** 사용한다. 예를 들어 부모의 `values.yaml`에서 `loki.image.tag: 2.9.0`이라고 쓰면 subchart의 `image.tag: 3.1.0`이 덮어씌워진다. 현재 루트 `values.yaml`과 `values-dev.yaml` 어디에도 `loki.image` 키가 없으므로 subchart 기본값 3.1.0이 최종값이 된다.

#### 각 파일의 역할과 책임

| 계층 | 파일 | 책임 | 이 파일이 관리하는 것 |
|------|------|------|---------------------|
| ① subchart 기본값 | `charts/loki/values.yaml` | Loki 자체 설정의 원본 | 이미지 태그, schema, storage, compactor, 포트, probe |
| ② 부모 차트 기본값 | `values.yaml` (루트) | 스택 전체의 기본 구성 | 어떤 컴포넌트를 켤지(enabled), Grafana/Promtail 기본 설정 |
| ③ 환경별 오버라이드 | `values-dev.yaml` | dev 환경 고유 설정 | MinIO 인증, retention, Grafana ingress 호스트 |
| ③ 환경별 오버라이드 | `values-op.yaml` | op 환경 고유 설정 | Nexus 레지스트리 경로, MinIO 인증, Grafana 비활성화 |

#### 왜 이미지 버전을 subchart에서 관리하는가

이미지 버전을 루트 `values.yaml`이나 `values-dev.yaml`로 올려서 관리할 수도 있다. 하지만 현재 구조에서는 subchart에 두는 것이 적절한데, 이유는 다음과 같다:

1. **환경 간 버전 동일**: dev/op 모두 Loki 3.1.0을 사용한다. 환경별로 버전이 다르다면 `values-dev.yaml`과 `values-op.yaml`에서 각각 오버라이드해야 하지만, 동일하므로 subchart 한 곳에서 관리하는 게 변경점이 집중된다.
2. **단일 진실 원천(Single Source of Truth)**: subchart와 부모 양쪽에 `image.tag`를 쓰면 "어디가 최종인가?"라는 혼란이 생긴다. subchart에만 두면 의심의 여지가 없다.
3. **subchart 교체 시 자연스러운 버전 업**: 나중에 Loki 4.x로 올린다면 subchart의 `values.yaml`만 수정하면 되고, 부모 차트를 건드릴 필요가 없다.

만약 환경별로 Loki 버전을 다르게 써야 하는 상황이 생기면, 그때 `values-dev.yaml`에 `loki.image.tag: 4.0.0` 같은 오버라이드를 추가하면 된다.

#### 현재 loki-stack의 값 적용 결과 요약

| 설정 키 | ① subchart | ② 루트 values.yaml | ③ values-dev.yaml | 최종 적용 값 |
|---------|-----------|-------------------|-------------------|------------|
| `loki.image.tag` | `3.1.0` | 미선언 | 미선언 | **3.1.0** (①) |
| `loki.config.schema_config` | v13/tsdb | 미선언 | 미선언 | **v13/tsdb** (①) |
| `loki.config.common.storage.s3` | MinIO 연결정보 | 미선언 | MinIO 인증 오버라이드 | **③의 값** |
| `loki.config.limits_config.retention_period` | `168h` | 미선언 | `168h` | **168h** (③, 동일값) |
| `grafana.enabled` | — | `true` | `true` | **true** (③) |
| `grafana.image.tag` | — | `11.2.0` | `11.4.0` | **11.4.0** (③이 ②를 오버라이드) |
| `promtail.enabled` | — | `true` | `false` | **false** (③이 ②를 오버라이드) |

#### Chart.yaml vs values-dev.yaml: 역할이 완전히 다르다

이 두 파일은 이름이 비슷해 보이지만 Helm에서 완전히 다른 역할을 한다. 혼동하기 쉬우므로 정리한다.

**Chart.yaml — 차트의 "신분증"**

```yaml
# helm-charts/loki-stack/Chart.yaml
apiVersion: v1
name: loki-stack
version: 2.10.0        # 차트 자체의 버전 (패키징/배포 단위)
appVersion: v2.6.1      # "이 차트가 배포하는 앱의 버전" (표시용)
```

Chart.yaml은 Helm 차트의 메타데이터를 정의한다. npm의 `package.json`이나 Maven의 `pom.xml`에서 버전 정보를 선언하는 것과 같다. 여기에 적힌 값은 **실제 배포에 영향을 주지 않는다.** `helm list`의 APP VERSION 컬럼, ArgoCD UI의 버전 표시, `helm search repo`의 검색 결과에만 사용된다.

| 필드 | 용도 | 실제 배포 영향 |
|------|------|--------------|
| `name` | 차트 이름 | 없음 (Release 이름은 `helm install <release-name>`으로 결정) |
| `version` | 차트 패키징 버전 | Helm 레포에서 차트를 가져올 때 버전 선택에 사용 |
| `appVersion` | 앱 버전 표시 | **없음** — 순수 표시용 문자열 |
| `description` | 설명 | 없음 |

**values-dev.yaml — 실제 배포를 결정하는 설정값**

```yaml
# helm-charts/loki-stack/values-dev.yaml
loki:
  config:
    common:
      storage:
        s3:
          access_key_id: loki
          endpoint: http://minio.trb-oss.svc.cluster.local:9000
grafana:
  enabled: true
  image:
    tag: 11.4.0
```

values 파일은 Helm 템플릿에 주입되는 **실제 설정값**이다. 여기에 적힌 이미지 태그, 포트, 환경변수, 인증정보가 K8s 매니페스트(StatefulSet, Secret, Service 등)로 렌더링되어 클러스터에 적용된다.

| 파일 | 용도 | 실제 배포 영향 |
|------|------|--------------|
| `values.yaml` | 모든 환경의 기본값 | **있음** — 템플릿 렌더링의 기본 입력 |
| `values-dev.yaml` | dev 환경 오버라이드 | **있음** — 기본값을 dev 환경에 맞게 덮어씀 |
| `values-op.yaml` | op 환경 오버라이드 | **있음** — 기본값을 op 환경에 맞게 덮어씀 |

**비유하자면**: Chart.yaml은 책의 표지(제목, 저자, 판수)이고, values-dev.yaml은 책의 내용(실제 텍스트)이다. 표지에 "초판"이라고 적혀 있어도 내용이 개정판이면 독자가 읽는 건 개정판 내용이다. 지금 loki-stack이 정확히 이 상태다 — 표지(Chart.yaml)는 v2.6.1이지만, 내용(values)은 3.1.0이다.

### 3-1. charts/loki/values.yaml (subchart 기본값 — 이미 정합됨)

subchart의 `charts/loki/values.yaml`을 확인하면 다음이 이미 설정되어 있다:

- `image.tag: 3.1.0` — Loki 3.1.0 이미지 사용 중
- `schema_config.configs[0].schema: v13` — Loki 3.x 전용 스키마
- `schema_config.configs[0].store: tsdb` — Loki 3.x 전용 스토리지 엔진
- `storage_config.tsdb_shipper` — TSDB 인덱스 관리
- `storage_config.aws.s3` — MinIO(S3 호환) 연결 정보
- `compactor.retention_enabled: true` — 168시간(7일) 보존 정책

이 설정들은 클러스터에서 실행 중인 Loki Secret(`loki`)의 `loki.yaml`과 일치한다.

### 3-2. templates/ (호환성 확인됨)

v2.16.0 차트의 템플릿이 Loki 3.x single-binary 모드와 호환되는 이유:

1. **StatefulSet 구조 동일**: Loki 2.x와 3.x 모두 single-binary 모드에서 StatefulSet 1 replica를 사용한다. 템플릿이 생성하는 StatefulSet spec(포트, 볼륨 마운트, probe 경로)이 동일하다.
2. **설정 주입 방식**: 템플릿은 `values.yaml`의 `config` 블록을 그대로 Secret으로 렌더링한다. config 내용을 해석하지 않으므로 Loki 버전에 무관하게 동작한다.
3. **서비스 포트**: HTTP 3100, gRPC 9095는 Loki 2.x/3.x 공통이다.
4. **Probe 경로**: `/ready` 엔드포인트는 Loki 2.x/3.x 공통이다.

### 3-3. values-dev.yaml / values-op.yaml

환경별 오버라이드 파일도 이미 3.1.0 설정과 정합되어 있다. MinIO 연결 정보와 retention 설정이 subchart `values.yaml`과 일관된다.

---

## 4. 실행 절차

### 4-1. 클러스터 실제 버전 확인

변경 전에 클러스터에서 실행 중인 Loki 버전을 한 번 더 확인한다.

```bash
ssh master-1

# StatefulSet 이미지 태그 확인
kubectl -n trb-mgm get statefulset loki \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
# 예상 출력: grafana/loki:3.1.0 또는 nexus.okestro-k8s.com:55000/.../grafana/loki:3.1.0

# Loki 버전 API로 직접 확인
kubectl -n trb-mgm exec statefulset/loki -- \
  wget -qO- http://localhost:3100/loki/api/v1/status/buildinfo 2>/dev/null \
  | grep version
# 예상 출력: "version":"3.1.0"

# Secret에서 schema 확인
kubectl -n trb-mgm get secret loki -o jsonpath='{.data.loki\.yaml}' \
  | base64 -d | grep -A3 schema_config
# 예상: schema: v13, store: tsdb
```

출력이 3.1.0이 아니라면 이 가이드의 대상이 아니다. 실제 클러스터 버전에 맞춰 appVersion을 조정해야 한다.

### 4-2. Chart.yaml 메타데이터 수정

로컬에서 2개 파일을 수정한다.

```bash
cd ~/okestro/tps_manifest

# 파일 1: loki-stack 루트 Chart.yaml
sed -i '' 's/appVersion: v2.6.1/appVersion: "3.1.0"/' \
  helm-charts/loki-stack/Chart.yaml

# 파일 2: loki subchart Chart.yaml
sed -i '' 's/appVersion: v2.6.1/appVersion: "3.1.0"/' \
  helm-charts/loki-stack/charts/loki/Chart.yaml

# 변경 확인
git diff helm-charts/loki-stack/Chart.yaml \
         helm-charts/loki-stack/charts/loki/Chart.yaml
```

diff 출력이 각 파일에서 `appVersion` 1줄만 변경되었는지 확인한다. 다른 줄이 바뀌었다면 되돌리고 수동으로 편집한다.

### 4-3. helm template 로컬 렌더링 테스트

메타데이터 변경이 렌더링 결과에 영향을 주지 않는지 확인한다.

```bash
# 변경 전 렌더링 (git stash로 원본 복원 후 실행)
git stash
helm template loki helm-charts/loki-stack \
  -f helm-charts/loki-stack/values-dev.yaml \
  --namespace trb-mgm > /tmp/loki-before.yaml
git stash pop

# 변경 후 렌더링
helm template loki helm-charts/loki-stack \
  -f helm-charts/loki-stack/values-dev.yaml \
  --namespace trb-mgm > /tmp/loki-after.yaml

# 비교 — 차이가 없어야 정상
diff /tmp/loki-before.yaml /tmp/loki-after.yaml
```

`appVersion`은 메타데이터이므로 렌더링 결과에 차이가 없어야 한다. 만약 차이가 있다면 템플릿에서 `.Chart.AppVersion`을 참조하는 곳이 있다는 뜻이므로, 해당 부분을 확인한 뒤 진행 여부를 판단한다.

### 4-4. 렌더링 결과 vs 클러스터 실제 diff

렌더링 결과가 클러스터에서 실행 중인 리소스와 일치하는지 비교한다. 이 단계는 ArgoCD 등록 전 준비 작업(Phase 0)의 일부다.

```bash
# 로컬 렌더링 (이미 /tmp/loki-after.yaml에 있음)

# 클러스터 실제 리소스 (SSH에서)
ssh master-1
kubectl -n trb-mgm get statefulset loki -o yaml > /tmp/loki-cluster.yaml
kubectl -n trb-mgm get secret loki -o yaml > /tmp/loki-secret-cluster.yaml
kubectl -n trb-mgm get service loki -o yaml > /tmp/loki-svc-cluster.yaml
```

비교 시 주의점:
- 클러스터 리소스에는 `metadata.annotations`, `status`, `metadata.resourceVersion` 등 런타임 필드가 포함되어 있으므로 이를 제외하고 비교한다
- Secret의 `data`는 base64 인코딩이므로 디코딩 후 비교한다

### 4-5. Git commit & push

```bash
cd ~/okestro/tps_manifest
git add helm-charts/loki-stack/Chart.yaml \
        helm-charts/loki-stack/charts/loki/Chart.yaml

git commit -m "chore: Loki Chart.yaml appVersion을 3.1.0으로 정합

values.yaml의 image.tag/schema/storage는 이미 3.1.0에 맞춰져 있었으나
Chart.yaml appVersion만 v2.6.1로 남아있던 불일치를 해소한다."

git push origin main
```

### 4-6. ArgoCD sync 확인

trb-mgm이 ArgoCD에 등록된 경우에만 해당한다. 현재는 등록되어 있지 않으므로(`promtail-to-alloy-전환-가이드.md` 섹션 4-1 참조) 이 단계는 건너뛴다.

등록 후라면:
```bash
# ArgoCD Application 상태 확인
kubectl -n trb-oss get application loki -o jsonpath='{.status.sync.status}'
# 예상: Synced

# OutOfSync diff가 없는지 확인
kubectl -n trb-oss get application loki -o jsonpath='{.status.conditions}'
# 예상: 빈 배열 또는 healthy 조건만
```

appVersion은 메타데이터이므로 ArgoCD가 diff를 감지하지 않을 수 있다. 그래도 Sync 상태가 정상인지 한 번 확인하는 것이 좋다.

---

## 5. values-dev vs values-op 비교

두 환경 파일의 차이점을 정리한다. Loki config 자체는 subchart `values.yaml`에서 공통 관리되고, 환경별 파일은 주변 서비스 설정만 오버라이드한다.

| 항목 | values-dev.yaml | values-op.yaml |
|------|-----------------|----------------|
| **이미지 레지스트리** | `docker.io` (공용) | `nexus.okestro-k8s.com:55000/trombone` (폐쇄망) |
| **Grafana 활성화** | `enabled: true` | `enabled: false` |
| **Grafana 태그** | `11.4.0` | `11.2.0` |
| **Grafana Ingress** | `grafana.dev.console.trombone.okestro.cloud` | `grafana.prd.console.trombone.okestro.cloud` |
| **Promtail** | `enabled: false` | `enabled: false` |
| **MinIO access_key** | `loki` | `loki` |
| **MinIO secret_key** | `ZwMGEo...` | `flaKLI...` (다름) |
| **MinIO endpoint** | `minio.trb-oss.svc.cluster.local:9000` | 동일 |
| **Loki retention** | `168h` (7일) | `168h` (7일) |

핵심 차이: op 환경은 Nexus 프록시 레지스트리를 사용하고, Grafana가 비활성화되어 있으며, MinIO secret_key가 다르다. Loki 자체 설정(스키마, 스토리지, 보존 정책)은 동일하다.

> op 환경에서도 동일하게 Chart.yaml appVersion을 수정해야 한다. 같은 파일을 공유하므로 한 번 수정으로 양쪽에 적용된다.

---

## 6. 롤백 절차

이 변경은 Chart.yaml 메타데이터만 수정하므로 롤백이 단순하다.

```bash
cd ~/okestro/tps_manifest

# 방법 1: git revert (권장)
git revert HEAD
git push origin main

# 방법 2: 수동 복원
sed -i '' 's/appVersion: "3.1.0"/appVersion: v2.6.1/' \
  helm-charts/loki-stack/Chart.yaml \
  helm-charts/loki-stack/charts/loki/Chart.yaml
git add -A && git commit -m "revert: Loki appVersion 원복" && git push origin main
```

appVersion은 메타데이터이므로 롤백해도 클러스터에서 실행 중인 Loki에 영향이 없다. 이미지 태그(`values.yaml`의 `image.tag: 3.1.0`)는 변경하지 않았으므로 Loki 컨테이너가 재시작되거나 다운그레이드되지 않는다.

---

## 7. promtail-to-alloy 연관관계

이 작업은 `promtail-to-alloy-전환-가이드.md`의 **Phase 0-2(Loki/Promtail 버전 정합)** 중 Chart.yaml 메타데이터 부분에 해당한다.

Phase 0 전체 절차에서의 위치:

| 단계 | 작업 | 이 가이드 범위 |
|------|------|--------------|
| 0-1 | Git 인증 정보 업데이트 (8개 values 파일) | 범위 밖 |
| **0-2** | **Loki 버전 정합** | **이 가이드** (Chart.yaml 메타데이터) |
| 0-3 | 로컬 Helm 렌더링 검증 | 이 가이드 4-3, 4-4 포함 |
| 0-4 | ArgoCD 루트 Application 등록 | 범위 밖 |
| 0-5 | 기존 Helm release 인계 | 범위 밖 |

Phase 0-2에서 남은 작업:
- `promtail.enabled: true`로 변경 (클러스터에서는 Promtail이 8대 Running이지만 Git에서는 `false`) — 이건 ArgoCD 등록 직전에 수행해야 한다. 지금 변경하면 `helm install`에는 영향이 없지만, ArgoCD Sync 시 Promtail DaemonSet이 삭제될 수 있다.

---

## 8. 체크리스트

```
사전 확인
□ 클러스터 Loki 버전이 3.1.0인지 확인 (4-1)
□ values.yaml의 image.tag, schema, storage가 3.1.0 설정인지 확인

변경 실행
□ helm-charts/loki-stack/Chart.yaml — appVersion: "3.1.0"
□ helm-charts/loki-stack/charts/loki/Chart.yaml — appVersion: "3.1.0"
□ 다른 줄은 변경하지 않았는지 git diff로 확인

검증
□ helm template 변경 전/후 diff 없음 (4-3)
□ 렌더링 결과의 StatefulSet 이미지가 grafana/loki:3.1.0
□ 렌더링 결과의 Secret에 schema v13, tsdb, S3 설정 포함

배포
□ git commit & push
□ (ArgoCD 등록 시) OutOfSync diff 없음 확인
```

---

## 참고 자료

- Helm Chart.yaml 스펙: `appVersion`은 표시용 메타데이터이며 이미지 태그에 영향 없음
- 전환 가이드: `promtail-to-alloy-전환-가이드.md` (Phase 0 상세)
- ArgoCD 구조: `tps-manifest-argocd-구조-분석.md`
- Helm 차트 추가: `tps-manifest-helm-차트-추가-가이드.md`
