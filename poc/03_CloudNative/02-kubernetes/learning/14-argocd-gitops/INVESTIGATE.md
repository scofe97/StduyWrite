# Ch14. ArgoCD와 GitOps - 점검 질문

## Q1: GitOps의 Push 모델(Jenkins)과 Pull 모델(ArgoCD) 차이

**질문**: Jenkins 기반 CD 파이프라인과 ArgoCD의 근본적인 차이는 무엇이며, 각각 어떤 상황에 적합한가?

**핵심 포인트**:

- **Push 모델(Jenkins)**은 CI/CD 파이프라인이 클러스터 외부에서 `kubectl apply`를 실행한다. 파이프라인이 클러스터에 접근하려면 kubeconfig나 서비스 어카운트 토큰이 필요하며, 이는 보안 위험이다. Jenkins가 해킹당하면 클러스터 전체가 노출될 수 있다. 또한 클러스터 상태가 Git과 불일치(Drift)해도 자동 감지하지 못한다.

- **Pull 모델(ArgoCD)**은 클러스터 내부에서 실행되는 ArgoCD가 Git 저장소를 주기적으로 폴링한다. 클러스터 자격증명이 외부로 나가지 않으므로 보안 경계가 명확하다. ArgoCD는 Git 상태와 클러스터 상태를 지속적으로 비교하여 Drift를 자동 감지하고, Self-Heal 옵션으로 자동 복구할 수 있다.

- **감사 추적(Audit Trail)** 측면에서 Pull 모델이 우수하다. Push 모델은 누가 배포했는지 알려면 CI 로그를 뒤져야 하지만, Pull 모델은 Git 커밋 히스토리가 곧 배포 히스토리다. `git log`만으로 모든 변경사항을 추적할 수 있다.

- **롤백** 시나리오에서 Push 모델은 이전 파이프라인을 다시 실행하거나 별도의 롤백 스크립트가 필요하다. Pull 모델은 `git revert` 후 ArgoCD가 자동으로 이전 상태를 적용한다.

- **적합한 상황**: Push 모델은 레거시 시스템 통합, Kubernetes 외 환경(VM, 온프레미스), 복잡한 승인 워크플로우가 있는 경우 유리하다. Pull 모델은 클라우드 네이티브 환경, 멀티 클러스터 관리, 보안 컴플라이언스가 중요한 경우 적합하다.

**심화 질문**: 하이브리드 모델(Jenkins로 빌드 + ArgoCD로 배포)을 구성할 때, Jenkins는 어디까지 담당하고 ArgoCD는 어디서부터 개입해야 하는가? 이미지 태그 업데이트는 누가 하는가?

---

## Q2: ArgoCD의 Sync 상태(Synced, OutOfSync, Unknown) 의미

**질문**: ArgoCD Application의 Sync 상태는 무엇을 의미하며, 각 상태에서 어떤 조치를 취해야 하는가?

**핵심 포인트**:

- **Synced**: Git 저장소의 매니페스트와 클러스터의 실제 리소스가 일치하는 상태다. ArgoCD가 계산한 "desired state"와 Kubernetes API가 반환한 "live state"의 해시값이 같다. 이 상태에서는 특별한 조치가 필요 없으며, 정상 운영 중이다.

- **OutOfSync**: Git과 클러스터가 불일치하는 상태다. 원인은 크게 두 가지다. (1) Git에 새로운 커밋이 있지만 아직 클러스터에 적용되지 않음 (Automated Sync가 비활성화된 경우). (2) 누군가 `kubectl edit`, `kubectl scale` 등으로 클러스터를 직접 수정함 (Drift). OutOfSync 상태에서는 "Diff" 버튼으로 정확히 무엇이 다른지 확인한 후, Manual Sync 또는 SelfHeal로 복구한다.

- **Unknown**: ArgoCD가 클러스터 상태를 확인할 수 없는 상태다. 원인은 (1) Git 저장소 접근 실패 (인증 오류, 네트워크 문제), (2) Kubernetes API 서버 접근 실패 (클러스터 다운, RBAC 권한 부족), (3) 매니페스트 파싱 오류 (잘못된 YAML, Helm 렌더링 실패). 이 상태에서는 ArgoCD 로그(`kubectl logs -n argocd argocd-application-controller`)를 확인하여 근본 원인을 파악해야 한다.

- **Health 상태**는 별개다. Synced라도 Pod가 CrashLoopBackOff면 Unhealthy다. Sync 상태는 "Git과 일치 여부"를 나타내고, Health 상태는 "리소스가 정상 작동 여부"를 나타낸다.

