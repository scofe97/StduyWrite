# Ch17. Kubernetes RBAC과 보안 - 최소 권한 원칙으로 클러스터 보호하기

> 📌 **핵심 요약**
>
> Kubernetes는 기본적으로 "허용(allow-all)" 모델에 가깝다. NetworkPolicy가 없으면 모든 Pod 간 통신이 허용되고, default ServiceAccount는 API 서버에 접근할 수 있으며, Secrets는 base64 인코딩일 뿐 암호화가 아니다. RBAC(Role-Based Access Control)은 "누가 무엇을 할 수 있는가"를 제어하는 핵심 메커니즘으로, Role/ClusterRole로 권한을 정의하고 RoleBinding/ClusterRoleBinding으로 주체(사용자, 그룹, ServiceAccount)에 권한을 부여한다. Pod Security Standards는 Pod가 실행할 수 있는 보안 수준(Privileged, Baseline, Restricted)을 정의하고, NetworkPolicy는 Pod 간 네트워크 트래픽을 제어한다. 본 챕터에서는 이 세 가지 보안 축과 Secrets 관리 전략을 학습하여, "최소 권한 원칙(Least Privilege)"에 기반한 클러스터 보안을 설계한다.

---

## 🎯 학습 목표

이번 챕터를 마치면 다음을 할 수 있다:

1. RBAC의 네 가지 리소스(Role, ClusterRole, RoleBinding, ClusterRoleBinding)의 차이와 사용 시점을 설명할 수 있다.
2. ServiceAccount를 생성하고 Pod에 최소 권한을 부여하는 RBAC 정책을 설계할 수 있다.
3. Pod Security Standards의 세 단계(Privileged, Baseline, Restricted)를 이해하고 Namespace에 적용할 수 있다.
4. NetworkPolicy로 Pod 간 인그레스/이그레스 트래픽을 제어할 수 있다.
5. Secrets의 base64 한계를 이해하고, Sealed Secrets 또는 External Secrets Operator로 보안을 강화할 수 있다.
6. Audit Log를 설정하여 클러스터에서 누가 무엇을 했는지 추적할 수 있다.

---

## 📖 본문

### 1. 왜 Kubernetes 보안이 중요한가

Kubernetes 클러스터는 조직의 핵심 인프라를 운영하는 플랫폼이다. 컨테이너화된 애플리케이션, 데이터베이스, 메시지 큐, CI/CD 파이프라인이 모두 같은 클러스터에서 실행될 수 있다. 보안이 취약하면 다음과 같은 위험이 발생한다:

- **권한 상승(Privilege Escalation)**: 하나의 Pod가 해킹되면, 과도한 권한을 가진 ServiceAccount를 통해 다른 Pod의 Secrets를 읽거나, 클러스터 전체를 제어할 수 있다.
- **횡적 이동(Lateral Movement)**: NetworkPolicy가 없으면, 해킹된 Pod에서 같은 클러스터의 다른 모든 Pod에 접근할 수 있다. 데이터베이스, 내부 API, 관리 도구에 무제한 접근.
- **정보 노출**: Secrets가 암호화되지 않은 상태로 etcd에 저장되면, etcd 접근 권한을 얻은 공격자가 모든 비밀번호, API 키, TLS 인증서를 탈취할 수 있다.
- **컴플라이언스 위반**: PCI-DSS, HIPAA, SOC2 등 규제 환경에서는 접근 제어, 감사 로그, 네트워크 격리가 필수 요건이다.

Kubernetes 보안은 크게 네 가지 축으로 구성된다:

```
┌─────────────────────────────────────────────────┐
│              Kubernetes 보안 4축                  │
├────────────────┬────────────────────────────────┤
│  1. RBAC       │ 누가 무엇을 할 수 있는가       │
│  2. Pod Security│ Pod가 무엇을 실행할 수 있는가  │
│  3. Network    │ 누가 누구와 통신할 수 있는가    │
│  4. Secrets    │ 민감 데이터를 어떻게 보호하는가  │
└────────────────┴────────────────────────────────┘
```

---

### 2. RBAC (Role-Based Access Control)

