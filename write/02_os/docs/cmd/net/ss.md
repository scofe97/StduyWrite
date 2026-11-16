---
title: ss 참조 시트
tags: [linux, cheatsheet, ss, socket, tcp, network, cli, reference]
status: draft
source:
  - iproute2 ss(8) (iproute2 6.19.0, Ubuntu 26.04 의 `man ss` 와 `ss --help` 원문)
  - Linux man-pages sock_diag(7)
  - net-tools netstat(8)
related:
  - ../README.md
  - ../resource/lsof.md
  - ../resource/lsof 포트와 스크립트용 출력.md
  - ../resource/watch.md
  - ../ssh/ssh.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-16
---

# ss 참조 시트

---

> 커널이 쥔 소켓을 종류·상태·포트로 골라 보는 `ss` 의 사용법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `ss` 는 소켓 하나를 한 줄로 찍는 소켓 조회 명령입니다.

줄마다 상태, 받을·보낼 큐, 로컬과 상대 주소를 보이고, 마지막 인자의 필터 표현으로 포트와 상태를 좁힙니다. 옵션 없이 치면 듣는 소켓이 빠지고 연결이 맺어진 소켓만 나옵니다.[^default]

iproute2 패키지의 외부 바이너리입니다(`dpkg -S` 결과 `iproute2: /usr/bin/ss`). 이 시트는 OrbStack 의 Linux VM(Ubuntu 26.04, iproute2 6.19.0)에서 실측했습니다.

옛 도구 `netstat` 는 이 VM 에 net-tools 패키지로 깔려 있습니다(`net-tools: /usr/bin/netstat`). 그 매뉴얼이 `ss` 를 대체재로 적습니다. macOS 에는 `ss` 가 없습니다.[^env]



## 핵심 문법

> 종류 옵션(`-t`·`-u`·`-x`)과 상태 옵션(`-l`·`-a`)으로 소켓을 고르고, 마지막 인자의 필터 표현으로 포트와 주소를 좁힙니다.

```bash
# 호출 형태
Usage: ss [ OPTIONS ]
       ss [ OPTIONS ] [ FILTER ]

# 연결이 맺어진 소켓을 모든 종류로 본다 (기본 출력의 범위)
ss

# 듣는 TCP 소켓을 포트 숫자로 본다 (듣는 포트 보기)
ss -tln

# 듣는 소켓과 연결 소켓을 함께 보고 TCP 상태로 거른다 (연결 상태로 거르기)
ss -tan state established

# 포트·주소 조건으로 좁힌다 (필터 표현으로 좁히기)
ss -tn 'sport = :80'

# 큐 두 열을 읽는다 (소켓 큐 읽기)
ss -tln 'sport = :18435'

# 소켓을 쥔 프로세스를 붙인다 (프로세스 붙이기)
ss -tlnp

# 종류별 합계를 본다 (요약 보기)
ss -s

# TCP 연결의 내부 값과 메모리를 본다 (TCP 내부 정보 보기)
ss -tni

# 유닛 소켓을 본다 (유닛 소켓 보기)
ss -xa

# 머리 줄을 빼고 다른 명령으로 센다 (다른 명령과 조합하기)
ss -Htn 'dport = :18435' | wc -l
```

### 필터 표현

> 마지막 인자로 주는 `state` 와 조건식입니다. 본문에 나온 것만 모았습니다.

뜻은 `man ss` 의 STATE-FILTER 와 EXPRESSION 을 따랐습니다.[^filter]

```bash
# FILTER := [ state STATE-FILTER ] [ EXPRESSION ]
# state established   TCP 상태가 established 인 소켓만 고른다
# state listening     듣는 소켓만 고른다
# exclude listening   그 상태를 뺀다
# sport = :80         로컬(source) 포트가 80 이다. :http 처럼 이름도 된다
# dport = :80         상대(destination) 포트가 80 이다
# dst 127.0.0.1       상대 주소가 127.0.0.1 이다 (로컬은 src)
# src PATH            로컬 경로가 PATH 인 유닛 소켓이다 (-x 와 함께)
# <  <=  =  !=  >=  > 포트를 비교하는 연산자다. 생략하면 = 다
# and  or  ( )        조건을 잇고 묶는다. 연산자 없이 이으면 and 다
```



