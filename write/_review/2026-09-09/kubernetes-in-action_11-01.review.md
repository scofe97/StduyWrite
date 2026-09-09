---
title: "Service 기초 — 파드 통신·ClusterIP·세션 어피니티 — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, service, clusterip]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/11-01.Service 기초 — 파드 통신·ClusterIP·세션 어피니티.md"
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

# Service 기초 — 파드 통신·ClusterIP·세션 어피니티 — 복습 회차 1

> 원본: [Service 기초 — 파드 통신·ClusterIP·세션 어피니티](../../08_cloud/book/kubernetes-in-action/11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md)
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

파드끼리의 flat 통신 위에서 Service 가 무엇을 추가하는지 — 가상 IP·selector·어피니티·DNS 를 각각의 계층으로 설명할 수 있는 상태.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — Service 는 L4 라는 한 문장이 Q1·Q5 를 동시에 설명한다. 그 한 문장이 서는지 본다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: Service 의 cluster IP 를 `ping` 하면 왜 응답이 없는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*
---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: 파드끼리 패킷을 주고받을 때 SNAT·DNAT 가 일어나지 않는다는 것이 애플리케이션에 어떤 의미인가. 이를 flat 네트워크라 부르는 이유는.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: Service 를 이름만으로 resolve 할 수 있는 이유는. `search` 줄과 `ndots` 가 각각 어떤 역할을 하는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: Service 가 어느 파드를 뒷받침으로 삼을지는 무엇이 정하는가. `kubectl expose pod` 로 만든 Service 의 selector 가 나중에 문제가 되는 상황을 예로 들라.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: 세션 어피니티로 쿠키 기반을 못 쓰고 ClientIP 만 되는 이유는 무엇인가.

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

cluster IP 는 실제 인터페이스에 붙은 IP 가 아니라 **가상 IP** 다. Service 에 정의된 **포트와 짝지어질 때만** 의미를 갖고, iptables·IPVS 규칙이 그 `IP:포트` 조합을 파드로 리다이렉트한다. ICMP(ping)에는 대응하는 포트 규칙이 없으므로 패킷이 어디로도 가지 못해 100% 손실이 난다 — 원본 §정답 3.

### 정답 2

출발지·목적지 IP 와 포트가 **그대로 유지**된다. 받는 파드가 보낸 파드의 진짜 IP 를 출발지로 보므로, 애플리케이션이 상대를 그대로 식별하고 접근 로그에 실제 IP 를 남길 수 있다.

flat 이라 부르는 이유는 노드가 지리적으로 흩어져 여러 라우터를 거치더라도 **파드 관점에서는 하나의 스위치에 물린 LAN 처럼** NAT 없이 서로 닿기 때문이다 — 원본 §정답 1.

### 정답 3

파드의 `/etc/resolv.conf` 에 있는 **`search` 줄**(`kiada.svc.cluster.local svc.cluster.local cluster.local …`)이 짧은 이름 뒤에 도메인 접미사를 차례로 붙여 매칭될 때까지 시도한다.

**`options ndots:5`** 는 점이 5개 미만인 이름을 상대 이름으로 보고 search 접미사를 붙이게 한다. 그래서 `quiz` 만 적어도 `quiz.kiada.svc.cluster.local` 로 확장돼 resolve 된다 — 원본 §정답 5.

### 정답 4

Service 오브젝트에 적은 **label selector** 가 정한다. selector 에 맞는 라벨을 가진 파드가 자동으로 포함된다.

`kubectl expose pod quiz` 는 그 파드의 라벨을 **전부** selector 로 가져온다 — `app=quiz,rel=stable` 둘 다다. 나중에 canary 를 배포하면 그 라벨은 `rel: canary` 라 stable 과 다르다. 이 selector 에 맞지 않으므로 트래픽이 canary 로 가지 않는다. `kubectl set selector` 로 `app=quiz` 만 남겨 좁혀야 한다 — 원본 §정답 2.

### 정답 5

Service 는 **OSI 전송 계층(TCP·UDP)** 에서 동작한다. HTTP 쿠키는 애플리케이션 계층 개념이라 전송 계층에서는 보이지 않는다. 그래서 Service 는 쿠키를 이해하지 못하고, 어피니티를 걸 수 있는 유일한 기준이 패킷에서 바로 읽히는 **클라이언트 IP** 다.

`sessionAffinity: ClientIP` 로 걸며 기본 지속 시간은 **3시간** 이다 — 원본 §정답 4.
