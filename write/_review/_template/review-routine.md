---
title: 학습 문서 복습 루틴 운영 가이드
tags: [review, routine, spaced-repetition, sm-2, active-recall]
status: final
source:
  - https://en.wikipedia.org/wiki/Forgetting_curve
  - https://en.wikipedia.org/wiki/SuperMemo
  - https://www.sciencedirect.com/science/article/abs/pii/S0959475217301810
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8476370/
related:
  - ./review-template.md
  - ../README.md
updated: 2026-05-22
---

# 학습 문서 복습 루틴 — 운영 가이드

---

> 본 문서는 `write/_review/` 시스템의 *운영 SSOT*. 회차별 간격·트리거·분량·interleaving·졸업 기준의 모든 결정 로직을 한 자리에 모은다. 복습 파일 작성 형식은 [review-template.md](review-template.md), 사용자가 코워크에서 호출할 표준 프롬프트는 본 문서 §7 에 있다.

## 0. 단위는 챕터, 명부는 `_queue.md`

**한 회차의 대상 1 건 = 한 챕터**다. 편 단위(`08-01`·`08-02`)로 쪼개면 kubernetes-in-action 한 권이 51 건이 되어 목록이 압도적이고, 실제로 그렇게 만든 시트 28 장이 한 번도 풀리지 않은 채 쌓였다(2026-09-11 청산). 챕터로 묶으면 같은 책이 18 건이고, 7 문항을 뽑을 재료도 편 하나보다 챕터 하나 쪽이 낫다.

**시트가 없는 챕터는 [`../_queue.md`](../_queue.md) 가 보존한다.** 이 큐가 없던 동안, 복습하겠다고 상태 채널에 적어 둔 챕터가 매 세션 조용히 누락됐다 — `learning-status.mjs` 가 `.review.md` 만 읽었기 때문이다. 시트는 회차를 *실제로 돌릴 때* 만들고, 그 전까지 대상은 큐의 한 행으로만 존재한다. 큐 행을 만들지 않고 시트부터 찍으면 미완 더미가 다시 커진다.

상태값 여섯(`미착수`·`학습중`·`게이트`·`대기`·`진행중`·`졸업`)의 정의와 갱신 주체는 큐 파일 머리말이 정본이다. **복습 재고는 `대기` 상태의 행 수**다.

## 1. 회차별 간격 — Ebbinghaus + SM-2 기반

> Ebbinghaus 망각곡선(1885): 학습 후 *1시간 안 50%, 24시간 안 70%* 망각. SM-2(Wozniak 1987): quality 점수로 간격 자동 조정. 본 루틴은 두 발견을 결합한 *수정 SM-2* 다.

| 회차 | 표준 간격 | quality 기반 조정 | 비고 |
|------|----------|------------------|------|
| 1 (첫 학습) | 학습 직후 | — | Phase 4 를 통과한 챕터 (§2 (A) 트리거) |
| 2 | +3일 | quality 5: +7일 / 0~2: +1일 | 회차 1 에서 quality ≤ 4 인 문서만 |
| 3 | +7일 | quality 5: +14일 / 0~2: +1일 | 회차 2 에서 막힌 것만 |
| 4 | +14일 (interleaving 시작) | quality 5: 졸업 후보 | 카테고리 무관 섞기 |
| 5 | +30일 | quality ≥ 4 면 *졸업* (장기 기억) | 미졸업만 6회차 |
| 6+ | 분기 1회 (90일) | 잊을 만하면 1회 | 졸업 후 유지 |

회차 4·5 의 *간격 길어짐* 은 망각곡선이 *완만해진* 후라 효과적. 회차 1·2 의 *짧은 간격* 은 24h 70% 망각을 차단하기 위함.

## 2. 회차 시작 트리거

> 회차 1 은 *학습 직후 자동*, 회차 2 이상은 *날짜 기반 캘린더* 또는 *사용자 수동*. 자동 cron 은 별도 plan 으로 (본 가이드 범위 밖).

세 가지 트리거 중 하나로 시작:

- **(A) Phase 4 종료 직후** — 4-Phase 세션이 한 챕터의 Phase 4 를 마치면 큐의 그 행을 `대기` 로 바꾸고 막힌 축을 비고에 적는다. **시트는 만들지 않는다** — 생성은 `learning-review` 실행 시점이다
- **(B) 캘린더 리마인더** — 회차 2~5 의 *다음 회차 날짜* (각 복습 파일 frontmatter 의 `next_round_date`) 가 오늘이면 자동 생성
- **(C) 사용자 수동 호출** — "이번 주 복습 시작해줘" 같이 직접. *큐에 `대기` 가 없으면 기존 챕터 중 무작위 5 챕터 선택*

## 3. 한 회차의 권장 분량

> 한 세션당 *5 챕터* 가 표준. 7 챕터 초과 시 active recall 효과가 떨어진다 (피로 누적).

- 1챕터당 20~25분 (Q&A 7문제 + 종합 평가). 문항이 둘 늘었지만 대상이 편 → 챕터로 묶여 건수가 1/3 로 줄어 세션 총량은 오히려 가볍다
- 한 세션 = 5챕터 = 100~125분 + Pomodoro 휴식 = 약 2.5시간
- 한 책이 18챕터면 *4 세션* 으로 분할
- 7챕터 초과 = *다음 회차로 분할*