RBAC은 Kubernetes API 서버에 대한 접근을 제어하는 메커니즘이다. "인증(Authentication)"은 "당신은 누구인가?"를, "인가(Authorization)"는 "당신은 무엇을 할 수 있는가?"를 결정한다. RBAC은 인가 단계에서 동작한다.

#### 2.1 RBAC의 네 가지 리소스

RBAC은 네 가지 Kubernetes 리소스로 구성된다:

```
권한 정의:
  Role           → Namespace 범위의 권한 (예: "default NS에서 Pod 조회 가능")
  ClusterRole    → 클러스터 범위의 권한 (예: "모든 NS에서 Node 조회 가능")

권한 부여:
  RoleBinding         → Role/ClusterRole을 주체에 바인딩 (Namespace 범위)
  ClusterRoleBinding  → ClusterRole을 주체에 바인딩 (클러스터 범위)
```

**Role**: 특정 Namespace 내에서의 권한을 정의한다. 해당 Namespace의 리소스(Pod, Service, ConfigMap 등)에 대한 동작(get, list, watch, create, update, delete)을 지정한다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: development
rules:
  - apiGroups: [""]           # Core API 그룹 (Pod, Service, ConfigMap 등)
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods/log"]   # 하위 리소스: Pod 로그 조회
    verbs: ["get"]
```

**ClusterRole**: 클러스터 전체에 걸친 권한을 정의한다. Namespace에 속하지 않는 리소스(Node, PersistentVolume, Namespace 자체)에 대한 권한이나, 모든 Namespace에 걸친 권한을 정의할 때 사용한다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-viewer
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["namespaces"]
    verbs: ["get", "list"]
  - apiGroups: ["metrics.k8s.io"]   # Metrics API
    resources: ["nodes", "pods"]
    verbs: ["get", "list"]
```

**RoleBinding**: Role이나 ClusterRole을 특정 Namespace 내의 주체에 바인딩한다. ClusterRole을 RoleBinding으로 바인딩하면, ClusterRole의 권한이 해당 Namespace로 한정된다. 이 패턴은 ClusterRole을 재사용할 때 유용하다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-pod-reader
  namespace: development
subjects:
  - kind: User
    name: developer@example.com
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: app-sa
    namespace: development
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**ClusterRoleBinding**: ClusterRole을 클러스터 전체 범위로 주체에 바인딩한다. 이 바인딩을 받은 주체는 모든 Namespace에서 해당 권한을 가진다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-node-viewer
subjects:
  - kind: Group
    name: ops-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: node-viewer
  apiGroup: rbac.authorization.k8s.io
```

#### 2.2 Role vs ClusterRole: 언제 무엇을 사용하는가

| 상황 | 사용할 리소스 | 이유 |
|------|-------------|------|
| 특정 NS에서 Pod 관리 | Role + RoleBinding | NS 범위로 권한 격리 |
| 모든 NS에서 Pod 조회 | ClusterRole + ClusterRoleBinding | 클러스터 전체 조회 필요 |
| Node, PV 관리 | ClusterRole + ClusterRoleBinding | NS에 속하지 않는 리소스 |
| 여러 NS에서 같은 권한 | ClusterRole + RoleBinding (NS별) | ClusterRole 재사용 |
| CRD 리소스 관리 | ClusterRole | CRD는 클러스터 범위 |

**ClusterRole + RoleBinding 패턴**이 특히 중요하다. ClusterRole을 한 번 정의하고, 각 Namespace마다 RoleBinding을 생성하면 권한 정의를 중복하지 않으면서 Namespace별로 접근을 제한할 수 있다:

```yaml
# 1. ClusterRole 정의 (한 번)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: deployment-manager
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

---
# 2. Namespace별 RoleBinding (team-a에만 적용)
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-deployment-manager
  namespace: team-a              # 이 Namespace로 권한 한정
subjects:
  - kind: Group
    name: team-a-devs
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole              # ClusterRole을 참조
  name: deployment-manager
  apiGroup: rbac.authorization.k8s.io
