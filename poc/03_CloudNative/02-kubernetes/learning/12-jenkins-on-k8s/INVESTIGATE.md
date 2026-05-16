<!-- migrated: write/09_cloud/kubernetes/deepdive/07-01.Jenkins on K8s 점검.md (2026-04-19) -->

# Ch12. Jenkins on Kubernetes - 심화 점검

## 점검 질문

---

### Q1: VM 기반 Jenkins Agent vs K8s Pod Agent의 차이와 장단점

**핵심 포인트:**

- **프로비저닝 속도**: VM 에이전트는 수동으로 생성하거나 VM 이미지로 자동화해도 분 단위가 걸린다. 반면 K8s Pod는 이미지가 캐시되어 있으면 초 단위로 생성된다. 빌드 큐가 급증할 때 Pod는 즉시 스케일 아웃할 수 있지만, VM은 클라우드 API 호출과 부팅 시간 때문에 느리다.

- **리소스 효율성**: VM 에이전트는 24시간 실행되므로 idle 시간에도 비용이 발생한다. 예를 들어, 하루 8시간만 빌드가 발생한다면 16시간은 낭비다. Pod는 빌드 시작 시 생성되고 종료 시 삭제되므로, 실제 사용 시간만큼만 비용을 지불한다. 100개의 빌드가 동시에 발생하면 100개의 Pod를, 1개만 발생하면 1개만 사용한다.

- **환경 일관성**: VM 에이전트는 시간이 지나면서 "drift"가 발생한다. A 팀이 Python 3.9를 설치하고, B 팀이 Node.js 16을 설치하면, 다음 빌드는 이전 빌드의 잔재물을 상속받는다. 심지어 빌드 산출물이 `/tmp`에 남아서 다음 빌드에 영향을 줄 수 있다. Pod는 매번 이미지에서 새로 시작하므로 항상 동일한 초기 상태를 갖는다.

- **보안과 격리**: VM 에이전트는 프로세스 레벨 격리만 제공한다. 악의적인 빌드 스크립트가 다른 프로세스를 조작하거나 민감한 파일을 읽을 수 있다. Pod는 컨테이너 격리와 Kubernetes RBAC, Network Policy로 훨씬 강력한 경계를 제공한다. 한 Pod의 침해가 다른 Pod에 영향을 주지 않는다.

- **유지보수 부담**: VM 에이전트는 OS 패치, 보안 업데이트, 도구 버전 업그레이드를 수동으로 해야 한다. Ansible이나 Chef로 자동화할 수 있지만, 여전히 관리 포인트가 많다. Pod는 이미지만 업데이트하면 되고, 이미지는 CI/CD로 자동 빌드할 수 있다.

**심화 질문:**

- Pod의 이미지 pull 시간이 길면 VM보다 느릴 수 있는데, 어떻게 최적화하는가? (ImagePullPolicy, 노드 이미지 캐싱, 레지스트리 위치)
- Pod는 상태가 없어서 빌드 캐시(Maven `.m2`, npm `node_modules`)를 재사용하기 어렵다. 어떻게 해결하는가? (PVC, 외부 캐시 서버)
- VM 에이전트가 여전히 유리한 케이스는? (GPU 작업, 특수 하드웨어, Windows 빌드)

---

### Q2: JCasC(Configuration as Code)가 해결하는 문제

**핵심 포인트:**

- **수동 설정의 재현 불가**: 전통적인 Jenkins는 웹 UI에서 클릭으로 설정한다. 시스템 설정, 플러그인 설정, 자격 증명, 클라우드 연결 등을 하나하나 입력한다. 문제는 이 설정을 다른 Jenkins 인스턴스에 복제하려면 똑같은 클릭을 반복해야 한다는 것이다. 스크린샷이나 문서로 기록할 수는 있지만, 사람이 하는 일이라 실수가 발생한다.

- **버전 관리의 어려움**: Jenkins 설정은 파일 시스템에 XML로 저장된다. 이 XML을 Git에 커밋할 수는 있지만, 수동 UI 변경과 코드 변경이 혼재된다. "누가, 언제, 왜" 이 설정을 바꿨는지 추적하기 어렵다. JCasC를 사용하면 `jenkins.yaml` 하나에 모든 설정을 선언하고, Git PR 리뷰를 거쳐 변경할 수 있다.

