---
title: kill·pgrep·killall 참조 시트
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
updated: 2026-11-11
---

# kill·pgrep·killall 참조 시트

---

> 프로세스에 신호를 보내는 `kill`, 이름이나 조건으로 PID 를 찾고 신호를 보내는 `pgrep`·`pkill`, 이름이 같은 프로세스에 한꺼번에 보내는 `killall` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 스크립트와 사용자가 모두 생깁니다.

옵션 풀이는 Linux 의 procps-ng 4.0.2(`kill`·`pgrep`·`pkill`)와 psmisc 23.6(`killall`) 기준입니다. `docker run -it --rm debian:12` 안이나 OrbStack 의 Linux VM 에서 `sudo -i` 로 연 root 셸에서 실행합니다. 준비 블록이 `apt-get`·`useradd` 를 쓰고 예가 `setpriv` 로 사용자를 바꾸므로 root 셸이어야 합니다. 출력은 Debian 12 컨테이너의 GNU bash 5.2.15 에서 받았습니다.

```bash
mkdir -p ~/cmd-lab/kill && cd ~/cmd-lab/kill
apt-get -qq update >/dev/null 2>&1; apt-get -qq install -y procps psmisc >/dev/null 2>&1
cat > trap.sh << 'EOF'
#!/bin/bash
trap 'echo "got SIGTERM, cleaning up"; exit 0' TERM
trap 'echo "got SIGHUP, reloading config"' HUP
trap 'echo "got SIGUSR1, dumping stats"' USR1
echo ready
exec 3<> <(:)
while true; do read -t 0.1 -u 3; done
EOF
cat > slow.sh << 'EOF'
#!/bin/bash
trap 'sleep 1; echo "cleanup done"; exit 0' TERM
exec 3<> <(:)
while true; do read -t 0.1 -u 3; done
EOF
chmod +x trap.sh slow.sh
ln -sf /bin/sleep mysleep
ln -sf /bin/sleep a_very_long_process_name
id app >/dev/null 2>&1 || useradd -m app
```

`trap.sh` 는 SIGTERM·SIGHUP·SIGUSR1 을 받으면 문구를 한 줄 남기는 스크립트입니다. `slow.sh` 는 SIGTERM 을 받으면 1초 뒤에 "cleanup done" 을 남기고 끝납니다. 둘 다 `sleep` 을 부르지 않고 bash 내장 `read -t` 로 기다립니다. 그래서 뒤에서 `sleep` 을 이름으로 찾는 예에 섞이지 않습니다.

`mysleep` 은 `sleep` 을 가리키는 링크라 이름만 다른 프로세스가 됩니다. `a_very_long_process_name` 은 15글자를 넘는 이름을 시험하는 링크입니다. `app` 은 사용자별로 고르는 옵션을 시험하려고 만든 일반 사용자입니다.

출력 중 PID 는 실행마다 다릅니다. 대화형 셸에서는 `&` 로 띄울 때 `[1] 123` 같은 잡 번호 줄이 더 나옵니다. 죽은 잡은 `Terminated` 같은 알림 줄을 찍습니다. 아래 출력은 그 줄과 셸 오류 메시지 앞의 `파일 이름: line N:` 접두어를 뺀 것입니다.



## 1. 신호 이름과 번호 찾기

> 신호는 이름과 번호를 모두 쓰므로, 한쪽만 알 때 다른 쪽을 바로 찾습니다.

### 이름과 번호 바꾸기

`-l` 은 신호 목록을 번호와 함께 찍고, 인자를 하나 주면 번호는 이름으로, 이름은 번호로 바꿉니다.[^killman] `kill -l 143` 처럼 종료 상태를 넣으면 128 을 뺀 번호의 이름이 나오므로 종료 상태를 해석할 때도 씁니다. 이것은 bash 내장 `kill` 의 기능이라 `/bin/kill -l 143` 은 `unknown signal name 143` 을 찍습니다.[^bashkill]

```bash
# -l: 신호 목록과 번호. 내장 kill 은 --list 를 받지 않는다. 실시간 신호는 head 로 잘랐다
kill -l | head -4
```

```bash
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL	 5) SIGTRAP
 6) SIGABRT	 7) SIGBUS	 8) SIGFPE	 9) SIGKILL	10) SIGUSR1
11) SIGSEGV	12) SIGUSR2	13) SIGPIPE	14) SIGALRM	15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD	18) SIGCONT	19) SIGSTOP	20) SIGTSTP
```

```bash
# -l 번호: 번호를 이름으로
kill -l 9       # KILL
# -l 이름: 이름을 번호로
kill -l TERM    # 15
# -l 종료 상태: 128 을 뺀 번호의 이름. 143 = 128 + 15
kill -l 143     # TERM
```

