---
title: ps·pstree 트리·스레드·상태 읽기
tags: [linux, cheatsheet, ps, pstree, process, thread, zombie, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 ps(1) (Debian 12 `man ps` 원문, manpages.debian.org bookworm)
  - psmisc 23.6 pstree(1) (Debian 12 `man pstree` 원문)
  - procps-ng 4.0.2 pgrep(1) (Debian 12 `man pgrep` 원문)
related:
  - ./ps.md
  - ../README.md
updated: 2026-11-13
---

# ps·pstree 트리·스레드·상태 읽기

---

> 프로세스의 부모·자식 관계와 `pstree`, 스레드, `STAT` 글자, `VSZ`·`RSS` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> 이 시트는 프로세스가 누구의 자식이고 스레드가 몇인지, 어떤 상태이고 메모리를 얼마나 쥐었는지 읽는 `ps` 와 `pstree` 를 다룹니다.

[ps 참조 시트](./ps.md)에서 프로세스를 고르고 열을 정하는 유스케이스를 뺀 나머지를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 를 돌린 상태에서 이어지고, 출력은 같은 Debian 12 컨테이너(procps-ng 4.0.2 의 `ps`, psmisc 23.6 의 `pstree`)에서 root 로 받았습니다. `pstree` 는 psmisc 패키지의 외부 바이너리이고 macOS 에는 기본으로 없습니다.



## 핵심 문법

> 관계와 스레드는 출력 옵션으로, 상태와 메모리는 열 이름으로 읽습니다.

```bash
# 호출 형태. ps --help simple 의 Usage 줄
ps [options]

# pstree 의 사용법 줄. pstree 는 --help 를 모르는 옵션으로 읽고 이 안내를 찍는다
pstree [-acglpsStTuZ] [ -h | -H PID ] [ -n | -N type ] \
       [ -A | -G | -U ] [ PID | USER ]
pstree -V

# 작업 제어 열과 가지 모양으로 부모·자식 관계를 본다 (부모와 자식 관계 보기)
ps -j
ps -e --forest
ps axf

# 트리를 PID 와 함께 그린다 (pstree 로 계통 보기)
pstree -p
pstree -ps PID

# 스레드를 한 줄씩 펼친다 (스레드까지 보기)
ps -L
ps -T

# 상태 열을 STAT 순으로 늘어놓는다 (STAT 글자 읽기)
ps -e -o stat,pid,args --sort=stat

# 멈춘 프로세스를 이어서 실행한다 (멈춤에서 풀기)
kill -CONT PID

# STAT 이 Z 인 좀비를 찾는다 (좀비 찾아서 없애기)
ps -e -o stat,pid,ppid,args | grep -E '^(STAT|Z)'

# 가상·물리 메모리 크기를 비교한다 (VSZ 와 RSS 비교)
ps -o pid,vsz,rss,%mem,comm -p PID
```

### STAT 글자

> `STAT` 은 상태 글자 하나에 부가 정보 기호가 덧붙는 열입니다.

뜻은 `man ps` 의 「PROCESS STATE CODES」 를 따랐습니다.[^stat]

```bash
# 상태 글자. STAT 의 첫 글자다
# D   인터럽트 불가능한 대기 (대개 I/O)
# I   유휴 커널 스레드
# R   실행 중이거나 실행 대기 (run queue 위)
# S   인터럽트 가능한 대기 (사건 완료를 기다림)
# T   작업 제어 신호로 멈춤
# t   추적(디버거) 중 멈춤
# W   페이징 (2.6 커널 이후 쓰이지 않음)
# X   죽은 상태 (보이지 않아야 함)
# Z   좀비. 끝났지만 부모가 거두지 않음
```

```bash
# BSD 형식이거나 stat 키워드를 쓰면 상태 글자 뒤에 덧붙는 글자다
# <   우선순위 높음 (다른 사용자에게 너그럽지 않음)
# N   우선순위 낮음 (다른 사용자에게 너그러움)
# L   페이지를 메모리에 잠금
# s   세션 리더
# l   멀티스레드 (CLONE_THREAD, NPTL 스레드 등)
# +   포그라운드 프로세스 그룹에 속함
```



## 종료 코드

> `pstree` 는 매뉴얼에 종료 코드 절이 없어서 실측한 값만 싣습니다.

`man pstree` 에는 종료 코드를 적은 절이 없습니다.[^pstree-exit] `ps` 의 코드는 [ps 참조 시트](./ps.md)의 「종료 코드」 에 있습니다.

```bash
# 0  트리를 찍었을 때. 없는 PID 를 줘도 0 이다
# 1  없는 사용자 이름이나 모르는 옵션을 줬을 때
# 매뉴얼에 종료 코드 절이 없어 값은 모두 실측이다

# PID 1 을 뿌리로 트리를 찍는다. 트리는 버리고 종료 코드만 본다. 0 이다
pstree 1 > /dev/null; echo $?    # 0

# 없는 PID 를 줘도 아무것도 찍지 않고 0 이다
pstree 99999; echo $?    # 0

# 없는 사용자 이름은 오류를 찍고 1 이다
pstree nosuchuser; echo $?    # No such user name: nosuchuser / 1

# 모르는 옵션은 오류와 긴 사용법을 찍고 1 이다. 사용법은 첫 줄만 본다
# 2>&1 은 오류 메시지를 표준 출력에 합치고, PIPESTATUS[0] 은 pstree 의 종료 코드다
#   sed -n 1p   첫 줄만 찍는다
pstree --bad 2>&1 | sed -n 1p; echo ${PIPESTATUS[0]}    # pstree: unrecognized option '--bad' / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 모두 [ps 참조 시트](./ps.md)의 「실습 준비」 가 띄운 프로세스를 읽습니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고 원래 시트의 프로세스를 그대로 씁니다.

먼저 [ps 참조 시트](./ps.md)의 「실습 준비」 블록을 돌립니다. PID·`TIME`·`START`·`%CPU`·메모리 값이 실행마다 다른 점과 PID 1 이 `bash /s/run.sh` 로 보이는 까닭은 그 시트의 「실습 준비」 에 적은 것과 같습니다.

### 부모와 자식 관계 보기

> 이 프로세스를 누가 띄웠고 어느 그룹과 세션에 속하는지는 열 몇 개와 트리 모양으로 읽습니다.

`-j` 는 man 의 「OUTPUT FORMAT CONTROL」 에 있는 형식입니다.[^fmt]

```bash
# 각 worker 는 따로 띄운 잡이라 PGID 가 자기 PID 와 같다
#   -j   작업 제어 형식이다. PID·PGID(프로세스 그룹)·SID(세션) 열이 붙는다
#   -C   실행 파일 이름으로 고른다
ps -j -C worker
```

```bash
    PID    PGID     SID TTY          TIME CMD
   3096    3096       1 pts/0    00:00:00 worker
   3097    3097       1 pts/0    00:00:00 worker
```

```bash
# 파이프라인으로 연결한 두 프로세스는 같은 프로세스 그룹에 든다. sleep 604 와 605 의 PGID 가 같다
#   -o        찍을 열을 고른다. -j 의 열을 직접 고르고 인자도 함께 본다
#   grep -E   PID 줄과 604·605 줄만 남긴다
ps -o pid,pgid,sid,args -C sleep | grep -E 'PID|60[45]'
```

```bash
    PID    PGID     SID COMMAND
   3106    3106       1 sleep 604
   3107    3106       1 sleep 605
```

`--forest`·`f`·`-H` 는 「OUTPUT MODIFIERS」 에 있습니다.[^forest]

```bash
# 부모와 자식을 ASCII 가지 모양으로 그린다
# STAT 이 Z 인 줄이 좀비이고 부모 sleep 609(PID 3122) 아래에 매달려 있다
#   -e         전부 선택한다. 부모와 자식이 둘 다 선택돼야 가지가 이어지므로 함께 쓴다
#   --forest   가지를 그린다
ps \
  -e \
  --forest \
  -o pid,ppid,stat,comm
```

```bash
    PID    PPID STAT COMMAND
      1       0 Ss   bash
   3096       1 S    worker
   3097       1 S    worker
   3098       1 R    yes
   3099       1 S    bash
   3105    3099 S     \_ sleep
   3100       1 T    sleep
   3106       1 S    sleep
   3107       1 S    sleep
   3108       1 Sl   python3
   3120       1 S    sleep
   3121       1 SN   sleep
   3122       1 S    sleep
   3125    3122 Z     \_ bash
   3124       1 Ss   sleep
   3182       1 R+   ps
```

```bash
# BSD 꼴 f 는 대시 없이 같은 \_ 가지를 그린다
# 일곱 줄 안에 PID 1 의 자식들과 memhog.sh 를 돌리는 bash 의 자식 sleep 602 가 들어 있다
#   f   forest. -H 는 가지 대신 자식을 두 칸씩 들여 쓴다
ps axf -o pid,comm | head -7
```

```bash
    PID COMMAND
      1 bash
   3096 worker
   3097 worker
   3098 yes
   3099 bash
   3105  \_ sleep
```

### pstree 로 계통 보기

> `pstree` 는 같은 계층을 PID 없이도 한눈에 보이는 가지 모양으로 그립니다.

`-p`·`-s` 의 정의는 `man pstree` 의 OPTIONS 에 있습니다.[^pstree] PID 를 구하는 `pgrep` 의 옵션 뜻은 `man pgrep` 을 따랐습니다.[^pgrep]

```bash
# 같은 이름의 프로세스를 합치지 않으니 어느 sleep 이 어느 부모의 자식인지 보인다
# 스레드는 {python3} 처럼 중괄호로 보인다
#   -p   PID 를 괄호 안에 붙이고 압축을 끈다 (--show-pids)
pstree -p
```

```bash
bash(1)-+-bash(3099)---sleep(3105)
        |-pstree(3187)
        |-python3(3108)-+-{python3}(3111)
        |               |-{python3}(3112)
        |               `-{python3}(3113)
        |-sleep(3100)
        |-sleep(3106)
        |-sleep(3107)
        |-sleep(3121)
        |-sleep(3122)---bash(3125)
        |-sleep(3124)
        |-sleep(3120)
        |-worker(3096)
        |-worker(3097)
        `-yes(3098)
```

```bash
# yes 의 부모들을 PID 1 까지 보인다
#   -s         지정한 프로세스의 부모들을 보인다 (--show-parents)
#   pgrep -x   이름이 정확히 같은 프로세스의 PID 를 찍는다
pstree -ps "$(pgrep -x yes)"    # bash(1)---yes(3098)
```

### 스레드까지 보기

> 한 프로세스 안의 스레드는 `ps` 에서 `NLWP` 로 개수, `-L` 이나 `-T` 로 목록을 봅니다.

스레드 옵션과 `lwp`·`nlwp`·`spid` 열은 man 의 「THREAD DISPLAY」 와 「STANDARD FORMAT SPECIFIERS」 에 있습니다.[^thread]

```bash
# threads.py 를 돌리는 python3 은 스레드를 셋 더 만들어 모두 넷이다
# 스레드를 펼치지 않으면 프로세스 한 줄만 나오고 개수는 nlwp 열로 안다
#   -o nlwp   프로세스에 속한 스레드(LWP) 수
ps -o pid,nlwp,comm -C python3
```

```bash
    PID NLWP COMMAND
   3108    4 python3
```

```bash
# 스레드마다 한 줄을 찍는다. 기본 열 PID LWP TTY TIME CMD 에 스레드 ID 인 LWP 가 붙고
# 첫 줄은 LWP 와 PID 가 같다
#   -L   스레드를 한 줄씩 펼친다
ps -L -C python3
```

```bash
    PID     LWP TTY          TIME CMD
   3108    3108 pts/0    00:00:00 python3
   3108    3111 pts/0    00:00:00 python3
   3108    3112 pts/0    00:00:00 python3
   3108    3113 pts/0    00:00:00 python3
```

```bash
# spid 는 스레드 ID 열 lwp 의 다른 이름이라 같은 값이 나온다
#   -T   스레드를 보인다
ps \
  -T \
  -o pid,spid,comm \
  -C python3
```

```bash
    PID    SPID COMMAND
   3108    3108 python3
   3108    3111 python3
   3108    3112 python3
   3108    3113 python3
```

```bash
# LWP 와 NLWP 가 모두 붙는다
#   -f           full format. -L 과 함께 쓰면 NLWP 도 붙는다
#   cut -c1-80   한 줄을 80자까지만 자른다
ps -fL -C python3 | cut -c1-80
```

```bash
UID          PID    PPID     LWP  C NLWP STIME TTY          TIME CMD
root        3108       1    3108  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3111  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3112  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3113  0    4 12:23 pts/0    00:00:00 python3 threads
```

### STAT 글자 읽기

> 글자 뜻은 「핵심 문법」 의 「STAT 글자」 에 있고, 여기서는 이 프로세스들에 붙은 글자를 읽습니다.

아래에서 `R`·`S`·`T`·`Z` 와 `N`·`s`·`l` 을 직접 봅니다. STAT 의 원리는 [커널은 전부를 하지만 운영체제는 아니다 노트의 「프로세스의 상태」](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#프로세스의-상태)에, 프로세스가 커널의 어떤 자료구조로 표현되는지는 [프로세스는 프로그램에 커널이 자원을 붙인 것이다 노트](../../../book/tlpi_the-linux-programming-interface/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md)에 있습니다.

```bash
# 상태 열 stat 순으로 늘어놓아 어떤 글자가 어떤 프로세스에 붙었는지 본다
# D·t 는 이 프로세스들에서 만들지 않았고, 컨테이너 안에서는 커널 스레드(I)도 보이지 않는다
#   R    실행 중인 yes
#   S    대기 중인 sleep 들
#   Sl   python3. 스레드가 여럿이다
#   SN   nice -n 5 로 우선순위를 낮춘 sleep 608
#   Ss   세션 리더. sleep 610 은 setsid 로 새 세션을 열었고 PID 1 도 세션 리더다
#   T    SIGSTOP 으로 멈춘 sleep 603
#   Z    맨 아래의 좀비
#   --sort   STAT 순으로 늘어놓는다
ps \
  -e \
  -o stat,pid,args \
  --sort=stat
```

```bash
STAT     PID COMMAND
R       3098 yes
R+      3196 ps -e -o stat,pid,args --sort=stat
Ss         1 bash /s/run.sh
S       3096 ./worker 600
S       3097 ./worker 601
S       3099 bash memhog.sh
S       3105 sleep 602
S       3106 sleep 604
S       3107 sleep 605
Sl      3108 python3 threads.py --name=payment-batch-worker --queue=orders-2026-
S       3120 sleep 607
SN      3121 sleep 608
S       3122 sleep 609
Ss      3124 sleep 610
T       3100 sleep 603
Z       3125 [bash] <defunct>
```

### 멈춤에서 풀기

> `T` 인 `sleep 603` 에 `SIGCONT` 를 보내면 다시 `S` 가 됩니다.

```bash
# 멈춘 상태다. STAT 이 T 로 나온다
#   -p         PID 로 고른다
#   pgrep -f   이름이 아니라 명령줄 전체와 맞춘다
ps -o pid,stat,args -p "$(pgrep -f 'sleep 603')"
```

```bash
    PID STAT COMMAND
   3100 T    sleep 603
```

```bash
# kill -CONT 로 이어서 실행시킨 뒤 다시 본다. STAT 이 S 로 돌아온다
#   kill -CONT   SIGCONT 를 보내 멈춘 프로세스를 이어서 실행한다
kill -CONT "$(pgrep -f 'sleep 603')"; sleep 0.2; \
  ps -o pid,stat,args -p "$(pgrep -f 'sleep 603')"
```

```bash
    PID STAT COMMAND
   3100 S    sleep 603
```

### 좀비 찾아서 없애기

> 좀비는 끝난 자식을 부모가 `wait` 로 거두지 않아 프로세스 표에 남은 항목입니다.

이름은 `[bash] <defunct>` 처럼 대괄호와 `<defunct>` 로 보입니다.[^zombie]

```bash
# STAT 이 Z 인 프로세스를 찾는다
#   grep -E '^(STAT|Z)'   헤더와 Z 로 시작하는 줄만 남긴다
ps -e -o stat,pid,ppid,args | grep -E '^(STAT|Z)'
```

```bash
STAT     PID    PPID COMMAND
Z       3125    3122 [bash] <defunct>
```

```bash
# 그 좀비의 부모(PPID)를 찾는다. 이 부모가 자식을 거두지 않는다
ps -o pid,ppid,stat,args -p "$(pgrep -f 'sleep 609')"
```

```bash
    PID    PPID STAT COMMAND
   3122       1 S    sleep 609
```

부모가 끝나면 init 이 좀비를 정리하고, 이 컨테이너에서는 PID 1 인 `bash` 가 그 일을 합니다.[^zombie]

```bash
# 부모 sleep 609 를 죽인 뒤 다시 찾는다. 좀비 줄이 사라지고 헤더만 남는다
# 첫 줄의 Terminated 는 잡 제어(set -m)를 켠 셸이 찍는 잡 알림이라 대화형 셸에서는 나오는 자리가 다를 수 있다
kill "$(pgrep -f 'sleep 609')"; sleep 0.5; \
  ps -e -o stat,pid,ppid,args | grep -E '^(STAT|Z)'
```

```bash
[10]+  Terminated              bash -c '(true) & exec sleep 609'
STAT     PID    PPID COMMAND
```

### VSZ 와 RSS 비교

> `VSZ` 는 주소 공간으로 약속된 크기이고 `RSS` 는 지금 물리 메모리에 올라와 있는 크기라서 같은 값이 아닙니다.

두 값의 정의와 단위는 man 의 「STANDARD FORMAT SPECIFIERS」 에 있습니다.[^rss]

```bash
# memhog.sh 를 돌리는 bash(PID 3099)는 VSZ 와 RSS 가 모두 약 60MB 이다
# python3 은 VSZ 가 약 230MB 로 크지만 RSS 는 약 8MB 이다
#   vsz    프로세스의 가상 메모리 크기 (KiB)
#   rss    스왑 밖에 있는 물리 메모리 양 (KiB)
#   %mem   물리 메모리 대비 비율
ps -o pid,vsz,rss,%mem,comm -C bash,python3,worker
```

```bash
    PID    VSZ   RSS %MEM COMMAND
      1   4300  3328  0.0 bash
   3096   2240  1132  0.0 worker
   3097   2240  1132  0.0 worker
   3099  62436 61360  0.7 bash
   3108 234788  8404  0.1 python3
```

`VSZ` 는 주소 공간에 잡아 둔 크기를, `RSS` 는 물리 메모리에 올라온 크기를 재므로 잡아 두기만 하고 쓰지 않은 영역이 많으면 둘의 차이가 벌어집니다. 왜 잡아 둔 것과 올라온 것이 갈리는지는 [프로세스 메모리 노트의 「2. 가상 메모리와 페이지 테이블」](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#2-가상-메모리와-페이지-테이블)에 있습니다.

### 실습 정리

> 실습이 끝나면 [ps 참조 시트](./ps.md)가 띄운 프로세스를 아래 블록으로 지웁니다.

이 시트가 만든 파일은 없고, 컨테이너를 나가면 모두 사라지므로 VM 에서 했을 때만 필요합니다. 출력은 `Killed` 알림 줄과 `memhog.sh` 가 찍는 `done` 뿐이라 싣지 않았습니다.

```bash
# 이름이 worker·yes·sleep·python3 인 프로세스를 SIGKILL 로 정리한다
#   -9   SIGKILL 을 보낸다
#   -x   이름이 정확히 같은 것만 고른다
pkill -9 -x 'worker|yes|sleep|python3'
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ps 참조 시트](./ps.md) — 이 시트가 이어받는 실습 준비와 프로세스 고르기·열 정하기 예
- [커널은 전부를 하지만 운영체제는 아니다](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#프로세스의-상태) — 프로세스의 상태와 `ps -j` 로 보는 PID·PGID·SID
- [프로세스는 프로그램에 커널이 자원을 붙인 것이다](../../../book/tlpi_the-linux-programming-interface/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md) — 프로세스 구조
- [프로세스 메모리는 세그먼트와 페이지로 나뉜다](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#2-가상-메모리와-페이지-테이블) — `RSS` 와 `VSZ` 의 원리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `man ps` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [ps(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/ps.1.en.html)
- [pstree(1) — Debian bookworm](https://manpages.debian.org/bookworm/psmisc/pstree.1.en.html)
- [pgrep(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/pgrep.1.en.html)

[^fmt]: `man ps` OUTPUT FORMAT CONTROL — `-f` "Do full-format listing. This option can be combined with many other UNIX-style options to add additional columns. It also causes the command arguments to be printed.", `-F` "Extra full format.", `-j` "Jobs format.", `-o` "Headers may be renamed (ps -o pid,ruser=RealUser -o comm=Command) as desired. If all column headers are empty (ps -o pid= -o comm=) then the header line will not be output."
[^forest]: `man ps` OUTPUT MODIFIERS — `--forest` "ASCII art process tree.", `f` "ASCII art process hierarchy (forest).", `-H` "Show process hierarchy (forest)."
[^pstree]: `man pstree` (psmisc 23.6) — `-p` "Show PIDs. PIDs are shown as decimal numbers in parentheses after each process name. -p implicitly disables compaction.", `-s` "Show parent processes of the specified process." https://manpages.debian.org/bookworm/psmisc/pstree.1.en.html
[^pgrep]: `man pgrep` (procps-ng 4.0.2) — `-x, --exact` "Only match processes whose names (or command lines if -f is specified) exactly match the pattern.", `-f, --full` "The pattern is normally only matched against the process name. When -f is set, the full command line is used." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^thread]: `man ps` THREAD DISPLAY — `-L` "Show threads, possibly with LWP and NLWP columns.", `-T` "Show threads, possibly with SPID column."; STANDARD FORMAT SPECIFIERS `lwp` "light weight process (thread) ID of the dispatchable entity", `spid` "see lwp."; OUTPUT FORMAT CONTROL `-f` "When used with -L, the NLWP (number of threads) and LWP (thread ID) columns will be added."; STANDARD FORMAT SPECIFIERS `nlwp` "number of lwps (threads) in the process."
[^stat]: `man ps` PROCESS STATE CODES — "D uninterruptible sleep (usually IO)", "I Idle kernel thread", "R running or runnable (on run queue)", "S interruptible sleep (waiting for an event to complete)", "T stopped by job control signal", "t stopped by debugger during the tracing", "Z defunct ("zombie") process, terminated but not reaped by its parent". "For BSD formats and when the stat keyword is used, additional characters may be displayed: < high-priority (not nice to other users), N low-priority (nice to other users), L has pages locked into memory, s is a session leader, l is multi-threaded (using CLONE_THREAD, like NPTL pthreads do), + is in the foreground process group".
[^zombie]: `man ps` NOTES — "Processes marked <defunct> are dead processes (so-called "zombies") that remain because their parent has not destroyed them properly. These processes will be destroyed by init(8) if the parent process exits."
[^rss]: `man ps` STANDARD FORMAT SPECIFIERS — `vsz` "virtual memory size of the process in KiB (1024-byte units). Device mappings are currently excluded; this is subject to change.", `rss` "resident set size, the non-swapped physical memory that a task has used (in kiloBytes)."
[^pstree-exit]: `man pstree` (psmisc 23.6) 의 절 제목 — "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "FILES", "BUGS", "SEE ALSO". 이 가운데 종료 코드를 적은 절은 없습니다. https://manpages.debian.org/bookworm/psmisc/pstree.1.en.html
