# 02-02 §3 — 원문의 필터 세 번 시도가 각각 어느 방향의 트래픽을 보여주는가.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가를 행×열 격자로 본다.
#           축약: 스펙의 역할(role)·컴포넌트(component) 어휘 대신 필터×방향 축을 쓴다.
#           visual-diagram-selection §알려진 공백이 이 격자 문법을 일반 대조표로 쓰는 선례다.
#           level 어휘는 full/none 두 단계만 쓰고, focal 은 대화가 드러나는 셀 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, COL_W, ROW_H = 384, 216, 76
COLS = [("10.0.0.221", "→ 122.167.99.148"), ("122.167.99.148", "→ 10.0.0.221")]
ROWS = [
    ("ip.src == 10.0.0.221", "출발지만 고정합니다",
     [("보임", OK), ("안 보임", BAD)]),
    ("(ip.src == …) && (ip.dst == …)", "양쪽을 고정해도 한 방향입니다",
     [("보임", OK), ("안 보임", BAD)]),
    ("ip.addr == 122.167.99.148", "출발지와 목적지를 모두 매칭합니다",
     [("보임", OK), ("보임", None)]),
]
X0, Y0 = 24, 140
W = X0 + LABEL_W + len(COLS) * COL_W + 24
H = Y0 + 40 + len(ROWS) * ROW_H + 96

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-02 §3",
      "필터 세 번과 보이는 방향",
      "같은 두 호스트의 대화를 세 가지 디스플레이 필터로 걸었을 때 각각 어느 방향이 보이는가. 앞의 둘은 한 방향만 보여주고, ip.addr 만이 양방향을 함께 보여준다.",
      "출발지를 고정하는 필드로는 대화가 보이지 않습니다 — 주소를 양쪽에서 매칭해야 합니다")

# 헤더
d.t(X0 + 8, Y0 + 4, "적용한 필터", 11, SOFT, KR, "start", 600)
for j, (a, b) in enumerate(COLS):
    cx = X0 + LABEL_W + j * COL_W + COL_W / 2
    d.t(cx, Y0 - 12, a, 11, SOFT, MONO)
    d.t(cx, Y0 + 4, b, 11, SOFT, MONO)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

for i, (name, hint, cells) in enumerate(ROWS):
    y = Y0 + 40 + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 26, name, 12, INK, MONO, "start", 600)
    d.t(X0 + 16, y + 46, hint, 11, MUTED, KR, "start")
    for j, (val, c) in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W
        focal = (c is None)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{COL_W - 12}" height="{ROW_H - 12}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + (COL_W - 12) / 2, y + 30, val, 13, ACC, KR, "middle", 600)
            d.t(x + (COL_W - 12) / 2, y + 50, "대화가 드러납니다", 11, MUTED, KR)
        else:
            d.tone(x, y, COL_W - 12, ROW_H - 12, c, 6)
            d.t(x + (COL_W - 12) / 2, y + 38, val, 13, c, KR, "middle", 600)

d.legend(H - 72, [("보임", OK), ("안 보임", BAD), ("양방향이 함께", ACC)])
d.save("02-02.filter-direction-matrix.svg")
