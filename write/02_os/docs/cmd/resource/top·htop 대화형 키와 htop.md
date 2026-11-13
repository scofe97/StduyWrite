---
title: top·htop 대화형 키와 htop
tags: [linux, cheatsheet, top, htop, process, monitoring, cli, reference]
status: draft
source:
  - procps-ng 4.0.2 top(1) (Debian 12 `man top` 원문, manpages.debian.org bookworm)
  - htop 3.2.2 htop(1) (Debian 12 `man htop`·`htop --help` 원문)
related:
  - ../README.md
  - ./top·htop.md
updated: 2026-11-13
---

# top·htop 대화형 키와 htop

---

> `top` 으로 스레드와 명령줄까지 펼치는 옵션, 화면에서 누르는 키, 같은 일을 하는 `htop` 의 옵션과 키를 모았습니다.

## 개요

> 이 시트는 `top` 으로 스레드와 명령줄까지 펼치는 옵션, 화면에서 누르는 키, 같은 일을 하는 `htop` 을 다룹니다.

[top·htop 참조 시트](./top·htop.md)에서 스레드·명령줄 옵션과 대화형 키, `htop` 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 를 돌린 상태에서 이어지고, 출력은 같은 Debian 12 컨테이너(procps-ng 4.0.2 의 `top`, htop 3.2.2)에서 root 로 `top -b` 로 받았습니다.

`-H`·`-c`·`-w` 는 화면에서 누르는 `H`·`c` 키의 배치 모드 짝이라 키와 같이 모았습니다. `htop` 은 htop 패키지의 외부 바이너리(`/usr/bin/htop`)이고, 대화형 화면은 글로 옮길 수 없어 싣지 않았습니다.



## 핵심 문법

> `-H`·`-c`·`-w` 로 스레드와 명령줄을 펼치고, `htop` 은 같은 일을 대화형 화면으로 합니다.

```bash
# 호출 형태. top 은 top --help 의 Usage 줄이다
top [options]

# htop 은 --help 에 Usage 줄이 없어 man htop 의 SYNOPSIS 를 싣는다
htop [-dCFhpustvH]

# 스레드마다 한 줄로 보고, 명령줄을 폭을 늘려 본다 (스레드와 명령줄까지 보기)
top \
  -b \
  -n 1 \
  -H \
  -p PID
top \
  -b \
  -n 1 \
  -c \
  -w 폭 \
  -p PID

# htop 을 사용자와 트리 보기로 연다 (htop 으로 옮겨 가기)
htop -u 사용자 -t
```

### 대화형 키

> 아래 키는 화면에서 누르는 것이라 출력을 실을 수 없습니다.

뜻은 man 의 「INTERACTIVE Commands」 를 옮긴 것이고 `k`·`r` 은 대화형 입력이라 `-b` 에서는 쓸 수 없습니다. 설정 파일의 저장 위치는 man 의 「FILES」 에 있습니다.[^keys]

```bash
#   P   %CPU 로 정렬
#   M   %MEM 으로 정렬
#   N   PID 로 정렬
#   T   TIME+ 로 정렬
#       (P·M·N·T 는 옛 top 과의 호환용이라 도움말 화면에는 나오지 않는다)
#   R   정렬 방향을 뒤집음
#   1   CPU 상태를 한 줄에 합쳐 보이거나 CPU 마다 한 줄씩 보임
#   k   프로세스에 신호 보내기. PID 를 묻고 기본 신호는 SIGTERM
#   r   renice. PID 를 묻고 nice 값을 정함
#   c   COMMAND 를 프로그램 이름과 명령줄 사이에서 바꿈
#   H   스레드 보기 토글
#   f   열을 고르고 순서와 정렬 열을 정하는 화면을 엶
#   W   지금의 옵션과 표시 방식을 설정 파일에 저장
#   q   종료
```

### htop 화면 키

> `htop` 화면 안에서 자주 쓰는 키입니다.

뜻은 man htop 의 「INTERACTIVE COMMANDS」 를 옮긴 것입니다.[^htopkeys]

```bash
#   F1, h, ?   도움말
#   F2, S      설정 화면. 상단 미터와 표시 열을 정함
#   F3, /      명령줄 검색
#   F4, \      명령줄에 이 문자열이 든 프로세스만 거름
#   F5, t      트리 보기 토글
#   F6, <, >   정렬 열 고르기
#   F7, ]      nice 값을 낮춤(우선순위 올림). 슈퍼유저만
#   F8, [      nice 값을 올림(우선순위 내림)
#   F9, k      신호 메뉴를 열어 보냄. 태그한 프로세스가 있으면 모두에게
#   F10, q     종료
#   Space      프로세스에 태그를 켜고 끔
#   I          정렬 방향을 뒤집음
#   u          사용자를 골라 그 프로세스만
#   H          사용자 스레드 숨김 토글
#   K          커널 스레드 숨김 토글

# top 의 정렬 키 M·P·T·N 도 htop 에서 같은 뜻으로 된다
# top 의 k 와 htop 의 F9 는 같은 일을 한다
# 다만 htop 은 신호를 메뉴에서 고르고 태그한 여러 프로세스에 한꺼번에 보낸다
```



