# 07-02 §라벨 둘로 Pod 를 2차원으로 조직한다
# 본문·옛 도식: 가로 = app(애플리케이션), 세로 = rel(릴리스). app=quote 셀렉터는 quote 열의
#   stable+canary 를 전부 고르고, rel=canary 는 canary 행 전체를, app=quote,rel=canary 는
#   quote-canary 하나만 고른다.
# 타입 스펙: type-dp-security-matrix.md — 축이 둘이고 셀렉터가 '행 또는 열' 을 고른다는 것이 요점이라 격자로 둔다.
#           격자여야 셀렉터가 무엇을 고르는지가 면적으로 보인다 — 목록으로는 안 보인다.
#           가로축이 app 라벨, 세로축이 rel 라벨인 2 차원 격자이고 칸이 곧 Pod 다. 셀렉터가 고르는 것이
#           열인지 행인지 한 칸인지가 면적으로 읽힌다 — 축이 둘 다 의미를 지는 정본 그대로의 격자다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 632
d = D(W, H, "KUBERNETES IN ACTION · 07-02",
      "라벨 둘을 붙이는 순간 Pod 가 격자로 정렬된다",
      "가로축은 app, 세로축은 rel 이다. 셀렉터는 이 격자에서 열을 고르거나 행을 고르거나 "
      "한 칸을 고른다 — 무엇을 고르는지가 면적으로 보인다.",
      lead="라벨이 없으면 Pod 는 그냥 무질서한 목록이다")

# 열 머리글을 y=268 에 두면 첫 행 상자(254~346) 밑에 깔린다 — 격자 위로 올린다.
COLS = [("app: kiada", 300), ("app: quiz", 530), ("app: quote", 760)]
ROWS = [("rel: stable", 312), ("rel: canary", 436)]
HDR_Y = 214
CW, CH = 190, 92

ddx.band(d, 104, 576, "app=quote 는 열 하나를, rel=canary 는 행 하나를, 둘을 겹치면 칸 하나를 고른다")

# quote 열 강조 — 본문이 드는 예
d.o.append(f'<rect x="{760-CW//2-12}" y="236" width="{CW+24}" height="284" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, 760 - CW // 2 - 12, 236, "app=quote 가 고르는 범위", 11, ACC, off=14)

for name, x in COLS:
    d.t(x, HDR_Y, name, 12, SOFT, MONO)
for name, y in ROWS:
    d.t(150, y + 5, name, 12, SOFT, MONO, "end")

CELLS = {(0, 0): "kiada-xxx", (1, 0): "quiz", (2, 0): "quote-xxx",
         (0, 1): "kiada-canary", (2, 1): "quote-canary"}
for (ci, ri), pod in CELLS.items():
    x, y = COLS[ci][1], ROWS[ri][1]
    c = ACC if ci == 2 else INFO
    d.box(x - CW // 2, y - CH // 2, CW, CH, PAPER2, c, 1.1, 6)
    d.t(x, y - 12, pod, 12, c, MONO, "middle", 600)
    d.t(x, y + 10, COLS[ci][0], 10, SOFT, MONO)
    d.t(x, y + 28, ROWS[ri][0], 10, SOFT, MONO)

d.t(530, 482, "quiz 에는 canary 가 없다", 10, SOFT, KR)

d.t(36, 552, "셀렉터를 겹칠수록 범위가 좁아진다 — app=quote,rel=canary 는 quote-canary 하나만 "
             "남는다.", 12, MUTED, KR, "start")
d.legend(592, [("격자 위의 Pod", INFO), ("app=quote 가 고르는 열", ACC)])
d.save("07-02-labels-two-dimensions.svg")
print("ok labels-two-dimensions")
