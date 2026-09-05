# 08-01 §1 — 느린 앱의 원인을 좁히는 절차. 한 번에 한 자원만 바꾼다.
# 원문("Observability Strategy"): "One widely established strategy in the observability context is the
#       OODA loop (observe-orient-decide-act)." · "let's say an application is slow. Let's further assume
#       there are multiple possible reasons for this (not enough memory, too few CPU cycles, network I/O
#       insufficient, etc.). First, you want to be able to measure each resource consumption. Then you
#       would change each resource allocation individually (keeping the others unchanged) and measure the
#       outcome." · "Does the performance improve after you provided more RAM to the app? If so, you may
#       have found the reason. If not, you continue with a different resource, always measuring the
#       consumption and trying to relate to the observed impact on the situation."
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모 하나에서 예·아니오가 갈리고
#           아니오 쪽이 앞 단계로 되돌아간다. 축약: OODA 네 국면 이름은 본문 표가 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 700
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §1",
      "한 번에 하나만 바꿔야 무엇이 들었는지 알 수 있다",
      "저자가 느린 앱을 예로 들어 적은 절차를 판단 논리로 세운 것. 되돌아가는 화살표가 있는 한 "
      "이것은 한 번 훑고 끝나는 점검표가 아니라 후보가 떨어질 때까지 도는 고리다.",
      "둘을 같이 바꾸면 좋아져도 어느 쪽 덕인지 모릅니다")

BX, BW, BH, STRIDE, Y0 = 232, 400, 56, 78, 112
steps = [
    ("앱이 느리다", "증상이지 원인이 아니다", MUTED),
    ("자원마다 소비량을 잰다", "CPU · 메모리 · 디스크 I/O · 네트워크", MUTED),
    ("자원 하나만 바꾼다", "나머지는 그대로 둔다", ACC),
    ("다시 잰다", "바꾼 뒤의 값을 같은 방법으로", MUTED),
]
for i, (name, note, col) in enumerate(steps):
    y = Y0 + i * STRIDE
    if col is ACC:
        d.tone(BX, y, BW, BH, ACC, 6, "12", 1.4)
    else:
        d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(BX + 20, y + 24, name, 14, col if col is ACC else INK, KR, "start", 600)
    d.t(BX + 20, y + 44, note, 11.5, MUTED, KR, "start")
    if i < len(steps) - 1:
        d.arrow([(BX + BW / 2, y + BH), (BX + BW / 2, y + STRIDE - 2)], MUTED, "ar", 1.3)

DY = Y0 + len(steps) * STRIDE
d.o.append(f'<rect x="{BX}" y="{DY}" width="{BW}" height="{BH}" rx="6" '
           f'fill="{PAPER}" stroke="{WARN}" stroke-width="1.4"/>')
d.t(BX + BW / 2, DY + 26, "좋아졌나?", 15, WARN, KR, "middle", 600)
d.t(BX + BW / 2, DY + 45, "바꾸기 전 값과 견준다", 11.5, MUTED, KR)
d.arrow([(BX + BW / 2, DY - STRIDE + BH), (BX + BW / 2, DY - 2)], MUTED, "ar", 1.3)

YY = DY + BH + 44
d.tone(BX, YY, BW, 52, OK, 6, "12", 1.3)
d.t(BX + BW / 2, YY + 22, "원인 후보를 찾았다", 14, OK, KR, "middle", 600)
d.t(BX + BW / 2, YY + 40, "저자는 확정이 아니라 후보라고 적는다", 11.5, MUTED, KR)
d.path(f"M {BX + BW / 2} {DY + BH} L {BX + BW / 2} {YY - 2}", OK, 1.3, m="ok")
d.chip(BX + BW / 2 + 34, DY + BH + 20, "예", OK)

RX = BX + BW + 40
d.path(f"M {BX + BW} {DY + BH / 2} L {RX} {DY + BH / 2} L {RX} {Y0 + 2 * STRIDE + BH / 2} "
       f"L {BX + BW + 4} {Y0 + 2 * STRIDE + BH / 2}", WARN, 1.3, m="warn", dash="5 5")
d.chip(RX + 44, DY + BH / 2, "아니오", WARN)
d.t(RX + 16, Y0 + 2 * STRIDE + BH / 2 - 24, "다음 자원으로", 12, WARN, KR, "start", 600)

NY = YY + 52 + 26
d.t(24, NY + 4, "저자는 이것을 OODA 고리라고 부릅니다 — 관찰하고, 방향을 잡고, 정하고, 행동합니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 26, "고리인 이유는 마지막 행동이 다음 관찰의 입력이 되기 때문입니다. 한 바퀴로 끝나지 않습니다.",
    12, SOFT, KR, "start")

d.legend(656, [("한 번에 하나만 바꾸는 자리", ACC), ("판정", WARN), ("멈추는 자리", OK),
                  ("절차의 나머지", MUTED)])
d.save("08-01.resource-ablation.svg")
print("ok 08-01.resource-ablation")
