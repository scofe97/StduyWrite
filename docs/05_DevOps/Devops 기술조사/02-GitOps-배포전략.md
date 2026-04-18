
# GitOps 및 배포 전략

> 작성일: 2025-01-14
> 목적: GitOps 개념, 도구 비교, Kubernetes 배포 전략 정리

---

## 1. GitOps란?

GitOps는 Git을 단일 진실의 원천(Single Source of Truth)으로 사용하여 인프라와 애플리케이션을 관리하는 방법론입니다.

### 핵심 원칙

| 원칙 | 설명 |
|-----|------|
| **Declarative** | 시스템 상태를 선언적으로 정의 |
| **Versioned & Immutable** | 모든 변경 사항을 Git에 기록 |
| **Pulled Automatically** | 변경 사항을 자동으로 클러스터에 적용 |
| **Continuously Reconciled** | 실제 상태와 원하는 상태를 지속적으로 동기화 |

### Push vs Pull 기반 배포

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Push 기반 (전통적인 CI/CD)                         │
├─────────────────────────────────────────────────────────────────────┤
│  Developer → Git → CI Server → Build → Push → Deploy to Cluster    │
│                                                                     │
│  * CI 서버가 클러스터에 직접 접근 필요                                  │
│  * 클러스터 자격 증명이 CI에 노출                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    Pull 기반 (GitOps)                               │
├─────────────────────────────────────────────────────────────────────┤
│  Developer → Git ← GitOps Controller (ArgoCD/Flux) ← Cluster       │
│                                                                     │
│  * 클러스터 내부에서 Git 저장소를 모니터링                              │
│  * 자격 증명이 클러스터 내부에만 존재                                   │
│  * 더 안전하고 감사 추적 용이                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. GitOps 도구 비교

### 2.1 ArgoCD vs FluxCD (2025)

| 기준 | ArgoCD | FluxCD |
|-----|--------|--------|
| **채택률** | ~60% (CNCF 조사) | 감소 추세 |
| **UI** | 강력한 웹 UI | CLI 중심 (UI 선택적) |
| **아키텍처** | Application 중심 | GitRepository/Kustomization 중심 |
| **리소스 사용** | 상대적으로 무거움 | 경량 |
| **멀티테넌시** | ApplicationSet 활용 | 네이티브 지원 |
| **Helm 지원** | 네이티브 | HelmRelease CRD |
| **상용 지원** | 활발 (Akuity 등) | Weaveworks 폐업(2024) 이후 약화 |

### 2.2 도구 선택 가이드

```
어떤 GitOps 도구를 선택할까?

┌─────────────────────────────────────────────────────┐
│ 시각적 관리 & 앱 중심 워크플로우 중요?              │
│ ├── Yes → ArgoCD                                   │
│ └── No                                             │
│     ├── 경량 솔루션 필요? (엣지/IoT)               │
│     │   └── Yes → FluxCD                           │
│     ├── 플랫폼 엔지니어링 중심?                    │
│     │   └── Yes → FluxCD                           │
│     └── 팀이 GitOps 처음?                          │
│         └── Yes → ArgoCD (학습 곡선 낮음)          │
└─────────────────────────────────────────────────────┘
```

### 2.3 ArgoCD 주요 기능

```yaml
# ArgoCD Application 예시
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true      # 삭제된 리소스 자동 정리
      selfHeal: true   # 드리프트 자동 복구
    syncOptions:
      - CreateNamespace=true
```

### 2.4 FluxCD 주요 기능

```yaml
# Flux GitRepository 예시
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/repo.git
  ref:
    branch: main

---
# Flux Kustomization 예시
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 10m
  path: ./k8s/overlays/production
  sourceRef:
    kind: GitRepository
    name: my-repo
  prune: true
  healthChecks:
    - kind: Deployment
      name: my-app
      namespace: default
```

---

## 3. Kubernetes 매니페스트 관리

### 3.1 Helm vs Kustomize

| 기준 | Helm | Kustomize |
|-----|------|-----------|
| **접근 방식** | 템플릿 기반 | 패치/오버레이 기반 |
| **패키징** | Chart (버전 관리) | 디렉토리 구조 |
| **재사용성** | 높음 (퍼블릭 차트) | 중간 |
| **복잡도** | 높음 (Go 템플릿) | 낮음 (YAML 패치) |
| **롤백** | 네이티브 지원 | Git 기반 |
| **kubectl 통합** | 별도 설치 | 네이티브 (`kubectl -k`) |

### 3.2 Helm + Kustomize 조합 사용

```
권장되는 하이브리드 접근법:

1. 외부/공용 Helm 차트 사용
2. helm template으로 렌더링
3. Kustomize 오버레이로 환경별 커스터마이징
```

