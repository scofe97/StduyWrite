---
title: 02_os/networking — Linux 네트워킹
tags: [moc, linux, networking, namespace, netfilter, ebpf, conntrack]
status: final
related:
  - ../../roadmap/network-roadmap.md
  - ../README.md
  - ../kernel/README.md
  - ../../08_cloud/kubernetes/README.md
updated: 2026-09-12
---

# 02_os/networking
---

> Linux 네트워크 원리와 Kubernetes 패킷 경로를 다룹니다. 전체 학습 순서와 실습은 [통합 네트워크 로드맵](../../roadmap/network-roadmap.md)에서 확인합니다.

## 문서

> netns·veth·routing·netfilter·conntrack에서 DNS와 주소 설계까지 연결합니다.

| Ch | 제목 | 핵심 질문 |
|---|---|---|
| 01-01 | [네트워킹 기초](./01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EA%B8%B0%EC%B4%88.md) | netns·veth·bridge·routing·netfilter·conntrack·TC·eBPF는 어떻게 협력합니까? |
| 01-02 | [K8s 패킷 여정](./01-02.K8s%20%ED%8C%A8%ED%82%B7%20%EC%97%AC%EC%A0%95%20%E2%80%94%20netfilter%C2%B7conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | Pod에서 Service까지 패킷이 커널을 어떻게 통과합니까? |
| 01-03 | [DNS 필터링 차단](./01-03.DNS%20%ED%95%84%ED%84%B0%EB%A7%81%20%EC%B0%A8%EB%8B%A8%20%E2%80%94%20NXDOMAIN%C2%B7DoH%C2%B7%EC%9A%B0%ED%9A%8C%20%EB%A7%88%EC%B0%B0.md) | NXDOMAIN·DoH는 DNS 차단과 우회에 어떻게 작용합니까? |
| 01-04 | [서브네팅과 CIDR](./01-04.%EC%84%9C%EB%B8%8C%EB%84%A4%ED%8C%85%EA%B3%BC%20CIDR%20%E2%80%94%20%EC%A3%BC%EC%86%8C%20%EA%B3%B5%EA%B0%84%EC%9D%84%20%EC%9E%90%EB%A5%B4%EB%8A%94%20%EB%B2%95.md) | VPC·Pod·Service 대역은 왜 겹치면 안 됩니까? |



## 이어서 읽기

> 커널 일반 메커니즘과 Kubernetes 구현을 양쪽에서 확장합니다.

| 방향 | 문서 |
|---|---|
| 커널 | [02_os/kernel](../kernel/README.md) |
| Kubernetes | [08_cloud/kubernetes](../../08_cloud/kubernetes/README.md) |
| 전체 순서 | [네트워크 학습 로드맵](../../roadmap/network-roadmap.md) |
