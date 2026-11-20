---
title: API 서버 헬스 엔드포인트 — livez와 readyz는 무엇을 나눠 묻는가
tags: [kubernetes, kube-apiserver, health-check, livez, readyz, healthz, componentstatuses, kubeadm, probe]
status: draft
source:
  - https://kubernetes.io/docs/reference/using-api/health-checks/
  - https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/component-status-v1/
  - https://github.com/kubernetes/kubernetes/blob/v1.31.0/cmd/kubeadm/app/phases/controlplane/manifests.go
related:
  - ../operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md
  - ../../../book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md
updated: 2026-11-11
---

# API 서버 헬스 엔드포인트 — livez와 readyz는 무엇을 나눠 묻는가

---

> API 서버는 "다시 시작해야 하는가"와 "지금 요청을 받아도 되는가"를 서로 다른 엔드포인트로 답합니다. 둘을 구분해 읽어야 점검 결과가 실패일 때 재시작할지 기다릴지를 정할 수 있습니다.

## 학습 목표

> 이 문서를 읽고 나면 아래 네 가지를 스스로 해낼 수 있습니다.

1. `/livez` 와 `/readyz` 가 실패했을 때 각각 무엇을 뜻하는지 구분해 말할 수 있습니다.
2. `?verbose` 출력에서 실패한 검사 항목을 찾고, 그 항목만 따로 조회할 수 있습니다.
3. kubeadm 이 API 서버 static pod 의 세 probe 에 어느 엔드포인트를 거는지 설명할 수 있습니다.
4. `kubectl get componentstatuses` 대신 무엇을 써야 하는지와 그 근거를 말할 수 있습니다.

다루지 않는 범위가 있습니다. 컨테이너 probe 자체의 동작은 [liveness·startup probe로 컨테이너 건강 유지](../../../book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md)가 설명합니다. etcd 쪽 상태 판독은 [etcd 헬스와 유지보수](../operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md)가 맡습니다.



## 1. 떠 있음과 받을 수 있음

> 프로세스가 살아 있어도 요청을 처리하지 못하는 구간이 있고, 그 구간에 재시작은 답이 아닙니다.

API 서버가 막 기동했거나 etcd 연결이 잠시 끊긴 순간을 떠올려 봅니다. 프로세스는 떠 있고 포트도 열려 있습니다. 하지만 etcd 를 기다리는 중이거나 watch 캐시가 etcd 와 처음 동기화를 마치지 못했다면 요청을 제대로 처리하지 못합니다.[^health]

이때 점검자가 "API 서버가 응답하는가" 하나만 묻는다면 두 가지 실수가 생깁니다. 곧 회복될 서버를 재시작해 기동 시간을 다시 쓰게 만들거나, 반대로 교착에 빠진 서버를 "포트는 열려 있다"며 내버려 둡니다. 그래서 질문을 둘로 나눠야 합니다. 이 서버를 다시 시작해야 하는가, 그리고 지금 트래픽을 보내도 되는가입니다.



## 2. 세 엔드포인트가 나눠 맡는 것

> `/livez` 는 재시작 여부를, `/readyz` 는 트래픽 수용 여부를 답하고, `/healthz` 는 폐기됐습니다.

공식 문서는 두 질문을 엔드포인트 둘에 나눠 담았습니다.[^health]

| 엔드포인트 | 묻는 것 | 실패의 뜻 |
|---|---|---|
| `/livez` | 다시 시작해야 하는가 | 교착처럼 회복할 수 없는 상태일 가능성이 높아 재시작이 필요합니다 |
| `/readyz` | 지금 트래픽을 받아도 되는가 | 초기화 중이거나 잠시 요청을 처리할 수 없으니 트래픽을 다른 곳으로 돌립니다 |
| `/healthz` | (두 질문을 하나로) | v1.16 부터 폐기됐고, 대신 위 둘을 씁니다 |

`/readyz` 가 실패하는 예로 공식 문서는 두 가지를 듭니다. 하나는 etcd 를 쓸 수 있을 때까지 기다리는 경우이고, 다른 하나는 등록된 모든 watch 캐시가 etcd 와 첫 동기화를 마치기를 기다리는 경우입니다.[^health] 둘 다 시간이 지나면 풀리는 상태라서, 재시작보다 기다리는 편이 맞습니다.