## 종료 코드

> `htop` 은 판을 찍으면 0, 옵션이나 그 값이 틀리면 1 로 끝납니다.

`man htop` 에는 종료 코드 절이 없어 뜻은 적지 않고 Debian 12 컨테이너에서 잰 값만 싣습니다.[^no-exit] `top` 의 실측값은 [top·htop 참조 시트](./top·htop.md)의 「종료 코드」 에 있습니다.

```bash
# 0  --version 처럼 정보를 찍고 끝났을 때
# 1  모르는 옵션을 주거나 옵션에 잘못된 값을 줬을 때
# 매뉴얼에 종료 코드 절이 없어 값은 모두 실측이다

# 판을 찍고 0 으로 끝난다
#   --version   판을 찍고 끝낸다
htop --version > /dev/null; echo $?    # 0

# htop 은 모르는 옵션에 메시지를 내고 1 로 끝난다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
htop --bad 2>&1; echo $?    # htop: unrecognized option '--bad' / 1

# 갱신 간격 값이 틀려도 메시지를 내고 1 로 끝난다
#   -d   갱신 간격 (--delay)
htop -d x 2>&1; echo $?    # Error: invalid delay value "x". / 1
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고 원래 시트의 프로세스를 그대로 씁니다.

먼저 [top·htop 참조 시트](./top·htop.md)의 「실습 준비」 블록을 돌립니다. PID·시각·메모리 값은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

### 스레드와 명령줄까지 보기

> 기본 화면은 프로세스 하나에 한 줄이고, 스레드는 `-H`, 명령줄 전체는 `-c`·`-w` 로 펼칩니다.

`threads.py` 를 돌리는 `python3` 은 스레드가 넷이고, `-p` 는 [top·htop 참조 시트](./top·htop.md)의 「프로세스 열 읽기」 에서 풀었습니다. 기본으로는 스레드를 합친 한 줄만 나옵니다.[^h]

```bash
# 스레드를 합산한 프로세스 한 줄이 나온다
top \
  -b \
  -n 1 \
  -p $(pgrep -f threads.py) \
  | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
```

```bash
# 스레드마다 한 줄이 나오고 요약 줄이 Threads: 4 total 로 바뀐다
#   -H   스레드를 하나씩 보인다 (--threads-show)
top \
  -b \
  -n 1 \
  -H \
  -p $(pgrep -f threads.py)
```

```bash
top - 13:06:55 up 1 day,  5:14,  0 user,  load average: 0.44, 0.28, 0.17
Threads:   4 total,   0 running,   4 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :   8004.2 total,   6516.0 free,   1006.4 used,    704.2 buff/cache     
MiB Swap:   9028.2 total,   9028.2 free,      0.0 used.   6997.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3137 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3138 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
   3139 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3
```

목록 첫 줄은 PID 와 같은 ID 를 가진 그룹 리더이고 나머지 셋이 그 프로세스에 속한 스레드의 ID 입니다.

`-c` 는 마지막으로 기억한 `c` 상태를 뒤집는 옵션이라 `c` 가 이미 켜져 있으면 프로그램 이름으로 돌아갑니다.[^c]

```bash
# COMMAND 열이 프로그램 이름 대신 명령줄로 나온다
# 출력을 파이프로 넘기면 80열에서 잘리고 끝에 + 가 붙는다
#   -c   COMMAND 를 프로그램 이름과 명령줄 사이에서 바꾼다 (--cmdline-toggle)
top \
  -b \
  -n 1 \
  -c \
  -p $(pgrep -f threads.py) \
  | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3+
```

`-w` 가 없으면 배치 모드에서도 폭은 `top` 을 띄운 터미널을 따릅니다.[^w]

```bash
# 폭을 100열로 잡는다. 아직 모자라면 + 로 잘린다
#   -w   출력 폭. 배치 모드에서 인자를 주면 그 폭이고 인자 없이 쓰면 최대 512열 (--width)
top \
  -b \
  -n 1 \
  -c \
  -w 100 \
  -p $(pgrep -f threads.py) \
  | tail -1
```

```bash
   3130 root      20   0  234796   8456   4728 S   0.0   0.1   0:00.00 python3 threads.py --name=p+
```

```bash
# 폭을 200열로 잡으면 명령줄이 잘리지 않고 마지막 줄은 줄바꿈까지 168바이트다
#   wc -c   바이트 수를 센다
top \
  -b \
  -n 1 \
  -c \
  -w 200 \
  -p $(pgrep -f threads.py) \
  | tail -1 \
  | wc -c
