---
title: Linkerd 학습 MOC
tags: [moc, service-mesh, linkerd, rust, mtls, observability]
status: final
related:
  - ../README.md
  - ../01_foundation/README.md
  - ../05_comparison/README.md
updated: 2026-05-30
---

# Linkerd 학습 MOC

---

> 단순함과 낮은 오버헤드를 무기로 한 Linkerd를 아키텍처·설치·트래픽·보안·관측성 다섯 축으로 한 폴더에 모았습니다. 본 묶음을 끝내면 "왜 Linkerd가 Rust 마이크로 프록시를 골랐고, 메시를 어떻게 주입하며, 트래픽·보안·관측성을 각각 무엇으로 푸는가" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Linkerd는 "서비스 메시는 단순해야 한다"는 한 가지 철학으로 모든 결정을 끌고 갑니다. Rust 마이크로 프록시 선택, 세 컴포넌트로 줄인 컨트롤 플레인, 자동 mTLS, Golden Metrics 기본 제공이 모두 그 철학의 다른 얼굴입니다. 그래서 Linkerd 문서들은 한 권의 이야기처럼 이어집니다. 구조(01)를 이해하고 설치(02)한 뒤, 그 위에서 트래픽(03)·보안(04)·관측성(05)을 차례로 얹습니다.

`03_istio`와 분리한 이유는 두 메시가 같은 문제를 정반대 방향에서 풀기 때문입니다. 한 폴더에 섞으면 "이건 Linkerd 방식, 저건 Istio 방식"을 매번 가려야 해서 학습 동선이 끊깁니다. 공통 개념(mTLS·Gateway API)은 [`01_foundation`](../01_foundation/README.md)이 SSOT이고, 여기서는 Linkerd 고유의 구현만 다룹니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 아키텍처 | 01-00 | [점검](01-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Linkerd%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%29.md) | 01장 진입 전 자가 점검 |
| 01 아키텍처 | 01-01 | [Linkerd 아키텍처](01-01.Linkerd%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Rust 마이크로 프록시, 3개 컴포넌트, EWMA |
| 02 설치 | 02-00 | [점검](02-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Linkerd%20%EC%84%A4%EC%B9%98%29.md) | 02장 진입 전 자가 점검 |
| 02 설치 | 02-01 | [Linkerd 설치](02-01.Linkerd%20%EC%84%A4%EC%B9%98.md) | 메시 주입, 업그레이드 절차 |
| 03 트래픽 | 03-01 | [Linkerd 트래픽](03-01.Linkerd%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | HTTPRoute 가중치 라우팅, 재시도 |
| 03 트래픽 | 03-02 | [Linkerd 트래픽 실습](03-02.Linkerd%20%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%8B%A4%EC%8A%B5.md) | 카나리 배포 hands-on |
| 04 보안 | 04-01 | [Linkerd 보안](04-01.Linkerd%20%EB%B3%B4%EC%95%88.md) | 자동 mTLS, 권한 정책 |
| 04 보안 | 04-02 | [Linkerd 보안 실습](04-02.Linkerd%20%EB%B3%B4%EC%95%88%20%EC%8B%A4%EC%8A%B5.md) | mTLS·정책 적용 hands-on |
| 05 관측성 | 05-01 | [Linkerd 관측성](05-01.Linkerd%20%EA%B4%80%EC%B8%A1%EC%84%B1.md) | Golden Metrics, Tap·Viz |
| 05 관측성 | 05-02 | [Linkerd 관측성 실습](05-02.Linkerd%20%EA%B4%80%EC%B8%A1%EC%84%B1%20%EC%8B%A4%EC%8A%B5.md) | 메트릭 수집·대시보드 hands-on |

순서대로 읽는 것을 권합니다. 구조(01)를 건너뛰면 왜 컴포넌트가 셋뿐인지, 왜 mTLS가 자동인지 같은 후속 장의 전제가 흔들립니다. 실습(`NN-02`)은 본문 개념을 직접 클러스터에서 확인하는 단계로, 본문을 먼저 읽고 진행합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Linkerd | 2.14 이상 | GAMMA(Gateway API) 지원 |
| Kubernetes | 1.28 이상 | |
| 실습 클러스터 | 개인 GCP K8s | [`gcp` 스킬](../../../../.claude/skills/gcp/SKILL.md) |

> 2024년부터 stable 바이너리는 BEL 라이선스(50인↑ 조직) 대상입니다. 학습은 edge 채널이나 소스 빌드로 우회할 수 있습니다(상세는 01-01).

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`01_foundation`](../01_foundation/README.md)의 mTLS·프록시 모델을 한 줄로 설명할 수 있습니다.
2. `kubectl`로 Pod·Deployment를 배포해 본 경험이 있습니다.

## 면접 대비 체크리스트

> 다섯 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Linkerd v1이 실패하고 v2가 Rust를 택한 이유는? 그 결과 프록시 크기·지연은 어떻게 달라졌습니까?
2. 컨트롤 플레인 세 컴포넌트(destination·identity·proxy-injector)는 각각 무엇을 합니까?
3. EWMA 로드밸런싱이 Round-Robin보다 나은 상황은?
4. Linkerd의 자동 mTLS는 어떤 절차로 인증서를 발급·갱신합니까(24시간 수명의 의미)?
5. Golden Metrics 네 지표는 무엇이며 왜 그 넷입니까?

각 질문에 막히면 해당 장으로 돌아갑니다.
