---
title: lsof 참조 시트
tags: [linux, cheatsheet, lsof, file-descriptor, socket, cli, reference]
status: draft
source:
  - lsof 4.95.0 lsof(8) (Debian 12 패키지, manpages.debian.org bookworm)
  - Linux man-pages proc(5), unlink(2), pid_namespaces(7), capabilities(7) (Debian 12 manpages)
  - coreutils df(1), du(1) (Debian 12 manpages)
related:
  - ./lsof 포트와 스크립트용 출력.md
  - ../README.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-13
---

# lsof 참조 시트

---

> 프로세스가 열어 둔 파일과 소켓을 보는 `lsof` 의 옵션을 출력 열 읽기, 프로세스·파일에서 출발하기, 지운 파일 찾기로 나눠, 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `lsof` 는 프로세스마다 열린 파일을 한 줄씩 나열합니다.

이름은 "list open files" 의 줄임말입니다. 리눅스에서는 소켓도 파일 디스크립터라 일반 파일과 같은 목록에 나옵니다.[^out]

Debian 의 `lsof` 패키지(`/usr/bin/lsof`)를 썼고, 이 시트는 `--cap-add SYS_PTRACE` 를 준 Debian 12 컨테이너의 root 에서 lsof 4.95.0 으로 실측했습니다. macOS 의 `lsof` 는 Apple 이 따로 낸 판이라 열과 옵션 일부가 다릅니다.

포트와 연결, 스크립트용 출력은 [lsof 포트와 스크립트용 출력](./lsof%20포트와%20스크립트용%20출력.md)에 있습니다.



## 핵심 문법

> 프로세스(`-p`·`-c`·`-u`), 파일 이름, 포트(`-i`) 중 아는 것에서 출발해 열린 파일을 고릅니다.

```bash
# 호출 형태 (lsof -h 의 usage 줄. 명령 이름 lsof 는 빠져 있다)
usage: [-?abhKlnNoOPRtUvVX] [+|-c c] [+|-d s] [+D D] [+|-E] [+|-e s] [+|-f[gG]]
[-F [f]] [-g [s]] [-i [i]] [+|-L [l]] [+m [m]] [+|-M] [-o [o]] [-p s]
[+|-r [t]] [-s [p:s]] [-S [t]] [-T [t]] [-u s] [+|-w] [-x [fl]] [--] [names]

# 프로세스가 연 파일 전부를 열 단위로 읽는다 (출력의 열 읽기)
lsof -p PID

# 명령 이름이나 사용자로 프로세스를 고른다 (프로세스가 연 파일 보기)
lsof -c 이름
lsof -u 사용자

# 파일이나 디렉터리를 연 프로세스를 찾는다 (이 파일을 연 프로세스 찾기)
lsof 파일
lsof +d 디렉터리
lsof +D 디렉터리

# 링크 수가 1 보다 작은 열린 파일, 곧 지운 파일을 찾는다 (지운 파일이 붙든 공간 찾기)
lsof +L1

# 포트·주소·상태로 소켓을 고른다 (lsof 포트와 스크립트용 출력 시트의 「포트와 연결 보기」)
lsof -i [4|6][프로토콜][@주소][:포트]
```

### 출력 열

> 한 줄은 아홉 열이고, FD 와 TYPE 이 그 파일이 무엇인지 알려 줍니다.

열의 뜻은 man 의 OUTPUT 풀이를 따랐습니다.[^out]

```bash
# COMMAND   명령 이름의 앞 아홉 글자
# PID       프로세스 번호
# USER      그 프로세스를 가진 사용자
# FD        파일 디스크립터 번호이거나 아래 이름
#           번호 뒤에 열린 방식이 한 글자 붙는다
#             r 읽기, w 쓰기, u 읽기와 쓰기
#           그 뒤에 잠금 글자가 올 수 있다
# TYPE      파일의 종류. 이 시트에서는 아래가 나온다
#             REG 일반 파일, DIR 디렉터리, CHR 문자 장치
#             FIFO 파이프, IPv4 IPv4 소켓, unix 유닉스 소켓
# DEVICE    일반 파일·디렉터리·문자 장치는 쉼표로 나눈 장치 번호(0,61)
#           이 환경에서는 FIFO 도 0,15 처럼 장치 번호로 나온다
#           IPv4 소켓은 /proc/PID/fd 의 socket:[번호] 와 같은 번호
#           유닉스 소켓은 커널 주소
# SIZE/OFF  파일 크기이거나 오프셋. 크기가 없는 파일은 비고
#           오프셋은 앞에 0t 가 붙는다
#           -s 를 주면 크기만 보이고 열 이름이 SIZE 로 바뀐다
# NODE      로컬 파일은 inode 번호
#           네트워크 파일은 TCP 같은 프로토콜 이름
# NAME      파일 이름이나 네트워크 주소
#           TCP 면 끝의 괄호에 연결 상태가 붙는다

# FD 열의 이름과 값
#   cwd   현재 작업 디렉터리
#   rtd   루트 디렉터리
#   txt   프로그램 텍스트(실행 파일)
#   mem   메모리에 매핑한 파일(공유 라이브러리 등)
#   3w    파일 디스크립터 3번을 쓰기(w)로 열었다
```



