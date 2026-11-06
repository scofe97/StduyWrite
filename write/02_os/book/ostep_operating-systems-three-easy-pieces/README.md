---
title: OSTEP — 정독 인덱스
tags: [moc, study-index, book, os, virtualization, concurrency, persistence, scheduling, file-system, security]
status: draft
source:
  - 《Operating Systems: Three Easy Pieces》(Remzi H. Arpaci-Dusseau · Andrea C. Arpaci-Dusseau, Arpaci-Dusseau Books) — 홈페이지 표기 "November, 2023 (Version 1.10)". 장 PDF 바닥글은 대부분 1.10 이고 서문·9장·32장은 1.20 이며 ISBN 은 확인 안 됨
  - https://pages.cs.wisc.edu/~remzi/OSTEP/  # 판 표기·장 목록·장별 PDF 주소·보안 장과 부록 목록 확인 (2026-11-06 조회)
  - https://pages.cs.wisc.edu/~remzi/OSTEP/combined.html  # 판 이력과 보안 장이 웹 전용이라는 문구 확인 (2026-11-06 조회)
  - https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html  # 숙제 형식과 코드 주소 확인 (2026-11-06 조회)
  - https://github.com/remzi-arpacidusseau/ostep-homework  # 장별 숙제 폴더 목록 확인 (2026-11-06 조회)
related:
  - ../learning-modern-linux/README.md
  - ../linux-kernel-programming/README.md
  - ../systems-performance/README.md
  - ../../../roadmap/os-roadmap.md
  - ../../README.md
learning:
  topic: ostep
  scope: durable
  level: 기본
  last_verified:
  blocked_count:
  next_lesson: "01-01 (원문 2장) 정독 노트 작성"
updated: 2026-11-06
---

# OSTEP — 정독 인덱스
---
> 이 폴더는 《Operating Systems: Three Easy Pieces》(Remzi H. Arpaci-Dusseau · Andrea C. Arpaci-Dusseau, Arpaci-Dusseau Books)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 장 PDF 를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> 이 책은 OS 가 왜 그렇게 동작하는지를 가상화·병행성·지속성 세 덩어리로 풀어 줍니다. 형제 책이 무엇을 재고 Linux 가 실제로 무엇을 내주는지를 다루는 동안, 이 책은 그 아래의 원리를 문제 하나씩 풀어 갑니다.

### 02_os 안에서 맡는 축

`02_os` 는 OS 공통 기반을 모은 카테고리입니다. 이 책은 그 안에서 원리 축을 맡습니다. 저자들은 2장에서 세 덩어리마다 CRUX 상자를 하나씩 둡니다. OS 는 자원을 어떻게 가상화하는가, 동시에 실행되는 스레드로 올바른 프로그램을 어떻게 만드는가, 데이터를 어떻게 영속적으로 저장하는가입니다.

이 세 질문이 가상화, 병행성, 지속성의 세 덩어리가 됩니다. 가상화는 CPU 와 메모리를, 병행성은 스레드와 락과 조건 변수를, 지속성은 디스크와 파일 시스템을 다룹니다. 뒤에는 분산 시스템 장이 붙습니다.

책의 구성은 다음과 같습니다. 1~51장 가운데 대화 장이 11개이고 나머지 40장이 본문입니다. 52~57장은 보안 장인데 웹 페이지에만 있고 인쇄본과 전체 PDF 에는 없습니다.[^sec] 부록 A~H 는 대화 3개와 가상 머신 모니터, 모니터, 실습 안내, 프로젝트 아이디어입니다. 노트 범위는 본문 40장과 보안 53~57장, 부록 B 입니다. 부록 D 는 저자가 Deprecated 로 표시했고 부록 F~H 는 실습 안내와 프로젝트 목록이라 범위 밖입니다.

### 형제 책과 보는 층의 차이

[『Systems Performance』](../systems-performance/README.md)는 성능 분석가의 눈으로 CPU·메모리·디스크를 무엇으로 어떻게 잴지 다룹니다. [『Learning Modern Linux』](../learning-modern-linux/README.md)는 클라우드 네이티브 환경을 전제로 리눅스를 한 바퀴 돕니다. [『Linux Kernel Programming』](../linux-kernel-programming/README.md)은 커널 개발자 관점에서 메모리 관리와 CPU 스케줄러와 동기화의 구현을 다룹니다. 이 책들은 Linux 가 실제로 내주는 인터페이스와 구현을 보여 줍니다.

이 책의 질문은 그 모든 것의 밑에 있는 원리입니다. 스케줄러는 왜 우선순위를 올리고 내리는가를 묻습니다. 페이지 테이블은 왜 여러 단계가 되는가를 묻습니다. 파일 시스템은 크래시 뒤에 왜 저널을 남기는가를 묻습니다. 설계가 어떤 문제의 답이었는지를 묻기 때문에, 노트는 Linux 이름을 외우는 대신 문제와 선택지를 먼저 적습니다.

### 로드맵 속 자리

[OS 로드맵](../../../roadmap/os-roadmap.md)은 OSTEP 을 가상화·병행성·지속성 범위의 필수 책으로 두고 2·4·6단계에 걸칩니다. 로드맵의 개념 단어 가운데 이 책의 절 제목이 직접 받치는 것만 아래에 짝지었습니다.

