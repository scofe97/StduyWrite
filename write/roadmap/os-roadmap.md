---
title: OS 학습 로드맵
tags: [roadmap, linux, os, kernel, container, performance, security]
status: final
source:
  - ../02_os/README.md
  - ../02_os/kernel/README.md
  - ../02_os/book/systems-performance/README.md
related:
  - README.md
  - network-roadmap.md
  - k8s-roadmap.md
  - ../02_os/README.md
updated: 2026-09-12
---

# OS 학습 로드맵
---

> Linux 운영에서 시작해 프로세스, 격리, 자원, 성능, 커널 내부 순서로 내려갑니다. Kubernetes에서 보이는 OOMKilled·CPU throttling·종료 문제도 같은 OS 경로에서 해석합니다.

## 이 순서를 잡은 기준

> 커널을 자료구조부터 배우면 `task_struct` 에서 지치고, 정작 매일 마주치는 종료 코드 137을 못 읽습니다. 이 로드맵은 반대로 갑니다 — **운영에서 올라온 증상에서 시작해 그 증상이 서 있는 층으로 한 겹씩 내려갑니다.**

![Linux 운영에서 커널 내부로 내려가는 OS 학습 순서](_assets/os-roadmap.svg)

증상이 먼저입니다. Pod가 137로 죽으면 3단계의 cgroup이 첫 자리이고, CPU 사용률이 낮은데 응답이 느리면 4단계의 run queue가 첫 자리입니다. 단계 번호는 진도가 아니라 **의존 순서**입니다.

여섯 단계는 셋으로 묶입니다. 1~3단계는 컨테이너가 무엇 위에 서 있는지를 잡는 기반입니다. 4~5단계는 느려진 이유를 재는 축이고, 6단계는 그 아래 커널 구현입니다. 앞의 셋은 운영자가 반드시 지나갑니다. 뒤의 셋은 필요가 생겼을 때 엽니다.

네트워크는 이 로드맵에서 일부러 얇게 다룹니다. 3단계의 network namespace까지만 잡고, 그 뒤 패킷이 어디로 가는지는 [네트워크 로드맵](network-roadmap.md)이 다섯 단계로 따로 맡습니다.



## 무엇을 골랐는가

> 자료가 두 종류입니다. Kubernetes 운영자 관점으로 쓴 자체 노트와, 책 한 권을 장 순서대로 따라간 정독본입니다.

둘의 경계는 [02_os MOC](../02_os/README.md) §카테고리 결정 원칙이 정합니다.

| 자료 | 편수 | 자리 |
|---|:---:|---|
| [kernel/](../02_os/kernel/README.md) | 7 | 2·3단계의 기둥 |
| [Learning Modern Linux](../02_os/book/learning-modern-linux/README.md) | 16 | 1단계의 기둥. 2·3단계의 보조 |
| [Systems Performance](../02_os/book/systems-performance/README.md) | 53 | 4·5단계의 기둥 |
| [Linux Kernel Programming](../02_os/book/linux-kernel-programming/README.md) | 32 | 6단계의 기둥. 2단계의 보조 |
| [Container Security](../08_cloud/book/container-security/README.md) | 17 | 5단계의 기둥. 3단계의 보조 |
| [troubleshooting/os](../troubleshooting/os/README.md) · [runtime](../troubleshooting/runtime/README.md) | 3 · 2 | 2·4단계를 시험하는 드릴 |

**[kernel/](../02_os/kernel/README.md) 일곱 편이 이 로드맵의 허리입니다.** 컨테이너를 만드는 커널 기능을 운영자 시선으로 적은 노트입니다. namespace와 cgroup을 설명하고 끝내지 않고 `/sys/fs/cgroup` 트리를 열어 Pod별 디렉토리를 찾는 데까지 갑니다. 그래서 3단계의 완료 기준이 대부분 이 폴더를 가리킵니다.

**책 셋은 같은 커널을 다른 시선으로 봅니다.** 02_os MOC가 적어 둔 대로 `kernel/` 은 운영자, `linux-kernel-programming/` 은 모듈 작성자, `systems-performance/` 는 성능 분석가 시선입니다. 같은 CPU 스케줄러가 세 곳에 나오는 이유가 여기 있습니다. 이 로드맵은 4단계에 성능 분석가 판을 놓고, 6단계에 모듈 작성자 판을 놓았습니다.

**《Container Security》를 5단계에 세운 데는 조건이 있습니다.** 격리 메커니즘 자체는 `kernel/` 이 정본이고, 이 책은 "그 격리가 정말 격리인가"를 묻는 축입니다. 질문이 성립하려면 3단계에서 namespace와 cgroup을 먼저 잡아야 합니다. 그래서 3단계에는 자원 제한과 루트 디렉토리를 다루는 두 편만 보조로 겁니다. 본체는 5단계에서 엽니다.

**《Systems Performance》 53편은 분량이 커서 통독을 전제하지 않습니다.** 4단계가 필요로 하는 것은 2장의 방법론과 자원별 네 장이고, 5단계가 관측 도구 4장과 추적 삼총사 13~15장을 씁니다. 나머지는 증상이 생겼을 때 찾아 들어갑니다.

**troubleshooting 다섯 편은 자료가 아니라 시험지입니다.** 증상에서 원인을 역추적하는 형식이라 읽는 순서에 넣지 않고, 배운 것을 확인하는 자리에 놓았습니다.



## 낡음 점검

