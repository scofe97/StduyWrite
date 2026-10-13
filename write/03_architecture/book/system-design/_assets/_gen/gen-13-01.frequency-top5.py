# 타입 스펙: type-bar — 빈도 표 여덟 행을 빈도 내림차순 가로 막대로 그리고, LIMIT 5 가 자르는 선을 막대 사이에 긋는다. focal 은 자르는 선.
# 사실 출처: 추출본 v2.txt 3622~3634행(빈도 표 · tw 입력 시 상위 5 · SQL) · PDF 204쪽 표와 그림(twitter 35 · twitch 29 · twilight 25 · twin peak 21 · twitch prime 18 · twitter search 14 · twillo 10 · twin peak sf 8).
#   표의 첫 행은 대문자 Twitter 로 적혀 있으나 질의를 소문자로 가정한 요구사항에 맞춰 twitter 로 쓴다. SQL 은 PDF 그림의 SELECT·WHERE·ORDER BY·LIMIT 순서를 따르고 따옴표만 표준 문자열 따옴표로 쓴다.
# Layout conventions: 행 stride 48(y=124 부터 8 행), 막대 높이 28, 막대 시작 x=232, 빈도 1 = 16px. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, INK, SOFT, KR, MONO

W, H = 960, 572
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §2",
      "tw 로 시작하는 질의 여덟 개 중 빈도 위쪽 다섯 개가 제안이 된다",
      "WHERE query LIKE 'tw%' 가 후보를 고르고 ORDER BY frequency DESC 가 줄을 세우며 LIMIT 5 가 자른다.",
      "빈도 표 예시 · 접두사 tw")

ROWS = (("twitter", 35), ("twitch", 29), ("twilight", 25), ("twin peak", 21),
        ("twitch prime", 18), ("twitter search", 14), ("twillo", 10), ("twin peak sf", 8))
X0, U, Y0, ST, BH = 232, 16, 124, 48, 28

d.t(24, 108, "query", 12, SOFT, MONO, "start")
d.t(X0, 108, "frequency", 12, SOFT, MONO, "start")

for i, (q, f) in enumerate(ROWS):
    y = Y0 + i * ST
    keep = i < 5
    c = OK if keep else MUTED
    d.t(24, y + 19, q, 14, INK if keep else MUTED, MONO, "start", 600 if keep else 400)
    d.tone(X0, y, f * U, BH, c, 4, "22" if keep else "14", 1.1)
    d.t(X0 + f * U + 10, y + 19, str(f), 14, INK if keep else MUTED, MONO, "start")

cut = Y0 + 5 * ST - 10
d.line(24, cut, W - 24, cut, ACC, 1.6, "6 4")
d.t(W - 24, cut - 8, "LIMIT 5", 13, ACC, MONO, "end", 600)

d.legend(H - 56, [("돌려주는 행", OK), ("버려지는 행", MUTED), ("자르는 선", ACC)])
d.save("13-01.frequency-top5.svg")
