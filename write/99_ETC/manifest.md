---
title: manifest
tags: []
status: draft
related: []
updated: 2026-04-19
---

# App-of-Apps

---

## 일반 ArgoCD 배포

> **ArgoCD의 기본 사용법은 하나의 Application 리소스가 하나의 서비스를 배포하는 구조다.** 
>
> - Jenkins를 배포하려면 Jenkins Application을 만들고, Grafana를 배포하려면 Grafana Application을 만든다. 
> - 서비스가 5개라면 ArgoCD에 5개의 Application을 각각 수동 등록해야 한다.

```
ArgoCD UI에서 수동 등록:
  Application: jenkins   → helm-charts/jenkins/
  Application: grafana   → helm-charts/grafana/
  Application: loki      → helm-charts/loki-stack/
  Application: prometheus → helm-charts/kube-prometheus-stack/
  ...
```

서비스가 적을 때는 문제없지만, TPS처럼 20개 이상의 서비스를 관리하면 Application 등록/삭제를 일일이 UI에서 해야 하고, 어떤 환경에 무엇이 배포되어 있는지 Git으로 추적할 수 없다.

## App-of-Apps 패턴

> **App-of-Apps는 "Application을 생성하는 Application"이다.** 
>
> - 루트 Application 하나만 ArgoCD에 수동 등록하면, 그 Application이 Helm 템플릿을 렌더링하여 자식 Application들을 자동으로 생성한다.

```
ArgoCD에 수동 등록하는 것은 딱 1개:
  루트 Application: trb-mgm
    ↓ Helm 렌더링
    자식 Application: loki        (자동 생성)
    자식 Application: prometheus  (자동 생성)
    자식 Application: alloy       (자동 생성)
```

이 패턴을 쓰는 이유는 명확하다. 새 서비스를 추가할 때 ArgoCD UI를 건드릴 필요 없이 Git에 템플릿 파일 하나를 추가하고 push하면 된다. 서비스 목록 자체가 Git으로 관리되므로 "언제 누가 어떤 서비스를 추가/제거했는지"가 커밋 히스토리에 남는다.

## Helm 기본 용어

| 용어                | 설명                                                         |
| ------------------- | ------------------------------------------------------------ |
| `Chart.yaml`        | Helm 차트의 메타데이터 파일. 차트 이름, 버전 등을 정의한다. `package.json`이나 `pom.xml`의 역할과 비슷하다. |
| `values.yaml`       | 차트에서 사용할 변수의 기본값을 정의한다. 환경별로 `values-dev.yaml`, `values-prd.yaml`을 만들어 기본값을 오버라이드한다. |
| `templates/`        | K8s yaml 파일에 `{{ .Values.xxx }}` 형태의 변수를 넣은 템플릿 디렉토리. Helm이 values와 결합하여 최종 yaml을 생성(렌더링)한다. |
| `{{ .Values.xxx }}` | Go 템플릿 문법. `values.yaml`에 정의된 값을 참조한다. `{{- if .Values.loki.enabled }}`는 "loki.enabled가 true일 때만 이 블록을 렌더링하라"는 의미다. |

# argocd-apps 폴더분석 (무엇을 배포하는가?)

---

> ArgoCD Application의 정의를 담고 있습니다. 실제 K8S 리소스가 아니라 어떤 Helm 차트를 어떤 설정으로 배포할지를 선언한다.

## 환경별 루트 Application (dev/)

```
argocd-apps/app-of-apps/dev/
├── trb-mgm-application.yaml   ← 모니터링 네임스페이스 루트
├── trb-oss-application.yaml   ← OSS 도구 네임스페이스 루트
├── trb-app-application.yaml   ← 애플리케이션 네임스페이스 루트
└── trb-app-tmp-application.yaml
```

각 파일이 ArgoCD의 `Application` 리소스 하나다. 이것들만 ArgoCD에 수동으로 등록(`kubectl apply`)하면, 나머지는 모두 자동으로 관리된다.

```yaml
# trb-mgm-application.yml의 내용
kind: Application
apiVersion: argoproj.io/v1alpha1
metadata:
  name: trb-mgm
  namespace: trb-oss          # ArgoCD가 설치된 네임스페이스
spec:
  destination:
    namespace: trb-mgm         # 배포 대상 네임스페이스
    server: https://kubernetes.default.svc
  project: default
  source:
    helm:
      valueFiles:
      - values-dev.yaml        # 환경별 values 파일
    path: argocd-apps/app-of-apps/charts/trb-mgm  # ← 이 경로의 Helm 차트를 렌더링
    repoURL: https://bitbucket.org/okestrolab/tps_manifest.git
```