> 책은 찍힌 시점에 멈춥니다. 기준은 앞선 로드맵들과 같습니다 — 도구와 제품 버전처럼 빨리 바뀌는 축은 5년을 넘기면 공식 문서로 대신하고, 커널 원리처럼 느리게 바뀌는 축은 오래돼도 남깁니다.

| 자료 | 기준 시점 | 조치 |
|---|:---:|---|
| kernel/ | 2026-09 · cgroup v2 | 그대로 |
| Learning Modern Linux | 2022 | **조건부 유지.** 도구 이름은 `man` 으로 확인 |
| Systems Performance | 2판 | 그대로. 방법론 축이라 느리게 바뀜 |
| Linux Kernel Programming | 2판 · 6.1 LTS | 그대로 |
| Container Security | 2020 · 1판 | **조건부 유지.** 2판이 이미 나옴 |
| troubleshooting/os · runtime | 2026-09 | 그대로 |

**《Learning Modern Linux》는 도구 목록이 가장 빨리 낡는 자리입니다.** 2022년 책이라 5년 기준 안에 있지만, 저자가 현대 도구로 고른 목록은 교체가 잦습니다. [레시피와 현대 도구 참조 시트](../02_os/book/learning-modern-linux/00-03.%EB%A0%88%EC%8B%9C%ED%94%BC%EC%99%80%20%ED%98%84%EB%8C%80%20%EB%8F%84%EA%B5%AC%20%EC%B0%B8%EC%A1%B0%20%EC%8B%9C%ED%8A%B8.md)를 열 때는 명령 이름을 그대로 믿지 않고 `man` 으로 확인합니다.

**《Systems Performance》는 저자가 낡음을 설계에 넣었습니다.** "도구는 낡아도 방법론은 남는다"가 책의 전제라 USE 메서드와 드릴다운은 그대로 씁니다. 대신 13~15장의 도구 사용법은 지금 쓰는 배포판 버전으로 대조합니다.

**《Container Security》는 2판이 나왔습니다.** 이 노트가 1판 기준이라는 사실은 폴더 README에 2판의 존재와 조회 일자로 함께 적혀 있습니다. 격리 강화 8장과 런타임 보호 13장처럼 제품이 빨리 바뀌는 장은 2판이나 공식 문서로 대조합니다. namespace·cgroup·capability를 다루는 2~4장은 그대로 씁니다.



## 손으로 확인하는 실습

> 읽기만 하면 남의 말을 옮기게 됩니다. 커널은 특히 그렇습니다 — namespace는 `unshare` 를 쳐 봐야 알고, OOMKilled는 한 번 직접 내 봐야 압니다.

기준은 **그 자리를 손으로 확인할 자료가 이미 노트 안에 있는가** 하나입니다. 비어 있는 단계는 실습이 필요 없어서가 아니라 확인한 자료를 못 찾아서이고, 지어낸 출처를 채우지 않았습니다.

| 출처 | 어느 단계 | 무엇 |
|---|:---:|---|
| [namespace 실습](../02_os/kernel/01-05.namespace%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%208%EA%B0%80%EC%A7%80%20%EA%B2%A9%EB%A6%AC%EC%99%80%20unshare.md) §9~11 | 3 | `unshare` 로 PID·UTS·MNT·NET 격리를 직접 만들기 |
| [cgroup 파일시스템 실습](../02_os/kernel/01-04.cgroup%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%8B%A4%EC%8A%B5.md) §6·8·10 | 3 | Pod의 cgroup 파일 확인, 의도적 OOM 트리거, QoS별 oom_score 비교 |
| [CPU 스케줄러 (6)](../02_os/book/linux-kernel-programming/11-03.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%286%29%20%E2%80%94%20cgroups%20CPU%20%EC%A0%9C%EC%95%BD%EA%B3%BC%20RTOS.md) §2 | 3 | `cpu.max` 를 손으로 걸어 throttling 재현 |
| [파일 시스템 (3)](../02_os/book/systems-performance/08-03.%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%283%29%20%E2%80%94%20%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%EC%8B%A4%ED%97%98%C2%B7%ED%8A%9C%EB%8B%9D.md) · [디스크 (3)](../02_os/book/systems-performance/09-03.%EB%94%94%EC%8A%A4%ED%81%AC%20%283%29%20%E2%80%94%20%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94%C2%B7%EC%8B%A4%ED%97%98%C2%B7%ED%8A%9C%EB%8B%9D.md) §4 | 4 | 의도적으로 부하를 걸어 포화 지점 찾기 |
| [벤치마킹 (3)](../02_os/book/systems-performance/12-03.%EB%B2%A4%EC%B9%98%EB%A7%88%ED%82%B9%20%283%29%20%E2%80%94%20%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%EB%B2%A4%EC%B9%98%EB%A7%88%ED%81%AC%20%EC%A7%88%EB%AC%B8.md) §3 | 4 | ramping load로 한계 지점 찾기 |
| [troubleshooting/os](../troubleshooting/os/README.md) · [runtime](../troubleshooting/runtime/README.md) | 2·4 | 증상에서 원인을 역추적하는 진단 드릴 다섯 편 |

