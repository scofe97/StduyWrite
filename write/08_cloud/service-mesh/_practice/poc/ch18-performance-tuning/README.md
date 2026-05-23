# Ch18 - 성능 튜닝 (Performance Tuning) 실습

---

> 대응 학습 문서: `learning/ch18-performance-tuning/LEARN.md`

## 사전 조건

- 멀티 네임스페이스 환경 (bookinfo 외 추가 앱 네임스페이스가 있을수록 효과가 명확하다)
- `istioctl` CLI 설치 완료
- Prometheus 접근 가능

```bash
# 현재 메시 전체 네임스페이스 확인
kubectl get ns --show-labels | grep "istio-injection=enabled"

# istiod 현재 메모리/CPU 사용량 확인
kubectl top pod -n istio-system -l app=istiod
```

---

## 실습 항목

| # | 항목 | 핵심 개념 |
|---|------|----------|
| 1 | config_dump 크기 측정 | 튜닝 전 기준선 확인 |
| 2 | Sidecar CRD 적용 (메시 전체 기본) | egress 범위 제한 |
| 3 | config_dump 크기 재측정 | 감소 확인 |
| 4 | discoverySelectors 설정 | `istio-exclude` 레이블 |
| 5 | proxy-config endpoint로 제외 확인 | 제거된 서비스 확인 |
| 6 | pilot_proxy_convergence_time PromQL | 수렴 시간 모니터링 |
| 7 | pilot_xds_pushes 모니터링 | 푸시 빈도 확인 |
| 8 | PILOT_DEBOUNCE_AFTER 변경 | 배치 처리 조정 |
| 9 | istiod 스케일 아웃 (replicaCount: 2) | HA 구성 |

---

## 실습 상세

### 1. config_dump 크기 측정 (튜닝 전 기준선)

**목표**: Envoy가 받은 xDS 설정 전체 크기를 바이트 단위로 측정한다. 메시에 네임스페이스가 많을수록 config_dump가 커지고, 이것이 메모리/CPU 오버헤드의 주원인이다. 튜닝 전 기준선을 반드시 기록한다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# config_dump 전체 크기 (바이트)
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- curl -s localhost:15000/config_dump | wc -c

# 섹션별 크기 분석
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- curl -s localhost:15000/config_dump | python3 -c "
import json, sys
d = json.load(sys.stdin)
for cfg in d.get('configs', []):
    name = cfg.get('@type','').split('.')[-1]
    size = len(json.dumps(cfg))
    print(f'{name}: {size:,} bytes')
"

# Cluster 개수 확인 (많을수록 오버헤드)
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- curl -s localhost:15000/clusters | grep "::" | wc -l
```

**기록**: 이 숫자를 메모해둔다. Sidecar CRD 적용 후 비교한다.

---

### 2. Sidecar CRD 적용 (메시 전체 기본값)

**목표**: Sidecar CRD로 각 워크로드가 알아야 하는 서비스 범위를 제한한다. 기본값(Sidecar 없음)은 메시 내 모든 서비스를 알지만, 대부분의 서비스는 같은 네임스페이스 + 공통 서비스만 알면 충분하다.

```bash
# istio-system 네임스페이스의 기본 Sidecar 리소스 (메시 전체 적용)
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: istio-system
spec:
  egress:
    - hosts:
        - "./*"          # 같은 네임스페이스의 모든 서비스
        - "istio-system/*"  # istio-system 네임스페이스
EOF

# 적용 확인
kubectl get sidecar -A
```

```bash
# bookinfo 네임스페이스용 추가 세밀 설정 (reviews는 ratings만 알면 됨)
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: reviews-sidecar
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: reviews
  egress:
    - hosts:
        - "./ratings"
        - "istio-system/*"
EOF
```

---

### 3. config_dump 크기 재측정 (감소 확인)

**목표**: Sidecar CRD 적용 후 config_dump 크기가 줄어들었음을 수치로 확인한다. 감소분이 클수록 메시 규모가 크고 튜닝 효과가 뚜렷하다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# 잠시 대기 (설정 수렴 시간)
sleep 10

# 크기 재측정
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- curl -s localhost:15000/config_dump | wc -c

# Cluster 개수 재확인
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- curl -s localhost:15000/clusters | grep "::" | wc -l
```