## 종료 코드

> 오류 없이 찾았으면 0, 오류가 하나라도 있으면 1 입니다.[^exit]

아래 예는 「실습 준비」 에서 만든 파일과 프로세스로 돌립니다.

```bash
# 0  오류가 없고, 지정한 검색 항목마다 찾은 것이 있다
#    -Q 를 주면 찾지 못한 항목이 있어도 0 이다
# 1  오류가 하나라도 있다
#    명령 이름·파일 이름·인터넷 주소·로그인 이름·PID·UID 를
#    찾지 못한 것도 오류다. -V 를 주면 찾지 못한 항목을 알려 준다

# 파일을 연 프로세스를 찾아 목록을 냈으므로 0 이다
lsof logs/app.log > /dev/null; echo $?    # 0

# 없는 파일은 오류 문구를 내고 1 이다
# 2>&1 은 오류 메시지를 표준 출력에 합쳐 종료 코드와 함께 보인다
lsof nofile.txt 2>&1; echo $?
```

```bash
lsof: status error on nofile.txt: No such file or directory
1
```

```bash
# appuser 가 연 nc 프로세스는 없어 출력 없이 1 이다
#   -a   조건을 AND 로 묶는다. 기본은 OR 다 (「여러 조건을 줄 때의 OR 와 AND」)
#   -u   사용자 이름이나 UID 로 고른다
#   -c   이름이 이 글자로 시작하는 프로세스를 고른다
lsof \
  -a \
  -u appuser \
  -c nc; \
echo "exit $?"
# exit 1
```

```bash
# 못 찾은 항목 nc 를 알리는 줄이 나오고 종료 코드는 그대로 1 이다
#   -V   찾지 못한 검색 항목을 알려 준다
lsof \
  -V \
  -a \
  -u appuser \
  -c nc 2>&1; \
echo $?
```

```bash
lsof: command not located: nc
1
```

```bash
# 같은 검색이 이번에는 0 으로 끝난다
#   -Q   찾지 못한 검색 항목을 오류로 세지 않는다
lsof \
  -Q \
  -a \
  -u appuser \
  -c nc; \
echo $?
# 0
```

```bash
# 지운 파일이 아직 없으면 +L1 은 아무것도 찾지 못하지만 종료 코드는 0 이다
#   +L1   링크 수가 1 보다 작은 열린 파일, 곧 지운 파일을 고른다 (+L 에 숫자)
lsof +L1; echo "exit $?"    # exit 0
```

위 블록의 `+L1` 이 무엇을 찾는지는 「지운 파일이 붙든 공간 찾기」 에서 봅니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 프로세스와 파일이 모두 뜹니다.

`docker run -it --rm --cap-add SYS_PTRACE debian:12` 로 연 Debian 12 컨테이너나 OrbStack 의 Linux VM 에서 root 로 실행합니다. `--cap-add SYS_PTRACE` 가 필요한 이유는 「컨테이너 안에서 보이는 범위」 에 있습니다.

