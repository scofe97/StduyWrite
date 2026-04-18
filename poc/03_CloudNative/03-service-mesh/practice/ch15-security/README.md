# Ch15 - 보안 (Security) 실습

---

> 대응 학습 문서: `learning/ch15-security/LEARN.md`

## 사전 조건

- bookinfo 네임스페이스에 Istio sidecar 주입 완료 (`kubectl label namespace bookinfo istio-injection=enabled`)
- bookinfo 앱 정상 기동 확인 (`kubectl get pods -n bookinfo`)
- `istioctl` CLI 설치 및 PATH 등록

```bash
# 사전 확인
kubectl get pods -n bookinfo
istioctl version
```

---

## 실습 항목

| # | 항목 | 핵심 개념 |
|---|------|----------|
| 1 | 기본 mTLS 상태 확인 | `istioctl authn tls-check` |
| 2 | PeerAuthentication STRICT 적용 | `peer-auth-strict.yaml` 활용 |
| 3 | 비메시 서비스 → 차단 확인 | sidecar 없는 Pod에서 접근 시도 |
| 4 | AuthorizationPolicy: SA 기반 허용 | `principals` 조건 |
| 5 | AuthorizationPolicy: HTTP 메서드 제한 | GET만 허용 |
| 6 | RequestAuthentication + JWT 검증 | `jwksUri` 설정 |
| 7 | deny-all 기본 정책 + 화이트리스트 | 기본 차단 후 개방 |

---

## 실습 상세

### 1. 기본 mTLS 상태 확인

**목표**: 현재 메시 내 서비스 간 TLS 상태를 파악한다. PERMISSIVE 모드에서는 평문과 mTLS 트래픽을 모두 허용한다.

```bash
# productpage Pod의 mTLS 연결 상태 전체 출력
istioctl authn tls-check $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -n bookinfo

# 특정 서비스 대상만 확인
istioctl authn tls-check $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') reviews.bookinfo.svc.cluster.local -n bookinfo
```

**검증**: `STATUS` 컬럼이 `OK`이고 `SERVER` 가 `mTLS` 또는 `PERMISSIVE` 로 표시되면 정상이다.

---

### 2. PeerAuthentication STRICT 적용

**목표**: bookinfo 네임스페이스 전체에 mTLS STRICT 모드를 적용해 평문 트래픽을 완전히 차단한다.

```bash
# security/ 디렉토리의 peer-auth-strict.yaml 적용
kubectl apply -f ../security/peer-auth-strict.yaml

# 적용 확인
kubectl get peerauthentication -n bookinfo
```

**peer-auth-strict.yaml 내용 확인**:
```bash
cat ../security/peer-auth-strict.yaml
```

**검증**: `istioctl authn tls-check` 재실행 시 `SERVER` 컬럼이 `mTLS` 로만 표시되면 STRICT 적용 성공이다.

---

### 3. 비메시 서비스에서 접근 시도 → 차단 확인

**목표**: sidecar가 없는 Pod에서 STRICT 모드 서비스에 접근하면 연결이 거부됨을 확인한다.

```bash
# sidecar 주입 없이 sleep Pod 생성 (default 네임스페이스)
kubectl run sleep --image=curlimages/curl -n default --restart=Never -- sleep 3600

# sleep Pod에서 bookinfo productpage로 접근 시도
kubectl exec -n default sleep -- curl -s http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"
```

**검증**: `000` (연결 실패) 또는 `Connection reset by peer` 메시지가 나타나면 STRICT 차단이 작동 중이다.

```bash
# 테스트 후 sleep Pod 삭제
kubectl delete pod sleep -n default
```

---

### 4. AuthorizationPolicy: 특정 ServiceAccount만 허용

**목표**: reviews 서비스에 대해 `bookinfo-productpage` ServiceAccount에서 오는 요청만 허용하는 정책을 적용한다. `peer-auth-strict.yaml` 에 이미 예시가 포함되어 있다.