```

같은 패턴으로 team-b Namespace에도 RoleBinding을 생성하면, team-a-devs는 team-a에서만, team-b-devs는 team-b에서만 Deployment를 관리할 수 있다. ClusterRole의 권한이 RoleBinding의 Namespace로 한정된다.

#### 2.3 RBAC 동사(Verbs) 상세

| 동사 | HTTP 메서드 | 설명 |
|------|-----------|------|
| `get` | GET (단일) | 특정 리소스 조회 |
| `list` | GET (목록) | 리소스 목록 조회 |
| `watch` | GET (스트림) | 리소스 변경 실시간 감시 |
| `create` | POST | 새 리소스 생성 |
| `update` | PUT | 리소스 전체 수정 |
| `patch` | PATCH | 리소스 부분 수정 |
| `delete` | DELETE | 리소스 삭제 |
| `deletecollection` | DELETE (목록) | 리소스 일괄 삭제 |

**주의사항**:

- `get`만 부여하고 `list`를 빼면, 리소스 이름을 정확히 알 때만 조회 가능하다. 보안 관점에서 유용하다.
- `watch`는 실시간 이벤트 스트림을 받는 권한이다. Operator나 Controller가 필요로 한다.
- `*` 와일드카드는 모든 동사를 의미한다. 최소 권한 원칙에 위배되므로 프로덕션에서 사용을 지양한다.

#### 2.4 기본 제공 ClusterRole

Kubernetes는 몇 가지 기본 ClusterRole을 제공한다:

| ClusterRole | 권한 | 용도 |
|-------------|------|------|
| `cluster-admin` | 모든 리소스에 대한 모든 동작 | 클러스터 관리자 전용 |
| `admin` | NS 내 대부분의 리소스 관리 (RBAC 제외) | NS 관리자 |
| `edit` | NS 내 리소스 읽기/쓰기 (Role/RoleBinding 제외) | 개발자 |
| `view` | NS 내 리소스 읽기 전용 | 조회 전용 사용자 |

```bash
# 기본 ClusterRole 확인
kubectl get clusterroles | grep -E "^(cluster-admin|admin|edit|view)"

# ClusterRole 상세 확인
kubectl describe clusterrole view
```

**위험**: `cluster-admin`을 일반 사용자에게 부여하면 안 된다. 이 권한은 Secrets 읽기, Node 삭제, Namespace 삭제 등 모든 작업이 가능하다. 프로덕션에서는 `cluster-admin`을 가진 주체를 최소한으로 유지하고, 필요한 권한만 가진 커스텀 ClusterRole을 만들어 사용한다.

---

### 3. ServiceAccount와 Pod 권한 제어

ServiceAccount는 Pod가 Kubernetes API 서버와 통신할 때 사용하는 ID이다. 사람(User)이 아닌 프로세스(Pod)에 권한을 부여하는 메커니즘이다.

#### 3.1 default ServiceAccount의 위험성

모든 Namespace에는 `default` ServiceAccount가 자동 생성된다. Pod에 명시적으로 ServiceAccount를 지정하지 않으면 `default` SA가 사용된다.

```bash
# default SA 확인
kubectl get sa -n default
# NAME      SECRETS   AGE
# default   0         30d
```

`default` SA 자체에는 큰 권한이 없지만, 문제는 다음과 같다:

1. **공유 SA**: 같은 Namespace의 모든 Pod가 동일한 `default` SA를 사용한다. 하나의 Pod에 RBAC 권한을 부여하면, 같은 Namespace의 모든 Pod가 그 권한을 가진다.
2. **토큰 자동 마운트**: Kubernetes는 기본적으로 SA 토큰을 Pod에 자동 마운트한다(`/var/run/secrets/kubernetes.io/serviceaccount/token`). 이 토큰으로 API 서버에 인증할 수 있다.
3. **권한 확대 위험**: 공격자가 Pod를 장악하면, 마운트된 토큰으로 API 서버에 요청을 보내 Secrets 조회, 다른 Pod 정보 수집 등을 시도할 수 있다.

#### 3.2 전용 ServiceAccount 생성

Pod마다 전용 SA를 생성하고 필요한 최소 권한만 부여하는 것이 보안 모범 사례이다.

```yaml
# 1. ServiceAccount 생성
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service-sa
  namespace: production
