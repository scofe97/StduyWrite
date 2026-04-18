# Ch09. Kubernetes 환경의 Jenkins — 점검 질문

면접 및 자기 점검용 질문 모음. 각 질문은 핵심 포인트와 심화 질문을 포함한다.

---

## Q1. VM 기반 Jenkins와 Kubernetes 기반 Jenkins의 차이

**VM 기반 Jenkins와 Kubernetes 기반 Jenkins의 차이를 Agent 관리와 리소스 효율성 관점에서 설명하시오.**

### 핵심 포인트

- VM 기반에서는 Agent를 사전에 프로비저닝하고 상시 가동해야 하므로, 빌드가 없는 시간에도 유휴 리소스 비용이 발생한다. 10대의 Agent VM을 운영하면서 평균 사용률이 30%라면, 70%의 컴퓨팅 리소스가 낭비된다.
- Kubernetes 기반에서는 빌드 요청이 들어올 때 Agent Pod을 동적으로 생성하고, 빌드 완료 후 즉시 삭제한다. 리소스 사용이 빌드 수요에 정확히 비례하므로 유휴 비용이 0에 수렴한다.
- VM Agent는 시간이 지나면 Configuration Drift가 발생하여 환경 불일치 문제가 생기지만, K8s Agent는 매번 깨끗한 컨테이너 이미지에서 시작하므로 빌드 재현성이 보장된다.
- 스케일링 관점에서, VM 추가는 수 분이 걸리지만 Pod 생성은 수 초 만에 완료된다. 빌드 큐가 갑자기 늘어나는 상황에 대한 반응 속도가 근본적으로 다르다.

### 심화 질문

- K8s Jenkins에서 Agent Pod 생성에 수 초가 걸린다고 했는데, 이미지가 큰 경우 Pull 시간 때문에 느려질 수 있다. 이를 어떻게 최적화하는가? (힌트: 이미지 사전 캐싱, 경량 이미지, DaemonSet으로 pull)
- VM 기반에서도 Cloud Plugin(EC2, Azure VM)으로 동적 프로비저닝이 가능하다. K8s 동적 Agent와 비교했을 때의 차이점은 무엇인가?

---

## Q2. Kubernetes Plugin의 동적 Agent Pod 프로비저닝

**Kubernetes Plugin의 동적 Agent Pod 프로비저닝이 동작하는 과정을 단계별로 설명하시오.**

### 핵심 포인트

- 개발자가 코드를 Push하면 Jenkins Controller가 빌드 작업을 큐에 추가한다.
- Controller는 큐에 있는 작업을 처리할 가용 Agent가 없으면 Kubernetes Plugin에 Agent 생성을 요청한다.
- Plugin은 Jenkinsfile의 `podTemplate` 또는 사전 정의된 Pod Template 스펙을 기반으로 Kubernetes API에 Pod 생성 요청을 보낸다.
- Kubernetes Scheduler가 적절한 Node에 Pod을 배치하고, 컨테이너 이미지를 Pull한 후 Pod을 실행한다.
- Pod 내의 JNLP 컨테이너(또는 inbound-agent)가 Controller의 JNLP Service(TCP 50000)에 연결을 수립한다.
- Controller가 연결된 Agent에 빌드 명령을 전달하고, Agent는 빌드를 실행한다.
- 빌드가 완료되면 결과를 Controller에 반환하고, Plugin이 Kubernetes API를 통해 Pod을 삭제한다.

### 심화 질문

- JNLP 연결이 실패하면 어떤 일이 발생하는가? Pod이 생성되었지만 Controller에 연결하지 못하는 상황의 원인과 트러블슈팅 방법은?
- `idleMinutes` 설정으로 Agent Pod을 일정 시간 유지할 수 있다. 이 설정이 유용한 시나리오는 무엇인가?

---

## Q3. 멀티 컨테이너 Pod Template과 사이드카 패턴

**K8s Jenkins에서 멀티 컨테이너 Pod Template을 사용하는 이유와 사이드카 패턴을 설명하시오.**

### 핵심 포인트

