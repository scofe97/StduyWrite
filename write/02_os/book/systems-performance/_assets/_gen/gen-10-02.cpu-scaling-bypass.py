# 10-02 §5 — 같은 목표(높은 패킷율)를 향한 세 수위: 분산 → 완화 → 우회.
# 타입 스펙: type-layers — 아래로 갈수록 스택에서 멀어지는(분산 → 완화 → 우회) 수위 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 수위 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 456
BX, BW, BH, Y0, STRIDE = 128, 704, 76, 116, 84

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §5",
       "패킷율을 올리는 세 수위",
       "여러 CPU 로 나누는 것, 인터럽트를 합치는 것, 스택을 우회하는 것. 아래로 갈수록 성능은 오르고 관측성은 떨어진다.",
       "바이패스의 대가는 관측성 상실입니다 — 카운터와 트레이싱 이벤트도 함께 우회됩니다")

BANDS = [
    ("01", "CPU 분산", "RSS · RPS · RFS · XPS", "여러 CPU 가 나눠 처리합니다", OK),
    ("02", "인터럽트 완화", "NAPI — 저부하 인터럽트, 고부하 폴링", "인터럽트를 합칩니다", INFO),
    ("03", "커널 바이패스", "DPDK 우회 · XDP 는 eBPF 로 가속", "스택을 건너뜁니다", ACC),
]

for i, (n, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c is ACC: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 44, n, 13, c, MONO, "end", 600)
    d.t(BX + 20, y + 30, name, 14, c, KR, "start", 600)
    d.t(BX + 20, y + 54, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 44, role, 13, c, KR, "end")

d.t(BX - 76, Y0 + 4, "관측 가능", 13, SOFT, KR, "middle")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 2 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 76, Y0 + 2 * STRIDE + BH + 16, "깜깜해짐", 13, SOFT, KR, "middle")

YB = Y0 + 3 * STRIDE + 8
d.t(BX, YB, "부하 분산이 없으면 NIC 가 한 CPU 만 인터럽트해 그 CPU 가 100% 에 닿습니다 — mpstat 의 높은 softirq 로 보입니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("스택을 우회하는 수위", ACC), ("CPU 를 늘리는 수위", OK), ("인터럽트를 합치는 수위", INFO)])
d.save("10-02.cpu-scaling-bypass.svg")
