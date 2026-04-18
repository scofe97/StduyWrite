# Ch08 - Linkerd 제로 트러스트 보안 실습
---
> 대응 학습 문서: `learning/ch08-linkerd-security/LEARN.md`

## 사전 조건

Ch06 실습이 완료되어 있어야 한다. Linkerd control plane과 emojivoto 앱이 실행 중이어야 한다:

```bash
linkerd check --proxy
kubectl get deploy -n emojivoto
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | default-deny.yaml 분석 | Server·AuthorizationPolicy·MeshTLSAuthentication 구조 확인 | 파일 직접 검토 |
| 2 | PERMISSIVE 모드 확인 | 정책 없이 서비스 간 통신 가능함을 확인 | `linkerd viz tap` |
| 3 | Server 적용 | `web-server` Server 리소스 등록 | `kubectl get server -n emojivoto` |
| 4 | AuthorizationPolicy 적용 | 허가되지 않은 서비스 차단 확인 | `linkerd viz tap`으로 deny 관찰 |
| 5 | MeshTLSAuthentication 적용 | 네임스페이스 내 서비스만 허용 | `curl` 차단 / 내부 서비스 허용 |
| 6 | viz tap으로 트래픽 관찰 | 허용·차단 요청을 실시간으로 구분 | `linkerd viz tap` 출력 |
| 7 | 정책 제거 후 복원 | 리소스 삭제 후 통신 재개 확인 | `curl` 응답 정상 복귀 |

## 실습 상세

### 1. default-deny.yaml 분석

**목표**: `default-deny.yaml`의 세 리소스가 어떻게 조합해 제로 트러스트 정책을 구성하는지 이해한다.

```bash
cat default-deny.yaml
```

리소스별 역할을 살펴본다:

- `Server (web-server)` — `app: web-svc` Pod의 8080 포트를 Linkerd 정책 대상으로 선언한다. Server가 존재하는 순간, 이 포트로의 접근은 명시적 허가가 없으면 기본 거부(default-deny) 상태가 된다.
- `AuthorizationPolicy (web-allow-vote)` — `web-server` Server에 대한 허가 조건을 정의한다. `requiredAuthenticationRefs`가 충족될 때만 접근을 허용한다.
- `MeshTLSAuthentication (mesh-tls)` — `*.emojivoto.serviceaccount.identity.linkerd.cluster.local` 패턴에 일치하는 mTLS ID를 가진 요청만 인증된 것으로 간주한다. emojivoto 네임스페이스의 서비스 어카운트만 허용하는 의미다.

세 리소스의 관계: `Server`가 포트를 선언하고, `AuthorizationPolicy`가 `Server`를 targetRef로 지정하며, `MeshTLSAuthentication`이 실제 ID 검증을 수행한다.

### 2. 정책 없이 통신 확인 (PERMISSIVE 모드)

**목표**: Server 리소스가 없으면 Linkerd가 기본적으로 모든 트래픽을 허용함을 확인한다.

**단계**:

```bash
# 네임스페이스 전체 서버 리소스 확인 (없어야 함)
kubectl get server -n emojivoto

# 메시 내부에서 web-svc 호출
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never \
  -n emojivoto \
  -- curl -s -o /dev/null -w "%{http_code}" http://web-svc/
```

**검증**:

```bash
linkerd viz tap deploy/web -n emojivoto --namespace emojivoto
# tls=true 이지만 정책 리소스 없이도 200 응답이 온다
# → PERMISSIVE 상태
```

### 3. Server 리소스 적용

**목표**: `web-server` Server를 등록해 `web-svc` Pod의 8080 포트를 정책 관리 대상으로 선언한다. 이 시점부터 AuthorizationPolicy 없이는 모든 접근이 거부된다.

**단계**:

```bash
# Server만 먼저 적용 (AuthorizationPolicy 없이)
kubectl apply -f - <<EOF
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: web-server
  namespace: emojivoto
spec:
  podSelector:
    matchLabels:
      app: web-svc
  port: 8080
  proxyProtocol: HTTP/2
EOF
```

**검증**:

```bash
kubectl get server -n emojivoto
# NAME         PORT   PROTOCOL
# web-server   8080   HTTP/2

# 이 상태에서 web-svc 호출 시 거부됨
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never \
  -n emojivoto \
  -- curl -s -o /dev/null -w "%{http_code}" http://web-svc/
