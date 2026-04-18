# Grafana 통합 및 Sidecar 연동 가이드

> 작성일: 2026-03-13
> TPS(Trombone) 개발 환경 모니터링 스택 대상
> 전제 지식: `loki-helm-차트-버전-정합-가이드.md`

---

## 1. 배경 및 문제 정의

개발계 클러스터에서 Grafana가 2개 중복 배포되고 있었다:

- loki-stack 차트: Grafana enabled (11.4.0), ingress `grafana.dev.trb.com`
- kube-prometheus-stack 차트: Grafana enabled, K8s 대시보드 + datasource 자동 구성

Grafana 2개가 별도 ingress로 접근 가능하여 사용자가 어느 Grafana를 써야 하는지 혼란이 발생했다. 또한 loki-stack Grafana는 Loki만, kube-prometheus-stack Grafana는 Prometheus만 datasource로 가지고 있어 한 곳에서 전체 관측 데이터를 볼 수 없었다.

---

## 2. 변경 전 현황

### 차트별 배포 컴포넌트

| 차트 | Prometheus | Grafana | Loki | Promtail |
|------|-----------|---------|------|---------|
| loki-stack (values-dev.yaml) | disabled | **enabled** (11.4.0) | enabled (3.1.0) | disabled |
| kube-prometheus-stack (values-dev.yaml) | enabled (Operator v0.79.2) | **enabled** | — | — |

### App of Apps 구조

argocd-apps/app-of-apps/charts/trb-mgm/ 아래 다음 템플릿이 정의되어 있다:

- `templates/loki-stack.yaml` → helm-charts/loki-stack
- `templates/kube-prometheus-stack.yaml` → helm-charts/kube-prometheus-stack
- `templates/alloy.yaml` → helm-charts/alloy
- `values-dev.yaml`: `loki.enabled=true`, `prometheus.enabled=true`, `alloy.enabled=true`

---

## 3. Grafana Sidecar Datasource 자동 발견 메커니즘

이것이 이번 작업의 핵심 발견이다. loki-stack의 `templates/datasources.yaml`은 Grafana Deployment가 아닌 **ConfigMap**을 생성한다:

```yaml
# loki-stack/templates/datasources.yaml (조건: grafana.sidecar.datasources.enabled)
metadata:
  labels:
    grafana_datasource: "1"    # sidecar가 감지하는 라벨
data:
  loki-stack-datasource.yaml:
    datasources:
    - name: Loki
      type: loki
      url: "http://loki:3100"
```

kube-prometheus-stack의 Grafana Pod에는 sidecar 컨테이너가 포함되어 있다. 이 sidecar는 같은 네임스페이스(trb-mgm)에서 `grafana_datasource: "1"` 라벨이 붙은 ConfigMap을 자동으로 감시한다. 새로운 ConfigMap을 발견하면 Grafana에 datasource로 등록한다.

**핵심**: ConfigMap 생성 조건은 `grafana.sidecar.datasources.enabled`이지, `grafana.enabled`가 아니다. 따라서 loki-stack의 Grafana를 비활성화해도(`grafana.enabled: false`), sidecar datasource ConfigMap은 `grafana.sidecar.datasources.enabled: true`가 values-dev.yaml에 남아 있으므로 계속 생성된다.

이 메커니즘 덕분에 별도 수동 설정(`additionalDataSources`) 없이도 Loki가 kube-prometheus-stack Grafana에 자동 등록된다.

---

## 4. 변경 내용

### 4-1. loki-stack Grafana 비활성화

파일: `helm-charts/loki-stack/values-dev.yaml`

```yaml
# Before
grafana:
  enabled: true

# After
grafana:
  enabled: false
```

### 4-2. ingress 호스트 변경 (향후 대비)

같은 파일에서 Grafana ingress 호스트를 수정했다:

```yaml
# Before
hosts:
  - grafana.dev.trb.com

# After
hosts:
  - grafana.dev.console.trombone.okestro.cloud
```

