---
title: Kubernetes 네트워크 학습 로드맵
tags: [roadmap, kubernetes, networking, ebpf, cilium, service-mesh, dns, security]
status: final
related:
  - README.md
  - 02_os/networking/roadmap.md
  - 08_cloud/kubernetes/04_networking/README.md
updated: 2026-09-05
---

# Kubernetes 네트워크 학습 로드맵
---

## 이 순서를 잡은 기준

> Kubernetes 네트워크는 선언 API 한 층으로 끝나지 않습니다. Service 를 만들면 커널의 어느 훅이 켜지고 패킷이 어디로 도는지까지 봐야 요소를 다 봤다고 할 수 있고, 그 층들이 아래에서 위로 쌓이기 때문에 읽는 순서가 있습니다.

![척추에 국면 여섯을 걸고 책을 노드로, 배우는 개념을 좌우로 뻗은 학습 로드맵](_assets/network-roadmap.svg)

순서를 잡은 규칙은 하나입니다. **뒤 단계가 앞 단계의 어휘로 설명되도록 놓았습니다.** Cilium 이 "kube-proxy 를 대체한다"고 말할 때 그 문장이 뜻을 가지려면 Service 가 무엇을 선언하는지, iptables 가 무엇을 하고 있었는지, eBPF 훅이 패킷 여정의 어디에 붙는지를 이미 알아야 합니다. 그래서 클러스터 모델이 데이터패스 앞에 오고, 패킷을 눈으로 보는 능력이 그 앞에 옵니다.

도식은 **무엇을 어떤 순서로 읽고 거기서 무엇을 배우는가** 하나만 말합니다. 척추에 국면 여섯을 걸고 책을 노드로, 그 책에서 배우는 개념을 좌우로 뻗었습니다.

**국면 사이에는 순서가 있고, 국면 안의 책은 화살표가 없으면 순서가 없습니다.**

실제로 강제되는 선행은 둘뿐입니다. eBPF 를 모르면 Cilium 데이터패스 장이 안 읽히고, 사이드카 메시를 모르면 앰비언트가 무엇을 줄인 것인지 알 수 없습니다. 나머지는 병렬이라 형편에 맞게 고릅니다.

배지는 넷입니다. **필수**는 빼면 뒤가 막히는 것, **추천**은 빼도 되지만 손해가 큰 것, **선택**은 목표가 생겼을 때만 여는 것입니다.

단계마다 표를 둘 둡니다. 하나는 책이 다루는 개념이고 다른 하나는 **책 밖 키워드**입니다. 읽는 축과 별개로 손으로 확인하는 축이 하나 더 있는데, 그것은 아래 실습 절이 맡습니다. 책은 찍힌 시점에 멈춰 있고 Kubernetes 네트워크는 그 뒤로도 움직이므로, 책 밖 키워드의 기본값과 승격 단계는 공식 문서에서 다시 확인하고 표는 무엇을 검색할지 정하는 용도로만 씁니다.

바닥부터 운영과 신뢰까지가 필수 구간으로 82장이고, 조건부 셋은 21장입니다. 책은 모두 Google Drive 의 `내 드라이브/book/` 아래에 있습니다.



## 낡음 점검

> 책은 찍힌 시점에 멈춥니다. 출간 연도를 OpenLibrary 와 출판사 페이지에서 2026-09-05 에 확인하고, 낡은 것은 단계에서 뺐습니다.

기준은 주제가 바뀌는 속도입니다. Kubernetes API·CNI·메시·클라이언트 라이브러리처럼 **빨리 바뀌는 축은 5년**을 넘기면 단계에서 빼고 공식 문서로 대신합니다. TCP/IP 프로토콜이나 암호 원리처럼 느리게 바뀌는 축은 오래돼도 남기되 무엇이 낡았는지를 적습니다.

| 책 | 출간 | 조치 |
|---|:---:|---|
| Learn Go with Pocket-Sized Projects · Container Security 2판 | 2025 | 그대로 |
| Kubernetes in Action 2nd · Learning eBPF · CKS Study Guide · Kubernetes Best Practices 2nd | 2023 | 그대로 |
| Istio in Action · Learning Modern Linux | 2022 | 그대로 |
| Networking and Kubernetes · Production Kubernetes | 2021 | 경계선. 그대로 두되 공식 문서와 대조 |
| Network Programming with Go | 2020 | 유지. 라우팅 패턴과 `log/slog` 는 책 밖 키워드로 |
| Learning CoreDNS | 2019 | 유지. 쿠버네티스 연동 장은 공식 DNS 스펙과 대조 |
| HTTP:2 in Action | 2019 | 프레이밍과 HPACK 만 씀. HTTP/3 은 RFC 로 |
| **Programming Kubernetes** | **2019** | **뺌.** client-go 가 그 뒤로 많이 바뀌어 공식 문서와 sample-controller 로 대신 |
| **High Performance Browser Networking** | **2013** | **뺌.** HTTP/2 가 초안이던 시점이라 QUIC·HTTP/3 이 아예 없음 |
| **Computer Networking Top-Down 9판** | **2026** | 참조서 1순위. TCP:IP Illustrated 를 대체 |
| Cloud Native Data Center Networking | 2019 | 언더레이 국면 신설. 7장 Container Networking 만 제외 |
| ~~TCP:IP Illustrated 2판~~ | 2011 | **뺌.** 같은 자리를 15년 새 책이 덮고 QUIC·HTTP/3·SDN 이 없다 |

