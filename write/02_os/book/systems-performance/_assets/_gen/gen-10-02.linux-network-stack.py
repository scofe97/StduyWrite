# 10-02 §4 — 송신 경로에서 버퍼·큐·오프로드가 놓이는 자리.
# 타입 스펙: type-layers — 애플리케이션에서 NIC 로 내려가는 송신 경로의 층 지도다.
#           축약: OSI 층이 아니라 커널 컴포넌트라 인덱스 태그를 단계 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 568
BX, BW, BH, Y0, STRIDE = 140, 664, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §4",
       "송신 경로의 버퍼 · 큐 · 오프로드",
       "애플리케이션에서 NIC 까지 패킷이 내려가며 지나는 커널 컴포넌트. 각 층이 서로 다른 오버헤드를 줄인다.",
       "패킷은 struct sk_buff 로 이 컴포넌트들을 통과합니다")

BANDS = [
    ("01", "애플리케이션", "send() · sendmsg()", "자체 버퍼로 모아 보냅니다", None),
    ("02", "소켓 · TCP 송신 버퍼", "tcp_wmem 으로 동적 조정", "작은 전송의 오버헤드를 줄입니다", None),
    ("03", "GSO", "최대 64KB 슈퍼 패킷", "스택 통과 횟수를 줄입니다", ACC),
    ("04", "qdisc", "fq_codel 이 흔한 기본", "분류 · 스케줄링 · 셰이핑", None),
    ("05", "드라이버 · NIC (TSO)", "쪼개기를 하드웨어에 맡김", "CPU 대신 NIC 가 자릅니다", None),
]

for i, (n, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 36, role, 13, c if c else SOFT, KR, "end")

d.arrow([(BX + BW + 40, Y0 + 8), (BX + BW + 40, Y0 + 4 * STRIDE + BH - 4)], MUTED, "ar", 1.3)
d.t(BX - 92, Y0 + 140, "송신", 13, SOFT, KR, "start")

YB = Y0 + 5 * STRIDE + 8
d.t(BX - 116, YB, "수신 쪽에서는 GRO 가 GSO 의 짝으로, 작은 패킷을 모아 스택에 한 번에 올립니다", 13, MUTED, KR, "start")

d.legend(YB + 28, [("스택 오버헤드를 줄이는 자리", ACC), ("나머지 단계", MUTED)])
d.save("10-02.linux-network-stack.svg")
