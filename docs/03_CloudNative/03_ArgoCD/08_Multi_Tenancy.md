# 08. Multi-Tenancy

---

## 📌 핵심 요약

Argo CD의 멀티 테넌시는 단일 Argo CD 인스턴스로 여러 팀과 프로젝트를 안전하게 격리하고 관리하는 아키텍처입니다. AppProject CRD를 통해 소스 저장소 접근, 배포 대상 클러스터/네임스페이스, Kubernetes 리소스 유형, 사용자/그룹별 권한을 세분화하여 제어할 수 있습니다. Cluster Scoped와 Namespace Scoped 두 가지 설치 모드를 제공하며, 각 모드는 보안 격리 수준과 관리 편의성 간의 트레이드오프가 있습니다.

---

## 🎯 학습 목표

이 내용을 읽고 나면:
- [ ] Argo CD의 두 가지 설치 모드(Cluster/Namespace Scoped)의 차이와 선택 기준을 설명할 수 있다
- [ ] AppProject의 역할과 멀티 테넌시에서의 중요성을 이해할 수 있다
- [ ] sourceRepos, destinations를 통한 리소스 접근 제어를 구현할 수 있다
- [ ] 네임스페이스/클러스터 스코프 리소스 화이트리스트/블랙리스트를 설정할 수 있다
- [ ] Project 레벨 RBAC를 구성하여 팀별 세분화된 권한 관리를 수행할 수 있다

---

## 📖 본문 정리

### 1. 멀티 테넌시 개념

멀티 테넌시는 단일 소프트웨어 인스턴스가 여러 독립적인 그룹(테넌트)을 동시에 서비스하면서도 각 그룹의 데이터와 권한을 격리하는 아키텍처 패턴입니다. Argo CD에서 멀티 테넌시가 중요한 이유는 대규모 조직에서 여러 팀이 동일한 GitOps 플랫폼을 공유하면서도 서로의 배포 환경을 침범하지 않고, 각 팀이 필요한 리소스에만 접근할 수 있도록 보장해야 하기 때문입니다.

**Argo CD 멀티 테넌시의 3가지 핵심 제어 차원:**

Argo CD는 누가(Actor), 무엇을(Resource), 어떻게(Action) 할 수 있는지를 세분화하여 제어합니다. Actor는 사용자, 그룹, 서비스 계정을 포함하며, Resource는 Application, Project, Cluster, Repository 등 Argo CD가 관리하는 모든 객체를 의미합니다. Action은 get, create, update, delete, sync 등 리소스에 대해 수행할 수 있는 작업을 나타냅니다.

**멀티 테넌시 시나리오:**

실무에서는 백엔드팀이 production과 staging 네임스페이스만 접근 가능하고, 프론트엔드팀은 frontend-dev, frontend-staging 네임스페이스만 접근 가능하도록 설정합니다. 플랫폼팀은 monitoring, logging 등 인프라 네임스페이스를 관리하며, 각 팀은 자신의 Git 저장소에서만 배포할 수 있도록 제한됩니다. 이러한 격리는 실수로 다른 팀의 프로덕션 환경을 수정하거나 삭제하는 사고를 방지합니다.

```mermaid
sequenceDiagram
    participant User as 사용자(mary<br/>Developers 그룹)
    participant ArgoCD as Argo CD
    participant Project as AppProject<br/>(team-a)
    participant Cluster as Kubernetes

    User->>ArgoCD: Application Sync 요청<br/>(app: frontend)
    ArgoCD->>Project: 권한 확인 요청
    Project->>Project: 1. sourceRepos 검증<br/>(허용된 Git 저장소인가?)
    Project->>Project: 2. destinations 검증<br/>(허용된 클러스터/네임스페이스인가?)
    Project->>Project: 3. RBAC 검증<br/>(사용자가 sync 액션 권한 보유?)
    alt 모든 검증 통과
        Project-->>ArgoCD: 허용
        ArgoCD->>Cluster: Sync 실행
        Cluster-->>User: 성공
    else 검증 실패
        Project-->>ArgoCD: 거부
        ArgoCD-->>User: permission denied
    end
</sequenceDiagram>

AppProject는 Argo CD 멀티 테넌시의 핵심 경계점으로, 위 다이어그램처럼 모든 요청이 AppProject의 3단계 검증(소스, 대상, RBAC)을 통과해야만 실행됩니다.

---

### 2. Argo CD 설치 모드

Argo CD는 Cluster Scoped와 Namespace Scoped 두 가지 설치 모드를 제공하며, 각 모드는 보안 격리와 관리 편의성 간의 트레이드오프가 있습니다. 설치 모드 선택은 조직의 보안 요구사항, 팀 구조, 운영 복잡도를 고려하여 결정해야 합니다.

#### 2.1 Cluster Scoped (클러스터 스코프)

Cluster Scoped는 Argo CD가 전체 클러스터에 대한 cluster-admin 권한을 가지는 가장 일반적인 설치 방법입니다. 이 모드가 일반적인 이유는 중앙 집중식 GitOps 플랫폼으로 여러 클러스터를 통합 관리할 수 있으며, 단일 UI/API로 모든 환경을 제어할 수 있기 때문입니다. Hub-and-Spoke 아키텍처에서 Argo CD는 Hub 클러스터에 설치되어 여러 Spoke 클러스터(dev, staging, production)를 관리합니다.

**Cluster Scoped 요청 흐름:**

```mermaid
sequenceDiagram
    participant User as 사용자
    participant ArgoCD as Argo CD<br/>(cluster-admin)
    participant Local as 로컬 클러스터
    participant Remote1 as Cluster 1 (dev)
    participant Remote2 as Cluster 2 (prod)

    User->>ArgoCD: Application 배포 요청
    ArgoCD->>ArgoCD: AppProject 권한 검증
    alt 로컬 클러스터 배포
        ArgoCD->>Local: manifest 적용<br/>(전체 클러스터 접근)
        Local-->>User: 배포 완료
    else 원격 클러스터 배포
        ArgoCD->>Remote1: manifest 적용<br/>(등록된 클러스터)
        Remote1-->>User: 배포 완료
    end
</sequenceDiagram>

Cluster Scoped의 장점은 모든 클러스터를 단일 인터페이스로 관리할 수 있어 운영 효율이 높고, AppProject와 RBAC를 통해 충분한 멀티 테넌시를 구현할 수 있다는 점입니다. 단, 기본적으로 cluster-admin 권한을 가지므로 Argo CD 자체가 침해되면 전체 클러스터가 위험에 노출되는 보안 리스크가 있습니다. 따라서 Argo CD의 인증/인가를 강화하고, 불필요한 클러스터 리소스 접근은 AppProject로 제한해야 합니다.

