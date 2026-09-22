# 10-01 §4 — 두 버퍼링은 자리가 다르고, 과할 때 나타나는 증상도 다르다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(어디에 있나 · 무엇을 흡수하나 · 과하면)이
#           반복되는 대조 지도다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
# ⚠ 2026-09-22 도식 검증: 백로그 카드에 "넘치면 SYN 드롭"으로 적어, 기본값(SYN cookies 켜짐)에서 SYN 큐가
#   넘쳐도 드롭하지 않는 경우를 지웠다. SYN 이 버려지는 것은 accept 큐가 찼거나 쿠키를 끈 채 SYN 큐가 찼을 때다(10-02 §4 표).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 500
CW, CH, GAP, X0, Y = 424, 228, 32, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §4",
      "두 버퍼링 — 떠받치는 것과 흡수하는 것",
      "데이터 버퍼링은 RTT 를 흡수해 처리량을 떠받치고, 백로그(SYN 큐·accept 큐)는 연결 폭주를 흡수한다. 둘 다 과하거나 차면 문제가 되지만 증상이 다르다.",
      "버퍼는 '충분하되 과하지 않게' 가 원칙입니다 — 과함의 증상이 둘로 갈립니다")

CARDS = [
    ("01", "데이터 버퍼링", "송신 · 수신 · 소켓 · 앱",
     ["ACK 를 기다리기 전에 더 보냄", "TCP: 슬라이딩 송신 윈도", "소켓 버퍼 · 앱 버퍼", "보낼 수 있는 양: min(cwnd, rwnd)"],
     "높은 RTT 흡수", INFO),
    ("02", "백로그 — 연결 요청의 줄", "커널 — SYN 큐 · accept 큐",
     ["핸드셰이크 전: SYN 큐", "accept 대기: accept 큐", "accept 큐가 차면 SYN 드롭",
      "SYN 큐가 차면 기본은 SYN cookies", "→ 드롭된 SYN 은 클라이언트가 재전송(1초+)"],
     "연결 폭주 흡수", ACC),
]

for i, (n, name, where, body, role, c) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    d.tone(x, Y, CW, CH, c, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" '
               f'fill="{c}" stroke="{c}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER, MONO)
    d.t(x + 48, Y + 29, name, 14, c, KR, "start", 600)
    d.t(x + 16, Y + 56, where, 13, MUTED, KR, "start")
    for j, line in enumerate(body):
        d.t(x + 16, Y + 84 + j * 20, line, 13, MUTED, KR, "start")
    d.line(x + 16, Y + CH - 40, x + CW - 16, Y + CH - 40, RULE, 0.8)
    d.t(x + 16, Y + CH - 18, role, 13, c, KR, "start", 600)

# 과하면 — 두 갈래
YB = Y + CH + 36
d.t(X0, YB, "과하면", 13, SOFT, KR, "start", 600)
d.box(X0 + 64, YB - 20, CW - 64, 60, PAPER2, RULE, 1.0, 6)
d.t(X0 + 80, YB + 2, "버퍼블로트", 13, WARN, KR, "start", 600)
d.t(X0 + 80, YB + 24, "중간 노드(스위치·라우터)의 과버퍼 → 긴 큐 대기", 13, MUTED, KR, "start")
d.box(X0 + CW + GAP, YB - 20, CW, 60, PAPER2, RULE, 1.0, 6)
d.t(X0 + CW + GAP + 16, YB + 2, "SYN 드롭 · 재전송", 13, WARN, KR, "start", 600)
d.t(X0 + CW + GAP + 16, YB + 24, "과부하 후보 · 서버 큐 카운터로 확인", 13, MUTED, KR, "start")

d.legend(YB + 64, [("연결 폭주를 흡수하는 자리", ACC), ("처리량을 떠받치는 자리", INFO), ("과하거나 찰 때의 증상", WARN)])
d.save("10-01.buffering-and-backlog.svg")
