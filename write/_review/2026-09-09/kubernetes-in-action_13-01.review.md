---
title: "Gateway API 개념과 Gateway 배포 — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, gateway-api, istio]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/13-01.Gateway API 개념과 Gateway 배포.md"
round: 1
round_date: 2026-09-09
prev_round_date: null
next_round_date: null
quality: null
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-09-09
---

# Gateway API 개념과 Gateway 배포 — 복습 회차 1

> 원본: [Gateway API 개념과 Gateway 배포](../../08_cloud/book/kubernetes-in-action/13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md)
> 회차 1 · 2026-09-09 · 이전 회차: 첫 회차
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 **파일 끝 §정답** 을 읽어라
> 3. 정답과 비교해 점수를 매긴다 (채점은 AI 가 한다)
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨
>
> **문항 출처** — 원본 §면접에서 받을 만한 질문 다섯을 5축(정의·동기·메커니즘·적용·함정)에 배치했다.
> 정답도 원본 §정답을 따르며, 노트가 책 밖에서 보탠 자리는 그 표시를 유지한다.

## 학습 목표

Gateway API 가 Ingress 에서 무엇을 떼어 내 무엇을 얻었는지를 역할 분리와 이식성 두 축으로 설명할 수 있는 상태.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — Ingress 가 겪은 문제(구현마다 다름)를 어떻게 제도로 막았는가가 Q3 다. Q2 의 역할 분리와 함께 이 편의 뼈대다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: Ingress 와 Gateway API 의 리소스는 어떻게 대응하는가. 서비스를 연결하는 방식에서 무엇이 다른가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*
---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: Route 를 별도 오브젝트로 분리해서 얻는 이점 셋은 무엇인가. 그중 가장 큰 것은.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: Gateway API 에서 release channel 과 support level 을 도입한 이유는 무엇인가. 둘은 각각 무엇을 보장하는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: Gateway 오브젝트를 만들면 Istio 가 무엇을 함께 만드는가. 그 프록시는 클러스터 전체가 쓰는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: 게이트웨이에 접속했는데 404 가 난다면 status 의 어디를 봐야 하는가. `attachedRoutes` 가 0 이면 무슨 뜻인가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

## 회차 종합 평가

### 1. SM-2 quality 점수 (0~5)

Q1~Q5 평균을 반올림, 또는 *가장 막힌 질문 기준* 으로 보수적으로.

**quality**: __

> Wozniak SM-2: 5=완벽, 4=정답+머뭇, 3=정답+힘듦, 2=오답+쉬워 보였음, 1=오답+정답 기억남, 0=완전 blackout.

### 2. 3축 메타인지 자가평가 (1~5)

| 축 | 점수 (1~5) | 메모 |
|----|----------|------|
| A. 면접 답변 가능성 | __ | |
| B. 그림 없이 말로 설명 | __ | |
| C. 다른 환경 응용 | __ | |

**평균**: __

### 3. 다음 회차 결정

| 현재 회차 | quality 5 | quality 4 | quality 3 | quality 0~2 |
|----------|----------|----------|----------|------------|
| 1 (첫 회차) | +14일 | +7일 | +3일 | +1일 (즉시 재학습) |

**다음 회차 날짜**: __ → 정한 값을 이 파일 frontmatter 의 `next_round_date` 에 반드시 쓴다.
이 필드가 비어 있으면 `learning-status.mjs` 가 다음 회차를 못 잡는다.

### 4. 졸업 판정

- [ ] 본 회차 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6
- [ ] `_mistakes.md` 에 본 문서 관련 미해결 패턴 0개

### 5. 오답 박제 → `_mistakes.md`

quality ≤ 3 인 질문을 `write/08_cloud/book/kubernetes-in-action/_mistakes.md` 에 append.

## 정답 (자답 후 펼치기)

> 다섯 문항에 *먼저 자답한 뒤* 읽습니다. 자답 없이 먼저 읽으면 학습 효과가 0 입니다.
> 정답을 문항 옆이 아니라 파일 끝에 모은 것은 Typora 가 raw HTML 접힘을 지원하지 않기 때문입니다 — 접기로는 가려지지 않습니다.

### 정답 1

**Ingress↔Gateway**, **IngressClass↔GatewayClass** 로 대응한다. 여기까지는 이름만 다르다.

차이는 **서비스 연결 방식**이다. Ingress 는 오브젝트 안에 백엔드 서비스를 **직접 적는다.** Gateway API 는 노출할 서비스 종류에 따라 **별도 Route 오브젝트**를 만들어 Gateway 와 서비스를 잇는다 — `HTTPRoute`·`TLSRoute`·`TCPRoute`·`UDPRoute`·`GRPCRoute` 가 그 종류다 — 원본 §정답 1.

### 정답 2

**첫째**, Gateway 오브젝트가 작게 유지되고 규칙이 성격별 Route 로 나뉜다. HTTP 외에 TLS·TCP·UDP·gRPC 도 직접 지원한다.
**둘째**, 관리 책임을 **역할별로** 나눌 수 있다 — Gateway 는 클러스터 관리자가, Route 는 개발자가 만든다.
**셋째**, Gateway 를 **네임스페이스 간에 공유**할 수 있어 IP 하나로 여러 네임스페이스의 서비스를 노출한다.

가장 큰 이점은 **둘째인 역할 분리**다. Ingress 에서는 이 책임을 나눌 수 없었다 — 원본 §정답 2.

### 정답 3

여러 구현이 있으면 동작·기능이 갈린다. **Ingress 에서 겪은 그 문제를 막으려고** 두 속성을 도입했다.

- **release channel** 은 API 의 **안정성**을 보장한다. `standard` 는 앞으로 안 바뀌고 `experimental` 은 바뀔 수 있다.
- **support level** 은 **이식성**을 보장한다. `core` 는 모든 구현이 지원해 전환이 자유롭고, `extended` 는 지원하기만 하면 동작이 같으며, `implementation-specific` 은 구현에 종속된다.

둘은 **별개 축**이다. standard 채널이어도 모든 구현이 지원하는 것은 아니기 때문이다 — 원본 §정답 3.

### 정답 4

Gateway 오브젝트를 만들면 컨트롤러가 대개 **LoadBalancer 서비스**를 만들어 연결한다. Istio 는 `kiada-istio` LoadBalancer 서비스와 `istio.io/gateway-name=kiada` 라벨을 가진 **파드(Envoy 프록시)** 를 만든다.

이 프록시는 **Gateway 오브젝트를 만든 네임스페이스에 배포되어 그 애플리케이션 트래픽에만 쓰이는 전용 프록시**다 — 클러스터 전체가 쓰는 시스템 프록시가 아니다. 다만 이는 Istio 구현 세부라 다른 provider 는 다를 수 있다 — 원본 §정답 4.

### 정답 5

Gateway status 뿐 아니라 **해당 listener 의 status** 도 봐야 한다. Gateway·listener conditions 에 오류가 없어도, listener status 의 **`attachedRoutes` 가 0 이면 그 listener 에 연결된 Route 가 하나도 없다**는 뜻이다.

Route 가 없으면 게이트웨이가 트래픽을 어디로 보낼지 몰라 **404 Not Found** 를 반환한다. HTTPRoute 를 만들어 Gateway 에 붙이면 해결된다 — 원본 §정답 5.