1·5·6단계 자리는 비어 있습니다. 1단계는 셸과 systemd를 매일 쓰는 자리라 노트가 별도 실습 절을 두지 않았습니다. 5·6단계는 관측 도구와 커널 모듈을 다루는 노트가 명령과 코드를 본문에 섞어 두어 실습 절로 떼어져 있지 않습니다. 그 자리에서 손을 쓰고 싶으면 [perf (1)](../02_os/book/systems-performance/13-01.perf%20%281%29%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7%EC%84%9C%EB%B8%8C%EC%BB%A4%EB%A7%A8%EB%93%9C%C2%B7%EC%9B%90%EB%9D%BC%EC%9D%B4%EB%84%88.md)의 원라이너를 그대로 쳐 보는 것이 가장 가깝습니다.

**드릴 다섯 편은 답을 보기 전에 먼저 풉니다.** 파일명이 증상이므로 제목만 읽고 어느 단계의 어느 개념을 봐야 할지 스스로 정한 뒤 본문을 엽니다. 그 판단 자체가 앞 단계의 완료 기준입니다.



## 학습 순서

> 같은 단계에서도 연결된 문서가 다르면 행을 나눴습니다. 현재 목적에 필요한 행까지 읽고 완료 기준으로 이해를 확인합니다.

| 단계 | 우선순위 | 주제 | 키워드 | 학습 문서 | 완료 기준 |
|---|:---:|---|---|---|---|
| 1. Linux 사용 | 필수 | 선수지식 · 셸·파일·권한 | path·permission<br>redirection·pipe<br>environment·job control | [Learning Modern Linux](../02_os/book/learning-modern-linux/README.md) | 파일과 명령 출력을 조합해 실행 환경의 상태를 확인합니다. |
| 1. Linux 사용 | 필수 | 실습·진단 · 부팅·서비스 | bootloader·initramfs<br>systemd unit·dependency<br>journal·mount | [02_os MOC](../02_os/README.md) · [Learning Modern Linux](../02_os/book/learning-modern-linux/README.md) | 서비스 시작 실패를 unit, log, mount 의존성으로 나눕니다. |
| 2. 실행 모델 | 필수 | 핵심 · 프로세스·시스템 콜 | process·thread·task<br>PID·TID·user/kernel mode<br>system call: `fork`·`exec`·`mmap`·`futex` | [커널과 컨테이너](../02_os/kernel/01-01.%EC%BB%A4%EB%84%90%EA%B3%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) · [Linux Kernel Programming](../02_os/book/linux-kernel-programming/README.md) | 애플리케이션 작업이 어떤 시스템 콜과 커널 자원으로 이어지는지 설명합니다. |
| 2. 실행 모델 | 필수 | 실습·진단 · 종료·FD | SIGTERM·SIGKILL·exit 137/143<br>zombie·PID 1<br>FD·`ulimit`·`epoll` | [Learning Modern Linux](../02_os/book/learning-modern-linux/README.md) · [Systems Performance](../02_os/book/systems-performance/README.md) | 종료 실패와 FD 고갈을 프로세스 상태와 제한값에서 찾습니다. |
| 3. 컨테이너 기반 | 필수 | 선수지식 · namespace | PID·NET·MNT namespace<br>UTS·IPC·USER namespace<br>`unshare`·shared kernel | [namespace 실습](../02_os/kernel/01-05.namespace%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%208%EA%B0%80%EC%A7%80%20%EA%B2%A9%EB%A6%AC%EC%99%80%20unshare.md) | 컨테이너가 격리하는 자원과 호스트와 공유하는 커널을 구분합니다. |
| 3. 컨테이너 기반 | 필수 | 실습·진단 · cgroup v2·OOM | controller·`cpu.max`·`cpu.stat`<br>`memory.max/current/events`<br>PSI·OOM Killer | [cgroup v2 깊이](../02_os/kernel/01-02.cgroup%20v2%20%EA%B9%8A%EC%9D%B4.md) · [cgroup 실습](../02_os/kernel/01-04.cgroup%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%8B%A4%EC%8A%B5.md) · [OOMKilled 사례](../02_os/kernel/01-06.cgroup%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20OOMKilled.md) | JVM 힙 OOM과 cgroup OOMKilled를 구분하고 제한 파일에서 원인을 확인합니다. |
| 3. 컨테이너 기반 | 필수 | 핵심 · 마운트·파일시스템 | mount namespace·propagation<br>VFS·inode·dentry<br>OverlayFS·copy-on-write·user namespace | [마운트 namespace](../02_os/kernel/01-03.%EB%A7%88%EC%9A%B4%ED%8A%B8%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20propagation.md) · [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) | 컨테이너 writable layer와 볼륨 마운트 문제를 커널 파일시스템 경로로 설명합니다. |
| 4. 성능 분석 | 필수 | 핵심 · CPU·스케줄링 | run queue·CFS·context switch<br>load average·CPU affinity<br>throttling·softirq | [Systems Performance](../02_os/book/systems-performance/README.md) | 낮은 CPU 사용률과 높은 지연이 함께 나타나는 원인을 실행 대기와 제한으로 나눕니다. |
| 4. 성능 분석 | 필수 | 실습·진단 · 메모리·I/O | virtual memory·RSS/VSS/PSS<br>page cache·swap·overcommit<br>block I/O·IOPS·queue depth·`fsync` | [Systems Performance](../02_os/book/systems-performance/README.md) | 메모리와 디스크 병목을 사용률, 포화, 오류로 분해합니다. |
| 5. 관측과 보안 | 추천 | 실습·진단 · `/proc`·추적·eBPF | procfs·sysfs·perf·Ftrace<br>tracepoint·kprobe·uprobe<br>BCC·bpftrace·BTF·CO-RE | [Systems Performance](../02_os/book/systems-performance/README.md) · [Linux Kernel Programming](../02_os/book/linux-kernel-programming/README.md) | 증상에 맞춰 상태 조회, 샘플링, 이벤트 추적 중 하나를 선택합니다. |
| 5. 관측과 보안 | 추천 | 핵심 · 커널 보안 경계 | capability·seccomp<br>AppArmor·SELinux<br>user namespace·rootless<br>no-new-privileges·privileged | [Container Security](../08_cloud/book/container-security/README.md) · [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) | 컨테이너 권한 요청이 넓히는 커널 공격면을 설명합니다. |
| 6. 커널 내부 | 추천 | 핵심·진단 · 자료구조·가상화 | interrupt·locking·spinlock·RCU<br>allocator·VFS·io_uring<br>LSM·KVM·crash analysis | [Linux Kernel Programming](../02_os/book/linux-kernel-programming/README.md) | 운영 증상을 관련 커널 자료구조와 실행 경로까지 추적합니다. |

