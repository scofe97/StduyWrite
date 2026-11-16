---
title: timeout 참조 시트
tags: [linux, cheatsheet, timeout, signal, shell, exit-code, cli, reference]
status: draft
source:
  - rust-coreutils(uutils 0.10.0) timeout(1) (OrbStack Ubuntu 26.04 VM 의 `timeout --help` 와 `man timeout` 원문)
  - GNU coreutils 9.7 timeout(1) (같은 VM 의 `gnutimeout --help` 와 `man gnutimeout` 원문)
related:
  - ../README.md
  - ../process/kill·pgrep·killall.md
  - ../process/nohup·disown·setsid.md
  - ./flock.md
  - ../net/netstat.md
  - ../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md
updated: 2026-11-16
---

# timeout 참조 시트

---

> 명령에 제한 시간을 걸고 넘기면 시그널로 끝내는 `timeout` 의 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `timeout` 은 명령을 돌리다가 제한 시간이 지나도 살아 있으면 시그널을 보내 끝냅니다.

Ubuntu 26.04 의 `/usr/bin/timeout` 은 GNU coreutils 가 아니라 rust-coreutils(uutils 0.10.0)의 것입니다. `dpkg -S` 결과는 `coreutils-from-uutils: /usr/bin/timeout` 입니다. GNU coreutils 9.7 판은 같은 VM 에 `gnutimeout` 이름으로 따로 깔려 있습니다(`gnu-coreutils: /usr/bin/gnutimeout`).[^impl]

이 시트는 OrbStack 의 Linux VM 에서 `timeout`(uutils)으로 실측했습니다. GNU 판과 결과가 갈리는 곳은 `gnutimeout` 으로 같이 돌렸고, 그 차이는 「uutils 와 GNU 의 -s KILL 종료 코드」 에 모았습니다.

macOS 26.6 에는 `/usr/bin/timeout` 이 없습니다. Homebrew 의 coreutils 9.9 를 넣으면 GNU 판이 `timeout`·`gtimeout` 두 이름으로 생깁니다(실측).



## 핵심 문법

> 앞에서부터 옵션, 제한 시간, 명령 순서로 쓰고, 옵션으로 보낼 시그널·유예·종료 코드 처리를 바꿉니다.

```bash
# 호출 형태 (timeout --help 의 usage. uutils)
Usage: timeout [OPTION] DURATION COMMAND...

# 호출 형태 (gnutimeout --help 의 usage. GNU)
Usage: gnutimeout [OPTION] DURATION COMMAND [ARG]...
  or:  gnutimeout [OPTION]

# 시간 안에 끝내지 못하면 TERM 으로 끊는다 (시간이 넘으면 끊기)
timeout 시간 명령

# 보낼 시그널을 바꾼다 (시그널 정하기)
timeout -s 시그널 시간 명령

# 시간 초과여도 명령 자신의 종료 코드를 낸다 (원래 종료 코드 보존)
timeout -p 시간 명령

# 시그널을 무시하는 명령을 유예 뒤 KILL 로 끝낸다 (시그널을 무시하는 스크립트)
timeout -k 유예 시간 명령

# 보낸 시그널을 stderr 로 알린다 (보낸 시그널 보기)
timeout -v 시간 명령

# 명령의 자식은 시간 초과 대상에서 뺀다 (자식까지 끊기와 --foreground)
timeout -f 시간 명령
```

### 지속 시간 접미사

> 제한 시간과 `-k` 의 유예 자리에 쓰는 숫자 뒤의 접미사입니다.

뜻은 GNU 판 매뉴얼의 DURATION 설명을 따랐고, uutils 의 `timeout --help` 도 같은 뜻을 적습니다.[^opts]

```bash
# 숫자 바로 뒤에 붙인다. 소수도 받는다 (0.5, 1.5m 처럼)
#   s   초 (접미사를 생략하면 이것)
#   m   분
#   h   시간
#   d   일
#   0   제한 없음 (시간 초과를 끈다)
```



## 종료 코드

> 시간 초과는 124, `timeout` 자체의 실패는 125, 명령을 못 돌린 경우는 126·127 이고, 그 밖에는 명령의 종료 코드를 그대로 냅니다.[^exit]

아래 예는 「실습 준비」 에서 만든 파일로 돌립니다.

