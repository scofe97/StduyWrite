---
title: 02_os 통합 학습 로드맵 — 백엔드·Kubernetes 운영 관점
tags: [roadmap, os, linux, kubernetes, backend, performance, security]
status: draft
source:
  - ./README.md
  - ./kernel/roadmap.md
  - ./networking/roadmap.md
  - ./book/systems-performance/README.md
related:
  - ./README.md
  - ./troubleshooting/README.md
  - ./kernel/README.md
  - ./networking/README.md
  - ./book/linux-kernel-programming/README.md
  - ./book/systems-performance/README.md
  - ../08_cloud/book/container-security/README.md
updated: 2026-09-05
---

# 02_os 통합 학습 로드맵
---
> 이 로드맵은 Linux를 처음부터 구현하는 과정이 아니라, 백엔드·Kubernetes 환경의 장애를 커널 원인까지 설명하기 위한 읽기 순서입니다. 개별 폴더의 로드맵은 상세 주제 목록이고, 이 문서는 여러 자료를 어떤 순서로 연결할지 결정합니다.

## 1. 이 로드맵을 쓰는 법

한 단계를 모두 끝낸 뒤에만 다음 단계로 갈 필요는 없습니다. 실제 장애를 만났다면 해당 증상 단계로 바로 들어가고, 이해에 필요한 선행 문서만 되돌아봅니다. 증상에서 출발하는 편이 빠를 때는 [troubleshooting/](./troubleshooting/README.md)이 지름길입니다. 사례집이 증상별 확인 순서를 정리해 두었고 각 사례가 원리를 다루는 문서로 되돌아가는 링크를 함께 답니다.

책 정독은 필수가 아니라 심화 경로입니다. 먼저 `kernel/`과 `networking/`의 운영자 관점 문서로 문제를 해석할 뼈대를 만들고, 더 깊은 원리나 도구가 필요할 때 `book/` 아래의 정독 노트를 사용합니다.

| 학습 목적 | 우선 경로 | 보류할 자료 |
|---|---|---|
| Pod가 느리거나 죽는 이유를 찾기 | 1 → 2 → 4단계 | 커널 모듈 개발 상세 |
| Service 연결·DNS·NAT 문제를 추적하기 | 1 → 3 → 4단계 | CPU·메모리 심화 |
| 컨테이너 보안 설정을 판단하기 | 1 → 2 → 5단계 | 성능 도구 심화 |
| 커널 내부 구현을 이해하기 | 1 → 2 뒤 6단계 | 운영 사례 중심 문서 |
| 지금 난 장애부터 끄기 | [troubleshooting/](./troubleshooting/README.md) → 해당 증상 단계 | 개념 정독 |

## 2. 1단계 — 실행 모델을 먼저 잡는다

프로세스가 시스템 콜로 커널에 일을 요청하고, 스레드가 CPU에서 실행되며, 상태가 `/proc`에 드러난다는 흐름을 먼저 잡습니다. 이 모델이 없으면 OOMKilled·느린 요청·파일 디스크립터 고갈을 각각 다른 문제로 오해하기 쉽습니다.

1. [커널과 컨테이너](./kernel/01-01.커널과%20컨테이너.md)로 유저 공간·커널 공간·시스템 콜·컨테이너 생성의 큰 흐름을 잡습니다.
2. [운영체제 (1) — 커널·시스템 콜·인터럽트·프로세스](./book/systems-performance/03-01.운영체제%20(1)%20—%20커널·시스템%20콜·인터럽트·프로세스.md)로 모드 전환과 컨텍스트 전환을 구분합니다.
3. 더 깊은 구조가 필요하면 [프로세스와 스레드 (1)](./book/linux-kernel-programming/06-01.프로세스와%20스레드%20(1)%20—%20컨텍스트·VAS·스택.md)과 [프로세스와 스레드 (2)](./book/linux-kernel-programming/06-02.프로세스와%20스레드%20(2)%20—%20task%20구조와%20current.md)를 읽습니다.

다음 단계로 가기 전에 요청 하나가 프로세스·스레드·시스템 콜·커널 작업으로 이어지는 경로와, `/proc/<pid>`에서 확인할 수 있는 상태를 설명할 수 있어야 합니다.

## 3. 2단계 — 자원 제한과 컨테이너 격리를 해석한다

