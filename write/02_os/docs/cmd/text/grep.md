---
title: grep 참조 시트
tags: [linux, cheatsheet, grep, zgrep, cli, reference]
status: draft
source:
  - GNU grep 매뉴얼 · zgrep(1)
related:
  - ../README.md
updated: 2026-11-13
---

# grep 참조 시트

---

> 맞은 줄을 고르는 `grep` 의 옵션을 일치 기준, 검색 대상, 출력 형식 세 묶음으로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `grep` 은 패턴에 맞는 줄을 골라 찍습니다.

옵션은 일치 기준, 검색 대상, 출력 형식 세 묶음으로 갈립니다.[^grep] grep 패키지의 외부 바이너리이며 이 시트는 GNU 판(grep 3.8, Debian 12 컨테이너)으로 실측했습니다. macOS 기본 `grep` 은 GNU 판이 아니어서 옵션과 출력이 조금 다릅니다.



## 핵심 문법

> 패턴과 파일을 주고, 옵션으로 무엇을 맞은 줄로 볼지, 어디를 읽을지, 무엇을 찍을지 정합니다.

```bash
# 호출 형태
grep [OPTION]... PATTERNS [FILE]...

# 패턴이 든 줄을 찍는다. 대소문자를 가리지 않거나 맞지 않는 줄을 고른다 (대소문자와 역일치)
grep -i 패턴 파일
grep -v 패턴 파일

# 줄 전체나 단어 하나와 같을 때만 맞게 한다 (줄 전체와 단어 단위)
grep -x 패턴 파일
grep -w 패턴 파일

# 패턴을 여럿 준다 (패턴 여러 개)
grep -e 패턴 -e 패턴 파일
grep -f 패턴파일 파일

# 패턴은 기본이 정규식이다 (정규식 기본 글자 . ^ $)
grep '정규식' 파일

# 디렉터리 아래를 읽고 파일 이름으로 좁힌다 (디렉터리 아래 읽기)
grep -r 패턴 디렉터리
grep -r --include='글롭' 패턴 디렉터리

# 맞은 줄 대신 줄 번호·개수·파일 이름을 찍는다 (줄 번호·개수·파일 이름 찍기)
grep -n 패턴 파일
grep -c 패턴 파일
grep -l 패턴 파일...
grep -L 패턴 파일...

# 맞은 부분만 찍거나 N 개에서 멈춘다 (맞은 부분만 찍고 일찍 멈추기)
grep -o 패턴 파일
grep -m 개수 패턴 파일

# 앞뒤 줄을 함께 찍는다 (앞뒤 문맥 줄 함께 찍기)
grep -A 줄수 -B 줄수 패턴 파일

# 정규식으로 주석과 빈 줄을 뺀다 (주석과 빈 줄 빼고 읽기)
grep -v -E '정규식' 파일

# 다른 명령으로 이어 센다 (로그인 실패를 출발지별로 세기)
grep 패턴 파일 | grep -o 패턴 | sort | uniq -c
```



## 종료 코드

> `grep` 은 맞는 줄이 있으면 0, 없으면 1, 오류가 나면 2 를 돌려줍니다.

매뉴얼은 세 코드와 함께 `-q` 를 줬을 때의 예외를 따로 적습니다.[^grep-exit] 아래 예는 「실습 준비」 에서 만든 `app.log` 로 돌립니다.

```bash
# 0  맞는 줄이 하나라도 있다
# 1  맞는 줄이 없다
# 2  오류가 났다. 없는 파일을 줬을 때가 그렇다

# 아무것도 찍지 않고 종료 상태만 남긴다
#   -q   표준 출력에 아무것도 쓰지 않는다 (--quiet)
grep -q heartbeat app.log; echo $?      # 0
grep -q panic app.log; echo $?          # 1

# 파일이 없으면 2 다. 오류 메시지는 그대로 나온다
grep x nofile.log; echo $?                   # grep: nofile.log: No such file or directory / 2

# 오류 메시지만 숨긴다. 종료 상태는 그대로 2 다
#   -s   없거나 읽을 수 없는 파일의 오류 메시지를 숨긴다 (--no-messages)
grep -s -q x nofile.log; echo $?        # 2

# -q 는 맞는 줄을 찾으면 오류가 있었어도 0 을 돌려준다
grep -q heartbeat nofile.log app.log; echo $?    # grep: nofile.log: No such file or directory / 0
```

위 블록의 `/` 는 여러 줄로 나온 출력을 한 줄에 줄여 적은 것입니다. 스크립트에서는 `if grep -q 패턴 파일; then …` 처럼 종료 상태로 가릅니다([《Learning Modern Linux》 3장 첫 노트](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) 4절).



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