- **환경 간 차이**: 개발/스테이징/프로덕션 Jenkins가 서로 다른 설정을 갖기 쉽다. 개발 환경에서는 되는데 프로덕션에서 안 되는 "works on my Jenkins" 문제가 발생한다. JCasC로 설정을 파일로 관리하면, 동일한 YAML을 모든 환경에 적용할 수 있다.

- **재해 복구**: Jenkins 서버가 날아가면, 백업에서 복원하거나 처음부터 재구축해야 한다. JCasC가 있으면 새 Jenkins 인스턴스를 띄우고 `jenkins.yaml`만 적용하면 몇 분 만에 원래 상태로 돌아온다. 작업 정의는 Jenkinsfile로 Git에 있고, 설정은 JCasC로 Git에 있으므로, 백업할 것은 빌드 기록뿐이다.

- **자동화와 GitOps**: Kubernetes에서 Jenkins를 배포하면, Helm 차트의 `values.yaml`에 JCasC 설정을 넣을 수 있다. ArgoCD나 Flux 같은 GitOps 도구로 `values.yaml`이 변경되면 자동으로 Jenkins에 적용된다. 설정 변경이 코드 배포와 똑같은 프로세스를 따르게 된다.

**심화 질문:**

- JCasC로 관리할 수 없는 설정은 무엇인가? (플러그인 바이너리, 사용자 생성 작업의 XML)
- JCasC 설정에 민감 정보(API 토큰)를 넣어야 한다면 어떻게 하는가? (Secret 참조, 환경 변수 치환)
- 기존 Jenkins를 JCasC로 마이그레이션하려면 어떻게 하는가? (export 플러그인, 수동 변환)

---

### Q3: Kubernetes Plugin의 Pod Template 동작 원리

**핵심 포인트:**

- **Pod Template이란**: 에이전트 Pod를 생성할 때 사용할 "청사진"이다. 어떤 이미지를 사용할지, 리소스는 얼마나 할당할지, 어떤 볼륨을 마운트할지를 정의한다. Pod Template은 JCasC에 정적으로 정의하거나, Jenkinsfile에 동적으로 정의할 수 있다.

- **Label 기반 매칭**: Pod Template에는 `label`이 있다. Jenkinsfile에서 `agent { label 'maven' }`이라고 쓰면, Jenkins가 "maven" 레이블을 가진 Pod Template을 찾아서 Pod를 생성한다. 레이블이 없으면 "There are no nodes with the label 'maven'" 에러가 발생한다.

- **JNLP 컨테이너**: Pod Template은 기본적으로 "jnlp" 컨테이너를 포함한다. 이 컨테이너는 `jenkins/inbound-agent` 이미지를 사용하고, Jenkins Controller의 50000 포트로 연결한다. JNLP는 Jenkins Network Launch Protocol로, 에이전트가 Controller에 먼저 연결을 맺는 "inbound" 방식이다. Controller는 이 연결을 통해 명령을 전달한다.

- **멀티 컨테이너 구조**: Pod Template에 여러 컨테이너를 정의할 수 있다. 예를 들어, `maven`, `docker`, `kubectl` 컨테이너를 하나의 Pod에 넣으면, Jenkinsfile에서 `container('maven') { ... }`로 특정 컨테이너에서 명령을 실행할 수 있다. 모든 컨테이너는 같은 네트워크와 볼륨을 공유하므로, localhost로 통신하고 파일을 주고받을 수 있다.

- **동적 프로비저닝 흐름**: 빌드가 스케줄링되면 → Kubernetes Plugin이 Pod Template을 읽고 → Kubernetes API에 Pod 생성 요청 → 노드가 이미지를 pull하고 Pod 시작 → jnlp 컨테이너가 Controller에 연결 → Controller가 빌드 작업 전달 → 빌드 완료 후 Pod 삭제. 이 모든 과정이 자동으로 일어난다.

- **리소스 할당**: Pod Template에 `resourceRequestCpu`, `resourceRequestMemory`, `resourceLimitCpu`, `resourceLimitMemory`를 설정할 수 있다. Kubernetes Scheduler는 requests를 보고 Pod를 배치할 노드를 선택하고, kubelet은 limits를 넘으면 Pod를 kill한다. 빌드마다 다른 리소스가 필요하면 Jenkinsfile에서 Pod Template을 오버라이드할 수 있다.

**심화 질문:**

