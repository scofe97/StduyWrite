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
updated: 2026-11-11
---

# ps 참조 시트

---

> 지금 떠 있는 프로세스를 한 번 찍어 보는 `ps` 의 옵션을 범위 고르기, 열 고르기, 정렬, 관계와 스레드 보기, 상태 읽기로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스가 모두 뜹니다.

macOS 의 `ps` 는 BSD 판이라 열 이름과 옵션이 다르고 `pstree` 도 기본으로 없습니다. 이 시트는 procps-ng 4.0.2 의 `ps` 와 psmisc 23.6 의 `pstree` 를 씁니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 root 로 실행합니다. 출력은 터미널 폭 80열에서 받았습니다.

```bash
apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq procps psmisc python3-minimal >/dev/null 2>&1
mkdir -p ~/cmd-lab/ps && cd ~/cmd-lab/ps
set -m
cp /bin/sleep worker
cat > memhog.sh << 'EOF2'
x=$(head -c 30000000 /dev/zero | tr '\0' a)
sleep 602
echo done
EOF2
cat > threads.py << 'EOF2'
import threading, time
for _ in range(3):
    threading.Thread(target=time.sleep, args=(606,)).start()
time.sleep(606)
EOF2
./worker 600 &
./worker 601 &
yes > /dev/null &
bash memhog.sh &
sleep 603 &
sleep 0.5; kill -STOP $!
sleep 604 | sleep 605 &
python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10 --retry=3 --timeout=30s &
id appuser >/dev/null 2>&1 || useradd -m appuser
setpriv --reuid=appuser --regid=appuser --init-groups sleep 607 &
nice -n 5 sleep 608 &
bash -c '(true) & exec sleep 609' &
setsid -f sleep 610
sleep 2
```

이 블록은 관찰할 프로세스를 여럿 띄웁니다. `worker` 두 개는 `sleep` 을 복사해 이름만 바꾼 것이라 `-C worker` 로 이름을 골라 볼 수 있습니다. `yes` 는 CPU 를 계속 쓰고 `memhog.sh` 를 돌리는 `bash` 는 30MB 문자열을 변수에 쥔 채 `sleep 602` 를 자식으로 둡니다.

`set -m` 은 잡 제어를 켭니다.[^bashm] 스크립트로 돌릴 때도 대화형 셸처럼 잡마다 프로세스 그룹이 갈리게 하려는 줄입니다.

`sleep 603` 은 `SIGSTOP` 으로 멈춰 있습니다. `sleep 604 | sleep 605` 는 한 파이프라인이고 `python3` 은 스레드를 셋 더 만듭니다. `sleep 607` 은 `appuser` 소유이고 `sleep 608` 은 nice 값이 5입니다.

`sleep 609` 는 자식 `bash` 가 끝났는데도 그 자식을 거두지 않는 부모라 좀비를 하나 만듭니다. `setsid -f sleep 610` 은 제어 터미널이 없는 프로세스입니다. 대화형 셸에서는 `[1] 3096` 같은 잡 번호 줄이 더 나옵니다.

PID·`TIME`·`START`·`%CPU`·메모리 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 출력에서 PID 1 이 `bash /s/run.sh` 로 보이는 것은 이 시트를 검증한 스크립트가 PID 1 이었기 때문입니다. 직접 칠 때는 `bash` 로 나옵니다.



## 1. 범위 고르기, a·-a·-e·x 의 차이

> `ps` 는 옵션 문법이 셋 섞여 있고, 같은 `a` 도 대시가 붙느냐에 따라 고르는 범위가 달라집니다.

`ps` 는 세 가지 옵션을 받습니다. 대시를 붙이는 UNIX 옵션은 `-e`, 대시 없이 쓰는 BSD 옵션은 `aux`, 대시 두 개의 GNU 긴 옵션은 `--sort` 입니다. 셋은 서로 섞어 쓸 수 있습니다. 같은 일을 하는 동의어가 여럿인 것은 여러 표준과 구현에 맞추기 때문입니다.[^syntax]

