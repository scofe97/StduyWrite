---
title: 02_os/linux-kernel-programming — 커널 개발자 관점의 리눅스 내부
tags: [moc, linux, kernel, lkm, kernel-module, memory-management, scheduler, synchronization]
status: final
related:
  - ../../README.md
  - ../../kernel/README.md
updated: 2026-06-03
---


# 02_os/linux-kernel-programming
---
> 『Linux Kernel Programming, 2판』(Kaiwan N. Billimoria, Packt)을 따라 커널 개발자 관점에서 리눅스 내부를 정리합니다. LKM(Loadable Kernel Module) 프레임워크로 커널 빌드·모듈 작성부터 메모리 관리·CPU 스케줄러·커널 동기화까지 다룹니다. 6.1 LTS 커널이 기준입니다.

이웃한 `kernel/` 폴더가 "K8s 운영자 관점"에서 커널 메커니즘을 본다면, 본 폴더는 "커널 모듈 작성자 관점"에서 한 단계 더 안으로 들어갑니다. 같은 메커니즘(예: cgroups)이 양쪽에서 등장하면 서로 교차참조합니다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 00-00 | [책 개요와 학습 로드맵](./00-00.책%20개요와%20학습%20로드맵.md) | 이 책은 무엇을 어떤 순서로 다루는가? 3섹션·13챕터의 큰 줄기와 학습 환경(6.1 LTS·VM)은? |
| 01-00 | [커널 개발 워크스페이스 셋업](./01-00.커널%20개발%20워크스페이스%20셋업.md) | 커널 실습 환경은 어떻게 꾸리는가? VM 게스트를 쓰는 이유, git clone, ctags/cscope 인덱싱은? (Ch 1 + 온라인 챕터) |
| 02-01 | [커널 빌드 (1) — 버전 체계와 소스 트리 종류](./02-01.커널%20빌드%20(1)%20—%20버전%20체계와%20소스%20트리%20종류.md) | `uname -r` 은 어떻게 읽는가? 릴리스는 왜 시간 기반인가? -next/-rc/stable/LTS/SLTS 는 어떻게 다르고 어느 걸 써야 하는가? (Ch 2 전반) |
| 02-02 | [커널 빌드 (2) — 다운로드·설정과 Kconfig/Kbuild](./02-02.커널%20빌드%20(2)%20—%20다운로드·설정과%20Kconfig·Kbuild.md) | 소스를 어떻게 받아 설정하는가? `CONFIG_FOO` 의 y/m/n, defconfig vs localmodconfig, menuconfig, 내 메뉴 항목 추가는? (Ch 2 후반) |
| 03-01 | [커널 빌드 (3) — 빌드·모듈 설치·initramfs·GRUB](./03-01.커널%20빌드%20(3)%20—%20빌드·모듈%20설치·initramfs·GRUB.md) | `make` 가 만드는 vmlinux/bzImage 차이는? 모듈은 어디에 설치되는가? initramfs 는 부팅의 닭-달걀 문제를 어떻게 푸는가? GRUB 커스터마이징은? (Ch 3 전반) |
| 03-02 | [커널 빌드 (4) — Raspberry Pi 크로스 컴파일과 빌드 팁](./03-02.커널%20빌드%20(4)%20—%20Raspberry%20Pi%20크로스%20컴파일과%20빌드%20팁.md) | 호스트와 다른 CPU 커널은 어떻게 빌드하는가? `ARCH`/`CROSS_COMPILE` 의 역할, 크로스 툴체인, deb 패키징은? (Ch 3 후반) |
| 04-01 | [첫 커널 모듈 (1) — 커널 아키텍처와 LKM](./04-01.첫%20커널%20모듈%20(1)%20—%20커널%20아키텍처와%20LKM.md) | 유저/커널 공간은 어떻게 나뉘는가? 시스템 콜·monolithic 은? LKM 은 왜 쓰며 Hello world 모듈을 어떻게 빌드·적재·제거하는가? (Ch 4 전반) |
| 04-02 | [첫 커널 모듈 (2) — printk 로깅과 Makefile](./04-02.첫%20커널%20모듈%20(2)%20—%20printk%20로깅과%20Makefile.md) | printk 는 어디로 출력되는가? 8개 로그 레벨·pr_* 매크로·dynamic debug·rate limiting 은? 모듈 Makefile 의 `obj-m`·재귀 빌드는? (Ch 4 후반) |
| 05-01 | [첫 커널 모듈 (3) — Makefile·크로스 컴파일·라이브러리식 기능](./05-01.첫%20커널%20모듈%20(3)%20—%20Makefile·크로스%20컴파일·라이브러리식%20기능.md) | 더 나은 Makefile·디버그 커널은? 모듈 크로스 컴파일이 왜 4번 걸리며 커널 ABI 규칙은? 라이브러리식 기능(링킹·모듈 스태킹)과 모듈 파라미터는? (Ch 5 전반) |
| 05-02 | [첫 커널 모듈 (4) — 시스템 정보·보안·자동 적재](./05-02.첫%20커널%20모듈%20(4)%20—%20시스템%20정보·보안·자동%20적재.md) | 포터블 코드·라이선스(GPL/dual)는? 왜 커널에서 FP 금지인가? 부팅 시 자동 적재, 모듈 서명·sysctl·lockdown 보안은? (Ch 5 후반) |
| 06-01 | [프로세스와 스레드 (1) — 컨텍스트·VAS·스택](./06-01.프로세스와%20스레드%20(1)%20—%20컨텍스트·VAS·스택.md) | 프로세스 vs 인터럽트 컨텍스트는? VAS 세그먼트(텍스트·힙·스택)는? 왜 스레드마다 유저·커널 두 스택인가? 스택은 어떻게 보는가(proc·GDB·eBPF)? (Ch 6 전반) |
| 06-02 | [프로세스와 스레드 (2) — task 구조와 current](./06-02.프로세스와%20스레드%20(2)%20—%20task%20구조와%20current.md) | task_struct 는 무엇을 담는가? `current` 매크로·`in_task()` 컨텍스트 판별은? task 리스트 순회와 TGID/PID 로 프로세스·스레드 구분은? (Ch 6 후반) |
| 07-01 | [메모리 관리 (1) — VM split과 주소 변환](./07-01.메모리%20관리%20(1)%20—%20VM%20split과%20주소%20변환.md) | VM split 은 무엇이며 왜 필요한가? 64비트 가상 주소는 왜 비트맵이고 KVA/UVA 구분은? MMU 의 주소 변환은? (Ch 7 전반) |
| 07-02 | [메모리 관리 (2) — VAS 검사와 KASLR](./07-02.메모리%20관리%20(2)%20—%20VAS%20검사와%20KASLR.md) | `/proc/PID/maps` 7개 필드·VMA 는? procmap·커널 VAS 매크로(`PAGE_OFFSET`)는? [K]ASLR 랜덤화는? (Ch 7 중반) |
| 07-03 | [메모리 관리 (3) — 물리 메모리와 NUMA](./07-03.메모리%20관리%20(3)%20—%20물리%20메모리와%20NUMA.md) | 노드·존·페이지 프레임 계층은? NUMA vs UMA 는? RAM direct-map 과 변환 API, sparsemem 모델은? (Ch 7 후반) |
| 08-01 | [메모리 할당 (1) — 페이지 할당자와 GFP 플래그](./08-01.메모리%20할당%20(1)%20—%20페이지%20할당자와%20GFP%20플래그.md) | 페이지 할당자(BSA)는 어떻게 동작하나? buddy system freelist·order·분할/병합은? 내부 단편화는 왜 치명적이고 GFP_KERNEL/ATOMIC 은 언제 쓰나? (Ch 8 전반) |
| 08-02 | [메모리 할당 (2) — slab 할당자와 kmalloc 낭비](./08-02.메모리%20할당%20(2)%20—%20slab%20할당자와%20kmalloc%20낭비.md) | slab 은 왜 page 위에 layered 되나? kmalloc/kzalloc/kfree·kmalloc-N 캐시는? 한 번에 4MB 한계와 ksize 낭비 측정, devm_·SLUB 는? (Ch 8 후반) |
| 09-01 | [메모리 할당 (3) — custom slab cache와 vmalloc](./09-01.메모리%20할당%20(3)%20—%20custom%20slab%20cache와%20vmalloc.md) | 자주 쓰는 객체용 전용 cache 는 어떻게 만드나? kmem_cache_create/alloc/free/destroy·생성자·shrinker 는? vmalloc 가상 연속·kvmalloc 폴백은? (Ch 9 전반) |
| 09-02 | [메모리 할당 (4) — API 선택과 memory reclaim](./09-02.메모리%20할당%20(4)%20—%20API%20선택과%20memory%20reclaim.md) | 어느 할당 API 를 언제 쓰나(양·타입)? kswapd·zone watermark(min/low/high) 회수는? MGLRU 다세대 LRU·DAMON 접근 모니터는? (Ch 9 중반) |
| 09-03 | [메모리 할당 (5) — demand paging과 OOM killer](./09-03.메모리%20할당%20(5)%20—%20demand%20paging과%20OOM%20killer.md) | malloc 성공이 왜 물리 할당이 아닌가(demand paging)? 페이지 폴트→OOM 흐름은? overcommit 3정책·OOM score·cgroups 메모리 제어는? (Ch 9 후반) |
| 10-01 | [CPU 스케줄러 (1) — 스케줄링 기초와 흐름 시각화](./10-01.CPU%20스케줄러%20(1)%20—%20스케줄링%20기초와%20흐름%20시각화.md) | 스케줄 단위(KSE)는 왜 스레드인가? 프로세스 상태 머신(R·S·D·T·Z·X)·POSIX 정책 5종·우선순위 스케일은? perf/gnome-system-monitor/ftrace 흐름 시각화는? (Ch 10 전반) |
| 10-02 | [CPU 스케줄러 (2) — 모듈식 스케줄링 클래스와 CFS](./10-02.CPU%20스케줄러%20(2)%20—%20모듈식%20스케줄링%20클래스와%20CFS.md) | 코어 스케줄러는 5개 클래스를 어떻게 순회하나? runqueue 는 왜 코어당·클래스당인가? CFS 의 vruntime·rb-tree·dynamic timeslice·EEVDF 는? (Ch 10 중반) |
| 10-03 | [CPU 스케줄러 (3) — 정책 질의와 선점·스케줄러 진입점](./10-03.CPU%20스케줄러%20(3)%20—%20정책%20질의와%20선점·스케줄러%20진입점.md) | chrt 로 정책·우선순위를 어떻게 질의하나? preemptible kernel·PREEMPT_DYNAMIC 은? 누가·언제 schedule()을 부르나(TIF_NEED_RESCHED)·context switch 는? (Ch 10 후반) |
| 11-01 | [CPU 스케줄러 (4) — CPU affinity와 정책·우선순위 설정](./11-01.CPU%20스케줄러%20(4)%20—%20CPU%20affinity와%20정책·우선순위%20설정.md) | affinity mask 는 왜 per-thread 인가? sched_{g,s}etaffinity·taskset·kthread affinity 해킹은? 커널 안 sched_set_fifo 3 API·threaded IRQ 는? (Ch 11 전반) |
| 11-02 | [CPU 스케줄러 (5) — cgroups v2](./11-02.CPU%20스케줄러%20(5)%20—%20cgroups%20v2.md) | cgroups 는 CFS 의 어떤 불공정을 푸나? 컨트롤러·단일 계층·top-down·subtree_control 은? systemd slice/scope·namespace·컨테이너는? (Ch 11 중반) |
| 11-03 | [CPU 스케줄러 (6) — cgroups CPU 제약과 RTOS](./11-03.CPU%20스케줄러%20(6)%20—%20cgroups%20CPU%20제약과%20RTOS.md) | cgroups CPU 제약 두 방식(systemd CPUQuota·수동 cpu.max)은? 제약은 왜 saturated 일 때만? RTOS 결정성·RTL(PREEMPT_RT) 전환·ghOSt 는? (Ch 11 후반) |
| 12-01 | [커널 동기화 (1) — 임계 구역과 data race](./12-01.커널%20동기화%20(1)%20—%20임계%20구역과%20data%20race.md) | 임계 구역의 두 조건은? atomicity 는 왜 i++ 조차 위험한가? 락은 어떻게 직렬화하나? data race(LKMM·KCSAN)·동시성 4원인·deadlock 가이드라인은? (Ch 12 전반) |
| 12-02 | [커널 동기화 (2) — mutex와 spinlock 선택](./12-02.커널%20동기화%20(2)%20—%20mutex와%20spinlock%20선택.md) | mutex(sleep)와 spinlock(spin)의 차이는? 어느 락을 언제 쓰나? mutex 초기화·API·변형(interruptible/trylock)·priority inversion·RT-mutex 는? (Ch 12 중반) |
| 12-03 | [커널 동기화 (3) — spinlock과 인터럽트](./12-03.커널%20동기화%20(3)%20—%20spinlock과%20인터럽트.md) | spinlock 사용·sleep-in-atomic 버그는? 인터럽트와 race 시 self-deadlock 과 _irq 변형은? _irqsave 마스크 보존·_bh·API 선택은? (Ch 12 후반) |
| 13-01 | [커널 동기화 (4) — atomic·refcount와 RMW 연산자](./13-01.커널%20동기화%20(4)%20—%20atomic·refcount와%20RMW%20연산자.md) | 정수는 왜 atomic_t·refcount_t 가 효율적인가? refcount 는 어떻게 IoF·UAF 를 막나? RMW 비트 연산자(set_bit)·bitmask 검색은? (Ch 13 전반) |
| 13-02 | [커널 동기화 (5) — reader-writer spinlock과 캐시 효과](./13-02.커널%20동기화%20(5)%20—%20reader-writer%20spinlock과%20캐시%20효과.md) | rwlock 은 read-mostly 에 왜 유용하고 writer starvation 은? CPU 는 왜 cacheline 단위로 읽나? cache coherency·false sharing 은? (Ch 13 중반) |
| 13-03 | [커널 동기화 (6) — lock-free와 lockdep·memory barrier](./13-03.커널%20동기화%20(6)%20—%20lock-free와%20lockdep·memory%20barrier.md) | per-CPU·RCU 는 어떻게 lock-free 인가? RCU grace period·core API 는? lockdep 은 deadlock 을 어떻게 잡나? memory barrier 는? (Ch 13 후반) |



