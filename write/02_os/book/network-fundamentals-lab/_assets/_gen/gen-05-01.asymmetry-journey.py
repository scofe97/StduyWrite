# 05-01 §4 — 리턴만 NAT 를 스칠 때 SYN-ACK 의 소스가 바뀌는 여정.
# 타입 스펙: type-sequence — 참여자 레인 사이를 시간 순으로 오가는 메시지가 본체다.
#           같은 핸드셰이크의 각 걸음이 어느 장비를 지나는지가 이 그림의 논점이라 시퀀스를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, BAD, OK, WARN, KR, MONO

W, H = 880, 460
d = Seq(W, H, "NETWORK FUNDAMENTALS LAB · 05-01 §4",
        "타임아웃인데 무응답이 아니다",
        "포워드는 NAT 를 거치지 않고 리턴만 거친다. NAT 가 소스를 재작성하면 클라이언트는 접속한 적 없는 주소에서 온 SYN-ACK 를 받는다.",
        "판별은 하나뿐 — 클라이언트에서 SYN-ACK 의 소스를 본다")

d.lanes([("cli", "10.11.1.10"), ("nat", "10.11.4.1"), ("srv", "10.11.2.10")], y0=104, lane_w=210)
d.rails(396)

d.msg("cli", "srv", "SYN", 190, OK, "ok", sub="포워드는 nat 을 거치지 않는다")
d.msg("srv", "nat", "SYN-ACK  src=srv", 236, MUTED, "ar", sub="리턴만 nat 으로 간다")
d.msg("nat", "cli", "SYN-ACK  src=nat", 288, BAD, "bad", sub="소스가 재작성됐다")
d.msg("cli", "nat", "RST", 332, BAD, "bad", sub="커널: 접속한 적 없는 상대")
d.msg("cli", "srv", "SYN (retry)", 376, WARN, "warn", sub="원래 시도는 타임아웃으로 끝난다")

d.t(24, 436, "서버는 요청 수신과 응답 발신이 모두 정상이라 무죄로 보인다 — 원인은 중간 라우터의 라우트 한 줄",
    12, ACC, KR, "start", 600)
d.save("05-01.asymmetry-journey.svg")
