---
title: grep 참조 시트
tags: [linux, cheatsheet, grep, zgrep, cli, reference]
status: draft
source:
  - GNU grep 매뉴얼 · zgrep(1)
related:
  - ../README.md
updated: 2026-11-11
---

# grep 참조 시트

---

> 맞은 줄을 고르는 `grep` 의 옵션을 일치 기준, 검색 대상, 출력 형식 세 묶음으로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일이 모두 생깁니다.

macOS 기본 `grep` 은 GNU 판이 아니어서 옵션과 출력이 조금 다릅니다. OrbStack 의 Linux VM 이나 `docker run -it --rm debian:12` 안에서 실행합니다.

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

`app.log` 는 일곱 줄짜리 애플리케이션 로그이고 `ERROR`·`error`·`[ERROR]` 가 섞여 있습니다. `sshd_config` 에는 주석·빈 줄·들여 쓴 주석이 있고 `auth.log` 에는 SSH 로그인 실패 세 줄과 성공 한 줄이 있습니다. `conf/` 에는 `timeout=30` 인 `a.conf` 와 `c.txt`, `timeout=60` 인 `b.conf` 가 있습니다.



## 1. 무엇을 맞은 줄로 보나

> 대소문자, 역일치, 줄 전체 일치처럼 맞은 줄의 기준을 바꾸는 옵션입니다. 패턴이 정규식으로 읽히는 함정도 여기 둡니다.

`grep 패턴 파일` 은 패턴과 맞는 줄만 내보냅니다. 옵션은 일치 기준, 검색 대상, 출력 형식으로 갈립니다.[^grep]

### 대소문자와 역일치

기본은 대소문자를 가립니다. 같은 오류라도 `error` 로 적힌 줄은 `grep ERROR` 에 걸리지 않습니다.

```bash
# 기본: 대문자 ERROR 가 든 줄만
grep ERROR app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# -i (--ignore-case): 대소문자를 가리지 않는다. 소문자 error 줄이 더해진다
grep -i error app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:01 error db connection reset
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

```bash
# -v (--invert-match): 맞지 않는 줄을 고른다. INFO 두 줄을 뺀 다섯 줄
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

패턴은 기본으로 줄 안 어디에 있어도 맞습니다. 줄 전체나 단어 하나와 같아야 맞게 하려면 범위를 좁힙니다.

```bash
# -x (--line-regexp): 줄 전체가 패턴과 같아야 맞는다
grep -x 'Port 22' sshd_config      # Port 22
grep -x 'Port' sshd_config         # 출력 없음, 종료 상태 1

# -w (--word-regexp): 단어 단위로 맞춘다. errors=3 의 error 는 뒤에 s 가 붙어 빠진다
grep -w error app.log              # 2026-11-10 10:06:01 error db connection reset
```

### 패턴 여러 개

패턴을 여럿 주면 하나라도 맞는 줄을 고릅니다. 패턴이 많으면 파일에 한 줄에 하나씩 적어 `-f` 로 읽힙니다.

```bash
# -e: 패턴을 하나씩 더한다
grep -e WARN -e heartbeat app.log
```

```bash
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 11:30:00 INFO  heartbeat
```

```bash
# -f 파일: 파일의 줄마다 패턴 하나. patterns.txt 는 ERROR 와 WARN 두 줄
grep -f patterns.txt app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:14:41 WARN  retrying orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

### 정규식으로 읽히는 글자

패턴은 기본이 정규식이라 눈에 보이는 글자 그대로 찾지 않을 때가 있습니다.

```bash
grep -c '[ERROR]' app.log        # 6