```bash
# 현재 적용된 AuthorizationPolicy 확인
kubectl get authorizationpolicy -n bookinfo

# productpage SA에서 reviews 접근 - 허용되어야 함
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy -- curl -s http://reviews.bookinfo.svc.cluster.local:9080/reviews/1 -o /dev/null -w "%{http_code}"
```

SA 기반 정책 직접 생성:
```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: reviews-sa-allow
  namespace: bookinfo
spec:
  selector:
    matchLabels:
      app: reviews
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/bookinfo/sa/bookinfo-productpage"]
EOF
```

**검증**: ratings Pod에서 reviews로 직접 접근 시 `403` 이 반환되면 SA 제한이 적용된 것이다.

```bash
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s http://reviews.bookinfo.svc.cluster.local:9080/reviews/1 -o /dev/null -w "%{http_code}"
```

---

### 5. AuthorizationPolicy: HTTP 메서드 제한 (GET만 허용)

**목표**: productpage 서비스에 GET 요청만 허용하고 POST는 차단한다.

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-get-only
  namespace: bookinfo
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
    - to:
        - operation:
            methods: ["GET"]
EOF
```

**검증**:
```bash
# GET - 허용 (200)
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s -X GET http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"

# POST - 차단 (403)
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s -X POST http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"
```

---

### 6. RequestAuthentication + JWT 토큰 검증

**목표**: JWT 토큰 없이 접근하면 요청을 통과시키되, 잘못된 JWT가 있으면 `401` 을 반환하는 RequestAuthentication을 적용한다.

```bash
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: productpage-jwt
  namespace: bookinfo
spec:
  selector:
    matchLabels:
      app: productpage
  jwtRules:
    - issuer: "testing@secure.istio.io"
      jwksUri: "https://raw.githubusercontent.com/istio/istio/release-1.20/security/tools/jwt/samples/jwks.json"
EOF
```

**검증**:
```bash
# 토큰 없이 접근 - 통과 (200, RequestAuthentication만으로는 차단 안 됨)
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"

# 잘못된 JWT로 접근 - 401
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s -H "Authorization: Bearer invalid.token.here" http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"

# 유효한 테스트 JWT 토큰 획득 후 접근
TOKEN=$(curl -s https://raw.githubusercontent.com/istio/istio/release-1.20/security/tools/jwt/samples/demo.jwt)
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s -H "Authorization: Bearer $TOKEN" http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"
```

---

### 7. deny-all 기본 정책 + 화이트리스트 방식

**목표**: bookinfo 네임스페이스에 기본적으로 모든 트래픽을 차단하고, 필요한 경로만 명시적으로 허용하는 방어적 정책을 구성한다.

```bash
# 1단계: deny-all 기본 정책 (rules 없음 = 전체 차단)
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: bookinfo
spec: {}
EOF

# 차단 확인 - 403
kubectl exec -n bookinfo $(kubectl get pod -n bookinfo -l app=ratings -o jsonpath='{.items[0].metadata.name}') -- curl -s http://productpage.bookinfo.svc.cluster.local:9080/productpage -o /dev/null -w "%{http_code}"
```

```bash
# 2단계: productpage만 인그레스 게이트웨이에서 허용
kubectl apply -f - <<'EOF'
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-ingress-to-productpage
  namespace: bookinfo
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["istio-system"]
EOF
```

**검증**: 인그레스 게이트웨이 IP로 외부 접근은 `200`, 메시 내부 직접 접근은 `403` 이어야 한다.

---

## 정리 (Cleanup)

```bash
# 이번 실습에서 생성한 리소스 전체 삭제
kubectl delete authorizationpolicy reviews-sa-allow productpage-get-only deny-all allow-ingress-to-productpage -n bookinfo --ignore-not-found
kubectl delete requestauthentication productpage-jwt -n bookinfo --ignore-not-found
kubectl delete peerauthentication default -n bookinfo --ignore-not-found

# 삭제 확인
kubectl get peerauthentication,authorizationpolicy,requestauthentication -n bookinfo
```
