<!-- migrated: write/09_cloud/kubernetes/deepdive/02-01.핵심 워크로드 점검.md (2026-04-19) -->

# Ch02. 핵심 워크로드 - 점검 질문

## Q1: Pod 안에 여러 컨테이너를 넣는 경우는 언제인가?

**핵심 포인트**

- **Sidecar 패턴**: 메인 컨테이너의 기능을 보조하는 컨테이너를 같은 Pod에 배치한다. 가장 흔한 예는 로그 수집기(Fluentd, Filebeat)다. 웹 서버가 `/var/log/nginx/access.log`에 로그를 쓰면, sidecar 컨테이너가 같은 emptyDir 볼륨을 마운트하여 로그를 읽고 중앙 로그 시스템(Elasticsearch)으로 전송한다. Service Mesh(Istio)도 sidecar 패턴을 사용하여 envoy-proxy 컨테이너를 자동 주입한다.
- **Ambassador 패턴**: 메인 컨테이너가 외부 서비스(DB, API)에 접근할 때, ambassador 컨테이너가 프록시 역할을 한다. 예를 들어, 레거시 애플리케이션이 `localhost:3306`으로 MySQL에 접근하는데, 실제 DB는 클라우드에 있다면 ambassador가 SSH 터널이나 Cloud SQL Proxy를 실행하여 `localhost:3306`을 원격 DB로 포워딩한다.
- **Adapter 패턴**: 메인 컨테이너의 출력 형식을 변환한다. 예를 들어, 레거시 애플리케이션이 커스텀 로그 포맷을 출력하면, adapter 컨테이너가 이를 JSON으로 변환하여 표준 로깅 시스템에 맞춘다. 또는 메트릭을 Prometheus 포맷으로 변환(StatsD → Prometheus exporter)할 때 사용한다.
- **Init Container**: 메인 컨테이너가 시작되기 전에 초기화 작업을 실행한다. DB 스키마 마이그레이션, Git 저장소 클론, 설정 파일 다운로드 등이 대표적이다. Init Container가 성공적으로 종료되어야 메인 컨테이너가 시작된다. 여러 개를 정의하면 순차적으로 실행된다.

**심화 질문**

- Sidecar 컨테이너와 DaemonSet의 차이는?
  - Sidecar는 특정 Pod에만 붙는다(예: 특정 애플리케이션의 로그만 수집). DaemonSet은 모든 노드에서 하나씩 실행되어 노드 전체의 로그를 수집한다. 용도에 따라 선택한다.
- Service Mesh가 sidecar를 자동 주입하는 원리는?
  - Admission Webhook(MutatingWebhookConfiguration)을 사용한다. Pod 생성 요청이 API 서버에 도달하면, Istio의 webhook이 가로채서 envoy-proxy 컨테이너를 추가한 뒤 etcd에 저장한다.
- Init Container가 실패하면 어떻게 되는가?
  - Pod는 `Init:Error` 또는 `Init:CrashLoopBackOff` 상태가 되며, 메인 컨테이너는 시작되지 않는다. `restartPolicy`에 따라 Init Container를 재시도한다(Always/OnFailure면 재시도, Never면 실패 유지).

---

## Q2: Deployment가 ReplicaSet을 관리하는 방식과 롤백 메커니즘은?

**핵심 포인트**

- **ReplicaSet 생성 규칙**: Deployment의 `spec.template`(Pod 템플릿)이 변경되면 새로운 ReplicaSet이 생성된다. 이미지 변경, 환경변수 추가, 리소스 제한 변경 등이 해당된다. 반면 `spec.replicas`만 변경하면 기존 ReplicaSet의 `replicas` 필드만 업데이트되고 새 ReplicaSet은 생성되지 않는다.
- **RollingUpdate 동작**: 새 ReplicaSet의 `replicas`를 0에서 시작하여 점진적으로 증가시키고, 동시에 이전 ReplicaSet의 `replicas`를 감소시킨다. `maxSurge=1, maxUnavailable=0`이면 (desired=3 기준) 4 → 3 → 4 → 3 → 4 → 3 순서로 Pod 수가 변동된다.
- **ReplicaSet 보존**: Deployment는 기본적으로 최근 10개 ReplicaSet을 보존한다(`spec.revisionHistoryLimit: 10`). 이전 ReplicaSet의 `replicas`는 0이지만 삭제되지 않아서, 롤백 시 즉시 활성화할 수 있다.
- **롤백 메커니즘**: `kubectl rollout undo`를 실행하면, Deployment Controller가 이전 ReplicaSet의 `replicas`를 desired 값(예: 3)으로 설정하고, 현재 ReplicaSet의 `replicas`를 0으로 설정한다. 이후 RollingUpdate 프로세스가 역방향으로 실행된다. Pod 이미지는 ReplicaSet의 `spec.template`에 저장되어 있으므로, 다시 빌드할 필요가 없다.

