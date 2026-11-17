# 10-01 drain 과 PDB — 허용 수가 0 이면 축출이 끝나지 않는다
# 본문: kubectl drain 은 노드를 cordon 한 뒤 Pod 마다 Eviction API 를 호출한다. API 서버는 PDB 의
#   disruptionsAllowed 를 보고 허용하면 200, 모자라면 429 를 돌려준다. replicas 3 + minAvailable 2 에서는
#   새 Pod 가 Ready 가 되면 재시도가 통과하지만, replicas 1 + minAvailable 1 은 허용 수가 영원히 0 이라
#   429 가 끝없이 반복된다.
# 타입 스펙: type-sequence — drain·API 서버·PDB 세 참여자가 시간 순으로 요청과 응답을 주고받는다.
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

W, H = 960, 968
d = Seq(W, H, "KUBERNETES PATTERNS · 10-01",
        "drain 의 축출 요청을 PDB 가 걸러냅니다",
        "kubectl drain 이 노드를 cordon 하고 Pod 마다 Eviction API 를 호출하면 API 서버는 PDB 의 disruptionsAllowed 를 봅니다. replicas 3 에 minAvailable 2 면 하나는 허용하고 다음 요청은 429 로 거부하며, "
        "새 Pod 가 Ready 가 되면 재시도가 통과합니다. replicas 1 에 minAvailable 1 이면 허용 수가 0 이라 429 가 반복되고 drain 이 끝나지 않습니다.",
        lead="PDB 는 허용 수만 계산하므로 싱글턴에 걸면 그 Pod 는 축출되지 않습니다")

ddx.lanes(d, [("kubectl drain", "node-a"), ("API 서버", "Eviction API"), ("PDB", "minAvailable: 2")],
          y0=96, lane_w=200)
STRIDE = 56
Y0 = 196
def y(n): return Y0 + n * STRIDE
BOT = Y0 + 8 * STRIDE + 38 + 212
d.rails(BOT)

# 구간 1 — replicas 3
d.t(24, y(0) - 22, "replicas 3 · minAvailable 2 — 허용 수 1", 13, INFO, KR, "start", 600)
_msg(d, "kubectl drain", "API 서버", "cordon node-a", y(0) + 18, c=MUTED, mk="ar")
_msg(d, "kubectl drain", "API 서버", "evict pod-a", y(1) + 18, c=INFO, mk="info", sub="Ready 3")
_msg(d, "API 서버", "PDB", "disruptionsAllowed 확인", y(2) + 18 - 4, c=INFO, mk="info")
_msg(d, "API 서버", "kubectl drain", "200 허용", y(3) + 6, c=OK, mk="ok", dash="4 3")
_msg(d, "kubectl drain", "API 서버", "evict pod-b", y(4) + 6, c=INFO, mk="info", sub="Ready 2")
_msg(d, "API 서버", "kubectl drain", "429 거부", y(5) + 6, c=WARN, mk="warn", dash="4 3", sub="허용 수 0")
ddx.state(d, "API 서버", "새 Pod Ready", y(6) + 6, OK)
_msg(d, "kubectl drain", "API 서버", "evict pod-b 재시도", y(7) + 4, c=INFO, mk="info")
_msg(d, "API 서버", "kubectl drain", "200 허용", y(8) - 2, c=OK, mk="ok", dash="4 3")

# 구간 2 — 싱글턴
SEP = y(8) + 38
d.line(24, SEP, W - 48, SEP, RULE, 0.8)
d.t(24, SEP + 28, "replicas 1 · minAvailable 1 — 허용 수 0", 13, BAD, KR, "start", 600)
_msg(d, "kubectl drain", "API 서버", "evict pod-s", SEP + 66, c=INFO, mk="info")
_msg(d, "API 서버", "kubectl drain", "429 거부", SEP + 100, c=BAD, mk="bad", dash="4 3", sub="허용 수 0")
ddx.selfmsg(d, "kubectl drain", "같은 요청 반복", SEP + 148, c=BAD)
ddx.state(d, "kubectl drain", "drain 끝나지 않음", SEP + 192, BAD)

d.legend(SEP + 236, [("허용", OK), ("거부 · 조건부", WARN), ("조회 · 요청", INFO), ("싱글턴 거부", BAD)])

d.save("10-01.pdb-drain.svg")
print("ok pdb-drain")