#### 2.2 Namespace Scoped (네임스페이스 스코프)

Namespace Scoped는 Argo CD가 특정 네임스페이스에 대한 권한만 가지도록 제한하는 설치 방법입니다. 이 모드가 중요한 이유는 규제가 엄격한 환경(금융, 의료)에서 최소 권한 원칙을 준수하고, 팀 간 완전한 격리가 필요한 경우 각 팀이 독립적인 Argo CD 인스턴스를 운영할 수 있기 때문입니다.

**Namespace Scoped 요청 흐름:**

```mermaid
sequenceDiagram
    participant UserA as Team A 사용자
    participant ArgoCDA as Argo CD A<br/>(team-a 네임스페이스)
    participant NSA as team-a 네임스페이스
    participant NSB as team-b 네임스페이스

    UserA->>ArgoCDA: Application 배포 요청
    ArgoCDA->>ArgoCDA: AppProject 권한 검증
    alt team-a 네임스페이스 배포
        ArgoCDA->>NSA: manifest 적용<br/>(네임스페이스 권한만)
        NSA-->>UserA: 배포 완료
    else team-b 네임스페이스 배포 시도
        ArgoCDA->>NSB: manifest 적용 시도
        NSB-->>UserA: permission denied<br/>(네임스페이스 권한 없음)
    end
</sequenceDiagram>

Namespace Scoped의 장점은 Kubernetes의 네임스페이스 격리를 활용하여 팀 간 완전한 독립성을 보장하고, Argo CD 침해 시 피해 범위가 단일 네임스페이스로 제한된다는 점입니다. 단점은 각 팀이 독립적인 Argo CD 인스턴스를 운영해야 하므로 관리 오버헤드가 증가하고, CRD 설치나 클러스터 레벨 리소스가 필요한 경우 클러스터 관리자의 협조가 필요합니다. 또한 in-cluster 배포를 위해서는 각 네임스페이스마다 ServiceAccount와 RoleBinding을 수동으로 설정해야 합니다.

#### 2.3 설치 모드 비교 및 선택 기준

**설치 모드 비교:**

| 항목 | Cluster Scoped | Namespace Scoped |
|------|----------------|------------------|
| **권한 범위** | 전체 클러스터 (cluster-admin) | 단일 네임스페이스 (Role) |
| **in-cluster 사용** | 기본 지원 (자동 ServiceAccount) | 추가 설정 필요 (수동 RBAC) |
| **CRD 설치** | 직접 가능 | 클러스터 관리자 협조 필요 |
| **멀티 테넌시 방식** | AppProject 기반 논리 격리 | 인스턴스 분리로 물리 격리 |
| **관리 오버헤드** | 낮음 (단일 인스턴스) | 높음 (N개 인스턴스) |
| **보안 격리 수준** | RBAC 기반 (논리적) | 네임스페이스 기반 (물리적) |
| **침해 시 피해 범위** | 전체 클러스터 | 단일 네임스페이스 |

**선택 기준:**

중앙 집중식 GitOps 플랫폼이 필요하고 AppProject 기반 멀티 테넌시로 충분한 격리가 가능한 경우 Cluster Scoped를 선택합니다. 규제 준수로 최소 권한 원칙이 필수이거나, 팀 간 완전한 독립성이 필요한 경우 Namespace Scoped를 선택합니다. 대부분의 기업 환경에서는 Cluster Scoped + AppProject 조합으로 운영 효율과 보안 간의 균형을 맞춥니다.

---

### 3. AppProject (프로젝트)

AppProject는 Argo CD 애플리케이션의 논리적 그룹화 단위이자 멀티 테넌시의 핵심 경계점입니다. AppProject가 중요한 이유는 Kubernetes RBAC만으로는 "어떤 Git 저장소에서 어떤 클러스터로 배포할 수 있는가"를 제어할 수 없지만, AppProject는 GitOps 워크플로우 전체를 세분화하여 제어할 수 있기 때문입니다.

#### 3.1 AppProject의 4가지 핵심 기능

**1. 소스 제한 (sourceRepos):**

AppProject는 허용된 Git/Helm 저장소만 Application의 소스로 사용할 수 있도록 제한합니다. 이는 승인되지 않은 외부 저장소나 악의적인 코드가 클러스터에 배포되는 것을 방지합니다. 예를 들어, 백엔드팀은 `https://github.com/company/backend-*` 저장소만 사용 가능하고, 프론트엔드팀은 `https://github.com/company/frontend-*` 저장소만 사용 가능하도록 제한합니다.

**2. 대상 제한 (destinations):**

AppProject는 배포 가능한 클러스터와 네임스페이스를 제한합니다. 이는 개발팀이 실수로 프로덕션 환경에 배포하거나, 다른 팀의 네임스페이스를 침범하는 것을 방지합니다. 예를 들어, 개발자는 dev/staging 클러스터만 접근 가능하고, SRE팀만 production 클러스터에 배포할 수 있도록 설정합니다.

**3. 리소스 제한 (whitelist/blacklist):**

AppProject는 생성 가능한 Kubernetes 리소스 종류를 제한합니다. 이는 개발자가 ClusterRole, PersistentVolume 등 민감한 클러스터 리소스를 생성하거나, ResourceQuota를 우회하는 것을 방지합니다. 네임스페이스 스코프 리소스(Deployment, Service)와 클러스터 스코프 리소스(Namespace, ClusterRole)를 독립적으로 제어할 수 있습니다.

**4. RBAC (roles/policies):**

AppProject는 사용자/그룹별로 세분화된 권한을 설정합니다. Kubernetes RBAC는 클러스터 리소스에 대한 권한만 제어하지만, AppProject RBAC는 Application의 sync, create, delete 등 GitOps 작업에 대한 권한을 제어합니다. 예를 들어, 개발자는 Application을 조회하고 sync만 가능하지만, SRE는 생성/삭제까지 가능하도록 설정합니다.

**AppProject 기능 구조:**