- 핵심은 `source.path`입니다. 이 루트 Application이 `charts/trb-mgm/` 디렉토리를 Helm 차트로 렌더링하면, 그 안의 `templates/` 파일들이 자식 Application으로 생성된다.

### 루트 Application 등록 방법

이 루트 Application yaml을 ArgoCD에 등록하는 방법은 두 가지입니다.

**CLI 방식** (실제 TPS에서 사용):

```bash
kubectl apply -f argocd-apps/app-of-apps/dev/trb-mgm-application.yaml
```

- 이 명령을 한 번 실행하면 ArgoCD가 해당 Application을 인식하고, 이후 자식 Application 생성부터 실제 배포까지 모두 자동으로 처리한다.

**UI 방식** (소규모 환경에서 사용): ArgoCD UI에서 `+ NEW APP` 버튼을 눌러 수동으로 동일한 설정을 입력할 수도 있다. 

- 하지만 yaml 파일로 관리하면 Git에 이력이 남고 환경 복구가 쉽기 때문에, TPS처럼 여러 환경을 운영하는 경우 CLI 방식이 표준이다.
- 등록 후에는 ArgoCD UI에서 트리 형태로 루트 Application과 자식 Application들을 확인할 수 있다.

### 2단계 path 참조 구조 (혼동 주의)

이 구조에서 `path`가 두 번 등장하는데, 각각 역할이 다르다. 이 차이를 이해하지 못하면 "values-dev.yaml이 어디 있는 거지?"라는 혼란에 빠진다.

```bash
# [1단계] 루트 Application (trb-mgm-application.yaml)
  source.path: argocd-apps/app-of-apps/charts/trb-mgm    # ← Application "생성기" 차트
  source.helm.valueFiles: values-dev.yaml                # ← charts/trb-mgm/values-dev.yaml

     ↓ Helm 렌더링으로 자식 Application 생성

# [2단계] 자식 Application (templates/loki-stack.yaml에서 생성)
  source.path: helm-charts/loki-stack                    # ← 실제 K8s 리소스 차트
  source.helm.valueFiles: values-dev.yaml                # ← helm-charts/loki-stack/values-dev.yaml
```

- 1단계의 `path`는 "어떤 Application들을 만들지"를 정의하는 **메타 차트**를 가리킨다. 
- 2단계의 `path`(템플릿에서 `{{ .Values.loki.helmPath }}`로 주입됨)는 Loki의 Deployment, Service 같은 **실제 K8s 리소스**를 만드는 차트를 가리킨다.
- `valueFiles`의 `values-dev.yaml`도 마찬가지로, 1단계에서는 `charts/trb-mgm/values-dev.yaml`을, 2단계에서는 `helm-charts/loki-stack/values-dev.yaml`을 각각 참조한다. 같은 파일명이지만 위치와 역할이 완전히 다르다.

## charts(Application 생성기)

```
argocd-apps/app-of-apps/charts/
├── trb-mgm/                    ← 모니터링 관련 서비스들
│   ├── Chart.yaml              ← Helm 차트 메타데이터
│   ├── values-dev.yaml         ← dev 환경 설정
│   └── templates/
│       ├── loki-stack.yaml     ← Loki ArgoCD Application 템플릿
│       └── kube-prometheus-stack.yaml  ← Prometheus ArgoCD Application 템플릿
│
└── trb-oss/                    ← OSS 도구 서비스들
    ├── Chart.yaml
    ├── values-dev.yaml
    └── templates/
        ├── gitlab.yaml
        ├── jenkins.yaml
        ├── harbor.yaml
        ├── nexus.yaml
        ├── minio.yaml
        ├── openldap.yaml
        ├── sonarqube.yaml
        └── repository.yaml
```

### templates/ 안의 각 파일(하나의 ArgoCD Application)

`templates/loki-stack.yaml`을 예로 보자

