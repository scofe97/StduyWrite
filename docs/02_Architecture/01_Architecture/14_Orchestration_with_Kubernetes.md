# 14장: Orchestration with Kubernetes (쿠버네티스 오케스트레이션)

---

## 📌 핵심 요약

> 이 장에서는 컨테이너 오케스트레이션 플랫폼인 Kubernetes의 아키텍처와 핵심 개념을 다룬다. 핵심은 **Control Plane과 Worker Node로 구성된 클러스터 아키텍처**를 이해하고, **Deployment, Service, Ingress 등의 매니페스트**를 작성하여 컨테이너화된 애플리케이션을 배포하는 것이다. minikube를 활용한 로컬 Kubernetes 환경 구축과 실제 배포 실습을 통해 프로덕션급 시스템 운영 기반을 학습한다.

---

## 🎯 학습 목표

이 내용을 읽고 나면:
- [ ] Kubernetes 클러스터 아키텍처(Control Plane, Worker Node)를 설명할 수 있다
- [ ] Kubernetes의 핵심 컴포넌트(Pod, Deployment, Service, Ingress)의 역할을 이해한다
- [ ] Docker Hub에 컨테이너 이미지를 푸시할 수 있다
- [ ] Kubernetes 매니페스트(YAML)를 작성하고 적용할 수 있다
- [ ] minikube로 로컬 Kubernetes 클러스터를 구축할 수 있다
- [ ] kubectl 명령어로 리소스를 관리할 수 있다

---

## 📖 본문 정리

### 1. Kubernetes 개요

Kubernetes(K8s)는 컨테이너화된 애플리케이션의 배포, 관리, 스케일링을 자동화하는 오픈소스 컨테이너 오케스트레이션 플랫폼이다.

```mermaid
mindmap
  root((Kubernetes))
    역사
      Google 개발
      2014년 오픈소스 공개
      K8s = K + 8글자 + s
    핵심 기능
      자동화된 배포/롤백
      서비스 디스커버리
      로드 밸런싱
      자동 스케일링
      셀프 힐링
    장점
      고가용성
      확장성
      이식성
      선언적 구성
    단점
      높은 학습 곡선
      복잡성
      리소스 오버헤드
```

> 💬 **비유**: Kubernetes는 "항해사(Helmsman)"라는 그리스어에서 유래했다. 컨테이너선(컨테이너화된 앱)을 목적지(프로덕션)까지 안전하게 운항하는 항해사 역할을 한다.

---

### 2. Kubernetes 클러스터 아키텍처

Kubernetes 클러스터는 **Control Plane**과 **Worker Nodes**로 구성된다.

```mermaid
graph TB
    subgraph cp["Control Plane (마스터)"]
        API["kube-api-server<br/>API 서버"]
        ETCD["etcd<br/>클러스터 상태 저장소"]
        SCHED["kube-scheduler<br/>Pod 스케줄링"]
        CM["kube-controller-manager<br/>컨트롤러 관리"]
        CCM["cloud-controller-manager<br/>클라우드 연동"]
    end

    subgraph wn1["Worker Node 1"]
        K1["kubelet"]
        P1["kube-proxy"]
        CR1["Container Runtime"]
        POD1["Pod"]
        POD2["Pod"]
    end

    subgraph wn2["Worker Node 2"]
        K2["kubelet"]
        P2["kube-proxy"]
        CR2["Container Runtime"]
        POD3["Pod"]
    end

    API --> K1
    API --> K2
    K1 --> POD1
    K1 --> POD2
    K2 --> POD3

    style cp fill:#3498db,color:#fff
    style wn1 fill:#27ae60,color:#fff
    style wn2 fill:#27ae60,color:#fff
```

#### Control Plane 컴포넌트

