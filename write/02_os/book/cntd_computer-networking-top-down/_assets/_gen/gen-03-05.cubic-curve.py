# 03-05 §3 CUBIC — 손실 뒤 창이 Wmax 를 향해 세제곱 곡선으로 돌아온다. 본문 근거(§3 「CUBIC — 가산 증가를 고칩니다」):
#   t 가 K 에서 멀면 증가폭이 크고, K 에 가까우면 작고, K 를 넘으면 다시 커진다. Reno 는 반으로 자르고 왕복마다 1 MSS 씩 올린다.
#   곡선은 W(t) = Wmax + C·(t − K)³ 의 모양이며 눈금은 두지 않는다 — 원문 Figure 3.54 처럼 값이 아니라 모양이 요점이다.
# 타입 스펙: type-line — 시간에 따른 cwnd 곡선. 초점 계열(CUBIC)에만 점, Reno 는 대조용 점선.
import sys; sys.path.insert(0, ".")
from _cc_common import Chart
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §3",
      "CUBIC — 손실 직전까지는 빨리, 그 근처에서는 천천히",
      "원문 Figure 3.54 의 모양. 손실 뒤 창은 Wmax 를 향해 세제곱 곡선으로 돌아오고, K 근처에서 평평해졌다가 K 를 넘으면 다시 빨리 는다. Reno 의 직선과 대조.",
      "가로축은 손실 뒤 흐른 시간, 세로축은 혼잡 창입니다. 눈금은 원문처럼 두지 않았습니다")

K, WMAX, C0 = 1.0, 0.72, 0.36          # 정규화 좌표. W(0) = Wmax − C·K³ = 0.36, 손실 때 절반
def w(t): return WMAX + C0 * (t - K) ** 3
c = Chart(d, 24, 110, 952, 380, "손실 뒤 흐른 시간 t", "혼잡 창 cwnd", [(0, "손실"), (K / 1.8, "K"), (1, "")], [(0, ""), (WMAX, "Wmax"), (1, "")])
ts = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
c.series([(t / 1.8, w(t)) for t in ts], ACC, focal=True)
c.series([(t / 1.8, 0.36 + 0.10 * t) for t in ts], MUTED, dash="5 4")           # Reno 대조 — 왕복마다 1 MSS
d.line(c.px(K / 1.8), c.T, c.px(K / 1.8), c.B, WARN, 0.8, "3 4")
c.note(0.04, 0.95, "K 에서 멀다 — 증가폭이 큼", ACC, "start")
c.note(0.04, 0.89, "손실 직전 값으로 빠르게 돌아감", MUTED, "start")
c.note(0.36, 0.60, "K 근처 — 증가폭이 작음", ACC, "start")
c.note(0.36, 0.54, "Wmax 근처에서 조심스럽게 더듬음", MUTED, "start")
c.note(0.66, 0.97, "K 를 넘으면 다시 빨리", ACC, "start")
c.note(0.66, 0.91, "혼잡 수준이 달라졌다면 새 지점을 찾음", MUTED, "start")
c.note(0.98, 0.42, "Reno — 반으로 자르고 왕복마다 1 MSS", MUTED, "end")

d.legend(H - 44, [("CUBIC — W(t) = Wmax + C·(t − K)³", ACC), ("Reno — 가산 증가", MUTED), ("K — 손실 없이 Wmax 에 닿을 시점", WARN)])
d.save("03-05.cubic-curve.svg")
print("ok cubic-curve")
