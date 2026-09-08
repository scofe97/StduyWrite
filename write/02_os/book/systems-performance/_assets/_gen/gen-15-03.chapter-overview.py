# 15-03 전체 지도 — 이 편이 다루는 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 564
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-03",
       "프로그램을 짜는 다섯 갈래",
       "구조를 세우고 변수와 함수를 익힌 뒤, 종합 예제로 지연 측정을 완성한다.",
       "원라이너로 안 되는 질문을 여기서 짭니다")

BANDS = [
    ("§1", "프로그램 구조", "프로브 · 필터 · 액션", "세 조각이 전부다", ACC),
    ("§2", "변수", "빌트인 · 스크래치 · 맵", "어디에 담을 것인가", None),
    ("§3", "함수 · 맵 함수", "출력과 집계", "무엇으로 셀 것인가", None),
    ("§4", "종합 예제", "vfs_read 지연 측정", "조각을 합친다", None),
    ("§5", "레퍼런스", "프로브 유형 · 연산자 · 빌트인", "찾아 쓰는 표", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")

d.legend(Y0 + 5 * STRIDE + 20, [("이 편의 중심", ACC), ("나머지 절", MUTED)])
d.save("15-03.chapter-overview.svg")