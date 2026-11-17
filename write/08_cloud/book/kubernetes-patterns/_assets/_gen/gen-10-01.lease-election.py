# 10-01 Lease 리더 선출 — 낙관적 잠금으로 하나만 이긴다
# 본문: pod-1 이 Lease my-app-leader 를 만들고 renewTime 을 주기적으로 갱신한다. pod-1 이 멈추면
#   renewTime + leaseDurationSeconds 가 지난 뒤 pod-2 와 pod-3 이 같은 resourceVersion 으로
#   holderIdentity 를 바꾸려 한다. API 서버는 먼저 도착한 하나만 받고 나머지는 409 Conflict 로 돌려보낸다.
# 타입 스펙: type-sequence — 참여자 넷이 시간 순으로 요청을 주고받고, 같은 순간 두 요청의 응답이 갈린다.
import sys; sys.path.insert(0, ".")
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

def _msg(d, a, b, label, y, c=None, mk="ar", dash=None, sub=None):
    # ddx.msg 는 한글 부제를 10px 로 찍어 하한(11px)을 어긴다 — 부제는 여기서 11px 로 찍는다
    ddx.msg(d, a, b, label, y, c=c, mk=mk, dash=dash)
    if sub:
        mx = (d.LX[a] + d.LX[b]) / 2
        lat = all(ord(ch) < 128 for ch in sub)
        d.t(mx, y + 16, sub, 11, MUTED, MONO if lat else KR)

W, H = 960, 800
d = Seq(W, H, "KUBERNETES PATTERNS · 10-01",
        "Lease 하나를 두고 pod 셋이 겨룹니다",
        "pod-1 이 Lease my-app-leader 를 만들고 renewTime 을 갱신하다가 멈춥니다. leaseDurationSeconds 가 지나면 pod-2 와 pod-3 이 같은 resourceVersion 으로 holderIdentity 를 바꾸려 하고, "
        "API 서버는 먼저 도착한 pod-2 의 update 만 받고 pod-3 에는 409 Conflict 를 돌려줍니다.",
        lead="잠금은 Lease 객체이고, 하나만 이기게 하는 것은 resourceVersion 비교입니다")

ddx.lanes(d, [("pod-1", "리더"), ("API 서버", "Lease my-app-leader"), ("pod-2", "대기"), ("pod-3", "대기")],
          y0=96, lane_w=176)
STRIDE = 56
Y0 = 196
def y(n): return Y0 + n * STRIDE
d.rails(y(9) + 20)

# 1 획득과 갱신
_msg(d, "pod-1", "API 서버", "create Lease", y(0), c=OK, mk="ok", sub="holderIdentity: pod-1")
_msg(d, "API 서버", "pod-1", "201 Created", y(1) + 4, c=OK, mk="ok", dash="4 3")
_msg(d, "pod-1", "API 서버", "update renewTime", y(2) + 8, c=OK, mk="ok", sub="주기적으로 반복")
# 2 중단
ddx.state(d, "pod-1", "pod-1 중단", y(3) - 6, BAD)
d.t(d.LX["pod-1"] + 110, y(3) - 2, "갱신 끊김", 12, MUTED, KR, "start")
# 3 대기 Pod 가 만료 확인
_msg(d, "pod-2", "API 서버", "get Lease", y(4), c=INFO, mk="info",
        sub="renewTime + 15초 경과 확인")
# 4 같은 resourceVersion 으로 동시에 update
_msg(d, "pod-2", "API 서버", "update holderIdentity: pod-2", y(5), c=WARN, mk="warn", sub="resourceVersion: 4182")
_msg(d, "pod-3", "API 서버", "update holderIdentity: pod-3", y(6) + 18, c=WARN, mk="warn", sub="resourceVersion: 4182")
# 5 응답이 갈린다
_msg(d, "API 서버", "pod-2", "200 OK", y(7) + 18, c=OK, mk="ok")
_msg(d, "API 서버", "pod-3", "409 Conflict", y(8) + 18, c=BAD, mk="bad")
# 마무리 상태
ddx.state(d, "pod-2", "새 리더", y(9) + 10, ACC)
ddx.state(d, "pod-3", "계속 대기", y(9) + 10, MUTED)

d.legend(y(9) + 52, [("성공", OK), ("대기 Pod 요청", WARN), ("조회", INFO), ("충돌 · 중단", BAD), ("새 리더", ACC)])

d.save("10-01.lease-election.svg")
print("ok lease-election")
