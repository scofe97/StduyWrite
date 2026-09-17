---
title: 네트워크 학습 로드맵
tags: [roadmap, linux, networking, kubernetes, cloud, ebpf, cilium, dns, security]
status: final
source:
  - ../02_os/networking/README.md
  - ../02_os/book/network-fundamentals-lab/README.md
  - ../08_cloud/kubernetes/04_networking/README.md
  - ../08_cloud/book/networking-and-kubernetes/README.md
related:
  - README.md
  - os-roadmap.md
  - k8s-roadmap.md
  - ../02_os/networking/README.md
  - ../02_os/book/network-fundamentals-lab/README.md
  - ../08_cloud/kubernetes/04_networking/README.md
updated: 2026-09-15
---

# 네트워크 학습 로드맵
---

> socket에서 시작해 커널 패킷 경로로 내려간 뒤 Kubernetes와 클라우드 underlay로 올라갑니다. 개념이 주인공이고 책은 그 개념을 다루는 자리입니다.

## 학습 순서

> 단계마다 배우는 개념을 묶음으로 갈랐습니다. 자료 위치는 아래 단계별 표가 짚습니다.

![socket에서 오버레이와 신뢰까지 이어지는 네트워크 학습 순서](_assets/network-roadmap.svg)

| 단계 | 묶음 | 배우는 개념 |
|---|---|---|
| 1 · 연결 | 소켓과 연결 | socket · `bind` · `listen` · `accept` · `connect` · 4-tuple · 듣는 소켓과 연결 소켓 |
| 1 · 연결 | TCP 동작 | 상태 · 3-way handshake · 재전송 · 타임아웃 · RTT · 흐름 제어 · cwnd · in-flight · 혼잡 제어 · CUBIC · BBR |
| 1 · 연결 | TCP 운영 | TIME_WAIT · SYN cookies · Nagle · delayed ACK · keepalive |
| 1 · 연결 | 이름 | DNS 질의 · 레코드 유형 · 위임 · TTL · negative caching |
| 1 · 연결 | 응용 프로토콜 | HTTP/1.1 · HTTP/2 · 멀티플렉싱 · QUIC · HTTP/3 · WebSocket · HTTP Upgrade |
| 1 · 연결 | 보안 전송 | TLS 핸드셰이크 · TLS 1.3 · 0-RTT · session resumption · ALPN · SNI · ECH · 인증서 체인 · SAN 호스트명 검증 · 유효 기간 · OS CA bundle · truststore |
| 1 · 연결 | 중계 | reverse proxy · TLS passthrough 대 TLS 종료 · SNI 라우팅 · Forwarded · X-Forwarded-For 신뢰 경계 · PROXY protocol · half-close · 배압 |
| 1 · 연결 | 큐와 UDP | listen 큐 · accept 큐 · ephemeral 포트 고갈 · UDP · 단편화 |
| 2 · Linux 경로 | 주소와 이웃 | interface · MAC · ARP · NDP · neighbor 테이블 포화 · IP 주소 · 서브네팅 · CIDR · IPv6 주소 · SLAAC |
| 2 · Linux 경로 | L2 분할과 묶음 | VLAN · 802.1Q · STP · bonding · LACP |
| 2 · Linux 경로 | 경로 결정 | 라우팅 테이블 · next hop · IP 포워딩 · data plane 과 control plane · ICMP · traceroute · 비대칭 경로 · `rp_filter` · policy routing · `ip rule` · VRF · 동적 라우팅 · OSPF · BGP · iBGP 풀메시 · 경로 반사기 |
| 2 · Linux 경로 | 흐름 식별 | 5-tuple · ECMP 해시 · 포트가 없어 흐름과 갈라지는 ICMP |
| 2 · Linux 경로 | 가상 인터페이스 | network namespace · veth · bridge · 컨테이너 네트워킹 모드 · 포트 매핑 |
| 2 · Linux 경로 | 패킷 변형 | netfilter hook · iptables · nftables · NAT · SNAT · DNAT · MASQUERADE · conntrack |
| 2 · Linux 경로 | NAT 너머 | NAT traversal · STUN · TURN · ICE |
| 2 · Linux 경로 | 크기와 구성 | MTU · MSS · PMTUD · PMTUD 블랙홀 · `tcp_mtu_probing` · DHCP |
| 3 · 관측 | 캡처 | tcpdump · tshark · 캡처 위치 · 캡처 필터 · 디스플레이 필터 |
| 3 · 관측 | 판독 | RST · 재전송 · 중복 ACK · TLS 핸드셰이크 판독 |
| 3 · 관측 | 진단 방법론 | 도구와 단위의 대응 · 패킷이 사라지는 네 자리 · 드롭 카운터 읽기 · conntrack 경합 · `insert_failed` |
| 3 · 관측 | 계층별 도구 | `ss` · `ip` · `ethtool` · `conntrack -L` · `nft list ruleset` · `nstat` · tcpretrans · tcplife |
| 3 · 관측 | 이름 진단 | `resolv.conf` · search domain · `ndots` · NXDOMAIN · EDNS(0) · TC 비트 · TCP fallback · Corefile · 플러그인 체인 · 응답 불일치 |
| 3 · 관측 | 측정의 함정 | 연결 지연 분포 · P99 · 측정 오차 · `tc qdisc` · `netem` |
| 3 · 관측 | 송수신 경로 성능 | GRO · GSO · TSO 오프로딩 · RSS · RPS · XPS · ring buffer |
| 4 · Kubernetes | Pod 네트워크 | Pod IP · Pod CIDR · Node CIDR · pause container · CNI · CNI 계약 ADD·DEL·CHECK · IPAM 할당과 반납 · 노드별 Pod CIDR 블록 · IP 고갈 |
| 4 · Kubernetes | CNI 구현체 | Calico · Flannel · Cilium 의 갈림 · 라우팅 대 오버레이 · iptables 대 eBPF · 정책 표현력 |
| 4 · Kubernetes | 노드 간 전달 | 오버레이 · VXLAN · underlay 와 overlay 의 갈림 |
| 4 · Kubernetes | 서비스 추상화 | Service · EndpointSlice · Service 5유형 · kube-proxy · iptables · IPVS · readiness · stale Endpoint |
| 4 · Kubernetes | Service 세부 | headless Service · sessionAffinity · `internalTrafficPolicy` |
| 4 · Kubernetes | kube-proxy 대체 | kube-proxy replacement · Maglev · DSR |
| 4 · Kubernetes | 이름과 진입 | 클러스터 DNS · Service FQDN · NodeLocal DNSCache · service discovery · east-west · Ingress · Gateway API · HTTPRoute |
| 4 · Kubernetes | 분배 | L4 로드밸런싱 · health check · round-robin · least connections · draining · 연결 단위와 요청 단위 분산 · LB idle timeout |
| 4 · Kubernetes | 트래픽 보존 | `externalTrafficPolicy` · 소스 IP 보존 |
| 4 · Kubernetes | 장애 구분 | 인증서 만료와 TLS 실패 구분 |
| 5 · 클라우드 | VPC 구성 | VPC · 서브넷 · 라우트 테이블 · IGW · NAT GW |
| 5 · 클라우드 | 경계 제어 | Security Group · NACL · stateful 과 stateless 의 갈림 |
| 5 · 클라우드 | 진입과 분배 | 클라우드 로드밸런서 · L4 · L7 |
| 5 · 클라우드 | 사이트 간 연결 | VPN · IPsec · AWS Direct Connect · 전용선 · VPC 피어링 · Transit Gateway |
| 5 · 클라우드 | 서비스 연결 | PrivateLink · VPC endpoint |
| 5 · 클라우드 | 데이터센터 축 | Clos 토폴로지 · BGP · ECMP · 3사 기본값의 갈림 |
| 6 · 데이터패스 | 정책 모델 | NetworkPolicy · ingress · egress · default deny · L7 정책 · FQDN 정책 · identity-aware policy |
| 6 · 데이터패스 | eBPF 기초 | 프로그램 구조 · 유형 · attach · hook · map · helper · verifier · CO-RE · BTF |
| 6 · 데이터패스 | 데이터패스 구현 | XDP · TC hook · Cilium 데이터패스 · IPAM · eBPF host routing · netkit · bandwidth manager |
| 6 · 데이터패스 | 암호화와 관측 | 투명 암호화 · WireGuard · Hubble · egress 게이트웨이 · 클러스터 access |
| 7 · 운영 경계 | 주소와 배치 | dual-stack · `ipFamilyPolicy` · topology-aware routing · EndpointSlice hint |
| 7 · 운영 경계 | 혼합 환경 | Windows HNS · HCS · Windows CNI · 멀티클러스터 메시 |
| 7 · 운영 경계 | 메시 데이터 플레인 | 서비스 메시가 인프라로 밀어낸 것 · Envoy · Gateway · VirtualService · DestinationRule · `istioctl proxy-config` |
| 7 · 운영 경계 | 복원력 | retry · timeout · circuit breaking · outlier detection · 재시도 증폭 |
| 7 · 운영 경계 | 신원과 기본값 | mTLS · 기본값 닫아 가기 · SPIFFE · SVID · Zero Trust 전제 · ambient · ztunnel · waypoint |
| 8 · 오버레이와 신뢰 | 진입 | bootstrap · reseed · 최초 접점 · trust anchor · stale data |
| 8 · 오버레이와 신뢰 | 발견 | peer discovery · DHT · Kademlia · 역할이 나뉜 피어 · gossip · membership · peer store · lease · TTL 갱신 |
| 8 · 오버레이와 신뢰 | 식별 | node ID · signed descriptor · 공개키 신원 · 키에서 나온 주소 · key rotation · replay · freshness |
| 8 · 오버레이와 신뢰 | 신뢰 | Sybil · eclipse · poisoning · identity 와 trust 의 차이 · 인증과 인가의 차이 · capability · behavior score · keyless TLS · trusted edge |
| 8 · 오버레이와 신뢰 | 관측 가능성 | traffic correlation · metadata · timing side-channel · 암호화가 숨기지 않는 것 |
| 8 · 오버레이와 신뢰 | 오버레이 | 물리와 논리의 분리 · 터널링 · 가상 토폴로지 · relay · hole punching · reachability · reverse tunnel · outbound-only relay |
| 9 · 터널과 경로 | 구성 | 터널 구성 · 피어 발견과의 차이 · 멀티홉 · 홉별 계층 암호화 · 홉 수의 대가 · inbound 와 outbound 의 분리 · RX 와 TX |
| 9 · 터널과 경로 | 선택 | path selection · latency · 가용성 · subnet · ASN diversity · 비용 함수 · selection bias · 클라이언트가 정하는 경로 |
| 9 · 터널과 경로 | 확률 | 종단 성공 확률 · 곱으로 쌓이는 실패 · 기하분포 · 평균 시도 횟수 |
| 9 · 터널과 경로 | 재시도 | 재시도 · 타임아웃 · heartbeat · 감지 시간 · exponential backoff · jitter · retry budget |
| 9 · 터널과 경로 | 자원 | 터널 풀 · 미리 열어 두기 · 예비 터널 · 터널 수명과 교체 · 준비 비용 · 전환 시간 · 자원 사용량 |



