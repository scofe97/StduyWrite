# 06-03.escape-decision — 포인터가 가리키는 데이터가 스택에 머무는가, 힙으로 탈출하는가
# 본문 요구(06-03 §1 「컴파일러가 스택에 둘 수 없다고 보면 데이터는 힙으로 탈출합니다」): 원문은 스택에 두려면
#           크기를 아는 지역 변수여야 하고, 포인터를 돌려주지 않아야 하며, 다른 함수에 넘겨도 조건이 지켜진다고
#           컴파일러가 확인할 수 있어야 한다고 말한다. 하나라도 어긋나면 힙으로 탈출한다 — 차례로 거치는 판단 흐름이다.
# 타입 스펙: type-flowchart — 02-02.declare-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각, 끝 타원).
#           흐름은 위→아래, 조건을 어기는 출구는 모두 오른쪽의 힙 결과 하나로 모인다(세 판단 높이를 덮는 세로 사각).
#           stride 는 세로 96, 판단 열 중심 x 256, 결과 열 x 536. coral 은 세 조건을 다 지나 스택에 남는 경로 하나.
# 사실 출처: Learning Go 2판 6장 「Reducing the Garbage Collector's Workload」 조건 문단과 C 비교 메모,
#           go1.25.1 go build -gcflags="-m"(2026-09-27) — MakePersonPointer 의 &Person{...} escapes to heap.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 612
CX, RX, RW = 256, 536, 400
DW, DH = 344, 64
START_Y, STRIDE = 112, 96
Q_Y = [START_Y + 88 + i * STRIDE for i in range(3)]     # 마름모 중심 y: 200 296 392
END_Y = Q_Y[-1] + DH // 2 + 56                           # 480


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 13, INK, kr(text), "middle", 600)


d = D(W, H, "FLOWCHART · 06-03 §1",
      "데이터는 스택에 머무는가, 힙으로 탈출하는가",
      "포인터가 가리키는 데이터를 스택에 두는 원문의 세 조건을 위에서 아래로 이은 흐름도. 컴파일 시점에 크기를 아는 지역 변수가 아니거나, "
      "그 포인터를 함수에서 돌려주거나, 다른 함수에 넘긴 뒤에도 조건이 지켜진다고 컴파일러가 확인할 수 없으면 데이터는 힙으로 탈출한다. "
      "세 조건을 모두 지나야 스택에 남아 함수가 끝날 때 한꺼번에 풀린다.",
      lead="조건을 어기는 출구는 모두 오른쪽 힙으로 모입니다. 판단은 컴파일러가 컴파일 시점에 합니다.")

# 시작
d.o.append(f'<rect x="{CX - 124}" y="{START_Y}" width="248" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "포인터가 가리키는 데이터", 14, INK, KR, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y[0] - DH // 2)], SOFT, "soft", 1.2)

qs = [("크기를 아는 지역 변수?", "아니오"),
      ("포인터를 함수에서 돌려주나?", "예"),
      ("넘긴 함수 안도 확인되나?", "아니오")]
passes = ["예", "아니오", "예"]

# 힙 결과 — 세 판단 높이를 덮는 세로 사각
hy0, hy1 = Q_Y[0] - 28, Q_Y[-1] + 28
d.tone(RX, hy0, RW, hy1 - hy0, WARN, 6, "10", 1.0)
d.t(RX + 24, hy0 + 36, "힙으로 탈출", 15, WARN, KR, "start", 600)
d.t(RX + 24, hy0 + 60, "escapes to heap", 12, MUTED, MONO, "start")
d.t(RX + 24, hy0 + 96, "스택의 변수에서 닿지 않게 되면 가비지", 12, MUTED, KR, "start")
d.t(RX + 24, hy0 + 118, "가비지 컬렉터가 추적해 회수", 12, MUTED, KR, "start")
d.t(RX + 24, hy0 + 154, "예: 지역 변수의 포인터 반환", 12, INK, KR, "start")
d.t(RX + 24, hy0 + 176, "&Person{...} escapes to heap", 12, MUTED, MONO, "start")

for i, (q, out) in enumerate(qs):
    y = Q_Y[i]
    diamond(CX, y, q)
    d.arrow([(CX + DW // 2, y), (RX, y)], SOFT, "soft", 1.2)
    d.t(CX + DW // 2 + 50, y - 8, out, 12, MUTED, KR, "middle")
    nxt = Q_Y[i + 1] - DH // 2 if i < 2 else END_Y
    d.arrow([(CX, y + DH // 2), (CX, nxt)], ACC, "acc", 1.4)
    d.t(CX + 12, y + DH // 2 + 22, passes[i], 12, ACC, KR, "start")

# 끝 — 스택에 남는다
d.o.append(f'<rect x="{CX - 124}" y="{END_Y}" width="248" height="44" rx="20" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, END_Y + 28, "스택에 남음", 15, ACC, KR, "middle", 600)
d.t(CX + 140, END_Y + 28, "함수가 끝나면 한꺼번에 풀림 · 가비지 없음", 12, MUTED, KR, "start")

d.legend(556, [("힙 · GC 대상", WARN), ("스택에 남는 경로", ACC)])
d.save("06-03.escape-decision.svg")
print("ok 06-03 escape-decision")