- 멀티 컨테이너 Pod Template은 하나의 Agent Pod 안에 여러 컨테이너(Maven, Docker, Node 등)를 함께 실행하는 구조이다. Jenkinsfile에서 `container('name')` 블록으로 어떤 컨테이너에서 명령을 실행할지 지정한다.
- 사이드카 패턴을 사용하는 핵심 이유는 관심사의 분리이다. 모든 도구를 하나의 거대한 이미지에 넣으면 이미지 크기가 커지고, 하나의 도구를 업데이트하려면 전체 이미지를 다시 빌드해야 한다.
- 같은 Pod 내의 컨테이너들은 네트워크 네임스페이스와 볼륨을 공유하므로, Maven이 빌드한 JAR 파일을 Docker 컨테이너가 바로 접근하여 이미지를 빌드할 수 있다.
- JNLP Agent 컨테이너가 기본적으로 포함되며, 이 컨테이너가 Controller와의 통신을 담당한다. 나머지 컨테이너들은 `command: ['sleep'], args: ['infinity']`로 실행을 유지하여 JNLP Agent가 명령을 전달할 수 있게 한다.

### 심화 질문

- Docker-in-Docker(DinD)를 사이드카로 실행할 때 `privileged: true`가 필요한 이유는 무엇이고, 보안 관점에서 어떤 대안이 있는가?
- Init Container와 사이드카 컨테이너의 차이점은? Jenkins 빌드에서 Init Container를 활용하면 좋은 시나리오는?

---

## Q4. StatefulSet 배포와 PersistentVolume의 역할

**Jenkins Controller를 Kubernetes에 배포할 때 StatefulSet을 사용하는 이유와 PersistentVolume의 역할을 설명하시오.**

### 핵심 포인트

- Jenkins Controller는 stateful 애플리케이션이다. JENKINS_HOME 디렉토리에 Job 정의, 빌드 히스토리, 플러그인, Credential, 사용자 설정이 저장되므로, Pod이 재시작되어도 이 데이터가 유지되어야 한다.
- StatefulSet은 Deployment와 달리 안정적인 네트워크 ID(고정된 Pod 이름)와 영구 스토리지 보장을 제공한다. Pod이 죽었다가 다시 생성되면 동일한 PVC에 자동으로 재마운트된다.
- PersistentVolume은 Pod의 생명주기와 독립적인 스토리지를 제공한다. Pod이 삭제되어도 PV의 데이터는 보존되므로, Controller를 업그레이드하거나 노드를 이동해도 데이터를 잃지 않는다.
- Deployment를 사용할 수도 있지만, 이 경우 replicas를 반드시 1로 제한해야 한다. Jenkins Controller는 Active-Active를 지원하지 않으므로, 2개 이상의 Controller가 같은 JENKINS_HOME에 접근하면 데이터 손상이 발생한다.

### 심화 질문

- PVC의 `ReclaimPolicy`가 `Delete`로 설정된 경우, Helm 릴리즈를 삭제하면 Jenkins 데이터가 모두 사라진다. 이를 방지하려면 어떻게 해야 하는가?
- Jenkins Controller Pod이 다른 Node로 재스케줄링될 때, PV의 접근 모드(ReadWriteOnce)가 문제가 될 수 있는 상황은?

---

## Q5. Jenkins on K8s, Jenkins X, Tekton 비교

**Jenkins on K8s, Jenkins X, Tekton의 차이를 설명하고 각각 어떤 팀에 적합한지 제시하시오.**

### 핵심 포인트

- **Jenkins on K8s**는 전통적 Jenkins를 Kubernetes 인프라 위에서 운영하는 방식이다. 기존 Jenkinsfile, Shared Library, 1,800+개 플러그인 자산을 그대로 활용하면서 동적 Agent의 이점을 얻는다. 이미 Jenkins 투자가 상당한 팀에 적합하다.
- **Jenkins X**는 이름에 Jenkins가 들어가지만 내부적으로 Tekton 엔진을 사용하며, GitOps와 Preview Environment가 내장되어 있다. 새 프로젝트를 시작하면서 처음부터 Kubernetes 네이티브 CI/CD를 도입하려는 팀에 적합하지만, 학습 곡선이 가장 높다.
- **Tekton**은 Kubernetes CRD로 파이프라인을 정의하는 순수한 엔진이다. 최종 사용자용 도구라기보다 CI/CD 플랫폼을 구축하기 위한 빌딩 블록이다. 내부 개발자 플랫폼(IDP)의 파이프라인 엔진으로 사용하려는 플랫폼 팀에 적합하다.
- 세 가지 모두 Agent/Task가 Pod으로 실행된다는 공통점이 있지만, 상태 관리 방식이 다르다. Jenkins on K8s는 Controller에 상태를 저장하고, Jenkins X는 Git을 진실의 원천으로 삼으며, Tekton은 CRD 자체가 상태이다.

