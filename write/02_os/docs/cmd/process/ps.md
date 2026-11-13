---
title: ps 참조 시트
tags: [linux, cheatsheet, ps, pstree, process, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 ps(1) (Debian 12 `man ps` 원문, manpages.debian.org bookworm)
  - psmisc 23.6 pstree(1) (Debian 12 `man pstree` 원문)
  - procps-ng 4.0.2 pgrep(1) (Debian 12 `man pgrep` 원문), bash 5.2.15 `help set`
related:
  - ../README.md
  - ./ps%20트리·스레드·상태%20읽기.md
updated: 2026-11-13
---

# ps 참조 시트

---

> 지금 떠 있는 프로세스를 한 번 찍어 보는 `ps` 의 옵션을 범위 고르기, 열 고르기, 정렬, 골라 보기로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `ps` 는 지금 떠 있는 프로세스를 한 번 찍어 목록으로 보여 줍니다.

procps 패키지의 외부 바이너리입니다. 이 시트는 procps-ng 4.0.2(Debian 12 컨테이너, root, 터미널 폭 80열)로 실측했고, macOS 의 `ps` 는 BSD 판이라 열 이름과 옵션이 다릅니다. 부모·자식 관계, 스레드, `STAT` 글자, `VSZ`·`RSS` 는 [ps 트리·스레드·상태 읽기 시트](./ps%20트리·스레드·상태%20읽기.md)에서 이어 다룹니다.



## 핵심 문법

> 선택 옵션은 어느 프로세스를, 출력 옵션은 어느 열을 어떤 순서로 찍을지 정합니다.

```bash
# 호출 형태. ps --help simple 의 Usage 줄
ps [options]

# 같은 사용자·같은 터미널의 프로세스만 찍는다 (범위 고르기, a·-a·-e·x 의 차이)
ps

# 전부 찍는다. -e 는 UNIX 꼴이고 ax 는 BSD 꼴이다 (범위 고르기, a·-a·-e·x 의 차이)
ps -e
ps ax

# 열 형식을 고른다. -ef 는 UNIX 꼴이고 aux 는 BSD 꼴이다 (ps -ef 와 ps aux 열 비교)
ps -ef
ps aux

# 찍을 열을 이름으로 고르고 헤더를 바꾼다 (열 이름 고르기와 바꾸기)
ps -o 열,열
ps -o 열=헤더

# 열 값 순으로 늘어놓는다. GNU 긴 옵션이다 (정렬)
ps aux --sort=-키

# 긴 명령줄을 폭 제한 없이 찍는다 (폭 넓히기)
ps -ww -o pid,args

# PID·이름·사용자·부모·터미널 가운데 아는 것으로 고른다 (특정 프로세스만 골라 보기)
ps -p PID
ps -C 이름
ps -u 사용자
ps --ppid PID
ps -t 터미널
```



## 종료 코드

> `ps` 는 매뉴얼에 종료 코드 절이 없어서 실측한 값만 싣습니다.

`man ps` 에는 종료 코드를 적은 절이 없습니다.[^ps-exit] 아래는 「실습 준비」 블록을 돌린 Debian 12 컨테이너에서 성공 하나와 실패 세 가지를 돌린 결과입니다.

```bash
# 0  PID 1 을 골랐을 때
# 1  없는 PID 를 골랐을 때, 모르는 옵션이나 틀린 인자를 줬을 때

# PID 1 하나를 골라 찍는다. 프로세스를 골랐으므로 0 으로 끝난다
#   -p   PID 로 고른다. 쉼표나 공백으로 여러 개를 줄 수 있다 (--pid)
ps -p 1; echo $?
```

```bash
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
0
```

```bash
# 없는 PID 를 고르면 헤더만 찍고 1 이다
ps -p 99999; echo $?    # PID TTY TIME CMD / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.

```bash
# 모르는 옵션은 오류 메시지와 사용법을 찍고 1 이다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
ps --bad 2>&1; echo $?
```

```bash
error: unknown gnu long option

Usage:
 ps [options]

 Try 'ps --help <simple|list|output|threads|misc|all>'
  or 'ps --help <s|l|o|t|m|a>'
 for additional help text.

For more details see ps(1).
1
```

```bash
# 틀린 인자도 오류 문구만 다를 뿐 1 이다
ps -p abc 2>&1; echo $?
```

```bash
error: process ID list syntax error

Usage:
 ps [options]

 Try 'ps --help <simple|list|output|threads|misc|all>'
  or 'ps --help <s|l|o|t|m|a>'
 for additional help text.

For more details see ps(1).
1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 모두 「실습 준비」 가 띄운 프로세스를 읽습니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스가 모두 뜹니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 root 로 실행합니다. `set -m` 은 잡 제어를 켭니다.[^bashm]

```bash
# 띄운 프로세스는 「실습 정리」 블록으로 지운다
# 대화형 셸에서는 & 로 띄울 때마다 [1] 3096 같은 잡 번호 줄이 더 나온다
# 이어지는 ps 트리·스레드·상태 읽기 시트도 같은 프로세스를 읽는다

# 패키지를 깔고 실습 폴더로 옮긴다. procps 는 ps·pgrep 을, psmisc 는 pstree 를 준다
apt-get update -qq >/dev/null 2>&1; \
  apt-get install -y -qq procps psmisc python3-minimal >/dev/null 2>&1
mkdir -p ~/cmd-lab/ps && cd ~/cmd-lab/ps

# 스크립트로 돌려도 대화형 셸처럼 잡마다 프로세스 그룹이 갈리게 한다
set -m

# worker 는 sleep 을 복사해 이름만 바꾼 것이다. -C worker 로 이름을 골라 볼 수 있다
# (「열 이름 고르기와 바꾸기」, 「특정 프로세스만 골라 보기」)
cp /bin/sleep worker

# memhog.sh 를 돌리는 bash 는 30MB 문자열을 변수에 쥔 채 sleep 602 를 자식으로 둔다
# (「정렬」, 「특정 프로세스만 골라 보기」)
cat > memhog.sh << 'EOF2'
x=$(head -c 30000000 /dev/zero | tr '\0' a)
sleep 602
echo done
EOF2

# threads.py 는 python3 이 스레드를 셋 더 만들게 한다 (「폭 넓히기」)
cat > threads.py << 'EOF2'
import threading, time
for _ in range(3):
    threading.Thread(target=time.sleep, args=(606,)).start()
time.sleep(606)
EOF2

# worker 둘. 이름으로 고르는 예에서 쓴다
./worker 600 &
./worker 601 &

# yes 는 CPU 를 계속 쓴다 (「정렬」, 「특정 프로세스만 골라 보기」)
yes > /dev/null &

# memhog.sh 를 돌리는 bash
bash memhog.sh &

# sleep 603 은 SIGSTOP 으로 멈춰 둔다 (「특정 프로세스만 골라 보기」)
sleep 603 &
sleep 0.5; kill -STOP $!

# sleep 604 | sleep 605 는 한 파이프라인이다
sleep 604 | sleep 605 &

# 긴 명령줄을 가진 python3 이다 (「폭 넓히기」)
python3 threads.py \
  --name=payment-batch-worker \
  --queue=orders-2026-11-10 \
  --retry=3 \
  --timeout=30s &

# sleep 607 은 appuser 소유이고 터미널이 같다 (「범위 고르기, a·-a·-e·x 의 차이」)
id appuser >/dev/null 2>&1 || useradd -m appuser
setpriv \
  --reuid=appuser \
  --regid=appuser \
  --init-groups \
  sleep 607 &

# sleep 608 은 nice 값이 5 이다
nice -n 5 sleep 608 &

# sleep 609 는 자식 bash 가 끝났는데도 그 자식을 거두지 않는 부모라 좀비를 하나 만든다
bash -c '(true) & exec sleep 609' &

# sleep 610 은 제어 터미널이 없는 프로세스다 (「범위 고르기, a·-a·-e·x 의 차이」)
setsid -f sleep 610
sleep 2
```

PID·`TIME`·`START`·`%CPU`·메모리 값은 실행마다 달라 이 시트의 값과 같지 않아도 됩니다. 출력에서 PID 1 이 `bash /s/run.sh` 로 보이는 것은 이 시트를 검증한 스크립트가 PID 1 이었기 때문이고, 직접 칠 때는 `bash` 로 나옵니다.

### 범위 고르기, a·-a·-e·x 의 차이

> 같은 `a` 도 대시가 붙느냐에 따라 고르는 범위가 달라집니다.

`ps` 의 세 옵션 문법은 서로 섞어 쓸 수 있고, 같은 일을 하는 동의어가 여럿인 것은 여러 표준과 구현에 맞추기 때문입니다.[^syntax] 기본 선택은 현재 사용자와 같은 유효 사용자 ID 를 가진 프로세스 가운데 이 `ps` 와 같은 터미널에 붙은 것입니다.[^select]

```bash
# 옵션 없이 호출한다. 열은 PID TTY TIME CMD 다
# appuser 의 sleep 607 도, 터미널이 없는 sleep 610 도 빠져 있다
ps
```

```bash
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
   3096 pts/0    00:00:00 worker
   3097 pts/0    00:00:00 worker
   3098 pts/0    00:00:02 yes
   3099 pts/0    00:00:00 bash
   3100 pts/0    00:00:00 sleep
   3105 pts/0    00:00:00 sleep
   3106 pts/0    00:00:00 sleep
   3107 pts/0    00:00:00 sleep
   3108 pts/0    00:00:00 python3
   3121 pts/0    00:00:00 sleep
   3122 pts/0    00:00:00 sleep
   3125 pts/0    00:00:00 bash
   3130 pts/0    00:00:00 ps
```

`a`·`-a`·`-e`·`x` 가 어떻게 다른지는 표지가 될 프로세스 셋으로 봅니다. PID 1(세션 리더이고 root 소유), `appuser` 가 가진 프로세스, 터미널이 없는 프로세스(`TTY` 가 `?`)입니다.

```bash
# 표지 셋을 골라 내는 패턴을 변수에 담는다. 이후 예가 grep -E 로 거르는 데 쓴다
#   appuser   appuser 소유 프로세스
#   \?        터미널이 없는 프로세스 (TTY 열이 ?)
#   ^ +1      PID 1. 세션 리더이고 root 소유
pick='appuser|\?|^ +1 '
```

```bash
# 표지 셋이 모두 나온다
#   -e        전부 선택한다 (-A 와 같다)
#   -o        찍을 열을 쉼표나 공백으로 나눠 고른다. 이름 뒤 = 는 헤더를 비운다 (--format)
#   grep -E   확장 정규식 $pick 에 맞는 줄만 남긴다
ps -e -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
   3124 root     ?        sleep
```

```bash
# 세션 리더(PID 1)와 터미널 없는 프로세스가 빠지고 appuser 만 남는다
#   -a   세션 리더와 터미널 없는 프로세스를 뺀 전부를 고른다
ps -a -o pid=,user=,tty=,comm= | grep -E "$pick"    # 3120 appuser  pts/0    sleep
```

```bash
# BSD 의 "tty 가 있어야 한다" 제한을 풀지만 내 소유만 고른다. appuser 는 빠진다
#   x   터미널 제한을 푼다
ps x -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3124 root     ?        sleep
```

```bash
# BSD 의 "내 것만" 제한을 풀지만 터미널이 있는 것만 고른다. tty 없는 sleep 은 빠진다
#   a   내 것만 보는 제한을 푼다
ps a -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
```

```bash
# 두 제한을 모두 풀면 전부 나온다. -e 와 같은 범위다
#   ax   a 와 x 를 함께 쓴다
ps ax -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
   3124 root     ?        sleep
```

옵션 없는 `ps` 에서 표지만 뽑으면 PID 1 한 줄만 남아 첫 출력과 같습니다.

```bash
# 옵션 없음: 같은 사용자이고 같은 터미널
ps -o pid=,user=,tty=,comm= | grep -E "$pick"    # 1 root     pts/0    bash
```

`-a` 와 `a` 의 차이는 세션 리더에 있어서, `-a` 는 PID 1 을 빼지만 BSD 의 `a` 는 세션 리더를 두고 터미널이 있는 것만 고릅니다.[^select]

### ps -ef 와 ps aux 열 비교

> `-ef` 는 부모와 시작 시각 쪽, `aux` 는 CPU·메모리 쪽의 열을 보여 줍니다.

`-f` 는 다른 UNIX 옵션에 붙여 열을 더하는 옵션입니다.[^fmt] `C` 는 프로세스가 사는 동안 CPU 를 쓴 비율의 정수값입니다.[^pcpu]

```bash
# 열은 UID PID PPID C STIME TTY TIME CMD 이고 CMD 에 인자까지 담긴다
#   -f   full format. 소유자(UID)·부모(PPID)·시작 시각(STIME) 열을 붙이고 명령줄을 찍는다
ps -ef | head -3
```

```bash
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 12:23 pts/0    00:00:00 bash /s/run.sh
root        3096       1  0 12:23 pts/0    00:00:00 ./worker 600
```

`aux` 에는 `PPID` 가 없는 대신 `%CPU`·`%MEM`·`VSZ`·`RSS`·`STAT` 이 있고, `VSZ`·`RSS`·`STAT` 은 [ps 트리·스레드·상태 읽기 시트](./ps%20트리·스레드·상태%20읽기.md)의 「VSZ 와 RSS 비교」·「STAT 글자 읽기」 에서 봅니다. `%CPU`·`%MEM` 의 정의는 man 의 「STANDARD FORMAT SPECIFIERS」 를 따랐습니다.[^pcpu]

```bash
# 열은 USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND 다
#   aux    전부(ax)를 BSD 의 사용자 중심 형식(u)으로 찍는다
#   %CPU   CPU 시간을 프로세스가 돈 시간으로 나눈 값. 시작 이후의 평균이다
#   %MEM   RSS 를 물리 메모리로 나눈 비율
ps aux | head -3
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.5  0.0   3784  2792 pts/0    Ss   12:23   0:00 bash /s/run.sh
root        3096  0.0  0.0   2240  1132 pts/0    S    12:23   0:00 ./worker 600
```

### 열 이름 고르기와 바꾸기

> 필요한 열만 골라 찍고 헤더를 바꾸거나 없앱니다.

열 이름 키워드는 man 의 「STANDARD FORMAT SPECIFIERS」 에 나옵니다.[^fmt]

```bash
# 열을 직접 고른다. %cpu·%mem 처럼 % 로 시작하는 키워드도 된다
# 열은 PID PPID STAT %CPU %MEM COMMAND 순서로 나온다
# -e -o 는 -eo 로 붙여 써도 같다
ps -e -o pid,ppid,stat,%cpu,%mem,comm | head -4
```

```bash
    PID    PPID STAT %CPU %MEM COMMAND
      1       0 Ss    0.5  0.0 bash
   3096       1 S     0.0  0.0 worker
   3097       1 S     0.0  0.0 worker
```

열 이름 뒤에 `=이름` 을 붙이면 헤더가 바뀌고, 모든 열의 헤더를 비우면 헤더 줄 자체가 나오지 않아 셸 변수에 담기 좋습니다.[^fmt]

```bash
# comm 열의 헤더가 NAME 으로 바뀌어 나온다
#   -C   실행 파일 이름으로 고른다. worker 둘이 나온다
ps -o pid,comm=NAME -C worker
```

```bash
    PID NAME
   3096 worker
   3097 worker
```

```bash
# 헤더를 비우면 PID 만 나온다. kill 인자로 쓸 때 좋다
ps -C worker -o pid=
```

```bash
   3096
   3097
```

```bash
# 헤더 줄을 없앤다. --no-heading 도 같다
#   --no-headers   헤더 줄을 찍지 않는다
ps \
  -C worker \
  -o pid,comm \
  --no-headers
```

```bash
   3096 worker
   3097 worker
```

### 정렬

> `--sort` 로 CPU 나 메모리 순으로 늘어놓으면 무엇이 자원을 쓰는지 한눈에 보입니다.

정렬 키는 「STANDARD FORMAT SPECIFIERS」 의 여러 글자 키에서 고릅니다.[^sort] `head` 를 붙여 위쪽만 보며, 출력에는 `ps` 자신이 한 줄 끼어 있을 수 있습니다.

```bash
# CPU 를 많이 쓴 순서로 늘어놓는다. yes 가 맨 위에 온다. aux 열과 같이 쓰는 형태다
#   --sort   [+|-]키 형식이다. 기본은 오름차순이고 - 를 붙이면 내림차순이다
#            키는 -o 에 쓰는 이름 그대로다
ps aux --sort=-%cpu | head -3
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        3098 99.6  0.0   2240   952 pts/0    R    12:23   0:02 yes
root        3099  3.5  0.7  62436 61360 pts/0    S    12:23   0:00 bash memhog.sh
```

```bash
# 물리 메모리(RSS)를 많이 쓴 순서로 늘어놓는다. memhog.sh 를 돌리는 bash 가 맨 위에 온다
ps -eo pid,rss,comm --sort=-rss | head -4
```

```bash
    PID   RSS COMMAND
   3099 61360 bash
   3108  8404 python3
   3162  3788 ps
```

### 폭 넓히기

> 긴 명령줄이 터미널 폭에서 잘릴 때는 `-w` 를 몇 번 쓰느냐로 폭을 고릅니다.

`-w` 는 man 의 「OUTPUT MODIFIERS」 에 있는 옵션입니다.[^sort]

```bash
# 옵션 없이 호출하면 80열에서 잘린다
ps -o pid,args -C python3
```

```bash
    PID COMMAND
   3108 python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10
```

```bash
# 명령줄이 폭 제한 없이 끝까지 나온다
#   -ww   폭을 넓힌다. -w 를 두 번 쓰면 폭 제한이 없다
ps -wwo pid,args -C python3
```

```bash
    PID COMMAND
   3108 python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10 --retry=3 --timeout=30s
```

### 특정 프로세스만 골라 보기

> 전체 목록에서 눈으로 찾지 않고 PID·이름·소유자·부모·터미널 가운데 아는 것으로 바로 고릅니다.

PID 를 구하는 `pgrep` 의 옵션 뜻은 `man pgrep` 을 따랐습니다.[^pgrep]

```bash
# yes 의 PID 를 구해 그 프로세스만 찍는다. 열은 PID STAT %CPU COMMAND 다
#   pgrep -x   이름이 정확히 yes 인 프로세스의 PID 를 찍는다
ps -p "$(pgrep -x yes)" -o pid,stat,%cpu,comm
```

```bash
    PID STAT %CPU COMMAND
   3098 R    99.2 yes
```

```bash
# -p 의 빠른 판이다. 다른 선택이나 정렬과 함께 못 쓴다. PID 하나의 이름만 얻을 때 쓴다
#   -q   PID 로 빠르게 고른다 (--quick-pid)
ps -q "$(pgrep -x yes)" -o comm=    # yes
```

`-C` 가 보는 것은 이름이지 명령줄이 아니라서 인자는 보지 않습니다.[^list]

```bash
# 이름이 worker 인 프로세스 둘이 나온다
ps -C worker
```

```bash
    PID TTY          TIME CMD
   3096 pts/0    00:00:00 worker
   3097 pts/0    00:00:00 worker
```

```bash
# 이름이 같은 프로세스를 모두 찍는다. PPID·STAT·인자를 함께 본다
ps -C sleep -o pid,ppid,stat,args
```

```bash
    PID    PPID STAT COMMAND
   3100       1 T    sleep 603
   3105    3099 S    sleep 602
   3106       1 S    sleep 604
   3107       1 S    sleep 605
   3120       1 S    sleep 607
   3121       1 SN   sleep 608
   3122       1 S    sleep 609
   3124       1 Ss   sleep 610
```

이 예에서는 유효 사용자와 실제 사용자가 모두 `appuser` 입니다.[^list]

```bash
# 유효 사용자 이름이나 ID 로 고른다
#   -u   유효 사용자(EUID)로 고른다. EUID 는 프로세스가 파일 접근 권한을 얻는 기준이 되는 사용자다 (--user)
ps -u appuser -o pid,user,comm
```

```bash
    PID USER     COMMAND
   3120 appuser  sleep
```

```bash
# 실제 사용자로 고른다. ruser 와 euser 열을 나란히 본다
#   -U   실제 사용자(RUID)로 고른다. RUID 는 프로세스를 만든 사용자다 (--User)
ps -U appuser -o pid,ruser,euser,comm
```

```bash
    PID RUSER    EUSER    COMMAND
   3120 appuser  appuser  sleep
```

```bash
# 부모가 memhog.sh 를 돌리는 bash 인 프로세스, 곧 그 자식을 모은다
#   --ppid     부모 PID 로 고른다. 즉 그 프로세스의 자식을 모은다
#   pgrep -f   이름이 아니라 명령줄 전체와 맞춘다
ps --ppid "$(pgrep -f memhog.sh)" -o pid,ppid,comm
```

```bash
    PID    PPID COMMAND
   3105    3099 sleep
```

터미널 이름은 `pts/0` 처럼 쓰고 대시 하나는 터미널에 붙지 않은 프로세스를 고릅니다.[^list]

```bash
# 터미널이 없는 프로세스를 찍는다. TT 열에 ? 가 나온다
#   -t   터미널로 고른다 (--tty)
ps -t - -o pid,user,tty,comm
```

```bash
    PID USER     TT       COMMAND
   3124 root     ?        sleep
```

### 실습 정리

> 실습이 끝나면 아래 블록으로 띄운 프로세스를 지웁니다.

컨테이너를 나가면 모두 사라지므로 VM 에서 했을 때만 필요하고, 이어서 [ps 트리·스레드·상태 읽기 시트](./ps%20트리·스레드·상태%20읽기.md)를 돌릴 때는 그 시트를 마친 뒤에 돌립니다. 출력은 `Killed` 알림 줄과 `memhog.sh` 가 찍는 `done` 뿐이라 싣지 않았습니다.

```bash
# 이름이 worker·yes·sleep·python3 인 프로세스를 SIGKILL 로 정리한다
#   -9   SIGKILL 을 보낸다
#   -x   이름이 정확히 같은 것만 고른다
pkill -9 -x 'worker|yes|sleep|python3'
```



## 주의사항과 동작 원리

### ps -aux 는 ps aux 와 다른 명령

> `ps -aux` 처럼 대시를 붙이면 `ps aux` 와 뜻이 달라질 수 있습니다.

`-aux` 는 POSIX 와 UNIX 표준대로면 `-a` 에 `x` 라는 사용자가 소유한 프로세스를 더하라는 뜻입니다. `x` 사용자가 없으면 `ps aux` 로 읽을 수도 있지만 바뀔 수 있는 동작이라 기대지 말라고 man 은 적습니다.[^syntax]

```bash
# -aux 는 -a 에 x 사용자를 더하라는 뜻이다. 여기서는 x 사용자가 없어 aux 로 읽혔다
ps -aux 2>&1 | head -2
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.5  0.0   3784  2792 pts/0    Ss   12:23   0:00 bash /s/run.sh
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ps 트리·스레드·상태 읽기 시트](./ps%20트리·스레드·상태%20읽기.md) — 부모·자식 관계와 `pstree`, 스레드, `STAT` 글자, `VSZ`·`RSS`
- [프로세스는 프로그램에 커널이 자원을 붙인 것이다](../../../book/tlpi_the-linux-programming-interface/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md) — 프로세스 구조



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `man ps` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- [ps(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/ps.1.en.html)
- [pstree(1) — Debian bookworm](https://manpages.debian.org/bookworm/psmisc/pstree.1.en.html)
- [pgrep(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/pgrep.1.en.html)

[^syntax]: `man ps` (procps-ng 4.0.2) DESCRIPTION — "This version of ps accepts several kinds of options: 1 UNIX options, which may be grouped and must be preceded by a dash. 2 BSD options, which may be grouped and must not be used with a dash. 3 GNU long options, which are preceded by two dashes." "Options of different types may be freely mixed, but conflicts can appear." "Note that ps -aux is distinct from ps aux." "The POSIX and UNIX standards require that ps -aux print all processes owned by a user named x, as well as printing all processes that would be selected by the -a option." "It is fragile, subject to change, and thus should not be relied upon." https://manpages.debian.org/bookworm/procps/ps.1.en.html
[^select]: `man ps` DESCRIPTION·SIMPLE PROCESS SELECTION — "By default, ps selects all processes with the same effective user ID (euid=EUID) as the current user and associated with the same terminal as the invoker." `-a` "Select all processes except both session leaders (see getsid(2)) and processes not associated with a terminal." `x` "Lift the BSD-style "must have a tty" restriction", `a` "Lift the BSD-style "only yourself" restriction", `-e` "Select all processes. Identical to -A."
[^fmt]: `man ps` OUTPUT FORMAT CONTROL — `-f` "Do full-format listing. This option can be combined with many other UNIX-style options to add additional columns. It also causes the command arguments to be printed.", `-F` "Extra full format.", `-j` "Jobs format.", `-o` "Headers may be renamed (ps -o pid,ruser=RealUser -o comm=Command) as desired. If all column headers are empty (ps -o pid= -o comm=) then the header line will not be output."
[^pcpu]: `man ps` STANDARD FORMAT SPECIFIERS — `c` "processor utilization. Currently, this is the integer value of the percent usage over the lifetime of the process.", `%cpu` "it is the CPU time used divided by the time the process has been running (cputime/realtime ratio), expressed as a percentage.", `%mem` "ratio of the process's resident set size to the physical memory on the machine, expressed as a percentage.", `sz` "size in physical pages of the core image of the process."
[^sort]: `man ps` OUTPUT MODIFIERS — `--sort spec` "Sorting syntax is [+|-]key[,[+|-]key[,...]]. Choose a multi-letter key from the STANDARD FORMAT SPECIFIERS section. The "+" is optional since default direction is increasing numerical or lexicographic order.", `-w` "Wide output. Use this option twice for unlimited width."
[^list]: `man ps` PROCESS SELECTION BY LIST — `-C cmdlist` "NOTE: The command name is not the same as the command line.", `-q pidlist` "No additional selection options, sorting and forest type listings are allowed in this mode.", `-t ttylist` "A plain "-" may be used to select processes not attached to any terminal.", `-u userlist` "Select by effective user ID (EUID) or name.", `-U userlist` "Select by real user ID (RUID) or name.", "The real user ID identifies the user who created the process, see getuid(2).", `-u` "The effective user ID describes the user whose file access permissions are used by the process (see geteuid(2)).", `--ppid pidlist` "That is, it selects processes that are children of those listed in pidlist."
[^pgrep]: `man pgrep` (procps-ng 4.0.2) — `-x, --exact` "Only match processes whose names (or command lines if -f is specified) exactly match the pattern.", `-f, --full` "The pattern is normally only matched against the process name. When -f is set, the full command line is used." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^bashm]: `help set` (bash 5.2) — `-m` "Job control is enabled."
[^ps-exit]: `man ps` (procps-ng 4.0.2) 의 절 제목 — "NAME", "SYNOPSIS", "DESCRIPTION", "EXAMPLES", "SIMPLE PROCESS SELECTION", "PROCESS SELECTION BY LIST", "OUTPUT FORMAT CONTROL", "OUTPUT MODIFIERS", "THREAD DISPLAY", "OTHER INFORMATION", "NOTES", "PROCESS FLAGS", "PROCESS STATE CODES", "OBSOLETE SORT KEYS", "AIX FORMAT DESCRIPTORS", "STANDARD FORMAT SPECIFIERS", "ENVIRONMENT VARIABLES", "PERSONALITY", "SEE ALSO", "STANDARDS", "AUTHOR". 이 가운데 종료 코드를 적은 절은 없습니다. https://manpages.debian.org/bookworm/procps/ps.1.en.html
