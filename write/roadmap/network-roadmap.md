---
title: 네트워크 학습 로드맵
tags: [roadmap, linux, networking, kubernetes, cloud, ebpf, cilium, dns, security]
status: final
source:
  - ../02_os/networking/README.md
  - ../08_cloud/kubernetes/04_networking/README.md
  - ../08_cloud/book/networking-and-kubernetes/README.md
related:
  - README.md
  - os-roadmap.md
  - k8s-roadmap.md
  - ../02_os/networking/README.md
  - ../08_cloud/kubernetes/04_networking/README.md
updated: 2026-09-13
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
| 1 · 연결 | TCP 동작 | 상태 · 3-way handshake · 재전송 · 타임아웃 · RTT · 흐름 제어 · cwnd · in-flight · 혼잡 제어 · CUBIC · BBR · keepalive |
| 1 · 연결 | 이름과 응용 | DNS 질의 · HTTP/1.1 · HTTP/2 · 멀티플렉싱 · QUIC · HTTP/3 |
| 1 · 연결 | 보안 전송 | TLS 핸드셰이크 · SNI · ECH · OS CA bundle · truststore |
| 1 · 연결 | 중계와 한계 | reverse proxy · half-close · 배압 · listen 큐 · accept 큐 · ephemeral 포트 고갈 · UDP · 단편화 |
| 2 · Linux 경로 | 주소와 이웃 | interface · MAC · ARP · NDP · IP 주소 · 서브네팅 · CIDR |
| 2 · Linux 경로 | 경로 결정 | 라우팅 테이블 · next hop · IP 포워딩 · ICMP · traceroute · policy routing · `ip rule` · VRF |
| 2 · Linux 경로 | 가상 인터페이스 | network namespace · veth · bridge · 컨테이너 네트워킹 모드 · 포트 매핑 |
| 2 · Linux 경로 | 패킷 변형 | netfilter hook · iptables · nftables · NAT · SNAT · DNAT · MASQUERADE · conntrack |
| 2 · Linux 경로 | 크기와 구성 | MTU · MSS · PMTUD · DHCP · bonding · LACP · NAT traversal |
| 3 · 관측 | 캡처와 판독 | 캡처 위치 · 캡처 필터 · 디스플레이 필터 · RST · 재전송 · 중복 ACK · TLS 핸드셰이크 판독 |
| 3 · 관측 | 진단 방법론 | 도구와 단위의 대응 · 패킷이 사라지는 네 자리 · 드롭 카운터 읽기 |
| 3 · 관측 | 계층별 도구 | `ss` · `ip` · `ethtool` · `conntrack -L` · `nft list ruleset` |
| 3 · 관측 | 이름 진단 | `resolv.conf` · search domain · `ndots` · NXDOMAIN · Corefile · 플러그인 체인 · 응답 불일치 |
| 3 · 관측 | 측정의 함정 | 연결 지연 분포 · P99 · 측정 오차 · GRO · GSO · TSO 오프로딩 · `tc qdisc` · `netem` |
| 4 · Kubernetes | Pod 네트워크 | Pod IP · Pod CIDR · Node CIDR · pause container · CNI · CNI 계약 ADD·DEL·CHECK |
| 4 · Kubernetes | CNI 구현체 | Calico · Flannel · Cilium 의 갈림 · 라우팅 대 오버레이 · iptables 대 eBPF · 정책 표현력 |
| 4 · Kubernetes | 노드 간 전달 | 오버레이 · VXLAN · underlay 와 overlay 의 갈림 |
| 4 · Kubernetes | 서비스 추상화 | Service · EndpointSlice · Service 5유형 · kube-proxy · iptables · IPVS · readiness · stale Endpoint |
| 4 · Kubernetes | 이름과 진입 | 클러스터 DNS · Service FQDN · service discovery · east-west · Ingress · Gateway API · HTTPRoute |
| 4 · Kubernetes | 분배와 보존 | L4 로드밸런싱 · health check · round-robin · least connections · draining · `externalTrafficPolicy` · 소스 IP · 인증서 만료 구분 |
| 5 · 클라우드 | VPC 구성 | VPC · 서브넷 · 라우트 테이블 · IGW · NAT GW |
| 5 · 클라우드 | 경계 제어 | Security Group · NACL · stateful 과 stateless 의 갈림 |
| 5 · 클라우드 | 진입과 분배 | 클라우드 로드밸런서 · L4 · L7 |
| 5 · 클라우드 | 사이트 간 연결 | VPN · IPsec · AWS Direct Connect · 전용선 · VPC 피어링 · Transit Gateway |
| 5 · 클라우드 | 데이터센터 축 | Clos 토폴로지 · BGP · ECMP · 3사 기본값의 갈림 |
| 6 · 데이터패스 | 정책 모델 | NetworkPolicy · ingress · egress · default deny · L7 정책 · FQDN 정책 · identity-aware policy |
| 6 · 데이터패스 | eBPF 기초 | 프로그램 구조 · 유형 · attach · hook · map · helper · verifier · CO-RE · BTF |
| 6 · 데이터패스 | 데이터패스 구현 | XDP · TC hook · Cilium 데이터패스 · IPAM · eBPF host routing · bandwidth manager |
| 6 · 데이터패스 | 암호화와 관측 | 투명 암호화 · WireGuard · Hubble · egress 게이트웨이 · 클러스터 access |
| 7 · 운영 경계 | 주소와 배치 | dual-stack · `ipFamilyPolicy` · topology-aware routing · EndpointSlice hint |
| 7 · 운영 경계 | 혼합 환경 | Windows HNS · HCS · Windows CNI · 멀티클러스터 메시 |
| 7 · 운영 경계 | 메시 데이터 플레인 | 서비스 메시가 옮긴 것 · Envoy · Gateway · VirtualService · DestinationRule |
| 7 · 운영 경계 | 신원과 기본값 | mTLS · 기본값 닫아 가기 · Zero Trust 전제 · ambient · ztunnel · waypoint |
| 8 · 오버레이와 신뢰 | 진입 | bootstrap · reseed · 최초 접점 · trust anchor · stale data |
| 8 · 오버레이와 신뢰 | 발견 | peer discovery · DHT · Kademlia · gossip · membership · peer store |
| 8 · 오버레이와 신뢰 | 식별 | node ID · signed descriptor · 공개키 신원 · key rotation · replay · freshness |
| 8 · 오버레이와 신뢰 | 신뢰 | Sybil · eclipse · poisoning · identity 와 trust 의 차이 · 인증과 인가의 차이 · behavior score |
| 8 · 오버레이와 신뢰 | 관측 가능성 | traffic correlation · metadata · timing side-channel · 암호화가 숨기지 않는 것 |
| 8 · 오버레이와 신뢰 | 오버레이 | 물리와 논리의 분리 · 터널링 · 가상 토폴로지 · relay · hole punching · reachability |
| 9 · 터널과 경로 | 구성 | 터널 구성 · 피어 발견과의 차이 · 멀티홉 · 홉 수의 대가 · inbound 와 outbound 의 분리 · RX 와 TX |
| 9 · 터널과 경로 | 선택 | path selection · latency · 가용성 · subnet · ASN diversity · 비용 함수 · selection bias · 클라이언트가 정하는 경로 |
| 9 · 터널과 경로 | 확률 | 종단 성공 확률 · 곱으로 쌓이는 실패 · 기하분포 · 평균 시도 횟수 · 재시도 · 타임아웃 · 감지 시간 |
| 9 · 터널과 경로 | 자원 | 터널 풀 · 미리 열어 두기 · 예비 터널 · 준비 비용 · 전환 시간 · 자원 사용량 |



