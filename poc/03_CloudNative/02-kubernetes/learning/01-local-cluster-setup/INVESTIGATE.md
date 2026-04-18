# Ch01. 로컬 클러스터 구성 - 점검 질문

## Q1: minikube vs kind vs k3d 선택 기준은 무엇인가?

**핵심 포인트**

- **학습/개발 우선순위**: minikube는 애드온 생태계가 풍부하여 한 줄 명령어로 Ingress, Dashboard, Metrics Server를 활성화할 수 있다. 초기 학습 시 Kubernetes 개념에 집중하고, 인프라 설정에 시간을 쓰지 않으려면 minikube가 적합하다.
- **CI/CD 파이프라인**: kind(Kubernetes IN Docker)는 Docker 컨테이너 안에 클러스터를 생성하므로 시작 속도가 빠르고(20초), GitHub Actions나 GitLab CI에서 매트릭스 테스트(여러 Kubernetes 버전 동시 테스트)를 쉽게 구성할 수 있다. `kind create cluster --config kind-config.yaml`로 멀티 노드, HA Control Plane을 간단히 구성 가능하다.
- **리소스 제약 환경**: k3d는 Rancher의 k3s(경량 Kubernetes)를 기반으로 하여 메모리 사용량이 낮다(512MB 이하). IoT 디바이스, Raspberry Pi, 또는 저사양 노트북에서 클러스터를 실행하거나, 동시에 10개 이상의 클러스터를 띄워야 하는 경우(멀티테넌시 테스트) k3d가 유리하다.
- **프로덕션 유사성**: kind는 kubeadm을 사용하여 클러스터를 부트스트랩하므로, 프로덕션의 kubeadm 기반 클러스터와 가장 유사하다. HA(고가용성) 테스트, etcd 백업/복구, 인증서 관리 등을 실험하려면 kind가 적합하다.

**심화 질문**

- Docker Desktop이 설치되지 않은 환경(VM, 원격 서버)에서는 어떤 도구를 선택해야 하는가?
  - minikube는 QEMU/KVM 드라이버를 지원하므로 Docker 없이도 사용 가능하다. kind는 Docker 필수이므로 사용 불가. k3d도 Docker 필수.
- CI 환경에서 kind를 사용할 때, 이미지 로딩 시간을 최소화하려면?
  - `kind load docker-image <image>` 명령으로 로컬 이미지를 클러스터에 직접 로드하거나, Registry 컨테이너를 클러스터와 함께 실행하여 네트워크를 공유한다.
- 멀티 클러스터 환경(Federation, Service Mesh)을 테스트하려면?
  - kind/k3d는 여러 클러스터를 동시에 실행하는 데 유리하다. minikube도 프로필(`-p` 플래그)로 가능하지만 리소스 소비가 크다.

---

## Q2: minikube driver(docker vs hyperkit vs qemu) 차이와 선택 기준은?

**핵심 포인트**

- **Docker 드라이버**: 가장 널리 사용되며 macOS/Linux/Windows 모두 지원한다. Docker Desktop이 설치되어 있다면 기본 선택지다. 클러스터가 Docker 컨테이너로 실행되므로 `docker ps`로 확인 가능하며, 시작 속도가 빠르다(30초). 하지만 Docker Desktop 자체가 무겁고(메모리 2GB 이상 소비), Nested Virtualization을 지원하지 않아 VM 내부에서 실행 불가.
- **Hyperkit 드라이버** (macOS 전용): 경량 하이퍼바이저로 Docker 없이 VM을 생성한다. Docker Desktop을 설치하고 싶지 않거나, VirtualBox의 성능 문제를 겪는 경우 사용한다. 하지만 minikube 1.30 이후 Deprecated 상태이며, QEMU로 대체 권장.
- **QEMU 드라이버**: 크로스 플랫폼 하이퍼바이저로 macOS(Apple Silicon), Linux, Windows 모두 지원한다. Docker 없이 순수 VM으로 클러스터를 실행하며, Nested Virtualization을 지원하여 VM 내부에서도 작동한다. Apple M1/M2 Mac에서 Docker Desktop의 성능 문제(x86 에뮬레이션)가 있을 때 QEMU를 사용하면 네이티브 ARM64 속도를 낼 수 있다.
- **VirtualBox 드라이버**: 과거에 많이 사용되었지만 현재는 비추천. 라이선스 이슈(Oracle), 느린 시작 속도(60초+), macOS Monterey 이후 지원 불안정 등의 문제가 있다.

