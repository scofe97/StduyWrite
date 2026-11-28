---
title: pause 컨테이너·Pod 샌드박스
tags: [kubernetes, pause, pod-sandbox, cri, namespace, pid1, shareprocessnamespace]
status: draft
source:
  - https://kubernetes.io/docs/concepts/workloads/pods/
  - https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/
  - https://github.com/kubernetes/kubernetes/blob/82ac28cc529c287e0f7e62d44a24ac714e6f42ee/build/pause/linux/pause.c
  - https://github.com/kubernetes/cri-api/blob/ea3944ec8a70f142f5a8a9518a031d56cde530d6/pkg/apis/runtime/v1/api.proto
  - https://github.com/containerd/containerd/blob/v2.2.0/internal/cri/server/sandbox_run.go
  - https://github.com/containerd/containerd/blob/v2.2.0/pkg/netns/netns_linux.go
  - https://man7.org/linux/man-pages/man7/pid_namespaces.7.html
  - https://man7.org/linux/man-pages/man7/namespaces.7.html
  - https://man7.org/linux/man-pages/man5/proc_pid_status.5.html
  - https://github.com/krallin/tini/blob/master/README.md
  - https://github.com/Yelp/dumb-init/blob/master/README.md
related:
  - ./%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md
  - ../../../book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md
  - ../../../../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md
  - ../../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md
  - ../README.md
allow:
  - "10.244.0.5"  # kind 로컬 pause-lab 클러스터 pod-isolated Pod IP (사내 IP 아님)
  - "10.244.0.6"  # kind 로컬 pause-lab 클러스터 pod-shared Pod IP (사내 IP 아님)
updated: 2026-11-28
---

# pause 컨테이너·Pod 샌드박스

---

> 쿠버네티스는 파드마다 숨은 인프라 컨테이너 `pause` 를 먼저 띄워 `ipc`·`uts`(켜면 `pid`) 네임스페이스의 기준점이자 샌드박스의 신원으로 삼습니다. `shareProcessNamespace: true` 를 켜면 `pause` 가 파드 공용 PID 1 까지 겸해 고아 좀비만 회수하지만, 앱으로 `SIGTERM` 을 넘기지는 않습니다.

## 학습 목표

> 이 문서를 읽고 나면 `pause` 컨테이너의 생성 흐름과 시그널 한계를 설명하고 노드에서 직접 네임스페이스 공유를 검증할 수 있습니다.

1. 앱 컨테이너가 재시작돼도 파드 IP 와 네트워크 네임스페이스가 유지되는 이유를 샌드박스 수명으로 설명합니다.
2. kubelet 에서 CRI `RunPodSandbox`·`CreateContainer`·`StartContainer` 로 이어지는 순서를 짚습니다.
3. `kubectl` 과 `crictl ps` 에 `pause` 가 빠지고 `crictl pods` 와 `ctr` 에만 보이는 이유를 가릅니다.
4. `pause.c` 가 하는 좀비 회수와 하지 않는 `SIGTERM` 전달을 `tini`·`dumb-init` 과 비교합니다.
5. 노드에서 `crictl inspectp` 와 `/proc/<PID>/ns/*`, `/proc/<PID>/status` 를 읽어 `NSpid`·`SigCgt` 를 검증합니다.

이 문서는 리눅스 네임스페이스 공유와 CRI 샌드박스 동작에 집중합니다. `crictl`·`ctr`·`nerdctl` 도구의 비교는 [컨테이너 런타임 인터페이스·crictl](./%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) 에 위임합니다.



## 1. 파드가 앱 하나만 띄우지 않는 이유

> 앱 컨테이너가 죽어 다시 떠도 파드 IP 와 `localhost` 통신 환경은 사라지지 않아야 하므로, 컨테이너와 수명이 분리된 샌드박스 `pause` 가 `ipc`·`uts` 의 기준점이자 파드의 신원이 됩니다.

파드 안의 유일한 앱 컨테이너가 OOMKilled 로 종료되면 리눅스 커널은 그 프로세스를 즉시 거둡니다. `ipc`·`uts` 네임스페이스가 앱 프로세스에만 매여 있다면 그 순간 함께 사라지고, 같은 파드의 다른 컨테이너가 쓰던 공유 상태도 끊깁니다.

리눅스 커널에는 "Pod" 라는 단위가 따로 없고, 프로세스 격리는 네임스페이스로 이뤄집니다.[^man-ns] 쿠버네티스는 파드를 네트워크와 스토리지 자원을 함께 쓰는 논리적 호스트로 정의합니다.[^k8s-pods]

한 파드의 여러 컨테이너는 같은 IP 와 `localhost` 포트 공간을 공유해야 합니다. 앱 컨테이너 하나가 재시작될 때마다 다른 컨테이너의 네트워크나 IPC 가 끊기면 논리적 호스트 모델이 무너집니다.

이를 막기 위해 런타임은 파드마다 가벼운 **앵커 프로세스**를 먼저 띄웁니다. 이것이 **Pod 샌드박스** 를 유지하는 **pause 컨테이너**입니다.

`pause` 는 `ipc` 와 `uts` 를 쥐고 파드 수명 동안 남습니다. 켜면 `pid` 도 쥡니다. 그래서 앱 컨테이너가 오가도 같은 네임스페이스에 합류할 수 있습니다.