- JNLP 대신 SSH로 에이전트를 연결할 수 있는가? (가능하지만 복잡함, JNLP가 권장됨)
- Pod Template을 JCasC와 Jenkinsfile 양쪽에 정의하면 어느 것이 우선인가? (Jenkinsfile이 우선)
- 한 빌드에서 서로 다른 Pod Template을 사용할 수 있는가? (Parallel 단계에서 가능)

---

### Q4: Jenkins Controller의 HA 구성 방법과 한계

**핵심 포인트:**

- **Active-Standby vs Active-Active**: Jenkins는 기본적으로 Active-Standby HA를 지원한다. 메인 Controller가 작동하고, 백업 Controller는 대기하다가 메인이 죽으면 PVC를 붙여서 활성화된다. Active-Active(여러 Controller가 동시에 작동)는 공식적으로 지원하지 않는다. 이유는 Jenkins Home의 파일 잠금과 플러그인 상태 동기화 문제 때문이다.

- **StatefulSet vs Deployment**: Helm 차트는 기본적으로 StatefulSet을 사용한다 (`controller.statefulSet.enabled: true`). StatefulSet은 Pod 이름이 고정되고 (`jenkins-0`), PVC가 Pod와 1:1로 바인딩된다. Deployment로도 배포할 수 있지만, PVC를 RWO(ReadWriteOnce)로 사용하면 Pod가 다른 노드로 옮겨갈 때 PVC를 detach/attach하는 시간이 걸린다.

- **PVC RWX 문제**: Jenkins Home을 여러 Pod가 공유하려면 PVC를 RWX(ReadWriteMany)로 만들어야 한다. 하지만 대부분의 클라우드 스토리지(AWS EBS, GCP PD)는 RWO만 지원한다. RWX를 지원하는 것은 NFS, EFS, Azure Files 정도인데, 성능이 떨어지고 파일 잠금 문제가 발생할 수 있다.

- **JobConfigHistory 플러그인**: Active-Standby HA에서는 Standby Controller가 메인의 Jenkins Home을 실시간으로 복제해야 한다. `rsync`나 클라우드 스토리지 복제 기능을 사용할 수 있지만, 완벽한 동기화는 어렵다. JobConfigHistory 플러그인으로 작업 변경 이력을 추적하고, 재해 발생 시 복구할 수 있다.

- **CloudBees Jenkins Enterprise**: 상용 솔루션인 CloudBees는 "Operations Center"로 여러 Controller를 중앙에서 관리한다. 각 팀이 독립된 Controller를 갖고, Operations Center가 플러그인 업데이트, RBAC, 백업을 통합 관리한다. 진짜 HA가 필요하면 이런 솔루션을 고려해야 한다.

- **에이전트는 HA 필요 없음**: 다행히 Kubernetes Pod 에이전트는 동적이라 HA가 필요 없다. 빌드 중에 Pod가 죽으면 Jenkins가 다른 Pod를 생성하고 빌드를 재시작한다. 문제는 Controller가 죽으면 모든 빌드가 멈춘다는 것이다.

**심화 질문:**

- Jenkins X나 Tekton 같은 대안은 HA를 어떻게 해결하는가? (Controller 없이 빌드를 직접 K8s에 제출)
- Controller를 여러 개 띄우고 로드밸런서로 분산하면 안 되는 이유는? (Jenkins Home 공유 문제, 세션 상태)
- Disaster Recovery 시나리오에서 RTO/RPO를 어떻게 줄이는가? (자동 백업, Blue-Green 배포)

---

### Q5: Jenkins on K8s에서 Docker-in-Docker vs Kaniko 차이

**핵심 포인트:**

- **DinD(Docker-in-Docker)**: Docker 데몬을 Pod 안에서 실행하는 방식이다. `docker:dind` 이미지를 사용하고, `privileged: true`로 컨테이너를 특권 모드로 실행한다. 빌드 스크립트에서 `docker build`, `docker push`를 그대로 사용할 수 있어서 편하지만, 보안 위험이 크다. Privileged 컨테이너는 호스트 커널에 접근할 수 있어서, 컨테이너 탈출 공격에 취약하다.

- **Kaniko**: Google이 만든 도구로, Docker 데몬 없이 컨테이너 이미지를 빌드한다. Dockerfile을 읽어서 각 레이어를 userspace에서 생성하고, 레지스트리에 직접 푸시한다. Privileged 모드가 필요 없어서 안전하다. 단점은 Dockerfile의 모든 기능을 지원하지 않고, 빌드 속도가 약간 느릴 수 있다.