```bash
# 옵션 없음: 같은 사용자(EUID)이고 같은 터미널에 붙은 프로세스만. 열은 PID TTY TIME CMD
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

기본 선택은 현재 사용자와 같은 유효 사용자 ID 를 가진 프로세스 가운데 이 `ps` 와 같은 터미널에 붙은 것입니다.[^select] 그래서 `appuser` 의 `sleep 607` 도, 터미널이 없는 `sleep 610` 도 빠져 있습니다.

`a`·`-a`·`-e`·`x` 가 어떻게 다른지는 표지가 될 프로세스 셋으로 봅니다. PID 1(세션 리더이고 root 소유), `appuser` 가 가진 프로세스, 터미널이 없는 프로세스(`TTY` 가 `?`)입니다. 아래 변수는 이 셋을 골라 내는 `grep -E` 패턴입니다.

```bash
pick='appuser|\?|^ +1 '
```

```bash
# -e (-A): 전부 선택. 표지 셋이 모두 나온다
# -o pid=,user=,tty=,comm= 은 필요한 열만 헤더 없이 찍는다
ps -e -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
   3124 root     ?        sleep
```

```bash
# -a: 세션 리더(PID 1)와 터미널 없는 프로세스를 뺀 전부
ps -a -o pid=,user=,tty=,comm= | grep -E "$pick"    # 3120 appuser  pts/0    sleep
```

```bash
# x: BSD 의 "tty 가 있어야 한다" 제한을 풀지만 내 소유만 (appuser 는 빠짐)
ps x -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3124 root     ?        sleep
```

```bash
# a: BSD 의 "내 것만" 제한을 풀지만 터미널이 있는 것만 (tty 없는 sleep 은 빠짐)
ps a -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
```

```bash
# ax: 두 제한을 모두 풀면 전부
ps ax -o pid=,user=,tty=,comm= | grep -E "$pick"
```

```bash
      1 root     pts/0    bash
   3120 appuser  pts/0    sleep
   3124 root     ?        sleep