### 내장 kill 과 /bin/kill 의 목록 형식

bash 의 내장 `kill` 은 `-L` 을 `-l` 과 같은 뜻으로 받습니다.[^bashkill] procps 의 `/bin/kill` 은 `-l` 이 번호 없이 이름만 찍습니다. 번호와 이름의 표는 `-L` 이 찍습니다.[^killman]

```bash
# /bin/kill -l: 이름만 나열
/bin/kill -l
```

```bash
HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM STKFLT
CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH POLL PWR SYS
```

### 실무에서 쓰는 신호

번호는 위 `kill -l` 출력에서 가져왔고 기본 동작과 설명은 signal(7) 의 신호 표를 옮겼습니다.[^signal]

| 신호 | 번호 | 기본 동작 | signal(7) 의 설명 |
|------|------|-----------|--------------------|
| `HUP` | 1 | 종료 | Hangup detected on controlling terminal or death of controlling process |
| `INT` | 2 | 종료 | Interrupt from keyboard |
| `QUIT` | 3 | 종료 후 코어 덤프 | Quit from keyboard |
| `KILL` | 9 | 종료 | Kill signal |
| `USR1` | 10 | 종료 | User-defined signal 1 |
| `TERM` | 15 | 종료 | Termination signal |
| `CONT` | 18 | 이어서 실행 | Continue if stopped |
| `STOP` | 19 | 정지 | Stop process |