| 단계 | 로드맵 개념 | 이 책의 장과 절 |
|------|------------|---------------|
| 2 | 유저·커널 스페이스·시스템 콜 | 6장 §Problem #1: Restricted Operations |
| 2 | process·thread·task 구조 · 주소 공간·heap·stack | 4장 §Data Structures, 13장 §The Address Space, 14장 §Types of Memory, 26장 |
| 2 | `fork` · `exec` 로 뜨는 새 프로세스 | 5장 §The fork() System Call, §Finally, The exec() System Call |
| 2 | event loop · readiness 모델 | 33장 §The Basic Idea: An Event Loop, §An Important API: select() (or poll()) |
| 2 | 동기화 · 교착 · 조건 변수 | 28~32장 |
| 4 | run queue · CFS · context switch | 6장 §Problem #2: Switching Between Processes, 7~10장 |
| 4 | swap · overcommit | 21장 §Swap Space, 22장 |
| 4 | malloc · free list · 단편화 · allocator | 14장 §The malloc() Call, 17장 Free-Space Management |
| 4 | block I/O · I/O 스케줄러 · `fsync` | 36장, 37장 §Disk Scheduling, 39장 §Writing Immediately With fsync() |
| 6 | TLB · page table · 가용 공간 관리 | 18~20장, 17장 |
| 6 | demand paging | 21장 §The Page Fault |
| 6 | 스케줄링 클래스 · CFS 구현 | 9장 §The Linux Completely Fair Scheduler (CFS), 10장 §Linux Multiprocessor Schedulers |
| 6 | 임계 구역 · mutex · spinlock · atomic | 26·28장 |
| 6 | 하이퍼바이저 · VM | 부록 B §Virtualizing the CPU, §Virtualizing Memory |

### 원본과 판

무료 공개판이라 원본 PDF 를 Drive 에 따로 두지 않습니다. 장 PDF 는 홈페이지 https://pages.cs.wisc.edu/~remzi/OSTEP/ 에서 받습니다. 노트마다 그 장 PDF 바닥글에 찍힌 판과 조회일을 적습니다.

홈페이지는 현재 판을 1.10, 2023년 11월로 적습니다. 서문과 9장과 32장 PDF 바닥글은 1.20 입니다. 그래서 책 전체가 한 판으로 맞춰져 있지 않습니다.[^bib]



## 장별 목표

> 장마다 저자가 **CRUX** 상자에 적어 둔 질문을 근거로 목표를 적습니다. 원문에 없는 목표는 넣지 않았습니다.

OSTEP 은 장이 푸는 문제를 `THE CRUX OF THE PROBLEM`(또는 `THE CRUX`, `CRUX`)이라는 음영 상자에 질문으로 적습니다. 표의 질문은 그 상자를 한국어로 옮긴 것입니다. 한 장에 상자가 여럿이면 장 전체를 묻는 첫 상자만 씁니다. 2장만 상자 셋이 세 덩어리에 하나씩 대응해서 셋을 줄여 모두 적었습니다. 26장의 상자는 라벨이 없는 음영 상자(§26.5 끝)라서 그 상자를 썼습니다. 원문에 질문 문장이 없는 상자는 상자 제목을 질문으로 옮겼습니다. 상자가 없는 장은 첫 문단의 저자 선언을 썼고 표에 첫 문단이라고 적었습니다.

### 소개 (1·2장)

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 1 | A Dialogue on the Book | 대화 — 책 전체 도입 | — |
| 2 | Introduction to Operating Systems | OS 는 자원을 어떻게 가상화하는가? / 동시에 실행되는 스레드로 올바른 프로그램을 어떻게 만드는가? / 데이터를 어떻게 영속적으로 저장하는가? | 세 덩어리 소개, 설계 목표, 짧은 역사 |



### 가상화 — CPU (3~11장)

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 3 | A Dialogue on Virtualization | 대화 — 가상화 도입 | — |
| 4 | The Abstraction: The Process | 물리 CPU 는 몇 개뿐인데, OS 는 어떻게 CPU 가 거의 끝없이 있는 듯한 환상을 주는가? | 프로세스 추상, 프로세스 API, 생성, 상태, 자료구조 |
| 5 | Interlude: Process API | 프로세스 생성과 제어에 OS 는 어떤 인터페이스를 내놓아야 하는가? 강력한 기능과 쓰기 쉬움, 높은 성능을 함께 얻으려면 인터페이스를 어떻게 설계해야 하는가? | `fork()`, `wait()`, `exec()`, API 를 이렇게 만든 이유, 프로세스 제어와 사용자, 도구 |
| 6 | Mechanism: Limited Direct Execution | 시스템의 통제권을 쥔 채로 CPU 를 어떻게 효율적으로 가상화하는가? | 제한된 직접 실행, 제한된 연산, 프로세스 간 전환, 동시성 걱정 |
| 7 | Scheduling: Introduction | 스케줄링 정책을 생각하는 기본 틀을 어떻게 세우는가? 핵심 가정과 중요한 지표는 무엇이고, 초기 컴퓨터 시스템은 어떤 기본 접근을 썼는가? | 작업 가정, 스케줄링 지표, FIFO · SJF · STCF, 응답 시간, Round Robin, I/O 포함, 오라클 없는 스케줄링 |
| 8 | Scheduling: The Multi-Level Feedback Queue | 작업 길이를 미리 모르는 채로, 대화형 작업의 응답 시간과 전체 반환 시간을 함께 줄이는 스케줄러를 어떻게 설계하는가? | MLFQ 기본 규칙, 우선순위 변경, 우선순위 부스트, 회계 개선, 튜닝 |
| 9 | Scheduling: Proportional Share | CPU 를 비례 배분하는 스케줄러를 어떻게 설계하는가? 핵심 메커니즘은 무엇이고 얼마나 효과적인가? | 티켓과 지분, 티켓 메커니즘, 구현, 티켓 배정, Stride 스케줄링, Linux CFS |
| 10 | Multiprocessor Scheduling (Advanced) | 여러 CPU 에서 작업을 어떻게 스케줄링하는가? 어떤 새 문제가 생기고, 기존 기법이 그대로 통하는가, 새 아이디어가 필요한가? | 멀티프로세서 구조, 동기화, 캐시 친화도, 단일 큐와 다중 큐, Linux 멀티프로세서 스케줄러 |
| 11 | Summary Dialogue on CPU Virtualization | 대화 — CPU 가상화 정리(앞 장들의 요약) | — |



