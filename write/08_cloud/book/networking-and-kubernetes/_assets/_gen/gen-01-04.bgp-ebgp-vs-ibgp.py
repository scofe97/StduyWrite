# 01-04.bgp-ebgp-vs-ibgp — 2행 대조 (같은 자리끼리 세로로 맞춰 본다)
# 본문: "같은 프로토콜인데 상대가 남이냐 식구냐로 출력이 갈립니다. 넷째 칸이 이 절의 갈림길입니다."
#        "eBGP 로 배운 것은 iBGP 이웃에게 넘길 수 있고, iBGP 로 배운 것은 넘길 수 없습니다."
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — capture-vantage 와 같은 형태로 맞춰
#           이 편 안에서 대조 도식의 읽는 법이 일관되게 한다.
#           coral 은 본문이 "갈림길"이라 부른 넷째 열 하나에만.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 596
d = D(W, H, "eBGP vs iBGP · SAME PROTOCOL",
      "상대가 남이냐 식구냐가 출력을 가른다",
      "윗줄이 eBGP(AS 65001↔65002), 아랫줄이 iBGP(AS 65001 안). 같은 자리끼리 세로로 맞춰 본다.",
      lead="같은 프로토콜인데 상대가 누구냐로 AS_PATH·localpref·재전달이 갈린다")

LBL_W, CW, GAP, CH = 156, 183, 16, 100
COL0 = 196
COLX = [COL0 + i * (CW + GAP) for i in range(4)]
ROW_Y = [244, 372]
HEAD_Y = 158
HEADS = ["AS_PATH", "표시", "localpref", "iBGP 이웃에 재전달"]
FOCAL_COL = 3                                                   # 본문이 "갈림길"이라 부른 그 열

for i, h in enumerate(HEADS):
    c = ACC if i == FOCAL_COL else SOFT
    d.t(COLX[i] + CW // 2, HEAD_Y, ddx.fit(h, 12, CW - 12, h), 12, c, KR, "middle", 600)
if True:
    x, top = COLX[FOCAL_COL] - 8, HEAD_Y - 26
    bot = ROW_Y[1] + CH // 2 + 12
    d.o.append(f'<rect x="{x}" y="{top}" width="{CW+16}" height="{bot-top}" rx="8" '
               f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
    d.t(x + (CW + 16) // 2, bot + 24, "풀메시가 필요한 이유", 11, ACC, KR)

for r, (kind, sub, cells, c) in enumerate([
        ("eBGP", "r1 ↔ r3 · 다른 AS",
         [("65002 가 붙는다", "AS 를 건널 때마다"), ("external", "밖에서 배운 경로"),
          ("없다", "AS 밖으로 안 나감"), ("한다", "금지 대상 아님")], WARN),
        ("iBGP", "r1 ↔ r2 · 같은 AS",
         [("비어 있다", "vtysh 는 Local 로"), ("internal", "안에서 배운 경로"),
          ("100", "내부 선호도"), ("안 한다", "루프를 막을 길이 없어서")], INFO)]):
    cy = ROW_Y[r]
    d.box(24, cy - CH // 2, LBL_W, CH, PAPER2, c, 1.2, 6)
    d.t(24 + LBL_W // 2, cy - 8, kind, 13, c, MONO, "middle", 600)
    d.t(24 + LBL_W // 2, cy + 14, ddx.fit(sub.split(" · ")[1], 11, LBL_W - 16, kind), 11, MUTED, KR)
    for i, (main, note) in enumerate(cells):
        x = COLX[i]
        cc = ACC if i == FOCAL_COL else RULE
        d.box(x, cy - CH // 2, CW, CH, PAPER2, cc, 1.1, 6)
        d.t(x + CW // 2, cy - 6, ddx.fit(main, 12, CW - 16, main), 12,
            ACC if i == FOCAL_COL else INK, KR, "middle", 600)
        d.t(x + CW // 2, cy + 16, ddx.fit(note, 11, CW - 16, note), 11, MUTED, KR)

d.t(36, 500, "금지되는 것은 iBGP 로 배운 것을 다시 iBGP 로 넘기는 경우뿐이다 — "
             "eBGP 로 배운 경로는 iBGP 이웃에게 넘어간다", 12, MUTED, KR, "start")
d.legend(556, [("eBGP", WARN), ("iBGP", INFO), ("갈림길", ACC)])
d.save("01-04.bgp-ebgp-vs-ibgp.svg")
print("ok bgp-ebgp-vs-ibgp")
