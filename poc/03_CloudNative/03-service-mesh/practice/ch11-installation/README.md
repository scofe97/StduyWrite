# Ch11 - Istio 설치 실습
---
> 대응 학습 문서: `learning/ch11-installation/LEARN.md`

istioctl과 Helm 두 가지 방법으로 Istio를 설치하고, 프로파일별 차이를 직접 비교한다. Prometheus/Grafana/Kiali/Jaeger 애드온을 설치하여 관찰 가능성 스택을 구성한다.

## 사전 조건

GCP K8s 클러스터에 접속 가능한 상태여야 한다. `istioctl`이 설치되어 있어야 하며, Helm 3.x가 설치되어 있어야 한다. 기존 Istio가 설치된 경우 실습 3(프로파일 비교)부터 진행해도 된다.

```bash
# 사전 확인
istioctl version
helm version
kubectl cluster-info
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | istioctl 설치 | demo 프로파일로 전체 설치 | istiod Running 확인 |
| 2 | Helm 설치 | base/istiod/ingress 순서대로 설치 | 3개 컴포넌트 Running 확인 |
| 3 | 프로파일 비교 | default/demo/minimal 덤프 비교 | 컴포넌트 차이 확인 |
| 4 | Namespace injection | istio-injection 레이블 설정 | 신규 Pod에 sidecar 주입 확인 |
| 5 | 애드온 설치 | samples/addons/ 일괄 설치 | Grafana/Kiali UI 접속 |
| 6 | NodePort 외부 접속 | ingressgateway NodePort 설정 | 클러스터 외부에서 접속 |

## 실습 상세

### 1. istioctl install (demo 프로파일)

**목표**: 가장 빠르게 Istio 전체 스택을 설치하는 방법을 익힌다. demo 프로파일은 모든 기능을 활성화하므로 학습 환경에 적합하다.

**단계**:

```bash
# istioctl 최신 버전 다운로드 (이미 설치되어 있으면 생략)
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.*/
export PATH=$PWD/bin:$PATH

# 사전 검사 (클러스터 호환성 확인)
istioctl x precheck

# demo 프로파일로 설치
istioctl install --set profile=demo -y

# 설치 확인
kubectl get pods -n istio-system
kubectl get svc -n istio-system
```

**검증**: `istiod`, `istio-ingressgateway`, `istio-egressgateway` Pod이 모두 `Running` 상태여야 한다.

```
NAME                                    READY   STATUS    RESTARTS   AGE
istio-egressgateway-xxx                 1/1     Running   0          1m
istio-ingressgateway-xxx                1/1     Running   0          1m
istiod-xxx                              1/1     Running   0          1m
```

### 2. Helm으로 설치

**목표**: 프로덕션 환경에서 일반적으로 사용하는 Helm 방식으로 설치한다. 각 컴포넌트를 독립적으로 관리할 수 있다는 점이 istioctl 방식과 다르다.

**단계**:

```bash
# 기존 istioctl 설치가 있으면 먼저 제거
istioctl uninstall --purge -y
kubectl delete namespace istio-system --ignore-not-found=true

# Helm 저장소 추가
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

# 네임스페이스 생성
kubectl create namespace istio-system

# Step 1: istio-base (CRD 설치)
helm install istio-base istio/base \
  -n istio-system \
  --set defaultRevision=default

# Step 2: istiod (Control Plane)
helm install istiod istio/istiod \
  -n istio-system \
  -f ../install/sidecar/istio-values.yaml \
  --wait

# Step 3: ingress gateway (Data Plane)
kubectl create namespace istio-ingress
helm install istio-ingressgateway istio/gateway \
  -n istio-ingress \
  --wait

# 설치 검증
helm list -n istio-system
helm list -n istio-ingress
kubectl get pods -n istio-system
kubectl get pods -n istio-ingress
```

**검증**: `helm list` 결과에 `istio-base`, `istiod`가 `deployed` 상태로 표시되어야 한다.

### 3. 프로파일 비교

**목표**: default/demo/minimal 프로파일의 컴포넌트 차이를 이해한다. 이를 통해 목적에 맞는 프로파일을 선택할 수 있다.

**단계**:

```bash
# 각 프로파일 덤프 (설치 없이 설정만 확인)
istioctl profile dump default > /tmp/profile-default.yaml
istioctl profile dump demo > /tmp/profile-demo.yaml
istioctl profile dump minimal > /tmp/profile-minimal.yaml

# 컴포넌트 활성화 여부 비교
echo "=== default ===" && \
  grep -E "enabled|egressGateways|ingressGateways" /tmp/profile-default.yaml | head -20

echo "=== demo ===" && \
  grep -E "enabled|egressGateways|ingressGateways" /tmp/profile-demo.yaml | head -20

