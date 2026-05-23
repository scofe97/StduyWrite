# Ch05 - Linkerd 아키텍처 실습
---
> 대응 학습 문서: `learning/05-linkerd-architecture/LEARN.md`

## 사전 조건

- Kind 클러스터 실행 중 (`make cluster-up`)
- linkerd CLI 설치
  ```bash
  curl -sL https://run.linkerd.io/install | sh
  export PATH=$PATH:$HOME/.linkerd2/bin
  ```
- kubectl 설치
- Helm 3 설치

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | 사전 요건 확인 | `linkerd check --pre` | 모든 체크 PASS |
| 2 | Control plane 설치 | `linkerd install \| kubectl apply` | `linkerd check` |
| 3 | 설치 검증 | `linkerd check` | 전체 green |
| 4 | Control plane Pod 구조 | destination / identity / proxy-injector 역할 파악 | `kubectl describe` |
| 5 | viz 확장 설치 | `linkerd viz install \| kubectl apply` | `linkerd viz check` |
| 6 | 대시보드 확인 | `linkerd viz dashboard` | 브라우저 접속 |
| 7 | emojivoto 메시 적용 | `linkerd inject` 후 배포 | 사이드카 2/2 확인 |

## 실습 상세

### 1. 사전 요건 확인

**목표**: Linkerd 설치 전 클러스터가 최소 요구사항을 충족하는지 확인한다. kernel 버전, API 서버 접근, 권한 등을 자동으로 점검한다.

**단계**:
1. 사전 체크 실행
   ```bash
   linkerd check --pre
   ```

**검증**:
```
kubernetes-api
--------------
√ can initialize the client
√ can query the Kubernetes API

kubernetes-version
------------------
√ is running the minimum Kubernetes API version

...

Status check results are √
```
모든 항목에 `√` 가 표시되면 설치 가능하다.

### 2. Control Plane 설치

**목표**: Linkerd control plane을 클러스터에 설치한다. CRD와 core control plane을 순서대로 설치해야 한다.

**단계**:
1. CRD 먼저 설치
   ```bash
   linkerd install --crds | kubectl apply -f -
   ```
2. Control plane 설치
   ```bash
   linkerd install | kubectl apply -f -
   ```
3. 설치 완료 대기
   ```bash
   kubectl wait --for=condition=Available deployment \
     --all -n linkerd --timeout=120s
   ```

**검증**:
```bash
kubectl get pods -n linkerd
```
```
NAME                                     READY   STATUS    RESTARTS
linkerd-destination-xxx                  4/4     Running   0
linkerd-identity-xxx                     2/2     Running   0
linkerd-proxy-injector-xxx               2/2     Running   0
```

### 3. 설치 검증

**목표**: `linkerd check`는 control plane의 전체 상태를 점검한다. 인증서 유효성, API 서버 통신, 각 컴포넌트 상태를 한 번에 확인한다.

**단계**:
1. 전체 체크 실행
   ```bash
   linkerd check
   ```

**검증**:
```
linkerd-config
--------------
√ control plane Namespace exists
√ control plane ClusterRoles exist
...

linkerd-control-plane-proxy
---------------------------
√ control plane proxies are healthy
√ control plane proxies are up-to-date

Status check results are √
```

### 4. Control Plane Pod 구조 확인

**목표**: Linkerd의 3개 핵심 컴포넌트(destination, identity, proxy-injector)가 각각 어떤 역할을 하는지 실제 Pod 정보로 확인한다.

**단계**:
1. 각 Deployment 상세 확인
   ```bash
   # destination: 서비스 디스커버리 + 로드밸런싱 정책 제공 (xDS 역할)
   kubectl describe deployment linkerd-destination -n linkerd | \
     grep -E "Image:|Port:|Args:"

   # identity: mTLS 인증서 발급 및 갱신 (CA 역할)
   kubectl describe deployment linkerd-identity -n linkerd | \
     grep -E "Image:|Port:|Args:"

   # proxy-injector: Pod 생성 시 linkerd-proxy 사이드카 자동 주입 (웹훅)
   kubectl describe deployment linkerd-proxy-injector -n linkerd | \
     grep -E "Image:|Port:|Args:"
   ```
2. 사이드카 프록시 버전 확인
   ```bash
   linkerd version
   ```
