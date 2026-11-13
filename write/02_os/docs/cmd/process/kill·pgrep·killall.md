---
title: kill·pgrep·pkill·killall 참조 시트
tags: [linux, cheatsheet, kill, pkill, pgrep, killall, signal, process, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 의 kill(1)·pgrep(1)·pkill(1) 매뉴얼 (Debian 12 bookworm)
  - psmisc 23.6 의 killall(1) 매뉴얼 (Debian 12 bookworm)
  - signal(7)·kill(2) 매뉴얼 (Debian 12 bookworm)
  - GNU bash 5.2.15 의 `help kill` 원문과 bash(1) 매뉴얼 (Debian 12 bookworm)
  - OpenBSD sshd(8) 매뉴얼
related:
  - ../README.md
  - ./kill·pgrep·killall%20이름으로%20찾아%20신호%20보내기.md
updated: 2026-11-13
---

# kill·pgrep·pkill·killall 참조 시트

---

> 프로세스에 신호를 보내는 `kill`, 이름이나 조건으로 PID 를 찾고 신호를 보내는 `pgrep`·`pkill`, 이름이 같은 프로세스에 한꺼번에 보내는 `killall` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `kill` 은 PID 나 잡 번호로 지정한 프로세스에 신호를 보내는 명령입니다.

`kill` 은 bash 내장과 procps 패키지의 `/bin/kill` 두 가지이고, bash 에서 `kill` 을 치면 내장이 실행됩니다.

이 시트는 신호 이름과 번호, `kill` 의 신호 지정과 종료·정지 예를 다루며, 이름으로 찾아 보내는 `pgrep`·`pkill`·`killall` 은 [이름으로 찾아 신호 보내기 시트](./kill·pgrep·killall%20이름으로%20찾아%20신호%20보내기.md)에서 다룹니다.

옵션 풀이는 Linux 의 procps-ng 4.0.2(`kill`·`pgrep`·`pkill`)와 psmisc 23.6(`killall`) 기준이고, 출력은 Debian 12 컨테이너의 GNU bash 5.2.15 에서 받았습니다.



## 핵심 문법

> `kill` 은 신호를 이름이나 번호로 지정해 PID 나 잡 번호에 보내고, 신호를 주지 않으면 TERM 을 보냅니다.

```bash
# 호출 형태. bash 내장 kill (help kill 의 첫 줄)
kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]

# 호출 형태. procps-ng 의 /bin/kill (--help 의 Usage 줄)
kill [options] <pid> [...]

# 신호 이름과 번호를 서로 바꾼다 (이름과 번호 바꾸기)
kill -l 신호

# /bin/kill 은 -l 이 이름만, -L 이 번호와 이름의 표를 찍는다
# (내장 kill 과 /bin/kill 의 목록 형식)
/bin/kill -l
/bin/kill -L

# 신호를 이름이나 번호로 지정해 보낸다 (신호를 지정하는 세 가지 표기)
kill -s 신호이름 PID
kill -신호이름 PID
kill -신호번호 PID

# 종료를 요청하고, 강제로 끝낸다 (종료 요청과 강제 종료 구분하기)
kill -15 PID
kill -9 PID

# 신호 없이 보낼 수 있는지만 확인한다 (프로세스가 살아 있는지 확인하기)
kill -0 PID

# 잡 번호로 보낸다 (잡 번호로 보내기)
kill %잡번호

# 종료가 아닌 신호를 보낸다 (설정 다시 읽기와 상태 출력 시키기)
kill -HUP PID
kill -USR1 PID

# 멈추고 이어 간다 (잠깐 멈췄다가 이어 가기)
kill -STOP PID
kill -CONT PID
```

### 신호

> 실무에서 쓰는 신호 여덟 개의 번호, 기본 동작, 설명입니다.

번호는 「이름과 번호 바꾸기」 의 `kill -l` 출력에서 가져왔고 기본 동작과 설명은 signal(7) 의 신호 표를 옮겼습니다.[^signal]

```bash
# 신호  번호  기본 동작          signal(7) 의 설명
# HUP     1   종료               Hangup detected on controlling terminal
#                                or death of controlling process
# INT     2   종료               Interrupt from keyboard
# QUIT    3   종료 후 코어 덤프  Quit from keyboard
# KILL    9   종료               Kill signal
# USR1   10   종료               User-defined signal 1
# TERM   15   종료               Termination signal
# CONT   18   이어서 실행        Continue if stopped
# STOP   19   정지               Stop process
# HUP 과 USR1 을 받았을 때 무엇을 할지는 프로그램이 정한다
```

`KILL` 과 `STOP` 은 프로세스가 잡거나 막거나 무시할 수 없습니다.[^signal] 신호가 프로세스에 도착하는 원리는 [시그널 노트의 「시그널 — 커널이 프로세스를 두드리는 방법」](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md#시그널--커널이-프로세스를-두드리는-방법)이 설명합니다.



## 종료 코드

> `kill` 은 신호를 보내면 0 이고, 모르는 옵션을 주거나 오류가 나면 0 이 아닌 값입니다.[^kill-exit]

내장 `kill` 은 `help kill` 의 Exit Status 를, `/bin/kill` 은 매뉴얼에 종료 코드 절이 없어 실측한 값을 싣습니다. `/bin/kill` 은 procps 가 주므로 아래 예는 「실습 준비」 블록을 돌린 셸에서 칩니다.

```bash
# 내장 kill
# 0  신호를 보냈다
# 1  PID 도 잡 번호도 아닌 인자, 없는 PID, 모르는 신호 이름처럼 오류가 났다
# 2  인자 없이 불러 사용법을 찍었다
# /bin/kill
# 1  PID 가 아닌 인자나 없는 PID 처럼 오류가 났다

# 신호를 보내면 0 이다. $! 는 방금 띄운 프로세스의 PID 다
sleep 300 &
kill $!; echo $?    # 0
wait $!

# 인자 없이 부르면 사용법을 찍고 2 로 끝난다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
kill 2>&1; echo $?
```

```bash
kill: usage: kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]
2
```

```bash
# PID 도 잡 번호도 아닌 인자는 1 이다
kill abc 2>&1; echo $?    # kill: abc: arguments must be process or job IDs / 1

# /bin/kill 은 PID 가 아닌 인자와 없는 PID 에 1 을 돌려준다
/bin/kill abc 2>&1; echo $?    # /bin/kill: failed to parse argument: 'abc' / 1
/bin/kill 999999 2>&1; echo $?    # /bin/kill: (999999): No such process / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 내장 `kill` 로 없는 PID 에 보냈을 때의 값은 「프로세스가 살아 있는지 확인하기」 에 있습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트와 이름으로 찾아 신호 보내기 시트의 예가 쓰는 스크립트와 사용자가 모두 생깁니다.

`docker run -it --rm debian:12` 안이나 OrbStack 의 Linux VM 에서 `sudo -i` 로 연 root 셸에서 실행합니다. 준비 블록이 `apt-get`·`useradd` 를 쓰고 예가 `setpriv` 로 사용자를 바꾸므로 root 셸이어야 합니다.

```bash
# 실습 폴더와 도구. procps 가 kill·pgrep·pkill 을, psmisc 가 killall 을 준다
mkdir -p ~/cmd-lab/kill && cd ~/cmd-lab/kill
apt-get -qq update >/dev/null 2>&1; \
  apt-get -qq install -y procps psmisc >/dev/null 2>&1

# trap.sh: SIGTERM·SIGHUP·SIGUSR1 을 받으면 문구를 한 줄 남기는 스크립트다
#   「종료 요청과 강제 종료 구분하기」, 「설정 다시 읽기와 상태 출력 시키기」 에서 쓴다
#   sleep 을 부르지 않고 bash 내장 read -t 로 기다려서
#   sleep 을 이름으로 찾는 예에 섞이지 않는다
cat > trap.sh << 'EOF'
#!/bin/bash
trap 'echo "got SIGTERM, cleaning up"; exit 0' TERM
trap 'echo "got SIGHUP, reloading config"' HUP
trap 'echo "got SIGUSR1, dumping stats"' USR1
echo ready
exec 3<> <(:)
while true; do read -t 0.1 -u 3; done
EOF

# slow.sh: SIGTERM 을 받으면 1초 뒤에 "cleanup done" 을 남기고 끝난다
#   이름으로 찾아 신호 보내기 시트의 「killall 끝날 때까지 기다리기」 에서 쓴다
#   trap.sh 와 같이 read -t 로 기다려서 sleep 을 이름으로 찾는 예에 섞이지 않는다
cat > slow.sh << 'EOF'
#!/bin/bash
trap 'sleep 1; echo "cleanup done"; exit 0' TERM
exec 3<> <(:)
while true; do read -t 0.1 -u 3; done
EOF
chmod +x trap.sh slow.sh

# mysleep: sleep 을 가리키는 링크라 이름만 다른 프로세스가 된다
ln -sf /bin/sleep mysleep

# a_very_long_process_name: 15글자를 넘는 이름을 시험하는 링크다
ln -sf /bin/sleep a_very_long_process_name

# app: 사용자별로 고르는 옵션을 시험하려고 만든 일반 사용자다
id app >/dev/null 2>&1 || useradd -m app
```

출력 중 PID 는 실행마다 다릅니다. 대화형 셸에서 `&` 로 띄울 때 더 나오는 `[1] 123` 같은 잡 번호 줄과 죽은 잡의 `Terminated` 같은 알림 줄, 셸 오류 메시지 앞의 `파일 이름: line N:` 접두어는 아래 출력에서 뺐습니다.

### 이름과 번호 바꾸기

> 신호는 이름과 번호를 모두 쓰므로, `-l` 로 한쪽만 알 때 다른 쪽을 바로 찾습니다.

인자를 하나 주면 번호는 이름으로, 이름은 번호로 바뀝니다.[^killman]

```bash
# 신호 20개가 번호와 함께 다섯 열로 나온다
#   -l   신호 목록과 번호를 찍는다. 내장 kill 은 --list 를 받지 않는다
# 실시간 신호는 head 로 잘랐다
kill -l | head -4
```

```bash
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL	 5) SIGTRAP
 6) SIGABRT	 7) SIGBUS	 8) SIGFPE	 9) SIGKILL	10) SIGUSR1
