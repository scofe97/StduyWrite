---
title: 02_os/networking — Linux 네트워킹
tags: [moc, linux, networking, namespace, netfilter, ebpf, conntrack]
status: final
related:
  - ../README.md
  - ../kernel/README.md
  - ../../08_cloud/kubernetes/README.md
updated: 2026-04-26
---

# 02_os/networking
---
> Linux 커널이 제공하는 네트워크 자료구조와 hook 중 Kubernetes·컨테이너·서비스 메시에서 반복 등장하는 것들을 한 곳에 정리한다. K8s 카테고리에서 다루기에는 깊고, OS 일반 지식으로 두기에는 K8s 디버깅에 직접 쓰이는 주제만 추린다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [네트워킹 기초](./01-01.네트워킹%20기초.md) | netns·veth·bridge·라우팅·netfilter·conntrack·TC·eBPF는 K8s 추상 아래에서 어떻게 협력하는가? |



## 상위·이웃·활용처

- 상위: [02_os/ MOC](../README.md)
- 이웃: [02_os/kernel/](../kernel/README.md) — 커널 일반 메커니즘(시스템 콜·namespace·cgroup·/proc)
- 활용처: [08_cloud/kubernetes/](../../08_cloud/kubernetes/README.md), [08_cloud/service-mesh/](../../08_cloud/service-mesh/README.md)