네트워크 namespace 이후의 패킷 경로는 [네트워크 로드맵](network-roadmap.md), Kubernetes 오브젝트와 클러스터 운영은 [Kubernetes 로드맵](k8s-roadmap.md)에서 이어갑니다.



## 기반 · 1~3단계

> 컨테이너가 무엇 위에 서 있는지를 잡습니다. 여기까지가 운영자가 반드시 지나가는 구간입니다.

각 단계는 표 둘로 적습니다. `개념` 표는 보유 노트가 그 자리를 어디서 다루는지이고, `자료 밖 키워드` 표는 노트가 다루지 않아 바깥에서 찾아야 하는 축입니다. OS 노트는 다섯 폴더 125편으로 촘촘한 편이라 둘째 표가 대부분 두 줄에 그칩니다. 빈칸을 채우려고 이미 노트에 있는 항목을 옮겨 적지 않았습니다.

### 1단계 · Learning Modern Linux 열여섯 편  `필수`

가장 아래에서 시작하지 않습니다. 셸에 명령을 치고 서비스를 띄우는 자리에서 시작해, 그 명령이 무엇을 건드리는지를 봅니다. 커널이 맡는 일과 배포판이 맡는 일을 여기서 갈라 두면 뒤 단계에서 "이건 커널 문제인가"를 물을 수 있습니다.

| 개념 | 어디서 |
|---|---|
| 하드웨어를 가린 뒤 무엇이 보이는가 | [01-01](../02_os/book/learning-modern-linux/01-01.%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4%EB%A5%BC%20%EA%B0%80%EB%A6%AC%EA%B3%A0%20%EB%82%98%EB%A9%B4%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%B3%B4%EC%9D%BC%EC%A7%80%EB%A5%BC%20%EC%A0%95%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) |
| 커널이 맡는 일과 맡지 않는 일 | [02-01](../02_os/book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md) |
| 셸 — 스트림·변수·종료 상태, 조용한 실패 | [03-01](../02_os/book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) · [03-02](../02_os/book/learning-modern-linux/03-02.%EC%9E%90%EC%A3%BC%20%EC%B9%98%EB%8A%94%20%EA%B2%83%EC%9D%BC%EC%88%98%EB%A1%9D%20%EC%A7%A7%EC%95%84%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) · [03-03](../02_os/book/learning-modern-linux/03-03.bash%20%EB%8A%94%20%EC%A1%B0%EC%9A%A9%ED%9E%88%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%AF%80%EB%A1%9C%20%EC%8B%9C%EB%81%84%EB%9F%BD%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) |
| 모든 것이 파일 — 손잡이가 하나라는 뜻 | [05-01](../02_os/book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) |
| 먼저 켜지는 것 — 부팅과 systemd | [06-01](../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) |

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| `systemd-analyze` | 어느 unit이 부팅 시간을 붙잡고 있는가 |
| core dump 저장 경로 | 컨테이너 안에서 죽은 프로세스의 덤프가 어디로 가는가 |

완료 기준은 파일과 명령 출력을 조합해 실행 환경의 상태를 확인하고, 서비스 시작 실패를 unit·로그·마운트 의존성 중 어디의 문제인지 나누는 것입니다.

### 2단계 · kernel/ 01-01과 Systems Performance 3장  `필수`

애플리케이션이 하는 일은 결국 시스템 콜입니다. 이 층을 지나야 "프로세스가 죽었다"를 "무엇이 어떤 신호로 내렸다"로 바꿔 말할 수 있습니다. 종료와 파일 디스크립터는 컨테이너 장애에서 가장 자주 올라오는 두 축입니다.

