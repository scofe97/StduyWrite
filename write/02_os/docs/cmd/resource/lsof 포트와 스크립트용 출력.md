---
title: lsof 포트와 스크립트용 출력
tags: [linux, cheatsheet, lsof, socket, port, script, cli, reference]
status: draft
source:
  - lsof 4.95.0 lsof(8) (Debian 12 패키지, manpages.debian.org bookworm)
related:
  - ./lsof.md
  - ../README.md
updated: 2026-11-13
---

# lsof 포트와 스크립트용 출력

---

> 포트에서 출발해 소켓과 연결을 보고, `-t`·`-F`·`-r` 로 스크립트에 넘길 출력을 만드는 `lsof` 를 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> 이 시트는 `lsof` 로 포트·주소·상태를 골라 소켓을 잡은 프로세스를 찾는 일과, 그 결과를 스크립트에 넘기는 일을 다룹니다.

[lsof 참조 시트](./lsof.md)에서 포트와 연결 보기, 스크립트용 출력 유스케이스를 떼어 낸 것입니다. 예는 그 시트의 「실습 준비」 를 돌린 상태에서 이어지고, 출력은 같은 Debian 12 컨테이너(lsof 4.95.0, `--cap-add SYS_PTRACE`)에서 root 로 받았습니다.



## 핵심 문법

> `-i` 로 포트·주소·상태를 고르고, `-t`·`-F` 로 스크립트에 넘길 출력을, `-r` 로 되풀이를 정합니다.

```bash
# 호출 형태. lsof -h 의 usage 줄을 줄 단위로 다시 끊고 앞에 lsof 를 붙였다
lsof [-?abhKlnNoOPRtUvVX] [+|-c c] [+|-d s] [+D D] [+|-E] [+|-e s] \
  [+|-f[gG]] [-F [f]] [-g [s]] [-i [i]] [+|-L [l]] [+m [m]] [+|-M] \
  [-o [o]] [-p s] [+|-r [t]] [-s [p:s]] [-S [t]] [-T [t]] [-u s] \
  [+|-w] [-x [fl]] [--] [names]

# 포트·주소·프로토콜로 소켓을 고른다 (포트와 연결 보기)
lsof -nP -i [4|6][프로토콜][@주소][:포트]

# 프로토콜의 상태로 좁힌다 (상태로 좁히기)
lsof \
  -nP \
  -i TCP \
  -sTCP:상태

# 유닉스 도메인 소켓을 고른다 (유닉스 소켓)
lsof -U

# PID 만, 또는 필드 문자로 고른 필드만 찍는다 (스크립트에 넘길 출력 만들기)
lsof -t -i :포트
lsof -F 필드문자 -i :포트

# 같은 조회를 되풀이한다. +r 은 목록이 비면 끝낸다 (스크립트에 넘길 출력 만들기)
lsof \
  -nP \
  -r 초c횟수 \
  -i :포트
lsof \
  -nP \
  +r 초 \
  -i :포트
```



## 종료 코드

> 종료 코드는 `lsof` 한 벌이라 이 시트는 목록을 따로 싣지 않습니다.

목록은 [lsof 참조 시트](./lsof.md)의 「종료 코드」 에 있습니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 이 시트는 따로 만드는 것이 없고 원래 시트의 프로세스와 소켓을 그대로 씁니다.

먼저 [lsof 참조 시트](./lsof.md)의 「실습 준비」 블록을 돌립니다. PID·장치 번호·inode·임시 포트는 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다.

### 포트와 연결 보기

> 포트에서 출발할 때는 `-i` 를 쓰고, 프로토콜·주소·상태로 좁히면 소켓을 잡은 프로세스까지 한 번에 나옵니다.

호스트 앞의 `@` 와 포트 앞의 `:` 는 생략할 수 없습니다.[^net]

```bash
# 네트워크 파일 전부. 이름 풀이가 켜져 있어 127.0.0.1 이 localhost 로,
# 8080 이 http-alt 로 보인다
# -i 뒤 주소 형식은 [46][프로토콜][@호스트][:포트] 다 (-i 는 lsof 시트에서 풀었다)
lsof -i
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP localhost:http-alt (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP localhost:http-alt->localhost:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP localhost:tproxy (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP localhost:48454->localhost:http-alt (ESTABLISHED)
```

