# 04-02 §4 — 출력 포트의 줄. 패브릭이 회선의 N 배로 빨라도 출력 링크가 하나뿐이라 줄이 선다.
# 단위 시간 셋을 가로로 펴서 "셋이 들어오고 하나가 나간다"가 큐 길이의 변화로 드러나게 했다.
# 큐 슬롯 수·입력 셋은 장면을 위한 값이다. 원문에 수치 예는 없다.
# 타입 스펙: type-data-flow — semantic-patterns 의 "Fan-in queue / bottleneck".
#           출발지 여럿 · 보이는 큐 슬롯 · 용량 라벨 · 병목 하나 · 넘치면 버림.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 450

IN_X, IN_W, IN_H = 16, 120, 38
IN_Y0, IN_STRIDE = 152, 50

TX, TW, TGAP = 178, 208, 18        # 단위 시간 칸
TY, TH = 128, 208
TICKS = 3

OUT_X, OUT_W = 876, 108
OUT_Y, OUT_H = 200, 60

PW, PH, PGAP = 22, 18, 4

def tick_x(i):
    return TX + (TW + TGAP) * i

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §4",
      "빨라도 출력에는 줄이 섭니다",
      "원문 Figure 4.9. 패브릭이 아무리 빨라도 출력 링크가 하나뿐이라 단위 시간에 하나만 나간다. "
      "셋이 들어오고 하나가 나가므로 차액 둘이 단위 시간마다 출력 큐에 쌓이고, 메모리가 차면 버려야 한다.",
      "패브릭 속도와 무관합니다 — 링크 하나가 병목입니다")

# 입력 포트 셋 — 패브릭을 건너 같은 출력으로 몰린다
d.t(IN_X, IN_Y0 - 24, "패브릭을 건너온 입력", 13, SOFT, KR, "start", 600)
for k in range(3):
    y = IN_Y0 + IN_STRIDE * k
    d.box(IN_X, y, IN_W, IN_H, PAPER2, RULE, 1.0, 6)
    d.t(IN_X + IN_W / 2, y + 24, f"입력 {k + 1}", 13, INK, KR, "middle", 600)
d.t(IN_X + IN_W / 2, IN_Y0 + IN_STRIDE * 3 + 16, "모두 같은 출력으로", 13, SOFT, KR)
my = IN_Y0 + IN_STRIDE + IN_H / 2
d.path(f"M {IN_X + IN_W + 4} {my} L {TX - 8} {my}", MUTED, 1.3, m="ar")

def prow(x, y, n, c, cap=6):
    shown = min(n, cap)
    for i in range(shown):
        d.tone(x + i * (PW + PGAP), y, PW, PH, c, 3, "22", 1.1)
    if n > cap:
        d.t(x + shown * (PW + PGAP) + 4, y + 14, f"+{n - cap}", 12, c, MONO, "start", 600)

# 단위 시간 칸 — 도착 3 · 나감 1 · 큐에 남음
SCENE = [(3, 1, 2, False), (3, 1, 4, False), (3, 1, 6, True)]
for i, (arr, out, left, focal) in enumerate(SCENE):
    x = tick_x(i)
    d.box(x, TY, TW, TH, PAPER2, RULE, 1.0, 6)
    d.t(x + TW / 2, TY - 12, f"단위 시간 {i + 1}", 13, MUTED, KR, "middle", 600)
    if i:
        d.path(f"M {x - TGAP + 4} {TY + TH / 2} L {x - 6} {TY + TH / 2}", MUTED, 1.2, m="ar")

    ix = x + 14
    d.t(ix, TY + 28, "도착", 13, SOFT, KR, "start")
    prow(ix + 40, TY + 14, arr, MUTED)

    d.t(ix, TY + 72, "나감", 13, OK, KR, "start")
    prow(ix + 40, TY + 58, out, OK)

    cq = ACC if focal else WARN
    d.t(ix, TY + 116, "큐에", 12, cq, KR, "start")
    prow(ix + 40, TY + 102, left, cq, cap=5)

    by = TY + TH - 40
    if focal:
        d.tone(ix - 6, by, TW - 16, 32, ACC, 5, "14", 1.4)
    else:
        d.line(ix - 6, by - 4, ix + TW - 22, by - 4, RULE, 0.8)
    d.t(x + TW / 2, by + 21, f"큐 길이 {left}", 13, cq, KR, "middle", 600)

# 출력 링크 — 병목
d.tone(OUT_X, OUT_Y, OUT_W, OUT_H, ACC, 6, "14", 1.4)
d.t(OUT_X + OUT_W / 2, OUT_Y + 26, "출력 링크", 13, ACC, KR, "middle", 600)
d.t(OUT_X + OUT_W / 2, OUT_Y + 46, "1개 / 단위", 12, SOFT, MONO)
d.path(f"M {tick_x(2) + TW + 6} {OUT_Y + OUT_H / 2} L {OUT_X - 4} {OUT_Y + OUT_H / 2}", OK, 1.4, m="ok")

# 넘치면 버림 — 큐 아래로 내려 오른쪽 폐기함으로
DBX, DBY, DBW, DBH = 764, 348, 176, 40
d.path(f"M {tick_x(2) + TW / 2} {TY + TH + 4} L {tick_x(2) + TW / 2} {DBY + DBH / 2} L {DBX - 6} {DBY + DBH / 2}",
       BAD, 1.3, m="bad", dash="5 4")
d.tone(DBX, DBY, DBW, DBH, BAD, 6, "14", 1.1)
d.t(DBX + DBW / 2, DBY + 25, "메모리가 차면 버림", 13, BAD, KR, "middle", 600)

d.legend(H - 44, [("출력 링크 — 병목", ACC), ("나감", OK), ("큐에 남음", WARN), ("버림", BAD)])
d.save("04-02.output-queue.svg")
