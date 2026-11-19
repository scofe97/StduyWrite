# 04-01 「프로그램이 CPU 를 내놓지 않아도 타이머가 통제권을 되찾는다」 — 협력 방식은 프로그램이 스스로 넘기기를 기다리고, 타이머 인터럽트는 하드웨어가 강제로 운영체제를 부른다.
# 본문 근거: 이 노트 「3. 타이머 인터럽트로 통제권 되찾기」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 6장 §6.3 — 협력 방식은 시스템 콜(yield 포함)로 운영체제에 넘어오고, 비협력 방식은 부팅 때 시작시킨 타이머 장치가 주기적으로 인터럽트를 일으킨다.
# 타입 스펙: type-flowchart — 판단 분기. 마름모는 판단(출구 둘, 모든 출구에 라벨), 사각형은 결과. 코랄은 가장 중요한 경로(타이머)에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, KR, MONO

W, H = 880, 568
d = D(W, H, "OSTEP · 04-01 §3",
      "스스로 내놓지 않는 프로그램은 타이머 인터럽트가 끊는다",
      "프로그램이 실행 중일 때 스스로 CPU 를 내놓으면 yield 나 시스템 콜로 운영체제가 통제권을 얻는다. "
      "내놓지 않으면 부팅 때 시작시킨 타이머가 주기적으로 인터럽트를 일으켜 운영체제의 핸들러가 실행되고, 두 경로 모두 운영체제가 통제권을 되찾는 자리에서 합쳐진다.")

CX = 440
# 시작
d.box(CX - 110, 100, 220, 40, PAPER2, RULE, 1.0, 20)
d.t(CX, 125, "프로그램 실행 중", 13, INK, KR, "middle", 600)
d.arrow([(CX, 140), (CX, 186)], MUTED, "ar", 1.4)

# 판단 (마름모)
cy, hw, hh = 230, 150, 44
d.o.append(f'<polygon points="{CX},{cy-hh} {CX+hw},{cy} {CX},{cy+hh} {CX-hw},{cy}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.1"/>')
d.t(CX, cy - 2, "프로그램이 스스로", 12, INK, KR, "middle", 600)
d.t(CX, cy + 16, "CPU 를 내놓는가", 12, INK, KR, "middle", 600)

# 예 (왼쪽)
LXc, RXc = 180, 700
d.arrow([(CX - hw, cy), (LXc, cy), (LXc, 300)], INFO, "info", 1.4)
d.chip((CX - hw + LXc) / 2, cy, "예", INFO, 12, 8)
d.tone(LXc - 130, 300, 260, 64, INFO)
d.t(LXc, 326, "yield · 시스템 콜", 12, INK, KR, "middle", 600)
d.t(LXc, 348, "trap 으로 운영체제를 부름", 12, MUTED, KR)
d.t(50, 206, "협력 방식 — 프로그램을 믿는다", 12, MUTED, KR, "start", 600)

# 아니오 (오른쪽)
d.arrow([(CX + hw, cy), (RXc, cy), (RXc, 300)], ACC, "acc", 1.6)
d.chip((CX + hw + RXc) / 2, cy, "아니오", ACC, 12, 8)
d.tone(RXc - 130, 300, 260, 64, ACC)
d.t(RXc, 326, "타이머 인터럽트", 12, ACC, KR, "middle", 600)
d.t(RXc, 348, "부팅 때 시작시킨 장치가 강제", 12, MUTED, KR)
d.t(W - 50, 206, "비협력 방식 — 하드웨어가 강제한다", 12, MUTED, KR, "end", 600)

# 합류
d.arrow([(LXc, 364), (LXc, 456), (CX - 150, 456)], INFO, "info", 1.4)
d.arrow([(RXc, 364), (RXc, 456), (CX + 150, 456)], ACC, "acc", 1.6)
d.tone(CX - 150, 424, 300, 64, OK)
d.t(CX, 450, "운영체제가 통제권을 되찾음", 13, INK, KR, "middle", 600)
d.t(CX, 472, "스케줄러가 계속할지 바꿀지 고름", 12, MUTED, KR)

d.legend(H - 56, [("협력 방식", INFO), ("타이머 인터럽트", ACC), ("운영체제 쪽 결과", OK)])
d.save("04-01.control-regain.svg")
print("ok 04-01 control-regain")