automountServiceAccountToken: false   # 토큰 자동 마운트 비활성화

---
# 2. 필요한 권한만 가진 Role 생성
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: order-service-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "watch"]
    resourceNames: ["order-config"]   # 특정 리소스만 허용
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["order-db-credentials"]

---
# 3. RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: order-service-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: order-service-sa
    namespace: production
roleRef:
  kind: Role
  name: order-service-role
  apiGroup: rbac.authorization.k8s.io

---
# 4. Pod에서 전용 SA 사용
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: order-service-sa
      automountServiceAccountToken: true   # 이 Pod만 토큰 마운트
      containers:
        - name: order-service
          image: order-service:v1.0
```

핵심은 `resourceNames` 필드이다. 이를 사용하면 "모든 Secrets"가 아닌 "order-db-credentials라는 이름의 Secret만" 접근할 수 있도록 세밀하게 제어한다.

#### 3.3 토큰 자동 마운트 비활성화

API 서버와 통신할 필요가 없는 Pod(대부분의 애플리케이션)는 SA 토큰을 마운트할 이유가 없다. 토큰이 마운트되어 있으면 공격 표면이 넓어진다.

```yaml
# SA 수준에서 비활성화 (이 SA를 사용하는 모든 Pod에 적용)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: no-api-access-sa
automountServiceAccountToken: false

# 또는 Pod 수준에서 비활성화
spec:
  automountServiceAccountToken: false
  containers:
    - name: app
      image: my-app:v1.0
```

SA 수준에서 `false`로 설정하고, API 접근이 필요한 Pod에서만 `true`로 오버라이드하는 패턴이 권장된다.

---

### 4. Pod Security Standards

Pod Security Standards(PSS)는 Pod의 보안 설정을 제어하는 Kubernetes 내장 기능이다. Kubernetes 1.25부터 Pod Security Admission(PSA)이 GA가 되었으며, 이전의 PodSecurityPolicy(PSP)를 대체한다.

#### 4.1 세 가지 보안 수준

| 수준 | 설명 | 허용 범위 |
|------|------|----------|
| **Privileged** | 제한 없음 | 모든 설정 허용 (hostNetwork, hostPID, 특권 컨테이너 등) |
| **Baseline** | 최소한의 제한 | 알려진 권한 상승 벡터 차단 (hostNetwork 금지, 특권 컨테이너 금지) |
| **Restricted** | 강력한 제한 | 최소 권한 강제 (root 실행 금지, 볼륨 타입 제한, seccomp 필수) |

각 수준에서 제한하는 항목을 구체적으로 살펴보면:

**Baseline이 차단하는 것**:
- `hostNetwork: true` (Pod가 노드의 네트워크 네임스페이스를 공유)
- `hostPID: true` (Pod가 노드의 PID 네임스페이스를 공유)
- `hostIPC: true` (Pod가 노드의 IPC 네임스페이스를 공유)
- `privileged: true` (컨테이너가 노드의 모든 디바이스에 접근)
- 위험한 Capabilities (NET_RAW, SYS_ADMIN 등)
- `/proc` 마운트 타입 변경

**Restricted가 추가로 강제하는 것**:
- `runAsNonRoot: true` (root가 아닌 사용자로 실행)
- `allowPrivilegeEscalation: false` (setuid 바이너리로 권한 상승 금지)
- `readOnlyRootFilesystem: true` (루트 파일시스템 읽기 전용, 권장)
- `seccompProfile: RuntimeDefault` (시스템 콜 제한)
- 볼륨 타입 제한 (configMap, downwardAPI, emptyDir, persistentVolumeClaim, projected, secret만 허용)
- Capabilities 제거 (`drop: ["ALL"]`)

#### 4.2 Namespace에 PSS 적용

PSA는 Namespace 라벨로 적용한다. 세 가지 모드를 조합할 수 있다:

| 모드 | 동작 |
|------|------|
| `enforce` | 위반 시 Pod 생성 거부 |
| `audit` | 위반 시 감사 로그에 기록 (Pod 생성은 허용) |
| `warn` | 위반 시 사용자에게 경고 메시지 (Pod 생성은 허용) |

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**점진적 적용 전략**:

처음부터 `enforce: restricted`를 적용하면 기존 워크로드가 일괄 거부될 수 있다. 단계적으로 적용한다:

```
1단계: audit + warn만 설정 → 위반 워크로드 파악
2단계: 위반 워크로드 수정 (runAsNonRoot, drop capabilities 등)
3단계: enforce 적용
```

```bash
# 1단계: 감사 + 경고만 (Pod 생성은 허용)
kubectl label namespace production \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted

