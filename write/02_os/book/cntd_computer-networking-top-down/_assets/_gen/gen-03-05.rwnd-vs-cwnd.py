# 03-05 §1 — rwnd 와 cwnd 를 한 시간축에 놓으면 병목이 번갈아 바뀐다. 실제 한도는 매 순간 둘 중 작은 쪽이다.
# 노트의 읽기: 2026-09-08 회차에서 학습자가 "03-04 가 rwnd 를, 03-05 가 cwnd 를 따로 다루는데 둘이 한 그림에
#       놓인 자리가 없다" 고 지목해 추가한 도식. 원문 3.7 은 식 LastByteSent − LastByteAcked ≤ min{cwnd, rwnd} 만 준다.
#   RFC 5681 §2: "At any given time, a TCP MUST NOT send data with a sequence number higher than the sum of the
#       highest acknowledged sequence number and the minimum of cwnd and rwnd." (03-04 [^rfc5681-min] 과 같은 문장)
#   원문 3.5.5: rwnd = RcvBuffer − [LastByteRcvd − LastByteRead] — 받는 쪽 앱이 안 읽으면 줄어든다.
#   원문 3.7.1: 느린 시작은 왕복마다 두 배, 혼잡 회피는 왕복마다 1 MSS, 중복 ACK 손실 때 절반.
# 타입 스펙: type-line — 연속 지표 위의 추세. 꺾은선으로 그리고 초점 계열(min)에만 꼭짓점을 찍는다.
#       값은 질적이다. 왕복 11개(0~10)에 톱니 한 주기와 상대의 멈춤 한 번을 담았고, 눈금은 MSS 단위로만 뜻이 있다.
#       cwnd 는 손실 뒤 8 에서 왕복마다 1 씩 오르고, rwnd 는 상대 앱이 읽기를 멈춘 세 왕복 동안 6·3·3 으로 떨어진다.
#       초점은 min 한 줄뿐이고, 어느 창이 한도인지는 배경 띠로 갈랐다 — 같은 편 §2 의 type-line(reno-vs-cubic) 은
#       한 계열의 모양이 요점이고 이 도식은 두 계열 중 작은 쪽이 요점이라 띠가 필요했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 612
PX0, PX1, PY0, PY1 = 120, 900, 140, 400
T = list(range(11))
CWND = [1, 2, 4, 8, 16, 8, 9, 10, 11, 12, 13]
RWND = [12, 12, 12, 12, 12, 12, 12, 6, 3, 3, 8]
MN = [min(a, b) for a, b in zip(CWND, RWND)]
YMAX = 20

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §1",
      "두 창 중 작은 쪽이 그때그때 병목입니다",
      "rwnd 는 받는 쪽이 알려 주는 창이고 cwnd 는 보내는 쪽이 추측하는 창이다. "
      "실제 전송 한도는 매 순간 둘 중 작은 쪽이며, 어느 쪽이 작은지는 시간에 따라 바뀐다.",
      "실제 한도는 둘 중 작은 쪽이고, 그 쪽은 시간에 따라 바뀝니다")

def xp(t): return PX0 + t * (PX1 - PX0) / 10
def yp(v): return PY1 - v / YMAX * (PY1 - PY0)

# ── 배경 띠: 어느 창이 한도인가. 이웃한 같은 판정을 하나로 합친다 ──
runs, cur = [], None
for t in T:
    who = "망" if CWND[t] < RWND[t] else "상대"
    if cur and cur[0] == who: cur[2] = t
    else: cur = [who, t, t]; runs.append(cur)
for who, a, b in runs:
    x0, x1 = xp(max(a - 0.5, 0)), xp(min(b + 0.5, 10))
    c = INFO if who == "망" else OK
    d.o.append(f'<rect x="{x0:.1f}" y="{PY0}" width="{x1 - x0:.1f}" height="{PY1 - PY0}" fill="{c}" opacity="0.07"/>')
    d.t((x0 + x1) / 2, PY0 - 12, "망이 한도" if who == "망" else "상대가 한도", 11, c, KR)

# ── 축과 눈금 ──
for v in (0, 5, 10, 15, 20):
    d.line(PX0, yp(v), PX1, yp(v), MUTED if v == 0 else "rgba(245,245,245,0.10)", 1.0 if v == 0 else 0.8)
    d.t(PX0 - 10, yp(v) + 4, "20 MSS" if v == 20 else str(v), 11, SOFT, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
for t in T:
    d.t(xp(t), PY1 + 20, str(t), 11, SOFT, MONO)
d.t((PX0 + PX1) / 2, PY1 + 44, "시간 — 왕복 횟수", 11, SOFT, KR)
d.t(PX0 - 12, PY0 - 16, "창 크기", 11, SOFT, KR, "end")

# ── 사건 표시 ──
for u, lab, an in ((4.5, "손실 · cwnd 절반", "start"), (6.5, "상대 앱이 읽기를 멈춤", "start"), (9.5, "다시 읽음", "end")):
    d.line(xp(u), PY0, xp(u), PY1, RULE, 0.9, "3 4")
    d.t(xp(u) + (6 if an == "start" else -6), PY0 + 16, lab, 11, MUTED, KR, an)

# ── 계열: cwnd·rwnd 는 가는 선, min 은 초점(굵은 선 + 꼭짓점) ──
def poly(vals, c, wd):
    d.o.append('<polyline points="' + " ".join(f"{xp(t):.1f},{yp(v):.1f}" for t, v in zip(T, vals))
               + f'" fill="none" stroke="{c}" stroke-width="{wd}" stroke-linejoin="round"/>')
poly(CWND, INFO, 1.3)
poly(RWND, OK, 1.3)
poly(MN, ACC, 2.2)
for t, v in zip(T, MN):
    d.o.append(f'<circle cx="{xp(t):.1f}" cy="{yp(v):.1f}" r="4" fill="{ACC}"/>')
d.t(PX1 + 8, yp(13) + 4, "cwnd", 11, INFO, MONO, "start")
d.t(PX1 + 8, yp(8) + 4, "rwnd", 11, OK, MONO, "start")
d.t(xp(8.5), yp(3) + 18, "min{cwnd, rwnd}", 11, ACC, MONO)

d.t(20, 486, "rwnd 는 받는 쪽이 헤더에 적어 보낸 숫자라 그쪽 앱이 읽기를 멈추면 뚝 떨어지고, cwnd 는 보내는 쪽이 혼자 올리고 중복 ACK 손실 때 반으로 접습니다.",
    11, MUTED, KR, "start")
d.t(20, 508, "보내는 쪽은 매 순간 둘 중 작은 값까지만 내보냅니다. 값은 질적이고, 눈금은 MSS 단위로만 뜻이 있습니다.",
    11, MUTED, KR, "start")
d.legend(H - 52, [("실제 한도 = min", ACC), ("cwnd — 보내는 쪽의 추측", INFO), ("rwnd — 받는 쪽이 알려 줌", OK)])
d.save("03-05.rwnd-vs-cwnd.svg")
print("ok 03-05.rwnd-vs-cwnd")