11) SIGSEGV	12) SIGUSR2	13) SIGPIPE	14) SIGALRM	15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD	18) SIGCONT	19) SIGSTOP	20) SIGTSTP
```

```bash
# 인자를 주면 번호는 이름으로, 이름은 번호로, 종료 상태는 이름으로 바뀐다
# -l 번호: 번호를 이름으로
kill -l 9       # KILL
# -l 이름: 이름을 번호로
kill -l TERM    # 15
# -l 종료 상태: 128 을 뺀 번호의 이름. 143 = 128 + 15
kill -l 143     # TERM
```

종료 상태를 넣는 것은 내장 `kill` 의 기능이라 `/bin/kill -l 143` 은 `unknown signal name 143` 을 찍습니다.[^bashkill]

### 내장 kill 과 /bin/kill 의 목록 형식

> 내장 `kill -l` 은 번호와 이름을, `/bin/kill -l` 은 이름만 찍습니다.

bash 의 내장 `kill` 은 `-L` 을 `-l` 과 같은 뜻으로 받습니다.[^bashkill] 번호와 이름의 표는 `/bin/kill` 에서 `-L` 이 찍습니다.[^killman]

```bash
# 번호 없이 이름만 두 줄로 나열한다
#   -l   신호 이름 목록을 찍는다 (--list)
/bin/kill -l
```

```bash
HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM STKFLT
CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH POLL PWR SYS
```

### 신호를 지정하는 세 가지 표기

> 세 표기는 같은 신호를 보내고, 신호로 죽은 프로세스의 종료 상태는 128 에 신호 번호를 더한 값입니다.

`kill` 의 기본 신호는 TERM 이고, 다른 신호는 `-9`, `-SIGKILL`, `-KILL` 세 방식으로 지정합니다.[^killman] 종료 상태의 규칙은 [시그널 노트의 「128+n 종료 코드와 systemctl stop」](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md#128n-종료-코드와-systemctl-stop)이 다룹니다.

```bash
# 신호를 주지 않으면 SIGTERM(15)이 간다. 네 예 모두 종료 상태가 143 이다
#   sleep 300 &   백그라운드로 띄운다
#   wait $!       그 프로세스가 끝나기를 기다려 종료 상태를 받는다
# 신호로 죽은 명령의 종료 상태는 128 에 신호 번호를 더한 값이라 143(128 + 15)이다
sleep 300 &
kill $!
wait $!; echo "exit $?"    # exit 143

