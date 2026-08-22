# 01-03.vlan-isolation — 태그별 도메인 분리
# 본문: "배선은 그대로 두고 태그만으로 도메인을 가른다. 같은 스위치에 꽂혀 있어도
#        태그가 다르면 옆 그룹의 방송이 들리지 않는다. 받고 버릴 남의 프레임이 줄어드니
#        혼잡과 노출이 함께 줄어든다."
# 타입 스펙: type-nested.md — 물리 한 겹 안에 논리 두 겹. 갈라짐 자체가 요점이라
#           경계선(둘 사이)에 focal 을 건다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "VLAN · ONE SWITCH, TWO DOMAINS",
      "VLAN — 같은 장비인데 서로 들리지 않는다",
      "물리 배선은 그대로 두고 태그로 브로드캐스트 도메인을 가른다",
      lead="물리 배선은 그대로 두고 태그로 브로드캐스트 도메인을 가른다")

SWX, SWY, SWW, SWH = 120, 176, 760, 76
DOM_Y, DOM_H, DOM_W = 296, 148, 356
D10_X, D20_X = 120, 524
MIDX = (D10_X + DOM_W + D20_X) // 2                # 두 도메인 사이

ddx.band(d, 104, 552, "포트는 전부 같은 장비에 꽂혀 있다 — 갈라지는 것은 배선이 아니라 태그다")

d.box(SWX, SWY, SWW, SWH, PAPER2, RULE, 1.1, 6)
d.t(SWX + SWW // 2, SWY + 30, "물리 스위치 한 대", 13, INK, KR, "middle", 600)
d.t(SWX + SWW // 2, SWY + 52, "포트는 전부 같은 장비 · 배선은 그대로", 11, MUTED, KR)

for x, name, tag, note, c in [(D10_X, "VLAN 10", "태그 10", "브로드캐스트가 이 안에서만", INFO),
                              (D20_X, "VLAN 20", "태그 20", "옆 태그의 방송은 안 들린다", WARN)]:
    d.o.append(f'<rect x="{x}" y="{DOM_Y}" width="{DOM_W}" height="{DOM_H}" rx="8" '
               f'fill="{c}08" stroke="{c}" stroke-width="1.2"/>')
    ddx.ring_label(d, x, DOM_Y, f"{name} · {tag}", 11, c)
    cx = x + DOM_W // 2
    for i in range(3):                              # 같은 도메인 안의 호스트들
        hx = x + 40 + i * 96
        d.box(hx, DOM_Y + 44, 76, 44, PAPER2, c, 1.0, 5)
        d.t(hx + 38, DOM_Y + 71, f"호스트 {i+1}", 11, c, KR)
    d.t(cx, DOM_Y + 118, ddx.fit(note, 11, DOM_W - 24, note), 11, MUTED, KR)
    d.path(f"M {cx} {SWY+SWH+6} L {cx} {DOM_Y-10}", MUTED, 1.4, m="ar")

# ── 갈라짐 그 자체 (focal) ────────────────────────────────
d.line(MIDX, DOM_Y - 16, MIDX, DOM_Y + DOM_H + 12, ACC, 1.6, "6 6")
ddx.focal_tag(d, MIDX, DOM_Y + DOM_H + 34, "태그가 다르면 방송이 안 넘어간다", 264)

d.t(36, 520, "받고 버릴 남의 프레임이 줄어드니 혼잡과 노출이 함께 줄어든다 — "
             "VLAN 이 가두는 기술인 이유가 이것이다", 12, MUTED, KR, "start")
d.legend(568, [("VLAN 10", INFO), ("VLAN 20", WARN), ("갈라지는 자리", ACC)])
d.save("01-03.vlan-isolation.svg")
print("ok vlan-isolation")
