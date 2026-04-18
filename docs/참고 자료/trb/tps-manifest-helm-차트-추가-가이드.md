# tps_manifest에 새 Helm 차트 추가 가이드

> 작성일: 2026-03-12 | 전제 문서: `tps-manifest-argocd-구조-분석.md`

이 문서는 TPS의 App-of-Apps 매니페스트 구조에 새 서비스의 Helm 차트를 추가하는 실제 절차를 설명한다. 예시로 `alloy`(Grafana Alloy)를 `trb-mgm`에 추가하는 과정을 따른다.

구조 분석 문서의 섹션 2-3(2단계 path 참조 구조)을 이해하고 있어야 이 가이드의 "어디에 무엇을 만드는지"가 혼동 없이 따라갈 수 있다.

---

## 1. 전체 흐름 요약

```
1. helm-charts/ 에 실제 차트 준비
2. charts/trb-mgm/templates/ 에 ArgoCD Application 템플릿 추가
3. charts/trb-mgm/values-dev.yaml 에 서비스 블록 추가
4. 로컬에서 Helm 렌더링 테스트
5. Git push → ArgoCD 자동 반영
```

작업 대상 디렉토리를 정리하면 이렇다:

```
tps_manifest/
├── helm-charts/{name}/                              ← Step 1: 실제 K8s 리소스 차트
├── argocd-apps/app-of-apps/charts/trb-mgm/
│   ├── templates/{name}.yaml                        ← Step 2: ArgoCD Application 템플릿
│   └── values-dev.yaml                              ← Step 3: 서비스 블록 추가
```

---

## 2. Step 1 — Helm 차트 가져오기

공식 Helm 차트를 `helm-charts/` 디렉토리에 가져온다. 방법은 두 가지다.

### 방법 A: `helm pull`로 다운로드 후 압축 해제

외부 오픈소스 차트(Prometheus, Loki, Grafana 등)를 가져올 때 사용한다.

```bash
# 차트 저장소 추가
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 차트 다운로드 (특정 버전 지정 권장)
helm pull grafana/alloy --version 0.12.0 --untar --untardir helm-charts/

# 결과: helm-charts/alloy/ 디렉토리 생성
```

`--version`을 지정하는 이유는 재현성이다. 버전 없이 pull하면 최신 버전이 받아지는데, 나중에 같은 명령을 실행했을 때 다른 버전이 받아져서 예상치 못한 변경이 발생할 수 있다.

### 방법 B: 기존 차트를 복사하고 수정

자체 서비스이거나 단순한 Deployment/Service 구성이라면 기존 차트(예: `helm-charts/jenkins/`)를 복사해서 `templates/`와 `values.yaml`을 수정하는 방법도 있다.

### 환경별 values 파일 생성

차트를 가져온 후 환경별 values 파일을 추가한다:

```bash
# 기본 values.yaml은 이미 포함되어 있으므로, 환경별 오버라이드만 생성
cd helm-charts/alloy/
touch values-dev.yaml values-stg.yaml values-prd.yaml
```

`values-dev.yaml`에는 기본값(`values.yaml`)과 **다른 부분만** 작성한다. Helm은 `values.yaml`을 먼저 적용하고 `values-dev.yaml`로 오버라이드하기 때문이다. 주로 들어가는 내용은 리소스 제한(`resources.limits`), 레플리카 수, 환경별 엔드포인트, 스토리지 크기 등이다.

---

## 3. Step 2 — ArgoCD Application 템플릿 작성

`argocd-apps/app-of-apps/charts/trb-mgm/templates/`에 새 파일을 만든다. 기존 템플릿을 복사하고 이름과 참조만 바꾸면 된다:

```bash
cp argocd-apps/app-of-apps/charts/trb-mgm/templates/loki-stack.yaml \
   argocd-apps/app-of-apps/charts/trb-mgm/templates/alloy.yaml
```

`alloy.yaml`에서 바꿀 부분은 3곳뿐이다:

```yaml
{{- if .Values.alloy.enabled }}          # ① .Values.{서비스명}.enabled
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: alloy                            # ② metadata.name
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
    path: {{ .Values.alloy.helmPath }}    # ③ .Values.{서비스명}.helmPath
    repoURL: {{ .Values.repository.url }}
    targetRevision: {{ .Values.repository.branch }}
  syncPolicy:
    {{- .Values.application.syncPolicy | toYaml | nindent 4 }}
{{- end }}
```

나머지(`application.*`, `repository.*`, `syncPolicy`)는 공통 설정이므로 건드리지 않는다. 이 값들은 `values-dev.yaml`의 `application:` 블록에서 일괄 주입된다.

---

## 4. Step 3 — values-dev.yaml에 서비스 블록 추가

`argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml` 하단에 추가:

```yaml
alloy:
  enabled: true
  helmPath: helm-charts/alloy
```

| 필드 | 역할 |
|------|------|
| `enabled` | `true`면 ArgoCD Application 생성, `false`면 생성하지 않음 (기존 배포가 있으면 `prune: true`에 의해 클러스터에서도 삭제) |
| `helmPath` | 실제 K8s 리소스를 만드는 Helm 차트 경로 (Git 레포 루트 기준 상대경로) |

