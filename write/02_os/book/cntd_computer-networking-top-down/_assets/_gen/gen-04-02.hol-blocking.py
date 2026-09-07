# 04-02 §1 — 원문 Figure 4.8 의 HOL 블로킹. 두 입력 큐의 맨 앞 패킷이 같은 출력으로 가면 하나가 막힌다.
# 막힌 큐의 두 번째 패킷이 자기 출력이 비어 있는데도 함께 기다리는 것이 이 그림의 요점이고, 원문의 서술 그대로다.
# 타입 스펙: type-swimlane — 행마다 한 주체, 레인을 건너는 화살표가 인계다. 막히는 인계에 강조색.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 588
LX, LR = 176, 960
LANES = [("입력 큐 1", "위쪽 입력 포트", 132), ("입력 큐 2", "아래쪽 입력 포트", 268)]
LH = 124
PW, PH = 96, 46

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §1",
      "자기 출구가 비어 있는데도 못 나갑니다",
      "원문 Figure 4.8. 두 입력 큐의 맨 앞이 같은 출력을 노려 하나가 막히고, 그 뒤에 선 패킷까지 함께 멈춘다.",
      "막힌 것은 앞 패킷인데 손해를 보는 것은 뒤 패킷입니다")

for name, sub, y in LANES:
    d.line(LX, y, LR, y, RULE, 0.8)
    d.t(12, y + 54, name, 12, INK, KR, "start", 600)
    d.t(12, y + 74, sub, 11, SOFT, KR, "start")
d.line(LX, LANES[-1][2] + LH, LR, LANES[-1][2] + LH, RULE, 0.8)

def pkt(cx, cy, lab, dst, c=MUTED, focal=False):
    if focal: d.tone(cx - PW / 2, cy - PH / 2, PW, PH, c, 5, "14", 1.4)
    else: d.box(cx - PW / 2, cy - PH / 2, PW, PH, PAPER2, c, 1.0, 5)
    d.t(cx, cy - 4, lab, 11, c if focal else INK, MONO, "middle", 600)
    d.t(cx, cy + 14, dst, 11, SOFT, KR)

Y1, Y2 = LANES[0][2] + LH / 2, LANES[1][2] + LH / 2
pkt(300, Y1, "A1", "→ 출력 1", OK, True)
pkt(206, Y1, "A2", "→ 출력 2")
pkt(300, Y2, "B1", "→ 출력 1", WARN, True)
pkt(206, Y2, "B2", "→ 출력 2", ACC, True)

OX, OY = 760, [Y1, Y2]
for i, y in enumerate(OY):
    c = OK if i == 0 else MUTED
    d.box(OX - 80, y - 30, 160, 60, PAPER2, c, 1.2, 6)
    d.t(OX, y - 4, f"출력 포트 {i+1}", 12, c, KR, "middle", 600)
    d.t(OX, y + 16, "비어 있음" if i else "이번에 A1 을 받음", 11, SOFT, KR)

d.path(f"M {300 + PW/2 + 6} {Y1} L {OX - 86} {Y1}", OK, 1.5, m="ok")
d.t((300 + OX) / 2, Y1 - 14, "건넙니다", 11, OK, KR)

d.path(f"M {300 + PW/2 + 6} {Y2} L {480} {Y2} L {480} {Y1 + 34}", WARN, 1.5, m="warn", dash="5 4")
d.t(500, Y2 - 14, "같은 출력을 노려 막힙니다", 11, WARN, KR, "start")

d.path(f"M {206} {Y2 + PH/2 + 4} L {206} {Y2 + 54} L {OX - 86} {Y2 + 54} L {OX - 86} {Y2 + 24}",
       ACC, 1.5, m="acc", dash="4 4")
d.t(300, Y2 + 68, "출력 2 는 비어 있는데도 B2 가 함께 기다립니다", 11, ACC, KR, "start")

d.t(24, 452, "이것이 HOL 블로킹입니다. 줄 맨 앞이 막히면 뒤에 선 것도 자기 길이 열려 있는지와 무관하게 멈춥니다.",
     11, MUTED, KR, "start")
d.t(24, 474, "도착률이 용량의 58%에 이르면 입력 큐가 무한히 길어집니다. 이 값의 닫힌 형태는 2 − √2 = 0.5858 입니다.",
     11, MUTED, KR, "start")
d.t(24, 496, "절반을 조금 넘긴 자리에서 무너지므로, 입력 큐잉 방식은 링크를 절반 남짓밖에 못 씁니다.",
     11, SOFT, KR, "start")

d.legend(H - 44, [("자기 길이 열렸는데 막힌 패킷", ACC), ("경쟁에서 진 패킷", WARN), ("건너간 패킷", OK)])
d.save("04-02.hol-blocking.svg")
