# 02-01.request-through-kernel — 가로 체인 + 커널 경계 (경계를 두 번 넘는다)
# 본문: "점선 안이 커널 공간. 왼쪽 두 칸은 그 밖(하드웨어와 유저 공간)이고,
#        패킷은 경계를 두 번 넘는다."
# 타입 스펙: type-process.md 의 단계 열 + type-nested.md 의 경계 링.
#           링을 가운데 다섯 칸에만 씌워 '두 번 넘는다'가 자리로 드러나게 한다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 496
d = D(W, H, "ONE REQUEST · THROUGH THE KERNEL",
      "요청 하나가 커널을 관통하는 순서 — 네 절이 실제로 이어지는 자리",
      "점선 안이 커널 공간. 양 끝 두 칸은 그 밖(하드웨어와 유저 공간)이고, 패킷은 경계를 두 번 넘는다.",
      lead="양 끝 두 칸은 커널 밖 · 패킷은 경계를 두 번 넘는다")

# 링 세로 테두리는 커널 밖 카드와 안쪽 카드 사이 통로(28px)의 한가운데를 지난다.
# 2026-09-15 이전에는 통로가 12px 이라 링이 양 끝 카드를 12px 씩 잘랐다.
OW, BW, BH, GAP, EDGE_GAP = 104, 128, 104, 12, 28                 # 커널 밖 카드는 좁게
X0 = (1000 - (2 * OW + 5 * BW + 4 * GAP + 2 * EDGE_GAP)) // 2    # 24
WS = [OW] + [BW] * 5 + [OW]
GS = [EDGE_GAP] + [GAP] * 4 + [EDGE_GAP]
CX, x = [], X0
for i, w in enumerate(WS):
    CX.append(x + w // 2); x += w + (GS[i] if i < 6 else 0)
CY = 300
RL = CX[1] - BW // 2 - EDGE_GAP // 2
RR = CX[5] + BW // 2 + EDGE_GAP // 2
RING = (RL, 216, RR - RL, 176)

NODES = [("NIC 도착", "8080 행 SYN", "하드웨어", INFO),
         ("PRE_ROUTING", "Raw·Mangle·NAT", "§4 훅", None),
         ("Conntrack", "5-tuple 조회", "§5 없으면 NEW", None),
         ("라우팅 판단", "목적지가 내 IP", "§6 구체성 우선", None),
         ("LOCAL_IN", "Mangle·NAT·Filter", "§4 INPUT", None),
         ("소켓 큐", "포트로 소켓 선택", "§1 fd 로 전달", None),
         ("Go 서버", "epoll 이 깨어남", "유저 공간", OK)]
# 경계를 넘는 두 통로는 링 테두리가 지나므로 라벨을 비운다 — 링 안쪽 아래 '경계 진입·이탈'이 대신한다
EDGE = ["", "조회", "질의", "", "통과", ""]

ddx.band(d, 104, 424, "네 절이 이어지는 자리 · 훅 · 연결 추적 · 라우팅 · 소켓")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "커널 공간", 11, ACC, off=20)

for cx, w, (l, s, t, c) in zip(CX, WS, NODES):
    x, y = cx - w // 2, CY - BH // 2
    d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, CY - 24, ddx.fit(l, 12, w - 14, l), 12, c or INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, CY - 2, ddx.fit(s, 11, w - 12, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, CY + 26, ddx.fit(t, 11, w - 10, t), 11, SOFT, KR)

for i, lab in enumerate(EDGE):
    a, b = CX[i] + WS[i] // 2, CX[i + 1] - WS[i + 1] // 2
    c = ACC if i in (0, 5) else MUTED                            # 경계를 넘는 두 걸음
    d.path(f"M {a+5} {CY} L {b-7} {CY}", c, 1.5, m="acc" if c is ACC else "ar")
    if lab: d.t((a + b) // 2, CY - BH // 2 - 12, ddx.fit(lab, 11, GAP + 22, lab), 11, c, KR)

d.t(rx + 12, CY + BH // 2 + 28, "경계 진입", 12, ACC, KR, "start")
d.t(rx + rw - 12, CY + BH // 2 + 28, "경계 이탈", 12, ACC, KR, "end")
d.legend(440, [("커널 밖", INFO), ("도착", OK), ("경계를 넘는 걸음", ACC)])
d.save("02-01.request-through-kernel.svg")
print("ok request-through-kernel")