```bash
mkdir -p ~/cmd-lab/grep && cd ~/cmd-lab/grep
cat > app.log << 'EOF'
2026-11-10 09:01:15 INFO  order-api started
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
2026-11-10 11:30:00 INFO  heartbeat
EOF
cat > sshd_config << 'EOF'
# This is the sshd server system-wide configuration file.

Port 22
#PermitRootLogin prohibit-password
PasswordAuthentication yes
  # indented comment

X11Forwarding no
EOF
cat > auth.log << 'EOF'
Nov 10 09:00:01 web1 sshd[811]: Failed password for root from 203.0.113.7 port 50122 ssh2
Nov 10 09:00:05 web1 sshd[811]: Failed password for root from 203.0.113.7 port 50122 ssh2
Nov 10 09:02:11 web1 sshd[815]: Accepted publickey for dev from 198.51.100.4 port 40210 ssh2
Nov 10 09:03:40 web1 sshd[820]: Failed password for invalid user admin from 203.0.113.9 port 51001 ssh2
EOF
mkdir -p conf
echo 'timeout=30' > conf/a.conf
echo 'timeout=30' > conf/c.txt
echo 'timeout=60' > conf/b.conf
gzip -c app.log > app.log.1.gz
printf 'ERROR\nWARN\n' > patterns.txt
```

`app.log` 는 `ERROR`·`error`·`[ERROR]` 가 섞인 일곱 줄짜리 애플리케이션 로그이고 `sshd_config` 에는 주석·빈 줄·들여 쓴 주석이 있습니다. `auth.log` 에는 SSH 로그인 실패 세 줄과 성공 한 줄이, `conf/` 에는 `timeout=30` 인 `a.conf`·`c.txt` 와 `timeout=60` 인 `b.conf` 가 있습니다.

### 대소문자와 역일치

> 기본은 대소문자를 가리고, `-i` 로 가리지 않게 하고 `-v` 로 맞지 않는 줄을 고릅니다.

```bash
# 기본: 대문자 ERROR 가 든 줄만. 소문자 error 로 적힌 줄은 걸리지 않는다
grep ERROR app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# 소문자 error 줄이 더해진다
#   -i   대소문자 구분을 없앤다 (--ignore-case)
grep -i error app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# INFO 두 줄을 뺀 다섯 줄이 나온다
#   -v   맞지 않는 줄을 고른다 (--invert-match)
grep -v INFO app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

### 줄 전체와 단어 단위

> 패턴은 기본으로 줄 안 어디에 있어도 맞고, `-x`·`-w` 는 줄 전체나 단어 하나와 같을 때만 맞게 합니다.

```bash
# 'Port 22' 는 맞고 'Port' 만으로는 맞지 않는다
#   -x   줄 전체와 일치시킨다 (--line-regexp)
grep -x 'Port 22' sshd_config      # Port 22
grep -x 'Port' sshd_config         # 출력 없음, 종료 상태 1

# errors=3 의 error 는 뒤에 s 가 붙어 빠진다
#   -w   단어 단위로 일치시킨다 (--word-regexp)
grep -w error app.log              # 2026-11-10 10:06:01 error db connection reset
```

### 패턴 여러 개

> 패턴을 여럿 주면 하나라도 맞는 줄을 고르고, 패턴이 많으면 파일에 한 줄에 하나씩 적어 읽게 합니다.

```bash
# 패턴을 하나씩 더한다
#   -e   패턴을 준다 (--regexp)
grep -e WARN -e heartbeat app.log
```

```bash
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 11:30:00 INFO  heartbeat
```

```bash
# 파일의 줄마다 패턴 하나. patterns.txt 는 ERROR 와 WARN 두 줄
#   -f   파일에서 패턴을 읽는다 (--file)
grep -f patterns.txt app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

### 정규식 기본 글자 . ^ $

> 정규식에서 자주 쓰는 글자는 셋으로, `.` 은 아무 글자 하나, `^` 는 줄 머리, `$` 는 줄 끝입니다.

```bash
# . : 아무 글자 하나. orderId=1001 과 1002 가 모두 맞는다
grep 'orderId=100.' app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

```bash
# ^ : 줄 머리에서 시작. 10시대 로그만
grep '^2026-11-10 10' app.log
```

```bash
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

### 디렉터리 아래 읽기

> `-r` 로 파일 하나 대신 디렉터리 아래를 읽게 하고, `--include`·`--exclude` 로 읽을 파일 이름을 좁힙니다.

```bash
# 디렉터리 아래를 읽으면 줄 앞에 파일 이름이 붙는다
#   -r   디렉터리 아래를 재귀로 읽는다 (--recursive)
grep -r 'timeout=30' conf
```

