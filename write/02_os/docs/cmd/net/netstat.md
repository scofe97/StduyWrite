---
title: netstat 참조 시트
tags: [linux, cheatsheet, netstat, socket, network, cli, reference]
status: draft
source:
  - net-tools netstat(8) (net-tools 2.10, OrbStack Ubuntu 26.04 VM 의 `netstat --help` 와 `man netstat` 원문)
  - net-tools route(8)
  - iproute2 ss(8)·nstat(8)
related:
  - ../README.md
  - ./ss.md
  - ../resource/watch.md
  - ../shell/timeout.md
  - ../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md
updated: 2026-11-16
---

# netstat 참조 시트

---

> 소켓·라우팅 표·인터페이스 표·프로토콜 통계를 옵션 하나로 갈라 보는 `netstat` 의 사용법과 `ss`·`ip` 대응을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `netstat` 는 소켓 목록과 라우팅 표, 인터페이스 표, 프로토콜 통계를 한 명령으로 찍는 옛 네트워크 조회 명령입니다.

net-tools 패키지의 외부 바이너리입니다(`dpkg -S` 결과 `net-tools: /usr/bin/netstat`). 이 시트는 OrbStack 의 Linux VM(Ubuntu 26.04, net-tools 2.10-2ubuntu1)에서 실측했습니다. 이 VM 에는 net-tools 가 이미 깔려 있었습니다. 매뉴얼이 스스로 "mostly obsolete" 라고 적고 대체 명령으로 `ss` 와 `ip` 를 가리킵니다.[^env]

`ubuntu:26.04` 컨테이너 이미지에는 net-tools 가 없어 `netstat` 가 명령 없음(127)으로 끝납니다. macOS 의 `netstat` 는 다른 판이라 `-p` 가 프로토콜 이름을 받습니다.[^bsd] 그래서 `-tulpn` 이 그대로 통하지 않습니다(「net-tools 가 없거나 다른 판일 때」). 소켓 큐 열의 원리는 [ss 참조 시트](./ss.md)와 책 노트에 있고, 이 시트는 옛 도구의 옵션과 `ss`·`ip` 대응을 다룹니다.



## 핵심 문법

> 소켓 종류(`-t`·`-u`)와 상태 범위(`-l`·`-a`)로 소켓 목록을 고르고, `-r`·`-i`·`-s` 로 다른 표로 바꿉니다.

```bash
# 호출 형태 (netstat --help 의 usage)
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
       netstat [-vWnNcaeol] [<Socket> ...]
       netstat { [-vWeenNac] -i | [-cnNe] -M | -s [-6tuw] }

# 듣는 TCP·UDP 소켓을 숫자와 프로세스로 본다 (듣는 포트와 프로세스 보기)
netstat -tulpn

# 듣는 소켓과 연결 소켓을 함께 본다 (연결까지 보기)
netstat -tanp

# 이름 해석을 켜고 본다 (이름 해석과 숫자 주소)
netstat -tulp

# 표를 매초 다시 찍는다 (매초 다시 찍기)
netstat -ctlpn

# 소유자·타이머 열을 붙인다 (소유자·타이머 열 붙이기)
netstat -tlpne
netstat -tlno

# 라우팅 표를 본다 (라우팅 표 보기)
netstat -rn

# 인터페이스 표를 본다 (인터페이스 표 보기)
netstat -i

# 프로토콜 통계를 본다 (프로토콜 통계 보기)
netstat -s
```



## 종료 코드

> 매뉴얼에 종료 코드 절이 없어서 실측한 값만 싣습니다.[^no-exit]

```bash
# 0    조회에 성공했을 때
# 1    알 수 없는 주소 계열을 -A 로 줬을 때
# 3    알 수 없는 옵션을 줬을 때 (usage 를 찍은 뒤)
# 127  netstat 가 없을 때 (셸이 정한 코드)
#      「net-tools 가 없거나 다른 판일 때」 에서 재현한다

# 「실습 준비」 의 네임스페이스 셸에서 돌린 값이다
#   -A   보일 주소 계열을 고른다 (inet, inet6, unix 처럼)
netstat -A foo; echo "exit=$?"
# Unknown address family `foo'.
# exit=1

