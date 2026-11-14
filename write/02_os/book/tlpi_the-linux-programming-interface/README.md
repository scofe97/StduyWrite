---
title: The Linux Programming Interface — 정독 인덱스
tags: [moc, study-index, book, the-linux-programming-interface, system-call, glibc, posix, linux, os]
status: draft
source:
  - 《The Linux Programming Interface》 (Michael Kerrisk) — 서문 기준 Linux 2.6.35·glibc 2.12 시점 · 본문 64장 · 부록 A~F
  - 원본 PDF — GoogleDrive/내 드라이브/book/The Linux Programming Interface/ (2026-11-11 추가, 장마다 PDF 하나, 서문·부록·색인 포함 72개)
  - 책 사이트 — https://man7.org/tlpi/
related:
  - ../learning-modern-linux/README.md
  - ../linux-kernel-programming/README.md
  - ../npg_network-programming-with-go/README.md
  - ../../README.md
  - ../../../landscape/os-keywords.md
updated: 2026-11-11
---

# The Linux Programming Interface — 정독 인덱스

---

> 이 폴더는 Michael Kerrisk 의 『The Linux Programming Interface』를 장 단위로 정독하며 정리하는 책 종속 학습 노트입니다. 운영 명령 아래에서 그 명령이 부르는 시스템 콜과 C 라이브러리 함수를 읽는 자리입니다.

## 이 책을 읽는 이유

> 명령은 알지만 그 명령이 왜 그렇게 동작하는지 설명하지 못하는 곳을, 커널이 프로그램에 내주는 인터페이스 쪽에서 메우려고 읽습니다.

[Learning Modern Linux](../learning-modern-linux/README.md) 노트는 운영자가 치는 명령을 중심으로 씁니다. 그래서 `ulimit -n` 으로 열린 파일 수를 늘리는 법이나 `lsof +L1` 로 지웠지만 열린 파일을 찾는 법은 있습니다. 하지만 그 명령 아래에서 무엇이 일어나는지는 짧게만 다룹니다. 예를 들어 파일을 지워도 공간이 바로 돌아오지 않는 이유는 `unlink()` 가 이름만 지우기 때문입니다. 실제 공간은 그 파일을 연 파일 디스크립터가 모두 닫혀야 돌아옵니다(18.3). 이 설명은 시스템 콜 층에 있습니다.

이 책은 바로 그 층을 다룹니다. 파일 I/O·프로세스·시그널·세션·자원 제한·소켓을 시스템 콜과 glibc 함수 단위로 설명합니다. 그리고 대부분을 직접 돌려 볼 수 있는 짧은 C 프로그램으로 보여 줍니다. 서문에 따르면 예제는 C 소스와 셸 기록을 합쳐 약 15,000줄입니다.

반대로 이 책에 없는 것도 분명합니다. 배포판의 관리 도구와 설정 파일은 다루지 않습니다. 방화벽 데몬, SELinux 정책 명령, 클러스터 관리 도구, 시간 동기화 데몬 설정이 그렇습니다. `limits.conf` 같은 PAM 설정도 범위 밖이고, 이 책은 그 설정이 결국 부르는 `setrlimit()` 까지만 다룹니다.



## 원문과 판

> 서문이 밝힌 기준 시점은 Linux 2.6.35 와 glibc 2.12 입니다. 그 뒤에 바뀐 인터페이스는 man page 로 다시 확인합니다.

서문에 따르면 이 책은 Linux 2.6.x 를 중심으로 쓰였고, 2.6 시리즈에서 새로 생긴 기능은 처음 들어간 커널 판을 적어 둡니다. 표준은 POSIX.1-2001/SUSv3 를 기준으로 설명하고 SUSv4 와 다른 곳을 따로 적습니다. 출간 뒤 바뀐 점은 책 사이트에 적는다고 서문이 안내합니다.

