# Ch07 - Linkerd 트래픽 분할 실습
---
> 대응 학습 문서: `learning/ch07-linkerd-traffic/LEARN.md`

## 사전 조건

Ch06 실습이 완료되어 있어야 한다. Linkerd control plane과 emojivoto 앱이 실행 중이어야 한다:

```bash
linkerd check --proxy
kubectl get deploy -n emojivoto
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | HTTPRoute 구조 | httproute-canary.yaml 분석 | 파일 직접 검토 |
| 2 | 카나리 서비스 | `web-svc-canary` Deployment + Service 배포 | `kubectl get svc -n emojivoto` |
| 3 | HTTPRoute 적용 | `httproute-canary.yaml` 클러스터에 등록 | `kubectl get httproute -n emojivoto` |
| 4 | 트래픽 분할 확인 | 반복 curl로 90/10 비율 관찰 | 응답 헤더·바디 확인 |
| 5 | 가중치 변경 | 50/50 → 0/100 순서로 조정 | `linkerd viz stat` 비율 변화 |
| 6 | viz stat 확인 | 트래픽 분포를 메트릭으로 관찰 | `linkerd viz stat httproute` |
| 7 | ServiceProfile | 라우트별 메트릭 수집 설정 | `linkerd viz routes` |

## 실습 상세

### 1. httproute-canary.yaml 분석

**목표**: HTTPRoute의 `parentRefs`와 `backendRefs` 구조가 트래픽 가중치를 어떻게 표현하는지 이해한다.

```bash
cat httproute-canary.yaml
```

핵심 필드를 살펴본다:

- `parentRefs.name: web-svc` — `web-svc` Service가 이 HTTPRoute의 부모다. `web-svc`로 들어오는 트래픽을 이 라우트가 제어한다.
- `backendRefs` 배열 — 트래픽을 분기할 목적지 목록이다. `weight` 값의 합이 100이 되도록 구성한다.
- `weight: 90` / `weight: 10` — 전체 요청 중 90%는 `web-svc`로, 10%는 `web-svc-canary`로 전달된다.

이 HTTPRoute는 `policy.linkerd.io/v1beta3` API 버전을 사용한다. Linkerd가 Gateway API를 확장한 방식이다.

### 2. 카나리 서비스 배포

**목표**: 트래픽의 10%를 받을 카나리 버전 `web-svc-canary`를 배포한다. 원본과 동일한 포트를 노출하되 다른 이미지 태그를 사용한다.

**단계**:

```bash
# 카나리 Deployment 생성 (web의 다른 버전으로 가정)
kubectl create deployment web-svc-canary \
  --image=buoyantio/emojivoto-web:v11 \
  -n emojivoto

# 카나리 Service 생성
kubectl expose deployment web-svc-canary \
  --port=80 \
  --target-port=8080 \
  -n emojivoto

# Linkerd 사이드카 주입
kubectl get deploy web-svc-canary -n emojivoto -o yaml \
  | linkerd inject - \
  | kubectl apply -f -
```

**검증**:

```bash
kubectl get svc -n emojivoto
# web-svc와 web-svc-canary가 모두 보여야 한다
kubectl get pods -n emojivoto | grep canary
# Running 상태여야 한다
```

### 3. HTTPRoute 적용

**목표**: `httproute-canary.yaml`을 적용해 `web-svc`로 향하는 트래픽을 Linkerd가 두 백엔드로 분기하게 한다.

**단계**:

```bash
kubectl apply -f httproute-canary.yaml
```

**검증**:

```bash
kubectl get httproute -n emojivoto
# NAME               HOSTNAMES   AGE
# backend-canary               ...

kubectl describe httproute backend-canary -n emojivoto
# Rules: web-svc(weight:90), web-svc-canary(weight:10)
```

### 4. 트래픽 분할 확인

**목표**: 반복 요청을 보내 실제로 90/10 비율이 적용되는지 확인한다.

**단계**:

```bash
# web-svc ClusterIP 확인
kubectl get svc web-svc -n emojivoto

# 임시 Pod에서 반복 요청 (10회)
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never \
  -n emojivoto \
  -- sh -c 'for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" http://web-svc/; done'
```

**검증**:

```bash
# linkerd viz로 실시간 RPS 확인
linkerd viz stat deploy -n emojivoto
# web-svc-canary 행의 RPS가 web-svc의 약 1/9 수준이어야 한다
```

### 5. 가중치 변경

**목표**: 가중치를 단계적으로 조정해 카나리 롤아웃을 시뮬레이션한다.

**단계**:

```bash
# 50/50으로 변경
kubectl patch httproute backend-canary -n emojivoto \
  --type=json \
  -p='[
    {"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":50},
    {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":50}
  ]'

# 잠시 트래픽 관찰 후 0/100으로 변경 (완전 카나리 전환)
kubectl patch httproute backend-canary -n emojivoto \
  --type=json \
  -p='[
    {"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":0},
    {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":100}
  ]'
```

**검증**:

```bash
linkerd viz stat deploy -n emojivoto
# weight 0인 web-svc의 RPS가 0에 수렴해야 한다
```

### 6. linkerd viz stat으로 트래픽 분포 확인

**목표**: CLI에서 HTTPRoute 레벨의 트래픽 분포와 성공률을 확인한다.

**단계**:

```bash
# Deploy 단위 통계
linkerd viz stat deploy -n emojivoto

# HTTPRoute 단위 통계 (Linkerd 2.12+)
linkerd viz stat httproute -n emojivoto
```

**검증**:

```
NAME             MESHED   SUCCESS    RPS   LATENCY_P50   LATENCY_P95   LATENCY_P99
backend-canary      -     100.00%   1.5rps      1ms           2ms           3ms
```

각 route의 성공률이 100%에 가까워야 정상이다. 오류가 있으면 `linkerd viz tap deploy/web-svc -n emojivoto`로 요청 내용을 실시간 확인한다.

### 7. ServiceProfile로 라우트별 메트릭 수집

**목표**: ServiceProfile을 생성해 서비스의 라우트별(경로별) 메트릭을 수집한다. HTTPRoute와 달리 Linkerd 전용 리소스다.

**단계**:

```bash
# ServiceProfile 자동 생성 (Swagger/protobuf가 있을 때 유용)
linkerd profile --open-api /dev/null web-svc.emojivoto.svc.cluster.local \
  -n emojivoto

# 수동으로 경로 정의
cat <<EOF | kubectl apply -f -
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: web-svc.emojivoto.svc.cluster.local
  namespace: emojivoto
spec:
  routes:
    - name: GET /api/vote
      condition:
        method: GET
        pathRegex: /api/vote
    - name: GET /
      condition:
        method: GET
        pathRegex: /
EOF
```

**검증**:

```bash
linkerd viz routes svc/web-svc -n emojivoto
# ROUTE           SERVICE    SUCCESS    RPS   LATENCY_P50
# GET /api/vote   web-svc    100.00%   ...
# GET /           web-svc    100.00%   ...
```

## 정리 (Cleanup)

```bash
# HTTPRoute 삭제
kubectl delete -f httproute-canary.yaml

# 카나리 서비스 삭제
kubectl delete deploy web-svc-canary -n emojivoto
kubectl delete svc web-svc-canary -n emojivoto

# ServiceProfile 삭제
kubectl delete serviceprofile web-svc.emojivoto.svc.cluster.local -n emojivoto
```