## 책 읽기 흐름

> 위 단계를 어떤 자료로 배우는지 모았습니다. 책 스물두 권이 각각 어느 단계의 무엇을 다루는지와 읽을 장을 적습니다.

![네트워크 책 읽기 흐름 — 우선순위와 읽을 장](_assets/network-books.svg)

통독하는 책은 셋뿐이고 나머지는 표의 `읽을 장`만 봅니다.

| 책 | 읽을 장 | 우선순위 | 자리 |
|---|---|:---:|---|
| [Computer Networking](../02_os/book/cntd_computer-networking-top-down/README.md) | 1~6 · 8장 | 필수 | 1·2·5단계 |
| TCP/IP Illustrated | 2~8 · 10~17장 | 필수 | 1·2단계 |
| [Networking and Kubernetes](../08_cloud/book/networking-and-kubernetes/README.md) | 전독 | 필수 | 2~6단계 |
| [Packet Analysis with Wireshark](../02_os/book/paw_packet-analysis-wireshark/README.md) | 1~5장 | 필수 | 3단계 |
| [Systems Performance](../02_os/book/systems-performance/README.md) | 10장 | 추천 | 1·3단계 |
| HTTP/2 in Action | 4·8·9장 | 추천 | 1단계 |
| [Container Security](../08_cloud/book/container-security/README.md) | 11장 | 선택 | 1단계 |
| [Learning CoreDNS](../08_cloud/book/learning-coredns/README.md) | 2·3·6·7장 | 추천 | 1·3·4단계 |
| [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | 11~13 · 16·17장 | 추천 | 1·4단계 |
| Production Kubernetes | 5장 | 선택 | 4단계 |
| Cloud Native Data Center Networking | 2·6·7·14장 | 추천 | 4·5단계 |
| System Design on AWS | 9장 | 추천 | 5단계 |
| Cilium Up and Running | 1~16장 | 필수 | 4~7단계 |
| Learning eBPF | 3·5~8장 | 추천 | 6단계 |
| [Istio in Action](../08_cloud/book/istio-in-action/README.md) | 1 · 3~6 · 9·10·12장 · 부록 C | 추천 | 7단계 |
| Zero Trust Networks | 1·2·4·6·8장 | 추천 | 7·8단계 |
| Real-World Cryptography | 2·3 · 7~10장 | 추천 | 8단계 |
| API Security in Action | 9장 | 선택 | 8단계 |
| Patterns of Distributed Systems | 7·26·28장 | 추천 | 8·9단계 |
| Database Internals | 9·12장 | 추천 | 8·9단계 |
| High Performance Browser Networking | 2·4·11·12·17장 | 대체 | 1단계 — HTTP/2 in Action 자리 |
| Sidecar-less Istio Explained | 1~3장 | 대체 | 7단계 — Istio in Action 12장 자리 |
| [network-fundamentals-lab](../02_os/book/network-fundamentals-lab/README.md) | 00~17편 중 코어 10편 | 필수 | 1~4단계 — 유일한 랩 저장소 |

소장 목록은 계속 늘어납니다. 새 책이 들어오면 이 표와 아래 단계별 표의 `책` 열을 함께 갱신합니다.

**표의 마지막 줄만 책이 아닙니다.** [network-fundamentals-lab](../02_os/book/network-fundamentals-lab/README.md)은 containerlab 토폴로지 18편이 원자료이고, 배포하면 고장이 장전된 채로 뜹니다. 다른 자료가 규격과 원리를 위에서 아래로 설명한다면 이쪽은 증상에서 계층을 좁히는 순서를 훈련시킵니다. 그래서 아래 단계별 표에서 이 자료의 노트는 `책` 열이 아니라 `노트` 열에 놓았습니다 — 읽는 자리가 아니라 손으로 밟는 자리이기 때문입니다.

**책만으로 안 되는 자리가 넷입니다.** 소장본이 없거나 낡은 자리는 아래 문서를 기준으로 삼습니다.

| 자리 | 책만으로 부족한 이유 | 기준 문서 |
|---|---|---|
| Gateway API · CNI · 클러스터 DNS | Kubernetes in Action 13장과 Cilium 7장이 다루지만 스펙이 계속 바뀝니다 | [Gateway API 가이드](https://gateway-api.sigs.k8s.io/guides/) · [CNI 규격](https://github.com/containernetworking/cni/blob/main/SPEC.md) · [CoreDNS Manual](https://coredns.io/manual/toc/) · [Kubernetes 서비스·네트워킹 문서](https://kubernetes.io/ko/docs/concepts/services-networking/) |
| BBR | 2016년에 나온 알고리즘이라 2011년판 TCP/IP Illustrated 에 없습니다 | [TCP Congestion Control: A Systems Approach](https://tcpcc.systemsapproach.org/) 5장 — Vegas 와 나란히 읽습니다 |
| 8·9단계 오버레이와 터널 | 소장본에 맞는 장이 없습니다 | [Tor 설계 논문](https://www.usenix.org/conference/13th-usenix-security-symposium/tor-second-generation-onion-router) — traffic correlation 의 한계 · 4.2·9절 회로 교체와 그 대가 · I2P [Tunnel Routing](https://i2p.net/en/docs/overview/tunnel-routing/) · [Peer Selection](https://i2p.net/en/docs/overview/peer-selection/) — 터널 풀과 경로 선택 · [Garlic Routing](https://i2p.net/en/docs/overview/garlic-routing/) — 홉별 계층 암호화 · [Network Database](https://i2p.net/en/docs/overview/network-database/) — floodfill 역할 · libp2p [Kademlia DHT](https://github.com/libp2p/specs/blob/master/kad-dht/README.md) — 서버 모드와 클라이언트 모드 |
| LLM 트래픽 | 아직 책이 없습니다 | [Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/guides/) |



## 호스트 · 1~3단계

> 노드 한 대 안에서 끝나는 구간입니다. Kubernetes 없이도 성립합니다.

### 1단계 · 연결

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| socket · `bind` · `listen` · `accept` · `connect` | 필수 | | TCP/IP Illustrated 12·13장 |
| 4-tuple · 듣는 소켓과 연결 소켓의 구분 | 필수 | | TCP/IP Illustrated 12장 |
| TCP 상태 · 3-way handshake · 연결 관리 | 필수 | [랩 05-01](../02_os/book/network-fundamentals-lab/05-01.%EC%97%B0%EA%B2%B0%EC%9D%80%20%EC%96%91%20%EB%81%9D%EB%A7%8C%EC%9D%98%20%EC%9D%BC%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%8B%A4.md) · [03-01](../02_os/book/cntd_computer-networking-top-down/03-01.%ED%8A%B8%EB%9E%9C%EC%8A%A4%ED%8F%AC%ED%8A%B8%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8A%94%EA%B0%80.md) · [03-04](../02_os/book/cntd_computer-networking-top-down/03-04.%ED%9D%90%EB%A6%84%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EC%97%B0%EA%B2%B0%20%EA%B4%80%EB%A6%AC%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%ED%98%BC%EC%9E%A1.md) | TCP/IP Illustrated 13장 |
| 신뢰성 · 순서 번호 · 재전송 · 타임아웃 · RTT | 필수 | [03-02](../02_os/book/cntd_computer-networking-top-down/03-02.%EC%8B%A0%EB%A2%B0%EC%84%B1%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%A7%80%EB%8A%94%EA%B0%80.md) · [03-03](../02_os/book/cntd_computer-networking-top-down/03-03.TCP%20%EB%8A%94%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%84%B8%EA%B3%A0%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EA%B8%B0%EB%8B%A4%EB%A6%AC%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 14장 |
| 흐름 제어 · 윈도 · cwnd · in-flight data | 필수 | [03-04](../02_os/book/cntd_computer-networking-top-down/03-04.%ED%9D%90%EB%A6%84%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EC%97%B0%EA%B2%B0%20%EA%B4%80%EB%A6%AC%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%ED%98%BC%EC%9E%A1.md) | TCP/IP Illustrated 15장 |
| 혼잡 제어 · CUBIC · Vegas | 필수 | [03-05](../02_os/book/cntd_computer-networking-top-down/03-05.%ED%98%BC%EC%9E%A1%EC%9D%84%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%8B%A4%EC%8A%A4%EB%A6%AC%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 16장 |
| BBR — 지연 기반 혼잡 제어 | 추천 |  | Cilium 8장 |
| DNS 질의 · 이름 해석 | 필수 | [02-03](../02_os/book/cntd_computer-networking-top-down/02-03.%EB%A9%94%EC%9D%BC%EA%B3%BC%20%EC%9D%B4%EB%A6%84%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%B0%BE%EC%95%84%EA%B0%80%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 11장 |
| DNS 레코드 유형 · 위임 · TTL · negative caching | 필수 | [02-01](../08_cloud/book/learning-coredns/02-01.%EC%9C%84%EC%9E%84%EC%9D%B4%20%EA%B7%B8%EC%9D%80%20%EA%B2%BD%EA%B3%84%EA%B0%80%20%EC%A7%88%EC%9D%98%20%EA%B2%BD%EB%A1%9C%EB%A5%BC%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) · [02-02](../08_cloud/book/learning-coredns/02-02.%EB%A0%88%EC%BD%94%EB%93%9C%20%ED%95%9C%20%EC%A4%84%EC%9D%84%20%EC%9D%BD%EC%9C%BC%EB%A9%B4%20%EC%A1%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%20%EC%9D%BD%ED%9E%8C%EB%8B%A4.md) | Learning CoreDNS 2장 · TCP/IP Illustrated 11장 |
| HTTP/1.1 · HTTP/2 · 멀티플렉싱 | 필수 | [02-02](../02_os/book/cntd_computer-networking-top-down/02-02.%EC%9B%B9%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%EA%B0%80.md) · [01-02](../08_cloud/book/networking-and-kubernetes/01-02.HTTP%EC%97%90%EC%84%9C%20TCP%C2%B7TLS%C2%B7UDP%EA%B9%8C%EC%A7%80%20%E2%80%94%20Transport%20%EA%B3%84%EC%B8%B5%20%ED%95%B4%EB%B6%80.md) | HTTP/2 in Action 4·8장 |
| TLS 핸드셰이크 · SNI · ECH | 필수 | [04-01](../02_os/book/paw_packet-analysis-wireshark/04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) · [08-03](../02_os/book/cntd_computer-networking-top-down/08-03.%EC%82%B4%EC%95%84%20%EC%9E%88%EB%8A%94%20%EC%83%81%EB%8C%80%EB%A5%BC%20%ED%99%95%EC%9D%B8%ED%95%98%EA%B3%A0%20%EB%A9%94%EC%9D%BC%EA%B3%BC%20TCP%20%EC%97%90%20%EB%B6%99%EC%9E%85%EB%8B%88%EB%8B%A4.md) | HPBN 4장 · Real-World Cryptography 9장 |
| 인증서 체인 · SAN 호스트명 검증 · 유효 기간 | 필수 |  | HPBN 4장 |
| TLS 1.3 · 0-RTT · session resumption · ALPN | 추천 |  | Real-World Cryptography 9장 · HPBN 4장 |
| QUIC · HTTP/3 | 추천 | | HTTP/2 in Action 9장 |
| HTTP 성능 축 | 대체 | | High Performance Browser Networking 11·12장 |
| WebSocket · HTTP Upgrade | 선택 | [03-01](../09_spring/03_network/realtime/03-01.WebSocket%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%EA%B3%BC%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC.md) | High Performance Browser Networking 17장 |
| UDP · 단편화 | 추천 | [03-01](../02_os/book/cntd_computer-networking-top-down/03-01.%ED%8A%B8%EB%9E%9C%EC%8A%A4%ED%8F%AC%ED%8A%B8%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 10장 |
| reverse proxy · half-close · 배압 | 추천 | | |
| TLS passthrough 대 TLS 종료 · SNI 라우팅 | 추천 | [13-03](../08_cloud/book/kubernetes-in-action/13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md) | Kubernetes in Action 13장 |
| Forwarded · X-Forwarded-For 신뢰 경계 · PROXY protocol | 추천 |  |  |
| listen 큐 · accept 큐 · ephemeral 포트 고갈 | 추천 | [10-02](../02_os/book/systems-performance/10-02.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%282%29%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) · [사례](../troubleshooting/os/2026-09-07_%EC%8B%A4%ED%8C%A8%EC%9C%A8%200.3%25%EA%B0%80%20%EC%82%AC%EB%9D%BC%EC%A7%80%EC%A7%80%20%EC%95%8A%EB%8A%94%20%EC%84%9C%EB%B2%84.md) | TCP/IP Illustrated 13장 · Systems Performance 10장 |
| TIME_WAIT · SYN cookies | 추천 |  | TCP/IP Illustrated 13장 |
| OS CA bundle · truststore | 선택 | [11-01](../08_cloud/book/container-security/11-01.TLS%EB%A1%9C%20%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0%20%E2%80%94%20%ED%82%A4%C2%B7%EC%9D%B8%EC%A6%9D%EC%84%9C%C2%B7CA%EC%9D%98%20%EC%97%AD%ED%95%A0.md) | Container Security 11장 |
| TCP keepalive | 선택 | | TCP/IP Illustrated 17장 |
| Nagle · delayed ACK | 선택 |  | TCP/IP Illustrated 15장 |

### 2단계 · Linux 경로

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| interface · MAC · ARP · NDP · neighbor | 필수 | [랩 02-01](../02_os/book/network-fundamentals-lab/02-01.%EA%B0%99%EC%9D%80%20%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%20%EC%95%88%EC%97%90%EC%84%9C%EB%A7%8C%20%ED%86%B5%ED%95%9C%EB%8B%A4.md) · [01-01](../02_os/networking/01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) | TCP/IP Illustrated 3·4장 |
| neighbor 테이블 포화 · `gc_thresh` | 선택 |  |  |
| IP 주소 체계 · 서브네팅 · CIDR | 필수 | [랩 01-01](../02_os/book/network-fundamentals-lab/01-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EC%9D%BD%EA%B3%A0%20%EB%8F%84%EA%B5%AC%20%EC%85%8B%EC%9D%84%20%EB%93%A0%EB%8B%A4.md) · [01-04](../02_os/networking/01-04.%EC%84%9C%EB%B8%8C%EB%84%A4%ED%8C%85%EA%B3%BC%20CIDR%20%E2%80%94%20%EC%A3%BC%EC%86%8C%20%EA%B3%B5%EA%B0%84%EC%9D%84%20%EC%9E%90%EB%A5%B4%EB%8A%94%20%EB%B2%95.md) | TCP/IP Illustrated 2·5장 |
| IPv6 주소 · SLAAC | 추천 | [04-04](../02_os/book/cntd_computer-networking-top-down/04-04.IPv6%20%EC%99%80%20%EC%9D%BC%EB%B0%98%ED%99%94%20%ED%8F%AC%EC%9B%8C%EB%94%A9.md) | TCP/IP Illustrated 2·6장 |
| 라우팅 테이블 · next hop · IP 포워딩 | 필수 | [랩 03-01](../02_os/book/network-fundamentals-lab/03-01.%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EB%A5%BC%20%EB%84%98%EC%9C%BC%EB%A9%B4%20%ED%85%8C%EC%9D%B4%EB%B8%94%EC%9D%B4%20%EC%A0%84%EB%B6%80%EB%8B%A4.md) · [01-03](../08_cloud/book/networking-and-kubernetes/01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) | TCP/IP Illustrated 5장 |
| data plane 과 control plane — 포워딩과 라우팅의 갈림 | 필수 | [04-01](../02_os/book/cntd_computer-networking-top-down/04-01.%EB%9D%BC%EC%9A%B0%ED%84%B0%EB%8A%94%20%EC%95%88%EC%97%90%EC%84%9C%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%98%EB%8A%94%EA%B0%80.md) · [05-03](../02_os/book/cntd_computer-networking-top-down/05-03.%EC%A0%9C%EC%96%B4%EB%A5%BC%20%EB%B0%96%EC%9C%BC%EB%A1%9C%20%EB%B9%BC%EA%B3%A0%20%EB%A7%9D%EC%9D%84%20%EB%93%A4%EC%97%AC%EB%8B%A4%EB%B4%85%EB%8B%88%EB%8B%A4.md) | Computer Networking 4·5장 |
| 비대칭 경로 · `rp_filter` | 추천 |  |  |
| 5-tuple · ECMP 해시 · 포트가 없어 흐름과 갈라지는 ICMP | 추천 | [진단 개념](../troubleshooting/_concepts/%ED%9D%90%EB%A6%84%EC%9D%84-%EA%B0%80%EB%A5%B4%EB%8A%94-%EB%8B%A4%EC%84%AF-%EA%B0%92.md) · [사례](../troubleshooting/os/2026-09-14_%EB%AA%87%EB%AA%87%20%EC%82%AC%EC%9A%A9%EC%9E%90%EB%A7%8C%20%EB%93%A4%EC%96%B4%EC%98%A4%EC%A7%80%20%EB%AA%BB%ED%95%98%EB%8A%94%20%EC%82%AC%EC%9D%B4%ED%8A%B8.md) |  |
| network namespace · veth · bridge | 필수 | [01-01](../02_os/networking/01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) · [02-04](../08_cloud/book/networking-and-kubernetes/02-04.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) | Networking and Kubernetes 2장 |
| netfilter hook · iptables · nftables | 필수 | [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) · [02-01](../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 7장 |
| NAT · SNAT · DNAT · MASQUERADE | 필수 | [랩 05-01](../02_os/book/network-fundamentals-lab/05-01.%EC%97%B0%EA%B2%B0%EC%9D%80%20%EC%96%91%20%EB%81%9D%EB%A7%8C%EC%9D%98%20%EC%9D%BC%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%8B%A4.md) · [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 7장 |
| conntrack · 상태 테이블 포화 | 필수 | [랩 05-01](../02_os/book/network-fundamentals-lab/05-01.%EC%97%B0%EA%B2%B0%EC%9D%80%20%EC%96%91%20%EB%81%9D%EB%A7%8C%EC%9D%98%20%EC%9D%BC%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%8B%A4.md) · [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | Networking and Kubernetes 2장 |
| MTU · MSS · PMTUD | 필수 | [랩 06-01](../02_os/book/network-fundamentals-lab/06-01.%EC%9E%91%EC%9D%80%20%EA%B2%83%EC%9D%80%20%EB%90%98%EA%B3%A0%20%ED%81%B0%20%EA%B2%83%EB%A7%8C%20%EB%A9%8E%EB%8A%94%EB%8B%A4.md) · [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 10장 |
| PMTUD 블랙홀 · `tcp_mtu_probing` | 추천 | [사례](../troubleshooting/os/2026-09-14_%EB%AA%87%EB%AA%87%20%EC%82%AC%EC%9A%A9%EC%9E%90%EB%A7%8C%20%EB%93%A4%EC%96%B4%EC%98%A4%EC%A7%80%20%EB%AA%BB%ED%95%98%EB%8A%94%20%EC%82%AC%EC%9D%B4%ED%8A%B8.md) |  |
| ICMP · traceroute | 추천 | [랩 03-01](../02_os/book/network-fundamentals-lab/03-01.%EC%84%B8%EA%B7%B8%EB%A8%BC%ED%8A%B8%EB%A5%BC%20%EB%84%98%EC%9C%BC%EB%A9%B4%20%ED%85%8C%EC%9D%B4%EB%B8%94%EC%9D%B4%20%EC%A0%84%EB%B6%80%EB%8B%A4.md) · [랩 07-01](../02_os/book/network-fundamentals-lab/07-01.%EA%B8%B8%EC%9D%80%20%EB%A9%80%EC%A9%A1%ED%95%9C%EB%8D%B0%20%EC%95%88%20%ED%86%B5%ED%95%A0%20%EB%95%8C.md) · [05-04](../02_os/book/cntd_computer-networking-top-down/05-04.%EC%8B%A4%EC%8A%B5%20-%20traceroute%C2%B7ICMP%C2%B7%ED%9D%90%EB%A6%84%20%ED%91%9C%EB%A5%BC%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%A9%EB%8B%88%EB%8B%A4.md) | TCP/IP Illustrated 8장 |
| 컨테이너 네트워킹 모드 · 포트 매핑 | 추천 | [03-02](../08_cloud/book/networking-and-kubernetes/03-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%93%9C%EC%99%80%20CNI%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EA%B1%B0%EB%9E%98.md) · [03-03](../08_cloud/book/networking-and-kubernetes/03-03.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%2C%20%EB%8B%A4%EB%A5%B8%20%ED%98%B8%EC%8A%A4%ED%8A%B8.md) | Networking and Kubernetes 3장 |
| VLAN · 802.1Q · STP | 추천 | [06-04](../02_os/book/cntd_computer-networking-top-down/06-04.%EC%8A%A4%EC%9C%84%EC%B9%98%EB%8A%94%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%B0%B0%EC%9A%B0%EA%B3%A0%20%EB%AC%B4%EC%97%87%EC%9C%BC%EB%A1%9C%20%EA%B0%88%EB%9D%BC%EB%86%93%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 3장 |
| DHCP · 자동 구성 | 선택 | [05-01](../02_os/book/paw_packet-analysis-wireshark/05-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%98%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) | TCP/IP Illustrated 6장 |
| NAT traversal · STUN · TURN · ICE | 선택 |  | TCP/IP Illustrated 7장 |
| bonding · LACP | 선택 |  | TCP/IP Illustrated 3장 |
| policy routing · `ip rule` · VRF | 선택 | | |
| 동적 라우팅 · OSPF · BGP 인접과 광고 | 선택 | [랩 03-02](../02_os/book/network-fundamentals-lab/03-02.%EB%9D%BC%EC%9A%B0%ED%8A%B8%EA%B0%80%20%EC%8A%A4%EC%8A%A4%EB%A1%9C%20%EA%B1%B8%EC%96%B4%EC%98%A4%EA%B2%8C%20%ED%95%9C%EB%8B%A4.md) | |
| iBGP 풀메시 · 경로 반사기 | 선택 | [05-02](../02_os/book/cntd_computer-networking-top-down/05-02.AS%20%EC%95%88%EA%B3%BC%20AS%20%EC%82%AC%EC%9D%B4.md) · [진단 개념](../troubleshooting/_concepts/%EB%85%B8%EB%93%9C-%EA%B0%84-%EA%B2%BD%EB%A1%9C%EB%A5%BC-%EB%88%84%EA%B0%80-%ED%8D%BC%EB%9C%A8%EB%A6%AC%EB%8A%94%EA%B0%80.md) | Computer Networking Top-Down 5장 |

### 3단계 · 관측

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 캡처 위치 · 캡처 필터 · 디스플레이 필터 | 필수 | [02-01](../02_os/book/paw_packet-analysis-wireshark/02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) · [02-02](../02_os/book/paw_packet-analysis-wireshark/02-02.%EC%9E%A1%EC%9D%80%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md) | Packet Analysis 2장 |
| tcpdump · tshark | 필수 | [02-01](../02_os/book/paw_packet-analysis-wireshark/02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) · [10-04](../02_os/book/systems-performance/10-04.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) | Packet Analysis 2장 · Systems Performance 10장 |
| 무엇을 보려면 무엇을 치는가 — 도구와 단위 | 필수 | [진단 개념](../troubleshooting/_concepts/%EB%AC%B4%EC%97%87%EC%9D%84-%EB%B3%B4%EB%A0%A4%EB%A9%B4-%EB%AC%B4%EC%97%87%EC%9D%84-%EC%B9%98%EB%8A%94%EA%B0%80.md) | |
| 패킷이 사라지는 네 자리 — 드롭 카운터 | 필수 | [진단 개념](../troubleshooting/_concepts/%ED%8C%A8%ED%82%B7%EC%9D%B4-%EC%82%AC%EB%9D%BC%EC%A7%80%EB%8A%94-%EB%84%A4-%EC%9E%90%EB%A6%AC.md) | |
| conntrack 경합 · `insert_failed` | 필수 | [사례](../troubleshooting/kubernetes/2026-09-12_%EC%A0%95%ED%99%95%ED%9E%88%201%EC%B4%88%EC%94%A9%20%EB%8A%A6%EB%8A%94%20%EC%9A%94%EC%B2%AD.md) |  |
| TCP 이상 판독 · RST · 재전송 · 중복 ACK | 필수 | [03-01](../02_os/book/paw_packet-analysis-wireshark/03-01.TCP%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0.md) · [03-02](../02_os/book/paw_packet-analysis-wireshark/03-02.TCP%EA%B0%80%20%EC%96%B4%EA%B8%8B%EB%82%A0%20%EB%95%8C.md) | Packet Analysis 3장 |
| TLS 핸드셰이크 판독 · 실패 원인 | 필수 | [04-01](../02_os/book/paw_packet-analysis-wireshark/04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) · [04-02](../02_os/book/paw_packet-analysis-wireshark/04-02.%EC%97%B4%EC%87%A0%EC%99%80%20%EC%8B%A4%ED%8C%A8.md) | Packet Analysis 4장 |
| 계층 순서 진단 — `ss` · `ip` · `ethtool` · `conntrack -L` | 필수 | [02-03](../08_cloud/book/networking-and-kubernetes/02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) | Networking and Kubernetes 2장 |
| `nstat` · tcpretrans · tcplife | 추천 | [10-04](../02_os/book/systems-performance/10-04.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%284%29%20%E2%80%94%20%EA%B4%80%EC%B8%A1%20%EB%8F%84%EA%B5%AC.md) | Systems Performance 10장 |
| `resolv.conf` · search domain · `ndots` · NXDOMAIN | 필수 | [랩 07-01](../02_os/book/network-fundamentals-lab/07-01.%EA%B8%B8%EC%9D%80%20%EB%A9%80%EC%A9%A1%ED%95%9C%EB%8D%B0%20%EC%95%88%20%ED%86%B5%ED%95%A0%20%EB%95%8C.md) · [01-03](../02_os/networking/01-03.DNS%20%ED%95%84%ED%84%B0%EB%A7%81%20%EC%B0%A8%EB%8B%A8%20%E2%80%94%20NXDOMAIN%C2%B7DoH%C2%B7%EC%9A%B0%ED%9A%8C%20%EB%A7%88%EC%B0%B0.md) | |
| EDNS(0) · TC 비트 · TCP fallback | 추천 |  | TCP/IP Illustrated 11장 |
| Corefile · 플러그인 체인 | 추천 | [03-01](../08_cloud/book/learning-coredns/03-01.Corefile%EC%9D%80%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) · [03-02](../08_cloud/book/learning-coredns/03-02.%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%20%EC%9D%BC%EA%B3%B1%EC%9D%B4%EB%A9%B4%20%EC%84%9C%EB%B2%84%20%ED%95%98%EB%82%98%EA%B0%80%20%EC%84%A0%EB%8B%A4.md) | Learning CoreDNS 3장 |
| 질문과 답의 불일치 | 추천 | [07-01](../08_cloud/book/learning-coredns/07-01.%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%EC%9D%B4%20%EC%96%B4%EA%B8%8B%EB%82%98%EB%A9%B4%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EB%B2%84%EB%A6%B0%EB%8B%A4.md) | Learning CoreDNS 7장 |
| 연결 지연 분포 · P99 · 측정 오차 | 선택 | [10-02](../02_os/book/systems-performance/10-02.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%282%29%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Systems Performance 10장 |
| GRO · GSO · TSO 오프로딩 | 선택 | [10-02](../02_os/book/systems-performance/10-02.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%282%29%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Systems Performance 10장 |
| RSS · RPS · XPS · ring buffer | 선택 | [10-02](../02_os/book/systems-performance/10-02.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%282%29%20%E2%80%94%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Systems Performance 10장 |
| `tc qdisc` · `netem` | 선택 | [10-03](../02_os/book/systems-performance/10-03.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%283%29%20%E2%80%94%20%EB%B0%A9%EB%B2%95%EB%A1%A0%C2%B7%EC%8B%A4%ED%97%98%C2%B7%ED%8A%9C%EB%8B%9D.md) | Systems Performance 10장 |



## 클러스터 · 4~6단계

> 같은 커널 경로 위에 이름과 정책이 얹히고, 그 아래에 클라우드 underlay가 깔립니다.

### 4단계 · Kubernetes

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Pod IP · Pod CIDR · Node CIDR · pause container | 필수 | [04-01](../08_cloud/book/networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) | Networking and Kubernetes 4장 |
| IPAM 할당과 반납 · 노드별 Pod CIDR 블록 · IP 고갈 | 필수 | [사례](../troubleshooting/cloud/2026-09-09_%EC%A0%88%EB%B0%98%EB%A7%8C%20%EB%9C%A8%EA%B3%A0%20%EB%A9%88%EC%B6%98%20%EB%B0%B0%ED%8F%AC.md) | Cilium 4장 |
| CNI | 필수 | [04-02](../08_cloud/kubernetes/04_networking/04-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) · [04-02](../08_cloud/book/networking-and-kubernetes/04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) | Cilium 2장 |
| CNI 구현체 비교 — 무엇이 다른가 | 추천 |  | Cilium 1~3장 · Production Kubernetes 5장 |
| CNI 계약 — ADD · DEL · CHECK | 추천 | | Networking and Kubernetes 4장 |
| 오버레이 · VXLAN | 필수 | [랩 04-01](../02_os/book/network-fundamentals-lab/04-01.%EB%9D%BC%EC%9A%B0%ED%84%B0%20%EB%84%88%EB%A8%B8%EC%97%90%20%EA%B0%99%EC%9D%80%20L2%EB%A5%BC%20%EB%A7%8C%EB%93%A0%EB%8B%A4.md) · [04-03](../08_cloud/kubernetes/04_networking/04-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | Cilium 5장 |
| underlay 와 overlay 의 갈림 | 추천 | | Cloud Native Data Center Networking 6장 |
| Service · EndpointSlice · Service 5유형 | 필수 | [04-04](../08_cloud/kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md) · [05-02](../08_cloud/book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) · [사례](../troubleshooting/kubernetes/2026-09-07_Pod%20%EB%A1%9C%EB%8A%94%20%EB%90%98%EA%B3%A0%20%EC%9D%B4%EB%A6%84%EC%9C%BC%EB%A1%9C%EB%8A%94%20%EC%95%88%20%EB%90%98%EB%8A%94%20%ED%98%B8%EC%B6%9C.md) | Networking and Kubernetes 5장 |
| kube-proxy — iptables · IPVS · eBPF | 필수 | [02-02](../08_cloud/book/networking-and-kubernetes/02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) | Networking and Kubernetes 2장 |
| kube-proxy replacement · Maglev · DSR | 추천 |  | Cilium 6장 |
| headless Service · sessionAffinity · `internalTrafficPolicy` | 추천 | [11-01](../08_cloud/book/kubernetes-in-action/11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md) · [16-01](../08_cloud/book/kubernetes-in-action/16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md) · [17-03](../08_cloud/book/kubernetes-in-action/17-03.%EB%A1%9C%EC%BB%AC%20daemon%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%20%E2%80%94%20hostPort%C2%B7hostNetwork%C2%B7internalTrafficPolicy.md) | Kubernetes in Action 11·16·17장 |
| readiness 와 endpoint 자격 · stale Endpoint | 필수 | [11-03](../08_cloud/book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) · [사례](../troubleshooting/kubernetes/2026-09-12_%EB%B0%B0%ED%8F%AC%ED%95%A0%20%EB%95%8C%EB%A7%88%EB%8B%A4%20%EC%9E%A0%EA%B9%90%20%EB%82%98%EC%98%A4%EB%8A%94%20502.md) | Kubernetes in Action 11장 |
| 클러스터 DNS · Service FQDN | 필수 | [04-05](../08_cloud/kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md) · [06-01](../08_cloud/book/learning-coredns/06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | Learning CoreDNS 6장 |
| NodeLocal DNSCache | 추천 |  |  |
| service discovery · east-west traffic | 추천 | | |
| Ingress | 필수 | [04-06](../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) · [05-03](../08_cloud/book/networking-and-kubernetes/05-03.Ingress%EC%99%80%20Service%20Mesh%20%E2%80%94%20L7%EC%9D%98%20%EB%91%90%20%EC%B8%B5.md) | Networking and Kubernetes 5장 · Kubernetes in Action 12장 |
| Gateway API · HTTPRoute | 추천 | [04-06](../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) | Kubernetes in Action 13장 · Cilium 7장 |
| L4 로드밸런싱 — health check · round-robin · least connections · draining | 추천 | | |
| 연결 단위와 요청 단위 분산 — HTTP/2 · gRPC 장기 연결 편중 | 추천 |  |  |
| LB idle timeout 과 keepalive 수명 불일치 | 추천 |  |  |
| 인증서 만료와 TLS 실패 구분 | 추천 | | |
| `externalTrafficPolicy` · 소스 IP 보존 | 추천 | [11-02](../08_cloud/book/kubernetes-in-action/11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) | Kubernetes in Action 11장 |

### 5단계 · 클라우드 네트워크

> 클러스터가 서 있는 underlay입니다. 소장본이 AWS 에 치우쳐 있어 GCP · Azure 의 세부는 각 공식 문서로 메웁니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| VPC · 서브넷 · 라우트 테이블 · IGW · NAT GW | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| Security Group · NACL — stateful 과 stateless | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| 클라우드 로드밸런서 — L4 와 L7 | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| 3사 기본값의 갈림 | 추천 | [06-02](../08_cloud/book/networking-and-kubernetes/06-02.GCP%C2%B7Azure%EC%99%80%203%EC%82%AC%20%EB%B9%84%EA%B5%90%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%EB%AC%B8%EC%A0%9C%2C%20%EB%8B%A4%EB%A5%B8%20%EA%B8%B0%EB%B3%B8%EA%B0%92.md) | Networking and Kubernetes 6장 |
| VPN · 사이트 간 연결 · IPsec | 추천 | [08-04](../02_os/book/cntd_computer-networking-top-down/08-04.%EB%A7%9D%20%EA%B3%84%EC%B8%B5%EC%97%90%20%ED%86%B5%EC%A7%B8%EB%A1%9C%20%EC%94%8C%EC%9A%B0%EA%B3%A0%20%EB%AC%B4%EC%84%A0%EC%97%90%20%EB%B6%99%EC%9E%85%EB%8B%88%EB%8B%A4.md) | System Design on AWS 9장 |
| AWS Direct Connect · 전용선 | 추천 |  | System Design on AWS 9장 |
| PrivateLink · VPC endpoint | 추천 |  | System Design on AWS 9장 |
| Clos 토폴로지 · BGP · ECMP | 선택 |  | Cloud Native Data Center Networking 2·14장 |
| VPC 피어링 · Transit Gateway | 선택 |  | System Design on AWS 9장 |

### 6단계 · 데이터패스와 정책

> 노트 열이 대부분 비어 있습니다. 소장본은 있고 정독을 아직 안 한 구간입니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| NetworkPolicy · ingress · egress · default deny | 필수 | [04-07](../08_cloud/kubernetes/04_networking/04-07.NetworkPolicy.md) · [04-03](../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) | Cilium 12장 |
| L7 정책 · FQDN 정책 | 추천 | | Cilium 13장 |
| identity-aware policy | 추천 | | Cilium 12장 |
| eBPF 프로그램 구조 · 유형 · attach | 추천 | | Learning eBPF 3·7장 |
| XDP · TC hook | 추천 | | Learning eBPF 7·8장 |
| eBPF map · helper | 추천 | | Learning eBPF 3장 |
| verifier · CO-RE · BTF | 추천 | | Learning eBPF 5·6장 |
| eBPF 네트워킹 | 추천 | [01-01](../02_os/networking/01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) | Learning eBPF 8장 |
| Cilium 데이터패스 · IPAM | 추천 | | Cilium 4·5장 |
| Hubble 관측 | 선택 | | Cilium 15장 |
| L4 와 L7 텔레메트리의 갈림 | 추천 | | |
| Beyla · Caretta — 자동 계측과 토폴로지 추출 | 선택 | | |
| 투명 암호화 · WireGuard | 선택 | | Cilium 14장 |
| 클러스터 access · egress 게이트웨이 | 선택 | | Cilium 10·11장 |
| eBPF host routing · netkit · bandwidth manager | 선택 |  | Cilium 8장 |



## 운영 경계와 오버레이 · 7~9단계

> 클러스터가 한 종류가 아닐 때, 그리고 노드끼리 서로를 모르는 채로 만날 때 생기는 문제들입니다.

### 7단계 · 운영 경계

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| dual-stack · `ipFamilyPolicy` | 추천 | [04-08](../08_cloud/kubernetes/04_networking/04-08.IPv4%EC%99%80%20IPv6%20%EC%9D%B4%EC%A4%91%20%EC%8A%A4%ED%83%9D.md) | |
| topology-aware routing · EndpointSlice hint | 추천 | [04-09](../08_cloud/kubernetes/04_networking/04-09.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EC%9D%B8%EC%A7%80%20%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | |
| 서비스 메시가 인프라로 밀어낸 것 | 추천 | [01-01](../08_cloud/book/istio-in-action/01-01.%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%A9%94%EC%8B%9C%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%9D%B8%ED%94%84%EB%9D%BC%EB%A1%9C%20%EB%B0%80%EC%96%B4%EB%83%88%EB%8A%94%EA%B0%80.md) | Istio in Action 1장 |
| Envoy · Gateway · VirtualService · DestinationRule | 추천 | [03-01](../08_cloud/book/istio-in-action/03-01.Envoy%EA%B0%80%20%EB%A7%A1%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20Istio%EA%B0%80%20%EB%B3%B4%ED%83%9C%EB%8A%94%20%EC%9D%BC.md) · [04-01](../08_cloud/book/istio-in-action/04-01.%EB%AC%B8%EC%9D%84%20%EC%97%AC%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EA%B8%B8%EC%9D%84%20%EB%82%B4%EB%8A%94%20%EC%9D%BC%EC%9D%84%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) · [05-01](../08_cloud/book/istio-in-action/05-01.%EC%9C%84%ED%97%98%EC%97%90%20%EB%85%B8%EC%B6%9C%EB%90%98%EB%8A%94%20%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%84%20%EC%A4%84%EC%97%AC%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | Istio in Action 3·4·5장 |
| mTLS · 기본값 닫아 가기 | 추천 | [09-01](../08_cloud/book/istio-in-action/09-01.%EA%B1%B0%EC%9D%98%20%EC%95%88%EC%A0%84%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EA%B0%92%EC%9D%84%20%EB%8B%AB%EC%95%84%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | Istio in Action 4·9장 |
| retry · timeout · circuit breaking · outlier detection · 재시도 증폭 | 필수 | [06-01](../08_cloud/book/istio-in-action/06-01.%EC%8B%A4%ED%8C%A8%EB%A5%BC%20%EA%B2%AC%EB%94%94%EB%8A%94%20%EC%9D%BC%EC%9D%84%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%EC%98%AE%EA%B2%BC%EC%9D%84%20%EB%95%8C.md) · [사례](../troubleshooting/mesh/2026-09-07_%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%B4%20%EB%8A%98%20%EB%95%8C%EB%A7%8C%20%EC%84%9E%EC%97%AC%20%EB%82%98%EC%98%A4%EB%8A%94%20503.md) | Istio in Action 6장 |
| SPIFFE · SVID — 워크로드 신원 | 추천 | [a0-03](../08_cloud/book/istio-in-action/a0-03.%EB%B6%80%EB%A1%9D%20%E2%80%94%20%EC%8B%A0%EC%9B%90%EC%9D%84%20%EB%AC%B8%EC%84%9C%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%84%A4%20%EA%B7%9C%EA%B2%A9.md) | Istio in Action 부록 C · Zero Trust Networks 6장 |
| Windows HNS · HCS · Windows CNI | 선택 | [04-10](../08_cloud/kubernetes/04_networking/04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | |
| 데이터 플레인 진단 · `istioctl proxy-config` | 선택 | [10-01](../08_cloud/book/istio-in-action/10-01.%ED%94%84%EB%A1%9D%EC%8B%9C%EB%8A%94%20%EB%8B%A4%20%EC%95%8C%EA%B3%A0%20%EC%9E%88%EA%B3%A0%20%EC%82%AC%EB%9E%8C%EC%9D%80%20%EB%AA%BB%20%EC%9D%BD%EB%8A%94%EB%8B%A4.md) | Istio in Action 10장 |
| Zero Trust 전제 · 신뢰 관리 | 선택 | [12-01](../08_cloud/book/istio-in-action/12-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%EC%9A%B0%EB%8A%94%20%EC%A0%84%EC%A0%9C%20%EC%85%8B%EA%B3%BC%20%EB%82%A8%EB%8A%94%20%ED%95%9C%20%EC%9E%90%EB%A6%AC.md) | Zero Trust Networks 1·2·8장 |
| 멀티클러스터 메시 | 선택 | | Cilium 9장 |
| ambient mode · ztunnel · waypoint | 대체 | | Sidecar-less Istio Explained 1~3장 |

### 8단계 · 오버레이와 신뢰

> 기술 이름이 아니라 문제를 배우는 자리입니다. Tor · I2P · libp2p · WireGuard · Consul 은 같은 문제에 대한 서로 다른 답입니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| identity 와 trust 의 차이 · 인증과 인가의 차이 | 필수 |  | Zero Trust Networks 2·4·6장 |
| traffic correlation · metadata · timing side-channel | 필수 |  |  |
| 암호화가 숨기는 것과 숨기지 않는 것 | 필수 | | Real-World Cryptography 9·10장 |
| bootstrap · reseed · 최초 접점 · trust anchor | 추천 | | |
| peer discovery · DHT · Kademlia · gossip · membership | 추천 |  | Patterns of Distributed Systems 7·28장 · Database Internals 12장 |
| lease · TTL 갱신 | 추천 |  | Patterns of Distributed Systems 26장 |
| signed descriptor · 공개키 신원 · 키에서 나온 주소 · 무결성 | 추천 | | Real-World Cryptography 2·7장 |
| key rotation · replay 방지 · freshness | 추천 |  | Real-World Cryptography 3·8·9장 |
| Sybil · eclipse · poisoning · behavior score | 추천 |  |  |
| 오버레이 — 물리와 논리의 분리 · 터널링 · 가상 토폴로지 | 추천 | | |
| reverse tunnel · outbound-only relay | 추천 |  |  |
| relay · hole punching · reachability | 선택 |  | TCP/IP Illustrated 7장 |
| keyless TLS · trusted edge — 서명 권한이 곧 신뢰 | 선택 |  |  |
| capability — 신원 대신 권한을 건네는 토큰 | 선택 |  | API Security in Action 9장 |
| 역할이 나뉜 피어 — DHT 서버 모드와 floodfill | 선택 |  |  |

**같은 질문이 이름만 바꿔 되풀이됩니다.** 아직 아무도 모르는 노드가 처음 네트워크에 어떻게 들어오는가는 Kubernetes node discovery, etcd cluster join, Kafka broker discovery, VPN mesh에서 같은 형태로 나옵니다. 그래서 이 단계를 마지막에 두되 특정 제품을 학습 대상으로 두지 않습니다.

### 9단계 · 터널과 경로

> 노드를 골랐다고 길이 나는 것은 아닙니다. 여기서는 실패가 곱으로 쌓이는 구조를 셈으로 다룹니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 피어 발견 성공과 터널 구성 성공은 다르다 | 필수 | | |
| 멀티홉 — 홉 수가 지연 · 성공률 · 프라이버시에 미치는 값 | 필수 | | |
| 홉별 계층 암호화 — 각 홉은 앞뒤만 안다 | 추천 | | |
| path selection · latency · 가용성 · 다양성 · 비용 함수 | 필수 | | |
| subnet · ASN · operator diversity · selection bias | 추천 | | |
| inbound 와 outbound — 단방향 터널을 조합한 양방향 통신 | 추천 | | |
| RX 와 TX 경로를 나누는 이유 | 추천 | | |
| 클라이언트가 경로를 정하고 서버는 목록만 준다 | 추천 | | |
| 종단 성공 확률 — 단계별 실패가 곱으로 쌓인다 | 필수 | | |
| 기하분포 — 최초 성공까지의 평균 시도 횟수 | 추천 | | |
| 재시도와 타임아웃 · heartbeat — 확률만큼 감지 시간도 값이다 | 필수 |  | Patterns of Distributed Systems 7장 · Database Internals 9장 |
| exponential backoff · jitter · retry budget | 필수 | [01-03](../09_spring/03_network/resilience/01-03.Retry%20%E2%80%94%20exponential%20backoff%C2%B7jitter%C2%B7%EC%9E%AC%EC%8B%9C%EB%8F%84%20%ED%8F%AD%EC%A3%BC%20%EB%B0%A9%EC%A7%80.md) · [사례](../troubleshooting/kubernetes/2026-09-08_%ED%95%9C%20%ED%95%98%EC%9C%84%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%97%90%EC%84%9C%20%EC%8B%9C%EC%9E%91%EB%90%9C%20%EC%A0%84%EB%A9%B4%20%EC%98%A4%EB%A5%98.md) |  |
| 터널 풀 — 연결마다 새로 여는 방식과의 갈림 | 추천 | | |
| 예비 터널 — 준비 비용 · 전환 시간 · 자원 사용량 | 추천 | | |
| 터널 수명과 교체 — 자주 바꾸면 비싸고 드물게 바꾸면 트래픽이 묶인다 | 추천 | | |




## 손으로 확인하는 실습

> 노트 안에 실제로 있는 실습 절만 적습니다. 지어낸 출처를 채우지 않았습니다.

| 출처 | 단계 | 무엇 |
|---|:---:|---|
| [패킷 캡처 실습](../08_cloud/book/networking-and-kubernetes/01-04.%ED%8C%A8%ED%82%B7%20%EC%BA%A1%EC%B2%98%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%201%EC%9E%A5%20%EA%B0%9C%EB%85%90%EC%9D%84%20%EB%88%88%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0.md) | 1·3 | 계층 개념을 캡처로 확인 |
| [5장 실습](../02_os/book/cntd_computer-networking-top-down/05-04.%EC%8B%A4%EC%8A%B5%20-%20traceroute%C2%B7ICMP%C2%B7%ED%9D%90%EB%A6%84%20%ED%91%9C%EB%A5%BC%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%A9%EB%8B%88%EB%8B%A4.md) | 1·2 | traceroute · ICMP · 흐름 표 |
| [커널 네트워킹 실습](../08_cloud/book/networking-and-kubernetes/02-04.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) · [실습 2](../08_cloud/book/networking-and-kubernetes/02-05.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%202%20%E2%80%94%20%EB%A7%89%EA%B3%A0%2C%20%EC%A7%84%EB%8B%A8%ED%95%98%EA%B3%A0%2C%20%EB%82%98%EB%88%84%EA%B8%B0.md) | 2 | client · router · server namespace 를 veth 로 잇고 NAT·conntrack 확인 |
| [패킷을 잡는 법](../02_os/book/paw_packet-analysis-wireshark/02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) | 3 | 캡처 위치와 필터 |
| [컨테이너 네트워크 실습](../08_cloud/book/networking-and-kubernetes/03-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EB%A7%A8%EC%86%90%20%EB%B0%B0%EC%84%A0%EC%97%90%EC%84%9C%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%EA%B9%8C%EC%A7%80.md) | 2·4 | 맨손 배선에서 포트 매핑까지 |
| [Kubernetes 네트워크 실습](../08_cloud/book/networking-and-kubernetes/04-04.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20CNI%20%EB%B6%80%EC%9E%AC%EB%B6%80%ED%84%B0%20%EC%A0%95%EC%B1%85%C2%B7DNS%EA%B9%8C%EC%A7%80.md) | 4·6 | CNI 부재 · 정책 · DNS |
| [troubleshooting/os](../troubleshooting/os/README.md) · [cloud](../troubleshooting/cloud/README.md) · [mesh](../troubleshooting/mesh/README.md) | 1~4·7 | 증상에서 원인 역추적 여섯 편 |
| [network-fundamentals-lab](../02_os/book/network-fundamentals-lab/README.md) | 1~4 | 고장이 장전된 containerlab 18편 — ARP·라우팅·NAT·MTU·DNS 를 깨뜨려 증상으로 되짚는다 |
| [troubleshooting/kubernetes](../troubleshooting/kubernetes/README.md) | 4·7 | 이름 해석 · DNS 연쇄 장애 · 배포 중 502 · 정확히 1초 지연 · 업그레이드 2분 뒤 멈춘 클러스터 |

5·7단계 자리는 비어 있습니다. 클라우드 축은 계정과 과금이 걸리고, 서비스 메시는 컨트롤 플레인이 서야 재현됩니다.

**노트 밖의 실습 경로가 둘 있습니다.** [LFS146 Introduction to Cilium](https://training.linuxfoundation.org/training/introduction-to-cilium-lfs146/)은 무료 26시간 과정으로 NetworkPolicy · Hubble · 투명 암호화 · kube-proxy replacement · Cluster Mesh 를 6·7단계 범위에서 손으로 밟게 합니다. [Isovalent Universe](https://labs.isovalent.com/)는 설치 없이 브라우저에서 도는 랩이라 클러스터를 세울 수 없을 때 씁니다.

**reverse tunnel 은 실제 구현을 돌려 봅니다.** [portal-tunnel](https://github.com/gosuda/portal-tunnel)은 MIT 라이선스로 공개된 Go reverse tunnel 이고 relay 를 직접 띄울 수 있습니다. 1단계의 SNI 라우팅과 8·9단계의 lease · keyless TLS · relay 선택이 한 저장소에 모여 있습니다. 코드를 따라 짜는 일은 Go 로드맵 몫입니다.

**장애를 주입해 확인할 목록을 따로 둡니다.** 실습 자료가 없는 자리도 증상은 만들 수 있습니다.

| 주입할 장애 | 겉으로 보이는 증상 | 확인할 증거 |
|---|---|---|
| 잘못된 Service selector | ClusterIP 접속 실패 | EndpointSlice 가 비어 있음 |
| readiness 실패 | 일부 endpoint 제외 | Pod condition 과 EndpointSlice readiness |
| CoreDNS 정지 | 이름 접근만 실패 | DNS timeout · SERVFAIL |
| 높은 `ndots` | 첫 요청 지연 | DNS query 순서 |
| NetworkPolicy default deny | TCP timeout | policy verdict 와 drop |
| MTU mismatch | 작은 요청만 성공 | fragmentation · ICMP PTB |
| conntrack 포화 | 간헐적 신규 연결 실패 | conntrack count · max |
| stale Endpoint | 특정 목적지만 reset | EndpointSlice 와 Pod lifecycle |
| 인증서 만료 | TCP 는 되고 TLS 만 실패 | TLS alert · 인증서 날짜 |

위 목록 중 **conntrack 포화**와 **MTU mismatch** 는 [network-fundamentals-lab](../02_os/book/network-fundamentals-lab/README.md) 의 09·12·13편이 이미 랩으로 재현합니다. 주입할 것을 새로 만들기 전에 그쪽을 먼저 돌립니다.



## 로드맵에 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| Kubernetes 오브젝트의 배포와 운영 | [Kubernetes 로드맵](k8s-roadmap.md)이 맡습니다 |
| socket · epoll · io_uring 의 커널 구현 | [OS 로드맵](os-roadmap.md) 2·6단계가 맡습니다 |
| tail latency · coordinated omission · 프로파일 | [OS 로드맵](os-roadmap.md) 4단계의 성능 방법론 축입니다 |
| metrics · logs · traces · OpenTelemetry | `06_observability` 소관입니다 |
| Go 로 프록시·로드밸런서를 구현하는 일 | [Go 로드맵](go-roadmap.md) 6단계가 맡습니다. 여기는 개념까지입니다 |
| Computer Networking 7장 | 무선과 이동성. 서버 운영과 접점이 적습니다 |
| Packet Analysis with Wireshark 6·7장 | 무선 캡처와 공격 분석. 판독 축이 아닙니다 |
| Learning CoreDNS 9장 | 플러그인을 *만드는* 쪽입니다. 필요가 생기면 3단계 뒤에 붙입니다 |



## 경계

> 이 문서가 정하는 것과 인접 문서에 넘기는 것입니다.

이 문서는 **개념의 순서와 우선순위**를 정합니다. 폴더 경계는 [02_os MOC](../02_os/README.md)와 [Kubernetes 네트워크 MOC](../08_cloud/kubernetes/04_networking/README.md)가 맡습니다.

맞닿는 문서가 셋입니다. socket과 파일 디스크립터의 커널 쪽은 [OS 로드맵](os-roadmap.md)이, 오브젝트 수준의 배포와 운영은 [Kubernetes 로드맵](k8s-roadmap.md)이, 프록시와 로드밸런서를 직접 구현하는 일은 [Go 로드맵](go-roadmap.md)이 맡습니다.

**OS 로드맵과는 network namespace에서 바통을 주고받습니다.** 그쪽 3단계가 namespace가 무엇을 가리는지까지 말하고 멈추면, 이쪽 2단계가 그 사이를 veth로 잇는 데서 시작합니다.
