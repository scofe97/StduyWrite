# Ch22 - Ambient Mesh 실습
---
> 대응 학습 문서: `learning/ch22-ambient-mesh/LEARN.md`

Ambient 모드는 sidecar 없이 ztunnel(L4)과 Waypoint Proxy(L7)로 메시 기능을 제공한다. 이 실습은 Helm 기반 설치, ztunnel 동작 확인, Waypoint를 통한 L7 정책 적용, sidecar→ambient 마이그레이션 순서로 진행한다.

## 사전 조건

- GCP K8s 클러스터 (기존 sidecar 기반 Istio와 별도 클러스터 권장)
- `istioctl` 1.21+ CLI 설치 완료
- `helm` 3.x 설치 완료
- 기존 `istio/base`, `istiod` Helm 차트 repo 추가 완료

```bash
# Istio Helm repo 추가 (미설치 시)
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
```

## 실습 항목

| # | 항목 | 유형 | 예상 시간 |
|---|------|------|----------|
| 1 | Ambient 모드 설치 (istio-base, istiod, istio-cni, ztunnel) | 설치 | 20분 |
| 2 | `ambient-values.yaml` 분석 | 설정 분석 | 10분 |
| 3 | ztunnel DaemonSet 확인 | 명령어 실행 | 5분 |
| 4 | 네임스페이스에 ambient 레이블 적용 | 리소스 설정 | 10분 |
| 5 | L4 인증 확인 (ztunnel mTLS) | 로그 분석 | 15분 |
| 6 | Waypoint Proxy 배포 | 리소스 배포 | 15분 |
| 7 | L7 정책 적용 (AuthorizationPolicy + waypoint) | 정책 설정 | 20분 |
| 8 | Sidecar → Ambient 마이그레이션 절차 | 절차 실습 | 20분 |
| 9 | Ambient 모드에서 `istioctl proxy-config` 차이 확인 | 명령어 실행 | 10분 |

## 실습 상세

### 1. Ambient 모드 설치

`install/ambient/ambient-values.yaml`의 설정을 사용해 Helm으로 설치한다. 설치 순서가 중요하다 — istio-base → istiod → istio-cni → ztunnel 순서를 지켜야 한다:

```bash
# 1. istio-base 설치 (CRD 포함)
helm install istio-base istio/base \
  -n istio-system \
  --create-namespace \
  --wait

# 2. istiod 설치 (ambient 프로파일 활성화)
helm install istiod istio/istiod \
  -n istio-system \
  --set profile=ambient \
  -f install/ambient/ambient-values.yaml \
  --wait

# 3. istio-cni 설치 (ambient 모드 네트워킹 필수)
helm install istio-cni istio/cni \
  -n istio-system \
  --set profile=ambient \
  --wait

# 4. ztunnel 설치 (노드별 L4 프록시)
helm install ztunnel istio/ztunnel \
  -n istio-system \
  --wait
```

설치 결과를 확인한다:

```bash
kubectl get pods -n istio-system
# 예상 출력:
# istio-cni-node-xxxxx   DaemonSet
# istiod-xxxxx           Deployment
# ztunnel-xxxxx          DaemonSet (노드당 1개)
```

### 2. `ambient-values.yaml` 분석

`install/ambient/ambient-values.yaml` 파일의 각 설정이 무엇을 제어하는지 확인한다:

```bash
cat install/ambient/ambient-values.yaml
```

파일 내용 분석:

```yaml
meshConfig:
  accessLogFile: /dev/stdout    # 모든 접근 로그를 stdout으로 출력 → kubectl logs로 확인 가능
  enableAutoMtls: true          # Pod 간 mTLS를 자동 활성화

ztunnel:
  resources:
    requests:
      cpu: 10m       # 노드당 최소 CPU (DaemonSet이므로 노드 수만큼 곱해서 계산)
      memory: 40Mi   # 노드당 최소 메모리
    limits:
      cpu: 100m
      memory: 128Mi
```

`enableAutoMtls: true`는 ambient 모드에서 HBONE(HTTP-Based Overlay Network Environment) 터널을 통해 자동으로 mTLS를 적용한다는 의미다. sidecar 모드의 PeerAuthentication과 달리 별도 정책 없이도 L4 암호화가 기본 활성화된다.

### 3. ztunnel DaemonSet 확인

ztunnel은 모든 노드에 DaemonSet으로 배포된다. 각 노드의 L4 트래픽을 처리하는 터널 프록시 역할을 한다:

```bash
# DaemonSet 확인
kubectl get ds -n istio-system

# ztunnel Pod가 모든 노드에 하나씩 있는지 확인
kubectl get pods -n istio-system -l app=ztunnel -o wide

# 특정 ztunnel Pod의 로그 확인 (HBONE 연결 수립 메시지 포함)
ZTUNNEL_POD=$(kubectl get pod -n istio-system -l app=ztunnel -o name | head -1)
kubectl logs $ZTUNNEL_POD -n istio-system --tail=20
```

