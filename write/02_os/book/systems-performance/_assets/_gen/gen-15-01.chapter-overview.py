# 15-01 전체 지도 — 이 편이 다루는 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 492
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-01",
       "BPF 를 시작하는 네 갈래",
       "BPF 가 무엇인지 세우고, 두 프론트엔드를 가른 뒤, BCC 도구를 단일 목적과 다목적으로 나눠 본다.",
       "기성 도구로 답이 나오면 거기서 끝내는 것이 가장 쌉니다")

BANDS = [
    ("§1", "BPF 개요", "프로그래밍 가능한 트레이서", "커널 안에서 집계한다", ACC),
    ("§2", "BCC 설치 · 커버리지", "무엇이 이미 있는가", "남의 것을 먼저 본다", None),
    ("§3", "BCC 단일 목적 도구", "opensnoop · execsnoop", "하나만 잘한다", None),
    ("§4", "BCC 다목적 · 원라이너", "funccount · trace · argdist", "조합해 쓴다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 3 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")

d.legend(Y0 + 4 * STRIDE + 20, [("이 편의 중심", ACC), ("나머지 절", MUTED)])
d.save("15-01.chapter-overview.svg")