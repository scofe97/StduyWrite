# 타입 스펙: type-swimlane — IPv6 세상과 IPv4 터널이라는 두 레인을 오가는 하나의 흐름.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.4 Figure 4.27 (터널링)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 960, 640
d = D(W, H, "IPV4-TO-IPV6 TRANSITION · TUNNELING",
      "IPv6 를 IPv4 안에 넣어 건너보냅니다",
      "IPv6 노드 둘 사이에 IPv4 라우터가 끼어 있을 때 IPv6 데이터그램을 IPv4 데이터그램의 적재량 자리에 넣어 나르는 터널링. 아래 세 줄은 같은 데이터가 구간마다 어떤 모습인지 보여준다.",
      "터널 안 라우터는 자기가 IPv4 데이터그램 하나를 나른다고만 압니다")

NH = 54
TOP = 116
MID = 228

d.t(30, 100, "IPv6 를 아는 세상", 11, SOFT, KR, "start", 600)


def node(x, y, w, name, sub, hot=False):
    c = ACC if hot else RULE
    d.box(x, y, w, NH, PAPER2, c, 1.4 if hot else 1.0, 7)
    d.t(x + w / 2, y + 24, name, 13, ACC if hot else INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 42, sub, 11, MUTED, KR)


# 터널 컨테이너 먼저 (노드가 그 위에 그려지도록)
d.o.append(f'<rect x="336" y="94" width="278" height="206" rx="10" '
           f'fill="{INK}05" stroke="{MUTED}" stroke-width="1.1" stroke-dasharray="5 5"/>')
d.t(475, 116, "터널 — 이 안은 IPv4 만 압니다", 11, MUTED, KR)

node(30, TOP, 130, "A", "IPv6 호스트")
node(190, TOP, 130, "B", "터널 입구", hot=True)
node(348, MID, 120, "C", "IPv4 라우터")
node(486, MID, 120, "D", "IPv4 라우터")
node(640, TOP, 130, "E", "터널 출구", hot=True)
node(800, TOP, 130, "F", "IPv6 호스트")

d.arrow([(160, TOP + 27), (186, TOP + 27)], MUTED, "ar", 1.5)
d.arrow([(320, TOP + 27), (334, TOP + 27), (334, MID + 27), (344, MID + 27)], ACC, "acc", 1.5)
d.arrow([(468, MID + 27), (482, MID + 27)], MUTED, "ar", 1.5)
d.arrow([(606, MID + 27), (620, MID + 27), (620, TOP + 27), (636, TOP + 27)], ACC, "acc", 1.5)
d.arrow([(770, TOP + 27), (796, TOP + 27)], MUTED, "ar", 1.5)

# 구간마다 데이터그램의 모습
SY, SH = 344, 44
LBL_X, S0, S1 = 30, 200, 930


def strip(y, label, parts):
    d.t(LBL_X, y + 27, label, 11, MUTED, KR, "start")
    x = S0
    for name, w, hot in parts:
        c = ACC if hot else MUTED
        d.box(x, y, w, SH, PAPER2, f"{c}66", 1.4 if hot else 0.9, 5)
        d.t(x + w / 2, y + 27, name, 11, ACC if hot else INK, KR)
        x += w


strip(SY, "B 가 만든 것", [("IPv6 헤더 40B", 240, False), ("데이터", 490, False)])
strip(SY + 68, "터널 안에서", [("IPv4 헤더 20B", 120, True), ("IPv6 헤더 40B", 240, False),
                            ("데이터", 370, False)])
strip(SY + 136, "E 가 꺼낸 것", [("IPv6 헤더 40B", 240, False), ("데이터", 490, False)])

d.t(260, SY + 62, "protocol = 41", 11, ACC, MONO)

d.t(30, 552, "IPv4 헤더의 프로토콜 번호 41 이 \"적재량은 IPv6 데이터그램\"이라는 표시입니다. "
              "바꿔야 하는 장비는 터널 양 끝 둘뿐입니다.", 11, MUTED, KR, "start")

d.legend(576, [("터널 양 끝이 감싸고 벗깁니다", ACC), ("그대로 지나는 구간", MUTED)])
d.t(920, 598, "KUROSE-ROSS 9E FIG 4.27 · IANA PROTO 41", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.tunneling.svg"
d.save(out)
print("→", out)
