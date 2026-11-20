---
title: Pod STATUS 열 계산 — phase 를 reason 이 덮어쓰는 순서
tags: [kubernetes, kubectl, pod-status, table, server-side-printing]
status: draft
source:
  - https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/printers/internalversion/printers.go
  - https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/registry/core/pod/storage/storage.go
  - https://github.com/kubernetes/website/blob/release-1.36/content/en/docs/concepts/workloads/pods/pod-lifecycle.md
related:
  - kubectl%20출력%20형식.md
  - ../operations/모니터링%20개요·트러블슈팅%20루틴.md
  - ../../../book/kubernetes-in-action/06-01.Pod%20상태%20—%20phase·conditions·컨테이너%20상태.md
updated: 2026-11-18
---

# Pod STATUS 열 계산 — phase 를 reason 이 덮어쓰는 순서

---

> `kubectl get pods` 의 STATUS 는 Pod 의 필드가 아니라 API 서버가 표를 만들 때 계산하는 값입니다. phase 에서 시작해 init 컨테이너와 컨테이너의 reason 이 차례로 덮어쓰므로, 문제가 있는 Pod 일수록 phase 와 다른 이름이 보입니다.

## 학습 목표와 범위

> STATUS 에 보이는 한 단어가 Pod 의 어느 필드에서 왔는지 거꾸로 짚습니다.

1. STATUS 값을 계산하는 쪽이 kubectl 이 아니라 API 서버임을 설명할 수 있습니다.
2. `Init:1/3`·`CrashLoopBackOff`·`Terminating` 같은 값이 Pod 의 어느 필드에서 왔는지 짚을 수 있습니다.
3. READY 와 RESTARTS 열이 무엇을 세는지 설명할 수 있습니다.

phase·conditions·컨테이너 state 가 각각 무엇인지는 [Pod 상태 — phase·conditions·컨테이너 상태](../../../book/kubernetes-in-action/06-01.Pod%20상태%20—%20phase·conditions·컨테이너%20상태.md)가 다룹니다. 이 문서는 그 값들이 표의 한 칸으로 줄어드는 순서만 봅니다. 기준은 쿠버네티스 v1.37.2 소스입니다.



## 1. 값을 계산하는 주체

> STATUS 는 저장된 값이 아니어서 `kubectl get pod -o yaml` 에는 없습니다. 표를 요청받은 API 서버가 그때그때 계산합니다.

Pod 오브젝트의 `status` 에는 `phase` 는 있어도 화면의 STATUS 에 해당하는 필드는 없습니다. 공식 문서도 STATUS 를 「사용자 직관을 위한 kubectl 표시 필드」라 부르고 phase 와 혼동하지 말라고 적습니다.[^lifecycle]

