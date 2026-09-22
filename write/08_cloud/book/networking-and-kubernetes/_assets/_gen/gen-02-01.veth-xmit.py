# 02-01.veth-xmit — veth 쌍 사이에서 빠지는 칸
# 본문 요구: "케이블도 qdisc 도 없다 · veth_xmit 가 반대쪽 끝의 RX 경로로 곧장 넘긴다"
# 타입 스펙: type-dp-integration 의 레인 둘 대응 — 위는 비교 기준(물리 NIC 두 장), 아래는 veth.
#           열을 맞춰 두면 아래 레인에서 비는 열이 곧 '없는 것'이다. 빠진 칸을 글로 적지 않고 자리로 보인다.
# 2026-09-21 손으로 쓴 SVG(생성기 없음)를 다시 그렸다. 옛 그림은 아래에 이점/비용 2단 격자를 붙였는데
#            스타일 계약 안티패턴이라 걷어내고, 그 내용은 본문 산문(macvlan·ipvlan 문단)에 맡긴다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 480
d = D(W, H, "veth PAIR · veth_xmit",
      "veth 는 송신을 반대쪽 끝의 수신으로 곧장 넘긴다",
      "위 레인은 비교 기준인 물리 NIC 두 장 사이 경로로 송신 스택, qdisc, NIC 드라이버, 케이블, 받는 NIC 순이다. "
      "아래 레인은 veth 쌍 사이 경로로 Pod 쪽 끝의 송신 스택에서 veth_xmit 를 거쳐 호스트 쪽 끝의 수신 처리로 바로 간다. "
      "qdisc 열과 케이블 자리가 비어 있다.",
      lead="물리 NIC 경로와 열을 맞추면 빈 자리가 qdisc 와 케이블이다")

CX, BW, BH = [152, 384, 616, 848], 176, 72     # stride 232 · 칸 사이 56
TOP_CY, BOT_CY = 172, 332
LX0, LX1 = 40, 960

def ring(cy, label, c):
    y0 = cy - BH // 2 - 24
    d.o.append(f'<rect x="{LX0}" y="{y0}" width="{LX1-LX0}" height="{BH+48}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, LX0, y0, label, 11, c, off=16)

def cell(cx, cy, title, sub, c=None, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = INK
    mono = all(ord(ch) < 128 for ch in title)
    d.t(cx, cy - 4, ddx.fit(title, 13, BW - 16, title), 13, tc, MONO if mono else KR, "middle", 600)
    d.t(cx, cy + 18, ddx.fit(sub, 11, BW - 16, sub), 11, MUTED, KR)

def hop(i, j, cy, label, c, mk):
    a, b = CX[i] + BW // 2, CX[j] - BW // 2
    d.path(f"M {a+6} {cy} L {b-10} {cy}", c, 1.5, m=mk)
    if label:
        mx = (a + b) // 2 if j == i + 1 else CX[i + 1]
        d.t(mx, cy - 10, label, 11, c, KR)

ring(TOP_CY, "물리 NIC 두 장 사이 · 비교 기준", MUTED)
for cx, (t, s) in zip(CX, [("보내는 쪽", "송신 스택"), ("qdisc", "송신 큐"),
                           ("NIC 드라이버", "물리 전송"), ("받는 NIC", "수신 처리")]):
    cell(cx, TOP_CY, t, s)
hop(0, 1, TOP_CY, "", MUTED, "ar")
hop(1, 2, TOP_CY, "", MUTED, "ar")
hop(2, 3, TOP_CY, "케이블", MUTED, "ar")

ring(BOT_CY, "veth 쌍 사이", INFO)
cell(CX[0], BOT_CY, "Pod 쪽 끝", "eth0 · 송신 스택", INFO)
cell(CX[2], BOT_CY, "veth_xmit", "피어 수신으로 넘김", focal=True)
cell(CX[3], BOT_CY, "호스트 쪽 끝", "수신 · backlog", INFO)
hop(0, 2, BOT_CY, "qdisc 없음", INFO, "info")
hop(2, 3, BOT_CY, "곧장", INFO, "info")

d.legend(424, [("물리 NIC 경로 · 비교 기준", MUTED), ("veth 경로", INFO),
               ("반대쪽 수신으로 넘기는 함수", ACC)])
d.save("02-01.veth-xmit.svg")
print("ok 02-01.veth-xmit")