# 감사 로그에서 위반 확인
kubectl get events -n production | grep Warning

# 3단계: 강제 적용
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted
```

#### 4.3 Restricted 수준을 만족하는 Pod 예시

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: my-app:v1.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
      resources:
        requests:
          memory: "256Mi"
          cpu: "250m"
        limits:
          memory: "512Mi"
          cpu: "500m"
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: config
          mountPath: /etc/app
          readOnly: true
  volumes:
    - name: tmp
      emptyDir: {}          # 쓰기 가능한 임시 디렉토리
    - name: config
      configMap:
        name: app-config
```

`readOnlyRootFilesystem: true`를 설정하면 컨테이너의 루트 파일시스템이 읽기 전용이 된다. 애플리케이션이 임시 파일을 쓸 필요가 있으면 `emptyDir` 볼륨을 `/tmp`에 마운트한다.

---

### 5. NetworkPolicy로 Pod 간 트래픽 제어

NetworkPolicy는 Kubernetes에서 Pod 간 네트워크 트래픽을 제어하는 방화벽 규칙이다. 중요한 사실은, **NetworkPolicy가 없으면 기본적으로 모든 트래픽이 허용된다**는 것이다.

#### 5.1 왜 기본이 Allow-All인가

Kubernetes의 네트워크 모델은 "모든 Pod는 다른 모든 Pod와 통신할 수 있다"를 전제로 설계되었다. 이는 Kubernetes 초기에 마이크로서비스 간 자유로운 통신을 위해 의도된 설계이다. 하지만 보안 관점에서는 위험하다:

```
NetworkPolicy 없을 때:
  Frontend Pod ──→ Backend Pod    ✅ (정상)
  Frontend Pod ──→ Database Pod   ✅ (위험! Frontend가 DB에 직접 접근)
  Backend Pod  ──→ Database Pod   ✅ (정상)
  Random Pod   ──→ Database Pod   ✅ (위험! 아무 Pod가 DB 접근)

NetworkPolicy 적용 후:
  Frontend Pod ──→ Backend Pod    ✅ (허용)
  Frontend Pod ──→ Database Pod   ❌ (차단)
  Backend Pod  ──→ Database Pod   ✅ (허용)
  Random Pod   ──→ Database Pod   ❌ (차단)
```

#### 5.2 NetworkPolicy 기본 구조

NetworkPolicy는 다음 요소로 구성된다:

- **podSelector**: 이 정책이 적용될 Pod를 선택한다.
- **policyTypes**: Ingress(들어오는 트래픽), Egress(나가는 트래픽) 또는 둘 다.
- **ingress**: 허용할 인바운드 트래픽 규칙.
- **egress**: 허용할 아웃바운드 트래픽 규칙.

#### 5.3 실무 시나리오: 3-Tier 아키텍처 보안

Frontend → Backend → Database 구조에서 NetworkPolicy를 적용하는 예시이다.

**1단계: Default Deny (모든 트래픽 차단)**

```yaml
# 모든 Ingress 차단
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}        # 빈 셀렉터 = Namespace의 모든 Pod
  policyTypes:
    - Ingress            # Ingress 정책 적용 (아무 규칙 없음 = 모두 차단)

---
# 모든 Egress 차단
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

**2단계: 필요한 트래픽만 허용**

```yaml
# Frontend: 외부에서 80 포트 접근 허용, Backend로만 요청 가능
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from: []            # 모든 소스에서 허용 (외부 트래픽)
      ports:
        - port: 80
          protocol: TCP
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: backend
      ports:
        - port: 8080
          protocol: TCP
    - to:                 # DNS 허용 (필수!)
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

