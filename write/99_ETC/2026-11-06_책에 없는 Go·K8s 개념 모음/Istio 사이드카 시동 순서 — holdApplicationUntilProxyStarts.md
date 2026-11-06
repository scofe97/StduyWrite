---
title: "Istio 사이드카 시동 순서 — holdApplicationUntilProxyStarts"
tags: [istio, sidecar, startup-order, holdApplicationUntilProxyStarts, native-sidecar, kubernetes]
status: draft
source:
  - https://istio.io/v1.27/docs/reference/config/istio.mesh.v1alpha1/
  - https://istio.io/v1.27/blog/2023/native-sidecars/
  - https://istio.io/v1.27/docs/reference/commands/pilot-discovery/
  - https://istio.io/v1.27/docs/reference/commands/pilot-agent/
  - https://v1-36.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
updated: 2026-11-06
---

# Istio 사이드카 시동 순서 — holdApplicationUntilProxyStarts

---

> 임시 참고 문서 — 정본은 나중에 따로 만듭니다.

파드가 뜰 때 애플리케이션 컨테이너가 Istio 프록시(`istio-proxy`)보다 먼저 준비되면 아웃바운드 요청이 실패합니다. 이 문서는 그 문제와 두 해법을 정리합니다. 하나는 Istio 설정 `holdApplicationUntilProxyStarts`, 다른 하나는 Kubernetes 네이티브 사이드카입니다. 종료 순서 쪽 설정은 문서로 확인된 것만 한 줄씩 적었습니다. 근거는 공식 문서이고 클러스터에서 재현하지는 않았습니다. 한계는 문서 끝에 적었습니다.

## 1. 앱이 프록시보다 먼저 뜨면 생기는 일

> 메시 안의 파드는 모든 네트워크 트래픽이 프록시를 거칩니다. 프록시가 준비되기 전에 앱이 요청을 보내면 그 요청은 나갈 길이 없습니다.

### 어떤 문제가 생기나

파드의 컨테이너들은 거의 동시에 시작합니다. 앱이 시작하자마자 설정 서버에 접속하거나 DB 연결 풀을 만들면, 그때 프록시가 아직 트래픽을 받을 준비가 안 돼 있어 연결이 거부됩니다. 앱이 재시도 없이 종료하면 파드가 `CrashLoopBackOff` 로 들어가고, 몇 번 재시작한 뒤에야 정상이 되기도 합니다. 재현은 되다 안 되다 하는 간헐 오류처럼 보여서 원인을 찾기 어렵습니다.

Istio 공식 블로그는 이 문제를 이렇게 적습니다.

> "If the application container starts faster than Istio's container, it cannot access the network."

같은 글은 반대 방향도 짚습니다. 종료할 때 프록시가 앱보다 먼저 내려가면 앱이 네트워크를 쓰지 못하고, 앱이 먼저 끝나는 `Job` 에서는 프록시가 남아 파드가 끝나지 않습니다. initContainer 는 프록시보다 먼저 실행되므로 네트워크를 쓸 수 없다는 점도 같은 글이 적습니다.

### 동작 원리

해법의 한쪽은 Istio 가 파드 시작 순서를 앱 쪽에서 막는 것입니다. `holdApplicationUntilProxyStarts` 를 켜면 프록시가 트래픽을 받을 준비가 될 때까지 앱 컨테이너 시작을 미룹니다. 공식 설정 문서는 이렇게 설명합니다.

> "Boolean flag for enabling/disabling the holdApplicationUntilProxyStarts behavior."

> "This feature adds hooks to delay application startup until the pod proxy is ready to accept traffic"

기본값은 `false` 입니다. 문서가 구현 방식을 설명하는 문장은 위 두 줄이 전부이고, 훅이 구체적으로 어떻게 붙는지는 열어 본 문서에 없었습니다.

다른 한쪽은 Kubernetes 가 순서를 보장하게 하는 것입니다. 네이티브 사이드카는 `restartPolicy: Always` 를 가진 initContainer 입니다. Kubernetes 문서는 이렇게 정의합니다.

> "Kubernetes implements sidecar containers as a special case of init containers; sidecar containers remain running after Pod startup."