```bash
# 124  시간 초과이고 --preserve-status 가 없을 때
# 125  timeout 명령 자체가 실패했을 때
# 126  명령을 찾았지만 실행할 수 없을 때
# 127  명령을 찾지 못했을 때
# 137  명령이나 timeout 자신이 KILL(9)을 받았을 때 (128+9)
# -    그 밖에는 명령의 종료 코드

# 시간이 넘으면 124 로 끝난다
timeout 1 sleep 30; echo "exit=$?"
# exit=124

# 시간 안에 끝나면 명령의 코드를 그대로 낸다
timeout 2 ./ok.sh; echo "exit=$?"
# exit=7

# 제한 시간 자리에 숫자가 아닌 것을 준다 (timeout 자체의 실패)
timeout abc sleep 1; echo "exit=$?"
```

```bash
timeout: invalid time interval 'abc'
Try 'timeout --help' for more information.
exit=125
```

```bash
# 없는 명령을 준다
timeout 1 ./nonexist; echo "exit=$?"
# timeout: failed to execute process: No such file or directory (os error 2)
# exit=127

# 실행 권한이 없는 파일을 준다. 오류 줄은 가리고 코드만 읽는다
timeout 1 ./noexec.sh 2> /dev/null; echo "exit=$?"
# exit=126
```

`137` 은 아래 「시그널을 무시하는 스크립트」 의 `-k` 예에서 재현합니다.



## 유스케이스

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 스크립트 넷이 생깁니다.

OrbStack 의 Linux VM 에서 실행합니다. 정리할 것은 `~/cmd-lab/timeout` 폴더입니다.

```bash
mkdir -p ~/cmd-lab/timeout && cd ~/cmd-lab/timeout

# trap.sh: TERM 을 잡아 메시지를 남기고 종료 코드 3 으로 끝난다
#          (시그널을 잡는 스크립트, 원래 종료 코드 보존)
cat > trap.sh << 'EOF'
#!/usr/bin/env bash
trap 'echo "SIGTERM 받음, 정리 후 종료"; exit 3' TERM
sleep 30 & wait
EOF

# ign.sh: TERM 을 무시하고 계속 돈다 (시그널을 무시하는 스크립트, 보낸 시그널 보기)
cat > ign.sh << 'EOF'
#!/usr/bin/env bash
trap '' TERM
while true; do sleep 1; done
EOF

# ok.sh: 종료 코드 7 로 바로 끝난다 (종료 코드)
printf '#!/usr/bin/env bash\nexit 7\n' > ok.sh

# noexec.sh: 실행 권한이 없는 빈 파일이다 (종료 코드)
touch noexec.sh

chmod +x trap.sh ign.sh ok.sh
```

### 시간이 넘으면 끊기

> 제한 시간 안에 끝나지 않으면 `timeout` 이 TERM 을 보내고 124 로 끝납니다.

```bash
# 1초 제한 안에 끝나지 않는 sleep 을 끊는다
timeout 1 sleep 30; echo "exit=$?"
# exit=124

# 제한보다 일찍 끝나면 명령의 코드를 그대로 낸다
timeout 2 sleep 0.2; echo "exit=$?"
# exit=0
```

### 지속 시간 쓰기

> 제한 시간에는 소수와 `m`·`h`·`d` 접미사를 쓸 수 있고, 0 은 제한을 끕니다.

```bash
# 소수로 0.5초를 준다
timeout 0.5 sleep 30; echo "exit=$?"
# exit=124

# 접미사 m 은 분이다. 1분 안에 끝나므로 0 이다
timeout 1m sleep 0.1; echo "exit=$?"
# exit=0

# 0 은 시간 초과를 끈다. 1.5초 걸리는 명령이 그대로 끝난다
timeout 0 sleep 1.5; echo "exit=$?"
# exit=0
```

### 시그널 정하기

> `-s` 로 만료 때 보낼 시그널을 TERM 이 아닌 것으로 바꿉니다.

```bash
# TERM 대신 HUP 을 보낸다. sleep 은 HUP 에도 죽는다
#   -s   만료 때 보낼 시그널 (이름이나 번호, --signal)
timeout -s HUP 1 sleep 30; echo "exit=$?"
# exit=124
```

### 시그널을 잡는 스크립트

> TERM 을 잡는 스크립트는 핸들러를 돌린 뒤 끝나지만 `timeout` 은 여전히 124 를 냅니다.

```bash
# trap.sh 는 TERM 을 받으면 메시지를 남기고 종료 코드 3 으로 끝난다
timeout 1 ./trap.sh; echo "exit=$?"
# SIGTERM 받음, 정리 후 종료
# exit=124
```

스크립트가 낸 3 은 아래 「원래 종료 코드 보존」 에서 봅니다.

### 원래 종료 코드 보존

> `-p` 를 주면 시간이 넘어도 124 가 아니라 명령이 낸 코드를 그대로 돌려줍니다.