**심화 질문**: OutOfSync 상태가 1시간 이상 지속되면 AlertManager로 알림을 보내도록 PrometheusRule을 작성하려면 어떤 메트릭을 사용해야 하는가?

---

## Q3: Self-Heal과 Prune 옵션의 동작과 위험성

**질문**: `selfHeal: true`와 `prune: true`는 무엇을 자동화하며, 어떤 상황에서 예상치 못한 문제를 일으킬 수 있는가?

**핵심 포인트**:

- **Self-Heal 동작**: 클러스터의 리소스가 Git과 다르면 자동으로 Git 상태로 복구한다. ArgoCD는 3초마다 Application을 Reconcile하며, Drift를 감지하면 즉시 `kubectl apply`로 원래대로 되돌린다. 예를 들어 관리자가 `kubectl scale deployment nginx --replicas=10`을 실행해도, Git에 `replicas: 3`으로 정의되어 있으면 5초 안에 다시 3개로 줄어든다.

- **HPA 충돌 문제**: HPA(Horizontal Pod Autoscaler)는 CPU/메모리 사용률에 따라 replicas를 동적으로 변경한다. Self-Heal이 활성화되면 HPA가 replicas를 5로 늘려도 ArgoCD가 다시 3으로 되돌린다. 이는 무한 루프를 만든다. 해결책은 `ignoreDifferences`로 replicas 필드를 무시하거나, HPA를 사용하는 Deployment는 Git에서 replicas를 명시하지 않는 것이다.

- **Prune 동작**: Git에서 삭제된 리소스를 클러스터에서도 자동으로 삭제한다. `deployment.yaml` 파일을 Git에서 삭제하고 푸시하면, ArgoCD가 클러스터의 Deployment도 `kubectl delete`로 제거한다. 이는 Git이 진실의 원천이라는 GitOps 원칙을 따른 것이다.

- **Prune 위험성**: 실수로 파일을 삭제하거나 Git 브랜치를 잘못 지정하면 프로덕션 리소스가 즉시 삭제된다. 예를 들어 `targetRevision: main`인 Application에서 실수로 `main` 브랜치를 삭제하면, ArgoCD가 모든 리소스를 삭제할 수 있다. 또한 `prune: true`는 Application 범위 밖의 리소스는 삭제하지 않으므로, 수동으로 생성한 ConfigMap이 남아 있을 수 있다.

- **프로덕션 권장 설정**: `selfHeal: false`, `prune: false`, Manual Sync. 변경사항을 먼저 Diff로 확인한 후 수동으로 Sync 버튼을 클릭한다. 개발 환경에서는 `selfHeal: true`, `prune: true`로 빠른 피드백을 얻는다.

**심화 질문**: StatefulSet에 연결된 PVC(PersistentVolumeClaim)는 Prune 대상인가? ArgoCD가 StatefulSet을 삭제할 때 PVC도 함께 삭제하는가, 아니면 남겨두는가?

---

## Q4: ArgoCD Application CR에서 source와 destination 설정 방법

**질문**: Application CR의 `source`와 `destination` 필드는 어떻게 구성하며, 멀티 클러스터 환경에서는 어떻게 변경되는가?

**핵심 포인트**:

- **source 필드**는 Git 저장소 정보를 정의한다. `repoURL`은 HTTPS 또는 SSH 형식의 Git URL이고, `targetRevision`은 브랜치, 태그, 커밋 해시를 지정한다. `HEAD`를 사용하면 기본 브랜치를 따라간다. `path`는 저장소 내 매니페스트가 있는 디렉토리 경로다 (예: `manifests/production`).

- **Helm 차트**를 사용할 때는 `path` 대신 `chart` 필드를 사용한다. `chart: nginx`, `repoURL: https://charts.bitnami.com/bitnami`, `targetRevision: 15.4.0`처럼 차트 이름과 버전을 지정한다. `helm.values`로 values.yaml 내용을 인라인으로 정의하거나, `helm.valueFiles: [values-prod.yaml]`로 저장소 내 파일을 참조할 수 있다.

- **destination 필드**는 배포 대상 클러스터와 네임스페이스를 정의한다. `server: https://kubernetes.default.svc`는 ArgoCD가 실행 중인 클러스터 자신을 가리킨다. `namespace: default`는 리소스가 생성될 네임스페이스다. `syncOptions`에서 `CreateNamespace=true`를 설정하면 네임스페이스가 없을 때 자동 생성한다.