```mermaid
sequenceDiagram
    participant User as 사용자
    participant ArgoCD as Argo CD
    participant Project as AppProject
    participant Git as Git 저장소
    participant K8s as Kubernetes

    User->>ArgoCD: Application 생성 요청<br/>(Git URL, 대상 클러스터)
    ArgoCD->>Project: 검증 요청

    Project->>Project: 1. sourceRepos 검증
    Note over Project: Git URL이<br/>허용 목록에 있는가?

    Project->>Project: 2. destinations 검증
    Note over Project: 클러스터/네임스페이스가<br/>허용 목록에 있는가?

    Project->>Project: 3. 리소스 검증
    Note over Project: manifest의 리소스 종류가<br/>whitelist/blacklist 통과?

    Project->>Project: 4. RBAC 검증
    Note over Project: 사용자가 create 액션<br/>권한 보유?

    alt 모든 검증 통과
        Project-->>ArgoCD: 허용
        ArgoCD->>Git: manifest 가져오기
        ArgoCD->>K8s: 리소스 생성
        K8s-->>User: Application 생성 완료
    else 검증 실패
        Project-->>ArgoCD: 거부
        ArgoCD-->>User: permission denied
    end
</sequenceDiagram>

위 다이어그램에서 볼 수 있듯이, AppProject는 4단계 게이트로 작동하여 모든 검증을 통과한 요청만 실행됩니다. 이러한 다층 방어(Defense in Depth) 전략은 단일 실수나 침해로 인한 피해를 최소화합니다.

#### 3.2 기본 프로젝트 (default)

Argo CD는 설치 시 `default` 프로젝트를 자동 생성하며, 이는 가장 허용적인 설정을 가집니다. default 프로젝트는 모든 소스 저장소, 모든 대상 클러스터/네임스페이스, 모든 리소스 종류를 허용합니다. 이는 초기 테스트와 프로토타이핑에는 편리하지만, 프로덕션 환경에서는 심각한 보안 위험입니다.

**default 프로젝트의 기본 설정:**

```yaml
# default 프로젝트 - 모든 것을 허용
spec:
  sourceRepos:
  - '*'                    # 모든 Git/Helm 저장소 허용
  destinations:
  - namespace: '*'         # 모든 네임스페이스 허용
    server: '*'            # 모든 클러스터 허용
  clusterResourceWhitelist:
  - group: '*'             # 모든 클러스터 리소스 허용
    kind: '*'
```

**default 프로젝트 관련 주요 규칙:**

하나의 Application은 정확히 하나의 AppProject에만 속할 수 있습니다. Application manifest에서 `spec.project` 필드를 생략하면 자동으로 default 프로젝트에 할당됩니다. default 프로젝트는 삭제할 수 없지만, 완전히 잠금(lockdown)하여 사용을 강제로 금지할 수 있습니다. 프로덕션 환경에서는 default 프로젝트를 잠그고, 모든 팀이 명시적인 AppProject를 생성하도록 강제하는 것이 보안 모범 사례입니다.

---

### 4. 리소스 관리

AppProject의 리소스 관리는 allow/deny 모델을 따르며, 첫 번째 매칭 규칙이 우선 적용됩니다. 이 모델이 중요한 이유는 명시적 거부(deny)를 먼저 배치하여 예외를 정의하고, 이후 일반 허용(allow)을 배치하여 기본 정책을 정의할 수 있기 때문입니다.

#### 4.1 소스 저장소 관리 (sourceRepos)

sourceRepos는 Application이 사용할 수 있는 Git 또는 Helm 저장소를 제한합니다. 이는 공격자가 악의적인 외부 저장소를 Application의 소스로 설정하여 악성 코드를 배포하는 공격을 방지합니다.

**소스 저장소 제한 예시:**

```yaml
spec:
  sourceRepos:
    # 1단계: 명시적 거부 (우선 순위 높음)
    - '!ssh://git@github.com:argoproj/test'  # 특정 저장소 거부
    - '!https://gitlab.com/external/**'      # 외부 조직 전체 거부

    # 2단계: 일반 허용 (우선 순위 낮음)
    - 'https://github.com/company/*'         # 회사 저장소만 허용
    - 'https://helm.company.com/*'           # 내부 Helm 저장소 허용
```

위 설정에서 `!` 접두사는 명시적 거부를 의미하며, 이 규칙이 먼저 평가됩니다. `*`는 단일 레벨 와일드카드(예: `/company/repo1`, `/company/repo2`)이고, `**`는 하위 경로 포함 와일드카드(예: `/external/group1/repo`, `/external/group2/repo`)입니다.

**실무 시나리오:**

백엔드팀은 `https://github.com/company/backend-*` 저장소만 접근 가능하고, 프론트엔드팀은 `https://github.com/company/frontend-*` 저장소만 접근 가능하도록 설정합니다. 외부 오픈소스 Helm 차트가 필요한 경우, 보안 검토를 거친 특정 차트만 `https://charts.bitnami.com/bitnami/nginx` 형식으로 명시적으로 허용합니다.

#### 4.2 배포 대상 관리 (destinations)

destinations는 Application이 배포할 수 있는 클러스터와 네임스페이스를 제한합니다. 이는 개발자가 실수로 프로덕션 환경을 수정하거나, 다른 팀의 네임스페이스에 리소스를 생성하는 것을 방지합니다.

**배포 대상 제한 예시:**

```yaml
spec:
  destinations:
  # 1단계: 민감한 네임스페이스 거부
  - namespace: '!kube-system'
    server: '*'
  - namespace: '!kube-public'
    server: '*'

  # 2단계: 특정 클러스터 패턴 거부
  - namespace: '*'
    server: '!https://prod-*'    # production 클러스터 전체 거부

  # 3단계: 허용 범위 정의
  - namespace: 'team-a-*'        # team-a 네임스페이스만 허용
    server: 'https://dev-cluster'
  - namespace: 'team-a-*'
    server: 'https://staging-cluster'
```

위 설정에서 규칙 순서가 중요한 이유는 Argo CD가 위에서 아래로 순차적으로 평가하여 첫 번째 매칭 규칙을 적용하기 때문입니다. deny 규칙을 먼저 배치하지 않으면, 이후 allow 규칙이 먼저 매칭되어 deny가 무시됩니다.

**실무 시나리오:**

개발팀은 `dev-*`, `staging-*` 네임스페이스에만 배포 가능하고, SRE팀은 `prod-*` 네임스페이스까지 접근 가능하도록 설정합니다. 모든 팀은 `kube-system`, `kube-public` 등 시스템 네임스페이스에 대한 접근을 거부하여 클러스터 안정성을 보호합니다.

#### 4.3 네임스페이스 스코프 리소스 제한

네임스페이스 스코프 리소스는 특정 네임스페이스 내에서만 존재하는 리소스(Pod, Deployment, Service 등)입니다. whitelist와 blacklist 중 하나만 사용하며, whitelist를 사용하면 명시적으로 허용하지 않은 모든 리소스가 거부됩니다(기본 거부).

**Blacklist (특정 리소스 거부):**

```yaml
spec:
  namespaceResourceBlacklist:
  - group: ''
    kind: ResourceQuota      # 할당량 우회 방지
  - group: ''
    kind: LimitRange         # 리소스 제한 우회 방지
  - group: ''
    kind: NetworkPolicy      # 네트워크 정책 변경 방지
```

