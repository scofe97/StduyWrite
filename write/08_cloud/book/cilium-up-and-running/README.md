---
title: Cilium Up and Running — 정독 인덱스
tags: [moc, study-index, book, cilium, ebpf, cni, kubernetes, hubble]
status: draft
source:
  - 《Cilium: Up and Running》(Nico Vibert · Filip Nikolic · James Laverack, O'Reilly, 2026, ISBN 979-8-341-62299-9) — 장 단위 PDF 16편
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Cilium Up and Running/
  - https://docs.cilium.io/en/stable/
related:
  - ./01-01.Cilium%20은%20eBPF%20데이터패스로%20iptables%20기반%20CNI%20의%20한계를%20넘는다.md
  - ./02-01.Cilium%20은%20에이전트·CNI%20플러그인·오퍼레이터로%20나눠%20노드와%20클러스터를%20맡는다.md
  - ./03-01.Cilium%20은%20kind%20클러스터에%20Helm%20으로%20설치하고%20정책과%20Hubble%20로%20동작을%20확인한다.md
  - ./04-01.Cilium%20IPAM%20모드는%20Pod%20대역을%20누가%20나눠%20주는지로%20갈린다.md
  - ./05-01.Cilium%20데이터패스는%20같은%20노드는%20eBPF%20로%20바로%20넘기고%20다른%20노드는%20라우팅이나%20터널로%20잇는다.md
  - ./06-01.Cilium%20은%20kube-proxy%20를%20eBPF%20로%20대신하고%20외부%20서비스에%20IP%20와%20경로를%20붙인다.md
  - ./07-01.Cilium%20Ingress%20는%20노드의%20Envoy%20로%20바깥%20HTTP%20를%20받고%20TLS%20를%20끝낸다.md
  - ./07-02.Gateway%20API%20는%20역할별%20객체로%20라우팅을%20나누고%20가중치·헤더·동서%20트래픽까지%20맡는다.md
  - ./08-01.트래픽%20분배와%20로컬%20리다이렉트는%20서비스%20트래픽을%20가까운%20백엔드로%20보낸다.md
  - ./08-02.DSR·Maglev·netkit%20은%20응답%20경로와%20백엔드%20선택과%20Pod%20연결의%20비용을%20줄인다.md
  - ./09-01.Cluster%20Mesh%20는%20클러스터마다%20API%20서버를%20두고%20서로의%20상태를%20읽어%20하나의%20망을%20만든다.md
  - ./09-02.전역%20서비스와%20전역%20정책은%20Cluster%20Mesh%20위에서%20클러스터%20경계를%20넘는다.md
  - ./10-01.L2%20Announcements%20는%20ARP%20응답으로%20서비스%20IP%20를%20같은%20L2%20망에%20알린다.md
  - ./10-02.BGP%20는%20피어%20라우터에%20Pod%20와%20서비스%20대역%20경로를%20광고한다.md
  - ./11-01.Egress%20는%20마스커레이딩과%20Egress%20Gateway%20로%20나가는%20출발지를%20정하고%20Bandwidth%20Manager%20로%20속도를%20묶는다.md
  - ./12-01.Cilium%20정책은%20라벨에서%20만든%20identity%20로%20허용을%20판정하고%20정책이%20붙으면%20기본%20거부가%20된다.md
  - ./12-02.여러%20규칙과%20클러스터%20범위·CIDR·거부%20규칙으로%20정책의%20경계를%20넓힌다.md
  - ./13-01.L7%20정책은%20Envoy%20로%20HTTP%20메서드와%20경로를%20검사한다.md
  - ./13-02.FQDN%20정책은%20DNS%20프록시가%20본%20응답%20IP%20를%20정책%20identity%20로%20바꾼다.md
  - ./13-03.HTTPS%20정책은%20TLS%20를%20끊어%20다시%20맺어야%20경로를%20볼%20수%20있다.md
  - ./14-01.Transparent%20Encryption%20은%20노드%20사이%20트래픽을%20WireGuard%20로%20감싼다.md
  - ./15-01.Hubble%20은%20노드마다%20흐름을%20모아%20Relay%20로%20묶고%20L7%20가시성과%20지표로%20내보낸다.md
  - ./16-01.Cilium%20운영은%20설치%20도구와%20업그레이드·CNI%20이전%20계획에서%20시작한다.md
  - ./16-02.Day%202%20장애는%20상태%20확인에서%20기능별%20점검%20순서로%20좁혀%20간다.md
  - ../networking-and-kubernetes/README.md
  - ../istio-in-action/README.md
  - ../../README.md
learning:
  topic: cilium-up-and-running
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "16장까지 정독 완료 — 01-01 부터 Phase 4 자답·복습으로 넘어간다"
updated: 2026-10-10
---

# Cilium Up and Running — 정독 인덱스

---

> 이 폴더는 『Cilium: Up and Running』(Vibert · Nikolic · Laverack, O'Reilly)을 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 16장을 모두 썼습니다(장에 따라 한 편에서 세 편).

## 이 책을 여기 두는 이유

> 같은 폴더의 정독본들이 쿠버네티스 네트워킹의 원리와 사이드카 메시를 세웠다면, 이 책은 그 일을 커널 안 eBPF 데이터패스 하나로 옮기면 무엇이 바뀌는지를 맡습니다.

`08_cloud` 는 클러스터 안에서 무엇이 어떻게 돌아가는지를 다루는 카테고리입니다. [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)은 iptables·IPVS·eBPF 가 무엇인지, CNI 와 kube-proxy 가 Pod 네트워크를 어떻게 잇는지를 이미 다룹니다. [『Istio in Action』 정독본](../istio-in-action/README.md)은 사이드카 프록시를 요청 경로에 얹었을 때 얻는 것과 잃는 것을 다룹니다.

이 책은 두 정독본 사이에 놓입니다. 같은 Pod 연결·서비스 부하 분산·정책·관측을 Cilium 이라는 CNI 하나가 eBPF 프로그램과 맵으로 처리할 때 구성 요소가 어떻게 나뉘고, 무엇을 커널에 두고 무엇을 Envoy 에 넘기는지가 이 폴더의 몫입니다.

경계는 한 문장으로 긋습니다. 개념 자체(iptables 체인, CNI 명세, 사이드카 모델)는 저쪽 정독본으로 링크하고, 여기에는 Cilium 이 그 개념을 어떻게 구현하고 어디서 다르게 결정했는지만 남깁니다.



## 범위와 읽는 순서

> 1·2장이 왜 Cilium 인가와 내부 구성 요소를 세우고, 3장부터 설치·IPAM·데이터패스·서비스·정책·관측을 장마다 하나씩 맡습니다.

| 장 | 제목 | 상태 |
|---|---|---|
| 1 | Why Cilium? | 작성 |
| 2 | Inside Cilium | 작성 |
| 3 | Getting Started with Cilium | 작성 |
| 4 | IP Address Management | 작성 |
| 5 | The Cilium Datapath | 작성 |
| 6 | Service Networking | 작성 |
| 7 | Ingress and Gateway API | 작성 |
| 8 | Performance Networking and Traffic Optimization | 작성 |
| 9 | Multicluster Networking | 작성 |
| 10 | Cluster Access | 작성 |
| 11 | Cluster Egress | 작성 |
| 12 | Network Policy | 작성 |
| 13 | Layer 7 and FQDN Policy | 작성 |
| 14 | Transparent Encryption | 작성 |
| 15 | Observability with Hubble | 작성 |
| 16 | Operations | 작성 |

장 제목은 챕터 PDF 파일명에서 옮겼습니다.



## 작성된 정독 노트

> 편마다 원문 장과 한 줄 핵심을 둡니다.

| 편 | 원문 | 한 줄 핵심 |
|---|---|---|
| [01-01 Cilium 은 eBPF 데이터패스로 iptables 기반 CNI 의 한계를 넘는다](./01-01.Cilium%20은%20eBPF%20데이터패스로%20iptables%20기반%20CNI%20의%20한계를%20넘는다.md) | 1장 | eBPF 맵 조회가 iptables 규칙의 선형 탐색을 대신하고, CNI 하나가 서비스·Ingress·정책·암호화·관측까지 맡게 된 흐름 |
| [02-01 Cilium 은 에이전트·CNI 플러그인·오퍼레이터로 나눠 노드와 클러스터를 맡는다](./02-01.Cilium%20은%20에이전트·CNI%20플러그인·오퍼레이터로%20나눠%20노드와%20클러스터를%20맡는다.md) | 2장 | 패킷 처리가 필요한 노드 영역(에이전트·CNI 플러그인·Envoy·DNS 프록시)과 전역 일관성이 필요한 클러스터 영역(오퍼레이터·Hubble Relay)을 나눈 구성 |
| [03-01 Cilium 은 kind 클러스터에 Helm 으로 설치하고 정책과 Hubble 로 동작을 확인한다](./03-01.Cilium%20은%20kind%20클러스터에%20Helm%20으로%20설치하고%20정책과%20Hubble%20로%20동작을%20확인한다.md) | 3장 | kind 클러스터에 기본 CNI 를 끄고 Helm 으로 Cilium 을 설치한 뒤, 라벨 기반 정책과 L7 규칙을 걸고 Hubble 로 판정을 흐름 단위로 보는 실습 |
| [04-01 Cilium IPAM 모드는 Pod 대역을 누가 나눠 주는지로 갈린다](./04-01.Cilium%20IPAM%20모드는%20Pod%20대역을%20누가%20나눠%20주는지로%20갈린다.md) | 4장 | Pod 대역을 쿠버네티스(Host Scope)·오퍼레이터(Cluster Scope)·풀 CRD(Multi-Pool)·AWS ENI 중 누가 나눠 주는지에 따라 갈리는 IPAM 모드와 듀얼 스택·IPv6 전용 |
| [05-01 Cilium 데이터패스는 같은 노드는 eBPF 로 바로 넘기고 다른 노드는 라우팅이나 터널로 잇는다](./05-01.Cilium%20데이터패스는%20같은%20노드는%20eBPF%20로%20바로%20넘기고%20다른%20노드는%20라우팅이나%20터널로%20잇는다.md) | 5장 | 같은 노드는 veth 의 eBPF 프로그램이 바로 넘기고, 다른 노드는 PodCIDR 경로를 알리는 native routing 이나 VXLAN·Geneve 터널로 잇는 데이터패스 |
| [06-01 Cilium 은 kube-proxy 를 eBPF 로 대신하고 외부 서비스에 IP 와 경로를 붙인다](./06-01.Cilium%20은%20kube-proxy%20를%20eBPF%20로%20대신하고%20외부%20서비스에%20IP%20와%20경로를%20붙인다.md) | 6장 | kube-proxy 를 eBPF 서비스 맵으로 대신하고(KPR) 에이전트가 멈춰도 데이터패스가 도는 구조, NodePort·LoadBalancer·LB IPAM |
| [07-01 Cilium Ingress 는 노드의 Envoy 로 바깥 HTTP 를 받고 TLS 를 끝낸다](./07-01.Cilium%20Ingress%20는%20노드의%20Envoy%20로%20바깥%20HTTP%20를%20받고%20TLS%20를%20끝낸다.md) | 7장 | 별도 Ingress 컨트롤러 없이 eBPF 가 서비스 포트에서 가로채 TPROXY 로 노드 Envoy 에 넘기는 Ingress 와 TLS 종단, Ingress 의 한계 |
| [07-02 Gateway API 는 역할별 객체로 라우팅을 나누고 가중치·헤더·동서 트래픽까지 맡는다](./07-02.Gateway%20API%20는%20역할별%20객체로%20라우팅을%20나누고%20가중치·헤더·동서%20트래픽까지%20맡는다.md) | 7장 | GatewayClass·Gateway·HTTPRoute 로 역할을 나눈 라우팅, 가중치 분배·헤더 수정·GAMMA 동서 트래픽 |
| [08-01 트래픽 분배와 로컬 리다이렉트는 서비스 트래픽을 가까운 백엔드로 보낸다](./08-01.트래픽%20분배와%20로컬%20리다이렉트는%20서비스%20트래픽을%20가까운%20백엔드로%20보낸다.md) | 8장 | trafficDistribution 으로 같은 존 백엔드를 고르고, Local Redirect Policy 로 서비스 트래픽과 DNS 질의를 같은 노드로 돌리는 방법 |
| [08-02 DSR·Maglev·netkit 은 응답 경로와 백엔드 선택과 Pod 연결의 비용을 줄인다](./08-02.DSR·Maglev·netkit%20은%20응답%20경로와%20백엔드%20선택과%20Pod%20연결의%20비용을%20줄인다.md) | 8장 | 응답이 진입 노드를 거치지 않는 DSR, 진입 노드가 바뀌어도 같은 백엔드를 고르는 Maglev, veth 비용을 줄이는 netkit |
| [09-01 Cluster Mesh 는 클러스터마다 API 서버를 두고 서로의 상태를 읽어 하나의 망을 만든다](./09-01.Cluster%20Mesh%20는%20클러스터마다%20API%20서버를%20두고%20서로의%20상태를%20읽어%20하나의%20망을%20만든다.md) | 9장 | 클러스터마다 clustermesh-apiserver 를 두고 공통 CA 로 서로를 믿게 해 잇는 Cluster Mesh 구조와 준비 조건 |
| [09-02 전역 서비스와 전역 정책은 Cluster Mesh 위에서 클러스터 경계를 넘는다](./09-02.전역%20서비스와%20전역%20정책은%20Cluster%20Mesh%20위에서%20클러스터%20경계를%20넘는다.md) | 9장 | 주석으로 묶는 전역 서비스, affinity 로 고르는 로컬 우선 백엔드, 클러스터 라벨로 거르는 전역 정책과 인증서 |
| [10-01 L2 Announcements 는 ARP 응답으로 서비스 IP 를 같은 L2 망에 알린다](./10-01.L2%20Announcements%20는%20ARP%20응답으로%20서비스%20IP%20를%20같은%20L2%20망에%20알린다.md) | 10장 | 리스를 쥔 노드 하나가 ARP 로 서비스 IP 를 알리는 L2 Announcements 와 노드 장애 시 리스 이전 |
| [10-02 BGP 는 피어 라우터에 Pod 와 서비스 대역 경로를 광고한다](./10-02.BGP%20는%20피어%20라우터에%20Pod%20와%20서비스%20대역%20경로를%20광고한다.md) | 10장 | 세 BGP 리소스로 피어·광고 대상을 나눠 외부 라우터에 PodCIDR·서비스 IP 경로를 광고하는 방법 |
| [11-01 Egress 는 마스커레이딩과 Egress Gateway 로 나가는 출발지를 정하고 Bandwidth Manager 로 속도를 묶는다](./11-01.Egress%20는%20마스커레이딩과%20Egress%20Gateway%20로%20나가는%20출발지를%20정하고%20Bandwidth%20Manager%20로%20속도를%20묶는다.md) | 11장 | BPF 마스커레이딩과 예외 대역, 정해진 노드·IP 로 나가게 하는 Egress Gateway, EDT 기반 Bandwidth Manager |
| [12-01 Cilium 정책은 라벨에서 만든 identity 로 허용을 판정하고 정책이 붙으면 기본 거부가 된다](./12-01.Cilium%20정책은%20라벨에서%20만든%20identity%20로%20허용을%20판정하고%20정책이%20붙으면%20기본%20거부가%20된다.md) | 12장 | 라벨에서 만든 identity 로 판정하는 정책, 정책이 붙으면 그 방향이 기본 거부가 되는 이유와 identity 폭증 억제 |
| [12-02 여러 규칙과 클러스터 범위·CIDR·거부 규칙으로 정책의 경계를 넓힌다](./12-02.여러%20규칙과%20클러스터%20범위·CIDR·거부%20규칙으로%20정책의%20경계를%20넓힌다.md) | 12장 | 규칙 여럿의 OR·문장 안의 AND, 클러스터 범위 정책, CIDR·엔티티 규칙, allow 보다 먼저 이기는 deny 규칙 |
| [13-01 L7 정책은 Envoy 로 HTTP 메서드와 경로를 검사한다](./13-01.L7%20정책은%20Envoy%20로%20HTTP%20메서드와%20경로를%20검사한다.md) | 13장 | L7 규칙이 있을 때만 Envoy 를 거쳐 HTTP 메서드·경로를 검사하는 정책과 그 비용 |
| [13-02 FQDN 정책은 DNS 프록시가 본 응답 IP 를 정책 identity 로 바꾼다](./13-02.FQDN%20정책은%20DNS%20프록시가%20본%20응답%20IP%20를%20정책%20identity%20로%20바꾼다.md) | 13장 | DNS 프록시가 본 응답 IP 를 FQDN identity 로 묶어 이름으로 egress 를 여는 정책, TTL 과 CDN 의 함정 |
| [13-03 HTTPS 정책은 TLS 를 끊어 다시 맺어야 경로를 볼 수 있다](./13-03.HTTPS%20정책은%20TLS%20를%20끊어%20다시%20맺어야%20경로를%20볼%20수%20있다.md) | 13장 | HTTPS 경로를 보려고 Envoy 가 TLS 를 끊어 다시 맺는 구조, 내부 CA 와 originatingTLS·terminatingTLS |
| [14-01 Transparent Encryption 은 노드 사이 트래픽을 WireGuard 로 감싼다](./14-01.Transparent%20Encryption%20은%20노드%20사이%20트래픽을%20WireGuard%20로%20감싼다.md) | 14장 | 노드 사이 트래픽만 WireGuard 로 감싸는 Transparent Encryption, 노드 공개키 배포와 캡처로 본 암호화 |
| [15-01 Hubble 은 노드마다 흐름을 모아 Relay 로 묶고 L7 가시성과 지표로 내보낸다](./15-01.Hubble%20은%20노드마다%20흐름을%20모아%20Relay%20로%20묶고%20L7%20가시성과%20지표로%20내보낸다.md) | 15장 | 노드별 Hubble 서버를 Relay 로 묶고 CLI 필터·Exporter·L7 가시성·흐름 가리기·지표로 내보내는 관측 |
| [16-01 Cilium 운영은 설치 도구와 업그레이드·CNI 이전 계획에서 시작한다](./16-01.Cilium%20운영은%20설치%20도구와%20업그레이드·CNI%20이전%20계획에서%20시작한다.md) | 16장 | 설치 도구 고르기, 한 마이너씩 올리는 업그레이드와 그동안의 트래픽 유지, 다른 CNI 에서 노드 단위 이전 |
| [16-02 Day 2 장애는 상태 확인에서 기능별 점검 순서로 좁혀 간다](./16-02.Day%202%20장애는%20상태%20확인에서%20기능별%20점검%20순서로%20좁혀%20간다.md) | 16장 | 상태·연결 시험·노드 건강·sysdump 순의 Day 2 점검과 L7·L2 Announcements·BGP 기능별 장애 판단 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 1~16장 완료 (24편) |
| 난이도 레벨 | 기본. 학습자 자답 전이라 조정 근거는 아직 없습니다 |
| 막힌 지점 | 아직 없음 |
| 다음 레슨 후보 | 정독은 끝났습니다. 01-01 부터 Phase 4 자답으로 이해를 확인합니다 |
| 최근 검증 결과 | 2026-10-10 2편 작성. 원문·docs.cilium.io·소스와 대조하는 적대적 검증에서 1차 오류 16건과 의심 16건이 나왔습니다. Hubble Relay 포트, Envoy DaemonSet 기본값 전환 버전, ipcache 맵 이름과 종류 등을 고쳤고, 재검증과 최종 검증 뒤 미해결 0입니다. 게이트 실패 0, 도식 11장 글자 예산 통과. 같은 날 3~5장 3편(도식 18장) 추가. agy 두 계정이 할당량을 다 써서 Claude Sonnet 창이 썼고, 1차 검증에서 오류 8건·의심 26건(kind 서비스 대역 /12→/16 퇴행 수정, ENI 는 EKS 전용이 아님, prefix delegation 기본 꺼짐, VXLAN 포트 출처 경로, 책 장 번호 지칭 등)을 고쳤습니다. 최종 검증에서 미해결 1건과 새 오류 1건(ENI 상한 라벨의 PD 조건, 링크 위치)도 고쳐 미해결 0, 3편 게이트 실패 0. 같은 날 6~16장 19편(도식 72장) 추가. agy 두 계정이 할당량을 다 쓴 뒤로는 cc-work 의 Claude Sonnet 창이 썼습니다. 1차 검증에서 오류 79건·의심 131건(지어낸 출력·IP 짝, 책과 다른 명령 출력 짝짓기, Envoy 리다이렉트 방식, DSR·Maglev 조건, trafficDistribution 버전, WireGuard AllowedIPs, 예약 identity 번호, 책 원문의 Helm YAML 들여쓰기 오류 등)을 고쳤고, 최종 검증과 재확인에서 나온 잔여를 고쳐 미해결 0입니다. 그 과정에서 02-01 의 DNS 프록시 문장 두 곳도 v1.20.2 동작으로 고쳤습니다. 24편 게이트 실패 0 |
| 복습 회차 | 없음 |



## 출처와 톤

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·이름은 원문에서만 가져오고, 책 밖 보강은 [Cilium 공식 문서](https://docs.cilium.io/en/stable/) 같은 1차 자료를 그 사실이 쓰이는 절에 링크로 녹입니다.
- 노트는 책 없이 읽히게 씁니다. 본문에 그림 번호·쪽·절 번호 같은 책 지칭을 두지 않고, 출처는 frontmatter 와 `## 참고 자료` 에만 적습니다.
- 책과 현재 동작이 다르면 그 절의 설명 안에 현재 동작을 1차 자료 링크와 함께 씁니다.
- 톤은 합니다체입니다. 도식 생성기는 `_assets/_gen/` 에 있고 `_assets/` 에서 실행합니다. `dd.py` 는 TII 정독본 `_assets/dd.py` 의 사본입니다.
- 이 저장소의 원격은 공개 저장소이므로 클러스터 실습을 붙일 때 사내 주소·이름을 쓰지 않습니다.
