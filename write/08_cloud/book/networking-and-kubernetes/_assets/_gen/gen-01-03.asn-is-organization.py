# 01-03.asn-is-organization — 조직 경계 + 내부 라우터 다수
# 본문: "ASN 은 라우터가 아니라 조직에 붙는다. 라우터는 여섯 대지만 밖에서 보이는 번호는
#        둘뿐이라 AS 목록에도 숫자가 두 개만 남는다."
# 타입 스펙: type-nested.md 의 조직 경계 + type-dependency.md 의 이웃 관계선.
#           경계를 넘는 변 하나만 eBGP — 거기에만 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 612
d = D(W, H, "ASN BELONGS TO AN ORGANIZATION",
      "ASN 은 라우터가 아니라 조직에 붙는다",
      "가로 한 줄만 eBGP 이고 나머지는 모두 iBGP 다 — 라우터는 여섯 대지만 밖에서 보이는 번호는 둘뿐이다",
      lead="한 줄만 eBGP, 나머지는 iBGP — 라우터 여섯 대에 번호는 둘뿐이다")

BW, BH = 140, 96
R1 = (40, 200, 430, 240)
R2 = (530, 200, 430, 240)
E1, E2 = (390, 320), (610, 320)                     # 경계 라우터
I1 = [(170, 254), (170, 386)]
I2 = [(830, 254), (830, 386)]

def rt(cx, cy, title, sub, tag, c=None):
    x, y = cx - BW // 2, cy - BH // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 16, title, 12, c or INK, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(sub, 11, BW - 18, sub), 11, MUTED, KR)
    d.t(cx, cy + 26, tag, 10, SOFT, MONO)

ddx.band(d, 104, 548, "번호는 라우터 대수와 무관하다 — 조직 하나에 하나씩 붙는다")
for (rx, ry, rw, rh), lab in [(R1, "AS 100 — 사업자 한 곳"), (R2, "AS 200 — 다른 사업자")]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, lab, 11, INFO)

rt(*E1, "경계 라우터", "eBGP 를 맡는다", "AS 100")
rt(*E2, "경계 라우터", "eBGP 를 맡는다", "AS 200")
for cx, cy in I1: rt(cx, cy, "내부 라우터", "iBGP 만 한다", "AS 100")
for cx, cy in I2: rt(cx, cy, "내부 라우터", "iBGP 만 한다", "AS 200")

for (ix, iy), (ex, ey) in [(I1[0], E1), (I1[1], E1), (I2[0], E2), (I2[1], E2)]:
    sx = ix + BW // 2 + 6 if ix < ex else ix - BW // 2 - 6
    tx = ex - BW // 2 - 8 if ix < ex else ex + BW // 2 + 8
    d.path(f"M {sx} {iy} L {tx} {ey}", MUTED, 1.3, dash="5 5")
d.line(I1[0][0], I1[0][1] + BH // 2 + 4, I1[1][0], I1[1][1] - BH // 2 - 4, MUTED, 1.3, "5 5")
d.line(I2[0][0], I2[0][1] + BH // 2 + 4, I2[1][0], I2[1][1] - BH // 2 - 4, MUTED, 1.3, "5 5")
d.t(170 + 14, 324, "iBGP", 11, MUTED, MONO, "start")
d.t(830 + 14, 324, "iBGP", 11, MUTED, MONO, "start")

d.path(f"M {E1[0]+BW//2+8} {E1[1]} L {E2[0]-BW//2-10} {E2[1]}", ACC, 1.8, m="acc")
d.t(500, 300, "eBGP", 12, ACC, MONO, "middle", 600)
d.t(500, 356, "여기서만 번호가 붙는다", 11, ACC, KR)

d.t(36, 500, "밖에서 보이는 번호는 둘뿐이라 이 구간을 지난 AS 목록에는 숫자가 두 개만 남는다", 12, MUTED, KR, "start")
d.chip(500, 470, "AS_PATH  [100, 200]", INFO, 12)
d.legend(564, [("조직 경계", INFO), ("경계를 넘는 한 줄", ACC)])
d.save("01-03.asn-is-organization.svg")
print("ok asn-is-organization")