### 가상화 — 메모리 (12~24장)

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 12 | A Dialogue on Memory Virtualization | 대화 — 메모리 가상화 도입 | — |
| 13 | The Abstraction: Address Spaces | 여러 프로세스가 하나의 물리 메모리를 나눠 쓰는데, OS 는 어떻게 각 프로세스에 사적이고 아주 클 수도 있는 주소 공간이라는 추상을 만드는가? | 초기 시스템, 멀티프로그래밍과 시분할, 주소 공간, 목표 |
| 14 | Interlude: Memory API | UNIX/C 로 견고한 소프트웨어를 만들려면 메모리를 어떻게 할당하고 관리해야 하는가? 흔히 쓰는 인터페이스는 무엇이고 피해야 할 실수는 무엇인가? | 메모리 유형, `malloc()`, `free()`, 흔한 오류, OS 지원, 그 밖의 호출 |
| 15 | Mechanism: Address Translation | 메모리를 효율적이고 유연하게 가상화하려면 어떻게 하는가? 응용이 접근할 수 있는 위치를 통제하면서, 이 모든 것을 효율적으로 하려면 어떻게 하는가? | 가정, 예, 동적(하드웨어) 재배치, 하드웨어 지원, OS 이슈 |
| 16 | Segmentation | 스택과 힙 사이에 빈 공간이 많은 큰 주소 공간을 어떻게 지원하는가? | Base/Bounds 를 일반화한 세그멘테이션, 세그먼트 식별, 스택, 공유, 세분도, OS 지원 |
| 17 | Free-Space Management | 크기가 제각각인 요청을 만족시키면서 빈 공간을 어떻게 관리하는가? 단편화를 줄이는 전략은 무엇이고, 대안별 시간·공간 비용은 얼마인가? | 가정, 저수준 메커니즘, 기본 전략, 그 밖의 접근 |
| 18 | Paging: Introduction | 세그멘테이션의 문제를 피하면서 페이지로 메모리를 어떻게 가상화하는가? 기본 기법은 무엇이고, 공간·시간 비용을 낮게 유지하려면 어떻게 하는가? | 단순 예와 개요, 페이지 테이블의 위치와 내용, 느린 페이징, 메모리 트레이스 |
| 19 | Paging: Faster Translations (TLBs) | 페이징이 요구하는 듯한 추가 메모리 참조를 피하면서 주소 변환을 어떻게 빠르게 하는가? 어떤 하드웨어 지원과 OS 관여가 필요한가? | TLB 기본 알고리즘, 배열 접근 예, TLB miss 처리 주체, TLB 내용, 컨텍스트 스위치, 교체 정책, 실제 TLB 엔트리 |
| 20 | Paging: Smaller Tables | 선형 페이지 테이블은 너무 크다. 페이지 테이블을 어떻게 작게 만드는가? 핵심 아이디어는 무엇이고, 새 자료구조에서 어떤 비효율이 생기는가? | 더 큰 페이지, 페이징과 세그먼트의 혼합, 멀티레벨 페이지 테이블, 역 페이지 테이블, 페이지 테이블 스왑 |
| 21 | Beyond Physical Memory: Mechanisms | OS 는 더 크고 느린 장치를 이용해 큰 가상 주소 공간이라는 환상을 어떻게 투명하게 제공하는가? | 스왑 공간, present 비트, 페이지 폴트, 메모리가 가득 찼을 때, 제어 흐름, 교체 시점 |
| 22 | Beyond Physical Memory: Policies | OS 는 어느 페이지를 메모리에서 내보낼지 어떻게 정하는가? | 캐시 관리, 최적 교체, FIFO · Random · LRU, 워크로드 예, LRU 근사, dirty 페이지, 스래싱 |
| 23 | Complete Virtual Memory Systems | 완전한 가상 메모리 시스템을 만들려면 어떤 기능이 필요한가? 그 기능은 성능을 높이거나 보안을 강화하거나 그 밖에 시스템을 어떻게 낫게 하는가? | VAX/VMS 가상 메모리, Linux 가상 메모리 시스템 |
| 24 | Summary Dialogue on Memory Virtualization | 대화 — 메모리 가상화 정리(앞 장들의 요약) | — |



### 병행성 (25~34장)

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 25 | A Dialogue on Concurrency | 대화 — 병행성 도입 | — |
| 26 | Concurrency: An Introduction | 동기화 프리미티브를 만들려면 하드웨어와 OS 에서 어떤 지원이 필요한가? 이 프리미티브를 올바르고 효율적으로 만들려면 어떻게 하고, 프로그램은 원하는 결과를 얻도록 이를 어떻게 쓰는가? | 스레드를 쓰는 이유, 스레드 생성 예, 공유 데이터, 통제 없는 스케줄링, 원자성, 서로 기다리기 |
| 27 | Interlude: Thread API | OS 는 스레드 생성과 제어에 어떤 인터페이스를 내놓아야 하는가? 쓰기 쉬움과 실용성을 함께 얻으려면 인터페이스를 어떻게 설계해야 하는가? | 스레드 생성과 종료, 락, 조건 변수, 컴파일과 실행 |
| 28 | Locks | 효율적인 락을 어떻게 만드는가? 어떤 하드웨어 지원과 OS 지원이 필요한가? | 락의 기본 개념, pthread 락, 락 만들기와 평가, 인터럽트 제어, test-and-set, compare-and-swap, LL/SC, fetch-and-add, 양보, 큐, two-phase 락 |
| 29 | Lock-based Concurrent Data Structures | 주어진 자료구조에 올바르게 동작하도록 락을 어떻게 더하는가? 여러 스레드가 동시에 접근하도록 높은 성능을 내려면 락을 어떻게 더하는가? | 동시 카운터, 연결 리스트, 큐, 해시 테이블 |
| 30 | Condition Variables | 스레드는 조건이 참이 되기를 어떻게 기다려야 하는가? | 정의와 루틴, 생산자/소비자(bounded buffer), covering condition |
| 31 | Semaphores | 락과 조건 변수 대신 세마포어를 어떻게 쓰는가? 세마포어는 무엇이고 이진 세마포어는 무엇인가? 락과 조건 변수로 세마포어를 쉽게 만들 수 있는가? 거꾸로 세마포어로 락과 조건 변수를 만들 수 있는가? | 세마포어 정의, 이진 세마포어, 순서 맞추기, 생산자/소비자, reader-writer 락, 식사하는 철학자, 스레드 조절, 구현 |
| 32 | Common Concurrency Problems | 흔한 동시성 버그를 어떻게 다루는가? | 버그 유형, 교착 아닌 버그, 교착 버그 |
| 33 | Event-based Concurrency (Advanced) | 스레드 없이 동시 서버를 어떻게 만드는가? 동시성을 직접 통제하면서, 다중 스레드 응용을 괴롭히는 문제를 어떻게 피하는가? | 이벤트 루프, `select()`/`poll()`, 락이 필요 없는 이유, 블로킹 시스템 콜, 비동기 I/O, 상태 관리 |
| 34 | Summary Dialogue on Concurrency | 대화 — 병행성 정리(앞 장들의 요약) | — |



