---
title: 02_os/systems-performance — 성능 분석가 관점의 시스템 성능
tags: [moc, performance, linux, kernel, observability, bpf, perf, ftrace, cloud]
status: draft
related:
  - ../README.md
  - ../linux-kernel-programming/README.md
  - ../kernel/README.md
  - ../networking/README.md
updated: 2026-06-04
---


# 02_os/systems-performance
---
> 『Systems Performance, 2판』(Brendan Gregg, Pearson/O'Reilly)을 따라 성능 분석가 관점에서 시스템·애플리케이션의 성능을 정리합니다. 리눅스를 주 예시로, 방법론·운영체제 내부부터 CPU·메모리·파일시스템·디스크·네트워크·클라우드, 그리고 고급 추적(perf·Ftrace·BPF)까지 다룹니다. "도구는 낡아도 방법론은 남는다"는 책의 설계를 따라, 도구 사용법보다 *시스템에 무엇을 묻는가* 에 무게를 둡니다.

이웃한 `linux-kernel-programming/` 폴더가 "커널 모듈 작성자 관점"으로, `kernel/` 폴더가 "K8s 운영자 관점"으로 커널을 본다면, 본 폴더는 "성능 분석가 관점"으로 같은 메커니즘을 봅니다. 같은 주제(예: CPU 스케줄링·가상 메모리)가 여러 폴더에서 등장하면 서로 교차참조합니다.



## 문서

| 장 | 제목 | 핵심 질문 |
|----|------|----------|
| 00-00 | [책 개요와 학습 로드맵](./00-00.책%20개요와%20학습%20로드맵.md) | 이 책은 무엇을 어떤 순서로 다루는가? unknown unknowns·durable vs faster-changing 설계와 16장 4그룹 배치는? |
| 01-01 | [서론 (1) — 성능이란 무엇이고 왜 어려운가](./01-01.서론%20(1)%20—%20성능이란%20무엇이고%20왜%20어려운가.md) | 풀 스택은 어디까지인가? 누가·언제·어느 관점에서 보는가? 성능이 주관적·복잡·다중 원인·다중 이슈로 어려운 까닭과, 모호함을 정량화하는 지연시간은? (Ch 1.1~1.6) |
| 01-02 | [서론 (2) — 관측·실험·방법론·케이스](./01-02.서론%20(2)%20—%20관측·실험·방법론·케이스.md) | 관측 vs 실험 두 손은? 카운터·프로파일링·플레임그래프·트레이싱(정적/동적·BPF)은? 60초 체크리스트와 두 케이스 스터디로 도구가 어떻게 맞물리는가? (Ch 1.7~1.11) |
| 02-01 | [방법론 (1) — 용어·모델·핵심 개념](./02-01.방법론%20(1)%20—%20용어·모델·핵심%20개념.md) | IOPS·지연·사용률·포화는? 시간 스케일·트레이드오프·확장성(knee point)·캐싱·known-unknowns는? "100% busy ≠ 100% capacity"와 두 분석 관점은? (Ch 2.1~2.4) |
| 02-02 | [방법론 (2) — 분석 방법론 20종](./02-02.방법론%20(2)%20—%20분석%20방법론%2020종.md) | anti-method 3종은? 문제 기술·과학적 방법은? USE·RED·워크로드 특성 파악·드릴다운·지연 분석·정적 튜닝·성능 만트라는? (Ch 2.5) |
| 02-03 | [방법론 (3) — 모델링·용량계획·통계·시각화](./02-03.방법론%20(3)%20—%20모델링·용량계획·통계·시각화.md) | Amdahl·USL·큐잉 이론(M/D/1 60%)은? 용량 계획은? 평균의 함정·백분위·다봉분포는? 라인·산점도·히트맵은? (Ch 2.6~2.10) |
| 03-01 | [운영체제 (1) — 커널·시스템 콜·인터럽트·프로세스](./03-01.운영체제%20(1)%20—%20커널·시스템%20콜·인터럽트·프로세스.md) | 커널/유저 모드·모드 전환 vs 컨텍스트 전환은? 시스템 콜(ioctl·mmap·brk·futex)은? 비동기/동기 인터럽트·top/bottom half는? 프로세스 수명주기·COW·스택 트레이스는? (Ch 3.1~3.2.7) |
| 03-02 | [운영체제 (2) — 가상메모리·스케줄러·파일시스템·I/O](./03-02.운영체제%20(2)%20—%20가상메모리·스케줄러·파일시스템·I/O.md) | 가상 메모리·스와핑/페이징은? 스케줄러는 CPU/I/O-bound를 어떻게 다루나? VFS·I/O 스택·캐시 층은? 멀티프로세서·IPI·선점·cgroups는? (Ch 3.2.8~3.2.17) |
| 03-03 | [운영체제 (3) — 커널 구현·Linux 발전사·BPF](./03-03.운영체제%20(3)%20—%20커널%20구현·Linux%20발전사·BPF.md) | Unix·BSD·Solaris의 성능 발전은? Linux 발전사(CFS·io_uring 등)는? systemd·KPTI(Meltdown)·Extended BPF는? unikernel·microkernel·커널 비교는? (Ch 3.3~3.6) |
| 04-01 | [관측 도구 (1) — 도구 커버리지·유형](./04-01.관측%20도구%20(1)%20—%20도구%20커버리지·유형.md) | 정적 도구·위기 도구(crisis tools)는 왜 미리 갖추나? 도구 두 축(system-wide/per-process·카운터/이벤트)은? 고정 카운터·프로파일링(99Hz)·트레이싱·모니터링의 오버헤드는? (Ch 4.1~4.2) |
| 04-02 | [관측 도구 (2) — 관측 소스](./04-02.관측%20도구%20(2)%20—%20관측%20소스.md) | /proc·/sys·delay accounting·netlink는? 트레이싱 소스 2×2(tracepoints·kprobes·uprobes·USDT)는? 안정 vs 불안정 API는? PMC·precise events는? (Ch 4.3) |
| 04-03 | [관측 도구 (3) — sar·트레이싱 도구·관측의 관측](./04-03.관측%20도구%20(3)%20—%20sar·트레이싱%20도구·관측의%20관측.md) | sar 설정·라이브·sadf 출력 형식은? perf·Ftrace·BPF 분업은? 도구·통계·문서를 왜 "건강한 회의"로 대해야 하나? (Ch 4.4~4.6) |
| 05-01 | [애플리케이션 (1) — 기초와 성능 기법](./05-01.애플리케이션%20(1)%20—%20기초와%20성능%20기법.md) | 앱 이해 출발 질문·성능 목표·Apdex·Big O는? I/O 크기·캐싱·버퍼링·동시성/병렬성·동기화(mutex·RCU)·해시테이블·논블로킹 I/O·바인딩은? (Ch 5.1~5.2) |
| 05-02 | [애플리케이션 (2) — 언어·방법론](./05-02.애플리케이션%20(2)%20—%20언어·방법론.md) | 컴파일·인터프리터·VM·GC의 성능·관측 차이는? CPU/off-CPU 프로파일링·플레임 그래프·syscall 분석·스레드 상태 9가지·락·분산 트레이싱은? (Ch 5.3~5.4) |
| 05-03 | [애플리케이션 (3) — 관측 도구·gotchas](./05-03.애플리케이션%20(3)%20—%20관측%20도구·gotchas.md) | perf·profile·offcputime·strace·execsnoop·syscount·bpftrace는? 심볼 누락(strip·JIT)·스택 누락(frame pointer)은 어떻게 고치나? (Ch 5.5~5.6) |
| 06-01 | [CPU (1) — 용어·모델·핵심 개념](./06-01.CPU%20(1)%20—%20용어·모델·핵심%20개념.md) | 프로세서·코어·하드웨어 스레드·논리 CPU는? 클럭·파이프라인·분기예측·IPC·사용률·포화·우선순위 역전·멀티스레딩은? (Ch 6.1~6.3) |
| 06-02 | [CPU (2) — 아키텍처·스케줄러](./06-02.CPU%20(2)%20—%20아키텍처·스케줄러.md) | P/C-state·CPU 캐시(연관성·일관성)·MMU/TLB·인터커넥트·PMC·GPU는? 스케줄러·스케줄링 클래스(RT·CFS·Deadline)·NUMA는? (Ch 6.4) |
| 06-03 | [CPU (3) — 방법론·실험·튜닝](./06-03.CPU%20(3)%20—%20방법론·실험·튜닝.md) | USE·워크로드 특성·프로파일링·사이클 분석·우선순위 튜닝·CPU 바인딩은? 마이크로벤치마킹은? 컴파일러·governor·cgroups·BIOS 튜닝은? (Ch 6.5·6.8·6.9) |
| 06-04 | [CPU (4) — 관측 도구·시각화](./06-04.CPU%20(4)%20—%20관측%20도구·시각화.md) | uptime/load average·PSI·mpstat·turbostat·pmcarch·perf·profile·runqlat는? 사용률 히트맵·subsecond-offset·플레임 그래프·FlameScope는? (Ch 6.6~6.7) |
| 07-01 | [메모리 (1) — 용어·핵심 개념](./07-01.메모리%20(1)%20—%20용어·핵심%20개념.md) | 가상 메모리·페이징(파일시스템 vs anonymous)·demand paging(minor/major fault)·overcommit·프로세스 스와핑·WSS는? 페이지 네 상태는? (Ch 7.1~7.2) |
| 07-02 | [메모리 (2) — 아키텍처·할당자](./07-02.메모리%20(2)%20—%20아키텍처·할당자.md) | DRAM·UMA/NUMA·DDR·MMU/TLB는? free list·kswapd·OOM·주소 공간은? slab·SLUB·glibc·TCMalloc·jemalloc은? (Ch 7.3) |
| 07-03 | [메모리 (3) — 방법론·튜닝](./07-03.메모리%20(3)%20—%20방법론·튜닝.md) | USE·사용 특성화·leak 탐지(누수 vs 증가)·WSS 추정은? swappiness·overcommit·huge pages·NUMA 바인딩·자원 제어는? (Ch 7.4·7.6) |
| 07-04 | [메모리 (4) — 관측 도구](./07-04.메모리%20(4)%20—%20관측%20도구.md) | vmstat·PSI·swapon·sar·slabtop·numastat·pmap(PSS)·perf(페이지 폴트 플레임 그래프)·drsnoop·wss·bpftrace는? (Ch 7.5) |
| 08-01 | [파일 시스템 (1) — 배경·핵심 개념](./08-01.파일%20시스템%20(1)%20—%20배경·핵심%20개념.md) | 왜 디스크가 아니라 파일 시스템 지연을 보나? 논리 vs 물리 I/O·캐싱·랜덤 vs 순차·미리읽기·되쓰기·동기 쓰기·raw/direct I/O·mmap·메타데이터는? (Ch 8.1~8.3) |
| 08-02 | [파일 시스템 (2) — 아키텍처·캐시·파일시스템 유형](./08-02.파일%20시스템%20(2)%20—%20아키텍처·캐시·파일시스템%20유형.md) | I/O 스택은 캐시 적중 여부로 어떻게 갈리나? VFS·네 캐시(page·buffer·dentry·inode)·저널링·COW·스크러빙·ext4/XFS/ZFS/btrfs·볼륨과 풀은? (Ch 8.4) |
| 08-03 | [파일 시스템 (3) — 방법론·실험·튜닝](./08-03.파일%20시스템%20(3)%20—%20방법론·실험·튜닝.md) | 방법론 8종(지연 분석 1순위)·캐시 튜닝·워크로드 분리는? dd/Bonnie/fio/FileBench와 캐시 플러시는? posix_fadvise·ext4·ZFS 튜닝은? (Ch 8.5·8.7·8.8) |
| 08-04 | [파일 시스템 (4) — 관측 도구](./08-04.파일%20시스템%20(4)%20—%20관측%20도구.md) | mount·free·sar·strace·fatrace·opensnoop·filetop·cachestat·ext4dist·ext4slower·bpftrace는 스택의 어느 층을 보나? 적중률·분포·꼬리는? (Ch 8.6) |
| 09-01 | [디스크 (1) — 배경·모델·핵심 개념](./09-01.디스크%20(1)%20—%20배경·모델·핵심%20개념.md) | 같은 I/O 지연이 커널 기준·디스크 기준에서 왜 다른가? 시간 스케일·캐싱·랜덤vs순차·IOPS는 동등하지 않다·사용률(가상 디스크 오해)·포화·I/O wait는? (Ch 9.1~9.3) |
| 09-02 | [디스크 (2) — 아키텍처](./09-02.디스크%20(2)%20—%20아키텍처.md) | HDD 탐색·회전·SMR·sloth? SSD 비대칭·FTL·웨어레벨링? SCSI/SAS/SATA/FC/NVMe? RAID 레벨별 성능·read-modify-write? Linux 병합·I/O 스케줄러·blk-mq? (Ch 9.4) |
| 09-03 | [디스크 (3) — 방법론·시각화·실험·튜닝](./09-03.디스크%20(3)%20—%20방법론·시각화·실험·튜닝.md) | USE·워크로드 특성화·지연 분석·스케일링은? 라인·스캐터·히트맵으로 다봉·이상치를 어떻게 보나? dd/ioping/fio·ionice·cgroup blkio·튜너블은? (Ch 9.5·9.7~9.9) |
| 09-04 | [디스크 (4) — 관측 도구](./09-04.디스크%20(4)%20—%20관측%20도구.md) | iostat(await·%util·읽기쓰기 분리)·sar·PSI·pidstat(iodelay)·perf·biolatency(이봉)·biosnoop·biotop·biostacks·blktrace(D2C·I2D)·bpftrace·smartctl은? (Ch 9.6) |
| 10-01 | [네트워크 (1) — 배경·모델·핵심 개념](./10-01.네트워크%20(1)%20—%20배경·모델·핵심%20개념.md) | 인터페이스·컨트롤러·프로토콜 스택은? 캡슐화·MTU(점보 프레임)·지연 6종(ping vs TTFB)·버퍼링·버퍼블로트·백로그·혼잡 회피·사용률·로컬 연결은? (Ch 10.1~10.3) |
| 10-02 | [네트워크 (2) — 아키텍처](./10-02.네트워크%20(2)%20—%20아키텍처.md) | TCP 성능 기능·혼잡 제어(CUBIC·BBR)·TIME_WAIT·UDP·QUIC? 인터페이스·컨트롤러·스위치·방화벽? Linux 스택·연결 큐·GSO/TSO·NAPI·RSS/RPS·커널 바이패스? (Ch 10.4) |
| 10-03 | [네트워크 (3) — 방법론·실험·튜닝](./10-03.네트워크%20(3)%20—%20방법론·실험·튜닝.md) | USE(방향별)·워크로드 특성화·지연 분석·TCP 분석(포트 고갈)·패킷 스니핑은? ping·traceroute·iperf·tc netem은? sysctl·소켓 옵션(TCP_NODELAY) 튜닝은? (Ch 10.5·10.7·10.8) |
| 10-04 | [네트워크 (4) — 관측 도구](./10-04.네트워크%20(4)%20—%20관측%20도구.md) | ss(limited 플래그)·ip·nstat·sar·nicstat(USE)·ethtool·tcplife·tcptop·tcpretrans·bpftrace(소켓 층)·tcpdump·Wireshark는 어느 층을 보나? (Ch 10.6) |
| 11-01 | [클라우드 컴퓨팅 (1) — 배경](./11-01.클라우드%20컴퓨팅%20(1)%20—%20배경.md) | 인스턴스 유형(튜너블화)·수평 확장·자동 스케일링(과잉 프로비저닝·bursting)·스토리지(휘발성 vs 영속)·멀티테넌시(noisy neighbor)·Kubernetes는? (Ch 11.1) |
| 11-02 | [클라우드 컴퓨팅 (2) — 하드웨어 가상화](./11-02.클라우드%20컴퓨팅%20(2)%20—%20하드웨어%20가상화.md) | Xen·KVM·Nitro? guest exit가 왜 CPU 오버헤드인가? EPT/NPT·SR-IOV·balloon 드라이버? 호스트(자원)와 게스트(자체 커널·BPF) 관측 차이는? (Ch 11.2) |
| 11-03 | [클라우드 컴퓨팅 (3) — OS 가상화](./11-03.클라우드%20컴퓨팅%20(3)%20—%20OS%20가상화.md) | 컨테이너 = namespace(격리) + cgroup(제한)? 단일 커널의 장단점? CPU shares·bandwidth·bursting 함정? idle 컨테이너 iostat이 바쁜 까닭은? (Ch 11.3) |
| 11-04 | [클라우드 컴퓨팅 (4) — 경량 가상화·기타·비교](./11-04.클라우드%20컴퓨팅%20(4)%20—%20경량%20가상화·기타·비교.md) | Firecracker·Kata(MicroVM)? FaaS·Unikernel의 관측 도전은? 세 기술 비교 — 왜 관측성이 선택을 가르나(컨테이너=운영자, VM=엔드유저)? (Ch 11.4~11.6) |
| 12-01 | [벤치마킹 (1) — 배경·효과적 벤치마킹·실패 16가지](./12-01.벤치마킹%20(1)%20—%20배경·효과적%20벤치마킹·실패%2016가지.md) | 왜 벤치마크를 믿으면 안 되나? casual benchmarking(A 재려다 B 측정)·벤치마크 역설·benchmark special 등 실패 16가지와 효과적 벤치마킹 조건은? (Ch 12.1) |
| 12-02 | [벤치마킹 (2) — 벤치마킹 유형](./12-02.벤치마킹%20(2)%20—%20벤치마킹%20유형.md) | 마이크로(인공·단순)·시뮬레이션(매크로·Markov)·리플레이(틀린 수준 함정)·산업표준(TPC 가격/성능·SPEC)은 어떻게 다르고 언제 쓰나? (Ch 12.2) |
| 12-03 | [벤치마킹 (3) — 방법론·벤치마크 질문](./12-03.벤치마킹%20(3)%20—%20방법론·벤치마크%20질문.md) | passive(돌리고 잊기) vs active(도는 동안 분석, bonnie++ 사례)? CPU 프로파일링·USE·ramping load·sanity check·체크리스트("왜 2배 안 됐나?")·벤치마크 질문은? (Ch 12.3~12.4) |
| 13-01 | [perf (1) — 개요·서브커맨드·원라이너](./13-01.perf%20(1)%20—%20개요·서브커맨드·원라이너.md) | perf는 왜 perf_events의 프론트엔드이자 CPU 분석에 강한 멀티툴인가? record→report/script 흐름·서브커맨드·카테고리별 원라이너는? (Ch 13.1~13.2) |
| 13-02 | [perf (2) — 이벤트 소스](./13-02.perf%20(2)%20—%20이벤트%20소스.md) | PMC 기반(하드웨어·빈도 샘플링 함정) vs 추적 기반(tracepoint·software)? kprobe·uprobe·USDT 동적 프로브 초기화와 인자 읽기는? (Ch 13.3~13.7) |
| 13-03 | [perf (3) — 명령](./13-03.perf%20(3)%20—%20명령.md) | stat(효율적 카운트·IPC)·record(CPU 프로파일링·precise event)·report(계층 요약)·script(샘플 나열·플레임 그래프)·trace(라이브)·Intel PT는? (Ch 13.8~13.14) |
| 14-01 | [Ftrace (1) — 개요·tracefs·프로파일러](./14-01.Ftrace%20(1)%20—%20개요·tracefs·프로파일러.md) | Ftrace는 왜 의존성 거의 없는 멀티툴인가? 프로파일러(요약) vs 트레이서(상세)? tracefs를 echo·cat으로 다루는 법·function 프로파일러는? (Ch 14.1~14.3) |
| 14-02 | [Ftrace (2) — 트레이서](./14-02.Ftrace%20(2)%20—%20트레이서.md) | function 트레이싱(trace vs trace_pipe)·tracepoint/kprobe/uprobe(filter·trigger)·function_graph(지연 기호)·hwlat·hist triggers·synthetic events(지연 히스토그램)는? (Ch 14.4~14.10) |
| 14-03 | [Ftrace (3) — 프론트엔드](./14-03.Ftrace%20(3)%20—%20프론트엔드.md) | trace-cmd(perf 비교)·KernelShark(시각화)·perf ftrace(래퍼)·perf-tools(execsnoop·funccount·funcgraph)? perf-tools vs BPF는 언제 무엇을? (Ch 14.11~14.14) |
| 15-01 | [BPF (1) — 개요·BCC vs bpftrace·BCC](./15-01.BPF%20(1)%20—%20개요·BCC%20vs%20bpftrace·BCC.md) | BPF는 왜 프로그래밍 가능한 트레이서인가(커널 집계)? BCC vs bpftrace(C vs 셸 스크립팅)? BCC 단일/다목적 도구(biolatency·trace·argdist)는? (Ch 15.1) |
| 15-02 | [BPF (2) — bpftrace 도구·원라이너](./15-02.BPF%20(2)%20—%20bpftrace%20도구·원라이너.md) | bpftrace는 왜 "추적의 awk"인가? 한 원라이너가 프로브·필터·맵·hist를 어떻게 조합하나? CPU·메모리·디스크·네트워크 원라이너는? (Ch 15.2.1~15.2.3) |
| 15-03 | [BPF (3) — bpftrace 프로그래밍·레퍼런스](./15-03.BPF%20(3)%20—%20bpftrace%20프로그래밍·레퍼런스.md) | 프로브/필터/액션 구조? 변수 세 종류(빌트인·$·@)? count·hist 맵 함수? vfs_read 지연 측정(@start[tid]·필터)·프로브 유형 레퍼런스는? (Ch 15.2.4~15.2.6) |
| 16-01 | [케이스 스터디 — 컨테이너가 3-4배 빠른 이유](./16-01.케이스%20스터디%20—%20컨테이너가%203-4배%20빠른%20이유.md) | Netflix 마이크로서비스가 컨테이너에서 3-4배 빠른 미스터리를 60초·USE→설정→PMC(IPC·LLC)→소프트웨어 이벤트→트레이싱으로 파고든 실전 분석 여정은? (Ch 16) |
| a0-01 | [부록 — USE 메서드 체크리스트·sar 요약](./a0-01.부록%20—%20USE%20메서드%20체크리스트·sar%20요약.md) | 자원별 USE(사용률·포화·에러) Linux 도구 매핑과 sar 옵션별 메트릭 치트시트는? (부록 A·B) |
| a0-02 | [부록 — 연습 풀이](./a0-02.부록%20—%20연습%20풀이.md) | 원서 선별 연습문제 풀이 — 지연·CPU를 떠나는 이유·paging vs swapping·논리vs물리 I/O·디스크 과부하·게스트 관측성은? (부록 D) |



## 학습 로드맵

> 16개 장을 네 그룹으로 묶은 지도입니다. 16장 전체 정리가 끝났으며(00-00 + 1~16장 = 51편), 각 행은 위 `## 문서` 표의 노트에 대응합니다. 그룹별 읽는 순서는 표 아래 안내를 따릅니다.

| 장 | 제목 | 그룹 | 다루는 범위 |
|----|------|------|------------|
| 1 | Introduction | 필수 배경 | 성능 분석 입문·핵심 개념 |
| 2 | Methodologies | 필수 배경 | 방법론·모델·용량 계획·통계 |
| 3 | Operating Systems | 필수 배경 | 성능 분석가를 위한 커널 내부 |
| 4 | Observability Tools | 필수 배경 | 관측 도구의 종류·인터페이스·프레임워크 |
| 5 | Applications | 분석 대상별 | 앱 성능을 OS 관점에서 관측 |
| 6 | CPUs | 분석 대상별 | 코어·캐시·인터커넥트·커널 스케줄링 |
| 7 | Memory | 분석 대상별 | 가상 메모리·페이징·할당자 |
| 8 | File Systems | 분석 대상별 | 파일시스템 I/O·캐시 |
| 9 | Disks | 분석 대상별 | 스토리지·RAID·커널 I/O 서브시스템 |
| 10 | Network | 분석 대상별 | 프로토콜·소켓·인터페이스 |
| 11 | Cloud Computing | 분석 대상별 | 하이퍼바이저·컨테이너의 오버헤드·격리·관측 |
| 12 | Benchmarking | 분석 대상별 | 정확한 벤치마킹·결과 해석·흔한 실수 |
| 13 | perf | 고급 추적 | 표준 리눅스 프로파일러 perf(1) |
| 14 | Ftrace | 고급 추적 | 커널 코드 실행 탐색용 추적기 |
| 15 | BPF | 고급 추적 | BCC·bpftrace (2판 신설) |
| 16 | Case Study | 종합 | Netflix 실전 성능 사례 |

> 1~4장은 먼저 읽는 필수 배경이고, 5~12장은 분석 대상별로 필요할 때 참조합니다. 13~15장(perf·Ftrace·BPF)은 추적·프로파일링 심화로 2판에서 새로 분리·신설된 장이며, 16장은 전체 그림을 먼저 보고 싶을 때 출발점으로 삼습니다.



## 상위·이웃

- 상위: [02_os/ MOC](../README.md)
- 이웃: [02_os/linux-kernel-programming/](../linux-kernel-programming/README.md) — 커널 개발자 관점의 리눅스 내부. 본서 3·6·7장(커널·CPU·메모리)과 메커니즘이 겹칩니다
- 이웃: [02_os/kernel/](../kernel/README.md) — K8s 운영 관점의 커널 메커니즘(namespace·cgroup). 본서 11장(컨테이너)과 맞닿습니다
- 이웃: [02_os/networking/](../networking/README.md) — Linux 네트워크 자료구조. 본서 10장(네트워크)과 주제가 겹칩니다
- cross-link: [06_observability/](../../06_observability/README.md) — Grafana LGTM 스택·SLO 운영 관점. 본서가 *커널 레벨 성능 분석*(perf·Ftrace·BPF)이라면 06은 *앱·인프라 관측 운영*이라 시선이 다릅니다
