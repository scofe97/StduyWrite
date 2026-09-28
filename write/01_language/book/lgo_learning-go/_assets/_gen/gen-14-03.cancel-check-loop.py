# 14-03.cancel-check-loop — 오래 도는 계산은 매 반복 앞에서 context.Cause 를 확인해, 취소됐으면 부분 결과와 오류를 돌려준다
# 본문 요구(14-03 §2 「오래 도는 코드는 스스로 취소를 확인합니다」): 라이프니츠 급수 루프는 매 반복 앞에서 context.Cause(ctx) 를 보고,
#           오류가 있으면 반복 횟수를 찍고 지금까지의 합과 오류를 돌려준다. 없으면 한 항을 더하거나 빼고 다음 반복으로 간다.
# 타입 스펙: type-flowchart — 09-01.error-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각). 판단 열 x 256, 결과 열 x 536.
#           아니오 가지는 아래 처리 사각을 거쳐 왼쪽으로 돌아 판단으로 올라가는 직교 고리. coral 은 취소 가지의 결과 하나.
# 사실 출처: Learning Go 2판 14장 「Context Cancellation in Your Own Code」 own_cancellation, go1.25.1 실행(2026-09-28) —
#           10초 제한에서 cancelled after 60618656 iterations · 10.000877s · context deadline exceeded.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 500
CX, RX, RW, RH = 256, 536, 400, 56
DW, DH = 312, 60
START_Y = 112
Q_Y = START_Y + 40 + 56 + DH // 2          # 238
P_Y = Q_Y + DH // 2 + 64                   # 332
PH = 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "FLOWCHART · 14-03 §2",
      "계산 루프는 매 반복 앞에서 취소를 확인합니다",
      "own_cancellation 의 calcPi 루프. 매 반복 앞에서 context.Cause(ctx) 를 부르고, 오류가 있으면 반복 횟수를 찍은 뒤 지금까지의 합과 오류를 돌려준다. "
      "오류가 없으면 급수의 한 항을 더하거나 빼고 분모를 2 늘려 다시 확인으로 돌아간다. 10초 제한에서는 60,618,656 번 돈 뒤 멈췄다.",
      lead="확인을 반복 앞에 두면 취소 뒤 늦어도 한 반복 안에 멈춥니다.")

d.o.append(f'<rect x="{CX - 120}" y="{START_Y}" width="240" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "calcPi(ctx) · for {", 13, INK, MONO, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y - DH // 2)], SOFT, "soft", 1.2)

pts = f"{CX},{Q_Y - DH // 2} {CX + DW // 2},{Q_Y} {CX},{Q_Y + DH // 2} {CX - DW // 2},{Q_Y}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, Q_Y + 5, "context.Cause(ctx) != nil ?", 12, INK, MONO, "middle", 600)

d.arrow([(CX + DW // 2, Q_Y), (RX, Q_Y)], ACC, "acc", 1.3)
d.t(CX + DW // 2 + 44, Q_Y - 8, "예", 12, ACC, KR, "middle", 600)
d.tone(RX, Q_Y - RH // 2, RW, RH, ACC, 6, "10", 1.4)
d.t(RX + 16, Q_Y - 4, "return sum, err", 13, ACC, MONO, "start", 600)
d.t(RX + 16, Q_Y + 16, "cancelled after 60618656 iterations", 11, MUTED, MONO, "start")

d.arrow([(CX, Q_Y + DH // 2), (CX, P_Y - 4)], SOFT, "soft", 1.2)
d.t(CX + 12, Q_Y + DH // 2 + 26, "아니오", 12, MUTED, KR, "start")
d.tone(CX - 140, P_Y, 280, PH, INFO, 6, "14", 1.1)
d.t(CX, P_Y + 24, "급수 한 항 더하기·빼기", 13, INFO, KR, "middle", 600)
d.t(CX, P_Y + 42, "d += 2 · i++", 11, MUTED, MONO, "middle")

LX = CX - DW // 2 - 24
d.arrow([(CX - 140, P_Y + PH // 2), (LX, P_Y + PH // 2), (LX, Q_Y), (CX - DW // 2 - 4, Q_Y)], SOFT, "soft", 1.2)
d.t(LX - 8, P_Y - 8, "다음 반복", 12, MUTED, KR, "end", 600)

d.legend(444, [("반복 본문", INFO), ("취소되면 부분 결과", ACC)])
d.save("14-03.cancel-check-loop.svg")
print("ok 14-03 cancel-check-loop")
