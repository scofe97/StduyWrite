# 10-02 §2 — TCP·UDP·QUIC 은 무엇을 주고 무엇을 포기하는가.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(무엇을 주나 · 무엇을 포기하나 · 어디에 쓰나)이
#           반복되는 대조 지도다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 512
CW, CH, GAP, X0, Y = 280, 220, 24, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §2",
       "TCP · UDP · QUIC — 무엇을 주고 무엇을 포기하나",
       "세 전송 프로토콜의 성능 맞교환. UDP 가 버린 것을 QUIC 이 유저 공간에서 다시 구현했다.",
       "QUIC 은 TCP 의 기능을 UDP 의 유연성 위에 다시 올린 것입니다")

CARDS = [
    ("TCP", "신뢰성 있는 연결의 표준", OK,
     ["슬라이딩 윈도로 높은 RTT 에서도", "처리량을 냅니다.", "혼잡 제어로 안정적입니다"],
     ["포기: 핸드셰이크 지연", "커널에 박혀 진화가 느림"]),
    ("UDP", "메시지를 그냥 보낸다", INFO,
     ["작은 헤더 · 무상태 · 무재전송.", "연결 오버헤드가 낮고", "TCP 의 큰 지연을 피합니다"],
     ["포기: 신뢰성 · 순서", "혼잡 회피가 없음"]),
    ("QUIC", "UDP 위에 다시 올린 기능", ACC,
     ["한 연결에 여러 스트림,", "0-RTT 핸드셰이크,", "주소가 바뀌어도 연결 유지"],
     ["얻음: 유저 공간이라", "빠르게 개선됨"]),
]

for i, (name, tag, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 15, c, KR, "start", 600)
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    d.line(x + 16, Y + 66, x + CW - 16, Y + 66, RULE, 0.8)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 92 + j * 20, line, 13, MUTED, KR, "start")
    for j, line in enumerate(foot):
        d.t(x + 16, Y + CH - 40 + j * 18, line, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "UDP 는 혼잡 제어가 없고 방화벽에 잘 막히지 않습니다. 그 위에 자체 신뢰성·혼잡 제어를 얹은 것이 QUIC 입니다",
    13, MUTED, KR, "start")
d.t(X0, YB + 24, "TCP 는 커널에 있어 배포가 느리지만, QUIC 은 애플리케이션과 함께 나가므로 개선 주기가 짧습니다",
    13, SOFT, KR, "start")

d.legend(YB + 48, [("유저 공간에서 진화하는 대안", ACC), ("신뢰성을 주는 쪽", OK), ("단순함을 주는 쪽", INFO)])
d.save("10-02.tcp-vs-udp-quic.svg")