init 컨테이너의 순서 보장이 그대로 적용되므로, 사이드카가 시작(`started`)된 뒤에야 다음 init 컨테이너와 일반 컨테이너가 시작됩니다. 이 상태는 프로세스가 돌고 있거나, `startupProbe` 가 있으면 그것이 성공했을 때 참이 됩니다. 종료는 반대입니다.

> "Upon Pod termination, the kubelet postpones terminating sidecar containers until the main application container has fully stopped."

Istio 가 이 기능을 쓰면 `istio-proxy` 는 `containers` 가 아니라 `initContainers` 에 나타납니다. Istio 블로그는 그것이 "an `initContainer` with `restartPolicy: Always` set" 이라고 설명합니다.

그 결과가 세 가지입니다. 프록시가 준비된 뒤에 다른 init 컨테이너가 돕니다. 앱이 끝난 뒤에 프록시가 내려갑니다. `Job` 도 앱이 끝나면 파드가 끝납니다.

### 최소 예제

메시 전체에 켜는 방법은 `meshConfig.defaultConfig` 입니다.

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    defaultConfig:
      holdApplicationUntilProxyStarts: true
```

파드 하나에만 켜려면 파드 템플릿에 annotation `proxy.istio.io/config` 를 씁니다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client
spec:
  replicas: 1
  selector:
    matchLabels: { app: client }
  template:
    metadata:
      labels: { app: client }
      annotations:
        proxy.istio.io/config: |
          holdApplicationUntilProxyStarts: true
    spec:
      containers:
      - name: app
        image: example/client:1.0
```

공식 문서는 두 설정이 겹칠 때의 규칙을 적습니다.

> "If both are configured, the two are merged with per field semantics; the field set in annotation will fully replace the field from mesh config defaults."

네이티브 사이드카는 istiod 환경 변수 `ENABLE_NATIVE_SIDECARS` 로 제어합니다. 레퍼런스에 따르면 기본값은 `auto` 이고, `true` 는 무조건 켜고 `false` 는 무조건 끄며 `auto` 는 지원되는 경우에 자동으로 켭니다.

```bash
istioctl install --set values.pilot.env.ENABLE_NATIVE_SIDECARS=true
```

### 흔한 함정

- annotation 은 파드가 만들어질 때 한 번 적용됩니다. 문서는 프록시 설정이 주입 과정에서 한 번 적용되고 파드 수명 동안 유지된다고 적습니다. 켠 뒤에는 파드를 다시 만들어야 반영됩니다.
- annotation 에서 지정한 필드는 메시 기본값의 같은 필드를 통째로 대체합니다. 필드 단위로 병합되므로 다른 필드는 기본값이 그대로 남습니다.
- 훅 방식(`holdApplicationUntilProxyStarts`)은 시작만 다루고, 네이티브 방식은 시작·종료·`Job` 종료·initContainer 네트워크를 모두 다룹니다. 증상이 시작 순서뿐인지 먼저 가립니다.
- Istio 블로그의 네이티브 사이드카 글은 `SidecarContainers` 가 알파이던 시기에 쓰였습니다. 현재 상태는 Kubernetes 문서와 Istio 레퍼런스(기본 `auto`)로 확인합니다.

### 공식 문서 근거