**심화 질문**

- Deployment가 Paused 상태일 때는 어떻게 되는가?
  - `kubectl rollout pause deployment/<name>`를 실행하면, 이후 모든 변경사항(이미지 변경, 환경변수 추가)이 실제 적용되지 않고 pending 상태가 된다. 여러 변경을 한 번에 적용하고 싶을 때 사용한다. `kubectl rollout resume`으로 재개하면 누적된 변경사항이 한 번의 RollingUpdate로 처리된다.
- ReplicaSet을 직접 삭제하면 어떻게 되는가?
  - Deployment Controller가 즉시 새로운 ReplicaSet을 생성한다. ReplicaSet은 Deployment의 소유물(OwnerReference)이므로, 직접 수정/삭제하지 말고 항상 Deployment를 통해 관리해야 한다.
- 롤백 후 다시 롤백하면(undo → undo)?
  - 첫 번째 undo로 Revision 2 → Revision 1로 돌아가고, 두 번째 undo로 Revision 1 → Revision 2로 돌아간다. 즉, 토글처럼 동작한다. 특정 리비전으로 가려면 `--to-revision=N`을 사용한다.

---

## Q3: Service의 label selector와 Endpoint 동작 원리는?

**핵심 포인트**

- **Label Selector**: Service의 `spec.selector`는 label 기반으로 Pod를 찾는다. `app: nginx` selector를 가진 Service는 `app=nginx` label을 가진 모든 Pod를 대상으로 한다. 네임스페이스 내부에서만 작동하므로, 다른 네임스페이스의 Pod는 선택되지 않는다.
- **Endpoints 객체**: Service가 생성되면, Endpoint Controller가 자동으로 Endpoints 객체를 생성한다. 이 객체는 label selector와 일치하는 Pod의 IP 주소와 포트 목록을 저장한다. `kubectl get endpoints <service-name>`으로 확인 가능하다.
- **kube-proxy 역할**: 각 노드의 kube-proxy는 Endpoints 객체를 감시하고, iptables 또는 IPVS 규칙을 업데이트한다. 클라이언트가 Service IP(ClusterIP)로 요청을 보내면, iptables 규칙이 이를 가로채서 Pod IP 중 하나로 랜덤 또는 라운드로빈 방식으로 포워딩한다.
- **Readiness Probe와 Endpoint**: Pod의 Readiness Probe가 실패하면, 해당 Pod는 Endpoints 목록에서 제거된다. Service는 트래픽을 보내지 않지만, Pod는 여전히 Running 상태다. Readiness가 다시 성공하면 Endpoints에 추가된다.

**심화 질문**

- Headless Service(ClusterIP: None)는 어떻게 동작하는가?
  - ClusterIP를 할당하지 않고, DNS 쿼리 시 모든 Pod의 IP 주소를 직접 반환한다. StatefulSet과 함께 사용하여 `pod-0.service.default.svc.cluster.local` 형태로 개별 Pod에 접근할 수 있다. Cassandra, Kafka 같은 분산 시스템에서 사용한다.
- ExternalName Service의 용도는?
  - 클러스터 외부의 DNS 이름을 Service로 매핑한다. 예를 들어, `external-db` Service를 `rds.amazonaws.com`으로 매핑하면, 애플리케이션은 `external-db`로 접근하고 실제로는 AWS RDS로 연결된다. 마이그레이션 시 유용하다(온프레미스 DB → 클라우드 DB).
- Service의 sessionAffinity: ClientIP는 어떻게 작동하는가?
  - 클라이언트 IP를 해시하여 항상 같은 Pod로 라우팅한다(Sticky Session). WebSocket이나 세션 기반 애플리케이션에서 사용하지만, Pod가 재시작되면 세션이 끊기므로 근본적인 해결책은 Redis 같은 외부 세션 스토리지를 사용하는 것이다.

---

## Q4: RollingUpdate 전략의 maxSurge/maxUnavailable 튜닝은?

**핵심 포인트**