### 지속성 (35~46장)

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 35 | A Dialogue on Persistence | 대화 — 지속성 도입 | — |
| 36 | I/O Devices | I/O 를 시스템에 어떻게 통합하는가? 일반 메커니즘은 무엇이고, 어떻게 효율적으로 만드는가? | 시스템 구조, 표준 장치와 프로토콜, 인터럽트, DMA, 장치 상호작용 방법, 장치 드라이버, IDE 디스크 드라이버 사례 |
| 37 | Hard Disk Drives | 현대 디스크는 데이터를 어떻게 저장하는가? 인터페이스는 무엇이고, 데이터는 실제로 어떻게 배치되고 접근되는가? 디스크 스케줄링은 성능을 어떻게 높이는가? | 인터페이스, 기본 기하, 단순 디스크, I/O 시간 계산, 디스크 스케줄링 |
| 38 | Redundant Arrays of Inexpensive Disks (RAIDs) | 크고 빠르고 믿을 만한 저장 시스템을 어떻게 만드는가? 핵심 기법은 무엇이고, 접근법마다 어떤 트레이드오프가 있는가? | 인터페이스와 RAID 내부, 결함 모델, RAID 평가, RAID 0 · 1 · 4 · 5, RAID 비교 |
| 39 | Interlude: Files and Directories | OS 는 영속 장치를 어떻게 관리하는가? API 는 무엇이고, 구현에서 중요한 점은 무엇인가? | 파일 시스템 인터페이스, 파일 생성·읽기·쓰기, `fsync()`, 이름 변경, 파일 정보, 삭제, 디렉터리, 하드·심볼릭 링크, 권한 비트와 ACL, 마운트 |
| 40 | File System Implementation | 단순한 파일 시스템을 어떻게 만드는가? 디스크에 어떤 구조가 필요하고, 그 구조는 무엇을 추적하며, 어떻게 접근되는가? | 전체 구성, inode, 디렉터리 구성, 빈 공간 관리, 접근 경로, 캐싱과 버퍼링 |
| 41 | Locality and The Fast File System | 성능을 높이려면 파일 시스템 자료구조를 디스크에 어떻게 배치하는가? 그 위에 어떤 할당 정책이 필요하고, 파일 시스템이 "디스크를 알게" 하려면 어떻게 하는가? | 성능 문제, 디스크를 아는 FFS, cylinder group, 할당 정책, 지역성 측정, 큰 파일 예외 |
| 42 | Crash Consistency: FSCK and Journaling | 디스크 쓰기 사이의 어느 지점에서든 크래시가 날 수 있을 때, 파일 시스템은 디스크 이미지를 어떻게 합리적인 상태로 유지하는가? | 자세한 예, fsck, 저널링(write-ahead logging), 그 밖의 접근 |
| 43 | Log-structured File Systems | 파일 시스템은 모든 쓰기를 어떻게 순차 쓰기로 바꾸는가? | 순차 쓰기, 버퍼 크기, inode 찾기와 inode map, checkpoint region, 디렉터리, 가비지 컬렉션, 블록 생존 판정, 크래시 복구 |
| 44 | Flash-based SSDs | 플래시 기반 SSD 를 어떻게 만드는가? 비싼 지우기를 어떻게 다루고, 덮어쓰기가 장치를 마모시키는데도 오래 쓰려면 어떻게 하는가? | 비트 저장, bank 와 plane, 플래시 연산, 성능과 신뢰성, FTL, 로그 구조 FTL, 가비지 컬렉션, 매핑 테이블 크기, 마모 평준화 |
| 45 | Data Integrity and Protection | 저장 장치에 쓴 데이터를 보호하려면 시스템은 어떻게 해야 하는가? 어떤 기법이 필요하고, 공간·시간 오버헤드를 낮게 하려면 어떻게 하는가? | 디스크 장애 유형, 잠재 섹터 오류, 체크섬, 잘못된 위치 쓰기, 유실 쓰기, 스크러빙, 체크섬 오버헤드 |
| 46 | Summary Dialogue on Persistence | 대화 — 지속성 정리(앞 장들의 요약) | — |



### 분산 시스템 (47~51장)