## 책 읽기 흐름

> 위 단계를 무엇으로 배우는가입니다. 책 열다섯이 각각 어느 단계의 무엇을 다루는지와 읽을 장을 적습니다.

![네트워크 책 읽기 흐름 — 우선순위와 읽을 장](_assets/network-books.svg)

통독하는 책은 셋뿐이고 나머지는 표의 `읽을 장`만 봅니다.

| 책 | 읽을 장 | 우선순위 | 자리 |
|---|---|:---:|---|
| [Computer Networking](../02_os/book/cntd_computer-networking-top-down/README.md) | 1~5장 | 필수 | 1단계 |
| TCP/IP Illustrated | 2~8 · 10~18장 | 필수 | 1·2단계 |
| [Networking and Kubernetes](../08_cloud/book/networking-and-kubernetes/README.md) | 전독 | 필수 | 2~6단계 |
| [Packet Analysis with Wireshark](../02_os/book/paw_packet-analysis-wireshark/README.md) | 1~5장 | 필수 | 3단계 |
| HTTP/2 in Action | 4·8·9장 | 추천 | 1단계 |
| [Learning CoreDNS](../08_cloud/book/learning-coredns/README.md) | 3·6·7장 | 추천 | 3·4단계 |
| Cloud Native Data Center Networking | 2·6·7·14장 | 추천 | 4·5단계 |
| Cilium Up and Running | 1~16장 | 필수 | 4~7단계 |
| Learning eBPF | 3·5~8장 | 추천 | 6단계 |
| [Istio in Action](../08_cloud/book/istio-in-action/README.md) | 1·3·4·5·9·12장 | 추천 | 7단계 |
| Zero Trust Networks | 1·2·6·8·10장 | 추천 | 7·8단계 |
| Real-World Cryptography | 5 · 7~10장 | 추천 | 8단계 |
| Patterns of Distributed Systems | 7·8장 | 추천 | 8·9단계 |
| High Performance Browser Networking | 2·4·11·12장 | 대체 | 1단계 — HTTP/2 in Action 자리 |
| Sidecar-less Istio Explained | 전 4장 | 대체 | 7단계 — Istio in Action 12장 자리 |

