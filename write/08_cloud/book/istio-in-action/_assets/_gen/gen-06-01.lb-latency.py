# 06-01 §2 세 알고리즘의 지연 백분위 — 원문 6.2.3 의 Fortio 결과 15개 수치를 그대로.
# 본문: "가로축은 백분위, 세로축은 밀리초. 세 선이 50%에서는 겹친다. 갈리는 곳은 75%.
# 색이 붙은 LEAST_CONN 만 195.63ms 에 머물고 나머지 둘은 1초를 넘는다. 대신 99% 이후로는 LEAST_CONN 이 가장 높다."
# 타입 스펙: type-line — 순차 인덱스(백분위) 위의 연속 추세. 점 5개(4~12), 시리즈 3개(≤5), 초점만 점을 찍는다.
#           y 축은 0 을 포함하고 x 는 스펙대로 등간격 인덱스. 비초점 색은 스타일 계약 토큰(muted·info)을 쓴다
#           — upstream series-1~5 는 이 저장소 스킨이 쓰지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 06-01 §2",
      "세 알고리즘의 지연 백분위",
      "simple-backend-1 에 최대 1초 지연을 넣고 커넥션 10개로 초당 1,000 요청을 60초 보낸 Fortio 결과. "
      "50% 에서는 셋이 겹치고 75% 에서 LEAST_CONN 만 195.63ms 에 머문다. 90% 부터는 LEAST_CONN 이 가장 높다.",
      "엔드포인트가 균일하지 않을 때 활성 요청 수를 보는 알고리즘이 중간값 구간을 지킵니다")

PL, PR, PT, PB = 80, W - 40, 108, 452
pcts = ["50%", "75%", "90%", "99%", "99.9%"]
series = [
    ("ROUND_ROBIN", [191.47, 1013.31, 1033.15, 1045.05, 1046.24], MUTED, 1.2, False),
    ("RANDOM",      [189.53, 1007.72, 1029.68, 1042.85, 1044.17], INFO,  1.2, False),
    ("LEAST_CONN",  [184.79,  195.63, 1036.89, 1124.00, 1132.71], ACC,   1.8, True),
]
YMAX = 1200
def X(i): return PL + i * (PR - PL) / (len(pcts) - 1)
def Y(v): return PB - v / YMAX * (PB - PT)
for g in range(0, YMAX + 1, 200):
    d.line(PL, Y(g), PR, Y(g), RULE, 1.0 if g == 0 else 0.8)
    d.t(PL - 10, Y(g) + 4, f"{g}", 8, SOFT, MONO, "end")
d.t(PL - 10, PT - 14, "ms", 8, SOFT, MONO, "end")
d.line(PL, PT, PL, PB, RULE, 0.8)
for i, p in enumerate(pcts):
    d.line(X(i), PB, X(i), PB + 6, RULE, 0.8)
    d.t(X(i), PB + 22, p, 9, MUTED, MONO)
d.t((PL + PR) / 2, PB + 44, "백분위", 11, SOFT, KR)
for name, vals, color, sw, focal in series:
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    d.o.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>')
    if focal:
        for i, v in enumerate(vals):
            d.o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{color}"/>')
# 논점 하나만 값으로 못 박는다 — 75% 에서 벌어지는 간격
d.t(X(1) + 12, Y(195.63) - 10, "195.63ms", 11, ACC, MONO, "start", 600)
d.t(X(1) + 12, Y(1013.31) + 20, "1013.31ms · 1007.72ms", 11, MUTED, MONO, "start")
d.t(X(4) - 4, 145, "90% 부터는 가장 높다", 11, ACC, KR, "end")
# 두 선이 6ms 안에서 겹쳐 포개진다 — 값을 옮기지 않고 그 사실을 적는다
d.t(X(0) + 12, Y(700), "ROUND_ROBIN 과 RANDOM 은 다섯 값이 모두 6ms 안에 들어", 11, SOFT, KR, "start")
d.t(X(0) + 12, Y(640), "선이 거의 포개집니다", 11, SOFT, KR, "start")
# 원문의 문장은 "least connection performs better than both random and round robin" 이다.
# "권하는" 은 그보다 강하므로 적은 그대로 옮긴다.
d.legend(512, [("ROUND_ROBIN", MUTED), ("RANDOM", INFO), ("LEAST_CONN — 저자가 더 낫다고 적은 쪽", ACC)])
d.save("06-01.lb-latency.svg")
