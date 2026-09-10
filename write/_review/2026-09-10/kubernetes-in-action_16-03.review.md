---
title: "StatefulSet 업데이트와 Operator — partition·OnDelete·CRD — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, statefulset, operator, crd, partition]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/16-03.StatefulSet 업데이트와 Operator — partition·OnDelete·CRD.md"
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

# StatefulSet 업데이트와 Operator — partition·OnDelete·CRD — 복습 회차 1

> 원본: [StatefulSet 업데이트와 Operator — partition·OnDelete·CRD](../../08_cloud/book/kubernetes-in-action/16-03.StatefulSet%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%99%80%20Operator%20%E2%80%94%20partition%C2%B7OnDelete%C2%B7CRD.md)
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
> 원본 9 문항 중 다섯을 골랐다. 남긴 넷(revision 저장 위치 · OnDelete · ControllerRevision 연결 · Operator 와 StatefulSet 의 관계)은 회차 2 의 몫이다.

## 학습 목표

StatefulSet도 선언적 업데이트를 제공합니다. Pod 템플릿을 바꾸면 컨트롤러가 파드를 재생성하되, Deployment와 다른 전략(RollingUpdate·OnDelete)을 씁니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — **생성은 오름차순인데 교체는 역순이다** — 이 비대칭이 Q3(왜 역순인가)과 Q4(partition 이 canary 가 되는 이유)를 한꺼번에 설명한다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: StatefulSet의 RollingUpdate는 Deployment의 것과 무엇이 다른가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: Kubernetes Operator란 무엇이고, CRD·커스텀 오브젝트와 어떻게 함께 동작하나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: StatefulSet의 RollingUpdate는 왜 ordinal 역순인가요? 생성은 오름차순인데 교체는 역순인 이유가 무엇인가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: StatefulSet에는 pause가 없는데 어떻게 canary를 구현하나요? partition 값은 어떻게 정하나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: RollingUpdate가 연쇄 장애를 막지 못하는 근본 원인은 무엇인가요? minReadySeconds를 늘리면 해결되나요?

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

StatefulSet의 RollingUpdate는 **한 번에 파드 하나만** 교체합니다. Deployment에 있는 maxSurge가 없고 maxUnavailable도 기본 비활성이기 때문입니다[^max-unavailable]. 교체는 ordinal 번호가 가장 높은 파드부터 시작합니다. 그 파드가 ready가 되면 다음으로 내려갑니다. minReadySeconds는 두 컨트롤러가 공유합니다. 다만 StatefulSet에서는 업데이트와 스케일 양쪽에 적용됩니다.

책은 두 파라미터가 모두 없다고 설명하지만, maxUnavailable은 현행 API에 존재합니다(v1.35 beta). 켜면 여러 파드를 동시에 교체할 수 있으므로 "한 번에 하나"는 기본 설정에서의 동작입니다.

> 원본 §정답 1 축자.

### 정답 2

Kubernetes Operator는 앱 전용 컨트롤러로, 상태 앱의 배포·관리를 자동화합니다. 스케일 시 리플리카 셋 재구성이나 장애 복구처럼 앞서 수동으로 하던 일이 대상입니다. 동작은 두 단계로 나뉩니다.

- **CRD**(CustomResourceDefinition)로 Kubernetes API에 커스텀 오브젝트 타입을 추가합니다. 예제에서는 MongoDBCommunity였습니다.
- 사용자가 그 **커스텀 오브젝트** 인스턴스를 만들면, Operator의 reconciliation loop가 이를 처리해 StatefulSet·Service·Secret을 생성·관리합니다.

사용자는 하위 오브젝트를 직접 다루지 않고 커스텀 오브젝트만 수정하며, Operator가 나머지를 반영합니다. 하위 오브젝트를 직접 바꾸면 Operator가 되돌립니다.

> 원본 §정답 5 축자.

### 정답 3

부트스트랩 패턴을 쓰는 앱에서는 ordinal이 낮은 파드일수록 다른 파드가 의존하는 쪽입니다. quiz-0이 먼저 떠서 클러스터를 만들고 나머지가 거기 가입하는 구조라면, quiz-0을 건드리는 것이 가장 위험합니다.

그래서 생성은 의존 대상부터 오름차순으로, 교체는 **가장 덜 중요한 것부터** 역순으로 진행합니다. 결함이 있는 새 버전을 시험할 때 피해가 가장 작은 파드가 먼저 맞습니다. partition이 카나리로 쓰이는 것도 이 순서 덕분입니다. 오름차순이었다면 첫 시험 대상이 quiz-0이 되어 카나리가 성립하지 않습니다.

다만 쿠버네티스가 ordinal 낮은 파드를 특별 취급하지는 않습니다. 부트스트랩 패턴이 흔하니 StatefulSet이 안전한 기본값을 고른 것이고, 앱이 그런 구조가 아니면 순서는 무의미하며 손해도 없습니다.

> 원본 §정답 6 축자.

### 정답 4

StatefulSet은 `rollout pause`를 지원하지 않습니다. 대신 RollingUpdate의 partition 파라미터로 canary를 구현합니다. partition은 분할 ordinal을 지정하며, 그보다 낮은 ordinal 파드는 업데이트되지 않습니다. 목적에 따라 값을 이렇게 잡습니다.

| 목적 | partition 값 | 결과 |
|------|-------------|------|
| staging (발동 없이 준비) | replica 수 **이상** | 템플릿을 바꿔도 롤아웃이 시작되지 않음 |
| canary (하나만) | replica 수 **− 1** | ordinal이 가장 높은 파드 하나만 업데이트 |
| 완료 | **0** | 나머지 전부를 낮은 ordinal 방향으로 업데이트 |

> 원본 §정답 2 축자.

### 정답 5

readiness probe가 **자기 자신만** 검사하기 때문입니다. 교체된 파드의 probe는 그 파드의 엔드포인트만 찌르므로, 그 파드가 다른 파드나 공유 자원을 망가뜨리고 있어도 알아채지 못합니다. 컨트롤러는 성공으로 판정하고 다음으로 넘어갑니다.

`minReadySeconds`를 늘려도 해결되지 않습니다. 관측 시간이 길어질 뿐 보는 대상은 여전히 파드 자신이기 때문입니다. Deployment에서 minReadySeconds가 30초여도 1분 뒤 터지는 장애를 못 잡는 것과 같은 한계입니다. OnDelete가 주는 것은 이 사각지대를 사람이 대신 보는 **판단 지점**입니다.

> 원본 §정답 8 축자.