# 이름으로 지정한 TERM 이 간다
#   -s   신호를 이름으로 지정한다. 내장 kill 은 --signal 을 받지 않는다
sleep 300 &
kill -s TERM $!
wait $!; echo "exit $?"    # exit 143

# 하이픈에 신호 이름을 붙여도 TERM 이 간다
#   -NAME   하이픈에 신호 이름을 붙인다
sleep 300 &
kill -TERM $!
wait $!; echo "exit $?"    # exit 143

# 하이픈에 신호 번호를 붙여도 TERM 이 간다
#   -N   하이픈에 신호 번호를 붙인다
sleep 300 &
kill -15 $!
wait $!; echo "exit $?"    # exit 143
```

### 종료 요청과 강제 종료 구분하기

> TERM(15)은 프로세스가 받아서 정리할 기회를 주고, KILL(9)은 받을 기회 없이 커널이 끝냅니다.

같은 `trap.sh` 에 TERM 과 KILL 을 한 번씩 보내 `t.out` 에 남은 문구를 비교합니다. `sleep 0.5` 는 스크립트가 `trap` 을 걸 시간을 줍니다.

```bash
# trap.sh 는 TERM 을 받으면 정리 문구를 남기고 exit 0 으로 끝난다
# -15 를 보내면 문구가 t.out 에 두 줄 남고 종료 상태는 0 이다
./trap.sh > t.out 2>&1 &
sleep 0.5
kill -15 $!
wait $!; echo "exit $?"    # exit 0
cat t.out
```

```bash
ready
got SIGTERM, cleaning up
```

```bash
# -9 는 trap 이 받을 수 없다. 문구 없이 죽고 종료 상태는 128 + 9 다
./trap.sh > t.out 2>&1 &
sleep 0.5
kill -9 $!
wait $!; echo "exit $?"    # exit 137
cat t.out                  # ready
```

KILL 로 죽은 프로세스는 열어 둔 임시 파일이나 락을 스스로 치우지 못합니다. 그래서 먼저 TERM 을 보내고 안 끝날 때만 KILL 을 씁니다.

### 프로세스가 살아 있는지 확인하기

> `kill -0` 은 신호를 보내지 않고 그 PID 로 보낼 수 있는지만 확인하며, 답은 종료 상태입니다.[^kill2]

```bash
# 살아 있는 동안은 0 이고, 죽인 뒤에는 오류 메시지와 1 이 나온다
#   -0   실제 신호는 없다. 프로세스가 있으면 종료 상태 0
./trap.sh > t.out 2>&1 &
sleep 0.5
kill -0 $!; echo "alive? $?"    # alive? 0
kill $!
wait $!
kill -0 $!; echo "alive? $?"
```

```bash
kill: (225) - No such process
alive? 1
```

스크립트에서 쓸 때는 메시지를 버리고 종료 상태만 봅니다.

### 잡 번호로 보내기

> 잡 번호(`%1`)로 보내면 PID 를 몰라도 `jobs` 목록의 번호로 신호를 보냅니다.

```bash
# jobs 로 잡 번호를 확인하고 kill %1 로 보내면 그 sleep 이 끝난다
#   %1   잡 번호로 지정한다. PID 를 몰라도 jobs 목록의 번호로 보낼 수 있다
sleep 300 &
jobs                  # [1]+  Running                 sleep 300 &
kill %1
# 종료가 반영될 때까지 잠깐 기다린다
sleep 0.2
```

### 설정 다시 읽기와 상태 출력 시키기

> 데몬은 HUP 를 설정 다시 읽기로 받는 일이 많고, USR1 은 프로그램이 뜻을 정하는 신호입니다.

signal(7) 은 HUP 를 터미널이 끊겼을 때 가는 신호로 정의하고,[^signal] 서버 프로그램이 이를 설정 다시 읽기로 쓰는 것은 프로그램의 약속입니다. sshd 매뉴얼에는 "rereads its configuration file when it receives a hangup signal, SIGHUP" 라고 적혀 있습니다.[^sshd]

```bash
# trap.sh 로 그 흐름을 흉내 낸다. HUP 와 USR1 을 받고도 프로세스는 끝나지 않는다
#   -HUP, -USR1   종료가 아니라 trap 이 정한 일을 하게 하는 신호다
./trap.sh > t.out 2>&1 &
sleep 0.5
kill -HUP $!
kill -USR1 $!
sleep 0.5
cat t.out
kill $!
wait $!
```

```bash
ready
got SIGHUP, reloading config
got SIGUSR1, dumping stats
```

Debian 12 컨테이너에서 이 블록을 여러 번 돌렸을 때는 모두 보낸 순서대로 HUP 줄이 먼저 찍혔지만, signal(7) 은 처리 안 된 표준 신호가 여럿일 때 전달 순서를 정하지 않는다고 적습니다.[^signal] 순서가 중요하면 신호 사이에 `sleep` 을 둡니다.

### 잠깐 멈췄다가 이어 가기

> STOP 은 프로세스를 얼려 두고 CONT 가 다시 돌게 하므로 종료가 아니라 일시 정지입니다.

```bash
# STAT 열이 T 로 바뀐다
#   -STOP   일시 정지
#   ps -o   찍을 열을 고른다 (--format)
#   ps -p   PID 로 프로세스를 고른다 (--pid)
sleep 300 &
sleep 0.2
kill -STOP $!
sleep 0.2
ps -o pid,stat,comm -p $!
```

```bash
    PID STAT COMMAND
    237 T    sleep