| 컴포넌트 | 역할 |
|---------|------|
| **kube-api-server** | Kubernetes API 노출, 사용자/클러스터 간 통신 처리 |
| **etcd** | 클러스터 구성 데이터 및 상태 정보 저장 (Key-Value 저장소) |
| **kube-scheduler** | 새 Pod를 적절한 노드에 할당 |
| **kube-controller-manager** | 노드 상태, Job 관리, 서비스 계정 생성 등 컨트롤러 실행 |
| **cloud-controller-manager** | 클라우드 프로바이더 API 연동 (AWS, GCP 등) |

#### Worker Node 컴포넌트

| 컴포넌트 | 역할 |
|---------|------|
| **kubelet** | Control Plane과 통신, 컨테이너 실행 상태 모니터링 |
| **kube-proxy** | Pod 간 네트워크 규칙 관리, 로드 밸런싱 |
| **Container Runtime** | 컨테이너 실행 (containerd, CRI-O 등) |

---

### 3. Kubernetes 컴포넌트 분류

```mermaid
graph TB
    subgraph core["Core Components"]
        POD["Pods"]
        NS["Namespaces"]
        DEP["Deployments"]
        RS["ReplicaSets"]
    end

    subgraph network["Networking"]
        SVC["Services"]
        ING["Ingress"]
        NP["Network Policies"]
        SM["Service Mesh"]
    end

    subgraph workload["Workloads"]
        SS["StatefulSets"]
        DS["DaemonSets"]
        JOB["Jobs/CronJobs"]
        HPA["Autoscalers"]
        CRD["CRDs"]
    end

    subgraph storage["Storage"]
        PV["Persistent Volumes"]
        PVC["Persistent Volume Claims"]
        SC["Storage Classes"]
    end

    subgraph config["Configuration"]
        CM["ConfigMaps"]
        SEC["Secrets"]
    end
```

#### Core Components

| 컴포넌트 | 설명 |
|---------|------|
| **Pods** | 가장 작은 배포 단위, 1개 이상의 컨테이너 포함 |
| **Namespaces** | 리소스 논리적 분리 (dev, staging, prod) |
| **Deployments** | 무상태 앱 관리, 롤링 업데이트/롤백 지원 |
| **ReplicaSets** | Pod 복제본 수 유지 |

#### Networking Components

| 컴포넌트 | 설명 |
|---------|------|
| **Services** | Pod 그룹에 안정적인 네트워크 엔드포인트 제공 |
| **Ingress** | 외부 HTTP/HTTPS 트래픽 라우팅 |
| **Network Policies** | Pod 간 트래픽 방화벽 규칙 |
| **Service Mesh** | Istio, Linkerd 등 고급 네트워킹 (mTLS, 트레이싱) |

#### Service 유형

| 유형 | 설명 | 사용 사례 |
|------|------|----------|
| **ClusterIP** | 클러스터 내부에서만 접근 가능 (기본값) | 내부 서비스 간 통신 |
| **NodePort** | 각 노드의 특정 포트로 외부 노출 | 개발/테스트 환경 |
| **LoadBalancer** | 클라우드 로드 밸런서 프로비저닝 | 프로덕션 외부 노출 |
| **ExternalName** | 외부 DNS 이름으로 매핑 | 외부 서비스 연결 |

#### Workload Components

| 컴포넌트 | 설명 |
|---------|------|
| **StatefulSets** | 상태 유지 앱 관리 (DB, 분산 시스템) |
| **DaemonSets** | 모든 노드에 Pod 실행 (로그 수집, 모니터링) |
| **Jobs** | 일회성 작업 (데이터 마이그레이션) |
| **CronJobs** | 스케줄링된 반복 작업 (백업, 리포트) |
| **HPA** | CPU/메모리 기반 Pod 자동 스케일링 |
| **VPA** | Pod 리소스 요청/제한 자동 조정 |

#### Storage & Configuration

