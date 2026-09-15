# 04-04 §3 「ICMP 블랙홀은 알림을 막는 방화벽과 라우터가 만듭니다」 — 알림이 사라지는 네 자리.
# 타입 스펙: type-architecture — 문제 · 해결 도식과 같은 노드 자리를 쓰고, 아래 트랙 한 줄에 사라지는 자리 하나씩을 둔다.
#       순서가 아니라 경우라서 번호 대신 A~D 배지를 라우터 오른쪽 빈 칸에 두고, 화살표는 라우터에서 왼쪽으로만 간다.
# 출처: 원문 밖. 전부 1차 자료에서 가져왔다.
#       - ICMP 를 제대로 보내지 않는 라우터 · 모든 ICMP 를 막도록 잘못 설정한 방화벽: RFC 2923 §2.1
#       - 알림의 출발지 주소만 보고 모르는 흐름이라 버리는 상태 추적 장비 · 인용된 원본으로 가려야 함: RFC 8900 §3.8.2
#       - ECMP 앞단이 인용 안 헤더를 전달 결정에 쓰지 않아 알림이 흐름과 다른 다음 홉으로 갈 수 있음: RFC 7690 §2
#       - 패킷이 닿지 않는데 송신자가 모르는 상태를 블랙홀, 그중 PTB 를 못 받은 경우를 ICMP 블랙홀이라 부름: RFC 8899 §2
# 노트의 예시: 문제 도식과 같은 1500 · 1480 망. D 의 "송신자" 칸은 같은 서비스 주소를 나눠 받는 서버 무리를 줄여 그린 것이다.
# focal: 알림이 사라지는 X 넷 — 본문 표가 짚는 "알림이 사라지는 자리".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, OK, BAD, INFO, ACC, MUTED, SOFT, KR, MONO
from _cc_04_04_pmtu import (topology, send, badge, chip, cross, UP,
                            W, SND_CX, SND_X, SND_W, FW_CX, RT_CX, RT_X, RT_W, RCV_CX, DROP_X)

H = 600
TR = (288, 344, 400, 456)          # 경우 A~D 트랙 (stride 56)
CHIP_Y, LEGEND_Y = 504, 540

d = D(W, H, "ICMP · BLACK HOLE · WHERE ALERTS VANISH",
      "줄이라는 알림은 네 자리에서 사라집니다",
      "문제 도식과 같은 망에서 1500 바이트 패킷이 터널 입구에서 버려진다. 그 뒤 Packet Too Big 이 송신자에게 닿지 못하는 경우가 넷이다. "
      "A 라우터가 알림을 만들지 않는다. B 방화벽이 모든 ICMP 를 막는다. C 상태 추적 장비가 알림의 출발지 주소만 보고 모르는 흐름이라 버린다. "
      "D ECMP 앞단이 알림을 연결이 없는 다른 서버로 보낸다. 넷 모두 송신자에게는 블랙홀 연결로 보인다.",
      "큰 패킷이 버려진 뒤, 알림이 만들어지지 않거나 막히거나 버려지거나 엉뚱한 서버로 갑니다")

topology(d, "ICMP 필터", BAD, "터널 입구")

# 계기 · 큰 패킷이 터널 입구에서 버려짐
send(d, UP, SND_CX, DROP_X, BAD, drop=BAD)
d.t(SND_CX + 8, UP - 15, "1500 B · 다음 링크보다 큼 · 버림", 13, BAD, KR, "start", 600)

CASE_X = RT_X + RT_W + 28
ALERT_X = RT_CX - 8


def case(y, letter, label):
    badge(d, CASE_X, y - 4, letter, ACC)
    d.t(CASE_X + 18, y + 1, label, 13, ACC, KR, "start", 600)


# A · 알림을 만들지 않는 라우터
cross(d, RT_X - 14, TR[0], ACC)
d.t(RT_X - 30, TR[0] + 5, "알림 없음", 12, ACC, KR, "end", 600)
case(TR[0], "A", "라우터가 알림을 만들지 않음")

# B · 모든 ICMP 를 막는 방화벽
send(d, TR[1], ALERT_X, FW_CX, INFO, dash="5 4", drop=ACC)
d.t(FW_CX - 20, TR[1] + 5, "ICMP 전부 차단", 12, ACC, KR, "end", 600)
case(TR[1], "B", "방화벽이 ICMP 를 전부 막음")

# C · 출발지 주소만 보고 버리는 상태 추적 장비
send(d, TR[2], ALERT_X, FW_CX, INFO, dash="5 4", drop=ACC)
d.t(FW_CX - 20, TR[2] + 5, "모르는 흐름", 12, ACC, KR, "end", 600)
case(TR[2], "C", "출발지 주소만 보고 버림")

# D · ECMP 앞단이 연결 없는 서버로
send(d, TR[3], ALERT_X, SND_X + SND_W + 14, INFO, dash="5 4", drop=ACC)
d.t(SND_CX, TR[3] + 5, "다른 서버", 12, ACC, KR, "middle", 600)
case(TR[3], "D", "ECMP 가 연결 없는 서버로 보냄")

chip(d, SND_CX + 110, CHIP_Y, "넷 모두 블랙홀 연결로 보임", BAD)

d.legend(LEGEND_Y, [("버려진 패킷", BAD), ("Packet Too Big", INFO), ("알림이 사라진 자리 · 본문이 짚는 곳", ACC)])
d.t(960, H - 8, "RFC 2923 §2.1 · RFC 8900 §3.8.2 · RFC 7690 §2 · RFC 8899 §2", 8, SOFT, MONO, "end")
d.save("04-04.icmp-blackhole-causes.svg")
print("→ 04-04.icmp-blackhole-causes.svg")