blacklist를 사용하는 이유는 대부분의 리소스를 허용하되, 민감한 일부 리소스만 차단하고 싶을 때 설정이 간단하기 때문입니다. 위 예시에서 ResourceQuota와 LimitRange를 차단하는 이유는 개발자가 플랫폼팀이 설정한 리소스 할당량을 임의로 변경하는 것을 방지하기 위함입니다.

**Whitelist (허용 리소스만 명시):**

```yaml
spec:
  namespaceResourceWhitelist:
  - group: 'apps'
    kind: Deployment         # 애플리케이션 배포만 허용
  - group: ''
    kind: Service            # 서비스 노출만 허용
  - group: ''
    kind: ConfigMap          # 설정만 허용
  - group: ''
    kind: Secret             # 비밀 정보만 허용
```

whitelist를 사용하는 이유는 보안이 중요한 환경에서 명시적으로 허용된 리소스만 사용하도록 강제하기 위함입니다(최소 권한 원칙). 예를 들어, 개발자는 Deployment, Service, ConfigMap만 생성 가능하고, StatefulSet, DaemonSet 등 복잡한 리소스는 플랫폼팀만 관리하도록 제한합니다.

#### 4.4 클러스터 스코프 리소스 제한

클러스터 스코프 리소스는 네임스페이스에 속하지 않고 클러스터 전체에 영향을 미치는 리소스(Namespace, ClusterRole, PersistentVolume 등)입니다. 기본적으로 클러스터 리소스는 모두 거부되므로, 필요한 리소스만 whitelist에 명시해야 합니다.

**클러스터 리소스 제한 예시:**

```yaml
spec:
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace          # Namespace 생성만 허용
```

위 설정이 중요한 이유는 대부분의 Application은 네임스페이스 리소스만 필요하므로, 클러스터 리소스를 제한하여 보안을 강화할 수 있기 때문입니다. 예를 들어, Namespace 생성은 허용하되, ClusterRole, ClusterRoleBinding, PersistentVolume 등 민감한 클러스터 리소스는 플랫폼팀만 관리하도록 제한합니다.

**실무 시나리오:**

애플리케이션팀은 Namespace 생성만 가능하고(멀티 테넌시 환경 생성), ClusterRole/ClusterRoleBinding은 보안팀만 관리합니다. PersistentVolume은 스토리지팀만 생성 가능하며, 개발자는 PersistentVolumeClaim만 사용하여 스토리지를 요청합니다.

#### 4.5 리소스 관리 규칙 요약

| 속성 | 스코프 | 동작 | 사용 시점 |
|------|--------|------|----------|
| `sourceRepos` | 소스 | 허용/거부할 Git/Helm 저장소 | 승인된 저장소만 사용하도록 제한 |
| `destinations` | 대상 | 허용/거부할 클러스터/네임스페이스 | 배포 환경 격리 (dev/staging/prod) |
| `namespaceResourceWhitelist` | 네임스페이스 | 허용할 리소스 종류 (기본 거부) | 최소 권한 원칙 적용 (보안 중요) |
| `namespaceResourceBlacklist` | 네임스페이스 | 거부할 리소스 종류 (기본 허용) | 특정 민감 리소스만 차단 (편의성 우선) |
| `clusterResourceWhitelist` | 클러스터 | 허용할 리소스 종류 (기본 거부) | 클러스터 리소스는 기본 차단 |
| `clusterResourceBlacklist` | 클러스터 | 거부할 리소스 종류 (기본 허용) | 거의 사용 안 함 (보안 위험) |

---

### 5. Project 레벨 RBAC

Project 레벨 RBAC는 Kubernetes RBAC와 별도로 작동하는 Argo CD 고유의 권한 시스템입니다. Kubernetes RBAC는 클러스터 리소스(Pod, Service 등)에 대한 권한을 제어하지만, Project RBAC는 GitOps 작업(Application sync, create, delete 등)에 대한 권한을 제어합니다. 두 시스템이 독립적으로 작동하는 이유는 "누가 Kubernetes 리소스를 직접 수정할 수 있는가"와 "누가 GitOps를 통해 배포할 수 있는가"는 다른 질문이기 때문입니다.

#### 5.1 RBAC 정책 형식

AppProject는 `roles` 필드에서 역할을 정의하고, 각 역할에 `policies` 리스트로 세분화된 권한을 설정합니다. 이 정책은 Casbin 문법을 따르며, p(policy) 타입으로 역할, 리소스, 액션, 대상, 허용/거부를 명시합니다.

**RBAC 정책 예시:**

```yaml
spec:
  roles:
  - name: developer                    # 역할 이름 (임의 문자열)
    description: Developers can view and sync applications
    policies:
    # 구문: p, <role>, <resource>, <action>, <object>, <allow/deny>
    - p, proj:myproj:developer, applications, get, myproj/*, allow
    - p, proj:myproj:developer, applications, sync, myproj/*, allow
    - p, proj:myproj:developer, projects, get, myproj, allow
    groups:
    - Developers                       # SSO에서 매핑할 그룹명
```

위 설정에서 `proj:myproj:developer`는 역할의 전체 식별자(Fully Qualified Name)이며, `myproj/\*`는 myproj 프로젝트의 모든 Application을 의미합니다. `groups` 필드는 SSO(Okta, Google, Azure AD 등)의 그룹과 연결하여, Developers 그룹에 속한 모든 사용자에게 이 역할을 자동 부여합니다.

#### 5.2 정책 구문 분석

```
p, proj:myproj:developer, applications, sync, myproj/frontend, allow
│   │                     │             │     │                 │
│   │                     │             │     │                 └─ 허용(allow) 또는 거부(deny)
│   │                     │             │     └─ 대상 객체 (project/app 또는 *)
│   │                     │             └─ 액션 (get, create, update, delete, sync, override, action)
│   │                     └─ 리소스 유형 (applications, projects, repositories, clusters, logs, exec)
│   └─ 역할 (proj:<project>:<role-name> 형식)
└─ 정책 타입 (p: policy, g: group)
```

**정책 구문의 각 요소가 중요한 이유:**

- **역할 (proj:myproj:developer):** 프로젝트별로 격리된 역할을 정의하여, 다른 프로젝트의 동일한 역할명과 충돌하지 않습니다.
- **리소스 (applications):** GitOps 작업 대상을 지정하며, applications는 배포 관리, projects는 프로젝트 설정 관리를 의미합니다.
- **액션 (sync):** 구체적인 작업을 지정하여 최소 권한 원칙을 구현합니다. 예를 들어, 개발자는 sync만 가능하고 delete는 불가능합니다.
- **대상 (myproj/frontend):** 와일드카드(`*`)로 전체 허용하거나, 특정 Application만 지정할 수 있습니다.
- **허용/거부 (allow):** 명시적 거부로 예외를 정의할 수 있지만, 일반적으로 암묵적 거부(명시하지 않으면 거부)를 사용합니다.