| 컴포넌트 | 설명 |
|---------|------|
| **PersistentVolume (PV)** | 클러스터에 프로비저닝된 스토리지 |
| **PersistentVolumeClaim (PVC)** | 애플리케이션의 스토리지 요청 |
| **StorageClass** | 스토리지 유형 정의 (SSD, HDD 등) |
| **ConfigMaps** | 비민감 설정 데이터 저장 (Key-Value) |
| **Secrets** | 민감 정보 암호화 저장 (비밀번호, API 키) |

---

### 4. Kubernetes의 장단점과 사용 시점

#### Kubernetes의 주요 기능

```mermaid
graph LR
    subgraph features["Kubernetes Features"]
        SD["서비스 디스커버리<br/>& 로드 밸런싱"]
        SO["스토리지<br/>오케스트레이션"]
        AR["자동 롤아웃<br/>& 롤백"]
        SH["셀프 힐링"]
        SM["시크릿 &<br/>설정 관리"]
        HS["수평적 스케일링"]
    end
```

| 기능 | 설명 |
|------|------|
| **서비스 디스커버리** | DNS 또는 IP로 컨테이너 접근, 트래픽 분산 |
| **스토리지 오케스트레이션** | 로컬/클라우드 스토리지 자동 마운트 |
| **자동 롤아웃/롤백** | 점진적 업데이트, 문제 시 자동 롤백 |
| **리소스 최적화** | CPU/메모리 요구사항에 따른 노드 할당 |
| **셀프 힐링** | 실패한 컨테이너 재시작, 비정상 컨테이너 교체 |
| **시크릿 관리** | 민감 데이터 안전 저장 및 업데이트 |
| **수평적 스케일링** | 명령어/UI/자동 트리거로 스케일 조정 |

#### 장단점 비교

| 장점 | 단점 |
|------|------|
| 고가용성 및 확장성 | 높은 학습 곡선 |
| 자동화된 배포 및 복구 | 클러스터 관리 복잡성 |
| 선언적 구성 | 소규모 앱에 오버헤드 |
| 다양한 환경 이식성 | 디버깅 어려움 |

#### 사용 시점 판단

| ✅ Kubernetes 사용 | ❌ Kubernetes 미사용 |
|------------------|---------------------|
| 고가용성, 확장성 필요 | 간단한 앱, 최소 스케일링 |
| 마이크로서비스 아키텍처 | 소규모 팀, 전문성 부족 |
| 복잡한 네트워킹 요구 | 빠른 프로토타이핑 |
| 자동화된 배포/롤백 필수 | 단일 서버로 충분 |

---

### 5. 컨테이너 이미지 레지스트리

이미지 레지스트리는 컨테이너 이미지를 저장, 관리, 배포하는 중앙 서비스이다.

```mermaid
graph LR
    subgraph registries["Registry Types"]
        PUB["Public Registry<br/>Docker Hub, Quay.io"]
        PRI["Private Registry<br/>ECR, Harbor"]
        SELF["Self-hosted<br/>Docker Registry"]
    end

    DEV["Developer"] -->|"docker push"| PUB
    PUB -->|"docker pull"| K8S["Kubernetes"]
    PRI -->|"docker pull"| K8S

    style PUB fill:#3498db,color:#fff
    style PRI fill:#e74c3c,color:#fff
    style SELF fill:#f39c12,color:#fff
```

| 유형 | 예시 | 특징 |
|------|------|------|
| **Public** | Docker Hub, Quay.io, GitHub CR | 공개 접근, 커뮤니티 이미지 |
| **Private** | Amazon ECR, Harbor, Docker Hub | 제한된 접근, 보안 강화 |
| **Self-hosted** | Docker Registry, Harbor | 완전한 제어, 인프라 관리 필요 |

#### Docker Hub에 이미지 푸시

```bash
# 1. Docker Hub 로그인
docker login

# 2. 이미지 빌드 (멀티 플랫폼)
docker build --platform linux/amd64,linux/arm64 \
  -t <username>/authentication-services:latest .

# 3. 이미지 푸시
docker push <username>/authentication-services:latest
```

---

### 6. Kubernetes 매니페스트