## 4. interleaving 시작 시점

> 회차 4 (+14일) 부터 카테고리 섞기 시작. 사용자가 *초보~중급* 단계라 회차 1~3 은 blocked 가 효과적.

```
회차 1~3: 같은 카테고리 순서대로  (blocked — 개념 안착)
  - kia 18챕터 따로 → lml 9챕터 따로
회차 4+ : 카테고리 무관 섞기  (interleaving — desirable difficulty)
  - kia·lml·새 카테고리 모두 무작위 순서
```

근거: Hwang et al. (2025) — 초보자는 blocked 가 인지 부하 낮추고, 숙련자는 interleaved 가 transfer 효과 큼.

## 5. Pomodoro 결합 권장 패턴

한 복습 세션 (5 챕터) 의 표준 흐름:

```
25분: 1 챕터 복습 (Q&A 7문제 풀고 채점)
 5분: 휴식 (걷기·물·창 보기)
25분: 2 챕터째
 5분: 휴식
25분: 3 챕터째
 5분: 휴식
25분: 4 챕터째
15분: 긴 휴식
25분: 5 챕터째
10분: 종합 평가 + _mistakes.md 갱신
```

총 2시간 30분 / 5 챕터. 한 세션이 *늘어지면 다음 날로 미루기* — testing effect 유지에 낫다.

## 6. 졸업 기준 (writing 스킬 §14 와 연동)

다음 *세 조건 모두 충족* 시 원본 학습 문서 `status: final` + 복습 졸업:

- [ ] 회차 4 (14일) 또는 회차 5 (30일) 에서 quality ≥ 4 — **회차 요건이 먼저다.** 회차 1~3 은 q5 여도 졸업이 아니고, 회차 3 q5 는 §1 표대로 "졸업 후보"에 머문다
- [ ] 3축 메타인지 평균 ≥ 3.6 (면접·말로설명·다른환경응용) — **AI 가 채점한다.** 사용자 자가평가로 두면 비워진 채 남는다
- [ ] 카테고리 `_mistakes.md` 에서 해당 챕터 관련 미해결 패턴 0개

졸업 판정이 나면 `_queue.md` 의 해당 행을 `_queue-archive.md` 로 옮긴다. 활성 큐에 졸업 행이 남으면 재고 집계가 부풀고, 분할 시점 판단(활성 200 행)도 어긋난다.

졸업 후 6회차 (90일) 부터는 *분기 1회 가벼운 점검* 만. 졸업해도 1년에 1~2회 복습은 권장 (장기 기억 유지).

## 7. 회차 진행

회차를 실제로 돌리는 것은 `/learning-review` 다. 모드 판별(회차·즉석), 판단 1·2·2b·3·4, 되묻기와 채점, 동작 C 회차 종합 평가의 절차 정본은
[`runners/review.md`](~/claude/.claude/skills/learning-method/references/runners/review.md) 에 있다.

여기에 복붙용 프롬프트를 두지 않는다. 2026-09-13 까지 이 자리에 있던 §7.1~7.5 는 git push 트리거·편 단위·Q1~Q5 로 짜인 구 체계였고,
§0 의 챕터 단위 전환과 §2 (A) 의 Phase 4 트리거가 들어온 뒤에도 갱신되지 않아 같은 문서 안에서 서로 어긋나 있었다.
절차가 두 곳에 있으면 한쪽만 고쳐지는 일이 반복된다 — 간격표(§1)·졸업 기준(§6)처럼 *수치와 판정*만 이 문서가 맡고, *진행 절차*는 러너가 맡는다.

## 8. 회차 통계 시각화 (README 와 연동)

각 회차 종합 평가 후 `write/_review/README.md` 의 통계 표가 자동 갱신:

| 회차 | 날짜 | 대상 편수 | 평균 quality | 3축 평균 | 졸업 수 |
|------|------|---------|------------|---------|--------|
| 1 | 2026-05-26 | 18 | __ | __ | 0 |
| 2 | 2026-05-29 | __ | __ | __ | __ |
| ... | | | | | |

장기적으로 *평균 quality 가 회차마다 올라가는지* 가 학습 효과의 직접 지표. 회차 5 에서 *졸업 수 / 대상 편수* 비율이 80% 이상이면 본 루틴이 잘 작동하는 것.

## 9. 참조

- [review-template.md](review-template.md) — 복습 파일 5문제 표준 템플릿
- [../README.md](../README.md) — 복습 시스템 진입점 + 회차 통계
- `../../../claude/.claude/skills/content/writing/references/02-learned-docs.md` <!-- 링크 끊김(2026-08): ../../../claude/.claude/skills/content/writing/references/02-learned-docs.md --> §12~§15 — 학습 문서 하네스의 Stage 2 워크플로우 규약
- 학술 근거:
  - [Forgetting curve (Ebbinghaus)](https://en.wikipedia.org/wiki/Forgetting_curve)
  - [SuperMemo SM-2 algorithm](https://en.wikipedia.org/wiki/SuperMemo)
  - [Rowland (2014) testing effect meta-analysis](https://www.sciencedirect.com/science/article/abs/pii/S0959475217301810)
  - [Interleaving research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476370/)