`KILL` 과 `STOP` 은 프로세스가 잡거나 막거나 무시할 수 없습니다.[^signal] `HUP` 과 `USR1` 을 받았을 때 무엇을 할지는 프로그램이 정합니다. 신호가 프로세스에 도착하는 원리는 [시그널을 보내는 세 도구 절](../../../book/learning-modern-linux/09-01.%EC%9D%B4%20%EC%9E%A5%EC%9D%84%20%EB%AC%B6%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%A3%BC%EC%A0%9C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%ED%95%84%EC%9A%94%ED%95%B4%EC%A7%80%EB%8A%94%20%EC%A1%B0%EA%B1%B4%EC%9D%B4%EB%8B%A4.md#시그널을-보내는-세-도구--killpkilltimeout)이 설명합니다.



## 2. 신호를 지정하는 세 가지 표기

> 신호를 주지 않으면 SIGTERM 이 가고, 신호를 고르는 표기는 `-s 이름`, `-이름`, `-번호` 세 가지입니다.

`kill` 의 기본 신호는 TERM 입니다. 다른 신호는 `-9`, `-SIGKILL`, `-KILL` 세 방식으로 지정합니다.[^killman] 아래 예는 `sleep 300` 을 백그라운드로 띄우고(`$!` 는 방금 띄운 프로세스의 PID 입니다) 신호를 보낸 뒤 `wait` 로 종료 상태를 받습니다. 신호로 죽은 명령의 종료 상태는 128 에 신호 번호를 더한 값입니다. 그래서 아래 네 줄이 모두 143(128 + 15)입니다. 그 규칙은 [종료 코드 128+n 절](../../../book/learning-modern-linux/09-01.%EC%9D%B4%20%EC%9E%A5%EC%9D%84%20%EB%AC%B6%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%A3%BC%EC%A0%9C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%ED%95%84%EC%9A%94%ED%95%B4%EC%A7%80%EB%8A%94%20%EC%A1%B0%EA%B1%B4%EC%9D%B4%EB%8B%A4.md#종료-코드-128n-과-systemctl-stop-의-순서)이 다룹니다.

```bash
# 신호를 주지 않으면 SIGTERM(15)
sleep 300 &
kill $!
wait $!; echo "exit $?"    # exit 143

# -s: 이름으로 지정. 내장 kill 은 --signal 을 받지 않는다
sleep 300 &
kill -s TERM $!
wait $!; echo "exit $?"    # exit 143

# -NAME: 하이픈에 신호 이름을 붙인다
sleep 300 &
kill -TERM $!
wait $!; echo "exit $?"    # exit 143

# -N: 하이픈에 신호 번호를 붙인다
sleep 300 &
kill -15 $!
wait $!; echo "exit $?"    # exit 143
```



## 3. 종료 요청과 강제 종료 구분하기

> TERM(15)은 프로세스가 받아서 정리할 기회를 주고, KILL(9)은 받을 기회 없이 커널이 끝냅니다.

`trap.sh` 는 TERM 을 받으면 정리 문구를 남기고 `exit 0` 으로 끝납니다. 같은 스크립트에 TERM 과 KILL 을 한 번씩 보내서 `t.out` 에 남은 문구를 비교합니다. 스크립트가 `trap` 을 걸 시간이 필요해서 0.5초 기다립니다.

```bash
# -15: 스크립트의 trap 이 받아서 문구를 남기고 정상 종료한다
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
# -9: trap 이 받을 수 없다. 문구 없이 죽고 종료 상태는 128 + 9
./trap.sh > t.out 2>&1 &
sleep 0.5
kill -9 $!
wait $!; echo "exit $?"    # exit 137
cat t.out                  # ready
```

TERM 쪽은 `got SIGTERM, cleaning up` 이 남고 KILL 쪽은 `ready` 뿐입니다. KILL 로 죽은 프로세스는 열어 둔 임시 파일이나 락을 스스로 치우지 못합니다. 그래서 먼저 TERM 을 보내고 안 끝날 때만 KILL 을 씁니다.



## 4. 프로세스가 살아 있는지 확인하기

> `kill -0` 은 신호를 보내지 않고 그 PID 로 보낼 수 있는지만 확인하며, 답은 종료 상태입니다.[^kill2]

```bash
# -0: 실제 신호는 없다. 프로세스가 있으면 종료 상태 0
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

PID 가 없으면 오류 메시지와 함께 종료 상태 1 입니다. 스크립트에서 쓸 때는 메시지를 버리고 종료 상태만 봅니다.



## 5. 잡 번호로 보내기와 kill 의 두 종류

> bash 에서 `kill` 을 치면 내장 명령이 실행되고, 잡 번호(`%1`)를 알아듣는 쪽도 내장입니다.

```bash
# type -a: 같은 이름의 명령이 몇 개 있고 무엇이 먼저 불리는지
type -a kill
```

```bash
kill is a shell builtin
kill is /usr/bin/kill
kill is /bin/kill
```

bash 의 `help kill` 은 내장으로 둔 이유를 두 가지로 적습니다. 하나는 PID 대신 잡 번호를 쓸 수 있게 하려는 것이고, 다른 하나는 만들 수 있는 프로세스 수가 한계에 닿아도 프로세스를 죽일 수 있게 하려는 것입니다.[^bashkill] 아래 예에서 `jobs` 로 잡 번호를 확인하고 `kill %1` 로 보냅니다.

```bash
# %1: 잡 번호로 지정. PID 를 몰라도 jobs 목록의 번호로 보낼 수 있다
sleep 300 &
jobs                  # [1]+  Running                 sleep 300 &
kill %1
# 종료가 반영될 때까지 잠깐 기다린다
sleep 0.2
```

procps 의 `/bin/kill` 은 `%1` 을 PID 로 읽으려다 실패합니다.

```bash
# /bin/kill: 외부 명령은 셸의 잡 표를 모른다
sleep 300 &
/bin/kill %1; echo "exit $?"
kill %1    # 내장 kill 로 정리
```

```bash
/bin/kill: failed to parse argument: '%1'
exit 1
```

procps 의 `kill` 매뉴얼도 셸에 내장 `kill` 이 있으면 `/bin/kill` 로 충돌을 피하라고 적습니다.[^killman]



## 6. 설정 다시 읽기와 상태 출력 시키기

> 데몬은 HUP 를 설정 다시 읽기로 받는 일이 많고, USR1 은 프로그램이 뜻을 정하는 신호입니다.

signal(7) 은 HUP 를 터미널이 끊겼을 때 가는 신호로 정의합니다.[^signal] 서버 프로그램이 이 신호를 설정 다시 읽기로 쓰는 것은 프로그램의 약속입니다. sshd 는 매뉴얼에 "rereads its configuration file when it receives a hangup signal, SIGHUP" 라고 적혀 있습니다.[^sshd] 아래는 `trap.sh` 로 그 흐름을 흉내 냅니다. HUP 와 USR1 을 받고도 프로세스는 끝나지 않습니다.

```bash
# -HUP, -USR1: 종료가 아니라 trap 이 정한 일을 하게 한다
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

Debian 12 컨테이너에서 이 블록을 여러 번 돌렸을 때는 모두 보낸 순서대로 HUP 줄이 먼저 찍혔습니다. 다만 signal(7) 은 처리 안 된 표준 신호가 여럿일 때 전달 순서를 정하지 않는다고 적습니다.[^signal] 순서가 중요하면 신호 사이에 `sleep` 을 둡니다.



## 7. 잠깐 멈췄다가 이어 가기

> STOP 은 프로세스를 얼려 두고 CONT 가 다시 돌게 합니다. 종료가 아니라 일시 정지입니다.

`ps` 의 STAT 열이 정지하면 `T`, 이어 가면 `S` 로 바뀝니다.

```bash
# -STOP: 일시 정지. STAT 가 T 로 바뀐다
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
# -CONT: 이어서 실행. STAT 가 S(잠든 상태)로 돌아온다
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



## 8. 이름으로 PID 찾기

> `pgrep` 은 프로세스 이름에 패턴이 들어 있는 PID 를 찍습니다. 옵션으로 이름을 보이게 하고, 명령줄까지 보고, 하나만 고릅니다.

패턴은 확장 정규식이고 기본으로 프로세스 이름만 검사하며, 조건을 여러 개 주면 모두 맞아야 합니다.[^pgrep] 아래 세 프로세스를 띄워 두고 시작합니다. 시작 시각 차이를 두려고 0.3초씩 쉽니다.

```bash
sleep 301 & sleep 0.3
sleep 302 & sleep 0.3
./mysleep 303 &
sleep 0.3
```

### 이름과 명령줄 보기

```bash
# 기본: PID 만. 이름에 sleep 이 든 프로세스 전부(mysleep 포함)
pgrep sleep
```

```bash
243
245
247
```

```bash
# -l (--list-name): PID 와 프로세스 이름
pgrep -l sleep
```

```bash
243 sleep
245 sleep
247 mysleep
```

```bash
# -a (--list-full): PID 와 명령줄 전체
pgrep -a sleep
```

```bash
243 sleep 301
245 sleep 302
247 ./mysleep 303
```

### 이름이 정확히 같은 것만 고르기

`mysleep` 이 걸린 것은 패턴이 이름의 일부만 맞아도 되기 때문입니다.

```bash
# -x (--exact): 이름 전체가 패턴과 같은 것만
pgrep -x sleep
```

```bash
243
245
```

```bash
# 패턴이 이름의 앞부분이어도 맞는다
pgrep slee
```

```bash
243
245
247
```

```bash
# -x 와 함께 쓰면 일부만 맞는 패턴은 탈락. 맞는 것이 없으면 종료 상태 1
pgrep -x slee; echo "exit $?"    # exit 1
```

### 명령줄로 찾기

```bash
# -f (--full): 이름이 아니라 명령줄 전체에서 찾는다. 인자로 프로세스를 구분할 때
pgrep -f 'sleep 302'    # 245
```

프로세스 이름은 `/proc/pid/stat` 에 있는 15글자까지만 비교할 수 있어서 이름이 더 긴 패턴은 맞는 것이 없다고 거절됩니다.[^pgrep]

```bash
# 15글자를 넘는 이름 패턴은 -f 를 쓰라는 안내와 함께 종료 상태 1
pgrep -l a_very_long_process_name; echo "exit $?"
```

```bash
pgrep: pattern that searches for process name longer than 15 characters will result in zero matches
Try `pgrep -f' option to match against the complete command line.
exit 1
```

### 하나만 고르기, 세기, 이어 붙이기

```bash
# -n (--newest): 가장 최근에 시작된 하나
pgrep -n sleep    # 247
# -o (--oldest): 가장 오래된 하나
pgrep -o sleep    # 243
# -c (--count): 맞는 개수만
pgrep -c sleep    # 3
# -d (--delimiter): 줄바꿈 대신 구분자로 한 줄에
pgrep -d, sleep   # 243,245,247
```

```bash
# -i (--ignore-case): 대소문자를 구분하지 않는다
pgrep -i SLEEP
```

```bash
243
245
247
```

```bash
# mysleep 만 이름으로 골라낸다
pgrep -l mysleep    # 247 mysleep
```

`-d` 로 만든 한 줄은 다른 명령의 PID 목록에 바로 붙일 수 있습니다. 매뉴얼은 `ps -fp $(pgrep -d, -x xterm)` 같은 예를 듭니다.[^pgrep]



## 9. 사용자와 부모로 좁히기

> 누가 띄웠는지(`-u`)와 누구의 자식인지(`-P`)로 대상을 줄이면 같은 이름의 다른 프로세스를 건드리지 않습니다.

`-u` 는 유효 사용자 ID 로 고릅니다. `-u root,daemon` 처럼 쉼표로 이으면 둘 중 하나(OR)이고, 다른 조건과는 모두 맞아야(AND) 합니다.[^pgrep]

```bash
setpriv --reuid=app --regid=app --clear-groups sleep 305 &
sleep 0.3
```

```bash
# -u (--euid): 그 사용자의 프로세스만
pgrep -u app -l
```

```bash
263 sleep
```

```bash
# -u root 와 패턴을 함께: root 가 띄운 sleep 계열(앞 절의 세 개)만 센다
pgrep -u root -c sleep    # 3
```

`-P` 는 부모 PID 로 고릅니다. 아래는 셸 하나가 `sleep` 두 개를 자식으로 띄운 상태에서 그 셸의 자식만 찾습니다.

```bash
bash -c 'sleep 311 & sleep 312 & wait' &
sleep 0.3
# -P (--parent): 부모 PID 가 $! 인 프로세스만
pgrep -P $! -a
```

```bash
269 sleep 311
270 sleep 312
```

같은 패턴을 `-f` 로 찾으면 자식뿐 아니라 부모 셸도 걸립니다. 명령줄에 `sleep 311` 이 들어 있기 때문입니다.

```bash
pgrep -f 'sleep 311'; echo "exit $?"
```

```bash
267
269
exit 0
```

267 이 부모 `bash -c` 이고 269 가 `sleep 311` 입니다. 종료 상태 0 은 하나 이상 맞았다는 뜻이고, 맞는 것이 없으면 1, 명령줄 문법 오류면 2 입니다.[^pgrep]



## 10. -f 가 엉뚱한 프로세스를 잡는 경우

> `pgrep -f` 는 자기 자신만 빼고 모든 명령줄을 훑으므로, 패턴 문자열을 명령줄에 가진 부모 셸이 걸립니다.

`pgrep`·`pkill` 은 자기 자신을 맞는 목록에서 빼지만 그 부모는 기본으로 빼지 않습니다.[^pgrep] 셸에서 `bash -c '... pgrep -af "패턴" ...'` 로 부르면 이 `bash -c` 의 명령줄 안에 패턴이 들어 있어 부모가 함께 잡힙니다. `bash -c` 에 명령을 하나만 주면 셸이 그 명령으로 바뀌어 부모 셸이 남지 않습니다. 그래서 아래 예는 뒤에 `; true` 를 붙여 셸을 남겨 둡니다.

```bash
# 부모 셸(bash -c)의 명령줄에도 패턴이 있어 같이 잡힌다
bash -c 'pgrep -af "sleep 302"; true'
```

```bash
245 sleep 302
273 bash -c pgrep -af "sleep 302"; true
```

패턴의 첫 글자를 대괄호로 감싸면 정규식은 `sleep 302` 와 맞지만 명령줄의 글자는 `[s]leep 302` 라서 부모가 걸리지 않습니다.

```bash
# [s]leep: 패턴 문자열 자체는 [s]leep 302 라서 부모 셸의 명령줄과 맞지 않는다
bash -c 'pgrep -af "[s]leep 302"; true'
```

```bash
245 sleep 302
```

`-A` 는 `pgrep` 자신의 조상 프로세스를 모두 맞는 목록에서 뺍니다.[^pgrep] 부모 셸이 걸리지 않고 `sleep 302` 만 남습니다.

```bash
# -A (--ignore-ancestors): 조상 프로세스(부모 bash -c)를 제외한다
bash -c 'pgrep -A -af "sleep 302"; true'    # 245 sleep 302
```

`pkill -f` 에서는 같은 문제가 자기 셸을 죽이는 사고가 됩니다. 11절에서 확인합니다. `pgrep -a` 로 대상을 먼저 찍어 본 뒤에 같은 조건으로 `pkill` 을 부르는 순서가 안전합니다.



## 11. 이름으로 신호 보내기

> `pkill` 은 `pgrep` 과 같은 선택 옵션을 받고 PID 를 찍는 대신 신호를 보냅니다. 기본 신호는 TERM 입니다.

`-신호` 로 신호를 정하고, `-e` 는 pkill 에서만 어느 프로세스에 보냈는지 찍습니다.[^pgrep]

```bash
# -u: app 이 띄운 sleep 에만. 보낸 것이 있으면 종료 상태 0
pkill -u app sleep; echo "exit $?"    # exit 0
```

```bash
# -e (--echo): 신호를 보낸 프로세스의 이름과 PID 를 찍는다. -f 라 부모 bash 도 걸렸다
pkill -e -f 'sleep 312'
```

```bash
bash killed (pid 267)
sleep killed (pid 270)
```

```bash
# 맞는 프로세스가 없으면 종료 상태 1
pkill -x nosuch; echo "exit $?"    # exit 1
```

```bash
# pkill -f 가 자기를 부른 셸까지 죽인다. survived 는 찍히지 않고 종료 상태는 128 + 15
bash -c 'pkill -f "sleep 302"; echo survived'; echo "exit $?"    # exit 143
```

`pkill` 은 자기 자신은 빼지만 부모 `bash -c` 는 명령줄에 패턴이 있어 맞았습니다. 그 셸이 TERM 으로 죽어서 `echo survived` 에 닿지 못했습니다. 아래처럼 `-A` 를 주면 부모를 빼서 `survived` 가 찍힙니다.

```bash
# 앞의 명령이 sleep 302 도 죽였으므로 다시 띄운 뒤 -A 로 조상을 제외한다
sleep 302 &
sleep 0.3
bash -c 'pkill -A -f "sleep 302"; echo survived'; echo "exit $?"
```

```bash
survived
exit 0
```

이름으로 신호를 보낼 때 `-f` 는 마지막 수단입니다. 가능하면 `-x`·`-u` 로 좁히거나 `-A` 를 함께 씁니다.

스크립트 프로세스의 이름은 스크립트 파일 이름입니다. 그래서 `pkill trap.sh` 로 부를 수 있습니다. 명령줄은 `/bin/bash ./trap.sh` 입니다.

```bash
# -USR1: 신호를 번호나 이름으로. 이름 trap.sh 로 찾는다
./trap.sh > t.out 2>&1 &
sleep 0.5
pkill -USR1 trap.sh
# -HUP -f: 명령줄로 찾는다
pkill -HUP -f 'bash ./trap.sh'
sleep 0.3
cat t.out
```

```bash
ready
got SIGUSR1, dumping stats
got SIGHUP, reloading config
```

```bash
# 신호를 주지 않으면 TERM
pkill trap.sh
sleep 0.3
cat t.out
```

```bash
ready
got SIGUSR1, dumping stats
got SIGHUP, reloading config
got SIGTERM, cleaning up
```

```bash
# 남은 sleep·mysleep 정리. -x 라 이름이 정확히 같은 것만
pkill -x sleep; pkill -x mysleep; sleep 0.3
```



## 12. 이름이 같은 프로세스 한꺼번에 다루기

> `killall` 은 PID 가 아니라 명령 이름을 받아 이름이 맞는 프로세스 모두에 신호를 보냅니다. 신호를 주지 않으면 SIGTERM 입니다.

`killall` 은 신호를 이름(`-HUP`, `-SIGHUP`)이나 번호(`-1`)나 `-s` 로 받습니다.[^killall] 이름에 `/` 가 있으면 그 파일을 실행 중인 프로세스를 고릅니다. `killall` 자신은 죽이지 않습니다.[^killall] 종료 상태는 이름마다 하나 이상 죽였으면 0 이고 아니면 0 이 아닙니다.[^killall]

### 사용자와 신호 고르기

```bash
sleep 401 & sleep 402 &
setpriv --reuid=app --regid=app --clear-groups sleep 405 &
sleep 0.3
```

```bash
# -s (--signal): TERM 이 아닌 신호. 이름이 sleep 인 프로세스 전부를 멈춘다
killall -s STOP sleep
ps -o pid,stat,user,comm -C sleep
```

```bash
    PID STAT USER     COMMAND
    301 T    root     sleep
    302 T    root     sleep
    303 T    app      sleep
```

```bash
# 멈춘 것을 이어서 실행
killall -s CONT sleep
# -u (--user): app 이 소유한 sleep 만. 이름을 빼면 app 의 프로세스 전부가 대상이다
killall -u app sleep; echo "exit $?"    # exit 0
sleep 0.3
ps -o pid,stat,user,comm -C sleep
```

```bash
    PID STAT USER     COMMAND
    301 S    root     sleep
    302 S    root     sleep
```

app 의 `sleep 405` 만 사라졌습니다. psmisc 매뉴얼은 `killall 이름` 이 비 Linux 시스템에서는 의도와 다르게 동작할 수 있다고 경고합니다.[^killall]

### 결과 확인과 조용히 하기

```bash
# -v (--verbose): 신호를 보낸 프로세스마다 한 줄
killall -v sleep
```

```bash
Killed sleep(301) with signal 15
Killed sleep(302) with signal 15
```

```bash
# 맞는 것이 없으면 메시지와 종료 상태 1
killall sleep; echo "exit $?"
```

```bash
sleep: no process found
exit 1
```

```bash
# -q (--quiet): 메시지만 뺀다. 종료 상태는 그대로 1
killall -q sleep; echo "exit $?"    # exit 1
```

```bash
# -i (--interactive): 하나씩 묻고 y 만 보낸다. 표준 입력으로 y 를 준다
sleep 501 &
sleep 0.2
killall -i sleep <<< y; echo "exit $?"    # Kill sleep(314) ? (y/N) exit 0

# n 이면 보내지 않는다. 아무것도 죽이지 않았으므로 종료 상태 1. 메시지는 버렸다
sleep 502 &
sleep 0.2
killall -i sleep 2>/dev/null <<< n; echo "exit $?"    # Kill sleep(317) ? (y/N) exit 1
```

### 이름을 정규식으로 고르기

```bash
# -r (--regexp): 이름을 POSIX 확장 정규식으로. 남아 있던 sleep 502 가 맞는다
killall -v -r '^sle+p$'    # Killed sleep(317) with signal 15
```

### 긴 이름과 -e

프로세스 이름은 15글자까지만 확인되는 경우가 있습니다. `-e` 는 그때 앞 15글자만 같은 프로세스를 건너뛰게 합니다.[^killall]

```bash
./a_very_long_process_name 400 &
sleep 0.3
# 커널이 아는 이름은 15글자로 잘려 있다
ps -o comm= -C a_very_long_pro    # a_very_long_pro
```

```bash
# -e (--exact): 긴 이름은 전체가 같은 것만. 전체 이름을 못 읽은 프로세스는 건너뛴다
killall -e -v a_very_long_process_name; echo "exit $?"
```

```bash
Killed a_very_long_process_name(321) with signal 15
exit 0
```

이 컨테이너는 전체 이름을 읽을 수 있어서 `-e` 의 유무로 결과가 갈리는 상황을 만들지 못했습니다. 위 출력은 `-e` 를 줘도 전체 이름이 같은 프로세스에는 신호가 간다는 것까지만 보여 줍니다. 전체 이름을 읽지 못하는 경우의 동작은 매뉴얼 문장으로만 적습니다.

### 끝날 때까지 기다리기

`slow.sh` 는 TERM 을 받으면 1초 뒤에 `cleanup done` 을 남깁니다. 기본으로는 신호를 보내자마자 `killall` 이 돌아오므로 그 순간 `slow.out` 은 비어 있습니다.

```bash
# 기본: 신호만 보내고 바로 돌아온다
./slow.sh > slow.out 2>&1 &
sleep 0.3
killall slow.sh; echo "killall returned"
cat slow.out    # 이 시점에는 비어 있다
sleep 1.5
cat slow.out
```

```bash
killall returned
cleanup done
```

```bash
# -w (--wait): 죽인 프로세스가 모두 사라질 때까지 1초마다 확인하며 기다린다
./slow.sh > slow.out 2>&1 &
sleep 0.3
killall -w slow.sh; echo "killall returned"
cat slow.out
```

```bash
killall returned
cleanup done
```

`-w` 일 때는 `cleanup done` 이 `killall returned` 앞에 이미 `slow.out` 에 있습니다. 신호를 무시하거나 좀비가 된 프로세스가 있으면 `-w` 는 끝나지 않을 수 있습니다.[^killall]



## 관련 문서

- [시그널을 보내는 세 도구 — kill·pkill·timeout](../../../book/learning-modern-linux/09-01.%EC%9D%B4%20%EC%9E%A5%EC%9D%84%20%EB%AC%B6%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%A3%BC%EC%A0%9C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%ED%95%84%EC%9A%94%ED%95%B4%EC%A7%80%EB%8A%94%20%EC%A1%B0%EA%B1%B4%EC%9D%B4%EB%8B%A4.md#시그널을-보내는-세-도구--killpkilltimeout) — 시그널이 프로세스에 도착하는 원리와 `timeout` 의 종료 상태
- [종료 코드 128+n 절](../../../book/learning-modern-linux/09-01.%EC%9D%B4%20%EC%9E%A5%EC%9D%84%20%EB%AC%B6%EB%8A%94%20%EA%B2%83%EC%9D%80%20%EC%A3%BC%EC%A0%9C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%ED%95%84%EC%9A%94%ED%95%B4%EC%A7%80%EB%8A%94%20%EC%A1%B0%EA%B1%B4%EC%9D%B4%EB%8B%A4.md#종료-코드-128n-과-systemctl-stop-의-순서) — 137·143 같은 종료 상태에서 신호를 읽는 법
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

- [kill(1) — procps-ng 4.0.2](https://manpages.debian.org/bookworm/procps/kill.1.en.html)
- [pgrep(1)·pkill(1) — procps-ng 4.0.2](https://manpages.debian.org/bookworm/procps/pgrep.1.en.html)
- [killall(1) — psmisc 23.6](https://manpages.debian.org/bookworm/psmisc/killall.1.en.html)
- [signal(7)](https://manpages.debian.org/bookworm/manpages/signal.7.en.html)
- [sshd(8) — OpenBSD](https://man.openbsd.org/sshd)

[^killman]: kill(1) (procps-ng 4.0.2, Debian 12) — "The default signal for kill is TERM." "Alternate signals may be specified in three ways: -9, -SIGKILL or -KILL." `-l` "List signal names. This option has optional argument, which will convert signal number to signal name, or other way round." `-L` "List signal names in a nice table." NOTES "Your shell (command line interpreter) may have a built-in kill command. You may need to run the command described here as /bin/kill to solve the conflict." https://manpages.debian.org/bookworm/procps/kill.1.en.html
[^kill2]: kill(2) (Debian 12) — "If sig is 0, then no signal is sent, but existence and permission checks are still performed; this can be used to check for the existence of a process ID or process group ID that the caller is permitted to signal." https://manpages.debian.org/bookworm/manpages-dev/kill.2.en.html
[^bashkill]: `help kill` (GNU bash 5.2.15) — "-L synonym for -l", "Kill is a shell builtin for two reasons: it allows job IDs to be used instead of process IDs, and allows processes to be killed if the limit on processes that you can create is reached." bash(1) (Debian 12) 의 kill 항목 — "The exit_status argument to -l is a number specifying either a signal number or the exit status of a process terminated by a signal." https://manpages.debian.org/bookworm/bash/bash.1.en.html
[^signal]: signal(7) (Debian 12) — SIGHUP "Hangup detected on controlling terminal or death of controlling process", SIGINT "Interrupt from keyboard", SIGQUIT "Quit from keyboard", SIGKILL "Kill signal", SIGTERM "Termination signal", SIGUSR1 "User-defined signal 1", SIGSTOP "Stop process", SIGCONT "Continue if stopped", "The signals SIGKILL and SIGSTOP cannot be caught, blocked, or ignored.", "If multiple standard signals are pending for a process, the order in which the signals are delivered is unspecified." https://manpages.debian.org/bookworm/manpages/signal.7.en.html
[^sshd]: sshd(8) (OpenBSD) — "sshd rereads its configuration file when it receives a hangup signal, SIGHUP, by executing itself with the name and options it was started with". https://man.openbsd.org/sshd
[^pgrep]: pgrep(1) (procps-ng 4.0.2, Debian 12) — "pattern Specifies an Extended Regular Expression for matching against the process names or command lines.", "All the criteria have to match.", "-signal --signal signal Defines the signal to send to each matched process.", "-u, --euid euid,... Only match processes whose effective user ID is listed.", "$ ps -fp $(pgrep -d, -x xterm)", "$ pgrep -u root,daemon will list the processes owned by root OR daemon.", "-e, --echo Display name and PID of the process being killed. (pkill only.)", "The process name used for matching is limited to the 15 characters present in the output of /proc/pid/stat. Use the -f option to match against the complete command line", "The running pgrep, pkill, or pidwait process will never report itself as a match.", "-A, --ignore-ancestors Ignore all ancestors of pgrep, pkill, or pidwait.", "-P, --parent ppid,... Only match processes whose parent process ID is listed.", 종료 상태 "0 One or more processes matched the criteria", "1 No processes matched or none of them could be signalled.", "2 Syntax error in the command line." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^killall]: killall(1) (psmisc 23.6, Debian 12) — "killall sends a signal to all processes running any of the specified commands. If no signal name is specified, SIGTERM is sent.", "Signals can be specified either by name (e.g. -HUP or -SIGHUP) or by number (e.g. -1) or by option -s.", "contains a slash (/), processes executing that particular file will be selected for killing, independent of their name.", "killall returns a zero return code if at least one process has been killed for each listed command", "killall returns non-zero otherwise.", "A killall process never kills itself", "-u, --user Kill only processes the specified user owns. Command names are optional.", "-r, --regexp Interpret process name pattern as a POSIX extended regular expression", "-i, --interactive Interactively ask for confirmation before killing", "-q, --quiet Do not complain if no processes were killed.", "-v, --verbose Report if the signal was successfully sent.", "-e, --exact Require an exact match for very long names. If a command name is longer than 15 characters, the full name may be unavailable (i.e. it is swapped out)... With -e, such entries are skipped.", "-w, --wait Wait for all killed processes to die. killall checks once per second if any of the killed processes still exist", "Note that killall may wait forever if the signal was ignored, had no effect, or if the process stays in zombie state.", "Be warned that typing killall name may not have the desired effect on non-Linux systems, especially when done by a privileged user." https://manpages.debian.org/bookworm/psmisc/killall.1.en.html
