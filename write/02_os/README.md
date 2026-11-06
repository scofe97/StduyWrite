---
title: 02_os — OS 공통 기반
tags: [moc, os, linux, kernel, networking]
status: final
related:
  - ../README.md
  - ../roadmap/os-roadmap.md
  - ./kernel/README.md
  - ./book/learning-modern-linux/README.md
  - ./book/ostep_operating-systems-three-easy-pieces/README.md
  - ./book/linux-kernel-programming/README.md
  - ./book/systems-performance/README.md
  - ./book/learning-ebpf/README.md
  - ./book/paw_packet-analysis-wireshark/README.md
  - ./book/cntd_computer-networking-top-down/README.md
  - ./book/sshm_ssh-mastery/README.md
  - ./project/network-fundamentals-lab/README.md
  - ../08_cloud/book/container-security/README.md
  - ./project/portal-tunnel/README.md
  - ../08_cloud/book/networking-and-kubernetes/README.md
  - ../08_cloud/book/learning-coredns/README.md
updated: 2026-11-06
---

# 02_os
---
> 언어가 아닌 실행 환경(OS·커널)에 해당하는 공통 기반을 모은다. `01_language`가 문법·생태계라면 이 카테고리는 그 아래 깔린 메커니즘이다.

상위 카테고리(K8s, 서비스 메시 등)에서 같은 OS 메커니즘이 반복 등장할 때 본 카테고리로 끌어 올려 한 곳에서만 정리한다.

처음에는 [OS 학습 로드맵](../roadmap/os-roadmap.md)을 읽습니다. 운영 장애를 실행 모델·자원·성능·보안으로 분해하는 순서로 연결합니다.



## 하위 폴더

| 경로 | 범위 |
|------|------|
| [OS 로드맵](../roadmap/os-roadmap.md) | 백엔드·Kubernetes 운영자가 OS 문제를 해석하는 학습 순서 |
| [networking-and-kubernetes/](../08_cloud/book/networking-and-kubernetes/README.md) | 커널 네트워크 메커니즘의 정본 — netns·veth·bridge·netfilter·conntrack·TC·eBPF·kube-proxy·CNI (책 기반, `08_cloud` 소재) |
| [kernel/](./kernel/README.md) | cgroup v2 깊이, 마운트 네임스페이스 propagation, cgroup 사례, OverlayFS와 user namespace |
| [learning-modern-linux/](./book/learning-modern-linux/README.md) | 클라우드 네이티브 환경을 전제로 리눅스를 한 바퀴 도는 개론 — 커널·셸·접근 제어·파일시스템·네트워크·관측 (책 기반) |
| [ostep_operating-systems-three-easy-pieces/](./book/ostep_operating-systems-three-easy-pieces/README.md) | OS 가 왜 그렇게 동작하는가 — 가상화(CPU·메모리)·병행성(스레드·락)·지속성(디스크·파일 시스템)과 분산 시스템, 웹 전용 보안 장(인증·접근 통제·암호)과 가상 머신 모니터 부록을 장마다의 CRUX 질문 순서로 읽는 원리 축. 형제 책이 보여 주는 Linux 인터페이스와 구현의 아래층 (책 기반) |
| [linux-kernel-programming/](./book/linux-kernel-programming/README.md) | 커널 개발자 관점의 리눅스 내부 — LKM 모듈 개발, 커널 빌드, 메모리 관리, CPU 스케줄러, 동기화 (책 기반) |
| [container-security/](../08_cloud/book/container-security/README.md) | 보안 관점의 컨테이너 — 커널 기초(namespace·cgroup·root 변경) 위의 이미지·공급망·런타임·통신 보안 (책 기반) |
| [learning-coredns/](../08_cloud/book/learning-coredns/README.md) | 이름 해석의 *서버* 편 — Corefile·플러그인 체인·존 데이터·쿠버네티스 연동. resolver 클라이언트 측(네트워크 로드맵 1단계·N&K 04-03 §5)과 편을 나눠 가진다 (책 기반) |
| [systems-performance/](./book/systems-performance/README.md) | 성능 분석가 관점의 시스템 성능 — 방법론·CPU·메모리·디스크·네트워크·클라우드·고급 추적(perf·Ftrace·BPF) (책 기반) |
| [learning-ebpf/](./book/learning-ebpf/README.md) | eBPF 프로그램 자체의 구조 — 맵·헬퍼·`bpf()` 시스템 콜·verifier·BTF·CO-RE·부착 유형과 네트워킹·보안 활용. `systems-performance/` 가 도구로 쓰는 BCC·bpftrace 의 아래층 (책 기반) |
| [paw_packet-analysis-wireshark/](./book/paw_packet-analysis-wireshark/README.md) | 선 위의 프레임을 떠서 프로토콜별로 읽는 법 — Wireshark 캡처·필터·TCP·TLS·응용 프로토콜·WLAN·보안 분석 (책 기반) |
| [cntd_computer-networking-top-down/](./book/cntd_computer-networking-top-down/README.md) | 프로토콜을 위에서 아래로 훑는 규격 축 — 응용·트랜스포트·네트워크 계층의 원리와 라우팅·SDN·망 관리. `paw_` 가 캡처로 확인하는 것을 여기서 규격으로 배운다 (책 기반) |
| [sshm_ssh-mastery/](./book/sshm_ssh-mastery/README.md) | OpenSSH 를 운영자 눈으로 다루는 축 — 호스트 키 검증·공개키 인증·SFTP·포트 포워딩·유휴 연결 유지. npg 확장 트랙 X9 리버스 터널과 ssh-bbs 가 기대는 장치를 설정과 명령으로 먼저 본다 (책 기반) |
| [network-fundamentals-lab/](./project/network-fundamentals-lab/README.md) | 고장이 장전된 채로 뜨는 containerlab 토폴로지 18편 — 증상에서 계층을 좁히는 훈련. N&K 정독본이 맡는 메커니즘을 깨뜨려 확인하는 축이다 (랩 저장소 기반) |


