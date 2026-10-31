# 14-03 §4 — 14장에서 1장까지 책 전체 종합 체계. 1~13장의 기술 주제를 장 묶음으로 쌓고 맨 위에 14장의 윤리적 책임을 둔다.
# 장 묶음(1~2·3~5·6~10·11~13·14)은 본문 표에 없는 정리라 Part 번호·목적/수단 축을 지우고 장 범위만 남겼다(2026-10-31 검증).
# 사실 출처: 14-03 본문 §4(L74~L103), DDIA 2판 Ch.14 "Summary" (PDF p.16~17).
# 타입 스펙: type-layers
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
STACK_X = 64
STACK_W = 788
STACK_Y = 152
LAYER_H = 58
INSIGHT_Y = STACK_Y + 5 * LAYER_H + 16
INSIGHT_H = 36
LEG = INSIGHT_Y + INSIGHT_H + 20
H = LEG + 52

d = D(W, H, "14-03 · §4 BOOK SUMMARY ARC", "14장에서 1장까지 책 전체 종합 체계",
      "1~13장의 기술 주제를 장 묶음으로 쌓고, 맨 위에 차별·착취·감시·프라이버시를 다룬 14장의 윤리적 책임을 둔다.",
      "1~2장 비기능 요구사항 · 3~5장 모델과 저장 · 6~10장 분산과 일관성 · 11~13장 배치와 스트림 · 14장 윤리")

# 상단 공통 전제 배너
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 23, "마지막 장은 한 걸음 물러나 데이터 시스템을 만드는 일의 윤리를 살핌", 12, INK, KR, "middle", 600)

# 좌측 방향 지시 (장 순서)
d.t(36, STACK_Y + 12, "14장", 11, ACC, KR, "middle", 600)
d.arrow([(36, STACK_Y + 5 * LAYER_H - 14), (36, STACK_Y + 22)], ACC, "acc", 1.4)
d.t(36, STACK_Y + 5 * LAYER_H - 2, "1장", 11, SOFT, KR, "middle")

layers = [
    ("14장", "옳은 일 하기", "차별 · 착취 · 감시 · 프라이버시의 윤리적 책임", ACC, True),
    ("11~13장", "배치 · 스트림 처리와 스트리밍 철학", "Unix 도구에서 분산 배치 · CDC · 시스템 통합", INFO, False),
    ("6~10장", "분산 데이터와 일관성", "복제 · 샤딩 · 트랜잭션 · 분산 결함 · 합의", WARN, False),
    ("3~5장", "데이터 모델 · 저장 · 인코딩과 진화", "관계형/문서/그래프 · LSM/B-tree · 직렬화", RULE, False),
    ("1~2장", "아키텍처와 비기능 요구사항", "아키텍처 트레이드오프 · 신뢰성 · 확장성 · 유지보수성", RULE, False),
]

for idx, (tag, name, note, color_token, is_focal) in enumerate(layers):
    ly = STACK_Y + idx * LAYER_H
    
    if is_focal:
        d.tone(STACK_X, ly, STACK_W, LAYER_H - 4, ACC, 6, "1C", 1.4)
        d.chip(STACK_X + 44, ly + (LAYER_H - 4) / 2, tag, ACC, 11)
        d.t(STACK_X + 96, ly + (LAYER_H - 4) / 2 + 5, name, 13.5, ACC, KR, "start", 600)
        d.t(STACK_X + STACK_W - 16, ly + (LAYER_H - 4) / 2 + 4, note, 12, ACC, KR, "end")
    else:
        d.box(STACK_X, ly, STACK_W, LAYER_H - 4, PAPER2, RULE, 0.9)
        d.chip(STACK_X + 44, ly + (LAYER_H - 4) / 2, tag, color_token if color_token != RULE else SOFT, 11)
        d.t(STACK_X + 96, ly + (LAYER_H - 4) / 2 + 5, name, 13.5, INK, KR, "start", 600)
        d.t(STACK_X + STACK_W - 16, ly + (LAYER_H - 4) / 2 + 4, note, 12, MUTED, KR, "end")

# 하단 책임 패널 (본문 §4 마지막 문단)
d.box(28, INSIGHT_Y, W - 56, INSIGHT_H, PAPER2, RULE, 1.0)
d.t(W / 2, INSIGHT_Y + 23, "엔지니어의 책임: 사람을 인간으로서 존중하며 대하는 세상을 향해 일하기", 12, INK, KR, "middle")

d.legend(LEG, [
    ("14장 윤리 (focal)", ACC),
    ("배치·스트림", INFO),
    ("분산·합의", WARN),
    ("모델·저장·기초", SOFT),
])

d.save("14-03.book-summary-arc.svg")
