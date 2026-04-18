# Ch16 - 가관측성 (Observability) 실습

---

> 대응 학습 문서: `learning/ch16-observability/LEARN.md`

## 사전 조건

- bookinfo 앱 정상 기동 (`kubectl get pods -n bookinfo`)
- Prometheus, Grafana, Jaeger, Kiali 설치 완료 (istio addons)
- 각 대시보드 포트포워딩 또는 LoadBalancer 접근 가능

```bash
# addons 설치 확인
kubectl get pods -n istio-system | grep -E "prometheus|grafana|jaeger|kiali"

# 트래픽 생성용 루프 (다른 터미널에서 실행)
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while true; do curl -s "http://$INGRESS_IP/productpage" -o /dev/null; sleep 1; done
```

---

## 실습 항목

| # | 항목 | 핵심 개념 |
|---|------|----------|
| 1 | Envoy 메트릭 직접 조회 | `curl localhost:15000/stats` |
| 2 | istio_requests_total PromQL | Prometheus 쿼리 |
| 3 | Grafana Istio Mesh Dashboard | 전체 메시 현황 |
| 4 | Grafana Istio Service Dashboard | 서비스별 성공률 |
| 5 | Jaeger 트레이스 조회 | `x-envoy-force-trace` 헤더 |
| 6 | 트레이스 샘플링 비율 변경 | 100% → 10% |
| 7 | Kiali 서비스 그래프 확인 | 토폴로지 시각화 |
| 8 | 커스텀 메트릭 추가 | Telemetry API |

---

## 실습 상세

### 1. Envoy 메트릭 직접 조회

**목표**: Envoy 사이드카가 노출하는 원시 메트릭을 직접 읽어 Prometheus가 수집하기 전 데이터를 확인한다. admin 포트(15000)는 클러스터 내부에서만 접근 가능하다.

```bash
# productpage Pod에서 자신의 Envoy 메트릭 조회
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15000/stats | head -50

# HTTP 관련 메트릭만 필터
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15000/stats | grep "http\."

# 업스트림 클러스터 연결 통계
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15000/stats | grep "outbound.*reviews"

# Prometheus 형식 메트릭 (15090 포트)
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s localhost:15090/stats/prometheus | grep istio_requests_total | head -10
```

---

### 2. istio_requests_total PromQL 쿼리

**목표**: Prometheus에서 Istio 표준 메트릭으로 요청 성공률과 트래픽 패턴을 파악한다.

```bash
# Prometheus 포트포워딩
kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
```

브라우저에서 `http://localhost:9090` 접속 후 아래 쿼리를 실행한다.

```promql
# bookinfo 네임스페이스 전체 요청 수 (1분 단위)
sum(rate(istio_requests_total{namespace="bookinfo"}[1m])) by (destination_service_name)

# 응답 코드별 요청 수
sum(rate(istio_requests_total{namespace="bookinfo"}[1m])) by (destination_service_name, response_code)

# 서비스별 성공률 (2xx 비율)
sum(rate(istio_requests_total{namespace="bookinfo", response_code=~"2.."}[1m])) by (destination_service_name)
/
sum(rate(istio_requests_total{namespace="bookinfo"}[1m])) by (destination_service_name)

# P99 응답 시간 (히스토그램 필요)
histogram_quantile(0.99, sum(rate(istio_request_duration_milliseconds_bucket{namespace="bookinfo"}[1m])) by (destination_service_name, le))
```

---

### 3. Grafana Istio Mesh Dashboard 확인

**목표**: 메시 전체의 글로벌 트래픽 현황(요청 수, 성공률, P50/P90/P99 지연)을 한 화면에서 파악한다.

```bash
# Grafana 포트포워딩
kubectl port-forward -n istio-system svc/grafana 3000:3000 &
```

1. `http://localhost:3000` 접속 (기본 계정: admin/admin)
2. Dashboards → Browse → Istio 폴더 선택
3. **Istio Mesh Dashboard** 선택
4. 확인 항목:
   - Global Request Volume (RPS)
   - Global Success Rate
   - 4xx/5xx 비율

```bash
# 의도적으로 에러 트래픽 발생 (존재하지 않는 경로)
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
for i in $(seq 1 20); do curl -s "http://$INGRESS_IP/nonexistent" -o /dev/null; done
```

**검증**: Dashboard에서 4xx 비율이 상승하는 것을 확인한다.

---

### 4. Grafana Istio Service Dashboard (서비스별 성공률)

**목표**: 특정 서비스(reviews)의 인바운드/아웃바운드 트래픽, 성공률, 지연 분포를 분석한다.

1. Dashboards → Istio → **Istio Service Dashboard** 선택
2. Service 드롭다운에서 `reviews.bookinfo.svc.cluster.local` 선택
3. 확인 항목:
   - Client Request Volume (클라이언트 관점)
   - Server Request Volume (서버 관점)
   - Client/Server Success Rate 비교 — 값이 다르면 네트워크 이슈나 정책 차단을 의심한다

```bash
# reviews v2/v3에는 ratings 호출이 있으므로 체인 트래픽 확인
# ratings 서비스도 Service Dashboard에서 확인
```

