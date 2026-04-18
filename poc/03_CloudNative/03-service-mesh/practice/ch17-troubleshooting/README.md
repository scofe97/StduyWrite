# Ch17 - 트러블슈팅 (Troubleshooting) 실습

---

> 대응 학습 문서: `learning/ch17-troubleshooting/LEARN.md`

## 사전 조건

- bookinfo 앱 정상 기동 (`kubectl get pods -n bookinfo`)
- Grafana, Prometheus 접근 가능
- `istioctl` CLI 설치 완료

```bash
# 사전 확인
kubectl get pods -n bookinfo
kubectl get virtualservice,destinationrule -n bookinfo
```

---

## 실습 항목

| # | 항목 | 핵심 개념 |
|---|------|----------|
| 1 | 의도적 오류 생성: 없는 subset 참조 → 503 NC | 오류 재현 |
| 2 | `istioctl analyze` 로 오류 탐지 | `IST0101` 코드 |
| 3 | `istioctl describe pod` 경고 확인 | 설정 요약 |
| 4 | proxy-config listener → route → cluster → endpoint 추적 | xDS 체인 |
| 5 | Access Log JSON 형식 전환 | `accessLogEncoding: JSON` |
| 6 | Envoy 로그 레벨 변경 | `--level http:debug` |
| 7 | Grafana 클라이언트/서버 성공률 비교 | 이중 성공률 |
| 8 | Prometheus DC 플래그 쿼리 | `response_flags=DC` |
| 9 | ControlZ 접속 | port-forward 9876 |

---

## 실습 상세

### 1. 의도적 오류 생성: 없는 subset 참조 → 503 NC

**목표**: VirtualService에서 DestinationRule에 정의되지 않은 subset을 참조하면 Envoy가 `503 No cluster found (NC)` 를 반환한다. 이 오류 패턴을 직접 재현해 원인을 체득한다.

```bash
# DestinationRule에 v1, v2, v3 정의
kubectl apply -f - <<'EOF'
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

# VirtualService에서 존재하지 않는 subset "v4" 참조
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-broken
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v4
EOF
```

```bash
# 503 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s "http://$INGRESS_IP/productpage" | grep -i "sorry\|503\|unavailable"

# productpage 로그에서 upstream connect error 확인
kubectl logs -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy --tail=20
```

---

### 2. istioctl analyze로 오류 탐지 (IST0101)

**목표**: `istioctl analyze` 는 메시 설정 전체를 정적 분석해 없는 subset 참조 같은 구성 오류를 `IST0101` 코드로 보고한다. 실시간 에러 없이 사전 탐지가 가능하다.

```bash
# bookinfo 네임스페이스 분석
istioctl analyze -n bookinfo

# 예상 출력:
# Warning [IST0101] (VirtualService reviews-broken.bookinfo) 
#   Referenced host+subset in destinationrule not found: "reviews+v4"

# 전체 메시 분석
istioctl analyze --all-namespaces

# 특정 파일을 적용하기 전에 미리 분석 (dry-run)
istioctl analyze -n bookinfo --dry-run <<'EOF'
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: test-vs
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v99
EOF
```

**검증**: `IST0101` 경고가 출력되면 분석이 정상 작동한 것이다. 오류를 수정하기 전 이 명령으로 탐지 가능함을 확인한다.

---

### 3. istioctl describe pod으로 경고 확인