#### 5.3 제어 가능한 리소스 및 액션

**리소스별 액션 매트릭스:**

| 리소스 | 가능한 액션 | 설명 |
|--------|------------|------|
| `applications` | get, create, update, delete, sync, override, action | Application 관리 (조회, 생성, 수정, 삭제, 동기화, 파라미터 재정의, 커스텀 액션) |
| `projects` | get, create, update, delete | AppProject 관리 (대부분 관리자 전용) |
| `repositories` | get, create, update, delete | Git/Helm 저장소 연결 관리 |
| `clusters` | get, create, update, delete | 대상 클러스터 연결 관리 |
| `logs` | get | Application Pod 로그 조회 (디버깅) |
| `exec` | create | Application Pod 내 명령 실행 (위험, 신중히 부여) |

**실무에서의 역할 분리 패턴:**

- **Developer 역할:** `applications: get, sync` + `logs: get` → Application 조회, 동기화, 로그 확인만 가능
- **Lead Developer 역할:** `applications: get, create, update, sync, override` → Application 생성 및 파라미터 조정 가능
- **SRE 역할:** `applications: *` + `projects: get, update` → 모든 Application 작업 가능, 프로젝트 설정 조정 가능
- **Platform Admin 역할:** `applications: *` + `projects: *` + `clusters: *` + `repositories: *` → 전체 관리 권한

**override와 action이 중요한 이유:**

`override` 액션은 Application manifest에 정의된 파라미터를 Argo CD UI에서 임시로 재정의할 수 있는 권한입니다. 이는 긴급 상황에서 Git 커밋 없이 즉시 배포를 수정할 수 있지만, GitOps 원칙을 우회하므로 제한적으로 부여해야 합니다. `action` 액션은 Argo CD Resource Action(커스텀 액션)을 실행하는 권한으로, 예를 들어 "restart deployment" 같은 운영 작업을 허용합니다.

**Project RBAC 적용 흐름:**

```mermaid
sequenceDiagram
    participant User as 사용자(mary<br/>Developers 그룹)
    participant ArgoCD as Argo CD
    participant SSO as SSO (Okta)
    participant Project as AppProject
    participant K8s as Kubernetes

    User->>ArgoCD: 로그인 요청
    ArgoCD->>SSO: 인증 요청
    SSO-->>ArgoCD: 인증 성공<br/>(그룹: Developers)

    User->>ArgoCD: Application Sync 요청
    ArgoCD->>Project: RBAC 검증 요청

    Project->>Project: 1. 역할 매핑<br/>(Developers → developer 역할)
    Project->>Project: 2. 정책 평가<br/>(applications, sync, allow?)

    alt RBAC 허용
        Project-->>ArgoCD: 허용
        ArgoCD->>K8s: Sync 실행
        K8s-->>User: 성공
    else RBAC 거부
        Project-->>ArgoCD: 거부
        ArgoCD-->>User: permission denied<br/>(applications, sync, myproj/app)
    end
</sequenceDiagram>

위 다이어그램에서 볼 수 있듯이, SSO 그룹이 AppProject의 역할로 자동 매핑되며, 각 요청마다 정책을 평가하여 실시간으로 권한을 검증합니다.

---

### 6. 실습: GitOps 대시보드 구현

이 실습에서는 golist라는 3-tier 애플리케이션(frontend, api, db)을 AppProject로 관리하고, 개발자 그룹에게 조회 및 동기화 권한만 부여하는 멀티 테넌시 시나리오를 구현합니다.

#### 6.1 아키텍처 개요

**실습 목표:**

Admin 사용자는 golist 프로젝트의 모든 Application에 대해 생성, 수정, 삭제, 동기화를 수행할 수 있습니다. Developers 그룹 사용자는 Application을 조회하고 동기화만 가능하며, 수정이나 삭제는 불가능합니다. 이를 통해 개발자는 GitOps를 통한 배포만 수행하고, 인프라 변경은 관리자만 수행하도록 제한합니다.

**권한 분리 시나리오:**

```mermaid
sequenceDiagram
    participant Admin as Admin 사용자
    participant Dev as Developer 사용자
    participant ArgoCD as Argo CD
    participant Project as golist AppProject
    participant K8s as Kubernetes

    Note over Admin,K8s: Admin 사용자 작업 흐름
    Admin->>ArgoCD: Application 생성 요청
    ArgoCD->>Project: RBAC 검증 (admin 역할)
    Project-->>ArgoCD: 허용 (모든 권한)
    ArgoCD->>K8s: Application 생성
    K8s-->>Admin: 성공

    Admin->>ArgoCD: Application 삭제 요청
    ArgoCD->>Project: RBAC 검증
    Project-->>ArgoCD: 허용
    ArgoCD->>K8s: Application 삭제
    K8s-->>Admin: 성공

    Note over Dev,K8s: Developer 사용자 작업 흐름
    Dev->>ArgoCD: Application 조회 요청
    ArgoCD->>Project: RBAC 검증 (developer 역할)
    Project-->>ArgoCD: 허용 (get 권한)
    ArgoCD-->>Dev: Application 정보 반환

    Dev->>ArgoCD: Application Sync 요청
    ArgoCD->>Project: RBAC 검증
    Project-->>ArgoCD: 허용 (sync 권한)
    ArgoCD->>K8s: Sync 실행
    K8s-->>Dev: 성공

    Dev->>ArgoCD: Application 삭제 시도
    ArgoCD->>Project: RBAC 검증
    Project-->>ArgoCD: 거부 (delete 권한 없음)
    ArgoCD-->>Dev: permission denied
</sequenceDiagram>

위 다이어그램은 동일한 AppProject 내에서 사용자 역할에 따라 접근 제어가 어떻게 다르게 작동하는지 보여줍니다.

#### 6.2 Step 1: 프로젝트 생성

먼저 admin 사용자로 로그인하여 golist 프로젝트를 생성합니다. 초기 생성 시에는 가장 허용적인 설정으로 시작하고, 이후 단계에서 RBAC를 추가합니다.

```bash
# admin 사용자로 로그인 확인
$ argocd account get-user-info -o json | jq .username
"admin"

# 현재 프로젝트 목록 확인 (default만 존재)
$ argocd proj list -o name
default

# golist 프로젝트 생성
# --src '*': 모든 소스 저장소 허용
# --dest '*,*': 모든 클러스터(*), 모든 네임스페이스(*) 허용
# --allow-cluster-resource '*/*': 모든 클러스터 리소스 허용
$ argocd proj create golist \
  --src '*' --dest '*,*' --allow-cluster-resource '*/*'

# 프로젝트 생성 확인
$ argocd proj list -o name
default
golist
```

