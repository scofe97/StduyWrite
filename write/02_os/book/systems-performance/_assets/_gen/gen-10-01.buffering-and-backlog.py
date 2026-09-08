# 10-01 §4 — 두 버퍼링은 자리가 다르고, 과할 때 나타나는 증상도 다르다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(어디에 있나 · 무엇을 흡수하나 · 과하면)이
#           반복되는 대조 지도다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 512
CW, CH, GAP, X0, Y = 424, 208, 32, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §4",
      "두 버퍼링 — 떠받치는 것과 흡수하는 것",
      "데이터 버퍼링은 RTT 를 흡수해 처리량을 떠받치고, 백로그는 연결 폭주를 흡수한다. 둘 다 과하면 문제가 되지만 증상이 다르다.",
      "버퍼는 '충분하되 과하지 않게' 가 원칙입니다 — 과함의 증상이 둘로 갈립니다")

CARDS = [
    ("01", "데이터 버퍼링", "송신·수신 양쪽 · 소켓 · 앱",
     ["ACK 를 기다리며 멈추기 전에", "더 보낼 수 있게 합니다.", "TCP 는 여기에 슬라이딩 송신", "윈도를 더해 처리량을 냅니다"],
     "높은 RTT 를 흡수한다", INFO),
    ("02", "백로그", "커널 — accept 이전의 SYN 큐",
     ["유저 프로세스가 accept 하기", "전까지 SYN 요청을 큐잉합니다.", "한도가 차면 SYN 이 드롭되고", "클라이언트가 재전송합니다"],
     "연결 폭주를 흡수한다", ACC),
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
    d.t(x + 16, Y + CH - 18, role, 12, c, KR, "start", 600)

# 과하면 — 두 갈래
YB = Y + CH + 36
d.t(X0, YB, "과하면", 13, SOFT, KR, "start", 600)
d.box(X0 + 64, YB - 20, CW - 64, 60, PAPER2, RULE, 1.0, 6)
d.t(X0 + 80, YB + 2, "버퍼블로트", 13, WARN, KR, "start", 600)
d.t(X0 + 80, YB + 24, "중간 노드(스위치·라우터)의 과버퍼 → 긴 큐 대기", 13, MUTED, KR, "start")
d.box(X0 + CW + GAP, YB - 20, CW, 60, PAPER2, RULE, 1.0, 6)
d.t(X0 + CW + GAP + 16, YB + 2, "SYN 드롭 · 재전송", 13, WARN, KR, "start", 600)
d.t(X0 + CW + GAP + 16, YB + 24, "호스트 과부하의 지표 — 연결 지연으로 나타난다", 13, MUTED, KR, "start")

d.t(X0, YB + 76, "버퍼링은 중간 노드가 아니라 엔드포인트가 맡는 게 낫다는 end-to-end 원칙이 그 배경입니다",
    13, MUTED, KR, "start")

d.legend(YB + 100, [("연결 폭주를 흡수하는 자리", ACC), ("처리량을 떠받치는 자리", INFO), ("과할 때의 증상", WARN)])
d.save("10-01.buffering-and-backlog.svg")
