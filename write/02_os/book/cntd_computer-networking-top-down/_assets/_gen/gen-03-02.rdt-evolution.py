# 03-02 §1 — 원문 3.4.1 의 점증적 설계. 채널이 무엇을 망가뜨릴 수 있느냐에 따라 장치가 하나씩 붙는다.
# 각 칸의 세 슬롯(채널 가정 · 더한 장치 · 남은 문제)은 원문 서술 그대로다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯이 반복되고 왼쪽에서 오른쪽으로 흐른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
BW, BH, BY = 178, 250, 148
XS = [116, 314, 512, 710, 896]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §1",
      "채널을 의심할수록 장치가 붙습니다",
      "원문 3.4.1 이 프로토콜을 다섯 번 다시 짓는다. 각 단계에서 채널에 무엇을 더 허용하느냐가 다음 장치를 부른다.",
      "완성품을 보여 주는 대신 왜 필요한지를 순서로 보여 줍니다")

STEPS = [
    ("rdt1.0", "채널이 완벽하다", "없음", "되먹임조차 필요 없음", MUTED, False),
    ("rdt2.0", "비트가 뒤집힌다", "체크섬 · ACK · NAK\n재전송", "ACK 가 깨지면?", WARN, False),
    ("rdt2.1", "ACK·NAK 도 깨진다", "1비트 순서 번호", "NAK 이 꼭 필요한가", MUTED, False),
    ("rdt2.2", "같음", "NAK 제거\n번호를 담은 ACK", "패킷을 잃으면?", MUTED, False),
    ("rdt3.0", "패킷을 잃는다", "카운트다운 타이머", "맞지만 너무 느림", ACC, True),
]

for x, (name, chan, add, left, c, focal) in zip(XS, STEPS):
    if focal:
        d.tone(x - BW / 2, BY, BW, BH, c, 6, "14", 1.4)
    else:
        d.box(x - BW / 2, BY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x, BY + 30, name, 13, c if focal else INK, MONO, "middle", 600)
    d.line(x - BW / 2 + 14, BY + 44, x + BW / 2 - 14, BY + 44, RULE, 0.8)
    d.t(x, BY + 68, "채널 가정", 11, SOFT, MONO)
    d.t(x, BY + 90, chan, 11, INK, KR)
    d.t(x, BY + 126, "더한 장치", 11, SOFT, MONO)
    for i, ln in enumerate(add.split("\n")):
        d.t(x, BY + 148 + i * 20, ln, 11, c if focal else OK, KR)
    d.t(x, BY + 200, "남은 문제", 11, SOFT, MONO)
    d.t(x, BY + 222, left, 11, SOFT, KR)

for i in range(4):
    d.path(f"M {XS[i] + BW / 2 + 3} {BY + BH / 2} L {XS[i+1] - BW / 2 - 9} {BY + BH / 2}", MUTED, 1.2, m="ar")

d.t(24, 448, "TCP 는 이 다섯 단계에서 나온 장치를 거의 다 씁니다 — 체크섬·순서 번호·타이머·누적 ACK·중복 ACK 가 그것입니다.",
     11, MUTED, KR, "start")
d.t(24, 470, "다만 순서 번호가 패킷이 아니라 바이트를 세고, 창이 흐름 제어와 혼잡 제어 둘 다에 묶입니다.",
     11, MUTED, KR, "start")
d.t(24, 500, "rdt3.0 의 수신자 FSM 을 원문은 숙제로 남기는데, 답은 rdt2.2 의 수신자와 같습니다. 손실 처리의 부담을 전부 송신자에게 지웠기 때문입니다.",
     11, SOFT, KR, "start")

d.legend(H - 44, [("맞게 도는 첫 프로토콜", ACC), ("치명적 결함이 드러난 단계", WARN), ("중간 단계", MUTED)])
d.save("03-02.rdt-evolution.svg")
