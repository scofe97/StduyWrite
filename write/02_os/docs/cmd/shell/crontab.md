---
title: crontab 참조 시트
tags: [linux, cheatsheet, crontab, cron, schedule, shell, cli, reference]
status: draft
source:
  - crontab(1)·crontab(5) (Debian bookworm cron 3.0pl1-162, manpages.debian.org)
  - 《Learning Modern Linux》 3장 "Shells and Scripting"(Michael Hausenblas, O'Reilly, 2022)의 cron 예
related:
  - ../README.md
  - ./flock.md
  - ../../../book/learning-modern-linux/03-03.bash%20는%20조용히%20실패하므로%20시끄럽게%20만들어야%20한다.md
updated: 2026-11-13
---

# crontab 참조 시트

---

> 시각을 정해 명령을 돌리는 예약 표를 등록하고 확인하는 `crontab` 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `crontab` 은 사용자별 예약 표를 등록하고 보고 지우는 명령이고, 표를 읽어 시각이 맞는 줄을 돌리는 쪽은 cron 데몬입니다.

cron 패키지의 외부 바이너리(`/usr/bin/crontab`)이며 표의 줄을 매분 살피는 것은 `cron` 데몬입니다.[^crontab-man] 이 시트는 Debian 12 컨테이너(cron 3.0pl1-162)로 실측했습니다. cron 이 주는 `PATH` 는 배포판마다 달라서 Ubuntu 26.04 VM 의 값을 「배포판마다 다른 cron 의 PATH」 에 따로 실었습니다.



## 핵심 문법

> 표의 한 줄은 시각 다섯 칸과 명령이고, 환경은 표 첫머리의 `이름=값` 줄로 정합니다.

```bash
# 호출 형태 (crontab -h 의 Usage)
crontab [-u user] [-n] file
crontab [ -u user ] [ -i ] { -e | -l | -r }

# 예약 한 줄의 모양. 앞 다섯 칸이 시각이고 나머지가 명령이다 (예약 표 등록하고 읽기)
분 시 일 월 요일 명령

# 파일에 쓴 표를 내 crontab 으로 통째로 등록한다
crontab 파일

# 등록된 표를 보고 지운다
crontab -l
crontab -r

# 명령의 출력을 파일에 쌓는다. 표준 오류까지 같은 파일로 보낸다 (cron 이 주는 환경과 오류 출력 남기기)
분 시 일 월 요일 명령 >> 로그 2>&1

# 표 첫머리에서 환경을 정한다 (cron 이 주는 환경과 오류 출력 남기기)
이름=값
```

### 시각 다섯 칸

> 칸은 분·시·일·월·요일 순서이고, 일과 월의 범위는 crontab(5) 표가 0 부터 적지만 cron 소스는 1 부터 받습니다.[^cron-fields]

```bash
# 칸마다 허용 값. 범위는 cron 소스(cron.h)의 정의다
# 분      0-59
# 시      0-23
# 일      1-31 (매뉴얼 표는 0-31)
# 월      1-12 (매뉴얼 표는 0-12, 이름도 된다)
# 요일    0-7 (0 과 7 이 일요일, 이름도 된다)
# *       칸이 받는 값 전체. 매뉴얼은 first-last 라고 적는다
# 등록이 된다고 범위가 맞는 것은 아니다. 0 0 32 * * /usr/bin/true 도 crontab 이 받았다(실측)
```



## 종료 코드

> `crontab` 의 매뉴얼에는 종료 상태 절이 없고, 아래 값은 이 시트의 실측입니다.[^crontab-exit]

```bash
# 0   등록·조회·삭제가 됐을 때
# 1   등록된 표가 없는데 -l 을 줬을 때
crontab -l; echo $?    # no crontab for root / 1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Debian 12 컨테이너에 한 번 붙여 넣으면 cron 데몬이 뜨고 예가 돌릴 스크립트가 생깁니다.

`docker run -it --rm debian:12` 안에서 실행합니다. 컨테이너는 root 라 sudo 없이 치고, 컨테이너를 나가면 `cron` 데몬도 함께 사라집니다.

```bash
apt-get update -qq && apt-get install -y -qq cron

# cron 데몬을 띄운다. 표를 매분 살피는 쪽이다
cron

mkdir -p ~/cmd-lab/crontab && cd ~/cmd-lab/crontab

# 예가 돌릴 스크립트. /usr/local/bin 에 둔다
printf '#!/bin/sh\necho hello from cron\n' > /usr/local/bin/cmd-lab-hello
chmod +x /usr/local/bin/cmd-lab-hello
```

### 예약 표 등록하고 읽기

> 표의 한 줄은 시각 다섯 칸 뒤에 명령을 씁니다. 파일로 쓴 표를 `crontab 파일` 로 등록합니다.

```bash
# 예약 한 줄을 파일에 쓴다. 분 30, 시 2, 나머지 칸은 * 라서 매일 02:30 이다
echo '30 2 * * * /usr/local/bin/cmd-lab-hello' > daily.cron

# 파일의 내용으로 내 crontab 을 통째로 바꾼다
crontab daily.cron

# 등록된 표를 본다
#   -l   현재 crontab 을 표준 출력으로 보인다
crontab -l    # 30 2 * * * /usr/local/bin/cmd-lab-hello

# 표를 지운다. 지운 뒤에는 표가 없다고 답한다
#   -r   현재 crontab 을 지운다
crontab -r
crontab -l    # no crontab for root
```

### cron 이 주는 환경과 오류 출력 남기기

> cron 이 돌리는 작업은 터미널과 다른 환경을 받으므로, 환경을 파일로 떠 보고 오류까지 한 파일에 쌓아 두어야 실패가 보입니다.

한 줄은 환경을 `env.txt` 에 뜨고, 둘째·셋째 줄은 같은 스크립트를 이름만 써서, 그리고 절대 경로로 돌려 로그에 쌓습니다. 표를 등록하고 1분이 지나야 결과 파일이 생깁니다.

```bash
cat > env.cron << 'EOF'
* * * * * /usr/bin/env | sort > $HOME/cmd-lab/crontab/env.txt
* * * * * cmd-lab-hello >> $HOME/cmd-lab/crontab/bare.log 2>&1
* * * * * /usr/local/bin/cmd-lab-hello >> $HOME/cmd-lab/crontab/abs.log 2>&1
EOF

crontab env.cron
sleep 70
```

```bash
# cron 이 작업에 준 환경이다
cat env.txt
```

```bash
HOME=/root
LOGNAME=root
PATH=/usr/bin:/bin
PWD=/root
SHELL=/bin/sh
```

```bash
# 이름만 쓴 쪽은 PATH 에서 못 찾는다. >> 로그 2>&1 덕에 그 오류 메시지가 파일에 남는다
cat bare.log    # /bin/sh: 1: cmd-lab-hello: not found

# 절대 경로로 쓴 쪽은 돈다
cat abs.log     # hello from cron
```

표 첫머리에서 `PATH` 를 다시 정하면 이름만 써도 찾습니다.

```bash
cat > fixed.cron << 'EOF'
PATH=/usr/local/bin:/usr/bin:/bin
* * * * * cmd-lab-hello >> $HOME/cmd-lab/crontab/fixed.log 2>&1
EOF

crontab fixed.cron
sleep 70
cat fixed.log    # hello from cron
```

### 실습 정리

```bash
crontab -r
rm -rf ~/cmd-lab/crontab /usr/local/bin/cmd-lab-hello
```



## 주의사항과 동작 원리

### 배포판마다 다른 cron 의 PATH

> 같은 표를 Ubuntu 26.04 VM 에 등록하면 `PATH` 가 Debian 12 보다 훨씬 넓어서, 이름만 쓴 명령이 터미널과 같이 돕니다.

매뉴얼은 `SHELL`·`LOGNAME`·`HOME` 만 약속하고 `PATH` 값은 정하지 않으므로 이 값은 배포판 몫입니다.[^cron-env] 아래는 환경을 뜨는 표를 VM(cron 3.0pl1-200ubuntu1)에 등록해 받은 `PATH` 와 `SHELL` 입니다. `PATH` 는 이 VM 의 `/etc/environment` 와 같은 값입니다.

```bash
mkdir -p ~/cmd-lab/crontab && cd ~/cmd-lab/crontab
echo '* * * * * /usr/bin/env | sort > $HOME/cmd-lab/crontab/env.txt' \
  > env-only.cron
crontab env-only.cron
sleep 70

# PATH 와 SHELL 줄만 본다
grep -E '^(PATH|SHELL)=' env.txt
```

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
SHELL=/bin/sh
```

```bash
# 같은 값이 /etc/environment 에 있다
grep ^PATH /etc/environment    # PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

# /etc/pam.d/cron 이 그 파일을 읽는다
sed -n 8,10p /etc/pam.d/cron
```

```bash
# Read environment variables from pam_env's default files, /etc/environment
# and /etc/security/pam_env.conf.
session       required   pam_env.so
```

```bash
# VM 에 등록한 표를 지운다
crontab -r
rm -rf ~/cmd-lab/crontab
```



## 관련 문서

> 이 시트를 쓰는 책 노트와 이어지는 시트입니다.

- [bash 는 조용히 실패하므로 시끄럽게 만들어야 한다](../../../book/learning-modern-linux/03-03.bash%20는%20조용히%20실패하므로%20시끄럽게%20만들어야%20한다.md) — cron 의 최소 환경이 조용한 실패를 만드는 이유와 최소 실행 계약
- [flock 참조 시트](./flock.md) — 주기 작업이 겹치지 않게 막는 법
- [systemctl 참조 시트](../service/systemctl.md) — cron 대신 쓰는 systemd 타이머의 `list-timers`
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: Debian 12 컨테이너(cron 3.0pl1-162), OrbStack Ubuntu 26.04 VM(cron 3.0pl1-200ubuntu1)
- [crontab(1)](https://manpages.debian.org/bookworm/cron/crontab.1.en.html) · [crontab(5)](https://manpages.debian.org/bookworm/cron/crontab.5.en.html) — Debian bookworm 판, 2026-11-13 조회
- 원서: 《Learning Modern Linux》 3장 Shells and Scripting (Michael Hausenblas, O'Reilly, 2022년) — 매일 02:30 에 로그를 남기며 돌리는 crontab 예

[^crontab-man]: crontab(1) (Debian bookworm, cron 3.0pl1-162) — "crontab is the program used to install, deinstall or list the tables used to drive the cron(8) daemon in Vixie Cron." "The -l option causes the current crontab to be displayed on standard output." "The -r option causes the current crontab to be removed." crontab(5) — "cron(8) examines cron entries once every minute." <https://manpages.debian.org/bookworm/cron/crontab.1.en.html>
[^cron-fields]: crontab(5) (Debian bookworm) — "Each line has five time and date fields, followed by a user name if this is the system crontab file, followed by a command." 표는 minute 0-59, hour 0-23, day of month 0-31, month 0-12 (or names, see below), day of week 0-7 (0 or 7 is Sun, or use names) 이고, "A field may be an asterisk (*), which always stands for ``first-last''." <https://manpages.debian.org/bookworm/cron/crontab.5.en.html> 같은 판의 소스 `cron.h` 는 `FIRST_DOM 1`·`LAST_DOM 31`·`FIRST_MONTH 1`·`LAST_MONTH 12` 로 정의합니다. <https://sources.debian.org/src/cron/3.0pl1-162/cron.h/>
[^cron-env]: crontab(5) (Debian bookworm) — "Several environment variables are set up automatically by the cron(8) daemon. SHELL is set to /bin/sh, and LOGNAME and HOME are set from the /etc/passwd line of the crontab's owner." 이 문서에는 `PATH` 라는 글자가 없습니다. <https://manpages.debian.org/bookworm/cron/crontab.5.en.html>
[^crontab-exit]: crontab(1) (Debian bookworm) 에는 종료 상태를 적은 절이 없고, DIAGNOSTICS 절은 사용법 메시지와 마지막 줄의 개행을 다룹니다. 0 과 1 은 Debian 12 컨테이너의 `echo $?` 실측입니다. <https://manpages.debian.org/bookworm/cron/crontab.1.en.html>