Kubernetes 매니페스트는 YAML 또는 JSON 형식의 설정 파일로, 리소스의 **원하는 상태(Desired State)**를 정의한다.

```mermaid
graph LR
    YAML["YAML Manifest"] -->|"kubectl apply"| API["API Server"]
    API --> ETCD["etcd<br/>(상태 저장)"]
    API --> CTRL["Controller<br/>(상태 유지)"]
    CTRL --> POD["Pods"]

    style YAML fill:#f39c12,color:#fff
    style API fill:#3498db,color:#fff
```

#### 선언적 vs 명령적 접근

| 선언적 (Declarative) | 명령적 (Imperative) |
|--------------------|-------------------|
| 원하는 상태를 YAML로 정의 | 직접 명령어로 리소스 수정 |
| `kubectl apply -f manifest.yaml` | `kubectl create deployment...` |
| 재현 가능, CI/CD 친화적 | 일회성 작업에 적합 |
| 버전 관리 용이 | 상태 추적 어려움 |

---

### 7. Deployment 매니페스트

Deployment는 Pod의 원하는 상태를 정의하고, 롤링 업데이트와 롤백을 관리한다.

```yaml
# authentication-services-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authentication-services       # 배포 이름
  labels:
    app: authentication-services
spec:
  replicas: 2                          # Pod 복제본 수
  selector:
    matchLabels:
      app: authentication-services     # 관리할 Pod 선택
  template:
    metadata:
      labels:
        app: authentication-services
    spec:
      containers:
        - name: authentication-services
          image: wxesquevixos/authentication-services:latest  # Docker 이미지
          ports:
            - containerPort: 8080      # 컨테이너 포트
          env:                         # 환경 변수
            - name: MONGODB_URL
              value: "mongodb://user:pass@mongodb-service:27017/auth_db"
            - name: USER-SERVICES
              value: "http://user-services.default.svc.cluster.local"
```

#### Deployment 핵심 필드

| 필드 | 설명 |
|------|------|
| `apiVersion` | API 버전 (`apps/v1`) |
| `kind` | 리소스 유형 (`Deployment`) |
| `metadata.name` | 배포 이름 |
| `spec.replicas` | 유지할 Pod 복제본 수 |
| `spec.selector` | 관리할 Pod 레이블 선택 |
| `spec.template` | Pod 템플릿 정의 |
| `containers[].image` | 컨테이너 이미지 |
| `containers[].env` | 환경 변수 주입 |

---

### 8. Service 매니페스트

Service는 Pod 그룹에 안정적인 네트워크 엔드포인트를 제공한다.

```yaml
# authentication-services-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: authentication-services
spec:
  selector:
    app: authentication-services       # 라우팅할 Pod 레이블
  ports:
    - protocol: TCP
      port: 80                         # Service 포트
      targetPort: 8080                 # 컨테이너 포트
  type: ClusterIP                      # 클러스터 내부에서만 접근
```

#### Kubernetes 내부 DNS

```
http://user-services.default.svc.cluster.local
       └─ 서비스명  └─ 네임스페이스
                          └─ svc (서비스)
                               └─ 클러스터 도메인
```

#### 외부 리소스 연결 (ExternalName)

```yaml
# mongodb-external-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
spec:
  type: ExternalName                   # 외부 리소스 연결
  externalName: 192.168.100.89         # 외부 IP/호스트
  ports:
    - port: 27017
      targetPort: 27017
```

---

### 9. Ingress 매니페스트

Ingress는 외부 HTTP/HTTPS 트래픽을 클러스터 내 Service로 라우팅한다.

```yaml
# authentication-services-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: authentication-services-ingress
  annotations:                          # NGINX Ingress 설정
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "*"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE"
spec:
  ingressClassName: nginx               # Ingress 컨트롤러
  rules:
    - host: authentication-services.com # 도메인 라우팅
      http:
        paths:
          - path: /v1/api/auth          # 경로 기반 라우팅
            pathType: Prefix
            backend:
              service:
                name: authentication-services
                port:
                  number: 80
```