## 종료 코드

> 매뉴얼에 종료 코드 절이 없어 실측한 값만 싣습니다.[^no-exit]

```bash
# 0    조회를 마쳤다
# 1    필터 표현의 값을 해석하지 못했다
# 255  모르는 옵션을 줬다

# -V 는 버전 정보를 찍는다 (--version)
ss -V; echo $?    # ss utility, iproute2-6.19.0 / 0

# 모르는 옵션은 오류 줄 뒤에 사용법 전체를 찍는다. 첫 줄만 본다
ss --badopt 2>&1 | head -1    # ss: unrecognized option '--badopt'
ss --badopt > /dev/null 2>&1; echo $?    # 255

# 포트가 아닌 값을 필터에 주면 오류 두 줄을 찍는다
ss 'sport = :abc'; echo $?
```

```bash
Error: "abc" does not look like a port.
Cannot parse dst/src address.
1
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 소켓만 씁니다.

### 실습 준비

> 아래 블록을 Linux 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 서버와 연결이 모두 뜹니다.

OrbStack 의 Linux VM 에서 root 로 실행합니다. 「프로세스 붙이기」 의 `setpriv` 예가 appuser 를 씁니다.

```bash
mkdir -p ~/cmd-lab/ss && cd ~/cmd-lab/ss

# 패키지. iproute2 가 ss 를, netcat-openbsd 가 nc 를, python3-minimal 이
# 서버·클라이언트 스크립트를 돌릴 python3 을, netbase 가 /etc/services 를 준다
# 80 이 http 로 보이는 것이 /etc/services 덕이다
apt-get -qq update >/dev/null 2>&1; \
  apt-get -qq install -y \
  iproute2 netcat-openbsd python3-minimal netbase >/dev/null 2>&1

# 다른 사용자(appuser) 소유의 소켓을 만들 때 쓴다. 「프로세스 붙이기」 가 쓴다
id appuser >/dev/null 2>&1 || useradd -m appuser

# 띄운 프로세스의 PID 는 pids 에 모아 「실습 정리」 에서 끈다
rm -f pids
mkdir -p www
echo hello > www/index.html

# http.server 가 IPv4 와 IPv6 의 80 포트를 듣는다
# 「듣는 포트 보기」 부터 여러 곳에서 쓴다
python3 -m http.server 80 --directory www --bind 127.0.0.1 >/dev/null 2>&1 &
echo $! >> pids
python3 -m http.server 80 --directory www --bind ::1 >/dev/null 2>&1 &
echo $! >> pids

# nc 가 UDP 18433 포트와 유닛 소켓 app.sock 을 각각 듣는다
# 「필터 표현으로 좁히기」 와 「유닛 소켓 보기」 가 쓴다
nc -u -l 127.0.0.1 18433 >/dev/null 2>&1 &
echo $! >> pids
nc -lU ~/cmd-lab/ss/app.sock >/dev/null 2>&1 &
echo $! >> pids

# hold.py 는 서버에 붙어 연결 하나를 유지한다. 인자는 주소와 포트다
# send.py 는 붙은 뒤 3MB 를 보낸다. 받는 쪽이 읽지 않으면 중간에서 멈춘다
cat > hold.py << 'EOF2'
import socket, sys, time
s = socket.create_connection((sys.argv[1], int(sys.argv[2])))
time.sleep(600)
EOF2
cat > send.py << 'EOF2'
import socket, sys
s = socket.create_connection((sys.argv[1], int(sys.argv[2])))
s.sendall(b'x' * 3000000)
EOF2