**심화 질문**

- Docker Desktop 없이 minikube를 실행하려면 어떤 드라이버를 사용해야 하는가?
  - macOS: QEMU (`brew install qemu && minikube start --driver=qemu`)
  - Linux: KVM (`minikube start --driver=kvm2`)
  - Windows: Hyper-V (`minikube start --driver=hyperv`) 또는 WSL2 + Docker
- Apple Silicon Mac(M1/M2)에서 Docker 드라이버 사용 시 발생하는 문제는?
  - Docker Desktop은 x86 이미지를 Rosetta 2로 에뮬레이션하므로 성능이 저하될 수 있다. ARM64 네이티브 이미지를 사용하거나, QEMU 드라이버로 전환하면 해결된다.
- Nested Virtualization이 필요한 상황은?
  - AWS EC2, GCP Compute Engine 같은 VM 인스턴스 내부에서 minikube를 실행하거나, KubeVirt(VM을 Pod로 실행)를 테스트할 때 필요하다. Docker/Hyperkit은 Nested Virtualization을 지원하지 않으므로 QEMU/KVM을 사용해야 한다.

---

## Q3: kubectl context와 kubeconfig 구조는 어떻게 이루어져 있는가?

**핵심 포인트**

- **kubeconfig 파일**: `~/.kube/config`(기본 경로)에 저장되며, 여러 클러스터의 접속 정보를 관리한다. `clusters`(API 서버 주소), `users`(인증 정보), `contexts`(클러스터+사용자+네임스페이스 조합)로 구성된다. `current-context`가 현재 사용 중인 클러스터를 가리킨다.
- **context 전환**: `kubectl config use-context minikube`로 컨텍스트를 전환하면, 이후 모든 kubectl 명령어가 해당 클러스터를 대상으로 실행된다. `kubectl config current-context`로 현재 컨텍스트를 확인한다.
- **namespace 기본값**: context마다 기본 namespace를 설정할 수 있다. `kubectl config set-context --current --namespace=dev`로 설정하면, 이후 `kubectl get pods`가 `dev` 네임스페이스를 대상으로 한다. `-n` 플래그로 오버라이드 가능.
- **여러 클러스터 관리**: minikube, GKE, EKS, on-premise 클러스터를 모두 하나의 kubeconfig에 저장하고, context로 전환하며 작업할 수 있다. `KUBECONFIG` 환경변수로 여러 kubeconfig 파일을 병합 가능(`export KUBECONFIG=~/.kube/config:~/.kube/config-prod`).

**심화 질문**

- kubeconfig에 저장된 인증 정보가 탈취되면 어떤 위험이 있는가?
  - 클러스터 관리자 권한(cluster-admin)을 가진 인증서가 있다면, 공격자가 모든 리소스를 삭제하거나 악성 Pod를 배포할 수 있다. kubeconfig는 git에 커밋하지 말고, `.gitignore`에 추가해야 한다. 프로덕션에서는 OIDC(Google, Azure AD), IAM Role(AWS) 기반 인증을 사용하여 인증서 만료 시간을 짧게(1시간) 설정한다.
- `kubectl config view` 출력에서 비밀번호가 보이지 않는 이유는?
  - 기본적으로 민감 정보(certificate-authority-data, client-certificate-data)는 `<REDACTED>`로 마스킹된다. `kubectl config view --raw`로 원본을 볼 수 있지만, 절대 로그나 공개 채널에 공유하면 안 된다.
- 여러 팀이 하나의 클러스터를 사용할 때 context를 어떻게 구성하는가?
  - 팀별로 namespace를 나누고(team-a, team-b), context마다 기본 namespace를 설정한다. RBAC(Role-Based Access Control)로 각 팀이 자신의 namespace만 접근하도록 제한한다.

---

