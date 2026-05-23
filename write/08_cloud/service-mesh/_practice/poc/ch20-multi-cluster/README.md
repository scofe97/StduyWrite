# Ch20 - Multi-Cluster 실습
---
> 대응 학습 문서: `learning/ch20-multi-cluster/LEARN.md`

단일 클러스터 환경에서는 실제 멀티클러스터 연동을 완전히 재현할 수 없다. 이 실습은 개념 이해와 설정 파일 분석을 중심으로 진행하며, Kind 2클러스터 구성은 선택 항목으로 제공한다.

## 사전 조건

- Istio가 설치된 GCP K8s 클러스터 (단일)
- `istioctl` CLI 설치 완료
- `kubectl` 컨텍스트가 대상 클러스터로 설정되어 있을 것

## 실습 항목

| # | 항목 | 유형 | 예상 시간 |
|---|------|------|----------|
| 1 | 멀티클러스터 아키텍처 유형 이해 | 개념 분석 | 15분 |
| 2 | 현재 클러스터의 mesh ID/network/cluster 이름 확인 | 명령어 실행 | 10분 |
| 3 | `istioctl create-remote-secret` 명령어 테스트 | 명령어 실행 | 10분 |
| 4 | ServiceEntry로 원격 서비스 시뮬레이션 | 리소스 배포 | 20분 |
| 5 | (선택) Kind 2클러스터 구성 시도 | 환경 구성 | 60분 |

## 실습 상세

### 1. 멀티클러스터 아키텍처 유형 이해

Istio 멀티클러스터는 두 가지 주요 토폴로지를 지원한다.

**Multi-Primary**: 각 클러스터에 독립적인 istiod가 존재하며, 두 클러스터가 대등한 관계를 갖는다. 한 클러스터의 istiod 장애가 다른 클러스터에 영향을 주지 않아 고가용성 구성에 적합하다.

**Primary-Remote**: 하나의 istiod가 여러 클러스터의 사이드카를 중앙에서 제어한다. 원격 클러스터는 istiod 없이 경량으로 운영되므로 리소스 절약이 가능하지만, Primary 장애 시 전체 메시 제어가 중단된다.

두 토폴로지에 공통으로 필요한 요소:

- 동일한 `meshID` 설정
- 클러스터 간 네트워크 도달 가능성 (또는 East-West Gateway)
- 루트 CA 공유 (cross-cluster mTLS)

### 2. 현재 클러스터의 mesh ID / network / cluster 이름 확인

현재 클러스터의 Istio 메시 설정을 확인한다:

```bash
# IstioOperator 또는 ConfigMap에서 meshID 확인
kubectl get configmap istio -n istio-system -o yaml | grep -E "meshID|network|cluster"

# istiod 환경변수에서 확인
kubectl get deployment istiod -n istio-system -o jsonpath='{.spec.template.spec.containers[0].env}' | jq '.[] | select(.name | test("MESH|NETWORK|CLUSTER"))'

# Helm values로 설치한 경우
helm get values istiod -n istio-system
```

예상 출력 예시:

```yaml
meshID: mesh1
network: network1
multiCluster:
  clusterName: cluster1
```

### 3. `istioctl create-remote-secret` 명령어 테스트

이 명령어는 원격 클러스터에서 실행해 현재 클러스터가 원격의 API 서버에 접근할 수 있는 시크릿을 생성한다. 단일 클러스터 환경에서는 dry-run으로 출력 구조를 확인한다:

```bash
# dry-run: 생성될 Secret 구조 확인
istioctl create-remote-secret \
  --name=remote-cluster1 \
  --type=remote \
  --namespace=istio-system \
  --dry-run

# 실제 멀티클러스터 환경에서는 원격 클러스터 kubeconfig를 지정
# istioctl create-remote-secret \
#   --kubeconfig=/path/to/remote-kubeconfig \
#   --name=cluster2 | kubectl apply -f - --context=cluster1
```

출력에서 확인할 내용:

- `type: kubernetes.io/service-account-token` 기반 시크릿 구조
- `istio/multiCluster: "true"` 어노테이션
- base64 인코딩된 kubeconfig 내용

### 4. ServiceEntry로 원격 서비스 시뮬레이션

실제 원격 클러스터 없이도 ServiceEntry를 통해 외부 서비스를 메시 내부에서 참조하는 패턴을 실습할 수 있다. 원격 클러스터의 서비스를 로컬 메시에 등록하는 것과 동일한 원리다:

```bash
# 테스트용 네임스페이스 생성
kubectl create namespace mesh-demo
kubectl label namespace mesh-demo istio-injection=enabled

# 원격 서비스를 시뮬레이션하는 ServiceEntry 배포
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: remote-httpbin
  namespace: mesh-demo
spec:
  hosts:
  - httpbin.remote-cluster.svc.cluster.local
  location: MESH_INTERNAL
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: STATIC
  endpoints:
  - address: httpbin.org   # 실습용 퍼블릭 엔드포인트
    ports:
      http: 80
EOF
```

검증 방법:

```bash
# 테스트 Pod 배포
kubectl run curl-test --image=curlimages/curl -n mesh-demo --rm -it -- \
  curl -s http://httpbin.remote-cluster.svc.cluster.local/get

# Envoy 라우팅 테이블에서 엔드포인트 확인
kubectl run curl-test --image=curlimages/curl -n mesh-demo --restart=Never -- sleep 3600
istioctl proxy-config endpoints curl-test.mesh-demo | grep remote
```

### 5. (선택) Kind 2클러스터 구성 시도

로컬 머신에 Kind가 설치된 경우, 두 클러스터를 생성해 Multi-Primary 구성의 초기 단계를 확인할 수 있다:

```bash
# cluster1 생성
kind create cluster --name cluster1

# cluster2 생성
kind create cluster --name cluster2

# 컨텍스트 확인
kubectl config get-contexts | grep kind

# 각 클러스터에 Istio 설치 (meshID 동일하게 설정)
istioctl install --context=kind-cluster1 \
  --set values.global.meshID=mesh1 \
  --set values.global.multiCluster.clusterName=cluster1 \
  --set values.global.network=network1 -y

istioctl install --context=kind-cluster2 \
  --set values.global.meshID=mesh1 \
  --set values.global.multiCluster.clusterName=cluster2 \
  --set values.global.network=network1 -y
```

> Kind는 단일 노드 클러스터이므로 클러스터 간 직접 Pod IP 통신이 되지 않는다. East-West Gateway 없이는 서비스 디스커버리 이후 실제 트래픽 전달이 실패한다. 개념 확인 수준에서 진행한다.

## 정리 (Cleanup)

```bash
# ServiceEntry 삭제
kubectl delete serviceentry remote-httpbin -n mesh-demo

# 네임스페이스 삭제
kubectl delete namespace mesh-demo

# (선택) Kind 클러스터 삭제
kind delete cluster --name cluster1
kind delete cluster --name cluster2
```