홈페이지는 이 장들을 지속성 열과 같은 색으로 칠해 둡니다. 책은 세 덩어리를 내세우므로 분산 시스템은 따로 묶어 적었습니다.

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 47 | A Dialogue on Distribution | 대화 — 분산 도입 | — |
| 48 | Distributed Systems | 늘 제대로 동작하지는 않는 부품으로 동작하는 시스템을 어떻게 만드는가? | 통신 기초, 신뢰할 수 없는 통신 계층, 신뢰할 수 있는 통신 계층, 통신 추상화, RPC |
| 49 | Sun’s Network File System (NFS) | 분산 파일 시스템을 어떻게 만드는가? 무엇을 생각해야 하고, 무엇을 틀리기 쉽고, 기존 시스템에서 무엇을 배울 수 있는가? | 기본 분산 파일 시스템, 서버 크래시 복구, statelessness, NFSv2 프로토콜, 멱등 연산, 클라이언트 캐싱, 캐시 일관성 |
| 50 | The Andrew File System (AFS) | 서버와 주고받는 상호작용을 최소화하도록 프로토콜을 어떻게 다시 설계하는가? TestAuth 메시지 수를 줄이고 남은 상호작용을 효율적으로 만들려면 어떻게 하는가? | AFS 버전 1과 그 문제, 프로토콜 개선, AFS 버전 2, 캐시 일관성, 크래시 복구, 규모와 성능 |
| 51 | Summary Dialogue on Distribution | 대화 — 분산 정리(앞 장들의 요약) | — |



### 보안과 부록

보안 장은 별도 저자가 쓴 웹 전용 장입니다. 노트 범위는 보안 53~57장과 부록 B 이고, 부록 D(저자가 Deprecated 로 표시)와 F~H(실습 안내·프로젝트 목록)는 범위 밖입니다. 범위 밖 부록은 참고로만 표에 남겼습니다. 부록 D·F·G·H 는 CRUX 상자가 없어서 첫 문단을 근거로 썼습니다.

| 장 | 제목 | 저자가 던진 질문(CRUX) | 주요 토픽 |
|----|------|----------------------|----------|
| 52 | A Dialogue on Security | 대화 — 53~57장 도입 | — |
| 53 | Introduction to Operating System Security | 같은 기계에서 동시에 돌 수도 있고 서로 영향을 주는 여러 프로세스가 있을 때, 각 프로세스가 접근하도록 허락된 자원이 정확히 의도한 방식으로만 접근되게 하려면 어떻게 하는가? OS 에는 어떤 프리미티브가, 하드웨어에는 어떤 메커니즘이 필요한가? 그것들로 보안 문제를 어떻게 푸는가? | 보호 대상, 보안 목표와 정책, 안전한 시스템 설계, OS 보안의 기초 |
| 54 | Authentication | 여러 주체에 속한 프로세스를 지원하는 시스템에서, 각 프로세스에 올바른 신원이 붙었다고 어떻게 확신하는가? 새 프로세스를 만들 때도, 악의적인 주체가 신원을 부당하게 바꾸지 못한다고도 어떻게 확신하는가? | 프로세스에 신원 붙이기, 아는 것·가진 것·자신인 것에 의한 인증, 사람 아닌 주체 인증 |
| 55 | Access Control | 특정 사용자의 특정 프로세스가 어느 순간에 한 요청을 허용할지 OS 는 어떻게 결정하는가? 어떤 정보를 쓰고, 그 정보로 원하는 보안 정책을 어떻게 담는가? | 접근 통제 문제의 측면, ACL, capability, 강제·임의 접근 통제, 구현상 실무 |
| 56 | Protecting Information With Cryptography | OS 의 통제 밖에서 누군가 핵심 데이터에 접근하더라도 그것을 쓰거나 바꾸지 못하게 하려면 암호학을 어떻게 쓰는가? 어떤 암호 기술이 있고, 어떻게 제대로 쓰며, 한계는 무엇인가? | 암호학, 공개 키 암호, 암호 해시, 암호 깨기, OS 와 암호, 저장 데이터 암호화, 암호학적 capability |
| 57 | Distributed System Security | 둘 이상의 기계에 걸친 시스템을 어떻게 안전하게 만드는가? 어떤 도구가 있고, 어떻게 제대로 쓰며, 어느 부분에서 신중해야 하는가? | 인증의 역할, 공개 키·패스워드 인증, SSL/TLS, 그 밖의 인증, 상위 수준 도구 |
| A | A Dialogue on Virtual Machine Monitors | 대화 — 부록 B 도입 | — |
| B | Virtual Machine Monitors | OS 아래의 기계를 가상 머신 모니터는 어떻게 투명하게 가상화하는가? 그러려면 어떤 기법이 필요한가? | VMM 을 쓰는 이유, CPU 가상화, 메모리 가상화, 정보 격차(information gap) |
| C | A Dialogue on Monitors | 대화 — 부록 D 도입(D 는 범위 밖) | — |
| D | Monitors (Deprecated) | 첫 문단: 객체지향 프로그래밍이 퍼지던 때 동기화를 구조화된 프로그래밍 환경에 합치려는 접근으로 나온 모니터 | 모니터, 폐기 표시 |
| E | A Dialogue on Labs | 대화 — 실습 부록 F~H 도입(범위 밖) | — |
| F | Laboratory: Tutorial | 첫 문단: UNIX 시스템에서 C 프로그래밍 환경의 기초를 익히게 하는 짧은 안내 | C 프로그래밍 환경 |
| G | Laboratory: Systems Projects | 첫 문단: 학기당 여섯이나 일곱 개를 하는 시스템 프로젝트 아이디어 제시 | 시스템 프로젝트 개요 |
| H | Laboratory: xv6 Projects | 첫 문단: xv6 커널과 관련된 프로젝트 아이디어 제시 | xv6 커널 프로젝트 |



## 작성된 정독 노트

> 편을 작성하는 대로 채우며, 아직 쓰지 않은 편은 상태만 "작성 예정"으로 둡니다. 제목 칸은 장 제목을 옮긴 가제입니다.

