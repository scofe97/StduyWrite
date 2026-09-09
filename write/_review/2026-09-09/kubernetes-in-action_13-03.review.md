---
title: "TLS·기타 프로토콜·크로스 네임스페이스·mesh — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, gateway-api, tls, mesh]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/13-03.TLS·기타 프로토콜·크로스 네임스페이스·mesh.md"
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

# TLS·기타 프로토콜·크로스 네임스페이스·mesh — 복습 회차 1

> 원본: [TLS·기타 프로토콜·크로스 네임스페이스·mesh](../../08_cloud/book/kubernetes-in-action/13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md)
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

게이트웨이가 무엇을 볼 수 있느냐가 무엇을 라우팅할 수 있느냐를 정한다는 것을, TLS 종료 지점과 Route 종류로 설명할 수 있는 상태.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — Q1 과 Q3 이 한 축이다 — 암호를 어디서 푸느냐가 게이트웨이가 볼 수 있는 것을 정하고, 그것이 쓸 수 있는 Route 를 정한다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: TLS termination 과 passthrough 는 무엇이 다른가. 각각 어떤 Route 를 쓰고 라우팅에 쓸 수 있는 정보는 무엇인가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*
---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: Gateway API 가 north/south 트래픽에서 east/west(mesh) 트래픽으로 확장된 방식은 무엇인가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: TCPRoute·TLSRoute 가 HTTPRoute 와 달리 내용 기반 라우팅을 못 하는 이유는 무엇인가. 그래도 할 수 있는 것은.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: 다른 네임스페이스의 Gateway 를 공유하는 것과 다른 네임스페이스의 서비스를 백엔드로 쓰는 것은 허가 방식이 어떻게 다른가. `ReferenceGrant` 는 어느 네임스페이스에 만드는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: Istio 가 UDPRoute·GRPCRoute 를 지원하는지 어떻게 확인하는가.

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

**termination** 은 게이트웨이가 TLS 를 종료(복호화)해 백엔드로 평문 HTTP 를 보낸다. 게이트웨이가 내용을 이해하므로 **HTTPRoute** 로 경로·헤더까지 라우팅한다. listener protocol 은 **HTTPS** 다.

**passthrough** 는 TLS 를 그대로 통과시켜 백엔드가 종료한다. 게이트웨이는 **SNI 의 호스트명만** 알고 안의 HTTP 는 모르므로 **TLSRoute** 로 호스트명 기반 라우팅만 한다. listener protocol 은 **TLS** 다.

암호화가 백엔드까지 이어지므로 **passthrough 쪽이 더 안전하다** — 원본 §정답 1.

### 정답 2

Route 오브젝트의 **`parentRefs` 에 Gateway 대신 Service 를 두는 것**이 GAMMA 의 해법이다.

north/south 에서는 parentRef 가 Gateway 를 가리켜 외부→서비스 트래픽을 관리한다. east/west 에서는 parentRef 의 kind 를 **`Service`** 로, group 을 **빈 문자열(`""`)** 로 둔다. 그러면 그 서비스로 향하는 **서비스 간 트래픽**에 rule 과 필터가 적용된다.

덕분에 **같은 API 로 mesh 내부 통신까지 재설정·재배포 없이** 관리한다 — 원본 §정답 5.

### 정답 3

게이트웨이가 **패킷 내용을 모르기 때문**이다 — TCP 는 애초에 페이로드가 불투명하고, TLS 는 암호화돼 **SNI 호스트명 외엔 안 보인다.**

그래서 TLSRoute 는 **호스트명으로만**, TCPRoute 는 **아무 조건 없이** 라우팅한다. 다만 둘 다 **백엔드를 여럿 두고 weight 를 주면 트래픽을 나눌 수 있다** — 원본 §정답 2.

### 정답 4

**Gateway 공유** 는 Gateway 오브젝트 **자체에서** 허가한다 — 각 listener 의 `allowedRoutes.namespaces.from` 을 `Same`·`All`·`Selector` 로 설정한다.

**다른 네임스페이스의 서비스를 백엔드로 쓰는 것** 은 Service 오브젝트가 아니라 별도 **`ReferenceGrant`** 오브젝트로 허가한다. ReferenceGrant 는 참조 **대상(referent)의 네임스페이스**(즉 서비스가 있는 네임스페이스)에 만들고, `from` 에 참조하는 쪽, `to` 에 참조되는 쪽을 적는다 — 원본 §정답 4.

### 정답 5

**Route 오브젝트를 만든 뒤 그 status 를 본다.** 지원하는 컨트롤러가 처리하면 status 에 조건이 채워지고, 처리하는 컨트롤러가 없으면 **status 가 빈 채로** 남는다.

원서 작성 시점에는 Istio 가 둘 다 지원하지 않아 두 Route 모두 status 가 비어 있었다. **현재는 GRPCRoute 가 Stable 이라 status 가 채워지고, UDPRoute 만 여전히 빈 status 로 남는다.** 그래서 지원 여부는 **문서가 아니라 이 status 로** 확인한다 — 원본 §정답 3.
