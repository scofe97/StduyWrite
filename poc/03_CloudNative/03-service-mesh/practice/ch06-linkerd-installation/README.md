# Ch06 - Linkerd 설치 실습
---
> 대응 학습 문서: `learning/ch06-linkerd-installation/LEARN.md`

## 사전 조건

Kind 클러스터가 실행 중이어야 한다. `step` CLI와 `helm`이 설치되어 있어야 한다:

```bash
# 도구 확인
step version
helm version
kubectl cluster-info
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | Trust Anchor 인증서 | step CLI로 루트 CA 생성 | `step certificate inspect ca.crt` |
| 2 | Issuer 인증서 | Trust anchor로 issuer 인증서 서명 | `step certificate inspect issuer.crt` |
| 3 | Linkerd CRD 설치 | `linkerd-crds` Helm 차트 설치 | `kubectl get crd \| grep linkerd` |
| 4 | values.yaml 분석 | 리소스 요청값·identity 설정 확인 | 파일 직접 검토 |
| 5 | Control Plane 설치 | `linkerd-control-plane` Helm 차트 설치 | `linkerd check` |
| 6 | Viz 확장 설치 | 대시보드 컴포넌트 배포 | `linkerd viz dashboard` |
| 7 | 메시 주입 | emojivoto 앱 배포 후 sidecar 주입 | `linkerd viz stat deploy -n emojivoto` |

## 실습 상세

### 1. Trust Anchor 인증서 생성

**목표**: Linkerd 메시의 루트 신뢰 앵커(root CA)를 생성한다. 모든 프록시 간 mTLS가 이 CA를 기반으로 검증된다.

**단계**:

```bash
# 루트 CA 생성 (비밀번호 없음, 만료 87600h = 10년)
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca \
  --no-password \
  --insecure \
  --not-after 87600h

# issuer 인증서 생성 (루트 CA로 서명, 만료 8760h = 1년)
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
  --profile intermediate-ca \
  --not-after 8760h \
  --no-password \
  --insecure \
  --ca ca.crt \
  --ca-key ca.key
```

**검증**:

```bash
step certificate inspect ca.crt --short
step certificate inspect issuer.crt --short
# 출력 예: Subject: root.linkerd.cluster.local, Issuer: root.linkerd.cluster.local
```

### 2. Linkerd CRD 설치

**목표**: Linkerd가 사용하는 커스텀 리소스 정의(CRD)를 클러스터에 등록한다. Control Plane보다 먼저 설치해야 한다.

**단계**:

```bash
# Linkerd Helm repo 추가
helm repo add linkerd https://helm.linkerd.io/stable
helm repo update

# CRD 설치
helm install linkerd-crds linkerd/linkerd-crds \
  -n linkerd \
  --create-namespace
```

**검증**:

```bash
kubectl get crd | grep linkerd
# Server, HTTPRoute, AuthorizationPolicy 등 CRD가 등록된다
```

### 3. values.yaml 분석

**목표**: `values.yaml`이 Kind 환경에서 왜 리소스를 줄였는지 이해한다.

`values.yaml` 파일의 핵심 설정은 다음과 같다:

```bash
cat values.yaml
```

주목할 항목:
- `proxy.resources.cpu.request: 10m` — 사이드카 프록시마다 CPU를 10m만 요청한다. 프로덕션 기본값(100m)의 10%다.
- `controllerResources` YAML 앵커(`&controller_resources`) — `destinationResources`, `identityResources`, `proxyInjectorResources`가 같은 값을 참조한다. 반복을 제거하는 YAML 기법이다.
- `identity.issuer.scheme: kubernetes.io/tls` — Kubernetes Secret에서 issuer 인증서를 읽는 방식이다. cert-manager 없이 수동으로 Secret을 생성해야 한다.

### 4. Control Plane 설치

**목표**: 인증서를 Secret으로 등록하고 `values.yaml`을 적용해 Control Plane을 배포한다.

**단계**:

```bash
# issuer 인증서를 Secret으로 등록
kubectl create secret tls linkerd-identity-issuer \
  --cert=issuer.crt \
  --key=issuer.key \
  -n linkerd

# ca.crt 내용을 values.yaml의 identityTrustAnchorsPEM에 붙여넣는다
# (또는 --set 플래그로 직접 전달)
CA_CRT=$(cat ca.crt)

# Control Plane 설치
helm install linkerd-control-plane \
  -n linkerd \
  --set identityTrustAnchorsPEM="${CA_CRT}" \
  -f values.yaml \
  linkerd/linkerd-control-plane
```

**검증**:

```bash
kubectl get pods -n linkerd
# linkerd-destination, linkerd-identity, linkerd-proxy-injector 가 Running 상태여야 한다
```

### 5. linkerd check로 설치 검증

**목표**: Linkerd가 정상적으로 동작하는지 내장 진단 도구로 확인한다.

**단계**:

```bash
linkerd check
```

**검증**:

```
Status check results are √
...
√ control plane is healthy
√ data plane is healthy
```

모든 항목 앞에 `√`가 표시되어야 한다. `×`가 있으면 해당 항목의 오류 메시지를 확인한다.

### 6. Viz 확장 설치

**목표**: 트래픽 메트릭을 시각화하는 `linkerd viz` 컴포넌트를 배포한다. Prometheus와 대시보드가 포함된다.

**단계**:

```bash
linkerd viz install | kubectl apply -f -

# 설치 완료 대기
kubectl rollout status deploy -n linkerd-viz
```

**검증**:

```bash
linkerd viz check
# 별도 탭에서 대시보드 접속
linkerd viz dashboard &
```

### 7. emojivoto 앱 배포 및 메시 주입

**목표**: 샘플 앱을 배포하고 Linkerd 사이드카를 주입해 메시 안에서 동작하게 한다.

**단계**:

```bash
# emojivoto 배포
curl -sL run.linkerd.io/emojivoto.yml | kubectl apply -f -

# 기존 Deployment에 사이드카 주입 (inject → apply)
kubectl get -n emojivoto deploy -o yaml \
  | linkerd inject - \
  | kubectl apply -f -

# 주입 완료 대기
kubectl rollout status deploy -n emojivoto
```

**검증**:

```bash
linkerd viz stat deploy -n emojivoto
# NAME       MESHED   SUCCESS   RPS   LATENCY_P50   LATENCY_P99
# emoji          1/1   100.00%   ...
# vote-bot       1/1   100.00%   ...
# web            1/1   100.00%   ...

# MESHED 열이 1/1이어야 사이드카가 주입된 것이다
```

## 정리 (Cleanup)

```bash
# emojivoto 삭제
kubectl delete ns emojivoto

# Viz 삭제
linkerd viz uninstall | kubectl delete -f -

# Control Plane 삭제
helm uninstall linkerd-control-plane -n linkerd
helm uninstall linkerd-crds -n linkerd
kubectl delete ns linkerd

# 인증서 파일 삭제
rm -f ca.crt ca.key issuer.crt issuer.key
```
