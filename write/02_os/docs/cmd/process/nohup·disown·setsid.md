---
title: nohup·disown·setsid 셸을 닫은 뒤에도 돌리기
tags: [linux, cheatsheet, jobs, nohup, disown, setsid, job-control, cli, reference]
status: draft
source:
  - GNU Bash Reference Manual 5.2 「Job Control Basics」·「Job Control Builtins」·「Signals」
  - GNU bash 5.2.15 `help disown` 원문 (Debian 12)
  - nohup(1) (GNU coreutils 9.1, Debian bookworm)
  - setsid(1) (util-linux 2.38.1, Debian bookworm)
  - proc_pid_status(5) (man7.org), ioctl_tty(2) (Linux man-pages 6.03, Debian bookworm)
related:
  - ./jobs·bg·fg·wait.md
  - ../README.md
updated: 2026-11-13
---

# nohup·disown·setsid 셸을 닫은 뒤에도 돌리기

---

> 터미널이 끊겨도 잡을 살려 두는 `nohup`·`disown`·`setsid` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `nohup`·`disown`·`setsid` 는 터미널이 끊겨 셸이 `SIGHUP` 을 받아도 잡이 죽지 않게 하는 세 방법입니다.

이 시트는 [jobs·bg·fg·wait 참조 시트](./jobs·bg·fg·wait.md)에서 셸을 닫은 뒤에도 돌리는 유스케이스를 떼어 낸 것이며, 예는 그 시트의 「실습 준비」 블록을 돌린 상태에서 이어집니다. 출력은 같은 Debian 12 컨테이너(GNU bash 5.2.15)에서 받았고 `script -qec` 는 util-linux 판 옵션이라 macOS 에서는 맞지 않으니 Linux 에서 실행합니다.

`nohup` 은 coreutils 9.1, `setsid` 는 util-linux 2.38.1 의 외부 바이너리(`dpkg -S` 로 확인)이고 `disown` 은 bash 내장입니다.



## 핵심 문법

> `nohup`·`setsid` 는 명령 앞에 붙여 시작하고, `disown` 은 이미 뜬 잡에 씁니다.

```bash
# 호출 형태. disown 은 bash 내장이라 help disown 의 첫 줄이고
# nohup·setsid 는 외부 바이너리라 --help 의 Usage 줄이다
disown [-h] [-ar] [jobspec ... | pid ...]
nohup COMMAND [ARG]...
  or:  nohup OPTION
setsid [options] <program> [arguments ...]

# SIGHUP 을 무시한 채 시작한다 (nohup 으로 SIGHUP 무시하고 시작하기)
nohup 명령 &
nohup 명령 > 파일 2>&1 < /dev/null &

# 이미 뜬 잡을 SIGHUP 전달 대상에서 뺀다 (disown 으로 이미 뜬 잡 떼어 놓기)
disown %1
disown -h %1
disown -r
disown -a

# 새 세션에서 시작한다 (setsid 로 새 세션에서 시작하기)
setsid 명령 &
setsid -w 명령
setsid -f 명령
setsid -c 명령 &
```



## 종료 코드

> `nohup` 은 125·126·127 로 실패를 나누고, 성공하면 명령의 종료 코드를 그대로 돌려줍니다.[^nohup-exit]

`disown` 은 성공하면 0 이고 `setsid` 는 매뉴얼에 종료 코드 절이 없어 실측만 싣습니다.[^disown-exit][^setsid-exit] 아래 예는 「실습 준비」 의 `set -m` 을 켠 셸에서 돌립니다.

