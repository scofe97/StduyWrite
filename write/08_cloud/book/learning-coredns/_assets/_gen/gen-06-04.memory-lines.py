# 06-04 §2 「켜지 않는 이유가 둘」 — 두 모드의 메모리 선이 객체 수가 늘수록 벌어진다.
# 원문 근거: 25,000 파드·1,000 서비스에서 160 / 80 MiB, 50,000 파드·2,000 서비스에서 264 / 106 MiB(이 노트 §2 표).
# 선: insecure·disabled = 객체/1000 + 54 (앞 편 추정식), verified = 객체/250 + 56 (Scaling_CoreDNS.md 의 autopath 식).
#     두 식 모두 네 실측점을 정확히 지난다(26k→80·160, 52k→106·264). 면접 7번의 32k 점은 답을 미리 보여 주지 않으려 찍지 않는다.
# 타입 스펙: type-line — 연속 x(객체 수)에 대한 두 계열의 추이와 그 사이 간격이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, INFO, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 06-04 §2",
      "객체가 늘수록 두 모드의 메모리가 벌어진다",
      "가로축은 파드와 서비스를 더한 객체 수, 세로축은 CoreDNS 인스턴스 하나의 메모리다. 두 선 모두 원서의 실측점 둘을 지나고, "
      "verified 의 기울기가 네 배라서 클러스터가 커질수록 차이가 커진다.",
      "주황 괄호가 52,000 개에서 벌어진 차이입니다")

PX0, PX1, PY0, PY1 = 120, 820, 130, 400
XMAX, YMAX = 60, 300


def X(k):
    return PX0 + k * (PX1 - PX0) / XMAX


def Y(v):
    return PY1 - v * (PY1 - PY0) / YMAX


for g in (0, 100, 200, 300):
    d.line(PX0, Y(g), PX1, Y(g), RULE, 0.8)
    d.t(PX0 - 12, Y(g) + 4, str(g), 12, SOFT, MONO, "end")
d.t(PX0 - 12, Y(300) - 18, "MiB", 12, SOFT, MONO, "end")
for k in (0, 10, 20, 30, 40, 50, 60):
    d.t(X(k), PY1 + 20, f"{k}k", 12, SOFT, MONO)
d.t(PX1, PY1 + 40, "파드 + 서비스", 12, MUTED, KR, "end")

d.path(f"M {X(0)} {Y(54)} L {X(60)} {Y(60 + 54)}", INFO, 2.0)
d.path(f"M {X(0)} {Y(56)} L {X(60)} {Y(240 + 56)}", MUTED, 2.0)

for k, v, c in ((26, 80, INFO), (52, 106, INFO), (26, 160, INK), (52, 264, INK)):
    d.o.append(f'<circle cx="{X(k)}" cy="{Y(v)}" r="5" fill="{PAPER}" stroke="{c}" stroke-width="2"/>')
    # 바탕 마스크 없이 선이 지나지 않는 쪽에 둔다 — verified 는 오른쪽 아래, insecure 는 위(2026-10-03: 마스크가 선을 끊었다)
    if c == INK:
        d.t(X(k) + 12, Y(v) + 20, str(v), 12, c, MONO, "start", 600)
    else:
        d.t(X(k), Y(v) - 14, str(v), 12, c, MONO, "middle", 600)

bx = X(52) + 70
d.path(f"M {bx - 8} {Y(264)} L {bx} {Y(264)} L {bx} {Y(106)} L {bx - 8} {Y(106)}", ACC, 1.4)
d.t(bx + 10, (Y(264) + Y(106)) / 2 + 5, "158 차이", 13, ACC, KR, "start", 600)

d.t(X(34) - 8, Y(4 * 34 + 56) - 18, "verified · 1,000개당 4", 12, INK, KR, "end", 600)
d.t(X(34), Y(34 + 54) + 28, "insecure · disabled · 1,000개당 1", 12, INFO, KR, "middle", 600)

d.t(20, 462, "점 넷 · 원서 실측 · 선 · 그 점을 지나는 두 추정식", 13, MUTED, KR, "start")

d.legend(480, [("verified", MUTED), ("insecure · disabled", INFO), ("벌어진 차이", ACC)])
d.save("06-04.memory-lines.svg")