```bash
# 이 블록은 열린 파일을 만드는 프로세스를 여럿 띄운다. 출력은 터미널 폭과 무관하다
# 대화형 셸에서는 [1] 3153 같은 잡 번호 줄이 더 나온다
mkdir -p ~/cmd-lab/lsof && cd ~/cmd-lab/lsof

# 패키지. procps 는 pgrep 을, python3-minimal 은 holder.py·conn.py·http.server 를
# 돌릴 python3 을, netbase 는 /etc/services 를 준다
# 8080 이 http-alt 로 보이는 것이 /etc/services 덕이다
apt-get -qq update >/dev/null 2>&1; \
  apt-get -qq install -y lsof procps netbase netcat-openbsd python3-minimal \
  >/dev/null 2>&1

# 다른 사용자(appuser) 소유의 프로세스를 만들 때 쓴다
id appuser >/dev/null 2>&1 || useradd -m appuser

# logs/ 는 holder.py 가 열 파일 자리, /dev/shm/lsof-lab 은 tmpfs 위 파일 자리다
mkdir -p logs/old /dev/shm/lsof-lab
echo 'start' > logs/app.log

# tmpfs 인 /dev/shm 의 20MB 파일을 tail -f 가 열어 둔다
# 「지운 파일이 붙든 공간 찾기」 에서 이 파일을 지운다
dd if=/dev/zero of=/dev/shm/lsof-lab/big.log bs=1M count=20 2>/dev/null

# holder.py 는 logs/ 아래 파일 셋을 열고 700초 동안 쥐고 있다
# 「출력의 열 읽기」 와 「이 파일을 연 프로세스 찾기」 가 쓴다
cat > holder.py << 'EOF2'
import time
log = open('logs/app.log', 'a')
conf = open('logs/app.conf', 'w')
old = open('logs/old/app.log.1', 'w')
time.sleep(700)
EOF2

# conn.py 는 http.server 8080 에 붙어 연결 하나를 유지한다
cat > conn.py << 'EOF2'
import socket, time
s = socket.create_connection(('127.0.0.1', 8080))
time.sleep(701)
EOF2

# 이름이 긴 sleep 복사본. 「출력의 열 읽기」 에서 COMMAND 열이 이름을 자르는 모습에 쓴다
cp /bin/sleep long-running-worker

# holder.py 가 파일 셋을 연다
python3 holder.py &

# http.server 가 127.0.0.1 의 8080 포트를 듣는다
python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &

# nc 가 TCP 9000 포트와 유닉스 소켓 app.sock 을 각각 듣는다
nc -4 -l 9000 &
nc -lU ~/cmd-lab/lsof/app.sock &

# tail -f 가 tmpfs 의 20MB 파일을 열어 둔다. 오류 출력은 tail.err 로 받는다
tail -f /dev/shm/lsof-lab/big.log >/dev/null 2>tail.err &

# long-running-worker 가 703초 동안 돈다
./long-running-worker 703 &

# appuser 소유의 http.server 가 8081 포트를 듣는다
(cd /home/appuser && \
  setpriv \
    --reuid=appuser \
    --regid=appuser \
    --init-groups \
    python3 -m http.server 8081 --bind 127.0.0.1 >/dev/null 2>&1) &
sleep 1

# conn.py 가 8080 에 붙어 연결 하나를 만든다
python3 conn.py &
sleep 1
```

PID·장치 번호·inode·소켓 번호·임시 포트(`conn.py` 가 쓰는 포트)·`ls -l` 의 시각은 실행마다 다르므로 이 시트의 값과 같지 않아도 됩니다. 아래 예는 `holder.py` 의 PID 를 `$(pgrep -f holder.py)` 로 구해 씁니다.

### 출력의 열 읽기

> 프로세스마다 열린 파일이 한 줄씩 나오고, FD 와 TYPE 이 그 파일이 무엇인지 알려 줍니다.

```bash
# holder.py 가 연 파일 전부. 열은 COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
#   -p   PID 로 고른다
lsof -p $(pgrep -f holder.py)
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root  rtd    DIR   0,61       42 4348902 /
python3 3153 root  txt    REG   0,61  6616880 4349624 /usr/bin/python3.11
python3 3153 root  mem    REG   0,61   353616 3986986 /usr/lib/locale/C.utf8/LC_CTYPE
python3 3153 root  mem    REG   0,61  1651408 3986083 /usr/lib/aarch64-linux-gnu/libc.so.6
python3 3153 root  mem    REG   0,61   198712 4349585 /usr/lib/aarch64-linux-gnu/libexpat.so.1.8.10
python3 3153 root  mem    REG   0,61   133520 3986181 /usr/lib/aarch64-linux-gnu/libz.so.1.2.13
python3 3153 root  mem    REG   0,61   591960 3986122 /usr/lib/aarch64-linux-gnu/libm.so.6
python3 3153 root  mem    REG   0,61   202912 3986065 /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1
python3 3153 root  mem    REG   0,61    27028 3986056 /usr/lib/aarch64-linux-gnu/gconv/gconv-modules.cache
python3 3153 root    0r   CHR    1,3      0t0       5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

`cwd`·`rtd`·`txt`·`mem` 은 프로세스가 `open` 으로 연 파일이 아니라 커널이 프로세스에 붙인 참조입니다. `holder.py` 가 직접 연 파일은 숫자로 시작하는 `3w`·`4w`·`5w` 세 줄이고, 파이프 `1w`·`2w` 는 셸이 물려준 표준 출력과 오류입니다.

```bash
# 전체 출력에서 TYPE 열만 세면 이 환경에 열린 파일의 종류가 한눈에 보인다
# TYPE 은 5번째 열이라 awk 로 뽑아 종류별로 센다
# 옵션 없이 전부 볼 때는 스레드마다 줄이 더 나와 열 위치가 바뀐다
#   -K i   스레드(task)를 무시한다
lsof -K i | awk 'NR>1{print $5}' | sort | uniq -c
```

```bash
     16 CHR
     32 DIR
     29 FIFO
      5 IPv4
    114 REG
      1 a_inode
      1 unix