```bash
# nohup   125    nohup 자체가 실패했다 (POSIXLY_CORRECT 가 없을 때)
#                POSIXLY_CORRECT 가 있으면 125 대신 127 이 된다
#         126    COMMAND 를 찾았지만 실행할 수 없다
#         127    COMMAND 를 찾을 수 없다
#         그 외  COMMAND 의 종료 코드
# disown  0      성공
#         1      없는 잡 지정
#         2      모르는 옵션
# setsid  매뉴얼에 종료 코드 절이 없다. 아래 실측만 적는다

# 명령 없이 부르면 nohup 자체의 실패라 125 다
nohup 2>&1; echo $?    # nohup: missing operand / Try 'nohup --help' for more information. / 125

# 없는 명령은 127, 실행할 수 없는 파일(/etc/passwd)은 126 이다
# 입력·출력·오류는 /dev/null 로 돌려 안내문을 막는다
nohup /no/such/cmd < /dev/null > /dev/null 2>&1; echo $?    # 127
nohup /etc/passwd < /dev/null > /dev/null 2>&1; echo $?    # 126

# 명령이 성공하면 0 이고 실패하면 그 코드가 그대로 나온다
nohup true < /dev/null > /dev/null 2>&1; echo $?    # 0
nohup sh -c 'exit 7' < /dev/null > /dev/null 2>&1; echo $?    # 7
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.

```bash
# 없는 잡 지정은 1 이고 모르는 옵션은 2 다. 오류 메시지는 버린다
disown %9 2>/dev/null; echo $?    # 1
disown -z 2>/dev/null; echo $?    # 2

# setsid: 명령 없이 부르면 1 이다
setsid 2>&1; echo $?    # setsid: no command specified / Try 'setsid --help' for more information. / 1

# setsid: fork 한 부모는 곧바로 끝나므로 0 이다
setsid true; echo $?    # 0

# setsid: 명령이 끝나기를 기다려 그 종료 코드를 돌려준다
#   -w   명령이 끝나기를 기다리고 그 종료 코드를 돌려준다
setsid -w sh -c 'exit 7'; echo "exit=$?"    # exit=7

# setsid: 기다리는데 명령을 못 찾으면 127 이다
setsid -w /no/such/cmd 2>&1; echo $?    # setsid: failed to execute /no/such/cmd: No such file or directory / 127
```

위 블록의 `/` 도 여러 줄 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 이 시트의 예는 jobs 시트의 준비 블록이 만든 `slow.sh`·`pty.sh` 와 `set -m` 을 씁니다.

먼저 [jobs·bg·fg·wait 참조 시트](./jobs·bg·fg·wait.md)의 「실습 준비」 블록을 돌립니다.

### nohup 으로 SIGHUP 무시하고 시작하기

> `nohup 명령 &` 는 `SIGHUP` 을 무시한 채 명령을 시작해, 터미널이 끊겨도 그 명령이 죽지 않게 합니다.

`nohup` 은 표준 출력이 터미널이면 `nohup.out` 에 덧붙이고 표준 입력이 터미널이면 못 읽는 파일에 이어 둡니다.[^nohup]

```bash
# 터미널 출력은 pty.sh 로 받는다
# [1]+  Done 알림 줄이 앞서 친 줄 사이에 끼어 보인다
./pty.sh 'nohup ./slow.sh 1 job &' 'sleep 2' 'cat nohup.out'
```

```bash
bash-5.2# nohup ./slow.sh 1 job &
[1] 259
bash-5.2# nohup: ignoring input and appending output to 'nohup.out'
sleep 2
cat nohup.out
[1]+  Done                    nohup ./slow.sh 1 job
bash-5.2# cat nohup.out
start job
end job
bash-5.2# exit
```

출력을 파일로 돌리면 `nohup.out` 을 만들지 않고, 입력이 터미널인 점만 `nohup: ignoring input` 으로 알려 줍니다.[^nohup]

```bash
# 먼저 앞 예의 nohup.out 을 지운다
rm -f nohup.out
./pty.sh \
  'nohup ./slow.sh 1 job > job.log 2>&1 &' \
  'sleep 2' \
  'cat job.log' \
  'ls nohup.out'