위 명령어에서 `--dest '*,*'`의 첫 번째 `*`는 서버(클러스터), 두 번째 `*`는 네임스페이스를 의미합니다. `--allow-cluster-resource '*/*'`는 모든 그룹(`*`)의 모든 종류(`*`) 클러스터 리소스를 허용합니다.

#### 6.3 Step 2: Application 배포

golist 프로젝트에 속하는 3개의 Application(frontend, api, db)을 생성합니다. 각 Application은 `spec.project: golist`로 명시적으로 프로젝트에 할당됩니다.

**Application manifest 예시:**

```yaml
# golist-db.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: golist-db
  namespace: argocd
spec:
  project: golist              # ⭐ golist 프로젝트에 명시적 할당
  source:
    repoURL: https://github.com/example/golist
    path: db                   # db/ 디렉토리의 Helm 차트 또는 Kustomize
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: golist
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```bash
# 3개 Application 생성
$ argocd app create --file ch08/argocd/applications/golist-db.yaml
$ argocd app create --file ch08/argocd/applications/golist-api.yaml
$ argocd app create --file ch08/argocd/applications/golist-frontend.yaml

# golist 프로젝트에 속한 Application 확인
$ argocd app list -o name --project=golist
argocd/golist-api
argocd/golist-db
argocd/golist-frontend

# Kubernetes Pod 상태 확인 (실제 배포 확인)
$ kubectl get pods -n golist
NAME                               READY   STATUS    RESTARTS   AGE
golist-api-764879758b-bs57q        1/1     Running   0          11m
golist-db-mariadb-0                1/1     Running   0          10m
golist-frontend-7647cb44d4-g7kvx   1/1     Running   0          10m
```

위 단계에서 Application이 생성되면 Argo CD는 자동으로 Git 저장소에서 manifest를 가져와 Kubernetes에 배포합니다. `syncPolicy.automated`를 설정하여 Git 변경사항이 자동으로 클러스터에 반영되도록 합니다.

#### 6.4 Step 3: Project RBAC 구성

golist 프로젝트에 developer 역할을 추가하고, Developers 그룹에 연결합니다. 이 역할은 Application 조회(get)와 동기화(sync)만 가능하며, 생성/수정/삭제는 불가능합니다.

**선언적 프로젝트 설정:**

```yaml
# golist.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: golist
  namespace: argocd