```

`a_inode` 는 man 의 TYPE 목록에 없는 값으로, inotify 처럼 inode 가 없는 디스크립터이며 `/proc/PID/fd` 에서는 `anon_inode:inotify` 로 보입니다.[^procfd]

```bash
# long-running-worker 가 long-runn 으로 잘려 나온다. COMMAND 열은 아홉 글자에서 잘린다
#   -d   FD 목록으로 고른다. 번호나 cwd·txt·mem 같은 이름이다
lsof \
  -c long-running \
  -a \
  -d cwd
```

```bash
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
long-runn 3158 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# 이름을 자르지 않으려고 0 을 줬다. 0 대신 숫자 w 를 주면 w 글자까지 보인다
#   +c   COMMAND 열에 찍을 최대 글자 수
lsof \
  +c 0 \
  -c long-running \
  -a \
  -d cwd
```

```bash
COMMAND          PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
long-running-wo 3158 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

`+c 0` 으로 봐도 이 환경에서는 15글자에서 끊깁니다. man 은 이 열이 UNIX 판이 lsof 에 넘기는 글자 수까지만 담는다고 적습니다.[^c]

```bash
# holder.py 의 부모 프로세스 번호가 PPID 열에 1 로 찍힌다
#   -R   부모 프로세스 번호를 PPID 열로 붙인다 (parent PID)
lsof \
  -R \
  -a \
  -d cwd \
  -p $(pgrep -f holder.py)
```

```bash
COMMAND  PID PPID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153    1 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# http.server 는 연결마다 스레드를 하나 만든다. 스레드도 한 줄씩 보인다
#   -K   스레드(task)까지 보인다. 열에 TID 와 TASKCMD 가 붙는다
lsof \
  -K \
  -a \
  -d cwd \
  -p $(pgrep -f 'http.server 8080')
```

```bash
COMMAND  PID  TID TASKCMD USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3154              root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3154 3164 python3 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

`TID` 가 빈 줄이 프로세스 자신이고 값이 있는 줄이 스레드입니다.[^K]

### 프로세스가 연 파일 보기

> 아는 것이 PID·명령 이름·사용자 중 하나일 때, 그것으로 출발해 열린 파일을 골라 냅니다.

조건을 둘 이상 줄 때 기본이 OR 라는 점이 가장 흔한 함정이며 「여러 조건을 줄 때의 OR 와 AND」 에서 다룹니다.

```bash
# holder.py 의 3번 파일과 tail 의 3번 파일이 나온다
# -p 에는 PID 를 쉼표로 여러 개 줄 수 있다(공백 없이)
lsof \
  -p $(pgrep -f holder.py),$(pgrep -x tail) \
  -a \
  -d 3
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
tail    3157 root    3r   REG   0,86 20971520       3 /dev/shm/lsof-lab/big.log
```

`^` 로 시작하는 PID 는 man 이 제외 항목이라 부르는 것입니다. 아래는 모든 프로세스의 작업 디렉터리 줄에서 PID 1 을 뺀 것이고 앞 세 줄만 봅니다.[^p]

```bash
# PID 1 을 뺀 작업 디렉터리 줄 가운데 앞 세 줄만 본다
#   ^PID   -p 에서 그 PID 를 제외한다
lsof -d cwd -p ^1 | head -3
```

```bash
COMMAND    PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3   3153    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3   3154    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# nc 가 둘 떠 있어 둘 다 나온다
lsof \
  -c nc \
  -a \
  -d cwd
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
nc      3155 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
nc      3156 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# 앞뒤를 슬래시로 감싸면 정규식이라 python3 프로세스가 모두 나온다
#   /정규식/   끝 슬래시 뒤에 i(대소문자 무시)·b(기본 정규식)를 붙일 수 있다
lsof \
  -c '/^py/' \
  -a \
  -d cwd
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3154    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3161 appuser  cwd    DIR   0,61       54 4353531 /home/appuser
python3 3162    root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
```

```bash
# 이름이 appuser 인 프로세스의 줄을 명령별로 센다
# awk 로 헤더를 건너뛰고 명령 이름과 사용자 열만 뽑는다
lsof -u appuser | awk 'NR>1{print $1,$3}' | sort | uniq -c
#      21 python3 appuser
```

```bash
# root 가 아닌 프로세스만 남는다
#   ^사용자   -u 에서 그 사용자를 제외한다
lsof -u ^root | awk 'NR>1{print $1,$3}' | sort | uniq -c
#      21 python3 appuser
```

```bash
# USER 열에 이름 대신 UID 1000 이 찍힌다
#   -l   USER 열에 이름 대신 UID 숫자를 찍는다 (이름 조회가 느릴 때도 쓴다)
lsof \
  -l \
  -a \
  -u appuser \
  -d cwd
