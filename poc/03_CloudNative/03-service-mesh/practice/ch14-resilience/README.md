# Ch14 - 복원력 실습
---
> 대응 학습 문서: `learning/ch14-resilience/LEARN.md`

로드 밸런싱 전략 비교, Timeout/Retry 설정, Circuit Breaker와 Outlier Detection을 단계별로 구성한다. Fortio 부하 도구로 실제 부하를 주면서 설정 효과를 수치로 확인한다.

## 사전 조건

bookinfo 앱이 `bookinfo` 네임스페이스에 배포되어 있어야 한다. ch13 실습에서 생성한 VirtualService, DestinationRule이 있으면 먼저 정리한다.

```bash
kubectl delete virtualservice reviews -n bookinfo --ignore-not-found=true
kubectl delete destinationrule reviews -n bookinfo --ignore-not-found=true
kubectl get pods -n bookinfo
```

Fortio 부하 테스트 도구를 배포한다:

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/httpbin.yaml -n bookinfo
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/sample-client/fortio-deploy.yaml -n bookinfo
kubectl rollout status deployment/fortio-deploy -n bookinfo
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | LB 전략 | RR → Random → LEAST_CONN 변경 | 요청 분산 패턴 비교 |
| 2 | Fortio 기준 부하 | 2 connections, 2 qps, 30s | 기준 성공률 측정 |
| 3 | Timeout | 0.5s timeout 설정 후 지연 서비스에 요청 | 0.5s 초과 시 504 확인 |
| 4 | Retry | 3회 재시도, 5xx에서만 재시도 | 간헐적 5xx 시 최종 성공 확인 |
| 5 | EnvoyFilter retry | retriable_status_codes 408 추가 | 408도 재시도 대상 확인 |
| 6 | Circuit Breaker | maxConnections: 1 설정 후 Fortio 부하 | overflow 오류(503) 발생 확인 |
| 7 | Outlier Detection | consecutive5xxErrors: 1로 즉시 격리 | 불량 Pod 격리 후 정상 트래픽 확인 |
| 8 | CB + 재시도 조합 | Circuit Breaker + Retry 동시 적용 | 빠른 복구 확인 |

## 실습 상세

### 1. DestinationRule LB 전략 변경

**목표**: Istio의 기본 LB 전략(Round Robin)과 다른 전략들의 차이를 직접 비교한다. LEAST_CONN은 연결이 적은 Pod에 우선 분산하므로 처리 시간이 다른 서비스에 효과적이다.

**단계**:

```bash
# 기본: Round Robin (명시 없으면 기본값)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews
  namespace: bookinfo
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
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

# 요청 10회, Pod별 수신 횟수 확인
for i in $(seq 1 10); do
  kubectl exec -n bookinfo deploy/productpage -c productpage -- \
    curl -s http://reviews:9080/reviews/1 > /dev/null
done
kubectl logs -n bookinfo -l app=reviews,version=v1 --tail=5 | grep -c "GET /reviews"

# LEAST_CONN으로 변경
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews
  namespace: bookinfo
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
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

# LB 설정이 Envoy에 반영되었는지 확인
PRODUCTPAGE=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')
istioctl proxy-config cluster $PRODUCTPAGE -n bookinfo | grep reviews
```

**검증**: `istioctl proxy-config cluster` 결과에서 reviews cluster의 `lb_policy`가 `LEAST_REQUEST`로 표시되어야 한다.

### 2. Fortio 기준 부하 테스트

**목표**: Circuit Breaker 설정 전 기준 성공률을 측정한다. 이 수치와 이후 설정 적용 후 수치를 비교하면 효과를 정량적으로 확인할 수 있다.

**단계**:

```bash
FORTIO=$(kubectl get pod -n bookinfo -l app=fortio -o jsonpath='{.items[0].metadata.name}')

# 기준 부하 측정 (2 connections, 2 qps, 30초)
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  fortio load \
  -c 2 \
  -qps 2 \
  -t 30s \
  -loglevel Warning \
  http://httpbin:8000/get

# 결과 요약만 출력
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  fortio load \
  -c 2 \
  -qps 2 \
  -t 30s \
  -loglevel Warning \
  -json /tmp/baseline.json \
  http://httpbin:8000/get > /dev/null 2>&1

kubectl exec -n bookinfo $FORTIO -c fortio -- \
  cat /tmp/baseline.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('총 요청:', data['DurationHistogram']['Count'])
print('성공률:', (1 - data.get('ErrorPercent', 0)/100) * 100, '%')
"
```

