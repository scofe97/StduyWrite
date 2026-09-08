# 09-03 전체 지도 — 이 편이 다루는 다섯 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 564
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-03",
       "행동으로 옮기는 다섯 갈래",
       "무엇부터 볼지 정하고, 원인을 좁히고, 분포로 보고, 부하를 걸고, 손잡이를 돌린다.",
       "평균 하나로는 봉우리가 둘인 분포를 볼 수 없습니다")

BANDS = [
    ("§1", "방법론 10종", "USE · 워크로드 특성화", "무엇부터 볼지 정한다", None),
    ("§2", "워크로드 특성화 · 지연 분석", "원인 좁히기", "어디서 시간을 쓰나", None),
    ("§3", "시각화", "수많은 I/O 를 한눈에", "분포가 평균을 이긴다", ACC),
    ("§4", "실험", "의도적으로 부하 걸기", "능동으로 잰다", None),
    ("§5", "튜닝", "어떤 손잡이를 돌리나", "마지막에 손댄다", None),
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
d.save("09-03.chapter-overview.svg")