# 02-01.bridge-fdb — 브리지가 FDB 로 목적지 포트를 고르는 한 번
# 본문 요구: "브리지에 물린 포트에서 본 source MAC 을 FDB 에 배우고, 그 MAC 으로 가는 프레임은 그 포트로만.
#            모르는 MAC 은 모든 포트로 flooding" + "브리지에 물리는 것은 veth 쌍의 한쪽 끝뿐"
# 타입 스펙: type-data-flow — 왼쪽이 Pod 셋, 가운데가 브리지와 그 안의 FDB, 오른쪽이 노드 밖.
#           Pod A → Pod B 한 번을 따라가며 FDB 한 줄에 focal 을 건다.
# 2026-09-21 손으로 쓴 SVG(생성기 없음)를 다시 그렸다. 옛 그림은 대각선 화살표와 문장형 하단 해설을
#            썼다. 브리지 포트를 'port 1' 번호 대신 veth 이름으로 적어 본문의 `bridge fdb show` 출력
#            (MAC · dev <포트 이름>)과 맞췄다. Pod 대역은 netns-isolation 과 같은 10.244.1.0/24 다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 496
d = D(W, H, "LINUX BRIDGE · FDB",
      "브리지는 FDB 에서 목적지 MAC 의 포트를 찾아 그쪽으로만 넘긴다",
      "왼쪽에 Pod 셋과 각 veth 쌍의 호스트 쪽 끝이 있고, 호스트 쪽 끝만 cni0 브리지의 포트로 물린다. "
      "Pod A 가 Pod B 의 MAC 으로 보낸 프레임은 veth-a 로 들어와 FDB 조회로 veth-b 를 찾아 그 포트로만 나간다. "
      "모르는 MAC 은 모든 포트로 flooding 하고, 다른 노드로 가는 패킷은 브리지 주소를 게이트웨이로 삼아 L3 라우팅으로 노드 eth0 에 간다.",
      lead="Pod A → Pod B · 배운 MAC 은 그 포트로만, 모르는 MAC 은 모든 포트로")

ROWS = [168, 264, 360]                        # stride 96
POD_CX, POD_W, BOX_H = 120, 160, 64           # 40~200
PORT_CX, PORT_W = 320, 144                    # 248~392
BR_X, BR_Y, BR_W, BR_H = 440, 120, 280, 272   # 440~720 · 120~392
UP_CX, UP_W = 876, 168                        # 792~960

def box(cx, cy, w, title, sub, c):
    d.box(cx - w // 2, cy - BOX_H // 2, w, BOX_H, PAPER2, c, 1.1, 6)
    mono = all(ord(ch) < 128 for ch in title)
    d.t(cx, cy - 4, ddx.fit(title, 13, w - 16, title), 13, c if c != RULE else INK,
        MONO if mono else KR, "middle", 600)
    smono = all(ord(ch) < 128 or ch == '…' for ch in sub)
    d.t(cx, cy + 16, ddx.fit(sub, 11, w - 16, sub), 11, MUTED, MONO if smono else KR)

PODS = [("Pod A", "aa:…:a5", "veth-a"), ("Pod B", "bb:…:b6", "veth-b"), ("Pod C", "cc:…:c7", "veth-c")]
for cy, (pod, mac, port) in zip(ROWS, PODS):
    box(POD_CX, cy, POD_W, pod, mac, INFO)
    box(PORT_CX, cy, PORT_W, port, "브리지 포트", RULE)

# 브리지와 FDB
d.box(BR_X, BR_Y, BR_W, BR_H, PAPER2, MUTED, 1.1, 8)
BCX = BR_X + BR_W // 2
d.t(BCX, BR_Y + 28, "cni0 브리지", 13, INK, KR, "middle", 600)
d.t(BCX, BR_Y + 48, "struct net_bridge · 10.244.1.1", 11, MUTED, MONO)
d.t(BCX, BR_Y + 80, "FDB · MAC → 포트", 11, SOFT, KR, "middle", 600)
FX, FW, FH = BR_X + 20, BR_W - 40, 32
for i, (mac, port) in enumerate([("aa:…:a5", "veth-a"), ("bb:…:b6", "veth-b"), ("cc:…:c7", "veth-c")]):
    y = BR_Y + 92 + i * 40
    hit = port == "veth-b"
    if hit:
        d.o.append(f'<rect x="{FX}" y="{y}" width="{FW}" height="{FH}" rx="5" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(FX, y, FW, FH, PAPER, RULE, 1.0, 5)
    d.t(BCX, y + 21, f"{mac} → {port}", 12, ACC if hit else INK, MONO)
d.t(BCX, BR_Y + 236, "모르는 MAC · 모든 포트로 flooding", 11, MUTED, KR)

# Pod A → veth-a → 브리지 → veth-b → Pod B
PL, PR = PORT_CX - PORT_W // 2, PORT_CX + PORT_W // 2
d.path(f"M {POD_CX+POD_W//2+6} {ROWS[0]} L {PL-10} {ROWS[0]}", INFO, 1.6, m="info")
d.path(f"M {PR+6} {ROWS[0]} L {BR_X-10} {ROWS[0]}", INFO, 1.6, m="info")
d.path(f"M {BR_X-6} {ROWS[1]} L {PR+10} {ROWS[1]}", INFO, 1.6, m="info")
d.path(f"M {PL-6} {ROWS[1]} L {POD_CX+POD_W//2+10} {ROWS[1]}", INFO, 1.6, m="info")
# 쓰지 않는 Pod C 는 선만 — 배선은 있으나 이번 프레임은 지나지 않는다
d.line(POD_CX + POD_W // 2 + 6, ROWS[2], PL - 6, ROWS[2], RULE, 1.2)
d.line(PR + 6, ROWS[2], BR_X - 6, ROWS[2], RULE, 1.2)

# 다른 노드 행 — 브리지 주소가 게이트웨이, 그다음은 L3
box(UP_CX, ROWS[1], UP_W, "노드 eth0", "다른 노드 행", MUTED)
UY = ROWS[1]
d.path(f"M {BR_X+BR_W+6} {UY} L {UP_CX-UP_W//2-10} {UY}", MUTED, 1.5, m="ar")
d.t((BR_X + BR_W + UP_CX - UP_W // 2) // 2, UY - 10, "L3 라우팅", 11, MUTED, KR)

d.legend(440, [("Pod A → Pod B 경로", INFO), ("FDB 조회가 찾은 포트", ACC), ("다른 노드 행", MUTED)])
d.save("02-01.bridge-fdb.svg")
print("ok 02-01.bridge-fdb")