- **Buildah와 Podman**: Red Hat의 대안이다. Buildah는 이미지 빌드, Podman은 컨테이너 실행 도구다. Kaniko처럼 데몬이 필요 없고, OCI 표준을 준수한다. Kubernetes Pod에서 사용할 수 있지만, Kaniko보다 덜 알려져 있다.

- **Docker Socket 마운트**: 또 다른 방법은 호스트의 Docker 소켓(`/var/run/docker.sock`)을 Pod에 마운트하는 것이다. Pod에서 `docker` 명령을 실행하면 호스트의 Docker 데몬이 처리한다. 간단하지만, 모든 Pod가 호스트 Docker를 공유하므로 격리가 없다. 한 빌드가 `docker rm -f $(docker ps -aq)`를 실행하면 다른 빌드의 컨테이너까지 삭제된다.

- **보안 트레이드오프**: DinD는 편리하지만 위험하고, Kaniko는 안전하지만 제약이 있다. 프로덕션 환경에서는 Kaniko를 권장하고, 로컬 개발이나 테스트에서는 DinD를 사용할 수 있다. 또는 이미지 빌드를 전용 빌드 클러스터나 외부 서비스(Google Cloud Build, AWS CodeBuild)로 분리하는 방법도 있다.

**심화 질문:**

- Kaniko에서 빌드 캐시를 사용하려면 어떻게 하는가? (`--cache=true`, 레지스트리에 캐시 저장)
- Docker Socket 마운트 시 보안을 강화하려면? (별도 namespace, AppArmor 프로파일)
- Kubernetes 1.24부터 dockershim이 제거되었는데, DinD에 영향이 있는가? (없음, DinD는 독립 데몬)

---

### Q6: RBAC과 ServiceAccount로 Jenkins 권한을 제한하는 방법

**핵심 포인트:**

- **최소 권한 원칙**: Jenkins Controller는 Pod를 생성하고 삭제할 권한이 필요하다. 하지만 Deployment를 수정하거나, 다른 Namespace에 접근하거나, Cluster Admin 권한을 줘서는 안 된다. RBAC으로 정확히 필요한 권한만 부여한다.

- **ServiceAccount**: Jenkins Controller Pod는 `jenkins` ServiceAccount로 실행된다. 이 ServiceAccount에 Role을 바인딩하면, Pod 내부에서 Kubernetes API를 호출할 때 해당 권한을 갖는다. `/var/run/secrets/kubernetes.io/serviceaccount/token` 파일에 JWT 토큰이 있고, 이 토큰으로 인증한다.

- **Role vs ClusterRole**: Role은 특정 Namespace에서만 유효하고, ClusterRole은 클러스터 전체에서 유효하다. Jenkins는 보통 자신의 Namespace에서만 Pod를 생성하므로 Role로 충분하다. 단, 여러 Namespace에 에이전트를 배포하려면 ClusterRole이 필요하다.

- **기본 권한**: Helm 차트가 생성하는 Role은 대략 이렇다:
  ```yaml
  rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["create", "delete", "get", "list", "watch", "patch"]
    - apiGroups: [""]
      resources: ["pods/exec"]
      verbs: ["create"]
    - apiGroups: [""]
      resources: ["pods/log"]
      verbs: ["get"]
  ```
  이 권한으로 Pod를 생성/삭제하고, 로그를 읽고, `exec`로 명령을 실행할 수 있다.

- **Secret 접근 제한**: `rbac.readSecrets: true`로 설정하면 Secret 읽기 권한이 추가된다. Jenkins가 자격 증명을 Secret으로 저장하려면 필요하지만, 모든 Secret을 읽을 수 있게 되므로 위험하다. 대신 특정 Secret만 읽을 수 있도록 제한하는 것이 좋다:
  ```yaml
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["git-token", "docker-registry"]
    verbs: ["get"]
  ```

- **감사 로그**: Kubernetes Audit Log로 Jenkins가 어떤 API를 호출했는지 추적할 수 있다. 의심스러운 권한 사용(예: 다른 Namespace의 Secret 읽기)이 발견되면 Role을 수정하고 재배포한다.

**심화 질문:**

- Pod Security Policy(PSP)나 Pod Security Standards로 추가 제약을 걸 수 있는가? (가능, privileged 차단 등)
- ServiceAccount 토큰이 탈취되면 어떻게 되는가? (해당 권한으로 API 호출 가능, 토큰 rotation 필요)
- 여러 팀이 같은 Jenkins를 사용하는데 Namespace를 분리하려면? (Folder별 다른 ServiceAccount 사용)