- **maxSurge**: desired 개수를 초과하여 생성할 수 있는 최대 Pod 수. 절대값(예: 2) 또는 비율(예: 25%)로 설정한다. `replicas: 10, maxSurge: 2`이면 업데이트 중 최대 12개 Pod가 동시에 실행된다. 높을수록 업데이트 속도가 빠르지만, 리소스 소비가 증가한다.
- **maxUnavailable**: desired 개수 미만으로 줄어들 수 있는 최대 Pod 수. `replicas: 10, maxUnavailable: 2`이면 업데이트 중 최소 8개 Pod가 실행된다. 높을수록 업데이트 속도가 빠르지만, 가용성이 감소한다(트래픽 급증 시 부하 처리 불가).
- **보수적 설정** (무중단 최우선): `maxSurge: 1, maxUnavailable: 0`. 한 번에 1개씩만 새 Pod를 추가하고, 기존 Pod는 준비될 때까지 종료하지 않는다. 업데이트 시간이 길지만(10개 Pod → 10분 이상), 항상 desired 개수를 유지하여 트래픽 처리에 문제가 없다.
- **공격적 설정** (속도 우선): `maxSurge: 50%, maxUnavailable: 50%`. 절반을 한 번에 교체한다. 업데이트 시간이 짧지만(10개 Pod → 2분 이내), 순간적으로 절반만 동작하므로 트래픽 급증 시 문제가 생길 수 있다. 개발/스테이징 환경에 적합하다.

**심화 질문**

- `maxSurge: 0, maxUnavailable: 1`로 설정하면?
  - 추가 리소스 없이 업데이트한다. 기존 Pod 1개를 종료하고, 같은 자리에 새 Pod를 생성한다. 리소스가 부족한 환경(minikube)에서 유용하지만, 업데이트 중 desired 개수보다 적은 Pod가 실행되므로 가용성이 일시적으로 떨어진다.
- Readiness Probe가 없으면 어떻게 되는가?
  - Pod가 생성되자마자 "Ready" 상태가 되어 Service Endpoint에 추가된다. 하지만 실제 애플리케이션은 아직 초기화 중이므로, 트래픽이 실패한다. RollingUpdate 중 서비스 장애가 발생할 수 있으므로, Readiness Probe는 필수다.
- Blue-Green 배포를 Deployment로 구현하려면?
  - 두 개의 Deployment(blue, green)를 생성하고, Service의 selector를 변경하여 트래픽을 전환한다. 하지만 Kubernetes는 Blue-Green을 네이티브로 지원하지 않으므로, Argo Rollouts, Flagger 같은 도구를 사용하는 것이 낫다.

---

## Q5: ConfigMap 변경 시 Pod에 반영하는 방법은?

**핵심 포인트**

- **환경변수로 주입한 경우**: Pod 생성 시점에 환경변수가 고정되므로, ConfigMap을 변경해도 기존 Pod에는 반영되지 않는다. Deployment를 재시작해야 한다(`kubectl rollout restart deployment/<name>`). 이는 RollingUpdate를 트리거하여 모든 Pod를 새로 생성한다.
- **볼륨으로 마운트한 경우**: kubelet이 주기적으로(기본 1분마다) ConfigMap을 동기화하여 `/etc/config/` 경로의 파일을 업데이트한다. 애플리케이션이 파일을 다시 읽으면 새 설정이 적용된다. 하지만 대부분의 애플리케이션은 파일 변경을 감지하지 못하므로, SIGHUP 시그널을 보내거나 재시작해야 한다.
- **Reloader 패턴**: Stakater Reloader, Kustomize ConfigMap Generator 같은 도구를 사용하면 ConfigMap 변경 시 Deployment를 자동으로 재시작한다. ConfigMap의 해시값을 Deployment의 annotation에 추가하여, 변경 시 RollingUpdate를 트리거한다.
- **Immutable ConfigMap** (Kubernetes 1.21+): `immutable: true`로 설정하면 ConfigMap을 변경할 수 없다. 변경이 필요하면 새로운 ConfigMap을 생성하고 Deployment를 업데이트한다. 이는 실수로 설정을 변경하는 것을 방지하고, etcd와 kubelet의 부하를 줄인다.

**심화 질문**

- subPath로 마운트한 ConfigMap은 자동 업데이트되는가?
  - 아니다. `volumeMounts.subPath`를 사용하면 kubelet이 동적 업데이트를 하지 않는다. 전체 디렉토리를 마운트하거나, Deployment를 재시작해야 한다.
