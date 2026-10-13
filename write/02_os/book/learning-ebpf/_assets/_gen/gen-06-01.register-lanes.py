# 타입 스펙: type-swimlane — 레인 다섯(R1 · R2 · R3 · R6 · R10), 가로축 명령 여섯(0 · 1 · 3 · 4 · 5 · 6). 칸은 그 명령을 실행한 뒤의 상태.
# 사실 출처: 추출본 src/ebpf6.txt 162~174행(0: r6 = r1 … 6: *(u32 *)(r1 +0) = r3, R1 map_value vs=16, R6 ctx, R10=fp0),
#   213~214행(R2 umax_value=4294967295, R3 umin_value=1 umax_value=4294967296). 명령 2 는 ld_imm64 의 두 번째 슬롯이라 열이 없다.
# Layout conventions: 레인 라벨 x=24 w=80, 명령 열 w=132 gap=8, 레인 stride 76, 상태 칸 h=60. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W = 968
LX, LW = 24, 80
CX0, CW, GAP = 112, 132, 8
HY = 108
LY0, STRIDE, CH = 160, 76, 60
cols = ["0 · r6 = r1", "1 · r1 = 0xffff…", "3 · r2 = *(u32*)", "4 · r3 = r2", "5 · r3 += 1", "6 · *(u32*) = r3"]
LEG_Y = LY0 + 5 * STRIDE + 8
H = LEG_Y + 56


def cx(j):
    return CX0 + j * (CW + GAP)


d = D(W, H, "LEARNING EBPF · 06-01 §2",
      "명령 0~6 에서 레지스터 다섯의 타입과 범위가 바뀌는 순서",
      "칸은 그 명령을 실행한 뒤의 상태이고 칸이 없는 열은 앞 상태가 이어진다. R3 의 범위만 두 번 바뀐다.",
      "가로 = 명령 번호 · 세로 = 레지스터")

for j, c in enumerate(cols):
    d.box(cx(j), HY, CW, 36, PAPER2, RULE, 0.9, 4)
    d.t(cx(j) + CW / 2, HY + 23, c, 12, INK, MONO)

lanes = [
    ("R1", [(0, ["ctx"], INFO), (1, ["map_value", "vs=16"], OK)]),
    ("R2", [(2, ["scalar", "umax 4294967295"], INFO)]),
    ("R3", [(3, ["scalar", "= R2"], INFO), (4, ["scalar", "umin 1", "umax 4294967296"], ACC)]),
    ("R6", [(0, ["ctx"], INFO)]),
    ("R10", [(0, ["fp0"], INFO)]),
]
# 상태가 시작되는 열 → 레인 끝까지 이어지는 선
span = {"R1": 0, "R2": 2, "R3": 3, "R6": 0, "R10": 0}
for i, (name, cells) in enumerate(lanes):
    y = LY0 + i * STRIDE
    d.box(LX, y, LW, CH, PAPER2, RULE, 0.9, 4)
    d.t(LX + LW / 2, y + 36, name, 13, INK, MONO, "middle", 600)
    xs = [(cx(j), cx(j) + CW) for (j, _, _) in cells]
    pts = [xs[0][1]] + [v for ab in xs[1:] for v in ab] + [cx(5) + CW]
    for a, b in zip(pts[0::2], pts[1::2]):
        if b - a > 1:
            d.line(a, y + CH / 2, b, y + CH / 2, SOFT, 1.0, "3 6")
    for (j, lines, c) in cells:
        if c == ACC:
            d.tone(cx(j), y, CW, CH, ACC, 6, "18", 1.4)
        else:
            d.tone(cx(j), y, CW, CH, c, 6, "12", 1.2)
        n = len(lines)
        top = y + CH / 2 - (n - 1) * 9 + 4
        for k, ln in enumerate(lines):
            d.t(cx(j) + CW / 2, top + k * 18, ln, 12, c if k == 0 else INK, MONO, "middle", 600 if k == 0 else 400)

d.legend(LEG_Y, [("컨텍스트 · 값", INFO), ("맵 값 포인터", OK), ("범위가 넓어지는 칸", ACC)])
d.save("06-01.register-lanes.svg")
