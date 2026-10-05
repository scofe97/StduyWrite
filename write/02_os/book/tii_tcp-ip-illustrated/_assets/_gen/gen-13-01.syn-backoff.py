# 13-01 §6 — 응답 없는 상대에게 SYN 을 다시 보내는 시각: 책의 리눅스(2009) 대 커널 7.0.14 실측(2026-10-04).
# 책 값: 원서 Listing 13-1 — 0, 2.997928, 8.997962, 20.997942, 44.997936, 92.997937 초, 타임아웃 약 3.2분(21:16:34 → 21:19:43, 189초).
# 실측 값: OrbStack Ubuntu, tcp_syn_retries=6 · tcp_syn_linear_timeouts=4, nftables 로 input 단계에서 SYN 을 버리고 tcpdump -ttt 로 잼.
#   간격 1.063 · 1.013 · 1.022 · 1.023 · 1.026 · 2.048 · 4.032 · 8.513 · 16.383 · 32.257 초 → 누적 시각. connect() 실패까지 133.9초.
# 타입 스펙: type-line — 가로 축이 SYN 순번(1–11), 세로 축이 보낸 시각(초)인 꺾은선 두 계열. 포기 시각은 가로 점선으로 표시한다.
#           focal 계열은 현재 리눅스 실측(꼭짓점 점은 focal 에만). 비교 계열은 책 값.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

book = [0, 2.997928, 8.997962, 20.997942, 44.997936, 92.997937]
gaps = [1.062747, 1.012729, 1.022007, 1.023250, 1.025833, 2.047960, 4.031773, 8.512682, 16.382553, 32.256828]
now = [0.0]
for g in gaps: now.append(now[-1] + g)
BOOK_GIVEUP, NOW_GIVEUP = 189.0, 133.9

W, H = 920, 588
PX0, PX1, PY0, PY1 = 96, 872, 132, 452       # 플롯 영역
TMAX = 220.0
def x(i): return PX0 + (i - 1) * (PX1 - PX0) / 10            # SYN 순번 1..11
def y(t): return PY1 - t * (PY1 - PY0) / TMAX

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §6",
      "응답 없는 상대에게 SYN 을 다시 보내는 시각",
      "가로 축은 몇 번째 SYN 인지, 세로 축은 첫 SYN 뒤 몇 초에 나갔는지다. 책의 리눅스(2009)는 3초에서 시작해 간격을 매번 두 배로 늘려 SYN 6개를 보내고 약 189초에 포기했다. "
      "커널 7.0.14 실측은 1초 간격으로 다섯 번 보낸 뒤에야 두 배로 늘려 SYN 11개를 보내고 약 134초에 포기했다.",
      "지금의 리눅스는 처음에 더 자주 묻고, 더 일찍 포기합니다")

# 격자와 축
for t in range(0, 201, 50):
    d.line(PX0, y(t), PX1, y(t), RULE, 0.6)
    d.t(PX0 - 12, y(t) + 4, f"{t}s", 11, SOFT, MONO, "end")
for i in range(1, 12):
    d.t(x(i), PY1 + 22, str(i), 11, SOFT, MONO)
d.t((PX0 + PX1) / 2, PY1 + 44, "몇 번째 SYN", 12, MUTED, KR)

# 포기 시각
for t, lab, c in ((BOOK_GIVEUP, "책 · 약 189초에 포기", MUTED), (NOW_GIVEUP, "실측 · 133.9초에 포기", ACC)):
    d.line(PX0, y(t), PX1, y(t), c, 1.0, "5 4")
    d.t(PX1 - 4, y(t) - 8, lab, 12, c, KR, "end", 600)

# 계열
pts_b = " ".join(f"{x(i + 1):.1f},{y(t):.1f}" for i, t in enumerate(book))
d.o.append(f'<polyline points="{pts_b}" fill="none" stroke="{INFO}" stroke-width="1.4" stroke-linejoin="round"/>')
for i, t in enumerate(book):
    d.o.append(f'<circle cx="{x(i + 1):.1f}" cy="{y(t):.1f}" r="3" fill="{PAPER}" stroke="{INFO}" stroke-width="1.2"/>')
pts_n = " ".join(f"{x(i + 1):.1f},{y(t):.1f}" for i, t in enumerate(now))
d.o.append(f'<polyline points="{pts_n}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for i, t in enumerate(now):
    d.o.append(f'<circle cx="{x(i + 1):.1f}" cy="{y(t):.1f}" r="4" fill="{ACC}"/>')

# 끝점 값
d.t(x(6) + 10, y(book[-1]) + 4, "93.0s", 11, INFO, MONO, "start", 600)
d.t(x(11) - 10, y(now[-1]) - 10, "68.4s", 11, ACC, MONO, "end", 600)
d.t(x(3), y(now[5]) - 22, "1초 간격 다섯 번", 12, ACC, KR, "middle", 600)

d.legend(H - 56, [("커널 7.0.14 실측 · SYN 11개", ACC), ("책의 리눅스 · SYN 6개", INFO)])
d.save("13-01.syn-backoff.svg")
