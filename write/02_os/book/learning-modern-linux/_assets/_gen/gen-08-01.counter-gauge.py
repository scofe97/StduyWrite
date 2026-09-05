# 08-01 §3 — 메트릭 세 종류 중 둘은 값이 움직이는 모양으로 갈린다.
# 원문("Metrics"): Counter("The value of a counter can only ever go up (besides resetting a counter to
#       zero). An example of a counter metric is the total number of requests handled by a service or the
#       bytes sent via an interface over a time period."),
#       Gauges("A gauge value can go up or down. For example, you gauge the currently available overall
#       main memory or the number of processes running."),
#       Histograms("A sophisticated way to build a distribution of values. Using buckets, histograms allow
#       you to assess how the data overall is structured.").
#       또 "Metrics are (usually regularly) sampled numerical data points, forming a time series."
# 주의: 원문에 수치 예시는 없다. 아래 두 계열은 저자가 정의한 *모양*(단조 증가 · 오르내림)만 그린 것이라
#       세로축에 눈금값을 적지 않는다. 눈금값을 적으면 본문의 "수치가 없다"는 서술과 어긋난다.
# 타입 스펙: type-line — 시간(샘플 순서)에 따른 연속 추세. 두 계열의 방향과 변화율이 논지다.
#           축약: 히스토그램은 시계열이 아니라 분포라 이 선그래프에 담기지 않아 본문 표가 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 880, 536
PX0, PX1, PY0, PY1 = 88, 840, 124, 384
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §3",
      "카운터는 올라가기만 하고 게이지는 오르내린다",
      "저자가 정의한 두 메트릭 종류의 값이 움직이는 모양. 세로축에 단위가 없는 것은 원문에 수치가 "
      "없기 때문이고, 여기서 읽을 것은 크기가 아니라 방향이다.",
      "세 번째 종류인 히스토그램은 시계열이 아니라 분포라 이 그림에 없습니다")

COUNTER = [0, 118, 246, 352, 498, 622, 744, 902]
GAUGE = [402, 566, 318, 690, 284, 604, 356, 470]
YMAX = 1000
N = len(COUNTER)


def px(i):
    return PX0 + (PX1 - PX0) * i / (N - 1)


def py(v):
    return PY1 - (PY1 - PY0) * v / YMAX


for g in range(5):
    y = PY0 + (PY1 - PY0) * g / 4
    d.line(PX0, y, PX1, y, RULE, 0.8)
d.t(PX0 - 12, (PY0 + PY1) / 2, "값", 11, SOFT, KR, "end")
d.t(PX0 - 12, (PY0 + PY1) / 2 + 18, "눈금 없음", 10, SOFT, KR, "end")
d.line(PX0, PY1, PX1, PY1, RULE, 1.2)
for i in range(N):
    d.t(px(i), PY1 + 20, f"t{i}", 10.5, SOFT, MONO)

pts_g = " ".join(f"{px(i)},{py(v)}" for i, v in enumerate(GAUGE))
d.o.append(f'<polyline points="{pts_g}" fill="none" stroke="{INFO}" stroke-width="1.2" '
           f'stroke-linejoin="round"/>')
pts_c = " ".join(f"{px(i)},{py(v)}" for i, v in enumerate(COUNTER))
d.o.append(f'<polyline points="{pts_c}" fill="none" stroke="{ACC}" stroke-width="1.8" '
           f'stroke-linejoin="round"/>')
for i, v in enumerate(COUNTER):
    d.o.append(f'<circle cx="{px(i)}" cy="{py(v)}" r="4" fill="{ACC}"/>')

d.t(PX0 + 12, 160, "카운터 — 서비스가 처리한 총 요청 수", 12, ACC, KR, "start", 600)
d.t(PX1 - 12, 348, "게이지 — 지금 돌고 있는 프로세스 수", 12, INFO, KR, "end", 600)

d.t(24, PY1 + 60, "카운터는 0 으로 초기화되는 경우를 빼면 값이 내려가지 않습니다. 그래서 그래프의 "
                  "기울기가 곧 처리율입니다.", 12, MUTED, KR, "start")
d.t(24, PY1 + 82, "게이지는 지금 이 순간의 값이라 오르내립니다. 남은 주 메모리처럼 "
                  "누적이 뜻을 갖지 않는 대상에 씁니다.", 12, MUTED, KR, "start")

d.legend(H - 56, [("카운터 — 올라가기만 한다", ACC), ("게이지 — 오르내린다", INFO),
                  ("눈금과 축", SOFT)])
d.save("08-01.counter-gauge.svg")
print("ok 08-01.counter-gauge")
