# 10-02 §2 — TCP·UDP·QUIC 은 무엇을 주고 무엇을 포기하는가.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(무엇을 주나 · 무엇을 포기하나 · 어디에 쓰나)이
#           반복되는 대조 지도다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 420
CW, CH, GAP, X0, Y = 280, 220, 24, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §2",
       "TCP · UDP · QUIC — 무엇을 주고 무엇을 포기하나",
       "세 전송 프로토콜의 성능 맞교환. UDP 가 버린 신뢰성·혼잡 제어를 QUIC 이 UDP 위에서 다시 구현했다.",
       "QUIC 은 신뢰성·혼잡 제어·암호화를 UDP 위에 다시 올린 표준 전송입니다")

CARDS = [
    ("TCP", "신뢰성 있는 연결의 표준", OK,
     ["슬라이딩 윈도 · 버퍼링", "높은 RTT 에서도 처리량", "혼잡 제어로 안정"],
     ["대가: 핸드셰이크 지연", "손실 시 재전송 대기"]),
    ("UDP", "메시지를 그대로 보냄", INFO,
     ["작은 헤더 · 무상태", "무재전송 · 연결 비용 낮음", "주 용도: DNS"],
     ["포기: 신뢰성 · 순서", "혼잡 회피 없음"]),
    ("QUIC", "UDP 위에 다시 올린 기능", ACC,
     ["한 연결에 여러 스트림", "0-RTT(사전 통신 있을 때)", "주소가 바뀌어도 연결 ID 로 유지"],
     ["표준: RFC 9000 (2021)", "비신뢰 전송: 확장 RFC 9221"]),
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

YB = Y + CH + 32
d.legend(YB, [("UDP 위에 다시 올린 대안", ACC), ("신뢰성을 주는 쪽", OK), ("단순함을 주는 쪽", INFO)])
d.save("10-02.tcp-vs-udp-quic.svg")
