---
title: jobs·bg·fg·wait 참조 시트
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
  - ./nohup·disown·setsid.md
updated: 2026-11-13
---

# jobs·bg·fg·wait 참조 시트

---

> 터미널 하나에서 명령 여럿을 돌리는 `&`·`jobs`·`fg`·`bg`·`wait` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `jobs`·`bg`·`fg`·`wait` 는 한 셸이 쥔 백그라운드 잡을 보고, 멈추고 이어 돌리고, 끝나기를 기다립니다.

네 명령은 모두 bash 내장이라 `type -a` 가 `shell builtin` 이라고 답하고 외부 바이너리가 없습니다. 터미널이 끊겨도 잡을 살려 두는 `nohup`·`disown`·`setsid` 는 [nohup·disown·setsid 시트](./nohup·disown·setsid.md)에서 다룹니다.

출력은 Debian 12 컨테이너(GNU bash 5.2.15)에서 받았고 `pty.sh` 의 `script -qec` 는 util-linux 판 옵션이라 macOS 에서는 맞지 않으니 Linux 에서 실행합니다. 스크립트를 `bash -s` 로 돌려 받은 오류 줄에는 `bash: line 25:` 가, 대화형 셸에서는 `bash:` 만 붙고 PID 와 `PGID`·`SID` 는 실행마다 달라집니다.



## 핵심 문법

> 잡은 `&` 로 띄우고 `%` 로 시작하는 잡 지정으로 가리키며, `jobs`·`bg`·`fg`·`wait` 가 보고 옮기고 기다립니다.

```bash
# 호출 형태. 네 명령 모두 bash 내장이고 help <이름> 의 첫 줄이다
jobs [-lnprs] [jobspec ...] or jobs -x command [args]
bg [job_spec ...]
fg [job_spec]
wait [-fn] [-p var] [id ...]

# 뒤에서 띄우고 방금 띄운 잡의 PID 를 받는다 (백그라운드로 띄우고 PID 받기)
명령 &
echo $!

# 잡 목록을 본다 (잡 목록을 옵션별로 보기)
jobs
jobs -l
jobs -p
jobs -r
jobs -s
jobs -x 명령 %1

# 잡을 번호·직전 잡·이름으로 가리킨다 (잡을 이름이나 번호로 가리키기)
jobs %1
jobs %-
jobs %이름
jobs %?문자열

# 멈춘 잡을 뒤나 앞에서 이어 돌린다 (Ctrl+Z 로 멈추고 bg·fg 로 잇기)
bg %1
fg %1

# 키 없이 멈추고 잇는다 (키 입력 없이 멈추고 잇기)
kill -TSTP %1
%1 &
%1

# 알림 뒤 상태가 바뀐 잡만 본다 (상태가 바뀐 잡만 보기)
jobs -n

# 잡이 끝나기를 기다린다 (잡이 끝나기를 기다리기)
wait %1
wait -n -p 변수
wait
```



## 종료 코드

> 내장 넷은 성공하면 0 이고, `wait` 는 기다린 잡의 종료 코드를 그대로 돌려줍니다.[^help-exit]

아래 예는 「실습 준비」 의 `set -m` 을 켠 셸에서 돌립니다. 모르는 옵션은 내장 공통으로 2 이고 신호로 죽은 잡은 128 에 신호 번호를 더한 값입니다.[^bash-exit]

```bash
# help 의 Exit Status 를 줄인 것이다. 숫자는 아래 실측이다
# jobs  성공이면 0. -x 를 쓰면 실행한 명령의 종료 코드
#       없는 잡 지정은 1, 모르는 옵션은 2
# bg    성공이면 0. 잡 제어가 꺼져 있거나 없는 잡 지정이면 1
# fg    앞으로 가져온 명령의 종료 코드. 없는 잡 지정이면 1
# wait  마지막 ID 의 종료 코드. 이 셸의 자식이 아니면 127
#       모르는 옵션은 2

# 없는 잡 지정은 1 이고 모르는 옵션은 2 다. 오류 메시지는 버린다
jobs %9 2>/dev/null; echo $?    # 1
bg %9 2>/dev/null; echo $?    # 1
fg %9 2>/dev/null; echo $?    # 1
wait -z 2>/dev/null; echo $?    # 2

# 기다린 잡의 종료 코드를 그대로 받는다. 이 잡은 3 으로 끝난다
(sleep 1; exit 3) &
wait %1
echo $?    # 3

# 인자 없이: 남은 잡이 모두 끝나기를 기다린다. 기다릴 잡이 없어도 상태는 0
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

```bash
# 신호로 죽은 잡은 128 + 신호 번호다. KILL(9) 로 죽이면 137 이다
sleep 100 &
p=$!
kill -KILL $p
wait $p 2>/dev/null
echo $?    # 137
```

잡 제어가 켜져 있으면 `wait` 는 잡이 끝날 때뿐 아니라 멈출 때도 돌아옵니다.[^bashjob]

```bash
# 멈춘 잡은 148(128 + SIGTSTP 20)을 돌려준다
sleep 2 &
p=$!
kill -TSTP $p
# 멈추면 바로 돌아온다
wait $p
echo $?    # 148