그 뒤로 커널이 많이 바뀌었으므로, 노트에서 동작을 단언할 때는 책 서술만 근거로 삼지 않습니다. 저자가 관리하는 [man-pages](https://man7.org/linux/man-pages/) 의 현행 문서와 대조하고, 다른 곳이 있으면 노트에 그 차이를 적습니다. 컨테이너 안에서 직접 돌려 확인할 수 있는 동작은 실행 결과를 함께 남깁니다.

원본은 장마다 따로 저장한 PDF 입니다. 웹 화면을 인쇄한 파일이라 PDF 쪽 수(72개 합계 2,002쪽)는 종이책 쪽수와 맞지 않습니다. 그래서 출처는 쪽수 대신 `36.2` 같은 절 번호로 밝힙니다. 책의 예제 코드는 GNU Affero GPL v3 로 배포되지만 본문은 그렇지 않으므로, 노트는 본문을 길게 옮기지 않습니다.



## 장 구성

> 서문은 64장을 여덟 묶음으로 나눕니다. 운영과 가장 자주 닿는 곳은 3묶음(파일 속성·ACL·링크·시그널)과 5묶음(세션·자원·데몬·로그인 기록)입니다.

| 묶음 | 장 | 다루는 것 |
|------|----|----------|
| 1 배경과 개념 | 1–3 | UNIX·C·Linux 의 역사와 표준, 시스템 프로그래밍의 기초 개념 |
| 2 기본 인터페이스 | 4–12 | 파일 I/O, 프로세스, 메모리 할당, 사용자와 그룹, 프로세스 자격, 시간, 시스템 한계, `/proc` 정보 |
| 3 고급 인터페이스 | 13–23 | I/O 버퍼링, 파일 시스템, 파일 속성, 확장 속성, ACL, 디렉터리와 링크, 파일 이벤트 감시, 시그널, 타이머 |
| 4 프로세스·프로그램·스레드 | 24–33 | 프로세스 생성과 종료, 자식 감시, 프로그램 실행, POSIX 스레드 |
| 5 고급 프로세스 주제 | 34–42 | 프로세스 그룹·세션·작업 제어, 우선순위와 스케줄링, 자원 제한, 데몬, 권한 프로그램, capability, 로그인 기록, 공유 라이브러리 |
| 6 프로세스 간 통신 | 43–55 | 파이프와 FIFO, System V IPC, 메모리 매핑, 가상 메모리 조작, POSIX IPC, 파일 잠금 |
| 7 소켓 | 56–61 | UNIX 도메인 소켓, TCP/IP 기초, 인터넷 도메인 소켓, 서버 설계, 소켓 고급 주제 |
| 8 고급 I/O | 62–64 | 터미널, select·poll·epoll 같은 다른 I/O 모델, 의사 터미널 |

부록 A~F 는 시스템 콜 추적·명령행 옵션 파싱·NULL 포인터 캐스팅·커널 설정·더 읽을 자료·연습 문제 풀이를 차례로 다룹니다.



## 장 ↔ 정독 노트

> 6장 노트 세 편을 썼습니다. 「기존 노트」 열은 같은 주제를 명령 쪽에서 이미 다룬 노트로, 이 책의 노트가 링크할 자리입니다.

「기존 노트」 열은 노트 제목과 키워드 검색으로 고른 후보이며, 절 내용을 하나하나 대조하지는 않았습니다. LML 은 [Learning Modern Linux](../learning-modern-linux/README.md), LKP 는 [Linux Kernel Programming](../linux-kernel-programming/README.md), NPG 는 [Network Programming with Go](../npg_network-programming-with-go/README.md) 입니다. 진척 컬럼은 ⏳ 진행 중, ✅ 완료, ◻ 미착수입니다.

| 장 | 제목 | 기존 노트 | 노트 | 진척 |
|----|------|----------|------|------|
| 1 | History and Standards | — | — | ◻ |
| 2 | Fundamental Concepts | LML 02-01 | — | ◻ |
| 3 | System Programming Concepts | LML 02-01 | — | ◻ |
| 4 | File I/O: The Universal I/O Model | LML 05-01 | — | ◻ |
| 5 | File I/O: Further Details | LML 05-01 | — | ◻ |
| 6 | Processes | LML 02-01 · LKP 06-01, 06-02 | [06-01](./06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md) · [06-02](./06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md) · [06-03](./06-03.%EB%B6%80%EB%AA%A8%EA%B0%80%20%EC%9E%90%EC%8B%9D%EC%97%90%EA%B2%8C%20%EA%B1%B4%EB%84%A4%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%9D%B8%EC%9E%90%20%EB%AA%A9%EB%A1%9D%EA%B3%BC%20%ED%99%98%EA%B2%BD%20%EB%AA%A9%EB%A1%9D%EC%9D%B4%EB%8B%A4.md) | ✅ |
| 7 | Memory Allocation | LKP 08-01(커널 쪽 할당) | — | ◻ |
| 8 | Users and Groups | LML 04-01 | — | ◻ |
| 9 | Process Credentials | LML 04-01 | — | ◻ |
| 10 | Time | LML 00-01(시간 동기화 레시피) | — | ◻ |
| 11 | System Limits and Options | — | — | ◻ |
| 12 | System and Process Information | LML 08-02 | — | ◻ |
| 13 | File I/O Buffering | — | — | ◻ |
| 14 | File Systems | LML 05-01, 05-02 | — | ◻ |
| 15 | File Attributes | LML 04-01 · LML 00-02(find 시간 조건) | — | ◻ |
| 16 | Extended Attributes | — | — | ◻ |
| 17 | Access Control Lists | — (빈칸) | — | ◻ |
| 18 | Directories and Links | LML 05-01 · LML 08-02(지웠지만 열린 파일) | — | ◻ |
| 19 | Monitoring File Events | — | — | ◻ |
| 20 | Signals: Fundamental Concepts | LML 03-01, 09-01 | — | ◻ |
| 21 | Signals: Signal Handlers | LML 03-01, 09-01 | — | ◻ |
| 22 | Signals: Advanced Features | — | — | ◻ |
| 23 | Timers and Sleeping | — | — | ◻ |
| 24 | Process Creation | LML 02-01 · LKP 06-01 | — | ◻ |
| 25 | Process Termination | LML 03-01(종료 상태) | — | ◻ |
| 26 | Monitoring Child Processes | — | — | ◻ |
| 27 | Program Execution | LML 02-01 | — | ◻ |
| 28 | Process Creation and Program Execution in More Detail | — | — | ◻ |
| 29 | Threads: Introduction | LKP 06-01 | — | ◻ |
| 30 | Threads: Thread Synchronization | LKP 12-01, 12-02(커널 쪽 동기화) | — | ◻ |
| 31 | Threads: Thread Safety and Per-Thread Storage | — | — | ◻ |
| 32 | Threads: Thread Cancellation | — | — | ◻ |
| 33 | Threads: Further Details | — | — | ◻ |
| 34 | Process Groups, Sessions, and Job Control | LML 03-01 · LML 00-01(nohup·disown) | — | ◻ |
| 35 | Process Priorities and Scheduling | LKP 10-01, 11-01 | — | ◻ |
| 36 | Process Resources | LML 07-02, 09-01(ulimit) | — | ◻ |
| 37 | Daemons | LML 06-01 · LML 08-01(로그) | — | ◻ |
| 38 | Writing Secure Privileged Programs | LML 04-01 | — | ◻ |
| 39 | Capabilities | LML 04-01 | — | ◻ |
| 40 | Login Accounting | LML 00-01(who·w) | — | ◻ |
| 41 | Fundamentals of Shared Libraries | — | — | ◻ |
| 42 | Advanced Features of Shared Libraries | — | — | ◻ |
| 43 | Interprocess Communication Overview | — | — | ◻ |
| 44 | Pipes and FIFOs | LML 03-01(파이프) | — | ◻ |
| 45 | Introduction to System V IPC | — | — | ◻ |
| 46 | System V Message Queues | — | — | ◻ |
| 47 | System V Semaphores | — | — | ◻ |
| 48 | System V Shared Memory | — | — | ◻ |
| 49 | Memory Mappings | — | — | ◻ |
| 50 | Virtual Memory Operations | — | — | ◻ |
| 51 | Introduction to POSIX IPC | — | — | ◻ |
| 52 | POSIX Message Queues | — | — | ◻ |
| 53 | POSIX Semaphores | — | — | ◻ |
| 54 | POSIX Shared Memory | — | — | ◻ |
| 55 | File Locking | — | — | ◻ |
| 56 | Sockets: Introduction | NPG 03-02 · LML 07-03 | — | ◻ |
| 57 | Sockets: UNIX Domain | NPG 07-01, 07-02 | — | ◻ |
| 58 | Sockets: Fundamentals of TCP/IP Networks | LML 07-01, 07-02 · NPG 03-01 | — | ◻ |
| 59 | Sockets: Internet Domains | NPG 03-02, 05-01 | — | ◻ |
| 60 | Sockets: Server Design | — | — | ◻ |
| 61 | Sockets: Advanced Topics | NPG 04-03 | — | ◻ |
| 62 | Terminals | — | — | ◻ |
| 63 | Alternative I/O Models | — | — | ◻ |
| 64 | Pseudoterminals | — | — | ◻ |



## 읽는 범위와 순서

> 64장짜리 참고서라 처음부터 끝까지 정독하지 않습니다. 기존 노트가 명령으로만 다룬 주제의 원리부터 읽습니다.

서문은 이 책을 쓰는 방법을 두 가지로 적습니다. 하나는 앞에서부터 차례로 읽는 입문서입니다. 다른 하나는 색인과 교차 참조를 따라 필요한 주제만 골라 읽는 참고서입니다. 그래서 아래 순서로 시작하고, 나머지 장은 필요할 때 엽니다.

| 순서 | 장 | 이유 |
|------|----|------|
| 1 | 17 Access Control Lists | 기존 노트에 ACL 을 받을 절이 없습니다. `getfacl`·`setfacl` 명령(17.5)과 기본 ACL(17.6)까지 이 책이 다룹니다 |
| 2 | 36 Process Resources | `ulimit` 아래의 `getrlimit()`·`setrlimit()` 와 자원별 한계(36.3)를 봅니다 |
| 3 | 14 File Systems · 18 Directories and Links | 마운트와 i-node, `unlink()` 와 공간 반환의 관계를 봅니다 |
| 4 | 15 File Attributes | 세 타임스탬프와 권한 비트(set-user-ID·sticky 포함)를 봅니다 |
| 5 | 34 Process Groups, Sessions, and Job Control | 터미널이 끊기면 `SIGHUP` 이 누구에게 가는지(34.6)를 봅니다 |
| 6 | 37 Daemons · 40 Login Accounting | 데몬이 되는 절차와 syslog, `who`·`last` 가 읽는 기록 파일을 봅니다 |

6장 Processes 는 이 표 밖에서 먼저 읽었습니다. LML 3장을 공부하다 PID·PPID 와 환경 목록의 원리를 이 책을 정본으로 삼아 따로 정리하기로 했기 때문입니다.

소켓 묶음(56~61장)은 NPG 와 TCP/IP 책들이 이미 넓게 다룹니다. 그래서 그 노트들에서 C 쪽 동작이 필요해질 때만 읽습니다.



## 이웃 책과 나눠 읽기

> 같은 주제가 세 층에 나뉘어 있습니다. 명령은 LML, 시스템 콜은 이 책, 커널 내부 구현은 LKP 가 맡습니다.

예를 들어 프로세스 우선순위는 LML 이 `nice`·`renice` 명령으로 다룹니다. 이 책 35장은 `setpriority()`·`sched_setscheduler()` 로 다루고, LKP 10~11장은 CFS 와 스케줄링 클래스가 그 값을 어떻게 쓰는지로 다룹니다. 세 노트가 같은 내용을 반복하지 않도록, 명령 사용법은 LML 에 두고 이 책의 노트는 시스템 콜이 무엇을 보장하는지에 집중합니다. 다른 층의 설명이 필요하면 링크로 넘깁니다.



## 작성 규칙

> 이 폴더의 노트를 쓸 때 지키는 규칙입니다. 책 서술과 현행 man page 를 함께 1차 자료로 씁니다.

- 파일명은 `{장}-{편}.{제목}.md` 입니다. 앞 번호는 원서의 장 번호(1~64), 뒤 번호는 그 장을 여러 편으로 나눈 순번입니다.
- 본문은 합니다체로 씁니다. 문단형 설명을 우선하고, 주장마다 왜 그런지를 함께 적습니다.
- 사실은 장별 PDF 에서 `pdftotext` 로 뽑은 본문에서 가져오고 절 번호로 출처를 밝힙니다. 2.6.35 이후 바뀌었을 수 있는 동작은 현행 man page 와 대조합니다.
- 실습 코드는 `write/` 밖의 별도 저장소에 두고, 노트에는 저장소 이름과 경로만 적습니다.
- 도식은 `_assets/` 에 두고, 생성기 선언을 원본으로 삼아 SVG 를 손으로 고치지 않습니다.



## 관련 문서

- [Learning Modern Linux 정독 인덱스](../learning-modern-linux/README.md) — 같은 주제의 명령 층
- [Linux Kernel Programming 정독 인덱스](../linux-kernel-programming/README.md) — 같은 주제의 커널 구현 층
- [Network Programming with Go 정독 인덱스](../npg_network-programming-with-go/README.md) — 소켓 묶음을 Go 로
- [OS 로드맵](../../../landscape/os-keywords.md)
- [02_os MOC](../../README.md)



## 참고 자료

- Michael Kerrisk, 『The Linux Programming Interface』 — https://man7.org/tlpi/
- Linux man-pages 프로젝트 — https://man7.org/linux/man-pages/
