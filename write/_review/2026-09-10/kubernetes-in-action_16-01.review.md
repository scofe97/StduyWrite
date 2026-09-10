---
title: "StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service — 복습 회차 1"
tags: [review, kubernetes, kubernetes-in-action, statefulset, headless-service, pets-vs-cattle]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/16-01.StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service.md"
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

# StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service — 복습 회차 1

> 원본: [StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service](../../08_cloud/book/kubernetes-in-action/16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md)
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
> 원본 7 문항 중 다섯을 골랐다. 남긴 둘(파드를 직접 소유하는 이유와 PVC 이름 · DNS 로 peer discovery 하는 이유)은 회차 2 의 몫이다.

## 학습 목표

Kiada suite의 세 서비스는 모두 Deployment로 배포됩니다. 하지만 Quiz 서비스는 데이터 때문에 쉽게 스케일되지 않아 replica가 하나뿐입니다. 이 편은 그런 상태 있는 워크로드를 StatefulSet으로 제대로 배포하는 법을 다룹니다.

이 목표 한 줄이 본 복습의 *기준점*. 5개 질문 모두 이 목표의 한 축을 검증한다.

> **이번 회차 표적** — **교체 가능한가 아닌가**가 모든 것을 가른다 — Q1(Pets vs Cattle)에서 나온 그 한 축이 Q3(headless DNS)·Q4(ordinal·PVC)의 설계 이유가 된다.

## Q&A 5문제

> 5문제의 축: **정의 (Q1) · 동기 (Q2) · 메커니즘 (Q3) · 적용 (Q4) · 함정 (Q5)**

### Q1. 정의 — 한 줄로 답할 수 있는가

**질문**: Pets vs Cattle 비유로 StatefulSet과 Deployment의 차이를 설명해 보세요.

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)
*점수 기준: 0=완전 못 답함, 1=틀린 답, 2=부분 답+큰 누락, 3=핵심 맞음+세부 누락, 4=정확하지만 머뭇, 5=막힘 없이 정확*

---

### Q2. 동기 — 왜 이 개념이 등장했는가

**질문**: 상태 있는 워크로드를 Deployment로 스케일하면 왜 문제가 생기나요? 두 가지 접근(공유 볼륨·전용 볼륨)이 각각 왜 어려운가요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q3. 메커니즘 — 그림 없이 말로 흐름을 설명할 수 있는가

**질문**: headless Service란 무엇이고, StatefulSet과 결합하면 DNS에 무엇이 추가되나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q4. 적용 — 실무 시나리오에 응용할 수 있는가

**질문**: StatefulSet이 Deployment와 다르게 지정할 수 있는 것은 무엇이고, 그것이 파드에 어떤 영향을 주나요?

**자기 답** (보고 답하지 말 것):

```
(여기에 자기 답 작성)
```

**점수 (0~5)**: __ (채점: AI — 근거 한 줄)

---

### Q5. 함정 — 흔한 실수 패턴을 진단할 수 있는가

**질문**: 이 예제에서 `publishNotReadyAddresses`와 `podManagementPolicy: Parallel`을 각각 빼면 무슨 일이 벌어지나요? 두 교착은 어떻게 다른가요?

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

두 비유가 가리키는 것은 각각 이렇습니다.

- **Cattle(소)** — 균질해서 이름이 없고 개체 차이가 무의미하므로 교체가 자명합니다. Deployment의 stateless 파드가 여기 해당하며, 교체돼도 아무도 알아채지 못합니다.
- **Pets(애완동물)** — 이름과 개성이 있어 잃으면 그냥 대체할 수 없습니다. StatefulSet의 stateful 파드가 여기 해당합니다.

다만 소프트웨어는 교체 인스턴스에 같은 네트워크 신원과 같은 상태를 줄 수 있습니다. StatefulSet이 정확히 이 일을 합니다. 같은 이름·PVC·주소로 재생성하는 것입니다.

> 원본 §정답 2 축자.

### 정답 2

공유 볼륨 접근은 여러 파드가 같은 PVC·PV를 써서, ReadWriteMany를 지원하지 않는 대부분의 클라우드 스토리지(ReadWriteOnce·ReadOnlyMany만)에서 다른 노드의 파드가 같은 볼륨에 읽고 쓸 수 없어 막힙니다. MongoDB는 같은 데이터 디렉토리를 여러 인스턴스가 못 써 크래시합니다. 전용 볼륨 접근은 replica마다 Deployment·Service·PVC를 따로 만들어야 해서(단일 Deployment로는 불가), 스케일에 kubectl scale도 못 쓰고 오브젝트를 계속 늘려야 해 복잡합니다.

> 원본 §정답 1 축자.

### 정답 3

headless Service는 clusterIP가 None인 Service로, IP가 없고 이름이 소속 파드 전부의 IP로 resolve됩니다. StatefulSet과 결합하면 레코드 두 종류가 파드마다 추가됩니다.

- **A/AAAA 레코드** — `quiz-0.quiz-pods...`처럼 파드 이름으로 개별 IP를 조회합니다
- **SRV 레코드** — `_mongodb._tcp...`로 주소와 포트를 자동 조회합니다

이 파드별 레코드는 headless Service가 StatefulSet과 연결되지 않으면 존재하지 않습니다. 이것이 파드의 안정된 네트워크 신원을 만듭니다.

> 원본 §정답 4 축자.

### 정답 4

StatefulSet은 Deployment와 달리 **PersistentVolumeClaim 템플릿**(`volumeClaimTemplates`)을 지정할 수 있습니다. 그 결과가 파드에 미치는 영향은 셋입니다.

- 컨트롤러가 replica마다 Pod뿐 아니라 PVC도 함께 만듭니다. 그래서 파드가 서로 완전한 복제본이 아니라 각자 다른 PVC를 가리킵니다.
- 이름이 랜덤이 아니라 고유 ordinal 번호로 붙습니다. 특정 ordinal 파드는 항상 같은 번호 PVC와 짝지어지므로, 재생성돼도 상태가 동일합니다.
- 기본적으로 파드가 동시에 만들어지지 않고 하나씩 만들어집니다. 각 파드가 ready가 될 때까지 기다린 뒤 다음으로 넘어갑니다.

> 원본 §정답 3 축자.

### 정답 5

둘 다 빼면 예제가 부팅되지 않지만, 막히는 지점이 다릅니다.

- **`publishNotReadyAddresses`를 빼면** 파드 셋이 모두 뜨긴 하는데 ready가 아니라서 DNS 레코드가 하나도 생기지 않습니다. `rs.initiate`가 주소를 풀지 못해 `Host not found`로 실패하고, 초기화가 안 되니 probe도 계속 실패합니다.
- **`podManagementPolicy: Parallel`을 빼면** 기본값 `OrderedReady`가 걸려 `quiz-0`이 ready가 될 때까지 `quiz-1`을 만들지 않습니다. `quiz-0`은 `rs.initiate` 전까지 ready가 되지 않으므로 나머지 파드가 생성조차 되지 않습니다.

앞은 파드가 다 있는데 **주소가 없어** 막힙니다. 뒤는 주소를 물어볼 **파드 자체가 없어** 막힙니다. 원인은 같은 부팅 순환입니다. 그것을 끊는 장치가 DNS 쪽과 생성 순서 쪽에 각각 하나씩 필요합니다.

> 원본 §정답 6 축자.
