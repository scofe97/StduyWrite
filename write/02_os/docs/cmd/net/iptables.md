---
title: iptables 참조 시트
tags: [linux, cheatsheet, iptables, netfilter, nat, firewall, network, cli, reference]
status: draft
source:
  - iptables(8)·iptables-extensions(8)·iptables-save(8)·iptables-restore(8)·xtables-nft(8)·xtables-monitor(8) (iptables-libs·iptables-nft 1.8.10-11.el9_5, Rocky Linux 9 컨테이너의 man 원문)
  - https://www.netfilter.org/documentation/
related:
  - ../README.md
  - ./firewall-cmd.md
  - ../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md
  - ../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md
updated: 2026-11-22
---

# iptables 참조 시트

---

> 리눅스 Netfilter 훅에 걸린 패킷 필터·NAT 규칙을 넣고 빼는 `iptables` 와 규칙을 백업·복원하는 `iptables-save`·`iptables-restore` 사용법을 컨테이너 실측 출력으로 모았습니다.

## 개요

> `iptables` 는 커널의 패킷 필터와 NAT 규칙을 조회·추가·삭제하는 CLI 이며, `iptables-save` 와 `iptables-restore` 가 그 규칙을 파일로 떠 두고 되살립니다.

이 명령 셋은 `iptables-nft-1.8.10-11.el9_5.x86_64` 패키지의 외부 바이너리입니다. `iptables`·`iptables-save`·`iptables-restore` 는 모두 `/etc/alternatives` 를 거치는 심볼릭 링크입니다. 끝까지 따라가면 `xtables-nft-multi` 에 닿습니다. 모든 출력은 Rocky Linux 9 `--privileged` 컨테이너에서 직접 돌려 확인했습니다.[^env]

