---
title: "rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종 — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, deployment, rollout, deployment-strategy]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/15-03.rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종.md"
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

# rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종 — 복습 회차 1

> 원본: [rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종](../../08_cloud/book/kubernetes-in-action/15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md)
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
> 원본 6 문항 중 다섯을 골랐다. 남긴 하나(`rollout undo` 와 이전 매니페스트 apply 의 차이)는 회차 2 의 몫이다.

## 학습 목표

[15-02](../../08_cloud/book/kubernetes-in-action/15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md)의 롤링 업데이트는 시작하면 끝까지 자동으로 진행됩니다. 이 편은 그 과정을 멈추고·검증하고·되돌리는 제어와, 네이티브가 아닌 배포 전략의 구현을 다룹니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — **ready 와 available 은 다르다** — 이 구분 하나가 Q1(minReadySeconds 가 결함 버전을 막는 원리)과 Q5(undo 뒤에도 안전한가)를 동시에 연다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: 파드가 ready인 것과 available인 것은 어떻게 다른가요? minReadySeconds가 결함 버전을 어떻게 막나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: rollout pause는 무엇을 하나요? 웹 앱을 롤링 업데이트할 때 주의할 점은 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: ProgressDeadlineExceeded는 언제 발생하나요? 이때 쿠버네티스는 무엇을 하나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: Blue/Green과 Shadowing은 각각 어떻게 구현하나요? 쿠버네티스가 직접 지원하나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: `minReadySeconds: 60`으로 운영하던 Deployment를 `rollout undo`로 되돌렸습니다. 이 Deployment는 여전히 안전한가요? 무엇을 확인해야 하나요?

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

ready는 파드가 요청을 받을 준비가 된 상태입니다. available은 그 ready를 **minReadySeconds만큼 유지**한 상태입니다.

minReadySeconds가 결함 버전을 막는 원리는 타이머 리셋에 있습니다. 새 파드가 ready가 되어도 그 시간 안에 크래시하거나 probe에 실패하면 타이머가 처음으로 돌아갑니다. 그러면 파드는 available이 되지 못합니다. 컨트롤러는 available을 기다리므로 롤아웃이 그 자리에서 멈춥니다. 결함 버전이 30초 뒤 실패하면 60초 minReadySeconds를 영영 못 채워, 첫 파드에서 롤아웃이 정지하고 피해가 최소화됩니다.

> 원본 §정답 2 축자.

### 정답 2

`rollout pause`는 Deployment spec의 `paused` 필드를 true로 만들어, 컨트롤러가 ReplicaSet을 바꾸기 전 이를 확인해 롤아웃을 멈춥니다. 웹 앱에서 두 버전이 도는 동안 pause하면, 브라우저가 리소스마다 다른 버전을 받아(HTML은 새 버전, CSS는 옛 버전) 렌더가 깨질 수 있습니다. 막으려면 session affinity를 쓰거나, 하위 호환 리소스를 먼저 배포하고 HTML을 나중에 배포하는 2단계 업데이트, 또는 Blue/Green을 씁니다.

> 원본 §정답 1 축자.

### 정답 3

Deployment의 `Progressing` condition이 **10분간 진행이 없으면** false·reason `ProgressDeadlineExceeded`가 됩니다. 기한은 `spec.progressDeadlineSeconds`로 조정하며, minReadySeconds가 600 이상이면 함께 올려야 합니다.

이때 쿠버네티스는 롤아웃이 멈췄다고 보고만 하고 별도 조치는 하지 않습니다. 파드가 다시 ready가 되어 minReadySeconds를 채우면 롤아웃이 이어지고, 아니면 그냥 멈춰 있습니다. 취소하려면 rollout undo를 씁니다.

> 원본 §정답 3 축자.

### 정답 4

Blue/Green은 Green Deployment를 Blue 옆에 만들고 **Service의 label selector**를 Blue에서 Green으로 바꿔 트래픽을 한 번에 전환합니다. 둘 다 Deployment 컨트롤러의 **네이티브 전략은 아닙니다** — `strategy.type`에 적을 수 있는 값은 Recreate와 RollingUpdate 둘뿐입니다. 다만 구현 난이도는 갈립니다. Blue/Green은 Service label selector 전환만으로 되어 **추가 도구가 필요 없고**, Shadowing은 그렇지 않습니다.

Shadowing은 새 버전을 배포하되 Service selector와 안 맞는 label을 주고, Ingress/프록시가 옛 파드로 보내면서 새 파드로 **미러링**(응답은 버림)합니다. 트래픽 복제를 해 주는 주체가 따로 있어야 하므로 일부 Ingress 구현이나 Gateway API RequestMirror가 필요합니다.

> 원본 §정답 5 축자.

### 정답 5

여전히 안전하다고 가정하면 안 됩니다. `minReadySeconds` 는 ReplicaSet 에 있는 필드라 revision 마다 스냅샷되고, 따라서 undo 로 **되돌아가는 대상**입니다. 되돌아간 revision 이 `minReadySeconds` 를 추가하기 *전* 의 것이었다면 그 값은 기본값 0 으로 돌아가, 결함 차단 장치가 조용히 풀린 상태로 운영이 이어집니다.

이 함정이 위험한 이유는 확률이 높아서가 아니라 **드러나지 않아서**입니다. `kubectl get deploy` 출력에는 나타나지 않고 롤아웃도 정상 완료되므로, 다음 배포에서 결함이 새어 나갈 때까지 아무도 모릅니다. 게다가 그 다음 배포는 방금 사고를 수습한 직후라 급하게 진행되기 쉽습니다 — 에어백이 필요한 바로 그 시점에 없는 셈입니다.

그래서 `undo` 는 응급 조치로만 쓰고, 상황이 안정되면 매니페스트를 재적용해 선언 상태와 맞춥니다. 확인은 `kubectl get deploy kiada -o yaml` 에서 `minReadySeconds` 값을 보는 것으로 끝납니다. 근본 원인은 §3 의 통찰과 같습니다 — undo 의 동작은 설계된 배려가 아니라 **저장 구조의 귀결**이므로, ReplicaSet 이 어떤 필드를 들고 있는지 알면 이런 경우는 추론으로 나옵니다.

> 원본 §정답 6 축자.
