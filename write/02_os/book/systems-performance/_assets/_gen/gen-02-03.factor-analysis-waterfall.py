# 02-03 §4 — 최대 구성에서 두 요인을 뺐을 때 남는 처리량.
# 타입 스펙: type-waterfall — 시작 총량이 부호 있는 감소를 차례로 거쳐 끝 총량이 된다.
#           원서 p.58: 최대 2GB/s, 프로세서 둘 −30%, 네트워크 카드 하나 −25%, 요구 1GB/s.
#           계산: 2.0 × 0.7 = 1.40, 1.40 × 0.75 = 1.05. 원서 본문 표기는 1.04 — 두 값을 함께 적는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 928, 500
X0, Y0, PW, PH = 96, 120, 736, 272
YMAX = 2.4
COLW, BARW = 184, 112

def py(v): return Y0 + PH - PH * v / YMAX

STEPS = [("최대 구성", 0.0, 2.0, "total", "2.00"),
         ("프로세서 둘로", 2.0, 1.4, "drop", "−30% · −0.60"),
         ("네트워크 카드 하나로", 1.4, 1.05, "drop", "−25% · −0.35"),
         ("남는 처리량", 0.0, 1.05, "end", "1.05")]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §4",
       "두 요인을 빼도 1GB/s 위에 남는다",
       "최대 구성 2GB/s 에서 프로세서를 둘로, 네트워크 카드를 하나로 줄인 하락을 차례로 곱했다. 끝 막대가 요구 1GB/s 선 위에 남는다.",
       "원서 p.58 요인 분석 예 · 단위 GB/s")

for v in (0, 1.0, 2.0):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, f"{v:.1f}", 12, SOFT, MONO, "end")
d.line(X0, py(1.0), X0 + PW, py(1.0), BAD, 1.0, "5 5")
d.t(X0 + PW, py(1.0) - 8, "요구 1GB/s", 12, BAD, KR, "end")

for i, (lab, a, b, kind, val) in enumerate(STEPS):
    cx = X0 + COLW / 2 + i * COLW
    top, bot = py(max(a, b)), py(min(a, b))
    if kind == "drop": d.tone(cx - BARW / 2, top, BARW, bot - top, WARN, 3)
    elif kind == "end": d.tone(cx - BARW / 2, top, BARW, bot - top, ACC, 3)
    else: d.box(cx - BARW / 2, top, BARW, bot - top, PAPER2, MUTED, 1.0, 3)
    d.t(cx, top - 10, val, 13, ACC if kind == "end" else INK, MONO, "middle", 600)
    d.t(cx, Y0 + PH + 24, lab, 13, INK, KR, "middle", 600)
    if i < 3:
        nxt = b
        d.line(cx + BARW / 2, py(nxt), cx + COLW - BARW / 2, py(nxt), MUTED, 0.8, "3 3")

cx = X0 + COLW / 2 + 3 * COLW
d.t(cx, py(1.05) + 28, "원서 표기 1.04", 12, MUTED, KR, "middle")

d.legend(Y0 + PH + 52, [("요인 하나를 줄인 하락", WARN), ("남는 처리량", ACC), ("요구치", BAD)])
d.save("02-03.factor-analysis-waterfall.svg")