# backlog.py 는 18435 를 듣지만 accept 를 부르지 않는다. 백로그는 2 다
# noread.py 는 18436 에서 연결 하나를 받고 읽지 않는다
# 「소켓 큐 읽기」 가 쓴다
cat > backlog.py << 'EOF2'
import socket, time
s = socket.socket()
s.bind(('127.0.0.1', 18435))
s.listen(2)
time.sleep(600)
EOF2
cat > noread.py << 'EOF2'
import socket, time
s = socket.socket()
s.bind(('127.0.0.1', 18436))
s.listen(1)
conn, _ = s.accept()
time.sleep(600)
EOF2
python3 backlog.py &
echo $! >> pids
python3 noread.py &
echo $! >> pids
sleep 1

# 80 포트에 연결 하나를 붙여 둔다. 「기본 출력의 범위」 부터 쓴다
python3 hold.py 127.0.0.1 80 &
echo $! >> pids
sleep 1
```

`pids` 에는 띄운 프로세스의 PID 가 한 줄씩 쌓입니다. 서버는 모두 `127.0.0.1` 과 `::1` 에만 묶여 밖에서 보이지 않습니다.

### 기본 출력의 범위

> 옵션 없이 치면 연결이 맺어진 소켓이 TCP·UDP·유닛 소켓 구분 없이 나옵니다.

유닛 소켓이 많아 앞 세 줄만 봅니다. `2>/dev/null` 은 이 VM 이 찍는 오류 줄을 숨기는 것으로, 이유는 「RTNETLINK 오류 줄」 에 있습니다.

```bash
ss 2>/dev/null | head -3
```

```bash
Netid State  Recv-Q Send-Q                                         Local Address:Port      Peer Address:Port
u_dgr ESTAB  0      0                                                          * 40132                * 40133
u_dgr ESTAB  0      0                                                          * 32995                * 30338
```

듣는 소켓은 `-l` 이나 `-a` 를 줘야 나옵니다.[^default] TCP 만 보려면 `-t` 를 주며, 같은 연결이 양 끝 두 줄로 나옵니다.

```bash
# 연결이 맺어진 TCP 소켓만 본다
#   -t   TCP 소켓만 보인다
ss -t
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:http     127.0.0.1:36114
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:http
```

위 출력의 `36114` 는 클라이언트가 받은 임시 포트라 실행마다 다릅니다.

### 듣는 포트 보기

> `-l` 로 듣는 소켓만 고르고, `-n` 으로 서비스 이름 대신 포트 숫자를 찍습니다.

`ss` 는 `/etc/services` 에 이름이 있는 포트를 이름으로 바꿔 찍으므로, 80 이 `http` 로 나옵니다.

```bash
# 듣는 TCP 소켓을 본다
#   -l   듣는 소켓만 보인다
ss -tl
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      5          127.0.0.1:http       0.0.0.0:*
LISTEN 0      4096       127.0.0.1:33189      0.0.0.0:*
LISTEN 0      2          127.0.0.1:18435      0.0.0.0:*
LISTEN 0      1          127.0.0.1:18436      0.0.0.0:*
LISTEN 0      5              [::1]:http          [::]:*
```

```bash
# 포트를 숫자로 찍는다. http 가 80 으로 바뀐다
#   -n   서비스 이름을 풀지 않는다 (--numeric)
ss -tln
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      5          127.0.0.1:80         0.0.0.0:*
LISTEN 0      4096       127.0.0.1:33189      0.0.0.0:*
LISTEN 0      2          127.0.0.1:18435      0.0.0.0:*
LISTEN 0      1          127.0.0.1:18436      0.0.0.0:*
LISTEN 0      5              [::1]:80            [::]:*
```

`Local Address:Port` 의 `[::1]:80` 은 IPv6 루프백입니다. 33189 는 이 VM 이 원래 듣던 포트이고, `Send-Q` 열의 숫자는 「소켓 큐 읽기」 에서 읽습니다.

### 연결 상태로 거르기

> `-a` 로 듣는 소켓과 연결 소켓을 함께 보고, `state` 키워드로 TCP 상태를 골라 냅니다.

```bash
# 듣는 소켓과 맺어진 연결을 함께 본다
#   -a   듣는 소켓과 듣지 않는 소켓을 모두 보인다 (--all)
ss -tan
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      5          127.0.0.1:80         0.0.0.0:*
LISTEN 0      4096       127.0.0.1:33189      0.0.0.0:*
LISTEN 0      2          127.0.0.1:18435      0.0.0.0:*
LISTEN 0      1          127.0.0.1:18436      0.0.0.0:*
ESTAB  0      0          127.0.0.1:80       127.0.0.1:36114
ESTAB  0      0          127.0.0.1:36114    127.0.0.1:80
LISTEN 0      5              [::1]:80            [::]:*
```

```bash
# 맺어진 연결만 본다. 상태를 하나로 골라서 State 열이 빠진다
ss -tan state established
```

```bash
Recv-Q Send-Q Local Address:Port  Peer Address:Port
0      0          127.0.0.1:80       127.0.0.1:36114
0      0          127.0.0.1:36114    127.0.0.1:80
```

```bash
# 듣는 소켓만 뺀다. 상태가 여럿 남아 State 열이 돌아온다
ss -tan exclude listening
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:80       127.0.0.1:36114
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:80
```

### 필터 표현으로 좁히기

> `sport`·`dport` 로 포트를, `src`·`dst` 로 주소를 좁히고, `and`·`or` 와 괄호로 조건을 잇습니다.

포트 앞에는 `:` 를 붙이고, 이름(`:http`)으로도 줄 수 있습니다.[^filter]

```bash
# 로컬 포트가 80 인 듣는 소켓을 고른다
ss -tln 'sport = :80'
```

```bash
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      5          127.0.0.1:80        0.0.0.0:*
LISTEN 0      5              [::1]:80           [::]:*
```

```bash
# 서비스 이름으로 줘도 위와 같은 두 줄이 나온다. -n 은 출력만 숫자로 바꾼다
ss -tln 'sport = :http'