```bash
conf/a.conf:timeout=30
conf/c.txt:timeout=30
```

`-r` 이 찍는 파일 순서는 디렉터리를 읽는 순서라 환경마다 다를 수 있습니다. 순서가 중요하면 `sort` 를 붙입니다.

```bash
# .conf 파일만 읽어 c.txt 가 빠진다
#   --include=GLOB   이름이 GLOB 에 맞는 파일만 읽는다
grep -r --include='*.conf' 'timeout=30' conf    # conf/a.conf:timeout=30

# .conf 파일을 빼면 c.txt 만 남는다
#   --exclude=GLOB   이름이 GLOB 에 맞는 파일을 건너뛴다
grep -r --exclude='*.conf' timeout conf         # conf/c.txt:timeout=30

# -r 로 읽어도 내용만 찍는다
#   -h   줄 앞의 파일 이름을 떼어 낸다 (--no-filename)
grep -rh 'timeout=30' conf
```

```bash
timeout=30
timeout=30
```

`--include` 와 `--exclude` 의 값은 따옴표로 감쌉니다. 감싸지 않으면 셸이 `*.conf` 를 지금 폴더의 파일 이름으로 먼저 펼칩니다.

### 줄 번호·개수·파일 이름 찍기

> 맞은 줄을 통째로 보는 대신 줄 번호, 개수, 파일 이름만 찍으면 다음 명령에 넘기기 쉽습니다.

```bash
# 맞은 줄이 몇째 줄인지 함께 찍는다
#   -n   출력 줄 앞에 줄 번호를 붙인다 (--line-number)
grep -n WARN app.log                # 3:2026-11-10 09:14:41 WARN  retrying orderId=1001

# 한 줄에 두 번 맞아도 1 로 센다
#   -c   파일마다 맞은 줄 수만 찍는다 (--count)
grep -c ERROR app.log               # 3

# 파일 둘 가운데 ERROR 가 든 쪽만 고른다
#   -l   맞은 줄이 있는 파일 이름만 찍는다 (--files-with-matches)
grep -l ERROR app.log sshd_config   # app.log

# -r 과 함께 써서 timeout=30 이 하나도 없는 파일을 고른다
#   -L   맞은 줄이 없는 파일 이름만 찍는다 (--files-without-match)
grep -rL 'timeout=30' conf          # conf/b.conf
```

### 맞은 부분만 찍고 일찍 멈추기

> `-o` 는 맞은 부분만 찍고, `-m` 은 맞은 줄을 N 개 찾으면 읽기를 멈춥니다.

```bash
# 줄 전체 대신 orderId=숫자 부분만 한 줄에 하나씩 낸다
#   -o   맞은 부분만 찍는다 (--only-matching)
grep -o 'orderId=[0-9]*' app.log
```

```bash
orderId=1001
orderId=1001
orderId=1002
```

```bash
# ERROR 줄을 2 개 찾으면 멈춘다. 큰 로그에서 | head -2 와 차이가 난다
#   -m N   맞은 줄이 N 개가 되면 읽기를 멈춘다 (--max-count)
grep -m 2 ERROR app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

`-m 2` 는 `grep ERROR app.log | head -2` 와 결과가 같지만 멈추는 쪽이 다릅니다. `-m` 은 `grep` 이 두 줄을 찾은 자리에서 멈추고, `| head -2` 쪽은 `grep` 이 파일을 계속 읽다가 `head` 가 끝난 뒤 더 쓰려 할 때에야 SIGPIPE 로 멈춥니다.

### 앞뒤 문맥 줄 함께 찍기

> 맞은 줄의 뒤(`-A n`)와 앞(`-B n`), 앞뒤(`-C n`) 줄을 함께 봅니다.

```bash
# 맞은 줄의 앞뒤 한 줄씩을 함께 찍는다. -B1 -A1 은 -C1 과 같다
#   -B NUM   맞은 줄 앞 NUM 줄을 함께 찍는다 (--before-context)
#   -A NUM   맞은 줄 뒤 NUM 줄을 함께 찍는다 (--after-context)
grep \
  -n \
  -B1 \
  -A1 \
  WARN \
  app.log
```

```bash
2-2026-11-10 09:14:40 ERROR payment timeout orderId=1001
3:2026-11-10 09:14:41 WARN  retrying orderId=1001
4-2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

맞은 줄 번호 뒤에는 `:` 가 붙고 문맥 줄에는 `-` 가 붙습니다.

### 주석과 빈 줄 빼고 읽기

> 역일치(`-v`)에 정규식을 주면 주석과 빈 줄을 뺀 설정만 볼 수 있습니다.