| 편 | 원문 장 | 제목 | 상태 | 숙제 |
|----|--------|------|------|------|
| 01-01 · 01-02 | 2장 | Introduction to Operating Systems (가제, 두 편 후보) | 작성 예정 | 없음 (Homework 절은 숙제 형식 안내) |
| 02-01 | 4장 | The Abstraction: The Process (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-intro/`) |
| 03-01 | 5장 | Interlude: Process API (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-api/` 의 `fork.py`·`generator.py`) + 코드 (직접 작성) |
| 04-01 | 6장 | Mechanism: Limited Direct Execution (가제) | 작성 예정 | 있음 — 측정 (저장소 폴더 없음, 직접 작성) |
| 05-01 | 7장 | Scheduling: Introduction (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-sched/`) |
| 06-01 | 8장 | Scheduling: The Multi-Level Feedback Queue (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-sched-mlfq/`) |
| 07-01 | 9장 | Scheduling: Proportional Share (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-sched-lottery/`) |
| 08-01 | 10장 | Multiprocessor Scheduling (Advanced) (가제) | 작성 예정 | 있음 — 시뮬레이터 (`cpu-sched-multi/`) |
| 09-01 | 13장 | The Abstraction: Address Spaces (가제) | 작성 예정 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 10-01 | 14장 | Interlude: Memory API (가제) | 작성 예정 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 11-01 | 15장 | Mechanism: Address Translation (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-mechanism/`) |
| 12-01 | 16장 | Segmentation (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-segmentation/`) |
| 13-01 | 17장 | Free-Space Management (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-freespace/`) |
| 14-01 | 18장 | Paging: Introduction (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-paging/`) |
| 15-01 | 19장 | Paging: Faster Translations (TLBs) (가제) | 작성 예정 | 있음 — 측정 (저장소 폴더 없음, 직접 작성) |
| 16-01 | 20장 | Paging: Smaller Tables (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-smalltables/`) |
| 17-01 | 21장 | Beyond Physical Memory: Mechanisms (가제) | 작성 예정 | 있음 — 측정 (`vm-beyondphys/`) |
| 18-01 | 22장 | Beyond Physical Memory: Policies (가제) | 작성 예정 | 있음 — 시뮬레이터 (`vm-beyondphys-policy/`) |
| 19-01 · 19-02 | 23장 | Complete Virtual Memory Systems (가제, 두 편 후보) | 작성 예정 | 없음 |
| 20-01 | 26장 | Concurrency: An Introduction (가제) | 작성 예정 | 있음 — 시뮬레이터 (`threads-intro/`) |
| 21-01 | 27장 | Interlude: Thread API (가제) | 작성 예정 | 있음 — 코드 (`threads-api/`) |
| 22-01 · 22-02 | 28장 | Locks (가제, 두 편 후보) | 작성 예정 | 있음 — 시뮬레이터 (`threads-locks/`) |
| 23-01 | 29장 | Lock-based Concurrent Data Structures (가제) | 작성 예정 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 24-01 | 30장 | Condition Variables (가제) | 작성 예정 | 있음 — 코드 (`threads-cv/`) |
| 25-01 | 31장 | Semaphores (가제) | 작성 예정 | 있음 — 코드 (`threads-sema/`) |
| 26-01 | 32장 | Common Concurrency Problems (가제) | 작성 예정 | 있음 — 코드 (`threads-bugs/`) |
| 27-01 | 33장 | [스레드 없이 동시 서버를 만드는 법 — 이벤트 루프와 select·비동기 입출력](./27-01.%EC%8A%A4%EB%A0%88%EB%93%9C%20%EC%97%86%EC%9D%B4%20%EB%8F%99%EC%8B%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%A3%A8%ED%94%84%EC%99%80%20select%C2%B7%EB%B9%84%EB%8F%99%EA%B8%B0%20%EC%9E%85%EC%B6%9C%EB%A0%A5.md) | 작성 완료 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 28-01 | 36장 | I/O Devices (가제) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소 `file-devices/` 는 `process-run.py` 하나) |
| 29-01 | 37장 | Hard Disk Drives (가제) | 작성 예정 | 있음 — 시뮬레이터 (`file-disks/`) |
| 30-01 · 30-02 | 38장 | Redundant Arrays of Inexpensive Disks (RAIDs) (가제, 두 편 후보) | 작성 예정 | 있음 — 시뮬레이터 (`file-raid/`) |
| 31-01 · 31-02 | 39장 | Interlude: Files and Directories (가제, 두 편 후보) | 작성 예정 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 32-01 · 32-02 | 40장 | File System Implementation (가제, 두 편 후보) | 작성 예정 | 있음 — 시뮬레이터 (`file-implementation/`) |
| 33-01 | 41장 | Locality and The Fast File System (가제) | 작성 예정 | 있음 — 시뮬레이터 (`file-ffs/`) |
| 34-01 · 34-02 | 42장 | Crash Consistency: FSCK and Journaling (가제, 두 편 후보) | 작성 예정 | 있음 — 시뮬레이터 (`file-journaling/`) |
| 35-01 | 43장 | Log-structured File Systems (가제) | 작성 예정 | 있음 — 시뮬레이터 (`file-lfs/`) |
| 36-01 · 36-02 | 44장 | Flash-based SSDs (가제, 두 편 후보) | 작성 예정 | 있음 — 시뮬레이터 (`file-ssd/`) |
| 37-01 | 45장 | Data Integrity and Protection (가제) | 작성 예정 | 있음 — 시뮬레이터 (`file-integrity/` 의 `checksum.py`) + 코드 (직접 작성) |
| 38-01 | 48장 | Distributed Systems (가제) | 작성 예정 | 있음 — 코드 (저장소 폴더 없음, 직접 작성) |
| 39-01 | 49장 | Sun’s Network File System (NFS) (가제) | 작성 예정 | 있음 — 측정 (`dist-nfs/` 에는 `README.md` 와 `sampleTrace.csv` 뿐, 시뮬레이터 없음) |
| 40-01 | 50장 | The Andrew File System (AFS) (가제) | 작성 예정 | 있음 — 시뮬레이터 (`dist-afs/`) |
| 41-01 | 53장 | Introduction to Operating System Security (가제) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |
| 42-01 · 42-02 | 54장 | Authentication (가제, 두 편 후보) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |
| 43-01 · 43-02 | 55장 | Access Control (가제, 두 편 후보) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |
| 44-01 · 44-02 | 56장 | Protecting Information With Cryptography (가제, 두 편 후보) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |
| 45-01 · 45-02 | 57장 | Distributed System Security (가제, 두 편 후보) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |
| 46-01 | 부록 B | Virtual Machine Monitors (가제) | 작성 예정 | 없음 (PDF 에 숙제 절이 없고, 저장소에 해당 폴더도 없음) |