# 상대 포트가 80 인 줄은 연결을 건 클라이언트 쪽 하나다
ss -tn 'dport = :80'
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:80
```

```bash
# 어느 쪽이든 80 포트인 연결을 양 끝 모두 본다. 괄호는 따옴표로 감싼다
ss -tn '( sport = :80 or dport = :80 )'
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:80       127.0.0.1:36114
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:80
```

```bash
# 상대 주소로 거른다. 연결이 모두 루프백이라 위와 같은 두 줄이 나온다
ss -tn dst 127.0.0.1

# UDP 소켓은 -u 로 고른다
#   -u   UDP 소켓만 보인다
ss -uln 'sport = :18433'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
UNCONN 0      0          127.0.0.1:18433      0.0.0.0:*
```

```bash
# 포트 범위는 비교 연산자와 and 로 준다. 따옴표로 > 와 < 를 셸에서 지킨다
ss -tln 'sport >= :18000 and sport <= :18999'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      2          127.0.0.1:18435      0.0.0.0:*
LISTEN 0      1          127.0.0.1:18436      0.0.0.0:*
```

### 소켓 큐 읽기

> `Recv-Q`·`Send-Q` 는 듣는 소켓에서는 대기 연결 수와 백로그 크기, 맺어진 소켓에서는 읽지 않은 바이트와 확인되지 않은 바이트입니다.

`sock_diag(7)` 는 듣는 소켓의 두 값을 "the number of pending connections" 와 "the backlog size" 로 적습니다. `netstat(8)` 은 맺어진 소켓의 두 값을 바이트 수로 적습니다.[^queue] 큐가 쌓일 때 어느 쪽을 의심하는지는 [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#ss-의-소켓-큐)에 있습니다.

```bash
# 듣는 소켓. 대기 연결이 없으면 Recv-Q 는 0 이고 Send-Q 는 listen 의 백로그 2 다
ss -tln 'sport = :18435'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      2          127.0.0.1:18435      0.0.0.0:*
```

```bash
# accept 를 부르지 않는 서버에 클라이언트 셋을 붙인다
for i in 1 2 3; do
  python3 hold.py 127.0.0.1 18435 &
  echo $! >> pids
