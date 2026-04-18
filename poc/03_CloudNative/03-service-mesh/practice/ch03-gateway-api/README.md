# Ch03 - Gateway API 실습
---
> 대응 학습 문서: `learning/03-gateway-api-and-traffic/LEARN.md`

## 사전 조건

- Kind 클러스터 실행 중 (`make cluster-up`)
- Istio 설치 완료 (`istioctl install --set profile=demo -y`)
- kubectl 설치

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | Gateway API CRD | 표준 CRD 설치 | `kubectl get crd | grep gateway` |
| 2 | GatewayClass | 컨트롤러 바인딩 확인 | `kubectl get gatewayclass` |
| 3 | Gateway 리소스 | HTTP 포트 80 개방 | `kubectl get gateway` |
| 4 | HTTPRoute 기본 라우팅 | 서비스로 트래픽 전달 | `curl` 응답 확인 |
| 5 | 가중치 기반 분할 | v1 80% / v2 20% 분할 | 100회 요청 후 비율 확인 |
| 6 | Istio Gateway vs K8s Gateway API | 동일 라우팅 두 방식 비교 | 각 방식 apply 후 동작 동일 확인 |

## 실습 상세

### 1. Gateway API CRD 설치

**목표**: Kubernetes 표준 Gateway API CRD를 클러스터에 설치한다. Istio 자체 Gateway CRD와는 별개의 표준 스펙이다.

**단계**:
1. 표준 CRD 설치 (실험적 채널 — HTTPRoute, Gateway 포함)
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.1.0/standard-install.yaml
   ```
2. 설치된 CRD 확인
   ```bash
   kubectl get crd | grep gateway.networking.k8s.io
   ```

**검증**:
```
gatewayclasses.gateway.networking.k8s.io
gateways.gateway.networking.k8s.io
httproutes.gateway.networking.k8s.io
```
3가지 CRD가 표시된다.

### 2. GatewayClass 확인

**목표**: Istio가 자동으로 등록한 GatewayClass를 확인하고 컨트롤러 연결 상태를 파악한다.

**단계**:
1. GatewayClass 조회
   ```bash
   kubectl get gatewayclass
   ```
2. 상세 정보 확인
   ```bash
   kubectl describe gatewayclass istio
   ```

**검증**:
```
NAME    CONTROLLER                    ACCEPTED
istio   istio.io/gateway-controller   True
```
`ACCEPTED=True`이면 Istio가 이 GatewayClass를 처리할 준비가 된 것이다.

### 3. Gateway 리소스 생성

**목표**: HTTP 포트 80을 여는 Gateway를 생성한다. Gateway는 로드밸런서 역할을 하며 실제 라우팅 규칙은 HTTPRoute에서 정의한다.

**단계**:
1. 네임스페이스 생성
   ```bash
   kubectl create namespace gwapi-demo
   ```
2. Gateway 생성
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: gateway.networking.k8s.io/v1
   kind: Gateway
   metadata:
     name: demo-gateway
     namespace: gwapi-demo
   spec:
     gatewayClassName: istio
     listeners:
       - name: http
         port: 80
         protocol: HTTP
         allowedRoutes:
           namespaces:
             from: Same
   EOF
   ```
3. 상태 확인 (LoadBalancer IP 할당에 수십 초 소요)
   ```bash
   kubectl get gateway -n gwapi-demo -w
   ```

**검증**: `PROGRAMMED=True` 상태가 되고 ADDRESS 컬럼에 IP가 할당된다.

### 4. HTTPRoute 기본 라우팅

**목표**: HTTPRoute로 특정 경로의 요청을 백엔드 서비스로 전달한다.

**단계**:
1. 백엔드 서비스 배포
   ```bash
   kubectl apply -n gwapi-demo -f - <<EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: httpbin-v1
   spec:
     replicas: 1
     selector:
       matchLabels: { app: httpbin, version: v1 }
     template:
       metadata:
         labels: { app: httpbin, version: v1 }
       spec:
         containers:
           - name: httpbin
             image: kennethreitz/httpbin
             ports:
               - containerPort: 80
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: httpbin-v1
   spec:
     selector: { app: httpbin, version: v1 }
     ports:
       - port: 80
   EOF
   ```
2. HTTPRoute 생성
   ```bash
   kubectl apply -n gwapi-demo -f - <<EOF
   apiVersion: gateway.networking.k8s.io/v1
   kind: HTTPRoute
   metadata:
     name: httpbin-route
   spec:
     parentRefs:
       - name: demo-gateway
     rules:
       - matches:
           - path: { type: PathPrefix, value: /get }
         backendRefs:
           - name: httpbin-v1
             port: 80
   EOF
   ```