**목표**: Pod 단위로 적용된 Istio 설정(VirtualService, DestinationRule, PeerAuthentication 등)과 경고를 요약해 확인한다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# Pod에 적용된 설정 요약
istioctl describe pod $PRODUCTPAGE_POD -n bookinfo
```

출력에서 확인할 항목:
- `Exposed on port ...` — 노출된 포트
- `VirtualService: ...` — 적용된 VirtualService
- `WARNING: ...` — 설정 경고 (subset 참조 오류 등)
- `mTLS: ...` — TLS 상태

```bash
# reviews Pod 확인 (subset 참조 오류가 있는 VS 상태)
REVIEWS_POD=$(kubectl get pod -n bookinfo -l app=reviews,version=v1 -o jsonpath='{.items[0].metadata.name}')
istioctl describe pod $REVIEWS_POD -n bookinfo
```

---

### 4. proxy-config listener → route → cluster → endpoint 추적

**목표**: Envoy xDS 설정을 단계별로 추적해 특정 요청이 어떤 경로로 라우팅되는지 확인한다. "9080 포트로 오는 요청이 reviews 클러스터 어느 엔드포인트로 가는가"를 추적하는 것이 목표다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# 1단계: Listener 목록 확인 (9080 포트 리스너 찾기)
istioctl proxy-config listener $PRODUCTPAGE_POD -n bookinfo --port 9080

# 2단계: Route 설정 확인 (9080 포트의 라우트 이름 확인 후)
istioctl proxy-config route $PRODUCTPAGE_POD -n bookinfo --name "9080"

# 3단계: Cluster 목록 (outbound|9080||reviews.bookinfo.svc.cluster.local)
istioctl proxy-config cluster $PRODUCTPAGE_POD -n bookinfo --fqdn reviews.bookinfo.svc.cluster.local

# 4단계: Endpoint 목록 (실제 Pod IP 확인)
istioctl proxy-config endpoint $PRODUCTPAGE_POD -n bookinfo --cluster "outbound|9080||reviews.bookinfo.svc.cluster.local"
```

**검증**: 마지막 endpoint 출력의 IP가 reviews Pod IP와 일치하면 xDS 체인이 올바르게 구성된 것이다.

```bash
# reviews Pod IP 확인 (비교용)
kubectl get pods -n bookinfo -l app=reviews -o wide
```

---

### 5. Access Log JSON 형식 전환

**목표**: 기본 텍스트 형식 Access Log를 JSON으로 변환하면 `jq` 로 파싱하거나 로그 수집 파이프라인(Fluentd 등)에서 구조화된 처리가 가능하다.

```bash
# 현재 Access Log 형식 확인 (텍스트)
kubectl logs -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy --tail=5

# Telemetry API로 JSON 형식으로 전환
kubectl apply -f - <<'EOF'
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: access-log-json
  namespace: bookinfo
spec:
  accessLogging:
    - providers:
        - name: envoy
      disabled: false
EOF

# istio ConfigMap에서 직접 변경하는 방법 (대안)
# kubectl edit configmap istio -n istio-system
# accessLogEncoding: JSON 추가
```

```bash
# 트래픽 발생 후 JSON 로그 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s "http://$INGRESS_IP/productpage" -o /dev/null

kubectl logs -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy --tail=3 | python3 -m json.tool 2>/dev/null || echo "JSON 파싱 실패 - 아직 텍스트 형식"
```

---

### 6. Envoy 로그 레벨 변경 (http:debug)

**목표**: 특정 요청의 상세 처리 흐름을 확인해야 할 때 Envoy 로그 레벨을 debug로 높여 헤더, 라우팅 결정, 필터 처리 과정을 출력한다. 운영 환경에서는 짧게 적용 후 복구해야 한다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# 현재 로그 레벨 확인
istioctl proxy-config log $PRODUCTPAGE_POD -n bookinfo

# http 컴포넌트만 debug 레벨로 변경
istioctl proxy-config log $PRODUCTPAGE_POD -n bookinfo --level http:debug

# 변경 확인
istioctl proxy-config log $PRODUCTPAGE_POD -n bookinfo | grep "^http"
```

```bash
# 요청 발생 후 debug 로그 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s "http://$INGRESS_IP/productpage" -o /dev/null

# [debug][http] 로그 확인
kubectl logs -n bookinfo $PRODUCTPAGE_POD -c istio-proxy --tail=50 | grep "debug.*http\|http.*debug"

