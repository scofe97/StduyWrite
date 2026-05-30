---
title: Istio 학습 MOC
tags: [moc, service-mesh, istio, envoy, xds, ambient]
status: final
related:
  - ../README.md
  - ../01_foundation/README.md
  - ../04_extension/README.md
  - ../05_comparison/README.md
updated: 2026-05-30
---

# Istio 학습 MOC

---

> Envoy의 풍부한 기능과 넓은 제어 표면을 가진 Istio를, 설치로 진입 장벽을 낮춘 뒤 구조를 이해하고 외부 진입·내부 제어·운영·고급 확장 순서로 한 폴더에 모았습니다. 본 묶음을 끝내면 "Istio를 어떻게 설치하고, istiod와 Envoy가 무엇을 하며, 트래픽·보안·관측성·성능·확장을 각각 어떤 CRD로 다루는가" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Istio는 Linkerd보다 다루는 표면이 훨씬 넓습니다. 설치 방법만 셋(istioctl·Helm·구 IstioOperator)이고, 트래픽 제어는 VirtualService·DestinationRule·Gateway 등 여러 CRD로 갈라지며, EnvoyFilter·WasmPlugin 같은 저수준 확장까지 열려 있습니다. 이 넓이를 한 폴더에 펼치되 **진입 순서**로 정렬했습니다. 먼저 설치(01)로 손에 잡히는 것을 만들고, 그 위에서 아키텍처(02)를 이해한 뒤, 외부 진입(03)→내부 라우팅(04)→레질리언스(05)로 트래픽을 좁혀 들어갑니다. 보안(06)·관측성(07)·트러블슈팅(08)은 운영 축이고, 성능(09)·EnvoyFilter(10)는 한계까지 밀어붙일 때 펴는 고급 카드입니다.