```

```bash
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3161     1000  cwd    DIR   0,61       54 4353531 /home/appuser
```

### 이 파일을 연 프로세스 찾기

> 파일이나 디렉터리 이름이 먼저일 때는 그 이름을 인자로 줍니다.

```bash
# 파일 이름을 인자로 준다. 그 파일을 연 프로세스가 나오고 3w 로 쓰기 모드로 열려 있다
lsof logs/app.log
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
```

인자는 심볼릭 링크를 풀어 비교하므로 링크인 `/usr/bin/nc` 를 줘도 실제 파일 이름이 나옵니다.[^out]

```bash
# 실행 파일을 주면 그 프로그램을 돌리는 프로세스가 txt 로 나온다
# /usr/bin/nc 는 nc.openbsd 를 가리키는 링크다
# awk 로 COMMAND·PID·FD·NAME 열만 남긴다
lsof /usr/bin/nc | awk '{print $1,$2,$4,$NF}'
```

```bash
COMMAND PID FD NAME
nc 3155 txt /usr/bin/nc.openbsd
nc 3156 txt /usr/bin/nc.openbsd
```

```bash
# app.log·app.conf 두 줄이 나오고 하위 디렉터리 old/ 안의 파일은 보지 않는다
#   +d   그 디렉터리와 바로 아래 항목을 연 프로세스를 찾는다
lsof +d logs
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 logs/app.conf
```

```bash
# logs/old/app.log.1 까지 나온다
#   +D   디렉터리 아래를 끝까지 내려가며 찾는다
lsof +D logs
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root    3w   REG   0,61        6 4353537 logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 logs/old/app.log.1
```

`+D` 는 디렉터리 트리를 훑으므로 큰 트리에서는 느립니다. 이 둘은 심볼릭 링크를 따라가지 않고 하위 마운트 지점도 건너뜁니다.[^dir]

```bash
# cwd 와 3번 이상의 디스크립터가 나온다
# 범위는 0-2 처럼 줄 수 있다. 3번 이상만 보려면 3-99
lsof \
  -a \
  -p $(pgrep -f holder.py) \
  -d cwd,3-99
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

```bash
# 라이브러리 줄(mem·txt)을 빼면 읽을 줄이 준다
#   ^이름   모두 ^ 로 시작하면 제외 목록이다
lsof \
  -a \
  -p $(pgrep -f holder.py) \
  -d '^mem,^txt'
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 3153 root  cwd    DIR   0,61      110 4348937 /root/cmd-lab/lsof
python3 3153 root  rtd    DIR   0,61       42 4348902 /
python3 3153 root    0r   CHR    1,3      0t0       5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0  401170 pipe
python3 3153 root    3w   REG   0,61        6 4353537 /root/cmd-lab/lsof/logs/app.log
python3 3153 root    4w   REG   0,61        0 4353543 /root/cmd-lab/lsof/logs/app.conf
python3 3153 root    5w   REG   0,61        0 4353544 /root/cmd-lab/lsof/logs/old/app.log.1
```

`-d` 의 목록은 전부 포함이거나 전부 제외여야 하고 섞어 쓸 수 없습니다.[^fd]

### 지운 파일이 붙든 공간 찾기

> 로그를 `rm` 했는데 디스크가 비지 않으면 그 파일을 열어 둔 프로세스를 `lsof +L1` 로 찾고 `/proc/PID/fd` 로 비웁니다.

파일 이름(디렉터리 항목)을 지워도 어떤 프로세스가 그 파일을 열어 두었다면 파일 자체는 마지막 디스크립터가 닫힐 때까지 남아 공간이 돌아오지 않습니다.[^unlink] `df` 는 파일시스템 단위의 사용량을, `du` 는 디렉터리 아래 파일의 크기를 추정하므로 두 값이 어긋나면 이 상황을 의심합니다.[^dfdu]

```bash
# 지우기 전에는 df 와 du 가 모두 20M 쪽이다
# tmpfs 라 df 의 Used 가 파일 크기를 그대로 따른다
#   df -h   크기를 1024 의 거듭제곱 단위로 찍는다
#   du -s   인자마다 합계만 찍는다
#   du -h   크기를 사람이 읽는 단위로 찍는다
df -h /dev/shm; du -sh /dev/shm/lsof-lab
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G   20M  3.9G   1% /dev/shm
20M	/dev/shm/lsof-lab
```

```bash
# 파일을 지운다. tail -f 가 아직 열고 있다
rm /dev/shm/lsof-lab/big.log
```

```bash
# df 는 그대로 20M, du 는 파일이 사라진 만큼 줄었다
df -h /dev/shm; du -sh /dev/shm/lsof-lab
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G   20M  3.9G   1% /dev/shm
0	/dev/shm/lsof-lab
```

```bash
# 이제 tail 의 3번 파일이 지운 파일로 잡힌다. NLINK 열이 붙는다
lsof +L1
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NLINK NODE NAME
tail    3157 root    3r   REG   0,86 20971520     0    3 /dev/shm/lsof-lab/big.log (deleted)
```

`+L` 은 숫자 없이 쓰면 모든 줄에 링크 수를 붙이고 `+L1` 은 링크 수가 0 인 지운 파일을 골라 내며, NAME 끝의 `(deleted)` 와 NLINK 의 0 이 그 표지입니다.[^l1]

