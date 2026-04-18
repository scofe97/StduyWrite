# Ch17: RBAC & Security 점검 질문

> 이 질문들은 Ch17 LEARN.md의 핵심 개념을 점검하기 위한 것이다. 각 질문의 핵심 포인트를 먼저 읽고, 심화 질문으로 이해의 깊이를 확인한다.

---

## Q1: Role과 ClusterRole의 차이, 언제 어떤 것을 사용하는가?

**질문**: Role과 ClusterRole은 모두 RBAC 권한을 정의하지만, 적용 범위가 다르다. 각각의 사용 시점과, ClusterRole을 RoleBinding으로 바인딩하는 패턴은 왜 존재하는가?

**핵심 포인트**:

- **Role은 Namespace-scoped**이다. `metadata.namespace`에 지정된 Namespace 내의 리소스에 대한 권한만 정의할 수 있다. 예를 들어 `development` Namespace의 Pod 조회 권한은 Role로 정의한다. Role은 해당 Namespace에서만 유효하며, 다른 Namespace의 리소스에는 영향을 미치지 않는다. 이는 팀별, 환경별(dev/staging/prod) 권한 격리에 적합하다.

- **ClusterRole은 Cluster-scoped**이다. 두 가지 경우에 사용한다. 첫째, Node, PersistentVolume, Namespace 같은 클러스터 범위 리소스는 Role로 정의할 수 없으므로 ClusterRole이 필수이다. 둘째, 여러 Namespace에서 동일한 권한을 재사용하고 싶을 때 ClusterRole을 한 번 정의하고 Namespace별로 RoleBinding을 생성하는 패턴을 사용한다.