done
sleep 1

# 맺어졌지만 아직 accept 하지 않은 연결 3 개가 Recv-Q 에 쌓인다
ss -tln 'sport = :18435'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 3      2          127.0.0.1:18435      0.0.0.0:*
```

백로그가 2 인데 3 이 쌓였습니다. 이 VM 에서는 세 연결이 모두 맺어졌습니다.

```bash
# 읽지 않는 서버(noread.py)에 3MB 를 보낸다. 서버가 읽지 않아 중간에서 멈춘다
python3 send.py 127.0.0.1 18436 &
echo $! >> pids
sleep 1

# 서버 쪽 줄은 Recv-Q 에, 클라이언트 쪽 줄은 Send-Q 에 바이트가 쌓인다
ss -tn 'sport = :18436 or dport = :18436'
```

```bash
State Recv-Q Send-Q  Local Address:Port  Peer Address:Port
ESTAB 126949 0           127.0.0.1:18436    127.0.0.1:54304
ESTAB 0      2483846     127.0.0.1:54304    127.0.0.1:18436
```

두 숫자는 커널이 버퍼를 잡는 대로 실행마다 달라집니다.

### 프로세스 붙이기

> `-p` 는 소켓을 쥔 프로세스를 붙이고, 남의 소켓은 root 권한이 있어야 보입니다.

```bash
# 소켓을 쥔 프로세스를 붙인다. root 로 치면 모두 보인다
#   -p   소켓을 쓰는 프로세스를 보인다 (--processes)
ss -tlnp 'sport = :80'
```

```bash
State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
LISTEN 0      5          127.0.0.1:80        0.0.0.0:*    users:(("python3",pid=61290,fd=3))
LISTEN 0      5              [::1]:80           [::]:*    users:(("python3",pid=61291,fd=3))
```

`users:(("python3",pid=61290,fd=3))` 는 프로세스 이름, PID, 그 프로세스가 소켓을 쥔 파일 디스크립터 번호입니다.

```bash
# appuser 권한으로 같은 명령을 친다. setpriv 는 다른 권한으로 명령을 실행한다
# root 소유 서버라 Process 열이 빈다
setpriv --reuid=appuser --regid=appuser --init-groups \
  ss -tlnp 'sport = :80'
```

```bash
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      5          127.0.0.1:80        0.0.0.0:*
LISTEN 0      5              [::1]:80           [::]:*
```

```bash
# appuser 가 연 서버는 appuser 의 ss 에도 프로세스까지 보인다
setpriv --reuid=appuser --regid=appuser --init-groups \
  python3 -m http.server 18438 --directory /tmp --bind 127.0.0.1 \
  >/dev/null 2>&1 &
echo $! >> pids
sleep 1
setpriv --reuid=appuser --regid=appuser --init-groups \
  ss -tlnp 'sport = :18438 or sport = :80'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
LISTEN 0      5          127.0.0.1:80         0.0.0.0:*
LISTEN 0      5          127.0.0.1:18438      0.0.0.0:*    users:(("python3",pid=61377,fd=3))
LISTEN 0      5              [::1]:80            [::]:*
```

### 요약 보기

> `-s` 는 소켓 목록을 읽지 않고 종류별 합계만 찍습니다.[^summary]

```bash
# 종류별 합계를 찍는다. 수는 실행할 때마다 다르다
#   -s   요약 통계를 찍는다 (--summary)
ss -s
```

```bash
Total: 169
TCP:   65 (estab 10, closed 49, orphaned 0, timewait 0)