3. identity가 발급한 인증서 확인
   ```bash
   linkerd identity -n linkerd linkerd-destination-$(kubectl get pod \
     -n linkerd -l linkerd.io/control-plane-component=destination \
     -o jsonpath='{.items[0].metadata.name}') 2>/dev/null || \
   kubectl exec -n linkerd deployment/linkerd-identity -- \
     linkerd identity 2>/dev/null || true
   ```

**검증**: 세 컴포넌트의 역할을 아래 표로 정리한다.

| 컴포넌트 | 역할 | Istio 대응 컴포넌트 |
|---------|------|-------------------|
| destination | 서비스 디스커버리, 트래픽 정책 배포 | Pilot (istiod 일부) |
| identity | mTLS 인증서 발급 CA | Citadel (istiod 일부) |
| proxy-injector | sidecar 자동 주입 웹훅 | Sidecar Injector (istiod 일부) |

### 5. viz 확장 설치

**목표**: Linkerd viz는 Prometheus, Grafana, tap 기능을 포함한 관측성 확장이다. core와 별도로 설치한다.

**단계**:
1. viz 설치
   ```bash
   linkerd viz install | kubectl apply -f -
   ```
2. 설치 완료 대기
   ```bash
   kubectl wait --for=condition=Available deployment \
     --all -n linkerd-viz --timeout=120s
   ```
3. viz 체크
   ```bash
   linkerd viz check
   ```

**검증**:
```bash
kubectl get pods -n linkerd-viz
```
```
NAME                          READY   STATUS
grafana-xxx                   2/2     Running
metrics-api-xxx               2/2     Running
prometheus-xxx                2/2     Running
tap-xxx                       2/2     Running
tap-injector-xxx              2/2     Running
web-xxx                       2/2     Running
```

### 6. 대시보드 확인

**목표**: Linkerd viz 대시보드를 브라우저에서 열어 클러스터 전체 서비스 맵과 메트릭을 확인한다.

**단계**:
1. 대시보드 실행 (포트 포워딩 자동)
   ```bash
   linkerd viz dashboard &
   ```
   자동으로 브라우저가 열린다. 열리지 않으면 출력된 URL을 직접 접속한다.
2. 대시보드에서 확인할 항목
   - Namespaces 탭: 메시에 포함된 네임스페이스 목록
   - Deployments 탭: 각 Deployment의 RPS, 성공률, P50/P99 레이턴시
   - Topology 탭: 서비스 간 트래픽 그래프

**검증**: 브라우저에서 `http://localhost:50750` (포트는 자동 할당) 접속 후 Linkerd 대시보드가 표시된다.

### 7. emojivoto 앱 배포 후 메시 적용

**목표**: 샘플 앱 emojivoto를 배포하고 `linkerd inject`로 사이드카를 주입해 메시에 포함시킨다.

**단계**:
1. emojivoto 배포
   ```bash
   curl -sL https://run.linkerd.io/emojivoto.yml | kubectl apply -f -
   ```
2. Pod 기동 대기
   ```bash
   kubectl wait --for=condition=Ready pod --all \
     -n emojivoto --timeout=60s
   ```
3. 현재 상태 확인 (사이드카 없음 — READY 1/1)
   ```bash
   kubectl get pods -n emojivoto
   ```
4. linkerd inject로 사이드카 주입 후 재배포
   ```bash
   kubectl get -n emojivoto deploy -o yaml \
     | linkerd inject - \
     | kubectl apply -f -
   ```
5. 재시작 완료 대기
   ```bash
   kubectl rollout status deploy --all -n emojivoto
   ```
6. 사이드카 주입 확인
   ```bash
   kubectl get pods -n emojivoto
   ```

**검증**:
```
NAME                        READY   STATUS
emoji-xxx                   2/2     Running
vote-bot-xxx                2/2     Running
voting-xxx                  2/2     Running
web-xxx                     2/2     Running
```
모든 Pod의 READY가 `2/2`로 바뀐다 (앱 컨테이너 + linkerd-proxy).

```bash
# viz에서도 확인
linkerd viz stat deploy -n emojivoto
```

## 정리 (Cleanup)

```bash
# emojivoto만 삭제
kubectl delete namespace emojivoto

# Linkerd 전체 삭제가 필요한 경우
linkerd viz uninstall | kubectl delete -f -
linkerd uninstall | kubectl delete -f -

# 클러스터 전체 삭제
make cluster-down
```
