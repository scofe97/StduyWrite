---
title: 복습 루틴 단일 통합 프롬프트
tags: [review, prompt, coworker, routine]
status: final
related:
  - ./review-routine.md
  - ./review-template.md
  - ../README.md
updated: 2026-05-22
---

# 복습 루틴 단일 통합 프롬프트

---

> **이 파일에는 프롬프트가 1개뿐입니다.** 매번 시나리오 골라 복붙할 필요 없이, 아래 *통합 프롬프트* 하나만 routine 에 박거나 직접 복붙하면 *상황을 알아서 판단* 해 회차 1·2·3·종합 평가 중 필요한 동작을 자동 실행합니다.
>
> 실행 주기 권장: **매주 월·수·금 오전 9시** (cron: `0 9 * * 1,3,5`). 학술 근거는 [§실행 주기](#실행-주기-권장) 참조.

## 통합 프롬프트 (이것 하나만 복붙)

```
복습 루틴 자동 실행:

오늘 날짜를 기준으로 다음 순서로 판단해 적절한 동작을 수행한다.

[판단 1] write/_review/{오늘 YYYY-MM-DD}/ 폴더가 이미 존재하는가?
  → Yes: 오늘 회차는 이미 생성됨. 폴더 안 .review.md 의 quality 입력 여부를 확인:
    - 입력 안 됨: "오늘 회차 N편 준비됨, 진행할까요?" 안내 후 종료
    - 일부만 입력됨: 미진행 N편 안내 + Pomodoro 권장
    - 모두 입력됨: [동작 C] 회차 종합 평가 자동 진행
  → No: 다음 판단으로

[판단 2] write/_review/ 의 모든 .review.md 의 frontmatter next_round_date 가 오늘 이하인 파일이 있는가?
  → Yes: [동작 A] 회차 2 이상 캘린더 트리거 케이스
    - 해당 파일들의 source (원본 학습 문서) 들을 묶음
    - write/_review/{오늘 YYYY-MM-DD}/ 폴더 생성
    - 각 원본 문서별 .review.md 신규 생성:
      · review-template.md 형식 그대로
      · round = 이전 회차 + 1
      · prev_round_date = 이전 회차 날짜
      · Q1~Q5 는 원본 본문에서 추출 (학습목표·정의·메커니즘·실무예시·함정)
    - 회차 4 이상이면 카테고리 무관 무작위 섞기 (interleaving)
    - 5편 초과면 사용자에게 우선순위 질문, 5편 이하면 그대로 진행
    - write/_review/README.md 통계 표 갱신
  → No: 다음 판단으로

[판단 3] 직전 git push (HEAD~3..HEAD 범위) 에서 write/ 안에 추가/수정된 학습 문서가 5편 이상 있는가?
  → Yes: [동작 B] 신규 회차 1 케이스
    - write/_review/{오늘 YYYY-MM-DD}/ 폴더 생성
    - 각 신규 학습 문서별 .review.md 생성 (round=1, prev_round_date=null)
    - 5편 초과면 사용자에게 우선순위 질문
    - README 통계 표에 회차 1 행 추가
    - Pomodoro 권장 분할 (5편/2.5시간) 안내
  → No: 다음 판단으로

[판단 4] 위 셋 모두 아니면
  → "오늘 예정된 복습이 없습니다. 강제로 무작위 5편 복습을 시작하시려면 '강제 시작' 라고 답해주세요" 안내

[동작 C] 회차 종합 평가 (판단 1 에서 모두 입력된 경우)
  → 폴더 안 모든 .review.md 의 quality 점수와 3축 메타인지 표로 요약
  → 평균 quality 와 표준편차 계산
  → quality ≤ 3 인 문서를 다음 회차 대상으로 식별
  → quality ≥ 4 인 문서 중 회차 4·5 이상이면 졸업 후보 표시
  → 다음 회차 날짜를 quality 별로 계산해 캘린더 형태 정리
  → README 회차 통계 표 갱신
  → quality ≤ 3 인 질문은 카테고리별 _mistakes.md 에 append
  → git status 보여주고 커밋 분할 계획 제시

규약:
- 모든 회차 파일은 write/_review/_template/review-template.md 형식 따름
- 간격·트리거·졸업 기준은 write/_review/_template/review-routine.md §1·§6 따름
- 사용자가 한 편 복습 시작하면 "Q1 부터 자기 답 적기 → '정답 보여줘' 요청 시 정답 → 점수 매김" 순서 의무
- 답을 미리 보여주지 말 것 (Karpicke testing effect)
```

## 실행 주기 권장

### 매주 월·수·금 오전 9시 (학술 근거 기반)

```
cron: 0 9 * * 1,3,5
```

근거:
- **하루 5편 표준** (Pomodoro 25분/5분 × 5회 = 2.5시간) — review-routine.md §5
- **18편 한 회차 = 월·수·금 3 세션** 분할 (6편씩, 살짝 여유)
- **오전 9시** — 인지심리학 연구상 active recall 효과가 가장 큰 시간대
- **회차 간격 (3·7·14·30일)** 이 월·수·금 주기와 자연스럽게 맞음

### `/schedule` 으로 자동 등록 (OMC routine)

다음 Claude 에게 한 번만 요청하시면 cron 등록됨:

```
/schedule 등록:
이름: weekly-review
cron: 0 9 * * 1,3,5
프롬프트: write/_review/_template/coworker-prompts.md 의 "통합 프롬프트" 섹션 그대로 실행
```

또는 mac launchd / cron 으로 직접 등록도 가능 (Claude 외부 트리거).

### 대안 주기

| 주기 | cron | 한 세션 분량 | 적합성 |
|------|------|-----------|--------|
| 월·수·금 9시 (권장) | `0 9 * * 1,3,5` | 5~6편 | ✅ Pomodoro 5편 표준에 부합 |
| 매일 9시 | `0 9 * * *` | 3~4편 | 매일 부담 큼, 주말 강제 학습 |
| 월요일 9시 | `0 9 * * 1` | 18편 한 번에 | active recall 효과 떨어짐 |
| 수동 호출만 | — | 자유 | 시간 제약 광범위, 학술 근거 약함 |

## 한 편 복습 시작 시 (통합 프롬프트가 회차 파일 생성 후 후속 동작)

회차 파일이 생성된 뒤 사용자가 *실제 Q&A 시작* 할 때는 통합 프롬프트가 자동으로 안내하지만, 명시적으로 시작하시려면:

```
write/_review/{날짜}/{파일명}.review.md 의 Q1 부터 시작.
규약: 내가 자기 답을 적은 뒤에만 정답을 보여줘.
```

이 한 줄은 통합 프롬프트의 *규약 섹션* 에 이미 포함되어 있어서 *생략 가능* — 통합 프롬프트가 회차 파일을 만들면 자동으로 "Q1 부터 시작하시겠습니까?" 안내합니다.

## 참조

- [review-template.md](review-template.md) — 복습 파일 표준 템플릿 (5문제 + SM-2 + 3축)
- [review-routine.md](review-routine.md) — 운영 가이드 (간격·졸업·학술 근거)
- [../README.md](../README.md) — 복습 시스템 진입점
