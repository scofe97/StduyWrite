# 01-02.tcp-open-3way — 3-way 핸드셰이크는 번호를 양방향으로 한 번씩 주고받는다
# 본문 요구(01-02 §3 "여는 쪽 — 3-way"): "화살표 라벨에 그 패킷이 나르는 번호와 보낸 직후 놓이는
#           상태를 함께 적었습니다" — 본문이 도식의 규격을 직접 적어 둔 자리라 라벨은 번호를,
#           레인 옆 칩은 그 직후의 상태를 맡는다. 그리고 "2번으로 줄이면 서버의 번호가 확인되지
#           않은 채 연결이 열린다"가 이 그림이 답하는 질문이라 리드로 올렸다.
#           마지막 두 칩이 같은 ESTABLISHED 인데 높이가 다른 것이 요점이다 — 클라이언트는 세 번째
#           패킷을 보내며 열리고 서버는 그것이 도착해야 열린다. 옆 주석 두 줄이 그 차이를 적는다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 상태는 레인 옆 칩이 받는다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, KR

W, H = 860, 566

d = Seq(W, H, "SEQUENCE · 01-02 TCP OPEN",
        "3-way 핸드셰이크 — 번호가 양방향으로 한 번씩 오간다",
        "TCP 3-way 핸드셰이크. 클라이언트가 seq=x를 보내면 서버가 ack=x+1로 확인하며 자기 번호 y를 "
        "함께 싣고, 클라이언트가 ack=y+1로 답한다. 클라이언트는 세 번째 패킷을 보내며 ESTABLISHED가 "
        "되지만 서버는 그 패킷이 도착해야 열린다.",
        lead="2번으로 줄이면 서버의 번호가 확인되지 않은 채 연결이 열립니다.")

C, S = "클라이언트", "서버"
LX = d.lanes([(C, "client"), (S, "server")])
MID = (LX[C] + LX[S]) / 2

# 시작 상태를 먼저 놓고 레일을 그 위에 긋는다 — 레일이 칩을 가르며 지나가야
# 칩이 레인에 붙어 있다는 것이 읽힌다.
d.state(S, "LISTEN", 164, INFO)
d.state(C, "CLOSED", 164, SOFT)
d.rails(476)

d.msg(C, S, "SYN  seq=x", 214, OK, "ok", sub="내 번호 x 를 알린다")
d.state(C, "SYN-SENT", 250, WARN)

d.msg(S, C, "SYN-ACK  seq=y, ack=x+1", 306, ACC, "acc",
      sub="x 확인 + 내 번호 y 를 함께 싣는다")
d.state(S, "SYN-RECEIVED", 342, WARN)

d.msg(C, S, "ACK  ack=y+1", 398, OK, "ok", sub="y 확인")
# 같은 상태인데 시점이 다르다 — 칩 높이가 그 시차다.
d.state(C, "ESTABLISHED", 440, OK)
d.state(S, "ESTABLISHED", 472, OK)
d.t(MID + 12, 440, "클라이언트가 먼저 열린다", 10, MUTED)
d.t(MID + 12, 472, "서버는 3번째가 도착해야 열린다", 10, MUTED)

d.legend(502, [("연결 요청·확인", OK), ("대기 상태", WARN), ("번호 두 개가 한 패킷에", ACC)])
d.save("01-02.tcp-open-3way.svg")
print("ok tcp-open-3way")
