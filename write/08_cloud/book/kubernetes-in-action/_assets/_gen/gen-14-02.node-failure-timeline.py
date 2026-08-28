# 14-02 §3 — 장부와 실물이 어긋나 있는 구간
# 본문이 "Terminating 은 실제 종료가 아니라 삭제 표시"라고 따로 절을 뗀다. 시간축 하나로는
# 그 어긋남이 안 보이므로 장부(API 서버)와 실물(그 노드) 두 레인을 겹쳐 놓는다.
# 타입 스펙: type-gantt.md — 시간축 위의 구간 막대. 장부(API 서버가 아는 것)와 실물(노드에서 도는 것) 두 줄이 같은
#           시간대에 서로 어긋나 있다는 것이 논지라, 구간의 시작과 끝이 곧 값이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1260, 656, "KUBERNETES IN ACTION · 14-02",
      "장부에는 삭제 중, 컨테이너는 아직 돌고 있다",
      "노드와 연락이 끊겼는데 그 노드의 파드를 Terminating 으로 바꿀 수 있는 것은, 그 표시가 노드에서 "
      "일어나는 일이 아니기 때문이다. deletionTimestamp 는 etcd 안의 기록을 고치는 일이다.",
      "노드 하나의 네트워크가 끊긴 뒤")

X = lambda t: 120 + t * 1.89   # t 는 초 · 560s 가 1178px 에 오게
AX = 480
MARK = [(0, "네트워크 차단"), (40, "NotReady"), (300, "축출 마킹"), (300, ""), (240, "")]

# 장부 레인 — API 서버가 아는 것
ddx.band(d, 100, 268, "장부 — API 서버가 아는 것", x=24, w=1212)
d.o.append(f'<rect x="{X(0)}" y="176" width="{X(300)-X(0)}" height="56" rx="6" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
d.t((X(0) + X(300)) / 2, 210, "Running — 아직 정상으로 센다", 12, OK, KR)
d.o.append(f'<rect x="{X(300)}" y="176" width="{X(560)-X(300)}" height="56" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t((X(300) + X(560)) / 2, 210, "Terminating — deletionTimestamp 가 찍혔다", 12, ACC, KR)

# 실물 레인 — 그 노드에서 실제로
ddx.band(d, 292, 460, "실물 — 그 노드에서 실제로", x=24, w=1212)
d.o.append(f'<rect x="{X(0)}" y="368" width="{X(560)-X(0)}" height="56" rx="6" '
           f'fill="{WARN}12" stroke="{WARN}" stroke-width="1.1"/>')
d.t((X(0) + X(560)) / 2, 402, "컨테이너가 계속 돈다 — kubelet 이 지시를 못 받는다", 12, WARN, KR)

# 시간축
d.line(X(0) - 12, AX, X(560) + 16, AX, RULE, 1.0)
for t, lab in ((0, "0s"), (100, "100s"), (200, "200s"), (300, "300s"), (400, "400s"), (500, "500s")):
    d.line(X(t), AX - 5, X(t), AX + 5, RULE, 1.0)
    d.t(X(t), AX + 22, lab, 9, SOFT, MONO)
for t, lab, c in ((0, "네트워크 차단", SOFT), (40, "Node NotReady", SOFT),
                  (300, "taint 축출 · 대체 파드 생성", ACC)):
    d.line(X(t), 240, X(t), AX - 6, c, 1.0, "4 4")
    d.t(X(t) + 8, 262 if t != 40 else 284, lab, 10, c, KR, "start")

def span(t0, t1, y, label, c):
    x0, x1 = X(t0), X(t1)
    d.path(f"M {x0} {y-7} L {x0} {y} L {x1} {y} L {x1} {y-7}", c, 1.2)
    d.t((x0 + x1) / 2, y + 18, label, 10, c, KR)
span(40, 300, 528, "tolerationSeconds 300 — 기본값 5 분", SOFT)

d.t(24, 584, "그래서 이 구간에 있는 파드를 없애는 길은 셋뿐이다 — Node 오브젝트를 지우거나, "
             "kubelet 이 응답을 재개해 스스로 정리하거나, 사용자가 강제 삭제하거나.", 11, MUTED, KR, "start")
d.legend(604, [("정상으로 셈", OK), ("실제로 도는 중", WARN), ("삭제 표시", ACC)])
d.save("14-02-node-failure-timeline.svg")
print("ok")
