---
title: 02_os — OS 공통 기반
tags: [moc, os, linux, kernel, networking]
status: final
related:
  - ../README.md
  - ./networking/README.md
  - ./kernel/README.md
  - ./linux-kernel-programming/README.md
  - ./container-security/README.md
updated: 2026-06-03
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
| [linux-kernel-programming/](./linux-kernel-programming/README.md) | 커널 개발자 관점의 리눅스 내부 — LKM 모듈 개발, 커널 빌드, 메모리 관리, CPU 스케줄러, 동기화 (책 기반) |
| [container-security/](./container-security/README.md) | 보안 관점의 컨테이너 — 커널 기초(namespace·cgroup·root 변경) 위의 이미지·공급망·런타임·통신 보안 (책 기반) |
| [systems-performance/](./systems-performance/README.md) | 성능 분석가 관점의 시스템 성능 — 방법론·CPU·메모리·디스크·네트워크·클라우드·고급 추적(perf·Ftrace·BPF) (책 기반) |



## 카테고리 결정 원칙

- 커널 네트워크 자료구조(netns, veth, conntrack, netfilter) → `networking/`
- 컨테이너 런타임 격리·자원 제한(namespace, cgroup, seccomp) → `kernel/`
- 시스템 콜 인터페이스, /proc, VFS, 메모리 관리 → `kernel/` (K8s 운영자 관점) 또는 `linux-kernel-programming/` (커널 모듈 작성자 관점)
- 커널 모듈(LKM) 개발, 커널 소스 빌드, 메모리 할당 API, 스케줄러·동기화 내부 → `linux-kernel-programming/`
- 컨테이너 이미지 포맷·OCI 표준 같은 빌드 측면은 `07_devops/`에 둔다 (런타임 측면이 아니므로 본 카테고리 아님)
- 컨테이너 보안(격리 메커니즘을 보안 관점에서 보기, 이미지·공급망·런타임 위협) → `container-security/`. namespace·cgroup 같은 메커니즘 자체는 `kernel/`이 SSOT이고 교차참조한다
- 시스템 성능 분석(방법론·병목 진단, CPU·메모리·디스크·네트워크 성능, perf·Ftrace·BPF 추적) → `systems-performance/`. 커널 메커니즘 자체는 `linux-kernel-programming/`·`kernel/`이 SSOT이고 "성능 관점"으로 교차참조한다. LGTM 스택·SLO 같은 앱·인프라 관측 운영은 `06_observability/` 소관이라 본 폴더 아님

> `kernel/`과 `linux-kernel-programming/`은 둘 다 커널을 다루지만 시선이 다르다. 전자는 "K8s가 cgroup 파일을 어떻게 쓰는가"(운영자), 후자는 "모듈에서 커널 메모리를 어떻게 할당하는가"(개발자) 관점이다. 같은 메커니즘이 양쪽에 나오면 교차참조한다.



## 관련 문서

- [write/ MOC](../README.md) — 전체 카테고리 지도
- [08_cloud/kubernetes/](../08_cloud/kubernetes/README.md) — 본 카테고리의 활용처