```

옵션 없는 `ps` 와 같은 조건으로 위 표지만 뽑으면 PID 1 한 줄만 남습니다. 앞의 `ps` 출력에서 본 결과와 같습니다.

```bash
# 옵션 없음: 같은 사용자이고 같은 터미널
ps -o pid=,user=,tty=,comm= | grep -E "$pick"    # 1 root     pts/0    bash
```

`-a` 는 세션 리더를 뺍니다. 그래서 PID 1 이 사라지고 `appuser` 의 프로세스만 남습니다. `-a` 는 터미널이 없는 프로세스도 뺍니다. 반면 BSD 의 `a` 는 세션 리더를 그대로 두고 터미널이 있는 것만 고르므로 PID 1 이 남습니다. `x` 는 터미널 제한만 풀기 때문에 내 소유인 터미널 없는 프로세스까지 오고 `a` 와 `x` 를 함께 쓴 `ax` 는 `-e` 와 같은 범위입니다.[^select]

`ps -aux` 는 `ps aux` 와 다른 명령입니다. POSIX 와 UNIX 표준대로면 `-a` 에 `x` 라는 사용자가 소유한 프로세스를 더하라는 뜻입니다. `x` 사용자가 없으면 `ps aux` 로 읽을 수도 있지만 바뀔 수 있는 동작이라 기대지 말라고 man 은 적습니다.[^syntax] 이 환경에서는 `x` 사용자가 없어 `ps aux` 와 같은 출력이 나왔습니다.

```bash
# -aux 는 -a 에 x 사용자를 더하라는 뜻. 여기서는 aux 로 읽혔다
ps -aux 2>&1 | head -2
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.5  0.0   3784  2792 pts/0    Ss   12:23   0:00 bash /s/run.sh
```




## 2. ps -ef 와 ps aux 열 비교

> 두 형식은 보여 주는 열이 다릅니다. `-ef` 는 부모와 시작 시각 쪽, `aux` 는 CPU·메모리 쪽을 봅니다.

```bash
# -e -f: 모든 프로세스를 full format 으로. 열은 UID PID PPID C STIME TTY TIME CMD
ps -ef | head -3
```

```bash
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 12:23 pts/0    00:00:00 bash /s/run.sh
root        3096       1  0 12:23 pts/0    00:00:00 ./worker 600
```

`-f` 를 붙이면 `CMD` 가 인자까지 담긴 명령줄로 바뀝니다. 소유자(`UID`)와 부모(`PPID`)와 시작 시각(`STIME`)도 열로 붙습니다.[^fmt] `C` 는 프로세스가 사는 동안 CPU 를 쓴 비율의 정수값입니다.[^pcpu]

```bash
# aux: BSD 의 사용자 중심 형식(u)으로 전부(ax). 열은 USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
ps aux | head -3
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.5  0.0   3784  2792 pts/0    Ss   12:23   0:00 bash /s/run.sh
root        3096  0.0  0.0   2240  1132 pts/0    S    12:23   0:00 ./worker 600
```

`aux` 에서는 `PPID` 가 없는 대신 `%CPU`·`%MEM`·`VSZ`·`RSS`·`STAT` 이 있습니다. `%CPU` 는 CPU 시간을 프로세스가 돈 시간으로 나눈 값이라 지금 순간의 사용률이 아니라 시작 이후의 평균입니다. `%MEM` 은 `RSS` 를 물리 메모리로 나눈 비율입니다.[^pcpu] `VSZ`·`RSS`·`STAT` 은 8절과 7절에서 따로 봅니다.



## 3. 열 고르기와 정렬

> 필요한 열만 골라 찍고 CPU 나 메모리 순으로 늘어놓으면, 무엇이 자원을 쓰는지 한눈에 보입니다.

### 열 이름 고르기와 바꾸기

`-o` 는 찍을 열을 쉼표나 공백으로 나눠 고릅니다. `-e -o` 는 `-eo` 로 붙여 써도 됩니다. 키워드는 man 의 「STANDARD FORMAT SPECIFIERS」에 나옵니다.[^fmt]

```bash
# -e -o (--format): 열을 직접 고른다. %cpu·%mem 처럼 % 로 시작하는 키워드도 된다. -eo 로 붙여 써도 같다
ps -e -o pid,ppid,stat,%cpu,%mem,comm | head -4
```

```bash
    PID    PPID STAT %CPU %MEM COMMAND
      1       0 Ss    0.5  0.0 bash
   3096       1 S     0.0  0.0 worker
   3097       1 S     0.0  0.0 worker
```

`-o` 의 열 이름 뒤에 `=이름` 을 붙이면 헤더를 바꿉니다. 모든 열의 헤더를 비우면 헤더 줄 자체가 나오지 않아 셸 변수에 담기 좋습니다.[^fmt]

```bash
# -o pid,comm=NAME: comm 열의 헤더를 NAME 으로 바꾼다
ps -o pid,comm=NAME -C worker
```

```bash
    PID NAME
   3096 worker
   3097 worker
```

```bash
# -o pid=: 헤더를 비우면 PID 만 나온다 (kill 인자로 쓸 때)
ps -C worker -o pid=
```

```bash
   3096
   3097
```

```bash
# --no-headers: 헤더 줄을 없앤다 (--no-heading 도 같다)
ps -C worker -o pid,comm --no-headers
```

```bash
   3096 worker
   3097 worker