같은 패턴으로 Backend(Frontend에서만 Ingress 허용, Database로만 Egress 허용)와 Database(Backend에서만 Ingress 허용) NetworkPolicy를 각각 작성한다.

**중요**: Egress 정책을 설정할 때 DNS(포트 53) 트래픽을 반드시 허용해야 한다. DNS를 차단하면 Service 이름으로의 통신이 불가능해진다.

#### 5.4 CNI 플러그인과 NetworkPolicy

NetworkPolicy는 Kubernetes API의 일부이지만, 실제 트래픽 제어는 CNI(Container Network Interface) 플러그인이 수행한다. 모든 CNI가 NetworkPolicy를 지원하는 것은 아니다:

| CNI 플러그인 | NetworkPolicy 지원 |
|-------------|-------------------|
| **Calico** | ✅ (완전 지원 + 확장 기능) |
| **Cilium** | ✅ (완전 지원 + L7 정책) |
| **Weave Net** | ✅ (기본 지원) |
| **Flannel** | ❌ (미지원) |
| **AWS VPC CNI** | ❌ (기본), ✅ (Calico 추가 시) |

minikube에서 NetworkPolicy를 테스트하려면 Calico CNI를 사용해야 한다:

```bash
minikube start --cni=calico
```

---

### 6. Secrets 관리 전략

Kubernetes Secrets는 비밀번호, API 키, TLS 인증서 등 민감 데이터를 저장하는 리소스이다. 하지만 기본 Secrets에는 근본적인 보안 한계가 있다.

#### 6.1 base64의 한계: 인코딩 ≠ 암호화

Kubernetes Secrets의 데이터는 base64로 인코딩되어 저장된다. base64는 **인코딩**이지 **암호화**가 아니다. 누구나 쉽게 디코딩할 수 있다:

```bash
# Secret 생성
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=SuperSecret123

# Secret 조회 (base64 인코딩 상태)
kubectl get secret db-credentials -o yaml
# data:
#   username: YWRtaW4=
#   password: U3VwZXJTZWNyZXQxMjM=

# base64 디코딩 (누구나 가능)
echo "U3VwZXJTZWNyZXQxMjM=" | base64 --decode
# SuperSecret123
```

이것은 Secrets에 대한 `get` 권한을 가진 사용자가 모든 비밀번호를 평문으로 확인할 수 있다는 의미이다. 또한 etcd에 저장될 때도 기본적으로 평문(base64 인코딩)이므로, etcd 백업 파일이나 etcd에 직접 접근하면 모든 Secrets가 노출된다.

#### 6.2 etcd 암호화 (Encryption at Rest)

Kubernetes는 etcd에 저장되는 데이터를 암호화하는 기능을 제공한다:

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}   # 암호화되지 않은 기존 Secrets 읽기 용
```

이 설정을 kube-apiserver에 `--encryption-provider-config` 플래그로 전달하면, 새로 생성되는 Secrets가 AES-CBC로 암호화되어 etcd에 저장된다. 하지만 이 방식의 한계는 암호화 키를 kube-apiserver가 관리한다는 것이다. 키 순환(rotation)이 수동이며, 키가 API 서버 노드에 평문으로 존재한다.

#### 6.3 Sealed Secrets

Bitnami의 Sealed Secrets는 Git에 안전하게 커밋할 수 있는 암호화된 Secret을 제공한다:

```
일반 Secret (Git에 커밋 불가):
  apiVersion: v1
  kind: Secret
  data:
    password: U3VwZXJTZWNyZXQxMjM=   # base64, 누구나 디코딩 가능

Sealed Secret (Git에 커밋 가능):
  apiVersion: bitnami.com/v1alpha1
  kind: SealedSecret
  spec:
    encryptedData:
      password: AgBy3i4OJSWK+P...    # 비대칭 암호화, 클러스터 키 없이 복호화 불가
```

동작 원리:

1. 클러스터에 Sealed Secrets Controller를 설치한다. Controller가 RSA 키 쌍을 생성한다.
2. `kubeseal` CLI로 일반 Secret을 SealedSecret으로 변환한다(공개키로 암호화).
3. SealedSecret YAML을 Git에 커밋한다.
4. 클러스터에서 Sealed Secrets Controller가 SealedSecret을 복호화하여 일반 Secret을 생성한다(비밀키 사용).

```bash
# Sealed Secrets 설치
helm install sealed-secrets sealed-secrets/sealed-secrets \
  -n kube-system