| [portal-tunnel/](./project/portal-tunnel/README.md) | 오픈소스 Go reverse tunnel 을 빌드해 띄우고 코드를 읽으며 기여까지 가는 시리즈 — 기초 개념·transport·TLS 신뢰 경계·identity 정책·SDK·코드 리뷰 (외부 저장소 기반) |

## 카테고리 결정 원칙

- 출간된 책을 읽고 정리한 정독본은 `book/` 에 둔다. 남의 랩 저장소를 따라 하거나 직접 만든 도구로 배운 기록은 책이 아니므로 `project/` 에 둔다
- 커널 네트워크 자료구조(netns, veth, conntrack, netfilter) → `08_cloud/book/networking-and-kubernetes/` 정독본. 질문을 그 편으로 보내는 라우팅표는 그 README 의 「질문별 정본」 절에 있다 — 02_os 에 네트워크 메커니즘 본문을 새로 쓰지 않는다
- 컨테이너 런타임 격리·자원 제한(namespace, cgroup, seccomp) → 기초는 `container-security/`(namespace)와 `kubernetes-in-action/` 02-03(cgroup), cgroup v2 깊이·마운트 propagation·사례는 `kernel/`
- GitHub 에 저장소가 있고 실제로 돌려 볼 수 있는 프로젝트는 남의 오픈소스여도 `project/` 다(예: `portal-tunnel/`). 공식문서처럼 개념만 정리한 노트는 `docs/` 에 둔다
- 시스템 콜 인터페이스, /proc, VFS, 메모리 관리 → `learning-modern-linux/` (운영자 관점) 또는 `linux-kernel-programming/` (커널 모듈 작성자 관점)
- 커널 모듈(LKM) 개발, 커널 소스 빌드, 메모리 할당 API, 스케줄러·동기화 내부 → `linux-kernel-programming/`
- 컨테이너 이미지 포맷·OCI 표준 같은 빌드 측면은 `07_devops/`에 둔다 (런타임 측면이 아니므로 본 카테고리 아님)
- 컨테이너 보안(격리 메커니즘을 보안 관점에서 보기, 이미지·공급망·런타임 위협) → `container-security/`. namespace 메커니즘 자체는 그 책의 04-01·04-02 가 정본이고, cgroup v2 깊이·마운트 propagation 은 `kernel/` 을 교차참조한다
- DNS 는 방향으로 가른다. 질의를 *보내는* 쪽(`/etc/resolv.conf`·ndots·search domain·glibc resolver)은 네트워크 로드맵 1단계가 SSOT 이고(본문은 N&K 04-03 §5), 질의를 *받는* 쪽(Corefile·플러그인·존 데이터)은 `learning-coredns/` 가 맡는다
- 증상에서 출발해 원인을 역추적하는 진단 문서(디스크가 찼다, 포트가 안 열린다, 패킷이 사라진다) → 최상위 [`troubleshooting/`](../troubleshooting/README.md). 메커니즘을 설명하는 쪽은 N&K 정독본·`kernel/`이 SSOT이고, 진단 사례가 그것을 교차참조한다
- 패킷을 떠서 읽는 일(캡처 필터·디스플레이 필터, 프로토콜 해독, tcpdump·tshark) → `paw_packet-analysis-wireshark/`. N&K 정독본이 커널이 패킷을 *어떻게 나르는가*를 맡고, 이쪽은 그 패킷을 *어떻게 들여다보는가*를 맡는다. 애플리케이션이 스스로 내보내는 메트릭·로그·트레이스는 `06_observability/` 소관이라 본 폴더 아님
- 시스템 성능 분석(방법론·병목 진단, CPU·메모리·디스크·네트워크 성능, perf·Ftrace·BPF 추적) → `systems-performance/`. 커널 메커니즘 자체는 `linux-kernel-programming/`·`kernel/`이 SSOT이고 "성능 관점"으로 교차참조한다. LGTM 스택·SLO 같은 앱·인프라 관측 운영은 `06_observability/` 소관이라 본 폴더 아님
- 메커니즘을 고장 내서 증상으로 되짚는 실습 → `network-fundamentals-lab/`. 메커니즘 자체는 N&K 정독본이 SSOT 이고 이쪽은 깨졌을 때의 지문을 맡는다. 직접 푼 진단 사례는 최상위 `troubleshooting/` 소관이라 본 폴더 아님