# 168

# 인자 없는 -w 는 배치 모드에서 최대 512열이라 같은 168바이트가 나온다
top \
  -b \
  -n 1 \
  -c \
  -w \
  -p $(pgrep -f threads.py) \
  | tail -1 \
  | wc -c
# 168
```

`-w` 에 인자를 안 주면 `COLUMNS=` 와 `LINES=` 환경 변수가 있을 때 그 값을 따릅니다.[^w]

```bash
# COLUMNS 가 있으면 인자 없는 -w 가 그 폭을 쓴다
COLUMNS=60 top \
  -b \
  -n 1 \
  -w \
  -p $(pgrep -f threads.py) \
  | sed -n 7,8p
```

```bash
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU
   3130 root      20   0  234796   8456   4728 S   0.0
```

### htop 으로 옮겨 가기

> `htop` 은 `top` 에 가로·세로 스크롤과 마우스, 트리 보기, 여러 프로세스 선택을 더한 화면입니다.

화면은 대화형이라 싣지 않고 실행 옵션과 키만 적으며, 키는 「htop 화면 키」 에 있습니다.

```bash
# 설치 (Debian/Ubuntu). top·htop 참조 시트의 「실습 준비」 가 이미 설치했다
apt-get install -y htop
htop --version    # htop 3.2.2
```

`htop` 의 실행 옵션은 `top` 과 이름이 비슷한데 뜻이 다른 것이 있습니다. `-d` 는 초가 아니라 10분의 1초 단위입니다.[^htopd]

```bash
# 기본 화면이 뜬다
htop

# appuser 의 프로세스만 남는다
#   -u   이 사용자의 프로세스만. 이름 없이 -u 만 주면 $USER (--user)
htop -u appuser

# PID 3128·3129 만 남는다
#   -p   이 PID 만. 쉼표로 여러 개 (--pid)
htop -p 3128,3129

# 프로세스가 부모 아래 트리로 나온다
#   -t   트리 보기 (--tree)
htop -t

# 2초마다 갱신한다
htop -d 20

# PERCENT_MEM 열로 정렬된다
#   -s   이 열로 정렬한다 (--sort-key)
htop -s PERCENT_MEM

# 명령에 python 이 든 프로세스만 남는다
#   -F   명령에 이 문자열이 든 프로세스만 (--filter)
htop -F python

# 신호 보내기·renice 같은 변경 기능이 꺼진다
#   --readonly   시스템과 프로세스를 바꾸는 기능을 끈다
htop --readonly

# 흑백 화면이 뜬다
#   -C   흑백으로 띄운다 (--no-color)
htop -C
```

`-s` 의 열 이름은 `htop --sort-key help` 가 보입니다. 아래는 그 목록에서 CPU 와 메모리 열만 고른 것입니다.[^htops]

```bash
# PERCENT_CPU·PERCENT_MEM·M_RESIDENT 가 든 줄 다섯이 나온다
htop --sort-key help | grep -E "PERCENT_(CPU|MEM)|M_RESIDENT"
```

```bash
         M_RESIDENT Resident set size, size of the text and data sections, plus stack usage
        PERCENT_CPU Percentage of the CPU time the process used in the last sampling
        PERCENT_MEM Percentage of the memory the process is using, based on resident memory size
  PERCENT_CPU_DELAY CPU delay %
              M_PSS proportional set size, same as M_RESIDENT but each page is divided by the number of processes sharing it