# Secret → SealedSecret 변환
kubectl create secret generic db-creds \
  --from-literal=password=SuperSecret123 \
  --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-db-creds.yaml

# SealedSecret 적용 (Controller가 자동으로 Secret 생성)
kubectl apply -f sealed-db-creds.yaml
```

#### 6.4 External Secrets Operator (ESO)

External Secrets Operator는 외부 비밀 관리 시스템(AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, Azure Key Vault)과 Kubernetes Secrets를 동기화한다:

```
외부 시스템 (AWS Secrets Manager, Vault 등)
  ↓ 동기화
External Secrets Operator
  ↓ Secret 생성
Kubernetes Secret (자동 생성, 자동 갱신)
  ↓ 마운트
Pod
```

```yaml
# ExternalSecret 정의 (어떤 Secret을 동기화할지)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  refreshInterval: 1h              # 1시간마다 외부 시스템과 동기화
  secretStoreRef:
    name: aws-secrets-manager      # SecretStore CR 참조
    kind: SecretStore
  target:
    name: db-credentials           # 생성될 Kubernetes Secret 이름
  data:
    - secretKey: password
      remoteRef:
        key: production/db/credentials
        property: password
```

SecretStore CR은 외부 시스템(AWS Secrets Manager, Vault 등)의 연결 정보를 정의하고, ExternalSecret CR은 어떤 비밀을 동기화할지 지정한다.

**Sealed Secrets vs External Secrets Operator**:

| 항목 | Sealed Secrets | External Secrets Operator |
|------|---------------|--------------------------|
| **비밀 저장 위치** | Git (암호화된 YAML) | 외부 시스템 (Vault, AWS 등) |
| **키 관리** | 클러스터 내 RSA 키 | 외부 시스템이 관리 |
| **자동 갱신** | ❌ (SealedSecret 재생성 필요) | ✅ (`refreshInterval`로 자동) |
| **복잡도** | 낮음 (단순한 구조) | 높음 (외부 시스템 필요) |
| **키 순환** | 수동 | 외부 시스템의 순환 정책 |
| **적합한 상황** | 소규모 팀, GitOps 중심 | 대규모 조직, 기존 Vault 사용 |

---

### 7. 실무 시나리오: 개발자에게 특정 Namespace만 접근 허용

실제 기업 환경에서 자주 발생하는 시나리오를 RBAC으로 해결한다.

**요구사항**: 개발팀 A는 `team-a` Namespace에서만 작업 가능. 다른 Namespace는 조회만 가능. 클러스터 수준 리소스(Node, PV)는 조회만 가능. Secrets는 접근 불가.

```yaml
# 1. team-a NS에서 대부분의 작업 가능 (Secrets 제외)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: team-a-developer
  namespace: team-a
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "statefulsets", "daemonsets", "replicasets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["pods", "pods/log", "pods/exec", "services", "configmaps"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["get", "list", "watch"]
  # Secrets 접근 없음! (명시적으로 포함하지 않음)
```

이 Role을 RoleBinding으로 `team-a-devs` 그룹에 바인딩한다. 다른 Namespace 조회는 기본 제공 `view` ClusterRole을 ClusterRoleBinding으로 부여한다. `view`에는 Secrets 조회 권한이 포함되어 있지 않으므로 Secrets는 보호된다.

#### 7.1 RBAC 디버깅

```bash
# 특정 사용자의 권한 확인
kubectl auth can-i get pods --as developer@example.com -n team-a
# yes

kubectl auth can-i get secrets --as developer@example.com -n team-a
# no

kubectl auth can-i delete nodes --as developer@example.com
# no

# ServiceAccount의 권한 확인
kubectl auth can-i get pods \
  --as system:serviceaccount:production:order-service-sa \
  -n production
# yes