```yaml
{{- if .Values.loki.enabled }}        # values에서 enabled: true일 때만 생성
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: loki
  namespace: trb-oss
spec:
  destination:
    namespace: {{ .Values.application.destination.namespace }}  # trb-mgm
    server: {{ .Values.application.destination.server }}
  project: {{ .Values.application.project }}
  source:
    helm:
      valueFiles:
        {{- range .Values.application.helm.valuesFiles }}
        - {{ . | quote }}              # "values-dev.yaml"
        {{- end }}
    path: {{ .Values.loki.helmPath }}  # helm-charts/loki-stack ← 실제 차트 위치
    repoURL: {{ .Values.repository.url }}
    targetRevision: {{ .Values.repository.branch }}
  syncPolicy:
    {{- .Values.application.syncPolicy | toYaml | nindent 4 }}
{{- end }}
```

- 이 템플릿이 렌더링되면 `loki`라는 이름의 ArgoCD Application이 생성되고, 그 Application이 `helm-charts/loki-stack/` 경로의 Helm 차트를 실제로 배포한다.

### values-dev.yaml(환경별 제어)

`charts/trb-mgm/values-dev.yaml`이 환경별 설정의 핵심이다:

```yaml
# 공통 설정 (모든 자식 Application이 공유)
application:
  helm:
    valuesFiles:
      - values-dev.yaml       # 각 helm-charts/*/values-dev.yaml을 사용
  destination:
    namespace: trb-mgm
    server: https://kubernetes.default.svc
  project: default
  syncPolicy:
    automated:
      prune: true              # Git에서 삭제하면 클러스터에서도 삭제
      selfHeal: true           # 수동 변경을 되돌림
    syncOptions:
    - ServerSideApply=true

repository:
  url: https://bitbucket.org/okestrolab/tps_manifest.git
  branch: main

# 서비스별 활성화/비활성화
loki:
  enabled: true                # true → loki Application 생성
  helmPath: helm-charts/loki-stack

prometheus:
  enabled: true
  helmPath: helm-charts/kube-prometheus-stack
```

- 새 서비스를 추가하려면 여기에 블록을 추가하고, `templates/`에 대응하는 yaml을 만들면 된다. 
- `enabled: false`로 바꾸면 해당 서비스의 ArgoCD Application이 삭제되고, `prune: true` 덕분에 클러스터의 실제 리소스도 함께 정리된다.

### syncPolicy 용어 설명

ArgoCD UI에서 Sync 버튼을 누르면 Git 상태를 클러스터에 반영하는데, `syncPolicy`는 이 동작을 자동화하고 세부 동작을 제어하는 설정이다.

| 설정                   | 의미                                                         | UI에서의 동작                                                |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `automated`            | Sync 버튼을 누르지 않아도 Git 변경 감지 시 자동으로 동기화   | UI에서 "Auto-Sync" 뱃지가 표시됨                             |
| `prune: true`          | Git에서 리소스를 삭제하면 클러스터에서도 해당 리소스를 삭제  | false면 Git에서 지워도 클러스터에 남아있어 "고아 리소스"가 생김 |
| `selfHeal: true`       | 누군가 `kubectl edit`으로 클러스터를 직접 수정해도, ArgoCD가 Git 상태로 되돌림 | UI에서 수동 변경 후 잠시 뒤 원래대로 돌아가는 이유가 이것    |
| `Validate=false`       | Helm 렌더링 결과의 K8s 스키마 검증을 건너뜀                  | CRD 등 커스텀 리소스가 있을 때 검증 오류를 방지              |
| `CreateNamespace=true` | 대상 네임스페이스가 없으면 자동 생성                         | 네임스페이스를 미리 만들지 않아도 됨                         |
| `ServerSideApply=true` | `kubectl apply`를 서버 사이드로 실행                         | 대규모 리소스(CRD 등)에서 annotation 크기 제한 문제를 방지   |



# helm-charts/폴더 분석 (어떻게 배포할지?)

---

> 이 폴더에는 실제 K8s 리소스를 생성하는 Helm 차트가 들어있다. argocd-apps가 "무엇을"이라면, helm-charts는 "어떻게"에 해당한다.

```bash
helm-charts/
├── alloy/                      ← Grafana Alloy (로그 수집)
├── kube-prometheus-stack/      ← Prometheus + Grafana + AlertManager
├── loki-stack/                 ← Loki + (Promtail)
├── jenkins/                    ← CI/CD
├── gitlab/                     ← 소스 관리
├── harbor/                     ← 컨테이너 레지스트리
├── nexus/                      ← 아티팩트 저장소
├── minio/                      ← 오브젝트 스토리지
├── sonarqube/                  ← 코드 품질
├── tps-helm/                   ← TPS 애플리케이션
└── ...                         ← 총 22개 차트
```

