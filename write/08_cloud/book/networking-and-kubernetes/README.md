---
title: Networking and Kubernetes — 정독 인덱스
tags: [moc, study-index, book, kubernetes, networking, linux-networking, cni, kube-proxy]
status: draft
source:
  - 《Networking and Kubernetes: A Layered Approach》(James Strong·Vallery Lancey, O'Reilly, 2021, ISBN 978-1492081654)
  - https://www.amazon.com/Networking-Kubernetes-Approach-James-Strong/dp/1492081655  # 서지 확인 (2026-07-16 조회)
related:
  - ../kubernetes-in-action/README.md
  - ../container-security/README.md
  - ../cilium-up-and-running/README.md
  - ../istio-in-action/README.md
  - ../../../_archive/08_cloud/kubernetes/README.md
  - ../../README.md
learning:
  topic: networking-and-kubernetes
  scope: durable
  level: 정상
  last_verified: 2026-09-23
  blocked_count: 2
  next_lesson: "4장 Phase 4 묶음 8 표적 재확인 대기(2026-09-08). 통과 후 3장 03-04 실습 연결 재확인, 1·2장 복습 3회차 진행(_review/_queue.md 참조)."
updated: 2026-11-29
---

# Networking and Kubernetes — 정독 인덱스

---

> 『Networking and Kubernetes: A Layered Approach』(James Strong·Vallery Lancey, O'Reilly, 2021)를 장 단위로 정독한 책-종속 학습노트입니다. TCP/IP와 Linux 커널 네트워킹에서 출발해 컨테이너·CNI·Service·Ingress·클라우드 관리형 K8s까지 계층 순서대로 다룹니다.

## 작성 현황

> 1~6장 정독·실습 노트 23편과 시리즈 보조 문서 4편(총 27편)의 목록입니다.

| 편 | 제목과 한 줄 요약 | 상태 |
|----|------------------|------|
| [00-01](./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md) | 용어집 — 1~6장 핵심 용어 한 문장 정의와 등장 편 | 완료 |
| [00-02](./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md) | 결정 치트시트 — 본문 17편의 판단 규칙 통합본 | 완료 |
| [00-03](./00-03.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%84%A0%EC%88%98%20%EA%B0%9C%EB%85%90.md) | 네트워크 선수 개념 — MAC·IP·포트·인터페이스·장비·ARP·DNS 기초 | 초안 (Phase 1 완료) |
| [오답 노트](./_mistakes.md) | 복습 회차에서 막힌 문항과 원인 기록 | 진행 중 |
| [01-01](./01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%97%AD%EC%82%AC%EC%99%80%20OSI%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%88%20%EC%9D%B4%EC%9C%A0.md) | 네트워킹 역사와 OSI 모델 — NCP·OSI·TCP/IP 계층과 예제 Go 웹 서버 | 완료 |
| [01-02](./01-02.HTTP%EC%97%90%EC%84%9C%20TCP%C2%B7TLS%C2%B7UDP%EA%B9%8C%EC%A7%80%20%E2%80%94%20Transport%20%EA%B3%84%EC%B8%B5%20%ED%95%B4%EB%B6%80.md) | HTTP에서 TCP·TLS·UDP까지 — 3·4-way 핸드셰이크·TIME-WAIT·TLS·UDP | 완료 (draft) |
| [01-03](./01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) | IP·라우팅·Ethernet — CIDR·BGP·ARP·L2 전달과 패킷 재조립 | 완료 |
| [01-04](./01-04.%ED%8C%A8%ED%82%B7%20%EC%BA%A1%EC%B2%98%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%201%EC%9E%A5%20%EA%B0%9C%EB%85%90%EC%9D%84%20%EB%88%88%EC%9C%BC%EB%A1%9C%20%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0.md) | 패킷 캡처 실습 — 루프백·ARP·상태 기계·TLS·eBGP·iBGP 확인 | 부분 실행 (§1·§4·§5 dig·§6 실측) |
| [02-01](./02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%20%EC%9E%90%EB%A6%AC%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80.md) | 커널이 패킷을 주고받는 자리 — 소켓·인터페이스·netns·veth·브리지 | 완료 (draft) |
| [02-02](./02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | 커널이 패킷을 판정하는 층 — Netfilter 5훅·Conntrack·라우팅 | 완료 (draft) |
| [02-03](./02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) | iptables·IPVS·eBPF — 규칙 평가·Service NAT·해시 조회·BPF 검증 | 완료 |
| [02-04](./02-04.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) | Linux 네트워크 진단 도구 — ping·dig·ss·nmap 계층별 수사 순서 | 완료 |
| [02-05](./02-05.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) | 커널 네트워킹 실습 — netns·veth·브리지·포워딩·conntrack 실측 | 실행 완료 (검증 전) |
| [02-06](./02-06.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%202%20%E2%80%94%20%EB%A7%89%EA%B3%A0%2C%20%EC%A7%84%EB%8B%A8%ED%95%98%EA%B3%A0%2C%20%EB%82%98%EB%88%84%EA%B8%B0.md) | 커널 네트워킹 실습 2 — DROP·REJECT·진단 사다리·확률 사다리 실측 | 실행 완료 (검증 전) |
| [03-01](./03-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%ED%83%84%EC%83%9D%20%E2%80%94%20%EC%95%B1%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%A7%84%ED%99%94%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C.md) | 컨테이너의 탄생 — 런타임 계보·cgroup·namespace·맨손 배선 개념 | 완료 |
| [03-02](./03-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%93%9C%EC%99%80%20CNI%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EA%B1%B0%EB%9E%98.md) | 컨테이너 네트워킹 모드와 CNI — 7가지 모드·CNM·VXLAN·CNI 비교 | 완료 |
| [03-03](./03-03.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%2C%20%EB%8B%A4%EB%A5%B8%20%ED%98%B8%EC%8A%A4%ED%8A%B8.md) | 컨테이너 연결과 포트 매핑 — multistage 빌드·같은·다른 호스트 접근 | 완료 |
| [03-04](./03-04.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EB%A7%A8%EC%86%90%20%EB%B0%B0%EC%84%A0%EC%97%90%EC%84%9C%20%ED%8F%AC%ED%8A%B8%20%EB%A7%A4%ED%95%91%EA%B9%8C%EC%A7%80.md) | 컨테이너 네트워크 실습 — Docker 배선·이미지·포트 매핑 실측 | 실행 완료 (묶음 2~5 완료·1 제외) |
| [04-01](./04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) | Kubernetes 네트워킹 모델 — Pod IP·레이아웃 3종·CIDR·Probe (v1.37) | 완료 |
| [04-02](./04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) | CNI와 kube-proxy — CNI 명세·4대 CNI·kube-proxy 모드·경로 대조 (v1.37) | 완료 |
| [04-03](./04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) | NetworkPolicy와 DNS — 선택-잠금·정책 문법·ndots·이중 스택 (v1.37) | 완료 |
| [04-04](./04-04.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20CNI%20%EB%B6%80%EC%9E%AC%EB%B6%80%ED%84%B0%20%EC%A0%95%EC%B1%85%C2%B7DNS%EA%B9%8C%EC%A7%80.md) | Kubernetes 네트워크 실습 — CNI 부재·규칙·정책·DNS·외부 경로 (kind v0.33) | 실행 완료 (재실행 완료·묶음 8 재확인 대기) |
| [05-01](./05-01.StatefulSet%C2%B7Endpoints%C2%B7EndpointSlices%20%E2%80%94%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%98%20%EC%9E%AC%EB%A3%8C.md) | StatefulSet·Endpoints·EndpointSlices — 고정 이름과 엔드포인트 분할 | 완료 |
| [05-02](./05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) | Service 5유형 — ClusterIP·NodePort·Headless·ExternalName·LoadBalancer | 완료 |
| [05-03](./05-03.Ingress%EC%99%80%20Service%20Mesh%20%E2%80%94%20L7%EC%9D%98%20%EB%91%90%20%EC%B8%B5.md) | Ingress와 Service Mesh — L7 진입 라우팅·프록시와 메시 분리 | 완료 |
| [06-01](./06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | AWS 네트워킹과 EKS — VPC·보안 그룹·ELB·AWS VPC CNI·ALB | 완료 |
| [06-02](./06-02.GCP%C2%B7Azure%EC%99%80%203%EC%82%AC%20%EB%B9%84%EA%B5%90%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%EB%AC%B8%EC%A0%9C%2C%20%EB%8B%A4%EB%A5%B8%20%EA%B8%B0%EB%B3%B8%EA%B0%92.md) | GCP·Azure와 3사 비교 — GKE·NEG·AKS와 클라우드별 기본값 | 완료 |

- 원서 밖 보강 단락은 본문에 `> 원서 밖 보강입니다`로 표시해 원서 대조 범위와 구분합니다.
- 4장 네 편(04-01~04-04)은 2026-11-08에 Kubernetes v1.37 기준으로 다시 정리했습니다.



## 학습 상태

> 세션을 열 때 현재 진행 위치만 빠르게 확인하는 요약입니다. 챕터별 복습 회차 정본은 복습 대기 큐에 있습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 6/6장 완주 — 장별 노트 23편(이론 18 · 실습 5) + 보조 문서 4편(용어집 · 결정 치트시트 · 선수 개념 · 오답 노트) |
| 현재 상태 | 난이도 `정상` (2026-09-23 기준). 1·2장 복습 2회차 진행 중, 3·4장 Phase 4 게이트(3장 `03-04` 실습 연결 · 4장 `04-04` 묶음 8 표적 재확인 대기), 5·6장 Phase 4 미실시 |
| 실습 코드 | `~/study/runners-lab/k8s/networking-and-kubernetes/` (`bgp/` · `netns-bridge/`) |
| 복습·오답 | [복습 대기 큐](../../../_review/_queue.md) (`nak` ch00~ch06) · [오답 노트](./_mistakes.md) |



## 질문별 정본

> 리눅스·Kubernetes 네트워킹 질문이 떠오르면 왼쪽에서 찾아 오른쪽 편의 해당 절로 갑니다. 이 책 밖의 편도 섞여 있습니다.

| 질문 | 정본 |
|---|---|
| 네트워크 네임스페이스는 커널에서 무엇이고, 왜 포트가 겹쳐도 되는가 | [N&K 02-01](./02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%20%EC%9E%90%EB%A6%AC%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80.md) §3 |
| veth 는 패킷을 어떻게 넘기고, 브리지는 MAC 을 어떻게 배우는가 | [N&K 02-01](./02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%20%EC%9E%90%EB%A6%AC%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80.md) §4 |
| netns·veth·브리지를 손으로 지어 보려면 | [N&K 02-05](./02-05.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) |
| 라우팅 테이블은 어떻게 고르고, 다음 홉의 MAC 은 어디서 오는가(NUD) | [N&K 02-02](./02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §3 |
| netfilter 다섯 훅과 iptables 테이블·체인은 어떻게 맞물리는가 | [N&K 02-02](./02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §1 · [02-03](./02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §1~2 |
| DNAT·SNAT·MASQUERADE 는 무엇을 바꾸는가 | [N&K 02-03](./02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §3 |
| conntrack 은 무엇을 적고, UDP 는 왜 테이블을 먼저 채우는가 | [N&K 02-02](./02-02.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%ED%8C%90%EC%A0%95%ED%95%98%EB%8A%94%20%EC%B8%B5%20%E2%80%94%20Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §2 |
| TC·qdisc 와 eBPF 어태치 지점은 성능을 어떻게 가르는가 | [N&K 02-03](./02-03.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §5 |
| kube-proxy 모드는 무엇이 다른가 | [N&K 04-02](./04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) §3 |
| CNI 는 Pod 에 무엇을 배선하고, Calico 노드에서는 무엇부터 보는가 | [N&K 04-02](./04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) §1~2 |
| NodePort 로 들어온 클라이언트 IP 는 왜 사라지는가 | [N&K 05-02](./05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) §3 |
| 패킷이 안 갈 때 커널 안 어디서 멈췄는지 좁히려면 | [N&K 02-04](./02-04.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) §6 |
| 서브네팅·CIDR·VLSM 을 손으로 계산하려면 | [N&K 01-03](./01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) §2 · [cntd 04-03](../../../02_os/book/cntd_computer-networking-top-down/04-03.IP%20%E2%80%94%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8%EA%B3%BC%20%EC%A3%BC%EC%86%8C.md) |
| VPC·Pod·Service 대역은 왜 겹치면 안 되는가 | [N&K 04-01](./04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) §3 |
| DNS 로 사이트를 어떻게 막고, 브라우저 DoH 는 왜 그 차단을 건너뛰는가 | [Learning CoreDNS 07-01](../learning-coredns/07-01.%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%EC%9D%B4%20%EC%96%B4%EA%B8%8B%EB%82%98%EB%A9%B4%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EB%B2%84%EB%A6%B0%EB%8B%A4.md) §9 · [패킷 분석 05-02](../../../02_os/book/paw_packet-analysis-wireshark/05-02.%EC%9D%B4%EB%A6%84%EA%B3%BC%20%EC%9A%94%EC%B2%AD.md) §1 |



## 관련 문서

> 같은 book/ 영역의 형제 정독본과 상위 인덱스입니다.

- [Kubernetes in Action 정독 인덱스](../kubernetes-in-action/README.md) — 오브젝트 중심 관점의 짝
- [Container Security 정독 인덱스](../container-security/README.md) — 격리 경계와 보안 관점
- [Cilium: Up and Running 정독 인덱스](../cilium-up-and-running/README.md) — eBPF 데이터패스와 CNI 심화
- [Istio in Action 정독 인덱스](../istio-in-action/README.md) — L7 프록시와 mTLS 서비스 메시 계층
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계
- [_archive/08_cloud/kubernetes](../../../_archive/08_cloud/kubernetes/README.md) — 이전 쿠버네티스 개념 노트 아카이브
