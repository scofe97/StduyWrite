---
title: 02_os — OS 공통 기반
tags: [moc, os, linux, kernel, networking]
status: final
related:
  - ../README.md
  - ./roadmap.md
  - ./networking/README.md
  - ./troubleshooting/README.md
  - ./kernel/README.md
  - ./book/linux-kernel-programming/README.md
  - ./book/systems-performance/README.md
  - ../08_cloud/book/container-security/README.md
  - ../08_cloud/book/learning-coredns/README.md
updated: 2026-09-05
---

# 02_os
---
> 언어가 아닌 실행 환경(OS·커널)에 해당하는 공통 기반을 모은다. `01_language`가 문법·생태계라면 이 카테고리는 그 아래 깔린 메커니즘이다.

상위 카테고리(K8s, 서비스 메시 등)에서 같은 OS 메커니즘이 반복 등장할 때 본 카테고리로 끌어 올려 한 곳에서만 정리한다.

처음에는 [통합 학습 로드맵](./roadmap.md)을 읽습니다. 문서가 많은 순서가 아니라, 운영 장애를 실행 모델·자원·네트워크·성능·보안으로 분해하는 순서로 연결합니다.



## 하위 폴더

| 경로 | 범위 |
|------|------|
| [roadmap.md](./roadmap.md) | 백엔드·Kubernetes 운영자가 OS 문제를 해석하는 통합 학습 순서 |
| [networking/](./networking/README.md) | Linux 네트워크 네임스페이스·veth·bridge·netfilter·conntrack·TC·eBPF |
| [kernel/](./kernel/README.md) | 유저/커널 스페이스, 시스템 콜, 커널 코어 영역, namespace·cgroup, /proc, K8s 노드 필수 커널 파라미터 |
| [troubleshooting/](./troubleshooting/README.md) | 증상에서 원인으로 역추적하는 장애 사례집 — 디스크·프로세스·자원·서비스 가용성·로그·네트워크 |
| [linux-kernel-programming/](./book/linux-kernel-programming/README.md) | 커널 개발자 관점의 리눅스 내부 — LKM 모듈 개발, 커널 빌드, 메모리 관리, CPU 스케줄러, 동기화 (책 기반) |
| [container-security/](../08_cloud/book/container-security/README.md) | 보안 관점의 컨테이너 — 커널 기초(namespace·cgroup·root 변경) 위의 이미지·공급망·런타임·통신 보안 (책 기반) |
| [learning-coredns/](../08_cloud/book/learning-coredns/README.md) | 이름 해석의 *서버* 편 — Corefile·플러그인 체인·존 데이터·쿠버네티스 연동. `networking/`이 맡는 resolver 클라이언트 측과 편을 나눠 가진다 (책 기반) |
| [systems-performance/](./book/systems-performance/README.md) | 성능 분석가 관점의 시스템 성능 — 방법론·CPU·메모리·디스크·네트워크·클라우드·고급 추적(perf·Ftrace·BPF) (책 기반) |



## 카테고리 결정 원칙

- 커널 네트워크 자료구조(netns, veth, conntrack, netfilter) → `networking/`
- 컨테이너 런타임 격리·자원 제한(namespace, cgroup, seccomp) → `kernel/`
- 시스템 콜 인터페이스, /proc, VFS, 메모리 관리 → `kernel/` (K8s 운영자 관점) 또는 `linux-kernel-programming/` (커널 모듈 작성자 관점)
- 커널 모듈(LKM) 개발, 커널 소스 빌드, 메모리 할당 API, 스케줄러·동기화 내부 → `linux-kernel-programming/`
- 컨테이너 이미지 포맷·OCI 표준 같은 빌드 측면은 `07_devops/`에 둔다 (런타임 측면이 아니므로 본 카테고리 아님)
- 컨테이너 보안(격리 메커니즘을 보안 관점에서 보기, 이미지·공급망·런타임 위협) → `container-security/`. namespace·cgroup 같은 메커니즘 자체는 `kernel/`이 SSOT이고 교차참조한다
- DNS 는 방향으로 가른다. 질의를 *보내는* 쪽(`/etc/resolv.conf`·ndots·search domain·glibc resolver)은 `networking/` 이 SSOT 이고, 질의를 *받는* 쪽(Corefile·플러그인·존 데이터)은 `learning-coredns/` 가 맡는다
- 증상에서 출발해 원인을 역추적하는 진단 문서(디스크가 찼다, 포트가 안 열린다, 패킷이 사라진다) → `troubleshooting/`. 같은 주제라도 메커니즘을 설명하는 쪽은 `networking/`·`kernel/`이 SSOT이고, 사례집은 그것을 교차참조한다
- 시스템 성능 분석(방법론·병목 진단, CPU·메모리·디스크·네트워크 성능, perf·Ftrace·BPF 추적) → `systems-performance/`. 커널 메커니즘 자체는 `linux-kernel-programming/`·`kernel/`이 SSOT이고 "성능 관점"으로 교차참조한다. LGTM 스택·SLO 같은 앱·인프라 관측 운영은 `06_observability/` 소관이라 본 폴더 아님

> `kernel/`과 `linux-kernel-programming/`은 둘 다 커널을 다루지만 시선이 다르다. 전자는 "K8s가 cgroup 파일을 어떻게 쓰는가"(운영자), 후자는 "모듈에서 커널 메모리를 어떻게 할당하는가"(개발자) 관점이다. 같은 메커니즘이 양쪽에 나오면 교차참조한다.

## 추천 읽기 경로

백엔드·Kubernetes 운영자는 `roadmap.md`의 1~4단계를 먼저 따릅니다. OOMKilled·CPU throttling·Pod 격리는 `kernel/`, DNS·Service·NAT 문제는 `networking/`, 성능 병목은 `book/systems-performance/`으로 확장합니다.

커널 모듈 작성이나 커널 소스 자체가 목적일 때만 `book/linux-kernel-programming/`을 별도 정독합니다. 컨테이너 보안 옵션과 공급망 위험을 판단하려면 1~2단계 뒤 `book/container-security/`으로 이동합니다.



## 관련 문서

- [통합 학습 로드맵](./roadmap.md) — OS 전체를 가로지르는 추천 순서
- [write/ MOC](../README.md) — 전체 카테고리 지도
- [08_cloud/kubernetes/](../08_cloud/kubernetes/README.md) — 본 카테고리의 활용처