편 번호는 노트를 쓰는 장에만 책 순서대로 붙입니다. 보안 장은 41~45편이고 부록 B 는 46편입니다. 부록 D·F~H 는 노트 범위 밖이라 이 표에 넣지 않았습니다.

장 끝 숙제는 각 노트 `## 연습 문제` 의 재료입니다. 시뮬레이터 숙제는 저장소의 `.py` 를 실제로 돌려 정답을 확인합니다. 숙제 페이지는 시뮬레이터의 `-c` 플래그가 답을 계산해 준다고 안내합니다. 이 방식은 위 표에서 시뮬레이터로 적은 장에만 해당하고, 코드나 측정으로 적은 장은 직접 짠 코드의 결과를 봅니다.

### 편 나누기 계획

한 편은 원문 4,000~5,000단어를 기준으로 합니다. 경계는 그 근처의 원문 절 경계에 맞춥니다(`learning-method` 스킬의 정독 노트 세션 규약). 전체 단어 수는 `pdftotext -layout` 추출본을 `wc -w` 로 쟀으므로 코드·표·그림 캡션과 참고문헌·숙제가 들어 있습니다. 본문 단어 수는 첫 `References` 줄 앞까지입니다. 절 경계는 PDF 목차의 `N.M` 항목을 장 본문에서 찾아 쟀습니다. 본문이 7,000단어 이상이면 두 편 후보, 6,000~6,999단어면 한 편 또는 두 편, 그 아래는 한 편으로 적었습니다.

| 장 | 전체 단어 | 본문 단어 | 계획 |
|----|---------:|---------:|------|
| 2 | 8,358 | 7,209 | 두 편 후보. §2.4 Persistence 앞에서 자르면 3,198 / 4,011 단어 |
| 4 | 4,495 | 3,676 | 한 편 |
| 5 | 5,591 | 4,234 | 한 편 |
| 6 | 6,872 | 5,799 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 7 | 4,851 | 4,218 | 한 편 |
| 8 | 4,809 | 3,972 | 한 편 |
| 9 | 6,145 | 5,292 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 10 | 5,476 | 4,088 | 한 편 |
| 13 | 3,639 | 2,632 | 한 편 |
| 14 | 4,231 | 3,436 | 한 편 |
| 15 | 5,638 | 5,029 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 16 | 4,764 | 3,948 | 한 편 |
| 17 | 6,099 | 5,440 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 18 | 5,211 | 4,612 | 한 편 |
| 19 | 7,152 | 5,676 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 20 | 6,409 | 5,879 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 21 | 4,840 | 3,801 | 한 편 |
| 22 | 7,390 | 6,185 | 한 편 또는 두 편. 두 편이면 §22.5 Using History: LRU 앞(2,755 / 3,430) |
| 23 | 8,659 | 7,939 | 두 편 후보. §23.2 The Linux Virtual Memory System 앞에서 자르면 3,372 / 4,567 단어 |
| 26 | 5,978 | 4,942 | 한 편 |
| 27 | 4,374 | 3,797 | 한 편 |
| 28 | 9,497 | 8,326 | 두 편 후보. §28.10 Load-Linked and Store-Conditional 앞에서 자르면 4,244 / 4,082 단어 |
| 29 | 5,085 | 4,267 | 한 편 |
| 30 | 6,423 | 5,577 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 31 | 7,504 | 6,313 | 한 편 또는 두 편. 두 편이면 §31.5 Reader-Writer Locks 앞(3,829 / 2,484) |
| 32 | 6,266 | 5,162 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 33 | 4,668 | 3,780 | 한 편 |
| 36 | 5,346 | 4,809 | 한 편 |
| 37 | 6,694 | 5,681 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 38 | 8,684 | 7,809 | 두 편 후보. §38.6 RAID Level 4: Saving Space With Parity 앞에서 자르면 4,623 / 3,186 단어 |
| 39 | 11,716 | 10,671 | 두 편 후보. §39.9 Getting Information About Files 앞에서 자르면 5,447 / 5,224 단어 |
| 40 | 8,243 | 7,575 | 두 편 후보. §40.4 Directory Organization 앞에서 자르면 3,402 / 4,173 단어 |
| 41 | 5,968 | 5,057 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 42 | 9,459 | 8,163 | 두 편 후보. §42.3 Solution #2: Journaling (or Write-Ahead Logging) 앞에서 자르면 2,824 / 5,339 단어 |
| 43 | 7,327 | 5,728 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 44 | 10,782 | 8,845 | 두 편 후보. §44.8 Garbage Collection 앞에서 자르면 4,251 / 4,594 단어 |
| 45 | 5,823 | 4,418 | 한 편 |
| 48 | 6,848 | 5,957 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 49 | 7,860 | 6,813 | 한 편 또는 두 편. 두 편이면 §49.7 Handling Server Failure With Idempotent Operations 앞(3,259 / 3,554) |
| 50 | 6,249 | 5,424 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 53 | 5,456 | 5,283 | 한 편 (본문이 5,000단어를 조금 넘음) |
| 54 | 10,017 | 9,548 | 두 편 후보. §54.5 Authentication by What You Have 앞에서 자르면 4,557 / 4,991 단어 |
| 55 | 9,878 | 9,307 | 두 편 후보. §55.4 Using Capabilities For Access Control 앞에서 자르면 4,076 / 5,231 단어 |
| 56 | 10,477 | 10,110 | 두 편 후보. §56.5 Cracking Cryptography 앞에서 자르면 4,582 / 5,528 단어 |
| 57 | 9,207 | 9,033 | 두 편 후보. §57.5 SSL/TLS 앞에서 자르면 3,700 / 5,333 단어 |
| B | 5,559 | 4,856 | 한 편 |

