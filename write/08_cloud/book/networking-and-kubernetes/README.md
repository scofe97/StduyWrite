---
title: Networking and Kubernetes — 정독 인덱스
tags: [moc, study-index, book, kubernetes, networking, linux-networking, cni, kube-proxy]
status: draft
source:
  - 《Networking and Kubernetes: A Layered Approach》(James Strong·Vallery Lancey, O'Reilly, 2021, ISBN 978-1492081654)
  - https://www.amazon.com/Networking-Kubernetes-Approach-James-Strong/dp/1492081655  # 서지 확인 (2026-07-16 조회)
related:
  - ../kubernetes-in-action/README.md
  - ../../kubernetes/README.md
  - ../../README.md
updated: 2026-08-24
---

# Networking and Kubernetes — 정독 인덱스
---
> 이 폴더는 『Networking and Kubernetes: A Layered Approach』(James Strong·Vallery Lancey, O'Reilly, 2021)를 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

> `08_cloud` 안에서 이 책이 맡는 자리와, 이 책만 정독으로 읽는 이유를 적습니다.

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 질문을 네트워킹 축으로 파고듭니다 — TCP/IP와 Linux 네트워킹이라는 바닥에서 출발해, 컨테이너·CNI를 거쳐 kube-proxy·Service·Ingress, 마지막으로 클라우드 관리형 K8s의 네트워크까지 층(layer)을 하나씩 쌓아 올리는 구성입니다. 제목의 "A Layered Approach"가 곧 책의 목차 구조입니다.

같은 폴더의 [『Kubernetes in Action』 정독본](../kubernetes-in-action/README.md)이 오브젝트 중심이라면 이 책은 패킷 중심입니다. 저쪽이 무엇을 배포하는가를 다루고, 여기는 그 오브젝트 사이를 트래픽이 실제로 어떻게 흐르는가를 다룹니다.

그래서 Service·Ingress처럼 겹치는 주제가 나와도 관점이 다릅니다. 저쪽이 사용법이라면 여기는 구현 원리입니다. 개념이 겹치는 지점은 [`../../kubernetes/`](../../kubernetes/README.md) 개념 노트와 `../../service-mesh/` <!-- 링크 끊김(2026-08): ../../service-mesh/README.md -->로 링크를 걸어 넘깁니다. 이 폴더에는 이 책만의 계층 관점과 예제에서 새로 얻는 것만 남깁니다.



## 장별 목표

> 각 장 PDF 앞머리의 저자 선언("In this chapter, we will…")을 근거로 채웠습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Networking Introduction | 네트워킹 기술·표준의 발전사를 훑고, 지배적 네트워킹 이론을 개관하며, 책 전체 예제의 기반이 될 Go 웹 서버를 소개 | 네트워킹 역사, OSI·TCP/IP 모델, Go 웹 서버 |
| 2 | Linux Networking | K8s 네트워크 스택 이해에 필요한 Linux 네트워킹 기초 — K8s에서 주목할 지점 중심의 스택 개요 | Linux 네트워크 스택, 인터페이스, 네트워크 관리 도구 |
| 3 | Container Networking Basics | 컨테이너의 역사와 실행 옵션·네트워킹 셋업을 살피고, Docker 네트워킹 모델과 CNI의 차이를 설명한 뒤 Docker 네트워킹 모드 예제로 마무리 | 컨테이너 역사, Docker 네트워킹 모델, CNI |
| 4 | Kubernetes Networking Introduction | Pod가 클러스터 내부·외부와 연결되는 방식과 K8s 내부 컴포넌트의 연결을 다룸 — K8s가 푸는 네트워킹 문제 4가지(컨테이너 간·Pod 간·Pod-Service·외부-Service) | Pod 네트워킹, kubelet·kube-proxy, CNI 플러그인 |
| 5 | Kubernetes Networking Abstractions | 서비스 디스커버리와 로드밸런싱 추상화 — 가장 가시적인 네트워크 스택인 Service와 Ingress의 동작 원리 | Service 유형, Endpoints, Ingress |
| 6 | Kubernetes and Cloud Networking | AWS·Azure·GCP의 네트워크 서비스가 그 클라우드 안에서 K8s 클러스터 운영에 필요한 네트워킹에 어떤 영향을 주는지, 각 프로바이더 CNI와 함께 탐구 | AWS·Azure·GCP 네트워크, 관리형 K8s, 클라우드 CNI |



## 작성된 정독 노트

> 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태만 "작성 예정"으로 표시하고, 본문 내용은 원문 도착 전까지 채우지 않습니다.

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%97%AD%EC%82%AC%EC%99%80%20OSI%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%88%20%EC%9D%B4%EC%9C%A0.md) | 네트워킹 역사와 OSI 모델 — 계층으로 나눈 이유 (Ch1 역사·OSI·TCP/IP 개관) | 완료 |
| [01-02](./01-02.HTTP%EC%97%90%EC%84%9C%20TCP%C2%B7TLS%C2%B7UDP%EA%B9%8C%EC%A7%80%20%E2%80%94%20Transport%20%EA%B3%84%EC%B8%B5%20%ED%95%B4%EB%B6%80.md) | HTTP에서 TCP·TLS·UDP까지 — Transport 계층 해부 (Ch1 Application·Transport) | 완료 |
| [01-03](./01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) | IP·라우팅·Ethernet — 패킷이 길을 찾는 법 (Ch1 Network·Link·재조립) | 완료 |
| [01-04](./01-04.%ED%8C%A8%ED%82%B7%20%EC%BA%A1%EC%B2%98%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%201%EC%9E%A5%20%EA%B0%9C%EB%85%90%EC%9D%84%20%EB%88%88%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0.md) | 패킷 캡처 실습 — 1장 개념을 눈으로 확인하기 (Ch1 실습편) | 작성 완료·실행 전 |
| [02-01](./02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | 커널이 패킷을 다루는 법 — 소켓·Netfilter·Conntrack·라우팅 (Ch2 Basics·Kernel) | 완료 |
| [02-02](./02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) | iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술 (Ch2 High-Level Routing) | 완료 |
| [02-03](./02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) | Linux 네트워크 진단 도구 — 계층 순서대로 수사하기 (Ch2 Troubleshooting Tools) | 완료 |
| [03-01](./03-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%ED%83%84%EC%83%9D%20%E2%80%94%20%EC%95%B1%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%A7%84%ED%99%94%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C.md) | 컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브 (Ch3 Intro·Primitives·실습) | 완료 |
| [03-02](./03-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%93%9C%EC%99%80%20CNI%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EA%B1%B0%EB%9E%98.md) | 컨테이너 네트워킹 모드와 CNI — 격리와 연결의 거래 (Ch3 모드·CNM·VXLAN·CNI) | 완료 |
| [03-03](./03-03.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%97%B0%EA%B2%B0%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%2C%20%EB%8B%A4%EB%A5%B8%20%ED%98%B8%EC%8A%A4%ED%8A%B8.md) | 컨테이너 연결 실습 — 같은 호스트, 다른 호스트 (Ch3 Connectivity) | 완료 |
| [04-01](./04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) | Kubernetes 네트워킹 모델 — Pod IP·레이아웃·Probe (Ch4 Model·Kubelet·Probes) | 완료 |
| [04-02](./04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) | CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서 (Ch4 CNI·kube-proxy) | 완료 |
| [04-03](./04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) | NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름 (Ch4 Policy·DNS·Dual Stack) | 완료 |
| [05-01](./05-01.StatefulSet%C2%B7Endpoints%C2%B7EndpointSlices%20%E2%80%94%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%98%20%EC%9E%AC%EB%A3%8C.md) | StatefulSet·Endpoints·EndpointSlices — 서비스의 재료 (Ch5 앞부분) | 완료 |
| [05-02](./05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) | Service 5유형 — ClusterIP에서 LoadBalancer까지 (Ch5 Services) | 완료 |
| [05-03](./05-03.Ingress%EC%99%80%20Service%20Mesh%20%E2%80%94%20L7%EC%9D%98%20%EB%91%90%20%EC%B8%B5.md) | Ingress와 Service Mesh — L7의 두 층 (Ch5 Ingress·Service Meshes) | 완료 |
| [06-01](./06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | AWS 네트워킹과 EKS — VPC 부품으로 조립하는 클러스터 (Ch6 AWS) | 완료 |
| [06-02](./06-02.GCP%C2%B7Azure%EC%99%80%203%EC%82%AC%20%EB%B9%84%EA%B5%90%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%EB%AC%B8%EC%A0%9C%2C%20%EB%8B%A4%EB%A5%B8%20%EA%B8%B0%EB%B3%B8%EA%B0%92.md) | GCP·Azure와 3사 비교 — 같은 문제, 다른 기본값 (Ch6 GCP·Azure·비교) | 완료 |
| [00-01](./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md) | 용어집 — 핵심 용어 + 한 문장 정의 + 등장 편 (시리즈 산출물) | 완료 |
| [00-02](./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md) | 결정 치트시트 통합본 — 17편의 판단 규칙 모음 (시리즈 산출물) | 완료 |
| [00-03](./00-03.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%84%A0%EC%88%98%20%EA%B0%9C%EB%85%90.md) | 네트워크 선수 개념 — 주소·인터페이스·장비 (본문이 설명 없이 쓰는 낱말) | 초안 · Phase 1 완료(2026-08-24) |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 6/6 장 완주 — 정독 노트 17편 + 시리즈 산출물 2편(용어집·결정 치트시트) |
| 난이도 레벨 | **한 단계 더 올린다** — 01-03 Phase 1 통과(5 절 전부). 근거 둘. (1) **뿌리 (A)·(B) 모두 재발 0 건.** (A)는 질문 13 에서 "다음 홉 IP 는 표에만 있고 헤더엔 안 들어간다"를 스스로 적용, (B)는 §4 에서 첫 답에 겉봉 2 칸을 맞혔습니다(§4 회차 되묻기 2 회 → §5 보강분 1 회 → 이번엔 표기 확인만). (2) **§5 다섯 단계를 유도 없이 순서·계층까지 자력 서술** — 이 편 학습 목표의 직접 증거. 막힘 12 건은 대부분 *설계를 의심해서 나온 물음*이고, 그중 하나(ARP 메시지 입출력 방향)는 AI 표기 오류를 사용자가 잡은 것입니다. 다음 편은 정상 난이도로 진행하되 IPv6·전파 타이밍 2 건만 표적 보완 |
| 막힌 지점 | **01-03 Phase 1 12 건 — 뿌리 없이 전부 단발.** §1 두 건(IP 보장 설계의 부담 범위 / "L3 장비"=판단 층과 "L2 통신"=배달 층 혼재). §2 한 건(`/21` 자유 3 비트 경계값·가짓수). §3 일곱 건(라우팅 표 출처를 DNS 형 중앙 서버로 / 표에 MAC 을 적으면 되지 않나 / MAC·IP 중 관리자 통제값 미분화 / BGP 참여 주체를 집 공유기까지 / 경로 선택을 "빠른 쪽"으로 — BGP 는 속도를 못 본다 / eBGP·iBGP 방향 반전 / K8s 마스크 대조 세 번째 마디 오독). §4 두 건(ARP 가 프레임에 실려 선을 타고 나감 / ARP 메시지 네 칸 구조 — **이건 AI 의 사람말 표기가 방향을 흐린 것을 사용자가 잡은 경우**). §5 0 건. **뿌리 (A)(IP=배달 주체)·(B)(장비가 MAC 읽어 골라 준다) 재발 0 건 — 둘 다 해소 판정** |
| 다음 레슨 후보 | **01-04 패킷 캡처 실습(Phase 3)** — 01-02·01-03 개념 의존이 충족됐습니다. 01-04 는 상태가 `작성 완료·실행 전`이라 실제 캡처를 돌리는 회차입니다. §5 다섯 단계를 tcpdump 출력으로 대조하면 Phase 1 결론의 실물 검증이 됩니다. **표적 보완 2 건**(다음 회차에 끼워 넣기) — §2 IPv6 축(주소 길이를 늘린 배경) · §3 "광고와 전달은 다른 시간에"의 전파 타이밍. **보강 요청 2 건은 2026-08-24 완료** |
| 최근 검증 결과 | **2026-08-24 01-03 learning-session — Phase 1 통과.** 5 절 전부 커버(하위절 §1 4/4 · §2 3/4 · §3 10/10 · §4 5/5 · §5 요청 흐름), 막힘 12, 되묻기 20 회. **출구 게이트 근거는 §5** — `example.com` 요청 하나를 다섯 단계로 유도 없이 서술하고 각 단계의 계층까지 맞혔다(DNS=통신 앞 별개 절차 / 마스크 대조=L3 판단 / ARP=L2 준비 / 겉봉 재작성=L2 배달 / 보장=L4 양 끝). 스스로 도달한 결론 일곱 — (1) IP 가 보장을 포기한 이득은 **부담이 쌓이는 자리를 양 끝으로 밀어낸 것**. (2) CIDR 의 더 큰 이득은 주소 절약이 아니라 **라우팅 표 합치기**. (3) 라우팅 표에 IP 를 적는 이유는 **IP 가 관리자 통제값**이라서(MAC 은 하드웨어값 → ARP 캐시가 짧은 이유). (4) 집 공유기가 BGP 판에 없는 이유는 **통로가 아니라 끝점**이라서. (5) K8s 노드는 **자기 Pod 블록을 소유한 작은 AS**, 광고 단위가 블록이라 Pod 재생성에 무관. (6) 브로드캐스트 부담은 개별은 비례·**전체는 제곱** → VLAN 이 선택이 아니라 필수. (7) VPC 가 Pod 주소를 모르는 것은 능력이 아니라 **통제권 문제** — 수단이 열리면(AWS VPC CNI) 오버레이가 불필요. **실습 대조**: `netstat -rn` 실제 출력에서 AI 예측(기본 경로 1 줄)이 어긋나고 실제는 3 줄(활성 1 + `I` 대기 2), VPN 이 추가한 `/23` 두 줄이 §3 의 "목적지별 줄 N 개"를 실물 확인 |
| 보강 산출물 | 전체 요약 도식 13장 신설(`*.chapter-overview.svg`, svg-check 전부 PASS) · H2 요약 인용 전 절 삽입 · 원문자 본문·SVG 전수 제거 · 기존 SVG 15장 가독성 정합화(대비 경고 100→8) · 2026-08-15 `01-01.encapsulation-roundtrip` 신설 + 01-01 §3·§4 설명 빈틈 3곳 보강 · 2026-08-16~17 01-02 archify 도식 6장 + `tls-handshake.sequence` 신설, **mermaid 3 → 0**, §3·§5 중복 산문 정리, §4 캡처 줄별 주석, 비유 절 2개 · **2026-08-24 00-03 Phase 1 막힘 7건 전수 보강** — `00-03-unicast-vs-broadcast.svg` 신설, `###` 5개 신설, §4 허브 무판단성·§6 예약주소·§7 조회 주체 보강, 도식 배치 위반 5→0 · **2026-08-24 세션 후속 보강 3건** — (1) 00-03 §5 를 `### 유니캐스트와 브로드캐스트` + `### ARP` 두 하위절로 분리(ARP 정의가 산문에 묻혀 안 보인다는 지적) (2) `00-03-arp-message-fields.svg` 신설 — ARP 메시지 네 칸의 *빈 칸 → 채워짐* 대조로 입력=IP·출력=MAC 방향 명시(사용자가 방향 반전을 지적한 지점) + EtherType 이 겉봉에서 하는 역할 산문 (3) `01-03.underlay-overlay-knowledge.svg` 신설 + 01-03 §4 에 `#### 하부 네트워크와 오버레이` 신설 — 두 주소 벌·통제 주체 대조, BGP/VXLAN 판단축이 "클라우드냐"가 아니라 "경로 주입 수단이 있는가"임을 명시, AWS VPC CNI 가 방향을 뒤집어 푼 사례와 06-01 링크. 4축 센서 전수 통과(placement·compat·sentence·wall-paragraph 전부 exit 0) |
| 복습 회차 | 0 (간격 반복 `_review` 기준). 별도로 learning-session 진행 4 편 — 01-01(Phase 1·4), 01-02(Phase 1, 전체 절 커버), 00-03(Phase 1 본편 7 절 + 보강분 §5 4 논점), **01-03(Phase 1 통과, 5 절 전부)** |



## 번호 체계와 작성 규약

> 파일명·번호·작성 규약을 한곳에 모읍니다. 새 편을 더하기 전에 여기를 먼저 봅니다.

파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 책의 장 번호, `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 모든 장이 45~64쪽으로 길기 때문에 장마다 PDF 목차를 보고 분할안을 정한 뒤 작성합니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계는 Mermaid로 본문에 직접 그립니다.

작성 규약은 writing 스킬의 책 요약 템플릿과 정독 노트 세션 규약을 따릅니다. 다만 한 가지를 이 책에 맞게 바꿨습니다. "Spring 앱 개발 관점" 섹션은 매 장 필수가 아니라 **Spring 접점이 자연스러운 장에만 선별 적용**합니다(합의 2026-07-16).

이 책은 TCP/IP·Linux·CNI 같은 인프라 계층이 본체입니다. 순수 네트워킹 장에 Spring을 붙이면 연결이 억지스러워지기 때문입니다.



## 관련 문서

- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md) — 같은 `book/` 영역, 오브젝트 중심 관점의 짝
- [08_cloud/kubernetes — 개념 노트](../../kubernetes/README.md) — 개념 중복을 링크로 위임하는 대상
- `08_cloud/service-mesh` <!-- 링크 끊김(2026-08): ../../service-mesh/README.md --> — 이 책 이후 계층(L7 프록시·mTLS)을 다루는 이웃 카테고리
