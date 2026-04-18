# Ch19 - EnvoyFilter 실습

---

> 대응 학습 문서: `learning/ch19-envoyfilter/LEARN.md`

## 사전 조건

- bookinfo 앱 정상 기동 (`kubectl get pods -n bookinfo`)
- `istioctl` CLI 설치 완료
- WasmPlugin 실습(항목 4)은 OCI 레지스트리 접근 또는 공개 WASM 이미지 필요

```bash
# 사전 확인
kubectl get pods -n bookinfo
kubectl get envoyfilter -A
```

> EnvoyFilter는 Istio 공식 API(VirtualService, DestinationRule 등)로 해결되지 않는 저수준 Envoy 설정을 직접 변경할 때 사용한다. 잘못 적용하면 트래픽이 전면 차단되므로 applyTo와 match 조건을 신중하게 설정해야 한다.

---

## 실습 항목

| # | 항목 | 핵심 개념 |
|---|------|----------|
| 1 | EnvoyFilter로 응답 헤더 추가 | `x-custom-header` |
| 2 | config_dump에서 필터 적용 확인 | 적용 검증 |
| 3 | retriable_status_codes 설정 | 408 재시도 |
| 4 | WasmPlugin 리소스 생성 | 예시 WASM 모듈 |
| 5 | EnvoyFilter 우선순위 테스트 | 두 개 충돌 시 |
| 6 | 잘못된 EnvoyFilter → 복구 절차 | 장애 복구 |

---

## 실습 상세

### 1. EnvoyFilter로 응답 헤더 추가 (x-custom-header)

**목표**: productpage 서비스의 모든 HTTP 응답에 `x-custom-header: istio-lab` 헤더를 추가한다. Lua 필터를 사용하며, 서버 코드 변경 없이 사이드카 레벨에서 헤더를 주입한다.

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: add-custom-header
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: productpage
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
              subFilter:
                name: envoy.filters.http.router
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.lua
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.LuaPerRoute
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
            inlineCode: |
              function envoy_on_response(response_handle)
                response_handle:headers():add("x-custom-header", "istio-lab")
              end
EOF
```

**검증**:
```bash
# 인그레스 게이트웨이를 통해 응답 헤더 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s -I "http://$INGRESS_IP/productpage" | grep -i "x-custom-header"
# 출력: x-custom-header: istio-lab
```

---

### 2. config_dump에서 필터 적용 확인

**목표**: EnvoyFilter 적용 후 실제로 Envoy 설정에 반영되었는지 config_dump의 HTTP 필터 체인에서 Lua 필터를 확인한다.

```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# HTTP 필터 체인에서 Lua 필터 확인
kubectl exec -n bookinfo $PRODUCTPAGE_POD -c istio-proxy -- \
  curl -s localhost:15000/config_dump | \
  python3 -c "
import json, sys
d = json.load(sys.stdin)
for cfg in d.get('configs', []):
    if 'dynamic_listeners' in cfg:
        for l in cfg['dynamic_listeners']:
            chains = l.get('active_state', {}).get('listener', {}).get('filter_chains', [])
            for chain in chains:
                for f in chain.get('filters', []):
                    if 'http_connection_manager' in f.get('name', ''):
                        hcm = f.get('typed_config', {})
                        for hf in hcm.get('http_filters', []):
                            if 'lua' in hf.get('name', '').lower():
                                print('Lua filter found:', hf['name'])
"
```

```bash
# 더 간단한 방법: proxy-config listener로 확인
istioctl proxy-config listener $PRODUCTPAGE_POD -n bookinfo --port 9080 -o json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2))" | \
  grep -A2 "lua"
```

**검증**: `envoy.filters.http.lua` 또는 `lua` 가 출력되면 필터가 주입된 것이다.

---

### 3. EnvoyFilter로 retriable_status_codes 설정 (408)

**목표**: 기본적으로 Envoy는 `connect-failure`, `retriable-4xx`, `refused-stream` 조건에서만 재시도한다. `408` (Request Timeout) 은 기본 재시도 대상이 아니지만, EnvoyFilter로 `retriable_status_codes` 에 추가할 수 있다.

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: retryable-408
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
            name: "reviews.bookinfo.svc.cluster.local:9080"
            route:
              action: ANY
      patch:
        operation: MERGE
        value:
          route:
            retry_policy:
              retry_on: "retriable-status-codes"
              retriable_status_codes:
                - 408
              num_retries: 3
EOF
```

**검증**:
```bash
PRODUCTPAGE_POD=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# reviews Route 설정에서 retry_policy 확인
istioctl proxy-config route $PRODUCTPAGE_POD -n bookinfo --name "9080" -o json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2))" | \
  grep -A10 "retry_policy"
```

`retriable_status_codes: [408]` 이 출력되면 적용 성공이다.

---

### 4. WasmPlugin 리소스 생성 (예시 WASM 모듈)

**목표**: WasmPlugin API는 EnvoyFilter보다 안전하고 선언적인 방식으로 WASM 필터를 주입한다. Istio 공식 예시 WASM 모듈(헤더 추가)로 동작을 확인한다.

