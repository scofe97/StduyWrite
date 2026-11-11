---
title: jobs·nohup·disown 참조 시트
tags: [linux, cheatsheet, jobs, nohup, disown, setsid, job-control, cli, reference]
status: draft
source:
  - GNU Bash Reference Manual 5.2 「Job Control Basics」·「Job Control Builtins」·「Signals」
  - GNU bash 5.2.15 `help jobs`·`help wait`·`help disown` 원문 (Debian 12)
  - nohup(1) (GNU coreutils 9.1, Debian bookworm)
  - setsid(1) (util-linux 2.38.1, Debian bookworm)
  - proc_pid_status(5) (man7.org), ioctl_tty(2) (Linux man-pages 6.03, Debian bookworm)
related:
  - ../README.md
updated: 2026-11-11
---

# jobs·nohup·disown 참조 시트

---

> 터미널 하나에서 명령 여럿을 돌리고(`&`·`jobs`·`fg`·`bg`·`wait`), 터미널이 끊겨도 살려 두는(`nohup`·`disown`·`setsid`) 방법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 스크립트가 모두 생깁니다.

출력은 Debian 12 컨테이너(GNU bash 5.2.15, coreutils 9.1, util-linux 2.38.1)에서 받았습니다. 잡 제어는 대화형 셸에서만 기본으로 켜지므로 대부분의 명령은 `set -m` 을 켠 스크립트로 돌려 받았습니다.

`Ctrl+Z` 처럼 키 입력이 필요한 예와 `[1]+  Done` 같은 알림이 나오는 예는 `pty.sh` 로 받았습니다. `pty.sh` 는 가상 터미널 안의 대화형 `bash` 에 명령을 한 줄씩 쳐 넣습니다.

