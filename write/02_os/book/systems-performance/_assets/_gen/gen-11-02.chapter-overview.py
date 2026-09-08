# 11-02 전체 지도 — 구현에서 오버헤드로, 제어와 관측으로.
# 타입 스펙: type-layers — 다섯 절이 구현 → 오버헤드 → 제어 → 관측으로 옮겨 가는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-02",
       "하드웨어 가상화를 보는 다섯 갈래",
       "11-02 가 다루는 다섯 절. 하이퍼바이저 구현에서 시작해 오버헤드가 어디서 생기는지 짚고, 제어와 관측으로 넘어간다.",
       "언제 오버헤드가 생기고 언제 안 생기는지를 아는 것이 이 편의 목표입니다")

BANDS = [
    ("§1", "구현", "VMware · Xen · KVM · Nitro", "I/O 경로의 단계 수가 갈린다", None),
    ("§2", "CPU 오버헤드", "guest exit 가 핵심", "빠져나간 시간이 곧 오버헤드", ACC),
    ("§3", "메모리 · I/O 오버헤드", "EPT/NPT · SR-IOV", "하드웨어가 단계를 없앤다", None),
    ("§4", "자원 제어", "vCPU · balloon · cgroup", "호스트 제어를 함께 쓴다", None),
    ("§5", "관측", "호스트는 자원 · 게스트는 커널", "보이는 것이 자리마다 다르다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "구조", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "분석", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "게스트마다 자체 커널이 있어, 게스트 안에서는 커널 추적 도구가 다 동작합니다", 13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("CPU 오버헤드의 정체", ACC), ("나머지 절", MUTED)])
d.save("11-02.chapter-overview.svg")
