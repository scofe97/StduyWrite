# Ch21 - VM Integration 실습
---
> 대응 학습 문서: `learning/ch21-vm-integration/LEARN.md`

실제 VM 온보딩은 GCP VM 인스턴스가 있는 경우에만 가능하다. 그 외 환경에서는 sidecar 없는 Pod로 VM을 시뮬레이션하고, WorkloadEntry/WorkloadGroup 리소스의 동작 원리를 확인한다.

## 사전 조건

- Istio가 설치된 GCP K8s 클러스터
- `istioctl` CLI 설치 완료
- (선택) GCP VM 인스턴스 — 실제 온보딩 실습 시 필요

## 실습 항목

| # | 항목 | 유형 | 예상 시간 |
|---|------|------|----------|
| 1 | WorkloadGroup 리소스 생성 | 리소스 배포 | 10분 |
| 2 | WorkloadEntry 수동 등록 (IP/labels) | 리소스 배포 | 10분 |
| 3 | VM 시뮬레이션: sidecar 없는 Pod 배포 | 리소스 배포 | 20분 |
| 4 | ServiceEntry vs WorkloadEntry 비교 | 개념 분석 | 15분 |
| 5 | `istioctl proxy-config endpoint`에서 VM 엔드포인트 확인 | 명령어 실행 | 10분 |
| 6 | (선택) GCP VM에서 실제 Istio sidecar 설치 | VM 설정 | 60분 |

## 실습 상세

### 1. WorkloadGroup 리소스 생성

WorkloadGroup은 VM 그룹의 템플릿 역할을 한다. Kubernetes의 Deployment가 Pod 스펙을 정의하듯, WorkloadGroup은 VM WorkloadEntry의 공통 속성을 정의한다:

```bash
# 실습용 네임스페이스 생성
kubectl create namespace vm-demo
kubectl label namespace vm-demo istio-injection=enabled

# WorkloadGroup 생성
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: WorkloadGroup
metadata:
  name: legacy-backend
  namespace: vm-demo
spec:
  metadata:
    labels:
      app: legacy-backend
      version: v1
    annotations:
      security.istio.io/tlsMode: istio
  template:
    ports:
      http: 8080
    serviceAccount: legacy-sa
  probe:
    httpGet:
      path: /healthz
      port: 8080
    periodSeconds: 15
    failureThreshold: 3
EOF
```

WorkloadGroup을 확인한다:

```bash
kubectl get workloadgroup -n vm-demo
kubectl describe workloadgroup legacy-backend -n vm-demo
```

### 2. WorkloadEntry 수동 등록 (IP/labels)

WorkloadEntry는 실제 VM 인스턴스를 메시에 등록하는 리소스다. VM의 IP 주소와 레이블을 직접 지정한다:

```bash
# WorkloadEntry 생성 (실습용 임의 IP 사용)
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: WorkloadEntry
metadata:
  name: legacy-backend-vm1
  namespace: vm-demo
spec:
  address: 10.128.0.50   # 실제 환경에서는 VM의 내부 IP
  labels:
    app: legacy-backend
    version: v1
    instance: vm1
  ports:
    http: 8080
  serviceAccount: legacy-sa
  network: network1
EOF
```

WorkloadEntry가 생성되었는지 확인한다:

```bash
kubectl get workloadentry -n vm-demo
kubectl describe workloadentry legacy-backend-vm1 -n vm-demo
```

WorkloadEntry를 등록하면 istiod가 해당 IP를 서비스 엔드포인트로 인식한다. 이때 Service 리소스의 selector와 WorkloadEntry의 labels가 일치해야 트래픽이 라우팅된다:

```bash
# WorkloadEntry와 매핑되는 Service 생성
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: legacy-backend
  namespace: vm-demo
spec:
  selector:
    app: legacy-backend
  ports:
  - port: 80
    targetPort: 8080
    name: http
EOF
```

### 3. VM 시뮬레이션: sidecar 없는 Pod 배포

GCP VM 없이 VM 동작을 시뮬레이션하려면 istio-injection 레이블이 없는 별도 네임스페이스에서 sidecar 미주입 Pod를 사용한다:

```bash
# sidecar 주입이 비활성화된 네임스페이스 생성
kubectl create namespace vm-sim
# 레이블을 붙이지 않음 → istio-injection=disabled 상태

# VM을 흉내내는 Pod 배포
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: vm-simulator
  namespace: vm-sim
  labels:
    app: legacy-backend
    version: v1
spec:
  containers:
  - name: app
    image: hashicorp/http-echo
    args: ["-text=hello from vm-simulator"]
    ports:
    - containerPort: 8080
EOF

# Pod IP 확인
kubectl get pod vm-simulator -n vm-sim -o wide
```

확인된 Pod IP를 WorkloadEntry의 `address`에 업데이트한다:

```bash
VM_IP=$(kubectl get pod vm-simulator -n vm-sim -o jsonpath='{.status.podIP}')
echo "VM Simulator IP: $VM_IP"

kubectl patch workloadentry legacy-backend-vm1 -n vm-demo \
  --type='json' \
  -p="[{\"op\": \"replace\", \"path\": \"/spec/address\", \"value\": \"$VM_IP\"}]"
```

### 4. ServiceEntry vs WorkloadEntry 비교

두 리소스는 모두 메시 외부 엔드포인트를 등록하지만, 목적과 사용 맥락이 다르다:

| 항목 | ServiceEntry | WorkloadEntry |
|------|-------------|---------------|
| 목적 | 외부 서비스(DNS/IP)를 메시에 등록 | VM 인스턴스를 K8s 서비스와 연결 |
| 엔드포인트 | 정적 IP 또는 외부 DNS | VM의 IP (WorkloadGroup 소속 가능) |
| 서비스 계정 | 없음 | 지정 가능 (SPIFFE 신원 부여) |
| 헬스 체크 | 없음 | WorkloadGroup의 probe 상속 |
| 주요 사용처 | 외부 API, 레거시 데이터베이스 | VM 기반 서비스의 점진적 메시 편입 |

ServiceEntry만으로도 VM IP를 직접 등록할 수 있다. WorkloadEntry는 VM에 SPIFFE 신원(서비스 계정 기반 mTLS)을 부여하고 헬스 체크를 지원한다는 점에서 차이가 있다.

실습으로 두 방식을 비교한다:

```bash
# ServiceEntry 방식으로 동일한 VM IP 등록
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: legacy-backend-se
  namespace: vm-demo
spec:
  hosts:
  - legacy-backend-se.vm-demo.svc.cluster.local
  location: MESH_INTERNAL
  ports:
  - number: 8080
    name: http
    protocol: HTTP
  resolution: STATIC
  endpoints:
  - address: $VM_IP
    labels:
      app: legacy-backend
EOF
```

### 5. `istioctl proxy-config endpoint`에서 VM 엔드포인트 확인

메시 내 sidecar가 VM IP를 엔드포인트로 인식하고 있는지 확인한다:

```bash
# 메시 내 테스트 Pod 배포
kubectl run debug-pod --image=istio/base --restart=Never -n vm-demo -- sleep 3600
kubectl wait --for=condition=Ready pod/debug-pod -n vm-demo --timeout=60s

# debug-pod의 Envoy가 알고 있는 엔드포인트 목록 확인
istioctl proxy-config endpoints debug-pod.vm-demo | grep legacy-backend

# 특정 클러스터의 엔드포인트 상세 확인
istioctl proxy-config endpoints debug-pod.vm-demo --cluster "outbound|80||legacy-backend.vm-demo.svc.cluster.local"
```

WorkloadEntry로 등록된 VM IP(`$VM_IP:8080`)가 `HEALTHY` 상태로 목록에 나타나면 정상이다.

전체 메시 관점에서 엔드포인트를 확인하려면 istiod의 endpoint 뷰를 사용한다:

```bash
istioctl proxy-status | grep vm-demo
```

### 6. (선택) GCP VM에서 실제 Istio sidecar 설치

GCP VM 인스턴스가 있는 경우에만 진행한다. VM이 K8s 클러스터와 동일한 VPC에 있어야 한다:

```bash
# 1. VM용 서비스 어카운트 생성
kubectl create serviceaccount legacy-sa -n vm-demo

# 2. istioctl로 VM 온보딩 파일 생성
istioctl x workload entry configure \
  --file workloadgroup.yaml \
  --output vm-bootstrap/ \
  --clusterID cluster1 \
  --ingressIP $(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 3. 생성된 파일을 VM으로 복사
# gcloud compute scp vm-bootstrap/* VM_NAME:/tmp/

# 4. VM에서 sidecar 설치 (VM 내부에서 실행)
# sudo dpkg -i /tmp/istio-sidecar.deb
# sudo cp /tmp/cluster.env /var/lib/istio/envoy/
# sudo cp /tmp/root-cert.pem /etc/certs/root-cert.pem
# sudo systemctl start istio
```

## 정리 (Cleanup)

```bash
# 실습 리소스 삭제
kubectl delete workloadentry legacy-backend-vm1 -n vm-demo
kubectl delete workloadgroup legacy-backend -n vm-demo
kubectl delete serviceentry legacy-backend-se -n vm-demo
kubectl delete service legacy-backend -n vm-demo
kubectl delete pod debug-pod -n vm-demo --force

# 시뮬레이션 Pod 삭제
kubectl delete pod vm-simulator -n vm-sim

# 네임스페이스 삭제
kubectl delete namespace vm-demo vm-sim