ztunnel은 sidecar와 달리 개별 Pod 옆에 붙지 않고 노드 수준에서 동작한다. 노드에 들어오고 나가는 모든 메시 트래픽이 ztunnel을 통과한다.

### 4. 네임스페이스에 ambient 레이블 적용

네임스페이스에 `istio.io/dataplane-mode=ambient` 레이블을 붙이면 해당 네임스페이스의 모든 Pod가 자동으로 ambient 메시에 참여한다. sidecar 모드처럼 Pod 재시작이 필요 없다:

```bash
# 테스트 네임스페이스 생성
kubectl create namespace ambient-demo

# ambient 레이블 적용 (Pod 재시작 불필요)
kubectl label namespace ambient-demo istio.io/dataplane-mode=ambient

# 레이블 확인
kubectl get namespace ambient-demo --show-labels

# 테스트 앱 배포 (sidecar 없음)
kubectl apply -n ambient-demo -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sleep
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sleep
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
      - name: sleep
        image: curlimages/curl
        command: ["/bin/sh", "-c", "sleep 3600"]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpbin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: httpbin
  template:
    metadata:
      labels:
        app: httpbin
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
  name: httpbin
spec:
  selector:
    app: httpbin
  ports:
  - port: 80
    targetPort: 80
EOF

kubectl wait --for=condition=Ready pod -l app=sleep -n ambient-demo --timeout=60s
kubectl wait --for=condition=Ready pod -l app=httpbin -n ambient-demo --timeout=60s
```

배포된 Pod에 sidecar가 없음을 확인한다:

```bash
# READY 컬럼이 1/1이면 sidecar 없는 상태 (sidecar 모드는 2/2)
kubectl get pods -n ambient-demo
```

### 5. L4 인증 확인 (ztunnel mTLS)

ztunnel 로그에서 HBONE 터널을 통한 mTLS 연결이 수립되는지 확인한다:

```bash
# sleep → httpbin 트래픽 발생
SLEEP_POD=$(kubectl get pod -n ambient-demo -l app=sleep -o name | head -1)
kubectl exec $SLEEP_POD -n ambient-demo -- curl -s http://httpbin.ambient-demo/get

# 트래픽이 통과하는 ztunnel 노드 확인 (httpbin Pod가 있는 노드의 ztunnel)
HTTPBIN_NODE=$(kubectl get pod -n ambient-demo -l app=httpbin -o jsonpath='{.items[0].spec.nodeName}')
echo "httpbin node: $HTTPBIN_NODE"

ZTUNNEL_ON_NODE=$(kubectl get pod -n istio-system -l app=ztunnel \
  --field-selector spec.nodeName=$HTTPBIN_NODE -o name)
kubectl logs $ZTUNNEL_ON_NODE -n istio-system --tail=30 | grep -E "inbound|mTLS|HBONE"
```

로그에서 다음 패턴을 확인한다:

```
# mTLS 수립 성공 시
inbound connection from ... using mTLS
HBONE CONNECT ... accepted
```

### 6. Waypoint Proxy 배포

Waypoint Proxy는 L7 정책(HTTP 헤더 기반 라우팅, JWT 인증 등)을 처리한다. 네임스페이스 단위 또는 서비스 어카운트 단위로 배포한다:

```bash
# 네임스페이스 단위 Waypoint 배포
istioctl waypoint apply -n ambient-demo --enroll-namespace --wait

# Waypoint가 생성되었는지 확인
kubectl get gateway -n ambient-demo
kubectl get pods -n ambient-demo | grep waypoint

# Waypoint가 처리하는 트래픽 범위 확인
istioctl waypoint status -n ambient-demo
```

특정 서비스 어카운트에만 Waypoint를 적용하려면 `--for serviceaccount`를 사용한다:

```bash
# httpbin 전용 서비스 어카운트 생성
kubectl create serviceaccount httpbin-sa -n ambient-demo

# httpbin 서비스 어카운트에만 Waypoint 적용
istioctl waypoint apply -n ambient-demo \
  --for serviceaccount \
  --name httpbin-waypoint \
  --wait
```

### 7. L7 정책 적용 (AuthorizationPolicy + waypoint)

Waypoint가 배포된 후에야 L7 기반 AuthorizationPolicy가 동작한다. Waypoint 없이는 ztunnel이 L4 수준에서만 정책을 처리한다:

```bash
# httpbin의 GET 메서드만 허용하는 AuthorizationPolicy
cat <<EOF | kubectl apply -f -
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: httpbin-get-only
  namespace: ambient-demo
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: httpbin
  action: ALLOW
  rules:
  - to:
    - operation:
        methods: ["GET"]
EOF

# GET 요청 → 허용
kubectl exec $SLEEP_POD -n ambient-demo -- \
  curl -s -o /dev/null -w "%{http_code}" http://httpbin.ambient-demo/get
# 예상: 200

# POST 요청 → 차단
kubectl exec $SLEEP_POD -n ambient-demo -- \
  curl -s -o /dev/null -w "%{http_code}" -X POST http://httpbin.ambient-demo/post
# 예상: 403
```