## 환경별 values 파일

각 차트 디렉토리 안에 환경별 values 파일이 있다:

```
helm-charts/alloy/
├── Chart.yaml
├── templates/
├── values.yaml          ← 기본값 (보통 upstream 원본)
├── values-dev.yaml      ← 개발 환경 오버라이드
└── values-op.yaml       ← 운영 환경 오버라이드
```

ArgoCD Application의 `source.helm.valueFiles`에 `values-dev.yaml`이 지정되어 있으므로, dev 환경에서는 `values.yaml` + `values-dev.yaml`이 병합되어 적용된다.

### argocd-apps와의 연결

argocd-apps의 템플릿에 있는 `path: {{ .Values.loki.helmPath }}`가 바로 이 폴더를 가리킨다. 예를 들어 `helmPath: helm-charts/loki-stack`이면, ArgoCD가 Git 레포에서 해당 경로의 Helm 차트를 꺼내 렌더링하여 클러스터에 적용한다.

## 전체 배포 흐름

### Git Push에서 클러스터 반영까지

```
개발자: Git push (tps_manifest 레포)
         │
         ▼
ArgoCD: 3분마다 Git 폴링 (또는 webhook)
         │
         ▼
루트 App (trb-mgm): argocd-apps/app-of-apps/charts/trb-mgm/ 렌더링
         │
         ├── templates/loki-stack.yaml  →  Application "loki" 생성/업데이트
         ├── templates/kube-prometheus-stack.yaml  →  Application "prometheus" 생성/업데이트
         └── templates/alloy.yaml  →  Application "alloy" 생성/업데이트
                                        │
                                        ▼
자식 App (alloy): helm-charts/alloy/ 렌더링
         │
         ▼
K8s 클러스터: DaemonSet, ConfigMap, ServiceAccount 등 생성
```

### 왜 kubectl 직접 적용이 아닌 Git Push 방식인가

이 환경은 **GitOps**로 관리된다. `kubectl apply`로 직접 리소스를 생성하면, ArgoCD의 `selfHeal: true` 설정 때문에 다음 sync 때 Git 상태로 되돌려버린다. 이것은 의도된 동작이다.

모든 변경은 반드시 Git을 통해야 하는데, 그 이유는 다음과 같다:

1. **변경 이력**: 누가 언제 무엇을 바꿨는지 Git 커밋으로 추적 가능
2. **코드 리뷰**: PR을 통해 인프라 변경도 코드 리뷰 가능
3. **롤백**: 문제 발생 시 Git revert로 즉시 이전 상태 복구
4. **일관성**: 클러스터 상태와 Git 상태가 항상 일치 (drift 방지)

### 트리 구조 전체 요약

```
tps_manifest/
│
├── argocd-apps/                             "무엇을 배포할지"
│   └── app-of-apps/
│       ├── dev/
│       │   ├── trb-mgm-application.yaml     루트 App (ArgoCD에 수동 등록)
│       │   ├── trb-oss-application.yaml     루트 App
│       │   └── trb-app-application.yaml     루트 App
│       └── charts/
│           ├── trb-mgm/                     모니터링 (Loki, Prometheus, Alloy)
│           │   ├── Chart.yaml
│           │   ├── values-dev.yaml          서비스 활성화/비활성화 + 공통 설정
│           │   └── templates/
│           │       ├── loki-stack.yaml       → helm-charts/loki-stack/
│           │       ├── kube-prometheus-stack.yaml → helm-charts/kube-prometheus-stack/
│           │       └── alloy.yaml           → helm-charts/alloy/ (신규)
│           └── trb-oss/                     OSS 도구 (Jenkins, GitLab, Harbor...)
│               ├── values-dev.yaml
│               └── templates/
│                   ├── jenkins.yaml         → helm-charts/jenkins/
│                   ├── gitlab.yaml          → helm-charts/gitlab/
│                   └── ...
│
└── helm-charts/                             "어떻게 배포할지"
    ├── alloy/                               Alloy DaemonSet + ConfigMap
    │   ├── values-dev.yaml
    │   └── values-op.yaml
    ├── loki-stack/                          Loki + Grafana
    │   └── values-dev.yaml                  (promtail.enabled: false)
    ├── kube-prometheus-stack/               Prometheus + AlertManager
    ├── jenkins/
    └── ...                                  총 22개 차트
```