```bash
# 시간이 넘어도 명령 자신의 종료 코드를 낸다. trap.sh 가 낸 3 이 나온다
#   -p   시간 초과여도 명령의 종료 코드로 끝난다 (--preserve-status)
timeout -p 1 ./trap.sh; echo "exit=$?"
# SIGTERM 받음, 정리 후 종료
# exit=3

# 시그널에 죽은 명령은 128+시그널 번호다. TERM(15)로 죽었으므로 143 이 나온다
timeout -p 1 sleep 30; echo "exit=$?"
# exit=143
```

### 시그널을 무시하는 스크립트

> TERM 을 무시하는 명령에는 `timeout` 이 끝나지 않으므로 `-k` 로 유예 뒤 KILL 을 보냅니다.

```bash
# ign.sh 는 TERM 을 무시한다. 1초 제한을 걸어 두고 뒤에서 돌린다
timeout 1 ./ign.sh &
# [1] 70774

# 3초 뒤에도 살아 있는지 센다. 1 이면 아직 돈다
#   pgrep -fc   명령줄 전체로 찾아 맞은 프로세스 수만 찍는다
sleep 3; pgrep -fc 'bash ./ign.sh'
# 1

# 살아 있는 스크립트를 KILL 로 끝내고 뒤의 작업을 거둔다
pkill -9 -f 'bash ./ign.sh'; wait
# [1]+  Exit 124                   timeout 1 ./ign.sh
```

`[1]` 줄은 대화형 셸이 찍는 작업 번호와 PID 이고, PID 는 실행마다 달라집니다. 스크립트를 `pkill` 로 끝냈어도 시간은 이미 넘었으므로 `timeout` 은 124 로 끝납니다.

```bash
# 첫 시그널 1초 뒤에도 살아 있으면 KILL 을 보낸다. 137 로 끝난다
#   -k   첫 시그널 뒤 이만큼 지나도 살아 있으면 KILL 도 보낸다 (--kill-after)
timeout -k 1 1 ./ign.sh; echo "exit=$?"
# exit=137
```

`timeout 1` 이 TERM 을 보낸 직후에는 살아 있고, `-k 1` 이 1초 뒤 KILL 을 보내 끝냅니다. 그래서 위 명령은 2초쯤 걸립니다.

### 보낸 시그널 보기

> `-v` 는 시간 초과로 시그널을 보낼 때마다 stderr 에 한 줄씩 남깁니다.

```bash
# TERM 을 보낸 줄이 나온다
#   -v   시간 초과로 보낸 시그널을 stderr 로 알린다 (--verbose)
timeout -v 1 sleep 30; echo "exit=$?"
# timeout: sending signal TERM to command 'sleep'
# exit=124
```

```bash
# TERM 에 이어 KILL 까지 보낸 줄이 나온다
timeout -v -k 1 1 ./ign.sh; echo "exit=$?"
```

```bash
timeout: sending signal TERM to command './ign.sh'
timeout: sending signal KILL to command './ign.sh'
exit=137
```

위 출력은 uutils 입니다. GNU 판은 줄 머리가 `gnutimeout:` 이고 명령 이름을 `‘sleep’` 처럼 굽은 따옴표로 감쌉니다.

### 자식까지 끊기와 --foreground

> 기본은 명령이 낳은 자식까지 함께 끊고, `-f` 를 주면 명령 자신만 끊습니다.

```bash
# 기본: bash 와 그 자식 sleep 이 모두 끊긴다. 남은 sleep 이 0 이다
timeout 1 bash -c 'sleep 33 & wait'
echo "exit=$? 남은 sleep=$(pgrep -fc 'sleep 33$')"
# exit=124 남은 sleep=0

# -f: 자식은 시간 초과 대상에서 빠진다. 남은 sleep 이 1 이다
#   -f   자식은 시간 초과 대상에서 빼고, 명령이 TTY 를 읽고 TTY 시그널을 받게 한다
#        (--foreground)
timeout -f 1 bash -c 'sleep 33 & wait'
echo "exit=$? 남은 sleep=$(pgrep -fc 'sleep 33$')"
# exit=124 남은 sleep=1

# 남은 sleep 을 지운다
pkill -f 'sleep 33$'
```

`-f` 는 `timeout` 을 셸 프롬프트에서 직접 돌리지 않을 때(다른 스크립트 안에서 TTY 를 읽는 명령에 걸 때) 쓰는 옵션입니다.[^opts]

### 스크립트에서 시간 초과 가르기

> 종료 코드 124 를 보면 시간 초과와 명령 자신의 실패를 나눌 수 있고, 파이프 앞에 두면 `PIPESTATUS` 로 읽습니다.