---

### 5. Jaeger 트레이스 조회

**목표**: `x-envoy-force-trace` 헤더를 사용해 샘플링 설정과 무관하게 특정 요청을 강제로 트레이싱한다.

```bash
# Jaeger 포트포워딩
kubectl port-forward -n istio-system svc/tracing 16686:80 &

# 강제 트레이스 요청 전송
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s -H "x-envoy-force-trace: true" "http://$INGRESS_IP/productpage" -o /dev/null
```

1. `http://localhost:16686` 접속
2. Service: `productpage.bookinfo` 선택
3. Find Traces 클릭
4. 트레이스 클릭 → 스팬 구조 확인 (productpage → reviews → ratings 호출 체인)

**검증**: productpage 요청 하나가 reviews, ratings 스팬을 포함한 트리 구조로 표시되면 분산 트레이싱이 정상이다.

---

### 6. 트레이스 샘플링 비율 변경 (100% → 10%)

**목표**: 프로덕션 환경에서는 100% 샘플링이 오버헤드를 유발한다. Telemetry API로 샘플링 비율을 동적으로 조정하는 방법을 익힌다.

```bash
# 현재 샘플링 설정 확인
kubectl get configmap istio -n istio-system -o jsonpath='{.data.mesh}' | grep tracing -A5

# Telemetry API로 샘플링 1% 설정 (메시 전체)
kubectl apply -f - <<'EOF'
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-tracing
  namespace: istio-system
spec:
  tracing:
    - randomSamplingPercentage: 10.0
EOF

# 적용 확인
kubectl get telemetry -n istio-system
```

```bash
# 10% 샘플링 확인: 100회 요청 중 약 10개만 Jaeger에 나타나야 함
for i in $(seq 1 100); do curl -s "http://$INGRESS_IP/productpage" -o /dev/null; done
# Jaeger에서 최근 트레이스 수가 ~10개이면 정상
```

```bash
# 실습 후 100%로 복구
kubectl apply -f - <<'EOF'
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-tracing
  namespace: istio-system
spec:
  tracing:
    - randomSamplingPercentage: 100.0
EOF
```

---

### 7. Kiali 서비스 그래프 확인

**목표**: Kiali의 서비스 그래프에서 트래픽 흐름, 오류 여부, mTLS 상태를 시각적으로 파악한다.

```bash
# Kiali 포트포워딩
kubectl port-forward -n istio-system svc/kiali 20001:20001 &
```

1. `http://localhost:20001` 접속
2. Graph 메뉴 → Namespace: `bookinfo` 선택
3. Display 옵션 체크:
   - Traffic Animation (트래픽 흐름 애니메이션)
   - Security (mTLS 자물쇠 아이콘)
   - Response Time
4. 엣지 클릭 시 해당 구간의 RPS, 성공률, 지연 확인 가능

```bash
# 에러 트래픽 주입 후 Kiali 그래프에서 빨간 엣지 확인
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-fault
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - fault:
        abort:
          percentage:
            value: 50
          httpStatus: 500
      route:
        - destination:
            host: reviews
EOF

# 트래픽 발생 후 Kiali에서 reviews 엣지가 빨간색으로 표시되는지 확인
for i in $(seq 1 30); do curl -s "http://$INGRESS_IP/productpage" -o /dev/null; done

# 테스트용 fault VirtualService 삭제
kubectl delete virtualservice reviews-fault -n bookinfo
```

---

### 8. 커스텀 메트릭 추가 (Telemetry API)

**목표**: Telemetry API를 사용해 기본 메트릭에 커스텀 태그(요청 헤더 값)를 추가한다. 이를 통해 A/B 테스트나 사용자 구분 메트릭을 Prometheus에서 집계할 수 있다.

```bash
kubectl apply -f - <<'EOF'
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: custom-metrics
  namespace: bookinfo
spec:
  metrics:
    - providers:
        - name: prometheus
      overrides:
        - match:
            metric: REQUEST_COUNT
          tagOverrides:
            user_agent:
              value: "request.headers['user-agent'] | 'unknown'"
EOF
```

```bash
# 커스텀 User-Agent로 요청 전송
for i in $(seq 1 10); do
  curl -s -H "User-Agent: my-test-client/1.0" "http://$INGRESS_IP/productpage" -o /dev/null
done

# Prometheus에서 새 태그 확인
# 쿼리: istio_requests_total{namespace="bookinfo", user_agent=~"my-test.*"}
```

**검증**: Prometheus에서 `user_agent="my-test-client/1.0"` 레이블이 포함된 `istio_requests_total` 메트릭이 조회되면 성공이다.

---

## 정리 (Cleanup)

```bash
# Telemetry 리소스 삭제
kubectl delete telemetry mesh-tracing -n istio-system --ignore-not-found
kubectl delete telemetry custom-metrics -n bookinfo --ignore-not-found

# 포트포워딩 종료
kill $(lsof -t -i:9090 -i:3000 -i:16686 -i:20001) 2>/dev/null

# 삭제 확인
kubectl get telemetry -A
```