Waypoint 로그에서 L7 정책이 적용되는 것을 확인한다:

```bash
WAYPOINT_POD=$(kubectl get pod -n ambient-demo -l gateway.istio.io/managed=istio.io-mesh-controller -o name | head -1)
kubectl logs $WAYPOINT_POD -n ambient-demo --tail=20
```

### 8. Sidecar → Ambient 마이그레이션 절차

기존 sidecar 기반 네임스페이스를 ambient로 전환하는 절차다. 트래픽 중단 없이 점진적으로 진행할 수 있다:

```bash
# 1. sidecar 기반 네임스페이스 생성 (마이그레이션 출발점 시뮬레이션)
kubectl create namespace sidecar-ns
kubectl label namespace sidecar-ns istio-injection=enabled

# 2. 테스트 앱 배포 (sidecar 자동 주입됨)
kubectl run httpbin-sidecar --image=kennethreitz/httpbin \
  --port=80 -n sidecar-ns
kubectl wait --for=condition=Ready pod/httpbin-sidecar -n sidecar-ns --timeout=60s

# sidecar가 주입되었는지 확인 (READY: 2/2)
kubectl get pod httpbin-sidecar -n sidecar-ns

# 3. ambient 레이블 추가 (sidecar 레이블은 유지)
kubectl label namespace sidecar-ns istio.io/dataplane-mode=ambient

# 4. 기존 Pod 재시작 → sidecar 제거 + ambient 편입
kubectl rollout restart deployment -n sidecar-ns 2>/dev/null || \
  kubectl delete pod httpbin-sidecar -n sidecar-ns

kubectl wait --for=condition=Ready pod -l run=httpbin-sidecar -n sidecar-ns --timeout=60s

# 5. sidecar가 제거되었는지 확인 (READY: 1/1로 변경)
kubectl get pod -n sidecar-ns

# 6. sidecar 주입 레이블 제거 (정리)
kubectl label namespace sidecar-ns istio-injection-
```

마이그레이션 시 주의할 점:

- DestinationRule의 `trafficPolicy.tls.mode: ISTIO_MUTUAL`은 ambient에서 불필요하다. ztunnel이 자동으로 mTLS를 처리한다.
- PeerAuthentication의 `mtls.mode: STRICT`는 ambient에서 무시된다. ztunnel 레벨에서 이미 강제된다.
- VirtualService와 AuthorizationPolicy는 Waypoint 배포 후 동일하게 동작한다.

### 9. Ambient 모드에서 `istioctl proxy-config` 차이 확인

sidecar 모드에서는 각 Pod의 Envoy를 직접 조회했지만, ambient 모드에서는 ztunnel과 Waypoint를 별도로 조회한다:

```bash
# sidecar 모드: Pod의 Envoy 직접 조회
# istioctl proxy-config endpoints <pod>.<namespace>

# ambient 모드: ztunnel 조회
ZTUNNEL_POD=$(kubectl get pod -n istio-system -l app=ztunnel -o name | head -1)
istioctl proxy-config all $ZTUNNEL_POD -n istio-system | head -30

# ambient 모드: Waypoint 조회
WAYPOINT_POD=$(kubectl get pod -n ambient-demo -l gateway.istio.io/managed=istio.io-mesh-controller -o name | head -1)
istioctl proxy-config endpoints $WAYPOINT_POD -n ambient-demo

# proxy-status 비교 (sidecar Pod는 표시, ambient Pod는 표시 안 됨)
istioctl proxy-status

# ambient 전용: ztunnel workload 목록 확인
istioctl ztunnel-config workload -n ambient-demo
```

sidecar 모드와의 핵심 차이:

- `proxy-status`에 ambient Pod가 나타나지 않는다. ztunnel이 Pod 대신 노드 단위로 등록된다.
- `proxy-config` 대상이 Pod가 아닌 ztunnel DaemonSet Pod 또는 Waypoint Pod다.
- L7 설정(라우팅, 필터)은 Waypoint에서만 확인할 수 있다.

## 정리 (Cleanup)

```bash
# L7 정책 삭제
kubectl delete authorizationpolicy httpbin-get-only -n ambient-demo

# Waypoint 삭제
istioctl waypoint delete -n ambient-demo --all

# 테스트 리소스 삭제
kubectl delete namespace ambient-demo sidecar-ns

# Istio 컴포넌트 전체 삭제 (필요 시)
helm uninstall ztunnel -n istio-system
helm uninstall istio-cni -n istio-system
helm uninstall istiod -n istio-system
helm uninstall istio-base -n istio-system
kubectl delete namespace istio-system
