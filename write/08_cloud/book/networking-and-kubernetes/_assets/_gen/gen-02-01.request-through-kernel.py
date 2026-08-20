# 02-01.request-through-kernel — 가로 체인 + 커널 경계 (경계를 두 번 넘는다)
# 본문: "점선 안이 커널 공간. 왼쪽 두 칸은 그 밖(하드웨어와 유저 공간)이고,
#        패킷은 경계를 두 번 넘는다."
# 타입 스펙: type-process.md 의 단계 열 + type-nested.md 의 경계 링.
#           링을 가운데 다섯 칸에만 씌워 '두 번 넘는다'가 자리로 드러나게 한다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 560
d = D(W, H, "ONE REQUEST · THROUGH THE KERNEL",
      "요청 하나가 커널을 관통하는 순서 — 네 절이 실제로 이어지는 자리",
      "점선 안이 커널 공간. 양 끝 두 칸은 그 밖(하드웨어와 유저 공간)이고, 패킷은 경계를 두 번 넘는다.",
      lead="양 끝 두 칸은 커널 밖 · 패킷은 경계를 두 번 넘는다")

BW, BH, GAP = 124, 104, 16
CX = [18 + BW // 2 + i * (BW + GAP) for i in range(7)]           # 80 220 360 500 640 780 920
CY = 300
RING = (CX[1] - BW // 2 - 24, 216, (CX[5] + BW // 2 + 24) - (CX[1] - BW // 2 - 24), 172)

NODES = [("NIC 도착", "8080 행 SYN", "하드웨어", INFO),
         ("PRE_ROUTING", "Raw·Mangle·NAT", "§4 훅", None),
         ("Conntrack", "5-tuple 조회", "§5 없으면 NEW", None),
         ("라우팅 판단", "목적지가 내 IP", "§6 구체성 우선", None),
         ("LOCAL_IN", "Mangle·NAT·Filter", "§4 INPUT", None),
         ("소켓 큐", "포트로 소켓 선택", "§1 fd 로 전달", None),
         ("Go 서버", "epoll 이 깨어남", "유저 공간", OK)]
EDGE = ["진입", "조회", "질의", "", "통과", "알림"]

ddx.band(d, 104, 512, "네 절이 실제로 이어지는 자리 — 훅·연결 추적·라우팅·소켓이 한 줄에 선다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "커널 공간", 11, ACC, off=20)

for cx, (l, s, t, c) in zip(CX, NODES):
    x, y = cx - BW // 2, CY - BH // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, CY - 24, ddx.fit(l, 12, BW - 14, l), 12, c or INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, CY - 2, ddx.fit(s, 10, BW - 12, s), 10, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, CY + 26, ddx.fit(t, 10, BW - 10, t), 10, SOFT, KR)

for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    c = ACC if i in (0, 5) else MUTED                            # 경계를 넘는 두 걸음
    d.path(f"M {a+5} {CY} L {b-7} {CY}", c, 1.5, m="acc" if c is ACC else "ar")
    if lab: d.t((a + b) // 2, CY - BH // 2 - 12, ddx.fit(lab, 10, GAP + 22, lab), 10, c, KR)

d.t(rx + 8, CY + BH // 2 + 30, "경계 진입", 10, ACC, KR, "start")
d.t(rx + rw - 8, CY + BH // 2 + 30, "경계 이탈", 10, ACC, KR, "end")
d.t(36, 476, "하드웨어에서 들어와 커널을 지나 유저 공간으로 나간다 — 그 사이가 이 편의 §4·§5·§6·§1 이다",
     12, MUTED, KR, "start")
d.legend(528, [("커널 밖", INFO), ("도착", OK), ("경계를 넘는 걸음", ACC)])
d.save("02-01.request-through-kernel.svg")
print("ok request-through-kernel")