echo "=== minimal ===" && \
  grep -E "enabled|egressGateways|ingressGateways" /tmp/profile-minimal.yaml | head -20

# 두 프로파일 차이 직접 비교
diff /tmp/profile-default.yaml /tmp/profile-demo.yaml | head -50

# 사용 가능한 프로파일 전체 목록
istioctl profile list
```

**검증**: minimal은 istiod만 포함하고, default는 ingressgateway가 추가되며, demo는 egressgateway까지 포함한다는 것을 확인한다.

### 4. Namespace에 sidecar injection 설정

**목표**: 애플리케이션 네임스페이스에 자동 주입을 설정하고, 신규 Pod에 sidecar가 주입되는지 확인한다.

**단계**:

```bash
# bookinfo 네임스페이스 생성
kubectl create namespace bookinfo

# sidecar injection 활성화
kubectl label namespace bookinfo istio-injection=enabled

# 레이블 확인
kubectl get namespace bookinfo --show-labels

# bookinfo 앱 배포
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/bookinfo/platform/kube/bookinfo.yaml -n bookinfo

# Pod 상태 확인 (각 Pod READY가 2/2 이어야 함)
kubectl get pods -n bookinfo

# injection 비활성화 방법 (참고용)
# kubectl label namespace bookinfo istio-injection-

# 특정 Pod만 injection 제외하는 어노테이션 (참고용)
# kubectl annotate pod <pod-name> sidecar.istio.io/inject="false"
```

**검증**: `kubectl get pods -n bookinfo`에서 모든 Pod의 `READY` 열이 `2/2`로 표시되어야 한다.

### 5. 애드온 설치 (Prometheus/Grafana/Kiali/Jaeger)

**목표**: 관찰 가능성 스택을 설치하여 트래픽 흐름, 메트릭, 추적 정보를 시각화한다.

**단계**:

```bash
# Istio 소스에서 애드온 매니페스트 다운로드
ISTIO_VERSION=$(istioctl version --short 2>/dev/null | head -1 | awk '{print $NF}')
echo "Istio version: $ISTIO_VERSION"

# 애드온 일괄 설치
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml

# 설치 확인 (모두 Running까지 대기)
kubectl rollout status deployment/prometheus -n istio-system
kubectl rollout status deployment/grafana -n istio-system
kubectl rollout status deployment/kiali -n istio-system
kubectl rollout status deployment/jaeger -n istio-system

# 접속 확인 (브라우저 열기)
istioctl dashboard grafana &
istioctl dashboard kiali &
```

**검증**: `kubectl get pods -n istio-system`에서 prometheus, grafana, kiali, jaeger Pod이 모두 `Running` 상태여야 한다.

### 6. NodePort로 외부 접속 설정

**목표**: GCP K8s 클러스터 외부(로컬 브라우저)에서 ingressgateway에 직접 접속하는 방법을 설정한다. LoadBalancer 타입이 지원되지 않는 환경에서 NodePort를 사용한다.

**단계**:

```bash
# 현재 ingressgateway 서비스 타입 확인
kubectl get svc -n istio-ingress istio-ingressgateway

# NodePort로 패치 (LoadBalancer → NodePort)
kubectl patch svc istio-ingressgateway -n istio-ingress \
  -p '{"spec": {"type": "NodePort"}}'

# 할당된 NodePort 확인
kubectl get svc istio-ingressgateway -n istio-ingress \
  -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}'

# 노드 외부 IP 확인
kubectl get nodes -o wide

# 접속 테스트 (NODE_IP와 NODE_PORT를 실제 값으로 교체)
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
NODE_PORT=$(kubectl get svc istio-ingressgateway -n istio-ingress -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
echo "접속 URL: http://${NODE_IP}:${NODE_PORT}"
curl -s -o /dev/null -w "%{http_code}" http://${NODE_IP}:${NODE_PORT}/productpage
```

**검증**: curl 결과가 `200` 또는 `404`(Gateway 라우팅 미설정)여야 한다. `000`이 나오면 방화벽 규칙을 확인한다.

GCP 방화벽 규칙 추가가 필요한 경우:

```bash
# GCP CLI로 NodePort 범위 허용 (30000-32767)
gcloud compute firewall-rules create istio-nodeport \
  --allow tcp:30000-32767 \
  --target-tags=<node-tag> \
  --description="Allow Istio NodePort"
```

## 정리 (Cleanup)

```bash
# 애드온 제거
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml

# bookinfo 제거 (필요 시)
kubectl delete namespace bookinfo

# istioctl dashboard 프로세스 종료
pkill -f "istioctl dashboard" || true
```