```

### 정렬

`--sort` 는 `[+|-]키` 형식입니다. 기본은 오름차순이고 `-` 를 붙이면 내림차순입니다. 키는 `-o` 에 쓰는 이름 그대로입니다.[^sort] `head` 를 붙여 위쪽만 봅니다. 아래 출력에는 `ps` 자신이 한 줄 끼어 있을 수 있습니다.

```bash
# --sort=-%cpu: CPU 를 많이 쓴 순서. aux 열과 같이 쓰는 형태
ps aux --sort=-%cpu | head -3
```

```bash
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        3098 99.6  0.0   2240   952 pts/0    R    12:23   0:02 yes
root        3099  3.5  0.7  62436 61360 pts/0    S    12:23   0:00 bash memhog.sh
```

```bash
# --sort=-rss: 물리 메모리(RSS)를 많이 쓴 순서
ps -eo pid,rss,comm --sort=-rss | head -4
```

```bash
    PID   RSS COMMAND
   3099 61360 bash
   3108  8404 python3
   3162  3788 ps
```

### 폭 넓히기

터미널이 80열이면 긴 명령줄은 폭에서 잘립니다. `-w` 는 넓게, 두 번 쓴 `-ww` 는 폭 제한 없이 찍습니다.[^sort]

```bash
# (옵션 없음): 80열에서 잘린다
ps -o pid,args -C python3
```

```bash
    PID COMMAND
   3108 python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10
```

```bash
# -ww (-w 두 번): 폭 제한 없이 끝까지
ps -wwo pid,args -C python3
```

```bash
    PID COMMAND
   3108 python3 threads.py --name=payment-batch-worker --queue=orders-2026-11-10 --retry=3 --timeout=30s
```




## 4. 특정 프로세스만 골라 보기

> 전체 목록에서 눈으로 찾지 않고 PID·이름·소유자·부모·터미널 가운데 아는 것으로 바로 고릅니다.

아래 예의 `pgrep -x yes` 는 이름이 정확히 `yes` 인 프로세스의 PID 를 찍는 `pgrep` 입니다.[^pgrep] 그 PID 를 `-p` 에 넘깁니다.

```bash
# -p (--pid): PID 로 고른다. 쉼표나 공백으로 여러 개를 줄 수 있다
ps -p "$(pgrep -x yes)" -o pid,stat,%cpu,comm
```

```bash
    PID STAT %CPU COMMAND
   3098 R    99.2 yes
```

```bash
# -q (--quick-pid): -p 의 빠른 판. 다른 선택이나 정렬과 함께 못 쓴다. PID 하나의 이름만 얻을 때
ps -q "$(pgrep -x yes)" -o comm=    # yes
```

`-C` 는 명령 이름으로 고릅니다. 이름이지 명령줄이 아니어서 인자는 보지 않습니다.[^list]

```bash
# -C: 실행 파일 이름으로 고른다
ps -C worker
```

```bash
    PID TTY          TIME CMD
   3096 pts/0    00:00:00 worker
   3097 pts/0    00:00:00 worker
```

```bash
# -C sleep: 이름이 같은 프로세스를 모두. -o 로 PPID·STAT·인자를 함께 본다
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

`-u` 는 유효 사용자(EUID), `-U` 는 실제 사용자(RUID) 로 고릅니다. 이름이든 ID 든 됩니다. 유효 사용자는 프로세스가 파일 접근 권한을 얻는 기준이 되는 사용자이고 실제 사용자는 프로세스를 만든 사용자입니다. 이 예에서는 둘이 같은 `appuser` 입니다.[^list]

```bash
# -u (--user): 유효 사용자 이름이나 ID 로
ps -u appuser -o pid,user,comm
```

```bash
    PID USER     COMMAND
   3120 appuser  sleep
```

```bash
# -U (--User): 실제 사용자로. ruser 와 euser 열을 나란히
ps -U appuser -o pid,ruser,euser,comm
```

```bash
    PID RUSER    EUSER    COMMAND
   3120 appuser  appuser  sleep
```

`--ppid` 는 부모 PID 로 고릅니다. 즉 그 프로세스의 자식을 모읍니다.

```bash
# --ppid: 부모가 PID 인 프로세스(자식)
ps --ppid "$(pgrep -f memhog.sh)" -o pid,ppid,comm
```