netstat --nonexist > /dev/null; echo "exit=$?"
```

```bash
netstat: unrecognized option '--nonexist'
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
...
exit=3
```

`unrecognized option` 줄과 usage 는 오류 출력이라 `> /dev/null` 로 가려지지 않고 화면에 남습니다. 위 블록은 usage 를 첫 줄만 남기고 줄였습니다.



## 유스케이스

### 실습 준비

> 아래 블록을 VM 의 Linux 셸에 차례로 붙여 넣으면 문서용 주소만 쓰는 네임스페이스와 듣는 서버 넷이 생깁니다.

VM 의 실제 인터페이스와 라우팅을 건드리지 않으려고 네트워크 네임스페이스 `nslab` 안에서 돌립니다. 둘째 블록부터는 모두 첫 블록 끝에서 연 root 셸에서 칩니다.

```bash
# 네임스페이스 nslab 과 veth 한 쌍을 만든다 (라우팅 표 보기, 인터페이스 표 보기)
# 바깥 쪽 끝은 192.0.2.254, 안쪽 끝은 아래에서 192.0.2.1 을 받는다
sudo ip netns add nslab
sudo ip link add vnsl0 type veth peer name vnsl1
sudo ip link set vnsl1 netns nslab
sudo ip addr add 192.0.2.254/24 dev vnsl0
sudo ip link set vnsl0 up

# 네임스페이스 안에서 root 셸을 연다. 시트 끝의 「실습 정리」 전까지 이 셸에서 친다
sudo ip netns exec nslab bash
```

```bash
# 안쪽 인터페이스에 주소와 기본 경로를 준다 (라우팅 표 보기, 인터페이스 표 보기)
ip link set lo up
ip addr add 192.0.2.1/24 dev vnsl1
ip link set vnsl1 up
ip route add default via 192.0.2.254

# 듣는 서버 넷을 띄운다 (듣는 포트와 프로세스 보기부터 여러 곳)
# 차례로 TCP IPv4, TCP IPv6, 연결 하나를 받는 TCP, UDP 서버다
cd /tmp
nohup python3 -m http.server 18082 --bind 127.0.0.1 > /dev/null 2>&1 &
nohup python3 -m http.server 18084 --bind ::1 > /dev/null 2>&1 &
nohup nc -l 127.0.0.1 18081 > /dev/null 2>&1 &
nohup nc -u -l 127.0.0.1 18083 > /dev/null 2>&1 &

# 18081 에 연결 하나를 열어 둔다 (연결까지 보기)
nohup sh -c 'sleep 600 | nc 127.0.0.1 18081' > /dev/null 2>&1 &
sleep 0.5
```

### 듣는 포트와 프로세스 보기

> 책 노트가 소개하는 `netstat -ctulpn` 은 옵션 여섯의 묶음이고, 한 번만 찍을 때는 `-c` 를 뺀 `-tulpn` 입니다.

```bash
# 듣는 TCP·UDP 소켓을 숫자 포트와 프로세스로 본다. 소켓 네 개가 한 줄씩 나온다
#   -c   표를 한 번이 아니라 매초 계속 찍는다 (아래 「매초 다시 찍기」)
#   -t   TCP 소켓
#   -u   UDP 소켓
#   -l   듣는 소켓만 (기본 출력에서는 빠져 있다)
#   -p   소켓을 쥔 프로그램의 PID 와 이름
#   -n   이름 해석 없이 숫자 주소와 포트
netstat -tulpn
```

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN      67254/python3       
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN      67256/nc            
tcp6       0      0 ::1:18084               :::*                    LISTEN      67255/python3       
udp        0      0 127.0.0.1:18083         0.0.0.0:*                           67257/nc            
```

UDP 줄은 연결이 없어서 `State` 칸이 비고, IPv6 TCP 는 `tcp6` 로 따로 나옵니다. PID 는 실행마다 달라집니다.[^opts]

### 연결까지 보기

> 옵션 없이 찍으면 맺어진 연결만 나오고, `-a` 를 주면 듣는 소켓이 함께 나옵니다.

`-l` 은 듣는 소켓만 보이는 옵션이라, 맺어진 연결까지 계속 보려면 `-l` 대신 `-a` 를 씁니다.

```bash
# 맺어진 TCP 연결만 본다. 머리 줄이 w/o servers 로 바뀐다. 연결 양 끝이 두 줄로 나온다
netstat -tn
```

```bash
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:60996         127.0.0.1:18081         ESTABLISHED
tcp        0      0 127.0.0.1:18081         127.0.0.1:60996         ESTABLISHED
```

```bash
# 듣는 소켓까지 함께 본다. 위 두 줄에 LISTEN 이 더해진다
#   -a   듣는 소켓과 듣지 않는 소켓을 모두 (기본은 연결된 것만)
netstat -tan
```