네트워크 네임스페이스는 `pause` 가 쥐지 않습니다. containerd 가 `/var/run/netns/cni-...` 에 bind mount 로 먼저 고정하고, `pause` 와 앱 컨테이너가 거기에 합류합니다. 순서는 2절에서 봅니다.

실제로 kind v1.35 노드(`pause-lab`)에서 이 동작을 확인했습니다. `app` 과 `sidecar` 를 담은 `pod-isolated` 파드에서 `app`(`java`)을 강제 종료해 재시작(`RESTARTS 1`)시켰습니다. 그래도 `pause` 의 호스트 PID(`1959`)와 파드 IP(`10.244.0.5`), `net:[4026533298]` 은 그대로 남았습니다.

```bash
# 앱 강제 종료 후 재시작된 파드 상태 확인
kubectl get pod pod-isolated -o wide

# 재시작 전후 pause 와 app 의 호스트 PID 비교 (변수에는 crictl 로 얻은 컨테이너 ID 와 info.pid 를 담아 둠)
echo "BEFORE: pause=$ISO_PAUSE_PID app_cid=$ISO_APP_CID app_pid=$ISO_APP_PID"
echo "AFTER:  pause=$ISO_PAUSE_PID_AFTER app_cid=$ISO_APP_CID_AFTER app_pid=$ISO_APP_PID_AFTER"
```

```bash
# 결과 (kind v1.35 pause-lab, NOMINATED NODE·READINESS GATES 열과 컨테이너 ID 뒷부분은 생략)
NAME           READY   STATUS    RESTARTS     AGE   IP           NODE
pod-isolated   2/2     Running   1 (4s ago)   8s    10.244.0.5   pause-lab-control-plane

BEFORE: pause=1959 app_cid=1e94e814e264... app_pid=1997
AFTER:  pause=1959 app_cid=a46dec70eff4... app_pid=2526
```

노드에서 `/proc/<PID>/ns` 를 조회해도 결과는 같습니다. 재시작 뒤 새 앱 프로세스(`PID 2526`)는 새 PID 네임스페이스(`pid:[4026533508]`)를 받았습니다. 반면 네트워크 네임스페이스는 `pause` 의 `net:[4026533298]` 에 다시 붙었습니다.

