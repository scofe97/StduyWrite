# 02-02.declare-choice — 변수 선언 형태를 고르는 네 갈림길
# 본문 요구(02-02 §1 「var 와 := 중 무엇을 쓸까」): 원문은 함수 안의 기본을 := 로 두고, := 를 피할 경우 셋과
#           함수 밖에서는 var 만 된다는 제약을 든다. 위에서 아래로 물음을 차례로 거치는 판단 흐름이다.
# 타입 스펙: type-flowchart — 시작·끝은 타원(rx 20), 판단은 마름모(출구 2), 결과는 사각형(rx 6).
#           흐름은 위→아래, 예는 오른쪽·아니오는 아래로 나가며 모든 출구에 라벨. coral 은 := 로 가는 기본 경로 한 곳.
#           stride 는 세로 88, 판단 열 중심 x 256, 결과 열 x 536. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 2장 「var Versus :=」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 684
CX, RX, RW, RH = 256, 536, 400, 48
DW, DH = 312, 60
START_Y, STRIDE = 112, 96
Q_Y = [START_Y + 88 + i * STRIDE for i in range(4)]     # 마름모 중심 y: 200 296 392 488


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(d, cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 13, INK, kr(text), "middle", 600)


def result(d, y, main, sub, c):
    d.tone(RX, y - RH // 2, RW, RH, c, 6, "10", 1.0)
    d.t(RX + 16, y - 2, main, 14, c, kr(main), "start", 600)
    d.t(RX + 16, y + 16, sub, 12, MUTED, kr(sub), "start")


d = D(W, H, "FLOWCHART · 02-02 §1",
      "var 와 := 중 무엇을 쓸까",
      "원문이 드는 변수 선언 규칙을 위에서 아래로 네 물음으로 이은 흐름도. 함수 밖이면 var 만 쓸 수 있고, "
      "함수 안에서도 제로 값을 의도할 때, 리터럴의 기본 타입이 원하는 타입이 아닐 때, 새 변수와 기존 변수가 섞일 때는 var 를 쓴다. "
      "넷 다 아니면 := 가 함수 안의 기본이다.",
      lead="예는 오른쪽 결과로, 아니오는 아래 물음으로 내려갑니다.")

# 시작
d.o.append(f'<rect x="{CX - 96}" y="{START_Y}" width="192" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "변수 선언", 14, INK, KR, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y[0] - DH // 2)], SOFT, "soft", 1.2)

qs = ["함수 밖?", "제로 값이 의도?", "리터럴 기본 타입과 다름?", "새 변수 · 기존 변수 섞임?"]
rs = [("var ( ... )", "패키지 수준 · := 는 문법 에러", WARN),
      ("var x int", "제로 값을 쓴다는 표시", INFO),
      ("var x byte = 20", "x := byte(20) 보다 관용적", INFO),
      ("새 변수는 var · 대입은 =", "섀도잉 실수 방지", INFO)]

for i, q in enumerate(qs):
    y = Q_Y[i]
    diamond(d, CX, y, q)
    d.arrow([(CX + DW // 2, y), (RX, y)], SOFT, "soft", 1.2)
    d.t(CX + DW // 2 + 44, y - 8, "예", 12, MUTED, KR, "middle")
    result(d, y, *rs[i])
    nxt = Q_Y[i + 1] - DH // 2 if i < 3 else 576
    c, m = (ACC, "acc") if i == 3 else (SOFT, "soft")
    d.arrow([(CX, y + DH // 2), (CX, nxt)], c, m, 1.4 if i == 3 else 1.2)
    d.t(CX + 12, y + DH // 2 + 22, "아니오", 12, ACC if i == 3 else MUTED, KR, "start")

# 끝 — 함수 안의 기본
d.o.append(f'<rect x="{CX - 120}" y="576" width="240" height="44" rx="20" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, 604, "x := 10", 15, ACC, MONO, "middle", 600)
d.t(CX + 136, 604, "함수 안의 기본", 12, MUTED, KR, "start")

d.legend(636, [("var 만 가능", WARN), ("var 가 더 분명", INFO), ("기본 경로", ACC)])
d.save("02-02.declare-choice.svg")
print("ok 02-02 declare-choice")