`localhost:http-alt` 처럼 읽기 쉬운 이름은 이름 조회를 거친 결과이고, 조회가 느리면 `lsof` 자체가 느려지므로 `-n` 과 `-P` 를 습관으로 씁니다.[^np]

```bash
# 호스트 이름을 풀지 않아 127.0.0.1 로 나온다
#   -n       네트워크 번호를 호스트 이름으로 바꾸지 않는다
#   head -2  앞 두 줄만 낸다
lsof -n -i :8080 | head -2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP 127.0.0.1:http-alt (LISTEN)
```

```bash
# 포트 이름을 풀지 않아 8080 으로 나온다
#   -P   포트 번호를 포트 이름으로 바꾸지 않는다
lsof -P -i :8080 | head -2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP localhost:8080 (LISTEN)
```

```bash
# 둘 다 끈다. 이 시트의 이후 예는 이 조합을 쓴다
lsof -nP -i :8080
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154 root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3162 root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

`-i :8080` 은 그 포트를 듣는 소켓과 연결된 소켓을 모두 보이며, 위 출력의 세 줄은 서버의 듣는 소켓(`LISTEN`)과 서버 쪽 연결, 클라이언트인 `conn.py` 의 연결입니다. `->` 의 왼쪽이 이 소켓의 로컬 주소이고 오른쪽이 상대입니다.

```bash
# 열린 TCP 소켓 다섯 줄이 모두 나온다
#   -i TCP   프로토콜로 좁힌다. UDP 도 같은 꼴이다
lsof -nP -i TCP
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# 열린 UDP 소켓이 없으면 출력이 비고 종료 코드가 1 이다
# (lsof 참조 시트의 「종료 코드」)
lsof -nP -i UDP; echo "exit $?"    # exit 1
```

```bash
# 앞 예의 TCP 목록과 같은 다섯 줄이 나온다
#   -i 4TCP:8000-9000   IP 버전(4)·프로토콜(TCP)·포트 범위를 한 번에 준다
#                       6 이면 IPv6 만 보며 이 환경에는 없다
lsof -nP -i 4TCP:8000-9000
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# 모든 주소에 묶인(*) nc 9000 은 빠진다
#   -i @주소   그 주소에 묶인 소켓을 고른다
lsof -nP -i @127.0.0.1
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
python3 3154    root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
python3 3162    root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

```bash
# 8081 의 LISTEN 소켓 하나만 나온다
#   -i TCP@주소:포트   프로토콜·주소·포트를 한 번에 준다
lsof -nP -i TCP@127.0.0.1:8081
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
```

### 상태로 좁히기

> `-s` 로 연결 상태를 고르면 듣는 소켓과 맺은 연결을 따로 봅니다.

`-s` 의 상태 조건은 TCP 와 UDP 파일에 걸리고, 상태 앞에 `^` 를 붙이면 그 상태가 빠집니다.[^state]

```bash
# 듣는 소켓만 남는다. 어느 프로세스가 포트를 쥐고 있는지 볼 때 쓴다
#   -sTCP:LISTEN   TCP 소켓 가운데 LISTEN 상태만 고른다
lsof \
  -nP \
  -i TCP \
  -sTCP:LISTEN
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154    root    3u  IPv4 405452      0t0  TCP 127.0.0.1:8080 (LISTEN)
nc      3155    root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
python3 3161 appuser    3u  IPv4 406324      0t0  TCP 127.0.0.1:8081 (LISTEN)
```

```bash
# LISTEN 이 아닌 것만 남아 이미 맺은 연결만 나온다
#   -sTCP:^LISTEN   ^ 를 붙이면 그 상태를 뺀다
lsof \
  -nP \
  -i TCP \
  -sTCP:^LISTEN
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3154 root    4u  IPv4 406330      0t0  TCP 127.0.0.1:8080->127.0.0.1:48454 (ESTABLISHED)
python3 3162 root    3u  IPv4 406329      0t0  TCP 127.0.0.1:48454->127.0.0.1:8080 (ESTABLISHED)
```