# 전체 권한 목록 확인
kubectl auth can-i --list --as developer@example.com -n team-a
```

---

### 8. Audit Log로 활동 추적

Kubernetes Audit Log는 API 서버에 대한 모든 요청을 기록한다. "누가, 언제, 무엇을, 어디서" 했는지를 추적할 수 있다.

#### 8.1 Audit Policy 설정

Audit Policy는 어떤 이벤트를 어느 수준으로 기록할지 정의한다:

```yaml
# /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Secrets 접근은 Metadata 수준으로 기록 (본문 제외)
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets"]

  # 인증 관련 이벤트는 상세 기록
  - level: RequestResponse
    resources:
      - group: "rbac.authorization.k8s.io"
        resources: ["clusterroles", "clusterrolebindings", "roles", "rolebindings"]

  # 워크로드 변경은 Request 수준
  - level: Request
    resources:
      - group: "apps"
        resources: ["deployments", "statefulsets"]
    verbs: ["create", "update", "patch", "delete"]

  # 읽기 작업은 최소 기록
  - level: None
    verbs: ["get", "list", "watch"]
    resources:
      - group: ""
        resources: ["events", "endpoints"]

  # 그 외 모든 요청은 Metadata
  - level: Metadata
```

**Audit Level**:

| 수준 | 기록 내용 |
|------|----------|
| `None` | 기록하지 않음 |
| `Metadata` | 요청 메타데이터(누가, 언제, 무엇을) |
| `Request` | Metadata + 요청 본문 |
| `RequestResponse` | Request + 응답 본문 |

#### 8.2 Audit Log 분석

Audit Log의 각 이벤트에는 `user`(누가), `verb`(무엇을), `requestURI`(어디에), `responseStatus`(결과), `requestReceivedTimestamp`(언제)가 포함된다. 예를 들어 `developer@example.com`이 `production` NS의 `db-credentials` Secret을 조회 시도하여 403 Forbidden이 반환된 기록이 남으면, RBAC이 정상 동작하고 있음을 확인할 수 있다. 반대로 200 OK가 반환되었다면 해당 사용자에게 불필요한 Secrets 접근 권한이 있다는 위험 신호이다.

Audit Log는 보안 인시던트 조사, 컴플라이언스 감사, 이상 행동 탐지에 필수적인 데이터를 제공한다.

---

### 9. 설계 원칙과 핵심 명령어

#### 9.1 최소 권한 원칙 체크리스트

```
□ 1. cluster-admin은 긴급 상황 전용 계정으로만 사용
□ 2. 모든 Pod에 전용 ServiceAccount 부여 (default SA 사용 금지)
□ 3. API 접근 불필요한 Pod는 automountServiceAccountToken: false
□ 4. Role의 resources/verbs에 와일드카드(*) 사용 금지
□ 5. 가능하면 resourceNames로 특정 리소스만 접근 허용
□ 6. ClusterRole보다 Role 우선 사용 (Namespace 격리)
□ 7. Namespace별 default-deny NetworkPolicy 적용
□ 8. Secrets 접근 권한은 별도로 관리 (view ClusterRole에 포함 안 됨)
```

#### 9.2 핵심 명령어

```bash
# === RBAC ===
kubectl get roles,rolebindings -n <namespace>
kubectl get clusterroles,clusterrolebindings
kubectl auth can-i <verb> <resource> --as <user> -n <namespace>
kubectl auth can-i --list --as <user> -n <namespace>

# === ServiceAccount ===
kubectl get sa -n <namespace>
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.serviceAccountName}{"\n"}{end}'

# === Pod Security / NetworkPolicy / Secrets ===
kubectl get ns --show-labels | grep pod-security
kubectl label namespace <ns> pod-security.kubernetes.io/enforce=restricted
kubectl get networkpolicy -n <namespace>
kubectl get secret <name> -n <namespace> -o jsonpath='{.data.password}' | base64 -d

# === 보안 점검 ===
kubectl get clusterrolebindings -o json | jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[]'
kubectl get roles,clusterroles -A -o json | jq '.items[] | select(.rules[]?.verbs[]? == "*") | .metadata.name'
```

---

### 참고 자료

- [Kubernetes RBAC 공식 문서](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [External Secrets Operator](https://external-secrets.io/)
- [Kubernetes Audit](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