```bash
# 124 면 시간 초과, 아니면 명령이 낸 코드로 갈라 말한다
timeout 1 sleep 30; rc=$?
if [ "$rc" -eq 124 ]; then echo "시간 초과"; else echo "명령 종료 코드 $rc"; fi
# 시간 초과

# 파이프 앞에서도 124 를 읽을 수 있다 (bash 의 PIPESTATUS)
timeout 1 sleep 30 | cat; echo "exit=${PIPESTATUS[0]}"
# Terminated                 timeout 1 sleep 30 | cat
# exit=124
```

`Terminated` 줄은 파이프 뒤의 `cat` 도 TERM 을 받아 끝났다고 셸이 알리는 줄입니다(「파이프 뒤 명령도 받는 TERM」).

### 조건이 설 때까지 기다리기

> 조건이 설 때까지 도는 반복문에 `timeout` 을 걸면 조건이 끝내 서지 않을 때 124 로 빠져나옵니다.

```bash
# 1초 뒤에 ready 파일을 만드는 작업을 뒤에서 돌린다
(sleep 1; touch ready) &
# [1] 71352

# ready 가 생길 때까지 0.2초마다 본다. 5초 안에 생겨 0 이다
timeout 5 bash -c 'until [ -e ready ]; do sleep 0.2; done'; echo "exit=$?"
# [1]+  Done                       ( sleep 1; touch ready )
# exit=0

# 파일을 지우고 1초만 기다린다. 끝내 생기지 않아 124 다
rm ready
timeout 1 bash -c 'until [ -e ready ]; do sleep 0.2; done'; echo "exit=$?"
# exit=124
```

### 실습 정리

```bash
# 실습 폴더를 지운다
cd ~ && rm -rf ~/cmd-lab/timeout
```



## 주의사항과 동작 원리

### uutils 와 GNU 의 -s KILL 종료 코드

> `-s KILL` 로 끊으면 uutils 의 `timeout` 은 124, GNU 의 `gnutimeout` 은 137 을 냅니다.

```bash
# uutils: 124 를 낸다
timeout -s KILL 1 sleep 30; echo "exit=$?"
# exit=124

# GNU: 자신도 KILL 로 끝나므로 137 이다. 셸이 Killed 줄을 함께 찍는다
gnutimeout -s KILL 1 sleep 30; echo "exit=$?"
# Killed                     gnutimeout -s KILL 1 sleep 30
# exit=137

# 두 구현이 같은 값을 내게 하려면 -p 를 준다
timeout -p -s KILL 1 sleep 30; echo "exit=$?"
gnutimeout -p -s KILL 1 sleep 30; echo "exit=$?"
```

```bash
exit=137
Killed                     gnutimeout -p -s KILL 1 sleep 30
exit=137
```

책 노트의 `timeout -s KILL 1 sleep 10` → 137 은 GNU 판의 값입니다. 다른 시그널(`-s HUP`)과 `-k` 의 137 은 두 구현이 같습니다.[^impl]

### 137·143 이 명령 자신의 시그널일 때

> 시그널로 죽은 명령은 128+n 을 내므로 `timeout` 이 보낸 KILL 과 명령이 스스로 받은 KILL 을 코드로는 가를 수 없습니다.

```bash
# timeout 이 아무것도 보내지 않았는데도 명령이 KILL 로 죽으면 137 이다
timeout 5 bash -c 'kill -9 $$'; echo "exit=$?"
# Killed                     timeout 5 bash -c 'kill -9 $$'
# exit=137

# TERM 으로 죽으면 143 이다
timeout 5 bash -c 'kill -TERM $$'; echo "exit=$?"
# Terminated                 timeout 5 bash -c 'kill -TERM $$'
# exit=143
```

제한 시간 안에 끝났는데 137·143 이 나오면 시간 초과가 아니라 명령이 시그널을 받은 것입니다. 시간 초과는 124 로만 알리고, `-p` 를 주면 이 구분이 사라집니다.

### 파이프 뒤 명령도 받는 TERM

> 대화형 셸에서 `timeout` 을 파이프 앞에 두면 시간 초과 때 파이프 뒤의 명령도 TERM 을 받아 함께 끝납니다.

```bash
# 대화형 셸에서 두 명령의 종료 코드를 다 본다. cat 도 TERM 에 죽어 143 이다
timeout 1 sleep 30 | cat; echo "exit=${PIPESTATUS[*]}"
# Terminated                 timeout 1 sleep 30 | cat
# exit=124 143

# 같은 줄을 bash -c 로 돌리면 cat 은 0 으로 끝난다
bash -c 'timeout 1 sleep 30 | cat; echo "exit=${PIPESTATUS[*]}"'
# exit=124 0
```

