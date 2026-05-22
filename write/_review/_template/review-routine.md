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

## 1. 회차별 간격 — Ebbinghaus + SM-2 기반

> Ebbinghaus 망각곡선(1885): 학습 후 *1시간 안 50%, 24시간 안 70%* 망각. SM-2(Wozniak 1987): quality 점수로 간격 자동 조정. 본 루틴은 두 발견을 결합한 *수정 SM-2* 다.

| 회차 | 표준 간격 | quality 기반 조정 | 비고 |
|------|----------|------------------|------|
| 1 (첫 학습) | 학습 직후 | — | 모든 신규 문서 (git push 트리거) |
| 2 | +3일 | quality 5: +7일 / 0~2: +1일 | 회차 1 에서 quality ≤ 4 인 문서만 |
| 3 | +7일 | quality 5: +14일 / 0~2: +1일 | 회차 2 에서 막힌 것만 |
| 4 | +14일 (interleaving 시작) | quality 5: 졸업 후보 | 카테고리 무관 섞기 |
| 5 | +30일 | quality ≥ 4 면 *졸업* (장기 기억) | 미졸업만 6회차 |
| 6+ | 분기 1회 (90일) | 잊을 만하면 1회 | 졸업 후 유지 |

회차 4·5 의 *간격 길어짐* 은 망각곡선이 *완만해진* 후라 효과적. 회차 1·2 의 *짧은 간격* 은 24h 70% 망각을 차단하기 위함.

## 2. 회차 시작 트리거

> 회차 1 은 *학습 직후 자동*, 회차 2 이상은 *날짜 기반 캘린더* 또는 *사용자 수동*. 자동 cron 은 별도 plan 으로 (본 가이드 범위 밖).

세 가지 트리거 중 하나로 시작:

- **(A) git push 직후** — 직전 push 된 *신규 학습 문서* 가 있으면 그 다음 평일에 회차 1 자동 생성
- **(B) 캘린더 리마인더** — 회차 2~5 의 *다음 회차 날짜* (각 복습 파일 frontmatter 의 `next_round_date`) 가 오늘이면 자동 생성
- **(C) 사용자 수동 호출** — "이번 주 복습 시작해줘" 같이 직접. *최근 커밋이 적으면 기존 학습 문서 중 무작위 5편 선택*

## 3. 한 회차의 권장 분량

> 한 세션당 *5편* 이 표준. 7편 초과 시 active recall 효과가 떨어진다 (피로 누적).

- 1편당 15~20분 (Q&A 5문제 + 종합 평가)
- 한 세션 = 5편 = 75~100분 + Pomodoro 휴식 = 약 2.5시간
- 18편이면 *3~4 세션* 으로 분할 (월·화·수 또는 한 주말)
- 7편 초과 = *다음 회차로 분할*

## 4. interleaving 시작 시점

> 회차 4 (+14일) 부터 카테고리 섞기 시작. 사용자가 *초보~중급* 단계라 회차 1~3 은 blocked 가 효과적.

```
회차 1~3: 같은 카테고리 순서대로  (blocked — 개념 안착)
  - querydsl 16편 따로 → JDBC 2편 따로
회차 4+ : 카테고리 무관 섞기  (interleaving — desirable difficulty)
  - querydsl·JDBC·새 카테고리 모두 무작위 순서
```

근거: Hwang et al. (2025) — 초보자는 blocked 가 인지 부하 낮추고, 숙련자는 interleaved 가 transfer 효과 큼.

## 5. Pomodoro 결합 권장 패턴

한 복습 세션 (5편) 의 표준 흐름:

```
25분: 1편 복습 (Q&A 5문제 풀고 채점)
 5분: 휴식 (걷기·물·창 보기)
25분: 2편째
 5분: 휴식
25분: 3편째
 5분: 휴식
25분: 4편째
15분: 긴 휴식
25분: 5편째
10분: 종합 평가 + _mistakes.md 갱신
```

총 2시간 30분 / 5편. 한 세션이 *늘어지면 다음 날로 미루기* — testing effect 유지에 낫다.

## 6. 졸업 기준 (writing 스킬 §14 와 연동)

다음 *세 조건 모두 충족* 시 원본 학습 문서 `status: final` + 복습 졸업:

- [ ] 회차 4 (14일) 또는 회차 5 (30일) 에서 quality ≥ 4
- [ ] 3축 메타인지 평균 ≥ 3.6 (면접·말로설명·다른환경응용)
- [ ] 카테고리 `_mistakes.md` 에서 해당 문서 관련 미해결 패턴 0개

졸업 후 6회차 (90일) 부터는 *분기 1회 가벼운 점검* 만. 졸업해도 1년에 1~2회 복습은 권장 (장기 기억 유지).

## 7. 코워크 표준 프롬프트 — 사용자가 그대로 복붙

> 사용자가 매주 월요일 또는 회차 트리거 시점에 *이 프롬프트 하나만 Claude 에게 복붙* 하면 자동으로 회차 시작·진행·평가·다음 회차 스케줄링이 이뤄지도록 설계. 4가지 시나리오별 프롬프트.

### 7.1 [신규 회차 1 시작] — 최근 푸시된 문서 자동 식별

