# 10-02 전체 지도 — 프로토콜에서 하드웨어, 그 위의 커널 소프트웨어로 내려간다.
# 타입 스펙: type-layers — 프로토콜 → 하드웨어 → 소프트웨어로 관심이 옮겨 가는 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO


W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02",
       "아키텍처를 보는 다섯 갈래",
       "10-02 가 다루는 다섯 절. 프로토콜의 성능 기능에서 시작해 하드웨어 한계로, 다시 커널이 그 위에서 하는 일로 내려간다.",
       "10-01 이 개념이었다면 이 편은 그 개념을 떠받치는 프로토콜과 구조입니다")

BANDS = [
    ("§1", "TCP 성능 기능", "슬라이딩 윈도 · 혼잡 제어 · SACK", "높은 RTT 를 이긴다", None),
    ("§2", "TCP 상태 · UDP · QUIC", "TIME_WAIT · 무상태 · 0-RTT", "연결을 관리하고 대안을 둔다", None),
    ("§3", "하드웨어", "인터페이스 · 컨트롤러 · 스위치 · 방화벽", "어느 것이든 병목이 된다", None),
    ("§4", "Linux 네트워크 스택", "연결 큐 · 버퍼 · GSO/TSO/GRO", "오버헤드를 줄인다", ACC),
    ("§5", "CPU 스케일링 · 커널 바이패스", "RSS/RPS/RFS · NAPI · DPDK/XDP", "패킷율을 끌어올린다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "프로토콜", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "커널", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "세 층 어디서든 병목이 생길 수 있어, 성능 특성을 층마다 따로 봅니다", 13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("커널이 오버헤드를 줄이는 절", ACC), ("나머지 절", MUTED)])
d.save("10-02.chapter-overview.svg")