`/proc/PID/fd` 의 항목은 연 파일을 가리키는 심볼릭 링크라 지워진 파일도 `(deleted)` 가 붙은 채 보입니다.[^procfd]

```bash
# 3번이 지워진 파일이다 (lsof 없이도 확인)
ls -l /proc/$(pgrep -x tail)/fd
```

```bash
total 0
lr-x------ 1 root root 64 Nov 11 13:12 0 -> /dev/null
l-wx------ 1 root root 64 Nov 11 13:12 1 -> /dev/null
l-wx------ 1 root root 64 Nov 11 13:12 2 -> /root/cmd-lab/lsof/tail.err
lr-x------ 1 root root 64 Nov 11 13:12 3 -> /dev/shm/lsof-lab/big.log (deleted)
lr-x------ 1 root root 64 Nov 11 13:12 4 -> anon_inode:inotify
```

```bash
# 공간을 돌려받는 정석은 그 프로세스를 재시작해 디스크립터를 닫는 것이다
# 재시작할 수 없는 프로세스는 /proc/PID/fd/번호 를 열어 내용만 비운다
# 쓰기로 열면서 크기를 0 으로 만드는 리다이렉션 하나면 되고 프로세스는 그대로 돈다
: > /proc/$(pgrep -x tail)/fd/3
```

```bash
# tail 이 파일이 줄어든 것을 알아차렸다 (tail 의 오류 출력을 실습 준비에서 tail.err 로 받아 두었다)
sleep 1; cat tail.err    # tail: /dev/shm/lsof-lab/big.log: file truncated
```

```bash
# 공간이 돌아왔다
df -h /dev/shm
```

```bash
Filesystem      Size  Used Avail Use% Mounted on
shm             4.0G     0  4.0G   0% /dev/shm
```

```bash
# 파일은 여전히 열려 있지만 SIZE 가 0 이다. 프로세스를 끝내면 이 줄도 사라진다
lsof +L1
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NLINK NODE NAME
tail    3157 root    3r   REG   0,86        0     0    3 /dev/shm/lsof-lab/big.log (deleted)
```



## 주의사항과 동작 원리

> 조건을 둘 이상 주면 기본이 OR 이고, 컨테이너 안의 `lsof` 는 그 컨테이너 안에서만 보입니다.

### 여러 조건을 줄 때의 OR 와 AND

> 조건을 지정하면 기본으로 OR 로 묶이고, `-a` 를 붙여야 모두 만족하는 줄만 남습니다.

그래서 `-u appuser -i` 는 "appuser 의 파일 또는 모든 네트워크 파일"입니다.[^sel]

```bash
# appuser 의 파일 OR 모든 네트워크 파일. root 의 nc 와 http.server 까지 섞여 나온다
#   -i   인터넷 주소와 맞는 파일을 고른다. 주소가 없으면 네트워크 파일 전부다
lsof -u appuser -i | awk 'NR>1{print $1,$3}' | sort | uniq -c
```

```bash
      1 nc root
     21 python3 appuser
      3 python3 root
```

```bash
# 조건을 모두 만족하는 줄만 남는다. appuser 의 네트워크 파일 하나뿐이다
lsof \
  -a \
  -u appuser \
  -i
```

```bash
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser    3u  IPv4 406324      0t0  TCP localhost:tproxy (LISTEN)
```

`-a` 는 어디에 두든 모든 조건에 걸려 두 옵션 사이에 끼워도 그 쌍만 묶지 못하고, 같은 종류의 값(`-u a,b`, `-c x -c y`)은 먼저 OR 로 묶인 뒤 `-a` 와 만납니다.[^sel]

`-p` 와 `-d` 도 같은 규칙이라 `-a` 없이 쓰면 두 조건이 OR 가 되어 PID 와 무관한 프로세스의 파일 디스크립터까지 나옵니다.

```bash
# -p 와 -d 만 쓰면 OR: holder.py 의 모든 줄에 다른 프로세스의 0~2번까지 섞여 줄 수만 센다
lsof -p $(pgrep -f holder.py) -d 0-2 | wc -l    # 50
```

```bash
# -a 를 붙이면 holder.py 의 0~2번만
lsof \
  -a \
  -p $(pgrep -f holder.py) \
  -d 0-2
```

```bash
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
python3 3153 root    0r   CHR    1,3      0t0      5 /dev/null
python3 3153 root    1w  FIFO   0,15      0t0 401170 pipe
python3 3153 root    2w  FIFO   0,15      0t0 401170 pipe
```

### 컨테이너 안에서 보이는 범위

> 컨테이너 안의 `lsof` 는 그 컨테이너의 PID 이름공간 안만 보고, 다른 사용자의 프로세스를 읽으려면 권한도 필요합니다.