Transport Total     IP        IPv6
RAW       1         0         1
UDP       2         2         0
TCP       16        15        1
INET      19        17        2
FRAG      0         0         0
```

### TCP 내부 정보 보기

> `-i` 는 연결의 TCP 내부 값을, `-m` 은 소켓 메모리를, `-e` 는 소켓 식별 값을 줄 끝에 덧붙입니다.

```bash
# 클라이언트 쪽 연결의 내부 값을 본다
#   -i   TCP 내부 정보를 보인다 (--info)
ss -tni 'dport = :80'
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:80
	 cubic wscale:10,10 rto:200 rtt:0.082/0.041 mss:32741 pmtu:65535 rcvmss:536 advmss:65483 cwnd:10 bytes_acked:1 segs_out:2 segs_in:1 send 31942439024bps lastsnd:4105 lastrcv:4105 lastack:4105 pacing_rate 63884878048bps delivered:1 app_limited rcv_space:65495 rcv_ssthresh:65495 minrtt:0.082 snd_wnd:65483 rcv_wnd:65536
```

`rto` 는 재전송 타임아웃(ms)이고 `rtt` 는 평균 왕복 시간과 그 편차(ms)입니다. `mss` 는 최대 세그먼트 크기, `cwnd` 는 혼잡 윈도 크기, `bytes_acked` 는 상대가 확인한 바이트입니다.[^info]

```bash
# 소켓이 쓰는 메모리를 본다
#   -m   소켓 메모리 사용량을 보인다 (--memory)
ss -tnm 'dport = :80'
```

```bash
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0          127.0.0.1:36114    127.0.0.1:80
	 skmem:(r0,rb131072,t0,tb2626560,f0,w0,o0,bl0,d0)
```

`skmem` 의 `rb` 는 받기 버퍼에 쓸 수 있는 전체 메모리, `tb` 는 보내기 버퍼에 쓸 수 있는 전체 메모리입니다.[^info]

```bash
# appuser 소유 서버의 식별 값을 본다
#   -e   소켓 상세 정보를 보인다 (--extended)
ss -tlne 'sport = :18438'

# root 소유 서버에는 uid 가 찍히지 않았다. IPv6 소켓은 v6only 가 더 붙는다
ss -tlne 'sport = :80'
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      5          127.0.0.1:18438      0.0.0.0:*    uid:1000 ino:1567589 sk:a cgroup:/.lxc <->
```

```bash
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      5          127.0.0.1:80        0.0.0.0:*    ino:1570143 sk:302e cgroup:/.lxc <->
LISTEN 0      5              [::1]:80           [::]:*    ino:1571864 sk:3031 cgroup:/.lxc v6only:1 <->
```

`-e` 의 형식은 `uid:<uid_number> ino:<inode_number> sk:<cookie>` 입니다.[^info]

### 유닛 소켓 보기

> `-x` 는 유닛 소켓만 고르고, 로컬 주소 칸에 포트 대신 경로가 찍힙니다.

```bash
# 유닛 소켓 서버에 클라이언트를 붙인다
nc -U app.sock < /dev/null &
echo $! >> pids
sleep 1

# 이 경로를 로컬로 쥔 유닛 소켓을 모두 본다
#   -x   유닛 소켓만 보인다 (--unix)
ss -xa "src $PWD/app.sock"
```

```bash
Netid State  Recv-Q Send-Q             Local Address:Port    Peer Address:Port
u_str LISTEN 0      5      /root/cmd-lab/ss/app.sock 1571859            * 0
u_str ESTAB  0      0      /root/cmd-lab/ss/app.sock 1571860            * 1566366
```

`LISTEN` 줄이 서버가 듣는 소켓이고 `ESTAB` 줄이 붙은 클라이언트와 맺은 쪽입니다. 경로는 실습 준비를 돌린 홈 디렉터리에 따라 달라집니다.

### 다른 명령과 조합하기

> `-H` 로 머리 줄을 빼면 출력이 데이터만 남아 `awk`·`wc` 로 셀 수 있습니다.

```bash
# 상태별로 소켓 수를 센다. awk 가 첫 열(상태)만 뽑고 uniq 가 센다
#   -H        머리 줄을 찍지 않는다 (--no-header)
#   uniq -c   같은 줄이 몇 번 나왔는지 앞에 붙인다
ss -tanH | awk '{print $1}' | sort | uniq -c
```

```bash
     10 ESTAB
      6 LISTEN