공통 개념(mTLS·Gateway API)은 [`01_foundation`](../01_foundation/README.md)이 SSOT이고, 멀티클러스터·VM·Ambient 같은 메시 경계 확장 토픽은 [`04_extension`](../04_extension/README.md)으로 분리했습니다. 이 폴더는 단일 클러스터 안에서의 Istio 운영에 집중합니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 설치 | 01-01 | [Istio 설치](01-01.Istio%20%EC%84%A4%EC%B9%98.md) | istioctl·Helm·IstioOperator 비교, 메시 모드 |
| 01 설치 | 01-02 | [Istio 설치 실습](01-02.Istio%20%EC%84%A4%EC%B9%98%20%EC%8B%A4%EC%8A%B5.md) | 설치 hands-on |
| 02 아키텍처 | 02-01 | [Istio 아키텍처](02-01.Istio%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | istiod 통합 진화, xDS 네 API, Envoy |
| 02 아키텍처 | 02-02 | [Istio 아키텍처 실습](02-02.Istio%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EC%8B%A4%EC%8A%B5.md) | 컴포넌트 관찰 hands-on |
| 03 진입 | 03-01 | [Istio Ingress Gateway](03-01.Istio%20Ingress%20Gateway.md) | 외부→내부 트래픽 수신 |
| 03 진입 | 03-02 | [Ingress Gateway 실습](03-02.Istio%20Ingress%20Gateway%20%EC%8B%A4%EC%8A%B5.md) | Gateway 구성 hands-on |
| 04 트래픽 | 04-01 | [Istio 트래픽 관리](04-01.Istio%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EA%B4%80%EB%A6%AC.md) | VirtualService·DestinationRule, 버전 분기 |
| 04 트래픽 | 04-02 | [트래픽 관리 실습](04-02.Istio%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EA%B4%80%EB%A6%AC%20%EC%8B%A4%EC%8A%B5.md) | 카나리·미러링 hands-on |
| 05 레질리언스 | 05-01 | [Istio 레질리언스](05-01.Istio%20%EB%A0%88%EC%A7%88%EB%A6%AC%EC%96%B8%EC%8A%A4.md) | 타임아웃·재시도·서킷 브레이커 |
| 05 레질리언스 | 05-02 | [레질리언스 실습](05-02.Istio%20%EB%A0%88%EC%A7%88%EB%A6%AC%EC%96%B8%EC%8A%A4%20%EC%8B%A4%EC%8A%B5.md) | 실패 주입 hands-on |
| 06 보안 | 06-01 | [Istio 보안](06-01.Istio%20%EB%B3%B4%EC%95%88.md) | mTLS·PeerAuthentication·인가 |
| 06 보안 | 06-02 | [보안 실습](06-02.Istio%20%EB%B3%B4%EC%95%88%20%EC%8B%A4%EC%8A%B5.md) | 정책 적용 hands-on |
| 07 관측성 | 07-01 | [Istio 관측성](07-01.Istio%20%EA%B4%80%EC%B8%A1%EC%84%B1.md) | Envoy 텔레메트리, Telemetry API |
| 07 관측성 | 07-02 | [관측성 실습](07-02.Istio%20%EA%B4%80%EC%B8%A1%EC%84%B1%20%EC%8B%A4%EC%8A%B5.md) | 메트릭·트레이스 hands-on |
| 08 트러블슈팅 | 08-01 | [Istio 트러블슈팅](08-01.Istio%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | 장애 진단 첫 5분 순서 |
| 08 트러블슈팅 | 08-02 | [트러블슈팅 실습](08-02.Istio%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85%20%EC%8B%A4%EC%8A%B5.md) | istioctl 진단 hands-on |
| 09 성능 | 09-00 | [점검](09-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Istio%20%EC%84%B1%EB%8A%A5%20%ED%8A%9C%EB%8B%9D%29.md) | 09장 진입 전 자가 점검 |
| 09 성능 | 09-01 | [Istio 성능 튜닝](09-01.Istio%20%EC%84%B1%EB%8A%A5%20%ED%8A%9C%EB%8B%9D.md) | xDS 병목, 컨트롤 플레인 부하 |
| 10 확장 | 10-00 | [점검](10-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Istio%20EnvoyFilter%29.md) | 10장 진입 전 자가 점검 |
| 10 확장 | 10-01 | [Istio EnvoyFilter](10-01.Istio%20EnvoyFilter.md) | 저수준 제어를 여는 시점과 한계 |
| 10 확장 | 10-02 | [EnvoyFilter 실습](10-02.Istio%20EnvoyFilter%20%EC%8B%A4%EC%8A%B5.md) | 필터 적용 hands-on |

처음 진입자는 01→02 순서로 설치·구조를 잡은 뒤, 자기 목적(트래픽/보안/관측성)으로 점프합니다. 이미 Istio를 운영 중이라면 08 트러블슈팅·09 성능에서 자기 환경의 약한 지점을 점검하고, 고수준 API로 부족할 때 10 EnvoyFilter로 내려갑니다. Helm 차트 실습 자료는 상위 [`helm/`](../helm/) 폴더에 있습니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Istio | 1.24 계열 (Ambient GA) | Ambient는 1.24 GA |
| 설치 | istioctl·Helm 권장 | in-cluster IstioOperator는 1.24 제거 |
| Kubernetes | 1.28 이상 | |
| 실습 클러스터 | 개인 GCP K8s | [`gcp` 스킬](../../../../.claude/skills/gcp/SKILL.md) |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`01_foundation`](../01_foundation/README.md)의 프록시 모델·mTLS·Gateway API를 설명할 수 있습니다.
2. `kubectl`로 리소스를 적용·조회해 본 경험이 있습니다.

## 면접 대비 체크리스트

> 본 묶음을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. istiod가 v1.0의 네 컴포넌트(Pilot·Citadel·Galley·Mixer)를 통합하면서 무엇이 바뀌었습니까? Mixer 폐기가 가용성에 준 영향은?
2. xDS 네 API(LDS·RDS·CDS·EDS)는 각각 Envoy의 무엇을 갱신합니까?
3. VirtualService와 DestinationRule의 역할 차이는? 카나리 배포는 어느 쪽으로 선언합니까?
4. PeerAuthentication의 mTLS 모드(STRICT·PERMISSIVE)는 점진 적용에서 왜 중요합니까?
5. EnvoyFilter를 써야 하는 순간은 언제이고, 그 위험은 무엇입니까?

각 질문에 막히면 해당 장으로 돌아갑니다.