# 이어 돌린 뒤 끝날 때까지 기다리면 상태가 0 이다
#   -f   멈춤이 아니라 종료를 기다린다
kill -CONT $p
wait -f $p
echo $?    # 0
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 스크립트가 모두 생깁니다.

실습 폴더를 만들고 스크립트 둘을 쓴 뒤 `set -m` 으로 잡 제어를 켭니다. 이 시트의 출력 대부분은 `set -m` 을 켠 스크립트로 받았습니다.

```bash
# 실습 폴더. 모든 예가 이 폴더에서 돌아간다
mkdir -p ~/cmd-lab/jobs && cd ~/cmd-lab/jobs

# ps·pgrep 가 든 procps 가 없는 컨테이너에서만 필요하다
apt-get update -qq >/dev/null 2>&1 \
  && apt-get install -y -qq procps >/dev/null 2>&1

# slow.sh 초 이름: 시작 줄을 찍고 그 초만큼 쉰 뒤 끝 줄을 찍는다
# 「키 입력 없이 멈추고 잇기」 와 nohup·disown·setsid 시트의 nohup 예가 쓴다
cat > slow.sh << 'EOS'
#!/bin/bash
echo "start $2"; sleep "$1"; echo "end $2"
EOS

# pty.sh '명령줄' ...: 인자를 한 줄씩 가상 터미널 안의 대화형 bash 에 쳐 넣고
# 화면을 보여 준다. Ctrl+Z 같은 키 입력과 [1]+  Done 알림이 나오는 예가 쓴다
# (「Ctrl+Z 로 멈추고 bg·fg 로 잇기」, nohup·disown·setsid 시트)
cat > pty.sh << 'EOS'
#!/bin/bash
(sleep 1; for c in "$@"; do echo "$c"; sleep 0.5; done; sleep 1) | script -qec "bash --norc ${BOPT:--i}" /dev/null | tr -d '\r'
EOS
chmod +x slow.sh pty.sh

# 스크립트에서 잡 제어를 켠다. 터미널에 직접 치는 셸에서는 이미 켜져 있다
set -m
```

### 백그라운드로 띄우고 PID 받기

> 명령 끝에 `&` 를 붙이면 프롬프트가 바로 돌아오고, 방금 띄운 잡의 PID 가 `$!` 에 담깁니다.

대화형 셸에서는 `&` 직후 `[1] 201` 같은 줄이 더 나옵니다.[^bashjob]

```bash
# 명령 끝의 & 는 명령을 백그라운드 잡으로 띄운다. 직후 PID 는 $! 에 담긴다
sleep 100 &
echo "마지막 백그라운드 PID: $!"    # 마지막 백그라운드 PID: 201

# 다음 예의 목록에서 쓸 잡 둘을 더 띄운다
tail -f /dev/null &
sleep 300 &
```

### 잡 목록을 옵션별로 보기

> `jobs` 가 그 셸이 쥔 잡을 번호와 상태로 보여 주고, 옵션이 보이는 범위와 열을 바꿉니다.

잡이 셋 있으니 옵션마다 무엇이 달라지는지 비교합니다. `+` 는 현재 잡, `-` 는 직전 잡입니다.[^bashjob]

```bash
# 잡 번호·상태·명령이 나온다. 끝의 & 는 백그라운드로 띄웠다는 표시다
jobs
```

```bash
[1]   Running                 sleep 100 &
[2]-  Running                 tail -f /dev/null &
[3]+  Running                 sleep 300 &
```

```bash
# 잡 번호 다음에 PID 열이 붙는다. 파이프라인이면 프로세스마다 한 줄이다
#   -l   PID 를 함께 찍는다
jobs -l
```

```bash
[1]    201 Running                 sleep 100 &
[2]-   202 Running                 tail -f /dev/null &
[3]+   203 Running                 sleep 300 &
```