```bash
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:60996         127.0.0.1:18081         ESTABLISHED
tcp        0      0 127.0.0.1:18081         127.0.0.1:60996         ESTABLISHED
tcp6       0      0 ::1:18084               :::*                    LISTEN     
```

```bash
# 연결 소켓에도 프로세스를 붙인다. 18081 의 두 끝이 다른 프로세스로 나온다
netstat -tanp
```

```bash
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN      67254/python3       
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN      67256/nc            
tcp        0      0 127.0.0.1:60996         127.0.0.1:18081         ESTABLISHED 67262/nc            
tcp        0      0 127.0.0.1:18081         127.0.0.1:60996         ESTABLISHED 67256/nc            
tcp6       0      0 ::1:18084               :::*                    LISTEN      67255/python3       
```

클라이언트 포트 60996 은 실행마다 달라집니다.

### 이름 해석과 숫자 주소

> `-n` 을 빼면 주소가 호스트 이름으로, 포트가 서비스 이름으로 바뀝니다.

```bash
# -n 없이 본다. 127.0.0.1 이 localhost 로, ::1 도 localhost 로 풀린다
netstat -tulp
```

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 localhost:18082         0.0.0.0:*               LISTEN      67254/python3       
tcp        0      0 localhost:18081         0.0.0.0:*               LISTEN      67256/nc            
tcp6       0      0 localhost:18084         [::]:*                  LISTEN      67255/python3       
udp        0      0 localhost:18083         0.0.0.0:*                           67257/nc            
```

두 주소가 모두 `localhost` 로 합쳐 보이므로 IPv4 와 IPv6 는 `Proto` 열(`tcp`·`tcp6`)이나 `-n` 으로 가릅니다.[^opts]

### 프로세스 열과 권한

> root 가 아닌 사용자가 `-p` 를 주면 경고 한 줄이 나오고 `PID/Program name` 칸이 `-` 로 채워집니다.

```bash
# root 가 아닌 사용자(UID 65534)로 -p 를 준다. setpriv 는 다른 권한으로 명령을 실행한다
setpriv --reuid=65534 --regid=65534 --clear-groups \
  netstat -tlpn
