# 01-03.same-subnet-or-not — 2행 대조
# 본문: "윗줄은 스위치만, 아랫줄은 라우터가 선다"
#        아래로 뻗은 상자가 그 장비가 실제로 읽는 부분이다
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 구조를 두 행으로 축약 +
#           type-nested.md 의 경계 링(같은 서브넷 = 한 L2 세그먼트)
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 660
d = D(W, H, "SAME SUBNET OR NOT",
      "같은 서브넷이냐 아니냐가 Pod 대역의 운명을 가른다",
      "아래로 뻗은 상자가 그 장비가 실제로 읽는 부분이다 — 스위치는 겉봉에서 멈추고 라우터는 속의 IP 까지 열어 표를 뒤진다",
      lead="스위치는 겉봉에서 멈추고, 라우터는 속의 IP 까지 열어 표를 뒤진다")

BW, BH, GAP = 168, 88, 52
CX = [86 + BW // 2 + i * (BW + GAP) for i in range(4)]        # 170 390 610 830
ROW_A, ROW_B = 252, 452
RING = (64, 184, 652, 136)

def cell(cx, cy, title, sub, tag, c=None, focal=False, dash=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{PAPER2}" '
                   f'stroke="{c or RULE}" stroke-width="1.1"'
                   f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>'); tc = c or INK
    d.t(cx, cy - 14, ddx.fit(title, 13, BW - 20, title), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 6,  ddx.fit(sub, 11, BW - 20, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 for ch in sub) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 16, tag), 10, SOFT, KR)

ddx.band(d, 104, 572, "같은 줄에 있으면 겉봉만으로 끝나고, 줄이 갈리면 표를 뒤져야 한다")

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "같은 서브넷 192.168.0.0/24 — 한 L2 세그먼트", 11, INFO)

cell(CX[0], ROW_A, "노드 1", "192.168.0.10", "Pod 10.244.1.0/24")
cell(CX[1], ROW_A, "스위치", "L2 장비", "MAC 표로 전달", INFO)
cell(CX[2], ROW_A, "노드 2", "192.168.0.11", "Pod 10.244.2.0/24")
cell(CX[3], ROW_A, "겉봉에서 멈춘다", "MAC = 노드 2 의 NIC", "속은 열지 않는다", INFO, dash=True)

d.t(64, 372, "다른 서브넷 — 라우터가 선다", 11, SOFT, KR, "start", 600)
cell(CX[0], ROW_B, "노드 1", "192.168.0.10", "다른 서브넷")
cell(CX[1], ROW_B, "라우터", "L3 장비", "라우팅 표로 전달", WARN)
cell(CX[2], ROW_B, "폐기", "노드 2 는 못 받는다", "ICMP 로 알린다", BAD)
cell(CX[3], ROW_B, "속까지 연다", "IP = 10.244.2.7", "표에 그 줄이 없다", focal=True)

HB = BW // 2
for cy, c, mk, labs in [(ROW_A, MUTED, "ar", ["프레임", "통과"]),
                        (ROW_B, MUTED, "ar", ["패킷", "버린다"])]:
    for i, lab in enumerate(labs):
        a, b = CX[i], CX[i + 1]
        cc = BAD if (cy == ROW_B and i == 1) else c
        d.path(f"M {a+HB+6} {cy} L {b-HB-10} {cy}", cc, 1.5, m="bad" if cc is BAD else mk)
        d.t((a + b) // 2, cy - 14, ddx.fit(lab, 11, GAP - 4, f"corridor {lab}"), 11, cc, KR)
    d.line(CX[2] + HB + 6, cy, CX[3] - HB - 6, cy, RULE, 1.0, "4 5")

d.t(36, 544, "노드 대역이 같은 L2 안에 있으면 스위치가 겉봉만 보고 넘기지만, 대역이 갈리면 "
             "라우터가 속을 열어 표를 뒤지고 그 줄이 없으면 버린다", 12, MUTED, KR, "start")
d.legend(592, [("겉봉 · L2", INFO), ("속 · L3", WARN), ("폐기", BAD), ("표에 줄이 없다", ACC)])
d.save("01-03.same-subnet-or-not.svg")
print("ok same-subnet")