3. Gateway IP 확인 후 요청
   ```bash
   GW_IP=$(kubectl get gateway demo-gateway -n gwapi-demo \
     -o jsonpath='{.status.addresses[0].value}')
   curl http://${GW_IP}/get
   ```

**검증**: httpbin의 `/get` JSON 응답이 반환된다.

### 5. 가중치 기반 트래픽 분할

**목표**: v1과 v2 서비스에 각각 80%, 20% 비율로 트래픽을 분배한다.

**단계**:
1. v2 서비스 배포
   ```bash
   kubectl apply -n gwapi-demo -f - <<EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: httpbin-v2
   spec:
     replicas: 1
     selector:
       matchLabels: { app: httpbin, version: v2 }
     template:
       metadata:
         labels: { app: httpbin, version: v2 }
       spec:
         containers:
           - name: httpbin
             image: kennethreitz/httpbin
             ports:
               - containerPort: 80
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: httpbin-v2
   spec:
     selector: { app: httpbin, version: v2 }
     ports:
       - port: 80
   EOF
   ```
2. HTTPRoute에 가중치 추가
   ```bash
   kubectl apply -n gwapi-demo -f - <<EOF
   apiVersion: gateway.networking.k8s.io/v1
   kind: HTTPRoute
   metadata:
     name: httpbin-route
   spec:
     parentRefs:
       - name: demo-gateway
     rules:
       - matches:
           - path: { type: PathPrefix, value: /get }
         backendRefs:
           - name: httpbin-v1
             port: 80
             weight: 80
           - name: httpbin-v2
             port: 80
             weight: 20
   EOF
   ```
3. 100회 요청으로 분배 비율 확인
   ```bash
   for i in $(seq 1 100); do
     curl -s http://${GW_IP}/get | grep -o '"version": "[^"]*"' 2>/dev/null || \
     curl -s http://${GW_IP}/get > /dev/null && echo "ok"
   done | sort | uniq -c
   ```

**검증**: v1이 약 80회, v2가 약 20회 응답한다 (±5% 오차 정상).

### 6. Istio Gateway vs Kubernetes Gateway API 비교

**목표**: 같은 라우팅을 Istio 전용 CRD(`Gateway` + `VirtualService`)와 표준 K8s Gateway API(`Gateway` + `HTTPRoute`) 두 방식으로 작성해 차이를 체감한다.

**단계**:
1. Istio 전용 방식 (참고용, 현재 gwapi-demo와 별개 네임스페이스)
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: networking.istio.io/v1beta1
   kind: Gateway
   metadata:
     name: istio-gw
     namespace: istio-system
   spec:
     selector:
       istio: ingressgateway
     servers:
       - port: { number: 80, name: http, protocol: HTTP }
         hosts: ["*"]
   ---
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: httpbin-vs
     namespace: gwapi-demo
   spec:
     hosts: ["*"]
     gateways: ["istio-system/istio-gw"]
     http:
       - match: [{ uri: { prefix: "/get" } }]
         route:
           - destination:
               host: httpbin-v1
               port: { number: 80 }
             weight: 80
           - destination:
               host: httpbin-v2
               port: { number: 80 }
             weight: 20
   EOF
   ```
2. 두 방식의 주요 차이 비교
   ```bash
   # K8s Gateway API 방식 리소스 확인
   kubectl get gateway,httproute -n gwapi-demo

   # Istio 전용 방식 리소스 확인
   kubectl get gateway,virtualservice -n istio-system
   kubectl get virtualservice -n gwapi-demo
   ```

**검증**: 아래 차이를 직접 확인한다.

| 항목 | Istio 전용 | K8s Gateway API |
|------|-----------|----------------|
| 리소스 | Gateway + VirtualService | Gateway + HTTPRoute |
| 이식성 | Istio 전용 | 표준 (벤더 중립) |
| 네임스페이스 | Gateway는 istio-system | Gateway는 앱 네임스페이스 가능 |
| 안정성 | GA | v1.0 GA (standard 채널) |

## 정리 (Cleanup)

```bash
kubectl delete namespace gwapi-demo
kubectl delete gateway istio-gw -n istio-system 2>/dev/null || true
kubectl delete virtualservice httpbin-vs -n gwapi-demo 2>/dev/null || true
```
