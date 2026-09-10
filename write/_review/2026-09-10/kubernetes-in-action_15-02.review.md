---
title: "Deployment 업데이트 — Recreate·RollingUpdate·maxSurge — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, deployment, rollingupdate, maxsurge]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/15-02.Deployment 업데이트 — Recreate·RollingUpdate·maxSurge.md"
round: 1
round_date: 2026-09-10
prev_round_date: null
next_round_date: null
quality: null
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-09-10
---

# Deployment 업데이트 — Recreate·RollingUpdate·maxSurge — 복습 회차 1

> 원본: [Deployment 업데이트 — Recreate·RollingUpdate·maxSurge](../../08_cloud/book/kubernetes-in-action/15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md)
> 회차 1 · 2026-09-10 · 이전 회차: 첫 회차
>
> **본 복습 규약 (Karpicke & Roediger 2006, testing effect):**
> 1. 각 질문에 *먼저 자기 답을 적어라* — 답을 보지 말 것
> 2. 자기 답 작성 후에만 **파일 끝 §정답** 을 읽어라
> 3. 정답과 비교해 점수를 매긴다 (채점은 AI 가 한다)
> 4. 회차 끝 종합 평가에서 다음 회차 날짜가 결정됨
>
> **문항 출처** — 원본 §면접에서 받을 만한 질문을 5축(정의·동기·메커니즘·적용·함정)에 배치했다.
> **정답은 원본 §정답을 축자로 옮겼다** — 요약하지 않는다. 노트가 책 밖에서 보탠 자리는 그 표시를 유지한다.
> 원본 9 문항 중 다섯을 골랐다. 남긴 넷(ReplicaSet 과의 반응 차이 · 새 ReplicaSet 생성 · 롤아웃 중 재적용 · `minReadySeconds` 트레이드오프)은 회차 2 의 몫이다.

## 학습 목표

[15-01](../../08_cloud/book/kubernetes-in-action/15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md)까지는 ReplicaSet 대비 이점이 안 보였습니다. 이점은 Pod 템플릿을 업데이트할 때 드러납니다 — ReplicaSet은 기존 파드에 반영 안 되지만, Deployment는 즉시 교체합니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — **두 숫자는 desired replicas 에 상대적이고, 반올림 방향이 서로 반대다** — Q1 과 Q4 가 이 한 문장에서 갈린다. 안전한 쪽으로 반올림된다는 규칙이 서는지 본다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: maxSurge와 maxUnavailable의 값은 무엇에 상대적인가요? 둘 다 0으로 두면 왜 안 되나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: Recreate와 RollingUpdate는 서비스 가용성 면에서 어떻게 다른가요? Recreate 중 클라이언트는 무엇을 겪나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: 파드가 삭제될 때 TERM 신호 전달과 EndpointSlice 정리는 어떤 순서로 일어나나요? `preStop` 훅이 필요한 이유는 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: maxSurge·maxUnavailable을 %로 줄 때 각각 어떻게 반올림되나요? 방향이 서로 반대인 이유는 무엇인가요? 기본값은요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: `maxUnavailable: 0`으로 뒀는데 배포 중 502가 관측됩니다. 원인으로 무엇을 의심해야 하나요? readinessProbe와 livenessProbe 중 어느 쪽을 넣어야 하며, 왜 그런가요?

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

### 2. 3축 메타인지 (1~5)

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

두 값은 **원하는 복제본 수에 상대적**입니다. replicas 3에 maxUnavailable 1이면 가용해야 할 수는 2개이며, 현재 파드가 몇 개든 상관없습니다.

둘 다 0으로 두면 안 되는 이유는 업데이트가 움직일 여지가 사라지기 때문입니다. maxSurge 0은 원하는 수를 초과하지 못하게 하고, maxUnavailable 0은 가용 수를 줄이지 못하게 합니다. 그러면 새 파드를 추가할 수도 옛 파드를 지울 수도 없어 롤아웃이 한 걸음도 나아가지 못합니다.

