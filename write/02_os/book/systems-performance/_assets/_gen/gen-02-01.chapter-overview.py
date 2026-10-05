# 02-01 전체 지도 — 용어에서 관점까지 네 층.
# 타입 스펙: type-layers — 아래층 어휘가 위층 개념을 받치는 쌓임이라 층으로 그린다.
#           축약: OS 층이 아니므로 인덱스 태그를 절 번호로 채운다. 위가 관점, 아래가 어휘.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 928, 552
BX, BW, BH, Y0, STRIDE = 136, 696, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01",
       "용어에서 관점까지 다섯 층",
       "02-01 의 열한 절을 다섯 층으로 묶었다. 아래층 어휘가 위층 개념을 받치고, 맨 위 두 관점이 그 개념을 분석 방향으로 묶는다.",
       "아래에서 위로 읽습니다 — 어휘가 먼저, 관점이 마지막")

BANDS = [
    ("§11", "두 분석 관점", "자원 분석 bottom-up · 워크로드 분석 top-down", "분석 방향", None),
    ("§8–10", "자원의 거동", "knee point · 사용률과 포화 · 캐시 적중률", "부하가 늘 때", None),
    ("§5–7", "판단 기준", "트레이드오프 · 튜닝 위치 · 멈출 때 · 부하 vs 아키텍처", "어디에 힘을 쓸까", None),
    ("§3–4", "지연과 시간 스케일", "시간으로 환산 · 나노초의 감각", "계산할 수 있는 지표", ACC),
    ("§1–2", "용어와 두 모델", "IOPS · 처리량 · 사용률 · 포화 · 지표 · SUT · 큐잉", "공통 어휘", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 16, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 28, role, 13, c if c else SOFT, KR, "end")

top, bot = Y0 + 8, Y0 + 4 * STRIDE + BH - 8
d.t(48, bot + 20, "어휘", 13, SOFT, KR, "middle")
d.arrow([(48, bot), (48, top + 16)], SOFT, "soft", 1.2, "4 6")
d.t(48, top + 4, "관점", 13, SOFT, KR, "middle")

d.legend(Y0 + 5 * STRIDE + 24, [("이 편의 중심 — 지연", ACC), ("나머지 층", MUTED)])
d.save("02-01.chapter-overview.svg")
