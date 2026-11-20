---
title: 02_os — OS 공통 기반
tags: [moc, os, linux, kernel, networking]
status: final
related:
  - ../README.md
  - os-keywords.md
  - ./docs/kernel/README.md
  - ./docs/cmd/README.md
  - ./book/learning-modern-linux/README.md
  - ./book/linux-kernel-programming/README.md
  - ./book/tlpi_the-linux-programming-interface/README.md
  - ./book/systems-performance/README.md
  - ./book/learning-ebpf/README.md
  - ./book/paw_packet-analysis-wireshark/README.md
  - ./book/cntd_computer-networking-top-down/README.md
  - ./book/npg_network-programming-with-go/README.md
  - ./project/network-fundamentals-lab/README.md
  - ./project/portal-tunnel/README.md
  - ./project/lampson-lab/README.md
  - ./project/learning-modern-linux-lab/README.md
  - ../08_cloud/book/container-security/README.md
  - ../08_cloud/book/networking-and-kubernetes/README.md
  - ../08_cloud/book/learning-coredns/README.md
updated: 2026-11-14
---

# 02_os

> 언어가 아닌 실행 환경(OS·커널)에 해당하는 공통 기반을 모읍니다. `01_language`가 문법·생태계라면 이 카테고리는 그 아래 깔린 메커니즘입니다.



## 경계 기준

상위 카테고리(Kubernetes, 서비스 메시 등)에서 같은 OS 메커니즘이 반복 등장할 때 본 카테고리로 끌어 올려 한 곳에서만 정리합니다.

- 출간된 책을 읽고 정리한 정독본은 `book/` 에 둡니다. 남의 랩 저장소를 따라 하거나 직접 만든 도구로 배운 기록은 책이 아니므로 `project/` 에 둡니다.
- GitHub 에 저장소가 있고 실제로 돌려 볼 수 있는 프로젝트는 남의 오픈소스여도 `project/` 입니다. 공식문서처럼 개념만 정리한 노트는 `docs/` 에 둡니다.
- 커널 네트워크 자료구조(netns, veth, conntrack, netfilter)는 `08_cloud/book/networking-and-kubernetes/` 정독본이 정본입니다. 질문을 그 편으로 보내는 라우팅표는 해당 README 의 「질문별 정본」 절에 있습니다. 본 카테고리에는 네트워크 메커니즘 본문을 새로 쓰지 않습니다.
- 컨테이너 런타임 격리·자원 제한(namespace, cgroup, seccomp) 기초는 `container-security/`(namespace)와 `kubernetes-in-action/` 02-03(cgroup)에 둡니다. cgroup v2 깊이·마운트 propagation·사례는 `docs/kernel/` 에 둡니다.
- 시스템 콜 인터페이스, /proc, VFS, 메모리 관리는 `learning-modern-linux/` (운영자 관점) 또는 `linux-kernel-programming/` (커널 모듈 작성자 관점)에 둡니다.
- 커널 모듈(LKM) 개발, 커널 소스 빌드, 메모리 할당 API, 스케줄러·동기화 내부는 `linux-kernel-programming/` 에 둡니다.
- 컨테이너 이미지 포맷·OCI 표준 같은 빌드 측면은 `07_devops/`에 둡니다. 런타임 측면이 아니므로 본 카테고리가 아닙니다.
- 컨테이너 보안(격리 메커니즘을 보안 관점에서 보기, 이미지·공급망·런타임 위협)은 `container-security/` 에 둡니다. namespace 메커니즘 자체는 그 책의 04-01·04-02 가 정본이고, cgroup v2 깊이·마운트 propagation 은 `docs/kernel/` 을 교차참조합니다.
- DNS 는 방향으로 가릅니다. 질의를 *보내는* 쪽(`/etc/resolv.conf`·ndots·search domain·glibc resolver)은 네트워크 로드맵 1단계가 SSOT 입니다(본문은 N&K 04-03 §5). 질의를 *받는* 쪽(Corefile·플러그인·존 데이터)은 `learning-coredns/` 가 맡습니다.
- 증상에서 출발해 원인을 역추적하는 진단 문서는 최상위 [`troubleshooting/`](../troubleshooting/README.md)에 둡니다. 메커니즘을 설명하는 쪽은 N&K 정독본·`docs/kernel/`이 SSOT 이고, 진단 사례가 그것을 교차참조합니다.
- 패킷을 떠서 읽는 일(캡처 필터·디스플레이 필터, 프로토콜 해독, tcpdump·tshark)은 `paw_packet-analysis-wireshark/` 에 둡니다. N&K 정독본이 커널의 패킷 전달을 맡고, 이쪽은 패킷 분석을 맡습니다. 애플리케이션 메트릭·로그·트레이스는 `06_observability/` 소관입니다.
- 시스템 성능 분석(방법론·병목 진단, CPU·메모리·디스크·네트워크 성능, perf·Ftrace·BPF 추적)은 `systems-performance/` 에 둡니다. 커널 메커니즘 자체는 `linux-kernel-programming/`·`docs/kernel/`이 SSOT 이고, 앱·인프라 관측 운영은 `06_observability/` 소관입니다.
- 메커니즘을 고장 내서 증상으로 되짚는 실습은 `network-fundamentals-lab/` 에 둡니다. 메커니즘 자체는 N&K 정독본이 SSOT 이고, 직접 푼 진단 사례는 최상위 [`troubleshooting/`](../troubleshooting/README.md) 소관입니다.
- `docs/kernel/`과 `linux-kernel-programming/`은 둘 다 커널을 다루지만 시선이 다릅니다. 전자는 "Kubernetes가 cgroup 파일을 어떻게 쓰는가"(운영자), 후자는 "모듈에서 커널 메모리를 어떻게 할당하는가"(개발자) 관점입니다. 같은 메커니즘이 양쪽에 나오면 교차참조합니다.