스크립트를 `bash -s` 의 표준 입력으로 넘겨 받은 오류 줄 앞에는 `bash: line 25:` 가 붙고 대화형 셸에서는 `bash:` 만 붙습니다. PID 와 `PGID`·`SID` 값은 실행마다 달라집니다. `script` 의 `-qec` 는 util-linux 판 옵션이라 macOS 에서는 맞지 않으니 Linux 에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/jobs && cd ~/cmd-lab/jobs
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq procps >/dev/null 2>&1
cat > slow.sh << 'EOS'
#!/bin/bash
echo "start $2"; sleep "$1"; echo "end $2"
EOS
cat > pty.sh << 'EOS'
#!/bin/bash
(sleep 1; for c in "$@"; do echo "$c"; sleep 0.5; done; sleep 1) | script -qec "bash --norc ${BOPT:--i}" /dev/null | tr -d '\r'
EOS
chmod +x slow.sh pty.sh
set -m
```

`slow.sh 초 이름` 은 시작 줄을 찍고 그 초만큼 쉰 뒤 끝 줄을 찍는 스크립트입니다. `pty.sh '명령줄' ...` 은 인자를 한 줄씩 대화형 `bash` 에 쳐 넣고 화면을 그대로 보여 줍니다. `apt-get` 줄은 `ps`·`pgrep` 가 든 procps 가 없는 컨테이너에서만 필요하고 마지막 `set -m` 은 스크립트에서 잡 제어를 켭니다. 터미널에 직접 치는 셸에서는 이미 켜져 있습니다.



## 1. 백그라운드 잡 띄우고 목록 보기

> 명령 끝에 `&` 를 붙이면 프롬프트가 바로 돌아오고, `jobs` 가 그 셸이 쥔 잡을 번호와 상태로 보여 줍니다.

### & 와 $!

`&` 는 명령을 백그라운드 잡으로 띄웁니다. 방금 띄운 잡의 PID 는 변수 `$!` 에 들어 있습니다. 대화형 셸에서는 `&` 직후 `[1] 201` 같은 줄이 더 나옵니다.[^bashjob]

```bash
sleep 100 &
echo "마지막 백그라운드 PID: $!"    # 마지막 백그라운드 PID: 201
tail -f /dev/null &
sleep 300 &
```

### jobs 와 옵션

잡이 셋 있으니 옵션마다 무엇이 달라지는지 비교합니다. `+` 는 현재 잡, `-` 는 직전 잡입니다.[^bashjob]

```bash
# jobs: 잡 번호·상태·명령. 끝의 & 는 백그라운드로 띄웠다는 표시
jobs
```

```bash
[1]   Running                 sleep 100 &
[2]-  Running                 tail -f /dev/null &
[3]+  Running                 sleep 300 &
```

```bash
# -l: PID 를 함께 찍는다. 파이프라인이면 프로세스마다 한 줄
jobs -l
```

```bash
[1]    201 Running                 sleep 100 &
[2]-   202 Running                 tail -f /dev/null &
[3]+   203 Running                 sleep 300 &
```

```bash
# -p: 잡의 프로세스 그룹 리더 PID 만 찍는다
jobs -p
```

```bash
201
202
203
```

`-r` 은 실행 중인 잡만, `-s` 는 멈춘 잡만 보입니다. 비교하려고 잡 3 을 `SIGTSTP`(`Ctrl+Z` 가 보내는 신호)로 멈춰 둡니다. 신호가 닿을 시간을 0.3초 줍니다.

```bash
kill -TSTP %3
sleep 0.3
# -r: 실행 중인 잡만
jobs -r
# -s: 멈춘 잡만
jobs -s
```

```bash
[1]   Running                 sleep 100 &
[2]-  Running                 tail -f /dev/null &
[3]+  Stopped                 sleep 300
```

앞 두 줄이 `-r` 의 출력이고 마지막 줄이 `-s` 의 출력입니다. 멈춘 잡에는 `&` 가 붙지 않습니다.

`-x` 는 명령 인자 속 잡 지정(`%1`)을 그 잡의 프로세스 그룹 ID 로 바꿔서 명령을 실행합니다. 잡을 PID 로 받는 명령에 넘길 때 씁니다.[^jobs]

```bash
# -x: 인자의 %1·%3 을 프로세스 그룹 ID 로 바꿔 echo 실행
jobs -x echo %1 %3    # 201 203
```



## 2. 잡을 이름이나 번호로 가리키기

> 잡 번호는 그 셸 안에서만 통하고, `%` 로 시작하는 잡 지정으로 번호·직전 잡·명령 이름을 가리킵니다.

앞 절의 잡 셋(1 `sleep 100`, 2 `tail -f /dev/null`, 3 `sleep 300` 이 멈춤)이 그대로 있다고 보고 이어 갑니다. 잡 지정은 `jobs` 뿐 아니라 `fg`·`bg`·`kill`·`wait`·`disown` 모두에 같게 쓰입니다.[^bashjob]

```bash
# %1: 번호로 지정
jobs %1    # [1]   Running                 sleep 100 &

# %+ (%%, %): 현재 잡. 가장 최근에 띄웠거나 멈춘 잡
jobs %+    # [3]+  Stopped                 sleep 300

# %-: 직전 잡
jobs %-    # [2]-  Running                 tail -f /dev/null &

# %%: %+ 와 같다
jobs %%    # [3]+  Stopped                 sleep 300
```

```bash
# %이름: 그 이름으로 시작하는 명령. 한 잡만 맞을 때
jobs %tail    # [2]-  Running                 tail -f /dev/null &