```

`-s` 를 `-t` 없이 주면 목록 보기로 강제되고 트리로 보려면 `-t` 를 함께 줍니다.[^htops]

### 실습 정리

> 이 시트는 따로 만든 것이 없어 원래 시트의 정리 블록만 돌립니다.

[top·htop 참조 시트](./top·htop.md)의 「실습 정리」 블록으로 띄운 프로세스를 끕니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [top·htop 참조 시트](./top·htop.md) — 배치 모드로 읽는 `top` 옵션과 실습 준비
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- procps-ng 4.0.2 의 `man top` 원문 — Debian 12 컨테이너에서 2026-11-11 확인
- htop 3.2.2 의 `htop --help`·`man htop` 원문 — Debian 12 컨테이너에서 2026-11-13 확인
- [top(1) — Debian bookworm](https://manpages.debian.org/bookworm/procps/top.1.en.html)
- [htop(1) — Debian bookworm](https://manpages.debian.org/bookworm/htop/htop.1.en.html)

[^h]: `man top` COMMAND-LINE Options — `-H, --threads-show` "Instructs top to display individual threads. Without this command-line option a summation of all threads in each process is shown."
[^c]: `man top` COMMAND-LINE Options — `-c, --cmdline-toggle` "Starts top with the last remembered `c' state reversed. Thus, if top was displaying command lines, now that field will show program names, and vice versa." 출력을 파이프로 넘겼을 때 80열에서 잘리는 것은 이 환경에서 관찰한 값입니다. 같은 명령을 120열 터미널에 바로 찍으면 120열 폭에서 잘렸습니다.
[^w]: `man top` COMMAND-LINE Options — `-w, --width [=COLUMNS]` "In Batch mode, when used without an argument top will format output using the COLUMNS= and LINES= environment variables, if set. Otherwise, width will be fixed at the maximum 512 columns. With an argument, output width can be decreased or increased (up to 512) but the number of rows is considered unlimited.", "Note: Without the use of this command-line option, output width is always based on the terminal at which top was invoked whether or not in Batch mode."
[^keys]: `man top` INTERACTIVE Commands — k :Kill-a-task: "You will be prompted for a PID and then the signal to send. ... The default signal, as reflected in the prompt, is SIGTERM.", r :Renice-a-Task: "You will be prompted for a PID and then the value to nice it to.", "c :Command-Line/Program-Name toggle", "H :Threads-mode toggle", f :Fields-Management: "This key displays a separate screen where you can change which fields are displayed, their order and also designate the sort field.", W :Write-the-Configuration-File: "This will save all of your options and toggles plus the current display mode and delay time.", "1 :Single/Separate-Cpu-States toggle", "q :Quit", "R :Reverse/Normal-Sort-Field toggle", 정렬 키 표(M 은 %MEM, N 은 PID, P 는 %CPU, T 는 TIME+), "For compatibility, this top supports most of the former top sort keys. Since this is primarily a service to former top users, these commands do not appear on any help screen.", FILES 6a "This file is created or updated via the 'W' interactive command."
[^htopd]: `htop --help` (htop 3.2.2) — "-d --delay=DELAY Set the delay between updates, in tenths of seconds", `man htop` COMMAND-LINE OPTIONS "-d --delay=DELAY Delay between updates, in tenths of a second.", "-u --user=USERNAME|UID Show only the processes of a given user", "-p --pid=PID,PID... Show only the given PIDs", "-t --tree Show processes in tree view.", "-F --filter=FILTER Filter processes by terms matching the commands.", "--readonly Disable all system and process changing features", "-C --no-color --no-colour Start htop in monochrome mode", `htop --help` "-u --user[=USERNAME] Show only processes for a given user (or $USER)". https://manpages.debian.org/bookworm/htop/htop.1.en.html
[^htops]: `man htop` COMMAND-LINE OPTIONS — "-s --sort-key COLUMN Sort by this column (use --sort-key help for a column list). This will force a list view unless you specify -t at the same time." `htop --sort-key help` 출력 (3.2.2): "PERCENT_CPU Percentage of the CPU time the process used in the last sampling", "PERCENT_MEM Percentage of the memory the process is using, based on resident memory size", "M_RESIDENT Resident set size, size of the text and data sections, plus stack usage".
[^htopkeys]: `man htop` INTERACTIVE COMMANDS — "F1, h, ? Go to the help screen", "F2, S Go to the setup screen", "F3, / Incrementally search the command lines of all the displayed processes", "F4, \ Incremental process filtering: type in part of a process command line and only processes whose names match will be shown", "F5, t Tree view: organize processes by parenthood", "F6, <, > Selects a field for sorting", "F7, ] Increase the selected process's priority (subtract from 'nice' value). This can only be done by the superuser.", "F8, [ Decrease the selected process's priority (add to 'nice' value)", "F9, k "Kill" process: sends a signal which is selected in a menu, to one or a group of processes. If processes were tagged, sends the signal to all tagged processes.", "F10, q Quit", "Space Tag or untag a process", "I Invert the sort order", "u Show only processes owned by a specified user", "K Hide kernel threads", "H Hide user threads", "N Sort by PID. M Sort by memory usage (top compatibility key). P Sort by processor usage (top compatibility key). T Sort by time (top compatibility key)."
[^no-exit]: `man top` (procps-ng 4.0.2) 과 `man htop` (htop 3.2.2) 의 절 제목에는 종료 코드를 다루는 절이 없습니다. top 은 "NAME", "SYNOPSIS", "DESCRIPTION", "OVERVIEW" 와 "1. COMMAND-LINE Options" 부터 "9. BUGS", "10. SEE Also" 까지이고, htop 은 "NAME", "SYNOPSIS", "DESCRIPTION", "COMMAND-LINE OPTIONS", "INTERACTIVE COMMANDS", "COLUMNS", "EXTERNAL LIBRARIES", "CONFIG FILES", "MEMORY SIZES", "SEE ALSO", "SEE ALSO FOR PCP", "AUTHORS", "COPYRIGHT" 입니다. https://manpages.debian.org/bookworm/procps/top.1.en.html, https://manpages.debian.org/bookworm/htop/htop.1.en.html
