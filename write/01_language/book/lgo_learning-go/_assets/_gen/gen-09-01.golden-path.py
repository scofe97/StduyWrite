# 09-01.golden-path — 오류는 if 안으로 옆으로 빠지고, 본문은 들여쓰지 않은 채 곧게 내려간다
# 본문 요구(09-01 §1 「예외 대신 반환 값을 쓰는 두 이유」): 원문은 오류 처리는 if 문 안으로 들여쓰고 비즈니스 로직은 들여쓰지 않아
#           어느 코드가 "황금 경로"이고 어느 코드가 예외 상황인지 눈으로 바로 구별된다고 말한다. main 의 calcRemainderAndMod 호출로 그린다.
# 타입 스펙: type-flowchart — 09-01.error-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각, 끝 타원).
#           황금 경로는 왼쪽 열(x 중심 256)로 곧게 내려가고, 예 가지는 오른쪽 결과 열(x 536)로 빠져 거기서 끝난다.
#           stride 세로 96. coral 은 오류 가지 하나(들여쓴 코드).
# 사실 출처: Learning Go 2판 9장 「How to Handle Errors: The Basics」, go1.25.1 로컬 실행(2026-09-27) — 6 2.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 572
CX, RX, RW, RH = 256, 536, 400, 56
DW, DH = 280, 60
START_Y = 112
Q_Y = START_Y + 40 + 64 + DH // 2          # 216
OK_Y = Q_Y + DH // 2 + 88                  # 334
END_Y = OK_Y + RH // 2 + 48                # 410


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def oval(cx, y, w, text, c=None):
    stroke = c or "rgba(191,192,192,0.22)"
    fill = (c + "14") if c else PAPER2
    d.o.append(f'<rect x="{cx - w // 2}" y="{y}" width="{w}" height="40" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="0.9"/>')
    d.t(cx, y + 25, text, 13, c or INK, kr(text), "middle", 600)


d = D(W, H, "FLOWCHART · 09-01 §1",
      "오류는 옆으로 빠지고 본문은 곧게 내려갑니다",
      "main 이 calcRemainderAndMod 를 부른 뒤의 흐름. 돌아온 err 를 if 로 nil 과 비교해, nil 이 아니면 들여쓴 블록에서 오류를 찍고 끝낸다. "
      "nil 이면 들여쓰지 않은 본문이 이어져 6 2 를 찍는다. 원문이 황금 경로라 부르는 것이 왼쪽 열이다.",
      lead="왼쪽 열이 들여쓰지 않은 황금 경로, 오른쪽이 if 안으로 들여쓴 오류 처리입니다.")

oval(CX, START_Y, 320, "calcRemainderAndMod(20, 3)")
d.arrow([(CX, START_Y + 40), (CX, Q_Y - DH // 2)], SOFT, "soft", 1.2)
d.t(CX + 12, START_Y + 40 + 32, "remainder, mod, err", 12, MUTED, MONO, "start")

pts = f"{CX},{Q_Y - DH // 2} {CX + DW // 2},{Q_Y} {CX},{Q_Y + DH // 2} {CX - DW // 2},{Q_Y}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, Q_Y + 5, "err != nil ?", 14, INK, MONO, "middle", 600)

d.arrow([(CX + DW // 2, Q_Y), (RX, Q_Y)], ACC, "acc", 1.3)
d.t(CX + DW // 2 + 48, Q_Y - 8, "예", 12, ACC, KR, "middle", 600)
d.tone(RX, Q_Y - RH // 2, RW, RH, ACC, 6, "10", 1.2)
d.t(RX + 16, Q_Y - 4, "fmt.Println(err) · os.Exit(1)", 13, ACC, MONO, "start", 600)
d.t(RX + 16, Q_Y + 16, "if 안으로 들여쓴 오류 처리 · 여기서 끝", 12, MUTED, KR, "start")

d.arrow([(CX, Q_Y + DH // 2), (CX, OK_Y - RH // 2)], SOFT, "soft", 1.2)
d.t(CX + 12, Q_Y + DH // 2 + 34, "아니오", 12, MUTED, KR, "start")
d.tone(CX - RW // 2 + 40, OK_Y - RH // 2, RW - 80, RH, OK, 6, "10", 1.0)
d.t(CX, OK_Y - 4, "fmt.Println(remainder, mod)", 13, OK, MONO, "middle", 600)
d.t(CX, OK_Y + 16, "들여쓰지 않은 본문", 12, MUTED, KR, "middle")

d.arrow([(CX, OK_Y + RH // 2), (CX, END_Y)], SOFT, "soft", 1.2)
oval(CX, END_Y, 160, "6 2", OK)

d.line(CX - 176, START_Y - 8, CX - 176, END_Y + 48, RULE, 0.8, "3 4")
d.t(CX - 184, END_Y + 44, "황금 경로", 12, MUTED, KR, "end", 600)

d.legend(516, [("황금 경로", OK), ("오류 처리", ACC)])
d.save("09-01.golden-path.svg")
print("ok 09-01 golden-path")
