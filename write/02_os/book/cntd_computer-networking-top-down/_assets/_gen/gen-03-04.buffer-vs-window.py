# 03-04 §1 — 수신 버퍼는 메모리이고 Window 칸은 그 여유를 적은 숫자다. 윈도우 스케일은 칸이 아니라 눈금의 뜻을 바꾼다.
# 노트의 읽기: 2026-09-08 회차에서 학습자가 "윈도우가 어떤 저장소의 이름인가, 백로그 같은 것인가" 라고 물어
#       추가한 도식. 원문 3.5.5 는 RcvBuffer 와 rwnd 의 식만 주고, 둘이 다른 층(메모리 vs 숫자)이라는 말은 없다.
#   RFC 7323 §2.1: "uses an implicit scale factor to carry this 30-bit value in the 16-bit window field of the TCP header"
#   RFC 7323 §2.2: "The maximum scale exponent is limited to 14 for a maximum permissible receive window size of 1 GiB (2^(14+16))."
#   RFC 7323 §2.4: "The end of the window will be on a boundary based on the granularity of the scale factor being used."
# 타입 스펙: type-bar — 가로 누적 막대 변형. 위 막대는 수신 버퍼(안 읽은 데이터 + 여유), 아래 막대는 칸에 적힌 숫자.
#       두 막대가 한 눈금 축을 공유하고 눈금 라벨을 두 줄(×1 · ×128)로 달아 "칸은 그대로인데 읽는 법이 달라진다"
#       를 보인다 — 눈금 100 짜리 저울로 1,000 kg 을 재는 것과 같다. 값 좌표는 스펙대로 축 공식으로 산출한다.
#       축약: 막대가 둘이라 스펙의 4~8개 하한을 밑돈다. 비교 대상이 둘뿐이고 셋째를 지어내지 않는다.
#       왼쪽 여백은 스펙 dumbbell 변형의 200 을 쓴다 — 한글 행 라벨이 길다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560
PX0, PX1, DOM = 200, 960, 65536
def X(v): return PX0 + v * (PX1 - PX0) / DOM

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §1",
      "수신 버퍼는 메모리이고 Window 칸은 숫자입니다",
      "커널의 수신 버퍼에서 안 읽은 바이트를 뺀 여유가 rwnd 이고, 그 숫자가 16비트 Window 칸에 실린다. "
      "윈도우 스케일은 칸을 늘리지 않고 눈금 하나의 뜻을 바꾼다.",
      "칸은 그대로인데 읽는 법이 달라집니다")

TICKS = [0, 16384, 32768, 49152, 65536]
AXIS_Y = 296
for v in TICKS:
    d.line(X(v), 112, X(v), AXIS_Y, "rgba(245,245,245,0.08)", 0.8)
d.line(PX0, AXIS_Y, PX1, AXIS_Y, "rgba(245,245,245,0.20)", 1.0)

def bar(x0, x1, y, h, c, op):
    d.box(x0, y, x1 - x0, h, PAPER, "none", 0, 4)          # 스펙의 불투명 종이 마스크
    d.tone(x0, y, x1 - x0, h, c, 4, op, 1.0)

# ── 막대 1: 수신 버퍼 (안 읽은 데이터 + 여유) ─────────────────────
UNREAD, FREE = 40960, 24576
Y1, BH = 128, 48
d.t(188, Y1 + 20, "수신 버퍼", 13, INK, KR, "end", 600)
d.t(188, Y1 + 38, "실제 메모리 · RcvBuffer", 12, MUTED, KR, "end")
bar(X(0), X(UNREAD), Y1, BH, MUTED, "26")
bar(X(UNREAD), X(DOM), Y1, BH, INFO, "26")
d.t((X(0) + X(UNREAD)) / 2, Y1 + 29, "안 읽은 데이터 · 40,960", 12, INK, KR, "middle", 600)
d.t((X(UNREAD) + X(DOM)) / 2, Y1 + 29, "여유 = rwnd · 24,576", 12, INFO, KR, "middle", 600)
d.t(PX1, Y1 - 10, "합계 65,536", 12, MUTED, MONO, "end")

# ── 막대 2: Window 칸에 적힌 숫자 (focal) ─────────────────────────
Y2 = 216
d.t(188, Y2 + 20, "Window 칸", 13, INK, KR, "end", 600)
d.t(188, Y2 + 38, "TCP 헤더의 16비트 숫자", 12, MUTED, KR, "end")
bar(X(0), X(FREE), Y2, BH, ACC, "20")
d.t((X(0) + X(FREE)) / 2, Y2 + 29, "24,576", 13, ACC, MONO, "middle", 600)
d.t(X(FREE) + 12, Y2 + 29, "여유를 그대로 적은 숫자 · 최대 65,535", 12, MUTED, KR, "start")

# ── 눈금 두 줄: 같은 눈금, 다른 뜻 ───────────────────────────────
d.t(188, 324, "×1 로 읽으면", 12, MUTED, KR, "end")
for v, lab in zip(TICKS, ["0", "16 KiB", "32 KiB", "48 KiB", "64 KiB"]):
    d.t(X(v), 324, lab, 12, MUTED, MONO)
d.t(188, 352, "×128 로 읽으면", 12, ACC, KR, "end")
for v, lab in zip(TICKS, ["0", "2 MiB", "4 MiB", "6 MiB", "8 MiB"]):
    d.t(X(v), 352, lab, 12, ACC, MONO)

d.t(24, 412, "배수 shift.cnt 는 SYN 에서 한 번 교환하고 그 뒤로는 양쪽이 기억해 곱합니다. 7 이면 ×128 이고, 칸은 16비트 그대로입니다.",
    12, MUTED, KR, "start")
d.t(24, 436, "×128 로 읽으면 눈금 하나가 128 바이트라, 창은 128 바이트 단위로만 표현됩니다.",
    12, MUTED, KR, "start")

d.legend(H - 44, [("안 읽은 데이터", MUTED), ("여유 = rwnd", INFO), ("칸에 적히는 숫자", ACC)])
d.save("03-04.buffer-vs-window.svg")
print("ok 03-04.buffer-vs-window")