### 유닉스 소켓

> 파일로 만든 소켓은 NAME 에 소켓 파일 경로와 종류(type=STREAM)가 나옵니다.

```bash
# nc 가 듣는 app.sock 한 줄이 나온다
#   -U   유닉스 도메인 소켓 파일을 고른다
lsof -U
```

```bash
COMMAND  PID USER   FD   TYPE             DEVICE SIZE/OFF   NODE NAME
nc      3156 root    3u  unix 0x0000000000000000      0t0 406316 /root/cmd-lab/lsof/app.sock type=STREAM (LISTEN)
```

`DEVICE` 의 `0x0000000000000000` 은 이 환경에서 커널 주소가 가려져 0 으로 찍힌 값입니다.

### 스크립트에 넘길 출력 만들기

> `-t` 는 PID 만, `-F` 는 필드를 한 줄씩 찍어 파이프라인에 바로 연결하고, `-r` 은 같은 조회를 되풀이합니다.

스크립트에는 헤더와 열 간격에 기대지 않는 출력이 필요합니다. 포트를 쥔 프로세스를 찾아 바로 다른 명령에 넘기는 일이 대표적입니다.

```bash
# 헤더 없이 PID 만 나온다. 같은 프로세스가 여러 줄이어도 한 번만 나온다
#   -t   PID 만 찍는다 (terse)
lsof -t -i :8081    # 3161
```

`-t` 는 `-w`(경고 억제)를 함께 켜며, 아래처럼 PID 를 다른 명령에 바로 넘깁니다.[^t]

```bash
# 끝내기 전에 8081 을 쥔 줄이 있는지 센다. 2 는 헤더 한 줄과 소켓 한 줄이다
lsof -nP -i :8081 | wc -l    # 2
```

```bash
# kill $(lsof -t ...): 포트를 쥔 프로세스에 TERM 을 보낸다
# Terminated 는 8081 서버를 감싼 서브셸이 찍는다
# (대화형 셸은 잡 알림 줄이 더 나온다)
kill $(lsof -t -i :8081); sleep 0.5    # Terminated
```

```bash
# 끝났는지 다시 확인. 일치하는 줄이 없으면 종료 코드 1
lsof -nP -i :8081; echo "exit $?"    # exit 1
```

대상이 없을 때 `kill $(lsof -t …)` 는 인자 없이 `kill` 이 돌아 오류가 나므로, 스크립트에서는 `lsof -t … | xargs -r kill` 로 인자가 없으면 건너뜁니다. 이 시트의 `-t` 예는 man 의 예(`lsof -t /lib/*/libssl.so.* | xargs -r kill -HUP`)와 같은 꼴입니다.[^t]

```bash
# 필드 하나가 한 줄이다. p=PID c=명령 f=FD n=이름
#   -F   문자마다 필드 하나를 찍는다
lsof -F pcfn -i :8080
```

```bash
p3154
cpython3
f3
nlocalhost:http-alt
f4
nlocalhost:http-alt->localhost:48454
p3162
cpython3
f3
nlocalhost:48454->localhost:http-alt
```

`p` 로 시작하는 줄이 프로세스 하나의 시작이고 그 아래 `f`·`n` 줄이 그 프로세스가 연 파일이며, 열 간격이 바뀌어도 깨지지 않으므로 `awk` 로 열 번호를 세는 것보다 안전합니다. `-F 0`(문자 `0` 만)은 모든 필드를 NUL 로 끝내 찍으며 공백이 든 파일 이름도 구분합니다.[^f]

```bash
# 1초 간격으로 두 번 되풀이한다. c2 를 빼면 Ctrl-C 까지 계속한다
#   -r   t초 간격으로 목록을 되풀이한다. c 뒤 숫자는 반복 횟수다
lsof \
  -nP \
  -r 1c2 \
  -i :9000
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3155 root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
=======
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3155 root    3u  IPv4 408031      0t0  TCP *:9000 (LISTEN)
=======
```

