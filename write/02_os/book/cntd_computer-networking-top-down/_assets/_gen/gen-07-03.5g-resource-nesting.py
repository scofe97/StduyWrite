# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 대역 안에 채널, 채널 안에 부반송파가 들어간다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.3 Figure 7.29 · Figure 7.30 —
#   4G 채널 폭 목록, 10 MHz = RB 50 개, 물리 채널 여섯의 이름과 역할은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 596
d = D(W, H, "SECTION 7.3.3 · BANDS, CHANNELS, SUBCARRIERS",
      "대역 안에 채널, 채널 안에 부반송파",
      "국가가 대역을 배정하면 사업자가 그 안을 채널로 자르고, 채널을 다시 부반송파로 자른다. 자르는 권한이 층마다 다르다.",
      "채널 폭 목록과 RB 개수는 원문 §7.3.3 의 값입니다")

LEVELS = [
    (24, 116, 496, 300, "대역", "국가가 배정하고 사업자가 경매로 받습니다", ACC),
    (56, 158, 432, 216, "채널", "4G 는 1.4 · 3 · 5 · 10 · 15 · 20 MHz", INFO),
    (88, 200, 368, 132, "부반송파", "채널을 다시 자릅니다 · 4G 는 15 kHz", INFO),
    (120, 242, 304, 48, "자원 블록", "부반송파 12 개 × 미니슬롯 7 개", OK),
]
for x, y, w, h, name, sub, c in LEVELS:
    d.tone(x, y, w, h, c, 8, "10", 1.3)
    d.t(x + 16, y + 22, name, 12, c, KR, "start", 600)
    d.t(x + 16, y + 40, sub, 10, MUTED, KR, "start")

d.t(24, 442, "10 MHz 폭 채널 하나는 서로 다른 부반송파를 쓰는 자원 블록 50 개로 나뉩니다.",
    11, MUTED, KR, "start")
d.t(24, 464, "5G 는 4G 채널 정의를 모두 물려받고 최대 100 MHz 폭 채널을 더 정의합니다.",
    11, MUTED, KR, "start")

PX, PW = 556, 348
d.box(PX, 116, PW, 300, PAPER2, RULE, 1.0)
d.t(PX + 20, 142, "자원 블록은 여섯 갈래로 나뉘어 쓰입니다", 12, INK, KR, "start", 600)
d.line(PX + 20, 154, PX + PW - 20, 154, RULE, 0.8)
GROUPS = [
    ("하향 — 기지국에서 기기로", INK, [
        ("PDSCH", "사용자 데이터와 제어 메시지"),
        ("PDCCH", "어느 블록으로 받고 보낼지 알림"),
        ("PBCH", "망 발견에 필요한 방송 정보"),
    ]),
    ("상향 — 기기에서 기지국으로", INK, [
        ("PUSCH", "사용자 데이터와 제어 메시지"),
        ("PRACH", "처음 붙을 때 쓰는 임의 접속"),
        ("PUCCH", "블록 요청 · 측정값 · ACK/NAK"),
    ]),
]
gy = 176
for title, c, items in GROUPS:
    d.t(PX + 20, gy, title, 11, c, KR, "start", 600)
    for j, (nm, desc) in enumerate(items):
        y = gy + 22 + j * 20
        d.t(PX + 20, y, nm, 11, SOFT, MONO, "start")
        d.t(PX + PW - 20, y, desc, 10, MUTED, KR, "end")
    gy += 108

NY = 494
d.box(24, NY, 880, 44, PAPER2, RULE, 1.0)
d.t(44, NY + 28,
    "상하향 비율은 사업자가 정합니다. 시간 슬롯으로 나누면 시분할 듀플렉싱, 주파수로 나누면 주파수 분할 듀플렉싱입니다.",
    11, MUTED, KR, "start")

d.legend(552, [("국가가 정하는 층", ACC), ("사업자가 정하는 층", INFO), ("배정 단위", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.5g-resource-nesting.svg"
d.save(out)
print("→", out)