현재 Grafana가 disabled 상태이므로 실제 영향은 없다. 향후 활성화할 경우를 대비해 도메인을 통일해 둔 것이다.

### 4-3. additionalDataSources 추가 후 제거

처음에는 `kube-prometheus-stack/values-dev.yaml`의 `grafana.additionalDataSources`에 Loki를 수동으로 추가했다. 그러나 섹션 3에서 설명한 sidecar 자동 발견 메커니즘을 확인한 후 제거했다. 수동 추가와 sidecar 자동 발견이 동시에 작동하면 Grafana에 Loki datasource가 2개 중복 표시된다.

---

## 5. 변경 후 상태

### 차트별 실제 배포 컴포넌트

| 차트 | 실제 배포 컴포넌트 |
|------|-----------------|
| loki-stack | Loki StatefulSet만 (+ sidecar datasource ConfigMap) |
| kube-prometheus-stack | Prometheus + Grafana + AlertManager + node-exporter + kube-state-metrics |
| alloy | Alloy DaemonSet |

Grafana 하나에서 Prometheus(메트릭)와 Loki(로그) 양쪽 데이터를 조회할 수 있다.

---

## 6. 검증 방법

```bash
# 1. loki-stack 렌더링에서 Grafana Deployment가 없는지 확인
helm template loki helm-charts/loki-stack \
  -f helm-charts/loki-stack/values-dev.yaml \
  --namespace trb-mgm | grep "kind: Deployment"
# Grafana Deployment가 없어야 정상

# 2. sidecar datasource ConfigMap은 여전히 생성되는지 확인
helm template loki helm-charts/loki-stack \
  -f helm-charts/loki-stack/values-dev.yaml \
  --namespace trb-mgm | grep -A5 "grafana_datasource"
# grafana_datasource: "1" 라벨이 있어야 정상

# 3. 클러스터에서 Grafana Pod 개수 확인
kubectl -n trb-mgm get pods | grep grafana
# kube-prometheus-stack의 Grafana 1개만 있어야 정상

# 4. Grafana UI에서 Loki datasource 확인
# Grafana → Configuration → Data Sources → Loki 있는지 확인
```

---

## 7. 커밋 이력

```
d684d2ef revert: kube-prometheus-stack additionalDataSources 제거
dc305bb9 chore: loki-stack Grafana ingress 호스트를 console 도메인으로 변경
c39561d4 chore: Grafana 통합 — loki-stack Grafana 비활성화, kube-prometheus-stack에 Loki datasource 추가
```

---

## 8. 롤백 절차

loki-stack Grafana를 다시 활성화해야 하는 경우:

```bash
cd ~/okestro/tps_manifest

# loki-stack Grafana 재활성화
# helm-charts/loki-stack/values-dev.yaml에서 grafana.enabled: true로 변경
git revert d684d2ef dc305bb9 c39561d4
git push origin main
```

롤백 후 kube-prometheus-stack Grafana와 loki-stack Grafana가 다시 공존하게 된다. 이 경우 kube-prometheus-stack의 `grafana.additionalDataSources`에서 Loki를 수동으로 제거하거나, loki-stack의 `grafana.sidecar.datasources.enabled`를 `false`로 설정해 중복을 막아야 한다.

---

## 9. 체크리스트

```
변경 확인
□ loki-stack values-dev.yaml grafana.enabled: false
□ loki-stack values-dev.yaml grafana.sidecar.datasources.enabled: true (유지)
□ kube-prometheus-stack values-dev.yaml에 additionalDataSources 없음

검증
□ helm template에서 Grafana Deployment 미생성 확인
□ helm template에서 sidecar datasource ConfigMap 생성 확인
□ 클러스터 Grafana Pod 1개만 존재
□ Grafana UI에서 Loki datasource 접근 가능
```

---

## 참고 자료

- Helm 값 병합: `loki-helm-차트-버전-정합-가이드.md` 섹션 3-0
- ArgoCD 구조: `tps-manifest-argocd-구조-분석.md`
- Promtail→Alloy 전환: `promtail-to-alloy-전환-가이드.md`
