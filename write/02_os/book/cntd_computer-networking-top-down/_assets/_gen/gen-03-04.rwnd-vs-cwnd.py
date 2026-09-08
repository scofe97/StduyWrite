# 03-04 §5 — 흐름 제어와 혼잡 제어를 나란히. 병목과 신호가 다르고, 마지막에 min{cwnd, rwnd} 하나로 합쳐진다.
# 노트의 읽기: 2026-09-08 회차. §4·§5 가 혼잡을 도입하는데 §1 의 흐름 제어와 어떻게 이어지는지가 없었다.
#       둘의 결정적 차이는 "보내는 쪽이 어떻게 아느냐" — 하나는 상대가 숫자로 알려 주고, 하나는 아무도 안 알려 줘서
#       손실과 지연으로 추측한다. 그래서 하나만으론 안 되고 실제 TCP 는 둘 중 작은 쪽을 쓴다.
#   RFC 5681 §3.1: "The minimum of cwnd and rwnd governs data transmission."
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 갈리는 축, 열은 두 조임 장치.
#       축약: 열이 둘뿐이라 열 폭을 148 에서 296 으로 넓혀 이 책의 폭 규칙(880~1000)에 맞췄다.
#       마지막 행은 두 열에 걸친 focal 셀 하나로 "둘이 하나로 합쳐진다" 를 보인다 — 연결선 없이 셀만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

roles = [("흐름 제어", "받는 쪽이 못 따라올 때"), ("혼잡 제어", "망이 못 견딜 때")]
rows = ["병목이 어디인가", "무엇이 넘치나", "보내는 쪽이 어떻게 아나", "창의 이름", "값을 정하는 쪽"]
# cells[row][col] = (표시값, 색 오버라이드 또는 None)
cells = [
    [("받는 쪽 애플리케이션", None), ("경로 중간의 라우터", None)],
    [("수신 버퍼", None), ("라우터 버퍼", None)],
    [("상대가 숫자로 알려 준다", INFO), ("손실·지연으로 추측한다", WARN)],
    [("rwnd · 수신 창", None), ("cwnd · 혼잡 창", None)],
    [("받는 쪽이 잰다", None), ("보내는 쪽이 추정한다", None)],
]

LEFT, RIGHT = 12, 48
COMP_W, GAP, COL_W, COL_GAP = 268, 12, 296, 16
HEADER_Y, HEADER_H = 96, 52
ROW_H, STRIDE = 36, 40
n = len(roles)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT      # 948
row_y = lambda k: 164 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
FOOT_Y, FOOT_H = row_y(len(rows)), 44
bottom = FOOT_Y + FOOT_H
H = bottom + 20 + 44

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §5",
      "같은 조임, 다른 이유, 하나의 한도",
      "흐름 제어와 혼잡 제어는 둘 다 송신자를 조이지만 병목과 신호가 다르다. "
      "실제로 보낼 수 있는 양은 두 창 중 작은 쪽이다.",
      "다른 것은 보내는 쪽이 어떻게 아느냐입니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "무엇이 다른가", 12, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 41, "vs. 두 조임 장치", 12, MUTED)
for j, (name, sub) in enumerate(roles):
    d.box(col_x(j), HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 24, name, 12, INK, KR, "middle", 600)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 41, sub, 12, MUTED, KR)

for k, name in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LEFT + 12, y + 23, name, 12, INK, KR, "start")
    for j, (val, c) in enumerate(cells[k]):
        if c:
            d.tone(col_x(j), y, COL_W, ROW_H, c, 4, "14", 1.0)
            d.t(col_x(j) + COL_W / 2, y + 23, val, 12, c, KR, "middle", 600)
        else:
            d.box(col_x(j), y, COL_W, ROW_H, PAPER, RULE, 0.6, r=4)
            d.t(col_x(j) + COL_W / 2, y + 23, val, 12, INK, _kr(val))

# 합류 행 — 두 열에 걸친 focal 셀 하나
d.box(LEFT, FOOT_Y, COMP_W, FOOT_H, PAPER2, RULE, 0.9, r=4)
d.t(LEFT + 12, FOOT_Y + 27, "실제로 보낼 수 있는 양", 12, INK, KR, "start", 600)
FX, FW = col_x(0), col_x(1) + COL_W - col_x(0)
d.tone(FX, FOOT_Y, FW, FOOT_H, ACC, 4, "14", 1.4)
d.t(FX + FW / 2, FOOT_Y + 19, "min{cwnd, rwnd}", 13, ACC, MONO, "middle", 600)
d.t(FX + FW / 2, FOOT_Y + 36, "둘 중 작은 쪽이 한도입니다", 12, ACC, KR, "middle", 400, op="0.85")

d.legend(bottom + 20, [("숫자로 알려 준다", INFO), ("손실·지연으로 추측한다", WARN), ("둘 중 작은 쪽", ACC)])
d.save("03-04.rwnd-vs-cwnd.svg")
print("ok 03-04.rwnd-vs-cwnd")
