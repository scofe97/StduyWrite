# 02-03 전체 지도 — 예측 → 결정 → 정량화 → 보이기.
# 타입 스펙: type-process — 주체 없는 단계 지도. 칸마다 절 번호·이름·다루는 것이 같은 자리에 반복된다.
#           축약: lanes·§2 공식 대신 카드 stride(selection §알려진 공백 "주체 없는 단계 지도").
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 928, 420
X0, CW, GAP, Y0, CH = 24, 196, 28, 120, 196
CARDS = [
    ("§1–3", "예측", ["확장성 프로파일", "Amdahl · USL", "큐잉 M/D/1"], "부하가 늘면?"),
    ("§4", "결정", ["자원 한계 외삽", "요인 분석", "수직 · 수평 · 샤딩"], "무엇을 살까?"),
    ("§5", "정량화", ["이득 정량화", "평균 · 백분위", "다봉 · 이상치"], "숫자를 믿을까?"),
    ("§6–7", "보이기", ["시간 패턴", "라인 · 산점도", "히트맵"], "모양이 보이나?"),
]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03",
       "예측하고, 결정하고, 재고, 보인다",
       "02-03 의 일곱 절을 네 단계로 묶었다. 모델로 예측하고, 그 예측으로 용량을 정하고, 측정값을 통계로 정량화하고, 시각화로 모양을 보인다.",
       "칸마다 절 번호 · 다루는 것 · 답하는 질문")

for i, (tag, name, items, q) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    focal = name == "정량화"
    if focal: d.tone(x, Y0, CW, CH, ACC, 8)
    else: d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y0 + 28, tag, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + CW - 16, Y0 + 28, name, 15, ACC if focal else INK, KR, "end", 600)
    d.line(x + 16, Y0 + 44, x + CW - 16, Y0 + 44, RULE, 0.8)
    for k, it in enumerate(items):
        d.t(x + 16, Y0 + 72 + k * 26, it, 13, INK, KR, "start")
    d.t(x + 16, Y0 + CH - 18, q, 13, ACC if focal else MUTED, KR, "start")
    if i < 3:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + CW + GAP - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(Y0 + CH + 32, [("이 편의 중심 — 평균을 의심하기", ACC), ("나머지 단계", MUTED)])
d.save("02-03.chapter-overview.svg")
