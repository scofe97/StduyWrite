---
title: 09_cloud/service-mesh — Service Mesh 실전
tags: [moc, service-mesh, istio, linkerd, cilium, mtls]
status: final
source:
  - ../../../poc/03_CloudNative/03-service-mesh/README.md@8ac9e97
related:
  - ../README.md
  - ../kubernetes/README.md
updated: 2026-04-19
---

# 09_cloud/service-mesh
> 마이크로서비스 간 통신 문제(보안·신뢰성·관측성)를 인프라 계층에서 풀기 위한 Service Mesh를 Linkerd·Istio·Cilium 세 축으로 다룬다. 기초 개념부터 시작해 각 구현체의 구조와 운영, 프로덕션 도입 전략까지 이어진다.

이 카테고리는 Kubernetes 기본 네트워킹 위에 한 층 더 올라가는 영역이다. Pod 네트워크, Service, Ingress, Gateway API의 기본 연결성과 진입 구조는 `kubernetes` 카테고리에서 먼저 다루고, 여기서는 그 위에 서비스 간 트래픽 정책, mTLS, 관측성을 어떻게 얹는지에 집중한다.



## 학습 흐름
> 공통 기반에서 시작해 Linkerd, Istio, 확장 토픽, 비교·도입 판단으로 넘어가는 흐름을 안내한다.


### Part 1 — 기반 (Ch01~04)
왜 서비스 메시가 등장했는지, 데이터/컨트롤 플레인의 역할 분리, Gateway API와 mTLS라는 공통 토대를 잡는다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01 | [서비스 메시 기초](./01-01.서비스%20메시%20기초.md) | 마이크로서비스 통신 복잡도를 인프라로 어떻게 옮기는가? |
| 02 | [프록시 아키텍처](./02-01.프록시%20아키텍처.md) | 사이드카·앰비언트·에이전트의 트레이드오프는? |
| 03 | [Gateway API와 트래픽](./03-01.Gateway%20API와%20트래픽.md) | Ingress의 한계를 Gateway API가 어떻게 뛰어넘는가? |
| 04 | [mTLS와 제로 트러스트](./04-01.mTLS와%20제로%20트러스트.md) | 서비스 간 통신 신뢰는 어떻게 자동화되는가? |

### Part 2 — Linkerd (Ch05~09)
단순함과 낮은 오버헤드를 무기로 한 Linkerd의 구조·운영·보안·관측성.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05 | [Linkerd 아키텍처](./05-01.Linkerd%20아키텍처.md) | Rust 마이크로 프록시가 선택된 이유는? |
| 06 | [Linkerd 설치](./06-01.Linkerd%20설치.md) | 메시 주입과 업그레이드 절차는? |
| 07 | [Linkerd 트래픽](./07-01.Linkerd%20트래픽.md) | 가중치 라우팅과 재시도를 어떻게 선언하는가? |
| 08 | [Linkerd 보안](./08-01.Linkerd%20보안.md) | mTLS·권한 정책은 어떻게 맞물리는가? |
| 09 | [Linkerd 관측성](./09-01.Linkerd%20관측성.md) | Golden Metrics를 어떻게 확보하는가? |

### Part 3 — Istio (Ch10~12)
먼저 설치로 진입 장벽을 낮추고, 구조를 이해한 뒤, 외부 진입과 내부 제어, 운영·고급 제어 순서로 Istio를 파고든다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 10 | [Istio 설치](./10-01.Istio%20설치.md) | 어떤 설치 경로와 메시 모드를 선택해야 하는가? |
| 10 | [Istio 아키텍처](./10-02.Istio%20아키텍처.md) | 설치 뒤에 어떤 제어 플레인과 데이터 플레인이 실제로 동작하는가? |
| 11 | [Istio Ingress Gateway](./11-01.Istio%20Ingress%20Gateway.md) | 메시 외부에서 내부로 트래픽을 어떻게 받는가? |
| 11 | [Istio 트래픽 관리](./11-02.Istio%20트래픽%20관리.md) | VirtualService·DestinationRule로 내부 라우팅과 버전 분기를 어떻게 선언하는가? |
| 11 | [Istio 레질리언스](./11-03.Istio%20레질리언스.md) | 실패 전파를 막기 위한 타임아웃·재시도·서킷 브레이커를 어떻게 조합하는가? |
| 12 | [Istio 보안](./12-01.Istio%20보안.md) | mTLS·인증·인가를 어떤 기준선으로 설계하는가? |
| 12 | [Istio 관측성](./12-02.Istio%20관측성.md) | Envoy가 만든 텔레메트리를 어떻게 읽고 연결하는가? |
| 12 | [Istio 트러블슈팅](./12-03.Istio%20트러블슈팅.md) | 메시 장애 진단의 첫 5분을 어떤 순서로 보낼 것인가? |
| 12 | [Istio 성능 튜닝](./12-04.Istio%20성능%20튜닝.md) | xDS 병목과 컨트롤 플레인 부하를 어디서 줄이는가? |
| 12 | [Istio EnvoyFilter](./12-05.Istio%20EnvoyFilter.md) | 고수준 API가 닿지 않는 제어를 언제, 어디까지 열어야 하는가? |

