# Ch01 - 서비스 메시 기초 실습
---
> 대응 학습 문서: `learning/01-service-mesh-fundamentals/LEARN.md`

## 사전 조건

- Docker Desktop 실행 중
- Kind 설치 (`go install sigs.k8s.io/kind@latest`)
- kubectl 설치
- istioctl 설치 (`curl -L https://istio.io/downloadIstio | sh -`)
- 클러스터 없음 (이 챕터에서 생성)

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | 클러스터 준비 | Kind 클러스터 생성 | `kubectl cluster-info` |
| 2 | 메시 없는 통신 | nginx 2개 배포 후 curl 직접 통신 | `kubectl logs` |
| 3 | 평문 통신 확인 | tcpdump로 패킷 캡처 | 평문 HTTP 내용 확인 |
| 4 | Istio 설치 + sidecar 주입 | 동일 서비스에 Envoy 사이드카 주입 | `kubectl get pods` 에서 2/2 확인 |
| 5 | mTLS 암호화 확인 | tcpdump 재시도 → 암호화 확인 | 평문 사라짐 확인 |

## 실습 상세

### 1. Kind 클러스터 생성

**목표**: 실습용 로컬 K8s 클러스터를 생성한다.

**단계**:
1. 클러스터 생성
   ```bash
   make cluster-up
   ```
2. 컨텍스트 확인
   ```bash
   kubectl cluster-info --context kind-mesh-lab
   kubectl get nodes
   ```

**검증**:
```
NAME                     STATUS   ROLES           AGE
mesh-lab-control-plane   Ready    control-plane   Xm
mesh-lab-worker          Ready    <none>          Xm
mesh-lab-worker2         Ready    <none>          Xm
```

### 2. 메시 없는 서비스 배포

**목표**: 사이드카 없이 두 nginx Pod가 직접 통신하는 상황을 만든다.

**단계**:
1. 네임스페이스 및 서비스 생성
   ```bash
   kubectl create namespace demo
   kubectl run server --image=nginx --port=80 -n demo
   kubectl expose pod server --port=80 --name=server-svc -n demo
   kubectl run client --image=curlimages/curl --restart=Never \
     -n demo -- sleep 3600
   ```
2. client에서 server로 요청
   ```bash
   kubectl exec -n demo client -- curl -s http://server-svc/
   ```

**검증**: nginx 기본 페이지 HTML이 출력된다.

### 3. 평문 통신 확인 (tcpdump)

**목표**: 메시 없는 상태에서 HTTP 패킷이 평문으로 흐름을 직접 눈으로 확인한다.

**단계**:
1. server Pod가 뜬 노드 확인
   ```bash
   kubectl get pod server -n demo -o wide
   ```
2. 해당 노드의 컨테이너 PID에서 tcpdump 실행 (Kind 노드 내부 접근)
   ```bash
   # Kind 노드에 접속
   docker exec -it mesh-lab-worker bash

   # 내부에서 tcpdump (eth0 또는 veth 인터페이스)
   tcpdump -i any port 80 -A 2>/dev/null | grep -E "GET|Host|HTTP"
   ```
3. 별도 터미널에서 반복 요청
   ```bash
   kubectl exec -n demo client -- \
     curl -s http://server-svc/ -o /dev/null
   ```

**검증**: `GET / HTTP/1.1`, `Host: server-svc` 등 평문 헤더가 출력된다.

### 4. Istio 설치 및 sidecar 주입

**목표**: Istio control plane을 설치하고 demo 네임스페이스에 자동 sidecar 주입을 활성화한다.

**단계**:
1. Istio 설치 (demo profile)
   ```bash
   istioctl install --set profile=demo -y
   ```
2. 설치 확인
   ```bash
   kubectl get pods -n istio-system
   ```
3. demo 네임스페이스에 자동 주입 레이블 추가
   ```bash
   kubectl label namespace demo istio-injection=enabled
   ```
4. 기존 Pod 재시작 (레이블은 새 Pod에만 적용됨)
   ```bash
   kubectl rollout restart deployment -n demo 2>/dev/null || true
   kubectl delete pod server client -n demo
   kubectl run server --image=nginx --port=80 -n demo
   kubectl expose pod server --port=80 --name=server-svc -n demo \
     --dry-run=client -o yaml | kubectl apply -f -
   kubectl run client --image=curlimages/curl --restart=Never \
     -n demo -- sleep 3600
   ```
5. sidecar 주입 확인
   ```bash
   kubectl get pods -n demo
   ```

**검증**: READY 컬럼이 `2/2`로 표시된다 (app 컨테이너 + istio-proxy).

### 5. mTLS 암호화 확인

**목표**: Istio가 자동으로 적용한 mTLS로 인해 동일 요청이 암호화됨을 확인한다.

**단계**:
1. 동일하게 tcpdump 실행 (Kind 노드 내부)
   ```bash
   docker exec -it mesh-lab-worker bash
   tcpdump -i any port 80 -A 2>/dev/null | head -50
   ```
2. 별도 터미널에서 요청
   ```bash
   kubectl exec -n demo client -- curl -s http://server-svc/
   ```
3. mTLS 상태 직접 확인
   ```bash
   istioctl authn tls-check client.demo
   ```

**검증**:
- tcpdump에서 HTTP 헤더 평문이 사라지고 암호화된 바이트가 보인다.
- `tls-check` 출력에서 `mTLS` 모드가 `STRICT` 또는 `PERMISSIVE`로 표시된다.

## 정리 (Cleanup)

```bash
kubectl delete namespace demo
# 클러스터 전체 삭제가 필요하면
make cluster-down
```
