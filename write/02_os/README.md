---
title: 02_os — OS 공통 기반
tags: [moc, os, linux, kernel, networking]
status: final
related:
  - ../README.md
  - ./networking/README.md
  - ./kernel/README.md
updated: 2026-04-26
---

# 02_os
---
> 언어가 아닌 실행 환경(OS·커널)에 해당하는 공통 기반을 모은다. `01_language`가 문법·생태계라면 이 카테고리는 그 아래 깔린 메커니즘이다.

상위 카테고리(K8s, 서비스 메시 등)에서 같은 OS 메커니즘이 반복 등장할 때 본 카테고리로 끌어 올려 한 곳에서만 정리한다.



## 하위 폴더

| 경로 | 범위 |
|------|------|
| [networking/](./networking/README.md) | Linux 네트워크 네임스페이스·veth·bridge·netfilter·conntrack·TC·eBPF |
| [kernel/](./kernel/README.md) | 유저/커널 스페이스, 시스템 콜, 커널 코어 영역, namespace·cgroup, /proc, K8s 노드 필수 커널 파라미터 |



## 카테고리 결정 원칙

- 커널 네트워크 자료구조(netns, veth, conntrack, netfilter) → `networking/`
- 컨테이너 런타임 격리·자원 제한(namespace, cgroup, seccomp) → `kernel/`
- 시스템 콜 인터페이스, /proc, VFS, 메모리 관리 → `kernel/`
- 컨테이너 이미지 포맷·OCI 표준 같은 빌드 측면은 `07_devops/`에 둔다 (런타임 측면이 아니므로 본 카테고리 아님)



## 관련 문서

- [write/ MOC](../README.md) — 전체 카테고리 지도
- [08_cloud/kubernetes/](../08_cloud/kubernetes/README.md) — 본 카테고리의 활용처