# %?문자열: 명령줄 어디에든 그 문자열이 든 잡
jobs %?null    # [2]-  Running                 tail -f /dev/null &
jobs %?300     # [3]+  Stopped                 sleep 300
```

접두사나 문자열이 둘 이상의 잡에 맞으면 오류를 냅니다. `sleep` 으로 시작하는 잡이 둘이라 아래는 실패합니다.[^bashjob]

```bash
jobs %sleep
```

```bash
bash: line 25: jobs: sleep: ambiguous job spec
bash: line 25: jobs: %sleep: no such job
```

정리하면서 잡 지정을 한 번에 여러 개 넘길 수 있다는 것도 봅니다. 신호가 닿을 시간을 주고 `wait` 로 알림을 받습니다.

```bash
kill %1 %2 %3
sleep 0.3
wait
```

```bash
[1]   Terminated              sleep 100
[2]-  Terminated              tail -f /dev/null
[3]+  Terminated              sleep 300
```



## 3. 잡 멈추고 이어 돌리기

> 포그라운드 명령은 `Ctrl+Z` 로 멈추고, `bg` 로 뒤에서 이어 돌리거나 `fg` 로 앞으로 가져옵니다.

### Ctrl+Z, bg, fg

`Ctrl+Z` 를 누르면 포그라운드 프로세스가 멈추고 셸로 제어가 돌아옵니다. 멈춘 잡을 `bg` 가 백그라운드에서, `fg` 가 포그라운드에서 이어 돌립니다.[^bashjob] 아래는 `pty.sh` 로 `sleep 100` 을 치고 실제 `Ctrl+Z`(`^Z`)와 `Ctrl+C`(`^C`)를 보낸 화면입니다. `bash-5.2#` 는 쳐 넣은 줄이 아니라 프롬프트입니다.

```bash
./pty.sh 'sleep 100' $'\x1a' 'jobs' 'bg' 'jobs' 'fg' $'\x03' 'jobs'
```

```bash
bash-5.2# sleep 100
^Z

[1]+  Stopped                 sleep 100
bash-5.2# 
bash-5.2# jobs
[1]+  Stopped                 sleep 100
bash-5.2# bg
[1]+ sleep 100 &
bash-5.2# jobs
[1]+  Running                 sleep 100 &
bash-5.2# fg
sleep 100
^C

bash-5.2# 
bash-5.2# jobs
bash-5.2# exit
```

`bg` 는 잡을 `&` 로 띄운 것처럼 바꿔 `[1]+ sleep 100 &` 를 찍고 `fg` 는 명령줄을 다시 보여 주며 터미널을 되가져옵니다. `Ctrl+C` 로 끝나 마지막 `jobs` 는 비어 있습니다.

### 키 없이 같은 일 하기

스크립트에는 키 입력이 없으므로 `kill -TSTP` 가 `Ctrl+Z` 를 대신합니다. 잡 지정만 쓴 `%1 &` 는 `bg %1` 과, `%1` 만 쓴 것은 `fg %1` 과 같습니다.[^bashjob]

```bash
sleep 100 &
kill -TSTP %1
sleep 0.3
jobs
# %1 &: bg %1 과 같다
%1 &
jobs
kill %1
sleep 0.3
wait
```

```bash
[1]+  Stopped                 sleep 100
[1]+ sleep 100 &
[1]+  Running                 sleep 100 &
[1]+  Terminated              sleep 100
```

`fg` 는 잡이 끝날 때까지 터미널을 쥡니다. 1초 걸리는 잡을 `fg %1` 과 `%1` 로 앞으로 가져옵니다.

```bash
bash slow.sh 1 quick &
fg %1
bash slow.sh 1 again &
# %1: fg %1 과 같다
%1
```

```bash
bash slow.sh 1 quick
start quick
end quick
bash slow.sh 1 again
start again
end again
```

### 상태가 바뀐 잡만 보기

`jobs -n` 은 마지막 알림 뒤 상태가 바뀐 잡만 보입니다. 한 번 보이면 다음 `jobs -n` 은 비어 있습니다.[^jobs]

```bash
sleep 100 &
jobs
kill -TSTP %1
sleep 0.2
# -n: 알림 뒤 상태가 바뀐 잡만. 두 번째는 출력 없음
jobs -n
jobs -n
kill -KILL %1
sleep 0.3
wait
```