---

### Q7: Jenkins Helm chart의 주요 values 파라미터

**핵심 포인트:**

- **이미지 설정**: `controller.image`와 `controller.tag`로 Jenkins 버전을 선택한다. LTS(Long Term Support) 버전은 `lts` 태그를 사용하고, 특정 버전은 `2.440-jdk17` 같은 태그를 사용한다. JDK 버전도 고려해야 하는데, 최신 플러그인은 JDK 11 이상을 요구한다.

- **리소스 설정**: `controller.resources`로 CPU/메모리 requests와 limits를 지정한다. Requests는 Scheduler가 Pod를 배치할 때 사용하고, limits는 Pod가 초과하면 kill된다. Jenkins는 메모리를 많이 사용하므로, requests를 너무 낮게 잡으면 OOMKilled가 발생한다. 권장 값은 최소 512Mi requests, 1Gi limits다.

- **Service 설정**: `controller.serviceType`을 `ClusterIP`, `NodePort`, `LoadBalancer` 중 선택한다. minikube나 개발 환경에서는 NodePort가 편하고, 프로덕션에서는 Ingress + ClusterIP를 사용한다. `controller.ingress.enabled: true`로 Ingress를 활성화하고, 호스트와 TLS를 설정한다.

- **플러그인 관리**: `controller.installPlugins`에 플러그인 이름과 버전을 리스트로 넣으면, Jenkins 시작 시 자동 설치된다. 예: `kubernetes:4253.v7700d91739e5`. 버전을 명시하지 않으면 최신 버전을 설치하는데, 호환성 문제가 생길 수 있으므로 프로덕션에서는 버전을 고정하는 것이 좋다.

- **JCasC 설정**: `controller.JCasC.configScripts`에 YAML로 설정을 넣는다. 여러 개의 configScript를 정의할 수 있고, 각각 이름을 붙인다 (예: `kubernetes-cloud`, `credentials`, `security`). 이 설정은 ConfigMap으로 저장되고, Jenkins가 `/var/jenkins_home/casc_configs/`에서 읽는다.

- **Persistence 설정**: `persistence.enabled: true`로 PVC를 사용하고, `persistence.size`로 크기를 지정한다. `persistence.storageClass`로 특정 스토리지 클래스를 선택할 수 있다. `persistence.existingClaim`으로 기존 PVC를 재사용할 수도 있다 (예: 백업 복원 시).

- **RBAC 설정**: `rbac.create: true`로 Role과 RoleBinding을 자동 생성한다. `rbac.readSecrets: true`로 Secret 읽기 권한을 추가할 수 있지만, 보안상 신중해야 한다. `serviceAccount.name`으로 ServiceAccount 이름을 커스터마이징할 수 있다.

- **Agent 설정**: `agent.resources`로 기본 에이전트의 리소스를 설정한다. 이 값은 Pod Template에서 오버라이드할 수 있다. `agent.podName`으로 에이전트 Pod의 네이밍 패턴을 바꿀 수 있다.

**심화 질문:**

- Helm 차트 업그레이드 시 PVC 데이터가 유지되는가? (유지됨, PVC는 삭제되지 않음)
- `controller.overwritePlugins: true`의 의미는? (기존 플러그인을 덮어쓸지 여부, 기본은 false)
- `controller.adminPassword`로 초기 비밀번호를 설정할 수 있는가? (가능하지만 Secret으로 관리하는 것이 안전)

---

## 정리

Jenkins on Kubernetes는 CI/CD 인프라를 현대화하는 강력한 방법이다. VM 기반 에이전트의 한계를 극복하고, 동적 Pod로 리소스 효율과 환경 일관성을 확보한다. JCasC로 설정을 코드화하고, Helm으로 배포를 자동화하며, RBAC으로 보안을 강화한다.

핵심은 **클라우드 네이티브 철학**을 이해하는 것이다. 상태를 PVC에 저장하고, 설정을 ConfigMap에 넣고, 권한을 RBAC으로 제한하고, 스케일링을 Kubernetes에 맡긴다. Jenkins는 더 이상 "애완동물"이 아니라 "가축"이다. 언제든지 재배포하고, 복제하고, 버릴 수 있다.

다음 챕터에서는 SonarQube를 Kubernetes에 배포하고, Jenkins 파이프라인과 통합하여 코드 품질 게이트를 자동화한다.
