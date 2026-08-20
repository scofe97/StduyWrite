# 01-03.chapter-overview — 중첩 포함 관계 (01-01/01-02 의 4단계 arc 와 다르다)
# 본문: "바깥 테두리가 §1의 전제이고 나머지 셋이 그 안에 들어 있습니다.
#        IP 가 도착을 보장하지 않기 때문에 주소·길 찾기·이웃 찾기가 비로소 필요해진다는 포함 관계"
# 타입 스펙: type-nested.md — 링 라벨은 좌상단 mono eyebrow, paper 마스크를 테두리 위에 얹는다.
#           coral 은 한 겹에만(여기서는 전제 링). 안쪽 padding 은 일정하게.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 492
d = D(W, H, "01-03 · CHAPTER MAP",
      "IP 라우팅과 Ethernet 전체 지도 — 전제 하나가 나머지를 감싼다",
      "IP 가 도착을 보장하지 않기 때문에 안쪽 셋이 필요해진다. 각 칸의 꼬리표가 그 대목을 다루는 절이다.",
      lead="IP 가 도착을 보장하지 않기 때문에 안쪽 셋이 필요해진다 · 꼬리표가 그 대목을 다루는 절")

RING = (40, 116, 920, 300)                     # x, y, w, h — 전제 링 (focal, 한 겹만)
BOX_W, BOX_H, GAP = 228, 116, 56
INNER_X = 102                                  # 링 안쪽 padding 62 (type-nested 권장 24~32 의 확대)
CX = [INNER_X + BOX_W // 2 + i * (BOX_W + GAP) for i in range(3)]   # 216 500 784
CY, STRIP = 236, (INNER_X, 324, 796, 64)

# ── 전제 링 ────────────────────────────────────────────────
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{ACC}08" stroke="{ACC}" stroke-width="1.4"/>')
ddx.ring_label(d, rx, ry, "§1 전제 — IP 는 도착을 보장하지 않는다")

# ── 안쪽 셋 — 전제가 있어야 비로소 필요해지는 것들 ─────────
for cx, (t, s, tag) in zip(CX, [("주소", "CIDR · NAT · IPv6", "§2 어디로 보낼까"),
                                ("길 찾기", "BGP 로 망 사이", "§3 어느 망으로"),
                                ("옆 이웃", "ARP 로 MAC 을", "§4 어느 기계로")]):
    x, y = cx - BOX_W // 2, CY - BOX_H // 2
    d.box(x, y, BOX_W, BOX_H, PAPER2, RULE, 1.1, 6)
    d.t(cx, CY - 22, ddx.fit(t, 15, BOX_W - 24, t), 15, INK, KR, "middle", 600)
    d.t(cx, CY + 2, ddx.fit(s, 12, BOX_W - 24, s), 12, MUTED, KR)
    d.t(cx, CY + 32, tag, 11, SOFT, KR)

for i, lab in enumerate(["망 단위", "기계 단위"]):
    a, b = CX[i] + BOX_W // 2, CX[i + 1] - BOX_W // 2
    d.path(f"M {a+8} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 14, lab, 11, MUTED, KR)

# ── 셋을 한 흐름으로 잇는 자리 ─────────────────────────────
sx, sy, sw, sh = STRIP
d.box(sx, sy, sw, sh, PAPER2, RULE, 1.1, 6)
d.t(sx + sw // 2, sy + 26, "§5 한 요청 — 감싸고 벗긴다", 13, INK, KR, "middle", 600)
d.t(sx + sw // 2, sy + 48, "앞의 셋이 요청 하나 안에서 순서대로 일어난다", 12, MUTED, KR)
for cx in CX:
    d.path(f"M {cx} {CY+BOX_H//2+6} L {cx} {sy-10}", MUTED, 1.3, m="ar")

d.line(24, 440, W - 48, 456, RULE, 0.8)
d.t(24, 462, "READING ORDER", 8, SOFT, MONO, "start")
d.t(140, 462, "전제(§1) → 주소(§2) → 길 찾기(§3) → 옆 이웃(§4) → 한 요청(§5)", 11, MUTED, KR, "start")
d.save("01-03.chapter-overview.svg")
print("ok chapter-overview")
