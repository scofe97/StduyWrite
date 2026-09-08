# 09-04 전체 지도 — 이 편이 다루는 다섯 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 564
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-04",
       "관측 도구를 꺼내는 다섯 갈래",
       "전통 통계에서 BPF 트레이싱으로, 마지막에 컨트롤러·펌웨어까지 내려간다.",
       "위에서 끝낼 수 있으면 아래로 내려가지 않습니다")

BANDS = [
    ("§1", "iostat", "디스크별 통계의 출발점", "분석은 여기서 시작", None),
    ("§2", "sar · PSI · pidstat", "시계열 · 압박 · 프로세스별", "추세와 책임자", None),
    ("§3", "perf · biolatency · biosnoop", "트레이스 · 히스토그램 · 건당", "분포와 이상치", ACC),
    ("§4", "biotop · biostacks · blktrace", "top · 유발 스택 · 저수준", "누가 왜 냈나", None),
    ("§5", "bpftrace · MegaCli · smartctl", "커스텀 · 컨트롤러 · 펌웨어", "스택 밖까지", None),
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
d.save("09-04.chapter-overview.svg")