# 10-04 전체 지도 — 전통 통계에서 BPF 트레이싱, 마지막에 패킷 캡처, 그리고 도구를 잇는 사례.
# 타입 스펙: type-layers — 다섯 절이 통계 → 트레이싱 → 캡처로 정밀도와 비용이 함께 오르는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
#           §6 사례는 깊이 축이 아니라 앞 절 도구를 잇는 자리라 한 stride 에 16 을 더 띄워 둔다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 628
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-04",
       "관측 도구를 꺼내는 다섯 갈래와 한 사례",
       "10-04 가 다루는 여섯 절. 전통 통계에서 BPF 이벤트 트레이싱으로, 마지막에 패킷 캡처로 내려가고, §6 에서 그 도구들로 한 사례를 끝까지 따라간다.",
       "10-03 의 방법론을 손에 든 연장으로 옮기는 편입니다")

BANDS = [
    ("§1", "ss · ip · nstat", "소켓 · 인터페이스 · 스택 통계", "분석의 출발점", None),
    ("§2", "sar · nicstat · ethtool", "시계열 · 사용률 · 드라이버", "추세와 USE 지표", None),
    ("§3", "tcplife · tcptop · tcpretrans", "연결 수명 · top · 재전송", "BPF 로 싸게 본다", ACC),
    ("§4", "bpftrace", "소켓 · TCP · 패킷 층 추적", "질문을 직접 짠다", None),
    ("§5", "tcpdump · Wireshark", "패킷 캡처와 그래픽 검사", "마지막 수단", WARN),
    ("§6", "사례 — 연결이 1초씩 늦을 때", "connect 시간 → nstat → bpftrace → ss · nstat(서버)", "원인 후보를 좁힌다", INFO),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE + (16 if i == 5 else 0)
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "통계", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "패킷", 13, SOFT, KR, "middle")

d.legend(Y0 + 6 * STRIDE + 36, [("커널 안 집계로 싼 절", ACC), ("마지막 수단", WARN), ("도구를 잇는 사례", INFO), ("전통 통계", MUTED)])
d.save("10-04.chapter-overview.svg")
