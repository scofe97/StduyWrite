# 타입 스펙: type-sequence — 참여자 레인 + 시간축. 시간은 위에서 아래로 흐른다.
#   축약: 가로축이 참여자 배열인 동시에 *공간*이라, 신호 전파를 레인을 가로지르는 사선으로 그린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3.2 Figure 6.12 · Figure 6.13 —
#   선형 브로드캐스트 버스 위의 네 노드 A·B·C·D, t0 에 B 가 전송 시작, t1 에 D 가 유휴로 판단
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 940, 552
d = D(W, H, "SECTION 6.3.2 · WHY CARRIER SENSING STILL COLLIDES",
      "듣고 보냈는데도 부딪히는 이유",
      "전파에 시간이 걸리기 때문이다. B 가 이미 보내고 있어도 그 비트가 아직 D 에 닿지 않았으면 D 는 채널을 유휴로 듣는다.",
      "가로는 버스 위의 위치, 세로는 시간입니다")

PX, PW = 24, 560
NODES = [("A", 88), ("B", 216), ("C", 344), ("D", 472)]
TOP, BOT = 152, 400
SLOPE = 0.25               # 시간 = 거리 x 0.25 — 신호가 한 칸(128px)을 32px 시간에 지납니다

d.t(PX + PW / 2, 112, "공간 — 선형 브로드캐스트 버스", 11, SOFT, KR)
for name, x in NODES:
    d.box(x - 26, 122, 52, 24, PAPER2, RULE, 0.9)
    d.t(x, 139, name, 12, INK, MONO, "middle", 600)
    d.line(x, TOP, x, BOT, RULE, 0.9, "3 6")
d.t(PX, BOT + 22, "시간은 아래로 흐릅니다", 10, SOFT, KR, "start")

LEFT, RIGHT = 56, 552
T0, T1 = 176, 228


def wavefront(x0, y0, color):
    """한 노드에서 양쪽으로 퍼지는 신호의 앞머리."""
    d.line(x0, y0, LEFT, y0 + (x0 - LEFT) * SLOPE, color, 1.6)
    d.line(x0, y0, RIGHT, y0 + (RIGHT - x0) * SLOPE, color, 1.6)


wavefront(216, T0, INFO)
wavefront(472, T1, OK)

d.chip(216, T0 - 16, "t0 · B 가 유휴를 듣고 보냅니다", INFO, 10)
d.chip(472, T1 - 16, "t1 · D 도 유휴로 듣습니다", OK, 10)

# B 의 신호가 D 에 닿는 시각 · D 의 신호가 B 에 닿는 시각
BD_Y = T0 + (472 - 216) * SLOPE
DB_Y = T1 + (472 - 216) * SLOPE
d.tone(472 - 8, BD_Y - 8, 16, 16, BAD, 3, "44", 1.4)
d.t(472 - 16, BD_Y + 4, "D 가 충돌을 압니다", 11, BAD, KR, "end", 600)
d.tone(216 - 8, DB_Y - 8, 16, 16, BAD, 3, "44", 1.4)
d.t(216 + 16, DB_Y + 4, "B 가 충돌을 압니다", 11, BAD, KR, "start", 600)

d.tone(PX + 8, 340, 544, 48, ACC, 6, "14", 1.4)
d.t(PX + 20, 360, "t1 에 D 가 유휴로 들은 것은 착각이 아닙니다. B 의 비트가", 11, ACC, KR, "start", 600)
d.t(PX + 20, 378, "그때까지 D 에 도착하지 않았습니다.", 11, ACC, KR, "start", 600)

AX, AW = 624, 292
d.box(AX, 116, AW, 148, PAPER2, RULE, 1.0)
d.t(AX + 16, 140, "충돌 감지를 더하면", 11, INK, KR, "start", 600)
d.line(AX + 16, 150, AX + AW - 16, 150, RULE, 0.8)
for i, s in enumerate([
    "보내는 동안에도 채널을 계속 듣습니다",
    "남의 신호 에너지를 감지하면 중단합니다",
    "망가진 프레임을 끝까지 보내지 않습니다",
    "무작위 시간을 기다린 뒤 다시 시도합니다",
]):
    d.t(AX + 16, 174 + i * 22, "·  " + s, 11, MUTED, KR, "start")

d.box(AX, 280, AW, 148, PAPER2, RULE, 1.0)
d.t(AX + 16, 304, "이진 지수 백오프", 11, INK, KR, "start", 600)
d.line(AX + 16, 314, AX + AW - 16, 314, RULE, 0.8)
for i, (a, b) in enumerate([("1 회 충돌 뒤", "K in {0,1}"),
                            ("2 회 충돌 뒤", "K in {0..3}"),
                            ("3 회 충돌 뒤", "K in {0..7}"),
                            ("10 회 이상", "K in {0..1023}")]):
    d.t(AX + 16, 338 + i * 22, a, 11, MUTED, KR, "start")
    d.t(AX + AW - 16, 338 + i * 22, b, 11, INK, MONO, "end", 600)

d.line(24, 452, W - 48, 452, RULE, 0.8)
d.t(24, 474, "전파 지연이 길수록 이미 시작된 전송을 못 듣는 노드가 늘어납니다. 그래서 효율이 전파 지연과 전송 시간의 비로 정해집니다.",
     11, MUTED, KR, "start")
d.t(24, 492, "효율 = 1 / (1 + 5 · d_prop / d_trans) — 전파 지연이 0 에 가까워지면 효율이 1 에 가까워집니다.",
     11, MUTED, MONO, "start")

d.legend(510, [("B 의 신호", INFO), ("D 의 신호", OK), ("겹치는 자리", BAD), ("이 도식의 요점", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.csma-spacetime.svg"
d.save(out)
print("→", out)