표시 필드라고 해서 kubectl 이 계산하지는 않습니다. `kubectl get` 의 기본 표는 API 서버가 만든 Table 응답이고, kubectl 은 받은 표를 그립니다([kubectl 출력 형식](kubectl%20출력%20형식.md#1-표를-그리는-주체)).

Pod 의 표 변환기는 API 서버의 Pod 저장소에 등록돼 있고, 한 줄을 만드는 함수가 `printPod` 입니다.[^convertor] 그래서 같은 클러스터에 붙으면 kubectl 버전이 달라도 같은 STATUS 를 봅니다.

열의 설명도 서버에 있습니다. STATUS 열은 「이 Pod 컨테이너들의 종합 상태」로 정의돼 있습니다.[^columns]



## 2. 값을 덮어쓰는 순서

> 뒤 단계가 앞 단계의 값을 덮어씁니다. 그래서 STATUS 에는 가장 늦게 적용된 규칙의 값이 남습니다.

STATUS 가 phase 와 다를 때는 어느 규칙이 마지막으로 값을 바꿨는지를 알아야 원인을 짚을 수 있습니다. `printPod` 는 변수 하나에 값을 넣고 아래 순서로 덮어씁니다.[^printpod]

| 순서 | 조건 | STATUS 에 들어가는 값 |
|---|---|---|
| 1 | 항상 | `status.phase`. `status.reason` 이 있으면 그 값 |
| 2 | `PodScheduled` condition 의 reason 이 `SchedulingGated` | `SchedulingGated` |
| 3 | 끝나지 않은 init 컨테이너가 있다 | `Init:` 으로 시작하는 값 |
| 4 | init 이 끝났다 | 컨테이너의 `Waiting`·`Terminated` reason |
| 5 | 4단계의 결과가 `Completed` | 돌고 있는 컨테이너가 있으면 `Running`·`NotReady` 등으로 보정 |
| 6 | 삭제 표시(`deletionTimestamp`)가 있다 | `Terminating` 또는 `Unknown` |

### init 컨테이너 단계

init 컨테이너는 선언 순서대로 봅니다. 종료 코드 0 으로 끝난 것과 이미 시작한 네이티브 사이드카는 건너뜁니다. 그렇지 않은 첫 컨테이너에서 값을 정하고 멈춥니다.[^printpod]

- **실패로 끝났다:** `Init:` 뒤에 종료 reason 을 붙입니다. reason 이 비었으면 `Init:Signal:N`, 신호도 없으면 `Init:ExitCode:N` 입니다.
- **기다리는 중이고 reason 이 있다:** `Init:` 뒤에 그 reason 을 붙입니다(`Init:ImagePullBackOff`·`Init:CrashLoopBackOff`). reason 이 `PodInitializing` 이면 이 규칙을 타지 않습니다.
- **그 밖(실행 중 등):** `Init:i/N` 입니다. `i` 는 이 컨테이너보다 앞에서 끝난 init 컨테이너 수이고 `N` 은 init 컨테이너 전체 수입니다.

### 컨테이너 단계

끝나지 않은 init 컨테이너가 없거나 `Initialized` condition 이 True 이면 주 컨테이너를 봅니다. 목록의 뒤에서 앞으로 훑으며 값을 덮어쓰므로, 문제가 있는 컨테이너가 여럿이면 선언 순서가 가장 앞인 것의 reason 이 남습니다.[^printpod]

- **`Waiting` 이고 reason 이 있다:** 그 reason 입니다(`ContainerCreating`·`CrashLoopBackOff`·`ErrImagePull`).
- **`Terminated` 이다:** 종료 reason 입니다(`Completed`·`Error`·`OOMKilled`). reason 이 비었으면 `Signal:N`, 신호도 없으면 `ExitCode:N` 입니다.
- **`Running` 이고 ready 다:** 값을 바꾸지 않습니다. READY 의 분자만 하나 올립니다.

모든 컨테이너가 ready 로 돌고 있으면 이 단계에서 아무것도 덮어쓰지 않아, 1단계의 phase(`Running`)가 그대로 남습니다.

### Completed 보정

컨테이너 하나가 정상 종료했어도 다른 컨테이너가 돌고 있으면 `Completed` 는 Pod 전체를 잘못 말합니다. 그래서 4단계의 결과가 `Completed` 일 때만 다시 고칩니다.[^printpod]

- 돌고 있는 ready 컨테이너가 있고 Pod 의 `Ready` condition 이 True 이면 `Running` 입니다.
- 그렇지 않고 종료 코드가 0 이 아닌 컨테이너가 있으면 그 컨테이너의 reason 입니다.
- 둘 다 아니고 돌고 있는 ready 컨테이너가 있으면 `NotReady` 입니다.

### 삭제 중인 Pod

삭제 표시가 있으면 앞의 값을 모두 덮어씁니다.[^printpod]

- Pod 의 `status.reason` 이 `NodeLost` 이면 `Unknown` 입니다. `NodeLost` 는 노드의 kubelet 이 응답하지 않아 Pod 상태를 확인할 수 없을 때 붙는 reason 입니다.[^nodelost]
- 그렇지 않고 phase 가 `Succeeded`·`Failed` 가 아니면 `Terminating` 입니다.

`Terminating` 과 `Unknown` 은 이렇게 표에서만 만들어지는 이름이라, 컨테이너 state 나 reason 에서는 찾을 수 없습니다.



## 3. READY 와 RESTARTS 열

> 두 열도 같은 함수가 같은 훑기에서 셉니다. 분모와 합계에 네이티브 사이드카가 들어간다는 점이 눈으로 센 값과 달라지는 곳입니다.

- **READY:** `ready 인 컨테이너 수/전체 수` 입니다. 전체 수는 `spec.containers` 의 개수에 네이티브 사이드카(재시작 가능한 init 컨테이너)를 더한 값입니다. 일반 init 컨테이너는 세지 않습니다.[^printpod]
- **RESTARTS:** init 이 끝난 뒤에는 주 컨테이너와 네이티브 사이드카의 `restartCount` 합입니다. init 중에는 init 컨테이너의 합입니다. 0 이 아니면 마지막 재시작이 얼마 전인지를 괄호로 붙입니다.[^printpod]



## 4. STATUS 만 보고 판단할 수 없는 것

> STATUS 는 한 칸이라 컨테이너 하나의 reason 만 남습니다. 나머지는 Pod 의 필드를 직접 읽어야 보입니다.

- **phase:** STATUS 가 `CrashLoopBackOff` 여도 phase 는 `Running` 일 수 있습니다. 스크립트에서 상태를 가를 때는 STATUS 문자열이 아니라 `status.phase` 와 conditions 를 읽습니다.
- **다른 컨테이너의 reason:** 컨테이너 둘이 다른 이유로 실패하면 선언 순서가 앞인 쪽만 보입니다. 전체는 `kubectl describe pod` 나 `status.containerStatuses` 에 있습니다.
- **Ready 여부:** STATUS 가 `Running` 이어도 READY 가 `1/2` 이면 Service 는 이 Pod 로 트래픽을 보내지 않습니다. STATUS 와 READY 를 함께 봅니다.



## 관련 문서

> 표를 만드는 쪽과 그 표가 줄여 보여 주는 원래 값을 다루는 문서입니다.

- [kubectl 출력 형식](kubectl%20출력%20형식.md) — 기본 표와 `-o wide` 가 서버의 Table 응답이라는 점과 열 우선순위
- [Pod 상태 — phase·conditions·컨테이너 상태](../../../book/kubernetes-in-action/06-01.Pod%20상태%20—%20phase·conditions·컨테이너%20상태.md) — STATUS 가 줄여 보여 주는 세 층의 값
- [모니터링 개요와 트러블슈팅 루틴](../operations/모니터링%20개요·트러블슈팅%20루틴.md) — STATUS 를 본 다음에 치는 진단 명령의 순서

[^lifecycle]: Kubernetes website `release-1.36` — Pod Lifecycle. "Make sure not to confuse _Status_, a kubectl display field for user intuition, with the pod's `phase`." <https://github.com/kubernetes/website/blob/release-1.36/content/en/docs/concepts/workloads/pods/pod-lifecycle.md> (2026-11-18 확인)

[^convertor]: kubernetes/kubernetes `v1.37.2` — `pkg/registry/core/pod/storage/storage.go`. "`TableConvertor: printerstorage.TableConvertor{TableGenerator: printers.NewTableGenerator().With(printersinternal.AddHandlers)}`" <https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/registry/core/pod/storage/storage.go> (2026-11-18 확인)

[^columns]: kubernetes/kubernetes `v1.37.2` — `pkg/printers/internalversion/printers.go` 의 Pod 열 정의. "`{Name: "Status", Type: "string", Description: "The aggregate status of the containers in this pod."}`" <https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/printers/internalversion/printers.go> (2026-11-18 확인)

[^printpod]: kubernetes/kubernetes `v1.37.2` — `pkg/printers/internalversion/printers.go` 의 `printPod`. `reason := string(podPhase)` 로 시작해 `pod.Status.Reason`, `SchedulingGated`, init 컨테이너(`Init:%d/%d`·`"Init:" + …`·`Init:Signal:%d`·`Init:ExitCode:%d`), 컨테이너의 `Waiting.Reason`·`Terminated.Reason`(`Signal:%d`·`ExitCode:%d`), `if reason == "Completed"` 보정, `pod.DeletionTimestamp != nil` 분기 순으로 덮어씁니다. READY 는 `fmt.Sprintf("%d/%d", readyContainers, totalContainers)` 입니다. <https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/printers/internalversion/printers.go> (2026-11-18 확인)

[^nodelost]: kubernetes/kubernetes `v1.37.2` — `pkg/util/node/node.go`. "NodeUnreachablePodReason is the reason on a pod when its state cannot be confirmed as kubelet is unresponsive on the node it is (was) running." 값은 `"NodeLost"` 입니다. <https://github.com/kubernetes/kubernetes/blob/v1.37.2/pkg/util/node/node.go> (2026-11-18 확인)
