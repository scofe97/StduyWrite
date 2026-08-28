# 11-03 §4 — 상태는 연속 횟수를 채워야 바뀐다
# 임계값이 시간 위에서만 읽히므로 timeline. 상태 띠·probe 결과·구간 괄호를 세 층으로 쌓고,
# 상태가 실제로 뒤집히는 한 지점만 focal.
# 타입 스펙: type-gantt.md — 시간축 위의 구간 막대 — 상태 밴드 둘이 지속 구간이고 아래 대괄호가 initialDelaySeconds·
#           failureThreshold·periodSeconds 를 잰다. probe 결과는 그 위에 놓인 점 사건이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 560, "KUBERNETES IN ACTION · 11-03",
      "상태는 연속 횟수를 채워야 바뀐다",
      "probe 는 initialDelaySeconds 가 지난 뒤 periodSeconds 마다 돈다. 한 번의 결과로 상태가 뒤집히지 않고, "
      "failureThreshold·successThreshold 만큼 연속돼야 명단에서 빠지거나 들어온다.",
      "periodSeconds 5 · failureThreshold 3 · successThreshold 2")

X = lambda t: 130 + t * 22
AX = 330

# 상태 띠
d.o.append(f'<rect x="{X(0)}" y="168" width="{X(30)-X(0)}" height="58" rx="6" '
           f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.1"/>')
d.t((X(0) + X(30)) / 2, 203, "명단에 없다 — notReady · ready: false", 12, BAD, KR)
d.o.append(f'<rect x="{X(30)}" y="168" width="{X(45)-X(30)}" height="58" rx="6" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
d.t((X(30) + X(45)) / 2, 203, "명단에 들어온다", 12, OK, KR)
d.t(30, 203, "상태", 11, SOFT, KR, "start")

# 시간축
d.line(X(0) - 10, AX, X(45) + 14, AX, RULE, 1.0)
for t in range(0, 46, 5):
    d.line(X(t), AX - 5, X(t), AX + 5, RULE, 1.0)
    d.t(X(t), AX + 22, f"{t}s", 9, SOFT, MONO)
d.t(30, AX + 4, "시간", 11, SOFT, KR, "start")

# probe 결과
d.t(30, 296, "probe", 11, SOFT, KR, "start")
for t, ok in ((10, False), (15, False), (20, False), (25, True), (30, True), (35, True), (40, True)):
    d.chip(X(t), 290, "성공" if ok else "실패", OK if ok else BAD, 9)

# 이벤트와 구간
d.line(X(22), 240, X(22), 276, ACC, 1.0, "4 4")
d.t(X(22) + 8, 258, "/var/ready 생성", 10, ACC, KR, "start")

def span(t0, t1, y, label, c):
    x0, x1 = X(t0), X(t1)
    d.path(f"M {x0} {y-7} L {x0} {y} L {x1} {y} L {x1} {y-7}", c, 1.2)
    d.t((x0 + x1) / 2, y + 18, label, 10, c, KR)

span(0, 10, 388, "initialDelaySeconds 10 — 아직 돌지 않는다", SOFT)
span(10, 20, 430, "failureThreshold 3 — 연속 세 번", BAD)
span(25, 30, 388, "successThreshold 2 — 연속 두 번", OK)
span(35, 40, 430, "periodSeconds 5", SOFT)

d.line(X(30), 232, X(30), 276, ACC, 1.4)
ddx.focal_tag(d, X(30) + 96, 250, "두 번째 성공에서 편입", 190)

d.t(24, 490, "실패해도 컨테이너는 재시작되지 않는다. 프로세스는 그대로 두고 트래픽만 끊는 것이 readiness 이고, "
             "그래서 명단에서 빠진 뒤에도 kubelet 은 파드 IP 로 직접 probe 를 계속 돌린다.", 11, MUTED, KR, "start")
d.legend(512, [("명단 밖", BAD), ("명단 안", OK), ("상태가 바뀌는 순간", ACC)])
d.save("11-03-readiness-probe-timeline.svg")
print("ok")
