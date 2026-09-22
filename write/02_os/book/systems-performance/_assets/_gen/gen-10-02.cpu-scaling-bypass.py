# 10-02 §5 — 같은 목표(높은 패킷율)를 향한 네 수위: 분산 → 완화 → 스택 앞단 판정(XDP) → 우회(DPDK).
# 타입 스펙: type-layers — 아래로 갈수록 스택에서 멀어지는(분산 → 완화 → 우회) 수위 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 수위 번호로 채운다.
#           XDP 는 커널 안에서 스택 앞단에 붙고 DPDK 는 포트를 커널에서 떼므로 두 띠로 가른다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 492
BX, BW, BH, Y0, STRIDE = 128, 704, 64, 116, 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §5",
       "패킷율을 올리는 네 수위",
       "여러 CPU 로 나누는 것, 인터럽트를 묶는 것, 스택 앞단에서 판정하는 것(XDP), 커널을 비켜 가는 것(DPDK). 아래로 갈수록 커널 도구가 보는 범위가 줄어든다.",
       "DPDK 는 카운터·트레이싱까지 비켜 가고, XDP 는 판정 뒤 스택에서 빠진 패킷만 안 보입니다")

BANDS = [
    ("01", "CPU 분산", "RSS · RPS · RFS · XPS", "여러 CPU 에 나눔", OK),
    ("02", "인터럽트 완화", "NAPI — 인터럽트 뒤 poll 로 묶어 처리", "인터럽트 횟수 감소", INFO),
    ("03", "스택 앞단 판정 (XDP)", "eBPF · PASS · DROP · TX · REDIRECT", "커널 안 · PASS 는 스택으로", WARN),
    ("04", "커널 우회 (DPDK)", "포트를 커널 드라이버에서 떼어 vfio-pci · 유저 공간 PMD", "커널 관측 없음", ACC),
]

for i, (n, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c is ACC: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 38, n, 13, c, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c, KR, "end")

d.t(BX - 76, Y0 + 4, "관측 가능", 13, SOFT, KR, "middle")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 3 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 76, Y0 + 3 * STRIDE + BH + 16, "깜깜해짐", 13, SOFT, KR, "middle")

YB = Y0 + 4 * STRIDE + 20
d.legend(YB, [("커널을 비켜 가는 수위", ACC), ("CPU 를 늘리는 수위", OK), ("인터럽트를 묶는 수위", INFO), ("스택 앞단 판정", WARN)])
d.save("10-02.cpu-scaling-bypass.svg")
