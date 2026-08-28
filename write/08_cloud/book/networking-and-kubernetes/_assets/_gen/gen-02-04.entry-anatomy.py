# 02-04.entry-anatomy — conntrack 엔트리 한 줄의 분해
# 본문 요구: §5 "한 줄에 src= 가 두 번 나옵니다. 앞이 원본 방향이고 뒤가 응답 방향입니다."
#           그 한 줄이 어떤 부분들로 이루어지는지가 안 보여 읽는 법을 따로 설명해야 했다.
# 타입 스펙: type-tree.md — 루트를 위에, 자식을 아래로. 연결선은 직각(수직 → 가로 버스 → 수직).
#           깊이 3(최대 4), 부모당 너비 2~3(최대 5). coral 은 한 노드 — NAT 를 걸면 바뀌는 쪽.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 568
d = D(W, H, "CONNTRACK ENTRY · ANATOMY",
      "한 줄에 튜플이 둘 — 어디까지가 원본이고 어디부터가 응답인가",
      "conntrack -L 의 한 줄은 프로토콜과 수명, 원본 방향 튜플, 응답 방향 튜플로 나뉩니다. "
      "src= 가 두 번 나오는 것이 그 경계이며, NAT 를 걸면 두 번째 튜플만 달라집니다.",
      lead="src= 가 두 번 나오는 자리가 두 튜플의 경계다")

ROOT_CY, L2_CY, L3_CY = 168, 280, 412
RW, RH = 260, 48
L2W, L2H = 236, 72
L3W, L3H = 150, 56
ROOT = 500
L2 = [(160, "icmp 1 29", "프로토콜 · 남은 수명", RULE),
      (460, "원본 방향", "type=8 · id=5321", INFO),
      (800, "응답 방향", "type=0 · id=5321", ACC)]
L3 = [(380, "src=10.10.1.11", INFO), (540, "dst=192.168.139.238", INFO),
      (720, "src=192.168.139.238", ACC), (880, "dst=10.10.1.11", ACC)]

# 연결선 먼저(z-order)
BUS1, BUS2 = 228, 356
d.line(ROOT, ROOT_CY + RH // 2, ROOT, BUS1, MUTED, 1.2)
d.line(L2[0][0], BUS1, L2[2][0], BUS1, MUTED, 1.2)
for cx, *_ in L2:
    d.line(cx, BUS1, cx, L2_CY - L2H // 2, MUTED, 1.2)
for parent, kids in ((460, (380, 540)), (800, (720, 880))):
    d.line(parent, L2_CY + L2H // 2, parent, BUS2, MUTED, 1.2)
    d.line(kids[0], BUS2, kids[1], BUS2, MUTED, 1.2)
    for k in kids:
        d.line(k, BUS2, k, L3_CY - L3H // 2, MUTED, 1.2)

d.box(ROOT - RW // 2, ROOT_CY - RH // 2, RW, RH, PAPER2, RULE, 1.1, 6)
d.t(ROOT, ROOT_CY + 5, "conntrack 엔트리 한 줄", 13, INK, KR, "middle", 600)

for cx, name, sub, c in L2:
    focal = c is ACC
    x, y = cx - L2W // 2, L2_CY - L2H // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{L2W}" height="{L2H}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, L2W, L2H, PAPER2, c, 1.1, 6)
    d.t(cx, L2_CY - 8, ddx.fit(name, 13, L2W - 20, name), 13,
        c if c is not RULE else INK, MONO if name[0].islower() else KR, "middle", 600)
    d.t(cx, L2_CY + 16, ddx.fit(sub, 11, L2W - 16, sub), 11, MUTED, MONO)

for cx, txt, c in L3:
    d.box(cx - L3W // 2, L3_CY - L3H // 2, L3W, L3H, PAPER, c, 0.8, 6)
    d.t(cx, L3_CY + 5, ddx.fit(txt, 11, L3W - 12, txt), 11, MUTED, MONO)

d.t(36, 482, "NAT 를 걸면 오른쪽 가지만 달라집니다. 왼쪽 원본 방향은 패킷이 도착했을 때의 값 그대로 "
             "남아, 응답을 되돌릴 때 복원표로 쓰입니다.", 12, MUTED, KR, "start")
d.legend(500, [("원본 방향 — 변하지 않는다", INFO), ("응답 방향 — NAT 가 여기를 바꾼다", ACC)])
d.save("02-04.entry-anatomy.svg")
print("ok entry-anatomy")