**검증**: Circuit Breaker 설정 전 기준 성공률이 100%에 가까워야 한다. 이 값을 기억해둔다.

### 3. VirtualService timeout 설정

**목표**: 응답이 느린 서비스에 대한 타임아웃을 설정한다. 0.5초 초과 시 Gateway가 504를 반환하여 클라이언트가 무한 대기하는 상황을 방지한다.

**단계**:

```bash
# httpbin의 /delay/1 엔드포인트는 1초 후 응답 (타임아웃 테스트에 사용)
# timeout 없이 요청 (1초 이상 걸림)
time kubectl exec -n bookinfo $FORTIO -c fortio -- \
  curl -s http://httpbin:8000/delay/1 -o /dev/null

# 0.5초 timeout 설정
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: bookinfo
spec:
  hosts:
    - httpbin
  http:
    - timeout: 0.5s
      route:
        - destination:
            host: httpbin
            port:
              number: 8000
EOF

# timeout 적용 후 동일 요청 (504가 반환되어야 함)
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  curl -s -o /dev/null -w "%{http_code}" http://httpbin:8000/delay/1
# 예상: 504

# 0.3초 요청은 성공해야 함
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  curl -s -o /dev/null -w "%{http_code}" http://httpbin:8000/delay/0
# 예상: 200
```

**검증**: `/delay/1` 요청은 504, `/delay/0` 요청은 200이어야 한다.

### 4. VirtualService retry 설정

**목표**: 5xx 오류 발생 시 자동으로 재시도하여 간헐적 장애를 투명하게 처리한다. 재시도 횟수와 재시도 조건(retryOn)을 함께 설정한다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: bookinfo
spec:
  hosts:
    - httpbin
  http:
    - retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,reset,connect-failure,retriable-4xx
      route:
        - destination:
            host: httpbin
            port:
              number: 8000
EOF

# httpbin /status/500 엔드포인트로 5xx 재시도 테스트
# 재시도 횟수는 Envoy 통계로 확인
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  curl -s -o /dev/null -w "%{http_code}" http://httpbin:8000/status/500
# 예상: 500 (3회 재시도 후 최종 실패)

# Envoy 통계에서 재시도 횟수 확인
PRODUCTPAGE=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n bookinfo $PRODUCTPAGE -c istio-proxy -- \
  pilot-agent request GET stats | grep "upstream_rq_retry" | grep httpbin
```

**검증**: Envoy 통계의 `upstream_rq_retry` 카운터가 증가해야 한다. 클라이언트는 1번 요청했지만 Envoy가 3번 재시도한 것을 확인한다.

### 5. EnvoyFilter로 retriable_status_codes 추가

**목표**: VirtualService의 `retryOn`에 없는 HTTP 상태 코드(408 Request Timeout)를 재시도 대상에 추가한다. EnvoyFilter는 Istio CRD로 처리할 수 없는 고급 Envoy 설정을 직접 적용할 때 사용한다.

**단계**:

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: httpbin-retry-408
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: productpage
  configPatches:
    - applyTo: HTTP_ROUTE
      match:
        context: SIDECAR_OUTBOUND
        routeConfiguration:
          vhost:
            name: "httpbin.bookinfo.svc.cluster.local:8000"
      patch:
        operation: MERGE
        value:
          route:
            retry_policy:
              retriable_status_codes:
                - 408
EOF

# 408 응답 재시도 확인
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  curl -s -o /dev/null -w "%{http_code}" http://httpbin:8000/status/408

# EnvoyFilter가 적용된 라우트 설정 확인
istioctl proxy-config route $PRODUCTPAGE -n bookinfo -o json | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for route in data:
    name = route.get('name', '')
    if 'httpbin' in name:
        vhosts = route.get('virtualHosts', [])
        for vh in vhosts:
            for r in vh.get('routes', []):
                retry = r.get('route', {}).get('retryPolicy', {})
                if retry:
                    print('retry policy:', json.dumps(retry, indent=2))
"
```

**검증**: `istioctl proxy-config route` 출력에서 `retriable_status_codes`에 `408`이 포함되어야 한다.

### 6. Circuit Breaker (connectionPool)

**목표**: 동시 연결 수를 1로 제한하여 과부하 시 빠른 실패(fast fail)를 유도한다. 무한정 요청을 쌓는 대신 503을 즉시 반환하여 upstream 서비스를 보호한다.

**단계**:

```bash
# Circuit Breaker 설정 (maxConnections: 1, pendingRequests: 1)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: httpbin
  namespace: bookinfo
spec:
  host: httpbin
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1
      http:
        http1MaxPendingRequests: 1
        maxRequestsPerConnection: 1
EOF

# CB 설정 전 기준 성공률 (1 connection, 1 qps)
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  fortio load -c 1 -qps 1 -t 10s -loglevel Warning \
  http://httpbin:8000/get

# CB 동작 확인 (2 connections로 초과 부하)
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  fortio load -c 2 -qps 10 -t 20s -loglevel Warning \
  http://httpbin:8000/get
# 예상: 일부 요청이 503 (overflow)으로 실패

# Envoy 통계에서 overflow 횟수 확인
kubectl exec -n bookinfo $FORTIO -c istio-proxy -- \
  pilot-agent request GET stats | grep "upstream_cx_overflow\|pending_overflow"
```

**검증**: 부하 테스트 결과에서 `503` 응답이 포함되어야 한다. Envoy 통계의 `overflow` 카운터가 0보다 커야 한다.

### 7. Outlier Detection (불량 Pod 격리)

**목표**: 연속으로 오류를 반환하는 Pod를 자동으로 로드 밸런싱에서 제외한다. 1번만 5xx 오류를 내도 5초 동안 격리하는 엄격한 설정을 실습한다.

**단계**:

```bash
# Outlier Detection 설정
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews
  namespace: bookinfo
spec:
  host: reviews
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 1
      interval: 10s
      baseEjectionTime: 5s
      maxEjectionPercent: 100
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

# v2 Pod에 오류를 강제로 주입 (fault injection으로 시뮬레이션)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-fault
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - match:
        - sourceLabels:
            app: productpage
      fault:
        abort:
          percentage:
            value: 50
          httpStatus: 500
      route:
        - destination:
            host: reviews
EOF

# 요청 10회 전송 (일부 500)
for i in $(seq 1 10); do
  kubectl exec -n bookinfo deploy/productpage -c productpage -- \
    curl -s -o /dev/null -w "%{http_code}\n" http://reviews:9080/reviews/1
done

# Outlier Detection 통계 확인
kubectl exec -n bookinfo $PRODUCTPAGE -c istio-proxy -- \
  pilot-agent request GET stats | grep "outlier_detection"
```

**검증**: Envoy 통계에서 `ejections_active` 카운터가 증가해야 한다. 격리된 Pod으로는 요청이 가지 않는다.

### 8. Circuit Breaker + Retry 조합

**목표**: CB(빠른 실패)와 Retry(투명한 재시도)를 조합하면 일시적 장애를 자동으로 흡수할 수 있다. CB가 503을 반환하면 Retry가 다른 Pod으로 재시도한다.

**단계**:

```bash
# DestinationRule: connectionPool(CB) + outlierDetection(격리)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: httpbin
  namespace: bookinfo
spec:
  host: httpbin
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 5
      http:
        http1MaxPendingRequests: 5
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
EOF

# VirtualService: Retry (CB 503에서도 재시도)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: bookinfo
spec:
  hosts:
    - httpbin
  http:
    - retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,reset,connect-failure,retriable-4xx,gateway-error
      route:
        - destination:
            host: httpbin
            port:
              number: 8000
EOF

# 조합 효과 테스트 (적절한 동시성으로 부하)
kubectl exec -n bookinfo $FORTIO -c fortio -- \
  fortio load \
  -c 4 \
  -qps 5 \
  -t 30s \
  -loglevel Warning \
  http://httpbin:8000/get

# 최종 성공률 출력
echo "=== 결과 요약 ==="
kubectl exec -n bookinfo $FORTIO -c istio-proxy -- \
  pilot-agent request GET stats | grep "upstream_rq_total\|upstream_rq_retry\|upstream_rq_5xx"
```

**검증**: 기준 부하 테스트(실습 2)와 비교하여 성공률이 유사하게 유지되면서, `upstream_rq_retry` 카운터가 증가하면 Retry가 동작한 것이다. CB 없이 동일한 부하를 주면 타임아웃이 급증한다.

## 정리 (Cleanup)

```bash
# DestinationRule 제거
kubectl delete destinationrule httpbin reviews -n bookinfo --ignore-not-found=true

# VirtualService 제거
kubectl delete virtualservice httpbin reviews-fault -n bookinfo --ignore-not-found=true

# EnvoyFilter 제거
kubectl delete envoyfilter httpbin-retry-408 -n bookinfo --ignore-not-found=true

# Fortio 및 httpbin 제거 (선택)
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/httpbin.yaml -n bookinfo --ignore-not-found=true
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/sample-client/fortio-deploy.yaml -n bookinfo --ignore-not-found=true
```