## Q4: 로컬 클러스터의 한계와 프로덕션 차이는?

**핵심 포인트**

- **노드 장애 시뮬레이션 불가**: 로컬 클러스터는 단일 노드이므로, 노드가 다운되었을 때 Pod가 다른 노드로 재스케줄링되는 과정을 테스트할 수 없다. 멀티 노드(`--nodes=3`)로 실행해도, 실제 네트워크 파티션(Split-Brain)이나 노드 간 지연(Latency)은 재현하기 어렵다.
- **스토리지 제한**: 프로덕션은 EBS(AWS), Persistent Disk(GCP), Ceph, Longhorn 같은 네트워크 스토리지를 사용하며, Zone 장애 시에도 데이터를 보존한다. 로컬은 호스트 파일시스템(`/tmp/hostpath-provisioner`)을 마운트하므로, minikube를 삭제하면 데이터가 사라진다. StatefulSet의 PersistentVolumeClaim 동작은 확인 가능하지만, 실제 데이터 내구성(Durability)은 테스트 불가.
- **LoadBalancer 타입 Service**: 프로덕션에서는 클라우드 제공자의 로드 밸런서(ELB, NLB)가 자동으로 생성되지만, 로컬에서는 `minikube tunnel`로 수동 터널을 생성하거나, NodePort로 접근해야 한다. MetalLB를 설치하면 로컬에서 LoadBalancer IP를 할당받을 수 있지만, 이는 프로덕션의 실제 로드 밸런서와 다르다.
- **보안 및 네트워크 정책**: 프로덕션은 NetworkPolicy, Pod Security Standards(PSS), Service Mesh(mTLS)를 사용하여 Pod 간 트래픽을 제한한다. 로컬에서도 NetworkPolicy를 적용할 수 있지만, 실제 DMZ 구성, 방화벽 규칙, VPC 피어링 등은 재현 불가.

**심화 질문**

- 로컬에서 멀티 노드 시나리오를 최대한 유사하게 재현하려면?
  - kind로 3-node 클러스터를 생성하고, `kubectl drain`으로 노드를 비활성화하여 Pod Eviction을 테스트한다. Chaos Engineering 도구(Chaos Mesh, Litmus)를 설치하여 네트워크 지연, CPU 스파이크를 주입할 수 있다.
- StatefulSet의 데이터 내구성을 로컬에서 테스트하려면?
  - Longhorn, OpenEBS 같은 클라우드 네이티브 스토리지를 minikube에 설치한다. 하지만 단일 노드이므로 replication은 의미가 없고, 주로 스냅샷/복구 기능을 테스트한다.
- 로컬 클러스터에서 프로덕션 배포 전 검증할 수 있는 항목은?
  - YAML 매니페스트 문법, Deployment 전략(RollingUpdate), ConfigMap/Secret 주입, Resource Requests/Limits, Liveness/Readiness Probe, Horizontal Pod Autoscaler(HPA) 동작 등. 이는 로컬에서 충분히 검증 가능하다.

---

## Q5: 애드온의 역할과 프로덕션 대응 컴포넌트는?

**핵심 포인트**

- **Ingress Controller**: 외부 HTTP(S) 트래픽을 클러스터 내부 Service로 라우팅한다. `minikube addons enable ingress`는 NGINX Ingress Controller를 설치한다. 프로덕션에서는 NGINX Ingress, Traefik, Istio Gateway, AWS ALB Ingress Controller 등을 사용하며, TLS 인증서 자동 갱신(cert-manager), WAF(Web Application Firewall) 통합이 추가된다.
- **Metrics Server**: CPU, 메모리 사용량을 수집하여 `kubectl top` 명령어와 Horizontal Pod Autoscaler(HPA)가 사용한다. 프로덕션에서는 Prometheus + Grafana로 더 상세한 메트릭(요청 수, 레이턴시, 에러율)을 수집하고, AlertManager로 알림을 보낸다.
- **Dashboard**: 웹 UI로 Pod, Service, Deployment를 조회/수정한다. 프로덕션에서는 보안 이슈(인증 우회 취약점)로 인해 대부분 비활성화하고, Lens(데스크톱 앱), k9s(터미널 UI), Grafana 대시보드를 대신 사용한다.
- **Storage Provisioner**: PersistentVolumeClaim을 생성하면 자동으로 PersistentVolume을 프로비저닝한다. 로컬은 `storage-provisioner` 애드온이 호스트 경로를 할당하지만, 프로덕션은 CSI(Container Storage Interface) 드라이버(EBS CSI, GCE PD CSI)가 클라우드 스토리지를 동적으로 생성한다.