**디렉토리 구조**:
```
k8s/
├── base/
│   ├── kustomization.yaml
│   └── helm-rendered.yaml  # helm template으로 생성
├── overlays/
│   ├── development/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   │       └── replica-count.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   └── production/
│       ├── kustomization.yaml
│       └── patches/
│           ├── replica-count.yaml
│           └── resource-limits.yaml
```

### 3.3 Kustomize 오버레이 예시

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

---
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namePrefix: prod-
commonLabels:
  environment: production
patches:
  - path: patches/replica-count.yaml
  - path: patches/resource-limits.yaml
configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=info
      - DEBUG=false

---
# overlays/production/patches/replica-count.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 5
```

---

## 4. 배포 전략

### 4.1 Rolling Update (기본)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 최대 1개 추가 Pod 허용
      maxUnavailable: 0  # 가용 Pod 수 유지
```

**장점**: 리소스 효율적, 무중단
**단점**: 롤백 시간 소요

### 4.2 Blue-Green Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                     Blue-Green 배포                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐         ┌─────────────┐                       │
│  │  Blue (v1)  │   ←──   │  Service    │                       │
│  │  (Current)  │         │  (Router)   │                       │
│  └─────────────┘         └─────────────┘                       │
│                                                                 │
│  ┌─────────────┐                                               │
│  │ Green (v2)  │  ← 테스트 후 트래픽 전환                        │
│  │   (New)     │                                               │
│  └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**구현 방법**:
- Service의 selector를 변경
- Ingress의 backend 변경
- Istio/Linkerd의 트래픽 시프팅

### 4.3 Canary Deployment

```yaml
# Argo Rollouts Canary 예시
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 10    # 10% 트래픽을 새 버전으로
        - pause: {duration: 5m}
        - setWeight: 30
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 100
      canaryService: my-app-canary
      stableService: my-app-stable
      trafficRouting:
        istio:
          virtualService:
            name: my-app-vsvc
```

### 4.4 배포 전략 비교

| 전략 | 롤백 속도 | 리소스 | 위험도 | 복잡도 |
|-----|----------|--------|--------|--------|
| **Rolling** | 느림 | 낮음 | 중간 | 낮음 |
| **Blue-Green** | 즉시 | 2배 | 낮음 | 중간 |
| **Canary** | 즉시 | 약간 증가 | 매우 낮음 | 높음 |

---

## 5. Progressive Delivery 도구

### 5.1 Argo Rollouts

ArgoCD와 함께 사용하는 Progressive Delivery 컨트롤러:

- Canary/Blue-Green 배포 자동화
- 메트릭 기반 자동 프로모션/롤백
- Istio, Nginx, AWS ALB 등 트래픽 관리 통합

### 5.2 Flagger

Flux와 함께 사용하는 Progressive Delivery 도구:

- Canary, A/B, Blue-Green 지원
- Prometheus 메트릭 기반 분석
- Slack, MS Teams 알림 통합

---

## 6. 환경 관리 전략

### 6.1 저장소 구조 패턴

**패턴 1: 단일 저장소 (권장)**
```
gitops-repo/
├── apps/
│   ├── app-a/
│   │   ├── base/
│   │   └── overlays/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── app-b/
│       └── ...
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── monitoring/
└── clusters/
    ├── dev-cluster/
    ├── staging-cluster/
    └── prod-cluster/
```

**패턴 2: 멀티 저장소**
```
app-a-repo/          # 애플리케이션 코드
app-a-gitops-repo/   # 배포 매니페스트
infrastructure-repo/ # 인프라 구성
```

### 6.2 환경별 승인 프로세스

```yaml
# ArgoCD Sync Window 예시
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: production
spec:
  syncWindows:
    - kind: allow
      schedule: '0 10 * * 1-5'  # 평일 10시에만 배포 허용
      duration: 2h
      applications:
        - '*'
    - kind: deny
      schedule: '0 0 * * *'
      duration: 24h
      manualSync: false
      applications:
        - critical-app
```

---

## 7. 참고 자료

- [GitOps in 2025 (CNCF)](https://www.cncf.io/blog/2025/06/09/gitops-in-2025-from-old-school-updates-to-the-modern-way/)
- [ArgoCD vs FluxCD in 2025 (DEV Community)](https://dev.to/inboryn_99399f96579fcd705/argocd-vs-fluxcd-in-2025-the-weaveworks-shutdown-changed-everything-which-gitops-tool-to-choose-872)
- [Flux vs Argo CD (Northflank)](https://northflank.com/blog/flux-vs-argo-cd)
- [Google GKE GitOps Best Practices](https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/concepts/gitops-best-practices)
- [Kustomize vs Helm (Spacelift)](https://spacelift.io/blog/kustomize-vs-helm)
- [Using Helm Chart with Kustomize (LinkedIn)](https://www.linkedin.com/pulse/using-helm-chart-kustomize-managing-multiple-microservices)
