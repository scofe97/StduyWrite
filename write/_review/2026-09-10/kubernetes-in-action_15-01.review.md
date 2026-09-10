---
title: "Deployment 기초 — 생성·pod-template-hash·스케일링 — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, deployment, replicaset, pod-template-hash]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/15-01.Deployment 기초 — 생성·pod-template-hash·스케일링.md"
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

# Deployment 기초 — 생성·pod-template-hash·스케일링 — 복습 회차 1

> 원본: [Deployment 기초 — 생성·pod-template-hash·스케일링](../../08_cloud/book/kubernetes-in-action/15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md)
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
> 원본 8 문항 중 다섯을 골랐다. 남긴 셋(파드가 안 뜰 때 볼 곳 · 롤백과 revisionHistoryLimit · `--cascade=orphan`)은 회차 2 의 몫이다.

## 학습 목표

ReplicaSet은 파드를 매끄럽게 업데이트하는 기능이 없습니다([14장 쿠키 커터](../../08_cloud/book/kubernetes-in-action/14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md)). 그 기능을 Deployment가 제공합니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — Deployment 는 파드를 **직접** 만들지 않는다 — ReplicaSet 을 만들고 그것이 파드를 만든다. 이 한 겹이 Q3(pod-template-hash)·Q5(직접 스케일)의 답을 모두 낳는다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: Deployment는 파드를 어떻게 관리하나요? ReplicaSet과 비교해 spec에 추가되는 필드는 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: ReplicaSet에 업데이트 기능을 직접 넣지 않고 Deployment라는 층을 따로 둔 이유는 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: pod-template-hash는 어떤 값이며 왜 붙나요? 이것 때문에 기존 파드가 흡수되지 않는 이유는 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: 매니페스트에 replicas 필드를 두면 어떤 함정이 있나요? 필드를 생략하면요? 권장 방법은 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: Deployment가 소유한 ReplicaSet을 직접 스케일하면 어떻게 되나요? 그 때문에 포기하게 되는 조작은 무엇인가요?

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

Deployment는 파드를 직접 관리하지 않고, 생성 시 자동으로 만들어지는 ReplicaSet을 통해 간접 관리합니다 — Deployment가 ReplicaSet을 제어하고 ReplicaSet이 파드를 제어하는 3계층입니다.

spec 필드는 ReplicaSet과 같은 replicas·selector·template에 더해 **strategy**가 추가됩니다. strategy는 Pod 템플릿을 업데이트할 때 파드를 어떻게 교체할지(Recreate/RollingUpdate) 정합니다.

책이 "strategy 하나만 더"라고 정리한 것은 업데이트 동작을 설명하기 위한 묶음입니다. 실제 스키마에서 ReplicaSet 대비 늘어나는 필드는 `strategy`·`revisionHistoryLimit`·`paused`·`progressDeadlineSeconds` **넷**입니다. 넷 다 업데이트를 관리하는 필드라는 점이 핵심입니다.

> 원본 §정답 1 축자.

### 정답 2

ReplicaSet의 `replicas`는 숫자 하나이고 `template`도 하나입니다. 롤아웃을 넣으려면 "구 템플릿 2개 + 신 템플릿 3개" 같은 상태를 한 오브젝트가 들어야 하는데, 그러면 숫자 하나로는 부족해지고 `status.readyReplicas`도 어느 쪽인지 없이는 의미를 잃습니다. **개수 유지라는 단일 책임이 깨집니다.**

그래서 ReplicaSet은 그대로 두고, 그런 ReplicaSet을 두 개 두고 숫자만 반대로 움직이는 층을 위에 얹었습니다. 각 ReplicaSet은 여전히 자기 숫자만 지키며 롤아웃이라는 개념을 모릅니다. Deployment는 ReplicaSet의 한계를 없앤 것이 아니라 **우회**했습니다.

> 원본 §정답 8 축자.

### 정답 3

pod-template-hash는 **Pod 템플릿 내용에서 계산한 해시**로(랜덤 아님), Deployment가 만드는 ReplicaSet의 이름 접미사이자 selector·label에 더해지는 값입니다. Deployment의 selector에는 이 label이 없지만 ReplicaSet의 selector에는 있으므로, hash label이 없는 기존 파드는 새 ReplicaSet의 selector에 맞지 않아 흡수되지 않습니다. template 내용이 바뀌면 해시가 달라져 새 ReplicaSet이 생기는데, 이것이 업데이트의 핵심입니다.

> 원본 §정답 2 축자.

### 정답 4

매니페스트에 `replicas: 3`을 두면, label 추가 같은 무관한 변경으로 재적용해도 복제본 수가 3으로 **덮어써집니다**(스케일해 둔 값이 리셋).

필드를 빼는 것이 답인지는 **그 필드가 이전 apply에 있었느냐**에 달렸습니다. 한 번 적었던 replicas를 이번에 빼면 apply가 삭제로 판정해 값이 **1로** 떨어지고, 수백 replica 프로덕션에선 심각한 장애입니다. 반대로 처음부터 적지 않았다면 지울 것이 없어, `kubectl scale`로 조정해 둔 값이 그대로 유지됩니다.

그래서 권장 방법은 Deployment를 만들 때 원본 매니페스트에서 replicas 필드를 **처음부터 생략**하는 것입니다. 이미 적어 버렸다면 `kubectl apply edit-last-applied`로 last-applied-configuration에서 replicas를 지워 같은 상태로 만듭니다.

> 원본 §정답 5 축자.

### 정답 5

값이 잠깐 올라갔다가 곧 Deployment의 복제본 수로 되돌아갑니다. Deployment 컨트롤러가 ReplicaSet의 복제본 수가 Deployment 오브젝트와 안 맞는 걸 감지해 되돌리기 때문입니다. 정상 경로는 사람이 Deployment를 고치면 컨트롤러가 ReplicaSet에 옮겨 적는 2단인데, 하류에 직접 쓰면 그 경로를 건너뛴 것이라 다음 조정에서 덮어써집니다. 컨트롤러는 값을 누가 썼는지 구분하지 않고 Deployment와 다르면 맞출 뿐입니다.

스케일뿐 아니라 ReplicaSet에 가한 어떤 변경도 되돌리며, ReplicaSet을 지워도 다시 만듭니다. 다른 컨트롤러가 소유한 오브젝트를 바꾸면 그 변경은 되돌려진다고 예상해야 합니다.

그래서 포기하는 조작은 **개별 ReplicaSet의 복제본 수를 사람이 직접 정하는 일**입니다. 롤아웃 중 두 ReplicaSet의 숫자 배분은 컨트롤러의 몫이고, 사람에게는 `strategy`(`maxSurge`·`maxUnavailable`)로 규칙을 미리 선언할 권한만 남습니다.

> 원본 §정답 4 축자.