```bash
# 잡마다 프로세스 그룹 리더의 PID 만 한 줄씩 나온다
#   -p   잡의 프로세스 그룹 리더 PID 만 찍는다
jobs -p
```

```bash
201
202
203
```

잡 3 을 멈춰 두고 실행 중인 잡과 멈춘 잡을 나눠 봅니다.

```bash
# 잡 3 을 SIGTSTP(Ctrl+Z 가 보내는 신호)로 멈춘다. 신호가 닿을 시간을 0.3초 준다
kill -TSTP %3
sleep 0.3

# 실행 중인 잡 1·2 만 나온다
#   -r   실행 중인 잡만 보인다
jobs -r

# 멈춘 잡 3 만 나온다
#   -s   멈춘 잡만 보인다
jobs -s
```

```bash
[1]   Running                 sleep 100 &
[2]-  Running                 tail -f /dev/null &
[3]+  Stopped                 sleep 300
```

앞 두 줄이 `-r` 의 출력이고 마지막 줄이 `-s` 의 출력입니다. 멈춘 잡에는 `&` 가 붙지 않습니다.

`-x` 는 잡을 PID 로 받는 명령에 넘길 때 씁니다.[^jobs]

```bash
# 인자의 %1·%3 이 프로세스 그룹 ID 로 바뀐 채 echo 가 실행된다
#   -x   명령 인자 속 잡 지정을 그 잡의 프로세스 그룹 ID 로 바꿔 실행한다
jobs -x echo %1 %3    # 201 203
```

### 잡을 이름이나 번호로 가리키기

> 잡 번호는 그 셸 안에서만 통하고, `%` 로 시작하는 잡 지정으로 번호·직전 잡·명령 이름을 가리킵니다.

「잡 목록을 옵션별로 보기」 의 잡 셋(1 `sleep 100`, 2 `tail -f /dev/null`, 3 멈춘 `sleep 300`)이 그대로 있다고 보고 이어 갑니다. 잡 지정은 `jobs` 뿐 아니라 `fg`·`bg`·`kill`·`wait`·`disown` 모두에 같게 쓰입니다.[^bashjob]

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

정리하면서 잡 지정을 한 번에 여러 개 넘길 수 있다는 것도 봅니다.

```bash
# 잡 지정 셋을 한 번에 넘겨 모두 종료한다. 신호가 닿을 시간을 주고 wait 로 알림을 받는다
kill %1 %2 %3
sleep 0.3
wait
```

```bash
[1]   Terminated              sleep 100
[2]-  Terminated              tail -f /dev/null
[3]+  Terminated              sleep 300
```

### Ctrl+Z 로 멈추고 bg·fg 로 잇기

> 포그라운드 명령은 `Ctrl+Z` 로 멈추고, `bg` 로 뒤에서 이어 돌리거나 `fg` 로 앞으로 가져옵니다.

`Ctrl+Z` 를 누르면 포그라운드 프로세스가 멈추고 셸로 제어가 돌아옵니다. 멈춘 잡을 `bg` 가 백그라운드에서, `fg` 가 포그라운드에서 이어 돌립니다.[^bashjob]

```bash
# sleep 100 을 치고 실제 Ctrl+Z(^Z)와 Ctrl+C(^C)를 보낸 화면을 받는다
# 출력의 bash-5.2# 는 쳐 넣은 줄이 아니라 프롬프트다
#   $'\x1a'   Ctrl+Z 키
#   $'\x03'   Ctrl+C 키
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

### 키 입력 없이 멈추고 잇기

> 스크립트에는 키 입력이 없으므로 `kill -TSTP` 가 `Ctrl+Z` 를 대신하고 잡 지정만 쓴 줄이 `bg`·`fg` 를 대신합니다.

잡 지정만 쓴 `%1 &` 는 `bg %1` 과, `%1` 만 쓴 것은 `fg %1` 과 같습니다.[^bashjob]

```bash
# 잡이 Stopped 로 바뀌었다가 Running 으로 돌아오고 마지막에 종료된다
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

```bash
# fg 는 잡이 끝날 때까지 터미널을 쥔다. 1초 걸리는 잡을 앞으로 가져온다
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

> `jobs -n` 은 마지막 알림 뒤 상태가 바뀐 잡만 보여 줍니다.

알림을 받은 잡은 다음 `jobs -n` 에서 빠집니다.[^jobs]

```bash
sleep 100 &
jobs
kill -TSTP %1
sleep 0.2
# 첫 -n 은 멈춘 잡을 보이고 두 번째는 출력이 없다
#   -n   마지막 알림 뒤 상태가 바뀐 잡만 보인다
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

