# 03-02 §2 — 같은 링크·같은 RTT 에서 정지 후 대기와 파이프라이닝의 시간표를 위아래로 잇는다.
# 본문 근거(값 그대로): d_trans = L/R = 8,000비트 / 10^9 bps = 8 마이크로초 = 0.008 ms,
#   RTT = 30 ms, "30.008 밀리초 중에 보내고 있던 시간이 0.008 밀리초입니다",
#   U = (L/R)/(RTT + L/R) = 0.00027, "셋을 미리 보낼 수 있게 하면 이용률이 사실상 세 배가 됩니다".
# 타입 스펙: type-sequence — 두 참여자 사이의 왕복이 시간순으로 쌓이고, 무엇을 기다리느라
#            언제 노는지가 세로 간격 그 자체로 드러난다.
#            축약: 전파 지연을 화살표 기울기로 그리지 않는다(dd-lint 가 사선을 막는다).
#                  대신 도착 시각을 라벨로 적는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 1000, 790
d = Seq(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §2",
        "같은 링크인데 하나는 놀고 하나는 찹니다",
        "1 Gbps · RTT 30 ms · 1,000바이트 패킷. 정지 후 대기는 30.008 ms 중 0.008 ms 만 보내고, "
        "파이프라이닝은 기다리기 전에 다음을 밀어 넣는다.",
        "고친 것은 링크가 아니라 기다리는 방식입니다")

d.lanes([("송신자", "sender"), ("수신자", "receiver")], y0=104, lane_w=260)
d.rails(616)
SX, RX = d.LX["송신자"], d.LX["수신자"]

d.t(24, 176, "정지 후 대기", 12, WARN, KR, "start", 600)
d.t(24, 194, "U = 0.00027", 11, SOFT, MONO, "start")
d.msg("송신자", "수신자", "pkt 0", 206, WARN, sub="t = 0 에 시작해 0.008 ms 에 다 밀어 넣습니다")
d.msg("수신자", "송신자", "ACK 0", 256, WARN, sub="마지막 비트 도착 t = 15.008 ms")
d.selfmsg("송신자", "wait", 306, SOFT, sub="이 29.992 ms 동안 링크는 비어 있습니다")
d.msg("송신자", "수신자", "pkt 1", 356, WARN, sub="t = 30.008 ms 에야 다음 패킷을 시작합니다")

d.line(24, 386, W - 24, 386, RULE, 0.8, "4 6")

d.t(24, 410, "파이프라이닝", 12, OK, KR, "start", 600)
d.t(24, 428, "U ≈ 0.0008", 11, SOFT, MONO, "start")
d.t(24, 456, "확인을 안 기다리고", 11, MUTED, KR, "start")
d.t(24, 476, "셋을 잇달아 보냅니다", 11, MUTED, KR, "start")
for i, y in enumerate((442, 470, 498)):
    d.msg("송신자", "수신자", f"pkt {i}", y, OK)
for i, y in enumerate((540, 568, 596)):
    d.msg("수신자", "송신자", f"ACK {i}", y, OK)

d.box(24, 636, W - 48, 76, PAPER2, RULE, 0.9, 6)
d.t(44, 662, "링크는 그대로입니다", 12, INK, KR, "start", 600)
d.t(44, 684, "바뀐 것은 '확인을 받고 나서 다음을 보낸다'는 규칙 하나입니다. 그 규칙을 풀면 같은 30 ms 안에 셋이 들어가고,",
    11, MUTED, KR, "start")
d.t(44, 702, "이용률도 그만큼 오릅니다. 대가는 순서 번호 범위·양쪽 버퍼·오류 대응 방식 셋이고 그것이 GBN 과 SR 을 가릅니다.",
    11, MUTED, KR, "start")

d.legend(H - 44, [("놀고 있는 구간", SOFT), ("정지 후 대기", WARN), ("파이프라이닝", OK)])
d.save("03-02.pipelining-timeline.svg")
print("ok pipelining-timeline")
