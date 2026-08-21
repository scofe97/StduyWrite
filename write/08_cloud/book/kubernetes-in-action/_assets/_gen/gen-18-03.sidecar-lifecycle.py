# 18-03 §3 — 먼저 뜨고 나중에 내려간다
# 캡션이 순서를 정확히 준다 — 사이드카를 먼저, started 만 확인, 메인이 끝난 뒤 역순으로.
# 그러니 시간축 위에 두 컨테이너의 구간이 겹쳐 보여야 하고 started 지점이 표시돼야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 18-03",
      "먼저 뜨고 나중에 내려간다",
      "사이드카는 init 컨테이너 자리에 restartPolicy: Always 로 적는다. kubelet 이 먼저 띄우고 "
      "started 만 확인한 뒤 메인을 시작하며, 메인이 끝나야 역순으로 내린다.",
      "ready 가 아니라 started 를 본다 — 그래야 Job 이 멈추지 않는다")

X = lambda t: 180 + t * 140
d.t(120, 240, "사이드카", 11, SOFT, KR, "end")
d.o.append(f'<rect x="{X(0)}" y="216" width="{X(6.4)-X(0)}" height="48" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t((X(0) + X(6.4)) / 2, 246, "먼저 뜨고, 메인이 끝난 뒤에 내려간다", 11, ACC, KR)

d.t(120, 330, "메인", 11, SOFT, KR, "end")
d.o.append(f'<rect x="{X(1.2)}" y="306" width="{X(5.6)-X(1.2)}" height="48" rx="6" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
d.t((X(1.2) + X(5.6)) / 2, 336, "Job 의 일을 한다", 11, OK, KR)

d.line(X(0) - 12, 404, X(6.4) + 12, 404, RULE, 1.0)
for t, lab, c in ((0, "사이드카 시작", SOFT), (1.2, "started 확인 → 메인 시작", ACC),
                  (5.6, "메인 종료", OK), (6.4, "사이드카 종료", ACC)):
    d.line(X(t), 372, X(t), 410, c, 1.0, "4 4")
    d.t(X(t), 432, lab, 10, c, KR)

d.t(24, 496, "started 만 보는 것이 요점이다. ready 를 기다렸다면 ready 가 안 되는 사이드카 하나가 "
             "Job 전체를 멈춰 세웠을 것이다.", 11, MUTED, KR, "start")
d.t(24, 518, "메인이 끝나도 사이드카가 계속 돌면 파드가 Completed 로 가지 못한다 — 그래서 kubelet 이 "
             "역순으로 내려 준다.", 11, MUTED, KR, "start")
d.legend(548, [("사이드카", ACC), ("메인", OK)])
d.save("18-03-sidecar-lifecycle.svg")
print("ok")