대화형 셸에서는 `cat` 이 `timeout` 과 같은 프로세스 그룹에 들고 `bash -c` 에서는 따로 듭니다. 두 구현이 같고, 매뉴얼에 없는 이 시트의 실측(`ps -o pid,pgid`)입니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [kill·pgrep·pkill·killall 참조 시트](../process/kill·pgrep·killall.md) — 이미 도는 프로세스에 시그널을 보내는 `kill`·`pkill`
- [nohup·disown·setsid 셸을 닫은 뒤에도 돌리기](../process/nohup·disown·setsid.md) — 터미널을 닫아도 살아남는 명령과 시그널 차단
- [flock 참조 시트](./flock.md) — `-n`·`-w` 로 기다릴 시간을 정하는 락 명령
- [netstat 참조 시트](../net/netstat.md) — `-c` 처럼 끝나지 않는 출력을 `timeout` 으로 끊는 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [시그널은 번호 하나만 보내고 끝나는 모양은 처리 방식이 정한다](../../../book/learning-modern-linux/09-02.%EC%8B%9C%EA%B7%B8%EB%84%90%EC%9D%80%20%EB%B2%88%ED%98%B8%20%ED%95%98%EB%82%98%EB%A7%8C%20%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EB%81%9D%EB%82%98%EB%8A%94%20%EB%AA%A8%EC%96%91%EC%9D%80%20%EC%B2%98%EB%A6%AC%20%EB%B0%A9%EC%8B%9D%EC%9D%B4%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) — 「kill·pkill·timeout 비교」 절과 128+n 종료 코드



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04 LTS — 2026-11-16 실측
- 패키지: rust-coreutils 0.10.0-1ubuntu2~26.04.1(`timeout`), gnu-coreutils 9.7-3ubuntu2.1(`gnutimeout`)
- [timeout(1) — Ubuntu 26.04 (rust-coreutils)](https://manpages.ubuntu.com/manpages/resolute/en/man1/timeout.1.html)
- [gnutimeout(1) — Ubuntu 26.04 (gnu-coreutils)](https://manpages.ubuntu.com/manpages/resolute/en/man1/gnutimeout.1.html)

[^impl]: `man timeout` (rust-coreutils 0.10.0) — "Start COMMAND, and kill it if still running after DURATION." 이 페이지의 "Provided by: rust-coreutils (Version: 0.10.0-1ubuntu2~26.04.1)" 와 `man gnutimeout` 페이지의 "Provided by: gnu-coreutils (Version: 9.7-3ubuntu2.1)" 가 두 구현을 가릅니다. `-s KILL` 의 종료 코드 차이는 두 매뉴얼에 적혀 있지 않고 이 시트의 실측입니다. <https://manpages.ubuntu.com/manpages/resolute/en/man1/timeout.1.html> · <https://manpages.ubuntu.com/manpages/resolute/en/man1/gnutimeout.1.html>
[^exit]: `timeout --help` 와 `man gnutimeout` (GNU coreutils 9.7) Exit status — "124 if COMMAND times out, and --preserve-status is not specified", "125 if the timeout command itself fails", "126 if COMMAND is found but cannot be invoked", "127 if COMMAND cannot be found", "137 if COMMAND (or timeout itself) is sent the KILL (9) signal (128+9)", "- the exit status of COMMAND otherwise". 같은 목록이 uutils 의 `timeout --help` 에도 있고, uutils 의 man 페이지는 EXIT STATUS 절 없이 이 목록을 EXTRA 절에 둡니다. <https://manpages.ubuntu.com/manpages/resolute/en/man1/gnutimeout.1.html> · <https://manpages.ubuntu.com/manpages/resolute/en/man1/timeout.1.html>
[^opts]: `man gnutimeout` (GNU coreutils 9.7) — `-f` "when not running timeout directly from a shell prompt, allow COMMAND to read from the TTY and get TTY signals; in this mode, children of COMMAND will not be timed out", `-k` "also send a KILL signal if COMMAND is still running this long after the initial signal was sent", `-p` "exit with the same status as COMMAND, even when the command times out", `-s` "specify the signal to be sent on timeout; SIGNAL may be a name like 'HUP' or a number; see 'kill -l' for a list of signals", `-v` "diagnose to stderr any signal sent upon timeout", "DURATION is a floating point number with an optional suffix: 's' for seconds (the default), 'm' for minutes, 'h' for hours or 'd' for days. A duration of 0 disables the associated timeout." <https://manpages.ubuntu.com/manpages/resolute/en/man1/gnutimeout.1.html>
