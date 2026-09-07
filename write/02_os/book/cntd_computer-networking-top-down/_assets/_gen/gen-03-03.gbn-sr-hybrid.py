# 03-03 §6 — 원문이 절을 닫으며 던지는 물음. TCP 는 GBN 도 SR 도 아닌 겹치는 자리에 있다.
# 각 항목은 원문 3.5.4 마지막 절의 서술 그대로다.
# 타입 스펙: type-venn — 두 집합의 겹침. 겹치는 자리가 이 절의 요점이므로 그 하나만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
CY, R = 292, 208
LX, RX = 386, 614

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §6",
      "TCP 는 어느 쪽도 아닙니다",
      "누적 확인 응답과 단일 타이머는 GBN 쪽이고, 순서 밖 버퍼링과 선택적 재전송은 SR 쪽이다. TCP 는 둘의 혼종이다.",
      "원문이 절을 닫으며 스스로 던지는 물음에 대한 답입니다")

for cx, c in ((LX, INFO), (RX, OK)):
    d.o.append(f'<circle cx="{cx}" cy="{CY}" r="{R}" fill="{c}0e" stroke="{c}" stroke-width="1.3"/>')
d.t(LX - 96, CY - R + 34, "Go-Back-N", 13, INFO, KR, "middle", 600)
d.t(RX + 96, CY - R + 34, "Selective Repeat", 13, OK, KR, "middle", 600)

LEFT = ["확인 응답이 누적입니다", "순서 밖 세그먼트를", "개별 확인하지 않습니다", "", "송신자 변수가 둘뿐입니다", "SendBase · NextSeqNum"]
RIGHT = ["많은 구현이 순서 밖", "세그먼트를 버퍼링합니다", "", "타임아웃 때 많아야", "하나만 재전송합니다", "SACK 로 골라서 확인"]
for i, t in enumerate(LEFT):
    if t: d.t(LX - 116, CY - 54 + i * 26, t, 11, SOFT, KR)
for i, t in enumerate(RIGHT):
    if t: d.t(RX + 116, CY - 54 + i * 26, t, 11, SOFT, KR)

# 겹치는 자리
d.tone(LX + 44, CY - 62, RX - LX - 88, 124, ACC, 8, "1c", 1.4)
d.t((LX + RX) / 2, CY - 28, "TCP", 15, ACC, MONO, "middle", 600)
d.t((LX + RX) / 2, CY - 2, "원문의 결론", 11, SOFT, KR)
d.t((LX + RX) / 2, CY + 24, "GBN 과 SR 의", 11, ACC, KR)
d.t((LX + RX) / 2, CY + 44, "혼종", 11, ACC, KR)

d.t(20, 528, "ACK n 하나만 잃어버렸을 때 GBN 은 n 부터 N 까지 전부 다시 보내고, TCP 는 많아야 n 하나만 보냅니다. n+1 의 ACK 가 먼저 오면 그것조차 안 보냅니다.",
     11, MUTED, KR, "start")

d.legend(H - 52, [("두 쪽의 성질을 함께 가짐", ACC), ("GBN 쪽 성질", INFO), ("SR 쪽 성질", OK)])
d.save("03-03.gbn-sr-hybrid.svg")
