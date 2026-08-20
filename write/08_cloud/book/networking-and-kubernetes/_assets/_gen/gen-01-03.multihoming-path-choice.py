# 01-03.multihoming-path-choice — 두 경로 비교 + 역방향 명시
# 본문: "화살표는 광고가 퍼지는 방향이고 패킷은 반대로 흐른다.
#        각 AS 가 자기 번호를 목록 앞에 붙여 넘기므로 AS_PATH 가 자란다."
# 타입 스펙: type-dependency.md 의 두 갈래 경로 + 방향 주의는 focal 로 못 박는다.
#           같은 대역이 두 길로 들어오는 것이 요점이므로 두 경로의 길이 차가 보이게 놓는다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 684
d = D(W, H, "BGP · MULTIHOMING PATH CHOICE",
      "멀티호밍 — 같은 대역이 두 갈래로 광고되어 들어올 때",
      "화살표는 광고가 퍼지는 방향이고 패킷은 반대로 흐른다. 각 AS 가 자기 번호를 목록 앞에 붙여 넘기므로 AS_PATH 가 자란다.",
      lead="같은 대역이 두 길로 들어오고, 우리 ISP 는 표엔 한 줄만 적는다")

BW, BH = 180, 104
US, TOPA, DST = (148, 320), (500, 236), (852, 320)
MID, TOPB = (700, 484), (400, 484)
PICK = (148, 500)

def node(cx, cy, title, sub, tag, c=None, dash=False):
    x, y = cx - BW // 2, cy - BH // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{PAPER2}" '
               f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 20, title, 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(sub, 11, BW - 18, sub), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 628, "같은 대역이 두 길로 들어와도 표에는 한 줄만 남는다")
ddx.focal_tag(d, 500, 152, "화살표는 광고 방향 — 패킷은 반대로 흐른다", 320)

node(*DST,  "목적지 망", "8.8.8.0/24 주인", "AS 500 · 광고 시작", OK)
node(*TOPA, "상위 A", "AS 200 · 앞에 붙임", "AS_PATH 200 500", INFO)
node(*MID,  "중간 사업자", "AS 400 · 앞에 붙임", "AS_PATH 400 500")
node(*TOPB, "상위 B", "AS 300 · 다시 붙임", "AS_PATH 300 400 500")
node(*US,   "우리 ISP", "AS 100 · 둘 다 받는다", "표엔 한 줄만 적는다", INFO)
node(*PICK, "고르는 순서", "1. Local Pref · 정책", "2. AS_PATH 길이", ACC, dash=True)

HB, HH = BW // 2, BH // 2
# 짧은 길 — 두 홉
d.path(f"M {DST[0]-HB-8} {DST[1]-20} L {TOPA[0]+HB+10} {TOPA[1]+24}", INFO, 1.6, m="info")
d.path(f"M {TOPA[0]-HB-8} {TOPA[1]+24} L {US[0]+HB+10} {US[1]-20}", INFO, 1.6, m="info")
d.chip(700, 250, "2 홉", INFO, 12)
# 먼 길 — 세 홉
d.path(f"M {DST[0]-56} {DST[1]+HH+6} L {MID[0]+64} {MID[1]-HH-10}", MUTED, 1.5, m="ar")
d.path(f"M {MID[0]-HB-8} {MID[1]} L {TOPB[0]+HB+10} {TOPB[1]}", MUTED, 1.5, m="ar")
d.path(f"M {TOPB[0]-HB-8} {TOPB[1]} L {US[0]+40} {US[1]+HH+10}", MUTED, 1.5, m="ar")
d.chip(550, 484, "3 홉", MUTED, 12)
d.path(f"M {US[0]} {US[1]+HH+6} L {US[0]} {PICK[1]-HH-10}", ACC, 1.6, m="acc")

d.t(36, 600, "고르는 규칙은 하나이고 표도 하나여서, 어느 쪽으로 배웠든 같은 표에 섞인 뒤 "
             "정책이 같다면 목록이 짧은 쪽이 이긴다", 12, MUTED, KR, "start")
d.legend(644, [("짧은 길", INFO), ("광고 시작", OK), ("고르는 자리", ACC)])
d.save("01-03.multihoming-path-choice.svg")
print("ok multihoming")