> `kernel/`과 `linux-kernel-programming/`은 둘 다 커널을 다루지만 시선이 다르다. 전자는 "K8s가 cgroup 파일을 어떻게 쓰는가"(운영자), 후자는 "모듈에서 커널 메모리를 어떻게 할당하는가"(개발자) 관점이다. 같은 메커니즘이 양쪽에 나오면 교차참조한다.



## 추천 읽기 경로

백엔드·Kubernetes 운영자는 [OS 로드맵](../roadmap/os-roadmap.md)의 1~4단계를 먼저 따릅니다. OOMKilled·CPU throttling 은 `kernel/`, Pod 격리는 [container-security](../08_cloud/book/container-security/README.md) 04-01, DNS·Service·NAT 문제는 [N&K 정독본](../08_cloud/book/networking-and-kubernetes/README.md), 성능 병목은 `book/systems-performance/`으로 확장합니다.

커널 모듈 작성이나 커널 소스 자체가 목적일 때만 `book/linux-kernel-programming/`을 별도 정독합니다. 컨테이너 보안 옵션과 공급망 위험을 판단하려면 1~2단계 뒤 `book/container-security/`으로 이동합니다.



## 관련 문서

- [OS 학습 로드맵](../roadmap/os-roadmap.md) — OS 전체를 가로지르는 추천 순서
- [write/ MOC](../README.md) — 전체 카테고리 지도
- [08_cloud/kubernetes/](../08_cloud/kubernetes/README.md) — 본 카테고리의 활용처
