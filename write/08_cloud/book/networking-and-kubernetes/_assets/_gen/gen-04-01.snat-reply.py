# 04-01.snat-reply — 나갈 때 바꾼 쌍을 돌아올 때 conntrack 이 되돌린다
# 본문 요구: "Pod 가 보낸 10.244.2.2:45678 을 노드가 192.168.148.4:61234 로 바꿔 내보내고, 답장은 목적지가
#           192.168.148.4:61234 인 채 돌아온다 — 커널이 5-tuple 로 conntrack 항목을 찾아 목적지를 되돌린 뒤 Pod 에 넘긴다"
# 타입 스펙: type-sequence.md — 시간순 왕복이고 참여자가 셋이라 시퀀스로 그린다. 돌아오는 구간(목적지 복원)에만 focal 을 건다.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = Seq(W, H, "SNAT REPLY · WHO RESTORES THE DESTINATION",
        "나갈 때 출발지를 바꾸고, 돌아올 때 목적지를 되돌린다",
        "Pod 의 출발지 10.244.2.2:45678 은 노드를 지나며 192.168.148.4:61234 로 바뀐다. 답장은 바뀐 쌍을 목적지로 달고 돌아오고, 커널이 conntrack 항목으로 원래 쌍을 찾아 목적지를 되돌린다.",
        lead="바꾼 쌍과 원래 쌍을 conntrack 항목 하나가 함께 들고 있다")

LX = ddx.lanes(d, [("Pod", "10.244.2.2"), ("노드", "SNAT · conntrack"), ("밖의 서버", "클러스터 밖")], y0=104, lane_w=212)
POD_, NODE_, SRV = (int(LX[k]) for k in ("Pod", "노드", "밖의 서버"))
SEGS = [(164, 336, "1 · 나갈 때 · 출발지를 바꾼다", False),
        (348, 520, "2 · 돌아올 때 · 목적지를 되돌린다", True)]
Y_END = 528
for a, b, lab, f in SEGS: ddx.band(d, a, b, lab, focal=f)
d.rails(Y_END)


def msg(a, b, y, label, c, mk, dash=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    d.t((a + b) // 2, y - 12, label, 11, c, KR, "middle", 600)


def selfmsg(a, y, label, sub, c, mk):
    d.path(f"M {a+10} {y-10} L {a+58} {y-10} L {a+58} {y+10} L {a+13} {y+10}", c, 1.4, m=mk)
    d.t(a + 70, y - 4, label, 11, c, KR, "start", 600)
    d.t(a + 70, y + 13, sub, 11, MUTED, KR, "start")


msg(POD_, NODE_, 212, "출발지 10.244.2.2:45678", INFO, "info")
selfmsg(NODE_, 260, "conntrack 에 두 쌍 기록", "원래 쌍과 바꾼 쌍을 한 항목에", MUTED, "ar")
msg(NODE_, SRV, 308, "출발지 192.168.148.4:61234", INFO, "info")
msg(SRV, NODE_, 396, "목적지 192.168.148.4:61234", MUTED, "ar", "6 5")
selfmsg(NODE_, 446, "5-tuple 로 항목 찾기", "목적지를 원래 쌍으로 되돌림", ACC, "acc")
msg(NODE_, POD_, 496, "목적지 10.244.2.2:45678", ACC, "acc")

d.legend(Y_END + 24, [("나가는 쪽", INFO), ("목적지를 되돌리는 구간", ACC)])
d.save("04-01.snat-reply.svg")
print("ok snat-reply")
