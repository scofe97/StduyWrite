# 03-05 §2 — 원문 Figure 3.51 의 톱니와 Figure 3.52 의 Reno·CUBIC 대비를 한 장에 합친 것.
# 곡선은 *질적* 그림이다. 원문도 이 두 그림에 축 눈금을 두지 않는다 — 값이 아니라 모양이 요점이다.
#   Reno  : 손실 때 절반으로 떨어진 뒤 왕복마다 1 MSS 씩 선형 증가 (원문 3.7.1)
#   CUBIC : 손실 때 덜 떨어진 뒤 Wmax 까지 세제곱으로 빠르게 올라가고 그 근처에서 완만해짐 (원문 3.7.2)
# 두 곡선의 증가율은 이 대비가 보이도록 고른 값이고, 축에 눈금이 없는 것도 그래서다.
# 타입 스펙: type-line — 연속 지표 위의 추세. 꺾은선으로 그리고 초점 계열에만 꼭짓점을 찍는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 608
PX0, PX1, PY0, PY1 = 130, 900, 140, 392
LOSSES = [0.30, 0.58, 0.86]
YMAX = 1.15

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §2",
      "톱니와 세제곱 곡선",
      "손실 때마다 창을 줄이고 다시 올리는 모양. Reno 는 선형으로 올라가고 CUBIC 은 손실 직전 값 근처까지 빠르게 올라간다.",
      "축에 눈금을 두지 않은 것은 원문과 같습니다 — 값이 아니라 모양이 요점입니다")

def xp(u): return PX0 + u * (PX1 - PX0)
def yp(v): return PY1 - min(v, YMAX) / YMAX * (PY1 - PY0)

def series(kind):
    pts, u, cw = [], 0.0, 0.06
    step, ssthresh, phase, li = 0.006, 0.55, "ss", 0
    seg = (0.0, 0.0, 1.0, 1.0)
    while u <= 1.02:
        pts.append((u, cw))
        if li < len(LOSSES) and u >= LOSSES[li]:
            wmax = cw
            cw *= 0.5 if kind == "reno" else 0.7
            pts.append((u, cw))
            li += 1
            nxt = LOSSES[li] if li < len(LOSSES) else 1.04
            seg, phase = (u, cw, wmax, nxt - u), "ca"
        elif phase == "ss":
            cw *= 1.16
            if cw >= ssthresh: cw, phase = ssthresh, "ca0"
        elif phase == "ca0":
            cw += 0.013
        elif kind == "reno":
            cw += 0.0075
        else:
            s0, base, target, span = seg
            f = min((u - s0) / span, 1.0)
            cw = base + (target - base) * (1 - (1 - f) ** 3)
        u += step
    return pts

d.line(PX0, yp(1.0), PX1, yp(1.0), RULE, 0.9, "5 4")
d.t(PX1 + 6, yp(1.0) + 4, "Wmax", 11, SOFT, MONO, "start")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.t(PX0 - 12, PY0 - 16, "혼잡 창 cwnd", 11, SOFT, KR, "end")

for i, u in enumerate(LOSSES):
    d.line(xp(u), PY0, xp(u), PY1, RULE, 0.8, "3 4")
    d.t(xp(u), PY1 + 24, f"손실 {i+1}", 11, SOFT, KR)
d.t((PX0 + PX1) / 2, PY1 + 48, "시간 — 왕복 횟수", 11, SOFT, KR)

for kind, c, wd in (("reno", INFO, 1.5), ("cubic", ACC, 1.9)):
    p = series(kind)
    d.o.append('<polyline points="' + " ".join(f"{xp(u):.1f},{yp(v):.1f}" for u, v in p)
               + f'" fill="none" stroke="{c}" stroke-width="{wd}" stroke-linejoin="round"/>')

d.t(xp(0.115), yp(0.22), "느린 시작 — 왕복마다 두 배", 11, SOFT, KR, "start")
d.t(xp(0.63), yp(0.30), "Reno — 왕복마다 1 MSS", 11, INFO, KR, "start")
d.t(xp(0.335), yp(1.09), "CUBIC — Wmax 까지 빠르게, 근처에서 완만하게", 11, ACC, KR, "start")

d.t(20, 486, "AIMD — 왕복마다 1 MSS 를 더하고(가산 증가) 손실 때 절반으로 나눕니다(승산 감소). 이 규칙이 톱니를 만듭니다.",
     11, MUTED, KR, "start")
d.t(20, 508, "평균 처리량은 0.75 · W / RTT 입니다. 분모에 RTT 가 있어서 왕복이 짧은 연결이 같은 병목에서 더 많이 가져갑니다.",
     11, MUTED, KR, "start")

d.legend(H - 52, [("CUBIC", ACC), ("Reno", INFO)])
d.save("03-05.reno-vs-cubic.svg")
