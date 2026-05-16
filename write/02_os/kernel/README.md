---
title: 02_os/kernel — 커널과 컨테이너
tags: [moc, linux, kernel, syscall, namespace, cgroup, proc, runtime]
status: final
related:
  - ../README.md
  - ../networking/README.md
  - ../../09_cloud/kubernetes/README.md
updated: 2026-04-26
---

# 02_os/kernel
---
> Linux 커널이 컨테이너 동작에서 맡는 책임을 정리한다. 유저/커널 스페이스 분리, 시스템 콜, 커널 코어 영역, namespace·cgroup, /proc, K8s 노드 필수 커널 파라미터까지 — 네트워크 영역은 별도 `networking/`에서 다루고 본 폴더는 그 외 커널 일반 메커니즘에 집중한다.



## 문서

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [커널과 컨테이너](./01-01.커널과%20컨테이너.md) | 유저/커널 스페이스 분리, 시스템 콜, 코어 7대 영역, namespace/cgroup, /proc, K8s 노드 필수 커널 파라미터, runc create 시퀀스는 어떻게 컨테이너 동작을 만드는가? |
| 01-02 | [cgroup v2 깊이](./01-02.cgroup%20v2%20깊이.md) | 단일 트리·컨트롤러·PSI·kubepods.slice·throttling/OOM 분석은 cgroup 파일에서 어떻게 읽는가? |
| 01-03 | [마운트 네임스페이스와 propagation](./01-03.마운트%20네임스페이스와%20propagation.md) | private/shared/slave/unbindable 4종과 K8s `mountPropagation` 옵션은 CSI·HostPath 사고를 어떻게 결정하는가? |
| 01-04 | [cgroup 파일시스템 실습](./01-04.cgroup%20파일시스템%20실습.md) | `/sys/fs/cgroup` 트리에서 Pod별 디렉토리를 찾아 `memory.max`·`cpu.max`와 K8s `requests`/`limits`를 어떻게 매핑하는가? |
| 01-05 | [namespace 실습 — 8가지 격리와 unshare](./01-05.namespace%20실습%20—%208가지%20격리와%20unshare.md) | `unshare`로 PID·UTS·MNT·NET 격리를 직접 만들고 호스트(2)–Pod(3)–컨테이너(2) 그루핑으로 외울 수 있는가? |



## 상위·이웃·활용처

- 상위: [02_os/ MOC](../README.md)
- 이웃: [02_os/networking/](../networking/README.md) — netns·veth·bridge·netfilter·conntrack·TC·eBPF 깊이
- 활용처: [09_cloud/kubernetes/](../../09_cloud/kubernetes/README.md) — Pod·자원 관리·보안 운영