```

```bash
# 18435 포트에 붙은 연결 수를 센다
ss -Htn 'dport = :18435' | wc -l    # 3
```

### 실습 정리

```bash
# 띄운 프로세스를 끄고 appuser 와 실습 폴더를 지운다
kill $(cat pids)
pkill -u appuser
sleep 1
userdel -r appuser 2>/dev/null
cd ~ && rm -rf ~/cmd-lab/ss
```



## 주의사항과 동작 원리

### 일치하는 소켓이 없어도 종료 코드는 0

> 조건에 맞는 소켓이 없어도 `ss` 는 머리 줄만 찍고 0 을 돌려주므로, 스크립트는 줄 수로 판정합니다.

```bash
# 9 포트를 듣는 소켓은 없다. 머리 줄만 나오고 종료 코드는 0 이다
ss -tln 'sport = :9'; echo $?
```

```bash
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
0
```

```bash
# 머리 줄을 빼고 줄 수를 세면 0 이다. 소켓이 있으면 1 이상이다
ss -Htln 'sport = :9' | wc -l    # 0
```

### RTNETLINK 오류 줄

> 이 VM 에서는 `ss -a` 가 표준 오류에 `RTNETLINK answers: Invalid argument` 를 찍지만 목록은 정상으로 나오고 종료 코드는 0 입니다.

```bash
# 표준 출력은 버리고 표준 오류만 본다
ss -a 2>&1 >/dev/null; echo $?    # RTNETLINK answers: Invalid argument / 0