**심화 질문**

- Ingress Controller 없이 외부 트래픽을 받으려면?
  - NodePort Service를 사용하거나, `kubectl port-forward`로 로컬 포트를 Pod에 연결한다. 하지만 도메인 기반 라우팅(예: api.example.com → api-service, web.example.com → web-service)은 Ingress 없이 불가능하다.
- metrics-server와 Prometheus의 차이는?
  - metrics-server는 최근 15초~1분의 메트릭만 메모리에 저장하며, 주로 HPA, VPA(Vertical Pod Autoscaler)가 사용한다. Prometheus는 장기 저장(retention 15일 이상)하고, PromQL로 복잡한 쿼리(예: 95th percentile latency)를 실행할 수 있다.
- minikube의 storage-provisioner는 어떻게 동작하는가?
  - PersistentVolumeClaim이 생성되면, storage-provisioner가 minikube VM 내부의 `/tmp/hostpath-provisioner/<pvc-name>/` 경로에 디렉토리를 만들고, 이를 PersistentVolume으로 바인딩한다. `minikube ssh`로 접속하여 실제 파일을 확인할 수 있다.

---

## Q6: minikube 리소스 관리 전략은?

**핵심 포인트**

- **CPU/메모리 할당**: 기본값(CPU 2개, 메모리 2GB)은 학습용으로 충분하지만, Ingress + Monitoring + 여러 애플리케이션을 실행하려면 부족하다. `minikube start --cpus=4 --memory=8192`로 시작하되, 노트북의 전체 리소스를 모두 할당하면 호스트 OS가 느려지므로 50~70% 정도만 할당한다(16GB 노트북 → minikube 8GB).
- **디스크 용량**: 기본 20GB가 할당되며, 이미지를 많이 다운로드하면 부족할 수 있다. `minikube start --disk-size=40g`로 증설하거나, `minikube ssh && docker system prune -a`로 미사용 이미지를 정리한다.
- **여러 클러스터 관리 시**: 프로필(`-p`)로 여러 클러스터를 실행하면 리소스가 N배로 소비된다. 동시에 3개 이상 실행하면 노트북이 버벅거리므로, 사용하지 않는 클러스터는 `minikube stop -p <profile>`로 중지한다.
- **애드온 선택적 활성화**: 모든 애드온을 활성화하면 메모리를 1GB 이상 추가 소비한다. 실습에 필요한 애드온만 활성화하고(`ingress`, `metrics-server`), dashboard는 필요할 때만 `minikube dashboard` 명령으로 임시 실행한다.

**심화 질문**

- minikube 클러스터가 메모리 부족으로 Eviction이 발생하면?
  - kubelet이 메모리 압박(Memory Pressure)을 감지하면, 우선순위가 낮은 Pod(BestEffort QoS)부터 종료한다. `kubectl describe node minikube`에서 `Conditions`를 확인하여 `MemoryPressure=True`인지 체크하고, `minikube stop && minikube start --memory=12288`로 메모리를 증설한다.
- minikube 이미지 캐싱 전략은?
  - `minikube cache add nginx:1.25`로 이미지를 미리 다운로드하면, 클러스터를 재시작해도 이미지가 보존된다. 여러 프로필에서 동일한 이미지를 사용할 때 유용하다.
- 리소스 제약 환경(노트북 8GB)에서 minikube를 실행하려면?
  - k3d로 전환하거나, minikube에서 불필요한 시스템 Pod를 비활성화한다(`minikube start --extra-config=kubeadm.skip-phases=addon/coredns`). 또는 클라우드 IDE(GitHub Codespaces, GitPod)를 사용하여 원격에서 클러스터를 실행한다.
