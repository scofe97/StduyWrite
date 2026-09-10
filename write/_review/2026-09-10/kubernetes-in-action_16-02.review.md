---
title: "StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, statefulset, at-most-one, pvc-retention]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/16-02.StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention.md"
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

# StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention — 복습 회차 1

> 원본: [StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention](../../08_cloud/book/kubernetes-in-action/16-02.StatefulSet%20%EB%8F%99%EC%9E%91%20%E2%80%94%20%EB%AF%B8%EC%8B%B1%20%ED%8C%8C%EB%93%9C%C2%B7%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%C2%B7retention.md)
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
> 원본 9 문항 중 다섯을 골랐다. 남긴 넷(retention 미적용 상황 · at-most-one 의 구멍 두 층 · OrderedReady 교착 · 사람이 개입하는 세 지점의 공통점)은 회차 2 의 몫이다.

## 학습 목표

[16-01](../../08_cloud/book/kubernetes-in-action/16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md)에서 StatefulSet을 만들고 헤드리스 Service로 데이터를 임포트했습니다. 이 편은 StatefulSet이 미싱 파드·노드 장애·스케일을 어떻게 다루는지 시험합니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — **at-most-one 은 자동 복구를 포기하고 산 보장이다** — 노드 장애에서 컨트롤러가 가만히 있는 것도, 사람이 `--force` 를 쳐야 하는 것도 같은 한 문장에서 나온다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: at-most-one 보장이란 무엇이고, 노드 장애 시 StatefulSet 컨트롤러가 파드를 자동 교체하지 않는 이유는요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: StatefulSet 파드가 삭제·교체되면 무엇이 유지되나요? 클라이언트가 차이를 못 느끼는 이유는요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: StatefulSet을 스케일다운하면 PVC는 어떻게 되나요? 삭제 순서는요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: 장애 노드의 파드를 재생성하려면 왜 `--force --grace-period 0`이 필요하고, 무엇을 먼저 확인해야 하나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: persistentVolumeClaimRetentionPolicy를 둘 다 Delete로 두면 왜 위험한가요?

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

at-most-one은 같은 신원의 파드가 둘 동시에 돌지 않는다는 보장입니다. ordinal 이름 규칙이 1차 방어인데, 같은 이름 Pod 오브젝트 둘이 한 네임스페이스에 공존할 수 없기 때문입니다. 단 이 제약은 API 오브젝트에만 걸리고 실행 중인 컨테이너까지 묶지 못합니다. 노드가 네트워크만 잃은 경우 파드 컨테이너는 여전히 돌고 있는데, 컨트롤러가 자동으로 삭제·재생성하면 새 파드가 다른 노드에 떠 같은 신원 인스턴스가 둘 돌게 됩니다. 이를 막으려 StatefulSet은 자동 교체하지 않습니다(ReplicaSet은 자동 교체함).

> 원본 §정답 2 축자.

### 정답 2

StatefulSet 파드가 삭제·교체되면 **같은 이름(ordinal)과 같은 PVC**가 유지됩니다. IP는 달라질 수 있지만 DNS 레코드가 새 주소로 갱신되어, 파드 이름(`quiz-1.quiz-pods...`)으로 통신하는 클라이언트는 차이를 못 느낍니다. 새 파드는 network-attached 볼륨이면 어느 노드에나, local 볼륨이면 항상 볼륨이 있는 노드에 스케줄됩니다.

> 원본 §정답 1 축자.

### 정답 3

스케일다운 시 파드는 삭제되지만 **PVC는 기본 보존**됩니다. 클레임을 지우면 바인딩된 PV가 recycle·삭제되어 데이터가 사라지기 때문입니다. 삭제 순서는 ReplicaSet과 달리 **ordinal 번호가 가장 높은 파드부터**인 역순입니다. 그래서 남는 파드의 번호가 항상 0부터 연속입니다. 3에서 1로 줄이면 quiz-2와 quiz-1이 삭제됩니다. PVC 자동 삭제를 원하면 persistentVolumeClaimRetentionPolicy를 씁니다.

> 원본 §정답 4 축자.

### 정답 4

장애 노드의 파드는 이미 Terminating으로 마킹돼, control plane이 Kubelet의 컨테이너 종료 보고를 기다리는데 그 Kubelet이 안 돌아 보통 삭제가 완료되지 않습니다. 그래서 `--force --grace-period 0`으로 확인을 기다리지 않고 즉시 삭제해야 합니다. 단 이 옵션은 "컨테이너가 계속 돌 수 있다"는 경고가 있으므로, **노드가 정말 장애임을 먼저 확인**해야 합니다 — 아니면 같은 신원 파드가 둘 돌게 됩니다.

> 원본 §정답 3 축자.

### 정답 5

whenScaled·whenDeleted를 둘 다 Delete로 두면 데이터가 쉽게 사라집니다. whenDeleted만 Retain으로 둬 실수 삭제 시 데이터를 지켜도, whenScaled가 Delete면 StatefulSet을 삭제하기 전 0으로 스케일하는 순간 PVC가 삭제되어 데이터가 유실됩니다. 그래서 PV 데이터가 다른 곳에 보존되거나 보존이 불필요할 때만 Delete를 쓰고, StorageClass reclaimPolicy를 Retain으로 두는 방어도 병행합니다.

> 원본 §정답 5 축자.