- ConfigMap 크기 제한은?
  - etcd의 기본 제한은 1MB다. 큰 설정 파일(수백 KB 이상)은 ConfigMap이 아닌 외부 스토리지(S3, ConfigServer)를 사용하는 것이 좋다. Init Container로 다운로드하여 emptyDir에 저장한다.
- 여러 환경(dev, prod)의 ConfigMap을 관리하려면?
  - Kustomize의 ConfigMapGenerator를 사용하거나, Helm의 values.yaml로 환경별 설정을 분리한다. 또는 네임스페이스별로 같은 이름의 ConfigMap을 생성한다(dev namespace → dev 설정, prod namespace → prod 설정).

---

## Q6: Secret은 정말 안전한가? (etcd 암호화, RBAC)

**핵심 포인트**

- **Base64는 암호화가 아니다**: Secret의 데이터는 base64로 인코딩되어 etcd에 저장된다. 이는 단순 인코딩이므로, etcd에 접근할 수 있으면 누구나 디코딩할 수 있다(`echo <base64> | base64 -d`). 따라서 etcd 자체를 보호해야 한다.
- **etcd 암호화**: Kubernetes는 etcd 암호화 기능(`--encryption-provider-config`)을 제공한다. AES-CBC 또는 KMS(AWS KMS, GCP KMS)로 Secret을 암호화하여 저장한다. 하지만 API 서버 메모리에는 평문으로 존재하므로, API 서버 접근 제어가 중요하다.
- **RBAC**: Secret에 접근할 수 있는 사용자/ServiceAccount를 Role/RoleBinding으로 제한한다. 개발자는 ConfigMap만 읽을 수 있고, Secret은 운영팀만 읽을 수 있도록 분리한다. `kubectl get secrets -n kube-system`이 거부되어야 정상이다.
- **External Secrets Operator**: Secret을 Kubernetes에 저장하지 않고, AWS Secrets Manager, HashiCorp Vault, Azure Key Vault에서 가져온다. Operator가 외부 시스템과 동기화하여 Secret을 생성하므로, etcd에는 임시로만 존재한다.

**심화 질문**

- ServiceAccount Token은 어떻게 주입되는가?
  - 모든 Pod는 기본적으로 ServiceAccount를 가지며, `/var/run/secrets/kubernetes.io/serviceaccount/token` 경로에 JWT 토큰이 마운트된다. 이 토큰으로 API 서버에 인증한다. RBAC로 ServiceAccount의 권한을 제한해야 한다(최소 권한 원칙).
- Secret을 환경변수로 주입하면 보안 위험이 있는가?
  - 환경변수는 `kubectl describe pod`, `docker inspect`, 프로세스 목록(`/proc/<pid>/environ`)에서 볼 수 있다. 볼륨 마운트가 더 안전하지만, 애플리케이션이 파일을 읽어야 하므로 코드 변경이 필요할 수 있다.
- Secret의 stringData 필드는 무엇인가?
  - `data` 필드는 base64 인코딩을 요구하지만, `stringData`는 평문으로 작성하면 API 서버가 자동으로 인코딩한다. YAML 가독성이 높아지지만, Git에 커밋하면 평문이 노출되므로 주의해야 한다. SealedSecrets, SOPS 같은 도구로 암호화한 뒤 커밋한다.

---

## Q7: liveness vs readiness vs startup probe 구분과 설정 기준은?

**핵심 포인트**

- **Liveness Probe**: "이 컨테이너가 살아 있는가?"를 체크한다. 실패하면 kubelet이 컨테이너를 재시작한다. 데드락(무한 루프), 메모리 누수로 인한 무응답 상태를 감지한다. 너무 민감하게 설정하면(failureThreshold: 1, periodSeconds: 5) 일시적인 부하로 인해 불필요한 재시작이 발생한다. 보수적으로 설정한다(failureThreshold: 3, periodSeconds: 10).
- **Readiness Probe**: "이 컨테이너가 트래픽을 받을 준비가 되었는가?"를 체크한다. 실패하면 Service Endpoint에서 제거되지만, 컨테이너는 재시작되지 않는다. 초기화 중, 의존성(DB) 연결 실패, 일시적 과부하 시 트래픽을 받지 않도록 한다. RollingUpdate 중 새 Pod가 준비되기 전에 트래픽을 받는 것을 방지한다.
- **Startup Probe**: "이 컨테이너가 시작되었는가?"를 체크한다. 시작이 느린 애플리케이션(Java Spring Boot, 대용량 ML 모델 로딩)을 위한 것이다. Startup Probe가 성공할 때까지 Liveness/Readiness Probe는 실행되지 않는다. `failureThreshold: 30, periodSeconds: 10`이면 최대 5분의 시작 시간을 허용한다. 성공 후에는 Liveness/Readiness가 평소대로 동작한다.
- **조합 전략**: Startup + Liveness + Readiness를 모두 설정한다. Startup은 초기 시작, Liveness는 장기 실행 중 데드락 감지, Readiness는 트래픽 제어에 사용한다.

