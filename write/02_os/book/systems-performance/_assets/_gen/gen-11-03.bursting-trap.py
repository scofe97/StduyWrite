# 11-03 §4 — shares 로 얻은 성능은 이웃이 없을 때만의 성능이다.
# 타입 스펙: type-process — 같은 컨테이너가 시간에 따라 겪는 세 국면의 단계 지도다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 480
CW, CH, GAP, X0, Y = 280, 164, 32, 40, 132

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-03 §4",
       "bursting 의 함정",
       "shares 는 유휴 CPU 를 빌려 쓰게 해 준다. 문제는 사용자가 그 빌린 성능을 자기 몫으로 착각한다는 데 있다.",
       "shares 가 보장하는 것은 최소치이지, 테스트에서 본 그 성능이 아닙니다")

STEPS = [
    ("01", "혼자 쓸 때", OK, ["idle 시스템에서 테스트합니다.", "유휴 CPU 를 다 빌려", "100% 를 얻습니다"], "여기서 만족합니다"),
    ("02", "이웃이 들어옴", WARN, ["다른 컨테이너가 배치됩니다.", "빌려 쓰던 CPU 가", "제 주인에게 돌아갑니다"], "성능이 내려갑니다"),
    ("03", "최소치만 남음", ACC, ["shares 가 보장하는 몫,", "예를 들어 10% 만 남습니다.", "10배 느려진 셈입니다"], "사용자는 장애로 오해합니다"),
]

for i, (n, name, c, body, foot) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" fill="{c}" stroke="{c}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER, MONO)
    d.t(x + 48, Y + 29, name, 14, c, KR, "start", 600)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 62 + j * 20, line, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")
    if i < 2:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 8, Y + CH / 2)], MUTED, "ar", 1.3)

YB = Y + CH + 44
d.t(X0, YB, "bandwidth 로 bursting 을 미리 제한해 두면(예: 10~20% 범위) 이 급락이 덜 심합니다", 13, INFO, KR, "start")
d.t(X0, YB + 24, "모니터링이 bursting 통계를 보여 주지 않으면 사용자는 잘못된 기대를 갖게 됩니다", 13, MUTED, KR, "start")

d.legend(YB + 48, [("사용자가 오해하는 지점", ACC), ("빌려 쓰던 국면", OK), ("반환이 시작되는 국면", WARN), ("완화책", INFO)])
d.save("11-03.bursting-trap.svg")