```

```bash
# STAT 이 S(잠든 상태)로 돌아온다
#   -CONT   이어서 실행
kill -CONT $!
sleep 0.2
ps -o pid,stat,comm -p $!
kill $!
```

```bash
    PID STAT COMMAND
    237 S    sleep
```

프로세스를 지우지 않고 잠시 재웠다가 이어 가고 싶을 때 씁니다.



## 주의사항과 동작 원리

> 내장 `kill` 과 `/bin/kill` 은 따로 있고, 잡 번호는 내장만 알아듣습니다.

### 내장 kill 과 /bin/kill 의 차이

> bash 에서 `kill` 을 치면 내장 명령이 실행되고, 잡 번호(`%1`)를 알아듣는 쪽도 내장입니다.

bash 의 `help kill` 은 내장으로 둔 이유를 두 가지로 적습니다. 하나는 PID 대신 잡 번호를 쓸 수 있게 하려는 것이고, 다른 하나는 만들 수 있는 프로세스 수가 한계에 닿아도 프로세스를 죽일 수 있게 하려는 것입니다.[^bashkill]

```bash
# 같은 이름의 명령이 세 개이고 내장이 먼저 불린다
#   -a   같은 이름의 명령을 모두 찍는다
type -a kill
```

```bash
kill is a shell builtin
kill is /usr/bin/kill
kill is /bin/kill
```

procps 의 `/bin/kill` 은 `%1` 을 PID 로 읽으려다 실패합니다.

```bash
# /bin/kill: 외부 명령은 셸의 잡 표를 모른다
sleep 300 &
/bin/kill %1; echo "exit $?"