```

```bash
bash-5.2# nohup ./slow.sh 1 job > job.log 2>&1 &
[1] 274
bash-5.2# sleep 2
cat job.log
ls nohup.out
[1]+  Done                    nohup ./slow.sh 1 job > job.log 2>&1
bash-5.2# cat job.log
nohup: ignoring input
start job
end job
bash-5.2# ls nohup.out
ls: cannot access 'nohup.out': No such file or directory
bash-5.2# exit
```

```bash
# 실무에서는 입력까지 /dev/null 로 돌려 세 스트림을 모두 정해 둔다
# /proc/PID/fd/0·1·2 가 가리키는 곳으로 확인한다
nohup ./slow.sh 3 job > job.log 2>&1 < /dev/null &
readlink /proc/$!/fd/0 /proc/$!/fd/1 /proc/$!/fd/2
wait
```

```bash
/dev/null
/root/cmd-lab/jobs/job.log
/root/cmd-lab/jobs/job.log
```

### disown 으로 이미 뜬 잡 떼어 놓기

> `disown` 은 이미 돌고 있는 잡을 셸의 `SIGHUP` 전달 대상에서 뺍니다.

대화형 셸은 `SIGHUP` 을 받으면 종료하기 전에 잡 표의 모든 잡에 `SIGHUP` 을 다시 보냅니다. `disown` 은 잡을 표에서 빼거나(`disown`) 표에 남기되 보내지 않게 표시합니다(`disown -h`).[^bashsig]

```bash
# 네 잡을 띄워 일반·nohup·disown -h·disown 을 맞댄다
# kill -HUP $$ 는 대화형 셸에 SIGHUP 을 보내 터미널 끊김을 흉내 낸다
# $$ 는 그 셸의 PID 이고 0.5초 뒤 ps 로 살아남은 sleep 을 본다
#   -h         표에 남기되 SIGHUP 을 보내지 않게 표시한다
#   jobs -l    잡마다 PID 를 함께 보인다
#   ps -o      찍을 열을 고른다
#   ps -C      그 이름의 프로세스만 고른다
#   pkill -x   이름이 정확히 sleep 인 프로세스에 SIGTERM 을 보내 정리한다
./pty.sh \
  'sleep 301 &' \
  'nohup sleep 302 > /dev/null 2>&1 &' \
  'sleep 303 &' \
  'disown -h %3' \
  'sleep 304 &' \
  'disown %4' \
  'jobs -l' \
  'kill -HUP $$'
sleep 0.5
ps -o pid,ppid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# sleep 301 &
[1] 293
bash-5.2# nohup sleep 302 > /dev/null 2>&1 &
[2] 295
bash-5.2# sleep 303 &
[3] 297
bash-5.2# disown -h %3
bash-5.2# sleep 304 &
[4] 300
bash-5.2# disown %4
bash-5.2# jobs -l
[1]    293 Running                 sleep 301 &
[2]-   295 Running                 nohup sleep 302 > /dev/null 2>&1 &
[3]+   297 Running                 sleep 303 &
bash-5.2# kill -HUP $$
Hangup
    PID    PPID STAT COMMAND
    295       1 S    sleep 302
    297       1 S    sleep 303
    300       1 S    sleep 304
```

대비 없이 띄운 `sleep 301` 만 사라졌고 나머지 셋은 부모가 PID 1 로 바뀐 채 살았습니다. `disown %4` 한 잡은 `jobs -l` 에서도 빠져 있고 `disown -h %3` 한 잡은 표에 남았습니다.

옵션은 대상을 고르고, `-h` 와 합치면(`-ah`) 표에서 빼지 않고 표시만 합니다.[^bashjob]

```bash
# 잡 지정 없이 실행 중인 잡만 표에서 뺀다
# 멈춘 잡(312)은 표에 남아 SIGHUP 을 받는다
#   -r   실행 중인 잡만 다룬다
./pty.sh \
  'sleep 311 &' \
  'sleep 312 &' \
  'kill -TSTP %2' \
  'disown -r' \
  'jobs' \
  'kill -HUP $$'
sleep 0.5
ps -o pid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# sleep 311 &
[1] 315
bash-5.2# sleep 312 &
[2] 317
bash-5.2# kill -TSTP %2
bash-5.2# disown -r

[2]   Stopped                 sleep 312
bash-5.2# jobs
[2]   Stopped                 sleep 312
bash-5.2# kill -HUP $$
Hangup
    PID STAT COMMAND
    315 S    sleep 311
