# 02-01 자리가 없으면 선점한다 — priority 1000 새 Pod 가 낮은 Pod 를 내보내는 순서
# 본문: 큐 앞에 선 새 Pod(priority 1000)가 모든 노드에서 필터에 떨어지면 스케줄러는 노드 하나에서
#   priority 가 더 낮은 Pod(priority 0)를 골라 graceful 종료를 요청하고, 새 Pod 에
#   nominatedNodeName 을 적은 뒤 자리가 생기면 바인드한다. PDB 는 최선 노력일 뿐 보장되지 않는다.
# 타입 스펙: type-sequence — 세 주체(API 서버·kube-scheduler·kubelet)가 시간 순서로 메시지를 주고받는
#   흐름이라 레인과 메시지 화살표로 그린다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

def _lat(t): return all(ord(c) < 128 for c in t)

def msg(d, a, b, label, y, c, mk="ar", dash=None, sub=None):
    """ddx.msg 와 같되 부제를 11px 로 — 한글 하한(11px)을 지킨다."""
    x1, x2 = d.LX[a], d.LX[b]; s = 1 if x2 > x1 else -1
    d.path(f"M {x1+10*s} {y} L {x2-12*s} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 9, label, 11, c, MONO if _lat(label) else KR, "middle", 600)
    if sub: d.t(mx, y + 17, sub, 11, MUTED, MONO if _lat(sub) else KR)

def selfmsg(d, a, label, y, c, sub=None, w=58):
    x = d.LX[a]
    d.path(f"M {x+10} {y-10} L {x+w} {y-10} L {x+w} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
    d.t(x + w + 10, y - 4, label, 11, c, MONO if _lat(label) else KR, "start", 600)
    if sub: d.t(x + w + 10, y + 13, sub, 11, MUTED, KR, "start")

W, H = 1000, 684
d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "자리가 없으면 낮은 Pod 를 내보내고 들어갑니다",
      "priority 1000 새 Pod 가 필터에 모두 떨어지면 kube-scheduler 가 노드 하나에서 priority 0 Pod 를 골라 "
      "API 서버를 통해 종료시키고, 새 Pod 에 nominatedNodeName 을 적은 뒤 자리가 나면 바인드합니다.",
      lead="PodDisruptionBudget 은 최선 노력으로만 존중되며 선점을 막지 못합니다")

LX = ddx.lanes(d, [("kube-scheduler", "큐 · 필터 · 선점"),
                   ("API 서버", "etcd 에 기록"),
                   ("kubelet", "노드의 낮은 Pod")], y0=104, lane_w=200)
Y0 = d.lane_top + 44
STRIDE = 56
ys = [Y0 + i * STRIDE for i in range(8)]

msg(d, "API 서버", "kube-scheduler", "큐 앞 새 Pod", ys[0], INFO, sub="priority 1000")
selfmsg(d, "kube-scheduler", "필터 전부 실패", ys[1], BAD, sub="Insufficient memory")
selfmsg(d, "kube-scheduler", "희생 Pod 선택", ys[2], ACC, sub="노드 1곳 · priority 0")
msg(d, "kube-scheduler", "API 서버", "낮은 Pod 삭제", ys[3], ACC, mk="acc")
msg(d, "API 서버", "kubelet", "graceful 종료", ys[4], WARN, mk="warn", sub="종료 유예 기간 존중")
msg(d, "kube-scheduler", "API 서버", "nominatedNodeName", ys[5], INFO, mk="info", dash="5 4", sub="새 Pod 에 후보 노드 기록")
msg(d, "kubelet", "API 서버", "종료 완료", ys[6], OK, mk="ok", dash="5 4")
msg(d, "kube-scheduler", "API 서버", "바인드", ys[7], OK, mk="ok", sub="자리가 생긴 뒤")

d.rails_y = ys[7] + 36
for x in LX.values():
    d.line(x, d.lane_top + 6, x, d.rails_y, RULE, 1.0, "3 6")
ddx.state(d, "API 서버", "PDB 는 최선 노력", ys[3], WARN, dx=176)

d.legend(ys[7] + 56, [("선점 경로", ACC), ("요청", INFO), ("종료·실패", WARN), ("완료", OK)])
d.save("02-01.preemption.svg")
print("ok preemption")