# 403 또는 연결 실패
```

### 4. AuthorizationPolicy 적용 후 차단 확인

**목표**: `web-allow-vote` AuthorizationPolicy를 적용해 mesh-tls 인증을 통과한 서비스만 허용하게 한다. 메시 외부 요청(plain curl Pod)은 여전히 차단된다.

**단계**:

```bash
kubectl apply -f - <<EOF
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: web-allow-vote
  namespace: emojivoto
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: web-server
  requiredAuthenticationRefs:
    - name: mesh-tls
      kind: MeshTLSAuthentication
      group: policy.linkerd.io
EOF
```

**검증**:

```bash
# Linkerd 사이드카 없는 Pod에서 호출 → 차단
kubectl run no-mesh-curl --image=curlimages/curl --rm -it --restart=Never \
  -- curl -s -o /dev/null -w "%{http_code}" http://web-svc.emojivoto/
# 403

# 메시 내부 서비스(vote-bot)에서 호출 → 허용됨
linkerd viz tap deploy/vote-bot -n emojivoto
# → :status=200
```

### 5. MeshTLSAuthentication 적용

**목표**: `mesh-tls` MeshTLSAuthentication을 등록해 emojivoto 네임스페이스 ServiceAccount ID만 인증된 것으로 처리한다.

**단계**:

```bash
kubectl apply -f default-deny.yaml
# 세 리소스가 모두 적용된다
```

**검증**:

```bash
kubectl get meshTLSAuthentication -n emojivoto
# NAME       AGE
# mesh-tls   ...

# emojivoto 네임스페이스 외 서비스에서 접근 시도
kubectl run ext-curl --image=curlimages/curl --rm -it --restart=Never \
  -n default \
  -- curl -s -o /dev/null -w "%{http_code}" http://web-svc.emojivoto/
# 403 또는 연결 실패 (다른 네임스페이스 SA이므로 패턴 불일치)
```

### 6. linkerd viz tap으로 허용/차단 트래픽 관찰

**목표**: `linkerd viz tap` 명령으로 요청의 허용·차단 여부를 실시간으로 확인한다.

**단계**:

```bash
# 한 터미널에서 tap 실행
linkerd viz tap deploy/web -n emojivoto

# 다른 터미널에서 내부 서비스 트래픽 발생
kubectl run mesh-curl --image=curlimages/curl --rm -it --restart=Never \
  -n emojivoto \
  -- sh -c 'for i in $(seq 1 5); do curl -s http://web-svc/; done'

# 외부(메시 없는) 요청도 시도
kubectl run nomesh-curl --image=curlimages/curl --rm -it --restart=Never \
  -n default \
  -- curl -s http://web-svc.emojivoto/
```

**검증**:

```
# 허용된 요청 (tap 출력)
req id=0:0 proxy=in  src=10.0.0.5:... dst=10.0.0.6:8080 tls=true :method=GET :path=/
rsp id=0:0 proxy=in  src=10.0.0.5:... dst=10.0.0.6:8080 tls=true :status=200

# 차단된 요청 (tap 출력)
req id=1:0 proxy=in  src=10.0.0.7:... dst=10.0.0.6:8080 tls=false :method=GET :path=/
rsp id=1:0 proxy=in  src=10.0.0.7:... dst=10.0.0.6:8080 tls=false :status=403
```

`tls=true`인 요청은 허용, `tls=false`인 요청은 차단되는 패턴을 확인한다.

### 7. 정책 제거 후 통신 복원 확인

**목표**: 정책 리소스를 삭제하면 PERMISSIVE 상태로 돌아가 모든 트래픽이 다시 허용됨을 확인한다.

**단계**:

```bash
# 정책 리소스 전체 삭제
kubectl delete -f default-deny.yaml
```

**검증**:

```bash
# Server 삭제 확인
kubectl get server,authorizationpolicy,meshTLSAuthentication -n emojivoto
# No resources found

# 외부 요청 복원 확인
kubectl run restore-test --image=curlimages/curl --rm -it --restart=Never \
  -n default \
  -- curl -s -o /dev/null -w "%{http_code}" http://web-svc.emojivoto/
# 200
```

## 정리 (Cleanup)

```bash
# 정책 리소스 삭제 (아직 남아있는 경우)
kubectl delete -f default-deny.yaml --ignore-not-found

# 테스트용 Pod가 남아있는 경우
kubectl delete pod curl-test no-mesh-curl ext-curl mesh-curl nomesh-curl restore-test \
  -n emojivoto --ignore-not-found
kubectl delete pod ext-curl nomesh-curl -n default --ignore-not-found
```