```

```bash
# 모든 잡을 표에서 뺀다. jobs 가 비어 있고 둘 다 산다
#   -a   잡 지정이 없을 때 모든 잡을 다룬다
./pty.sh 'sleep 321 &' 'sleep 322 &' 'disown -a' 'jobs' 'kill -HUP $$'
sleep 0.5
ps -o pid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# sleep 321 &
[1] 333
bash-5.2# sleep 322 &
[2] 335
bash-5.2# disown -a
bash-5.2# jobs
bash-5.2# kill -HUP $$
Hangup
    PID STAT COMMAND
    333 S    sleep 321
    335 S    sleep 322
```

```bash
# -a 와 -h 를 합치면 모든 잡을 표에 남기고 SIGHUP 만 보내지 않게 표시한다
# jobs 에 둘 다 보이고 둘 다 산다
./pty.sh 'sleep 321 &' 'sleep 322 &' 'disown -ah' 'jobs' 'kill -HUP $$'
sleep 0.5
ps -o pid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# sleep 321 &
[1] 350
bash-5.2# sleep 322 &
[2] 352
bash-5.2# disown -ah
bash-5.2# jobs
[1]-  Running                 sleep 321 &
[2]+  Running                 sleep 322 &
bash-5.2# kill -HUP $$
Hangup
    PID STAT COMMAND
    350 S    sleep 321
    352 S    sleep 322
```

`disown` 의 인자는 잡 지정 대신 PID 도 받습니다. 그때는 그 PID 가 든 잡을 가리킵니다.[^bashjob]

### setsid 로 새 세션에서 시작하기

> `setsid` 는 명령을 새 세션에서 실행해 원래 터미널과의 연결을 끊습니다.

`setsid` 는 자신이 프로세스 그룹 리더이면 `fork` 한 뒤 자식에서 실행하고 아니면 그 프로세스에서 곧바로 실행합니다.[^setsid] 잡 제어가 켜진 셸에서는 앞 명령이 리더라 `fork` 하고 `setsid` 자신은 바로 끝나는데, `-w` 는 「종료 코드」 에서 푼 대로 그 끝을 기다립니다.

```bash
# 옵션 없이: setsid 는 곧바로 끝나고 sleep 은 계속 돈다
#   pgrep -x   이름이 정확히 같은 프로세스만 고른다. wc -l 이 그 수를 센다
setsid sleep 2; pgrep -x sleep | wc -l    # 1

# -w 를 주면 sleep 이 끝난 뒤에 setsid 가 끝나 sleep 이 남지 않는다
setsid -w sleep 2; pgrep -x sleep | wc -l    # 0
```

잡 제어가 없는 `bash -c` 안에서 비교합니다. 옵션 없이는 `$!` 가 곧 `sleep` 의 PID 이고, `-f` 를 주면 `$!`(`setsid` 의 PID)와 `sleep` 의 PID 가 다릅니다.[^setsid]

```bash
pkill -x sleep
# 옵션 없이: setsid 가 그 프로세스에서 곧바로 실행해 PID 가 같다
bash -c 'setsid sleep 100 & echo "setsid pid=$!"; sleep 0.2; pgrep -x sleep'
pkill -x sleep
# -f: 리더가 아닐 때도 fork 하므로 setsid 의 PID 와 sleep 의 PID 가 다르다
#   -f   항상 새 프로세스를 만든다
bash -c 'setsid -f sleep 101 & echo "setsid pid=$!"; sleep 0.2; pgrep -x sleep'
pkill -x sleep
```

```bash
setsid pid=371
371
setsid pid=375
377
```

`sleep 102` 는 터미널(`pts/0`)이 남았고 `sleep 103` 은 `setsid` 로 터미널이 `?` 가 되었습니다. `-c` 는 그 터미널이 이미 다른 세션의 제어 터미널이면 커널이 `EPERM` 으로 거절하고, `CAP_SYS_ADMIN` 권한이 있으면 터미널을 빼앗아 성공합니다.[^ioctl]

```bash
# -c 를 준 sleep 104 는 CAP_SYS_ADMIN 이 없는 기본 Docker 컨테이너라 실패했다
# 컨테이너 밖의 root 셸에서는 터미널을 빼앗아 성공하므로 결과가 다르다
#   -c      제어 터미널을 현재 터미널로 정한다
#   grep -E   확장 정규식으로 머리줄과 sleep 10x 줄만 남긴다
./pty.sh \
  'sleep 102 &' \
  'setsid sleep 103 &' \
  'setsid -c sleep 104 &' \
  'ps -o pid,pgid,sid,tty,args -C sleep | grep -E "PID|sleep 10"'
