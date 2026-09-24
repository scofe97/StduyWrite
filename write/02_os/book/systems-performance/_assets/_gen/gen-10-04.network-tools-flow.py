# 10-04 §1 — 도구는 소켓에서 패킷으로 내려가고, 비용은 층의 순서가 아니라 이벤트 빈도가 정한다.
# 타입 스펙: type-layers — 관측 대상이 소켓 → 인터페이스 → 스택 → 연결 → 패킷으로 깊어지는 층 지도다.
#           축약: OSI 층이 아니라 관측 대상이라 인덱스 태그를 깊이 번호로 채운다.
# ⚠ 2026-09-23 적대적 검증: 왼쪽 축을 "싸다 → 비싸다" 로 적어 ss 가 인터페이스 카운터보다 싸다는 근거 없는 서열을 실었다.
#   원서 10.6 도입의 순서(전통 통계 → 트레이싱 → 패킷 캡처)로 바꾸고 비용은 이벤트 빈도로 설명한다.
# ⚠ 2026-09-22 도식 검증: 04 층을 "싸다"·"싼 층"으로 적어 정답 2 가 경고하는 오해(BPF 라서 모두 싸다)를 실었고,
#   sar 를 스택 집계에만 두어 %ifutil(인터페이스 지표)의 자리를 흐렸다. 비용은 이벤트 빈도, sar 는 -n DEV·-n TCP,ETCP 로 가른다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 592
BX, BW, BH, Y0, STRIDE = 148, 692, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-04 §1",
       "관측 도구는 소켓에서 패킷으로 내려간다",
       "원서의 순서대로 전통 통계에서 BPF 트레이싱, 패킷 캡처로 내려간다. 비용은 층의 순서보다 도구가 일하는 이벤트의 빈도가 정하고, 패킷마다 일하는 캡처가 가장 비싸다.",
       "가능하면 위쪽에서 끝내고, 아래로는 필요할 때만 내려갑니다")

BANDS = [
    ("01", "소켓", "ss", "어떤 연결이 무엇에 제약되나", None),
    ("02", "인터페이스", "ip · sar -n DEV · nicstat · ethtool", "에러 · 사용률 · 드라이버 설정", None),
    ("03", "스택 집계", "nstat · sar -n TCP,ETCP", "재전송율 같은 전체 지표 · 추세", None),
    ("04", "연결 이벤트 (BPF)", "tcplife · tcptop · tcpretrans", "커널 안 집계 · 이벤트 빈도만큼 비용", ACC),
    ("05", "커스텀 추적", "bpftrace", "질문을 직접 짠다", None),
    ("06", "패킷", "tcpdump · Wireshark", "가장 자세함 · 가장 비쌈", WARN),
]

for i, (n, name, tools, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, tools, 13, MUTED, MONO, "start")
    d.t(BX + BW - 20, y + 36, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 116, Y0 + 4, "전통 통계", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 116, Y0 + 5 * STRIDE + BH + 8, "패킷 캡처", 13, SOFT, KR, "start")

YB = Y0 + 5 * STRIDE + BH + 24
d.legend(YB, [("커널 안 집계 층", ACC), ("마지막 수단", WARN), ("전통 통계", MUTED)])
d.save("10-04.network-tools-flow.svg")
