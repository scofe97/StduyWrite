# 타입 스펙: type-architecture
# 1절 Launch method 셋의 연결 방향과 java 를 시작하는 쪽 — 방법마다 존 하나, 화살표는 연결을 여는 쪽에서 닫는 쪽으로
"""01-02 Launch method 셋의 연결 방향 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-02.launch-direction.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC,  # noqa: E402
                OK, INFO, KR, MONO)

W = 960
ZH, ZS = 140, 156           # 존 높이, 존 stride (간격 16)
Z0 = 100                    # 첫 존 y
LEG_Y = Z0 + ZS * 2 + ZH + 24
H = LEG_Y + 48              # 범례 아래 여유 포함

d = D(
    W, H,
    "JENKINS · LAUNCH METHOD DIRECTION",
    "Launch method 셋의 연결 방향",
    "inbound 는 Agent 가 Controller 로, SSH 는 Controller 가 Agent 의 sshd 로, 명령 실행은 Controller 위의 명령이 표준 입출력으로 연결을 열고 java 를 시작하는 쪽도 다르다",
    lead="화살표는 연결을 여는 쪽에서 받는 쪽으로 향하고, 초록 칩은 java 를 시작하는 쪽에 붙습니다",
)


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
    lw = sum(12 * (1.0 if "가" <= c <= "힣" else 0.62) for c in label) + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw:.0f}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 20, y + 17, label, 12, SOFT, KR, "start", 600)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO


def node_box(x, y, w, h, title, sub, stroke=RULE):
    d.box(x, y, w, h, PAPER2, stroke, 1.0, 6)
    d.t(x + w / 2, y + 26, title, 14, INK, fam(title), "middle", 600)
    d.t(x + w / 2, y + 48, sub, 13, MUTED, fam(sub), "middle")


def java_tag(cx, y):
    d.chip(cx, y, "java 를 시작하는 쪽", OK, 13)


LX, LW = 48, 216            # Controller 박스
RX, RW = 696, 216           # Agent 박스
BH = 64
MID0, MID1 = LX + LW, RX    # 화살표 구간
MIDX = (MID0 + MID1) // 2

bands = [
    ("inbound · JNLPLauncher", "연결을 받는 쪽", "연결을 여는 쪽", "L", ACC,
     "TCP 포트", "WebSocket 이면 HTTP(S)", "R"),
    ("SSH · SSHLauncher", "연결을 여는 쪽", "sshd 가 받는 쪽", "R", INFO,
     "SSH", "Agent 의 sshd 로", "L"),
    ("명령 실행 · CommandLauncher", "명령을 실행하는 쪽", "표준 입출력으로 이어지는 쪽", "R", INFO,
     "표준 입출력", "Controller 위 명령의 stdin · stdout", "L"),
]

for i, (zlabel, ctitle, atitle, direction, col, above, below, tag) in enumerate(bands):
    zy = Z0 + i * ZS
    zone(24, zy, W - 48, ZH, zlabel)
    by = zy + 28
    node_box(LX, by, LW, BH, "Controller", ctitle, INFO if direction == "R" else ACC)
    node_box(RX, by, RW, BH, "Agent 기계", atitle, INFO if direction == "R" else ACC)
    ay = by + 32
    mk = "acc" if col == ACC else "info"
    if direction == "R":
        d.arrow([(MID0, ay), (MID1, ay)], col, mk, 1.6)
    else:
        d.arrow([(MID1, ay), (MID0, ay)], col, mk, 1.6)
    d.t(MIDX, ay - 12, above, 13, col, fam(above), "middle", 600)
    d.t(MIDX, ay + 26, below, 13, MUTED, fam(below), "middle")
    # java 를 시작하는 쪽 칩: inbound 는 Agent 쪽, SSH·명령은 Controller 쪽
    chip_cx = (RX + RW // 2) if tag == "R" else (LX + LW // 2)
    java_tag(chip_cx, by + BH + 24)

d.legend(LEG_Y, [
    ("Agent 가 여는 연결", ACC),
    ("Controller 가 여는 연결", INFO),
    ("java 를 시작하는 쪽", OK),
])

out_path = pathlib.Path(__file__).resolve().parent.parent / "01-02.launch-direction.svg"
d.save(str(out_path))
print("saved", out_path)