# 문자열 그대로 검색
grep -F '[ERROR]' app.log        # 2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
grep 'WARN|ERROR' app.log        # 출력 없음
grep -w error app.log            # 2026-11-10 10:06:01 error db connection reset
grep -E 'WARN|\[ERROR\]' app.log
# 2026-11-10 09:14:41 WARN  retrying orderId=1001
# 2026-11-10 10:06:02 [ERROR] pool exhausted, errors=3
```

- 기본 정규식에서 대괄호는 문자 집합이라 `[ERROR]` 는 한 글자라도 든 줄에 맞습니다. 
- 세로 막대(|)로 둘 중 하나를 찾으려면 확장 정규식 `-E` 를 줍니다. 기본 정규식에서는 `|` 가 글자 그대로라 GNU grep 에서는 `\|` 로 씁니다.[^bre] `-w` 는 단어 단위로 일치시켜 `errors=3` 을 거릅니다. 

정규식으로 쓸 때 자주 쓰는 글자는 셋입니다. `.` 은 아무 글자 하나, `^` 는 줄 머리, `$` 는 줄 끝입니다.

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



## 2. 어디를 읽나

> 파일 하나 대신 디렉터리 아래를 읽게 하고, 읽을 파일 이름을 좁힙니다.

검색 대상은 `-r` 로 넓히고 `--include`·`--exclude` 로 좁힙니다.

```bash
# -r (--recursive): 디렉터리 아래를 재귀로 읽고 줄 앞에 파일 이름을 붙인다
grep -r 'timeout=30' conf
```

```bash
conf/a.conf:timeout=30
conf/c.txt:timeout=30
```

`-r` 이 찍는 파일 순서는 디렉터리를 읽는 순서라 환경마다 다를 수 있습니다. 순서가 중요하면 `sort` 를 붙입니다.

```bash
# --include=GLOB: 이름이 맞는 파일만 읽는다
grep -r --include='*.conf' 'timeout=30' conf    # conf/a.conf:timeout=30

# --exclude=GLOB: 이름이 맞는 파일을 뺀다
grep -r --exclude='*.conf' timeout conf         # conf/c.txt:timeout=30

# -h (--no-filename): 줄 앞 파일 이름을 떼고 내용만
grep -rh 'timeout=30' conf
```

```bash
timeout=30
timeout=30
```

`--include` 와 `--exclude` 의 값은 따옴표로 감쌉니다. 감싸지 않으면 셸이 `*.conf` 를 지금 폴더의 파일 이름으로 먼저 펼칩니다.



## 3. 무엇을 찍나

> 맞은 줄 대신 줄 번호, 개수, 파일 이름, 맞은 부분, 앞뒤 문맥을 찍게 합니다.

맞은 줄을 통째로 보는 대신 필요한 것만 찍으면 다음 명령에 넘기기 쉽습니다.

```bash
# -n (--line-number): 줄 번호를 붙인다
grep -n WARN app.log                # 3:2026-11-10 09:14:41 WARN  retrying orderId=1001

# -c (--count): 맞은 줄 수만 낸다. 한 줄에 두 번 맞아도 1 로 센다
grep -c ERROR app.log               # 3

# -l (--files-with-matches): 맞은 파일 이름만 낸다
grep -l ERROR app.log sshd_config   # app.log

