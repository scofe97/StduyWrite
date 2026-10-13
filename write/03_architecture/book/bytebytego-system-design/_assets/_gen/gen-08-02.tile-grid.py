# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 줌 레벨 행마다 한 변 타일 수 2^z·전체 타일 수 4^z·지도 한 변 픽셀 256·2^z·시카고가 든 타일을 같은 열에 나란히 놓아 한 단계마다 4배가 되는 모양을 보인다.
# 사실 출처: Google Maps JavaScript API 문서 Map and tile coordinates(타일 256×256, 줌 1 은 4장 512×512, 픽셀 = 세계 좌표 × 2^줌, 타일 = 픽셀 ÷ 256 의 정수부, 시카고 41.85 -87.65, project() 식),
#   MaxZoomService 문서(대부분 로드맵은 줌 0~18, 위성은 위치마다 달라 도쿄 일대 18~21), OSM Slippy map tilenames(줌 12 는 16,777,216 장·줌 18 은 68.7 billion 으로 4^z 와 일치).
#   전체 타일 수·픽셀·시카고 타일은 위 식으로 직접 계산한 값이다.
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 56, 열 폭 [88, 160, 224, 160, 152, 124], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 608
d = D(W, H, "BYTEBYTEGO · 08-02 §4",
      "줌 레벨이 하나 오르면 타일은 4배, 지도 한 변은 2배가 된다",
      "한 변 2^z 장을 제곱한 4^z 장에 한 장 256 픽셀을 곱한 값입니다. 시카고 타일은 Google 문서의 식으로 계산했습니다.",
      "시카고 좌표 41.85, -87.65 는 Google 문서의 예시 값입니다")

cols = [("줌 z", 88), ("한 변 2^z", 160), ("전체 4^z", 224), ("지도 한 변 px", 160), ("시카고 타일", 152), ("비고", 124)]
X0, Y0, HH, RH = 12, 100, 40, 56
x = X0
xs = []
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, fam(nm), "middle", 600)
    x += w

rows = [
    ("0", "1", "1", "256", "(0, 0)", "세계 한 장"),
    ("1", "2", "4", "512", "(0, 0)", ""),
    ("2", "4", "16", "1,024", "(1, 1)", ""),
    ("3", "8", "64", "2,048", "(2, 2)", "본문 계산 예"),
    ("10", "1,024", "1,048,576", "262,144", "(262, 380)", ""),
    ("18", "262,144", "68,719,476,736", "67,108,864", "(67247, 97459)", "로드맵 대부분"),
    ("21", "2,097,152", "4,398,046,511,104", "536,870,912", "(537977, 779672)", "위성 일부"),
]
FOCAL_ROW = 3
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    for k, val in enumerate(row):
        cx0, w = xs[k]
        if r == FOCAL_ROW:
            d.tone(cx0, y, w, RH, ACC, 0, "14", 1.4)
            col = ACC
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
            col = INK if k != 5 else MUTED
        if val:
            d.t(cx0 + w / 2, y + 34, val, 13, col, fam(val), "middle", 600 if k == 0 else 400)

d.legend(H - 56, [("본문 계산 예", ACC), ("계산한 값", INK)])
d.save("08-02.tile-grid.svg")