- **멀티 클러스터 환경**에서는 ArgoCD에 외부 클러스터를 등록한 후, `destination.server`에 해당 클러스터 URL을 지정한다. 예를 들어 `argocd cluster add gke-prod-context` 명령으로 GKE 클러스터를 등록하면, `server: https://35.123.45.67`처럼 API 서버 주소를 사용한다. 또는 `destination.name: gke-prod`처럼 클러스터 이름으로도 지정 가능하다.

- **보안 고려사항**: Private Git 저장소는 SSH 키나 Personal Access Token으로 인증한다. ArgoCD 웹 UI의 Settings → Repositories에서 저장소를 추가하고, SSH 키를 Secret으로 저장한다. Helm 차트 저장소도 마찬가지로 username/password를 Secret에 저장한다.

**심화 질문**: Git 저장소가 Monorepo 구조일 때 (하나의 저장소에 여러 마이크로서비스), 각 서비스별로 Application을 만들려면 `path`를 어떻게 설정해야 하는가? 디렉토리 변경 감지는 어떻게 동작하는가?

---

## Q5: App of Apps 패턴이 필요한 시나리오

**질문**: 어떤 상황에서 App of Apps 패턴을 사용하며, 대안(ApplicationSet)과 비교했을 때 장단점은 무엇인가?

**핵심 포인트**:

- **시나리오 1: 환경별 배포**. 개발, 스테이징, 프로덕션 환경에 동일한 애플리케이션을 배포하되, 각각 다른 네임스페이스와 설정을 사용한다. Root Application이 `environments/` 디렉토리의 `dev-app.yaml`, `staging-app.yaml`, `prod-app.yaml`을 관리한다. 새 환경 추가 시 YAML 파일 하나만 추가하면 된다.

- **시나리오 2: 마이크로서비스 관리**. 수십 개의 마이크로서비스가 있고, 각각 독립적인 Git 저장소와 배포 주기를 가진다. Root Application이 `apps/` 디렉토리의 모든 Application CR을 관리하며, 서비스 추가 시 `apps/new-service.yaml`을 커밋하면 자동으로 배포된다.

- **시나리오 3: 인프라 부트스트래핑**. 새 클러스터를 구성할 때 Ingress Controller, Cert-Manager, Prometheus, ArgoCD 자체를 순서대로 배포해야 한다. Root Application이 Sync Waves를 사용하여 인프라 컴포넌트를 올바른 순서로 설치한다.

- **ApplicationSet 비교**: ApplicationSet은 템플릿 기반으로 여러 Application을 생성한다. Git 디렉토리 구조(`git.directories` generator)나 클러스터 목록(`cluster` generator)을 기반으로 동적 생성이 가능하다. App of Apps는 명시적 YAML 파일이 필요하지만, ApplicationSet은 패턴 매칭으로 자동 생성한다. 예를 들어 `apps/**/config.yaml`이 있는 모든 디렉토리마다 Application을 생성할 수 있다.

- **App of Apps 장점**: 간단하고 직관적이다. 각 Application의 설정을 명시적으로 볼 수 있으며, PR 리뷰 시 변경사항이 명확하다. **단점**: Application 수가 많으면 YAML 중복이 많고, 일괄 변경이 어렵다 (예: 모든 Application의 syncPolicy 변경).

- **ApplicationSet 장점**: 템플릿으로 수백 개의 Application을 관리할 수 있으며, 새 디렉토리/클러스터 추가 시 자동 생성된다. **단점**: 학습 곡선이 높고, 디버깅이 어렵다. 템플릿 문법 오류 시 모든 Application이 영향받는다.

**심화 질문**: App of Apps 패턴에서 Root Application이 삭제되면 모든 Child Application도 삭제되는가? 또는 독립적으로 유지되는가? Finalizer를 사용하여 Cascade 삭제를 제어할 수 있는가?

---

## Q6: ArgoCD vs Flux CD 비교

**질문**: Kubernetes GitOps 도구로 ArgoCD와 Flux CD 중 무엇을 선택해야 하며, 결정 기준은 무엇인가?

**핵심 포인트**:

- **아키텍처 차이**: ArgoCD는 중앙 집중식 컨트롤러와 웹 UI를 제공한다. 모든 Application은 ArgoCD 네임스페이스에서 관리되며, 단일 대시보드에서 전체 클러스터 상태를 볼 수 있다. Flux CD는 분산형 접근 방식으로, 각 네임스페이스에 Kustomization/HelmRelease CR을 배포하며, 중앙 UI가 없다 (Weave GitOps 별도 설치 필요).

