# 09-02 전체 지도 — 이 편이 다루는 다섯 절.
# 타입 스펙: type-layers — 절이 차례로 구체화되는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 564
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-02",
       "아키텍처를 보는 다섯 갈래",
       "HDD 에서 SSD 로, 인터페이스와 RAID 를 거쳐 커널 블록 층까지 내려간다.",
       "물리 특성이 위로 올라오며 어떻게 가려지는지를 봅니다")

BANDS = [
    ("§1", "회전 디스크(HDD)", "탐색과 회전이 만드는 지연", "물리가 그대로 드러난다", None),
    ("§2", "SSD", "비대칭 읽기/쓰기와 FTL", "움직이는 부품이 없다", None),
    ("§3", "인터페이스", "SCSI 에서 NVMe 까지", "경로의 폭을 정한다", None),
    ("§4", "RAID · 스토리지 유형", "묶음의 성능", "여럿을 하나로 보인다", None),
    ("§5", "Linux 블록 I/O 스택", "병합 · 스케줄러 · blk-mq", "커널이 다시 배치한다", ACC),
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
d.save("09-02.chapter-overview.svg")