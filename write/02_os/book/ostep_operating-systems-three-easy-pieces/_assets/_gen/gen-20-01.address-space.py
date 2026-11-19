# 20-01 「스레드가 나누는 것과 따로 갖는 것」 — 스레드는 코드·힙을 한 주소 공간에서 함께 쓰고, 스택은 스레드마다 하나씩 가진다.
# 본문 근거: 이 노트 「1. 스레드와 주소 공간」.
# 값 근거: OSTEP 26장 그림 26.1 의 0KB·1KB·2KB·15KB·16KB 눈금. 스택 (2) 의 시작 눈금은 원서 그림에서 읽히지 않아 적지 않는다.
# 공식 근거: OSTEP 26장 §26.1 — 스레드마다 PC·레지스터가 따로 있고(TCB), 다중 스레드 프로세스는 스택이 스레드 수만큼 있다.
# 타입 스펙: type-layers — 같은 높이 눈금의 두 층 쌓기. 왼쪽 단일 스레드, 오른쪽 다중 스레드를 나란히 두고 달라진 층만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W, H = 920, 596
d = D(W, H, "LAYERS · 20-01 §1",
      "스레드를 더하면 주소 공간에서 스택만 한 층 늘어난다",
      "단일 스레드 프로세스의 주소 공간은 위에서부터 프로그램 코드(0KB~1KB), 힙(1KB~2KB), 빈 공간, 스택(15KB~16KB)으로 쌓인다. "
      "스레드가 둘인 프로세스의 주소 공간은 코드와 힙이 그대로이고, 빈 공간 아래쪽에 스택이 하나 더 생겨 스택 (2) 와 스택 (1) 두 개가 놓인다.",
      lead="왼쪽은 스레드 하나, 오른쪽은 스레드 둘입니다. 눈금은 원서 그림의 값입니다.")

LW = 300
LX, RX = 120, 560
TOP = 112


def layer(x, y, h, name, sub, c=None):
    if c:
        d.tone(x, y, LW, h, c, 6, "18", 1.3 if c == ACC else 1.1)
    else:
        d.box(x, y, LW, h, PAPER2, RULE, 1.0, 6)
    d.t(x + LW / 2, y + h / 2 - (2 if sub else -4), name, 14, c or INK, KR, "middle", 600)
    if sub:
        d.t(x + LW / 2, y + h / 2 + 18, sub, 12, MUTED, KR, "middle")


def column(x, title, two):
    d.t(x + LW / 2, TOP - 12, title, 14, INK, KR, "middle", 600)
    layer(x, TOP, 52, "프로그램 코드", "명령어가 있는 자리", INFO)
    layer(x, TOP + 56, 52, "힙", "malloc 으로 받은 데이터", INFO)
    layer(x, TOP + 112, 164 if two else 232, "빈 공간", None)
    if two:
        layer(x, TOP + 280, 60, "스택 (2)", "스레드 2 의 지역 변수·인자", ACC)
        layer(x, TOP + 344, 60, "스택 (1)", "스레드 1 의 지역 변수·인자", ACC)
    else:
        layer(x, TOP + 344, 60, "스택", "지역 변수·인자·반환값", ACC)


column(LX, "스레드 하나", False)
column(RX, "스레드 둘", True)

# 눈금(왼쪽 열 기준, 오른쪽 열도 같은 높이)
for yy, lab in ((TOP, "0KB"), (TOP + 52, "1KB"), (TOP + 108, "2KB"), (TOP + 344, "15KB"), (TOP + 404, "16KB")):
    d.t(LX - 12, yy + 4, lab, 12, MUTED, MONO, "end")
    d.t(RX - 12, yy + 4, lab, 12, MUTED, MONO, "end")

# 가운데 표지: 달라진 층
d.arrow([(LX + LW + 12, TOP + 372), (RX - 52, TOP + 372)], ACC, "acc", 1.5)
d.t((LX + LW + RX - 52) / 2 + 6, TOP + 358, "스택이 하나 더", 13, ACC, KR, "middle", 600)

d.legend(H - 40, [("함께 쓰는 층", INFO), ("스레드마다 따로", ACC), ("아직 안 쓴 공간", SOFT)])
d.save("20-01.address-space.svg")
print("ok 20-01 address-space")
