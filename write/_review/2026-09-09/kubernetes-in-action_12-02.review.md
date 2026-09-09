---
title: "Ingress TLS·설정·IngressClass — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, ingress, tls, ingressclass]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/12-02.Ingress TLS·설정·IngressClass.md"
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

# Ingress TLS·설정·IngressClass — 복습 회차 1

> 원본: [Ingress TLS·설정·IngressClass](../../08_cloud/book/kubernetes-in-action/12-02.Ingress%20TLS%C2%B7%EC%84%A4%EC%A0%95%C2%B7IngressClass.md)
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

Ingress 가 TLS 를 어디서 끝내는지, 표준 스키마가 담지 못하는 설정을 어디로 밀어냈는지, 컨트롤러가 여럿일 때 누가 처리할지를 설명할 수 있는 상태.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — Q2 와 Q5 가 같은 뿌리다 — 구현이 여럿이면 하나의 스키마로 못 담는다. 그 대가가 annotation 과 IngressClass 다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: Ingress 에서 HTTPS 를 지원하는 두 방식(passthrough·termination)은 무엇이 다른가. 표준은 어느 쪽인가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*
---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: Ingress `spec` 에 필드가 넷(`defaultBackend`·`rules`·`tls`·`ingressClassName`)뿐인 이유는 무엇인가. 나머지 설정은 어떻게 하는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: TLS termination 에서 백엔드 파드가 HTTPS 를 몰라도 되는 이유는 무엇인가. 인증서·키는 어떻게 프록시에 전달하는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: 클러스터에 컨트롤러가 여럿일 때 어느 컨트롤러가 특정 Ingress 를 처리할지 어떻게 정하는가. Ingress 가 클래스를 안 적으면 어떻게 되는가.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: Service 는 쿠키 기반 세션 어피니티를 못 하는데 Ingress 는 할 수 있는 이유는 무엇인가.

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

**passthrough** 는 TLS 연결을 프록시가 통과시켜 **백엔드 파드가 직접 TLS 를 끝내는** 방식이다.
**termination** 은 **프록시가 TLS 를 끝내고** 백엔드로는 평문 HTTP 를 보낸다.

**termination 이 표준**이다 — 대부분의 컨트롤러가 지원한다. passthrough 는 쿠버네티스에 표준 방식이 없어 **컨트롤러별 annotation 과 플래그**에 의존하는 비표준 기능이다. Nginx 라면 `ssl-passthrough` annotation 과 `--enable-ssl-passthrough` 플래그다 — 원본 §정답 1.

### 정답 2

**모든 Ingress 구현의 모든 설정 옵션을 하나의 스키마에 담기란 사실상 불가능하기 때문**이다.

그래서 공통으로 필요한 넷만 spec 에 두고, 구현별 세부 설정(인증·세션 어피니티·URL 재작성·CORS 등)은 **annotation 이나 컨트롤러가 제공하는 커스텀 오브젝트**로 붙인다 — 원본 §정답 3.

### 정답 3

termination 에서는 **클라이언트↔프록시 구간만 TLS 로 암호화**되고, 프록시가 복호화한 뒤 백엔드 파드로는 **평문 HTTP** 를 보낸다. 따라서 파드의 애플리케이션은 HTTPS 를 처리할 필요가 없다.

인증서와 개인 키는 **`tls` 타입 Secret**(`tls.crt`·`tls.key`)으로 만들어 Ingress 의 `spec.tls[].secretName` 으로 참조해 프록시에 전달한다. `tls.hosts` 는 **인증서 이름과 일치해야** 한다 — 원본 §정답 2.

### 정답 4

각 Ingress 의 **`spec.ingressClassName`** 에 IngressClass 이름을 적고, **IngressClass 가 컨트롤러 이름을 지정**하므로 그 컨트롤러가 이 Ingress 를 처리한다.

클래스를 안 적으면 **`ingressclass.kubernetes.io/is-default-class: "true"`** annotation 이 붙은 기본 IngressClass 가 적용된다. **기본 클래스도 없고 지정도 안 하면 어떤 컨트롤러도 처리하지 않아 주소가 안 잡힌다** — 원본 §정답 5.

### 정답 5

Service 는 **OSI L4(TCP·UDP)** 에서 동작해 HTTP 쿠키를 이해하지 못하므로 클라이언트 IP 기반 어피니티만 가능하다.

Ingress 는 **L7(HTTP)** 에서 동작하므로 요청의 쿠키를 읽고 쓸 수 있어 쿠키 기반 세션 어피니티를 지원한다. Nginx 라면 `affinity: cookie` annotation 으로 켠다 — 원본 §정답 4.

11-01 Q5 와 같은 한 문장이 답이다 — **Service 는 L4, Ingress 는 L7.**