PID 이름공간은 프로세스 번호 공간을 나누고, `lsof` 가 읽는 `/proc` 은 마운트한 프로세스의 이름공간에서 보이는 프로세스만 담습니다.[^pidns]

다른 사용자의 `/proc/PID/fd` 링크는 ptrace 권한이 있어야 읽히는데[^procfd], 컨테이너에는 기본으로 `CAP_SYS_PTRACE` 가 없어[^cap] 준비 블록이 `--cap-add SYS_PTRACE` 를 씁니다.

```bash
# --cap-add SYS_PTRACE 없이 준비 블록을 돌린 컨테이너: appuser 의 줄은 NAME 에 오류가 찍힌다
lsof \
  -a \
  -u appuser \
  -d cwd,3
```

```bash
COMMAND  PID    USER   FD      TYPE DEVICE SIZE/OFF NODE NAME
python3 3161 appuser  cwd   unknown                      /proc/3161/cwd (readlink: Permission denied)
python3 3161 appuser    3   unknown                      /proc/3161/fd/3 (readlink: Permission denied)
```



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [lsof 포트와 스크립트용 출력](./lsof%20포트와%20스크립트용%20출력.md) — 이 시트의 「실습 준비」 를 돌린 상태에서 이어지는 포트와 연결 보기, `-t`·`-F`·`-r` 스크립트용 출력
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#lsof-의-두-방향) — `lsof` 로 포트에서 출발하는 법과 프로세스에서 출발하는 법의 원리
- [지워도 공간이 안 돌아오는 파일](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#지워도-공간이-안-돌아오는-파일) — 지운 로그가 디스크를 붙드는 원리와 logrotate 와의 관계

소켓 쪽을 보는 다른 도구는 `ss` 입니다.



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- lsof 4.95.0 의 `lsof -v`·`lsof -h` 출력 — Debian 12 컨테이너에서 2026-11-11 확인, 2026-11-13 종료 코드와 usage 줄을 다시 확인
- [lsof(8) — Debian bookworm](https://manpages.debian.org/bookworm/lsof/lsof.8.en.html)
- [proc(5) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/proc.5.en.html)
- [unlink(2) — Debian bookworm](https://manpages.debian.org/bookworm/manpages-dev/unlink.2.en.html)
- [pid_namespaces(7) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/pid_namespaces.7.en.html)
- [capabilities(7) — Debian bookworm](https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html)
- [df(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/df.1.en.html), [du(1) — Debian bookworm](https://manpages.debian.org/bookworm/coreutils/du.1.en.html)

[^out]: `man lsof` (lsof 4.95.0) OUTPUT — "COMMAND contains the first nine characters of the name of the UNIX command associated with the process.", "FD is the File Descriptor number of the file or: cwd current working directory; ... mem memory-mapped file; ... rtd root directory; ... txt program text (code and data)", "r for read access; w for write access; u for read and write access", "TYPE is the type of the node associated with the file", "IPv4 for an IPv4 socket", "DIR for a directory", "FIFO for a FIFO special file", "REG for a regular file", "unix for a UNIX domain socket", "DEVICE contains the device numbers, separated by commas, for a character special, block special, regular, directory or NFS file; ... or a kernel reference address that identifies the file", "SIZE/OFF ... the offset is normally displayed in decimal with a leading 0t if it contains 8 digits or less", "If the -s option is specified, lsof always displays the file size ... and labels the column SIZE.", "NODE is the node number of a local file; ... or the Internet protocol type - e.g, TCP", "or the name of a file specified in the names option (after any symbolic links have been resolved)". https://manpages.debian.org/bookworm/lsof/lsof.8.en.html
[^procfd]: `man 5 proc` 의 /proc/pid/fd/ 항목 (Linux man-pages 6.03) — "For file descriptors that have no corresponding inode (e.g., file descriptors produced by bpf(2), epoll_create(2), eventfd(2), inotify_init(2), ...), the entry will be a symbolic link with contents of the form anon_inode:file-type", "Permission to dereference or read (readlink(2)) the symbolic links in this directory is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2)." https://manpages.debian.org/bookworm/manpages/proc.5.en.html
[^K]: `man lsof` OPTIONS — `-K k` "selects the listing of tasks (threads) of processes, on dialects where task (thread) reporting is supported.", "If -K is followed by a value, k, it must be i. That causes lsof to ignore tasks, particularly in the default, list-everything case when no other options are specified."; OUTPUT "TID is the task (thread) IDentification number", "A blank TID column in Linux indicates a process - i.e., a non-task.", "TASKCMD is the task command name."
[^c]: `man lsof` OPTIONS — `-c c` "selects the listing of files for processes executing the command that begins with the characters of c.", `+c w` "defines the maximum number of initial characters of the name, supplied by the UNIX dialect, of the UNIX command associated with a process to be printed in the COMMAND column. (The lsof default is nine.)"; OUTPUT "If a non-zero w value is specified to the +c w option, the column contains the first w characters of the name of the UNIX command associated with the process up to the limit of characters supplied to lsof by the UNIX dialect.", "If a zero w value is specified to the +c w option, the column contains all the characters of the name of the UNIX command associated with the process." 15글자 한계는 이 환경에서 `+c 0` 출력으로 확인한 값입니다.
[^p]: `man lsof` OPTIONS — `-p s` "excludes or selects the listing of files for the processes whose optional process IDentification (PID) numbers are in the comma-separated set s - e.g., 123 or 123,^456. (There should be no spaces in the set.)", "PID numbers that begin with ^ (negation) represent exclusions."; `-u s` "selects the listing of files for the user whose login names or user ID numbers are in the comma-separated set s", `-l` "inhibits the conversion of user ID numbers to login names."
[^sel]: `man lsof` OPTIONS — "Normally, list options that are specifically stated are ORed - i.e., specifying the -i option without an address and the -ufoo option produces a listing of all network files OR files belonging to processes owned by user foo.", "The -a option may be used to AND the selections.", "Caution: the -a option causes all list selection options to be ANDed; it can't be used to cause ANDing of selected pairs of selection options by placing it between them, even though its placement there is acceptable. Wherever -a is placed, it causes the ANDing of all selection options.", "Items of the same selection set - command names, file descriptors, network addresses, process identifiers, user identifiers, zone names, security contexts - are joined in a single ORed set and applied before the result participates in ANDing."
[^dir]: `man lsof` OPTIONS — `+d s` "causes lsof to search for all open instances of directory s and the files and directories it contains at its top level. +d does NOT descend the directory tree, rooted at s.", `+D D` "causes lsof to search for all open instances of directory D and all the files and directories it contains to its complete depth.", "Processing of the +D option does not follow symbolic links within D unless the -x or -x l option is also specified. Nor does it search for open files on file system mount points on subdirectories of D unless the -x or -x f option is also specified.", "Further note: lsof may process this option slowly and require a large amount of dynamic memory to do it."
[^fd]: `man lsof` OPTIONS — `-d s` "specifies a list of file descriptors (FDs) to exclude from or include in the output listing. The file descriptors are specified in the comma-separated set s - e.g., cwd,1,3, ^6,^2.", "The list is an exclusion list if all entries of the set begin with ^. It is an inclusion list if no entry begins with ^. Mixed lists are not permitted.", "A file descriptor number range may be in the set as long as neither member is empty, both members are numbers, and the ending member is larger than the starting one - e.g., 0-7 or 3-10."
[^unlink]: `man 2 unlink` (Linux man-pages 6.03) — "If the name was the last link to a file but any processes still have the file open, the file will remain in existence until the last file descriptor referring to it is closed." https://manpages.debian.org/bookworm/manpages-dev/unlink.2.en.html
[^dfdu]: `man df` (coreutils 9.1) NAME — "df - report file system space usage"; `man du` NAME — "du - estimate file space usage". https://manpages.debian.org/bookworm/coreutils/df.1.en.html
[^l1]: `man lsof` OPTIONS — `+|-L [l]` "enables (+) or disables (-) the listing of file link counts, where they are available - e.g., they aren't available for sockets, or most FIFOs and pipes.", "When +L is followed by a number, only files having a link count less than that number will be listed. ... A specification of the form +L1 will select open files that have been unlinked."; OUTPUT "NLINK contains the file link count when +L has been specified".
[^pidns]: `man pid_namespaces` (Linux man-pages 6.03) — "PID namespaces isolate the process ID number space, meaning that processes in different PID namespaces can have the same PID.", "A /proc filesystem shows (in the /proc/pid directories) only processes visible in the PID namespace of the process that performed the mount, even if the /proc filesystem is viewed from processes in other namespaces." https://manpages.debian.org/bookworm/manpages/pid_namespaces.7.en.html
[^cap]: `man capabilities` (Linux man-pages 6.03) — `CAP_SYS_PTRACE` 항목 "Trace arbitrary processes using ptrace(2)". 컨테이너가 기본으로 이 capability 를 갖지 않는다는 것은 이 환경에서 `--cap-add` 없이 받은 출력으로 확인했습니다. https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html
[^exit]: `man lsof` DIAGNOSTICS (lsof 4.95.0) — "Lsof returns a one (1) if any error was detected, including the failure to locate command names, file names, Internet addresses or files, login names, NFS files, PIDs, PGIDs, or UIDs it was asked to list. If the -V option is specified, lsof will indicate the search items it failed to list. If the -Q option is specified, lsof will ignore any search item failures and only return an error if something unusual and unrecoverable happened.", "It returns a zero (0) if no errors were detected and if either the -Q option was specified or it was able to list some information about all the specified search arguments." https://manpages.debian.org/bookworm/lsof/lsof.8.en.html