- **사용자 경험**: ArgoCD는 웹 UI가 강력하다. Diff 뷰, 리소스 트리 시각화, 실시간 로그, 수동 Sync 버튼 등 GUI 중심 워크플로우를 제공한다. Flux CD는 CLI 중심이며, `flux get kustomizations`, `flux reconcile`으로 상태를 확인한다. UI를 원하면 Weave GitOps를 설치해야 하지만 ArgoCD보다 기능이 제한적이다.

- **멀티 테넌시**: ArgoCD는 AppProject로 팀별 권한 분리가 가능하다. RBAC으로 특정 팀은 `team-a` 네임스페이스만 배포하도록 제한할 수 있다. Flux CD는 네임스페이스 단위로 격리되므로, 각 팀이 자신의 네임스페이스에서 독립적으로 Flux를 운영한다.

- **Helm 지원**: 둘 다 Helm을 지원하지만 방식이 다르다. ArgoCD는 `helm template`으로 차트를 렌더링한 후 YAML을 kubectl apply한다 (Helm Release 객체 없음). Flux CD는 HelmRelease CR과 Helm Controller를 사용하여 실제 Helm 릴리스를 생성한다 (`helm list`에 나타남). Helm hooks, 롤백 기능을 사용하려면 Flux가 유리하다.

- **이미지 자동 업데이트**: Flux CD는 Image Automation Controller로 컨테이너 레지스트리의 새 이미지를 감지하여 Git에 자동 커밋할 수 있다. ArgoCD는 이 기능이 없으며, 외부 도구(ArgoCD Image Updater 플러그인)가 필요하다.

- **커뮤니티와 생태계**: ArgoCD는 CNCF Graduated 프로젝트로, 더 큰 커뮤니티와 많은 기업 도입 사례를 가진다. Flux CD는 CNCF Incubating이며, Weaveworks가 주도했지만 2024년 회사가 폐업하여 커뮤니티 주도로 전환 중이다.

**심화 질문**: 두 도구를 함께 사용하는 하이브리드 접근 방식이 가능한가? 예를 들어 ArgoCD로 인프라 컴포넌트를 관리하고 Flux로 애플리케이션을 배포한다면 어떤 장단점이 있는가?

---

## Q7: ArgoCD RBAC과 SSO 통합 방법

**질문**: ArgoCD에서 팀별로 접근 권한을 분리하고, 회사 IdP(GitHub, Google)로 SSO를 구성하는 방법은?

**핵심 포인트**:

- **RBAC 구조**: ArgoCD는 두 가지 RBAC 개념을 사용한다. (1) **AppProject**: 어떤 Git 저장소, 클러스터, 네임스페이스를 사용할 수 있는지 정의한다. (2) **RBAC Policy**: 어떤 사용자가 어떤 AppProject에 어떤 작업(get, create, sync, delete)을 할 수 있는지 정의한다.

- **AppProject 예시**: 팀 A는 `team-a` 네임스페이스에만 배포할 수 있다.
  ```yaml
  apiVersion: argoproj.io/v1alpha1
  kind: AppProject
  metadata:
    name: team-a-project
  spec:
    destinations:
    - namespace: team-a
      server: https://kubernetes.default.svc
    sourceRepos:
    - https://github.com/company/team-a-apps.git
  ```

- **RBAC Policy 예시**: `team-a-developers` 그룹은 `team-a-project`의 Application을 get, sync할 수 있지만 delete는 불가.
  ```csv
  p, role:team-a-dev, applications, get, team-a-project/*, allow
  p, role:team-a-dev, applications, sync, team-a-project/*, allow
  g, team-a-developers, role:team-a-dev
  ```

- **SSO 통합 (GitHub 예시)**: Dex를 사용하여 GitHub OAuth를 구성한다. `argocd-cm` ConfigMap에 GitHub OAuth App 정보를 추가한다.
  ```yaml
  data:
    dex.config: |
      connectors:
      - type: github
        id: github
        name: GitHub
        config:
          clientID: $GITHUB_CLIENT_ID
          clientSecret: $GITHUB_CLIENT_SECRET
          orgs:
          - name: your-org
  ```

  GitHub Organization의 팀(`your-org:team-a`)이 ArgoCD 그룹으로 매핑된다. `g, your-org:team-a, role:team-a-dev`로 RBAC에 연결한다.