기계가 이 엔드포인트를 검사할 때는 HTTP 상태 코드만 봅니다. `200` 이면 해당 엔드포인트의 질문에 "예"이고, `500` 같은 실패 코드면 "아니요"입니다.[^health] 응답 본문은 사람이 읽으라고 있는 것이지 파싱하라고 있는 것이 아닙니다.



## 3. verbose 로 실패 항목 찾기

> 상태 코드는 성공·실패만 알려 주므로, 원인을 좁힐 때는 `verbose` 를 붙여 검사 항목을 펼칩니다.

`/readyz` 가 실패했다는 사실만으로는 무엇을 기다리는지 알 수 없습니다. 사람이 원인을 볼 때는 `verbose` 쿼리를 붙입니다. 노드 안에서는 `curl` 로, 원격에서는 인증된 `kubectl` 로 조회합니다.[^health]

```bash
curl -k https://localhost:6443/livez?verbose
kubectl get --raw='/readyz?verbose'
```

출력은 검사 항목마다 한 줄씩 나오고 마지막 줄이 전체 판정입니다. 아래는 공식 문서 예시의 앞부분입니다.[^health]

```bash
[+]ping ok
[+]log ok
[+]etcd ok
[+]poststarthook/watch-cache-initialization ok
[+]poststarthook/start-kube-apiserver-admission-initializer ok
...
[+]autoregister-completion ok
[+]poststarthook/apiservice-openapi-controller ok
healthz check passed
```

`[+]` 와 `ok` 사이의 문자열이 검사 이름입니다. 이름에서 짐작할 수 있듯 `etcd` 는 저장소 연결을, `poststarthook/...` 는 기동 뒤에 도는 초기화 작업들을 봅니다. 실패한 항목이 있으면 그 줄에서 원인 영역이 좁혀집니다.

### 한 항목만 보거나 빼고 보기

검사 이름을 알면 경로에 붙여 그 항목만 조회할 수 있습니다. 형식은 `/livez/<검사 이름>` 또는 `/readyz/<검사 이름>` 입니다.[^health]

```bash
curl -k https://localhost:6443/livez/etcd
```

반대로 특정 항목을 빼고 나머지만 볼 수도 있습니다. `exclude` 를 `verbose` 와 함께 쓰면 뺀 항목은 `[+]etcd excluded: ok` 처럼 표시됩니다.[^health]

```bash
curl -k 'https://localhost:6443/readyz?verbose&exclude=etcd'
```

공식 문서는 개별 검사 경로를 기계가 쓰지 말고 사람이 디버깅할 때만 쓰라고 적습니다.[^health] 모니터링이나 probe 에는 `/livez`·`/readyz` 전체 판정을 겁니다.



## 4. kubeadm 이 거는 세 probe

> 같은 두 질문을 kubelet 도 probe 로 묻고, 그래서 `/livez` 실패는 컨테이너 재시작으로 이어집니다.

kubeadm 으로 만든 클러스터에서 API 서버는 static pod 로 뜹니다. kubeadm v1.31 소스는 이 Pod 의 probe 를 다음처럼 잡습니다.[^kubeadm]

| probe | 경로 | 실패하면 kubelet 이 하는 일 |
|---|---|---|
| liveness | `/livez` | 컨테이너를 재시작합니다 |
| startup | `/livez` | 기동이 끝날 때까지 liveness 검사를 미룹니다 |
| readiness | `/readyz` | Pod 를 준비되지 않음으로 표시합니다 |

오른쪽 열은 probe 일반의 동작이며 [liveness·startup probe로 컨테이너 건강 유지](../../../book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md)에 있습니다. 이 배치는 §2 의 구분과 맞아떨어집니다. 재시작 판단에는 `/livez` 를, 트래픽 판단에는 `/readyz` 를 씁니다.