**심화 질문**

- Liveness Probe 없이 Readiness만 사용하면?
  - 컨테이너가 데드락에 빠져도 재시작되지 않고, 단지 트래픽을 받지 않을 뿐이다. 메모리는 계속 소비되고, 노드 리소스를 낭비한다. 두 Probe를 함께 사용해야 한다.
- Liveness Probe가 애플리케이션의 의존성(DB)을 체크하면 안 되는 이유는?
  - DB가 다운되면 모든 Pod의 Liveness Probe가 실패하여 동시에 재시작된다. 하지만 재시작해도 DB는 여전히 다운 상태이므로, 무한 재시작 루프에 빠진다. Liveness는 애플리케이션 자체의 건강만 체크하고, 의존성은 Readiness에서 체크한다.
- HTTP Probe의 경로(`/healthz`)는 어떻게 구현하는가?
  - 단순히 200 OK를 반환하는 엔드포인트를 만든다. DB 연결, 캐시 상태 등 의존성 체크는 선택적으로 추가한다. Spring Boot Actuator(`/actuator/health`), Express.js의 health check 미들웨어 등 프레임워크가 제공하는 기능을 사용한다.

---

## Q8: Pod QoS 클래스(Guaranteed, Burstable, BestEffort)는?

**핵심 포인트**

- **Guaranteed**: 모든 컨테이너가 `requests == limits`를 가진다. 예를 들어, `requests: {cpu: 500m, memory: 1Gi}`, `limits: {cpu: 500m, memory: 1Gi}`이면 Guaranteed다. 노드에 메모리 압박이 생겨도 가장 마지막에 종료된다. 프로덕션의 중요한 서비스(결제, 인증)에 사용한다.
- **Burstable**: 최소 1개 컨테이너가 `requests` 또는 `limits`를 가지지만, `requests != limits`다. 예를 들어, `requests: {cpu: 100m, memory: 128Mi}`, `limits: {cpu: 500m, memory: 512Mi}`이면 Burstable이다. 평소에는 requests만큼 사용하고, 여유가 있으면 limits까지 사용한다. 메모리 압박 시 BestEffort 다음으로 종료된다.
- **BestEffort**: 모든 컨테이너가 `requests`와 `limits`를 가지지 않는다. 노드의 여유 리소스를 사용하며, 메모리 압박 시 가장 먼저 종료된다. 로그 분석, 배치 작업 같은 비중요 워크로드에 사용한다.
- **Eviction 순서**: BestEffort → Burstable (메모리 사용량이 requests를 초과한 것부터) → Guaranteed. kubelet이 메모리 부족을 감지하면 이 순서로 Pod를 종료한다.

**심화 질문**

- CPU requests와 limits의 차이는?
  - requests는 스케줄러가 노드 선택 시 사용하며, kubelet이 최소 보장한다(cgroup의 cpu.shares). limits는 최대 사용량이며, 초과하면 CPU throttling(속도 제한)이 발생한다. 하지만 CPU는 압축 가능한(compressible) 리소스이므로, limits를 초과해도 컨테이너가 종료되지는 않는다(단지 느려질 뿐).
- 메모리 limits를 초과하면?
  - OOMKilled(Out Of Memory Killed)로 컨테이너가 즉시 종료된다. `kubectl describe pod`에서 `Reason: OOMKilled`를 확인할 수 있다. 메모리는 비압축 가능한(incompressible) 리소스이므로, limits를 초과하면 강제 종료된다.
- Pod의 QoS 클래스는 어디서 확인하는가?
  - `kubectl get pod <pod-name> -o jsonpath='{.status.qosClass}'` 또는 `kubectl describe pod <pod-name>`의 `QoS Class` 필드에서 확인한다. 잘못된 리소스 설정으로 BestEffort가 되면, 메모리 압박 시 예상치 못한 종료가 발생할 수 있다.