**Kurose 는 참조서가 아니라 절반이 단계입니다.** 처음에 717쪽이라는 이유로 통째로 참조서에 넣었는데 장마다 성격이 다릅니다. 3·4·5장은 로드맵의 나머지가 전제하는 바닥이라 바닥 국면에서 읽고, 2·6·8장만 참조서로 둡니다. 1·7장은 읽지 않습니다.

**TCP:IP Illustrated 를 Kurose 9판으로 갈았습니다.** 2011년 책을 "프로토콜은 느린 축"이라는 예외로 남겨 뒀는데, 같은 자리를 덮는 2026년 책이 들어오면서 예외를 유지할 이유가 사라졌습니다. Kurose 9판은 QUIC 을 106회, HTTP/3 을 6회 언급하고 5장이 통째로 컨트롤 플레인과 SDN 입니다. 둘 다 2011년 책에는 없습니다. 패킷 필드 단위의 깊이가 필요한 드문 경우에만 옛 책을 엽니다.

**Container Security 는 2판을 권합니다.** Drive 에 있는 것은 2020년 1판인데 2025년에 2판이 나왔습니다. Container Security 가 쓰는 10·11장은 컨테이너 네트워크 보안과 TLS 라 그사이 바뀐 것이 적지 않습니다.

조건부 두 자리는 책을 빼면서 자리를 공식 자료로 채웠습니다. QUIC 은 [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt), HTTP/2 는 [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.txt), HTTP/3 은 [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) 가 정본이고, 컨트롤러 작성은 Kubernetes 의 `sample-controller` 저장소가 현행 코드입니다.



## 손으로 확인하는 실습

> 읽기만 하면 남의 말을 옮기게 됩니다. 다만 이건 책과 다른 축이라 도식에서는 뺐고, 아래 표가 맡습니다.

기준은 **그 자리를 손으로 확인할 검증된 자료가 있는가** 하나입니다. 스물한 개 중 책만으로 되는 것은 하나도 없습니다. 외부 저장소를 클론하거나 클러스터를 띄워야 하므로 책 개념과 같은 무게로 도식에 그리면 논점이 흐려집니다. 출처는 셋입니다. 실습 저장소의 편 번호, 책이 딸린 예제 저장소, 공식 핸즈온 문서입니다. 비어 있는 단계는 실습이 필요 없어서가 아니라 제가 확인한 자료를 못 찾아서이고, 지어낸 출처를 채우지 않았습니다.

