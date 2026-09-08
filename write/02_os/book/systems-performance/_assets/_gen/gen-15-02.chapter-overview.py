# 15-02 전체 지도 — 이 편이 다루는 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 420
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-02",
       "원라이너를 쓰는 세 갈래",
       "한 줄의 구조를 익히고, 자원별로 이미 검증된 원라이너를 손에 넣는다.",
       "외우는 것이 아니라 조각을 바꿔 끼우는 것입니다")

BANDS = [
    ("§1", "bpftrace 개요", "추적의 awk", "한 줄로 묻는다", ACC),
    ("§2", "원라이너 — CPU · 메모리 · FS", "자원별 검증된 한 줄", "가져다 고쳐 쓴다", None),
    ("§3", "원라이너 — 디스크 · 네트워크 · 앱", "같은 문법 다른 프로브", "패턴은 하나다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 2 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")

d.legend(Y0 + 3 * STRIDE + 20, [("이 편의 중심", ACC), ("나머지 절", MUTED)])
d.save("15-02.chapter-overview.svg")