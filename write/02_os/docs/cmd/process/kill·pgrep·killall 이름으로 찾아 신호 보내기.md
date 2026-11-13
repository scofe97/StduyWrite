---
title: pgrep·pkill·killall 이름으로 찾아 신호 보내기
tags: [linux, cheatsheet, pgrep, pkill, killall, process, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 의 pgrep(1)·pkill(1) 매뉴얼 (Debian 12 bookworm)
  - psmisc 23.6 의 killall(1) 매뉴얼 (Debian 12 bookworm)
  - setpriv(1) 매뉴얼 (Debian 12 bookworm)
related:
  - ./kill·pgrep·killall.md
  - ../README.md
updated: 2026-11-13
---

# pgrep·pkill·killall 이름으로 찾아 신호 보내기

---

> 이름이나 조건으로 PID 를 찾는 `pgrep`, 찾아서 신호를 보내는 `pkill`, 이름이 같은 프로세스에 한꺼번에 보내는 `killall` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `pgrep` 은 조건에 맞는 프로세스의 PID 를 찍고, `pkill` 과 `killall` 은 맞는 프로세스에 신호를 보냅니다.

[kill·pgrep·pkill·killall 참조 시트](./kill·pgrep·killall.md)에서 이름으로 찾아 신호를 보내는 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어지고, 출력은 같은 Debian 12 컨테이너(procps-ng 4.0.2 의 `pgrep`·`pkill`, psmisc 23.6 의 `killall`)의 root 셸에서 받았습니다.



## 핵심 문법

> `pgrep`·`pkill` 은 패턴과 선택 옵션으로 프로세스를 고르고, `killall` 은 명령 이름으로 고릅니다.

```bash
# 호출 형태. pgrep (--help 의 Usage 줄)
pgrep [options] <pattern>

# 호출 형태. pkill (--help 의 Usage 줄)
pkill [options] <pattern>

# 호출 형태. killall (--help 의 Usage 줄)
killall [OPTION]... [--] NAME...
killall -l, --list
killall -V, --version

# PID 를 찍는다. -l 은 이름을, -a 는 명령줄을 함께 찍는다 (pgrep 이름과 명령줄 보기)
pgrep 패턴
pgrep -l 패턴
pgrep -a 패턴

# 이름이 정확히 같은 것만 고른다 (pgrep 정확히 같은 이름만 고르기)
pgrep -x 이름

# 명령줄 전체에서 찾는다 (pgrep 명령줄로 찾기)
pgrep -f 패턴

# 하나만 고르거나 세거나 한 줄로 잇는다 (pgrep 하나만 고르기, 세기, 이어 붙이기)
pgrep -n 패턴
pgrep -o 패턴
pgrep -c 패턴
pgrep -d 구분자 패턴

# 사용자와 부모 PID 로 좁힌다 (pgrep 사용자와 부모로 좁히기)
pgrep -u 사용자 패턴
pgrep -P 부모PID 패턴

# 이름으로 신호를 보낸다. 신호를 주지 않으면 TERM 이다 (pkill 이름으로 신호 보내기)
pkill 패턴
pkill -신호 패턴

# 명령 이름이 같은 프로세스 모두에 보낸다 (killall 사용자와 신호 고르기)
killall 이름
killall -s 신호 이름
killall -u 사용자 이름

# 보낸 결과를 찍고, 메시지를 줄이고, 하나씩 묻는다 (killall 결과 확인과 조용히 하기)
killall -v 이름
killall -q 이름
killall -i 이름

# 이름을 정규식으로 고른다 (killall 이름을 정규식으로 고르기)
killall -r 정규식

# 프로세스가 끝날 때까지 기다린다 (killall 끝날 때까지 기다리기)
killall -w 이름
```



## 종료 코드

> `pgrep`·`pkill` 은 0·1·2·3 을, `killall` 은 0 과 0 이 아닌 값을 돌려줍니다.[^pgrep-exit]

`killall` 의 매뉴얼은 0 이 아닌 값을 나누지 않고, 실측은 모두 1 이었습니다.[^killall-exit] 아래 예는 「실습 준비」 에서 만든 `app` 사용자로 돌립니다.

```bash
# pgrep
# 0  하나 이상 맞았다
# 1  맞는 프로세스가 없다
# 2  명령줄 문법 오류
# 3  치명적 오류 (메모리 부족 등). 재현하지 못했다
# pkill
# 0  하나 이상 맞았고, 맞은 것에 신호도 보냈다
# 1  맞는 프로세스가 없거나, 맞은 것 모두에 신호를 보내지 못했다
# 2·3  pgrep 과 같다
# killall
# 0  이름마다 하나 이상 죽였다. 이름 없이 -u·-Z 만 줬을 때는 하나 이상 맞았다
# 0 이 아닌 값  그 밖의 경우

# pgrep: 출력은 /dev/null 로 버리고 echo $? 로 종료 코드만 읽는다
#   > /dev/null    표준 출력을 버린다
#   2>&1           오류 메시지를 표준 출력에 합친다
sleep 300 &
pgrep sleep > /dev/null; echo $?    # 0
pgrep nosuch; echo $?    # 1
pgrep > /dev/null 2>&1; echo $?    # 2
```

```bash
# pkill: root 의 sleep 에 app 권한으로 보내려다 실패해 1 이 나온다
#   setpriv --reuid         실제·유효 사용자 ID 를 바꾼다
#   setpriv --regid         실제·유효 그룹 ID 를 바꾼다
#   setpriv --clear-groups  보조 그룹을 비운다. 그룹 ID 를 바꾸면 하나를 꼭 줘야 한다
setpriv \
  --reuid=app \
  --regid=app \
  --clear-groups \
  pkill sleep > /dev/null 2>&1; echo $?
# 1

# root 가 보내면 0 이고 sleep 이 끝난다
pkill sleep; echo $?    # 0
pkill > /dev/null 2>&1; echo $?    # 2
```

```bash
# killall: sleep 을 죽이면 0 이고, 이름 없이 부르면 사용법을 찍고 1 이 나온다
sleep 300 &
killall sleep; echo $?    # 0
killall > /dev/null 2>&1; echo $?    # 1
```

이름에 맞는 프로세스가 없을 때의 `killall` 종료 상태는 「killall 결과 확인과 조용히 하기」 에 있습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 이 시트는 별도 준비 없이 참조 시트의 실습 준비를 씁니다.

먼저 [kill·pgrep·pkill·killall 참조 시트](./kill·pgrep·killall.md)의 「실습 준비」 블록을 돌립니다. PID 는 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

### pgrep 예제 프로세스 띄우기

> `pgrep` 은 프로세스 이름에 패턴이 들어 있는 PID 를 찍고, 옵션으로 이름과 명령줄을 보이거나 하나만 고릅니다.

패턴은 확장 정규식이고 기본으로 프로세스 이름만 검사하며, 조건을 여러 개 주면 모두 맞아야 합니다.[^pgrep]

```bash
# 세 프로세스를 띄워 두고 시작한다. 시작 시각 차이를 두려고 0.3초씩 쉰다
sleep 301 & sleep 0.3
sleep 302 & sleep 0.3
./mysleep 303 &
sleep 0.3
```

### pgrep 이름과 명령줄 보기

> 기본은 PID 만 찍고, 이름이나 명령줄은 옵션으로 함께 찍습니다.

```bash
# 이름에 sleep 이 든 프로세스 전부가 나온다. mysleep 도 포함이다
pgrep sleep
```

```bash
243
245
247
```

```bash
# PID 와 프로세스 이름이 나온다
#   -l   PID 와 프로세스 이름을 찍는다 (--list-name)
pgrep -l sleep
```

```bash
243 sleep
245 sleep
247 mysleep
```

```bash
# PID 와 명령줄 전체가 나온다
#   -a   PID 와 명령줄 전체를 찍는다 (--list-full)
pgrep -a sleep
```

```bash
243 sleep 301
245 sleep 302
247 ./mysleep 303
```

### pgrep 정확히 같은 이름만 고르기

> `-x` 는 이름 전체가 패턴과 같은 프로세스만 고릅니다.

`mysleep` 이 걸린 것은 패턴이 이름의 일부만 맞아도 되기 때문입니다.

```bash
# mysleep 이 빠지고 sleep 두 개만 나온다
#   -x   이름 전체가 패턴과 같은 것만 고른다 (--exact)
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

### pgrep 명령줄로 찾기

> `-f` 는 이름이 아니라 명령줄 전체에서 패턴을 찾으므로 인자로 프로세스를 구분합니다.

```bash
# sleep 302 한 개만 나온다
#   -f   이름이 아니라 명령줄 전체에서 찾는다 (--full)
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

### pgrep 하나만 고르기, 세기, 이어 붙이기

> `-n`·`-o` 는 가장 최근·가장 오래된 하나를, `-c` 는 개수를, `-d` 는 구분자로 이은 한 줄을 냅니다.

```bash
# 시작 시각 순서로 하나, 개수, 한 줄이 나온다
#   -n   가장 최근에 시작된 하나 (--newest)
#   -o   가장 오래된 하나 (--oldest)
#   -c   맞는 개수만 (--count)
#   -d   줄바꿈 대신 구분자로 한 줄에 (--delimiter)
pgrep -n sleep    # 247
pgrep -o sleep    # 243
pgrep -c sleep    # 3
pgrep -d, sleep   # 243,245,247
```

```bash
# 대소문자와 상관없이 세 개가 모두 나온다
#   -i   대소문자를 구분하지 않는다 (--ignore-case)
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

### pgrep 사용자와 부모로 좁히기

> 누가 띄웠는지(`-u`)와 누구의 자식인지(`-P`)로 대상을 줄이면 같은 이름의 다른 프로세스를 건드리지 않습니다.

`-u` 는 유효 사용자 ID 로 고릅니다. `-u root,daemon` 처럼 쉼표로 이으면 둘 중 하나(OR)이고, 다른 조건과는 모두 맞아야(AND) 합니다.[^pgrep]

```bash
# app 사용자로 sleep 을 띄운다. setpriv 옵션 뜻은 「종료 코드」 에 있다
setpriv \
  --reuid=app \
  --regid=app \
  --clear-groups \
  sleep 305 &
sleep 0.3
```

```bash
# app 의 sleep 305 한 개만 나온다
#   -u   그 사용자의 프로세스만 고른다 (--euid)
pgrep -u app -l
```

```bash
263 sleep
```

```bash
# root 가 띄운 sleep 계열(앞 예의 세 개)만 센다. app 의 sleep 은 빠진다
pgrep -u root -c sleep    # 3
```

아래는 셸 하나가 `sleep` 두 개를 자식으로 띄운 상태에서 그 셸의 자식만 찾습니다.

```bash
bash -c 'sleep 311 & sleep 312 & wait' &
sleep 0.3
# 부모 PID 가 $! 인 sleep 311·312 두 개가 나온다
#   -P   부모 PID 가 $! 인 프로세스만 고른다 (--parent)
pgrep -P $! -a
```

```bash
269 sleep 311
270 sleep 312
```

같은 패턴을 `-f` 로 찾으면 자식뿐 아니라 부모 셸도 걸립니다. 명령줄에 `sleep 311` 이 들어 있기 때문입니다.

```bash
# 부모 bash -c 와 sleep 311 두 개가 나오고 종료 상태는 0 이다
pgrep -f 'sleep 311'; echo "exit $?"
```

```bash
267
269
exit 0
```

267 이 부모 `bash -c` 이고 269 가 `sleep 311` 입니다.

### pkill 이름으로 신호 보내기

> `pkill` 은 `pgrep` 과 같은 선택 옵션을 받고 PID 를 찍는 대신 신호를 보내며, 신호를 주지 않으면 TERM 입니다.

`-신호` 로 신호를 정하고, `-e` 는 pkill 에서만 어느 프로세스에 보냈는지 찍습니다.[^pgrep]

```bash
# app 의 sleep 305 에만 TERM 이 가고, 보낸 것이 있으므로 종료 상태 0 이다
pkill -u app sleep; echo "exit $?"    # exit 0
```

```bash
# 부모 bash 와 sleep 312 에 신호를 보내고 이름과 PID 를 찍는다. -f 라 부모 bash 도 걸렸다
#   -e   신호를 보낸 프로세스의 이름과 PID 를 찍는다 (--echo)
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

스크립트 프로세스의 이름은 스크립트 파일 이름이라 `pkill trap.sh` 로 부를 수 있습니다. 명령줄은 `/bin/bash ./trap.sh` 입니다.

```bash
# trap.sh 가 USR1 과 HUP 문구를 한 줄씩 남긴다
# 첫 pkill 은 이름 trap.sh 로, 둘째 pkill 은 -f 로 명령줄에서 찾는다
#   -USR1   USR1 을 보낸다. 신호는 번호나 이름으로 준다
#   -HUP    HUP 을 보낸다
./trap.sh > t.out 2>&1 &
sleep 0.5
pkill -USR1 trap.sh
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
# 신호를 주지 않으면 TERM 이라 trap.sh 가 정리 문구를 남기고 끝난다
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

### killall 사용자와 신호 고르기

> `killall` 은 PID 가 아니라 명령 이름을 받아 이름이 맞는 프로세스 모두에 신호를 보내고, 신호를 주지 않으면 SIGTERM 입니다.

신호는 이름(`-HUP`, `-SIGHUP`)이나 번호(`-1`)나 `-s` 로 받습니다.[^killall] 이름에 `/` 가 있으면 그 파일을 실행 중인 프로세스를 고르고, `killall` 자신은 죽이지 않습니다.[^killall]

```bash
# sleep 세 개를 띄운다. 405 는 app 사용자의 프로세스다
sleep 401 & sleep 402 &
setpriv \
  --reuid=app \
  --regid=app \
  --clear-groups \
  sleep 405 &
sleep 0.3
```

```bash
# sleep 세 개가 모두 정지(T) 상태가 된다
#   -s   TERM 이 아닌 신호를 보낸다 (--signal)
#   ps -o   찍을 열을 고른다 (--format)
#   ps -C   명령 이름으로 프로세스를 고른다
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

# app 의 sleep 405 만 사라진다. 이름을 빼면 app 의 프로세스 전부가 대상이다
#   -u   그 사용자가 소유한 프로세스만 고른다 (--user)
killall -u app sleep; echo "exit $?"    # exit 0
sleep 0.3
ps -o pid,stat,user,comm -C sleep
```

```bash
    PID STAT USER     COMMAND
    301 S    root     sleep
    302 S    root     sleep
```

psmisc 매뉴얼은 `killall 이름` 이 비 Linux 시스템에서는 의도와 다르게 동작할 수 있다고 경고합니다.[^killall]

### killall 결과 확인과 조용히 하기

> `-v` 는 보낸 프로세스마다 한 줄을 찍고, `-q` 는 메시지만 빼고, `-i` 는 하나씩 묻습니다.

```bash
# 신호를 보낸 sleep 마다 한 줄이 나온다
#   -v   신호를 보낸 프로세스마다 한 줄 (--verbose)
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
# 메시지가 빠지고 종료 상태는 그대로 1
#   -q   메시지만 뺀다 (--quiet)
killall -q sleep; echo "exit $?"    # exit 1
```

```bash
# y 를 주면 보내고 종료 상태 0
#   -i   하나씩 묻고 y 만 보낸다 (--interactive). 표준 입력으로 y 를 준다
#   <<<  뒤의 문자열을 표준 입력으로 준다
sleep 501 &
sleep 0.2
killall -i sleep <<< y; echo "exit $?"    # Kill sleep(314) ? (y/N) exit 0

# n 이면 보내지 않는다. 아무것도 죽이지 않았으므로 종료 상태 1. 메시지는 버렸다
sleep 502 &
sleep 0.2
killall -i sleep 2>/dev/null <<< n; echo "exit $?"
# Kill sleep(317) ? (y/N) exit 1
```

### killall 이름을 정규식으로 고르기

> `-r` 은 이름을 POSIX 확장 정규식으로 읽습니다.

```bash
# 남아 있던 sleep 502 가 맞아 신호를 받는다
#   -r   이름을 POSIX 확장 정규식으로 읽는다 (--regexp)
killall -v -r '^sle+p$'    # Killed sleep(317) with signal 15
```

### killall 끝날 때까지 기다리기

> `-w` 는 죽인 프로세스가 모두 사라질 때까지 `killall` 이 돌아오지 않게 합니다.

`slow.sh` 는 TERM 을 받으면 1초 뒤에 `cleanup done` 을 남깁니다. 기본으로는 신호를 보내자마자 `killall` 이 돌아오므로 그 순간 `slow.out` 은 비어 있습니다.

```bash
# 기본: 신호만 보내고 바로 돌아온다
./slow.sh > slow.out 2>&1 &
sleep 0.3
killall slow.sh; echo "killall returned"

# 이 시점에는 비어 있다
cat slow.out

# 1.5초 기다리면 slow.sh 가 남긴 문구가 보인다
sleep 1.5
cat slow.out
```

```bash
killall returned
cleanup done
```

```bash
# killall 이 돌아오기 전에 cleanup done 이 slow.out 에 이미 있다
#   -w   죽인 프로세스가 모두 사라질 때까지 1초마다 확인하며 기다린다 (--wait)
./slow.sh > slow.out 2>&1 &
sleep 0.3
killall -w slow.sh; echo "killall returned"
cat slow.out
```

```bash
killall returned
cleanup done
```

신호를 무시하거나 좀비가 된 프로세스가 있으면 `-w` 는 끝나지 않을 수 있습니다.[^killall]



## 주의사항과 동작 원리

> `-f` 는 부모 셸까지 맞히고, 15글자를 넘는 이름은 `killall -e` 로 가립니다.

### pgrep -f 가 부모 셸까지 잡는 경우

> `pgrep -f` 는 자기 자신만 빼고 모든 명령줄을 훑으므로, 패턴 문자열을 명령줄에 가진 부모 셸이 걸립니다.

`pgrep`·`pkill` 은 자기 자신을 맞는 목록에서 빼지만 그 부모는 기본으로 빼지 않습니다.[^pgrep] 셸에서 `bash -c '... pgrep -af "패턴" ...'` 로 부르면 이 `bash -c` 의 명령줄 안에 패턴이 들어 있어 부모가 함께 잡힙니다.

```bash
# 앞의 예에서 sleep 을 정리했으므로 sleep 302 를 다시 띄운다
sleep 302 &
sleep 0.3
```

```bash
# 부모 셸(bash -c)의 명령줄에도 패턴이 있어 같이 잡힌다
#   ; true   bash -c 에 명령이 하나뿐이면 셸이 그 명령으로 바뀌어 부모 셸이 남지 않는다
#            그래서 뒤에 붙여 셸을 남겨 둔다
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

`-A` 는 `pgrep` 자신의 조상 프로세스를 모두 맞는 목록에서 뺍니다.[^pgrep]

```bash
# 조상 프로세스(부모 bash -c)를 제외해 sleep 302 만 남는다
#   -A   조상 프로세스를 제외한다 (--ignore-ancestors)
bash -c 'pgrep -A -af "sleep 302"; true'    # 245 sleep 302
```

`pkill -f` 에서는 같은 문제가 자기 셸을 죽이는 사고가 되므로 「pkill -f 가 자기 셸을 죽이는 경우」 에서 확인합니다. `pgrep -a` 로 대상을 먼저 찍어 본 뒤에 같은 조건으로 `pkill` 을 부르는 순서가 안전합니다.

### pkill -f 가 자기 셸을 죽이는 경우

> `pkill -f` 는 패턴이 든 부모 셸에도 TERM 을 보내 자기를 부른 셸이 죽고, `-A` 로 조상을 빼면 막습니다.

```bash
# pkill -f 가 자기를 부른 셸까지 죽인다. survived 는 찍히지 않고 종료 상태는 128 + 15
bash -c 'pkill -f "sleep 302"; echo survived'; echo "exit $?"    # exit 143
```

`pkill` 은 자기 자신은 빼지만 부모 `bash -c` 는 명령줄에 패턴이 있어 맞았고, 그 셸이 TERM 으로 죽어서 `echo survived` 에 닿지 못했습니다. `-A` 를 주면 부모를 빼서 `survived` 가 찍힙니다.

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

### killall 긴 이름과 -e

> 프로세스 이름이 15글자까지만 확인되는 경우에 `-e` 는 전체 이름이 같은 것만 고릅니다.

프로세스 이름은 15글자까지만 확인되는 경우가 있고, `-e` 는 그때 앞 15글자만 같은 프로세스를 건너뛰게 합니다.[^killall]

```bash
./a_very_long_process_name 400 &
sleep 0.3
# 커널이 아는 이름은 15글자로 잘려 있다
#   ps -o comm=   머리글 없이 이름만 찍는다
ps -o comm= -C a_very_long_pro    # a_very_long_pro
```

```bash
# 긴 이름은 전체가 같은 것만 고른다. 전체 이름을 못 읽은 프로세스는 건너뛴다
#   -e   긴 이름은 전체가 같은 것만 고른다 (--exact)
killall -e -v a_very_long_process_name; echo "exit $?"
```

```bash
Killed a_very_long_process_name(321) with signal 15
exit 0
```

이 컨테이너는 전체 이름을 읽을 수 있어서 `-e` 의 유무로 결과가 갈리는 상황을 만들지 못했고, 위 출력은 `-e` 를 줘도 전체 이름이 같은 프로세스에는 신호가 간다는 것까지만 보여 줍니다. 전체 이름을 읽지 못하는 경우의 동작은 매뉴얼 문장으로만 적습니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [kill·pgrep·pkill·killall 참조 시트](./kill·pgrep·killall.md) — 이 시트가 이어받는 실습 준비와 신호 이름·`kill` 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `pgrep --help`·`pkill --help`·`man pgrep` 과 psmisc 23.6 의 `killall --help`·`man killall` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [pgrep(1)·pkill(1) — procps-ng 4.0.2](https://manpages.debian.org/bookworm/procps/pgrep.1.en.html)
- [killall(1) — psmisc 23.6](https://manpages.debian.org/bookworm/psmisc/killall.1.en.html)

[^pgrep]: pgrep(1) (procps-ng 4.0.2, Debian 12) — "pattern Specifies an Extended Regular Expression for matching against the process names or command lines.", "All the criteria have to match.", "-signal --signal signal Defines the signal to send to each matched process.", "-u, --euid euid,... Only match processes whose effective user ID is listed.", "$ ps -fp $(pgrep -d, -x xterm)", "$ pgrep -u root,daemon will list the processes owned by root OR daemon.", "-e, --echo Display name and PID of the process being killed. (pkill only.)", "The process name used for matching is limited to the 15 characters present in the output of /proc/pid/stat. Use the -f option to match against the complete command line", "The running pgrep, pkill, or pidwait process will never report itself as a match.", "-A, --ignore-ancestors Ignore all ancestors of pgrep, pkill, or pidwait.", "-P, --parent ppid,... Only match processes whose parent process ID is listed.", 종료 상태 "0 One or more processes matched the criteria", "1 No processes matched or none of them could be signalled.", "2 Syntax error in the command line." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^killall]: killall(1) (psmisc 23.6, Debian 12) — "killall sends a signal to all processes running any of the specified commands. If no signal name is specified, SIGTERM is sent.", "Signals can be specified either by name (e.g. -HUP or -SIGHUP) or by number (e.g. -1) or by option -s.", "contains a slash (/), processes executing that particular file will be selected for killing, independent of their name.", "killall returns a zero return code if at least one process has been killed for each listed command", "killall returns non-zero otherwise.", "A killall process never kills itself", "-u, --user Kill only processes the specified user owns. Command names are optional.", "-r, --regexp Interpret process name pattern as a POSIX extended regular expression", "-i, --interactive Interactively ask for confirmation before killing", "-q, --quiet Do not complain if no processes were killed.", "-v, --verbose Report if the signal was successfully sent.", "-e, --exact Require an exact match for very long names. If a command name is longer than 15 characters, the full name may be unavailable (i.e. it is swapped out)... With -e, such entries are skipped.", "-w, --wait Wait for all killed processes to die. killall checks once per second if any of the killed processes still exist", "Note that killall may wait forever if the signal was ignored, had no effect, or if the process stays in zombie state.", "Be warned that typing killall name may not have the desired effect on non-Linux systems, especially when done by a privileged user." https://manpages.debian.org/bookworm/psmisc/killall.1.en.html
[^pgrep-exit]: pgrep(1) (procps-ng 4.0.2, Debian 12) 의 EXIT STATUS — "0 One or more processes matched the criteria. For pkill and pidwait, one or more processes must also have been successfully signalled or waited for.", "1 No processes matched or none of them could be signalled.", "2 Syntax error in the command line.", "3 Fatal error: out of memory etc." https://manpages.debian.org/bookworm/procps/pgrep.1.en.html
[^killall-exit]: killall(1) (psmisc 23.6, Debian 12) — "killall returns a zero return code if at least one process has been killed for each listed command, or no commands were listed and at least one process matched the -u and -Z search criteria. killall returns non-zero otherwise." 1 은 이 시트의 실측입니다(Debian 12, psmisc 23.6). https://manpages.debian.org/bookworm/psmisc/killall.1.en.html
