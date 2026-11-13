---
title: flock 참조 시트
tags: [linux, cheatsheet, flock, lock, shell, cron, cli, reference]
status: draft
source:
  - util-linux flock(1) (OrbStack Ubuntu 26.04 VM 의 `flock --help`·`man flock` 원문, util-linux 2.41.3)
  - 《Learning Modern Linux》 3장 "Shells and Scripting"(Michael Hausenblas, O'Reilly, 2022)의 `flock -n` 예
related:
  - ../README.md
  - ../../../book/learning-modern-linux/03-03.bash%20는%20조용히%20실패하므로%20시끄럽게%20만들어야%20한다.md
updated: 2026-11-13
---

# flock 참조 시트

---

> 같은 락 파일을 쓰는 프로세스를 하나만 돌게 하는 `flock` 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `flock` 은 락 파일에 락을 걸고, 락을 쥔 동안만 명령을 돌립니다.

util-linux 패키지의 외부 바이너리(`/usr/bin/flock`)입니다. 이 시트를 쓴 Mac 에는 없어서 OrbStack Ubuntu 26.04 VM(util-linux 2.41.3)으로 실측했습니다. 락을 못 잡았을 때 기본 동작은 기다림입니다.[^flock-man]



## 핵심 문법

> 락 파일을 정하고, 락을 못 잡았을 때 기다릴지 포기할지를 옵션으로 정합니다.

```bash
# 호출 형태 (flock --help 의 Usage)
flock [options] <file>|<directory> <command> [<argument>...]
flock [options] <file>|<directory> -c <command>
flock [options] <file descriptor number>

# 락을 쥐고 명령을 돌린다. 락이 잡혀 있으면 풀릴 때까지 기다린다 (락이 잡혀 있을 때의 옵션 차이)
flock 락파일 명령

# 정한 초만 기다리고 실패한다
flock -w 초 락파일 명령

# 기다리지 않고 실패한다
flock -n 락파일 명령

# 실패했을 때의 종료 코드를 바꾼다
flock -n -E 코드 락파일 명령

# 스크립트 첫머리에서 락을 걸어 중복 실행을 막는다 (스크립트 안에서 중복 실행 막기)
exec 200> 락파일
flock -n 200 || exit 1
```



## 종료 코드

> 명령이 돌았으면 그 명령의 종료 코드를 내고, 락을 못 잡았을 때와 명령을 실행하지 못했을 때는 `flock` 이 따로 정한 코드를 냅니다.[^flock-exit]

```bash
# (명령의 코드)  명령이 돌았으면 그 코드를 그대로 낸다
# 1             -n 이나 -w 가 락을 못 잡고 실패한 경우. -E 로 바꿀 수 있다. 재현은 「락이 잡혀 있을 때의 옵션 차이」 를 본다
# 69            명령을 실행하지 못한 경우. 매뉴얼은 sysexits.h 의 값을 쓴다고만 적고 69 는 이 시트의 실측이다

# 없는 명령을 준 경우 (「실습 준비」 의 폴더에서 돌린 값이다)
flock cmd-lab.lock nonexistent-cmd; echo $?    # flock: failed to execute nonexistent-cmd: No such file or directory / 69
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 폴더와 도우미 함수가 생깁니다.

OrbStack 의 Linux VM 에서 실행합니다. 정리할 것은 `~/cmd-lab/flock` 폴더와 `/tmp` 의 락 파일 하나입니다.

```bash
mkdir -p ~/cmd-lab/flock && cd ~/cmd-lab/flock

# hold N: 락 파일을 N초 쥔 프로세스를 뒤에서 띄운다. 0.3초는 그 프로세스가 락을 쥘 때까지 주는 시간이다
hold() { flock cmd-lab.lock sleep "$1" & sleep 0.3; }

# time 이 찍는 형식을 걸린 초 한 줄로 줄인다
TIMEFORMAT='%1R초'
```

### 락이 잡혀 있을 때의 옵션 차이

> 락이 잡혀 있으면 옵션 없는 `flock` 은 풀릴 때까지 기다리고, `-w` 는 정한 초만 기다리고, `-n` 은 한 번도 기다리지 않습니다.

`-n` 은 "그만큼 기다리고 포기" 가 아니라 기다림 자체를 하지 않는 옵션입니다. 아래는 `hold 5` 로 5초짜리 락을 잡아 둔 채 각 옵션을 걸어 본 결과입니다.[^flock-nw]

```bash
# 옵션 없이 건다. 락이 풀릴 때까지 기다렸다가 명령을 돌린다
hold 5; time flock cmd-lab.lock echo got-lock; echo "exit=$?"; wait
# got-lock / 4.7초 / exit=0

# -w 는 정한 초만 기다리고 실패한다
#   -w   락을 못 잡으면 이 초 안에서 기다리다 실패한다 (--timeout). 소수도 받는다
hold 5; time flock -w 2 cmd-lab.lock echo got-lock; echo "exit=$?"; wait
# 2.0초 / exit=1

# -n 은 기다리지 않고 바로 실패한다
#   -n   기다리지 않고 실패한다 (--nonblock)
hold 5; time flock -n cmd-lab.lock echo got-lock; echo "exit=$?"; wait
# 0.0초 / exit=1

# -w 0 은 -n 과 같은 뜻이다
hold 5; time flock -w 0 cmd-lab.lock echo got-lock; echo "exit=$?"; wait
# 0.0초 / exit=1

# 락을 못 잡았을 때의 종료 코드를 바꾼다
#   -E   락을 못 잡았을 때의 종료 코드 (--conflict-exit-code). 기본은 1
hold 5; time flock -n -E 99 cmd-lab.lock echo got-lock; echo "exit=$?"; wait
# 0.0초 / exit=99
```

첫 줄의 4.7초는 `hold` 가 락을 쥔 뒤 0.3초를 보낸 값이라 5초에서 그만큼 줄어든 것입니다.

### 스크립트 안에서 중복 실행 막기

> 스크립트 첫머리에서 락을 걸면 같은 스크립트를 두 번 띄울 때 뒤에 온 쪽만 메시지를 남기고 끝납니다.

락 파일은 일부러 `/tmp` 에 둡니다. 스크립트가 끝나면 그 스크립트가 쥔 락도 함께 풀립니다.

```bash
# 200 번 파일 디스크립터로 락 파일을 열고 그 번호에 락을 건다. 못 잡으면 메시지를 남기고 종료 코드 1 로 끝난다
cat > backup.sh << 'EOF'
#!/usr/bin/env bash
exec 200> /tmp/cmd-lab-backup.lock
flock -n 200 || { echo "이미 다른 백업 작업이 실행 중입니다." >&2; exit 1; }
sleep 3
echo "백업 끝"
EOF
chmod +x backup.sh
```

```bash
# 첫 실행이 락을 쥔 동안 두 번째를 띄운다
./backup.sh & sleep 0.5; ./backup.sh; echo "exit=$?"; wait
# 이미 다른 백업 작업이 실행 중입니다. / exit=1 / 백업 끝

# 첫 실행이 끝나면 락도 풀려서 다시 돌 수 있다
./backup.sh; echo "exit=$?"
# 백업 끝 / exit=0
```

### 주기 실행이 겹칠 때

> 3초 걸리는 작업을 1초마다 띄우면 `-n` 은 겹친 회차를 버리고, 옵션 없는 `flock` 은 회차마다 늦어지는 줄을 세웁니다.

cron 처럼 같은 작업을 주기로 띄우는 쪽을 흉내 낸 함수입니다. 작업이 간격보다 길면 기다리는 프로세스가 회차마다 하나씩 쌓입니다.

```bash
# run5 [flock 옵션]: 3초 작업을 락 아래에서 1초 간격으로 5번 띄운다
# 회차마다 끝난 시각이나 포기한 시각을 찍고, 5번째를 띄운 직후 flock 프로세스 수를 센다
# 인자 없이 부르면 옵션 없이 건다
run5() {
  local t0=$SECONDS n
  for n in 1 2 3 4 5; do
    ( flock $1 cmd-lab.lock sleep 3 \
        && echo "t=$((SECONDS - t0)) 회차 $n 끝" \
        || echo "t=$((SECONDS - t0)) 회차 $n 포기" ) &
    sleep 1
  done
  echo "t=$((SECONDS - t0)) flock 프로세스 $(pgrep -c -x flock)개"
  wait
}

run5 -n
```

```bash
t=1 회차 2 포기
t=2 회차 3 포기
t=3 회차 1 끝
t=4 회차 5 포기
t=5 flock 프로세스 1개
t=6 회차 4 끝
```

```bash
run5
```

```bash
t=3 회차 1 끝
t=5 flock 프로세스 4개
t=6 회차 2 끝
t=9 회차 3 끝
t=12 회차 4 끝
t=15 회차 5 끝
```

`-n` 은 1·4회차만 돌고 나머지 셋을 버립니다. 옵션 없는 쪽은 5회차를 모두 돌지만 끝나는 시각이 3초씩 밀리고, t=5 의 프로세스 넷은 락을 쥔 하나와 기다리는 셋입니다.

### 실습 정리

```bash
cd ~ && rm -rf ~/cmd-lab/flock /tmp/cmd-lab-backup.lock
unset -f hold run5
unset TIMEFORMAT
```



## 관련 문서

> 이 시트를 쓰는 책 노트와 이어지는 시트입니다.

- [bash 는 조용히 실패하므로 시끄럽게 만들어야 한다](../../../book/learning-modern-linux/03-03.bash%20는%20조용히%20실패하므로%20시끄럽게%20만들어야%20한다.md) — 포기와 기다림 가운데 무엇을 고르는지, 중복 실행을 막아야 하는 이유
- [crontab 참조 시트](./crontab.md) — 주기 실행을 등록하는 법
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04 VM, util-linux 2.41.3, bash 5.3.9
- [flock(1)](https://man7.org/linux/man-pages/man1/flock.1.html) — 2026-11-13 조회
- 원서: 《Learning Modern Linux》 3장 Shells and Scripting (Michael Hausenblas, O'Reilly, 2022년) — `flock -n` 으로 중복 실행을 막는 예

[^flock-man]: flock(1) DESCRIPTION — "By default, if the lock cannot be immediately acquired, flock waits until the lock is available." <https://man7.org/linux/man-pages/man1/flock.1.html>
[^flock-nw]: flock(1) OPTIONS — `-n` "Fail rather than wait if the lock cannot be immediately acquired. See the -E option for the exit status used." `-w` "Fail if the lock cannot be acquired within seconds. Decimal fractional values are allowed. See the -E option for the exit status used. The zero number of seconds is interpreted as --nonblock." <https://man7.org/linux/man-pages/man1/flock.1.html>
[^flock-exit]: flock(1) EXIT STATUS — "The command uses <sysexits.h> exit status values for everything, except when using either of the options -n or -w which report a failure to acquire the lock with an exit status given by the -E option, or 1 by default." "When using the command variant, and executing the child worked, then the exit status is that of the child command." <https://man7.org/linux/man-pages/man1/flock.1.html>
