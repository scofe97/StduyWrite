---
title: 02_os/networking — Linux 네트워킹
tags: [moc, linux, networking, namespace, netfilter, ebpf, conntrack]
status: final
related:
  - roadmap.md
  - ../README.md
  - ../kernel/README.md
  - ../../08_cloud/kubernetes/README.md
updated: 2026-04-26
---

# 02_os/networking
---
> Linux 커널이 제공하는 네트워크 자료구조와 hook 중 Kubernetes·컨테이너·서비스 메시에서 반복 등장하는 것들을 한 곳에 정리한다. K8s 카테고리에서 다루기에는 깊고, OS 일반 지식으로 두기에는 K8s 디버깅에 직접 쓰이는 주제만 추린다.

> OS 네트워크 딥다이브 로드맵의 **섹션별 키워드 전체**(socket·TCP state·routing·netfilter·conntrack·namespace·veth·bridge·NAT·packet capture 등 20주제)는 [roadmap.md](roadmap.md)에 원문 그대로 정리해 두었다. 아래 "문서"가 *이미 작성된 본문*이라면, roadmap.md는 *다뤄야 할 전체 범위*의 SSOT다 — 중심은 Linux OS 네트워크 원리, Kubernetes는 적용 사례·디버깅 대상으로만 연결한다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [네트워킹 기초](./01-01.네트워킹%20기초.md) | netns·veth·bridge·라우팅·netfilter·conntrack·TC·eBPF는 K8s 추상 아래에서 어떻게 협력하는가? |



## 상위·이웃·활용처

- 상위: [02_os/ MOC](../README.md)
- 이웃: [02_os/kernel/](../kernel/README.md) — 커널 일반 메커니즘(시스템 콜·namespace·cgroup·/proc)
- 활용처: [08_cloud/kubernetes/](../../08_cloud/kubernetes/README.md), [08_cloud/service-mesh/](../../08_cloud/service-mesh/README.md)