## 키워드

### os-keywords.md

키워드 파일: [os-keywords.md](os-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · Linux 사용 | 7편 | — |
| 2단계 · 실행 모델 | 12편 | `fork` · `exec` · copy-on-write 로 뜨는 새 프로세스 · 주소 공간 · heap · stack · 프로세스 메모리 배치 |
| 3단계 · 컨테이너 기반 | 5편 | — |
| 4단계 · 성능 분석 | 19편 | 활용률 대 압력 — PSI 가 답하는 질문 · coordinated omission — 측정이 놓치는 지연 |
| 5단계 · 관측과 보안 | 18편 | `/proc/stat` · `/proc/meminfo` 읽기 · `/proc/PID/stat` · `status` · `statm` · `/proc/pressure` — some 과 full · avg10 · 비밀의 수명 — 생성·사용·파기 · zeroing · `explicit_bzero` · `OPENSSL_cleanse` |
| 6단계 · 커널 내부 | 13편 | — |

### network-keywords.md

키워드 파일: [network-keywords.md](network-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 연결 | 37편 | 4-tuple · 듣는 소켓과 연결 소켓의 구분 · ClientHello · ServerHello · 확장 협상 · ECDHE · X25519 · secp256r1 · forward secrecy · AEAD · AES-GCM · ChaCha20-Poly1305 · cipher suite |
| 2단계 · Linux 경로 | 23편 | — |
| 3단계 · 관측 | 15편 | — |
| 4단계 · Kubernetes | 2편 | — |
| 5단계 · 클라우드 네트워크 | 5편 | — |
| 6단계 · 데이터패스와 정책 | 15편 | — |
| 7단계 · 운영 경계 | 1편 | identity 와 trust 의 차이 · 인증과 인가의 차이 |
| 8단계 · 오버레이와 신뢰 | 11편 | traffic correlation · metadata · timing side-channel · 암호화가 숨기는 것과 숨기지 않는 것 |
| 9단계 · 터널과 경로 | 2편 | 피어 발견 대 터널 구성 — 찾았다고 연결된 것은 아니다 · 멀티홉 — 홉 수가 지연 · 성공률 · 프라이버시에 미치는 값 · path selection · latency · 가용성 · 다양성 · 비용 함수 · 종단 성공 확률 — 단계별 실패가 곱으로 쌓인다 |



## 하위 폴더·문서 목록

| 경로 | 범위 |
|------|------|
| [OS 로드맵](os-keywords.md) | 백엔드·Kubernetes 운영자가 OS 문제를 해석하는 학습 순서 |
| [networking-and-kubernetes/](../08_cloud/book/networking-and-kubernetes/README.md) | 커널 네트워크 메커니즘의 정본 — netns·veth·bridge·netfilter·conntrack·TC·eBPF·kube-proxy·CNI (책 기반, `08_cloud` 소재) |
| [docs/cmd/](./docs/cmd/README.md) | 리눅스 명령 사용법을 명령별로 모은 조회용 시트 — 지금은 텍스트 처리(`sed`·`grep`·`awk` 등). 책 노트가 원리를, 이 폴더가 옵션과 실행 예를 맡아 다른 리눅스 노트가 링크로 가져다 쓴다 (공식 매뉴얼 기반) |
| [docs/kernel/](./docs/kernel/README.md) | cgroup v2, 마운트 propagation, OverlayFS 사례 (공통 개념 2편 + 사례 1편) |
| [learning-modern-linux/](./book/learning-modern-linux/README.md) | 클라우드 네이티브 환경을 전제로 리눅스를 한 바퀴 도는 개론 — 커널·셸·접근 제어·파일시스템·네트워크·관측 (책 기반) |
| [tlpi_the-linux-programming-interface/](./book/tlpi_the-linux-programming-interface/README.md) | 명령 아래의 시스템 콜 층 — 파일 I/O·파일 속성·ACL·시그널·세션·자원 제한·데몬·IPC·소켓을 시스템 콜과 glibc 함수로. `learning-modern-linux/` 가 명령, `linux-kernel-programming/` 이 커널 구현을 맡는다 (책 기반) |
| [linux-kernel-programming/](./book/linux-kernel-programming/README.md) | 커널 개발자 관점의 리눅스 내부 — LKM 모듈 개발, 커널 빌드, 메모리 관리, CPU 스케줄러, 동기화 (책 기반) |
| [container-security/](../08_cloud/book/container-security/README.md) | 보안 관점의 컨테이너 — 커널 기초(namespace·cgroup·root 변경) 위의 이미지·공급망·런타임·통신 보안 (책 기반) |
| [learning-coredns/](../08_cloud/book/learning-coredns/README.md) | 이름 해석의 *서버* 편 — Corefile·플러그인 체인·존 데이터·쿠버네티스 연동. resolver 클라이언트 측(네트워크 로드맵 1단계·N&K 04-03 §5)과 편을 나눠 가진다 (책 기반) |
| [systems-performance/](./book/systems-performance/README.md) | 성능 분석가 관점의 시스템 성능 — 방법론·CPU·메모리·디스크·네트워크·클라우드·고급 추적(perf·Ftrace·BPF) (책 기반) |
| [learning-ebpf/](./book/learning-ebpf/README.md) | eBPF 프로그램 자체의 구조 — 맵·헬퍼·`bpf()` 시스템 콜·verifier·BTF·CO-RE·부착 유형과 네트워킹·보안 활용. `systems-performance/` 가 도구로 쓰는 BCC·bpftrace 의 아래층 (책 기반) |
| [paw_packet-analysis-wireshark/](./book/paw_packet-analysis-wireshark/README.md) | 선 위의 프레임을 떠서 프로토콜별로 읽는 법 — Wireshark 캡처·필터·TCP·TLS·응용 프로토콜·WLAN·보안 분석 (책 기반) |
| [cntd_computer-networking-top-down/](./book/cntd_computer-networking-top-down/README.md) | 프로토콜을 위에서 아래로 훑는 규격 축 — 응용·트랜스포트·네트워크 계층의 원리와 라우팅·SDN·망 관리. `paw_` 가 캡처로 확인하는 것을 여기서 규격으로 배운다 (책 기반) |
| [npg_network-programming-with-go/](./book/npg_network-programming-with-go/README.md) | 같은 네트워크 장치를 Go 표준 라이브러리로 짜는 애플리케이션 축 — TCP·UDP·Unix 소켓, HTTP 클라이언트·서비스, TLS, 직렬화·로깅. `cntd_`·`tii_` 가 규격과 패킷으로 보이는 것을 여기서 `net` 패키지 코드로 옮긴다 (책 기반) |
| [network-fundamentals-lab/](./project/network-fundamentals-lab/README.md) | 고장이 장전된 채로 뜨는 containerlab 토폴로지 18편 — 증상에서 계층을 좁히는 훈련. N&K 정독본이 맡는 메커니즘을 깨뜨려 확인하는 축이다 (랩 저장소 기반) |
| [portal-tunnel/](./project/portal-tunnel/README.md) | 오픈소스 Go reverse tunnel 을 빌드해 띄우고 코드를 읽으며 기여까지 가는 시리즈 — 기초 개념·transport·TLS 신뢰 경계·identity 정책·SDK·코드 리뷰 (외부 저장소 기반) |
| [lampson-lab/](./project/lampson-lab/README.md) | SSH 고정 키 없이 워크로드 신원(SPIRE)으로 5분짜리 SSH 인증서를 받아 호스트의 역할 계정에 들어가는 참조 구현 정독 6편 — 신원 발급·step-ca 매핑·sshd 호스트·거부 테스트·만료와 열린 연결 (외부 저장소 기반) |
| [learning-modern-linux-lab/](./project/learning-modern-linux-lab/README.md) | 『Learning Modern Linux』 정독 노트의 동작을 OrbStack Debian 12·Rocky 9 머신에서 예측하고 확인하는 실습 기록 — 8장 로그 한 줄의 흐름(journald·rsyslog·logrotate)부터 (runners-lab `os/learning-modern-linux`) |



## 추천 읽기 경로

백엔드·Kubernetes 운영자는 [OS 로드맵](os-keywords.md)의 1~4단계를 먼저 따릅니다. OOMKilled·CPU throttling은 `docs/kernel/`, Pod 격리는 [container-security](../08_cloud/book/container-security/README.md) 04-01을 봅니다. DNS·Service·NAT 문제는 [N&K 정독본](../08_cloud/book/networking-and-kubernetes/README.md), 성능 병목은 `book/systems-performance/`으로 확장합니다.

커널 모듈 작성이나 커널 소스 자체가 목적일 때만 `book/linux-kernel-programming/`을 별도 정독합니다. 컨테이너 보안 옵션과 공급망 위험을 판단하려면 1~2단계 뒤 `book/container-security/`으로 이동합니다.



## 관련 문서

- [OS 학습 로드맵](os-keywords.md) — OS 전체를 가로지르는 추천 순서
- [write/ MOC](../README.md) — 전체 카테고리 지도
- [08_cloud/kubernetes/](../08_cloud/kubernetes/README.md) — 본 카테고리의 활용처