테이블 5종과 Netfilter 훅 대응, 타깃 종결 범위의 원리는 책 노트 [커널이 패킷을 판정하는 층](../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md#훅-다섯과-그것을-정하는-두-질문)과 [iptables·IPVS·eBPF](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#구성--테이블체인규칙)가 정본입니다. 이 시트는 명령 꼴과 옵션 뜻, 실측 출력, 실수하기 쉬운 함정을 맡습니다.



## 핵심 문법

> `-t` 로 테이블을 고른 뒤 동작 플래그(`-A`·`-I`·`-D`·`-L`·`-S`·`-P`·`-N`)로 체인을 지정합니다. 규칙 명세에서는 조건 매치 뒤에 `-j` 로 타깃을 둡니다.

```bash
# 호출 형태 (iptables -h 의 Usage 와 각 man 페이지의 SYNOPSIS)
Usage: iptables -[ACD] chain rule-specification [options]
       iptables -I chain [rulenum] rule-specification [options]
       iptables -R chain rulenum rule-specification [options]
       iptables -D chain rulenum [options]
       iptables -[LS] [chain [rulenum]] [options]
       iptables -[FZ] [chain] [options]
       iptables -[NX] chain
       iptables -E old-chain-name new-chain-name
       iptables -P chain target [options]
       iptables -h (print this help information)
iptables-save [-M modprobe] [-c] [-t table] [-f filename]
iptables-restore [-chntvV] [-w seconds] [-M modprobe] [-T name] [file]

# 규칙 목록을 숫자·상세·줄 번호와 함께 본다 (현재 규칙과 열 읽기)
iptables -L -n -v --line-numbers

# 규칙을 명령 형태 그대로 뽑는다 (현재 규칙과 열 읽기)
iptables -S

# 체인 끝에 붙이거나 지정한 번호에 끼운다 (규칙 추가·삽입·삭제·교체·확인)
iptables -A <체인> <조건> -j <타깃>
iptables -I <체인> [번호] <조건> -j <타깃>

# 확장 매치로 상태·복수 포트·주석을 건다 (패킷 조건과 확장 매치)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 내장 체인의 기본 정책을 바꾼다 (체인 기본 정책 확인과 변경)
iptables -P <체인> <ACCEPT|DROP>

# 사용자 체인을 만들고 호출한 뒤 지운다 (사용자 체인 생성·호출·삭제)
iptables -N <체인>
iptables -A INPUT -j <체인>

# nat 테이블에서 목적지·출발지를 바꾼다 (목적지와 출발지 주소 바꾸기)
iptables -t nat -A PREROUTING -d <VIP> -p tcp --dport 80 -j DNAT --to-destination <대상:포트>
iptables -t nat -A POSTROUTING -s <대역> -o <인터페이스> -j MASQUERADE

# 카운터·로그·트레이스로 매칭을 추적한다 (규칙 매칭과 카운터·로그·추적)
iptables -L <체인> -n -v -Z
iptables -t nat -A PREROUTING -d <주소> -j LOG --log-prefix "MATCH: "
iptables -t raw -A PREROUTING <조건> -j TRACE

# 규칙 전체를 파일로 저장하고 검증한 뒤 복원한다 (규칙 저장과 복원)
iptables-save > <파일>
iptables-restore --test < <파일>
iptables-restore < <파일>
```



## 종료 코드

> 성공은 0 이며, 잘못된 인자는 2, 커널·유저스페이스 불일치는 3, 락·메모리·커널 거절은 4, 나머지 오류는 1 입니다.[^exit]

```bash
# 0  정상 종료
# 1  규칙 미존재(-C) 등 일반 오류
# 2  잘못된 명령줄 옵션·인자
# 3  커널과 유저스페이스 불일치 (정상 컨테이너에서는 재현하지 못함)
# 4  xtables 락 충돌, 메모리 부족, 커널 측 규칙 거절
iptables -C INPUT -p tcp --dport 9999 -j ACCEPT; echo $?    # iptables: Bad rule (does a matching rule exist in that chain?). / 1

iptables --badflag; echo $?
# iptables v1.8.10 (nf_tables): unknown option "--badflag"
# Try `iptables -h' or 'iptables --help' for more information. / 2

iptables -t nat -A INPUT -j REDIRECT; echo $?    # iptables v1.8.10 (nf_tables):  RULE_APPEND failed (Invalid argument): rule in chain INPUT / 4
```



## 유스케이스

### 실습 준비

> 아래 블록을 실행하면 이 시트의 모든 예제가 돌아가는 Rocky Linux 9 컨테이너와 가상 네트워크가 준비됩니다.

```bash
# 컨테이너를 띄우고 iptables 와 실습 도구를 설치한다
docker run -d --name ipt9 --privileged rockylinux:9 sleep 3600
docker exec ipt9 dnf -y install iptables-nft iproute nmap-ncat

# 이후 예는 컨테이너 안의 셸에서 친다
docker exec -it ipt9 bash
```

```bash
# NAT·차단·카운터 확인(「목적지와 출발지 주소 바꾸기」부터 여러 곳)에 쓸 가상 네트워크를 만든다
ip netns add client
ip link add veth-c-host type veth peer name veth-c
ip link set veth-c netns client
ip addr add 192.0.2.1/24 dev veth-c-host
ip link set veth-c-host up
ip netns exec client ip addr add 192.0.2.2/24 dev veth-c
ip netns exec client ip link set lo up
ip netns exec client ip link set veth-c up
ip netns exec client ip route add default via 192.0.2.1

ip netns add server
ip link add veth-s-host type veth peer name veth-s
ip link set veth-s netns server
ip addr add 198.51.100.1/24 dev veth-s-host
ip addr add 198.51.100.10/24 dev veth-s-host
ip link set veth-s-host up
ip netns exec server ip addr add 198.51.100.2/24 dev veth-s
ip netns exec server ip link set lo up
ip netns exec server ip link set veth-s up
ip netns exec server ip route add default via 198.51.100.1

echo 1 > /proc/sys/net/ipv4/ip_forward
```

### 현재 규칙과 열 읽기

> `-L -n -v --line-numbers` 로 테이블별 규칙과 패킷 카운터를 읽고, `-S` 로 명령 꼴 그대로의 규칙을 확인합니다.

```bash
# 기본 filter 테이블을 숫자·상세·줄 번호와 함께 본다
#   -L               체인 규칙 목록을 출력한다
#   -n               IP·포트를 이름 풀이 없이 숫자로 출력한다
#   -v               패킷·바이트 카운터와 인터페이스·세부 조건을 출력한다
#   --line-numbers   규칙 앞에 삭제·교체용 번호(num)를 붙인다
iptables \
  -L \
  -n \
  -v \
  --line-numbers
```

```bash
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
```

```bash
# filter 테이블 규칙을 iptables 명령 형식으로 본다
iptables -S
```

```bash
-P INPUT ACCEPT
-P FORWARD ACCEPT
-P OUTPUT ACCEPT
```

```bash
# nat 테이블을 골라 확인한다 (-t 생략 시 filter 테이블)
#   -t   대상 테이블(filter·nat·mangle·raw·security)을 고른다
iptables -t nat -L -n -v
```

```bash
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
```

`-L -v --line-numbers` 의 열은 왼쪽부터 다음 값을 뜻합니다.

- `num`: 체인 안에서 규칙의 위치 번호(1부터 시작)입니다.
- `pkts`·`bytes`: 그 규칙에 맞은 누적 패킷 수와 바이트 수입니다.
- `target`·`prot`·`opt`: 맞았을 때 실행할 타깃, L4 프로토콜, 조각(fragment) 조건입니다. 조건이 없으면 `--`, `-f` 규칙이면 `-f`, `! -f` 규칙이면 `!f` 로 찍힙니다.
- `in`·`out`: 들어온 인터페이스와 나갈 인터페이스(`*` 는 모든 인터페이스)입니다.
- `source`·`destination`: 출발지·목적지 CIDR 이며, 뒤에 포트나 확장 매치 조건이 이어집니다.

### 규칙 추가·삽입·삭제·교체·확인

> 규칙은 위에서 아래로 평가되므로 끝에 붙이는 `-A` 와 앞에 끼우는 `-I` 가 적용 순서를 가릅니다.

```bash
# 루프백 허용 규칙을 체인 끝에 붙인다
#   -A   지정한 체인 맨 뒤에 규칙을 붙인다
#   -i   패킷이 들어온 인터페이스를 고른다
#   -j   조건에 맞았을 때 넘어갈 타깃이나 체인을 정한다
iptables \
  -A INPUT \
  -i lo \
  -j ACCEPT

# SSH 포트 허용 규칙을 뒤에 이어 붙인다
#   -p       프로토콜(tcp·udp·icmp 등)을 고른다
#   --dport  목적지 포트를 고른다
iptables \
  -A INPUT \
  -p tcp \
  --dport 22 \
  -j ACCEPT

# ICMP 허용 규칙을 1번 자리에 끼워 넣는다 (번호 생략 시 1번)
#   -I   지정한 위치(기본 1)에 규칙을 삽입한다
iptables \
  -I INPUT 1 \
  -p icmp \
  -j ACCEPT

# 세 규칙의 배치 순서를 확인한다
iptables -L INPUT -n -v --line-numbers
```

```bash
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0           
2        0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0           
3        0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22
```

```bash
# 같은 규칙이 이미 들어 있는지 확인한다 (있으면 종료 코드 0, 없으면 1)
#   -C   규칙 존재 여부를 검사하고 종료 코드로 답한다
iptables -C INPUT -p tcp --dport 22 -j ACCEPT    # rc=0 (규칙 있음)

# 3번 규칙을 새 명세로 교체한다
#   -R   지정한 번호의 규칙을 통째로 바꾼다
iptables \
  -R INPUT 3 \
  -p tcp \
  --dport 2222 \
  -j ACCEPT

# 1번 규칙은 번호로 지우고, 2222 규칙은 명세로 찾아 지운다
#   -D   번호나 일치하는 규칙 명세로 규칙을 지운다
iptables -D INPUT 1
iptables -D INPUT -p tcp --dport 2222 -j ACCEPT

# 남은 규칙을 확인한 뒤 체인을 비운다
iptables -S INPUT
```

```bash
-P INPUT ACCEPT
-A INPUT -i lo -j ACCEPT
```

```bash
# INPUT 체인의 모든 규칙을 비운다
#   -F   체인의 모든 규칙을 삭제한다 (체인 생략 시 테이블 전체)
iptables -F INPUT
```

### 패킷 조건과 확장 매치

> `-m` 으로 확장 모듈을 열어 연결 추적 상태, 여러 포트, 설명 주석을 달고, `!` 로 조건을 뒤집습니다.

```bash
# 이미 맺어진 연결이나 연관된 패킷을 허용한다
#   -m conntrack   연결 추적 상태를 검사하는 모듈을 연다
#   --ctstate      일치시킬 상태 목록(NEW·ESTABLISHED·RELATED·INVALID·UNTRACKED 등)
iptables \
  -A INPUT \
  -m conntrack \
  --ctstate ESTABLISHED,RELATED \
  -j ACCEPT

# 80·443 포트를 한 규칙으로 묶고 설명 주석을 단다
#   -m multiport   최대 15개 포트(콜론 범위는 2개로 계산)를 묶어 고른다
#   --dports       쉼표로 잇거나 콜론 범위로 쓴 목적지 포트 목록
#   -m comment     규칙에 메모를 남기는 모듈을 연다
#   --comment      최대 256자의 설명 문자열
iptables \
  -A INPUT \
  -p tcp \
  -m multiport \
  --dports 80,443 \
  -m comment \
  --comment "web" \
  -j ACCEPT

# 특정 인터페이스와 출발지 대역의 SSH 접속만 허용한다
#   -s   출발지 IP 주소 또는 CIDR 대역
iptables \
  -A INPUT \
  -i veth-c-host \
  -s 192.0.2.0/24 \
  -p tcp \
  --dport 22 \
  -j ACCEPT

# client 대역이 아닌 출발지의 SSH 접속은 버린다
#   ! -s   지정한 주소 대역을 제외한 나머지 출발지
iptables \
  -A INPUT \
  ! -s 192.0.2.0/24 \
  -p tcp \
  --dport 22 \
  -j DROP

# 등록된 규칙을 명령 형태로 확인한다
iptables -S INPUT
```

```bash
-P INPUT ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m multiport --dports 80,443 -m comment --comment web -j ACCEPT
-A INPUT -s 192.0.2.0/24 -i veth-c-host -p tcp -m tcp --dport 22 -j ACCEPT
-A INPUT ! -s 192.0.2.0/24 -p tcp -m tcp --dport 22 -j DROP
```

```bash
# 실습한 INPUT 규칙을 비운다
iptables -F INPUT
```

`-m conntrack --ctstate` 가 받는 연결 상태의 뜻은 책 노트 [테이블에 실제로 적히는 것 — 상태와 플래그](../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md#테이블에-실제로-적히는-것--상태와-플래그)에 있습니다.

### 체인 기본 정책 확인과 변경

> 체인 맨 끝까지 아무 규칙에도 맞지 않은 패킷의 운명은 `-P` 로 지정한 기본 정책(`ACCEPT`·`DROP`)이 정합니다.

```bash
# 현재 INPUT 기본 정책을 본다
iptables -L INPUT -n | head -n 1    # Chain INPUT (policy ACCEPT)

# 기본 정책을 DROP 으로 바꾼 뒤 -S 로 확인한다
#   -P   내장 체인의 기본 정책(ACCEPT 또는 DROP)을 바꾼다
iptables -P INPUT DROP
iptables -S INPUT | head -n 1       # -P INPUT DROP

# 뒤 예제를 위해 다시 ACCEPT 로 되돌린다
iptables -P INPUT ACCEPT
```

원격 SSH 접속 중에 허용 규칙을 먼저 넣지 않고 `-P INPUT DROP` 을 치면 연결이 끊깁니다. 이 원인은 [규칙을 운용할 때 걸리는 것들](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#규칙을-운용할-때-걸리는-것들)에서 다룹니다.

### 사용자 체인 생성·호출·삭제

> 사용자 체인은 `-N` 으로 선언하고 내장 체인에서 `-j` 로 부르며, 지울 때는 참조 제거·규칙 비우기·체인 삭제 순서를 지킵니다.

```bash
# 새 사용자 체인을 만들고 규칙을 넣은 뒤 INPUT 에서 호출한다
#   -N   새 사용자 정의 체인을 만든다
iptables -N CUSTOM_IN
iptables -A CUSTOM_IN -s 192.0.2.0/24 -j RETURN
iptables -A CUSTOM_IN -j DROP
iptables -A INPUT -p tcp --dport 22 -j CUSTOM_IN

# 체인 구조와 호출 관계를 확인한다
iptables -S
```

```bash
-P INPUT ACCEPT
-P FORWARD ACCEPT
-P OUTPUT ACCEPT
-N CUSTOM_IN
-A INPUT -p tcp -m tcp --dport 22 -j CUSTOM_IN
-A CUSTOM_IN -s 192.0.2.0/24 -j RETURN
-A CUSTOM_IN -j DROP
```

```bash
# 참조와 규칙이 남아 있으면 -X 는 실패한다
#   -X   빈 사용자 체인을 삭제한다
iptables -X CUSTOM_IN    # iptables v1.8.10 (nf_tables):  CHAIN_DEL failed (Device or resource busy): chain CUSTOM_IN

# 참조 제거 -> 내부 규칙 비우기 -> 체인 삭제 순으로 지운다
iptables -D INPUT -p tcp --dport 22 -j CUSTOM_IN
iptables -F CUSTOM_IN
iptables -X CUSTOM_IN
```

`RETURN` 이 체인 순회를 멈추는 범위와 `ACCEPT` 와의 차이는 [타깃의 종결 범위](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#타깃의-종결-범위--다음-줄이-체인이-테이블패킷-전체)에 정리돼 있습니다.

### 목적지와 출발지 주소 바꾸기

> `nat` 테이블에서 `DNAT`·`REDIRECT` 는 목적지를, `MASQUERADE`·`SNAT` 는 출발지를 바꿉니다.

```bash
# NAT 없이 server(198.51.100.2:8080)에 붙으면 client 주소 192.0.2.2 가 그대로 보인다
timeout 3 ip netns exec server ncat -l 8080 -c 'printf "peer=%s\n" "$NCAT_REMOTE_ADDR"' &
sleep 0.2 && ip netns exec client ncat --recv-only -w 2 198.51.100.2 8080    # peer=192.0.2.2

# 목적지 203.0.113.10:80 을 server 로 돌리고, 출발지를 나가는 인터페이스 주소로 바꾼다
#   -d                 목적지 IP 주소 또는 CIDR 대역
#   --to-destination   DNAT 이 바꿀 새 목적지 주소[:포트]
iptables \
  -t nat \
  -A PREROUTING \
  -d 203.0.113.10 \
  -p tcp \
  --dport 80 \
  -j DNAT \
  --to-destination 198.51.100.2:8080

#   -o   패킷이 나갈 인터페이스를 고른다
iptables \
  -t nat \
  -A POSTROUTING \
  -s 192.0.2.0/24 \
  -o veth-s-host \
  -j MASQUERADE

# 가상 주소 203.0.113.10:80 으로 붙으면 server 는 veth-s-host 주소 198.51.100.1 을 본다
timeout 3 ip netns exec server ncat -l 8080 -c 'printf "peer=%s\n" "$NCAT_REMOTE_ADDR"' &
sleep 0.2 && ip netns exec client ncat --recv-only -w 2 203.0.113.10 80    # peer=198.51.100.1

# MASQUERADE 를 고정 주소 SNAT(198.51.100.10)으로 바꿔 확인한다
#   --to-source   SNAT 이 바꿀 고정 출발지 주소[:포트]
iptables \
  -t nat \
  -R POSTROUTING 1 \
  -s 192.0.2.0/24 \
  -o veth-s-host \
  -j SNAT \
  --to-source 198.51.100.10

timeout 3 ip netns exec server ncat -l 8080 -c 'printf "peer=%s\n" "$NCAT_REMOTE_ADDR"' &
sleep 0.2 && ip netns exec client ncat --recv-only -w 2 203.0.113.10 80    # peer=198.51.100.10

# 호스트로 들어오는 8080 요청을 로컬 18080 포트로 돌린다
#   --to-ports   REDIRECT 가 돌릴 로컬 포트(또는 범위)
iptables \
  -t nat \
  -A PREROUTING \
  -i veth-c-host \
  -p tcp \
  --dport 8080 \
  -j REDIRECT \
  --to-ports 18080

timeout 3 ncat -l 18080 -c 'printf "redirected=%s\n" "$NCAT_REMOTE_ADDR"' &
sleep 0.2 && ip netns exec client ncat --recv-only -w 2 192.0.2.1 8080    # redirected=192.0.2.2

# nat 테이블 규칙과 통과한 패킷 카운터를 본다
iptables -t nat -L -n -v --line-numbers
```

```bash
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        2   120 DNAT       tcp  --  *      *       0.0.0.0/0            203.0.113.10         tcp dpt:80 to:198.51.100.2:8080
2        1    60 REDIRECT   tcp  --  veth-c-host *       0.0.0.0/0            0.0.0.0/0            tcp dpt:8080 redir ports 18080

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        1    60 SNAT       all  --  *      veth-s-host  192.0.2.0/24         0.0.0.0/0            to:198.51.100.10
```

```bash
# nat 테이블 규칙을 비운다
iptables -t nat -F
```

### 규칙 매칭과 카운터·로그·추적

> 규칙이 실제로 맞았는지는 `-v` 카운터와 `-Z` 초기화, `LOG` 타깃, `raw` 테이블의 `TRACE` 로 확인합니다.

```bash
# 규칙을 넣고 ping 2패킷을 보낸 뒤 정확한 바이트 수를 본다
#   -x   카운터의 K·M·G 축약 없이 정확한 숫자를 찍는다
iptables -A INPUT -s 192.0.2.2 -p icmp -j ACCEPT
ip netns exec client ping -c 2 -q 192.0.2.1 >/dev/null
iptables -L INPUT -n -v -x --line-numbers
```

```bash
Chain INPUT (policy ACCEPT 4 packets, 216 bytes)
num      pkts      bytes target     prot opt in     out     source               destination         
1           2      168 ACCEPT     icmp --  *      *       192.0.2.2            0.0.0.0/0           
```

```bash
# 카운터를 출력하면서 동시에 0 으로 초기화한다
#   -Z   패킷·바이트 카운터를 0 으로 초기화한다 (-L 과 함께 쓰면 출력 직후 원자적 초기화)
iptables -L INPUT -n -v -Z
```

```bash
Chain INPUT (policy ACCEPT 4 packets, 216 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    2   168 ACCEPT     icmp --  *      *       192.0.2.2            0.0.0.0/0           
Zeroing chain `INPUT'
```

```bash
# 초기화된 카운터를 확인하고 규칙을 비운다
iptables -L INPUT -n -v
```

```bash
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 ACCEPT     icmp --  *      *       192.0.2.2            0.0.0.0/0           
```

```bash
iptables -F INPUT

# conntrack 규칙을 먼저 두고 nat PREROUTING 에 LOG 규칙을 넣는다
#   --log-prefix   커널 로그 줄 앞에 붙일 접두 문자열(최대 29자)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables \
  -t nat \
  -A PREROUTING \
  -d 203.0.113.10 \
  -j LOG \
  --log-prefix "MATCH: "

ip netns exec client ping -c 1 -W 1 -q 203.0.113.10 >/dev/null || true
iptables -t nat -L PREROUTING -n -v
```

```bash
Chain PREROUTING (policy ACCEPT 1 packets, 84 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    1    84 LOG        all  --  *      *       0.0.0.0/0            203.0.113.10         LOG flags 0 level 4 prefix "MATCH: "
```

```bash
# 컨테이너에서 커널 로그를 조회한다
dmesg | grep "MATCH:"    # rc=1 (컨테이너에서는 비어 있음)

iptables -t nat -F PREROUTING
iptables -F INPUT
```

위 출력에서 `LOG` 규칙 카운터는 1 패킷 올라갔지만 `dmesg` 에는 `MATCH:` 줄이 하나도 없었습니다. 같은 컨테이너에서 `dmesg` 는 `x_tables` 경고 같은 다른 커널 메시지를 보여 줬으니 `dmesg` 자체가 막힌 것은 아닙니다. 줄이 없는 이유는 확인하지 못했습니다.[^log-container]

`conntrack` 규칙이나 `DNAT` 같은 nat 타깃 규칙이 하나도 없을 때는 nat `PREROUTING` 의 `LOG` 규칙 카운터가 0 packets 에 머물렀습니다. 같은 `ping` 을 보내도 그랬습니다. 그래서 위 예는 `-m conntrack` 규칙을 먼저 둡니다. 이 컨테이너에서 관찰한 것이고 원인은 확인하지 못했습니다. filter `INPUT` 의 `LOG` 규칙은 `conntrack` 규칙 없이도 카운터가 올랐습니다.

```bash
# raw 테이블 PREROUTING 에 TRACE 를 걸고 xtables-monitor 로 패킷 경로를 따라간다
iptables \
  -t raw \
  -A PREROUTING \
  -s 192.0.2.2 \
  -p icmp \
  -j TRACE

timeout 2 xtables-monitor --trace > /tmp/trace.out & sleep 0.3; ip netns exec client ping -c 1 -q 192.0.2.1 >/dev/null; wait || true; cat /tmp/trace.out
```

```bash
PACKET: 2 5a47f27c IN=veth-c-host MACSRC=6e:d8:22:8c:df:88 MACDST=a6:e2:39:3d:59:1f MACPROTO=0800 SRC=192.0.2.2 DST=192.0.2.1 LEN=84 TOS=0x0 TTL=64 ID=21989 DF 
 TRACE: 2 5a47f27c raw:PREROUTING:rule:0x2:CONTINUE  -4 -t raw -A PREROUTING -s 192.0.2.2/32 -p icmp -j TRACE
 TRACE: 2 5a47f27c raw:PREROUTING:policy:ACCEPT 
PACKET: 2 5a47f27c IN=veth-c-host MACSRC=6e:d8:22:8c:df:88 MACDST=a6:e2:39:3d:59:1f MACPROTO=0800 SRC=192.0.2.2 DST=192.0.2.1 LEN=84 TOS=0x0 TTL=64 ID=21989 DF 
 TRACE: 2 5a47f27c filter:INPUT:policy:ACCEPT 
```

```bash
# TRACE 규칙과 임시 파일을 지운다
iptables -t raw -F PREROUTING && rm -f /tmp/trace.out
```

### 규칙 저장과 복원

> `iptables-save` 로 규칙을 텍스트 파일에 떠 두고, `iptables-restore --test` 로 문법을 검사한 뒤 복원합니다.

```bash
# 저장할 샘플 규칙 두 줄을 넣는다
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 활성 테이블 전체를 파일로 저장해 내용을 본다
iptables-save > /tmp/rules.v4 && cat /tmp/rules.v4
```

```bash
# Generated by iptables-save v1.8.10 (nf_tables) on Sun Nov 22 05:48:10 2026
*raw
:PREROUTING ACCEPT [1:84]
:OUTPUT ACCEPT [0:0]
COMMIT
# Completed on Sun Nov 22 05:48:10 2026
# Generated by iptables-save v1.8.10 (nf_tables) on Sun Nov 22 05:48:10 2026
*filter
:INPUT ACCEPT [1:84]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
COMMIT
# Completed on Sun Nov 22 05:48:10 2026
# Generated by iptables-save v1.8.10 (nf_tables) on Sun Nov 22 05:48:10 2026
*nat
:PREROUTING ACCEPT [1:84]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [1:84]
COMMIT
# Completed on Sun Nov 22 05:48:10 2026
```

```bash
# 카운터 값까지 포함해 filter 테이블만 뽑는다
#   iptables-save -c   규칙 앞에 [패킷:바이트] 카운터를 함께 적는다
#   iptables-save -t   지정한 테이블 하나만 덤프한다
iptables-save -c -t filter | head -n 6
```

```bash
# Generated by iptables-save v1.8.10 (nf_tables) on Sun Nov 22 05:48:10 2026
*filter
:INPUT ACCEPT [1:84]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
[0:0] -A INPUT -i lo -j ACCEPT
```

```bash
# 복원 전에 파일 문법만 검사한다 (오류가 없으면 출력 없이 종료 코드 0)
#   iptables-restore --test   규칙셋을 파싱·구성만 하고 커널에 반영하지 않는다 (-t 도 같음)
iptables-restore --test < /tmp/rules.v4    # rc=0 (오류 없음)

# 규칙을 비운 뒤 파일에서 되살린다 (기본 동작은 기존 테이블을 비우고 복원)
iptables -F INPUT && iptables-restore < /tmp/rules.v4
iptables -S INPUT
```

```bash
-P INPUT ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
```

```bash
# 기존 규칙을 지우지 않고 뒤에 덧붙이며 복원한다
#   iptables-restore -n   기존 테이블 내용을 비우지 않는다 (--noflush)
iptables-restore -n < /tmp/rules.v4
iptables -S INPUT
```

```bash
-P INPUT ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
```

```bash
# 실습 규칙과 임시 파일을 지운다
iptables -F INPUT && rm -f /tmp/rules.v4
```

### 실습 정리

```bash
# 실습 컨테이너를 지운다 (안에서 만든 가상 네트워크도 함께 사라진다)
docker rm -fv ipt9
```



## 주의사항과 동작 원리

### iptables -V 의 백엔드 표시

> `iptables -V` 끝에 `(nf_tables)` 가 붙으면 문법만 `iptables` 이고 커널 API 는 `nf_tables` 를 씁니다.[^xtables-nft]

```bash
# 버전 문자열과 실제 바이너리 경로를 확인한다
iptables -V                     # iptables v1.8.10 (nf_tables)
readlink -f /usr/sbin/iptables  # /usr/sbin/xtables-nft-multi
```

`(legacy)` 는 `get/setsockopt` 기반 `x_tables` 커널 API 를 씁니다. `(nf_tables)` 는 `nft_compat` 를 거쳐 `nf_tables` 서브시스템에 규칙을 넣습니다. 이 Rocky Linux 9 컨테이너는 `iptables-nft` 만 제공하며 `iptables-legacy` 는 설치돼 있지 않습니다. `iptables-nft` 와 kube-proxy `nftables` 모드의 차이는 [심화 학습](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#심화-학습)에 있습니다.

### 이름 풀이로 -L 이 느릴 때

> `-n` 없이 `iptables -L` 을 치면 IP 와 포트를 호스트·서비스 이름으로 풀려고 조회하므로, DNS 가 느리면 출력이 늦어질 수 있습니다.[^numeric]

```bash
iptables -A INPUT -s 192.0.2.10 -p tcp --dport 22 -j ACCEPT

# -n 없이 치면 0.0.0.0/0 이 anywhere, 22 가 ssh 로 바뀐다
iptables -L INPUT
```

```bash
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     tcp  --  192.0.2.10           anywhere             tcp dpt:ssh
```

```bash
# -n 을 붙이면 숫자를 그대로 찍는다
iptables -L INPUT -n
```

```bash
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     tcp  --  192.0.2.10           0.0.0.0/0            tcp dpt:22
```

```bash
iptables -F INPUT
```

이 컨테이너는 규칙이 한 줄뿐이라 걸리는 시간은 재지 않았습니다. man 은 `-n` 을 긴 reverse DNS 조회를 피하는 용도로 적습니다. 조회할 때는 `-L -n` 을 함께 씁니다.

### 뒤에 붙인 차단 규칙이 먹지 않을 때

> 체인 앞쪽에 `ESTABLISHED,RELATED` 허용 줄이 있으면, 뒤에 `-A` 로 붙인 차단 규칙은 이미 맺어진 연결에 닿지 않습니다.

```bash
# 기존 연결 허용 줄을 먼저 두고, 연결을 맺은 뒤 -A 로 차단 규칙을 붙인다
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
timeout 3 ncat -l 19000 >/dev/null &
ip netns exec client bash -c 'exec 3<>/dev/tcp/192.0.2.1/19000; echo one >&3; sleep 0.6; echo two >&3; sleep 0.6; echo three >&3' &
sleep 0.3 && iptables -A INPUT -s 192.0.2.2 -p tcp --dport 19000 -j DROP && sleep 0.6 && iptables -L INPUT -n -v --line-numbers
```

```bash
Chain INPUT (policy ACCEPT 2 packets, 129 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        4   216 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
2        0     0 DROP       tcp  --  *      *       192.0.2.2            0.0.0.0/0            tcp dpt:19000
```

```bash
# 같은 차단 규칙을 -I 로 1번 자리에 끼우면 즉시 패킷이 걸린다
iptables -I INPUT 1 -s 192.0.2.2 -p tcp --dport 19000 -j DROP && sleep 0.8 && iptables -L INPUT -n -v --line-numbers
```

```bash
Chain INPUT (policy ACCEPT 2 packets, 129 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        4   220 DROP       tcp  --  *      *       192.0.2.2            0.0.0.0/0            tcp dpt:19000
2        4   216 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
3        0     0 DROP       tcp  --  *      *       192.0.2.2            0.0.0.0/0            tcp dpt:19000
```

```bash
wait || true; iptables -F INPUT
```

`ESTABLISHED,RELATED` 줄이 `ACCEPT` 로 `filter` 순회를 끝내기 때문입니다. 이 동작과 `conntrack -D` 대안은 [규칙을 운용할 때 걸리는 것들](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#규칙을-운용할-때-걸리는-것들)에 있습니다.

### 재시작하면 규칙이 사라지는 이유

> `iptables` 는 규칙을 커널에 넣을 뿐 저장 파일을 만들지 않아서, 되살리는 장치가 없으면 재시작 때 규칙이 사라집니다.

```bash
# 규칙을 여러 번 넣은 뒤에도 이 컨테이너에는 부팅 시 읽을 저장 파일이 없다
ls -l /etc/sysconfig/iptables    # ls: cannot access '/etc/sysconfig/iptables': No such file or directory
```

규칙을 부팅 뒤에도 남기려면 `iptables-save` 로 떠 둔 뒤 `iptables-restore` 를 부팅 서비스로 실행해야 합니다. 컨테이너에서 재부팅까지는 해 보지 못했고, 재시작하면 사라진다는 서술은 책 노트를 따랐습니다. 원인과 배경은 [규칙을 운용할 때 걸리는 것들](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#규칙을-운용할-때-걸리는-것들)에서 다룹니다.

### IPv4 규칙이 IPv6 에 닿지 않을 때

> `iptables` 는 IPv4 전용이라, IPv6 트래픽은 별도 도구인 `ip6tables` 로 관리해야 합니다.

```bash
# IPv4 에 규칙을 넣어도 ip6tables INPUT 은 비어 있다
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
ip6tables -S INPUT    # -P INPUT ACCEPT

# iptables 에 IPv6 주소를 넘기면 오류로 거부된다
iptables -A INPUT -s ::1/128 -j ACCEPT
# iptables v1.8.10 (nf_tables): invalid mask `128' specified
# Try `iptables -h' or 'iptables --help' for more information.

iptables -F INPUT
```

듀얼 스택 환경에서 IPv4 만 막으면 IPv6 경로가 열려 남는 이유도 [규칙을 운용할 때 걸리는 것들](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md#규칙을-운용할-때-걸리는-것들)에 있습니다.

### firewalld 가 도는 호스트에서 혼용

> firewalld 가 켜진 호스트에서 `iptables` 로 규칙을 직접 고치면 firewalld 관리 밖이라 `--reload` 때 어떻게 될지 알 수 없습니다.

자세한 동작과 이유는 [firewall-cmd 참조 시트 — iptables 와 혼용 금지](./firewall-cmd.md#iptables-와-혼용-금지)를 따릅니다.

### 동시 실행 잠금과 -w 옵션

> `iptables-legacy` 에서는 여러 프로세스가 동시에 규칙을 바꿀 때 `/run/xtables.lock` 잠금에 걸려 실패할 수 있으며, `-w` 로 대기합니다.[^wait]

```bash
# -w 로 대기 시간을 줄 수 있지만, iptables-nft 에서는 락 파일 없이 원자적으로 처리된다
iptables -w 5 -L INPUT -n
```

```bash
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
```

```bash
ls -la /run/xtables.lock    # ls: cannot access '/run/xtables.lock': No such file or directory
```

man 은 락을 얻지 못하면 기본으로 종료한다고 적고, 종료 코드 4 의 예로 busy lock 을 듭니다. 이 컨테이너에는 `iptables-legacy` 가 없어 락 경합은 재현하지 못했습니다. 반면 `iptables-nft` 는 `nf_tables` 커널 API 로 규칙을 넣어 추가와 삭제가 항상 원자적입니다. 그래서 xtables-nft(8) 도 `--wait` 를 no-op 으로 적습니다.[^xtables-nft]



## 관련 문서

> 상위 방화벽 도구와 Netfilter 커널 구조는 아래 문서에서 이어서 봅니다.

- [firewall-cmd 참조 시트](./firewall-cmd.md) — firewalld 데몬을 통한 방화벽 관리와 혼용 금지
- [커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅](../../../../08_cloud/book/networking-and-kubernetes/02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) — 5개 Netfilter 훅과 Conntrack 상태
- [iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술](../../../../08_cloud/book/networking-and-kubernetes/02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) — 테이블·체인·규칙 구조와 타깃 종결 범위



## 참고 자료

> 검증은 Rocky Linux 9 컨테이너에서 했고, 옵션과 종료 코드 뜻은 같은 컨테이너의 man 원문과 대조했습니다.

- 검증 환경: Rocky Linux 9 컨테이너(`--privileged`), 2026-11-22
- 패키지 버전: `iptables-nft 1.8.10-11.el9_5`, `iproute 6.17.0-3.el9`, `nmap-ncat 7.92-5.el9`
- man 원문: iptables(8)·iptables-extensions(8)·iptables-save(8)·iptables-restore(8) 는 `iptables-libs 1.8.10-11.el9_5` 에 들어 있습니다
- man 원문: xtables-nft(8)·xtables-monitor(8) 는 `iptables-nft` 에 들어 있습니다
- [Netfilter/iptables 공식 문서](https://www.netfilter.org/documentation/)

[^env]: 컨테이너에서 `iptables -V` 는 `iptables v1.8.10 (nf_tables)` 를, `rpm -qf /usr/sbin/iptables` 는 `iptables-nft-1.8.10-11.el9_5.x86_64` 를 출력했습니다. `iptables-save`·`iptables-restore` 도 같은 패키지 소속입니다.
[^exit]: iptables(8) DIAGNOSTICS. "The exit code is 0 for correct functioning. Errors which appear to be caused by invalid or abused command line parameters cause an exit code of 2. Errors which indicate an incompatibility between kernel and user space cause an exit code of 3. Errors which indicate a resource problem, such as a busy lock, failing memory allocation or error messages from kernel cause an exit code of 4. Finally, other errors cause an exit code of 1."
[^log-container]: iptables-extensions(8) `LOG` 절은 로그가 "via the kernel log (where it can be read with dmesg(1) or read in the syslog)" 로 간다고 적습니다. 이 컨테이너에는 `journalctl` 이 없었고, `iptables -t nat -L PREROUTING -n -v` 에서 `LOG` 규칙 패킷 카운터는 올랐지만 `dmesg | grep "MATCH:"` 는 비어 있었습니다.
[^xtables-nft]: xtables-nft(8) DIFFERENCES TO LEGACY IPTABLES. "Because the xtables-nft tools use the nf_tables kernel API, rule additions and deletions are always atomic. ... For this reason, the iptables-legacy --wait option is a no-op in iptables-nft."
[^numeric]: iptables(8) `-n, --numeric`. "IP addresses and port numbers will be printed in numeric format. By default, the program will try to display them as host names, network names, or services (whenever applicable)." `-L` 설명은 "often used with the -n option, in order to avoid long reverse DNS lookups." 라고 덧붙입니다.
[^wait]: iptables(8) LOCK FILE 및 `-w, --wait`. "iptables uses the /run/xtables.lock file to take an exclusive lock at launch." "By default, the program will exit if the lock cannot be obtained."