| 출처 | 어느 자리 | 무엇 |
|---|---|---|
| [network-fundamentals-lab](https://github.com/gnu-gnu/network-fundamentals-lab) | 0~4 · 6 · 10 | 17편 트러블슈팅 실습과 자가 진단 두 편 |
| [Kurose 공식 Wireshark 랩](http://gaia.cs.umass.edu/kurose_ross/wireshark.php) | Wireshark | HTTP·DNS·TCP·UDP·IP·ICMP·Ethernet·ARP·TLS 랩. 참조서가 실습까지 준다 |
| [luksa/kubernetes-in-action-2nd-edition](https://github.com/luksa/kubernetes-in-action-2nd-edition) | 3 | Service·Ingress·Gateway API 매니페스트 |
| [lizrice/learning-ebpf](https://github.com/lizrice/learning-ebpf) | 5 | 장별 eBPF 프로그램과 빌드 환경 |
| [Cilium 시작하기](https://docs.cilium.io/en/stable/gettingstarted/) | 6 | kind 위에 Cilium 을 올리고 정책을 걸기 |
| [OPA Playground](https://play.openpolicyagent.org/) · [Kyverno 정책 모음](https://kyverno.io/policies/) | 7 | Rego 를 브라우저에서 돌리고, 검증된 정책을 읽기 |
| [istioinaction/book-source-code](https://github.com/istioinaction/book-source-code) | 8 | 책의 샘플 서비스와 Istio 설정 |
| [Istio Ambient 시작하기](https://istio.io/latest/docs/ambient/getting-started/) | 9 | ztunnel 과 waypoint 를 실제로 띄우기 |
| [CoreDNS kubernetes 플러그인](https://coredns.io/plugins/kubernetes/) | 4 | Corefile 을 고쳐 보며 레코드 모양 확인 |
| [kubernetes/sample-controller](https://github.com/kubernetes/sample-controller) · `~/study/podwire` | 15 | 컨트롤러 현행 코드, 그리고 직접 짓는 CNI |

Container Security·Zero Trust·HTTP/2·클라우드 자리는 비어 있습니다. 컨테이너 네트워크 보안, 제로 트러스트, HTTP/3, 클라우드 네트워킹은 클러스터나 계정이 있어야 손으로 확인되는데, 그 조건을 로드맵이 정할 수 없어 자리를 비웠습니다.

한국어로 쓰인 containerlab 기반 트러블슈팅 시리즈입니다. 17편과 자가 진단 두 편으로 이뤄져 있고, 편마다 **개념·고장·관찰·교훈** 네 칸이 같은 자리에 반복됩니다. 각 디렉토리에 토폴로지(`.clab.yml`), 지시문(`README.md`), 실행 기록이 붙은 모범 답안(`WALKTHROUGH.md`), 복구 스크립트(`fix.sh`)가 들어 있습니다.

이 로드맵과 짝이 맞는 이유는 순서가 아니라 **방식**입니다. Wireshark 에서 캡처로 확인하는 능력을 만들라고 한 것과 같은 목적을 실습으로 강제합니다. 고장을 미리 심어 두고 증상만 주기 때문에, 원인을 좁히는 순서를 손으로 익히게 됩니다.

| 실습 | 어느 자리에 붙나 |
|---|---|
| 00 온램프 | 바닥 국면 앞. CIDR 표기와 `ip`·`ping`·`tcpdump` 첫걸음 |
| 01 L2 인접성과 ARP · 02 브로드캐스트 도메인과 L2 루프 | Wireshark. 캡처로 ARP 와 MAC 학습을 보기 |
| 04 L3 라우팅 · 05 LPM 과 블랙홀 · 06 TTL 과 라우팅 루프 | Wireshark. 라우팅 테이블이 전부라는 감각 |
| 08 TCP 3-way 실패 유형 | Wireshark. 타임아웃·refused·RST 의 지문 차이 |
| 09 conntrack 과 idle timeout · 12 MTU·MSS·PMTUD | Wireshark 의 책 밖 키워드가 그대로 실습이 된 편 |
| 14 DNS 기본 · 15 ICMP 차단의 대가 | Wireshark · CoreDNS. TTL 이 곧 페일오버 시간인 이유 |
| 03 VLAN·트렁크 · 07 VXLAN 기초 | N&K · 언더레이. 오버레이와 CNI 가 딛는 캡슐화 |
| 10 NAT 기본 · 11 대칭성과 소스 재작성 · 16 NAT 헤어핀 | N&K · KIA. Service 와 Ingress 뒤의 주소 변환 |
| 13 터널·오버레이 MTU | Cilium. 오버레이의 50바이트 세금 |
| 17 동적 라우팅 OSPF·BGP | Production K8s · 언더레이. BGP 와 짝 |
| CP-1 · CP-2 자가 진단 | Wireshark 를 끝낸 뒤. README 없이 증상만으로 원인 좁히기 |

실습 저장소는 `~/study/network-fundamentals-lab` 에 클론해 두었습니다. 랩 디렉토리와 `clab.sh` 가 저장소 루트에 바로 있습니다.

**환경은 미리 확인하고 시작합니다.** containerlab 을 깔지 않아도 Docker 만 있으면 저장소가 주는 `clab.sh` 래퍼로 macOS 에서 돌아갑니다. 다만 17편의 FRR 은 x86 네이티브를 전제로 하고 arm64 에서는 에뮬레이션이 필요하다고 저장소가 적어 두었으니, Apple Silicon 에서는 그 편만 따로 판단합니다. 관리망이 이미 쓰는 Docker 네트워크와 겹치면 배포가 실패하므로 각 토폴로지의 `mgmt.ipv4-subnet` 을 먼저 봅니다.



## 바닥 · 순서 없음

> 프로토콜 모델을 잡고 캡처로 확인하는 국면입니다. 4장의 match + action 이 뒤에서 만날 iptables 와 eBPF 가 공유하는 추상입니다.

### Learning Modern Linux 7장  `선택`

Kubernetes 네트워크 문서는 "Pod 마다 네트워크 네임스페이스가 있다"는 문장에서 출발하는데, 그 네임스페이스가 무엇을 격리하는지 모르면 문장이 통과만 하고 남지 않습니다. 30분짜리 복습이고, 이미 아는 내용이면 건너뛰어도 됩니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 네트워크 네임스페이스 | Pod 마다 따로 갖는 격리 단위. 무엇이 격리되고 무엇이 공유되는가 |
| 인터페이스와 라우팅 테이블 | 네임스페이스 안에서 패킷이 어느 인터페이스로 나가는지 정하는 규칙 |
| `ip`·`ss` 진단 도구 | 위 둘을 눈으로 확인하는 명령 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| `ip netns` 실습 | 네임스페이스를 손으로 만들어 넣고 빼 보기 |
| veth pair 와 브리지 | Pod 네트워크가 조립되는 방식을 맨손으로 재현 |
| `nsenter` | 다른 네임스페이스 안으로 들어가 진단하기 |

### Computer Networking: A Top-Down Approach 3·4·5장  `추천`

로드맵의 나머지가 전제하지만 아무도 가르치지 않던 자리입니다. 717쪽 전권이 아니라 세 장, 약 220쪽만 봅니다.

**4장이 이 로드맵에서 가장 값이 큽니다.** `generalized forwarding` 이 22회, `match-plus-action` 이 24회, `OpenFlow` 가 49회 나오는데, **match + action** 이 바로 iptables 규칙과 eBPF 데이터패스가 하는 일의 추상입니다. 이 모델을 먼저 잡으면 뒤에서 만날 Cilium 의 eBPF 맵 조회가 새로운 것이 아니라 같은 모델의 다른 구현으로 읽힙니다.

5장은 통째로 컨트롤 플레인이고 `SDN` 이 39회 나옵니다. 데이터 플레인과 컨트롤 플레인을 가르는 발상이 Kubernetes 네트워크의 뼈대인데, 이 로드맵에서 그걸 정면으로 다루는 유일한 책입니다.

3장은 `congestion control` 이 128회입니다. 책 밖 키워드에 MTU·PMTUD 와 conntrack 을 적어 뒀는데 TCP 를 이 깊이로 다루는 자료가 없었습니다.

**1장과 7장은 읽지 않습니다.** 1장 개론은 Networking and Kubernetes 가 덮고, 7장은 `802.11`·`cellular` 이 249회 나오는 무선 전용이라 이 로드맵과 겹치지 않습니다. 2·6·8장은 참조서로 돌립니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| TCP 혼잡제어와 재전송 | 느린 원인이 앱인지 네트워크인지 가르는 바닥 |
| QUIC 이 UDP 위에 선 이유 | 전송 계층을 왜 바꿨는가 |
| match + action 포워딩 | iptables 와 eBPF 데이터패스가 공유하는 추상 |
| 데이터 플레인과 컨트롤 플레인 | 무엇이 패킷을 나르고 무엇이 규칙을 정하는가 |
| 라우팅 알고리즘과 SDN | 경로가 정해지는 방식과 그것을 중앙화한 발상 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| [공식 Wireshark 랩](http://gaia.cs.umass.edu/kurose_ross/wireshark.php) | 같은 저자가 주는 실습. 읽은 것을 바로 캡처로 확인 |
| P4 와 프로그래머블 데이터플레인 | 책은 두 번만 언급한다. match + action 의 다음 세대 |

### Packet Analysis with Wireshark 1~5장  `추천`

이 단계의 목적은 지식이 아니라 **반증 능력**입니다. 뒤에서 만날 "Cilium 은 iptables 를 건너뛴다", "mTLS 가 걸려 있다" 같은 주장을 캡처로 확인할 수 있어야 남의 설명을 그대로 옮기지 않게 됩니다.

이 책은 장별 PDF 가 아니라 절 단위로 쪼개져 있습니다. `1. Packet Analyzers` 같은 파일이 장 표지고, `3TCP connection establishment` 처럼 앞 숫자가 장 번호인 파일들이 본문이라 1~5장이 33개 파일입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 캡처와 필터 문법 | 원하는 패킷만 남기는 법. 이후 모든 확인의 전제 |
| TCP 수립·종료 시퀀스 | 3-way 와 종료 절차를 시퀀스 번호로 읽기 |
| 재전송과 지연 분석 | 느린 원인이 앱인지 네트워크인지 가르는 근거 |
| TLS 핸드셰이크와 복호화 | 키 교환 절차, 그리고 캡처를 복호화해 안을 보는 방법 |
| DHCP·DNS·HTTP 해부 | 클러스터에서 가장 자주 깨지는 세 프로토콜 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| `kubectl debug` 임시 컨테이너 | 이미지에 도구가 없는 Pod 에서 캡처를 뜨는 법 |
| MTU 와 PMTUD 블랙홀 | 오버레이에서 큰 패킷만 사라지는 전형적 장애 (실습 12편) |
| conntrack 테이블 포화 | 연결이 갑자기 끊기는 원인 중 가장 흔한 하나 (실습 09편) |
| `pwru` | 커널 안에서 패킷이 어디서 버려졌는지 추적 |



## 클러스터 모델 · 약한 순서

> 커널로 내려가기 전에 Kubernetes 가 무엇을 선언하는지 먼저 세웁니다. 이 어휘가 없으면 데이터패스를 읽어도 무엇을 구현한 것인지 모릅니다.

### Networking and Kubernetes 3~5장  `필수`

컨테이너 하나가 네트워크를 갖는 방식에서 시작해 Pod 네트워크 모델과 Service 추상화까지 한 번에 올라갑니다. "모든 Pod 는 NAT 없이 서로 통신한다"는 모델의 요구사항이 왜 CNI 라는 별도 규약을 낳았는지가 이 구간의 논지입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 컨테이너 네트워킹 모드 | bridge·host·none 이 각각 무엇을 포기하고 무엇을 얻는가 |
| Pod 네트워크 모델 | NAT 없는 평평한 주소 공간이라는 요구사항과 그 결과 |
| CNI 의 자리 | 그 요구사항을 누가 어떻게 만족시키는가 |
| Service 다섯 유형 | ClusterIP·NodePort·LoadBalancer·ExternalName·Headless |
| EndpointSlice | Service 뒤의 실제 Pod 목록이 관리되는 단위 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| CNI 스펙과 플러그인 체이닝 | Cilium 도 그 규약 위에 있다 |
| VXLAN 캡슐화 | 라우터 너머에 같은 L2 를 만드는 원리 (실습 07편) |
| Multus 와 SR-IOV | Pod 에 인터페이스를 여럿 붙여야 할 때 |
| IPv4/IPv6 듀얼스택 | 주소 계열이 둘일 때 달라지는 것 |

### Kubernetes in Action 2nd 11~13장  `필수`

앞 단계가 모델이라면 여기는 그 모델을 쓰는 선언 API 입니다. 같은 대상을 API 축에서 한 번 더 보는 이유는, 뒤에서 Cilium 과 Istio 가 이 API 를 각자 다르게 구현하는 것을 볼 것이기 때문입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| Service 선언과 세션 어피니티 | 클라이언트를 같은 Pod 로 묶는 조건 |
| 트래픽 정책 | `internalTrafficPolicy`·`externalTrafficPolicy` 가 바꾸는 경로 |
| Ingress 와 TLS | 하나의 IP 뒤에 여러 서비스를 두는 방식 |
| Gateway API 와 HTTPRoute | Ingress 의 한계와 역할 분리 설계 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| Gateway API 의 GAMMA | 메시까지 Gateway API 로 표현하려는 흐름 |
| Ingress 에서 Gateway API 로 이행 | 기존 자원을 어떻게 옮길 것인가 |
| Topology Aware Routing | 같은 존 안으로 트래픽을 몰아 비용을 줄이기 |

### Learning CoreDNS 1~8장  `추천`

2019년 책이라 쿠버네티스 연동을 다루는 6장은 공식 DNS 스펙과 대조하며 읽습니다. Service 를 만들면 이름이 생깁니다. 그 이름을 푸는 일이 클러스터 안에서 가장 자주 깨지는 지점이라 별도 단계로 둡니다. DNS 는 Service 와 짝이지 부록이 아닙니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| Corefile 과 플러그인 체인 | 하나의 서버가 플러그인 조합으로 성격이 바뀌는 구조 |
| 존 데이터와 위임 | 위임이 그은 경계가 질의 경로를 정한다 |
| 쿠버네티스 서비스 디스커버리 | Service·Pod 에 어떤 레코드가 생기는가 |
| 질의 조작과 응답 재작성 | 질문과 답이 어긋나면 클라이언트가 버린다 |
| 모니터링과 트러블슈팅 | 무엇을 볼지 좁히는 손잡이 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| `ndots:5` 와 search 도메인 | 질의가 다섯 배로 튀는 기본값 |
| DNS TTL 과 페일오버 | 고쳤는데도 안 되는 이유가 캐시일 때 (실습 14편) |
| NodeLocal DNSCache | 그 폭증을 노드에서 흡수하는 방식 |
| CoreDNS autopath | search 도메인 순회를 서버가 대신 하기 |
| TTL 과 캐시 | 바뀐 이름이 언제 반영되는가 |



## 데이터패스 · 강한 순서

> 이 로드맵에서 가장 큰 덩어리입니다. 앞에서 선언한 것이 실제 패킷 경로가 되는 지점을 여기서 봅니다.

### Learning eBPF 1~3장, 6~9장  `필수`

kube-proxy 가 iptables 규칙 수천 개를 선형으로 훑는 구조를 왜 떠났는지 이해하려면, 그 대안이 커널의 어디에 어떻게 끼어드는지를 먼저 알아야 합니다.

7장과 8장이 이 단계의 핵심입니다. 훅이 붙는 자리는 셋인데 XDP 는 드라이버 수준이라 커널 스택에 들어오기 전에 처리하고, TC 훅은 스택 안쪽에서, socket 훅은 소켓 계층에서 동작합니다. **이 세 위치의 차이가 곧 성능과 가시성의 트레이드오프입니다.** 4~5장과 10~11장은 직접 프로그램을 짤 때 필요하니 읽는 것이 목적이면 넘어갑니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| eBPF 프로그램과 맵 | 커널 안 프로그램과 사용자 공간이 상태를 주고받는 유일한 통로 |
| verifier 제약 | 반복문과 포인터 제한이 곧 안전성 주장의 근거 |
| XDP 훅 | 드라이버 수준. 커널 스택에 들어오기 전에 패킷을 처리 |
| TC 훅 | 스택 안쪽. 대부분의 CNI 가 쓰는 자리 |
| socket 훅 | 소켓 계층. 연결 단위로 개입 |
| eBPF 보안 관측 | 같은 기술이 런타임 보안으로 쓰이는 축 (9장) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| cgroup·sockops·sockmap 훅 | 네트워킹 훅 셋 말고도 붙는 자리가 있다 |
| XDP 의 native 와 generic 모드 | 드라이버가 지원하지 않으면 성능 이점이 사라진다 |
| BPF 맵 종류와 `bpftool` | 맵을 직접 열어 보며 상태를 확인하기 |

### Cilium Up and Running 전 16장  `필수`

앞 단계가 원리라면 여기는 그 원리로 지은 실물입니다. 2장 Inside Cilium 과 5장 The Cilium Datapath 가 중심이고, "kube-proxy 를 대체한다"는 문장의 실체가 여기서 확정됩니다.

정책은 12장과 13장인데 **정책을 IP 가 아니라 identity 로 쓴다는 발상**이 여기서 나옵니다. Pod IP 가 수시로 바뀌는 환경에서 IP 기반 규칙이 왜 무너지는지를 함께 읽으면 Policy as Code 의 정책 도구들이 무엇을 자동화하려는지 보입니다. 14장의 WireGuard·IPsec 비교는 Zero Trust 국면의 mTLS 와 층이 다른 암호화라, 둘을 구분해 두면 "메시가 있는데 왜 또 암호화하는가"를 설명할 수 있게 됩니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 데이터패스 | Pod 에서 나온 패킷이 노드를 지나 다른 Pod 로 가는 실제 경로 (5장) |
| IPAM | Pod IP 를 누가 어떤 단위로 나눠 주는가 (4장) |
| kube-proxy 대체 | Service 가 eBPF 맵 조회로 바뀌는 과정 (6장) |
| identity 기반 정책 | IP 가 아니라 identity 로 쓰는 L3/L4 정책 (12장) |
| L7·FQDN 정책 | HTTP 메서드와 도메인 단위 허용 (13장) |
| egress 게이트웨이 | 클러스터 밖으로 나가는 트래픽의 출구를 고정 (11장) |
| 전송 암호화 | WireGuard 와 IPsec (14장) |
| Hubble 흐름 관측 | 지금까지 배운 경로를 흐름 단위로 보는 도구 (15장) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| kube-proxy 의 nftables 모드 | iptables 를 떠나는 또 다른 길 |
| ClusterMesh · netkit · BIG TCP | 멀티클러스터와 최근의 성능 작업 |
| 오버레이 MTU 의 세금 | 캡슐화가 먹는 바이트와 숨은 단편화 (실습 13편) |
| EndpointSlice 미러링 | 외부 엔드포인트가 클러스터 안으로 들어오는 방식 |



## 언더레이 · 순서 없음

> 클러스터가 얹히는 물리 패브릭입니다. 지금까지가 Pod 부터 위였다면 여기는 그 아래입니다.

### Cloud Native Data Center Networking 2·5·6·14·16장  `추천`

Pod 네트워크와 Service 를 다 봐도 "노드 사이 패킷이 실제로 어느 스위치를 지나는가"는 안 보입니다. 이 책이 그 층입니다. Clos 토폴로지가 왜 데이터센터의 기본형이 됐는지, 왜 L2 확장 대신 L3 라우팅으로 갔는지가 시작점입니다.

Cilium 의 네이티브 라우팅과 Production Kubernetes 5장의 BGP 가 여기서 뜻을 갖습니다. 위에서 "BGP 모드를 쓴다"고 읽은 것이 아래에서 무엇을 전제하는지 보입니다.

**7장 Container Networking 은 뺐습니다.** 2019년 책이라 Cilium 이 초기이고 eBPF 데이터패스 이전입니다. 그 자리는 데이터패스 국면이 이미 덮습니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| Clos 토폴로지 | 데이터센터가 왜 이 모양으로 수렴했는가 |
| 라우팅 프로토콜 선택 | OSPF 와 BGP 중 무엇을 언제 고르는가 |
| 네트워크 가상화 | VXLAN 이 L2 를 L3 위로 나르는 방식 |
| BGP 와 EVPN | 데이터센터 안에서 BGP 를 쓰는 이유와 EVPN 의 자리 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| BGP unnumbered | 인터페이스마다 IP 를 주지 않고 피어링하기 |
| 언더레이 MTU 설계 | 오버레이가 먹는 바이트를 아래에서 미리 확보 |



## 정책과 메시 · 메시만 순서

> 무엇을 어디서 막고 어디서 신원을 붙이는가를 정리합니다. 데이터패스에서 막는 것과 어드미션에서 막는 것은 층이 다릅니다.

### Policy as Code 4·5·7·8장, Kubernetes Best Practices 9·11장  `추천`

NetworkPolicy 는 트래픽이 흐를 때 막고, 어드미션 컨트롤은 그 정책이 만들어지기 전에 막습니다. 층이 다르므로 둘 다 필요합니다. Gatekeeper 가 Rego 를 쓰는 반면 Kyverno 는 YAML 로 규칙을 쓴다는 차이가 도입 비용을 가릅니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| OPA 와 Rego | Kubernetes 리소스를 판정하는 규칙 언어 |
| 어드미션 컨트롤 | 정책이 만들어지기 전에 막는 층 |
| Gatekeeper | Rego 로 규칙을 쓰는 구현 |
| Kyverno | YAML 로 규칙을 쓰는 구현. 도입 비용이 갈리는 지점 |
| 네트워크 보안 관례 | 현장에서 정하는 기본값 (KBP 9·11장) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| NetworkPolicy 의 한계 | egress DNS 와 CIDR 규칙이 잘 듣지 않는 이유 |
| AdminNetworkPolicy | 관리자가 네임스페이스 위에서 거는 정책 |
| ValidatingAdmissionPolicy 와 CEL | 외부 컨트롤러 없이 API 서버가 직접 판정 |

### Istio in Action 1~9장  `필수`

앰비언트를 이해하려면 그것이 무엇을 줄이려 했는지를 먼저 알아야 합니다. 사이드카 메시가 무엇을 인프라로 밀어냈고 그 대가로 무엇을 냈는지가 이 단계의 내용입니다.

메시는 앞 단계까지의 L3/L4 정책 위에 **애플리케이션 수준의 신원과 라우팅**을 얹습니다. Envoy 가 그 일을 실제로 하는 프로세스라, 3장에서 데이터 플레인을 따로 보는 것이 이후 앰비언트의 ztunnel 과 waypoint 를 읽는 바탕이 됩니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 메시가 인프라로 민 것 | 재시도·타임아웃·회로차단이 앱을 떠나는 이유 |
| Envoy 와 데이터 플레인 | 실제로 트래픽을 나르는 프로세스 |
| 게이트웨이 | 클러스터 안으로 트래픽을 들이는 문 |
| 트래픽 라우팅 | 가중치·헤더 기반 분기와 카나리 |
| 복원력 | 실패를 견디는 일을 프록시로 옮겼을 때 |
| mTLS 와 메시 관측 | 서비스 간 신원, 그리고 그 위에서 얻는 지표 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| Envoy 의 xDS 프로토콜 | 컨트롤 플레인이 프록시에 설정을 미는 방식 |
| SPIFFE 와 SPIRE | 메시 신원의 표준 규격 |
| Gateway API 와 메시의 접점 | GAMMA 가 메시 라우팅을 표준으로 끌어오는 방향 |

### Sidecar-less Istio Explained 전 4장  `추천`

사이드카 메시는 Pod 마다 프록시를 하나씩 붙여 리소스와 업그레이드 비용을 냈습니다. 앰비언트 모드는 그 비용을 줄이려고 층을 둘로 쪼갭니다. Learning eBPF 에서 본 eBPF 훅 지식이 여기서 회수되는데, ztunnel 로 트래픽을 우회시키는 방식이 커널 훅 위에서 동작하기 때문입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 앰비언트 모드의 전제 | 대부분의 워크로드가 L7 정책을 쓰지 않는다는 관찰 |
| ztunnel | 노드마다 하나씩 떠서 L4 와 mTLS 를 맡는 프록시 |
| waypoint | L7 처리가 필요할 때만 뜨는 프록시 |
| 사이드카와의 차이 | 기존 메시를 어떤 조건에서 옮길지 판단하는 근거 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| waypoint 를 어느 단위로 둘지 | 네임스페이스 단위와 서비스 단위의 차이 |
| 앰비언트의 성숙도 | 어느 기능이 아직 사이드카에만 있는가 |



## 운영과 신뢰 · 순서 없음

> 고르는 법과 지키는 법입니다. 여기까지 오면 클러스터의 네트워크를 남에게 설명할 수 있게 됩니다.

### Production Kubernetes 5·6·10장  `추천`

앞에서 Cilium 한 구현을 깊게 봤으니, 이제 여러 구현을 놓고 고르는 축이 필요합니다. 캡슐화 오버헤드를 낼 것인가, 아니면 하부 네트워크에 라우팅을 요구할 것인가라는 선택이 5장의 핵심입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 오버레이 대 네이티브 라우팅 | 캡슐화 오버헤드냐, 하부 네트워크 요구냐 |
| BGP | 하부 네트워크와 경로를 나누는 방식 |
| 서비스 라우팅 선택 | kube-proxy 모드와 대안, Ingress 컨트롤러 고르기 |
| 워크로드 신원 | 제로 트러스트로 넘어가는 다리 (10장) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| CNI 성능 벤치마크 | 남의 수치가 아니라 내 클러스터에서 재는 법 |
| 노드 수와 규칙 수의 관계 | 클러스터가 커질 때 무엇이 먼저 무너지는가 |
| MetalLB 의 L2 와 BGP 모드 | 온프레미스에서 LoadBalancer 를 세우는 법 (실습 17편) |

### Container Security 10·11장  `추천`

Drive 에 있는 것은 2020년 1판인데 2025년에 2판이 나왔으니 구할 수 있으면 2판을 봅니다. 정책과 메시가 붙기 전에 컨테이너 자체가 네트워크에서 어떻게 노출되는지를 봅니다. 10장은 계층별로 나눠 막는 방법이고, 11장은 그 위에서 TLS 로 컴포넌트를 잇는 방법입니다. 12단계의 제로 트러스트가 원리라면 이 두 장은 그 원리가 컨테이너에 닿는 자리입니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 계층별 네트워크 차단 | 어느 계층에서 막는 것이 싸고 확실한가 |
| 컨테이너 방화벽과 정책 | NetworkPolicy 가 실제로 무엇을 거는가 |
| TLS 로 컴포넌트 잇기 | 키·인증서·CA 가 각각 맡는 역할 |
| 인증서 검증의 실패 지점 | 검증을 끄면 무엇이 무너지는가 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| 인증서 회전과 SDS | 만료가 장애가 되지 않게 하는 구조 |
| cert-manager | 클러스터 안에서 인증서를 발급하고 갱신하기 |

### Zero Trust Networks 4~8장, CKS Study Guide 2·3·5장, Real-World Cryptography 5·9장  `선택`

Zero Trust Networks 는 "네트워크 위치를 신뢰하지 않는다"는 전제에서 다시 시작합니다. 앞에서 배운 mTLS 와 NetworkPolicy 가 이 틀 안에서 각각 어떤 자리를 차지하는지 정리됩니다. CKS 는 같은 내용을 시험 축으로 되짚고, Real-World Cryptography 5·9장은 mTLS 가 딛는 바닥을 한 겹 더 팝니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 신뢰 모델 | 네트워크 위치를 신뢰하지 않는다는 전제 |
| 인가 결정 | 무엇을 근거로 허용할지 (ZTN 4장) |
| 기기·신원·앱 신뢰 | 신뢰를 세우는 세 축 (ZTN 5~7장) |
| 트래픽 신뢰 | mTLS 와 필터링이 이 틀에서 갖는 자리 (ZTN 8장) |
| 클러스터 하드닝 | API 서버 접근 제한, NetworkPolicy, Ingress TLS (CKS 2·3장) |
| 키 교환 | 세션 키가 만들어지는 절차 (RWC 5장) |
| 보안 전송 | TLS 의 내부 구조 (RWC 9장) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| 암호화를 겹쳐 쓸 때의 판단 | mTLS 와 전송 암호화를 둘 다 켤 것인가 |
| 감사 로그와 네트워크 이벤트 | 막은 것을 어떻게 증명할 것인가 |



## 조건부 · 목표가 생겼을 때만

> 필수 구간과 달리 목표가 생겼을 때만 엽니다. 순서대로 읽을 이유는 없습니다.

### HTTP:2 in Action 4·8장과 RFC 9000·9113·9114  `선택`

Envoy 와 gRPC 가 실제로 무엇을 나르는지까지 팔 때 엽니다. High Performance Browser Networking 을 여기 두지 않은 이유는 2013년 책이어서입니다. HTTP/2 가 아직 초안이던 시점이라 QUIC 과 HTTP/3 이 아예 없습니다. HTTP:2 in Action 도 2019년이라 프레이밍과 HPACK 만 가져오고, 전송 계층은 RFC 를 정본으로 씁니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| HTTP/2 프레이밍 | 스트림 다중화가 동작하는 방식 |
| HPACK 헤더 압축 | 프록시 부하와 직결되는 압축 구조 |
| QUIC 와 HTTP/3 | 전송 계층이 UDP 로 바뀌는 이유 (RFC 9000·9114) |
| 0-RTT 와 연결 마이그레이션 | QUIC 이 핸드셰이크 비용을 줄이는 방식 (RFC 9000) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| Envoy 의 QUIC 지원 | 메시가 HTTP/3 을 나를 수 있는가 |
| gRPC 로드밸런싱 | 연결 하나를 오래 쓰면 L4 분산이 듣지 않는 이유 |
| HTTP/3 의 0-RTT | 재전송과 재생 공격 사이의 거래 |

### System Design on AWS 5·9장, Mastering OpenStack 6장, Operating OpenShift 3·4장  `선택`

클러스터 밖으로 나갈 때 엽니다. Mastering OpenStack 6장은 Neutron 이고, 회사 CMP 가 딛고 선 바닥이라 실무에서 바로 걸립니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| VPC 와 로드밸런서 | 서브넷과 보안그룹이 EKS 와 만나는 지점 |
| Neutron | OpenStack 네트워킹의 구성요소 |
| OpenShift 운영 | 워크로드와 보안. 네트워킹 전용 장은 없음 |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| VPC CNI 의 ENI 한계 | 노드당 Pod 수가 인스턴스 타입에 묶이는 구조 |
| prefix delegation | 그 한계를 늘리는 방식 |
| Pod 단위 보안그룹 | 클라우드 방화벽을 Pod 에 직접 거는 길 |
| OVN-Kubernetes | OpenShift 의 기본 CNI |

### Network Programming with Go 1~7장과 client-go 공식 문서  `선택`

읽는 축에서 만드는 축으로 넘어가는 자리입니다. `~/study/podwire` 의 로드맵이 미니 CNI 에서 Service, Policy, eBPF, WireGuard, ztunnel 로 올라가는 순서라 이 단계와 그대로 이어집니다.

Programming Kubernetes 를 빼고 공식 문서를 넣었습니다. 2019년 책이라 그사이 client-go 와 코드 생성 방식이 많이 바뀌었고, Kubernetes 의 `sample-controller` 저장소가 현행 코드를 그대로 보여 줍니다.

| 개념 | 무엇을 알게 되는가 |
|---|---|
| 소켓과 주소 해석 | 이름이 주소가 되고 연결이 열리는 과정을 코드로 |
| TCP·UDP 직접 다루기 | 스트림과 데이터그램의 차이를 손으로 |
| Unix 도메인 소켓 | 같은 호스트 안에서의 통신 |
| client-go 와 informer | 네트워크 오브젝트를 감시하고 조정하기 (`sample-controller`) |

| 책 밖 키워드 | 왜 보는가 |
|---|---|
| CNI 플러그인 규약 | ADD·DEL·CHECK 세 동작이 계약의 전부 |
| netlink 로 veth 만들기 | 명령이 아니라 코드로 인터페이스를 세우기 |
| SIG-Network KEP | 다음에 무엇이 바뀌는지 미리 읽기 |



## 로드맵에 넣지 않은 책

> `book/` 아래 97개 중 네트워크에 걸치는 책은 스무 권이 넘습니다. 뺀 책에도 이유가 있어서 어디에 쓸지를 적어 둡니다.

### 참조서 · 통독하지 않고 막힐 때만 엽니다

이 책들을 단계에 넣지 않은 이유는 분량입니다. 앞에서 끝까지 읽으면 로드맵이 두 배가 되는데, 정작 필요한 것은 특정 장 하나일 때가 많습니다.

| 책 | 열 장면 |
|---|---|
| Computer Networking Top-Down 9판 **2·6·8장** | DNS·HTTP, 링크 계층·ARP, 보안. 3·4·5장은 바닥 국면에서 읽습니다 |
| CompTIA Network+ 6th | 7장 IP 주소, 8장 서브네팅·NAT, 9·10장 라우팅, 11장 스위칭·VLAN |
| How Linux Works 3rd | 9장 네트워크 설정, 10장 네트워크 응용 |
| High Performance Browser Networking | 지연과 대역폭의 감각이 필요할 때만. 2013년 책이라 HTTP/3 은 없습니다 |
| Programming Kubernetes | 컨트롤러의 개념 지도가 필요할 때. 2019년 책이라 코드는 공식 저장소를 봅니다 |

### 단계와 자리가 겹치는 책

같은 요소를 다른 각도에서 다룹니다. 단계 대신 이쪽을 골라도 되고, 설명이 부족할 때 대조 자료로 씁니다.

| 책 | 겹치는 자리 |
|---|---|
| Kubernetes Up and Running 3rd 7·15·20·21장 | 서비스 디스커버리, 메시 도입 판단, 정책, 멀티클러스터 |
| Kubernetes Patterns 2nd 24장 | Network Segmentation |
| Systems Performance 2nd 10·15장 | 네트워크 성능 방법론과 BPF 관측 도구 |
| Networking and Kubernetes 1·2·6장 | 2단계에서 3~5장만 읽었을 때 남는 OSI·커널·클라우드 부분 |

### 이웃 주제

네트워크 요소를 직접 채우지는 않지만 옆에서 만나는 책들입니다.

| 책 | 무엇을 보태는가 |
|---|---|
| API Security in Action 10·11장 | Kubernetes 안의 API 보안, 서비스 간 통신 인증 |
| Distributed Tracing in Practice | 메시 관측을 요청 추적 축으로 확장 |
| Designing Distributed Systems 3·4·6장 | 사이드카·앰배서더·부하분산 패턴의 원형 |
| Network Programmability and Automation 2nd | 네트워크 장비 자동화. 클러스터 밖 축입니다 |
| Learning DevSecOps | 파이프라인에 보안을 끼우는 축 |



## 경계

> 같은 주제를 다루는 문서가 셋이라 무엇을 어디서 찾을지 갈라 둡니다.

네트워크는 한 카테고리에 담기지 않습니다. 커널과 패킷은 `02_os`, Service 와 메시는 `08_cloud`, 제로 트러스트와 암호는 `99_ETC/security` 에 흩어져 있어서 어느 카테고리 README도 이 순서를 혼자 가질 수 없습니다. 그래서 이 문서는 `write/` 직계에 둡니다.

책을 고르고 순서를 정하는 일은 이 문서가 맡습니다. Linux 네트워크 원리를 키워드 축으로 늘어놓은 것은 [`02_os/networking/roadmap.md`](02_os/networking/roadmap.md) 가, Kubernetes 공식 문서의 개념 학습 순서는 [`08_cloud/kubernetes/04_networking/`](08_cloud/kubernetes/04_networking/README.md) 가 맡습니다.
