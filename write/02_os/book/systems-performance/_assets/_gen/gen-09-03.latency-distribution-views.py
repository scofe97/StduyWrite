# 09-03 §3 — 평균 하나는 봉우리가 둘인 분포를 가린다.
# 타입 스펙: type-process — 같은 데이터를 세 방식으로 볼 때 무엇이 보이고 무엇이 사라지는지의 대조 지도.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 480
CW, CH, GAP, X0, Y = 280, 196, 24, 24, 132

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-03 §3",
       "같은 I/O 를 세 가지로 본다",
       "한 디스크는 캐시 적중과 미스라는 두 종류 지연을 섞어 돌려준다. 평균은 그 사이 어딘가를 가리켜 실제로는 없는 값이 된다.",
       "봉우리가 둘인 분포를 평균 하나로 접으면 둘 다 사라집니다")

CARDS = [
    ("평균", "iostat 의 한 줄", ACC,
     ["적중 100μs 와 미스 8ms 를", "하나로 접습니다.", "그 중간값은 실제로", "일어나지 않은 지연입니다"],
     "가장 싸지만 가장 많이 가립니다"),
    ("히스토그램", "biolatency", OK,
     ["구간별 개수를 세어", "봉우리가 둘임을 드러냅니다.", "적중 무리와 미스 무리가", "따로 보입니다"],
     "분포의 모양을 봅니다"),
    ("건당 추적", "biosnoop · 히트맵", INFO,
     ["I/O 하나하나를 시각에", "찍습니다. 이상치가", "언제 몰렸는지, 무엇과", "겹쳤는지 보입니다"],
     "가장 비싸고 가장 자세합니다"),
]
for i, (name, tool, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 15, c, KR, "start", 600)
    d.t(x + CW - 16, Y + 30, tool, 12, SOFT, MONO, "end")
    d.line(x + 16, Y + 46, x + CW - 16, Y + 46, RULE, 0.8)
    for j, l in enumerate(body):
        d.t(x + 16, Y + 72 + j * 20, l, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "지연이 시간에 따라 어떻게 변하는지 보려면 히트맵을 씁니다 — 축은 시각과 지연, 색은 그 칸에 떨어진 I/O 수입니다", 13, MUTED, KR, "start")

d.legend(YB + 24, [("가리는 쪽", ACC), ("모양을 드러내는 쪽", OK), ("낱낱이 보는 쪽", INFO)])
d.save("09-03.latency-distribution-views.svg")