# 로그 레벨 원복 (warning으로)
istioctl proxy-config log $PRODUCTPAGE_POD -n bookinfo --level http:warning
```

---

### 7. Grafana에서 클라이언트/서버 성공률 비교

**목표**: Grafana Istio Service Dashboard에서 클라이언트 측 성공률과 서버 측 성공률이 다를 때 어느 구간에서 문제가 발생했는지 추론한다.

```bash
# Grafana 포트포워딩
kubectl port-forward -n istio-system svc/grafana 3000:3000 &

# 테스트 트래픽 발생
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
for i in $(seq 1 50); do curl -s "http://$INGRESS_IP/productpage" -o /dev/null; done
```

1. `http://localhost:3000` → Dashboards → Istio → **Istio Service Dashboard**
2. Service: `reviews.bookinfo.svc.cluster.local`
3. **Client Success Rate** vs **Server Success Rate** 비교

| 상황 | 의미 |
|------|------|
| Client 낮음, Server 높음 | 네트워크 레벨 또는 sidecar 수신 전 차단 |
| Client 높음, Server 낮음 | 애플리케이션 레벨 오류 |
| 둘 다 낮음 | 업스트림 서비스 장애 |

**검증**: 1단계에서 만든 `reviews-broken` VirtualService 적용 상태에서 Client Success Rate가 낮고 Server는 높은 패턴을 확인한다.

---

### 8. Prometheus DC 플래그 쿼리

**목표**: `response_flags` 레이블을 사용해 Envoy가 반환하는 오류 유형을 분류한다. `DC` (Downstream Connection Termination), `NR` (No Route), `NC` (No Cluster) 등 플래그로 근본 원인을 좁힌다.

```bash
# Prometheus 포트포워딩
kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
```

`http://localhost:9090` 에서 아래 쿼리 실행:

```promql
# NC 플래그 (No Cluster - subset 참조 실패) 확인
sum(rate(istio_requests_total{namespace="bookinfo", response_flags="NC"}[1m])) by (destination_service_name, source_app)

# 모든 오류 플래그 분포
sum(rate(istio_requests_total{namespace="bookinfo", response_code!="200"}[1m])) by (response_flags, destination_service_name)

# UH 플래그 (No Healthy Upstream) 확인
sum(rate(istio_requests_total{response_flags="UH"}[5m])) by (destination_service_name)
```

**주요 response_flags 참조**:
- `DC` — 다운스트림 연결 끊김
- `NC` — 클러스터 없음 (subset 오류)
- `NR` — 라우트 없음
- `UH` — 헬시 업스트림 없음
- `UT` — 업스트림 타임아웃

---

### 9. ControlZ 접속 (port-forward 9876)

**목표**: ControlZ는 istiod 내부 상태(로그 레벨, 메모리, 고루틴)를 브라우저 UI로 확인할 수 있는 관리 인터페이스다. 운영 중 istiod 이슈 진단에 사용한다.

```bash
# istiod Pod 확인
kubectl get pod -n istio-system -l app=istiod

# ControlZ 포트포워딩 (9876 → 9876)
kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=istiod -o jsonpath='{.items[0].metadata.name}') 9876:9876 &
```

1. `http://localhost:9876` 접속
2. 확인 항목:
   - **Logging** 탭: 컴포넌트별 로그 레벨 실시간 변경 (UI에서 직접 변경 가능)
   - **Memory** 탭: Heap 사용량, GC 상태
   - **Process** 탭: Go 고루틴 수, CPU 사용

```bash
# 포트포워딩 종료
kill $(lsof -t -i:9876) 2>/dev/null
```

---

## 정리 (Cleanup)

```bash
# 오류 재현용 리소스 삭제
kubectl delete virtualservice reviews-broken -n bookinfo --ignore-not-found
kubectl delete destinationrule reviews -n bookinfo --ignore-not-found
kubectl delete telemetry access-log-json -n bookinfo --ignore-not-found

# 포트포워딩 종료
kill $(lsof -t -i:9090 -i:3000 -i:9876) 2>/dev/null

# 최종 상태 확인
kubectl get virtualservice,destinationrule,telemetry -n bookinfo
istioctl analyze -n bookinfo
```
