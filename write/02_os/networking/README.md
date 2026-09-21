---
title: 02_os/networking — 리눅스 네트워킹 라우팅표
tags: [moc, linux, networking, routing-table]
status: final
related:
  - ../../roadmap/network-roadmap.md
  - ../README.md
  - ../kernel/README.md
  - ../../08_cloud/book/networking-and-kubernetes/README.md
  - ../../08_cloud/kubernetes/README.md
updated: 2026-09-21
---

# 02_os/networking
---

> 리눅스·Kubernetes 네트워킹 질문을 정본 편으로 보내는 라우팅표입니다. 메커니즘 본문은 이 폴더에 없고, 질문마다 답하는 편과 절을 가리킵니다.

## 질문별 정본

> 왼쪽 질문이 떠오르면 오른쪽 편의 해당 절로 갑니다.

| 질문 | 정본 |
|---|---|
| 네트워크 네임스페이스는 커널에서 무엇이고, 왜 포트가 겹쳐도 되는가 | [N&K 02-01](../../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §3 |
| veth 는 패킷을 어떻게 넘기고, 브리지는 MAC 을 어떻게 배우는가 | [N&K 02-01](../../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §3 |
| netns·veth·브리지를 손으로 지어 보려면 | [N&K 02-04](../../08_cloud/book/networking-and-kubernetes/02-04.%EC%BB%A4%EB%84%90%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20veth%C2%B7%EB%B8%8C%EB%A6%AC%EC%A7%80%C2%B7%ED%8F%AC%EC%9B%8C%EB%94%A9%EC%9D%84%20%EC%86%90%EC%9C%BC%EB%A1%9C%20%EC%A7%93%EA%B8%B0.md) |
| 라우팅 테이블은 어떻게 고르고, 다음 홉의 MAC 은 어디서 오는가(NUD) | [N&K 02-01](../../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §6 |
| netfilter 다섯 훅과 iptables 테이블·체인은 어떻게 맞물리는가 | [N&K 02-01](../../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §4 · [02-02](../../08_cloud/book/networking-and-kubernetes/02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §1~2 |
| DNAT·SNAT·MASQUERADE 는 무엇을 바꾸는가 | [N&K 02-02](../../08_cloud/book/networking-and-kubernetes/02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §3 |
| conntrack 은 무엇을 적고, UDP 는 왜 테이블을 먼저 채우는가 | [N&K 02-01](../../08_cloud/book/networking-and-kubernetes/02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) §5 |
| TC·qdisc 와 eBPF 어태치 지점은 성능을 어떻게 가르는가 | [N&K 02-02](../../08_cloud/book/networking-and-kubernetes/02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) §5 |
| kube-proxy 모드는 무엇이 다른가 | [N&K 04-02](../../08_cloud/book/networking-and-kubernetes/04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) §4 |
| CNI 는 Pod 에 무엇을 배선하고, Calico 노드에서는 무엇부터 보는가 | [N&K 04-02](../../08_cloud/book/networking-and-kubernetes/04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) §1~5 |
| NodePort 로 들어온 클라이언트 IP 는 왜 사라지는가 | [N&K 05-02](../../08_cloud/book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) §3 |
| 패킷이 안 갈 때 커널 안 어디서 멈췄는지 좁히려면 | [N&K 02-03](../../08_cloud/book/networking-and-kubernetes/02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) §6 |
| 서브네팅·CIDR·VLSM 을 손으로 계산하려면 | [N&K 01-03](../../08_cloud/book/networking-and-kubernetes/01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) §2 · [cntd 04-03](../book/cntd_computer-networking-top-down/04-03.IP%20%E2%80%94%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8%EA%B3%BC%20%EC%A3%BC%EC%86%8C.md) |
| VPC·Pod·Service 대역은 왜 겹치면 안 되는가 | [N&K 04-01](../../08_cloud/book/networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) §3 |

이 폴더에 본문이 남아 있는 편은 하나입니다. [01-03](./01-03.DNS%20%ED%95%84%ED%84%B0%EB%A7%81%20%EC%B0%A8%EB%8B%A8%20%E2%80%94%20NXDOMAIN%C2%B7DoH%C2%B7%EC%9A%B0%ED%9A%8C%20%EB%A7%88%EC%B0%B0.md) DNS 필터링 차단은 NXDOMAIN 으로 이름 해석을 막는 필터링과 DoH 우회를 다루며, 책 어디에도 같은 각도가 없어 여기에 둡니다.



## 이 폴더가 얇아진 이유

> 같은 개념이 두 곳에 살던 것을 한 곳으로 합쳤습니다.

2026-09-21 까지 이 폴더에는 네트워킹 기초·K8s 패킷 여정·서브네팅과 CIDR 세 편이 있었습니다. 강의 트랜스크립트와 RFC 를 근거로 먼저 쓴 편들인데, 뒤이어 채운 《Networking and Kubernetes》 정독본이 같은 주제를 실습까지 붙여 더 깊게 다루게 됐습니다. 두 곳을 함께 유지하면 한쪽을 고칠 때 다른 쪽이 낡으므로, 책에 없던 내용만 골라 정독본 본문으로 옮기고 세 편을 걷어냈습니다.

옮긴 단락에는 착지한 자리마다 "원서 밖 보강" 표기와 출처를 달아 두었습니다. 정독본을 원서와 대조할 때 그 단락이 원서에 없다는 사실이 바로 드러나게 하려는 것입니다.



## 이어서 읽기

> 커널 일반 메커니즘과 Kubernetes 구현을 양쪽에서 확장합니다.

| 방향 | 문서 |
|---|---|
| 커널 | [02_os/kernel](../kernel/README.md) |
| 네트워크 정본 | [Networking and Kubernetes 정독본](../../08_cloud/book/networking-and-kubernetes/README.md) |
| Kubernetes | [08_cloud/kubernetes](../../08_cloud/kubernetes/README.md) |
| 전체 순서 | [네트워크 학습 로드맵](../../roadmap/network-roadmap.md) |