```mermaid
sequenceDiagram
    participant Client
    participant Ingress as Ingress Controller
    participant Service
    participant Pod

    Client->>Ingress: GET /v1/api/auth (Host: auth-services.com)
    Ingress->>Service: 라우팅 규칙에 따라 전달
    Service->>Pod: 로드 밸런싱
    Pod-->>Service: 응답
    Service-->>Ingress: 응답
    Ingress-->>Client: 응답
```

---

### 10. minikube 설정 및 kubectl 명령어

minikube는 로컬 개발/테스트용 경량 Kubernetes 구현체이다.

#### minikube 기본 명령어

```bash
# 클러스터 시작
minikube start

# 대시보드 열기
minikube dashboard

# 터널 시작 (LoadBalancer 서비스 노출)
minikube tunnel

# 클러스터 중지
minikube stop

# 클러스터 삭제
minikube delete
```

#### 필수 kubectl 명령어

| 명령어 | 설명 |
|--------|------|
| `kubectl get <resource>` | 리소스 목록 조회 (pods, services, deployments) |
| `kubectl apply -f <file>` | 매니페스트 적용 (생성/업데이트) |
| `kubectl delete -f <file>` | 매니페스트의 리소스 삭제 |
| `kubectl describe <resource> <name>` | 리소스 상세 정보 |
| `kubectl logs <pod-name>` | Pod 로그 조회 |
| `kubectl exec -it <pod> -- <cmd>` | Pod 내 명령 실행 |
| `kubectl get service` | 서비스 목록 및 상태 확인 |

---

### 11. 애플리케이션 배포 실습

#### 배포 단계

```mermaid
graph LR
    A["1. Ingress Controller<br/>설치"] --> B["2. 외부 서비스<br/>매니페스트 적용"]
    B --> C["3. Deployment<br/>적용"]
    C --> D["4. Service<br/>적용"]
    D --> E["5. Ingress<br/>적용"]
    E --> F["6. /etc/hosts<br/>DNS 설정"]
    F --> G["7. 테스트"]

    style A fill:#3498db,color:#fff
    style G fill:#27ae60,color:#fff
```

#### 배포 명령어 예시

```bash
# 1. Ingress Controller 설치 (NGINX)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/cloud/deploy.yaml

# 2. 외부 MongoDB 서비스 배포
kubectl apply -f mongodb-external-service.yaml

# 3. Deployment 배포
kubectl apply -f authentication-services-deployment.yaml

# 4. Service 배포
kubectl apply -f authentication-services-service.yaml

# 5. Ingress 배포
kubectl apply -f authentication-services-ingress.yaml

# 6. 배포 확인
kubectl get pods
kubectl get services
kubectl get ingress

# 7. 로컬 DNS 설정 (/etc/hosts)
# 127.0.0.1  authentication-services.com
```

#### Spring Cloud → Kubernetes 마이그레이션

| Spring Cloud | Kubernetes Native |
|--------------|------------------|
| Eureka (서비스 디스커버리) | Kubernetes Service DNS |
| Config Server | ConfigMaps, Secrets |
| Ribbon (로드 밸런싱) | kube-proxy, Service |
| Zuul/Gateway | Ingress Controller |

> 💡 **팁**: Spring Cloud Kubernetes를 사용하면 Spring Cloud 패턴을 유지하면서 Kubernetes 리소스와 통합할 수 있다.

---

## 🔍 심화 학습

### 추가 조사 내용

#### Helm
- Kubernetes 패키지 매니저
- Chart(패키지)로 복잡한 앱 템플릿화
- 버전 관리 및 롤백 지원

#### Kustomize
- 매니페스트 커스터마이징 도구
- 환경별 오버레이 (dev, staging, prod)
- kubectl에 기본 내장

#### GitOps (ArgoCD, Flux)
- Git 저장소를 단일 진실 공급원으로 사용
- 선언적 배포 자동화
- 지속적 동기화