`-r` 은 목록 사이에 `=======` 줄을 찍고, `+r` 은 목록이 비는 순간 스스로 끝나 포트를 쥔 프로세스가 사라질 때까지 기다리는 용도에 맞습니다.[^r]

```bash
# 1.5초 뒤 9100 을 듣는 nc 를 죽이면 목록이 두 번 찍히고 exit 0 으로 끝난다
#   +r   목록이 비면 되풀이를 끝낸다
nc -4 -l 9100 & sleep 0.5; \
(sleep 1.5; kill $(lsof -t -i :9100)) & \
lsof \
  -nP \
  +r 1 \
  -i :9100; \
echo "exit $?"
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3280 root    3u  IPv4 410918      0t0  TCP *:9100 (LISTEN)
=======
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nc      3280 root    3u  IPv4 410918      0t0  TCP *:9100 (LISTEN)
=======
exit 0
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [lsof 참조 시트](./lsof.md) — 이 시트가 이어받는 실습 준비와 출력 열·프로세스·파일에서 출발하는 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록

소켓 쪽을 보는 다른 도구는 `ss` 입니다.



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- lsof 4.95.0 의 `lsof -v`·`lsof -h` 출력 — Debian 12 컨테이너에서 2026-11-11 확인
- [lsof(8) — Debian bookworm](https://manpages.debian.org/bookworm/lsof/lsof.8.en.html)

[^net]: `man lsof` OPTIONS — `-i [i]` "selects the listing of files any of whose Internet address matches the address specified in i. If no address is specified, this option selects the listing of all Internet and x.25 (HP-UX) network files.", "[46][protocol][@hostname|hostaddr][:service|port]", "The @ character, leading the host specification, is always required; as is the :, leading the port specification.", "If -i4 or -i6 is specified with no following address, only files of the indicated IP version, IPv4 or IPv6, are displayed."; `-U` "selects the listing of UNIX domain socket files."
[^np]: `man lsof` OPTIONS — `-n` "inhibits the conversion of network numbers to host names for network files. Inhibiting conversion may make lsof run faster. It is also useful when host name lookup is not working properly.", `-P` "inhibits the conversion of port numbers to port names for network files. Inhibiting the conversion may make lsof run a little faster. It is also useful when port name lookup is not working properly."
[^state]: `man lsof` OPTIONS — `-s [p:s]` "the option causes open TCP and UDP files to be excluded if their state name(s) are in the list (s) preceded by a ^; or included if their name(s) are not preceded by a ^."
[^t]: `man lsof` OPTIONS — `-t` "produce terse output comprising only process identifiers (without a header), so that it is easy to use programmatically. e.g. # reload anything using old SSL lsof -t /lib/*/libssl.so.* | xargs -r kill -HUP", "The -t option implies the -w option."
[^f]: `man lsof` OPTIONS — `-F f` "specifies a character list, f, that selects the fields to be output for processing by another program, and the character that terminates each output field. ... The field terminator defaults to NL, but may be changed to NUL (000).", "When the field selection character list contains only a zero (0), all fields are selected (except the raw device field for compatibility reasons) and the NUL terminator character is used."; OUTPUT FOR OTHER PROGRAMS "A process set begins with a field whose identifier is p (for process IDentifier (PID))", field identifiers "c process command name", "f file descriptor", "n file name, comment, Internet address", "p process ID (always selected)".
[^r]: `man lsof` OPTIONS — `+|-r [t[c<N>][m<fmt>]]` "puts lsof in repeat mode. There lsof lists open files as selected by other options, delays t seconds (default fifteen), then repeats the listing", "If the prefix is a -, repeat mode is endless.", "`c<N>` is for specifying the limits of repeating; if the number of iterations reaches at <N>, Lsof stops itself.", "If the prefix is +, repeat mode will end the first cycle no open files are listed", "otherwise the default marker is ========". man 은 `=` 여덟 개로 적지만 이 환경의 4.95.0 이 실제로 찍는 줄은 일곱 개입니다.