- **ClusterRole + RoleBinding 재사용 패턴**: 이 패턴이 존재하는 이유는 DRY(Don't Repeat Yourself) 원칙 때문이다. 10개 Namespace에서 동일한 "Deployment 관리" 권한이 필요하면, Role을 10개 만드는 대신 ClusterRole을 1개 만들고 RoleBinding을 10개 생성한다. ClusterRole의 권한이 RoleBinding의 Namespace로 한정되므로, ClusterRoleBinding으로 바인딩하는 것보다 안전하다.

- **위험한 패턴**: ClusterRole + ClusterRoleBinding으로 `edit` 이상의 권한을 부여하면, 해당 주체가 모든 Namespace의 리소스를 수정할 수 있다. 이는 멀티테넌트 환경에서 심각한 보안 위험이 된다. "모든 Namespace에서 작업 가능한 사용자"가 필요한 경우에만 ClusterRoleBinding을 사용하고, 그 외에는 항상 RoleBinding을 사용하는 것이 원칙이다.

- **기본 제공 ClusterRole 활용**: Kubernetes가 제공하는 `view`, `edit`, `admin` ClusterRole은 잘 설계된 권한 세트이다. 커스텀 Role을 만들기 전에 이 기본 ClusterRole이 요구사항을 충족하는지 먼저 확인한다. 특히 `view`는 Secrets 조회 권한을 포함하지 않으므로 안전하게 사용할 수 있다.

**심화 질문**: ClusterRole에 `aggregationRule`을 설정하면 여러 ClusterRole을 하나로 합칠 수 있다. 이 기능은 어떤 상황에서 유용하며, Operator가 CRD에 대한 RBAC 권한을 자동으로 추가할 때 어떻게 활용되는가?

---

## Q2: default ServiceAccount의 위험성과 전용 SA 생성 이유

**질문**: 모든 Namespace에 자동 생성되는 default ServiceAccount는 어떤 위험을 초래하며, 왜 Pod마다 전용 ServiceAccount를 생성해야 하는가?

**핵심 포인트**:

- **공유 ID의 문제**: default SA는 Namespace 내 모든 Pod가 공유하는 단일 ID이다. Pod A에 RBAC 권한을 부여하기 위해 default SA에 RoleBinding을 추가하면, 같은 Namespace의 Pod B, Pod C, 미래에 생성될 모든 Pod가 동일한 권한을 가진다. 이는 최소 권한 원칙을 위배하며, 하나의 Pod가 침해되면 같은 권한으로 다른 리소스에 접근할 수 있는 횡적 이동(Lateral Movement)의 통로가 된다.

- **토큰 자동 마운트**: Kubernetes는 기본적으로 Pod에 SA 토큰을 자동 마운트한다(`/var/run/secrets/kubernetes.io/serviceaccount/token`). 이 토큰은 API 서버에 인증하는 Bearer Token이다. 대부분의 애플리케이션은 Kubernetes API와 통신할 필요가 없지만, 토큰이 마운트되어 있으면 공격자가 이를 탈취하여 API 서버에 요청을 보낼 수 있다. 컨테이너 내부에서 `curl -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces/`를 실행하면 API 서버에 접근 가능하다.

- **전용 SA의 이점**: Pod별 전용 SA를 생성하면 (1) 각 Pod에 필요한 최소 권한만 부여할 수 있고, (2) Audit Log에서 어떤 Pod(SA)가 어떤 API를 호출했는지 추적할 수 있으며, (3) `automountServiceAccountToken: false`로 API 접근이 불필요한 Pod의 토큰 마운트를 비활성화할 수 있다.

- **Operator/Controller의 SA**: Operator나 Custom Controller처럼 Kubernetes API에 접근해야 하는 Pod는 전용 SA에 정확히 필요한 리소스(특정 CRD, 특정 동사)에 대한 권한만 부여한다. 예를 들어 Redpanda Operator의 SA는 Redpanda CRD, StatefulSet, Service, ConfigMap에 대한 권한만 가지며, 다른 리소스(Secrets, Node 등)에는 접근하지 않는다.

- **Token 수명 관리**: Kubernetes 1.22부터 Bound Service Account Token(TokenRequest API)이 기본이다. 토큰에 만료 시간(기본 1시간), 대상 API 서버(audience), 바인딩된 Pod 정보가 포함된다. Pod가 삭제되면 토큰도 무효화된다. 이전의 non-expiring Secret-based 토큰보다 보안이 강화되었다.

**심화 질문**: Kubernetes 1.24부터 SA의 Secret이 자동 생성되지 않는다. 외부 시스템(CI/CD, 모니터링 도구)이 장기 토큰이 필요한 경우 어떻게 해야 하는가? TokenRequest API와 Secret-based 토큰의 보안 차이는 무엇인가?

---

## Q3: NetworkPolicy가 없으면 기본적으로 모든 트래픽이 허용되는 이유

**질문**: Kubernetes에서 NetworkPolicy가 없으면 모든 Pod 간 통신이 허용된다. 이것이 의도된 설계라면 왜 그렇게 결정되었으며, 보안 관점에서 어떻게 대응해야 하는가?

**핵심 포인트**:

- **Kubernetes 네트워크 모델의 원칙**: Kubernetes는 "모든 Pod는 NAT 없이 다른 모든 Pod와 통신할 수 있어야 한다"를 기본 네트워크 모델로 정의한다(Kubernetes Network Model). 이는 마이크로서비스 아키텍처에서 서비스 간 자유로운 통신을 위해 설계된 것이다. Docker의 브릿지 네트워크에서 컨테이너 간 통신을 위해 포트 매핑이 필요했던 불편함을 해소하기 위한 결정이다.

- **"기본 허용(Default Allow)"의 의미**: NetworkPolicy가 하나도 없는 Namespace에서는 모든 인바운드/아웃바운드 트래픽이 허용된다. 이는 방화벽의 "default allow" 정책과 같다. 새로운 Pod를 배포하면 즉시 다른 모든 Pod와 통신할 수 있으므로 개발 편의성은 높지만, 보안 경계가 없다는 의미이다.

- **NetworkPolicy의 동작 모델**: NetworkPolicy가 Pod에 적용되는 순간, 해당 Pod는 "default deny" 모드로 전환된다. NetworkPolicy에 명시된 트래픽만 허용되고 나머지는 모두 차단된다. 이것이 중요한 개념이다 - NetworkPolicy는 "허용 목록(whitelist)"이지, "차단 목록(blacklist)"이 아니다. 특정 트래픽을 차단하는 것이 아니라, 허용할 트래픽을 명시하는 것이다.

- **default-deny 정책의 필요성**: 보안 모범 사례는 Namespace에 default-deny NetworkPolicy를 먼저 적용하고, 필요한 트래픽만 추가로 허용하는 것이다. `podSelector: {}`(빈 셀렉터)는 Namespace의 모든 Pod에 적용되며, Ingress/Egress 규칙이 없으면 모든 트래픽이 차단된다.

- **CNI 의존성**: NetworkPolicy는 Kubernetes API의 일부이지만, 실제 트래픽 제어는 CNI 플러그인이 수행한다. Flannel 같은 단순한 CNI는 NetworkPolicy를 무시하므로, `kubectl apply`해도 실제로 트래픽이 차단되지 않는다. Calico, Cilium 등 NetworkPolicy를 지원하는 CNI를 사용해야 한다. 이 불일치가 실무에서 보안 사고의 원인이 되기도 한다.

- **DNS 예외 처리**: Egress deny를 적용할 때 DNS(UDP/TCP 53) 트래픽을 반드시 허용해야 한다. DNS가 차단되면 Service 이름으로의 통신이 불가능해지고, Pod가 외부 서비스에도 접근하지 못한다. 이는 NetworkPolicy 적용 시 가장 흔한 실수이다.

**심화 질문**: Cilium의 L7 NetworkPolicy는 HTTP 메서드와 경로 기반으로 트래픽을 제어할 수 있다(예: "GET /api/health만 허용"). 이것이 기본 NetworkPolicy(L3/L4)와 어떻게 다르며, Service Mesh(Istio)의 Authorization Policy와는 어떤 관계인가?

---

## Q4: Secrets의 base64 인코딩이 "보안"이 아닌 이유

**질문**: Kubernetes Secrets는 base64로 데이터를 저장한다. base64가 보안을 제공하지 않는다면, Kubernetes는 왜 이 방식을 채택했으며, 실제로 Secrets를 안전하게 관리하려면 어떤 추가 조치가 필요한가?

**핵심 포인트**:

- **base64는 인코딩이지 암호화가 아니다**: base64는 바이너리 데이터를 텍스트로 변환하는 인코딩 방식이다. 키 없이도 누구나 `base64 --decode`로 원본 데이터를 복원할 수 있다. Kubernetes가 base64를 사용하는 이유는 보안이 아니라, YAML/JSON에 바이너리 데이터(TLS 인증서 등)를 안전하게 포함하기 위함이다. 예를 들어 TLS 인증서의 바이너리 바이트를 YAML 문자열로 직접 넣으면 인코딩 오류가 발생하지만, base64로 변환하면 안전한 ASCII 문자열이 된다.

- **etcd 저장 시 기본 평문**: Kubernetes의 모든 리소스는 etcd에 저장된다. Secrets도 마찬가지이며, 기본 설정에서는 base64 인코딩된 상태(즉, 사실상 평문)로 etcd에 저장된다. etcd 백업 파일에 접근하거나, etcd API에 직접 접근하면 모든 Secrets를 읽을 수 있다. 이를 방지하려면 EncryptionConfiguration으로 etcd 암호화(Encryption at Rest)를 활성화해야 한다.

- **RBAC과의 조합**: Secrets에 대한 `get` 권한을 가진 주체는 base64 디코딩으로 모든 비밀 데이터를 볼 수 있다. 따라서 RBAC에서 Secrets 접근 권한은 매우 신중하게 부여해야 한다. 기본 제공 `view` ClusterRole은 의도적으로 Secrets 조회 권한을 제외하고 있다. `edit`와 `admin` ClusterRole에는 Secrets 권한이 포함되어 있으므로 주의가 필요하다.

- **Git 노출 위험**: Secret YAML 파일을 Git에 커밋하면 base64 디코딩만으로 비밀번호가 노출된다. Git 히스토리에서 삭제하더라도 `git reflog`으로 복구할 수 있다. Sealed Secrets나 External Secrets Operator는 이 문제를 해결하기 위해 만들어졌다. Sealed Secrets는 비대칭 암호화로 Git에 안전하게 커밋할 수 있는 형태로 변환하고, ESO는 비밀 데이터를 외부 시스템(Vault, AWS Secrets Manager)에 보관하고 클러스터에서 동기화한다.

- **실질적 보안 계층**: Secrets를 안전하게 관리하려면 여러 계층의 보안을 조합해야 한다. (1) RBAC으로 접근 제한, (2) etcd 암호화로 저장 시 보호, (3) Sealed Secrets/ESO로 Git 노출 방지, (4) Audit Log로 접근 추적, (5) Pod에서 Secrets를 환경 변수가 아닌 볼륨으로 마운트(환경 변수는 `kubectl describe pod`로 노출 가능).

**심화 질문**: Kubernetes 1.27부터 도입된 `ValidatingAdmissionPolicy`를 사용하면 "Secrets를 환경 변수로 사용하는 Pod 생성을 거부"하는 정책을 만들 수 있다. 이 정책을 어떻게 구현하며, OPA Gatekeeper와 비교했을 때 장단점은 무엇인가?

---

## Q5: Pod Security Standards의 3단계 적용 전략

**질문**: Pod Security Standards의 Privileged, Baseline, Restricted 수준을 실제 클러스터에 적용할 때, 어떤 순서와 전략으로 도입해야 하는가? 기존 워크로드를 깨지 않으면서 보안을 강화하려면 어떻게 해야 하는가?

**핵심 포인트**:

- **Privileged는 예외적 상황 전용이다**: Privileged 수준은 아무런 제한이 없으므로 사실상 "보안 없음"과 같다. 이 수준이 필요한 워크로드는 호스트 네트워크/PID가 필요한 CNI 플러그인(Calico, Cilium), 노드 수준 로그 수집기(Fluent Bit DaemonSet), 스토리지 드라이버(CSI Node Plugin) 등이다. 이러한 시스템 워크로드는 `kube-system` Namespace에 배치하고, `kube-system`만 Privileged로 설정한다.

- **Baseline은 합리적인 최소 기준이다**: Baseline은 알려진 권한 상승 경로(hostNetwork, privileged container, dangerous capabilities)를 차단하면서, 대부분의 일반 애플리케이션이 수정 없이 통과할 수 있다. 새로운 Namespace를 생성할 때 기본으로 Baseline enforce를 적용하면, 명백히 위험한 설정만 차단하면서 개발 편의성을 유지할 수 있다.

- **Restricted는 프로덕션 목표이다**: Restricted는 `runAsNonRoot`, `drop: ["ALL"]`, `readOnlyRootFilesystem`, `seccompProfile` 등을 강제한다. 많은 기존 컨테이너 이미지가 root로 실행되거나, 특정 capabilities를 요구하므로, 기존 워크로드에 즉시 적용하면 Pod 생성이 거부될 수 있다. 따라서 점진적 접근이 필수이다.

- **점진적 적용 전략**: (1) 모든 Namespace에 `audit: restricted` + `warn: restricted`를 먼저 적용한다. Pod 생성은 허용하면서 위반 사항을 로그와 경고로 수집한다. (2) 위반 워크로드를 분석하고 수정한다. Dockerfile에서 `USER nonroot`를 추가하고, Pod spec에 `securityContext`를 설정한다. (3) 수정이 완료된 Namespace부터 `enforce: restricted`를 적용한다. (4) 수정이 어려운 서드파티 워크로드(Helm 차트 등)는 별도 Namespace에 Baseline으로 격리한다.

- **Namespace 분류 패턴**: 실무에서는 Namespace를 보안 수준별로 분류한다. `kube-system`(Privileged), `monitoring`/`logging`(Baseline, 호스트 접근 필요), `production`(Restricted), `staging`(Restricted), `development`(Baseline 또는 Restricted). 이 분류를 Namespace 라벨로 관리하고, GitOps로 일관되게 적용한다.

- **예외 처리**: Restricted를 enforce하는 Namespace에서 일부 Pod만 예외가 필요한 경우, PSA 자체에는 Pod 단위 예외 기능이 없다. 대신 해당 Pod를 별도의 Baseline Namespace로 분리하거나, 런타임 보안 도구(Kyverno, OPA Gatekeeper)를 사용하여 더 세밀한 정책을 적용한다.

**심화 질문**: PodSecurityPolicy(PSP)에서 Pod Security Admission(PSA)으로 마이그레이션할 때, PSP의 `MustRunAs`, `MustRunAsNonRoot` 같은 세밀한 정책을 PSA에서는 어떻게 구현하는가? PSA의 3단계 모델로 부족한 경우 Kyverno나 OPA Gatekeeper를 조합하는 전략은 무엇인가?

---

## Q6: RBAC 설계에서 가장 흔한 실수와 방지 방법

**질문**: 실무에서 RBAC을 설계할 때 자주 발생하는 실수는 무엇이며, 각 실수가 어떤 보안 위험을 초래하는가?

**핵심 포인트**:

- **cluster-admin 남용**: "편의를 위해" 모든 개발자에게 cluster-admin을 부여하는 경우가 가장 위험하다. cluster-admin은 모든 Namespace의 모든 리소스에 대한 모든 동작이 가능하므로, 실수로 프로덕션 Namespace의 Deployment를 삭제하거나, 다른 팀의 Secrets를 읽을 수 있다. 방지: cluster-admin은 긴급 대응 계정(break-glass account)으로만 사용하고, 개발자에게는 Namespace 범위의 edit 또는 커스텀 Role을 부여한다.

- **와일드카드 권한**: `resources: ["*"]`, `verbs: ["*"]`를 사용하면 모든 리소스에 대한 모든 동작이 허용된다. 새로운 CRD가 추가되어도 자동으로 권한이 부여되므로 예상치 못한 접근이 발생한다. 방지: 필요한 리소스와 동사를 명시적으로 나열한다. 코드 리뷰에서 와일드카드를 발견하면 반드시 구체적 리소스로 대체한다.

- **default SA에 권한 부여**: "이 Pod에 API 접근 권한이 필요하다"고 해서 default SA에 RoleBinding을 추가하면, 같은 Namespace의 모든 Pod가 그 권한을 가진다. 방지: 항상 전용 SA를 생성하고, 해당 SA에만 RoleBinding을 추가한다.

- **Secrets 접근 권한 무분별 부여**: 개발자에게 `edit` ClusterRole을 ClusterRoleBinding으로 부여하면, 모든 Namespace의 Secrets(DB 비밀번호, API 키, TLS 인증서)를 읽을 수 있다. 방지: `edit`는 RoleBinding으로 특정 Namespace에만 부여하고, Secrets 접근이 불필요한 경우 커스텀 Role에서 Secrets를 제외한다.

- **미사용 RoleBinding 방치**: 팀원이 퇴사하거나 프로젝트가 종료되어도 RoleBinding이 남아 있으면 불필요한 접근 경로가 유지된다. 방지: 분기별로 RoleBinding을 감사하고, Audit Log에서 실제 사용 여부를 확인하여 미사용 바인딩을 정리한다.

- **escalate/bind 동사 무시**: `escalate`와 `bind` 동사는 RBAC 자체를 수정할 수 있는 권한이다. 이 동사를 가진 주체는 자신의 권한을 상승시킬 수 있다. 방지: `escalate`, `bind`, `impersonate` 동사는 클러스터 관리자에게만 부여한다.

**심화 질문**: RBAC 정책이 수백 개로 늘어나면 "어떤 사용자가 실제로 어떤 권한을 가지는지" 파악하기 어려워진다. `kubectl auth can-i --list`만으로는 부족할 때, RBAC 정책을 시각화하고 분석하는 도구(rbac-lookup, rakkess, kubectl-who-can)는 어떻게 활용하는가?

---

## Q7: Operator의 RBAC 설계와 최소 권한 적용

**질문**: Kubernetes Operator(예: Redpanda Operator, Strimzi)는 클러스터 리소스를 자동으로 관리하기 위해 광범위한 RBAC 권한이 필요하다. Operator에 최소 권한 원칙을 적용하려면 어떻게 설계해야 하며, Operator의 RBAC이 보안에 미치는 영향은 무엇인가?

**핵심 포인트**:

- **Operator가 필요로 하는 권한의 범위**: Operator는 CRD를 감시(watch)하고, 그에 따라 StatefulSet, Service, ConfigMap, PVC 등을 생성/수정/삭제해야 한다. 이러한 작업을 수행하려면 해당 리소스에 대한 create, get, list, watch, update, patch, delete 동사가 필요하다. 문제는 이 권한이 상당히 넓다는 것이다. Operator의 ServiceAccount가 탈취되면 공격자가 클러스터의 핵심 리소스를 조작할 수 있다.

- **Namespace-scoped vs Cluster-scoped Operator**: Namespace-scoped Operator는 특정 Namespace의 리소스만 관리하므로 RBAC 범위가 제한적이다(Role + RoleBinding). Cluster-scoped Operator는 모든 Namespace의 리소스를 관리하므로 ClusterRole + ClusterRoleBinding이 필요하다. 보안 관점에서 가능하면 Namespace-scoped Operator를 선호한다. 하지만 Strimzi의 Cluster Operator처럼 여러 Namespace를 감시해야 하는 경우 Cluster-scoped가 불가피하다.

- **Operator의 RBAC 감사 방법**: Operator가 설치한 ClusterRole을 주기적으로 검토하여 불필요한 권한이 포함되어 있지 않은지 확인한다. `kubectl describe clusterrole <operator-role>`로 권한 목록을 확인하고, Operator가 실제로 사용하지 않는 리소스나 동사가 있으면 Helm values나 Operator 설정에서 제거할 수 있는지 확인한다. 일부 Operator는 설치 시 `cluster-admin`을 요구하는데, 이는 보안 감사에서 반드시 검토해야 할 위험 신호이다.

- **Operator ServiceAccount 보호**: Operator의 SA 토큰은 높은 권한을 가지므로 특별히 보호해야 한다. (1) Operator Pod의 NetworkPolicy를 설정하여 API 서버와의 통신만 허용하고 다른 Pod로의 접근을 차단한다. (2) Pod Security Standards에서 Operator Pod에 대해 `readOnlyRootFilesystem`, `runAsNonRoot`를 적용한다. (3) Operator Pod가 실행되는 Namespace에 대한 접근을 제한하여, 일반 사용자가 Operator Pod의 로그나 설정을 볼 수 없도록 한다.

- **CRD와 RBAC aggregation**: Operator가 CRD를 설치할 때, 해당 CRD에 대한 RBAC 권한을 기본 ClusterRole(`admin`, `edit`, `view`)에 자동으로 추가할 수 있다. 이를 RBAC aggregation이라 하며, ClusterRole에 `rbac.authorization.k8s.io/aggregate-to-admin: "true"` 라벨을 설정하면 `admin` ClusterRole에 해당 CRD 권한이 자동 합산된다. 이 기능은 편리하지만, 의도하지 않은 권한 확장이 발생할 수 있으므로 주의가 필요하다.

- **멀티테넌트 환경에서의 Operator RBAC**: 여러 팀이 같은 클러스터를 공유하는 멀티테넌트 환경에서 Operator의 ClusterRole은 모든 팀의 리소스에 접근할 수 있다. 이를 완화하려면 Operator의 `watchNamespaces` 설정으로 감시 범위를 제한하거나, 팀별로 별도의 Operator 인스턴스를 Namespace-scoped로 배포하는 전략을 사용한다. 후자는 리소스 오버헤드가 있지만 보안 격리가 강화된다.

- **Operator 취약점의 파급 효과**: Operator 이미지에 CVE(취약점)가 발견되면, Operator의 높은 RBAC 권한 때문에 일반 애플리케이션 Pod의 취약점보다 파급력이 크다. 따라서 Operator 이미지를 정기적으로 스캔(Trivy, Snyk)하고, 새 버전이 출시되면 우선적으로 업데이트해야 한다.

**심화 질문**: Operator를 OLM(Operator Lifecycle Manager)으로 관리할 때, OLM이 자동 생성하는 RBAC 리소스는 어떤 것이 있으며, Operator 업그레이드 시 RBAC 권한이 자동으로 확장되는 위험을 어떻게 방지하는가?
