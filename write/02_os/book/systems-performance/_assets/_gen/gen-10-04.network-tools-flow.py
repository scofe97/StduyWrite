# 10-04 §1 — 도구는 소켓에서 패킷으로 내려가고, 내려갈수록 비싸진다.
# 타입 스펙: type-layers — 관측 대상이 소켓 → 인터페이스 → 스택 → 연결 → 패킷으로 깊어지는 층 지도다.
#           축약: OSI 층이 아니라 관측 대상이라 인덱스 태그를 깊이 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 636
BX, BW, BH, Y0, STRIDE = 148, 692, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-04 §1",
       "관측 도구는 소켓에서 패킷으로 내려간다",
       "무엇을 보는지에 따라 도구가 갈리고, 아래로 갈수록 자세하지만 비싸진다. 패킷 캡처는 가장 아래이자 마지막 수단이다.",
       "가능하면 위쪽에서 끝내고, 아래로는 필요할 때만 내려갑니다")

BANDS = [
    ("01", "소켓", "ss", "어떤 연결이 무엇에 제약되나", None),
    ("02", "인터페이스", "ip · nicstat · ethtool", "에러 · 사용률 · 드라이버 설정", None),
    ("03", "스택 집계", "nstat · sar", "재전송율 같은 전체 지표 · 추세", None),
    ("04", "연결 이벤트 (BPF)", "tcplife · tcptop · tcpretrans", "커널 안에서 집계해 싸다", ACC),
    ("05", "커스텀 추적", "bpftrace", "질문을 직접 짠다", None),
    ("06", "패킷", "tcpdump · Wireshark", "가장 자세하고 가장 비싸다", WARN),
]

for i, (n, name, tools, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, tools, 13, MUTED, MONO, "start")
    d.t(BX + BW - 20, y + 36, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 108, Y0 + 4, "싸다", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 116, Y0 + 5 * STRIDE + BH - 8, "비싸다", 13, SOFT, KR, "start")

YB = Y0 + 6 * STRIDE + 36
d.t(BX - 116, YB, "ss·ip·nstat 은 iproute2 라 최신 커널 기능을 가장 잘 따라갑니다. ifconfig·netstat 은 deprecated 입니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("커널 안 집계로 싼 층", ACC), ("마지막 수단", WARN), ("전통 통계", MUTED)])
d.save("10-04.network-tools-flow.svg")