다른 환경(stg, prd)에도 배포하려면 `values-stg.yaml`, `values-prd.yaml`에도 동일한 블록을 추가해야 한다.

---

## 5. Step 4 — 로컬 렌더링 테스트

Git push 전에 Helm 렌더링이 정상인지 로컬에서 확인한다. `helm template`은 렌더링만 수행하고 클러스터에 적용하지 않으므로 안전하다.

### 테스트 1: App-of-Apps 템플릿 확인

루트 차트가 올바른 ArgoCD Application yaml을 생성하는지 확인한다:

```bash
cd tps_manifest/

helm template trb-mgm argocd-apps/app-of-apps/charts/trb-mgm \
  -f argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml
```

출력에서 확인할 것:
- `alloy`라는 이름의 Application이 생성되는가
- `source.path`가 `helm-charts/alloy`를 가리키는가
- `valueFiles`에 `values-dev.yaml`이 포함되어 있는가

### 테스트 2: 실제 차트 렌더링 확인

Helm 차트가 유효한 K8s 리소스를 생성하는지 확인한다:

```bash
helm template alloy helm-charts/alloy \
  -f helm-charts/alloy/values-dev.yaml \
  --namespace trb-mgm
```

출력에서 확인할 것:
- Deployment/DaemonSet, Service, ConfigMap 등이 정상적으로 생성되는가
- 문법 오류(indentation, 누락된 변수)가 없는가
- namespace가 `trb-mgm`으로 설정되어 있는가

### 흔한 오류와 대처

| 오류 | 원인 | 해결 |
|------|------|------|
| `Error: template: no template "xxx" associated with template "xxx"` | templates/ 디렉토리에 파일이 없음 | 차트 구조 확인 (`Chart.yaml` + `templates/` 필수) |
| `Error: values don't meet the specifications` | values-dev.yaml 형식 오류 | YAML 들여쓰기 확인 |
| `nil pointer evaluating interface {}` | values에 필요한 키가 누락 | `values.yaml`과 `values-dev.yaml` 키 대조 |

---

## 6. Step 5 — Git Push 후 확인

```bash
git add helm-charts/alloy/ \
        argocd-apps/app-of-apps/charts/trb-mgm/templates/alloy.yaml \
        argocd-apps/app-of-apps/charts/trb-mgm/values-dev.yaml

git commit -m "feat: add alloy helm chart to trb-mgm"
git push origin main
```

ArgoCD가 Git 변경을 감지하면(기본 3분 폴링 또는 webhook) 자동으로:
1. 루트 Application(`trb-mgm`)이 재렌더링되어 `alloy` 자식 Application 생성
2. `alloy` Application이 `helm-charts/alloy/`를 렌더링하여 실제 K8s 리소스 배포

### ArgoCD UI에서 확인

1. `trb-mgm` Application 클릭 → 하위에 `alloy`가 나타나는지 확인
2. `alloy` Application의 상태가 **Healthy/Synced**이면 성공
3. OutOfSync 상태라면 Sync 버튼 클릭 (auto-sync가 설정되어 있으면 자동으로 진행)
4. 에러가 있으면 Application 클릭 → Events 탭에서 원인 확인

---

## 7. 체크리스트

```
□ helm-charts/{name}/                    차트 디렉토리 존재
□ helm-charts/{name}/Chart.yaml          차트 메타데이터
□ helm-charts/{name}/values.yaml         기본값 (보통 upstream 원본)
□ helm-charts/{name}/values-dev.yaml     환경별 오버라이드
□ charts/{namespace}/templates/{name}.yaml   ArgoCD Application 템플릿
□ charts/{namespace}/values-dev.yaml     서비스 블록 (enabled + helmPath)
□ helm template 테스트 1 (App-of-Apps) 통과
□ helm template 테스트 2 (실제 차트) 통과
□ Git push 후 ArgoCD UI에서 Healthy/Synced 확인
```

---

## 8. trb-oss에 추가하는 경우

위 예시는 `trb-mgm`(모니터링) 기준이다. OSS 도구(Jenkins, Harbor 등)를 추가하려면 경로만 바꾸면 된다:

| 항목 | trb-mgm (모니터링) | trb-oss (OSS 도구) |
|------|--------------------|--------------------|
| Application 템플릿 | `charts/trb-mgm/templates/` | `charts/trb-oss/templates/` |
| values 파일 | `charts/trb-mgm/values-dev.yaml` | `charts/trb-oss/values-dev.yaml` |
| 배포 대상 namespace | `trb-mgm` | `trb-oss` |

Helm 차트 자체(`helm-charts/{name}/`)는 어느 네임스페이스에 배포하든 같은 위치에 둔다.

---

## 참고

- 구조 이해: `tps-manifest-argocd-구조-분석.md`
- 실제 마이그레이션 사례: `promtail-to-alloy-migration-handson.md`