### 심화 질문

- Tekton Pipeline에서 Task 간 데이터 전달은 어떻게 이루어지는가? Jenkins Pipeline의 stash/unstash와 비교하면?
- Jenkins X의 Preview Environment가 PR 리뷰 프로세스를 어떻게 개선하는가?

---

## Q6. 빌드 캐시 관리 전략

**K8s Jenkins에서 빌드 캐시(Maven/Gradle)를 효율적으로 관리하는 전략을 설명하시오.**

### 핵심 포인트

- K8s Jenkins에서 Agent Pod은 빌드마다 새로 생성되므로, 캐시를 별도로 관리하지 않으면 매 빌드마다 모든 의존성을 네트워크에서 다시 다운로드해야 한다. Maven Central에서 수백 MB의 의존성을 매번 받으면 빌드 시간이 수 분 이상 증가한다.
- **PVC 기반 캐시**: PersistentVolumeClaim을 생성하여 `.m2/repository`나 `.gradle/caches`를 마운트한다. 여러 Pod이 동시에 접근해야 하므로 `ReadWriteMany(RWX)` 접근 모드를 지원하는 스토리지(NFS, CephFS, EFS 등)가 필요하다.
- **PVC 동시 쓰기 문제**: 여러 빌드가 동시에 같은 의존성을 같은 위치에 쓰면 파일 충돌이 발생할 수 있다. Maven의 `-Dmaven.repo.local` 옵션으로 Pod별 로컬 저장소를 분리하되, 읽기는 공유 캐시에서 하는 레이어 전략이 효과적이다.
- **Init Container 활용**: 빌드 시작 전 Init Container에서 공유 캐시를 Pod 로컬 디렉토리로 복사하고, 빌드는 로컬 디렉토리에서 수행한다. 빌드 후 새로 다운로드된 의존성만 공유 캐시에 동기화한다.
- **이미지 베이킹**: 자주 사용하는 의존성을 미리 포함한 커스텀 빌드 이미지를 만드는 방법도 있다. 의존성 변경이 드문 프로젝트에서 효과적이지만, 이미지 관리 부담이 늘어난다.

### 심화 질문

- RWX PVC의 I/O 성능이 병목이 되는 경우, 어떤 대안 스토리지를 검토할 수 있는가?
- Gradle의 Build Cache와 Dependency Cache의 차이는 무엇이고, K8s 환경에서 각각을 어떻게 최적화하는가?

---

## Q7. K8s Jenkins 보안 모범 사례

**Kubernetes 환경의 Jenkins에서 보안을 강화하기 위한 방법을 ServiceAccount, Pod SecurityContext, NetworkPolicy 관점에서 설명하시오.**

### 핵심 포인트

- **ServiceAccount 최소 권한**: Jenkins Controller의 ServiceAccount에는 Agent Pod을 생성/조회/삭제할 수 있는 RBAC 권한만 부여한다. `pods`, `pods/exec`, `pods/log` 리소스에 대한 `create`, `get`, `list`, `watch`, `delete` 동사만 허용하고, Secret이나 다른 네임스페이스 접근은 차단한다.
- **Pod SecurityContext**: Docker-in-Docker를 위해 `privileged: true`를 설정하면 컨테이너가 호스트 커널에 완전한 접근 권한을 가지게 되어, 컨테이너 탈출 공격에 취약해진다. Kaniko, BuildKit rootless, Podman 등 비특권 빌드 도구를 사용하여 이 위험을 제거해야 한다.
- **NetworkPolicy**: Agent Pod이 접근할 수 있는 네트워크 대상을 명시적으로 제한한다. Jenkins Controller(JNLP), 내부 컨테이너 레지스트리, 소스 코드 저장소(GitLab/GitHub)만 허용하고, 나머지 트래픽은 기본 차단(deny-all)한다.
- **Credential 관리**: Jenkins 내장 Credential Store 대신 Kubernetes Secret이나 HashiCorp Vault를 사용하고, CSI Secret Store Driver로 Pod에 시크릿을 주입하는 방식이 더 안전하다.

### 심화 질문

- Kaniko와 Docker-in-Docker의 빌드 성능 차이는 어느 정도이며, Kaniko의 제약사항은 무엇인가?
- Pod Security Admission(PSA)의 `restricted` 프로필을 적용하면 Jenkins Agent에 어떤 영향이 있는가?