**검증**: Cluster 개수가 줄어들면 Sidecar CRD가 정상 적용된 것이다. 기존 대비 30~70% 감소가 일반적이다.

```bash
# reviews Pod는 ratings 클러스터만 남아있어야 함
REVIEWS_POD=$(kubectl get pod -n bookinfo -l app=reviews,version=v1 -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n bookinfo $REVIEWS_POD -c istio-proxy -- curl -s localhost:15000/clusters | grep "::" | grep -v "istio-system\|ratings\|reviews"
# 위 명령 결과가 비어있으면 정상 (ratings, reviews, istio-system 외 클러스터 없음)
```

---

### 4. discoverySelectors 설정 (istio-exclude 레이블)

**목표**: discoverySelectors는 istiod 자체가 감시하는 네임스페이스를 제한한다. `istio-exclude` 레이블을 가진 네임스페이스는 메시에서 완전히 제외되어 istiod 메모리 사용량이 줄어든다.

```bash
# 테스트용 비메시 네임스페이스 생성
kubectl create namespace non-mesh-test --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace non-mesh-test istio-exclude=true

# istio ConfigMap에 discoverySelectors 추가
kubectl get configmap istio -n istio-system -o yaml > /tmp/istio-cm-backup.yaml

kubectl patch configmap istio -n istio-system --type=merge -p '{
  "data": {
    "meshConfig": "discoverySelectors:\n- matchExpressions:\n  - key: istio-exclude\n    operator: DoesNotExist\n"
  }
}'
```

```bash
# istiod 재시작 (설정 반영)
kubectl rollout restart deployment/istiod -n istio-system
kubectl rollout status deployment/istiod -n istio-system
```

---

### 5. proxy-config endpoint로 제외 확인

**목표**: discoverySelectors 적용 후 `non-mesh-test` 네임스페이스 서비스가 Envoy endpoint 목록에서 사라졌는지 확인한다.

```bash
# non-mesh-test에 테스트 서비스 배포
kubectl apply -n non-mesh-test -f - <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: excluded-svc
spec:
  ports:
    - port: 80
  selector:
    app: excluded
EOF

# productpage의 endpoint 목록에서 excluded-svc 확인 (없어야 함)
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')
istioctl proxy-config endpoint $PRODUCTPAGE_POD -n bookinfo | grep "excluded"
# 결과가 비어있으면 제외 성공
```

```bash
# 비교: bookinfo 내 서비스는 여전히 존재해야 함
istioctl proxy-config endpoint $PRODUCTPAGE_POD -n bookinfo | grep "reviews"
```

**검증**: `excluded` 는 결과 없음, `reviews` 는 결과 있음이어야 한다.

---

### 6. pilot_proxy_convergence_time PromQL 쿼리

**목표**: istiod가 설정 변경을 감지한 후 Envoy에 전달 완료까지 걸리는 시간(수렴 시간)을 측정한다. 메시가 클수록 수렴 시간이 길어지고, Sidecar CRD 적용 후 단축됨을 확인할 수 있다.

```bash
# Prometheus 포트포워딩
kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
```

`http://localhost:9090` 에서 아래 쿼리 실행:

```promql
# 수렴 시간 P50/P90/P99
histogram_quantile(0.50, sum(rate(pilot_proxy_convergence_time_bucket[5m])) by (le))
histogram_quantile(0.90, sum(rate(pilot_proxy_convergence_time_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(pilot_proxy_convergence_time_bucket[5m])) by (le))

# 수렴 시간 평균
rate(pilot_proxy_convergence_time_sum[5m]) / rate(pilot_proxy_convergence_time_count[5m])
```

```bash
# 설정 변경을 강제로 유발 (수렴 시간 측정용)
kubectl label namespace bookinfo test-label=trigger
kubectl label namespace bookinfo test-label-
```

**검증**: Sidecar CRD 적용 전후 수렴 시간 P99을 비교한다. 네임스페이스가 많을수록 차이가 크게 나타난다.

---

### 7. pilot_xds_pushes 모니터링

**목표**: istiod가 Envoy에 xDS 설정을 푸시하는 빈도와 유형(CDS, LDS, EDS, RDS)을 모니터링한다. 과도한 푸시는 불필요한 네트워크/CPU 사용의 신호다.

```bash
# Prometheus에서 쿼리 실행
# http://localhost:9090
```