```bash
    PID    PPID COMMAND
   3105    3099 sleep
```

`-t` 는 터미널로 고릅니다. 이름은 `pts/0` 처럼 쓰고 대시 하나는 터미널에 붙지 않은 프로세스를 고릅니다.[^list]

```bash
# -t -: 터미널이 없는 프로세스
ps -t - -o pid,user,tty,comm
```

```bash
    PID USER     TT       COMMAND
   3124 root     ?        sleep
```




## 5. 부모와 자식 관계 보기

> 이 프로세스를 누가 띄웠고 어느 그룹과 세션에 속하는지는 열 몇 개와 트리 모양으로 읽습니다.

`-j` 는 작업 제어 형식이라 `PGID`(프로세스 그룹)와 `SID`(세션) 열이 붙습니다.[^fmt] 각 `worker` 는 따로 띄운 잡이라 `PGID` 가 자기 PID 와 같습니다.

```bash
# -j: PID·PGID·SID 열을 붙인 작업 제어 형식
ps -j -C worker
```

```bash
    PID    PGID     SID TTY          TIME CMD
   3096    3096       1 pts/0    00:00:00 worker
   3097    3097       1 pts/0    00:00:00 worker
```

파이프라인으로 연결한 두 프로세스는 같은 프로세스 그룹에 들어갑니다. 아래에서 `sleep 604` 와 `sleep 605` 의 `PGID` 가 같습니다.

```bash
# -o pid,pgid,sid,args: -j 의 열을 직접 고르고 인자도 함께
ps -o pid,pgid,sid,args -C sleep | grep -E 'PID|60[45]'
```

```bash
    PID    PGID     SID COMMAND
   3106    3106       1 sleep 604
   3107    3106       1 sleep 605
```

트리 모양은 `--forest` 가 가지를 ASCII 로 그립니다. 부모와 자식이 둘 다 선택돼야 가지가 이어지므로 `-e` 와 함께 씁니다.[^forest] `STAT` 이 `Z` 인 줄이 좀비입니다. 부모 `sleep 609`(PID 3122) 아래에 매달려 있습니다.

```bash
# --forest: 부모와 자식 관계를 가지 모양으로
ps -e --forest -o pid,ppid,stat,comm
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

BSD 의 `f` 는 대시 없이 같은 `\_` 가지를 그립니다. `-H` 는 가지 대신 자식을 두 칸씩 들여 씁니다.[^forest] 아래 일곱 줄 안에 PID 1 의 자식들과 `memhog.sh` 를 돌리는 `bash` 의 자식 `sleep 602` 가 들어 있습니다.

```bash
# f: BSD 형식의 forest. 대시 없이 쓴다 (-H 는 가지 대신 들여쓰기)
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

`pstree` 는 같은 계층을 PID 없이 한눈에 보이는 가지 모양으로 그립니다. `-p` 는 PID 를 괄호 안에 붙이고 압축을 끕니다.[^pstree] 같은 이름의 프로세스를 합치지 않으니 어느 `sleep` 이 어느 부모의 자식인지 보입니다. 스레드는 `{python3}` 처럼 중괄호로 보입니다.

```bash
# pstree -p: 트리에 PID 를 붙인다
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
# pstree -ps: -s 는 지정한 프로세스의 부모들을 PID 1 까지 보인다
pstree -ps "$(pgrep -x yes)"    # bash(1)---yes(3098)
```




## 6. 스레드까지 보기

> 한 프로세스 안의 스레드는 `ps` 에서 `NLWP` 로 개수, `-L` 이나 `-T` 로 목록을 봅니다.

`threads.py` 를 돌리는 `python3` 은 스레드를 셋 더 만들어 모두 넷입니다. 스레드를 펼치지 않으면 프로세스 한 줄만 나오고 개수는 `nlwp` 열로 압니다.[^thread]

```bash
# -o nlwp: 프로세스에 속한 스레드(LWP) 수
ps -o pid,nlwp,comm -C python3
```