파드의 네트워크 수명주기와 ClusterIP 배선 해부는 [Service 5유형](../../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md#pause-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80-%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4-%EC%88%98%EB%AA%85) 에서 이어서 볼 수 있습니다.



## 2. 샌드박스 생성과 앱 컨테이너 합류

> `kubelet` 은 CRI `RunPodSandbox` 로 `pause` 컨테이너와 공용 네임스페이스를 먼저 연 뒤, `CreateContainer` 와 `StartContainer` 로 앱 컨테이너를 합류시킵니다.

`kubelet` 은 파드 매니페스트의 앱 컨테이너를 곧장 띄우지 않습니다. 먼저 CRI(Container Runtime Interface) gRPC 호출로 파드 수준의 격리 울타리부터 만듭니다.[^cri-proto]

![kubelet의 Pod 샌드박스 생성과 앱 컨테이너 합류](./_assets/pause%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7Pod%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4.sandbox-flow.svg)

위 시퀀스는 `pod-isolated` 실측값 기준으로 네 참여자 사이의 순서를 보여 줍니다. 파란 선은 `RunPodSandbox` 와 `CreateContainer` 호출입니다. 초록 박스는 `pause` 가 속한 공용 네임스페이스이고 주황 선은 `StartContainer` 실행입니다.

### CRI RPC 세 단계와 네임스페이스 모드

첫 단계에서 `kubelet` 은 `RunPodSandbox` RPC 를 호출합니다.[^cri-proto] containerd 는 먼저 네트워크 네임스페이스를 만들어 `/var/run/netns/cni-...` 에 bind mount 로 고정합니다.[^containerd-run] 이어 CNI 플러그인으로 IP 를 붙입니다. 그다음 `registry.k8s.io/pause:3.10` 으로 `/pause`(호스트 `PID 1959`)를 띄우고 이 경로를 넘깁니다.[^containerd-run] 아래 `ctr` 출력에서 `pause` 스펙의 `network` 항목에 이 경로가 이미 들어 있는 것이 그 흔적입니다.

`pause` 컨테이너와 함께 새로 만들어지는 공용 네임스페이스는 `ipc` 와 `uts` 이고, `net` 은 위에서 만든 네임스페이스에 합류합니다. 둘째 단계에서 `kubelet` 은 `CreateContainer` RPC 로 앱 컨테이너 생성을 요청합니다.[^cri-proto] containerd 는 요청의 `NamespaceOption` 값에 따라 OCI 스펙 `namespaces` 의 합류 경로를 정합니다.

파드 명세의 `shareProcessNamespace: true` 는 같은 파드 컨테이너가 `pause` 의 PID 네임스페이스를 함께 쓰게 하는 설정입니다. 기본값(`false`)일 때와 설정을 켰을 때의 `NamespaceMode` 차이는 아래 표와 같습니다.

| 네임스페이스 | 기본 `NamespaceMode` | `shareProcessNamespace: true` | 설명 |
|---|---|---|---|
| `network` | `POD` | `POD` | `pause` 의 `net` 네임스페이스 경로에 합류 |
| `ipc` | `POD` | `POD` | `pause` 의 `ipc` 네임스페이스 경로에 합류 |
| `pid` | `CONTAINER` | `POD` | 기본은 컨테이너마다 독립 생성, 켜면 `pause` 와 공유 |
| `uts` | (필드 없음) | (필드 없음) | `NamespaceOption` 에 `uts` 필드가 없습니다. 실측에서는 파드 안 `uts` inode 가 같았고 앱 스펙이 `pause` 의 `uts` 경로에 합류했습니다 |
| `mnt` | (필드 없음) | (필드 없음) | `NamespaceOption` 에 `mnt` 필드가 없습니다. 실측에서는 컨테이너마다 `mnt` inode 가 달라 이미지 루트 파일시스템으로 분리됩니다 |

CRI `api.proto` 의 `NamespaceOption.pid` 주석은 CRI 기본값이 `POD` 라고 적습니다.[^cri-proto] 하지만 kubelet 런타임 매니저는 `v1.PodSpec` 기본 정책에 맞춰 `pid` 를 `CONTAINER` 로 명시합니다.[^cri-proto] 셋째 단계인 `StartContainer` 가 호출되면 앱 프로세스(`java`)가 이 조합 위에서 실행됩니다.[^cri-proto]

노드에서 `ctr -n k8s.io containers info` 를 실행해 OCI 스펙을 열어 보면 이 차이가 그대로 드러납니다. 아래는 `pod-isolated` 의 샌드박스와 `pod-shared` 의 `app` 컨테이너를 조회한 결과입니다.

```bash
# pod-isolated 샌드박스(pause)의 OCI 네임스페이스 설정 조회
ctr -n k8s.io containers info 27f0a4528fa19... | jq '{ID, Image, Spec: {process: .Spec.process.args, namespaces: .Spec.linux.namespaces}}'

# pod-shared 앱 컨테이너가 합류한 pause 네임스페이스 경로 조회
ctr -n k8s.io containers info 611709562635e... | jq '{ID, Image, Spec: {process: .Spec.process.args, namespaces: .Spec.linux.namespaces}}'
```

```bash
# 결과 (pause-lab-control-plane 노드, jq 출력은 항목마다 한 줄로 접고 process 의 셸 스크립트는 앞부분을 줄여 적음)
{
  "ID": "27f0a4528fa194fc1969bfc336d3e7523224cdddb1f93ae98bee66b509fa4180",
  "Image": "registry.k8s.io/pause:3.10",
  "Spec": {
    "process": ["/pause"],
    "namespaces": [
      {"type": "pid"},
      {"type": "ipc"},
      {"type": "uts"},
      {"type": "mount"},
      {"type": "network", "path": "/var/run/netns/cni-2041763d-8a75-7d48-7cef-e68bfd1928ad"}
    ]
  }
}
{
  "ID": "611709562635edf7dcae9f03b4a7c729d9a255f3dda22eb185300f987036ec54",
  "Image": "docker.io/library/eclipse-temurin:21-jdk",
  "Spec": {
    "process": ["sh", "-c", "... exec java /tmp/App.java\n"],
    "namespaces": [
      {"type": "pid", "path": "/proc/1961/ns/pid"},
      {"type": "ipc", "path": "/proc/1961/ns/ipc"},
      {"type": "uts", "path": "/proc/1961/ns/uts"},
      {"type": "mount"},
      {"type": "network", "path": "/proc/1961/ns/net"},
      {"type": "cgroup"}
    ]
  }
}
```

아래쪽 `pod-shared` 앱 컨테이너의 `namespaces` 배열에는 `path` 가 채워져 있습니다. `pid`, `ipc`, `uts`, `network` 네 항목 모두 `pause` 의 `/proc/1961/ns/*` 를 가리킵니다. 반면 `mount` 와 `cgroup` 은 `path` 가 비어 있어 컨테이너마다 새로 생성됩니다.



## 3. kubectl과 k9s에 보이지 않는 이유

> `kubectl` 과 `k9s` 는 API 서버의 `Pod.spec.containers` 와 `status.containerStatuses` 만 읽으므로 노드 아래층 CRI 샌드박스인 `pause` 는 노출되지 않습니다.

파드 안에 컨테이너가 몇 개 도는지 보려고 `kubectl get pod` 나 `k9s` 를 열면 매니페스트에 적은 컨테이너만 나타납니다. `pause-lab` 에서 `app` 과 `sidecar` 두 개를 띄운 `pod-isolated` 를 조회해도 `READY` 는 `2/2` 입니다. `status.containerStatuses` 이름 목록에도 둘만 나옵니다.

```bash
# API 서버 관점의 파드와 컨테이너 목록 조회
kubectl get pods -o wide
kubectl get pod pod-isolated -o jsonpath='{.status.containerStatuses[*].name}{"\n"}'
```

```bash
# 결과 (pause-lab, NOMINATED NODE·READINESS GATES 열 생략)
NAME           READY   STATUS    RESTARTS   AGE   IP           NODE
pod-isolated   2/2     Running   0          3s    10.244.0.5   pause-lab-control-plane
pod-shared     2/2     Running   0          3s    10.244.0.6   pause-lab-control-plane

app sidecar
```

이 차이는 쿠버네티스 API 모델과 CRI 모델의 경계에서 생깁니다. API 서버의 `Pod` 리소스는 사용자가 선언한 워크로드 컨테이너만 관리합니다. `pause` 는 노드의 `kubelet` 이 CRI 샌드박스 구현을 위해 띄우는 인프라 프로세스라 API 서버 목록에 올라가지 않습니다.

노드 안으로 들어가면 계층마다 보이는 범위가 갈립니다. `crictl pods` 는 `ListPodSandbox` RPC 로 샌드박스만 보여 줍니다. 반면 `crictl ps` 는 `ListContainers` RPC 로 애플리케이션 컨테이너만 조회합니다.[^cri-proto] 두 명령과 `ctr -n k8s.io` 의 차이는 [컨테이너 런타임 인터페이스·crictl](./%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md#%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4%EC%99%80-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98-%EB%B6%84%EB%A6%AC-%EA%B4%80%EC%B8%A1) 에서 자세히 다룹니다.



## 4. PID 공유와 pause.c 동작

> `shareProcessNamespace: true` 를 켜면 `/pause` 가 파드 공용 PID 1 이 되어 고아 좀비를 회수하지만, `pause.c` 는 `SIGTERM` 을 다른 컨테이너로 전달하지는 않습니다.

앱 컨테이너가 남긴 자식 프로세스가 좀비로 쌓이거나, 디버깅 셸 없는 컨테이너를 조사하려면 다른 컨테이너의 프로세스를 봐야 할 때가 있습니다. 이때 `shareProcessNamespace` 설정을 켜면 PID 네임스페이스 경계와 `PID 1` 주체가 달라집니다.

![shareProcessNamespace 설정에 따른 PID 네임스페이스와 PID 1 차이](./_assets/pause%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7Pod%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4.pidns-compare.svg)

좌측 `pod-isolated` 는 `pause`, `java`, `sleep` 이 각자 독립된 `pid:[...]` 고리 안에서 모두 `PID 1` 로 돕니다. 우측 `pod-shared` 는 주황색 `pid:[4026533505]` 고리 하나를 함께 씁니다. 그 결과 `/pause` 만 `PID 1` 이 되고 `java` 는 `PID 7`, `sleep` 은 `PID 35` 가 됩니다.

### 기본 격리와 PID 네임스페이스 공유

기본값(`shareProcessNamespace: false`)에서는 컨테이너마다 `pid` 네임스페이스가 분리됩니다. 따라서 `pod-isolated` 의 `sidecar` 에서 `ps` 를 쳐도 자기 자신의 `sleep 3600` 만 보입니다.

`shareProcessNamespace: true` 를 켜면 같은 파드 안 컨테이너가 `pause` 의 PID 네임스페이스를 공유합니다.[^k8s-share-pid] 실제로 두 파드 안에서 `ps` 를 실행해 보면 차이가 바로 드러납니다.

```bash
# 기본 격리 파드와 PID 공유 파드 내부의 ps 비교
kubectl exec pod-isolated -c sidecar -- ps
kubectl exec pod-shared -c sidecar -- ps
```

```bash
# 결과 (pause-lab)
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
   11 root      0:00 ps

PID   USER     TIME  COMMAND
    1 65535     0:00 /pause
    7 root      0:01 java /tmp/App.java
   35 root      0:00 sleep 3600
   47 root      0:00 ps
```

쿠버네티스 공식 문서는 PID 네임스페이스를 공유할 때 따르는 트레이드오프를 세 가지로 짚습니다.[^k8s-share-pid]

- PID 1 상실: 앱이 `PID 1` 이 아니므로 [kill 명령](../../../../02_os/docs/cmd/process/kill%C2%B7pgrep%C2%B7killall.md)으로 `kill -HUP 1` 을 실행하면 앱 대신 `/pause` 로 신호가 갑니다.
- 프로세스 정보 노출: 다른 컨테이너 프로세스가 `/proc` 에 보여 인자나 환경변수 비밀을 일반 유닉스 권한만으로 보호해야 합니다.
- 파일시스템 열람: `/proc/<PID>/root` 링크로 다른 컨테이너의 파일시스템을 읽을 수 있어 디버깅은 쉽지만 격리는 약해집니다.

### pause.c의 시그널 처리와 좀비 회수

`/pause` 바이너리의 동작은 쿠버네티스 저장소의 `pause.c` 파일 68줄에 전부 들어 있습니다.[^pause-c] 핵심은 `sigdown`, `sigreap`, 그리고 `main` 의 무한 대기 루프 셋입니다.

아래 코드는 `pause.c` 에서 시그널 핸들러 등록과 대기 루프 핵심부만 추린 발췌입니다.

```c
// kubernetes/build/pause/linux/pause.c (커밋 82ac28cc52, 32~40행·55~65행 발췌)
static void sigdown(int signo) {
  psignal(signo, "Shutting down, got signal");
  exit(0);
}

static void sigreap(int signo) {
  while (waitpid(-1, NULL, WNOHANG) > 0)
    ;
}

// main() 내부
  if (sigaction(SIGINT, &(struct sigaction){.sa_handler = sigdown}, NULL) < 0)
    return 1;
  if (sigaction(SIGTERM, &(struct sigaction){.sa_handler = sigdown}, NULL) < 0)
    return 2;
  if (sigaction(SIGCHLD, &(struct sigaction){.sa_handler = sigreap,
                                             .sa_flags = SA_NOCLDSTOP},
                NULL) < 0)
    return 3;

  for (;;)
    pause();
```

`pause.c` 는 세 시그널에만 핸들러를 등록합니다.[^pause-c] `SIGINT` 와 `SIGTERM` 을 받으면 자기 자신이 종료(`sigdown`)합니다. `SIGCHLD` 를 받으면 `waitpid(-1, NULL, WNOHANG)` 를 반복해 입양된 고아 좀비만 거둡니다(`sigreap`).[^pause-c]

그 밖의 시간에는 `pause()` 시스템 콜로 시그널이 올 때까지 잠들어 있습니다.[^pause-c] 리눅스에서 부모가 먼저 끝난 고아 프로세스는 PID 네임스페이스의 `PID 1` 에게 입양됩니다. 따라서 `shareProcessNamespace: true` 환경에서 앱이 남긴 고아 좀비는 `/pause` 가 회수합니다.[^man-pidns]

### SIGTERM 미전달 문제와 init 도구 비교

여기서 흔한 오해가 생깁니다. `pause.c` 코드 어디에도 다른 프로세스에 시그널을 넘기는 `kill()` 호출은 없습니다.[^pause-c] `pause` 는 앱 컨테이너를 `fork()` 한 부모가 아니며, 다른 컨테이너의 PID 를 추적해 `SIGTERM` 을 전달하지도 않습니다.

따라서 Dockerfile 의 shell form(`/bin/sh -c`) 때문에 `SIGTERM` 이 JVM 에 닿지 않는 문제는 `shareProcessNamespace: true` 로 풀리지 않습니다. 파드가 내려갈 때 `kubelet` 은 `pause` 가 아니라 각 컨테이너의 엔트리포인트에 `SIGTERM` 을 보내기 때문입니다.

이 차이 때문에 `pause` 와 경량 init 도구인 `tini`, `dumb-init`, 그리고 `ENTRYPOINT` exec form 은 역할이 갈립니다.

| 방식 | PID 1 주체 | 고아 좀비 회수 | 앱으로 SIGTERM 전달 | 적합한 용도 |
|---|---|---|---|---|
| `ENTRYPOINT` exec form (`exec` 포함) | 앱(예: JVM) | 안 함 | 불필요(앱이 직접 수신) | 단일 프로세스 앱의 정상 종료 |
| `shareProcessNamespace: true` | `/pause` | 함(`SIGCHLD`→`waitpid`) | 안 함 | 사이드카 협업·외부 좀비 회수 |
| `tini` | `tini` | 함(`wait()`) | 함(단일 자식 프로세스)[^tini] | 좀비 회수와 시그널 전달 병행 |
| `dumb-init` | `dumb-init` | 함(`wait()`) | 함(자식 세션·프로세스 그룹 전체)[^dumb-init] | 셸 스크립트 하위 그룹까지 시그널 전달 |

`tini` 는 컨테이너 안에서 단일 자식을 직접 `spawn` 한 뒤 좀비 회수와 시그널 전달을 함께 맡습니다.[^tini] `dumb-init` 은 자식을 새 세션(`setsid`)의 루트로 띄워 받은 시그널을 프로세스 그룹 전체로 전달합니다.[^dumb-init]

컨테이너 안 PID 1 의 두 책임인 시그널 처리와 고아 회수의 상세는 [06-03. lifecycle hook과 Pod 생애주기 전체](../../../book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md#sigterm-%EC%B2%98%EB%A6%AC%EC%99%80-%EA%B3%A0%EC%95%84-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4-%ED%9A%8C%EC%88%98) 와 [Learning Modern Linux 06-01](../../../../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md#%EC%A0%81%EC%9A%A9-%EA%B4%80%EC%A0%90) 에서 이어집니다.



## 5. 노드에서 pause와 네임스페이스 관찰하기

> 노드에서 `crictl pods` → `crictl inspectp` (`info.pid`) → `crictl ps --pod` → `/proc/<PID>/ns/*` 와 `/proc/<PID>/status` 순서로 따라가면 네임스페이스 공유와 시그널 핸들러 등록 상태를 수치로 확정할 수 있습니다.

파드 종료가 30초씩 걸리거나 네임스페이스 공유가 의도대로 먹혔는지 헷갈릴 때는 로그만으로 원인을 찾기 어렵습니다. 노드 커널의 `/proc` 파일시스템을 직접 읽어야 합니다. 아래 절차는 `pause-lab` 노드에서 `pod-isolated` 와 `pod-shared` 를 대상으로 실행한 순서입니다.

### 1단계: crictl로 샌드박스와 컨테이너 PID 찾기

먼저 `crictl pods` 로 샌드박스 ID 를 찾습니다. 그다음 `crictl inspectp` 의 `info.pid` 로 `pause` 의 호스트 PID 를 얻습니다. 같은 샌드박스의 앱과 사이드카 PID 는 `crictl ps --pod` 뒤 `crictl inspect` 로 확인합니다.

```bash
# 샌드박스 ID 와 info.pid, 네임스페이스 옵션 조회
crictl pods --name 'pod-.*'
crictl inspectp 27f0a4528fa19... | jq '{pid: .info.pid, ip: .status.network.ip, namespaces: .status.linux.namespaces}'

# 샌드박스 소속 컨테이너 목록 조회
crictl ps --pod 27f0a4528fa19...
```

```bash
# 결과 (pause-lab-control-plane 노드, inspectp 의 usernsOptions 는 한 줄로 접어 적음)
POD ID              CREATED             STATE               NAME                NAMESPACE           ATTEMPT             RUNTIME
27f0a4528fa19       2 seconds ago       Ready               pod-isolated        default             0                   (default)
69c0fc8f4fec1       2 seconds ago       Ready               pod-shared          default             0                   (default)

{
  "pid": 1959,
  "ip": "10.244.0.5",
  "namespaces": {
    "options": {
      "ipc": "POD",
      "network": "POD",
      "pid": "CONTAINER",
      "targetId": "",
      "usernsOptions": {"gids": [], "mode": "NODE", "uids": []}
    }
  }
}

CONTAINER           IMAGE               CREATED             STATE               NAME                ATTEMPT             POD ID              POD                 NAMESPACE
ba96348181a59       b7c873bd97bdc       1 second ago        Running             sidecar             0                   27f0a4528fa19       pod-isolated        default
1e94e814e264c       63bb4b7fbcbd5       1 second ago        Running             app                 0                   27f0a4528fa19       pod-isolated        default
```

이 조회로 `pod-isolated` 의 호스트 PID 셋(`pause=1959`, `app=1997`, `sidecar=2089`)을 얻었습니다. 같은 방식으로 `pod-shared` 도 `pause=1961`, `app=2020`, `sidecar=2115` 를 확인했습니다. `pod-shared` 의 `crictl inspectp` 에서는 `namespaces.options.pid` 가 `"POD"` 로 찍혔습니다.

### 2단계: ns inode 비교

두 프로세스가 같은 네임스페이스에 속하면 `/proc/<PID>/ns/<유형>` 심볼릭 링크의 inode 번호가 같습니다.[^man-ns] 확보한 여섯 PID 에 대해 `net`, `ipc`, `uts`, `pid`, `mnt` 링크를 나란히 비교합니다.

```bash
# pod-isolated(1959, 1997, 2089) 와 pod-shared(1961, 2020, 2115) 의 네임스페이스 inode 비교
for p in 1959 1997 2089; do ls -l /proc/$p/ns/net /proc/$p/ns/ipc /proc/$p/ns/uts /proc/$p/ns/pid /proc/$p/ns/mnt; done
for p in 1961 2020 2115; do ls -l /proc/$p/ns/net /proc/$p/ns/ipc /proc/$p/ns/uts /proc/$p/ns/pid /proc/$p/ns/mnt; done
```

```bash
# 결과 요약 (여섯 프로세스의 ls -l 출력에서 inode 만 뽑아 정리)
pod-isolated (shareProcessNamespace: false)
  pause   (1959): ipc:[4026533500]  net:[4026533298]  uts:[4026533499]  pid:[4026533501]  mnt:[4026533498]
  java    (1997): ipc:[4026533500]  net:[4026533298]  uts:[4026533499]  pid:[4026533507]  mnt:[4026533506]
  sleep   (2089): ipc:[4026533500]  net:[4026533298]  uts:[4026533499]  pid:[4026533512]  mnt:[4026533511]

pod-shared (shareProcessNamespace: true)
  pause   (1961): ipc:[4026533504]  net:[4026533396]  uts:[4026533503]  pid:[4026533505]  mnt:[4026533502]
  java    (2020): ipc:[4026533504]  net:[4026533396]  uts:[4026533503]  pid:[4026533505]  mnt:[4026533509]
  sleep   (2115): ipc:[4026533504]  net:[4026533396]  uts:[4026533503]  pid:[4026533505]  mnt:[4026533514]
```

두 파드 모두 `ipc`, `net`, `uts` 는 파드 안에서 일치하고 `mnt` 는 컨테이너마다 다릅니다. `pid` inode 만 `pod-isolated` 에서 셋(`3501`, `3507`, `3512`)으로 갈리고 `pod-shared` 에서 `4026533505` 하나로 합쳐졌습니다.

### 3단계: NSpid와 SigCgt 해석

`/proc/<PID>/status` 의 `NSpid` 는 바깥 PID 네임스페이스부터 안쪽 순서로 PID 를 나열합니다.[^man-proc] `SigCgt` 는 프로세스가 핸들러를 등록해 잡는 시그널을 16진 비트마스크로 나타냅니다.[^man-proc]

```bash
# pod-isolated 와 pod-shared 프로세스들의 NSpid 및 시그널 마스크 확인
for p in 1959 1997 2089 1961 2020 2115; do
  grep -E '^(Name|Pid|NSpid|SigBlk|SigIgn|SigCgt):' /proc/$p/status
done
```

```bash
# 결과 (Name·Pid·NSpid·SigCgt 만 한 줄로 발췌)
# pod-isolated
Name: pause   Pid: 1959   NSpid: 1959 1    SigCgt: 0000000000014002
Name: java    Pid: 1997   NSpid: 1997 1    SigCgt: 2000000101005ccf
Name: sleep   Pid: 2089   NSpid: 2089 1    SigCgt: 0000000000000000

# pod-shared
Name: pause   Pid: 1961   NSpid: 1961 1    SigCgt: 0000000000014002
Name: java    Pid: 2020   NSpid: 2020 7    SigCgt: 2000000101005ccf
Name: sleep   Pid: 2115   NSpid: 2115 35   SigCgt: 0000000000000000
```

`SigCgt` 비트마스크에서 1번 시그널은 `bit 0`(`2^(1-1)`)에 해당합니다. `pause` 의 `0x14002` 를 2진수로 풀면 세 비트가 켜져 있습니다.

| 프로세스 | `SigCgt` 16진수 | 켜진 핵심 시그널 비트 | `pause.c` 또는 런타임 대응 |
|---|---|---|---|
| `pause` | `0000000000014002` | `SIGINT`(2=`0x2`), `SIGTERM`(15=`0x4000`), `SIGCHLD`(17=`0x10000`) | `sigdown` 과 `sigreap` 핸들러 등록 결과 |
| `java` | `2000000101005ccf` | `SIGHUP`(1), `SIGINT`(2), `SIGTERM`(15) 켜짐 / `SIGCHLD`(17) 꺼짐 | shutdown hook 용 핸들러만 등록, `SIGCHLD` 핸들러 없음 |
| `sleep` | `0000000000000000` | 핸들러 없음 | PID 1 이면 상위 네임스페이스 `SIGTERM` 도 무시됨 |

`NSpid` 결과는 두 파드의 PID 격리 차이를 그대로 보여 줍니다. `pod-isolated` 에서는 세 프로세스 모두 마지막 열이 `1` 입니다. 반면 `pod-shared` 에서는 `pause` 만 `1961 1` 이고 `java` 는 `2020 7`, `sleep` 은 `2115 35` 입니다.

마지막으로 리눅스 PID 1 시그널 규약 하나를 덧붙입니다. `pod-isolated` 에서 `kubectl exec pod-isolated -c app -- sh -c 'kill -KILL 1'` 을 실행했을 때 `java` 는 죽지 않았습니다. 같은 PID 네임스페이스에서는 `init` 이 핸들러를 단 신호만 보낼 수 있고 `SIGKILL` 은 핸들러를 달 수 없기 때문입니다.[^man-pidns] 노드에서 `kill -KILL 1997` 을 보냈을 때만 종료됐습니다.



## 6. 관련 실습과 검증

> 공개 로컬 kind v1.35(`containerd 2.2.0`, `crictl 1.33.0`) 클러스터에서 `pod-isolated` 와 `pod-shared` 파드를 띄워 본문의 모든 출력과 도식 수치를 실측했습니다.

앞 절의 네임스페이스 inode 와 시그널 마스크 수치는 커널 실행 환경마다 달라지므로 공개 로컬 클러스터에서 직접 재현해 검증했습니다. 공개 이미지(`eclipse-temurin:21-jdk`, `busybox:1.36`, `registry.k8s.io/pause:3.10`)만 썼으며 실험 뒤 `pause-lab` 클러스터는 삭제했습니다.

- **실측 범위**: `kubectl get pods` 와 `crictl` 조회, `ctr` OCI 스펙, `/proc/<PID>/ns/*`, `/proc/<PID>/status` 를 직접 실행했습니다. 앱 강제 종료 후 `pause` PID 와 `net` 네임스페이스 유지 여부도 확인했습니다.
- **자료 대조 확인**: `tini` 와 `dumb-init` 의 동작, `pause.c` 와 CRI `api.proto` 인용은 각 공식 저장소의 코드와 문서를 직접 읽어 대조했습니다. `tini`·`dumb-init` 바이너리의 파드 내 단독 실행은 따로 측정하지 않았습니다.



## 관련 문서

> 파드 샌드박스, 런타임 관찰 도구, PID 1 시그널 처리를 함께 잇는 문서입니다.

- [컨테이너 런타임 인터페이스·crictl](./%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) — `crictl pods` 대 `crictl ps`, `ctr -n k8s.io` 와 CRI 소켓 구조 상세
- [06-03. lifecycle hook과 Pod 생애주기 전체](../../../book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) — `ENTRYPOINT` shell form 의 `SIGTERM` 미전달과 graceful shutdown 시간 예산
- [06-01. 먼저 켜지는 것 하나가 나머지 전부를 켠다](../../../../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) — 리눅스 PID 1 의 두 책임(데몬 시작·고아 회수)과 컨테이너 환경 적용
- [05-02. Service 5유형 — ClusterIP에서 LoadBalancer까지](../../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) — `pause` 컨테이너와 ClusterIP 네트워크 네임스페이스 수명주기
- [쿠버네티스 공식문서 정독 MOC](../README.md) — 아키텍처·스케줄링·운영·API 묶음 전체 목록



## 참고 자료

[^k8s-pods]: Kubernetes Documentation — Pods: "A Pod (as in a pod of whales or pea pod) is a group of one or more containers, with shared storage and network resources, and a specification for how to run the containers." / "A Pod models an application-specific \"logical host\": it contains one or more application containers which are relatively tightly coupled." <https://kubernetes.io/docs/concepts/workloads/pods/> (2026-11-28 조회)
[^k8s-share-pid]: Kubernetes Documentation — Share Process Namespace between Containers in a Pod: "When process namespace sharing is enabled, processes in a container are visible to all other containers in the same pod." / "In pods with a shared process namespace, kill -HUP 1 will signal the pod sandbox (/pause in the above example)." <https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/> (2026-11-28 조회)
[^pause-c]: Kubernetes `build/pause/linux/pause.c` (커밋 `82ac28cc529c287e0f7e62d44a24ac714e6f42ee`): 32~40행 `sigdown`·`sigreap(while (waitpid(-1, NULL, WNOHANG) > 0))`, 55~65행 `SIGINT`·`SIGTERM`·`SIGCHLD` 핸들러 등록 및 `for (;;) pause();`. <https://github.com/kubernetes/kubernetes/blob/82ac28cc529c287e0f7e62d44a24ac714e6f42ee/build/pause/linux/pause.c> (2026-11-28 조회)
[^cri-proto]: Kubernetes CRI `pkg/apis/runtime/v1/api.proto` (커밋 `ea3944ec8a70f142f5a8a9518a031d56cde530d6`): 30행 `RunPodSandbox`, 50행 `ListPodSandbox`, 66·68행 `CreateContainer`·`StartContainer`, 81행 `ListContainers`, 425~445행 `enum NamespaceMode { POD = 0; CONTAINER = 1; NODE = 2; TARGET = 3; }`, 473~502행 `NamespaceOption`(필드는 `network`·`pid`·`ipc`·`target_id`·`userns_options`·`cgroupns_options` 이고 `uts`·`mnt` 는 없음), 478~481행 "The CRI default is POD, but the v1.PodSpec default is CONTAINER. The kubelet's runtime manager will set this to CONTAINER explicitly for v1 pods." <https://github.com/kubernetes/cri-api/blob/ea3944ec8a70f142f5a8a9518a031d56cde530d6/pkg/apis/runtime/v1/api.proto> (2026-11-28 조회)
[^containerd-run]: containerd v2.2.0 `internal/cri/server/sandbox_run.go` 는 204행 `netns.NewNetNS(netnsMountDir)` 로 네임스페이스를 만들고, 261행 `setupPodNetwork` 로 CNI 를 부릅니다. 276행 `CreateSandbox`(`WithNetNSPath`)와 280행 `StartSandbox` 는 그 뒤에 옵니다. `pkg/netns/netns_linux.go` 124~127행은 이 네임스페이스를 `unix.Mount(..., MS_BIND, ...)` 로 고정하며 주석에 "persist, even when there are no threads in the ns" 라고 적습니다. <https://github.com/containerd/containerd/blob/v2.2.0/internal/cri/server/sandbox_run.go> · <https://github.com/containerd/containerd/blob/v2.2.0/pkg/netns/netns_linux.go> (2026-11-28 조회)
[^man-pidns]: Linux manual page `pid_namespaces(7)`: "Only signals for which the \"init\" process has established a signal handler can be sent to the \"init\" process by other members of the PID namespace." / "When a child process becomes orphaned, it is reparented to the \"init\" process in the PID namespace of its parent". <https://man7.org/linux/man-pages/man7/pid_namespaces.7.html> (2026-11-28 조회)
[^man-ns]: Linux manual page `namespaces(7)`: "A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the global resource." / "If two processes are in the same namespace, then the device IDs and inode numbers of their /proc/pid/ns/xxx symbolic links will be the same". <https://man7.org/linux/man-pages/man7/namespaces.7.html> (2026-11-28 조회)
[^man-proc]: Linux manual page `proc_pid_status(5)`: `NSpid` 항목 "Thread ID in each of the PID namespaces of which pid is a member. The fields are ordered as for NStgid." / `NStgid` 항목 "The leftmost entry shows the value with respect to the PID namespace of the process that mounted this procfs (or the root namespace if mounted by the kernel), followed by the value in successively nested inner namespaces." / `SigBlk`·`SigIgn`·`SigCgt` 항목 "Masks (expressed in hexadecimal) indicating signals being blocked, ignored, and caught (see signal(7))." <https://man7.org/linux/man-pages/man5/proc_pid_status.5.html> (2026-11-28 조회)
[^tini]: `krallin/tini` README: "All Tini does is spawn a single child (Tini is meant to be run in a container), and wait for it to exit all the while reaping zombies and performing signal forwarding." <https://github.com/krallin/tini/blob/master/README.md> (2026-11-28 조회)
[^dumb-init]: `Yelp/dumb-init` README: "dumb-init runs as PID 1, acting like a simple init system. It launches a single process and then proxies all received signals to a session rooted at that child process." <https://github.com/Yelp/dumb-init/blob/master/README.md> (2026-11-28 조회)
