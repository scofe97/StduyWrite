> 출처: NotebookLM · 2026-11-16 · Kubernetes Service 와 kube-proxy 커널 패킷 흐름 (영상 「How Kubernetes Services Really Work - iptables, kube-proxy, and Packet Flow Explained」 자막 분석) · 분야: k8s-keywords, network-keywords · 미검증

## 요점

한 줄: ClusterIP 는 어느 인터페이스에도 없는 가상 IP 입니다. kube-proxy 는 프록시 서버가 아니라 Netfilter 훅에 iptables 규칙을 심어 커널 안에서 목적지를 Pod IP 로 바꾸게 합니다.

- 가상 IP 의 문제: ClusterIP 는 `eth0`·`lo`·`cni0` 어디에도 붙지 않습니다. 가로채지 않으면 라우팅 조회에서 경로를 못 찾거나 기본 게이트웨이로 새어 나갑니다.
- 다섯 훅과 세 경로:
  - 노드로 들어옴: `PREROUTING` → 라우팅 → `INPUT`
  - 노드에서 나감: `OUTPUT` → 라우팅 → `POSTROUTING`
  - 노드를 지나감: `PREROUTING` → 라우팅 → `FORWARD` → `POSTROUTING`
- 두 군데에 거는 이유: 보통 Pod 의 패킷은 veth 로 들어오니 호스트 입장에서 `PREROUTING` 을 탑니다. 노드 프로세스와 `hostNetwork` Pod 의 패킷은 `OUTPUT` 에서 시작합니다. 그래서 kube-proxy 는 `KUBE-SERVICES` 점프를 두 체인에 모두 겁니다.
- 테이블 순서: 한 훅 안에서 `raw` → conntrack 분류 → `mangle` → `nat` → `filter` → `security` 순으로 돕니다. `nat` 은 연결의 첫(NEW) 패킷만 봅니다.
- NAT 시점: DNAT 는 라우팅 조회 전(`PREROUTING`·`OUTPUT`)에 목적지를 바꿉니다. SNAT·MASQUERADE 는 나갈 인터페이스가 정해진 뒤(`POSTROUTING`)에 출발지를 바꿉니다.
- conntrack 역변환: 첫 패킷의 원래 튜플과 응답 튜플을 기록해 두고, 응답이 오면 역방향 규칙 없이 출발지를 ClusterIP 로 되돌립니다.
- 세 층 체인:
  - `KUBE-SERVICES`: 모든 Service 의 ClusterIP·포트를 매칭하는 입구입니다.
  - `KUBE-SVC-*`: `statistic --mode random --probability` 로 백엔드를 고릅니다. i번째 규칙 확률은 1/(N−i+1) 이라 세 개면 1/3 → 1/2 → 1 입니다.
  - `KUBE-SEP-*`: 고른 Pod 로 DNAT 합니다. 자기 Service 로 돌아오는 헤어핀에 대비해 `KUBE-MARK-MASQ` 표시를 겁니다.
- 브리지 함정: 리눅스 브리지는 L2 로 스위칭해 iptables 를 거치지 않습니다. `br_netfilter` 모듈과 `net.bridge.bridge-nf-call-iptables=1` 이 있어야 Pod 트래픽이 훅을 탑니다. 브리지를 쓰지 않는 CNI 는 여기에 기대지 않습니다.
- 디버깅 요령: `nat` 은 후속 패킷을 건너뛰니 LOG 규칙은 모든 패킷이 지나는 `mangle` 에 걸라고 리포트가 권합니다.
- 규모 한계와 대안:
  - iptables 는 규칙을 위에서부터 순서대로 대조해 비용이 O(N) 이라는 것이 리포트의 설명입니다. Service 가 수천 개면 CPU 와 지연이 늘어납니다.
  - 대안은 IPVS(해시 조회·스케줄러 선택), nftables(셋·맵, 증분 갱신), Cilium eBPF(소켓·TC 단계에서 변환)입니다.
