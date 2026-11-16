---
title: 02_os/docs/kernel — 커널과 컨테이너
tags: [moc, linux, kernel, syscall, namespace, cgroup, proc, runtime]
status: final
related:
  - ../../os-keywords.md
  - ../../README.md
  - ../../../08_cloud/book/networking-and-kubernetes/README.md
  - ../../../08_cloud/kubernetes/README.md
updated: 2026-09-12
---

# 02_os/docs/kernel
---
> Linux 커널이 컨테이너 동작에서 맡는 책임을 정리한다. cgroup v2 깊이, 마운트 네임스페이스 propagation, cgroup 사례, OverlayFS와 user namespace까지 — 네트워크 영역은 `08_cloud/book/networking-and-kubernetes/` 정독본에서 다루고 본 폴더는 그 외 커널 일반 메커니즘에 집중한다.

> 프로세스·시스템 콜·스케줄링·메모리·cgroup·namespace·파일시스템·보안·관측의 읽기 순서는 [OS 로드맵](../../os-keywords.md)에 정리했습니다.



## 문서

공통 개념은 번호 파일(`NN-NN.`), 거기서 갈라진 세부 주제나 사례는 번호 없는 이름 파일로 배치합니다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [cgroup v2](./01-01.cgroup%20v2.md) | 단일 트리·컨트롤러·PSI·kubepods.slice·throttling/OOM 분석은 cgroup 파일에서 어떻게 읽는가? |
| 01-02 | [mount propagation](./01-02.mount%20propagation.md) | private/shared/slave/unbindable 4종과 K8s `mountPropagation` 옵션은 CSI·HostPath 사고를 어떻게 결정하는가? |
| — | [OverlayFS 와 idmapped mount — Netflix 사례](./OverlayFS%20와%20idmapped%20mount%20%E2%80%94%20Netflix%20%EC%82%AC%EB%A1%80.md) | 컨테이너마다 ID 를 매핑하면 마운트 연산이 어떻게 20,200회로 불어나고, 전역 마운트 락과 CPU 구조가 그것을 어떻게 키우며, 부모 디렉터리 한 번 idmap 으로 어떻게 푸는가? |

> 기존 01-06 Endowus OOMKilled 사례는 [ITJVM ch02 01-05](../../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch02_automatic-memory-management/01-05.실전 — Docker 컨테이너 네이티브 메모리와 OOMKilled.md#64-컨테이너-힙-비율과-오프힙-예산)에 고유 사실을 흡수했습니다.



## 상위·이웃·활용처

- 통합 경로: [OS 학습 로드맵](../../os-keywords.md) — 자원·격리 단계의 진입점
- 상위: [02_os/ MOC](../../README.md)
- 이웃: [N&K 질문별 정본](../../../08_cloud/book/networking-and-kubernetes/README.md#%EC%A7%88%EB%AC%B8%EB%B3%84-%EC%A0%95%EB%B3%B8) — netns·veth·bridge·netfilter·conntrack·TC·eBPF 깊이
- 활용처: [08_cloud/kubernetes/](../../../08_cloud/kubernetes/README.md) — Pod·자원 관리·보안 운영