```
복습 루틴 시작:

1. 직전 git push (HEAD~2..HEAD 범위) 에서 추가/수정된 write/ 학습 문서를 모두 식별
2. 그 결과가 5편 이하면 모두 회차 1 대상, 5편 초과면 사용자에게 어느 카테고리부터 시작할지 질문
3. 만약 최근 푸시에 학습 문서가 없으면 write/ 하위 기존 학습 문서 중 무작위 5편 선택
4. write/_review/{오늘 YYYY-MM-DD}/ 폴더 생성
5. 각 대상 문서마다 _review/_template/review-template.md 기반으로 복습 파일 생성
   - 파일명: {카테고리축약}_{원본번호}.review.md (예: querydsl_01-01.review.md, jdbc_04-01.review.md)
   - Q1~Q5 는 원본 문서 본문에서 추출 (학습 목표·정의·메커니즘·실무 예시·함정)
   - frontmatter: round=1, round_date=오늘, prev_round_date=null
6. README 의 회차 통계 표에 오늘 회차 1 행 추가
7. 사용자에게 권장 분할 안내 (5편 단위 세션)
```

### 7.2 [회차 진행 — 한 편 복습 시작] — 사용자가 복습 도중 호출

```
다음 복습 진행:

대상 파일: write/_review/{날짜}/{파일명}.review.md

규약:
1. 내가 Q1 부터 자기 답을 직접 적을 것 — 너는 정답을 미리 보여주지 말 것
2. 내가 자기 답을 적고 "정답 보여줘" 라고 하면 그때 <details> 의 정답 한 줄을 보여줘
3. 내가 자가 점수 (0~5) 를 매기면 그 점수를 파일에 기록
4. Q5 까지 끝나면 종합 평가 (SM-2 quality, 3축 메타인지) 를 진행
5. 종합 평가 후 다음 회차 날짜 자동 계산 (review-routine.md §1 표 기반)
6. quality ≤ 3 인 질문은 _mistakes.md 에 append
```

### 7.3 [회차 종합 평가 — 한 세션 끝났을 때]

```
회차 종합:

오늘 진행한 복습 파일: write/_review/{날짜}/

다음을 자동 처리:
1. 폴더 안 모든 .review.md 의 quality 점수와 3축 메타인지를 표로 요약
2. 평균 quality 와 표준편차 계산
3. quality ≤ 3 인 문서를 *다음 회차 대상* 으로 식별
4. quality ≥ 4 인 문서 중 회차 4·5 이상이면 *졸업 후보* 로 표시
5. 다음 회차 날짜를 quality 별로 계산해 캘린더 형태로 정리
   - 회차 N+1 날짜별 대상 문서 묶음 표시
6. README 의 회차 통계 표 갱신 (회차·날짜·평균 quality·졸업 수)
7. 모든 변경 git status 보여주고 커밋 분할 계획 제시 (PRE-COMMIT GATE 준수)
```

### 7.4 [회차 2 이상 — 캘린더 기반 트리거]

```
오늘 예정된 복습:

1. write/_review/ 의 모든 .review.md 파일에서 frontmatter next_round_date 가 오늘 (YYYY-MM-DD) 이하인 파일 식별
2. 그 파일들의 source (원본 문서) 들을 묶어 새 회차 폴더 생성
   - write/_review/{오늘}/ 안에 새 회차 파일 생성
   - round = 이전 회차 + 1, prev_round_date = 이전 회차 날짜
3. 회차 4 이상이면 카테고리 무관 무작위 섞기 (interleaving)
4. 5편 초과면 분할 안내, 5편 이하면 그대로 진행
5. 사용자에게 "오늘 복습 N편 준비됨, 시작할까요?" 확인
```

### 7.5 사용자 워크플로우 — 한 주 표준 패턴

월요일 아침 (또는 학습 푸시 직후 다음 평일):

```
1. Claude 에게 7.4 [캘린더 트리거] 프롬프트 복붙
   → 오늘 예정된 복습 파일 자동 생성됨
2. 첫 복습 파일 열기 → 7.2 [한 편 복습 진행] 프롬프트 복붙
3. Q1 자기 답 → "정답 보여줘" → 점수 매김
4. Q2~Q5 반복
5. 한 편 끝나면 다음 파일로 (Pomodoro 패턴)
6. 5편 끝나면 7.3 [회차 종합 평가] 프롬프트 복붙
   → 통계 + 다음 회차 날짜 + 커밋 분할 계획
7. 커밋 승인 + push
```

신규 학습 문서 push 직후:

```
1. Claude 에게 7.1 [신규 회차 1] 프롬프트 복붙
   → 그 푸시의 학습 문서들 복습 파일 자동 생성
2. 위 월요일 패턴 1~7 진행
```

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
- [`../../../claude/.claude/skills/content/writing/references/02-learned-docs.md`](../../../claude/.claude/skills/content/writing/references/02-learned-docs.md) §12~§15 — 학습 문서 하네스의 Stage 2 워크플로우 규약
- 학술 근거:
  - [Forgetting curve (Ebbinghaus)](https://en.wikipedia.org/wiki/Forgetting_curve)
  - [SuperMemo SM-2 algorithm](https://en.wikipedia.org/wiki/SuperMemo)
  - [Rowland (2014) testing effect meta-analysis](https://www.sciencedirect.com/science/article/abs/pii/S0959475217301810)
  - [Interleaving research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476370/)