- conntrack 포화: `nf_conntrack_max` 를 넘으면 새 패킷이 조용히 버려집니다. CoreDNS 의 UDP 질의가 많을 때 잘 생기고, 한도 상향과 NodeLocal DNSCache 로 막습니다.
- 진단 순서: `ip_forward`·`bridge-nf-call-iptables` 를 봅니다. 그다음 `KUBE-SERVICES`·`SVC`·`SEP` 규칙과 카운터, `FORWARD` 드롭 카운터, `nf_conntrack_count`/`max` 순으로 봅니다.
- L4 와 L7 의 경계: kube-proxy 는 IP·포트로만 나눕니다. HTTP 경로·헤더 라우팅, 재시도, mTLS 는 Ingress·Gateway API·Service Mesh 몫입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| ClusterIP 가상 IP | 어느 인터페이스에도 붙지 않아 커널 규칙이 목적지를 바꿔야 닿는 Service 주소 | [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) |
| Netfilter 다섯 훅 | 라우팅 판단을 사이에 두고 패킷이 지나는 다섯 검사 자리 | [커널이 패킷을 판정하는 층](../../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md) |
| PREROUTING·OUTPUT 두 진입점 | Pod 발신은 PREROUTING, 노드 발신은 OUTPUT 에서 DNAT 되는 차이 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| iptables 테이블 순서 | 한 훅 안에서 raw·mangle·nat·filter·security 가 우선순위대로 도는 순서 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| DNAT·SNAT·MASQUERADE 시점 | 목적지는 라우팅 전, 출발지는 나갈 인터페이스가 정해진 뒤에 바꾸는 규칙 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| conntrack 자동 역변환 | 첫 패킷의 NAT 매핑을 기억해 응답의 주소를 되돌리는 연결 추적 | [커널이 패킷을 판정하는 층](../../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md) |
| KUBE-SERVICES·SVC·SEP 체인 | Service 매칭 → 백엔드 고르기 → DNAT 로 한 겹씩 점프하는 세 층 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| statistic 확률 사다리 | i번째 규칙이 1/(N−i+1) 로 걸려 전체가 균등해지는 분배 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| KUBE-MARK-MASQ·헤어핀 | 표시를 단 패킷만 POSTROUTING 에서 MASQUERADE 해 응답이 같은 길로 오게 하는 장치 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| br_netfilter | 브리지를 지나는 L2 트래픽도 iptables 훅을 타게 하는 모듈과 sysctl | [커널이 패킷을 판정하는 층](../../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md) |
| LOG 로 훅 통과 추적 | nat 은 첫 패킷만 보니 모든 패킷이 지나는 mangle 에 LOG 를 거는 방법 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) (일부: LOG 타깃과 nat PREROUTING 매칭 확인, mangle 다섯 체인으로 훅 순서를 찍는 실험 없음) |
| iptables 조회·갱신 비용 | 규칙을 선형으로 대조하고 룰셋을 다시 써서 Service 수천 개에서 느려지는 문제 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| IPVS 모드 | 해시로 백엔드를 찾고 스케줄러를 고를 수 있는 커널 L4 로드밸런서 | [iptables·IPVS·eBPF](../../08_cloud/book/networking-and-kubernetes/02-03.iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술.md) |
| nftables 모드 | iptables 모드의 후계로 권장되는 kube-proxy 모드 | [CNI와 kube-proxy](../../08_cloud/book/networking-and-kubernetes/04-02.CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서.md) (일부: 버전 이력·기본값 전환·커널 요구, 셋·맵 자료구조와 증분 갱신 내부 없음) |
| Cilium kube-proxy 대체 | `connect()` 시점에 소켓 단계에서 백엔드를 골라 netfilter 를 건너뛰는 eBPF | [Cilium kube-proxy 대체](../../08_cloud/book/cilium-up-and-running/06-01.Cilium 은 kube-proxy 를 eBPF 로 대신하고 외부 서비스에 IP 와 경로를 붙인다.md) |
| conntrack 포화·NodeLocal DNSCache | 한도를 넘으면 새 패킷이 버려지고, DNS 질의의 추적 항목을 노드 캐시로 없애 막는 구성 | [커널이 패킷을 판정하는 층](../../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md), [NetworkPolicy와 DNS](../../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름.md) |
| externalTrafficPolicy | 외부 트래픽을 받은 노드의 Pod 로만 보낼지 정해 소스 IP 보존과 홉 수를 맞바꾸는 설정 | [Service 5유형](../../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) |



## 자료와 실습