```bash
[1]+  Running                 sleep 100 &
[1]+  Stopped                 sleep 100
bash: line 37:   206 Killed                  sleep 100
```

첫 줄은 `jobs`, 둘째 줄은 첫 `jobs -n`, 마지막 줄은 `wait` 가 알린 종료입니다.



## 4. 잡이 끝나기를 기다리기

> `wait` 는 백그라운드 잡이 끝날 때까지 기다리고 그 종료 상태를 돌려줍니다.

종료 상태 3 으로 끝나는 잡, 2초 잡, 3초 잡을 띄워 둡니다. `p2` 는 2초 잡의 PID 입니다.

```bash
(sleep 1; exit 3) &
sleep 2 &
p2=$!
sleep 3 &
```

```bash
# wait %N: 그 잡이 끝나기를 기다린다. 종료 상태는 $? 로 받는다
wait %1
echo $?    # 3

# -n: 남은 잡 중 하나가 끝나기를 기다린다. -p 변수: 끝난 잡의 PID 를 담는다
wait -n -p who
echo "who=$who p2=$p2"    # who=233 p2=233
```

`-n` 은 먼저 끝난 2초 잡을 받았고 `who` 가 `p2` 와 같습니다. `-p` 는 `-n` 과 함께 쓸 때만 쓸모가 있습니다.[^bashjob]

```bash
# 인자 없이: 남은 잡이 모두 끝나기를 기다린다. 상태는 0
wait
echo $?    # 0

# 이 셸의 자식이 아닌 PID: 상태 127
wait 99999
echo $?
```

```bash
bash: line 66: wait: pid 99999 is not a child of this shell
127
```

잡 제어가 켜져 있으면 `wait` 는 잡이 끝날 때뿐 아니라 멈출 때도 돌아옵니다. 멈춘 잡의 `wait` 가 148(128 + `SIGTSTP` 20)을 돌려주고 `-f` 를 주면 끝날 때까지 기다립니다.[^bashjob]

```bash
sleep 2 &
p=$!
kill -TSTP $p
# 멈추면 바로 돌아온다
wait $p
echo $?    # 148
kill -CONT $p
# -f: 멈춤이 아니라 종료를 기다린다
wait -f $p
echo $?    # 0
```



## 5. nohup 으로 SIGHUP 무시하고 시작하기

> `nohup 명령 &` 는 `SIGHUP` 을 무시한 채 명령을 시작해, 터미널이 끊겨도 그 명령이 죽지 않게 합니다.

`nohup` 은 표준 출력이 터미널이면 `nohup.out` 에 덧붙이고 표준 입력이 터미널이면 못 읽는 파일에 이어 둡니다.[^nohup] 터미널 출력은 `pty.sh` 로 받습니다. 알림 줄(`[1]+  Done`)이 앞서 친 줄 사이에 끼어 보입니다.

```bash
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

출력을 파일로 돌리면 `nohup.out` 을 만들지 않습니다. 먼저 앞 예의 `nohup.out` 을 지웁니다. 입력이 터미널인 점만 `nohup: ignoring input` 으로 알려 줍니다.[^nohup]

```bash
rm -f nohup.out
./pty.sh 'nohup ./slow.sh 1 job > job.log 2>&1 &' 'sleep 2' 'cat job.log' 'ls nohup.out'
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

실무에서는 입력까지 `/dev/null` 로 돌려 세 스트림을 모두 정해 둡니다. `/proc/PID/fd/0·1·2` 가 가리키는 곳으로 확인합니다.

```bash
nohup ./slow.sh 3 job > job.log 2>&1 < /dev/null &
readlink /proc/$!/fd/0 /proc/$!/fd/1 /proc/$!/fd/2
wait
```

```bash
/dev/null
/root/cmd-lab/jobs/job.log
/root/cmd-lab/jobs/job.log
```