점검에서 이 사실이 쓸모 있는 이유는 재시작 횟수와 이어지기 때문입니다. `kube-system` 의 `kube-apiserver-<노드>` Pod 재시작 횟수가 늘었다면 `/livez` 가 실패한 적이 있다는 뜻입니다. 반면 `READY` 가 `0/1` 인데 재시작이 없다면 `/readyz` 만 실패하는 중이니, `?verbose` 로 무엇을 기다리는지 먼저 봅니다.



## 5. componentstatuses 를 쓰지 않는 이유

> 예전에는 `kubectl get componentstatuses` 로 컨트롤 플레인을 한 번에 봤지만, 이 API 는 v1.19 부터 폐기됐습니다.

`kubectl get componentstatuses` 는 컨트롤 플레인 구성요소의 상태를 한 표로 보여 주던 명령입니다. scheduler, controller-manager, etcd 가 한 줄씩 나왔습니다. 『Kubernetes Up and Running』 3판도 클러스터가 대체로 건강한지 보는 간단한 진단으로 이 명령을 소개합니다. 하지만 공식 API 레퍼런스는 ComponentStatus 를 "v1.19+ 에서 폐기된 API" 로 표시합니다.[^cs]

폐기된 API 는 앞으로 결과를 믿을 근거가 약해지므로 점검 절차에 새로 넣지 않습니다. 같은 질문은 두 갈래로 나눠 답합니다.

- API 서버 자체: 이 문서의 `/livez`·`/readyz` 와 `?verbose`
- etcd: `etcdctl endpoint health`·`endpoint status` ([etcd 헬스와 유지보수](../operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md) §2)

scheduler 와 controller-manager 는 `kube-system` 에서 static pod 로 뜨므로 Pod 상태와 재시작 횟수로 봅니다. 공식 레퍼런스가 폐기 이유는 적지 않으므로 이유는 여기서 단정하지 않습니다.



## 6. 점검 질문

> 위 내용을 실제 점검 상황에 대 봅니다.

### Q1. readyz 만 실패할 때 재시작하는가

재시작하지 않고 먼저 `kubectl get --raw='/readyz?verbose'` 로 실패한 항목을 찾습니다. `/livez` 가 성공한다는 것은 재시작이 필요한 상태가 아니라는 뜻입니다. `etcd` 줄이 실패라면 etcd 쪽을, `poststarthook/...` 줄이라면 기동 뒤 초기화가 덜 끝난 것을 의심합니다.

### Q2. 모니터링에 개별 검사 경로를 거는가

권하지 않습니다. 공식 문서는 개별 검사 경로를 사람의 디버깅용으로 두고 기계가 쓰지 말라고 적었습니다. 모니터링에는 `/readyz` 전체 판정을 걸고, 실패했을 때 사람이 개별 경로로 내려갑니다.

### Q3. componentstatuses 결과를 근거로 쓰는가

남기더라도 판정 근거로 쓰지 않습니다. ComponentStatus 는 v1.19 부터 폐기된 API 입니다. 판정 근거는 `/readyz?verbose` 결과와 etcd 의 `endpoint health` 결과로 남깁니다.



## 관련 문서

> 같은 컨트롤 플레인 점검을 다른 쪽에서 다루는 문서입니다.

- [etcd 헬스와 유지보수](../operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md) — API 서버 `etcd` 검사가 실패할 때 내려가 볼 저장소 쪽 판독
- [liveness·startup probe로 컨테이너 건강 유지](../../../book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) — §4 의 probe 가 실패했을 때 kubelet 이 하는 일

[^health]: Kubernetes — Kubernetes API health endpoints. `/livez`·`/readyz`·`/healthz` 의 뜻, 상태 코드, `verbose`·`exclude`, 개별 검사 경로. <https://kubernetes.io/docs/reference/using-api/health-checks/>

[^cs]: Kubernetes API Reference — ComponentStatus v1. "Deprecated: This API is deprecated in v1.19+". <https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/component-status-v1/>

[^kubeadm]: kubernetes/kubernetes v1.31.0 — `cmd/kubeadm/app/phases/controlplane/manifests.go`. kube-apiserver static pod 의 LivenessProbe·StartupProbe 는 `/livez`, ReadinessProbe 는 `/readyz`. <https://github.com/kubernetes/kubernetes/blob/v1.31.0/cmd/kubeadm/app/phases/controlplane/manifests.go>