- [MeshConfig 레퍼런스](https://istio.io/v1.27/docs/reference/config/istio.mesh.v1alpha1/): `holdApplicationUntilProxyStarts` 의 형식(BoolValue)·기본값(false)·설명, `proxy.istio.io/config` 병합 규칙.
- [Istio 블로그: native sidecars](https://istio.io/v1.27/blog/2023/native-sidecars/): 시작·종료 문제 네 가지와 `ENABLE_NATIVE_SIDECARS` 사용법.
- [Kubernetes sidecar containers](https://v1-36.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/): 정의와 종료 순서. 문서 표기는 v1.28 최초 제공, v1.29 부터 기본 활성, v1.33 부터 안정입니다.
- [pilot-discovery 레퍼런스](https://istio.io/v1.27/docs/reference/commands/pilot-discovery/): `ENABLE_NATIVE_SIDECARS` 기본값 `auto`.



## 2. 종료 쪽 설정

> 종료 순서는 시작과 짝입니다. 프록시가 요청을 다 처리하기 전에 내려가면 진행 중인 연결이 끊깁니다.

### 어떤 문제가 생기나

앱은 SIGTERM 을 받은 뒤에도 마무리 요청을 보냅니다. 그때 프록시가 이미 내려가 있으면 마무리 요청이 실패하고, 반대로 프록시가 너무 오래 남으면 파드 종료가 지연됩니다.

### 동작 원리

문서로 확인된 설정은 둘입니다.

- `terminationDrainDuration` 은 프록시 종료 때 연결이 끝나도록 허용하는 시간입니다. SIGTERM 이나 SIGINT 를 받으면 `istio-agent` 가 활성 Envoy 에게 우아하게 비우기(draining)를 시작시킵니다. 설정하지 않으면 기본 5초가 적용됩니다.
- 환경 변수 `EXIT_ON_ZERO_ACTIVE_CONNECTIONS` 는 불리언이고 기본값은 `false` 입니다. 문서 설명은 "When set to true, terminates proxy when number of active connections become zero during draining" 입니다.

함께 나오는 `MINIMUM_DRAIN_DURATION`(기본 5초)은 에이전트가 활성 연결을 확인하기 전에 기다리는 최소 시간입니다.

### 최소 예제

```yaml
meshConfig:
  defaultConfig:
    terminationDrainDuration: 30s
```

환경 변수는 파드 annotation 이나 주입 설정으로 프록시 컨테이너에 전달합니다. 전달 방법은 열어 본 문서에서 확인하지 못했습니다.

### 흔한 함정

- `terminationDrainDuration` 이 파드의 `terminationGracePeriodSeconds` 보다 길면 그 시간을 다 쓰지 못하고 강제 종료됩니다. 두 값을 같이 봅니다. 이 관계는 열어 본 Istio 문서의 문장이 아니라 Kubernetes 종료 동작에서 나온 추론입니다.
- `EXIT_ON_ZERO_ACTIVE_CONNECTIONS` 를 켜면 연결이 0 이 되는 즉시 프록시가 끝납니다. `MINIMUM_DRAIN_DURATION` 이 그 확인 시작 시점을 정합니다.

### 공식 문서 근거

- [MeshConfig 레퍼런스](https://istio.io/v1.27/docs/reference/config/istio.mesh.v1alpha1/): `terminationDrainDuration` 정의와 기본 5초.
- [pilot-agent 레퍼런스](https://istio.io/v1.27/docs/reference/commands/pilot-agent/): `EXIT_ON_ZERO_ACTIVE_CONNECTIONS` (Boolean, 기본 false)와 `MINIMUM_DRAIN_DURATION` (기본 5s).



## 확인하지 못한 것

- 클러스터에서 재현하지 않았습니다. YAML 은 문법만 확인했습니다.
- `holdApplicationUntilProxyStarts` 가 훅을 구체적으로 어떻게 붙이는지(어떤 컨테이너에 어떤 lifecycle 훅인지)는 열어 본 레퍼런스에 없었습니다.
- Istio 공식 문서의 트러블슈팅 페이지(`ops/common-problems/network-issues`)와 사이드카 주입 페이지에는 이 설정 설명이 없었습니다. MeshConfig 레퍼런스가 유일한 설명이었습니다.
- Istio 버전별로 `ENABLE_NATIVE_SIDECARS=auto` 가 실제로 켜지는 조건(Kubernetes 버전·주입 방식)은 확인하지 못했습니다. 블로그 글은 Istio 1.19 시험판과 알파 시기 기준입니다.
- `EXIT_ON_ZERO_ACTIVE_CONNECTIONS` 를 파드에 전달하는 정확한 방법과 `terminationGracePeriodSeconds` 와의 관계는 문서에서 확인하지 못했습니다.
- 훅 방식과 네이티브 방식을 함께 켰을 때의 상호작용은 열어 본 문서에 없었습니다.
- Kubernetes 문서의 `restartPolicy: Always` 사이드카는 "sidecar 가 먼저 시작" 한다고 직접 서술한 문장이 열어 본 범위에 없었고, init 컨테이너 순서 보장 문장에서 이끌어 낸 설명입니다.



## 관련 문서

- 같은 주제로 이미 있는 write/ 문서는 찾지 못했습니다. [사이드카를 이루는 넷과 VM 이 받는 다섯 파일](../../08_cloud/book/istio-in-action/a0-02.부록%20—%20사이드카를%20이루는%20넷과%20VM%20이%20받는%20다섯%20파일.md) 이 사이드카 구성을 다룹니다.