# -L (--files-without-match): 맞는 줄이 하나도 없는 파일 이름만 낸다
grep -rL 'timeout=30' conf          # conf/b.conf
```

```bash
# -o (--only-matching): 맞은 부분만 한 줄에 하나씩 낸다
grep -o 'orderId=[0-9]*' app.log
```

```bash
orderId=1001
orderId=1001
orderId=1002
```

```bash
# -m N (--max-count): 맞은 줄을 N 개 찾으면 읽기를 멈춘다
grep -m 2 ERROR app.log
```

```bash
2026-11-10 09:14:40 ERROR payment timeout orderId=1001
2026-11-10 09:20:02 ERROR payment timeout orderId=1002
```

`-m 2` 는 `grep ERROR app.log | head -2` 와 결과가 같지만 멈추는 쪽이 다릅니다. `-m` 은 `grep` 이 두 줄을 찾은 자리에서 읽기를 멈춥니다. `| head -2` 쪽은 `grep` 이 파일을 계속 읽고 `head` 가 끝난 뒤 더 쓰려 할 때에야 SIGPIPE 로 멈춥니다. 큰 로그에서 차이가 납니다.

### 앞뒤 문맥과 역일치

맞은 줄의 뒤(`-A n`)와 앞(`-B n`), 앞뒤(`-C n`) 줄을 함께 보는 문맥 옵션과 역일치(`-v`)는 아래처럼 씁니다.

```bash
# -B1 -A1 은 -C1 과 같다
grep -n -B1 -A1 WARN app.log
grep -vE '^[[:space:]]*(#|$)' sshd_config
```

```bash
2-2026-11-10 09:14:40 ERROR payment timeout orderId=1001
3:2026-11-10 09:14:41 WARN  retrying orderId=1001
4-2026-11-10 09:20:02 ERROR payment timeout orderId=1002
Port 22
PasswordAuthentication yes
X11Forwarding no
```

맞은 줄 번호 뒤에는 `:` 가 붙고 문맥 줄에는 `-` 가 붙습니다. `grep -v '^#'` 만 쓰면 빈 줄과 들여 쓴 주석이 남고 [sed 참조 시트](./sed.md)의 `sed '/^#/d; /^$/d'` 도 들여 쓴 주석은 못 지웁니다. 줄 머리 공백까지 `[[:space:]]*` 로 받아야 세 줄만 남습니다.

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

### 압축 로그와 종료 상태

`auth.log` 에는 로그인 실패가 세 줄 있습니다. 실패 줄을 고른 뒤 출발지 주소만 뽑아 세면 어느 주소가 몇 번 두드렸는지 보입니다.

```bash
grep -c 'Failed password' auth.log               # 3
grep 'Failed password' auth.log | grep -o 'from [0-9.]*' | sort | uniq -c
```

```bash
      2 from 203.0.113.7
      1 from 203.0.113.9
```

```bash
# 압축 해제 없이 검색
zgrep -c ERROR app.log.1.gz                      # 3
```

`zgrep` 은 옵션을 그대로 `grep` 에 넘깁니다.[^zgrep] `grep` 종료 상태는 맞으면 0, 없으면 1, 오류면 2입니다. `if grep -q` 처럼 조건식에 씁니다([《Learning Modern Linux》 3장 첫 노트](../../../book/learning-modern-linux/03-01.%EC%85%B8%EC%9D%98%20%EC%8B%A4%EC%B2%B4%EB%8A%94%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EA%B3%BC%20%EB%B3%80%EC%88%98%EC%99%80%20%EC%A2%85%EB%A3%8C%20%EC%83%81%ED%83%9C%EB%8B%A4.md) 4절).

```bash
# -q (--quiet): 아무것도 찍지 않고 종료 상태만 남긴다
grep -q heartbeat app.log; echo $?      # 0
grep -q panic app.log; echo $?          # 1

# 파일이 없으면 2. -s (--no-messages) 는 오류 메시지만 숨긴다
grep -s -q x nofile.log; echo $?        # 2
```



## 관련 문서

- [sed 참조 시트](./sed.md) · [cut 참조 시트](./cut.md) · [awk 참조 시트](./awk.md) — 고른 줄을 바꾸거나 칸을 뽑는 다음 단계



## 참고 자료

- [GNU grep 매뉴얼](https://www.gnu.org/software/grep/manual/grep.html) — 2026-11-10 조회

[^grep]: GNU grep 매뉴얼, "Command-line Options" 와 "Exit Status" — "the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred". <https://www.gnu.org/software/grep/manual/grep.html>
[^bre]: GNU grep 매뉴얼, "Basic vs Extended Regular Expressions" — "The characters '?', '+', '{', '|', '(', and ')' lose their special meaning; instead use the backslashed versions". <https://www.gnu.org/software/grep/manual/grep.html#Basic-vs-Extended>
[^zgrep]: `zgrep(1)` — "All options specified are passed directly to grep". <https://manpages.debian.org/bookworm/gzip/zgrep.1.en.html>
