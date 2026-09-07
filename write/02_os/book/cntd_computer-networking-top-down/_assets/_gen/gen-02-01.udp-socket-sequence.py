# 02-01 §5 — 원서 UDPClient.py / UDPServer.py 가 실제로 부르는 순서.
# 호출 이름과 인자는 원문 코드 그대로다. 곁줄은 원문이 그 줄을 설명하며 짚은 것 —
# 클라이언트 포트는 OS 가 붙이고, 목적지 주소는 sendto 가 붙이고, 회신 주소는 recvfrom 이 알려 준다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 시간은 위에서 아래로만 흐른다.
#
# 상태 칩(state)은 ASCII 만 담는다. dd.py 의 폭 계산이 문자당 7px 이라 한글을 넣으면 칩이 글자보다 좁아진다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO

W, H = 1000, 640

d = Seq(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §5",
        "UDP 소켓 — 누가 무엇을 붙이는가",
        "원서 UDPClient.py 와 UDPServer.py 의 호출 순서. 주소를 붙이는 주체가 줄마다 다르다.",
        "서버는 포트를 코드로 명시하고, 클라이언트는 OS 에게 맡깁니다")

d.lanes([("UDPClient.py", "socket · sendto · recvfrom"),
         ("UDPServer.py", "bind · recvfrom · sendto")])
d.rails(548)

# 서버가 먼저 떠 있어야 합니다
d.state("UDPServer.py", "socket(AF_INET, SOCK_DGRAM)", 176, INFO)
d.state("UDPServer.py", "bind(('', 12000))", 212, OK)
d.state("UDPServer.py", "recvfrom(2048) blocks", 248, MUTED)
d.t(742, 268, "포트를 개발자가 명시합니다", 11, SOFT, KR, "end")

d.selfmsg("UDPClient.py", "socket(AF_INET, SOCK_DGRAM)", 306,
          sub="포트 번호는 운영체제가 붙입니다")

d.msg("UDPClient.py", "UDPServer.py", "sendto(message, (host, 12000))", 372, ACC,
      sub="목적지 주소를 이 줄이 붙입니다")

d.state("UDPServer.py", "message.decode().upper()", 418, WARN)

d.msg("UDPServer.py", "UDPClient.py", "sendto(MSG, clientAddress)", 476, MUTED, dash="5 4",
      sub="회신 주소는 recvfrom 이 알려 준 것입니다")

d.selfmsg("UDPClient.py", "close()", 528, sub="소켓을 닫고 프로세스가 끝납니다")

d.t(12, 586, "출발지 주소도 패킷에 붙지만 그것은 애플리케이션 코드가 아니라 하위 운영체제가 자동으로 하는 일입니다.",
     11, MUTED, KR, "start")

d.legend(H - 40, [("요청", ACC), ("응답", MUTED), ("서버 쪽 상태", INFO)])
d.save("02-01.udp-socket-sequence.svg")
