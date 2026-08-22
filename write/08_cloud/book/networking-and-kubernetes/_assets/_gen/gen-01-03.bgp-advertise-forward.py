# 01-03.bgp-advertise-forward — 2구간 분리 (광고 시간 / 전달 시간)
# 본문: "두 시간이 갈린다 — 광고는 평소에, 전달은 표를 흘끗"
# 타입 스펙: type-sequence.md — 시간이 둘로 갈리므로 한 시간축이 아니라 구간 둘로 나눈다.
#           광고(평소)는 dashed, 전달(패킷이 올 때)은 solid.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 648
d = Seq(W, H, "BGP · ADVERTISE vs FORWARD",
        "광고와 전달은 다른 시간에 일어난다",
        "위 구간은 패킷과 무관하게 평소에 오가며 표를 채우고, 아래 구간은 그 표를 흘끗 보는 것으로 끝난다",
        lead="위 구간은 평소에 표를 채우고, 아래 구간은 그 표를 흘끗 보는 것으로 끝난다")

LX = ddx.lanes(d, [("AS 100", "출발지 관할"), ("AS 200", "중간 사업자"), ("AS 300", "목적지 관할")],
               y0=104, lane_w=212)
A1, A2, A3 = LX["AS 100"], LX["AS 200"], LX["AS 300"]
SEG1, SEG2 = (164, 316), (332, 552)
Y_RAILS = 580

ddx.band(d, *SEG1, "평소 — 패킷과 무관하게 광고가 오가며 표가 채워진다", focal=True)
ddx.band(d, *SEG2, "패킷이 올 때 — 채워 둔 표에서 다음 하나만 고른다")
d.rails(Y_RAILS)

def msg(a, b, y, label, c, mk, dash=None, anchor=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    if anchor == "start":
        d.t(a + 18, y - 12, label, 12, c, KR, "start", 600)
    elif anchor == "end":
        d.t(a - 18, y - 12, label, 12, c, KR, "end", 600)
    else:
        d.t((a + b) // 2, y - 12, label, 12, c, KR, "middle", 600)

# ① 광고 — 목적지 쪽에서 거슬러 올라오며 표를 채운다
msg(A3, A2, 240, "150.10.0.0/16 은 우리 관할이다", INFO, "info", "6 5")
msg(A2, A1, 288, "150.10.0.0/16 은 나를 거치면 닿는다", INFO, "info", "6 5")

# ② 전달 — 한 홉씩, 전체 경로를 아는 곳은 없다
msg(A1, A2, 408, "목적지 150.10.2.30 · 전체 경로는 모른 채 넘긴다", INK, "ar")
msg(A2, A3, 456, "채워 둔 표에서 다음 AS 를 고른다", INK, "ar")
msg(A3, A1, 520, "도착 — 어느 AS 도 전체 경로를 갖고 있지 않았다", OK, "ok", "6 5", "end")

d.legend(Y_RAILS + 20, [("평소의 광고", INFO), ("패킷 전달", INK), ("도착", OK)])
d.save("01-03.bgp-advertise-forward.svg")
print("ok bgp")
