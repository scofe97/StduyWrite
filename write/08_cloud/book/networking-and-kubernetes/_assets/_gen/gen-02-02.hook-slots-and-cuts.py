# 02-02.hook-slots-and-cuts — 어느 테이블이 어느 훅에 붙는가
# 본문 요구: 본문 표는 어느 칸이 비었는지만 보이고 왜 비었는지를 안 보인다.
#           빈칸의 이유가 전부 하나의 축(라우팅 결정 전인가 뒤인가)에서 나온다.
# 타입 스펙: type-dp-security-matrix.md — 어느 조합이 되고 안 되는가.
#           열은 훅을 시점 순으로, 행은 테이블, 오른쪽 열에 그 행이 지키는 규칙 한 줄.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 540
d = D(W, H, "iptables · TABLE x HOOK",
      "어느 테이블이 어느 훅에 붙는가",
      "빈칸은 규칙을 안 넣어서가 아니라 그 시점에 그 일을 할 수 없어서 비어 있다.",
      lead="빈칸의 이유는 하나다 — 라우팅 결정 전인가 뒤인가")

X0, CW, GAP = 150, 118, 8
RX0, RW = 786, 190
def cx(i): return X0 + i * (CW + GAP) + CW / 2

HOOKS = [("PREROUTING", "결정 전"), ("INPUT", "나에게 확정"), ("FORWARD", "통과 확정"),
         ("OUTPUT", "내가 보냄"), ("POSTROUTING", "나가기 직전")]
HY, HH = 106, 52
for i, (nm, sub) in enumerate(HOOKS):
    x = X0 + i * (CW + GAP)
    d.box(x, HY, CW, HH, PAPER2, RULE, 1.0)
    d.t(cx(i), HY + 21, ddx.fit(nm, 11, CW - 12, f"hook {nm}"), 11, INK, MONO, "middle", 600)
    d.t(cx(i), HY + 38, ddx.fit(sub, 11, CW - 12, f"sub {sub}"), 11, MUTED, KR)
d.t(RX0 + RW / 2, HY + 32, "이 행이 지키는 규칙", 11, SOFT, KR)

ROWS = [
    ("raw",    "conntrack 시작 전이라야",   ["NOTRACK", None, None, "NOTRACK", None]),
    ("mangle", "제약 없음 · 다섯 모두",      ["표시", "표시", "표시", "표시", "표시"]),
    ("nat",    "결정 전이거나 나가기 직전",  ["DNAT", "(형식)", None, "DNAT", "SNAT"]),
    ("filter", "운명이 정해진 뒤라야",       [None, "차단", "차단", "차단", None]),
]
FOCAL = {(2, 2), (3, 0)}          # nat x FORWARD · filter x PREROUTING — 이 편의 물음
RY0, RH, RG = 172, 56, 8

for r, (tbl, rule, cells) in enumerate(ROWS):
    y = RY0 + r * (RH + RG)
    d.t(24, y + RH / 2 + 5, ddx.fit(tbl, 13, 118, f"table {tbl}"), 13, INK, MONO, "start", 600)
    for c, val in enumerate(cells):
        x = X0 + c * (CW + GAP)
        focal = (r, c) in FOCAL
        if val:
            col = SOFT if val == "(형식)" else INFO
            d.tone(x + 8, y + 10, CW - 16, RH - 20, col, 6, "14", 1.0)
            latin = all(ord(ch) < 128 for ch in val)
            d.t(cx(c), y + RH / 2 + 4,
                ddx.fit(val, 11, CW - 24, f"cell {tbl}/{val}"),
                11, col, MONO if latin else KR)
        else:
            col = ACC if focal else SOFT
            d.o.append(f'<rect x="{x+8}" y="{y+10}" width="{CW-16}" height="{RH-20}" rx="6" '
                       f'fill="none" stroke="{col}" stroke-width="{1.4 if focal else 0.9}" '
                       f'stroke-dasharray="4 4"/>')
            d.t(cx(c), y + RH / 2 + 4, "없다" if focal else "—", 11, col, KR)
    d.t(RX0 + 8, y + RH / 2 + 4,
        ddx.fit(rule, 11, RW - 16, f"rule {tbl}"), 11, MUTED, KR, "start")
    if r < len(ROWS) - 1:
        d.line(24, y + RH + RG / 2, W - 48, y + RH + RG / 2, RULE, 0.8)

d.t(24, 452,
    "nat 은 주소를 바꾸면 라우팅이 달라지므로 결정 전이거나 나가기 직전이라야 하고,",
    12, MUTED, KR, "start")
d.t(24, 472,
    "filter 는 통과 여부를 정하므로 이 패킷의 운명이 정해진 뒤라야 뜻이 선다.",
    12, MUTED, KR, "start")
d.legend(492, [("붙는다", INFO), ("붙지 않는다 — 이 편의 물음", ACC)])
d.save("02-02.hook-slots-and-cuts.svg")
print("ok hook-slots-and-cuts")