소장 목록은 계속 늘어납니다. 새 책이 들어오면 이 표와 아래 단계별 표의 `책` 열을 함께 갱신합니다.

**책만으로 안 되는 축이 둘입니다.** Gateway API 와 멀티클러스터는 소장본 중 Cilium 만 최신이라 [Gateway API 가이드](https://gateway-api.sigs.k8s.io/guides/)와 [CNI 규격](https://github.com/containernetworking/cni/blob/main/SPEC.md), [CoreDNS Manual](https://coredns.io/manual/toc/), [Kubernetes 서비스·네트워킹 문서](https://kubernetes.io/ko/docs/concepts/services-networking/)로 메웁니다. LLM 트래픽은 아직 책이 없어 [Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/guides/) 문서가 유일한 기준입니다.



## 호스트 · 1~3단계

> 노드 한 대 안에서 끝나는 구간입니다. Kubernetes 없이도 성립합니다.

### 1단계 · 연결

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| socket · `bind` · `listen` · `accept` · `connect` | 필수 | | TCP/IP Illustrated 12·13장 |
| 4-tuple · 듣는 소켓과 연결 소켓의 구분 | 필수 | | TCP/IP Illustrated 12장 |
| TCP 상태 · 3-way handshake · 연결 관리 | 필수 | [03-01](../02_os/book/cntd_computer-networking-top-down/03-01.%ED%8A%B8%EB%9E%9C%EC%8A%A4%ED%8F%AC%ED%8A%B8%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8A%94%EA%B0%80.md) · [03-04](../02_os/book/cntd_computer-networking-top-down/03-04.%ED%9D%90%EB%A6%84%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EC%97%B0%EA%B2%B0%20%EA%B4%80%EB%A6%AC%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%ED%98%BC%EC%9E%A1.md) | TCP/IP Illustrated 13장 |
| 신뢰성 · 순서 번호 · 재전송 · 타임아웃 · RTT | 필수 | [03-02](../02_os/book/cntd_computer-networking-top-down/03-02.%EC%8B%A0%EB%A2%B0%EC%84%B1%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%96%B4%EC%A7%80%EB%8A%94%EA%B0%80.md) · [03-03](../02_os/book/cntd_computer-networking-top-down/03-03.TCP%20%EB%8A%94%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%84%B8%EA%B3%A0%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EA%B8%B0%EB%8B%A4%EB%A6%AC%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 14장 |
| 흐름 제어 · 윈도 · cwnd · in-flight data | 필수 | [03-04](../02_os/book/cntd_computer-networking-top-down/03-04.%ED%9D%90%EB%A6%84%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EC%97%B0%EA%B2%B0%20%EA%B4%80%EB%A6%AC%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%ED%98%BC%EC%9E%A1.md) | TCP/IP Illustrated 15장 |
| 혼잡 제어 · CUBIC · BBR · Vegas | 필수 | [03-05](../02_os/book/cntd_computer-networking-top-down/03-05.%ED%98%BC%EC%9E%A1%EC%9D%84%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%8B%A4%EC%8A%A4%EB%A6%AC%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 16장 |
| DNS 질의 · 이름 해석 | 필수 | [02-03](../02_os/book/cntd_computer-networking-top-down/02-03.%EB%A9%94%EC%9D%BC%EA%B3%BC%20%EC%9D%B4%EB%A6%84%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%B0%BE%EC%95%84%EA%B0%80%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 11장 |
| HTTP/1.1 · HTTP/2 · 멀티플렉싱 | 필수 | [02-02](../02_os/book/cntd_computer-networking-top-down/02-02.%EC%9B%B9%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%EA%B0%80.md) · [01-02](../08_cloud/book/networking-and-kubernetes/01-02.HTTP%EC%97%90%EC%84%9C%20TCP%C2%B7TLS%C2%B7UDP%EA%B9%8C%EC%A7%80%20%E2%80%94%20Transport%20%EA%B3%84%EC%B8%B5%20%ED%95%B4%EB%B6%80.md) | HTTP/2 in Action 4·8장 |
| TLS 핸드셰이크 · SNI · ECH | 필수 | [04-01](../02_os/book/paw_packet-analysis-wireshark/04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) | HPBN 4장 · TCP/IP Illustrated 18장 |
| QUIC · HTTP/3 | 추천 | | HTTP/2 in Action 9장 |
| HTTP 성능 축 | 대체 | | High Performance Browser Networking 11·12장 |
| UDP · 단편화 | 추천 | [03-01](../02_os/book/cntd_computer-networking-top-down/03-01.%ED%8A%B8%EB%9E%9C%EC%8A%A4%ED%8F%AC%ED%8A%B8%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8A%94%EA%B0%80.md) | TCP/IP Illustrated 10장 |
| reverse proxy · half-close · 배압 | 추천 | | |
| listen 큐 · accept 큐 · ephemeral 포트 고갈 | 추천 | | |
| OS CA bundle · truststore | 선택 | | |
| TCP keepalive | 선택 | | TCP/IP Illustrated 17장 |

### 2단계 · Linux 경로

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| interface · MAC · ARP · NDP · neighbor | 필수 | [01-01](../02_os/networking/01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) | TCP/IP Illustrated 3·4장 |
| IP 주소 체계 · 서브네팅 · CIDR | 필수 | [01-04](../02_os/networking/01-04.%EC%84%9C%EB%B8%8C%EB%84%A4%ED%8C%85%EA%B3%BC%20CIDR%20%E2%80%94%20%EC%A3%BC%EC%86%8C%20%EA%B3%B5%EA%B0%84%EC%9D%84%20%EC%9E%90%EB%A5%B4%EB%8A%94%20%EB%B2%95.md) | TCP/IP Illustrated 2·5장 |
| 라우팅 테이블 · next hop · IP 포워딩 | 필수 | [01-03](../08_cloud/book/networking-and-kubernetes/01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) | TCP/IP Illustrated 5장 |
| network namespace · veth · bridge | 필수 | [01-01](../02_os/networking/01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) · [02-04](../08_cloud/book/networking-and-kubernetes/02-04.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) | Networking and Kubernetes 2장 |
| netfilter hook · iptables · nftables | 필수 | [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) · [02-01](../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 7장 |
| NAT · SNAT · DNAT · MASQUERADE | 필수 | [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 7장 |
| conntrack · 상태 테이블 포화 | 필수 | [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | Networking and Kubernetes 2장 |
| MTU · MSS · PMTUD | 필수 | [01-02](../02_os/networking/01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | TCP/IP Illustrated 10장 |
| ICMP · traceroute | 추천 | [05-04](../02_os/book/cntd_computer-networking-top-down/05-04.5%EC%9E%A5%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20traceroute%C2%B7ICMP%C2%B7%ED%9D%90%EB%A6%84%20%ED%91%9C%EB%A5%BC%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%A9%EB%8B%88%EB%8B%A4.md) | TCP/IP Illustrated 8장 |
| 컨테이너 네트워킹 모드 · 포트 매핑 | 추천 | [03-02](../08_cloud/book/networking-and-kubernetes/03-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%93%9C%EC%99%80%20CNI%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EA%B1%B0%EB%9E%98.md) · [03-03](../08_cloud/book/networking-and-kubernetes/03-03.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%2C%20%EB%8B%A4%EB%A5%B8%20%ED%98%B8%EC%8A%A4%ED%8A%B8.md) | Networking and Kubernetes 3장 |
| DHCP · 자동 구성 | 선택 | [05-01](../02_os/book/paw_packet-analysis-wireshark/05-01.%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%98%A4%EB%8A%94%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C.md) | TCP/IP Illustrated 6장 |
| NAT traversal | 선택 | | |
| bonding · LACP | 선택 | | |
| policy routing · `ip rule` · VRF | 선택 | | |

### 3단계 · 관측

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 캡처 위치 · 캡처 필터 · 디스플레이 필터 | 필수 | [02-01](../02_os/book/paw_packet-analysis-wireshark/02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) · [02-02](../02_os/book/paw_packet-analysis-wireshark/02-02.%EC%9E%A1%EC%9D%80%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9D%BD%EB%8A%94%20%EB%B2%95.md) | Packet Analysis 2장 |
| 무엇을 보려면 무엇을 치는가 — 도구와 단위 | 필수 | [진단 개념](../troubleshooting/_concepts/%EB%AC%B4%EC%97%87%EC%9D%84-%EB%B3%B4%EB%A0%A4%EB%A9%B4-%EB%AC%B4%EC%97%87%EC%9D%84-%EC%B9%98%EB%8A%94%EA%B0%80.md) | |
| 패킷이 사라지는 네 자리 — 드롭 카운터 | 필수 | [진단 개념](../troubleshooting/_concepts/%ED%8C%A8%ED%82%B7%EC%9D%B4-%EC%82%AC%EB%9D%BC%EC%A7%80%EB%8A%94-%EB%84%A4-%EC%9E%90%EB%A6%AC.md) | |
| TCP 이상 판독 · RST · 재전송 · 중복 ACK | 필수 | [03-01](../02_os/book/paw_packet-analysis-wireshark/03-01.TCP%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EC%83%9D%EC%95%A0.md) · [03-02](../02_os/book/paw_packet-analysis-wireshark/03-02.TCP%EA%B0%80%20%EC%96%B4%EA%B8%8B%EB%82%A0%20%EB%95%8C.md) | Packet Analysis 3장 |
| TLS 핸드셰이크 판독 · 실패 원인 | 필수 | [04-01](../02_os/book/paw_packet-analysis-wireshark/04-01.TLS%20%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%81%AC%20%EC%9D%BD%EA%B8%B0.md) · [04-02](../02_os/book/paw_packet-analysis-wireshark/04-02.%EC%97%B4%EC%87%A0%EC%99%80%20%EC%8B%A4%ED%8C%A8.md) | Packet Analysis 4장 |
| 계층 순서 진단 — `ss` · `ip` · `ethtool` · `conntrack -L` | 필수 | [02-03](../08_cloud/book/networking-and-kubernetes/02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) | Networking and Kubernetes 2장 |
| `resolv.conf` · search domain · `ndots` · NXDOMAIN | 필수 | [01-03](../02_os/networking/01-03.DNS%20%ED%95%84%ED%84%B0%EB%A7%81%20%EC%B0%A8%EB%8B%A8%20%E2%80%94%20NXDOMAIN%C2%B7DoH%C2%B7%EC%9A%B0%ED%9A%8C%20%EB%A7%88%EC%B0%B0.md) | |
| Corefile · 플러그인 체인 | 추천 | [03-01](../08_cloud/book/learning-coredns/03-01.Corefile%EC%9D%80%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) · [03-02](../08_cloud/book/learning-coredns/03-02.%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%20%EC%9D%BC%EA%B3%B1%EC%9D%B4%EB%A9%B4%20%EC%84%9C%EB%B2%84%20%ED%95%98%EB%82%98%EA%B0%80%20%EC%84%A0%EB%8B%A4.md) | Learning CoreDNS 3장 |
| 질문과 답의 불일치 | 추천 | [07-01](../08_cloud/book/learning-coredns/07-01.%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%EC%9D%B4%20%EC%96%B4%EA%B8%8B%EB%82%98%EB%A9%B4%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EB%B2%84%EB%A6%B0%EB%8B%A4.md) | Learning CoreDNS 7장 |
| 연결 지연 분포 · P99 · 측정 오차 | 선택 | | |
| GRO · GSO · TSO 오프로딩 | 선택 | | |
| `tc qdisc` · `netem` | 선택 | | |



## 클러스터 · 4~6단계

> 같은 커널 경로 위에 이름과 정책이 얹히고, 그 아래에 클라우드 underlay가 깔립니다.

### 4단계 · Kubernetes

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Pod IP · Pod CIDR · Node CIDR · pause container | 필수 | [04-01](../08_cloud/book/networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) | Networking and Kubernetes 4장 |
| CNI | 필수 | [04-02](../08_cloud/kubernetes/04_networking/04-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) · [04-02](../08_cloud/book/networking-and-kubernetes/04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) | Cilium 4장 |
| CNI 구현체 비교 — 무엇이 다른가 | 추천 | | Cilium 1~3장 |
| CNI 계약 — ADD · DEL · CHECK | 추천 | | Networking and Kubernetes 4장 |
| 오버레이 · VXLAN | 필수 | [04-03](../08_cloud/kubernetes/04_networking/04-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | Cilium 5장 |
| underlay 와 overlay 의 갈림 | 추천 | | Cloud Native Data Center Networking 6장 |
| Service · EndpointSlice · Service 5유형 | 필수 | [04-04](../08_cloud/kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md) · [05-02](../08_cloud/book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) | Networking and Kubernetes 5장 |
| kube-proxy — iptables · IPVS · eBPF | 필수 | [02-02](../08_cloud/book/networking-and-kubernetes/02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) | Networking and Kubernetes 2장 |
| readiness 와 endpoint 자격 · stale Endpoint | 필수 | | |
| 클러스터 DNS · Service FQDN | 필수 | [04-05](../08_cloud/kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md) · [06-01](../08_cloud/book/learning-coredns/06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) | Learning CoreDNS 6장 |
| service discovery · east-west traffic | 추천 | | |
| Ingress | 필수 | [04-06](../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) · [05-03](../08_cloud/book/networking-and-kubernetes/05-03.Ingress%EC%99%80%20Service%20Mesh%20%E2%80%94%20L7%EC%9D%98%20%EB%91%90%20%EC%B8%B5.md) | Networking and Kubernetes 5장 |
| Gateway API · HTTPRoute | 추천 | [04-06](../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) | Cilium 7장 |
| L4 로드밸런싱 — health check · round-robin · least connections · draining | 추천 | | |
| 인증서 만료와 TLS 실패 구분 | 추천 | | |
| `externalTrafficPolicy` · 소스 IP 보존 | 추천 | | |

### 5단계 · 클라우드 네트워크

> 클러스터가 서 있는 underlay입니다. 소장본이 한 장뿐이라 나머지는 각 클라우드 공식 문서로 메웁니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| VPC · 서브넷 · 라우트 테이블 · IGW · NAT GW | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| Security Group · NACL — stateful 과 stateless | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| 클라우드 로드밸런서 — L4 와 L7 | 필수 | [06-01](../08_cloud/book/networking-and-kubernetes/06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | Networking and Kubernetes 6장 |
| 3사 기본값의 갈림 | 추천 | [06-02](../08_cloud/book/networking-and-kubernetes/06-02.GCP%C2%B7Azure%EC%99%80%203%EC%82%AC%20%EB%B9%84%EA%B5%90%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%EB%AC%B8%EC%A0%9C%2C%20%EB%8B%A4%EB%A5%B8%20%EA%B8%B0%EB%B3%B8%EA%B0%92.md) | Networking and Kubernetes 6장 |
| VPN · 사이트 간 연결 · IPsec | 추천 | | |
| AWS Direct Connect · 전용선 | 추천 | | |
| Clos 토폴로지 · BGP · ECMP | 선택 | | Cloud Native Data Center Networking 2·14·15장 |
| VPC 피어링 · Transit Gateway | 선택 | | |

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
| eBPF host routing · bandwidth manager | 선택 | | |



## 운영 경계와 오버레이 · 7~9단계

> 클러스터가 한 종류가 아닐 때, 그리고 노드끼리 서로를 모르는 채로 만날 때 생기는 문제들입니다.

### 7단계 · 운영 경계

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| dual-stack · `ipFamilyPolicy` | 추천 | [04-08](../08_cloud/kubernetes/04_networking/04-08.IPv4%EC%99%80%20IPv6%20%EC%9D%B4%EC%A4%91%20%EC%8A%A4%ED%83%9D.md) | |
| topology-aware routing · EndpointSlice hint | 추천 | [04-09](../08_cloud/kubernetes/04_networking/04-09.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EC%9D%B8%EC%A7%80%20%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | |
| 서비스 메시가 인프라로 밀어낸 것 | 추천 | [01-01](../08_cloud/book/istio-in-action/01-01.%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%A9%94%EC%8B%9C%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%9D%B8%ED%94%84%EB%9D%BC%EB%A1%9C%20%EB%B0%80%EC%96%B4%EB%83%88%EB%8A%94%EA%B0%80.md) | Istio in Action 1장 |
| Envoy · Gateway · VirtualService | 추천 | [03-01](../08_cloud/book/istio-in-action/03-01.Envoy%EA%B0%80%20%EB%A7%A1%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20Istio%EA%B0%80%20%EB%B3%B4%ED%83%9C%EB%8A%94%20%EC%9D%BC.md) · [04-01](../08_cloud/book/istio-in-action/04-01.%EB%AC%B8%EC%9D%84%20%EC%97%AC%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EA%B8%B8%EC%9D%84%20%EB%82%B4%EB%8A%94%20%EC%9D%BC%EC%9D%84%20%EA%B0%80%EB%A5%B8%EB%8B%A4.md) | Istio in Action 3·4장 |
| mTLS · 기본값 닫아 가기 | 추천 | [05-01](../08_cloud/book/istio-in-action/05-01.%EC%9C%84%ED%97%98%EC%97%90%20%EB%85%B8%EC%B6%9C%EB%90%98%EB%8A%94%20%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%84%20%EC%A4%84%EC%97%AC%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) · [09-01](../08_cloud/book/istio-in-action/09-01.%EA%B1%B0%EC%9D%98%20%EC%95%88%EC%A0%84%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EA%B0%92%EC%9D%84%20%EB%8B%AB%EC%95%84%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) | Istio in Action 5·9장 |
| Windows HNS · HCS · Windows CNI | 선택 | [04-10](../08_cloud/kubernetes/04_networking/04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | |
| Zero Trust 전제 · 신뢰 관리 | 선택 | [12-01](../08_cloud/book/istio-in-action/12-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%EC%9A%B0%EB%8A%94%20%EC%A0%84%EC%A0%9C%20%EC%85%8B%EA%B3%BC%20%EB%82%A8%EB%8A%94%20%ED%95%9C%20%EC%9E%90%EB%A6%AC.md) | Zero Trust Networks 1·2·8장 |
| 멀티클러스터 메시 | 선택 | | Cilium 9장 |
| ambient mode · ztunnel · waypoint | 대체 | | Sidecar-less Istio Explained 1~3장 |

### 8단계 · 오버레이와 신뢰

> 기술 이름이 아니라 문제를 배우는 자리입니다. Tor · I2P · libp2p · WireGuard · Consul 은 같은 문제에 대한 서로 다른 답입니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| identity 와 trust 의 차이 · 인증과 인가의 차이 | 필수 | | Zero Trust Networks 2·6장 |
| traffic correlation · metadata · timing side-channel | 필수 | | Zero Trust Networks 8장 |
| 암호화가 숨기는 것과 숨기지 않는 것 | 필수 | | Real-World Cryptography 9·10장 |
| bootstrap · reseed · 최초 접점 · trust anchor | 추천 | | |
| peer discovery · DHT · Kademlia · gossip · membership | 추천 | | Patterns of Distributed Systems 7·8장 |
| signed descriptor · 공개키 신원 · 무결성 | 추천 | | Real-World Cryptography 7장 |
| key rotation · replay 방지 · freshness | 추천 | | Real-World Cryptography 5·8장 |
| Sybil · eclipse · poisoning · behavior score | 추천 | | Zero Trust Networks 10장 |
| 오버레이 — 물리와 논리의 분리 · 터널링 · 가상 토폴로지 | 추천 | | |
| relay · hole punching · reachability | 선택 | | |

**같은 질문이 이름만 바꿔 되풀이됩니다.** 아직 아무도 모르는 노드가 처음 네트워크에 어떻게 들어오는가는 Kubernetes node discovery, etcd cluster join, Kafka broker discovery, VPN mesh에서 같은 형태로 나옵니다. 그래서 이 단계를 마지막에 두되 특정 제품을 학습 대상으로 두지 않습니다.

### 9단계 · 터널과 경로

> 노드를 골랐다고 길이 나는 것은 아닙니다. 여기서는 실패가 곱으로 쌓이는 구조를 셈으로 다룹니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 피어 발견 성공과 터널 구성 성공은 다르다 | 필수 | | |
| 멀티홉 — 홉 수가 지연 · 성공률 · 프라이버시에 미치는 값 | 필수 | | |
| path selection · latency · 가용성 · 다양성 · 비용 함수 | 필수 | | |
| subnet · ASN · operator diversity · selection bias | 추천 | | |
| inbound 와 outbound — 단방향 터널을 조합한 양방향 통신 | 추천 | | |
| RX 와 TX 경로를 나누는 이유 | 추천 | | |
| 클라이언트가 경로를 정하고 서버는 목록만 준다 | 추천 | | |
| 종단 성공 확률 — 단계별 실패가 곱으로 쌓인다 | 필수 | | |
| 기하분포 — 최초 성공까지의 평균 시도 횟수 | 추천 | | |
| 재시도와 타임아웃 — 확률만큼 감지 시간도 값이다 | 필수 | | Patterns of Distributed Systems 7장 |
| 터널 풀 — 연결마다 새로 여는 방식과의 갈림 | 추천 | | |
| 예비 터널 — 준비 비용 · 전환 시간 · 자원 사용량 | 추천 | | |




## 손으로 확인하는 실습

> 노트 안에 실제로 있는 실습 절만 적습니다. 지어낸 출처를 채우지 않았습니다.

| 출처 | 단계 | 무엇 |
|---|:---:|---|
| [패킷 캡처 실습](../08_cloud/book/networking-and-kubernetes/01-04.%ED%8C%A8%ED%82%B7%20%EC%BA%A1%EC%B2%98%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%201%EC%9E%A5%20%EA%B0%9C%EB%85%90%EC%9D%84%20%EB%88%88%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0.md) | 1·3 | 계층 개념을 캡처로 확인 |
| [5장 실습](../02_os/book/cntd_computer-networking-top-down/05-04.5%EC%9E%A5%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20traceroute%C2%B7ICMP%C2%B7%ED%9D%90%EB%A6%84%20%ED%91%9C%EB%A5%BC%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%A9%EB%8B%88%EB%8B%A4.md) | 1·2 | traceroute · ICMP · 흐름 표 |
| [커널 네트워킹 실습](../08_cloud/book/networking-and-kubernetes/02-04.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) · [실습 2](../08_cloud/book/networking-and-kubernetes/02-05.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%202%20%E2%80%94%20%EB%A7%89%EA%B3%A0%2C%20%EC%A7%84%EB%8B%A8%ED%95%98%EA%B3%A0%2C%20%EB%82%98%EB%88%84%EA%B8%B0.md) | 2 | client · router · server namespace 를 veth 로 잇고 NAT·conntrack 확인 |
| [패킷을 잡는 법](../02_os/book/paw_packet-analysis-wireshark/02-01.%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%9E%A1%EB%8A%94%20%EB%B2%95.md) | 3 | 캡처 위치와 필터 |
| [컨테이너 네트워크 실습](../08_cloud/book/networking-and-kubernetes/03-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EB%A7%A8%EC%86%90%20%EB%B0%B0%EC%84%A0%EC%97%90%EC%84%9C%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%EA%B9%8C%EC%A7%80.md) | 2·4 | 맨손 배선에서 포트 매핑까지 |
| [Kubernetes 네트워크 실습](../08_cloud/book/networking-and-kubernetes/04-04.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20CNI%20%EB%B6%80%EC%9E%AC%EB%B6%80%ED%84%B0%20%EC%A0%95%EC%B1%85%C2%B7DNS%EA%B9%8C%EC%A7%80.md) | 4·6 | CNI 부재 · 정책 · DNS |
| [troubleshooting/os](../troubleshooting/os/README.md) · [cloud](../troubleshooting/cloud/README.md) · [mesh](../troubleshooting/mesh/README.md) | 1~4·7 | 증상에서 원인 역추적 다섯 편 |
| [troubleshooting/kubernetes](../troubleshooting/kubernetes/README.md) | 4·7 | 이름 해석 · 배포 중 502 · 정확히 1초 지연 |

5·7단계 자리는 비어 있습니다. 클라우드 축은 계정과 과금이 걸리고, 서비스 메시는 컨트롤 플레인이 서야 재현됩니다.

**노트 밖의 실습 경로가 둘 있습니다.** [LFS146 Introduction to Cilium](https://training.linuxfoundation.org/training/introduction-to-cilium-lfs146/)은 무료 26시간 과정으로 NetworkPolicy · Hubble · 투명 암호화 · kube-proxy replacement · Cluster Mesh 를 6·7단계 범위에서 손으로 밟게 합니다. [Isovalent Universe](https://labs.isovalent.com/)는 설치 없이 브라우저에서 도는 랩이라 클러스터를 세울 수 없을 때 씁니다.

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



## 로드맵에 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| Kubernetes 오브젝트의 배포와 운영 | [Kubernetes 로드맵](k8s-roadmap.md)이 맡습니다 |
| socket · epoll · io_uring 의 커널 구현 | [OS 로드맵](os-roadmap.md) 2·6단계가 맡습니다 |
| tail latency · coordinated omission · 프로파일 | [OS 로드맵](os-roadmap.md) 4단계의 성능 방법론 축입니다 |
| metrics · logs · traces · OpenTelemetry | `06_observability` 소관입니다 |
| Go 로 프록시·로드밸런서를 구현하는 일 | [Go 로드맵](go-roadmap.md) 6단계가 맡습니다. 여기는 개념까지입니다 |
| Computer Networking 6~8장 | 무선 · 물리 계층 · 암호 일반. 서버 운영과 접점이 적습니다 |
| Packet Analysis with Wireshark 6·7장 | 무선 캡처와 공격 분석. 판독 축이 아닙니다 |
| Learning CoreDNS 9장 | 플러그인을 *만드는* 쪽입니다. 필요가 생기면 3단계 뒤에 붙입니다 |



## 경계

> 이 문서가 정하는 것과 인접 문서에 넘기는 것입니다.

이 문서는 **개념의 순서와 우선순위**를 정합니다. 폴더 경계는 [02_os MOC](../02_os/README.md)와 [Kubernetes 네트워크 MOC](../08_cloud/kubernetes/04_networking/README.md)가 맡습니다.

맞닿는 문서가 셋입니다. socket과 파일 디스크립터의 커널 쪽은 [OS 로드맵](os-roadmap.md)이, 오브젝트 수준의 배포와 운영은 [Kubernetes 로드맵](k8s-roadmap.md)이, 프록시와 로드밸런서를 직접 구현하는 일은 [Go 로드맵](go-roadmap.md)이 맡습니다.

**OS 로드맵과는 network namespace에서 바통을 주고받습니다.** 그쪽 3단계가 namespace가 무엇을 가리는지까지 말하고 멈추면, 이쪽 2단계가 그 사이를 veth로 잇는 데서 시작합니다.