pkill -x sleep
```

```bash
bash-5.2# sleep 102 &
[1] 387
bash-5.2# setsid sleep 103 &
[2] 389
bash-5.2# setsid -c sleep 104 &
[3] 392
[2]   Done                    setsid sleep 103
bash-5.2# setsid: failed to set the controlling terminal: Operation not permitted
ps -o pid,pgid,sid,tty,args -C sleep | grep -E "PID|sleep 10"
    PID    PGID     SID TT       COMMAND
    387     387     384 pts/0    sleep 102
    390     390     390 ?        sleep 103
[3]+  Done                    setsid -c sleep 104
bash-5.2# exit
```



## 주의사항과 동작 원리

> 셋이 끊는 고리는 서로 다르고, 셸을 닫는 것만으로는 잡에 `SIGHUP` 이 가지 않습니다.

### nohup·disown·setsid 맞대기

> 같은 `sleep` 을 세 방식으로 띄워 프로세스 그룹·세션·무시하는 신호를 비교하면 셋이 끊는 고리가 다름이 보입니다.

`sleep 401` 은 `nohup`, `402` 는 `disown`, `403` 은 `setsid`, `404` 는 대조군입니다. 무시하는 신호는 `/proc/PID/status` 의 `SigIgn` 비트마스크로 봅니다.[^proc]

```bash
# ps 가 이 셸과 sleep 넷의 PGID·SID·STAT 를 함께 보여 준다
#   ps -p   그 PID($$, 이 셸)도 함께 보여 준다
nohup sleep 401 > /dev/null 2>&1 &
sleep 402 & disown
setsid sleep 403 &
sleep 404 &
sleep 0.3
ps \
  -o pid,pgid,sid,stat,args \
  -p $$ \
  -C sleep
```

```bash
    PID    PGID     SID STAT COMMAND
      6       1       1 S    bash -s
    237     237       1 S    sleep 401
    238     238       1 S    sleep 402
    240     240       1 S    sleep 404
    242     242     242 Ss   sleep 403
```

```bash
for p in $(pgrep -x sleep); do echo "$p $(grep SigIgn /proc/$p/status)"; done
```

```bash
237 SigIgn:	0000000200000001
238 SigIgn:	0000000200000000
240 SigIgn:	0000000200000000
242 SigIgn:	0000000200000000
```

- `SID`: 셸(`bash -s`)의 `SID` 는 1 이고 `401`·`402`·`404` 도 1 입니다. `setsid` 로 띄운 `403` 만 자기 PID 242 가 `SID` 이고 `STAT` 에 세션 리더를 뜻하는 `s` 가 붙습니다.
- `SigIgn`: 마지막 비트가 `SIGHUP`(1번 신호)입니다. `nohup` 으로 띄운 `401` 만 `...01` 이고 나머지는 `...00` 입니다. 위쪽 `2` 는 네 줄이 같으므로 비교에서 뺍니다.
- `PGID`: 잡 제어가 켜져 있어 `&` 로 띄운 잡은 모두 자기 프로세스 그룹입니다. 그룹은 세 방식을 가르는 기준이 아닙니다.

`nohup` 잡은 신호를 무시해서, `disown` 잡은 셸이 신호를 보내지 않아서 삽니다. `setsid` 잡은 세션이 달라 끊김이 닿지 않습니다.

`nohup` 잡과 대조군은 아래 정리 때 종료 알림이 나옵니다.

```bash
pkill -x sleep
sleep 0.3
wait
```

```bash
[1]   Terminated              nohup sleep 401 > /dev/null 2>&1
[3]+  Terminated              sleep 404
```

### 셸을 닫을 때 잡에 신호 보내기

> `shopt -s huponexit` 를 켜면 셸이 종료할 때도 모든 잡에 `SIGHUP` 을 보냅니다.

기본값(꺼짐)에서는 `exit` 로 셸을 닫아도 백그라운드 잡에 `SIGHUP` 을 보내지 않습니다. 매뉴얼은 `huponexit` 이 대화형 로그인 셸의 종료에 적용된다고 적습니다.[^bashsig]

```bash
# 기본값으로 셸을 닫는다. 마지막 ps 가 비어 있어야 잡이 죽었다는 뜻이다
./pty.sh 'sleep 331 &' 'exit'
ps -o pid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# sleep 331 &
[1] 406
bash-5.2# exit
exit
    PID STAT COMMAND
    406 S    sleep 331