## 완간

전권(Ch 1~13) 정독 노트를 모두 작성했습니다. 섹션별 구성은 다음과 같습니다.

| 섹션 | 챕터 | 주제 | 노트 |
|------|------|------|------|
| 1 기초 | Ch 1~5 | 커널 개발 환경·빌드·첫 LKM | 00-00 ~ 05-02 (10편) |
| 2 핵심 | Ch 6~7 | 프로세스·스레드, 메모리 관리 | 06-01 ~ 07-03 (5편) |
| 2 핵심 | Ch 8~9 | 메모리 할당 (page·slab·vmalloc·OOM) | 08-01 ~ 09-03 (5편) |
| 2 핵심 | Ch 10~11 | CPU 스케줄러 (CFS·affinity·cgroups·RTOS) | 10-01 ~ 11-03 (6편) |
| 3 고급 | Ch 12~13 | 커널 동기화 (mutex·spinlock·atomic·RCU·lockdep) | 12-01 ~ 13-03 (6편) |



## 상위·이웃

- 상위: [02_os/ MOC](../../README.md)
- 이웃: [02_os/kernel/](../../kernel/README.md) — K8s 운영 관점의 커널 메커니즘(namespace·cgroup·/proc). 본서 Ch 6·7·11과 주제가 겹칩니다
