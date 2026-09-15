# 03-05 §3 Vegas — 안 막힌 처리량 cwnd/RTTmin 과 실제 처리량의 차이로 큐 형성을 손실 전에 알아챈다.
# 본문 근거(§3 「Vegas — 지연을 신호로」): RTTmin 은 큐잉 지연이 최소일 때의 RTT · 안 막힌 처리량은 cwnd/RTTmin ·
#   실제가 그에 가까우면 올리고, 뚜렷이 낮으면 큐가 쌓인 것이므로 내린다. 곡선 모양은 이 논리를 그린 개략이다.
# 타입 스펙: type-line — cwnd 에 대한 처리량 두 계열. 차이가 곧 신호.
import sys; sys.path.insert(0, ".")
from _cc_common import Chart
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §3",
      "Vegas — 기대와 실제의 차이가 곧 큐입니다",
      "cwnd 를 올리면 안 막힌 경로에서는 처리량이 cwnd/RTTmin 로 따라 오른다. 실제 처리량이 그 직선에서 떨어지기 시작하는 자리가 큐가 쌓이기 시작한 자리이고, Vegas 는 손실이 나기 전에 거기서 물러선다.",
      "가로축은 혼잡 창, 세로축은 처리량입니다. 두 선의 벌어짐이 큐에 쌓인 양입니다")

c = Chart(d, 24, 110, 952, 380, "혼잡 창 cwnd", "처리량", [(0, "0"), (0.5, ""), (1, "")], [(0, "0"), (0.62, "병목 대역폭"), (1, "")])
xs = [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]
c.series([(x, x * 0.95) for x in xs], INFO, dash="5 4")                                    # 기대 = cwnd/RTTmin
act = [(0, 0), (0.15, 0.142), (0.3, 0.285), (0.45, 0.42), (0.6, 0.54), (0.75, 0.60), (0.9, 0.62), (1.0, 0.62)]
c.series(act, ACC, focal=True)
# 차이 영역 — 큐
poly = " ".join(f"{c.px(x):.1f},{c.py(x * 0.95):.1f}" for x in xs[4:]) + " " + " ".join(f"{c.px(x):.1f},{c.py(y):.1f}" for x, y in reversed(act[4:]))
d.o.append(f'<polygon points="{poly}" fill="{WARN}" opacity="0.14"/>')
d.line(c.px(0.6), c.T, c.px(0.6), c.B, WARN, 0.8, "3 4")
c.note(0.04, 0.84, "기대 처리량 = cwnd / RTTmin", INFO, "start")
c.note(0.04, 0.78, "RTTmin 은 안 막혔을 때의 왕복 시간", MUTED, "start")
c.note(0.30, 0.55, "실제가 기대에 가깝다 → 올림", ACC, "start")
c.note(0.63, 0.92, "여기서부터 벌어짐", WARN, "start")
c.note(0.63, 0.86, "실제가 뚜렷이 낮다 → 큐가 쌓이는 중 → 내림", WARN, "start")
c.note(0.98, 0.68, "손실은 아직 안 났음", MUTED, "end")

d.legend(H - 44, [("실제로 잰 처리량", ACC), ("안 막혔을 때의 기대치", INFO), ("차이 — 큐에 쌓인 양", WARN)])
d.save("03-05.vegas-gap.svg")
print("ok vegas-gap")
