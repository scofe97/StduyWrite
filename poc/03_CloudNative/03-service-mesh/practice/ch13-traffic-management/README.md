# Ch13 - 트래픽 관리 실습
---
> 대응 학습 문서: `learning/ch13-traffic-management/LEARN.md`

DestinationRule의 subset으로 버전을 분리하고, VirtualService로 헤더/가중치 기반 라우팅을 구성한다. Traffic Mirroring으로 프로덕션 트래픽을 복사하여 신규 버전을 검증하고, ServiceEntry로 클러스터 외부 서비스 접근을 제어한다.

참조 파일: `../traffic/virtual-service-canary.yaml`

## 사전 조건

bookinfo 앱이 `bookinfo` 네임스페이스에 배포되어 있고, sidecar injection이 활성화되어 있어야 한다. reviews 서비스의 v1/v2/v3 버전이 모두 실행 중이어야 한다.

```bash
kubectl get pods -n bookinfo -l app=reviews
# v1, v2, v3 각 1개씩 Running 상태 확인
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | DestinationRule subset | v1/v2/v3 버전 레이블로 subset 정의 | proxy-config cluster에서 subset 확인 |
| 2 | 헤더 기반 라우팅 | x-istio-cohort: internal → v2로 라우팅 | 헤더 포함/미포함 요청 결과 비교 |
| 3 | 가중치 카나리 | 90/10 → 50/50 단계적 전환 | 요청 분포 비율 통계 확인 |
| 4 | Traffic Mirroring | v1으로 가면서 v2에 shadow 복사 | v2 로그에서 -shadow 요청 확인 |
| 5 | Mesh Gateway | 내부 서비스 간 VirtualService 적용 | 내부 요청도 라우팅 규칙 적용 확인 |
| 6 | REGISTRY_ONLY | 등록되지 않은 외부 접속 차단 | curl example.com 차단 확인 |
| 7 | ServiceEntry | 외부 서비스 명시적 허용 | httpbin.org 접속 허용 확인 |

## 실습 상세

### 1. DestinationRule subset 정의

**목표**: reviews 서비스의 v1/v2/v3 버전을 subset으로 분리하여 각 버전에 독립적으로 트래픽을 라우팅할 수 있는 기반을 만든다. 이 파일은 `../traffic/virtual-service-canary.yaml`에서 이미 정의된 패턴을 따른다.

**단계**:

```bash
# DestinationRule 적용 (virtual-service-canary.yaml과 동일한 패턴)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews
  namespace: bookinfo
spec:
  host: reviews
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
    - name: v3
      labels:
        version: v3
EOF

# subset이 Envoy cluster에 반영되었는지 확인
PRODUCTPAGE=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

istioctl proxy-config cluster $PRODUCTPAGE -n bookinfo | grep reviews
# 예상: reviews|9080|v1|bookinfo, reviews|9080|v2|bookinfo, reviews|9080|v3|bookinfo
```

**검증**: `istioctl proxy-config cluster` 결과에 `v1`, `v2`, `v3` subset이 각각 별도 cluster로 등록되어야 한다.

### 2. 헤더 기반 라우팅

**목표**: `x-istio-cohort: internal` 헤더가 있는 요청만 v2(별점 흑백)로 보내고, 나머지는 모두 v1(별점 없음)으로 라우팅한다. 내부 테스터만 신기능을 볼 수 있게 하는 패턴이다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            x-istio-cohort:
              exact: internal
      route:
        - destination:
            host: reviews
            subset: v2
    - route:
        - destination:
            host: reviews
            subset: v1
EOF

# 헤더 없이 요청 (v1으로 가야 함 - 별점 없음)
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s http://reviews:9080/reviews/1 | python3 -m json.tool

# 헤더 포함 요청 (v2로 가야 함 - 흑백 별점)
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s -H "x-istio-cohort: internal" http://reviews:9080/reviews/1 | python3 -m json.tool
```

**검증**: 헤더 없는 요청의 응답에는 `color` 필드가 없어야 하고, 헤더 포함 요청의 응답에는 `color: black`이 포함되어야 한다.

### 3. 가중치 카나리 배포

**목표**: v1에서 v2로 점진적으로 트래픽을 전환한다. `../traffic/virtual-service-canary.yaml`에서 이미 90/10 예시를 제공하며, 여기서는 50/50까지 전환 과정을 실습한다.

**단계**:

```bash
# Step 1: 90/10 배포 (canary 시작)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 90
        - destination:
            host: reviews
            subset: v2
          weight: 10
EOF

# 10회 요청하여 분포 확인
for i in $(seq 1 10); do
  kubectl exec -n bookinfo deploy/productpage -c productpage -- \
    curl -s http://reviews:9080/reviews/1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
ratings = data.get('ratings', {})
print('v2' if ratings else 'v1')
"
done

# Step 2: 50/50으로 가중치 조정
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 50
        - destination:
            host: reviews
            subset: v2
          weight: 50
EOF

# 분포 재확인
for i in $(seq 1 20); do
  kubectl exec -n bookinfo deploy/productpage -c productpage -- \
    curl -s http://reviews:9080/reviews/1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
ratings = data.get('ratings', {})
print('v2' if ratings else 'v1')
" 2>/dev/null
done | sort | uniq -c
```

