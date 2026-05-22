---
title: write 학습 문서 복습 시스템
tags: [moc, review, spaced-repetition, sm-2]
status: final
related:
  - ./_template/review-template.md
  - ./_template/review-routine.md
  - ../README.md
updated: 2026-05-22
---

# write 학습 문서 복습 시스템

---

> write/ 의 모든 학습 문서를 *간격 반복(spaced repetition) + 능동 회상(active recall)* 으로 장기 기억에 안착시키는 시스템. Ebbinghaus 망각곡선 + SM-2 알고리즘 + Karpicke testing effect 의 학술 근거 기반.

## 빠른 시작

오늘이 복습을 시작할 좋은 날인가? 아래 두 갈래 중 하나:

- **신규 학습 문서를 push 한 직후** → [routine §7.1 신규 회차 1 시작](_template/review-routine.md#71-신규-회차-1-시작--최근-푸시된-문서-자동-식별) 프롬프트 복붙
- **회차 2 이상의 예정 날짜가 오늘** → [routine §7.4 캘린더 트리거](_template/review-routine.md#74-회차-2-이상--캘린더-기반-트리거) 프롬프트 복붙

두 갈래 모두 *Claude 에게 프롬프트 한 줄 복붙* 으로 자동 시작.

## 구조

```
write/_review/
├── README.md                        ← 진입점 (현재 파일, 회차 통계 표)
├── _template/
│   ├── review-template.md           ← 복습 파일 표준 템플릿 (5문제 + SM-2 + 3축)
│   └── review-routine.md            ← 운영 가이드 (간격·트리거·졸업·코워크 프롬프트)
└── YYYY-MM-DD/                      ← 회차별 날짜 폴더
    └── {카테고리}_{번호}.review.md   ← 문서별 1파일
```

`_review/` 와 `_template/` 의 언더스코어 prefix 는 [second-brain-harness.md §4.1](../../../claude/.claude/skills/content/writing/references/second-brain-harness.md) 의 "일반 최종본이 아님" 규약.

## 핵심 원칙 3가지

1. **Active recall (Karpicke & Roediger 2006)** — 답을 *떠올린 뒤* 정답과 비교. 답을 먼저 보면 학습 효과 80% 감소
2. **Spaced repetition (Ebbinghaus 1885)** — 1·3·7·14·30일 간격으로 회차 반복. 매번 quality 점수로 다음 간격 조정 (SM-2 변형)
3. **Interleaving (회차 4 이상)** — 회차 1~3 은 같은 카테고리 blocked, 회차 4+ 는 카테고리 무관 섞기 (transfer 효과)

## 회차 통계 표

> 각 회차 종합 평가 후 자동 갱신. 평균 quality 가 회차마다 올라가는지가 학습 효과의 직접 지표.

| 회차 | 날짜 | 대상 편수 | 평균 quality | 3축 평균 | 졸업 수 |
|------|------|---------|------------|---------|--------|
| 1 | 2026-05-26 (예정) | 18 (querydsl 16 + JDBC 2) | _ | _ | _ |

회차 5 에서 *졸업 수 / 대상 편수 ≥ 80%* 면 본 시스템이 잘 작동하는 것.

## 졸업한 문서 목록

> 회차 4~5 에서 졸업 기준 (quality ≥ 4 + 메타인지 평균 ≥ 3.6 + 미해결 _mistakes 0개) 충족한 문서.

*(아직 졸업 문서 없음 — 첫 회차 30일 후 첫 졸업 후보 등장 예정)*

## 운영 중인 오답 노트

| 카테고리 | _mistakes.md 경로 | 누적 패턴 수 |
|---------|------------------|------------|
| querydsl | `../06_data/querydsl/_mistakes.md` | 0 |
| JDBC wrap | `../06_data/_mistakes.md` | 0 |

복습 회차에서 *quality ≤ 3 인 질문* 이 발생할 때마다 해당 카테고리 `_mistakes.md` 에 append. 같은 패턴 *3회 이상* 반복 시 원본 챕터 본문 보강 트리거.

## 학술 근거

본 시스템의 모든 설계 결정은 다음 학술 근거에 기반:

- [Forgetting curve (Ebbinghaus 1885, Wikipedia)](https://en.wikipedia.org/wiki/Forgetting_curve) — 1h 안 50%, 24h 안 70% 망각
- [Karpicke & Roediger (2006)](https://cognitivetrain.com/active-recall/) — 1주일 후 retrieval practice 그룹이 80% 더 많이 기억
- [Rowland (2014) 메타분석](https://www.sciencedirect.com/science/article/abs/pii/S0959475217301810) — 159 비교/61 연구, retrieval practice 효과 medium-large
- [SuperMemo SM-2 (Wozniak 1987)](https://en.wikipedia.org/wiki/SuperMemo) — quality 점수 + easiness factor 기반 간격 자동 조정
- [Interleaving research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476370/) — 초보 blocked, 숙련 interleaved

상세는 [_template/review-routine.md](_template/review-routine.md) §1·§4 참조.

## 관련 문서

- [_template/review-template.md](_template/review-template.md) — 복습 파일 표준 템플릿
- [_template/review-routine.md](_template/review-routine.md) — 운영 가이드 + 코워크 프롬프트 §7
- [`../../../claude/.claude/skills/content/writing/references/02-learned-docs.md`](../../../claude/.claude/skills/content/writing/references/02-learned-docs.md) §12~§15 — 학습 문서 하네스의 Stage 2 워크플로우 규약