```bash
    PID NLWP COMMAND
   3108    4 python3
```

`-L` 은 스레드마다 한 줄을 찍습니다. 기본 열 `PID LWP TTY TIME CMD` 에 스레드 ID 인 `LWP` 가 붙고 첫 줄은 `LWP` 와 `PID` 가 같습니다.[^thread]

```bash
# -L: 스레드마다 한 줄. 기본 열에 LWP 가 붙는다
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
# -T: 스레드를 보인다. spid 는 lwp 의 다른 이름이라 같은 값이 나온다
ps -T -o pid,spid,comm -C python3
```

```bash
    PID    SPID COMMAND
   3108    3108 python3
   3108    3111 python3
   3108    3112 python3
   3108    3113 python3
```

`-f` 와 함께 쓰면 `NLWP` 도 붙습니다.[^thread]

```bash
# -f -L: LWP 와 NLWP 가 모두 붙는다
ps -fL -C python3 | cut -c1-80
```

```bash
UID          PID    PPID     LWP  C NLWP STIME TTY          TIME CMD
root        3108       1    3108  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3111  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3112  0    4 12:23 pts/0    00:00:00 python3 threads
root        3108       1    3113  0    4 12:23 pts/0    00:00:00 python3 threads
```




## 7. STAT 글자 읽기

> `STAT` 은 프로세스 상태 한 글자에 보조 글자가 덧붙은 열입니다. 대문자가 상태이고 뒤에 붙는 기호가 부가 정보입니다.

man 의 「PROCESS STATE CODES」에 나온 값은 다음과 같습니다.[^stat]

| 글자 | 뜻 |
|------|-----|
| `D` | 인터럽트 불가능한 대기 (대개 I/O) |
| `I` | 유휴 커널 스레드 |
| `R` | 실행 중이거나 실행 대기 (run queue 위) |
| `S` | 인터럽트 가능한 대기 (사건 완료를 기다림) |
| `T` | 작업 제어 신호로 멈춤 |
| `t` | 추적(디버거) 중 멈춤 |
| `Z` | 좀비. 끝났지만 부모가 거두지 않음 |

`BSD` 형식이거나 `stat` 키워드를 쓰면 글자가 더 붙습니다.[^stat]

| 덧붙는 글자 | 뜻 |
|------|-----|
| `<` | 우선순위 높음 (다른 사용자에게 너그럽지 않음) |
| `N` | 우선순위 낮음 (다른 사용자에게 너그러움) |
| `L` | 페이지를 메모리에 잠금 |
| `s` | 세션 리더 |
| `l` | 멀티스레드 (CLONE_THREAD, NPTL 스레드 등) |
| `+` | 포그라운드 프로세스 그룹에 속함 |

`W`(2.6 커널 이후 쓰이지 않음)와 `X`(죽은 상태, 보이지 않아야 함)도 man 에 있습니다. `D` 와 `t` 는 이 시트의 프로세스에서 만들지 않았습니다. 컨테이너 안에서는 커널 스레드(`I`)도 보이지 않습니다. 아래에서 `R`·`S`·`T`·`Z` 와 `N`·`s`·`l` 을 직접 봅니다.

```bash
# --sort=stat: STAT 순으로 늘어놓아 어떤 글자가 어떤 프로세스에 붙었는지 본다
ps -e -o stat,pid,args --sort=stat
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

`yes` 는 `R`(실행 중), `sleep` 들은 `S`(대기)입니다. `Sl` 은 `python3` 의 스레드가 여럿이라는 뜻이고 `SN` 은 `nice -n 5` 로 우선순위를 낮춘 `sleep 608` 입니다. `Ss` 는 세션 리더입니다. `sleep 610` 은 `setsid` 로 새 세션을 열었고 PID 1 도 세션 리더입니다. `T` 는 `SIGSTOP` 으로 멈춘 `sleep 603` 이고 맨 아래 `Z` 는 좀비입니다.

### 멈춤에서 풀기

`T` 인 `sleep 603` 에 `SIGCONT` 를 보내면 다시 `S` 가 됩니다.

```bash
# 멈춘 상태
ps -o pid,stat,args -p "$(pgrep -f 'sleep 603')"
```

```bash
    PID STAT COMMAND
   3100 T    sleep 603
