# 01-02.tcp-close-paths — 연결을 닫는 두 길, 합의로 닫거나 통보로 끊거나
# 본문 요구(01-02 §3 "닫는 쪽 — 4-way와 RST"): 4-way 는 양쪽이 각각 FIN 을 보내고 서로 확인하는
#           합의 절차이고, RST 는 그 절차를 통째로 건너뛴다. 두 길을 한 장에 담되 시간 축을 쓰는
#           것은 4-way 뿐이라 RST 는 아래 띠 한 칸으로 요약했다 — 절차가 없다는 것이 요점이므로
#           그릴 순서 자체가 없다. 띠 오른쪽 "절차 없음" 칩이 그 대비를 받는다.
#           CLOSE-WAIT 와 TIME-WAIT 에 주석을 단 것은 본문이 둘을 따로 짚기 때문이다 —
#           CLOSE-WAIT 는 상대가 아니라 자기 앱을 기다리는 상태이고, TIME-WAIT 는 포트를 붙잡아
#           임시 포트 고갈로 이어진다. 이 편의 2MSL 절이 그 뒤를 잇는다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 상태는 레인 옆 칩이 받는다.
#           아래 RST 띠는 시퀀스가 아니라 대조용 각주라 레일 밖에 둔다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import Seq, INK, MUTED, SOFT, ACC, OK, WARN, BAD, KR

W, H = 980, 732

d = Seq(W, H, "SEQUENCE · 01-02 TCP CLOSE",
        "연결을 닫는 두 길 — 합의로 닫거나 통보로 끊거나",
        "TCP 연결을 닫는 두 경로. 위쪽 4-way는 양쪽이 각각 FIN을 보내고 서로 확인해 버퍼의 데이터가 "
        "전부 전달된다. 아래쪽 RST는 확인 응답 없이 그 자리에서 연결을 지우며 미전달 데이터는 버려진다.",
        lead="FIN 은 절차를 밟고 RST 는 절차를 건너뜁니다.")

A, B = "먼저 닫는 쪽", "상대"
LX = d.lanes([(A, "active close"), (B, "passive close")])
MID = (LX[A] + LX[B]) / 2

d.rails(536)
d.state(A, "ESTABLISHED", 164, OK)
d.state(B, "ESTABLISHED", 164, OK)

d.msg(A, B, "FIN", 212, WARN, "warn", sub="보낼 것 다 보냈다")
d.state(A, "FIN-WAIT-1", 246, WARN)

d.msg(B, A, "ACK", 292, OK, "ok", sub="알겠다 — 여기서 끝나지 않는다")
d.state(A, "FIN-WAIT-2", 326, WARN)
d.state(B, "CLOSE-WAIT", 326, ACC)
d.t(MID + 12, 354, "CLOSE-WAIT 는 상대가 아니라 자기 사정을 기다린다", 10, ACC)

d.msg(B, A, "FIN", 396, WARN, "warn", sub="나도 다 했다")
d.state(B, "LAST-ACK", 430, WARN)

d.msg(A, B, "ACK", 476, OK, "ok")
d.state(A, "TIME-WAIT", 510, BAD)
d.state(B, "CLOSED", 510, SOFT)
d.t(MID + 12, 534, "TIME-WAIT 가 포트를 붙잡아 임시 포트 고갈로 이어진다", 10, BAD)

# 다른 길 — 순서가 없어서 레일 밖에 띠로 둔다
d.tone(12, 570, 920, 96, BAD, 6, "0E", 1.3)
d.t(30, 596, "다른 길 — RST 통보", 12, BAD, KR, "start", 600)
d.t(30, 620, "확인 응답 없이 그 자리에서 연결 삭제 · 미전달 데이터는 버려진다", 11, INK, KR, "start")
d.t(30, 644, "열린 적 없는 포트 · 죽은 프로세스 · 정리된 연결에 뒤늦게 도착한 패킷",
    10, MUTED, KR, "start")
d.chip(830, 604, "절차 없음", BAD)

d.legend(688, [("종료 요청 FIN", WARN), ("확인 ACK", OK),
               ("자기 사정 대기", ACC), ("포트 점유·강제 종료", BAD)])
d.save("01-02.tcp-close-paths.svg")
print("ok tcp-close-paths")