### Part 4 — 확장 (Ch13)
단일 클러스터 밖으로 메시 경계를 넓히는 확장 토픽을 묶어 읽는다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 13 | [멀티클러스터](./13-01.멀티클러스터.md) | 메시 경계를 여러 클러스터로 어떻게 넓히는가? |
| 13 | [Istio VM 통합](./13-02.Istio%20VM%20통합.md) | K8s 바깥 워크로드를 메시에 합류시키는 법은? |
| 13 | [Istio Ambient Mesh](./13-03.Istio%20Ambient%20Mesh.md) | 사이드카리스 전환의 조건과 득실은? |

### Part 5 — 비교·eBPF·도입 (Ch14)
세 구현체를 비교하고, eBPF 대안을 이해한 뒤, 프로덕션 패턴과 도입 판단으로 마무리한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 14 | [비교 매트릭스](./14-01.비교%20매트릭스.md) | Linkerd·Istio·Cilium의 역량은 어디서 갈라지는가? |
| 14 | [eBPF와 Cilium](./14-02.eBPF와%20Cilium.md) | 커널 계층에서 메시를 구현하면 무엇이 바뀌는가? |
| 14 | [프로덕션 패턴](./14-03.프로덕션%20패턴.md) | 현업에서 어떤 구성이 검증됐는가? |
| 14 | [도입 전략과 의사결정](./14-04.도입%20전략과%20의사결정.md) | 조직·규모·역량을 기준으로 무엇을 택하는가? |
| 14 | [Cilium과 Istio Ambient 통합 전략](./14-05.Cilium과%20Istio%20Ambient%20통합%20전략.md) | 두 도구를 같이 쓸 때 책임을 어디서 가르고 정책을 어떻게 겹치는가? ([인터랙티브 시각화](./14-05-mesh-integration.html)) |



## 심화 탐구 (deepdive/)
> 각 장과 짝을 이루는 점검.md와 실습.md 문서의 구성 원칙을 설명한다.


각 장에는 `deepdive/` 하위에 짝을 이루는 문서가 있다. 기초 개념 장(Ch01~06)과 Istio 성능 튜닝은 점검 질문 중심의 `점검.md`가 붙고, Linkerd·Istio 운영 장은 hands-on 절차 중심의 `실습.md`가 붙는다. EnvoyFilter 이후 확장·비교 파트는 `실습.md`와 `점검.md`를 함께 둔다. 어느 쪽이든 상단 `## 실습 환경` 섹션만 환경 특화 명령을 담고 본문은 범용 CLI로 작성되어 환경 교체가 쉽다.



## 실습 환경
> 개인 GCP K8s 클러스터(dev-server 1~3)를 기반으로 한 실습 환경 구성을 안내한다.


기초 챕터(Part 1)와 Linkerd·Istio 설치·트래픽 실험은 개인 GCP K8s 클러스터(dev-server 1~3)에서 수행한다. 멀티클러스터(Ch13-01)·VM 통합(Ch13-02)은 추가 GCE VM을 스핀업해 진행한다. 환경 특화 명령은 각 심화 문서 `## 실습 환경` 섹션에만 두고, 본문은 `kubectl`·istioctl·linkerd CLI 범용 명령으로 쓴다. 클러스터 상세는 [`gcp` 스킬 문서](../../../../.claude/skills/gcp/SKILL.md) 참조.



## 관련 문서
> 본 카테고리의 전제가 되는 kubernetes MOC와 Ingress 관련 문서를 안내한다.


- [kubernetes MOC](../kubernetes/README.md) — 본 카테고리의 전제. Pod·Service·Ingress 이해가 선행돼야 한다
- [Ingress와 Gateway API](../kubernetes/04-06.Ingress와%20Gateway%20API.md) — 03-01과 주제 겹침, K8s 진입 계층 관점에서 본 서술