Kubernetes의 `requests`·`limits`는 선언일 뿐이고, 실제 제한과 관측은 cgroup 파일시스템에서 일어납니다. namespace는 무엇을 보게 할지, cgroup은 얼마나 쓰게 할지를 정하므로 두 개념을 함께 익혀야 Pod의 실행 환경을 올바르게 읽을 수 있습니다.

1. [cgroup v2 깊이](./kernel/01-02.cgroup%20v2%20깊이.md)와 [cgroup 파일시스템 실습](./kernel/01-04.cgroup%20파일시스템%20실습.md)으로 `memory.max`, `cpu.max`, PSI를 실제 경로와 연결합니다.
2. [namespace 실습](./kernel/01-05.namespace%20실습%20—%208가지%20격리와%20unshare.md), [마운트 네임스페이스와 propagation](./kernel/01-03.마운트%20네임스페이스와%20propagation.md), [OverlayFS와 user namespace](./kernel/01-07.OverlayFS와%20user%20namespace%20—%20Netflix%20UID%20격리.md) 순서로 격리와 파일시스템 관점을 확장합니다.
3. OOMKilled를 만났다면 [cgroup 사례 — Endowus OOMKilled](./kernel/01-06.cgroup%20사례%20—%20Endowus%20OOMKilled.md)를 먼저 읽고, 메모리의 내부 동작은 [메모리 (1) — 용어·핵심 개념](./book/systems-performance/07-01.메모리%20(1)%20—%20용어·핵심%20개념.md)부터 보강합니다.

이 단계의 목표는 JVM 힙 크기와 컨테이너 RSS의 차이, CPU throttling과 애플리케이션 지연의 관계, Pod·컨테이너·호스트가 공유하거나 분리하는 namespace를 근거와 함께 설명하는 것입니다.

## 4. 3단계 — 네트워크 패킷의 실제 경로를 본다

Service·Ingress 같은 Kubernetes 추상은 결국 Linux socket, 네트워크 namespace, 라우팅, netfilter와 conntrack 위에서 동작합니다. 패킷이 어느 계층에서 사라졌는지 구분해야 DNS·NAT·정책 문제를 같은 방식으로 진단하지 않게 됩니다.

1. [네트워킹 기초](./networking/01-01.네트워킹%20기초.md)로 netns·veth·bridge·routing·netfilter·conntrack의 역할을 한 번에 연결합니다.
2. [K8s 패킷 여정](./networking/01-02.K8s%20패킷%20여정%20—%20netfilter·conntrack·라우팅.md)으로 Pod에서 Service까지의 데이터 경로를 따라갑니다.
3. 이름 해석 문제는 [DNS 필터링 차단](./networking/01-03.DNS%20필터링%20차단%20—%20NXDOMAIN·DoH·우회%20마찰.md)으로 분리하고, TCP 상태·큐·포트 고갈·패킷 캡처는 [networking 상세 로드맵](./networking/roadmap.md)에서 필요한 항목만 확장합니다.

다음 단계로 가기 전에 연결 실패를 DNS, TCP 연결, 라우팅·NAT, 정책·conntrack 중 어느 층에서 확인할지와 각 층의 첫 관측 명령을 설명할 수 있어야 합니다.

## 5. 4단계 — 성능을 증상 대신 방법론으로 분석한다

CPU 사용률 하나만 보고 병목을 판단하면 I/O 대기·락 경합·스케줄링 지연을 놓칠 수 있습니다. 먼저 문제를 지연·사용률·포화로 분해하고, 그 뒤에 CPU·메모리·파일시스템·디스크·네트워크 중 측정할 대상을 고릅니다.

1. [방법론 (1)](./book/systems-performance/02-01.방법론%20(1)%20—%20용어·모델·핵심%20개념.md)과 [방법론 (2)](./book/systems-performance/02-02.방법론%20(2)%20—%20분석%20방법론%2020종.md)로 USE·RED와 지연 분석의 질문을 익힙니다.
2. 증상에 따라 CPU(06장), 메모리(07장), 파일시스템(08장), 디스크(09장), 네트워크(10장) 문서를 선택합니다. 각각의 MOC에서 방법론·도구 편을 우선하고, 아키텍처·튜닝 편은 원인이 좁혀진 뒤 읽습니다.
3. 기본 관측이 부족할 때 [관측 도구 (2)](./book/systems-performance/04-02.관측%20도구%20(2)%20—%20관측%20소스.md)로 `/proc`·`/sys`·tracepoint를, 심화 추적이 필요할 때 perf·Ftrace·BPF 장으로 들어갑니다.