```bash
# 줄 머리 공백까지 [[:space:]]* 로 받아야 주석 두 가지와 빈 줄이 모두 빠져 세 줄만 남는다
#   -E   패턴을 확장 정규식으로 읽는다 (--extended-regexp)
grep -vE '^[[:space:]]*(#|$)' sshd_config
```

```bash
Port 22
PasswordAuthentication yes
X11Forwarding no
```

[sed 참조 시트](./sed.md)의 `sed '/^#/d; /^$/d'` 도 아래 `grep -v '^#'` 처럼 들여 쓴 주석을 지우지 못합니다.

```bash
# 비교: -v '^#' 만 쓰면 빈 줄 둘과 들여 쓴 주석이 남는다
grep -v '^#' sshd_config
```

```bash

Port 22
PasswordAuthentication yes
  # indented comment

X11Forwarding no
```

### 압축 로그 읽기

> 압축된 로그는 풀지 않고 `zgrep` 으로 읽습니다.

```bash
# 압축 해제 없이 검색한다. zgrep 은 gzip 패키지의 셸 스크립트다
zgrep -c ERROR app.log.1.gz                      # 3
```

`zgrep` 은 옵션을 그대로 `grep` 에 넘깁니다.[^zgrep]

### 로그인 실패를 출발지별로 세기

> `auth.log` 에서 실패 줄을 고른 뒤 출발지 주소만 뽑아 세면 어느 주소가 몇 번 두드렸는지 보입니다.

```bash
# 로그인 실패 줄 수
grep -c 'Failed password' auth.log               # 3

# 실패 줄에서 출발지 주소만 뽑아 센다. uniq -c 는 이웃한 같은 줄만 합치므로 sort 로 먼저 모은다
grep 'Failed password' auth.log | grep -o 'from [0-9.]*' | sort | uniq -c
```

```bash
      2 from 203.0.113.7
      1 from 203.0.113.9
```



## 주의사항과 동작 원리

> 패턴은 기본이 정규식이라 `[ERROR]` 는 문자 집합으로, `|` 는 글자 그대로 읽힙니다.

### 정규식으로 읽히는 글자

> 패턴은 기본이 정규식이라 눈에 보이는 글자 그대로 찾지 않을 때가 있습니다.

```bash
# 대괄호는 문자 집합이라 [ERROR] 는 E·R·O 가운데 한 글자라도 든 줄에 맞는다
grep -c '[ERROR]' app.log        # 6

# [ERROR] 를 대괄호까지 글자 그대로 찾는다
#   -F   패턴을 정규식이 아니라 글자 그대로 읽는다 (--fixed-strings)
grep -F '[ERROR]' app.log        # 2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3

# | 를 그대로 주면 맞는 줄이 없다
grep 'WARN|ERROR' app.log        # 출력 없음

# 단어 단위로 맞추면 errors=3 이 걸러진다
grep -w error app.log            # 2026-11-10 10:06:01 error db connection reset

# 확장 정규식으로 읽으면 | 가 둘 중 하나를 뜻하고, \[ \] 는 대괄호 글자 그대로다
grep -E 'WARN|\[ERROR\]' app.log
# 2026-11-10 09:14:41 WARN  retrying orderId=1001
# 2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

기본 정규식에서는 `|` 가 글자 그대로라 GNU grep 에서는 `\|` 로 씁니다.[^bre]



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [sed 참조 시트](./sed.md) · [cut 참조 시트](./cut.md) · [awk 참조 시트](./awk.md) — 고른 줄을 바꾸거나 칸을 뽑는 다음 단계
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- GNU grep 3.8 의 `grep --help`·`man grep` 원문 — Debian 12 컨테이너에서 2026-11-13 출력
- [GNU grep 매뉴얼](https://www.gnu.org/software/grep/manual/grep.html) — 2026-11-10 조회

[^grep]: GNU grep 매뉴얼, "Command-line Options" 와 "Exit Status" — "the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred". <https://www.gnu.org/software/grep/manual/grep.html>
[^bre]: GNU grep 매뉴얼, "Basic vs Extended Regular Expressions" — "The characters '?', '+', '{', '|', '(', and ')' lose their special meaning; instead use the backslashed versions". <https://www.gnu.org/software/grep/manual/grep.html#Basic-vs-Extended>
[^zgrep]: `zgrep(1)` — "All options specified are passed directly to grep". <https://manpages.debian.org/bookworm/gzip/zgrep.1.en.html>
[^grep-exit]: `grep(1)` 의 EXIT STATUS (GNU grep 3.8, Debian 12 의 `man grep`) — "Normally the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred. However, if the -q or --quiet or --silent is used and a line is selected, the exit status is 0 even if an error occurred." <https://manpages.debian.org/bookworm/grep/grep.1.en.html>