```

```bash
# 로그인 셸이 아닌 셸에서 huponexit 를 켠 경우도 잡은 산다
./pty.sh 'shopt -s huponexit' 'sleep 332 &' 'exit'
ps -o pid,stat,args -C sleep
pkill -x sleep
```

```bash
bash-5.2# shopt -s huponexit
bash-5.2# sleep 332 &
[1] 419
bash-5.2# exit
exit
    PID STAT COMMAND
    419 S    sleep 332
```

```bash
# 로그인 셸(-il)에서 huponexit 를 켜면 잡이 죽어 ps 가 비어 있다
# BOPT=-il: pty.sh 가 띄우는 bash 를 로그인 셸로 바꾼다. 프롬프트를 L$ 로 맞춘다
BOPT=-il ./pty.sh "PS1='L\$ '" 'shopt -s huponexit' 'sleep 333 &' 'exit'
ps -o pid,stat,args -C sleep
```

```bash
root@fbd03da2882c:~/cmd-lab/jobs# PS1='L$ '
L$ shopt -s huponexit
L$ sleep 333 &
[1] 435
L$ exit
logout
    PID STAT COMMAND
```

로그인 셸에서만 `sleep 333` 이 죽었습니다. 첫 줄의 `root@...` 는 컨테이너마다 달라지는 로그인 셸의 기본 프롬프트입니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [jobs·bg·fg·wait 참조 시트](./jobs·bg·fg·wait.md) — 이 시트가 이어받는 실습 준비와 잡 제어 예
- [세션과 제어 터미널](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#세션과-제어-터미널) — `PGID`·`SID`·제어 터미널이 무엇인지
- [터미널이 끊길 때 살아남는 잡](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#터미널이-끊길-때-살아남는-잡) — 끊김이 `SIGHUP` 으로 잡에 닿는 사슬
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU bash 5.2.15 의 `help disown` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- `nohup --help`·`setsid --help` 원문 (coreutils 9.1, util-linux 2.38.1) — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU Bash Reference Manual — Job Control](https://www.gnu.org/software/bash/manual/html_node/Job-Control.html) — 「Job Control Basics」·「Job Control Builtins」. 지금 gnu.org 는 5.3 판이라 각주의 5.2 인용과 문구가 조금 다릅니다
- [nohup(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/nohup.1.en.html), [setsid(1) — Debian bookworm](https://manpages.debian.org/bookworm/util-linux/setsid.1.en.html)

[^bashjob]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Job Control Basics — "When Bash starts a job asynchronously, it prints a line that looks like", "The character '%' introduces a job specification", "A job may also be referred to using a prefix of the name used to start it, or using a substring that appears in its command line", "If the prefix or substring matches more than one job, Bash reports an error", "Typing the ... character (typically '^Z', Control-Z) while a process is running causes that process to be stopped and returns control to Bash", "'%1' is a synonym for 'fg %1'", "'%1 &' resumes job 1 in the background, equivalent to 'bg %1'", "When the shell is waiting for a job or process using the 'wait' builtin, and job control is enabled, 'wait' will return when the job changes state". Job Control Builtins — `wait` "If the '-n' option is supplied, 'wait' waits for a single job from the list of PIDs or JOBSPECs or, if no arguments are supplied, any job, to complete and returns its exit status", "If the '-p' option is supplied, the process or job identifier of the job for which the exit status is returned is assigned to the variable VARNAME ... This is useful only when the '-n' option is supplied", "Supplying the '-f' option, when job control is enabled, forces 'wait' to wait for each PID or JOBSPEC to terminate before returning its status, instead of returning when it changes status", `disown` "disown [-ar] [-h] [JOBSPEC ... | PID ... ]", "If no JOBSPEC is supplied, the '-a' option means to remove or mark all jobs; the '-r' option without a JOBSPEC argument restricts operation to running jobs". https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html, https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
[^bashsig]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Signals — "Before exiting, an interactive shell resends the 'SIGHUP' to all jobs, running or stopped", "To prevent the shell from sending the 'SIGHUP' signal to a particular job, it should be removed from the jobs table with the 'disown' builtin ... or marked to not receive 'SIGHUP' using 'disown -h'", "If the 'huponexit' shell option has been set with 'shopt' ... Bash sends a 'SIGHUP' to all jobs when an interactive login shell exits". https://www.gnu.org/software/bash/manual/html_node/Signals.html
[^nohup]: nohup(1) (GNU coreutils 9.1, Debian bookworm) — "Run COMMAND, ignoring hangup signals", "If standard input is a terminal, redirect it from an unreadable file. If standard output is a terminal, append output to 'nohup.out' if possible, '$HOME/nohup.out' otherwise. If standard error is a terminal, redirect it to standard output. To save output to FILE, use 'nohup COMMAND > FILE'". https://manpages.debian.org/bookworm/coreutils/nohup.1.en.html
[^setsid]: setsid(1) (util-linux, Debian bookworm) — "setsid runs a program in a new session. The command calls fork(2) if already a process group leader. Otherwise, it executes a program in the current process", "-c, --ctty Set the controlling terminal to the current one", "-f, --fork Always create a new process", "-w, --wait Wait for the execution of the program to end, and return the exit status of this program as the exit status of setsid". https://manpages.debian.org/bookworm/util-linux/setsid.1.en.html
[^ioctl]: ioctl_tty(2) (Linux man-pages 6.03, Debian bookworm), TIOCSCTTY — "If this terminal is already the controlling terminal of a different session group, then the ioctl fails with EPERM, unless the caller has the CAP_SYS_ADMIN capability and arg equals 1, in which case the terminal is stolen". https://manpages.debian.org/bookworm/manpages-dev/ioctl_tty.2.en.html
[^proc]: proc_pid_status(5), `SigBlk`·`SigIgn`·`SigCgt` — "Masks (expressed in hexadecimal) indicating signals being blocked, ignored, and caught". https://man7.org/linux/man-pages/man5/proc_pid_status.5.html
[^nohup-exit]: GNU coreutils 9.1 매뉴얼(Debian 12 의 `coreutils.info`), "nohup invocation" — "125 if 'nohup' itself fails, and 'POSIXLY_CORRECT' is not set", "126 if COMMAND is found but cannot be invoked", "127 if COMMAND cannot be found", "the exit status of COMMAND otherwise", "If 'POSIXLY_CORRECT' is set, internal failures give status 127 instead of 125". <https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html>
[^disown-exit]: GNU bash 5.2.15 `help disown` 의 Exit Status (Debian 12) — "Returns success unless an invalid option or JOBSPEC is given." 모르는 옵션의 2 는 `bash.info` Exit Status 의 "All builtins return an exit status of 2 to indicate incorrect usage, generally invalid options or missing arguments" 이고, 없는 잡 지정의 1 은 이 시트의 실측입니다(Debian 12 컨테이너, GNU bash 5.2.15). <https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html>
[^setsid-exit]: setsid(1) (util-linux 2.38.1, Debian 12 의 `/usr/share/man/man1/setsid.1.gz`) 는 NAME·SYNOPSIS·DESCRIPTION·OPTIONS·AUTHORS·SEE ALSO·REPORTING BUGS·AVAILABILITY 절뿐이고 EXIT STATUS 절이 없으며, `-w` 만 "return the exit status of this program as the exit status of setsid" 라고 적습니다. 0·1·127 은 이 시트의 실측입니다(Debian 12 컨테이너, util-linux 2.38.1). <https://manpages.debian.org/bookworm/util-linux/setsid.1.en.html>