spec:
  description: Golist application project with RBAC

  # 리소스 제한 (변경 없음)
  sourceRepos:
  - '*'
  destinations:
  - namespace: '*'
    server: '*'
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'

  # ⭐ RBAC 설정 추가
  roles:
  - name: golist-developer       # 역할 이름 (임의)
    description: Developers can view and sync applications only
    policies:
    # Application 조회 권한
    - p, proj:golist:golist-developer, applications, get, golist/*, allow
    # Application 동기화 권한
    - p, proj:golist:golist-developer, applications, sync, golist/*, allow
    # Project 정보 조회 권한 (UI에서 프로젝트 보기 위해 필요)
    - p, proj:golist:golist-developer, projects, get, golist, allow
    # Application 로그 조회 권한 (디버깅용)
    - p, proj:golist:golist-developer, logs, get, golist/*, allow
    groups:
    - Developers                 # ⭐ SSO의 Developers 그룹과 매핑
```

```bash
# 프로젝트 설정 적용 (기존 프로젝트 업데이트)
# --upsert: 존재하면 업데이트, 없으면 생성
$ argocd proj create --upsert --file ch08/argocd/projects/golist.yaml

# RBAC 설정 확인
$ argocd proj role list golist
ROLE-NAME           DESCRIPTION
golist-developer    Developers can view and sync applications only

# 역할의 상세 정책 확인
$ argocd proj role get golist golist-developer
```

위 설정에서 `golist/*`는 golist 프로젝트의 모든 Application을 의미하며, 특정 Application만 허용하려면 `golist/frontend`처럼 명시할 수 있습니다. `logs, get` 권한을 추가한 이유는 개발자가 배포 후 Pod 로그를 확인하여 디버깅할 수 있도록 하기 위함입니다.

#### 6.5 Step 4: 테스트

Developers 그룹에 속한 사용자(mary)로 로그인하여 권한이 올바르게 작동하는지 확인합니다.

**테스트 시나리오:**

| 작업 | 명령어 | 예상 결과 | 이유 |
|------|--------|----------|------|
| **로그인** | `argocd login --username mary` | ✅ 성공 | SSO에서 Developers 그룹으로 인증 |
| **Application 목록 조회** | `argocd app list --project golist` | ✅ 성공 | `get` 권한 보유 |
| **Application 상세 조회** | `argocd app get golist/golist-frontend` | ✅ 성공 | `get` 권한 보유 |
| **Application Sync** | `argocd app sync golist/golist-frontend` | ✅ 성공 | `sync` 권한 보유 |
| **Application 삭제 시도** | `argocd app delete golist/golist-frontend` | ❌ 실패 | `delete` 권한 없음 |
| **Application 생성 시도** | `argocd app create ...` | ❌ 실패 | `create` 권한 없음 |
| **Project 수정 시도** | `argocd proj set golist ...` | ❌ 실패 | `update` 권한 없음 |

**삭제 시도 시 에러 메시지:**

```bash
$ argocd app delete golist/golist-frontend
FATA[0000] rpc error: code = PermissionDenied desc = permission denied: applications, delete, golist/golist-frontend, sub: proj:golist:golist-developer, iat: 2024-01-15T10:30:00Z
```

위 에러 메시지는 `proj:golist:golist-developer` 역할이 `applications` 리소스의 `delete` 액션 권한이 없음을 명확히 보여줍니다. 이를 통해 개발자는 GitOps를 통한 배포만 수행하고, 인프라 변경은 관리자의 승인을 받아야 합니다.

---

## 🔍 심화 학습

### AppProject 잠금 패턴

프로덕션 환경에서는 default 프로젝트를 완전히 잠금(lockdown)하여 모든 팀이 명시적인 AppProject를 생성하도록 강제하는 것이 보안 모범 사례입니다. default 프로젝트를 잠그는 이유는 개발자가 `spec.project`를 생략하여 의도치 않게 모든 권한을 가진 default 프로젝트에 Application을 생성하는 실수를 방지하기 위함입니다.

**default 프로젝트 완전 잠금:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: default
  namespace: argocd
spec:
  description: Default project (locked down for security)

  # ⭐ 모든 소스 거부 (빈 리스트)
  sourceRepos: []

  # ⭐ 모든 대상 거부 (빈 리스트)
  destinations: []

  # ⭐ 모든 클러스터 리소스 거부 (빈 리스트)
  clusterResourceWhitelist: []

  # ⭐ 모든 네임스페이스 리소스 거부 (빈 리스트)
  namespaceResourceWhitelist: []
```

위 설정을 적용하면 default 프로젝트에 속한 Application은 어떤 저장소에서도 가져올 수 없고, 어떤 클러스터에도 배포할 수 없으므로 사실상 사용 불가능합니다. 이를 통해 모든 팀이 명시적으로 AppProject를 생성하고 최소 권한 원칙을 적용하도록 강제합니다.

### Project Windows (배포 시간 제한)

Project Windows는 특정 시간대에만 Application Sync를 허용하거나 거부하는 기능입니다. 이는 업무 시간에 프로덕션 배포를 금지하거나, 변경 관리 정책에 따라 승인된 시간대에만 배포를 허용하는 데 사용됩니다.

**배포 시간 제한 예시:**

```yaml
spec:
  syncWindows:
  # ✅ 매일 22:00부터 1시간 동안 배포 허용
  - kind: allow
    schedule: '0 22 * * *'     # Cron 표현식 (UTC)
    duration: 1h
    applications:
    - '*'                      # 모든 Application 적용
    timeZone: 'Asia/Seoul'     # 타임존 명시

  # ❌ 평일 업무시간(09:00-18:00) 프로덕션 배포 금지
  - kind: deny
    schedule: '0 9 * * 1-5'    # 월-금 09:00
    duration: 9h
    applications:
    - 'prod-*'                 # prod로 시작하는 Application만
    timeZone: 'Asia/Seoul'
```

위 설정이 실무에서 중요한 이유는 프로덕션 배포를 야간 시간대로 제한하여 업무 시간에 발생할 수 있는 장애를 방지하고, 배포 후 모니터링할 수 있는 시간을 확보하기 위함입니다. 또한 변경 관리 정책을 자동화하여 수동 승인 프로세스를 줄일 수 있습니다.

### 출처
- [Argo CD Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
- [Argo CD RBAC](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/)
- [Namespace Scoped Installation](https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/#non-high-availability)

---

## 💡 실무 적용 포인트

### 설치 모드 선택 가이드

설치 모드 선택은 조직의 보안 요구사항, 팀 구조, 운영 복잡도를 종합적으로 고려하여 결정해야 합니다.

| 상황 | 권장 모드 | 이유 |
|------|----------|------|
| 중앙 집중 관리, Hub-and-Spoke | Cluster Scoped | 단일 UI로 모든 클러스터 관리, AppProject로 충분한 격리 가능 |
| 팀별 완전 격리 필요 | Namespace Scoped | Kubernetes 네임스페이스 격리로 물리적 경계 보장 |
| 규정 준수로 권한 분리 필수 | Namespace Scoped | 최소 권한 원칙 적용, 감사 추적 간소화 |
| 관리 오버헤드 최소화 | Cluster Scoped + AppProject | 단일 인스턴스 운영, RBAC로 세분화 제어 |

**실무 의사결정 프로세스:**

대부분의 기업은 Cluster Scoped로 시작하여 AppProject와 RBAC로 멀티 테넌시를 구현합니다. 이후 특정 팀이나 프로젝트에서 규제 요구사항이 발생하면 Namespace Scoped 인스턴스를 추가로 배포하는 하이브리드 접근 방식을 사용합니다. 예를 들어, 일반 애플리케이션은 중앙 Argo CD로 관리하고, PCI-DSS 준수가 필요한 결제 시스템은 독립적인 Namespace Scoped Argo CD로 관리합니다.

### 멀티 테넌시 구현 패턴

조직 구조와 배포 전략에 따라 AppProject를 어떻게 나눌지 결정해야 합니다.

| 패턴 | 설명 | 적합한 경우 | 예시 |
|------|------|------------|------|
| **Project per Team** | 팀별로 프로젝트 분리 | 팀 자율성이 높고 서로 다른 배포 정책 필요 | team-backend, team-frontend, team-platform |
| **Project per Environment** | 환경별로 프로젝트 분리 | 환경 격리가 중요하고 배포 승인 프로세스 상이 | project-dev, project-staging, project-prod |
| **Project per Application** | 애플리케이션별로 프로젝트 분리 | 애플리케이션마다 다른 보안/규정 요구사항 | project-payment, project-analytics, project-public-api |
| **하이브리드** | 위 패턴 조합 | 대규모 조직, 복잡한 요구사항 | team-backend-prod, team-frontend-dev |

**실무 예시:**

중소 기업(팀 5개 이하)은 Project per Team 패턴으로 시작하여 각 팀이 자율적으로 배포 관리합니다. 대기업(팀 10개 이상)은 Project per Environment로 시작하여 환경별 변경 관리 정책을 적용합니다. 금융/의료 같은 규제 산업은 Project per Application으로 민감한 애플리케이션을 격리하고 감사 추적을 간소화합니다.

### 주의할 점 / 흔한 실수

**1. 규칙 순서 실수:**

deny 규칙이 allow 규칙보다 뒤에 오면 allow가 먼저 매칭되어 deny가 무시됩니다. 항상 deny를 먼저 배치해야 합니다.

```yaml
# ❌ 잘못된 순서 (kube-system 허용됨)
destinations:
  - namespace: '*'
    server: '*'
  - namespace: '!kube-system'  # 위에서 이미 매칭되어 무시됨
    server: '*'

# ✅ 올바른 순서
destinations:
  - namespace: '!kube-system'  # deny 먼저
    server: '*'
  - namespace: '*'              # allow 나중
    server: '*'
```

**2. 암묵적 거부 오해:**

whitelist를 사용하면 명시하지 않은 모든 리소스가 거부됩니다. 개발자가 새로운 리소스 종류를 추가하려고 할 때 permission denied가 발생하면, whitelist에 해당 리소스를 추가해야 합니다.

```yaml
# Deployment만 허용 → Service 생성 시도는 거부됨
namespaceResourceWhitelist:
  - group: 'apps'
    kind: Deployment
# ⭐ Service를 추가하려면 whitelist에 명시 필요
```

**3. default 프로젝트 방치:**

프로덕션에서 default 프로젝트를 잠그지 않으면, 개발자가 `spec.project`를 생략하여 의도치 않게 모든 권한을 가진 Application을 생성할 수 있습니다. 보안 감사에서 가장 많이 지적되는 항목입니다.

**4. SSO 그룹명 불일치:**

AppProject의 `roles.groups`는 SSO 제공자의 그룹명과 정확히 일치해야 합니다. 대소문자, 공백, 특수문자까지 완전히 동일해야 하며, 불일치 시 권한이 부여되지 않습니다.

```yaml
# ❌ SSO 그룹명: "Backend Developers" (공백 포함)
groups:
  - BackendDevelopers  # 매칭 실패

# ✅ 정확히 일치
groups:
  - "Backend Developers"
```

**5. Cluster Scoped 과도한 권한:**

Cluster Scoped 설치 시 기본적으로 cluster-admin 권한을 가지므로, 불필요한 클러스터 리소스 접근은 AppProject의 `clusterResourceWhitelist`로 제한해야 합니다. 대부분의 Application은 Namespace 생성만 필요합니다.

### 면접에서 나올 수 있는 질문

**Q1: Cluster Scoped와 Namespace Scoped 설치 모드의 차이점은 무엇이고, 언제 각각 사용하나요?**

Cluster Scoped는 Argo CD가 전체 클러스터에 대한 cluster-admin 권한을 가지는 방식으로, 중앙 집중식 GitOps 플랫폼에 적합합니다. 단일 UI로 여러 클러스터를 관리할 수 있고, AppProject와 RBAC로 충분한 멀티 테넌시를 구현할 수 있습니다. Namespace Scoped는 특정 네임스페이스에 대한 권한만 가지는 방식으로, 팀 간 완전한 격리가 필요하거나 규제 준수로 최소 권한 원칙이 필수인 경우 사용합니다. 대부분의 조직은 Cluster Scoped로 시작하여 필요 시 Namespace Scoped 인스턴스를 추가하는 하이브리드 접근 방식을 사용합니다.

**Q2: AppProject의 역할과 Kubernetes RBAC와의 차이점은 무엇인가요?**

AppProject는 Argo CD의 멀티 테넌시 핵심 구성 요소로, GitOps 워크플로우 전체를 제어합니다. sourceRepos로 허용된 Git 저장소를 제한하고, destinations로 배포 가능한 클러스터/네임스페이스를 제한하며, whitelist/blacklist로 생성 가능한 Kubernetes 리소스 종류를 제한하고, RBAC로 사용자/그룹별 권한을 설정합니다. Kubernetes RBAC는 클러스터 리소스에 대한 직접 접근 권한만 제어하지만, AppProject는 "어떤 Git 저장소에서 어떤 클러스터로 배포할 수 있는가"를 제어하여 GitOps 보안을 강화합니다. 두 시스템은 독립적으로 작동하며 모두 통과해야만 작업이 실행됩니다.

**Q3: sourceRepos와 destinations에서 deny 규칙을 설정하는 방법과 주의사항은 무엇인가요?**

deny 규칙은 `!` 접두사로 명시적 거부를 나타내며, 반드시 allow 규칙보다 먼저 배치해야 합니다. Argo CD는 위에서 아래로 순차적으로 평가하여 첫 번째 매칭 규칙을 적용하므로, deny가 allow보다 뒤에 오면 무시됩니다. 예를 들어, sourceRepos에서 외부 저장소를 거부하려면 `- '!https://external.com/**'`를 먼저 배치하고, 이후 `- 'https://github.com/company/*'`로 회사 저장소만 허용합니다. destinations에서 kube-system 네임스페이스를 거부하려면 `- namespace: '!kube-system'`를 먼저 배치하고, 이후 `- namespace: '*'`로 나머지를 허용합니다.

**Q4: Project 레벨 RBAC와 플랫폼 레벨 RBAC의 차이는 무엇인가요?**

Project 레벨 RBAC는 AppProject의 `roles` 필드에 정의하며, 해당 프로젝트에 속한 Application에만 적용됩니다. 예를 들어, golist 프로젝트의 developer 역할은 golist의 Application만 조회/동기화 가능하고 다른 프로젝트는 접근할 수 없습니다. 플랫폼 레벨 RBAC는 argocd-rbac-cm ConfigMap에 정의하며, 전체 Argo CD 시스템에 적용됩니다. 예를 들어, admin 그룹은 모든 프로젝트와 Application을 관리할 수 있고, 시스템 설정도 변경할 수 있습니다. 일반적으로 플랫폼 레벨 RBAC는 관리자와 플랫폼팀에게만 부여하고, 애플리케이션팀은 Project 레벨 RBAC로 제한합니다.

**Q5: default 프로젝트를 보안 강화하려면 어떻게 해야 하나요?**

default 프로젝트는 모든 리소스를 허용하므로 프로덕션에서는 반드시 잠금(lockdown)해야 합니다. `sourceRepos: []`, `destinations: []`, `clusterResourceWhitelist: []`로 설정하여 모든 접근을 거부하고, 모든 팀이 명시적인 AppProject를 생성하도록 강제합니다. 또는 `sourceRepos: ['https://github.com/company/*']`, `destinations: [namespace: 'dev-*']`처럼 제한된 범위만 허용하여 개발 환경에서만 사용 가능하도록 설정합니다. 추가로 Admission Webhook을 구성하여 `spec.project`가 없는 Application 생성을 차단할 수 있습니다.

---

## ✅ 핵심 개념 체크리스트

- [ ] Cluster Scoped는 cluster-admin 권한으로 중앙 집중 관리에 적합하고, Namespace Scoped는 네임스페이스 격리로 팀 간 완전한 독립성을 보장한다는 것을 설명할 수 있는가?
- [ ] AppProject가 sourceRepos, destinations, 리소스 제한, RBAC 4가지 기능으로 GitOps 워크플로우 전체를 제어한다는 것을 이해했는가?
- [ ] sourceRepos와 destinations에서 deny 규칙(`!` 접두사)을 allow 규칙보다 먼저 배치해야 하는 이유를 설명할 수 있는가?
- [ ] namespaceResourceWhitelist는 명시적 허용(기본 거부)이고, blacklist는 명시적 거부(기본 허용)라는 차이를 구분할 수 있는가?
- [ ] Project 레벨 RBAC 정책 구문(`p, proj:project:role, resource, action, object, allow/deny`)의 각 요소가 무엇을 의미하는지 이해했는가?
- [ ] SSO 그룹을 AppProject의 `roles.groups`에 연결하여 자동으로 권한을 부여하는 방법을 알고 있는가?
- [ ] default 프로젝트가 모든 리소스를 허용하므로 프로덕션에서는 잠금하거나 제한해야 한다는 보안 원칙을 이해했는가?
- [ ] 클러스터 스코프 리소스는 기본적으로 거부되므로 `clusterResourceWhitelist`에 명시적으로 허용해야 한다는 것을 알고 있는가?

---

## 🔗 참고 자료

- 📄 공식 문서: [Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
- 📄 RBAC: [RBAC Configuration](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/)
- 📄 설치 모드: [Installation Methods](https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/)
- 📄 Sync Windows: [Sync Windows](https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/)
- 📄 AppProject CRD: [AppProject Specification](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#projects/)

---
