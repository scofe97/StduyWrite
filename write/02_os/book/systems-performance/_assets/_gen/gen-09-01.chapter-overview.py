# 09-01 전체 지도 — 시간을 어디서 재느냐에서 시작해 사용률의 함정까지.
# 타입 스펙: type-layers — 여섯 절이 용어에서 지표 해석으로 옮겨 가는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 632
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-01",
       "디스크를 보는 여섯 갈래",
       "09-01 이 다루는 여섯 절. 시간을 어디서 재느냐를 세운 뒤, 그 위에서 지연·IOPS·사용률을 차례로 해석한다.",
       "같은 I/O 지연도 커널에서 재느냐 디스크에서 재느냐에 따라 다른 값입니다")

BANDS = [
    ("§1", "용어와 모델", "큐를 가진 디스크", "무대를 세운다", None),
    ("§2", "시간 측정", "커널 기준 · 디스크 기준", "어디서 재느냐가 다르다", ACC),
    ("§3", "시간 스케일 · 캐싱", "적중과 미스가 자릿수로 갈린다", "평균 하나로 가려진다", None),
    ("§4", "랜덤 vs 순차 · IOPS", "탐색과 회전이 만드는 차이", "IOPS 는 동등하지 않다", None),
    ("§5", "사용률 · 포화", "가상 디스크가 오해를 부른다", "100% 가 곧 한계는 아니다", None),
    ("§6", "I/O wait · 동기 vs 비동기", "혼란스러운 지표", "앱이 정말 기다렸나", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "용어", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 5 * STRIDE + BH + 16, "해석", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 6 * STRIDE + 18, "8장이 캐시로 디스크를 가리는 층이었다면, 9장은 그 아래 물리 디스크입니다", 13, MUTED, KR, "start")

d.legend(Y0 + 6 * STRIDE + 44, [("나머지를 떠받치는 절", ACC), ("나머지 절", MUTED)])
d.save("09-01.chapter-overview.svg")