```

```bash
# kill -CONT 로 이어서 실행시킨 뒤
kill -CONT "$(pgrep -f 'sleep 603')"; sleep 0.2; ps -o pid,stat,args -p "$(pgrep -f 'sleep 603')"
```

```bash
    PID STAT COMMAND
   3100 S    sleep 603
```

### 좀비 찾아서 없애기

좀비는 끝난 자식이 부모가 `wait` 를 부르지 않아 프로세스 표에 남은 항목입니다. 이름은 `[bash] <defunct>` 처럼 대괄호와 `<defunct>` 로 보입니다.[^zombie] `grep -E '^(STAT|Z)'` 는 헤더와 `Z` 로 시작하는 줄만 남깁니다.

```bash
# STAT 이 Z 인 프로세스
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

부모가 끝나면 init 이 좀비를 정리합니다. 이 컨테이너에서는 PID 1 인 `bash` 가 그 일을 합니다.[^zombie] 아래에서 부모를 죽이면 좀비 줄이 사라지고 헤더만 남습니다. 첫 줄의 `Terminated` 는 잡 제어(`set -m`)를 켠 셸이 찍는 잡 알림이라 대화형 셸에서는 나오는 자리가 다를 수 있습니다.

```bash
# 부모 sleep 609 를 죽인 뒤 다시 찾는다
kill "$(pgrep -f 'sleep 609')"; sleep 0.5; ps -e -o stat,pid,ppid,args | grep -E '^(STAT|Z)'
```

```bash
[10]+  Terminated              bash -c '(true) & exec sleep 609'
STAT     PID    PPID COMMAND
```