```

```bash
(No info could be read for "-p": geteuid()=65534 but you should be root.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN      -                   
tcp6       0      0 ::1:18084               :::*                    LISTEN      -                   
```

소켓은 그대로 나오고 프로세스만 가려집니다. 매뉴얼은 소켓이 커널 것이거나 프로세스가 이미 끝났을 때도 하이픈을 보인다고 적습니다.[^opts]

### 매초 다시 찍기

> `-c` 는 같은 표를 지우지 않고 매초 이어서 찍습니다.

```bash
# 2.5초 동안 돌리고 표 머리가 몇 번 찍혔는지 센다 (표가 3번 찍힌다)
timeout 2.5 netstat -ctlpn | grep -c '^Active'
# 3
```

화면을 지우고 갱신하지 않아서 표가 위로 쌓이므로 끝낼 때는 `Ctrl+C` 를 누르거나 위처럼 [timeout 참조 시트](../shell/timeout.md)의 `timeout` 으로 끊습니다. 변화만 같은 자리에서 보려면 [watch 참조 시트](../resource/watch.md)의 `watch -n 1` 을 씁니다.[^opts]

### 소유자·타이머 열 붙이기

> `-e` 는 소유자와 inode 열을, `-o` 는 타이머 열을 표 끝에 붙입니다.

```bash
# 소유자(User)와 inode(Inode) 열이 붙는다
#   -e   다른 열을 더 보인다 (두 번 주면 최대한 자세히)
netstat -tlpne
```

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name    
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN      0          2005815    67254/python3       
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN      0          2008260    67256/nc            
tcp6       0      0 ::1:18084               :::*                    LISTEN      0          2007363    67255/python3       
```

```bash
# 타이머(Timer) 열이 붙는다
#   -o   네트워킹 타이머 정보를 보인다
netstat -tlno
```

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       Timer
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp6       0      0 ::1:18084               :::*                    LISTEN      off (0.00/0/0)
```

inode 는 실행마다 달라집니다. 이 소켓들은 모두 root 가 띄웠으므로 `User` 칸이 0 입니다.

### 라우팅 표 보기

> `-r` 은 소켓 목록 대신 커널 라우팅 표를 찍고, `-n` 을 더하면 `default` 가 `0.0.0.0` 으로 바뀝니다.

```bash
# 라우팅 표를 본다. 기본 경로는 default 로 나온다
#   -r   라우팅 표
netstat -r
```

```bash
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         192.0.2.254     0.0.0.0         UG        0 0          0 vnsl1
192.0.2.0       0.0.0.0         255.255.255.0   U         0 0          0 vnsl1
```

```bash
# 이름 해석 없이 본다. default 가 0.0.0.0 이 된다
netstat -rn
```

```bash
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.0.2.254     0.0.0.0         UG        0 0          0 vnsl1
192.0.2.0       0.0.0.0         255.255.255.0   U         0 0          0 vnsl1
```

`Flags` 의 `U` 는 경로가 살아 있다는 뜻이고 `G` 는 게이트웨이를 거친다는 뜻입니다. 같은 일을 하는 `ip route` 는 「ss·ip 명령으로 바꿔 쓰기」 에 있습니다.[^flags]

### 인터페이스 표 보기

> `-i` 는 인터페이스마다 송수신 패킷 수를 한 줄로 찍고, `-e` 를 더하면 `ifconfig` 모양으로 찍습니다.

```bash
# 인터페이스 표를 본다. 인터페이스 두 개가 한 줄씩 나온다
#   -i   인터페이스 표
netstat -i
```

```bash
Kernel Interface table
Iface             MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
lo              65536        3      0      0 0             3      0      0      0 LRU
vnsl1            1500        8      0      0 0            10      0      0      0 BMRU
```

```bash
# -e 를 더하면 인터페이스마다 여러 줄이 나온다. 이름·플래그·IPv4 주소 줄만 거른다
netstat -ie | grep -E '^[a-z]|inet '
```

```bash
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
vnsl1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.0.2.1  netmask 255.255.255.0  broadcast 0.0.0.0
```

패킷 수는 실행마다 달라집니다.

### 프로토콜 통계 보기

> `-s` 는 프로토콜마다 누적 카운터를 찍고, `-t`·`-u` 로 한 프로토콜만 좁힙니다.

```bash
# TCP 카운터만 본다. 앞 열두 줄만 줄여 싣는다
#   -s   프로토콜별 통계
netstat -st | head -n 12
```

```bash
Tcp:
    1 active connection openings
    1 passive connection openings
    0 failed connection attempts
    0 connection resets received
    2 connections established
    3 segments received
    3 segments sent out
    0 segments retransmitted
    0 bad segments received
    0 resets sent
TcpExt:
```

```bash
# UDP 카운터만 본다
netstat -su
```

```bash
Udp:
    0 packets received
    0 packets to unknown port received
    0 packet receive errors
    2 packets sent
    0 receive buffer errors
    0 send buffer errors
IpExt:
    InOctets: 172
    OutOctets: 334
    InNoECTPkts: 3
```

카운터는 네임스페이스를 만든 뒤 쌓인 값이라 실행마다 달라집니다.

### 상태별 연결 수 세기

> `State` 열만 뽑아 세면 `ESTABLISHED`·`LISTEN` 같은 상태마다 소켓이 몇 개인지 봅니다.

```bash
# 머리 두 줄을 빼고 여섯째 열(State)만 뽑아 상태마다 센다
#   uniq -c   같은 줄이 몇 번 나왔는지 앞에 붙인다
netstat -tan | awk 'NR > 2 {print $6}' | sort | uniq -c
```

```bash
      2 ESTABLISHED
      3 LISTEN
```

### ss·ip 명령으로 바꿔 쓰기

> 소켓은 `ss`, 라우팅 표는 `ip route`, 인터페이스 표는 `ip -s link` 가 같은 일을 합니다.[^env]

```bash
# netstat 한 줄을 같은 일을 하는 명령으로 바꾼다 (왼쪽이 netstat, 오른쪽이 대체)
# netstat -tulpn   ss -tulpn          듣는 TCP·UDP 소켓과 프로세스
# netstat -tan     ss -tan            TCP 소켓 전체
# netstat -r       ip route           라우팅 표
# netstat -i       ip -s link         인터페이스 표
# netstat -g       ip maddr           멀티캐스트 그룹
# netstat -c       watch -n 1 ss ...  매초 다시 찍기 (매뉴얼 대응표에 없는 것은 이 시트의 판단)

# 소켓 목록. 옵션 글자가 그대로 통한다
ss -tulpn
```

```bash
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                            
udp   UNCONN 0      0          127.0.0.1:18083      0.0.0.0:*    users:(("nc",pid=67257,fd=3))     
tcp   LISTEN 0      5          127.0.0.1:18082      0.0.0.0:*    users:(("python3",pid=67254,fd=3))
tcp   LISTEN 0      1          127.0.0.1:18081      0.0.0.0:*    users:(("nc",pid=67256,fd=3))     
tcp   LISTEN 0      5              [::1]:18084         [::]:*    users:(("python3",pid=67255,fd=3))
```

```bash
# 연결 소켓까지 본다. 상태 이름이 ESTABLISHED 가 아니라 ESTAB 으로 줄어든다
ss -tan
```

```bash
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port 
LISTEN 0      5          127.0.0.1:18082      0.0.0.0:*    
LISTEN 0      1          127.0.0.1:18081      0.0.0.0:*    
ESTAB  0      0          127.0.0.1:60996    127.0.0.1:18081
ESTAB  0      0          127.0.0.1:18081    127.0.0.1:60996
LISTEN 0      5              [::1]:18084         [::]:*    
```

```bash
# 라우팅 표와 인터페이스 표. ip -s link 는 인터페이스마다 RX 줄 하나를 찍어 두 개를 센다
ip route
ip -s link | grep -c 'RX:'
```

```bash
default via 192.0.2.254 dev vnsl1
192.0.2.0/24 dev vnsl1 proto kernel scope link src 192.0.2.1
2
```

```bash
# netstat -s 의 첫 카운터와 같은 값을 nstat 로도 볼 수 있다 (둘 다 수신 패킷 3)
#   nstat -a   지난번과의 차이가 아니라 누적값을 찍는다
netstat -s | sed -n 3p; nstat -a | grep IpInReceives
```

```bash
    3 total packets received
IpInReceives                    3                  0.0
```

`netstat -s` 와 `nstat -a` 가 같은 값을 보인다는 것은 이 시트의 실측이고, 매뉴얼 대응표에는 `-s` 가 없습니다. `ss -s` 는 카운터가 아니라 소켓 개수 요약이라 다른 일을 합니다.

### 실습 정리

```bash
# 네임스페이스 셸에서 나온다
exit

# 네임스페이스에 남은 프로세스를 끝내고 네임스페이스와 veth 를 지운다
sudo ip netns pids nslab | xargs -r sudo kill
sudo ip netns del nslab
sudo ip link del vnsl0 2> /dev/null
```



## 주의사항과 동작 원리

### 듣는 소켓의 Send-Q 값

> 매뉴얼은 듣는 소켓의 `Send-Q` 를 backlog 최대값이라고 적지만 실측에서는 `Recv-Q` 만 대기 연결 수를 따라가고 `Send-Q` 는 0 이었습니다.

```bash
# 「실습 정리」 전에 네임스페이스 셸에서 친다
# 연결 세 개를 받아 놓고 accept 하지 않는 서버를 18085 에 띄운다
cat > /tmp/nslab-q.py << 'EOF'
import socket, time
s = socket.socket()
s.bind(("127.0.0.1", 18085))
s.listen(5)
cs = [socket.create_connection(("127.0.0.1", 18085)) for _ in range(3)]
time.sleep(600)
EOF
nohup python3 /tmp/nslab-q.py > /dev/null 2>&1 &
sleep 0.5

# 같은 소켓을 netstat 와 ss 로 본다
netstat -tln | grep -E 'Recv-Q|:18085'
ss -tln 'sport = :18085'

# 서버와 파일을 지운다
pkill -f nslab-q.py; rm /tmp/nslab-q.py
```

```bash
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        3      0 127.0.0.1:18085         0.0.0.0:*               LISTEN     
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 3      5          127.0.0.1:18085      0.0.0.0:*   
```

`Recv-Q` 3 은 두 도구가 같지만 `Send-Q` 는 `netstat` 가 0, `ss` 가 5(listen 에 준 backlog)입니다. 큐 크기가 중요한 진단이면 `ss` 로 봅니다.[^queue]

### net-tools 가 없거나 다른 판일 때

> `netstat` 가 없는 환경에서는 127 로 끝나고, macOS 의 `netstat` 는 같은 옵션 글자를 다르게 읽습니다.

```bash
# net-tools 가 없는 컨테이너에서 돌린다 (Mac 의 Docker)
docker run --rm ubuntu:26.04 bash -c 'netstat -tan; echo "exit=$?"'
# bash: line 1: netstat: command not found
# exit=127

# macOS 에서 같은 옵션을 준다. -p 가 프로토콜 이름을 받아 n 을 프로토콜로 읽는다
netstat -tulpn 2>&1 | head -n 1
# netstat: n: unknown or uninstrumented protocol: Undefined error: 0
```

Debian 계열에서는 `apt-get install net-tools` 로 넣습니다. 새로 쓰는 스크립트라면 처음부터 `ss`·`ip` 를 쓰는 편이 이식성이 좋습니다.



## 관련 문서

> 이 시트의 예와 이어지는 시트와 책 노트입니다.

- [ss 참조 시트](./ss.md) — `netstat -tulpn` 을 대체하는 `ss` 의 필터와 소켓 큐 읽기
- [timeout 참조 시트](../shell/timeout.md) — `-c` 처럼 끝나지 않는 명령에 시간 제한을 거는 법
- [watch 참조 시트](../resource/watch.md) — `ss` 같은 명령을 일정 간격으로 다시 실행하는 법
- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다](../../../book/learning-modern-linux/08-02.%EC%9E%90%EC%9B%90%EB%A7%88%EB%8B%A4%20%EC%B0%BD%EC%9D%B4%20%EB%94%B0%EB%A1%9C%20%EB%82%98%20%EC%9E%88%EC%96%B4%20%EC%96%B4%EB%8A%90%20%EC%B0%BD%EC%9D%84%20%EC%97%AC%EB%8A%90%EB%83%90%EA%B0%80%20%EA%B3%A7%20%EC%A7%84%EB%8B%A8%EC%9D%B4%EB%8B%A4.md#ss-의-소켓-큐) — 멈춘 서버의 `Recv-Q` 가 쌓이는 실험과 `netstat -ctulpn` 소개



## 참고 자료

> 검증 환경, 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04 LTS, net-tools 2.10-2ubuntu1, iproute2 6.19.0 — 2026-11-16 실측
- [netstat(8) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html)
- [route(8) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/en/man8/route.8.html)
- [nstat(8) — Ubuntu 26.04](https://manpages.ubuntu.com/manpages/resolute/en/man8/nstat.8.html)

[^env]: `man netstat` (net-tools 2.10) NOTES — "This program is mostly obsolete. Replacement for netstat is ss. Replacement for netstat -r is ip route. Replacement for netstat -i is ip -s link. Replacement for netstat -g is ip maddr." <https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html>
[^bsd]: macOS 26.6 의 `man netstat` — "-p protocol Show statistics about protocol, which is either a well-known name for a protocol or an alias for it." FreeBSD `netstat(1)` 도 `-p protocol` 을 "Filter by protocol." 로 적습니다. <https://man.freebsd.org/cgi/man.cgi?query=netstat&sektion=1>
[^no-exit]: `netstat(8)` 의 man 에는 종료 코드 절이 없습니다. 위 값은 Ubuntu 26.04 VM 에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^opts]: `man netstat` (net-tools 2.10) — `-l` "Show only listening sockets. (These are omitted by default.)", `-a` "Show both listening and non-listening sockets.", `-c` "This will cause netstat to print the selected information every second continuously.", `-p` "Show the PID and name of the program to which each socket belongs. A hyphen is shown if the socket belongs to the kernel (e.g. a kernel service, or the process has exited but the socket hasn't finished closing yet)." `-A` "Specifies the address families (perhaps better described as low level protocols) for which connections are to be shown.", State 열 "usually no states used in UDP and UDPLite, this column may be left blank". `-n`·`-t`·`-u` 의 뜻은 `netstat --help` 의 "-n, --numeric don't resolve names" 와 `<Socket>={-t|--tcp} {-u|--udp}` 입니다. <https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html>
[^flags]: `man route` (net-tools 2.10) Flags — "U (route is up)", "H (target is a host)", "G (use gateway)". `man netstat` 는 "netstat -r and route -e produce the same output." 라고 적습니다. <https://manpages.ubuntu.com/manpages/resolute/en/man8/route.8.html>
[^queue]: `man netstat` (net-tools 2.10) — Recv-Q "Listening: Since Kernel 2.6.18 this column contains the current syn backlog.", Send-Q "Listening: Since Kernel 2.6.18 this column contains the maximum size of the syn backlog." 이 시트의 실측은 `Recv-Q` 가 대기 연결 수와 같고 `Send-Q` 는 0 이었습니다. <https://manpages.ubuntu.com/manpages/resolute/en/man8/netstat.8.html>
