---
title: OS 네트워크 딥다이브 로드맵 — 섹션별 키워드 원문
tags: [moc, linux, networking, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# OS 네트워크 딥다이브 로드맵 — 섹션별 키워드 원문

---

> 중심 주제는 **Linux / OS Network** 입니다. 학습 동기는 Kubernetes 와 백엔드 운영이지만, Kubernetes 의 `Service`·`Ingress`·`NetworkPolicy` 자체를 깊게 설명하지 않고 그것들이 의존하는 **Linux 네트워크 원리**(namespace·veth·bridge·routing·netfilter·conntrack·socket·TCP state·DNS resolver·packet flow)를 중심으로 봅니다. Kubernetes 는 적용 사례·디버깅 대상·왜 이 OS 개념이 필요한지 보여주는 배경입니다. 이 문서는 제공받은 OS 네트워크 딥다이브 로드맵 원문을 **섹션별로 빠짐없이** 옮긴 기록이고, 카테고리 경계·등록 문서는 [README.md](README.md) 가 맡습니다.

## 1. OS 네트워크 딥다이브 전체 지도

```text
1. Process와 Socket
2. File Descriptor
3. TCP / UDP
4. TCP State
5. Listen Queue / Accept Queue
6. Ephemeral Port
7. DNS Resolver
8. Network Interface
9. Routing Table
10. ARP / Neighbor Table
11. Network Namespace
12. veth Pair
13. Linux Bridge
14. netfilter
15. iptables / nftables
16. NAT / SNAT / DNAT / MASQUERADE
17. conntrack
18. Packet Capture
19. Kernel Network Parameter
20. 장애 분석 루틴
```

한 줄로: 백엔드 애플리케이션의 HTTP 호출은 OS 에서는 socket 과 file descriptor 가 되고, kernel 에서는 TCP packet 이 되며, routing table 과 netfilter 를 지나, namespace/veth/bridge 구조를 통해 다른 네트워크 세계로 이동합니다.

핵심 줄기: Socket → TCP → Interface → Routing → netfilter → namespace → veth → bridge → NAT → conntrack → packet capture.

## 2. Process / Socket / File Descriptor

Spring Boot · Tomcat · Netty · Kafka Client · JDBC Driver 모두 결국 OS socket 을 씁니다. Java Application → Socket → File Descriptor → Kernel TCP/IP Stack.

알아야 할 것:

```text
socket()
bind()
listen()
accept()
connect()
read()
write()
close()

file descriptor
port
local address
remote address
listen socket
connected socket
```

Pod 안 Spring Boot 앱 = Linux network namespace 안에서 떠 있는 Java process = socket 을 열고 port 를 listen 하는 process. 컨테이너라고 socket 의 본질이 바뀌지 않습니다.

명령어: `ss -lntp` · `ss -antp` · `lsof -i` · `ulimit -n` · `cat /proc/<pid>/fd`.

실무 질문: 애플리케이션이 실제로 8080 을 listen 하고 있는가 / listen 은 하는데 연결이 안 되는가 / file descriptor 가 부족하지 않은가 / socket 이 CLOSE_WAIT 로 쌓이지 않는가.

## 3. TCP / UDP

알아야 할 것:

```text
TCP
UDP
3-way handshake
SYN
SYN-ACK
ACK
FIN
RST
retransmission
keepalive
MTU
MSS
```

TCP 상태: LISTEN · SYN_SENT · SYN_RECV · ESTABLISHED · FIN_WAIT · CLOSE_WAIT · TIME_WAIT · LAST_ACK · CLOSED.

상태별 감각: LISTEN(연결 받을 준비) · SYN_SENT(요청 보냈으나 응답 못 받음) · ESTABLISHED(연결 성공) · CLOSE_WAIT(상대가 닫았는데 내 앱이 아직 close 안 함) · TIME_WAIT(정상 종료 후 커널이 잠시 연결 정보 보관).

Kubernetes 와의 연결 — "Pod 연결이 안 된다" 는 OS 관점에서 보통: DNS 가 IP 를 못 찾음 / TCP SYN 이 나가지 못함 / SYN 은 나갔지만 SYN-ACK 가 안 옴 / SYN-ACK 는 왔지만 애플리케이션이 응답 안 함 / 중간에 RST 발생.

명령어: `ss -ant` · `ss -ant state established` · `ss -ant state time-wait` · `ss -ant state close-wait`.

## 4. Listen Queue / Accept Queue

서버가 `listen()` 한다고 무한히 연결을 받지 못합니다.

알아야 할 것:

```text
SYN backlog
accept queue
somaxconn
tcp_max_syn_backlog
application accept 속도
```

장애 감각: 트래픽 몰림 → SYN queue 또는 accept queue 밀림 → 클라이언트 connection timeout 증가 → 서버 CPU 는 낮아 보이는데 연결 실패.

백엔드 연결 — Tomcat: `server.tomcat.threads.max` · `accept-count` · `max-connections`. OS: `cat /proc/sys/net/core/somaxconn` · `cat /proc/sys/net/ipv4/tcp_max_syn_backlog`.

실무 질문: 서버가 요청을 처리 못 하는 것인가 / 아예 connection accept 를 못 하는 것인가 / 애플리케이션 thread 가 부족한가 / OS queue 가 부족한가.

## 5. Ephemeral Port

클라이언트가 외부로 연결할 때도 port 가 필요합니다. `10.1.1.20:42152 → 10.1.1.30:8080`.

알아야 할 것:

```text
ephemeral port
ip_local_port_range
TIME_WAIT
port exhaustion
connection reuse
keep-alive
```

Pod 가 외부 API·DB·Kafka·Redis 로 대량 연결을 만들 때 문제: 짧은 연결을 너무 많이 생성 / HTTP keep-alive 미사용 / connection pool 미설정 / TIME_WAIT 폭증 / NAT 환경에서 source port 고갈.

명령어: `cat /proc/sys/net/ipv4/ip_local_port_range` · `ss -ant state time-wait | wc -l` · `ss -ant | awk '{print $1}' | sort | uniq -c`.

## 6. DNS Resolver

OS 와 애플리케이션의 DNS 해석 흐름을 봅니다.

알아야 할 것:

```text
/etc/resolv.conf
nameserver
search domain
ndots
glibc resolver
DNS cache
TTL
A record
AAAA record
CNAME
```

OS 관점 흐름: application 이 hostname 요청 → resolver 설정 확인 → `/etc/hosts` 확인 → DNS server 질의 → IP 반환 → socket connect. Pod 내부 프로세스도 OS resolver 설정을 보고 DNS 를 조회합니다.

명령어: `cat /etc/resolv.conf` · `cat /etc/hosts` · `getent hosts payment-api` · `nslookup payment-api` · `dig payment-api`.

실무 질문: DNS 가 실패한 것인가 / DNS 는 됐는데 TCP 연결이 실패한 것인가 / search domain 때문에 예상보다 많은 DNS 질의가 발생하는가 / JVM DNS cache 때문에 오래된 IP 를 들고 있지는 않은가.

## 7. Network Interface

알아야 할 것:

```text
lo
eth0
ens*
veth*
bridge interface
MAC address
MTU
RX / TX
packet drop
```

명령어: `ip addr` · `ip link` · `ip -s link` · `cat /proc/net/dev` · `ethtool -S eth0`.

Pod 안에서는 보통 `eth0` 만 보이지만 Node 에서는 eth0 · cni0 · flannel.1 · cali* · veth* · docker0 등이 보입니다. OS 관점 질문: 패킷이 어느 interface 로 들어오고 나가는가 / interface drop 이 발생하는가 / MTU 가 맞지 않는가 / veth peer 가 어느 namespace 와 연결되는가.

## 8. Routing Table

패킷이 어느 interface 로 나갈지는 routing table 이 결정합니다.

알아야 할 것:

```text
default route
gateway
CIDR
metric
source IP
policy routing
ip rule
```

명령어: `ip route` · `ip rule` · `ip route get 8.8.8.8` · `ip route get <target-ip>`.

핵심 질문: 목적지 IP 로 가는 route 가 있는가 / 어느 interface 로 나가는가 / source IP 는 무엇으로 선택되는가 / 응답 패킷이 돌아올 수 있는 경로가 있는가. Kubernetes 의 Pod CIDR · Service CIDR 는 여기서 OS route 와 만나지만, 학습 중심은 Linux routing decision 입니다.

## 9. ARP / Neighbor Table

같은 L2 네트워크에서 IP 를 MAC 주소로 바꾸는 과정입니다.

알아야 할 것:

```text
ARP
Neighbor Table
MAC address
L2 reachability
stale entry
failed entry
```

명령어: `ip neigh` · `arp -n`.

IP route 는 맞는데 L2 에서 상대를 못 찾는 경우: route 있음 → next hop IP → ARP 로 MAC 조회 → 실패하면 패킷 전달 실패. Node 간 통신·bare metal 에서 중요해질 수 있습니다.

## 10. Network Namespace

컨테이너 네트워크의 핵심입니다.

```text
network namespace는 독립된 네트워크 세계다.
각 namespace는 별도의 interface · IP address · routing table
· iptables rule · port space · socket table 을 가질 수 있다.
```

호스트에서 8080 을 쓰고 있어도 컨테이너 안에서 8080 을 또 쓸 수 있습니다 — host network namespace 의 8080 과 container network namespace 의 8080 은 서로 다른 네트워크 세계이기 때문입니다.

명령어: `ls -l /proc/<pid>/ns/net` · `ip netns list` · `ip netns exec <ns> ip addr` · `ip netns exec <ns> ip route` · `ip netns exec <ns> ss -lntp`.

Pod 하나는 보통 하나의 network namespace 를 공유 → 내부 컨테이너들이 같은 IP 공유 · localhost 통신 가능 · port 충돌 가능. 여기까지만 K8s 와 연결하고 핵심은 namespace 자체입니다.

## 11. veth Pair

namespace 와 namespace 를 연결하는 가상 케이블입니다. veth pair 는 양 끝이 연결된 가상 Ethernet 장치로, 한쪽에 패킷을 넣으면 다른 쪽으로 나옵니다.

구조: container namespace 의 eth0 — veth pair — host namespace 의 vethxxxx.

명령어: `ip link` · `ip -d link show` · `ethtool -S <veth-name>`.

직접 실험:

```bash
sudo ip netns add ns1
sudo ip link add veth-host type veth peer name veth-ns
sudo ip link set veth-ns netns ns1
sudo ip addr add 10.200.1.1/24 dev veth-host
sudo ip link set veth-host up
sudo ip netns exec ns1 ip addr add 10.200.1.2/24 dev veth-ns
sudo ip netns exec ns1 ip link set veth-ns up
sudo ip netns exec ns1 ip link set lo up
ping 10.200.1.2
```

이 실험이 Kubernetes Pod 네트워크의 바닥입니다.

## 12. Linux Bridge

veth 가 케이블이라면 bridge 는 스위치에 가깝습니다.

알아야 할 것:

```text
linux bridge
L2 switching
bridge port
MAC learning
broadcast
```

구조: namespace A eth0 → veth → bridge → veth → namespace B eth0.

명령어: `ip link add br0 type bridge` · `ip link set br0 up` · `bridge link` · `bridge fdb show`.

일부 CNI·Docker bridge 모델에서 bridge 가 핵심이지만, OS 원리는 "여러 namespace 의 veth 를 하나의 L2 segment 로 묶을 수 있다" 입니다.

## 13. netfilter / iptables / nftables

OS 네트워크 디버깅에서 중요한 계층입니다.

알아야 할 것:

```text
netfilter
hook
table
chain
rule
match
target
iptables
nftables
```

주요 hook: PREROUTING · INPUT · FORWARD · OUTPUT · POSTROUTING.

패킷 흐름 — 외부 유입: NIC → PREROUTING → routing decision → INPUT 또는 FORWARD. 내부 송신: Application → OUTPUT → routing decision → POSTROUTING → NIC.

명령어: `iptables -L -n -v` · `iptables -t nat -L -n -v` · `iptables -t mangle -L -n -v` · `nft list ruleset`.

K8s 의 Service 구현·NAT·NetworkPolicy 일부는 이 계층을 쓰지만, OS 학습 핵심은 "패킷은 kernel 내부 여러 hook point 를 지나며 그 지점에서 허용·차단·변환·NAT 될 수 있다" 입니다.

## 14. NAT / SNAT / DNAT / MASQUERADE

알아야 할 것:

```text
NAT
SNAT
DNAT
MASQUERADE
source IP rewrite
destination IP rewrite
port mapping
```

DNAT(목적지 변경): `10.96.10.20:80 → 10.244.1.15:8080`. SNAT(출발지 변경): `10.244.1.15 → 192.168.0.10`. MASQUERADE: 동적으로 source IP 를 interface IP 로 바꾸는 SNAT 형태.

명령어: `iptables -t nat -L -n -v` · `conntrack -L`.

Pod 가 외부로 나갈 때 source IP 가 바뀌고, Service 로 들어간 패킷의 destination 이 실제 Pod IP 로 바뀝니다. 핵심은 "패킷의 source/destination 은 kernel 에서 바뀔 수 있고, 그래서 tcpdump 위치에 따라 보이는 IP 가 다를 수 있다" 입니다.

## 15. conntrack

NAT 와 방화벽을 이해하려면 conntrack(connection tracking)이 중요합니다. 커널이 연결 상태와 NAT 전후 mapping 을 기억합니다.

NAT 는 첫 패킷만 보고 끝나지 않습니다. 응답 패킷을 원래 연결로 돌려보내려면 상태 기억이 필요합니다: client → NAT → server, server → NAT → client 의 대응 관계를 conntrack 이 기억.

명령어: `conntrack -L` · `conntrack -S` · `cat /proc/sys/net/netfilter/nf_conntrack_max` · `cat /proc/sys/net/netfilter/nf_conntrack_count`.

장애 감각: conntrack table full → 새 연결 추적 불가 → 간헐적 connection timeout → Kubernetes 네트워크가 랜덤하게 불안정해 보임. 애플리케이션 로그에는 단서가 없고 네트워크만 흐릿하게 흔들리는 무서운 장애입니다.

## 16. MTU / Fragmentation

자주 보지 않지만 걸리면 어렵습니다.

알아야 할 것:

```text
MTU
MSS
fragmentation
Path MTU Discovery
ICMP
overlay network overhead
```

Overlay network 는 원본 packet 에 캡슐화 overhead(overlay header)가 붙습니다. MTU 가 맞지 않으면 큰 응답만 실패하는 이상한 장애가 납니다.

명령어: `ip link` · `ping -M do -s 1472 <target-ip>` · `tracepath <target-ip>`.

증상: 작은 요청은 성공 / 큰 응답은 실패 / TLS handshake 중 멈춤 / 간헐적 timeout / 특정 경로에서만 실패.

## 17. Packet Capture

OS 네트워크의 진실은 결국 packet 에 있습니다.

알아야 할 것:

```text
tcpdump
wireshark
pcap
SYN
ACK
RST
FIN
retransmission
duplicate ACK
TLS ClientHello
DNS query
```

명령어: `tcpdump -i any -nn host <ip>` · `tcpdump -i any -nn port 8080` · `tcpdump -i any -nn tcp` · `tcpdump -i any -nn udp port 53` · `tcpdump -i any -w dump.pcap`.

분석 질문: DNS query 가 나가는가 / DNS response 가 오는가 / TCP SYN 이 나가는가 / SYN-ACK 가 오는가 / RST 가 오는가 / TLS handshake 가 시작되는가 / HTTP 요청이 실제로 나가는가 / 응답이 돌아오는가.

K8s 에서 tcpdump 위치가 중요합니다: Pod namespace 안 / Node host namespace / veth / node eth0 — 보는 위치에 따라 NAT 전 IP 와 NAT 후 IP 가 다르게 보입니다.

## 18. Kernel Parameter

```bash
# file descriptor
ulimit -n
cat /proc/sys/fs/file-max
# listen backlog
cat /proc/sys/net/core/somaxconn
cat /proc/sys/net/ipv4/tcp_max_syn_backlog
# ephemeral port
cat /proc/sys/net/ipv4/ip_local_port_range
# TIME_WAIT
cat /proc/sys/net/ipv4/tcp_fin_timeout
# conntrack
cat /proc/sys/net/netfilter/nf_conntrack_max
cat /proc/sys/net/netfilter/nf_conntrack_count
# keepalive
cat /proc/sys/net/ipv4/tcp_keepalive_time
cat /proc/sys/net/ipv4/tcp_keepalive_intvl
cat /proc/sys/net/ipv4/tcp_keepalive_probes
```

실무 질문: 동시 연결 수에 비해 file descriptor 가 부족하지 않은가 / 짧은 연결이 많아 ephemeral port 가 고갈되지 않는가 / conntrack table 이 꽉 차지 않았는가 / backlog 가 트래픽에 비해 작지 않은가.

## 19. Kubernetes 관련성 — "적용 위치" 로만 연결

OS 네트워크 문서 안에서는 Kubernetes 를 깊게 설명하지 말고 적용 위치로만 둡니다.

```text
Network Namespace: Pod가 독립된 네트워크 세계를 갖는 원리
veth: Pod namespace와 Node namespace가 연결되는 원리
Routing: Pod IP 대역으로 패킷이 이동하는 원리
netfilter / NAT: Service·NodePort·Pod egress에서 IP/Port가 바뀔 수 있는 원리
conntrack: NAT된 연결을 커널이 추적하는 원리
DNS resolver: Pod 내부 프로세스가 Service 이름을 IP로 바꾸는 원리
Socket / FD: Spring Boot·Kafka·DB 연결이 OS 리소스를 쓰는 원리
TCP State: connection timeout·reset·close_wait·time_wait를 해석하는 원리
```

## 20. 최종 학습 키워드

```text
Linux Network Stack
Socket
File Descriptor
Port
bind / listen / accept / connect
TCP
UDP
TCP 3-way Handshake
TCP State
TIME_WAIT
CLOSE_WAIT
SYN_SENT
ESTABLISHED
Listen Backlog
SYN Backlog
Ephemeral Port
DNS Resolver
/etc/resolv.conf
/etc/hosts
Network Interface
lo / eth0
Routing Table
Default Gateway
ARP
Neighbor Table
Network Namespace
/proc/<pid>/ns/net
veth Pair
Linux Bridge
netfilter
iptables
nftables
PREROUTING
INPUT
FORWARD
OUTPUT
POSTROUTING
NAT
SNAT
DNAT
MASQUERADE
conntrack
MTU
MSS
Packet Fragmentation
tcpdump
ss
iproute2
ethtool
sysctl
Kernel Network Parameters
```

## 21. 추천 프로젝트

- **1. Socket & TCP State Lab** — Java/Spring 서버·클라이언트를 띄우고 TCP 상태 관찰: LISTEN · ESTABLISHED · TIME_WAIT 증가 · CLOSE_WAIT 재현 · connection refused · connection timeout. (`ss -antp` · `lsof -i` · `tcpdump -i any port 8080`)
- **2. Network Namespace Lab** — namespace 생성 · veth 연결 · namespace별 ip route 확인 · namespace 안에서 서버 실행 · host 에서 namespace 서버 호출.
- **3. Bridge & Routing Lab** — ns1·ns2 생성 · veth pair 2개 · br0 bridge · namespace 간 ping · routing table 변경 · tcpdump 로 패킷 확인.
- **4. NAT & conntrack Lab** — namespace 에서 외부 통신 · MASQUERADE 설정 · DNAT port forwarding · conntrack table 확인 · NAT 전후 tcpdump 비교.
- **5. Backend Timeout Lab** — connection timeout · read timeout · connection reset · DNS 실패 · SYN drop · RST 응답 · server accept 지연 이 백엔드 timeout 으로 어떻게 보이는지 확인.

## 22. TLS truststore — OS CA bundle 관점

> TLS truststore 의 *전체 계층 이동*(JVM/Envoy/cert-manager/VM)은 [05_JVM roadmap §26](../../01_language/java/05_JVM/roadmap.md) 에 메인으로 정리돼 있다. 여기서는 OS 계층 관점만 — TLS 클라이언트가 **OS 도구(curl 등)이거나 Nginx/HAProxy** 일 때의 신뢰 저장소다.

원칙: truststore 는 "TLS 클라이언트 쪽" 에 필요하고, 클라이언트가 누구냐에 따라 위치가 바뀐다. OS 레벨 도구가 HTTPS 상대를 검증하는 경우의 신뢰 저장소가 **OS CA bundle** 이다.

```text
OS 도구/curl 가 TLS 클라이언트
  → /etc/ssl/certs (배포판별 CA bundle 경로)
  → update-ca-certificates 로 사내 CA 추가
Nginx / HAProxy 가 TLS 클라이언트
  → proxy_ssl_trusted_certificate / ca-file 로 CA 지정
```

VM 미들웨어가 K8s Ingress 를 HTTPS 로 호출할 때(VM→Pod 방향) VM 이 Java 면 JVM truststore, Nginx 면 ca-file, OS 도구면 `/etc/ssl/certs` 가 검증 저장소가 된다. 사내 CA·Self-signed 인증서면 OS CA bundle 에 추가해야 한다 — 공인 CA 면 OS 기본 bundle 로 통과할 수 있다. JVM 측 변환·적용은 [05_JVM roadmap §26.5](../../01_language/java/05_JVM/roadmap.md) 참조.

## 23. 결론

```text
Kubernetes 자체를 공부하는 것:
  Pod, Service, Ingress, NetworkPolicy, CNI 리소스 중심

OS 네트워크를 공부하되 Kubernetes에 연결하는 것:
  namespace, veth, bridge, routing, netfilter, conntrack, socket 중심
```

이번 주제는 후자입니다. 가장 중요한 줄기: Socket → TCP → Interface → Routing → netfilter → namespace → veth → bridge → NAT → conntrack → packet capture. 이걸 잡으면 Kubernetes 네트워크도 더 단단하게 보입니다 — Kubernetes 가 만든 추상화 아래에서 실제로 물길을 파는 것은 결국 Linux kernel 입니다.
