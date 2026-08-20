# 01-03.calico-node-detail — 노드 내부 구조
# 본문: "Pod 는 라우터가 아니라 끝점입니다. 라우팅을 하는 것은 노드의 커널이고,
#        Pod 와 커널은 veth 쌍이라는 가상 인터페이스 한 켤레로 이어집니다."
#        "Pod = 호스트, 노드 = 라우터, 클러스터 = AS 하나"
# 타입 스펙: type-nested.md 의 경계 링(커널 안) + type-flowchart.md 의 직교 라우팅
#   나가는 길과 들어오는 길을 두 줄로 접어 같은 부품이 마주 보게 둔다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 644
d = D(W, H, "CALICO · INSIDE THE NODE",
      "노드 안을 열어 보면 — Pod 에서 나가 Pod 로 들어가기까지",
      "Pod 는 끝점이고 라우팅을 하는 것은 노드의 커널이다. 광고로 표에 줄이 생겼으므로 가운데를 지나는 동안 겉은 한 겹뿐이다.",
      lead="Pod 는 끝점이고 라우팅을 하는 것은 노드의 커널이다")

BW, BH = 136, 76
CX  = [128, 288, 448, 608]
OUT, IN = 244, 452                                  # 나가는 줄 / 들어오는 줄
NET = (856, 348, 172, 96)                           # 회사 네트워크
RING1 = (40, 176, 700, 136)
RING2 = (40, 384, 700, 136)

def cell(cx, cy, title, sub, tag, c=None, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 12, ddx.fit(title, 12, BW - 16, title), 12, tc, KR, "middle", 600)
    d.t(cx, cy + 6,  ddx.fit(sub, 11, BW - 16, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in "→" for ch in sub) else KR)
    d.t(cx, cy + 25, ddx.fit(tag, 10, BW - 12, tag), 10, SOFT, KR)

ddx.band(d, 104, 588, "Pod = 호스트 · 노드 = 라우터 · 클러스터 = AS 하나")

for (rx, ry, rw, rh), lab in [(RING1, "노드 1 의 커널 안"), (RING2, "노드 2 의 커널 안")]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, lab, 11, INFO)

cell(CX[0], OUT, "Pod A", "10.244.1.5", "끝점 · 라우팅 안 함", OK)
cell(CX[1], OUT, "veth 쌍", "cali 인터페이스", "Pod 와 커널 사이")
cell(CX[2], OUT, "라우팅 표", "-> 192.168.0.11", "BGP 로 배운 줄", focal=True)
cell(CX[3], OUT, "물리 NIC", "192.168.0.10", "여기로 나간다")

cell(CX[3], IN, "물리 NIC", "192.168.0.11", "여기로 들어온다")
cell(CX[2], IN, "라우팅 표", "-> cali 인터페이스", "직접 연결")
cell(CX[1], IN, "veth 쌍", "cali 인터페이스", "커널과 Pod 사이")
cell(CX[0], IN, "Pod B", "10.244.2.7", "끝점 · 라우팅 안 함", OK)

HB = BW // 2
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+HB+6} {OUT} L {b-HB-10} {OUT}", MUTED, 1.4, m="ar")
for a, b in zip(CX[::-1], CX[::-1][1:]):
    d.path(f"M {a-HB-6} {IN} L {b+HB+10} {IN}", MUTED, 1.4, m="ar")

nx, ny, nw, nh = NET
d.box(nx - nw // 2, ny - nh // 2, nw, nh, PAPER2, INFO, 1.1, 6)
d.t(nx, ny - 12, "회사 네트워크", 13, INFO, KR, "middle", 600)
d.t(nx, ny + 8, "라우터 · 스위치", 11, MUTED, KR)
d.t(nx, ny + 28, "겉이 한 겹뿐", 10, SOFT, KR)
d.path(f"M {CX[3]+HB+6} {OUT} L {nx} {OUT} L {nx} {ny-nh//2-10}", MUTED, 1.5, m="ar")
d.path(f"M {nx} {ny+nh//2+6} L {nx} {IN} L {CX[3]+HB+10} {IN}", MUTED, 1.5, m="ar")

d.t(36, 556, "Pod 와 커널은 veth 쌍 한 켤레로 이어지고, 한쪽 끝이 Pod 안의 eth0, "
             "다른 쪽 끝이 노드 쪽 cali 인터페이스다", 12, MUTED, KR, "start")
d.legend(604, [("커널 경계", INFO), ("끝점", OK), ("라우팅하는 자리", ACC)])
d.save("01-03.calico-node-detail.svg")
print("ok calico")