```bash
# Istio 공식 예시 WASM 플러그인 적용
kubectl apply -f - <<'EOF'
apiVersion: extensions.istio.io/v1alpha1
kind: WasmPlugin
metadata:
  name: example-wasm-plugin
  namespace: bookinfo
spec:
  selector:
    matchLabels:
      app: productpage
  url: oci://ghcr.io/istio-ecosystem/wasm-extensions/basic_auth:latest
  phase: AUTHN
  pluginConfig:
    basic_auth_rules:
      - prefix: "/"
        request_methods:
          - "GET"
        credentials:
          - "user1:password1"
EOF
```

```bash
# WasmPlugin 적용 확인
kubectl get wasmplugin -n bookinfo

# productpage Pod에서 WASM 플러그인 로딩 로그 확인
kubectl logs -n bookinfo $(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}') -c istio-proxy | grep -i wasm | tail -10
```

> 네트워크 제한으로 OCI 레지스트리 접근이 안 될 경우 `url` 을 로컬 HTTP 서버로 변경하거나 항목을 건너뛰고 5번으로 이동한다.

```bash
# 테스트 후 삭제
kubectl delete wasmplugin example-wasm-plugin -n bookinfo --ignore-not-found
```

---

### 5. EnvoyFilter 우선순위 테스트 (두 개 충돌 시)

**목표**: 같은 워크로드에 두 개의 EnvoyFilter가 같은 위치에 패치를 적용하면 적용 순서가 중요하다. `priority` 필드로 순서를 명시하거나, 네임스페이스 레벨과 워크로드 레벨 EnvoyFilter의 우선순위 규칙을 확인한다.

```bash
# 첫 번째 EnvoyFilter: x-filter-order: first 헤더 추가
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: header-filter-a
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: productpage
  priority: 10
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
              subFilter:
                name: envoy.filters.http.router
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.lua
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
            inlineCode: |
              function envoy_on_response(response_handle)
                response_handle:headers():add("x-filter-order", "filter-a")
              end
EOF

# 두 번째 EnvoyFilter: priority 낮게 설정 (나중에 적용)
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: header-filter-b
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: productpage
  priority: 20
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
              subFilter:
                name: envoy.filters.http.router
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.lua
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
            inlineCode: |
              function envoy_on_response(response_handle)
                response_handle:headers():add("x-filter-order", "filter-b")
              end
EOF
```

```bash
# 두 필터 모두 적용 확인
kubectl get envoyfilter -n bookinfo

# 응답 헤더에서 두 필터 모두 나타나는지 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s -I "http://$INGRESS_IP/productpage" | grep -i "x-filter-order"
```

**priority 규칙 정리**:
- 숫자가 낮을수록 먼저 적용된다 (기본값 0)
- 네임스페이스 레벨 EnvoyFilter(workloadSelector 없음)는 워크로드 레벨보다 먼저 적용된다
- 같은 priority면 이름 알파벳 순으로 적용된다

```bash
# 정리
kubectl delete envoyfilter header-filter-a header-filter-b -n bookinfo --ignore-not-found
```

---

### 6. 잘못된 EnvoyFilter 적용 → 복구 절차

**목표**: 잘못된 EnvoyFilter를 적용해 트래픽이 차단되는 상황을 재현하고, 빠른 복구 절차를 익힌다. EnvoyFilter 장애의 특징은 에러 메시지 없이 조용하게 트래픽이 끊기는 것이다.

```bash
# 의도적으로 잘못된 Lua 코드가 포함된 EnvoyFilter 적용
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: broken-filter
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: productpage
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
              subFilter:
                name: envoy.filters.http.router
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.lua
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
            inlineCode: |
              function envoy_on_request(request_handle)
                -- 의도적 오류: 존재하지 않는 메서드 호출
                request_handle:nonexistent_method()
              end
EOF

# 트래픽 차단 확인
INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s -o /dev/null -w "%{http_code}" "http://$INGRESS_IP/productpage"
# 500 또는 연결 실패
```

**복구 절차**:
```bash
# 1단계: 잘못된 EnvoyFilter 즉시 삭제
kubectl delete envoyfilter broken-filter -n bookinfo

# 2단계: productpage Pod Envoy 설정 수렴 확인 (5~10초 대기)
sleep 10

# 3단계: 트래픽 복구 확인
curl -s -o /dev/null -w "%{http_code}" "http://$INGRESS_IP/productpage"
# 200이어야 함

# 4단계: istiod 로그에서 EnvoyFilter 오류 원인 확인
kubectl logs -n istio-system $(kubectl get pod -n istio-system -l app=istiod -o jsonpath='{.items[0].metadata.name}') | grep -i "envoyfilter\|lua" | tail -20
```

**EnvoyFilter 안전 적용 체크리스트**:
- `istioctl analyze` 로 사전 검증
- `workloadSelector` 를 반드시 좁게 설정 (전체 메시 적용 주의)
- 프로덕션 적용 전 개발 네임스페이스에서 먼저 테스트
- 적용 직후 `curl -s -o /dev/null -w "%{http_code}"` 로 즉시 검증
- 롤백 명령을 사전에 준비 (`kubectl delete envoyfilter <name>`)

---

## 정리 (Cleanup)

```bash
# 모든 EnvoyFilter 삭제
kubectl delete envoyfilter add-custom-header retryable-408 header-filter-a header-filter-b broken-filter -n bookinfo --ignore-not-found

# WasmPlugin 삭제
kubectl delete wasmplugin -n bookinfo --all --ignore-not-found

# 최종 확인
kubectl get envoyfilter,wasmplugin -n bookinfo
# 결과: No resources found
```
