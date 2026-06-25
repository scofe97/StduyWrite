---
title: OS Kernel 딥다이브 로드맵 — 섹션별 키워드 원문
tags: [moc, linux, kernel, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# OS Kernel 딥다이브 로드맵 — 섹션별 키워드 원문

---

> Kubernetes 를 배우는 것이 아니라, Kubernetes 위에서 보이는 CPU·Memory·OOM·File·Network·Process 문제를 **Linux Kernel 관점에서 해석하는 능력**을 기르는 것이 목표입니다. 이 문서는 제공받은 OS Kernel 딥다이브 로드맵 원문을 **섹션별로 빠짐없이** 옮긴 기록이고, 카테고리 경계·등록 문서는 [README.md](README.md) 가 맡습니다. 네트워크 영역은 [networking/roadmap.md](../networking/roadmap.md) 가 따로 다룹니다.

## 1. Process / Thread 모델

백엔드 애플리케이션은 커널 입장에서는 프로세스와 스레드의 집합입니다.

핵심 키워드:

```text
Process
Thread
Task
task_struct
PID / TID
Parent Process
Child Process
Zombie Process
Orphan Process
Daemon Process
PID 1
Signal
Exit Code
Context Switch
System Call
User Mode / Kernel Mode
```

백엔드/K8s 관점: Java 애플리케이션은 하나의 프로세스이지만 내부에 수많은 JVM Thread 를 가진다. Pod 안의 PID 1 프로세스가 signal 을 제대로 처리하지 못하면 graceful shutdown 이 깨진다. 컨테이너 종료 시 SIGTERM → grace period → SIGKILL 흐름을 이해하려면 signal 개념이 필요하다. 좀비 프로세스가 쌓이면 PID 고갈이나 리소스 누수가 발생할 수 있다.

특히 봐야 할 것: SIGTERM · SIGKILL · SIGINT · SIGQUIT · exit code 0 · exit code 137 · exit code 143 · PID namespace · init process · tini / dumb-init. 실무에서는 `exit code 137` 만 봐도 "SIGKILL 이구나, OOMKilled 나 강제 종료 가능성" 으로 읽을 수 있어야 합니다.

## 2. System Call

애플리케이션은 디스크·네트워크·프로세스를 직접 만지지 않고 시스템 콜로 커널에 요청합니다.

핵심 키워드:

```text
System Call
User Mode
Kernel Mode
Trap
open
read
write
close
socket
bind
listen
accept
connect
send
recv
epoll
fork
exec
clone
mmap
futex
```

백엔드/K8s 관점: HTTP 요청 처리도 socket·accept·read·write 시스템 콜의 연속이다. 파일 로그 출력은 open/write/fsync 계열과 연결된다. JVM Thread 대기·lock 경합은 futex 와 연결된다. 성능 병목은 strace 로 시스템 콜 호출 패턴을 확인할 수 있다.

도구: `strace` · `perf` · `bpftrace`. Spring Boot 서버가 느릴 때 "코드가 느리다" 가 아니라 — DB 응답 대기인가 / 파일 I/O 대기인가 / socket read 대기인가 / lock 경합인가 / GC 인가 / 커널 스케줄링 지연인가 — 로 갈라봐야 합니다.

## 3. CPU Scheduling

커널은 여러 스레드에게 CPU 시간을 나눠줍니다.

핵심 키워드:

```text
Scheduler
CFS
Run Queue
Time Slice
Context Switch
CPU Affinity
nice
Priority
Load Average
Runnable
Blocked
Interrupt
SoftIRQ
CPU Throttling
```

백엔드/K8s 관점: CPU usage 는 낮은데 latency 가 높을 수 있다. CPU limit 을 걸면 cgroup quota 에 의해 CPU throttling 이 발생할 수 있다. Java Thread 가 많아지면 context switch 비용이 커진다. Pod CPU limit 이 낮으면 GC·Netty EventLoop·Tomcat Worker 모두 영향을 받는다.

중요 개념: CPU request · CPU limit · CFS quota · CFS period · cpu.shares · cpu.stat · nr_throttled · throttled_time. CPU limit 을 걸면 cgroup 아래에서 "일정 시간 동안 CPU 를 여기까지만 쓸 수 있고, 한도를 다 쓰면 다음 주기까지 실행을 멈춰 latency 가 튄다". 백엔드 운영에서는 `CPU 사용률` 보다 `CPU throttling` 이 더 중요한 경우가 많습니다.

## 4. Memory Management

K8s 에서 가장 자주 마주치는 커널 주제입니다. OOMKilled · RSS · Page Cache · Native Memory · Swap 은 반드시 알아야 합니다.

핵심 키워드:

```text
Virtual Memory
Physical Memory
Page
Page Table
RSS
VSS
PSS
Heap
Stack
Native Memory
mmap
Page Cache
Buffer Cache
Slab
Swap
OOM Killer
Overcommit
Transparent Huge Page
Memory Fragmentation
```

백엔드/K8s 관점: JVM Heap 만 보고 메모리를 판단하면 위험하다. 컨테이너 메모리에는 Heap·Metaspace·Thread Stack·DirectBuffer·Native Memory·Page Cache 가 함께 잡힌다. 파일을 많이 읽고 쓰면 Page Cache 가 증가한다. memory limit 을 넘으면 커널 OOM Killer 가 프로세스를 죽인다.

Java 백엔드 중요: -Xmx · -Xms · Metaspace · Thread Stack · Direct Memory · Code Cache · GC Region · Native Memory Tracking.

JVM 메모리 구조:

```text
Container Memory
├── Java Heap
├── Metaspace
├── Thread Stack
├── Direct Buffer
├── Code Cache
├── JNI / Native Library
├── GC Internal Structure
└── Page Cache
```

`-Xmx=2G` 이고 Pod memory limit 이 `2G` 이면 위험합니다 — JVM 은 Heap 만 먹고 사는 생물이 아니기 때문입니다.

## 5. OOM Killer / OOMKilled

K8s 의 `OOMKilled` 는 자주 보이지만 원인은 커널 메모리 관리에 있습니다.

핵심 키워드:

```text
OOM Killer
oom_score
oom_score_adj
cgroup memory limit
memory.max
memory.current
memory.events
RSS
Page Cache
Swap
Kernel Memory
Exit Code 137
```

백엔드/K8s 관점: Pod 가 죽었다고 반드시 Java Heap OOM 은 아니다. 커널이 cgroup memory limit 을 넘겼다고 판단하면 프로세스를 죽인다. exit code 137 은 SIGKILL 종료를 의미한다. Java OutOfMemoryError 와 Kubernetes OOMKilled 는 다르다.

구분:

```text
Java Heap OOM
- java.lang.OutOfMemoryError: Java heap space
- JVM 내부에서 발생
- 프로세스가 살아있을 수도 있음

Container OOMKilled
- Kernel OOM Killer가 프로세스 강제 종료
- exit code 137
- Pod restart 발생 가능
```

이 차이를 모르면 장애 분석이 빗나갑니다.

## 6. Cgroups

컨테이너 리소스 제한의 실체입니다. K8s 의 request/limit 은 커널 cgroup 으로 내려갑니다.

핵심 키워드:

```text
cgroup
cgroup v1
cgroup v2
cpu controller
memory controller
pids controller
blkio controller
cpuset controller
cpu.max
memory.max
memory.current
memory.events
pids.max
```

백엔드/K8s 관점: Pod CPU limit 은 cgroup CPU controller 로, memory limit 은 memory controller 로 구현된다. Pod 안에서 보는 /proc 정보가 Node 전체와 다를 수 있다. JVM 은 컨테이너 메모리 제한을 인식해야 적절한 Heap 크기를 잡는다.

봐야 할 파일: `/sys/fs/cgroup/cpu.stat` · `memory.current` · `memory.max` · `memory.events` · `pids.current` · `pids.max`. 장애 분석 시 이 파일들은 조용한 증인입니다.

## 7. Namespace

컨테이너가 격리된 것처럼 보이는 이유입니다. 가상머신처럼 커널을 따로 갖는 게 아니라 같은 커널을 공유하면서 namespace 로 시야를 나눕니다.

핵심 키워드:

```text
PID Namespace
Network Namespace
Mount Namespace
UTS Namespace
IPC Namespace
User Namespace
Cgroup Namespace
```

백엔드/K8s 관점: 컨테이너 안에서 PID 1 로 보여도 Node 전체에서는 다른 PID 다. Pod 안 hostname 은 UTS namespace 로 격리된다. 컨테이너 파일시스템은 mount namespace 로 격리된다. Pod 내부 네트워크는 network namespace 와 연결된다.

핵심: Container 는 작은 VM 이 아니다. Container 는 namespace 와 cgroup 으로 격리된 Linux process 다. Pod 안 여러 container 는 보통 network namespace 를 공유한다.

## 8. File Descriptor

백엔드 서버에서 중요합니다. HTTP connection · DB connection · file · socket 모두 파일 디스크립터로 다뤄집니다.

핵심 키워드:

```text
File Descriptor
ulimit
open file limit
socket fd
regular file
pipe
epoll fd
stdin / stdout / stderr
Too many open files
```

백엔드/K8s 관점: DB·HTTP 연결·로그 파일 모두 FD 를 쓴다. FD limit 이 낮으면 트래픽이 적어도 장애가 날 수 있다.

자주 보는 에러: Too many open files · Connection refused · Connection reset · Cannot allocate memory.

확인 명령: `ulimit -n` · `lsof -p <PID>` · `ls /proc/<PID>/fd | wc -l` · `cat /proc/<PID>/limits`. thread pool·connection pool 만 볼 게 아니라 FD limit 도 같이 봐야 합니다.

## 9. File System / VFS / OverlayFS

컨테이너 이미지·로그·볼륨·임시 파일 문제를 이해하려면 파일시스템을 알아야 합니다.

핵심 키워드:

```text
VFS
inode
dentry
superblock
page cache
fsync
sync
journaling
ext4
xfs
overlayfs
copy-on-write
tmpfs
mount
bind mount
volume mount
```

백엔드/K8s 관점: 컨테이너 이미지는 overlayfs 기반으로 동작하는 경우가 많다. writable layer 에 많은 파일을 쓰면 성능·안정성 문제가 생긴다. emptyDir·hostPath·PVC 는 커널 mount 관점에서 이해해야 한다. 로그를 stdout 으로 남기는 것과 파일로 남기는 것은 커널 I/O 경로가 다르다.

장애: No space left on device · inode full · Read-only file system · Slow fsync · OverlayFS copy-up 비용 · PVC I/O latency 증가. 디스크 용량이 남아도 inode 가 고갈되면 파일을 못 만듭니다 — 로그·임시 파일 폭증에서 자주 만나는 문제입니다.

## 10. Disk I/O / Block Layer

DB·로그·파일 업로드·Kafka 를 다룬다면 커널 I/O 를 피할 수 없습니다.

핵심 키워드:

```text
Block Device
I/O Scheduler
IOPS
Throughput
Latency
Queue Depth
Page Cache
Dirty Page
Writeback
fsync
Direct I/O
Buffered I/O
```

백엔드/K8s 관점: DB 가 느린 게 아니라 디스크 writeback 이 밀린 것일 수 있다. 로그가 많으면 애플리케이션 latency 에 영향을 준다. PVC 성능은 애플리케이션 성능과 직결된다. fsync 가 많은 워크로드는 throughput 보다 latency 가 중요하다.

도구: `iostat` · `iotop` · `pidstat -d` · `sar -d`. MariaDB·PostgreSQL·Kafka·Elasticsearch·Loki 는 디스크 I/O 를 모르면 운영 감각이 흐려집니다.

## 11. Socket / epoll

백엔드 서버가 커널 소켓을 어떻게 사용하는지에 초점을 둡니다.

핵심 키워드:

```text
Socket
File Descriptor
listen
accept
backlog
accept queue
send buffer
receive buffer
epoll
event loop
non-blocking I/O
SO_REUSEPORT
TIME_WAIT
```

백엔드/K8s 관점: Tomcat·Netty·Nginx 모두 커널 socket 위에서 동작한다. 트래픽이 몰리면 accept queue·backlog·FD limit 이 문제가 된다. WebFlux/Netty 는 epoll 기반 이벤트 루프와 연결해 이해할 수 있다. Connection 이 많으면 socket buffer·FD 사용량이 증가한다.

Java 연결: Tomcat Worker Thread · NIO Connector · Netty EventLoop · Selector · epoll · SocketChannel. "이 연결은 커널에서 어떤 FD 와 queue 로 관리되는가" 를 보는 쪽입니다.

## 12. Lock / Futex / Contention

애플리케이션 lock 경합은 커널 수준 대기와 연결될 수 있습니다.

핵심 키워드:

```text
Mutex
Semaphore
Spinlock
Futex
Blocking
Waking
Contention
Context Switch
Thread State
```

백엔드/K8s 관점: Java synchronized·ReentrantLock 경합이 심하면 thread 가 대기한다. 대기 thread 가 많으면 CPU 를 쓰지 않는데도 응답이 느려진다. Lock 경합은 CPU 사용률만 봐서는 잘 드러나지 않는다.

Java 연결: BLOCKED · WAITING · TIMED_WAITING · park · unpark · futex · thread dump. `jstack` · `async-profiler` · `perf` 를 같이 보면 좋습니다.

## 13. Kernel Security

컨테이너 보안에서 중요합니다. K8s 보안 설정은 커널 기능과 맞닿아 있습니다.

핵심 키워드:

```text
Linux Capability
seccomp
AppArmor
SELinux
User Namespace
Rootless Container
No New Privileges
Privileged Container
readOnlyRootFilesystem
```

백엔드/K8s 관점: 컨테이너 안에서 root 라도 host root 와 같지 않을 수 있다. privileged container 는 커널 공격면을 크게 넓힌다. CAP_NET_ADMIN·CAP_SYS_ADMIN 같은 capability 는 강력하다. seccomp 는 허용할 system call 을 제한한다.

봐야 할 것: CAP_SYS_ADMIN · CAP_NET_ADMIN · CAP_CHOWN · CAP_DAC_OVERRIDE · seccomp profile · AppArmor profile · SELinux context. 백엔드/K8s 관점에서는 "컨테이너가 커널 기능을 얼마나 쓸 수 있는가" 를 우선 봅니다.

## 14. Observability: /proc, /sys, eBPF

커널을 공부하는 가장 실용적인 이유는 관측입니다.

핵심 키워드:

```text
/proc
/sys
procfs
sysfs
cgroupfs
eBPF
kprobe
uprobe
tracepoint
perf event
flame graph
PSI
```

백엔드/K8s 관점: Pod CPU·Memory 지표는 cgroup·kernel metric 에서 나온다. 프로세스 상태는 /proc/<PID> 아래에서 확인한다. eBPF 는 커널 이벤트를 낮은 오버헤드로 관측한다. Cilium·Pixie·Parca·bpftrace 가 eBPF 를 활용한다.

익힐 경로: `/proc/cpuinfo` · `/proc/meminfo` · `/proc/loadavg` · `/proc/<PID>/status` · `/proc/<PID>/limits` · `/proc/<PID>/fd` · `/proc/<PID>/net/tcp` · `/sys/fs/cgroup`.

도구: `top` · `htop` · `ps` · `vmstat` · `pidstat` · `iostat` · `sar` · `ss` · `lsof` · `strace` · `perf` · `bpftrace`. 커널은 먼 산맥이 아니라 `/proc`·`/sys` 라는 창문 너머의 풍경입니다.

## 15. 학습 우선순위

1순위 (반드시):

```text
Process / Thread
Signal
Exit Code
System Call
CPU Scheduling
Cgroup CPU
Memory Management
OOM Killer
File Descriptor
/proc
/sys/fs/cgroup
```

2순위 (장애 분석에 유용):

```text
Page Cache
RSS / VSS / PSS
Context Switch
Load Average
CPU Throttling
OverlayFS
Disk I/O
epoll
Socket Queue
ulimit
```

3순위 (고급 운영/플랫폼):

```text
eBPF
perf
ftrace
seccomp
Linux Capability
NUMA
PSI
Kernel Parameter Tuning
Transparent Huge Page
I/O Scheduler
```

## 16. 백엔드 장애와 커널 개념 매핑

| 장애 현상 | 봐야 할 커널 개념 |
|----------|-----------------|
| Pod OOMKilled | cgroup memory, OOM Killer, RSS, Page Cache |
| Exit Code 137 | SIGKILL, OOM Killer |
| Exit Code 143 | SIGTERM, graceful shutdown |
| CPU 사용률 낮은데 응답 지연 | run queue, context switch, blocking I/O, lock contention |
| CPU limit 후 latency 증가 | CFS quota, CPU throttling |
| Too many open files | file descriptor, ulimit |
| Connection refused | listen backlog, accept queue, socket state |
| 로그 많을 때 느려짐 | write syscall, page cache, dirty page, fsync |
| 디스크 용량 남았는데 파일 생성 실패 | inode |
| 컨테이너에서 kill이 안 먹힘 | PID 1, signal handling |
| JVM 메모리 계산이 안 맞음 | heap, metaspace, direct memory, thread stack, native memory |
| 네트워크 연결 많을 때 불안정 | socket buffer, FD limit, TIME_WAIT |
| DB/Kafka가 갑자기 느림 | disk I/O, page cache, fsync, queue depth |

## 17. 최종 학습 문구

```text
OS Kernel:
Linux Kernel의 프로세스, 스케줄링, 메모리 관리, 시스템 콜, 파일시스템,
cgroup, namespace, signal, file descriptor, socket I/O 등의 핵심 개념을 이해하고,
Kubernetes 및 백엔드 운영 환경에서 발생하는 OOMKilled, CPU throttling,
graceful shutdown 실패, file descriptor 고갈, disk I/O 병목, JVM 메모리 사용량
불일치 등의 문제를 커널 관점에서 분석하고 해결할 수 있는 역량을 함양한다.
```

## 18. 최종 압축 키워드

```text
Process / Thread / task_struct
PID / TID / PID Namespace / PID 1
Signal / SIGTERM / SIGKILL / Exit Code 137 / Exit Code 143
System Call / User Mode / Kernel Mode / strace
CPU Scheduler / CFS / Run Queue / Context Switch / Load Average
Cgroup v1/v2 / CPU Quota / CPU Throttling / memory.max / memory.events
Virtual Memory / Page Table / RSS / VSS / PSS
JVM Heap / Metaspace / Direct Memory / Thread Stack / Native Memory
Page Cache / Buffer Cache / Dirty Page / Writeback
OOM Killer / oom_score / oom_score_adj / Container OOMKilled
File Descriptor / ulimit / lsof / Too many open files
VFS / inode / dentry / ext4 / xfs / OverlayFS / Copy-on-Write
Disk I/O / IOPS / Throughput / Latency / fsync / I/O Scheduler
Socket FD / listen backlog / accept queue / epoll / non-blocking I/O
Futex / Lock Contention / Thread State / BLOCKED / WAITING
Linux Capability / seccomp / AppArmor / SELinux / Privileged Container
/proc / /sys / cgroupfs / procfs / sysfs
perf / bpftrace / eBPF / kprobe / uprobe / tracepoint / Flame Graph
PSI / NUMA / Transparent Huge Page / Kernel Parameter / sysctl
```

이 주제는 결국 "컨테이너 안에서 죽은 애플리케이션의 사인을 커널의 언어로 읽는 법" 입니다. 백엔드 개발자가 여기까지 내려갈 수 있으면 장애 대응의 시야가 한 겹 깊어집니다.