## 6. disown 으로 이미 뜬 잡 떼어 놓기

> `disown` 은 이미 돌고 있는 잡을 셸의 `SIGHUP` 전달 대상에서 뺍니다.

대화형 셸은 `SIGHUP` 을 받으면 종료하기 전에 잡 표의 모든 잡에 `SIGHUP` 을 다시 보냅니다. `disown` 은 잡을 표에서 빼거나(`disown`) 표에 남기되 보내지 않게 표시합니다(`disown -h`).[^bashsig] 터미널 끊김은 대화형 셸에 `kill -HUP $$` 를 쳐서 흉내 냅니다. `$$` 는 그 셸의 PID 입니다. 네 잡을 띄워 일반·`nohup`·`disown -h`·`disown` 을 맞댑니다.

```bash
./pty.sh 'sleep 301 &' 'nohup sleep 302 > /dev/null 2>&1 &' 'sleep 303 &' 'disown -h %3' 'sleep 304 &' 'disown %4' 'jobs -l' 'kill -HUP $$'
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

옵션은 대상을 고릅니다. 잡 지정 없이 `-r` 은 실행 중인 잡만, `-a` 는 모든 잡을 다룹니다. `-h` 와 합치면(`-ah`) 표에서 빼지 않고 표시만 합니다. 아래 셋은 같은 방식으로 `SIGHUP` 을 보내 살아남은 `sleep` 을 봅니다.[^bashjob]

```bash
# -r: 실행 중인 잡만 뺀다. 멈춘 잡(312)은 표에 남아 SIGHUP 을 받는다
./pty.sh 'sleep 311 &' 'sleep 312 &' 'kill -TSTP %2' 'disown -r' 'jobs' 'kill -HUP $$'
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
# -a: 모든 잡을 표에서 뺀다. jobs 가 비어 있고 둘 다 산다
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
# -ah: 표에는 남기고 SIGHUP 만 보내지 않게 표시한다. jobs 에 둘 다 보이고 둘 다 산다
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



## 7. setsid 로 새 세션에서 시작하기

> `setsid` 는 명령을 새 세션에서 실행해 원래 터미널과의 연결을 끊습니다.

`setsid` 는 자신이 프로세스 그룹 리더이면 `fork` 한 뒤 자식에서 실행하고 아니면 그 프로세스에서 곧바로 실행합니다.[^setsid] 잡 제어가 켜진 셸에서는 앞 명령이 리더라 `fork` 하고 `setsid` 자신은 바로 끝납니다. `-w` 는 그 끝을 기다립니다.

```bash
# 옵션 없이: setsid 는 곧바로 끝나고 sleep 은 계속 돈다
setsid sleep 2; pgrep -x sleep | wc -l    # 1

# -w (--wait): 명령이 끝나기를 기다리고 그 종료 상태를 돌려받는다
setsid -w sleep 2; pgrep -x sleep | wc -l    # 0
setsid -w sh -c 'exit 7'; echo "exit=$?"    # exit=7
```

`-f` 는 리더가 아닐 때도 `fork` 하게 합니다. 잡 제어가 없는 `bash -c` 안에서 비교합니다. 옵션 없이는 `$!` 가 곧 `sleep` 의 PID 입니다. `-f` 를 주면 `$!`(`setsid` 의 PID)와 `sleep` 의 PID 가 다릅니다.[^setsid]

```bash
pkill -x sleep
bash -c 'setsid sleep 100 & echo "setsid pid=$!"; sleep 0.2; pgrep -x sleep'
pkill -x sleep
bash -c 'setsid -f sleep 101 & echo "setsid pid=$!"; sleep 0.2; pgrep -x sleep'
pkill -x sleep
```

```bash
setsid pid=371
371
setsid pid=375
377
```