| 개념 | 어디서 |
|---|---|
| 유저·커널 스페이스, 시스템 콜, 커널 코어 7대 영역 | [커널과 컨테이너](../02_os/kernel/01-01.%EC%BB%A4%EB%84%90%EA%B3%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) |
| `strace` 로 본 runc create — 컨테이너가 만들어지는 콜 순서 | [커널과 컨테이너](../02_os/kernel/01-01.%EC%BB%A4%EB%84%90%EA%B3%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) §9 |
| 커널·시스템 콜·인터럽트·프로세스 | [운영체제 (1)](../02_os/book/systems-performance/03-01.%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%20%281%29%20%E2%80%94%20%EC%BB%A4%EB%84%90%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EC%9D%B8%ED%84%B0%EB%9F%BD%ED%8A%B8%C2%B7%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4.md) |
| 프로세스 컨텍스트·가상 주소 공간·스택, task 구조 | [프로세스와 스레드 (1)](../02_os/book/linux-kernel-programming/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%99%80%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%281%29%20%E2%80%94%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%C2%B7VAS%C2%B7%EC%8A%A4%ED%83%9D.md) · [(2)](../02_os/book/linux-kernel-programming/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%99%80%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%282%29%20%E2%80%94%20task%20%EA%B5%AC%EC%A1%B0%EC%99%80%20current.md) |
| 종료 상태와 신호, 좀비 프로세스 | [03-01](../02_os/book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) · [06-01](../02_os/book/learning-modern-linux/06-01.%EB%A8%BC%EC%A0%80%20%EC%BC%9C%EC%A7%80%EB%8A%94%20%EA%B2%83%20%ED%95%98%EB%82%98%EA%B0%80%20%EB%82%98%EB%A8%B8%EC%A7%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%EC%BC%A0%EB%8B%A4.md) |
| 파일 디스크립터, 자원마다 다른 관측 창 | [05-01](../02_os/book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md) · [08-02](../02_os/book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md) |
| `epoll` 과 논블로킹 I/O | [운영체제 (3)](../02_os/book/systems-performance/03-03.%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%20%283%29%20%E2%80%94%20%EC%BB%A4%EB%84%90%20%EA%B5%AC%ED%98%84%C2%B7Linux%20%EB%B0%9C%EC%A0%84%EC%82%AC%C2%B7BPF.md) · [애플리케이션 (1)](../02_os/book/systems-performance/05-01.%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%281%29%20%E2%80%94%20%EA%B8%B0%EC%B4%88%EC%99%80%20%EC%84%B1%EB%8A%A5%20%EA%B8%B0%EB%B2%95.md) |

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| `prctl`·`PR_SET_PDEATHSIG` | 부모가 죽을 때 자식을 함께 내리는 방법 |
| `vfork`·`clone3` | 런타임이 `fork` 대신 실제로 쓰는 호출 |

완료 기준은 애플리케이션 작업이 어떤 시스템 콜과 커널 자원으로 이어지는지 설명하고, 종료 실패와 FD 고갈을 프로세스 상태와 제한값에서 찾는 것입니다.

### 3단계 · kernel/ 01-02 ~ 01-07  `필수`

컨테이너는 새 기술이 아니라 조합입니다. namespace가 무엇을 가리고 cgroup이 무엇을 조이는지를 갈라 두면, Pod 하나가 죽은 이유를 애플리케이션과 커널 중 어디서 찾을지가 정해집니다. 이 단계의 여섯 편은 개념을 설명한 뒤 `/sys/fs/cgroup` 트리를 직접 여는 데까지 갑니다.

| 개념 | 어디서 |
|---|---|
| namespace 여덟 가지와 `unshare` | [namespace 실습](../02_os/kernel/01-05.namespace%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%208%EA%B0%80%EC%A7%80%20%EA%B2%A9%EB%A6%AC%EC%99%80%20unshare.md) |
| cgroup v2 — 단일 트리·컨트롤러·PSI·throttling | [cgroup v2 깊이](../02_os/kernel/01-02.cgroup%20v2%20%EA%B9%8A%EC%9D%B4.md) |
| cgroup 파일과 `requests`/`limits` 매핑 | [cgroup 파일시스템 실습](../02_os/kernel/01-04.cgroup%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%8B%A4%EC%8A%B5.md) |
| JVM 힙과 cgroup RSS가 갈리는 자리 | [cgroup 사례 — Endowus OOMKilled](../02_os/kernel/01-06.cgroup%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20OOMKilled.md) |
| mount propagation 네 가지와 CSI·HostPath | [마운트 네임스페이스와 propagation](../02_os/kernel/01-03.%EB%A7%88%EC%9A%B4%ED%8A%B8%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20propagation.md) |
| OverlayFS·copy-on-write와 user namespace | [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) |
| 재료가 아니라 조합이라는 관점 | [06-02](../02_os/book/learning-modern-linux/06-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%EC%83%88%EB%A1%9C%EC%9B%80%EC%9D%80%20%EC%9E%AC%EB%A3%8C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%EC%A1%B0%ED%95%A9%EC%97%90%20%EC%9E%88%EB%8B%A4.md) |
| 같은 메커니즘을 보안 경계로 읽기 | [Control Group](../08_cloud/book/container-security/03-01.Control%20Group%20%E2%80%94%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EC%A0%9C%ED%95%9C%ED%95%B4%20%EA%B5%B6%EA%B8%B0%EA%B8%B0%EB%A5%BC%20%EB%A7%89%EB%8B%A4.md) · [namespace와 루트 디렉토리](../08_cloud/book/container-security/04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md) |

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| cgroup namespace | 컨테이너 안에서 본 cgroup 경로가 호스트와 다른 이유 |
| hugetlbfs | 큰 페이지를 쓰는 워크로드의 메모리 회계 |

완료 기준은 JVM 힙 OOM과 cgroup OOMKilled를 구분해 제한 파일에서 원인을 확인하고, 컨테이너 writable layer와 볼륨 마운트 문제를 커널 파일시스템 경로로 설명하는 것입니다.



## 자원과 관측 · 4~5단계

> 죽지는 않는데 느린 경우를 다룹니다. 3단계까지가 "왜 멈췄나"라면 여기는 "왜 느린가"입니다.

