# 09-01 §4 — IOPS 하나로는 아무것도 비교할 수 없다.
# 타입 스펙: type-process — 같은 IOPS 숫자를 두고 조건이 갈리는 대조 지도.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 476
CW, CH, GAP, X0, Y = 424, 176, 32, 24, 132

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-01 §4",
       "IOPS 는 동등하지 않다",
       "회전 디스크에서 순차 5,000 IOPS 가 랜덤 1,000 IOPS 보다 훨씬 빠를 수 있다. 숫자가 크다고 빠른 것이 아니라 어떤 I/O 인지가 정한다.",
       "탐색과 회전을 기다리느냐가 자릿수를 가릅니다")

CARDS = [
    ("순차 5,000 IOPS", "다음 I/O 가 바로 뒤에 있음", OK,
     ["헤드를 옮길 필요가 없습니다.", "회전을 기다리지 않습니다.", "처리량이 크게 나옵니다"],
     "숫자는 크고 실제로도 빠릅니다"),
    ("랜덤 1,000 IOPS", "I/O 가 흩어져 있음", ACC,
     ["매번 탐색하고 회전을 기다립니다.", "7,200rpm 랜덤 읽기는 8ms 안팎.", "SSD 는 이 차이가 거의 없습니다"],
     "숫자는 작지만 더 어려운 일입니다"),
]
for i, (name, tag, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.tone(x, Y, CW, CH, c, 8)
    d.t(x + 16, Y + 30, name, 15, c, KR, "start", 600)
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    d.line(x + 16, Y + 66, x + CW - 16, Y + 66, RULE, 0.8)
    for j, l in enumerate(body):
        d.t(x + 16, Y + 92 + j * 20, l, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "IOPS 를 읽으려면 함께 봐야 할 것 — 랜덤/순차 · I/O 크기 · 읽기/쓰기 · 버퍼드/다이렉트 · 병렬 개수", 13, MUTED, KR, "start")
d.t(X0, YB + 24, "워크로드 성격도 갈립니다. 랜덤 요청은 지연에 민감하고, 스트리밍은 처리량에 민감해 큰 I/O 의 낮은 IOPS 가 낫습니다", 13, SOFT, KR, "start")

d.legend(YB + 48, [("어려운 쪽 — 탐색·회전을 문다", ACC), ("쉬운 쪽 — 연속으로 읽는다", OK)])
d.save("09-01.iops-not-equal.svg")