`-c` 는 제어 터미널을 현재 터미널로 정하는 옵션입니다. 그 터미널이 이미 다른 세션의 제어 터미널이면 커널이 `EPERM` 으로 거절합니다. 다만 `CAP_SYS_ADMIN` 권한이 있으면 터미널을 빼앗아 성공하므로, 컨테이너 밖의 root 셸에서는 결과가 다릅니다.[^ioctl]

아래 `sleep 102` 는 터미널(`pts/0`)이 남아 있습니다. `sleep 103` 은 `setsid` 로 터미널이 `?` 가 되었습니다. `-c` 를 준 `sleep 104` 는 `CAP_SYS_ADMIN` 이 없는 기본 Docker 컨테이너라 실패했습니다.

```bash
./pty.sh 'sleep 102 &' 'setsid sleep 103 &' 'setsid -c sleep 104 &' 'ps -o pid,pgid,sid,tty,args -C sleep | grep -E "PID|sleep 10"'
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



## 8. nohup·disown·setsid 한 예로 맞대기

> 같은 `sleep` 을 세 방식으로 띄워 프로세스 그룹·세션·무시하는 신호를 비교하면 셋이 끊는 고리가 다름이 보입니다.

`sleep 401` 은 `nohup`, `402` 는 `disown`, `403` 은 `setsid`, `404` 는 대조군입니다. `ps` 의 `-p $$` 는 이 셸을 함께 보여 줍니다. 무시하는 신호는 `/proc/PID/status` 의 `SigIgn` 비트마스크로 봅니다.[^proc]

```bash
nohup sleep 401 > /dev/null 2>&1 &
sleep 402 & disown
setsid sleep 403 &
sleep 404 &
sleep 0.3
ps -o pid,pgid,sid,stat,args -p $$ -C sleep
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

`nohup` 잡은 신호를 무시해서 삽니다. `disown` 잡은 셸이 신호를 보내지 않아서 삽니다. `setsid` 잡은 세션이 달라 끊김이 닿지 않아서 삽니다.

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



## 9. 셸을 닫을 때 잡에 신호 보내기

> `shopt -s huponexit` 를 켜면 셸이 종료할 때도 모든 잡에 `SIGHUP` 을 보냅니다.

기본값(꺼짐)에서는 `exit` 로 셸을 닫아도 백그라운드 잡에 `SIGHUP` 을 보내지 않습니다. 매뉴얼은 `huponexit` 이 대화형 로그인 셸의 종료에 적용된다고 적습니다.[^bashsig] 아래는 기본값, 로그인 셸이 아닌 셸에서 켠 경우, 로그인 셸(`-il`)에서 켠 경우를 차례로 받은 것입니다. 마지막 `ps` 가 빈 것만 잡이 죽었다는 뜻입니다.

