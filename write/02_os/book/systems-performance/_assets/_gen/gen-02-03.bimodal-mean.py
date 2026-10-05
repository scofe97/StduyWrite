# 02-03 §5 — 두 봉우리 사이 골짜기에 떨어진 평균 3.3ms.
# 타입 스펙: type-bar — 0.5ms 구간별 개수 히스토그램.
#           원서 그림 2.23(p.63)에서 가져온 사실은 셋뿐이다: 왼쪽 봉우리 1ms 미만, 오른쪽 봉우리 약 7ms, 평균 3.3ms.
#           막대 높이는 그 셋에 맞춘 설명용 모양이다(이 높이로 계산한 평균 3.29ms). 실제 측정 분포가 아니다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 480
X0, Y0, PW, PH = 96, 128, 736, 248
COUNTS = [40, 30, 7, 3, 2, 1, 1, 1, 1, 2, 3, 5, 8, 11, 10, 8, 5, 3, 2, 1]
BIN, XMAX, YMAX = 0.5, 10.0, 44
MEAN = sum(c * (BIN / 2 + BIN * i) for i, c in enumerate(COUNTS)) / sum(COUNTS)

def px(v): return X0 + PW * v / XMAX
def py(v): return Y0 + PH - PH * v / YMAX

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §5",
       "평균은 아무도 없는 골짜기에 떨어진다",
       "디스크 I/O 지연 히스토그램의 두 봉우리(1ms 미만 캐시 적중, 약 7ms 캐시 미스) 사이에 평균 3.3ms 가 놓인다. 막대 높이는 설명용 모양이다.",
       "원서 그림 2.23 의 세 값만 씀 · 막대 높이는 설명용")

d.line(X0, Y0 + PH, X0 + PW, Y0 + PH, MUTED, 1.0)
for v in range(0, 11, 2):
    d.t(px(v), Y0 + PH + 22, f"{v}ms", 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "디스크 I/O 지연 →", 12, SOFT, KR, "end")
d.t(X0 - 12, Y0 + 8, "개수", 12, SOFT, KR, "end")

bw = PW * BIN / XMAX
for i, c in enumerate(COUNTS):
    x = px(i * BIN)
    d.box(x + 2, py(c), bw - 4, Y0 + PH - py(c), PAPER2, INFO, 1.0, 2)

mx = px(3.3)
d.line(mx, Y0 - 8, mx, Y0 + PH, ACC, 2.0)
d.t(mx + 10, Y0 + 8, "평균 3.3ms", 14, ACC, MONO, "start", 600)
d.t(px(0.5), py(40) - 12, "캐시 적중 · 1ms 미만", 13, INFO, KR, "start", 600)
d.t(px(7.0), py(11) - 14, "캐시 미스 · 약 7ms", 13, INFO, KR, "middle", 600)

d.legend(Y0 + PH + 60, [("지연 구간별 개수", INFO), ("평균", ACC)])
d.save("02-03.bimodal-mean.svg")