# 내장 kill 로 정리
kill %1
```

```bash
/bin/kill: failed to parse argument: '%1'
exit 1
```

procps 의 `kill` 매뉴얼도 셸에 내장 `kill` 이 있으면 `/bin/kill` 로 충돌을 피하라고 적습니다.[^killman]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [시그널은 번호 하나만 보내고 끝나는 모양은 처리 방식이 정한다](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md#시그널--커널이-프로세스를-두드리는-방법) — 시그널이 프로세스에 도착하는 원리
- [kill·pkill·timeout 비교](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md#killpkilltimeout-비교) — 세 도구의 기본 신호와 대상 고르는 법, `timeout` 의 종료 상태
- [128+n 종료 코드와 systemctl stop](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md#128n-종료-코드와-systemctl-stop) — 137·143 같은 종료 상태에서 신호를 읽는 법
- [pgrep·pkill·killall 이름으로 찾아 신호 보내기](./kill·pgrep·killall%20이름으로%20찾아%20신호%20보내기.md) — 이 시트의 실습 준비를 이어받아 이름으로 찾아 신호를 보내는 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `kill --help`·`man kill` 과 GNU bash 5.2.15 의 `help kill` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [kill(1) — procps-ng 4.0.2](https://manpages.debian.org/bookworm/procps/kill.1.en.html)
- [signal(7)](https://manpages.debian.org/bookworm/manpages/signal.7.en.html)
- [sshd(8) — OpenBSD](https://man.openbsd.org/sshd)

[^killman]: kill(1) (procps-ng 4.0.2, Debian 12) — "The default signal for kill is TERM." "Alternate signals may be specified in three ways: -9, -SIGKILL or -KILL." `-l` "List signal names. This option has optional argument, which will convert signal number to signal name, or other way round." `-L` "List signal names in a nice table." NOTES "Your shell (command line interpreter) may have a built-in kill command. You may need to run the command described here as /bin/kill to solve the conflict." https://manpages.debian.org/bookworm/procps/kill.1.en.html
[^kill2]: kill(2) (Debian 12) — "If sig is 0, then no signal is sent, but existence and permission checks are still performed; this can be used to check for the existence of a process ID or process group ID that the caller is permitted to signal." https://manpages.debian.org/bookworm/manpages-dev/kill.2.en.html
[^bashkill]: `help kill` (GNU bash 5.2.15) — "-L synonym for -l", "Kill is a shell builtin for two reasons: it allows job IDs to be used instead of process IDs, and allows processes to be killed if the limit on processes that you can create is reached." bash(1) (Debian 12) 의 kill 항목 — "The exit_status argument to -l is a number specifying either a signal number or the exit status of a process terminated by a signal." https://manpages.debian.org/bookworm/bash/bash.1.en.html
[^signal]: signal(7) (Debian 12) — SIGHUP "Hangup detected on controlling terminal or death of controlling process", SIGINT "Interrupt from keyboard", SIGQUIT "Quit from keyboard", SIGKILL "Kill signal", SIGTERM "Termination signal", SIGUSR1 "User-defined signal 1", SIGSTOP "Stop process", SIGCONT "Continue if stopped", "The signals SIGKILL and SIGSTOP cannot be caught, blocked, or ignored.", "If multiple standard signals are pending for a process, the order in which the signals are delivered is unspecified." https://manpages.debian.org/bookworm/manpages/signal.7.en.html
[^sshd]: sshd(8) (OpenBSD) — "sshd rereads its configuration file when it receives a hangup signal, SIGHUP, by executing itself with the name and options it was started with". https://man.openbsd.org/sshd
[^kill-exit]: `help kill` (GNU bash 5.2.15) 의 Exit Status — "Returns success unless an invalid option is given or an error occurs." kill(1) (procps-ng 4.0.2, Debian 12) 에는 종료 코드 절이 없고, 코드 2 와 `/bin/kill` 의 1 은 이 시트의 실측입니다(Debian 12, bash 5.2.15).
