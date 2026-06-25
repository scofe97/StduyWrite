---
title: 02_os/kernel — 커널과 컨테이너
tags: [moc, linux, kernel, syscall, namespace, cgroup, proc, runtime]
status: final
related:
  - roadmap.md
  - ../README.md
  - ../networking/README.md
  - ../../08_cloud/kubernetes/README.md
updated: 2026-04-26
---

# 02_os/kernel
---
> Linux 커널이 컨테이너 동작에서 맡는 책임을 정리한다. 유저/커널 스페이스 분리, 시스템 콜, 커널 코어 영역, namespace·cgroup, /proc, K8s 노드 필수 커널 파라미터까지 — 네트워크 영역은 별도 `networking/`에서 다루고 본 폴더는 그 외 커널 일반 메커니즘에 집중한다.

> OS Kernel 딥다이브 로드맵의 **섹션별 키워드 전체**(Process/Thread·System Call·CPU Scheduling·Memory·OOM Killer·Cgroup·Namespace·FD·VFS/OverlayFS·Disk I/O·Socket·Futex·Kernel Security·관측 14주제)는 [roadmap.md](roadmap.md)에 원문 그대로 정리해 두었다. 아래 "문서"가 *이미 작성된 본문*이라면, roadmap.md는 *다뤄야 할 전체 범위*의 SSOT다 — 중심은 Linux Kernel 원리, Kubernetes는 그 위에서 보이는 OOMKilled·CPU throttling·FD 고갈 같은 현상을 해석하는 적용처로만 연결한다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [커널과 컨테이너](./01-01.커널과%20컨테이너.md) | 유저/커널 스페이스 분리, 시스템 콜, 코어 7대 영역, namespace/cgroup, /proc, K8s 노드 필수 커널 파라미터, runc create 시퀀스는 어떻게 컨테이너 동작을 만드는가? |
| 01-02 | [cgroup v2 깊이](./01-02.cgroup%20v2%20깊이.md) | 단일 트리·컨트롤러·PSI·kubepods.slice·throttling/OOM 분석은 cgroup 파일에서 어떻게 읽는가? |
| 01-03 | [마운트 네임스페이스와 propagation](./01-03.마운트%20네임스페이스와%20propagation.md) | private/shared/slave/unbindable 4종과 K8s `mountPropagation` 옵션은 CSI·HostPath 사고를 어떻게 결정하는가? |
| 01-04 | [cgroup 파일시스템 실습](./01-04.cgroup%20파일시스템%20실습.md) | `/sys/fs/cgroup` 트리에서 Pod별 디렉토리를 찾아 `memory.max`·`cpu.max`와 K8s `requests`/`limits`를 어떻게 매핑하는가? |
| 01-05 | [namespace 실습 — 8가지 격리와 unshare](./01-05.namespace%20실습%20—%208가지%20격리와%20unshare.md) | `unshare`로 PID·UTS·MNT·NET 격리를 직접 만들고 호스트(2)–Pod(3)–컨테이너(2) 그루핑으로 외울 수 있는가? |
| 01-06 | [cgroup 사례 — Endowus OOMKilled](./01-06.cgroup%20사례%20—%20Endowus%20OOMKilled.md) | Pod 6GB·JVM 힙 4.37GB인데 OOMKilled가 반복되는 이유는? cgroup의 RSS 기준이 JVM 힙과 어떻게 다르며, jimage·Akka·Netty가 만든 사각지대 1.63GB를 어떻게 추적했는가? |
| 01-07 | [OverlayFS와 user namespace — Netflix UID 격리](./01-07.OverlayFS와%20user%20namespace%20—%20Netflix%20UID%20격리.md) | user namespace + ID map이 보안을 어떻게 강화했고, OverlayFS lowerdir 마운트가 글로벌 락 폭주를 일으켜 노드 마비로 번진 5단계 나비 효과는? Linux 6.3 recursive bind mount의 해결 원리는? |



## 상위·이웃·활용처

- 상위: [02_os/ MOC](../README.md)
- 이웃: [02_os/networking/](../networking/README.md) — netns·veth·bridge·netfilter·conntrack·TC·eBPF 깊이
- 활용처: [08_cloud/kubernetes/](../../08_cloud/kubernetes/README.md) — Pod·자원 관리·보안 운영
