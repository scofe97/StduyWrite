# 타입 스펙: type-bar — 가로 막대 8 개(스펙 상한 4~8). 값이 10^-1 ns 부터 10^9 ns 까지 열 자릿수에 걸쳐 선형 축이 성립하지 않아 log10 축을 쓴다(스펙의 "0 에서 시작하는 선형 축"에서 벗어난 적응).
# 사실 출처: Jeff Dean 슬라이드 PDF(https://research.google.com/people/jeff/stanford-295-talk.pdf, 2007 년 봄 CS295 강의) 「Numbers Everyone Should Know」 표,
#   같은 값을 옮긴 High Scalability 2011-01-26 글, 추출본 v2.txt 563~577행·PDF 36쪽 표 2-2.
#   값(ns): L1 0.5 · L2 7 · 메인 메모리 100 · 메모리 1 MB 250,000 · 데이터 센터 왕복 500,000 · 디스크 탐색 10,000,000 · 디스크 1 MB 30,000,000 · CA→NL→CA 150,000,000.
# Layout conventions: 플롯 x=296(10^-1 ns)~896(10^9 ns), decade 당 60px, 행 stride 48·막대 높이 24, 행 시작 y=112. 데이터 좌표는 4 의 배수 예외.
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 600
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 02-01 §2",
      "지연 시간은 0.5 ns 에서 150 ms 까지 아홉 자릿수 가까이 벌어진다",
      "L1 캐시 0.5 ns 에서 대륙 간 왕복 150 ms 까지 8 개 값을 로그 축 막대로 그렸다. 디스크 탐색은 메인 메모리 참조의 10^5 배다.",
      "Jeff Dean 이 든 값 · 로그 축 · 막대 길이는 자릿수")

PX0, PPD, LOG0 = 296, 60, -1.0
ROW0, STRIDE, BH = 112, 48, 24
rows = [
    ("L1 캐시 참조", 0.5, "0.5 ns", INFO, False),
    ("L2 캐시 참조", 7, "7 ns", INFO, False),
    ("메인 메모리 참조", 100, "100 ns", INFO, False),
    ("메모리에서 1 MB 순차 읽기", 250_000, "250 µs", INFO, False),
    ("같은 데이터 센터 안 왕복", 500_000, "500 µs", OK, False),
    ("디스크 탐색", 10_000_000, "10 ms", WARN, True),
    ("디스크에서 1 MB 순차 읽기", 30_000_000, "30 ms", WARN, False),
    ("패킷 CA → 네덜란드 → CA", 150_000_000, "150 ms", BAD, False),
]


def x_of(ns):
    return round(PX0 + (math.log10(ns) - LOG0) * PPD, 1)


# 눈금선: 1 ns · 1 µs · 1 ms · 1 s
ticks = [(1, "1 ns"), (1_000, "1 µs"), (1_000_000, "1 ms"), (1_000_000_000, "1 s")]
ytop, ybot = ROW0 - 12, ROW0 + 7 * STRIDE + BH + 12
for ns, lab in ticks:
    x = x_of(ns)
    d.line(x, ytop, x, ybot, RULE, 0.8, "3 5")
    d.t(x, ybot + 24, lab, 12, MUTED, MONO)
d.line(PX0, ytop, PX0, ybot, RULE, 1.0)

for k, (name, ns, lab, c, focal) in enumerate(rows):
    y = ROW0 + k * STRIDE
    xe = x_of(ns)
    d.t(PX0 - 16, y + 17, name, 13, INK, KR, "end", 600 if focal else 400)
    if focal:
        d.o.append(f'<rect x="{PX0}" y="{y}" width="{xe - PX0}" height="{BH}" rx="3" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{PX0}" y="{y}" width="{xe - PX0}" height="{BH}" rx="3" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(xe + 10, y + 17, lab, 13, ACC if focal else c, MONO, "start", 600)

d.legend(H - 56, [("캐시 · 메모리", INFO), ("데이터 센터 안", OK), ("디스크", WARN), ("대륙 간", BAD), ("짚는 값", ACC)])
d.save("02-01.latency-scale.svg")