이 단계의 완료 기준은 “CPU가 높다”가 아니라 어떤 리소스가 얼마나 바쁘고, 어디에 대기열이 쌓이며, 어떤 관측으로 가설을 반증할지 말할 수 있는 상태입니다.

## 6. 5단계 — 컨테이너 보안을 실행 모델 위에서 판단한다

보안 옵션은 체크리스트로 외우기보다 실행 모델을 얼마나 줄이는지로 판단해야 합니다. capability·user namespace·seccomp는 모두 프로세스가 커널에 요청할 수 있는 권한과 범위를 제한하지만, 줄이는 공격 표면과 운영 비용은 서로 다릅니다.

1. [리눅스 시스템 콜·권한·Capabilities](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md)와 [제어 그룹](../08_cloud/book/container-security/03-01.Control%20Group%20%E2%80%94%20%EC%9E%90%EC%9B%90%EC%9D%84%20%EC%A0%9C%ED%95%9C%ED%95%B4%20%EA%B5%B6%EA%B8%B0%EA%B8%B0%EB%A5%BC%20%EB%A7%89%EB%8B%A4.md)으로 권한과 자원 경계를 복습합니다.
2. [컨테이너 격리 (1)](../08_cloud/book/container-security/04-01.namespace%EC%99%80%20%EB%A3%A8%ED%8A%B8%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EB%A5%BC%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%EB%91%90%20%EC%9E%A5%EC%B9%98.md), [컨테이너 격리 (2)](../08_cloud/book/container-security/04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md), [격리 강화 (1)](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) 순서로 방어 계층을 연결합니다.
3. 이미지·공급망·런타임 정책은 [container-security MOC](../08_cloud/book/container-security/README.md)의 6~16장을 따라 확장하고, 애플리케이션 보안 자체는 [99_ETC/security](../99_ETC/security/README.md)에서 이어서 다룹니다.

이 단계의 목표는 `privileged`, host namespace 공유, root 실행, capability 추가 요청을 받았을 때 위험·필요성·대안을 구분해 설명하는 것입니다.

## 7. 6단계 — 목적에 맞는 심화 경로를 고른다

운영 문제를 해석할 수 있게 된 뒤에만 심화 경로로 들어갑니다. 세 경로는 같은 메커니즘을 다루지만 질문이 다르므로, 한 권을 끝낸 뒤 다음 권으로 넘어가야 하는 선후 관계는 아닙니다.

| 목적 | 경로 | 얻는 관점 |
|---|---|---|
| 커널 코드와 LKM 이해 | [Linux Kernel Programming](./book/linux-kernel-programming/README.md) | 커널 모듈 작성자 |
| 병목 분석과 추적 도구 사용 | [Systems Performance](./book/systems-performance/README.md) | 성능 분석가 |
| 컨테이너 위협과 완화책 판단 | [Container Security](../08_cloud/book/container-security/README.md) | 보안 엔지니어 |

## 8. 후속 후보

새 문서는 실제 장애·실습에서 현재 MOC로 설명할 수 없는 질문이 반복될 때만 추가합니다. 후보가 다섯 편 이상 쌓이기 전에는 새 폴더를 만들지 않고 기존 `kernel/` 또는 `networking/`에 두며, 개별 문서가 기존 책 노트와 겹치는지 먼저 확인합니다.

- 파일 디스크립터 고갈, `epoll`, listen backlog, ephemeral port, TIME_WAIT를 하나의 백엔드 연결 장애 흐름으로 묶는 운영 문서
- VFS·페이지 캐시·블록 I/O를 Kubernetes volume과 함께 해석하는 저장소 지연 문서
- `perf`, Ftrace, BPF를 동일 장애에서 언제 어떻게 나눠 쓸지 비교하는 추적 선택 문서

## 관련 문서

- [02_os MOC](./README.md) — 폴더 경계와 모든 자료의 진입점
- [troubleshooting 사례집](./troubleshooting/README.md) — 증상에서 원인으로 역추적하는 리눅스 장애 41건
- [kernel 상세 로드맵](./kernel/roadmap.md) — 커널 주제 전체와 장애 매핑
- [networking 상세 로드맵](./networking/roadmap.md) — 네트워크 주제 전체와 추천 프로젝트
- [08_cloud/kubernetes](../08_cloud/kubernetes/README.md) — 이 OS 메커니즘을 사용하는 상위 플랫폼