### 4단계 · Systems Performance 2·6~9장  `필수`

느리다는 말은 진단이 아닙니다. 이 단계는 그 말을 사용률·포화·오류 셋으로 쪼개는 훈련입니다. 도구를 먼저 배우지 않고 방법론을 먼저 배우는 것이 이 책의 설계이고, 이 로드맵도 2장을 6~9장 앞에 둡니다.

| 개념 | 어디서 |
|---|---|
| 용어·모델·핵심 개념, 분석 방법론 20종 | [방법론 (1)](../02_os/book/systems-performance/02-01.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%281%29%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) · [(2)](../02_os/book/systems-performance/02-02.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%282%29%20%E2%80%94%20%EB%B6%84%EC%84%9D%20%EB%B0%A9%EB%B2%95%EB%A1%A0%2020%EC%A2%85.md) |
| 모델링·용량계획·통계·시각화 | [방법론 (3)](../02_os/book/systems-performance/02-03.%EB%B0%A9%EB%B2%95%EB%A1%A0%20%283%29%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EB%A7%81%C2%B7%EC%9A%A9%EB%9F%89%EA%B3%84%ED%9A%8D%C2%B7%ED%86%B5%EA%B3%84%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94.md) |
| CPU — 아키텍처·스케줄러·튜닝·관측 | [06-01](../02_os/book/systems-performance/06-01.CPU%20%281%29%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [06-04](../02_os/book/systems-performance/06-04.CPU%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%C2%B7%EC%8B%9C%EA%B0%81%ED%99%94.md) |
| 메모리 — 할당자·방법론·관측 | [07-01](../02_os/book/systems-performance/07-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%281%29%20%E2%80%94%20%EC%9A%A9%EC%96%B4%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [07-04](../02_os/book/systems-performance/07-04.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) |
| 파일 시스템 — 캐시와 파일시스템 유형 | [08-01](../02_os/book/systems-performance/08-01.%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%281%29%20%E2%80%94%20%EB%B0%B0%EA%B2%BD%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [08-04](../02_os/book/systems-performance/08-04.%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) |
| 디스크 — 아키텍처·방법론·관측 | [09-01](../02_os/book/systems-performance/09-01.%EB%94%94%EC%8A%A4%ED%81%AC%20%281%29%20%E2%80%94%20%EB%B0%B0%EA%B2%BD%C2%B7%EB%AA%A8%EB%8D%B8%C2%B7%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md) ~ [09-04](../02_os/book/systems-performance/09-04.%EB%94%94%EC%8A%A4%ED%81%AC%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) |
| 재는 것은 바깥이고 알고 싶은 것은 안이다 | [08-01](../02_os/book/learning-modern-linux/08-01.%EC%9E%AC%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EB%B0%94%EA%B9%A5%EC%9D%B4%EA%B3%A0%20%EC%95%8C%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EC%95%88%EC%9D%B4%EB%8B%A4.md) |

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| blk-cgroup·`io.max` | CPU·메모리처럼 디스크 대역을 제한하는 자리 |
| IRQ affinity·`irqbalance` | 인터럽트가 한 코어로 몰릴 때 무엇이 밀리는가 |

완료 기준은 낮은 CPU 사용률과 높은 지연이 함께 나타나는 원인을 실행 대기와 제한으로 나누고, 메모리·디스크 병목을 사용률·포화·오류로 분해하는 것입니다.

### 5단계 · Systems Performance 4·13~15장과 Container Security  `추천`

증상마다 맞는 창이 다릅니다. 상태를 조회할 것인지, 샘플링할 것인지, 이벤트를 추적할 것인지를 고르는 훈련이 앞이고 도구 사용법이 뒤입니다. 보안 경계를 같은 단계에 둔 이유는 관측과 제한이 결국 같은 커널 훅을 쓰기 때문입니다.

| 개념 | 어디서 |
|---|---|
| 관측 도구 커버리지·유형·관측 소스 | [04-01](../02_os/book/systems-performance/04-01.%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%20%281%29%20%E2%80%94%20%EB%8F%84%EA%B5%AC%20%EC%BB%A4%EB%B2%84%EB%A6%AC%EC%A7%80%C2%B7%EC%9C%A0%ED%98%95.md) ~ [04-03](../02_os/book/systems-performance/04-03.%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC%20%283%29%20%E2%80%94%20sar%C2%B7%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%8B%B1%20%EB%8F%84%EA%B5%AC%C2%B7%EA%B4%80%EC%B8%A1%EC%9D%98%20%EA%B4%80%EC%B8%A1.md) |
| perf — 서브커맨드·이벤트 소스·명령 | [13-01](../02_os/book/systems-performance/13-01.perf%20%281%29%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7%EC%84%9C%EB%B8%8C%EC%BB%A4%EB%A7%A8%EB%93%9C%C2%B7%EC%9B%90%EB%9D%BC%EC%9D%B4%EB%84%88.md) ~ [13-03](../02_os/book/systems-performance/13-03.perf%20%283%29%20%E2%80%94%20%EB%AA%85%EB%A0%B9.md) |
| Ftrace — tracefs·트레이서·프론트엔드 | [14-01](../02_os/book/systems-performance/14-01.Ftrace%20%281%29%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7tracefs%C2%B7%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%9F%AC.md) ~ [14-03](../02_os/book/systems-performance/14-03.Ftrace%20%283%29%20%E2%80%94%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C.md) |
| BPF — BCC와 bpftrace | [15-01](../02_os/book/systems-performance/15-01.BPF%20%281%29%20%E2%80%94%20%EA%B0%9C%EC%9A%94%C2%B7BCC%20vs%20bpftrace%C2%B7BCC.md) ~ [15-03](../02_os/book/systems-performance/15-03.BPF%20%283%29%20%E2%80%94%20bpftrace%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%C2%B7%EB%A0%88%ED%8D%BC%EB%9F%B0%EC%8A%A4.md) |
| 시스템 콜·권한·capability | [02-01](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) |
| 샌드박싱 세 갈래, 설정 하나로 무너지는 경계 | [08-01](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) · [09-01](../08_cloud/book/container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) |
| user namespace로 UID 가르기 | [OverlayFS와 user namespace](../02_os/kernel/01-07.OverlayFS%EC%99%80%20user%20namespace%20%E2%80%94%20Netflix%20UID%20%EA%B2%A9%EB%A6%AC.md) |

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| Landlock | LSM 설정 없이 프로세스가 스스로 권한을 좁히는 방법 |
| eBPF 검증기의 거절 조건 | 문법이 맞는데도 프로그램이 로드되지 않는 이유 |

완료 기준은 증상에 맞춰 상태 조회·샘플링·이벤트 추적 중 하나를 고르고, 컨테이너 권한 요청이 넓히는 커널 공격면을 설명하는 것입니다.



## 커널 내부 · 6단계

> 앞의 다섯 단계가 커널을 바깥에서 봤다면, 여기서는 안으로 들어갑니다. 필요가 생겼을 때 여는 자리이지 순서상 반드시 지나야 하는 자리가 아닙니다.

### 6단계 · Linux Kernel Programming 6~13장  `추천`

운영 증상을 커널 자료구조까지 잇고 싶을 때 엽니다. 4단계에서 "run queue가 길다"까지 갔다면 여기서 그 run queue가 어떤 스케줄링 클래스로 나뉘는지를 봅니다. 커널 모듈을 직접 쓸 일이 없어도, 잠금과 할당자를 보고 나면 성능 도구의 출력이 다르게 읽힙니다.

| 개념 | 어디서 |
|---|---|
| VM split·주소 변환·KASLR, 물리 메모리와 NUMA | [07-01](../02_os/book/linux-kernel-programming/07-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EA%B4%80%EB%A6%AC%20%281%29%20%E2%80%94%20VM%20split%EA%B3%BC%20%EC%A3%BC%EC%86%8C%20%EB%B3%80%ED%99%98.md) ~ [07-03](../02_os/book/linux-kernel-programming/07-03.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EA%B4%80%EB%A6%AC%20%283%29%20%E2%80%94%20%EB%AC%BC%EB%A6%AC%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20NUMA.md) |
| 페이지 할당자·GFP 플래그, slab과 `kmalloc` 낭비 | [08-01](../02_os/book/linux-kernel-programming/08-01.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%281%29%20%E2%80%94%20%ED%8E%98%EC%9D%B4%EC%A7%80%20%ED%95%A0%EB%8B%B9%EC%9E%90%EC%99%80%20GFP%20%ED%94%8C%EB%9E%98%EA%B7%B8.md) · [08-02](../02_os/book/linux-kernel-programming/08-02.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%282%29%20%E2%80%94%20slab%20%ED%95%A0%EB%8B%B9%EC%9E%90%EC%99%80%20kmalloc%20%EB%82%AD%EB%B9%84.md) |
| demand paging과 OOM killer | [09-03](../02_os/book/linux-kernel-programming/09-03.%EB%A9%94%EB%AA%A8%EB%A6%AC%20%ED%95%A0%EB%8B%B9%20%285%29%20%E2%80%94%20demand%20paging%EA%B3%BC%20OOM%20killer.md) |
| 모듈식 스케줄링 클래스와 CFS, 선점 | [10-01](../02_os/book/linux-kernel-programming/10-01.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%281%29%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%20%EA%B8%B0%EC%B4%88%EC%99%80%20%ED%9D%90%EB%A6%84%20%EC%8B%9C%EA%B0%81%ED%99%94.md) ~ [10-03](../02_os/book/linux-kernel-programming/10-03.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%283%29%20%E2%80%94%20%EC%A0%95%EC%B1%85%20%EC%A7%88%EC%9D%98%EC%99%80%20%EC%84%A0%EC%A0%90%C2%B7%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%EC%A7%84%EC%9E%85%EC%A0%90.md) |
| CPU affinity와 cgroups v2 CPU 제약 | [11-01](../02_os/book/linux-kernel-programming/11-01.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%284%29%20%E2%80%94%20CPU%20affinity%EC%99%80%20%EC%A0%95%EC%B1%85%C2%B7%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%20%EC%84%A4%EC%A0%95.md) ~ [11-03](../02_os/book/linux-kernel-programming/11-03.CPU%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%20%286%29%20%E2%80%94%20cgroups%20CPU%20%EC%A0%9C%EC%95%BD%EA%B3%BC%20RTOS.md) |
| 임계 구역·data race, mutex와 spinlock 선택 | [12-01](../02_os/book/linux-kernel-programming/12-01.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%281%29%20%E2%80%94%20%EC%9E%84%EA%B3%84%20%EA%B5%AC%EC%97%AD%EA%B3%BC%20data%20race.md) ~ [12-03](../02_os/book/linux-kernel-programming/12-03.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%283%29%20%E2%80%94%20spinlock%EA%B3%BC%20%EC%9D%B8%ED%84%B0%EB%9F%BD%ED%8A%B8.md) |
| atomic·refcount, lock-free와 lockdep·memory barrier | [13-01](../02_os/book/linux-kernel-programming/13-01.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%284%29%20%E2%80%94%20atomic%C2%B7refcount%EC%99%80%20RMW%20%EC%97%B0%EC%82%B0%EC%9E%90.md) ~ [13-03](../02_os/book/linux-kernel-programming/13-03.%EC%BB%A4%EB%84%90%20%EB%8F%99%EA%B8%B0%ED%99%94%20%286%29%20%E2%80%94%20lock-free%EC%99%80%20lockdep%C2%B7memory%20barrier.md) |

**정독 노트는 13장 동기화에서 멈춥니다.** 학습 순서 표의 6단계 키워드에 적힌 VFS 구현·io_uring·LSM·KVM은 노트가 다루지 않는 축이고, 그 자리가 아래 표입니다. 인터럽트와 RCU는 12·13장이 잠금 맥락에서 다루므로 그쪽으로 가면 됩니다.

| 자료 밖 키워드 | 무엇을 검색할지 |
|---|---|
| kdump·crash 분석 | 커널이 죽은 뒤 남는 것을 어떻게 읽는가 |
| io_uring 제출·완료 큐 | `epoll` 을 대체하는 모델이 시스템 콜을 어떻게 줄이는가 |
| VFS 구현과 LSM 훅 | 마운트와 보안 모듈이 커널 어디에 끼워지는가 |

완료 기준은 운영 증상을 관련 커널 자료구조와 실행 경로까지 추적하는 것입니다.



## 로드맵에 넣지 않은 것

> 다른 문서가 정본이거나, 선후 관계가 없어 순서를 말할 수 없는 것들입니다.

### 네트워크 패킷 경로

veth·bridge·netfilter·conntrack·라우팅은 [네트워크 로드맵](network-roadmap.md)이 다섯 단계로 맡습니다. 이 로드맵은 3단계의 network namespace에서 멈추고 넘깁니다. `02_os/networking/` 네 편도 그쪽 소관입니다. 두 곳에 같은 내용을 두면 어느 쪽이 정본인지 흐려집니다.

### 커널 소스 빌드와 모듈 개발 환경

《Linux Kernel Programming》 1~5장은 커널을 내려받아 설정하고 빌드해 첫 모듈을 올리는 과정입니다. 운영 증상을 읽는 축이 아니라 개발 환경을 세우는 축이라 단계에 넣지 않았습니다. 커널 모듈을 직접 쓸 일이 생겼을 때 6단계 앞에 붙입니다.

### 클라우드 가상화와 벤치마킹

《Systems Performance》 11장(클라우드 컴퓨팅)과 12장(벤치마킹)은 순서에 넣지 않았습니다. 11장은 하드웨어 가상화와 OS 가상화를 비교하는 축이라 컨테이너를 이미 아는 상태에서 읽어야 값이 있고, 12장은 실습 표에만 걸었습니다. 벤치마킹은 배우는 순서가 아니라 재야 할 일이 생겼을 때 여는 자리입니다.

### 컨테이너 이미지와 공급망

《Container Security》 6·7장(이미지 해부·공급망·CVE)은 런타임이 아니라 빌드 측면입니다. 02_os MOC가 이미지 포맷과 OCI 표준을 `07_devops/` 소관으로 정해 두었으므로 여기서는 순서에 넣지 않습니다.



## 경계

> 이 문서가 무엇을 정하고 무엇을 정하지 않는지, 그리고 인접 문서와 어디서 맞닿는지입니다.

이 문서는 **읽기 순서**를 정합니다. 어느 자료가 어느 폴더에 있는지, 폴더 사이 경계가 어디인지는 [02_os MOC](../02_os/README.md)가 맡습니다. 둘을 한 문서에 두면 자료가 늘 때마다 순서까지 다시 써야 합니다.

단계 번호는 **의존 순서**이지 진도가 아닙니다. 실제 장애를 만났다면 해당 증상 단계로 바로 들어가고, 이해에 필요한 선행만 되돌아봅니다. 서비스가 안 뜨면 1단계, 종료가 이상하면 2단계, OOMKilled는 3단계, 느려짐은 4단계가 첫 자리입니다.

맞닿는 문서가 둘 있습니다. 패킷이 namespace를 떠난 뒤는 [네트워크 로드맵](network-roadmap.md)이, 오브젝트 수준의 배포와 운영은 [Kubernetes 로드맵](k8s-roadmap.md)이 맡습니다. 3단계와 5단계가 각각 그 둘과 맞닿는 자리입니다.

**Kubernetes 로드맵과는 같은 증상을 양쪽에서 봅니다.** OOMKilled는 그쪽 7단계와 이쪽 3단계에 모두 나오는데, 그쪽이 `kubectl describe` 로 보이는 것을 다루고 이쪽이 cgroup 파일로 보이는 것을 다룹니다. 두 문서를 같이 여는 것이 정상이고, 중복이 아니라 층이 다른 것입니다.



## 책 읽기 흐름

> 단계 표에 연결된 책을 처음 읽는 시점과 집중할 범위를 표시합니다.

![OS 책 읽기 흐름](_assets/os-books.svg)