**검증**: 20회 요청 중 v1과 v2가 대략 10:10으로 분포되어야 한다. 정확히 50:50은 아닐 수 있으나 큰 편차가 없어야 한다.

### 4. Traffic Mirroring

**목표**: v1으로 가는 모든 요청을 v2에도 동시에 복사(shadow)한다. v2의 처리 결과는 클라이언트에게 전달되지 않으므로, 프로덕션 트래픽으로 신규 버전을 안전하게 검증할 수 있다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 100
      mirror:
        host: reviews
        subset: v2
      mirrorPercentage:
        value: 100.0
EOF

# v2 Pod 로그 실시간 확인
V2_POD=$(kubectl get pod -n bookinfo -l app=reviews,version=v2 -o jsonpath='{.items[0].metadata.name}')
kubectl logs -f $V2_POD -n bookinfo -c reviews &
LOG_PID=$!

# 요청 전송 (v1에 가면서 v2에도 미러링)
for i in $(seq 1 5); do
  kubectl exec -n bookinfo deploy/productpage -c productpage -- \
    curl -s http://reviews:9080/reviews/1 > /dev/null
  sleep 1
done

kill $LOG_PID 2>/dev/null
```

**검증**: v2 Pod 로그에서 요청 헤더에 `x-forwarded-host: reviews-shadow`가 포함된 요청이 확인되어야 한다. 클라이언트에는 v1 응답만 반환된다.

### 5. Mesh Gateway (내부 서비스 간 VirtualService)

**목표**: 외부 Gateway가 아닌 mesh 내부 서비스 간 통신에도 VirtualService 라우팅 규칙을 적용한다. `gateways: [mesh]`를 명시하면 내부 요청에도 규칙이 적용된다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
  namespace: bookinfo
spec:
  hosts:
    - reviews
  gateways:
    - mesh
  http:
    - route:
        - destination:
            host: reviews
            subset: v3
          weight: 100
EOF

# 내부에서 reviews 호출 (v3 - 컬러 별점으로 응답해야 함)
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s http://reviews:9080/reviews/1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('color:', data.get('ratings', {}).get('Reviewer1', 'none'))
"
# 예상: color: red (v3은 red star)
```

**검증**: `gateways: [mesh]`로 설정한 VirtualService가 내부 서비스 호출에도 적용되어 v3로만 트래픽이 가야 한다.

### 6. outboundTrafficPolicy: REGISTRY_ONLY 설정

**목표**: 서비스 레지스트리에 등록되지 않은 외부 서비스 접속을 차단한다. 이 설정을 활성화하면 ServiceEntry 없이는 클러스터 외부로 나갈 수 없다.

**단계**:

```bash
# 현재 외부 접속 가능 확인
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://httpbin.org/get
# 예상: 200 (현재 허용 상태)

# outboundTrafficPolicy를 REGISTRY_ONLY로 변경
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: bookinfo
spec:
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
EOF

# 외부 접속 차단 확인
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://httpbin.org/get
# 예상: 502 또는 연결 실패
```

**검증**: `REGISTRY_ONLY` 설정 후 외부 요청이 502 또는 타임아웃으로 실패해야 한다.

### 7. ServiceEntry로 외부 서비스 허용

**목표**: REGISTRY_ONLY 환경에서 특정 외부 서비스만 명시적으로 허용한다. ServiceEntry는 외부 서비스를 Istio 서비스 레지스트리에 등록하는 방법이다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: httpbin-external
  namespace: bookinfo
spec:
  hosts:
    - httpbin.org
  ports:
    - number: 80
      name: http
      protocol: HTTP
    - number: 443
      name: https
      protocol: HTTPS
  resolution: DNS
  location: MESH_EXTERNAL
EOF

# httpbin.org 접속 허용 확인
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s -o /dev/null -w "%{http_code}" --max-time 10 http://httpbin.org/get
# 예상: 200

# 다른 외부 사이트는 여전히 차단 확인
kubectl exec -n bookinfo deploy/productpage -c productpage -- \
  curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://google.com
# 예상: 502 또는 연결 실패

# ServiceEntry 목록 확인
kubectl get serviceentry -n bookinfo
```

**검증**: httpbin.org는 200이고 등록하지 않은 도메인은 실패해야 한다. 이것이 Zero Trust 네트워크 정책의 기본 원리다.

## 정리 (Cleanup)

```bash
# VirtualService 제거
kubectl delete virtualservice reviews -n bookinfo --ignore-not-found=true

# DestinationRule 제거
kubectl delete destinationrule reviews -n bookinfo --ignore-not-found=true

# Sidecar 리소스 제거 (outboundTrafficPolicy 초기화)
kubectl delete sidecar default -n bookinfo --ignore-not-found=true

# ServiceEntry 제거
kubectl delete serviceentry httpbin-external -n bookinfo --ignore-not-found=true
```
