# 11-01 §3 — 자동 스케일링은 부하와 사고를 구분하지 못한다.
# 타입 스펙: type-process — 같은 입력(인스턴스 증가)에 대해 원인이 셋으로 갈리는 판별 지도다.
#           축약: 주체(lane)가 없는 분기 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 436
CW, CH, GAP, X0, Y = 280, 140, 24, 24, 148

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-01 §3",
       "인스턴스가 늘었다 — 셋 중 무엇인가",
       "자동 스케일링은 부하가 늘면 인스턴스를 늘린다. 그런데 늘어난 이유가 진짜 수요인지 공격인지 회귀인지는 구분하지 못한다.",
       "그래서 증가가 타당한지는 모니터링이 따로 판정해야 합니다")

d.t(X0, Y - 32, "인스턴스 증가", 14, INK, KR, "start", 600)
d.t(X0 + 116, Y - 32, "→  원인 후보 셋", 13, MUTED, KR, "start")

CARDS = [
    ("정상 수요", OK, ["실제 사용자 증가", "늘린 만큼의 값어치"], "조치 불필요"),
    ("DoS 공격", ACC, ["부하처럼 보이는 공격 트래픽", "공격에 반응한 인스턴스 증가"], "비용 누수"),
    ("성능 회귀", WARN, ["같은 부하 · 더 많은 인스턴스", "느려진 코드"], "원인 — 배포"),
]

for i, (name, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 14, c, KR, "start", 600)
    d.line(x + 16, Y + 44, x + CW - 16, Y + 44, RULE, 0.8)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 70 + j * 20, line, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 20, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "bursting (OS 가상화) — 유휴 CPU 즉시 대여 · 부하 지속 여부 확인 시간 확보", 13, INFO, KR, "start")
d.t(X0, YB + 24, "Netflix — 일일 streams-per-second 패턴 · 매일 수만 인스턴스 증감", 13, MUTED, KR, "start")

d.legend(YB + 48, [("과잉 프로비저닝을 부르는 원인", ACC), ("정상", OK), ("코드에 원인이 있는 경우", WARN), ("완충 장치", INFO)])
d.save("11-01.autoscaling-trap.svg")
