# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가를 격자로. 여기서는 "누가 누구를 듣는가".
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.1 Figure 7.6(a)(b) —
#   A·B·C 세 노드와 청취 관계는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 536
d = D(W, H, "SECTION 7.2.1 · HIDDEN TERMINALS",
      "둘 다 조용하다고 판단하고 동시에 말합니다",
      "경로 손실 때문에 A 와 C 는 서로를 못 듣는다. 그런데 둘의 신호는 B 에서 겹친다.",
      "노드 배치와 청취 관계는 원문 Figure 7.6 의 것입니다")

NODES = ["A", "B", "C"]
CW, CH, X0, Y0, STRIDE = 112, 52, 160, 168, 56
d.t(24, 148, "가로 = 듣는 쪽 · 세로 = 말하는 쪽", 11, SOFT, KR, "start")
for j, n in enumerate(NODES):
    d.t(X0 + j * CW + CW / 2, 160, n, 12, SOFT, MONO, "middle", 600)
HEARS = {("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")}
for i, a in enumerate(NODES):
    y = Y0 + i * STRIDE
    d.t(148, y + CH / 2 + 4, a, 12, SOFT, MONO, "end", 600)
    for j, b in enumerate(NODES):
        x = X0 + j * CW
        if a == b:
            d.box(x, y, CW, CH, PAPER2, RULE, 0.9)
            d.t(x + CW / 2, y + CH / 2 + 4, "—", 12, SOFT, MONO)
        elif (a, b) in HEARS:
            d.tone(x, y, CW, CH, OK, 6, "18", 1.2)
            d.t(x + CW / 2, y + CH / 2 + 4, "들립니다", 11, OK, KR)
        else:
            d.tone(x, y, CW, CH, BAD, 6, "18", 1.3)
            d.t(x + CW / 2, y + CH / 2 + 4, "안 들립니다", 11, BAD, KR)

PX, PW = 536, 368
d.box(PX, 152, PW, 176, PAPER2, RULE, 1.0)
d.t(PX + 20, 178, "그래서 벌어지는 일", 12, INK, KR, "start", 600)
d.line(PX + 20, 190, PX + PW - 20, 190, RULE, 0.8)
STEPS = [
    ("1", "A 와 C 가 각각 B 에게 보내려 합니다."),
    ("2", "둘 다 채널을 들어 보고 비었다고 판단합니다."),
    ("3", "서로의 송신이 검출 문턱 아래라 안 들립니다."),
    ("4", "두 신호가 B 에서 겹쳐 둘 다 못 받습니다."),
]
for i, (no, txt) in enumerate(STEPS):
    y = 214 + i * 26
    d.t(PX + 24, y, no, 11, ACC if no == "4" else SOFT, MONO, "start", 600)
    d.t(PX + 44, y, txt, 11, ACC if no == "4" else MUTED, KR, "start")

FY = 358
d.tone(24, FY, 880, 62, ACC, 8, "12", 1.3)
d.t(44, FY + 26, "충돌은 보내는 쪽이 아니라 받는 쪽에서 일어납니다", 12, ACC, KR, "start", 600)
d.t(44, FY + 48,
    "그래서 유선의 CSMA/CD 처럼 \"들어 보고 비었으면 보낸다\"만으로는 무선에서 충돌을 못 막습니다.",
    11, MUTED, KR, "start")

BY = 434
d.t(24, BY, "원문은 같은 결과를 낳는 두 번째 배치도 듭니다 — A 와 C 사이가 건물 같은 장애물로 물리적으로 막힌 경우입니다.",
    11, INFO, KR, "start")

d.legend(462, [("서로 들리는 쌍", OK), ("숨은 쌍", BAD), ("이 도식의 논점", ACC), ("두 번째 배치", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.hidden-terminal.svg"
d.save(out)
print("→", out)