대화 장 11개는 260~966단어라 편을 따로 두지 않습니다. 도입 대화인 1, 3, 12, 25, 35, 47장은 뒤 장 노트의 도입으로 씁니다. 정리 대화인 11, 24, 34, 46, 51장은 앞 덩어리의 마지막 노트인 10, 23, 33, 45, 50장 노트의 마무리로 흡수합니다.

대화 장 52·A·C·E 도 같은 규칙으로 편을 따로 두지 않습니다. 52장은 604단어라 53장 노트의 도입으로 쓰고 부록 A 는 187단어라 부록 B 노트의 도입으로 씁니다. 부록 C 는 239단어이고 E 는 490단어인데 짝이 되는 부록 D 와 F~H 가 범위 밖이라 쓰지 않습니다.

묶을 후보는 없습니다. 본문이 가장 짧은 13장(2,632)과 14장(3,436)을 합쳐도 6,068단어라 기준을 넘고, 다른 짧은 장끼리의 합은 그보다 큽니다.



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 1/46 장. 정독 노트 1편(27-01, 원문 33장). 분모는 위 표의 장 수인 46이고 본문 40장에 보안 5장과 부록 B 를 더한 값입니다. 대화 장과 부록 D·F~H 는 넣지 않았습니다 |
| 난이도 레벨 | 기본 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 01-01 (원문 2장 Introduction to Operating Systems, 1장 대화를 도입으로 흡수) |
| 최근 검증 결과 | 이 README `verify-gate.sh --type=learning --style=jondae` 실패 항목 합계 0 (2026-11-06). 경고 하나는 유지합니다. 정의로 시작하는 절 한 곳은 번호 규약을 세워야 뒤 규칙이 읽히는 규약 절입니다 |
| 원문 정오 누적 | 0 |
| 버전 차이 기록 | 0 |
| 복습 회차 | 0 |



## 번호 체계와 작성 규약

> 파일명은 `NN-MM.제목.md`이고 `NN` 은 노트를 쓰는 장에만 붙인 01~46 연번입니다. 책이 예로 드는 Linux 동작은 커널 버전과 함께 적습니다.

`NN`은 노트를 쓰는 장에만 책 순서대로 붙인 01부터 46까지의 연번이고 `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 대화 장에는 번호가 없고 부록 B 는 46입니다. 책의 장 번호는 노트 frontmatter `source` 와 위 표의 "원문 장" 열에만 남깁니다. 책 장 번호를 그대로 쓰면 대화 장과 범위 밖 장 때문에 번호가 건너뛰기 때문입니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계 중 자동 배치가 나은 것은 Mermaid로 본문에 직접 그립니다.

이 책은 판이 장마다 다르게 찍혀 있으므로 노트마다 그 장 PDF 바닥글의 판과 조회일을 적습니다.

책이 Linux 의 실제 동작을 설명하는 곳은 지금과 다를 수 있습니다. 해당하는 곳은 다섯 절입니다.

- 9장 §The Linux Completely Fair Scheduler (CFS)
- 10장 §Linux Multiprocessor Schedulers
- 23장 §The Linux Virtual Memory System
- 28장 §Different OS, Different Support (futex)
- 42장 §Solution #2: Journaling (or Write-Ahead Logging) (ext3)

이 절들의 노트에는 책이 설명하는 커널 버전과 지금 값을 함께 적습니다. 지금 값은 현재 공식 문서 https://docs.kernel.org/ 와 대조합니다. 원문과 현재 값이 다르면 노트에는 현재 값만 출처와 함께 적습니다. 바뀐 항목은 학습 상태 표의 버전 차이 기록에만 셉니다.

노트 끝 순서는 `## 연습 문제` → `## 정답 (자답 후 펼치기)` → `## 참고 자료` 입니다. 연습 문제 재료는 장 끝 숙제입니다.



## 관련 문서

- [『Systems Performance』 정독본](../systems-performance/README.md) — 같은 `book/` 영역, 무엇을 어떻게 잴지의 짝이자 4단계에서 이 책의 CPU·메모리·저장 원리와 이어지는 책
- [『Learning Modern Linux』 정독본](../learning-modern-linux/README.md) — Linux 가 실제로 내주는 인터페이스의 짝
- [『Linux Kernel Programming』 정독본](../linux-kernel-programming/README.md) — 스케줄러·메모리 관리·동기화의 Linux 구현, 6단계에서 이 책과 맞물리는 책
- [OS 로드맵](../../../roadmap/os-roadmap.md) — 2·4·6단계에서 이 책이 놓인 자리
- [02_os MOC](../../README.md) — 상위 카테고리 경계

[^sec]: 보안 장이 웹 전용이라는 근거는 https://pages.cs.wisc.edu/~remzi/OSTEP/combined.html 의 판 이력 문구("included only on the webpage and not in printed form or in the entire PDF")입니다(2026-11-06 조회). 장 PDF 첫머리에 UCLA 소속 별도 저자가 쓴 장이라고 적혀 있습니다.

[^bib]: 서지 확인 결과입니다. 홈페이지는 "November, 2023 (Version 1.10)" 를 현재 판으로 적습니다. 장 PDF 바닥글은 1.10 이 대부분이고 서문·9장·32장은 1.20 이며 헌사와 부록 A·C 는 판 표기가 없습니다. ISBN 은 서문·목차 PDF 에 없고 홈페이지의 판매 링크에도 ISBN 표기가 없어 확인 안 됨으로 둡니다.