# DCCP 소켓만 조회해도 같은 줄이 나온다
ss -d; echo $?
```

```bash
RTNETLINK answers: Invalid argument
State Recv-Q Send-Q Local Address:Port Peer Address:Port
0
```

`-t`·`-u`·`-x`·`-w`·`-0`·`-S`·`-M` 로 한 종류씩 조회할 때는 이 줄이 나오지 않았습니다. 이 VM 의 커널이 DCCP 조회를 받지 않는 것으로 보이며, `2>/dev/null` 로 이 줄을 숨길 수 있습니다.

### 괄호 필터의 따옴표

> `( … )` 는 셸 문법이라 따옴표 없이 주면 `ss` 에 닿기 전에 셸이 구문 오류로 거부합니다.

```bash
# 따옴표 없는 괄호는 bash 가 거부한다. 새 bash 로 쳐서 오류만 본다
bash -c 'ss -tn ( sport = :80 or dport = :80 )'
```

```bash
bash: -c: line 1: syntax error near unexpected token `('
bash: -c: line 1: `ss -tn ( sport = :80 or dport = :80 )'
```

「필터 표현으로 좁히기」 처럼 표현 전체를 작은따옴표로 감싸면 `ss` 가 괄호를 받습니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트입니다.

- [lsof 참조 시트](../resource/lsof.md) — 소켓에서 출발하는 `ss -p` 와 달리 열린 파일 목록에서 소켓을 거르는 법
- [lsof 포트와 스크립트용 출력](../resource/lsof%20포트와%20스크립트용%20출력.md) — 포트에서 출발해 그 포트를 쥔 프로세스를 찾는 법
- [watch 참조 시트](../resource/watch.md) — `ss` 같은 명령을 일정 간격으로 다시 실행해 큐가 쌓이는 모양을 볼 때
- [ssh 접속·config·포트 포워딩 참조 시트](../ssh/ssh.md) — 포트 포워딩 뒤 `ss -ltn` 으로 열린 포트를 확인하는 예
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#ss-의-소켓-큐) — `Recv-Q` 가 쌓이는 모양과 읽는 법의 원리



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04 LTS, iproute2 6.19.0-1ubuntu1.1, net-tools 2.10-2ubuntu1 — 2026-11-16 실측
- [ss(8) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/en/man8/ss.8.html)
- [sock_diag(7)](https://man7.org/linux/man-pages/man7/sock_diag.7.html)
- [netstat(8) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html)

[^default]: `man ss` (iproute2 6.19.0) OPTIONS — "When no option is used ss displays a list of open non-listening sockets (e.g. TCP/UNIX/UDP) that have established connection.", `-l` "Display only listening sockets (these are omitted by default).", `-a` "Display both listening and non-listening (for TCP this means established connections) sockets." <https://manpages.ubuntu.com/manpages/resolute/en/man8/ss.8.html>
[^env]: `man netstat` (net-tools 2.10) — "This program is mostly obsolete. Replacement for netstat is ss." <https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html> macOS 26.6.2 에서 `command -v ss` 가 아무것도 찍지 않았습니다(이 시트의 실측).
[^filter]: `man ss` (iproute2 6.19.0) — "STATE-FILTER allows one to construct arbitrary set of states to match. Its syntax is sequence of keywords state and exclude followed by identifier of state.", "EXPRESSION allows filtering based on specific criteria.", "{dst|src} [=] HOST", "{dport|sport} [OP] [FAMILY:]:PORT", "Compare the destination or source port to PORT. OP can be any of "<", "<=", "=", "!=", ">=" and ">".", 예 "ss -x src /tmp/.X11-unix/*". `:http` 처럼 이름을 주는 것은 이 시트의 실측입니다. <https://manpages.ubuntu.com/manpages/resolute/en/man8/ss.8.html>
[^no-exit]: `ss(8)` 의 man 에는 종료 코드 절이 없습니다. 아래 값은 Ubuntu 26.04 VM 에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^queue]: `man sock_diag` (Linux man-pages) `idiag_rqueue` — "For listening sockets: the number of pending connections.", "For other sockets: the amount of data in the incoming queue."; `idiag_wqueue` — "For listening sockets: the backlog size." <https://man7.org/linux/man-pages/man7/sock_diag.7.html> `man netstat` (net-tools 2.10) Recv-Q — "Established: The count of bytes not copied by the user program connected to this socket.", Send-Q — "Established: The count of bytes not acknowledged by the remote host." netstat 는 듣는 소켓의 Recv-Q 를 "the current syn backlog" 로 적지만, 이 시트에서 대기 연결 3 개를 만들자 3 이 나와 sock_diag(7) 의 설명과 맞았습니다. <https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html>
[^summary]: `man ss` (iproute2 6.19.0) `-s` — "Print summary statistics. This option does not parse socket lists obtaining summary from various sources." <https://manpages.ubuntu.com/manpages/resolute/en/man8/ss.8.html>
[^info]: `man ss` (iproute2 6.19.0) — `-i` "Show internal TCP information.", `rto:<icsk_rto>` "tcp re-transmission timeout value, the unit is millisecond", `rtt:<rtt>/<rttvar>` "rtt is the average round trip time, rttvar is the mean deviation of rtt, their units are millisecond", `mss:<mss>` "max segment size", `cwnd:<cwnd>` "congestion window size", `bytes_acked:<bytes_acked>` "bytes acked"; `-m` "Show socket memory usage.", `<rcv_buf>` "the total memory can be allocated for receiving packet", `<snd_buf>` "the total memory can be allocated for sending packet"; `-e` "Show detailed socket information." <https://manpages.ubuntu.com/manpages/resolute/en/man8/ss.8.html>