```promql
# 초당 xDS 푸시 횟수 (타입별)
sum(rate(pilot_xds_pushes[1m])) by (type)

# 오류 포함 전체 푸시
sum(rate(pilot_xds[1m])) by (type)

# 설정 변경 없이 재연결로 인한 Full Push 횟수
rate(pilot_xds_push_time_count[5m])
```

```bash
# 푸시를 강제로 유발하는 방법: Pod 재시작
kubectl rollout restart deployment/reviews-v1 -n bookinfo
# Prometheus에서 pilot_xds_pushes 급증 확인
```

---

### 8. PILOT_DEBOUNCE_AFTER 변경

**목표**: istiod는 짧은 시간 내 여러 설정 변경이 발생하면 Debounce 처리로 묶어서 한 번에 푸시한다. `PILOT_DEBOUNCE_AFTER` 를 늘리면 푸시 횟수가 줄지만 반영 지연이 증가한다. 트레이드오프를 직접 확인한다.

```bash
# 현재 Debounce 설정 확인
kubectl get deployment istiod -n istio-system -o jsonpath='{.spec.template.spec.containers[0].env}' | python3 -m json.tool 2>/dev/null | grep -A2 DEBOUNCE

# istioctl install로 변경 (기본값: 100ms → 500ms)
istioctl install --set profile=default \
  --set "values.pilot.env.PILOT_DEBOUNCE_AFTER=500ms" \
  -y

# istiod 재시작 확인
kubectl rollout status deployment/istiod -n istio-system
```

```bash
# 연속 설정 변경으로 Debounce 효과 확인
for i in $(seq 1 5); do
  kubectl label namespace bookinfo debounce-test=$i --overwrite
  sleep 0.1
done
# Prometheus에서 pilot_xds_pushes - 5번이 아닌 1~2번으로 묶여야 함
```

```bash
# 기본값으로 복구
istioctl install --set profile=default \
  --set "values.pilot.env.PILOT_DEBOUNCE_AFTER=100ms" \
  -y
```

---

### 9. istiod 스케일 아웃 (replicaCount: 2)

**목표**: istiod를 2개로 스케일 아웃해 단일 장애점을 제거하고 xDS 처리량을 분산한다. 메시 규모가 클수록 istiod 하나로는 수렴 시간 지연이 발생한다.

```bash
# 현재 istiod 레플리카 수 확인
kubectl get deployment istiod -n istio-system -o jsonpath='{.spec.replicas}'

# replicaCount 2로 스케일 아웃
kubectl patch deployment istiod -n istio-system \
  --type=merge \
  -p '{"spec":{"replicas":2}}'

# 스케일 아웃 확인
kubectl rollout status deployment/istiod -n istio-system
kubectl get pods -n istio-system -l app=istiod
```

```bash
# 두 istiod Pod가 모두 Ready 상태인지 확인
kubectl get pods -n istio-system -l app=istiod -o wide

# Prometheus에서 istiod 메모리 사용량 비교
# process_resident_memory_bytes{app="istiod"}
```

**검증**: istiod Pod 2개가 모두 Running/Ready 상태이고, `kubectl get pods -n bookinfo` 가 정상이면 HA 구성 성공이다.

```bash
# 실습 후 1개로 복구 (리소스 절약)
kubectl patch deployment istiod -n istio-system \
  --type=merge \
  -p '{"spec":{"replicas":1}}'
```

---

## 정리 (Cleanup)

```bash
# Sidecar CRD 삭제
kubectl delete sidecar default -n istio-system --ignore-not-found
kubectl delete sidecar reviews-sidecar -n bookinfo --ignore-not-found

# 테스트 네임스페이스 삭제
kubectl delete namespace non-mesh-test --ignore-not-found

# discoverySelectors 설정 제거 (원복)
cp /tmp/istio-cm-backup.yaml /tmp/istio-cm-restore.yaml
kubectl apply -f /tmp/istio-cm-restore.yaml

# istiod 재시작
kubectl rollout restart deployment/istiod -n istio-system
kubectl rollout status deployment/istiod -n istio-system

# 포트포워딩 종료
kill $(lsof -t -i:9090) 2>/dev/null

# 최종 확인
kubectl get sidecar -A
kubectl get pods -n istio-system -l app=istiod
```
