# 20-01 「스레드가 나누는 것과 따로 갖는 것」 — 스레드는 코드·힙을 한 주소 공간에서 함께 쓰고, 스택은 스레드마다 하나씩 가진다.
# 본문 근거: 이 노트 「1. 스레드와 주소 공간」.
# 값 근거: OSTEP 26장 그림 26.1 의 0KB·1KB·2KB·15KB·16KB 눈금. 스택 (2) 의 시작 눈금은 원서 그림에서 읽히지 않아 적지 않는다.
# 점선 층 「정적 데이터」: 원서 그림 26.1 에 없는 층이다(그림은 코드·힙·스택 셋뿐). 13장은 "statically-initialized variables" 가 주소 공간에 더 있지만 셋만 가정한다고 말한다.
#   자리는 코드 다음, 힙 앞이다. 근거 — man7.org end(3) (Linux man-pages 6.19): etext 는 "the first address past the end of the text segment (the program code)",
#   edata 는 "the first address past the end of the initialized data segment", end 는 "the first address past the end of the uninitialized data segment (also known as the BSS segment)" 이고,
#   "At the start of program execution, the program break will be somewhere near &end". brk(2) 는 "the program break is the first location after the end of the uninitialized data segment" 라고 적는다.
#   즉 텍스트 → 초기화된 데이터 → 초기화되지 않은 데이터 → program break(힙이 자라는 끝) 순이다. 두 데이터 세그먼트를 한 층 「정적 데이터」 로 묶어 그린다.
#   눈금: 원서 눈금 글자는 그대로이고 1KB 는 코드 아래 변, 2KB 는 힙 아래 변에 붙는다. 점선 층에는 눈금을 붙이지 않고 왼쪽 눈금 열에 「눈금 없음」 을 적는다. 힙은 점선 층 아래로 밀려 내려간다.
# 공식 근거: OSTEP 26장 §26.1 — 스레드마다 PC·레지스터가 따로 있고(TCB), 다중 스레드 프로세스는 스택이 스레드 수만큼 있다.
# 타입 스펙: type-layers — 같은 높이 눈금의 두 층 쌓기. 왼쪽 단일 스레드, 오른쪽 다중 스레드를 나란히 두고 달라진 층만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W, H = 920, 596
d = D(W, H, "LAYERS · 20-01 §1",
      "스레드를 더하면 주소 공간에서 스택만 한 층 늘어난다",
      "단일 스레드 프로세스의 주소 공간은 위에서부터 프로그램 코드(0KB~1KB), 정적 데이터, 힙(아래 변이 2KB), 빈 공간, 스택(15KB~16KB)으로 쌓인다. "
      "스레드가 둘인 프로세스의 주소 공간은 코드·정적 데이터·힙이 그대로이고, 빈 공간 아래쪽에 스택이 하나 더 생겨 스택 (2) 와 스택 (1) 두 개가 놓인다. "
      "전역 변수가 놓이는 정적 데이터 층은 코드와 힙 사이에 있다. 원서 그림에 없어 점선으로 더했고 눈금은 붙이지 않았다. 이 층도 스레드가 함께 쓴다.",
      lead="왼쪽은 스레드 하나, 오른쪽은 스레드 둘입니다. 눈금은 원서 값이고, 코드와 힙 사이의 점선 층은 원서 그림에 없습니다.")

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
    # 원서 그림에 없는 층: 코드와 힙 사이, 점선 테두리, 눈금 없음
    d.o.append(f'<rect x="{x}" y="{TOP + 56}" width="{LW}" height="52" rx="6" fill="{INFO}18" stroke="{INFO}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    d.t(x + LW / 2, TOP + 56 + 24, "정적 데이터", 14, INFO, KR, "middle", 600)
    d.t(x + LW / 2, TOP + 56 + 44, "전역 변수 · 원서 그림에 없는 층", 12, MUTED, KR, "middle")
    layer(x, TOP + 112, 52, "힙", "malloc 으로 받은 데이터", INFO)
    layer(x, TOP + 168, 108 if two else 176, "빈 공간", None)
    if two:
        layer(x, TOP + 280, 60, "스택 (2)", "스레드 2 의 지역 변수·인자", ACC)
        layer(x, TOP + 344, 60, "스택 (1)", "스레드 1 의 지역 변수·인자", ACC)
    else:
        layer(x, TOP + 344, 60, "스택", "지역 변수·인자·반환값", ACC)


column(LX, "스레드 하나", False)
column(RX, "스레드 둘", True)

# 눈금(왼쪽 열 기준, 오른쪽 열도 같은 높이)
for yy, lab in ((TOP, "0KB"), (TOP + 52, "1KB"), (TOP + 164, "2KB"), (TOP + 344, "15KB"), (TOP + 404, "16KB")):
    d.t(LX - 12, yy + 4, lab, 12, MUTED, MONO, "end")
    d.t(RX - 12, yy + 4, lab, 12, MUTED, MONO, "end")
# 점선 층 옆 눈금 열: 원서 눈금이 없다는 표시
d.t(LX - 12, TOP + 56 + 30, "눈금 없음", 12, MUTED, KR, "end")
d.t(RX - 12, TOP + 56 + 30, "눈금 없음", 12, MUTED, KR, "end")

# 가운데 표지: 달라진 층
d.arrow([(LX + LW + 12, TOP + 372), (RX - 52, TOP + 372)], ACC, "acc", 1.5)
d.t((LX + LW + RX - 52) / 2 + 6, TOP + 358, "스택이 하나 더", 13, ACC, KR, "middle", 600)

d.legend(H - 40, [("함께 쓰는 층", INFO), ("스레드마다 따로", ACC), ("아직 안 쓴 공간", SOFT)])
d.save("20-01.address-space.svg")
print("ok 20-01 address-space")