STAT 의 원리는 [커널은 전부를 하지만 운영체제는 아니다 노트의 「프로세스의 상태」](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#프로세스의-상태)에, 프로세스가 커널의 어떤 자료구조로 표현되는지는 [프로세스는 프로그램에 커널이 자원을 붙인 것이다 노트](../../../book/tlpi_the-linux-programming-interface/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md)에 있습니다.



## 8. VSZ 와 RSS 가 재는 것

> `VSZ` 는 주소 공간으로 약속된 크기이고 `RSS` 는 지금 물리 메모리에 올라와 있는 크기입니다. 둘은 같은 값이 아닙니다.

`VSZ` 는 프로세스의 가상 메모리 크기이고 `RSS` 는 스왑 밖에 있는 물리 메모리 양입니다. 둘 다 KiB 단위입니다.[^rss]

```bash
# -o vsz,rss,%mem: 가상 크기, 물리 크기, 물리 메모리 대비 비율
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

`memhog.sh` 를 돌리는 `bash`(PID 3099)는 변수에 30MB 문자열을 쥐고 있어 `VSZ` 와 `RSS` 가 모두 약 60MB 입니다. `python3` 은 `VSZ` 가 약 230MB 로 크지만 `RSS` 는 약 8MB 입니다. `VSZ` 는 주소 공간에 잡아 둔 크기를 재고 `RSS` 는 물리 메모리에 올라온 크기를 잽니다. 그래서 잡아 두기만 하고 쓰지 않은 영역이 많으면 둘의 차이가 벌어집니다. 왜 잡아 둔 것과 올라온 것이 갈리는지는 [프로세스 메모리 노트의 「2. 가상 메모리와 페이지 테이블」](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#2-가상-메모리와-페이지-테이블)에 있습니다.

실습이 끝나면 띄운 프로세스를 정리합니다. 컨테이너를 나가면 모두 사라지므로 VM 에서 했을 때만 필요합니다. 출력은 `Killed` 알림 줄과 `memhog.sh` 가 찍는 `done` 뿐이라 싣지 않았습니다.

```bash
pkill -9 -x 'worker|yes|sleep|python3'
```



## 관련 문서

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [커널은 전부를 하지만 운영체제는 아니다](../../../book/learning-modern-linux/02-01.%EC%BB%A4%EB%84%90%EC%9D%80%20%EC%A0%84%EB%B6%80%EB%A5%BC%20%ED%95%98%EC%A7%80%EB%A7%8C%20%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%8A%94%20%EC%95%84%EB%8B%88%EB%8B%A4.md#프로세스의-상태) — 프로세스의 상태와 `ps -j` 로 보는 PID·PGID·SID
- [프로세스는 프로그램에 커널이 자원을 붙인 것이다](../../../book/tlpi_the-linux-programming-interface/06-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EC%97%90%20%EC%BB%A4%EB%84%90%EC%9D%B4%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EB%B6%99%EC%9D%B8%20%EA%B2%83%EC%9D%B4%EB%8B%A4.md) — 프로세스 구조
- [프로세스 메모리는 세그먼트와 페이지로 나뉜다](../../../book/tlpi_the-linux-programming-interface/06-02.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EB%8A%94%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EC%99%80%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A1%9C%20%EB%82%98%EB%89%9C%EB%8B%A4.md#2-가상-메모리와-페이지-테이블) — `RSS` 와 `VSZ` 의 원리



## 참고 자료

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
[^forest]: `man ps` OUTPUT MODIFIERS — `--forest` "ASCII art process tree.", `f` "ASCII art process hierarchy (forest).", `-H` "Show process hierarchy (forest)."
[^pstree]: `man pstree` (psmisc 23.6) — `-p` "Show PIDs. PIDs are shown as decimal numbers in parentheses after each process name. -p implicitly disables compaction.", `-s` "Show parent processes of the specified process." https://manpages.debian.org/bookworm/psmisc/pstree.1.en.html
[^pgrep]: `man pgrep` (procps-ng 4.0.2) — `-x, --exact` "Only match processes whose names (or command lines if -f is specified) exactly match the pattern.", `-f, --full` "The pattern is normally only matched against the process name. When -f is set, the full command line is used." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^thread]: `man ps` THREAD DISPLAY — `-L` "Show threads, possibly with LWP and NLWP columns.", `-T` "Show threads, possibly with SPID column."; STANDARD FORMAT SPECIFIERS `lwp` "light weight process (thread) ID of the dispatchable entity", `spid` "see lwp."; OUTPUT FORMAT CONTROL `-f` "When used with -L, the NLWP (number of threads) and LWP (thread ID) columns will be added."; STANDARD FORMAT SPECIFIERS `nlwp` "number of lwps (threads) in the process."
[^stat]: `man ps` PROCESS STATE CODES — "D uninterruptible sleep (usually IO)", "I Idle kernel thread", "R running or runnable (on run queue)", "S interruptible sleep (waiting for an event to complete)", "T stopped by job control signal", "t stopped by debugger during the tracing", "Z defunct ("zombie") process, terminated but not reaped by its parent". "For BSD formats and when the stat keyword is used, additional characters may be displayed: < high-priority (not nice to other users), N low-priority (nice to other users), L has pages locked into memory, s is a session leader, l is multi-threaded (using CLONE_THREAD, like NPTL pthreads do), + is in the foreground process group".
[^zombie]: `man ps` NOTES — "Processes marked <defunct> are dead processes (so-called "zombies") that remain because their parent has not destroyed them properly. These processes will be destroyed by init(8) if the parent process exits."
[^bashm]: `help set` (bash 5.2) — `-m` "Job control is enabled."
[^rss]: `man ps` STANDARD FORMAT SPECIFIERS — `vsz` "virtual memory size of the process in KiB (1024-byte units). Device mappings are currently excluded; this is subject to change.", `rss` "resident set size, the non-swapped physical memory that a task has used (in kiloBytes)."