### 잡이 끝나기를 기다리기

> `wait` 는 백그라운드 잡이 끝날 때까지 기다리고 그 종료 상태를 돌려줍니다.

종료 코드를 받는 예는 「종료 코드」 에 있고, 여기서는 먼저 끝나는 잡을 받습니다.

```bash
# 2초 잡과 3초 잡을 띄워 둔다. p2 는 2초 잡의 PID 다
sleep 2 &
p2=$!
sleep 3 &

# 먼저 끝난 2초 잡을 받았고 who 가 p2 와 같다
#   -n   남은 잡 중 하나가 끝나기를 기다린다
#   -p   끝난 잡의 PID 를 변수에 담는다
wait -n -p who
echo "who=$who p2=$p2"    # who=233 p2=233

# 남은 3초 잡이 끝나기를 기다린다
wait
```

`-p` 는 `-n` 과 함께 쓸 때만 쓸모가 있습니다.[^bashjob]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [jobs·nohup·disown 이론](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md#잡의-상태를-옮기는-명령) — 잡 상태가 바뀌는 흐름과 상태 그림
- [nohup·disown·setsid 시트](./nohup·disown·setsid.md) — 셸을 닫은 뒤에도 잡을 살려 두는 `nohup`·`disown`·`setsid`
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU bash 5.2.15 의 `help jobs`·`help bg`·`help fg`·`help wait` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU Bash Reference Manual — Job Control](https://www.gnu.org/software/bash/manual/html_node/Job-Control.html) — 「Job Control Basics」·「Job Control Builtins」. 지금 gnu.org 는 5.3 판이라 각주의 5.2 인용과 문구가 조금 다릅니다

[^bashjob]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Job Control Basics — "When Bash starts a job asynchronously, it prints a line that looks like", "The character '%' introduces a job specification", "A job may also be referred to using a prefix of the name used to start it, or using a substring that appears in its command line", "If the prefix or substring matches more than one job, Bash reports an error", "Typing the ... character (typically '^Z', Control-Z) while a process is running causes that process to be stopped and returns control to Bash", "'%1' is a synonym for 'fg %1'", "'%1 &' resumes job 1 in the background, equivalent to 'bg %1'", "When the shell is waiting for a job or process using the 'wait' builtin, and job control is enabled, 'wait' will return when the job changes state". Job Control Builtins — `wait` "If the '-n' option is supplied, 'wait' waits for a single job from the list of PIDs or JOBSPECs or, if no arguments are supplied, any job, to complete and returns its exit status", "If the '-p' option is supplied, the process or job identifier of the job for which the exit status is returned is assigned to the variable VARNAME ... This is useful only when the '-n' option is supplied", "Supplying the '-f' option, when job control is enabled, forces 'wait' to wait for each PID or JOBSPEC to terminate before returning its status, instead of returning when it changes status", `disown` "disown [-ar] [-h] [JOBSPEC ... | PID ... ]", "If no JOBSPEC is supplied, the '-a' option means to remove or mark all jobs; the '-r' option without a JOBSPEC argument restricts operation to running jobs". https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html, https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
[^jobs]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Job Control Builtins — `jobs` "'-l' List process IDs in addition to the normal information", "'-n' Display information only about jobs that have changed status since the user was last notified of their status", "'-p' List only the process ID of the job's process group leader", "'-r' Display only running jobs", "'-s' Display only stopped jobs", "If the '-x' option is supplied, 'jobs' replaces any JOBSPEC found in COMMAND or ARGUMENTS with the corresponding process group ID". https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
[^help-exit]: GNU bash 5.2.15 `help` 의 Exit Status 문단 (Debian 12) — jobs "Returns success unless an invalid option is given or an error occurs. If -x is used, returns the exit status of COMMAND.", bg "Returns success unless job control is not enabled or an error occurs.", fg "Status of command placed in foreground, or failure if an error occurs.", wait "Returns the status of the last ID; fails if ID is invalid or an invalid option is given, or if -n is supplied and the shell has no unwaited-for children." 1·2·127·137·148 은 이 시트의 실측입니다(Debian 12 컨테이너, GNU bash 5.2.15).
[^bash-exit]: GNU Bash Reference Manual 5.2 (Debian 12 `bash-doc` 의 `bash.info`), Exit Status — "All builtins return an exit status of 2 to indicate incorrect usage, generally invalid options or missing arguments", "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status". Job Control Builtins — `wait` "If neither JOBSPEC nor PID specifies an active child process of the shell, the return status is 127". https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html, https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
