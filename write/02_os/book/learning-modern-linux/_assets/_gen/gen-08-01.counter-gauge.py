# 08-01 §1 — 메트릭 세 종류 중 둘은 값이 움직이는 모양으로 갈린다.
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
#           실제 구조로 보이는 것: 시계열은 일정 간격으로 표집한 점의 줄이고(두 계열 모두 점을 찍었다),
#           카운터가 내려가는 경우는 본문이 밝힌 단 하나 "0 으로 초기화" 뿐이다(t6 의 떨어짐).
#           축약: 히스토그램은 시계열이 아니라 분포라 이 선그래프에 담기지 않아 본문 표가 맡는다.
#           본문에 없는 해석(기울기 = 처리율)은 그리지 않는다. 초기화 시점 t6 은 예시다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, RULE, PAPER, KR, MONO

W, H = 880, 584
PX0, PX1, PY0, PY1 = 104, 840, 124, 384
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §1",
      "카운터는 올라가기만 하고 게이지는 오르내린다",
      "일정 간격으로 표집한 점이 이룬 두 시계열. 카운터는 점마다 이전 값 이상이고, 내려가는 것은 0 으로 "
      "초기화될 때뿐이다. 게이지는 점마다 그 순간의 값이라 오르내린다. 세로축에 단위가 없는 것은 크기가 "
      "아니라 방향을 보이려는 그림이기 때문이다.",
      "세 번째 종류인 히스토그램은 시계열이 아니라 분포라 이 그림에 없습니다")

COUNTER = [0, 120, 236, 352, 470, 590, 0, 118, 240, 356]
RESET = 6
GAUGE = [402, 566, 318, 690, 284, 470, 356, 470, 300, 520]
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
d.t(PX0 - 12, (PY0 + PY1) / 2 + 18, "눈금 없음", 11, SOFT, KR, "end")
d.line(PX0, PY1, PX1, PY1, RULE, 1.2)
for i in range(N):
    d.t(px(i), PY1 + 20, f"t{i}", 10.5, SOFT, MONO)
d.t(PX1, PY1 + 40, "표집 시각 · 간격 일정", 11, SOFT, KR, "end")

# 게이지 — 점마다 그 순간의 값
pts_g = " ".join(f"{px(i)},{py(v)}" for i, v in enumerate(GAUGE))
d.o.append(f'<polyline points="{pts_g}" fill="none" stroke="{INFO}" stroke-width="1.2" '
           f'stroke-linejoin="round"/>')
for i, v in enumerate(GAUGE):
    d.o.append(f'<circle cx="{px(i)}" cy="{py(v)}" r="3.2" fill="{PAPER}" stroke="{INFO}" stroke-width="1.2"/>')

# 카운터 — 초기화 앞뒤를 끊어 그리고, 떨어지는 구간만 점선
for a, b in ((0, RESET), (RESET, N)):
    seg = " ".join(f"{px(i)},{py(COUNTER[i])}" for i in range(a, b))
    d.o.append(f'<polyline points="{seg}" fill="none" stroke="{ACC}" stroke-width="1.8" '
               f'stroke-linejoin="round"/>')
d.line(px(RESET - 1), py(COUNTER[RESET - 1]), px(RESET), py(0), WARN, 1.4, "4 3")
for i, v in enumerate(COUNTER):
    d.o.append(f'<circle cx="{px(i)}" cy="{py(v)}" r="4" fill="{WARN if i == RESET else ACC}"/>')
d.t(px(RESET) - 14, py(0) - 10, "0 으로 초기화", 12, WARN, KR, "end", 600)

d.t(PX0 + 12, 152, "카운터 — 서비스가 처리한 총 요청 수", 12.5, ACC, KR, "start", 600)
d.t(PX1 - 8, 152, "게이지 — 실행 중인 프로세스 수", 12.5, INFO, KR, "end", 600)

NY = PY1 + 76
d.chip(196, NY, "카운터가 내려가는 때", ACC, 12)
d.t(304, NY + 4, "0 으로 초기화될 때뿐 · 다른 예: 인터페이스로 보낸 총 바이트", 12, MUTED, KR, "start")
d.chip(196, NY + 34, "게이지 = 그 순간의 값", INFO, 12)
d.t(304, NY + 38, "예: 가용 주 메모리 · 실행 중인 프로세스 수", 12, MUTED, KR, "start")

d.legend(H - 56, [("카운터 — 올라가기만 한다", ACC), ("게이지 — 오르내린다", INFO),
                  ("0 으로 초기화 (t6 은 예시)", WARN)])
d.save("08-01.counter-gauge.svg")
print("ok 08-01.counter-gauge")