```bash
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

- [jobs·nohup·disown 이론](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#잡의-상태를-옮기는-명령) — 잡 상태가 바뀌는 흐름과 상태 그림
- [세션과 제어 터미널](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#세션과-제어-터미널) — `PGID`·`SID`·제어 터미널이 무엇인지
- [터미널이 끊길 때 살아남는 잡](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#터미널이-끊길-때-살아남는-잡) — 끊김이 `SIGHUP` 으로 잡에 닿는 사슬
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

- GNU bash 5.2.15 의 `help jobs`·`help bg`·`help fg`·`help wait`·`help disown` 원문 — Debian 12 컨테이너에서 2026-11-11 출력
- [GNU Bash Reference Manual — Job Control](https://www.gnu.org/software/bash/manual/html_node/Job-Control.html) — 「Job Control Basics」·「Job Control Builtins」. 지금 gnu.org 는 5.3 판이라 각주의 5.2 인용과 문구가 조금 다릅니다
- [nohup(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/nohup.1.en.html), [setsid(1) — Debian bookworm](https://manpages.debian.org/bookworm/util-linux/setsid.1.en.html)

[^bashjob]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Job Control Basics — "When Bash starts a job asynchronously, it prints a line that looks like", "The character '%' introduces a job specification", "A job may also be referred to using a prefix of the name used to start it, or using a substring that appears in its command line", "If the prefix or substring matches more than one job, Bash reports an error", "Typing the ... character (typically '^Z', Control-Z) while a process is running causes that process to be stopped and returns control to Bash", "'%1' is a synonym for 'fg %1'", "'%1 &' resumes job 1 in the background, equivalent to 'bg %1'", "When the shell is waiting for a job or process using the 'wait' builtin, and job control is enabled, 'wait' will return when the job changes state". Job Control Builtins — `wait` "If the '-n' option is supplied, 'wait' waits for a single job from the list of PIDs or JOBSPECs or, if no arguments are supplied, any job, to complete and returns its exit status", "If the '-p' option is supplied, the process or job identifier of the job for which the exit status is returned is assigned to the variable VARNAME ... This is useful only when the '-n' option is supplied", "Supplying the '-f' option, when job control is enabled, forces 'wait' to wait for each PID or JOBSPEC to terminate before returning its status, instead of returning when it changes status", `disown` "disown [-ar] [-h] [JOBSPEC ... | PID ... ]", "If no JOBSPEC is supplied, the '-a' option means to remove or mark all jobs; the '-r' option without a JOBSPEC argument restricts operation to running jobs". https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html, https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
[^jobs]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Job Control Builtins — `jobs` "'-l' List process IDs in addition to the normal information", "'-n' Display information only about jobs that have changed status since the user was last notified of their status", "'-p' List only the process ID of the job's process group leader", "'-r' Display only running jobs", "'-s' Display only stopped jobs", "If the '-x' option is supplied, 'jobs' replaces any JOBSPEC found in COMMAND or ARGUMENTS with the corresponding process group ID". https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
[^bashsig]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Signals — "Before exiting, an interactive shell resends the 'SIGHUP' to all jobs, running or stopped", "To prevent the shell from sending the 'SIGHUP' signal to a particular job, it should be removed from the jobs table with the 'disown' builtin ... or marked to not receive 'SIGHUP' using 'disown -h'", "If the 'huponexit' shell option has been set with 'shopt' ... Bash sends a 'SIGHUP' to all jobs when an interactive login shell exits". https://www.gnu.org/software/bash/manual/html_node/Signals.html
[^nohup]: nohup(1) (GNU coreutils 9.1, Debian bookworm) — "Run COMMAND, ignoring hangup signals", "If standard input is a terminal, redirect it from an unreadable file. If standard output is a terminal, append output to 'nohup.out' if possible, '$HOME/nohup.out' otherwise. If standard error is a terminal, redirect it to standard output. To save output to FILE, use 'nohup COMMAND > FILE'". https://manpages.debian.org/bookworm/coreutils/nohup.1.en.html
[^setsid]: setsid(1) (util-linux, Debian bookworm) — "setsid runs a program in a new session. The command calls fork(2) if already a process group leader. Otherwise, it executes a program in the current process", "-c, --ctty Set the controlling terminal to the current one", "-f, --fork Always create a new process", "-w, --wait Wait for the execution of the program to end, and return the exit status of this program as the exit status of setsid". https://manpages.debian.org/bookworm/util-linux/setsid.1.en.html
[^ioctl]: ioctl_tty(2) (Linux man-pages 6.03, Debian bookworm), TIOCSCTTY — "If this terminal is already the controlling terminal of a different session group, then the ioctl fails with EPERM, unless the caller has the CAP_SYS_ADMIN capability and arg equals 1, in which case the terminal is stolen". https://manpages.debian.org/bookworm/manpages-dev/ioctl_tty.2.en.html
[^proc]: proc_pid_status(5), `SigBlk`·`SigIgn`·`SigCgt` — "Masks (expressed in hexadecimal) indicating signals being blocked, ignored, and caught". https://man7.org/linux/man-pages/man5/proc_pid_status.5.html
