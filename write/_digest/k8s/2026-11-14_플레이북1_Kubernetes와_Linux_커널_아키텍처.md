# Kubernetes와 Linux 커널 아키텍처 분석 — AI 요약

> 출처: Gemini · 2026-11-14 · [플레이북] 1. Kubernetes와 Linux 커널 아키텍처 분석 · 분야: k8s-keywords · 미검증

## 요점

한 줄: 쿠버네티스는 목표 상태를 선언·조정할 뿐이고 실제 격리·자원 통제는 커널(cgroups·OOM Killer·CFS)이 집행하므로, 쓰로틀링·종료 코드 137 같은 증상은 커널 지표로 본다는 내용입니다.

- `kubelet` → CRI(gRPC) → `containerd` → OCI → `runc` 로 이어지며, 커널의 namespaces·OverlayFS·veth 로 컨테이너가 조립되고 cgroups 에 상한이 기록됨. 물리적 통제권은 커널에 있음
- `limits.memory` 는 `memory.max` 로 기록되고, 넘으면 커널 OOM Killer 가 `SIGKILL(9)` 로 정리 기회 없이 종료함. 종료 코드 137(128+9)
- OOM 경로는 둘: 컨테이너 cgroup 상한 초과와 노드 전체 메모리 고갈. 노드 고갈 때는 `oom_score` 가 높은 Pod 부터 희생되고, QoS 는 `oom_score_adj` 로 그 점수를 조정함
- OOMKilled 를 limit 증설로 덮지 않고 노드 `dmesg -T` 와 런타임 힙 설정(예: JVM 힙과 cgroup 상한 불일치)을 먼저 봄
- 같은 컨테이너가 반복 종료되면 `CrashLoopBackOff`. 재시작 대기를 10초부터 두 배씩 늘려 최대 5분에서 멈춤
- `limits.cpu: 50m` 은 `cpu.max` 에 `5000 100000` 으로 기록됨. 1코어를 다 쓰려는 프로세스면 100ms 주기마다 5ms 만 실행하고 나머지 95ms 는 강제 대기(throttling)
- `kubectl top` 은 평균만 보여 throttling 빈도를 숨김. 멀티스레드 앱은 쿼터를 몇 ms 만에 써 버려 P99 지연이 치솟으므로 `cpu.stat` 의 `nr_throttled / nr_periods` 와 `throttled_usec` 를 봄
- 노드 진단 경로는 `crictl ps` → `crictl inspect`(호스트 PID) → `/proc/<PID>/cgroup` → `cpu.max`·`cpu.stat` 순서임. 노드가 많으면 cAdvisor 지표의 throttling 비율을 PromQL 로 경보함
- CPU 는 압축 가능 자원이라 넘으면 느려지고, 메모리는 압축 불가 자원이라 넘으면 죽음. CPU limits 를 걸지 requests 만 걸지는 지연 민감도와 노이즈 이웃 격리 요구로 정함
- 자가 치유는 개별 컨테이너 종료만 복구하고 트래픽 폭증형 연쇄 장애(Cascade Failure)는 못 막음. Ingress Rate Limiting(429), Circuit Breaker, HPA, 자원 산정을 함께 설계함
- VM(AWS Nitro)은 컨테이너 탈출을 막는 하드웨어 경계, 컨테이너는 빠른 기동·고밀도를 맡음. 그 사이에 MicroVM(Firecracker·Kata), 초저지연·GPU 학습에는 Bare Metal + 컨테이너



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
|---|---|---|
| Linux Namespaces | PID·네트워크·마운트 등 시스템 자원의 가시성을 프로세스별로 논리 격리하는 커널 기능 | [namespace와 루트 디렉토리](../../08_cloud/book/container-security/04-01.namespace와 루트 디렉토리 — 격리를 만드는 두 장치.md) |
| cgroups v2 | CPU·메모리·I/O 하드웨어 자원의 상한을 프로세스 그룹 단위로 제한·계측 | [네임스페이스와 cgroup으로 보는 컨테이너 격리](../../08_cloud/book/kubernetes-in-action/02-03.네임스페이스와 cgroup으로 보는 컨테이너 격리.md) · [cgroup v2](../../02_os/docs/kernel/01-01.cgroup v2.md) |
| OOM Killer & Exit Code 137 | cgroup memory.max 초과 시 oom_score 기반으로 SIGKILL(9)을 전송해 즉시 강제 종료 (128+9) | [demand paging과 OOM killer](../../02_os/book/linux-kernel-programming/09-03.메모리 할당 (5) — demand paging과 OOM killer.md) · [Endowus OOMKilled 사례](../../01_language/book/Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/ch02_automatic-memory-management/01-05.%EC%8B%A4%EC%A0%84%20%E2%80%94%20Docker%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20OOMKilled.md#64-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88-%ED%9E%99-%EB%B9%84%EC%9C%A8%EA%B3%BC-%EC%98%A4%ED%94%84%ED%9E%99-%EC%98%88%EC%82%B0) (일부: 힙 비율 사례, 137 설명은 같은 노트 §2) |
| CFS Bandwidth Control | 100ms 기본 주기 내 할당 quota 소진 시 다음 주기까지 프로세스를 강제 대기(Throttling) | [네임스페이스와 cgroup으로 보는 컨테이너 격리](../../08_cloud/book/kubernetes-in-action/02-03.네임스페이스와 cgroup으로 보는 컨테이너 격리.md) |
| 압축 가능·불가 자원 | CPU 는 넘으면 느려지고(throttling) 메모리는 넘으면 죽음(OOMKill). limits 설계의 기준 | [Predictable Demands](../../08_cloud/book/kubernetes-patterns/02-01.Predictable Demands — 자원 요구를 선언해 스케줄러에 알리기.md) |
| CrashLoopBackOff | 반복 실패한 컨테이너의 재시작 대기를 10초부터 두 배씩 늘려 최대 5분에서 멈춤 | [liveness·startup probe](../../08_cloud/book/kubernetes-in-action/06-02.liveness·startup probe로 컨테이너 건강 유지.md) |
| cAdvisor throttling 지표 | `container_cpu_cfs_throttled_periods_total` ÷ `container_cpu_cfs_periods_total` 로 노드 접속 없이 throttling 비율을 봄 | |
| OverlayFS | 불변 lowerdir(이미지)과 쓰기 가능 upperdir(컨테이너)을 병합하는 Union 파일시스템 | [OverlayFS와 user namespace](../../02_os/docs/kernel/OverlayFS%20%EC%99%80%20idmapped%20mount%20%E2%80%94%20Netflix%20%EC%82%AC%EB%A1%80.md) |
| veth pair | 격리된 Pod 네트워크 네임스페이스와 호스트 브리지를 양방향 가상 케이블로 연결 | [소켓·인터페이스·veth·브리지](../../08_cloud/book/networking-and-kubernetes/02-01.커널이 패킷을 주고받는 자리 — 소켓·인터페이스·veth·브리지.md) |
| CRI (Container Runtime Interface) | kubelet 이 containerd·CRI-O 등 다양한 컨테이너 런타임을 제어하기 위한 표준 gRPC 규격 | [컨테이너의 탄생](../../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| Self-Healing & Control Loop | etcd의 목표 상태와 현재 상태를 지속 비교해 비정상 Pod를 자동 복구하는 조정 루프 | [Reconciliation Loop의 계보](../../99_ETC/2026-04-19_Reconciliation Loop의 계보 — 제어이론에서 GitOps까지.md) |
| High Availability & Cascade Failure | SPOF 없는 다중 복제 구조 및 트래픽 폭증 시 Pod 전멸을 방어하는 Rate Limit·QoS 설계 | [Deployment Models — 배포 모델과 고가용성 인프라 구축](../../08_cloud/book/production-kubernetes/02-01.Deployment Models — 배포 모델과 고가용성 인프라 구축.md) (일부: 컨트롤 플레인 HA·SPOF 만, 연쇄 장애·Rate Limit 없음) · [실패를 견디는 일을 프록시로](../../08_cloud/book/istio-in-action/06-01.실패를 견디는 일을 프록시로 옮겼을 때.md) (일부: 타임아웃·재시도·서킷 브레이킹만, Rate Limit 없음) |
| AWS Nitro & MicroVM | Nitro 는 전용 하드웨어로 하이퍼바이저 일을 떼어 VM 격리와 성능을 양립함. MicroVM(Firecracker·Kata)은 경량 VMM 으로 VM 격리와 컨테이너 기동 속도를 결합함 | [하드웨어 가상화](../../02_os/book/systems-performance/11-02.클라우드 컴퓨팅 — 하드웨어 가상화.md) · [경량 가상화](../../02_os/book/systems-performance/11-04.클라우드 컴퓨팅 — 경량 가상화·기타·비교.md) |



## 자료와 실습

- 자료:
  - [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html): `memory.max`·`cpu.max`·`cpu.stat` 의 정의입니다. 노트는 [cgroup v2](../../02_os/docs/kernel/01-01.cgroup v2.md) 입니다.
  - [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html)·proc(5): 네임스페이스와 `/proc/<pid>/cgroup`·`/proc/<pid>/oom_score` 를 봅니다.
  - [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/): requests·limits 가 cgroup 설정과 QoS Class 로 바뀌는 규칙입니다.
  - [The Security Design of the AWS Nitro System](https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/welcome.html): Nitro Card 로 하이퍼바이저 일을 떼어 내는 구조입니다.
  - 『Container Security』 2·4·5장: 시스템 콜·권한, 격리 장치, VM 과 컨테이너를 다룹니다. 노트는 [정독 인덱스](../../08_cloud/book/container-security/README.md) 입니다.
  - 『Systems Performance』 2판 6·7·11장: CPU 스케줄링과 throttling, 메모리와 OOM, 클라우드와 컨테이너를 다룹니다. 노트는 [정독 인덱스](../../02_os/book/systems-performance/README.md) 입니다.
  - 『Kubernetes in Action』 2판 11·14장(리포트 표기): kubelet·CRI 내부와 자원 관리·QoS 를 다룹니다. 가까운 노트는 [02-03](../../08_cloud/book/kubernetes-in-action/02-03.네임스페이스와 cgroup으로 보는 컨테이너 격리.md) 입니다.
  - [Containers From Scratch](https://www.youtube.com/watch?v=8fi7uSYlOdc) 강연과 [lizrice/containers-from-scratch](https://github.com/lizrice/containers-from-scratch): Go 100줄 안팎으로 `CLONE_NEWPID`·`CLONE_NEWNS` 와 cgroup 제한을 직접 겁니다.
  - Indeed Engineering Blog 의 CPU Throttling in Kubernetes: CFS 쿼터로 P99 가 치솟은 운영 사례입니다. 리포트에 URL 은 없습니다.
  - 코드 읽기: runc 의 cgroup v2 기록부와 `libcontainer/nsenter/` 를 봅니다. 커널은 `mm/oom_kill.c` 의 `out_of_memory()`·`oom_badness()` 와 CFS 대역폭 제어를 봅니다. kubernetes 는 `pkg/kubelet/qos/policy.go` 의 `GetContainerOOMScoreAdjust` 를 봅니다.
- 실습:
  - Level 1: Docker 없이 `unshare --pid --fork --mount-proc` 와 cgroup v2 로 미니 컨테이너를 만듭니다. `memory.max` 를 50M 으로 두고 Python 으로 100MB 를 할당합니다. 완료는 `echo $?` 가 137 이고 `dmesg -T` 에 `Memory cgroup out of memory` 가 남는 것입니다. 함정은 cgroup v1 혼용이라, `stat -fc %T /sys/fs/cgroup/` 가 `cgroup2fs` 인지 먼저 봅니다.
  - Level 2: kind 에 OOM Pod(`limits.memory: 128Mi`, `stress --vm-bytes 200M`)와 throttling Pod(`limits.cpu: 50m`, `stress --cpu 1`)를 띄웁니다. 노드 안에서 `crictl` → `/proc` → `cpu.stat` 순으로 따라가 `nr_throttled / nr_periods` 를 계산합니다. 도구는 kind·kubectl·crictl·jq·`polinux/stress` 입니다. 완료는 `kubectl top` 50m 과 throttling 85% 이상의 차이를 적고, `limits.cpu: 1000m` 뒤 0%대로 떨어지는 수치까지 비교한 노트입니다. 함정은 `kubectl top` 에 metrics-server 를 따로 깔아야 한다는 점입니다(`--kubelet-insecure-tls`).
  - Level 3: `kube-prometheus-stack` 을 깔고 k6·hey 로 CPU limit 100m 서비스에 부하를 겁니다. Grafana 한 화면에 P99, `kubectl top` CPU, throttling 비율, `OOMKilled` 종료 사유 패널을 둡니다. 완료는 대시보드만으로 10초 안에 throttling 을 원인으로 짚는 것입니다. 함정은 PromQL 에 `container!="", container!="POD"` 를 빼면 pause 컨테이너가 비율을 흐린다는 점입니다.



## 경고

- ⚠ "Linux 6.6+에서 CFS가 EEVDF로 대체됨" (원문 33줄) — Ubuntu 22.04 LTS 의 GA 커널(5.15)은 CFS 이고, 22.04 HWE 6.8 커널은 EEVDF 입니다. 확인됨: [v6.6 fair.c](https://raw.githubusercontent.com/torvalds/linux/v6.6/kernel/sched/fair.c) 에 EEVDF 가 있고 v6.5 에는 없습니다. [linux-hwe-6.8](https://launchpad.net/ubuntu/+source/linux-hwe-6.8) 은 Jammy 용입니다.
- ⚠ "`oom_score` 범위는 -1000 ~ 1000" (원문 53·79줄) — 그 범위는 `oom_score_adj` 이고, `/proc/<pid>/oom_score` 는 0~2000 입니다. 원문 5-2 dmesg 예시의 `oom_score:967` 도 실제 커널은 `oom_score_adj:` 로 찍습니다. 확인됨: [fs/proc/base.c](https://raw.githubusercontent.com/torvalds/linux/master/fs/proc/base.c) 의 "[0, 2000] range" 주석입니다.
- ⚠ "AWS Nitro는 가상화 오버헤드가 1% 미만", "기존 하이퍼바이저는 CPU 오버헤드 15~20%" (원문 68·86줄) — I/O 패턴에 따라 체감 차이가 있음 — 미확인: 벤더 수치라 공식 문서 대상 아님
- ⚠ "노드 OOM 방지를 위해 Guaranteed QoS(requests==limits) 설정이 표준" (원문 53줄) — 자원 집적도·비용과 상충해 일괄 표준은 아님 — 미확인: 운영 설계 의견
- ⚠ "CPU Throttling 방지를 위해 limits를 빼고 requests만 설정" (원문 60~61줄) — 지연은 줄지만 노이즈 이웃 간섭 위험이 있습니다. 『Kubernetes Patterns』는 CPU 에 requests 만 걸라고 권합니다(위 표 「압축 가능·불가 자원」 노트). 미확인: 운영 판단 사항입니다.
- ⚠ 코드 경로 "runc `libcontainer/cgroups/fs2/`", "`kernel/sched/fair.c` 의 `tg_set_cfs_quota`" (원문 271~272줄) — 둘 다 지금 소스와 다릅니다. runc main 에는 `libcontainer/cgroups/` 가 없고, cgroup 코드는 [opencontainers/cgroups](https://github.com/opencontainers/cgroups/tree/main/fs2) 로 옮겨졌습니다. 커널 master(7.4)에는 `tg_set_cfs_quota` 가 없습니다. 설정은 `core.c` 의 `tg_set_cfs_bandwidth()`, 멈춤은 `fair.c` 의 `throttle_cfs_rq()` 가 맡습니다. 확인됨: 2026-11-16 GitHub 조회입니다. `mm/oom_kill.c` 의 두 함수와 `GetContainerOOMScoreAdjust` 는 원문대로 있습니다. v6.6 에서도 `tg_set_cfs_quota` 는 `core.c` 에 있었으므로 원문의 `fair.c` 위치는 그때도 틀렸습니다.
- ⚠ 『Kubernetes in Action』 2판 "11장 = 내부 구조, 14장 = 리소스 관리·QoS" (원문 257줄) — 이 저장소의 2판 노트에서 11장은 Service, 14장은 ReplicaSet 입니다. 미확인: 장 번호 불일치입니다.
- ⚠ "runc 가 Namespaces·OverlayFS·veth 로 컨테이너를 조립" (원문 91줄) — veth 는 CNI 플러그인이 만들고, OverlayFS rootfs 마운트는 containerd shim 이 runc 호출 전에 합니다. runc 는 namespace·cgroup·pivot_root 를 맡습니다. 확인됨: [bridge.go](https://github.com/containernetworking/plugins/blob/main/plugins/main/bridge/bridge.go) 의 `ip.SetupVeth`, [container.go](https://github.com/containerd/containerd/blob/main/cmd/containerd-shim-runc-v2/runc/container.go) 의 `mount.All` 입니다.
- ⚠ "JVM 에 `-XX:MaxRAMPercentage` 를 지정하지 않아 호스트 메모리 기준으로 힙을 키운다" (원문 52줄) — 옛 JDK 이야기입니다. JDK 10+(8u191+)는 컨테이너 한도를 읽고 `MaxRAMPercentage` 기본값 25% 를 씁니다. 확인됨: openjdk [globals_linux.hpp](https://github.com/openjdk/jdk/blob/master/src/hotspot/os/linux/globals_linux.hpp) 의 `UseContainerSupport=true`, [gc_globals.hpp](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/gc/shared/gc_globals.hpp) 의 25.0 입니다.
- ⚠ Level 1 완료 기준 "echo $? 가 137" (원문 332줄) — swap 이 켜진 호스트에서는 `memory.max` 만으로는 넘친 메모리가 swap 으로 빠져 0 으로 끝납니다. 같은 cgroup 에 `memory.swap.max` 를 0 으로 두면 137 과 dmesg 줄이 나옵니다. 확인됨: 2026-11-16 Ubuntu VM(커널 7.2, swap 있음) 실측입니다.
- ⚠ containers-from-scratch 의 "메모리/프로세스 제한" (원문 270줄) — `main.go` 는 cgroup v1 `pids` 컨트롤러(`pids.max=20`)만 씁니다. 메모리 제한은 없고, cgroup v2 전용 호스트에서는 그대로 돌지 않습니다. 확인됨: [main.go](https://github.com/lizrice/containers-from-scratch/blob/master/main.go) 63~69줄입니다.