- 자료:
  - [Virtual IPs and Service Proxies (Kubernetes 문서)](https://kubernetes.io/docs/reference/networking/virtual-ips/): iptables·IPVS·nftables 모드의 동작과 트래픽 정책 명세입니다. 정독 노트는 [CNI와 kube-proxy](../../08_cloud/book/networking-and-kubernetes/04-02.CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서.md) 입니다.
  - [netfilter 문서](https://www.netfilter.org/documentation/): 다섯 훅과 테이블 통과 순서의 1차 자료입니다.
  - [Kubernetes Without kube-proxy (Cilium 문서)](https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/): 소켓 단계 부하 분산으로 iptables·conntrack 을 대신하는 구성입니다.
  - [A Deep Dive into Iptables and Netfilter Architecture](https://www.digitalocean.com/community/tutorials/a-deep-dive-into-iptables-and-netfilter-architecture): 훅과 테이블 순회 순서를 표로 정리한 튜토리얼입니다.
  - [Cracking Kubernetes Node Proxy (aka kube-proxy)](https://arthurchiao.art/blog/cracking-k8s-node-proxy/): kube-proxy 가 만드는 `KUBE-SVC`·`KUBE-SEP` 같은 체인을 실제 규칙 덤프로 해부한 블로그 글입니다.
  - 『Networking and Kubernetes』: 리포트는 2장(Linux 네트워킹)·3장(컨테이너 네트워킹)·5장(Service 와 kube-proxy)을 권합니다. [정독 노트](../../08_cloud/book/networking-and-kubernetes/README.md) 에서는 02-0x·03-0x 편과, kube-proxy 를 다룬 04-02·Service 를 다룬 05-02 입니다.
  - 『Systems Performance』 2판 10장(네트워크)·11장(클라우드와 컨테이너): 규칙 수가 늘 때 커널 CPU 와 지연을 계측하는 방법입니다. 10장 정독 노트는 [네트워크 — 아키텍처](../../02_os/book/systems-performance/10-02.네트워크 — 아키텍처.md) 입니다. 11장은 [OS 가상화](../../02_os/book/systems-performance/11-03.클라우드 컴퓨팅 — OS 가상화.md) 입니다.
  - 『Learning eBPF』 1~3장·8장: eBPF 기초와 XDP·TC 훅, iptables 대신 eBPF 맵을 쓰는 네트워킹입니다. 8장 정독 노트는 [XDP 와 TC](../../02_os/book/learning-ebpf/08-01.XDP 와 TC 는 패킷을 경계 검사로 파싱해 반환 코드로 버리고 고쳐 되돌린다.md) 입니다. 이어지는 편은 [쿠버네티스 네트워킹](../../02_os/book/learning-ebpf/08-02.uprobe 는 암호화 전후의 평문을 읽고 쿠버네티스 네트워킹은 iptables 대신 eBPF 맵으로 정책을 건다.md) 입니다.
  - 코드: kubernetes `pkg/proxy/iptables/proxier.go` 의 `syncProxyRules`(SVC·SEP 체인과 확률 규칙 생성)를 봅니다. cilium `bpf/bpf_sock.c`·`bpf/lib/lb.h`(소켓 `connect()` 때 백엔드 변환)와 bcc `tools/tcpconnect.py`·`tcplife.py`(연결 관측)도 봅니다.
- 실습:
  - Level 1: VM 한 대에서 `mangle` 다섯 체인에 접두사가 다른 `-j LOG` 를 걸고 `python3 -m http.server` 로 로컬 요청과 인터페이스 경유 요청을 비교합니다. 함정은 `nat` 에 LOG 를 걸어 첫 패킷만 찍히는 것과, 루프백 요청이 `lo` 로 다시 들어와 `PREROUTING`·`INPUT` 이 한 번 더 찍히는 것입니다. 완료: `dmesg -T | grep NF-` 로 `INPUT` 과 `FORWARD` 로 갈리는 이유를 설명하고, `iptables -t mangle -F` 로 원복합니다.
  - Level 2: kube-proxy 없이 `ip netns` 백엔드 둘과 `MY-SERVICES`·`MY-SVC-WEB`·`MY-SEP-1/2` 체인을 만듭니다. 가상 IP `10.99.99.99:80` 을 50:50 DNAT 하고 `POSTROUTING` 에 MASQUERADE 를 겁니다. 함정은 `ip_forward` 가 꺼져 있거나 Docker 의 `FORWARD` 기본 정책 DROP 에 막히는 것입니다. 완료: `curl` 20회가 두 백엔드에 약 1:1 로 가고, `conntrack -L` 매핑과 `iptables -t nat -L -n -v` 카운터가 규칙별로 늘어납니다.
  - Level 3: kind 에 더미 Service·EndpointSlice 를 100 → 1,000 → 3,000개로 늘리며 iptables 모드와 IPVS 또는 Cilium `kubeProxyReplacement=true` 를 비교합니다. 함정은 실제 Pod 수천 개를 띄워 메모리·PID 가 바닥나는 것으로, 규칙 수만 부풀려야 합니다. 완료: 새 연결 지연 P50·P99, `kubeproxy_sync_proxy_rules_duration_seconds`, 노드 CPU 를 모드별 표로 만들고 전환 임계점을 적습니다.



## 경고

- ⚠ 갱신 비용: 리포트는 규칙 하나만 고쳐도 전체 룰셋을 다시 적재한다고 적었습니다. 정독 노트는 v1.28 부터 iptables 모드가 바뀐 Service·EndpointSlice 자리만 고친다고 적어, 이 서술은 옛 동작입니다.
- ⚠ 모드 현황: 리포트는 nftables 를 "1.29 도입, 1.31 베타" 까지만 적었습니다. 정독 노트 기준으로 nftables 는 1.33 에서 GA 가 됐습니다. IPVS 는 1.35 에서 deprecated 돼 대안으로 권하는 자리가 바뀌었습니다.
- ⚠ 복잡도 표기: IPVS·nftables·eBPF 의 O(1) 조회와 Cilium 의 `sock_ops` 단계 변환은 리포트가 보탠 설명입니다. 영상 자막과 1차 자료로 대조하지 않았습니다.
- ⚠ mangle LOG 권고: 모든 패킷을 보려면 `mangle` 에 LOG 를 걸라는 것은 리포트의 실무 팁입니다. 커널 문서로 확인하지 않았습니다.
- ⚠ 책 장 번호: 리포트는 『Networking and Kubernetes』 5장을 Service 와 kube-proxy 장으로 적었습니다. 정독 노트에서는 kube-proxy 가 04-02, Service 가 05-02 로 나뉩니다. 『Systems Performance』·『Learning eBPF』 장 범위는 목차로 대조하지 않았습니다.
- ⚠ 자막 교정: 영어 자동 자막의 오인식(`cube proxy`, `DNET`, `contract` 등)을 리포트가 고쳤습니다.
