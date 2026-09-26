# 04-02.for-choice — for 네 형태 가운데 무엇을 쓸까
# 본문 요구(04-02 §5 「for 형태 고르기」): 원문은 대부분 for-range, 복합 타입의 처음부터 끝까지가 아니면 완전 for,
#           계산한 값을 조건으로 돌면 조건만 for, 나머지 드문 경우는 break·return 을 품은 무한 for 라고 정리한다.
#           위에서 아래로 물음을 차례로 거치는 판단 흐름이다.
# 타입 스펙: type-flowchart — 02-02.declare-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각, 끝 타원).
#           첫 장의 stride·여백을 그대로 쓴다: 세로 stride 96, 판단 열 중심 x 256, 결과 열 x 536.
#           coral 은 원문이 "대부분" 이라 한 for-range 결과 하나.
# 사실 출처: Learning Go 2판 4장 「Choosing the Right for Statement」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 588
CX, RX, RW, RH = 256, 536, 400, 48
DW, DH = 312, 60
START_Y, STRIDE = 112, 96
Q_Y = [START_Y + 88 + i * STRIDE for i in range(3)]     # 200 296 392


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 13, INK, kr(text), "middle", 600)


def result(y, main, sub, c, focal=False):
    d.tone(RX, y - RH // 2, RW, RH, c, 6, "14" if focal else "10", 1.4 if focal else 1.0)
    d.t(RX + 16, y - 2, main, 14, c, kr(main), "start", 600)
    d.t(RX + 16, y + 16, sub, 12, MUTED, kr(sub), "start")


d = D(W, H, "FLOWCHART · 04-02 §5",
      "for 네 형태 가운데 무엇을 쓸까",
      "원문의 for 형태 선택 기준을 위에서 아래로 세 물음으로 이은 흐름도. 복합 타입을 처음부터 끝까지 돌면 for-range, "
      "시작과 끝을 따로 정해 돌면 완전 for, 계산한 값을 조건으로 돌면 조건만 for 를 쓴다. 셋 다 아니면 break 나 return 을 품은 "
      "무한 for 이고, 다른 언어의 do-while 도 이 모양으로 흉내 낸다.",
      lead="예는 오른쪽 결과로, 아니오는 아래 물음으로 내려갑니다.")

d.o.append(f'<rect x="{CX - 96}" y="{START_Y}" width="192" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "반복이 필요함", 14, INK, KR, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y[0] - DH // 2)], SOFT, "soft", 1.2)

qs = ["복합 타입 전체를 차례로?", "시작·끝을 따로 정함?", "계산한 값이 조건?"]
rs = [("for i, v := range s", "slice·map·문자열(룬 단위)·채널", ACC, True),
      ("for i := 1; i < n-1; i++", "완전 for · 문자열에는 쓰지 않음", INFO, False),
      ("for i < 100", "조건만 for · 다른 언어의 while", INFO, False)]
for i, q in enumerate(qs):
    y = Q_Y[i]
    diamond(CX, y, q)
    d.arrow([(CX + DW // 2, y), (RX, y)], SOFT, "soft", 1.2)
    d.t(CX + DW // 2 + 44, y - 8, "예", 12, MUTED, KR, "middle")
    result(y, *rs[i])
    nxt = Q_Y[i + 1] - DH // 2 if i < 2 else 480
    d.arrow([(CX, y + DH // 2), (CX, nxt)], SOFT, "soft", 1.2)
    d.t(CX + 12, y + DH // 2 + 22, "아니오", 12, MUTED, KR, "start")

d.o.append(f'<rect x="{CX - 120}" y="480" width="240" height="44" rx="20" fill="{WARN}10" stroke="{WARN}" stroke-width="1.0"/>')
d.t(CX, 508, "for { ... break }", 15, WARN, MONO, "middle", 600)
d.t(CX + 136, 500, "무한 for", 13, WARN, KR, "start", 600)
d.t(CX + 136, 518, "break·return 필수 · do-while 대신", 12, MUTED, KR, "start")

d.legend(540, [("대부분 여기", ACC), ("나머지 두 형태", INFO), ("드물게 · 끝낼 길을 반드시 둠", WARN)])
d.save("04-02.for-choice.svg")
print("ok 04-02 for-choice")