#### Istio (Service Mesh)
- 서비스 간 통신 관리
- mTLS, 트래픽 관리, 관찰성
- 사이드카 프록시 패턴

### 출처

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Spring Cloud Kubernetes](https://spring.io/projects/spring-cloud-kubernetes)

---

## 💡 실무 적용 포인트

### 이런 상황에서 사용하세요

| 상황 | Kubernetes 리소스 |
|------|------------------|
| 무상태 앱 배포 | Deployment |
| 상태 유지 앱 (DB) | StatefulSet |
| 모든 노드에 Pod 실행 | DaemonSet |
| 일회성 작업 | Job |
| 정기 작업 | CronJob |
| 외부 트래픽 라우팅 | Ingress |
| 내부 서비스 통신 | Service (ClusterIP) |
| 설정 관리 | ConfigMap |
| 비밀 정보 관리 | Secret |

### 주의할 점 / 흔한 실수

- ⚠️ **리소스 제한 미설정**: Pod에 CPU/메모리 limits 필수 설정
- ⚠️ **liveness/readiness probe 누락**: 셀프 힐링 및 롤링 업데이트에 필수
- ⚠️ **Secret을 Deployment에 하드코딩**: Secret 매니페스트 분리 필수
- ⚠️ **네임스페이스 미사용**: 환경 분리를 위해 네임스페이스 활용
- ⚠️ **이미지 태그 latest 사용**: 버전 태그 명시 권장 (v1.0.0)
- ⚠️ **PVC 없이 StatefulSet 사용**: 데이터 영속성 보장 불가

### 면접에서 나올 수 있는 질문

- Q: Kubernetes란 무엇이고 왜 중요한가요?
- Q: Control Plane과 Worker Node의 역할을 설명해주세요.
- Q: Deployment와 StatefulSet의 차이점은 무엇인가요?
- Q: Service의 ClusterIP, NodePort, LoadBalancer 유형의 차이는?
- Q: Ingress의 역할과 구성 방법을 설명해주세요.
- Q: Kubernetes에서 셀프 힐링은 어떻게 동작하나요?
- Q: ConfigMap과 Secret의 차이점은 무엇인가요?

---

## ✅ 핵심 개념 체크리스트

- [ ] Kubernetes 클러스터의 Control Plane과 Worker Node 구성을 설명할 수 있는가?
- [ ] kube-api-server, etcd, kubelet, kube-proxy의 역할을 알고 있는가?
- [ ] Pod, Deployment, ReplicaSet, Service의 관계를 이해하는가?
- [ ] Service 유형(ClusterIP, NodePort, LoadBalancer, ExternalName)을 구분할 수 있는가?
- [ ] Ingress의 역할과 라우팅 규칙 설정 방법을 알고 있는가?
- [ ] YAML 매니페스트의 기본 구조(apiVersion, kind, metadata, spec)를 이해하는가?
- [ ] kubectl apply, get, describe, logs 명령어를 사용할 수 있는가?
- [ ] ConfigMap과 Secret으로 설정을 외부화하는 방법을 알고 있는가?
- [ ] minikube로 로컬 클러스터를 구축하고 앱을 배포할 수 있는가?
- [ ] Desired State와 Kubernetes의 자동 복구 메커니즘을 이해하는가?

---

## 🔗 참고 자료

- 📄 공식 문서: [Kubernetes](https://kubernetes.io/docs/), [minikube](https://minikube.sigs.k8s.io/)
- 📄 도구: [Helm](https://helm.sh/), [Kustomize](https://kustomize.io/), [ArgoCD](https://argo-cd.readthedocs.io/)
- 🎬 추천 영상: [Kubernetes Tutorial for Beginners](https://www.youtube.com/results?search_query=kubernetes+tutorial)
- 📚 연관 서적: "Kubernetes in Action" (Marko Lukša), "The Kubernetes Book" (Nigel Poulton)

---