막는 방식은 두 갈래입니다. 직접 0을 적으면 API 검증이 거부하고, 퍼센트가 내림 때문에 0이 되는 경우는 컨트롤러가 `maxUnavailable`을 1로 보정해 롤아웃이 멈추지 않게 합니다.

> 원본 §정답 4 축자.

### 정답 2

Recreate는 모든 파드를 동시에 삭제합니다. 컨테이너가 다 끝난 뒤 새 파드를 동시에 만듭니다. 그 사이 **서비스가 불가**합니다. 클라이언트는 Ingress에서 `503 Service Temporarily Unavailable`을 받습니다. 클러스터 IP 로 직접 접근하면 연결 거부를 겪습니다. RollingUpdate는 옛 파드를 점진적으로 교체하되 새 파드가 준비된 뒤 다음 옛 파드를 지웁니다. 그래서 서비스가 파드 없이 남는 순간이 없습니다. 그래서 RollingUpdate가 기본입니다.

> 원본 §정답 2 축자.

### 정답 3

**동시에** 시작됩니다. kubelet이 컨테이너에 TERM을 보내는 것과 같은 시점에 컨트롤 플레인이 그 파드를 EndpointSlice에서 뺄지 판단하며, 두 경로는 서로를 기다리지 않습니다. 앱이 TERM을 받자마자 커넥션을 끊으면 전달 규칙이 아직 갱신 중인 노드에서 온 요청이 갈 곳을 잃습니다.

쿠버네티스는 종료 중 엔드포인트를 즉시 지우지 않고 `ready: false`로 표시해 로드밸런서가 새 트래픽을 보내지 않게 하지만, 전파 시차는 남습니다. `preStop`으로 몇 초를 벌면 그동안 앱이 계속 응답하면서 규칙 전파가 끝납니다. 이것은 공식 권고가 아니라 실무 관행입니다. `server.shutdown=graceful`을 함께 써 처리 중인 요청을 마저 끝냅니다.

> 원본 §정답 7 축자.

### 정답 4

%로 줄 때 maxSurge는 **올림**, maxUnavailable은 **내림**으로 절대 수를 계산합니다. 기본값은 둘 다 **25%**입니다.

replicas 10에 둘 다 25%를 준 경우로 보면 이렇습니다.

- maxSurge: 2.5를 올려 **3** → 업데이트 중 최대 13개
- maxUnavailable: 2.5를 내려 **2** → 항상 최소 8개 가용

공식 문서는 이유를 밝히지 않지만, 결과를 보면 **둘 다 가용성에 유리한 쪽으로 굴린** 것으로 읽힙니다. maxSurge는 크면 여유가 늘고 maxUnavailable은 크면 가용 파드가 줄어, 같은 기준이 반대 방향으로 나타납니다. 반대로 정했다면 총 최대가 12로 줄어 업데이트가 느려지는 동시에 가용 최소가 7로 내려가 덜 안전해집니다. 어느 쪽으로도 이득이 없습니다.

> 원본 §정답 5 축자.

### 정답 5

이 설정은 "새 파드가 준비되기 전엔 옛 파드를 지우지 않는다"까지만 보장합니다. **무엇을 준비로 볼 것인가**는 별개입니다. readinessProbe가 없으면 컨테이너가 실행됐다는 사실 자체가 ready라, 앱이 아직 기동 중인 파드를 근거로 옛 파드를 지웁니다.

넣어야 할 것은 **readinessProbe**입니다. readiness는 실패해도 파드를 살려 둔 채 엔드포인트에서만 뺍니다. liveness는 컨테이너를 죽이고 재시작합니다. 기동이 느린 것은 고장이 아니므로 liveness를 걸면 "느리다"를 "죽었다"로 판정해 재시작 루프에 빠집니다. 기동이 아주 느리면 `startupProbe`를 따로 둡니다.

검사 대상도 포트 열림이 아니라 실제 처리 가능 상태여야 합니다. Spring Boot는 `/actuator/health/readiness`가 의존성까지 반영합니다.

> 원본 §정답 6 축자.