- **Google SSO**: Google Workspace를 사용한다면 OIDC 연동이 가능하다. Google Cloud Console에서 OAuth 2.0 클라이언트 생성 후, Dex에 OIDC 커넥터를 추가한다. 사용자의 이메일 도메인(`@company.com`)으로 자동 그룹 할당도 가능하다.

- **로컬 사용자**: SSO 외에도 `argocd account` 명령으로 로컬 사용자를 생성할 수 있다. CI/CD 파이프라인용 서비스 어카운트는 로컬 사용자로 만들고 API 토큰을 발급한다.

**심화 질문**: AppProject에서 `clusterResourceWhitelist`를 사용하여 특정 팀이 Namespace, ClusterRole 같은 클러스터 레벨 리소스를 생성하지 못하도록 제한하는 방법은?

---

## Q8: Sync Waves를 사용한 배포 순서 제어 예시

**질문**: 복잡한 애플리케이션 스택 (DB → Backend → Frontend)을 배포할 때 Sync Waves를 어떻게 설계해야 하는가?

**핵심 포인트**:

- **기본 전략**: Wave 번호를 논리적 레이어로 나눈다. 인프라(0) → 데이터(1) → 백엔드(2) → 프론트엔드(3) → 헬스체크(4). 음수 Wave는 Namespace, RBAC 같은 사전 준비에 사용한다.

- **Wave -1: Namespace와 RBAC**
  ```yaml
  apiVersion: v1
  kind: Namespace
  metadata:
    name: myapp
    annotations:
      argocd.argoproj.io/sync-wave: "-1"
  ---
  apiVersion: v1
  kind: ServiceAccount
  metadata:
    name: myapp-sa
    annotations:
      argocd.argoproj.io/sync-wave: "-1"
  ```

- **Wave 0: ConfigMap, Secret, PVC**
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: app-config
    annotations:
      argocd.argoproj.io/sync-wave: "0"
  ---
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: postgres-pvc
    annotations:
      argocd.argoproj.io/sync-wave: "0"
  ```

- **Wave 1: 데이터베이스**
  ```yaml
  apiVersion: apps/v1
  kind: StatefulSet
  metadata:
    name: postgres
    annotations:
      argocd.argoproj.io/sync-wave: "1"
  ```

  StatefulSet이 Ready 상태가 될 때까지 Wave 2가 시작되지 않는다. ArgoCD는 Pod의 `status.conditions`를 체크한다.

- **Wave 2: 백엔드 + DB 마이그레이션 (PostSync Hook)**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: backend
    annotations:
      argocd.argoproj.io/sync-wave: "2"
  ---
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: db-migration
    annotations:
      argocd.argoproj.io/hook: PostSync
      argocd.argoproj.io/sync-wave: "2"
      argocd.argoproj.io/hook-delete-policy: HookSucceeded
  ```

  백엔드 Deployment가 생성된 후, PostSync Hook으로 DB 마이그레이션 Job이 실행된다. Job이 성공하면 자동 삭제된다.

- **Wave 3: 프론트엔드와 Ingress**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: frontend
    annotations:
      argocd.argoproj.io/sync-wave: "3"
  ---
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: myapp-ingress
    annotations:
      argocd.argoproj.io/sync-wave: "3"
  ```

- **Wave 10: 헬스체크 (PostSync Hook)**
  ```yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: healthcheck
    annotations:
      argocd.argoproj.io/hook: PostSync
      argocd.argoproj.io/sync-wave: "10"
      argocd.argoproj.io/hook-delete-policy: Always
  spec:
    template:
      spec:
        containers:
        - name: curl
          image: curlimages/curl
          command: ["curl", "-f", "http://frontend/health"]
        restartPolicy: Never
  ```

  모든 리소스가 배포된 후, 헬스체크 Job으로 엔드투엔드 테스트를 수행한다. 실패 시 전체 Sync가 실패로 표시된다.

**심화 질문**: Sync Wave 중간에 실패하면 어떻게 되는가? 이미 생성된 이전 Wave의 리소스는 롤백되는가, 아니면 그대로 남는가? Rollback을 자동화하려면 어떤 전략을 사용해야 하는가?


---

> **[이관 완료]** write/09_cloud/kubernetes/09-01.ArgoCD와 GitOps.md · deepdive/09-01.ArgoCD와 GitOps 점검.md (2026-04-19)
