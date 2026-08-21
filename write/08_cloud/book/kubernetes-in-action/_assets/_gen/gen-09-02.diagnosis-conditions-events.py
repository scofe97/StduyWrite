# 09-02 §2 — 조건은 증상까지, 원인은 이벤트에
# 본문이 "conditions 는 증상까지입니다"로 한 줄 못박는다. 그러니 두 조회를 나란히 놓고
# 각자 어디까지 말해 주는지가 대비돼야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 700, "KUBERNETES IN ACTION · 09-02",
      "어디서 멈췄는지와 왜 멈췄는지",
      "conditions 는 어느 단계까지 통과했는지를 말해 준다. 왜 거기서 멈췄는지는 말해 주지 않는다 — "
      "그 답은 events 에 있다.",
      "type: Directory 인데 경로가 없어 멈춘 파드")

ddx.band(d, 100, 260, "① kubectl get po — 문제가 있다는 신호", x=24, w=1172)
d.t(140, 204, "STATUS", 11, SOFT, MONO, "start")
ddx.tag(d, 420, 200, "0/1  ContainerCreating", WARN, 300)
d.t(700, 204, "무언가 잘못됐다는 것까지", 11, MUTED, KR, "start")

ddx.band(d, 284, 452, "② conditions — 어느 단계에서 멈췄는가", x=24, w=1172)
for i, (t, v, c) in enumerate((("PodScheduled", "True", OK), ("Initialized", "True", OK),
                               ("Ready", "False — ContainersNotReady", WARN))):
    y = 348 + i * 32
    d.t(140, y, t, 11, SOFT, MONO, "start")
    d.t(380, y, v, 11, c, MONO, "start")
d.t(760, 364, "스케줄과 init 은 통과했고", 11, MUTED, KR, "start")
d.t(760, 386, "컨테이너가 준비되지 못했다 — 증상까지다", 11, WARN, KR, "start")

ddx.band(d, 476, 620, "③ events — 왜 멈췄는가", x=24, w=1172, focal=True)
d.t(140, 540, "FailedMount", 11, ACC, MONO, "start")
d.t(380, 540, "hostPath type check failed:", 11, ACC, MONO, "start")
d.t(380, 562, "/tmp/does-not-exist-xyz is not a directory", 11, ACC, MONO, "start")
d.t(880, 550, "근본 원인을 정확히 지목한다", 11, ACC, KR, "start")

d.t(24, 656, "type 이 없었다면 이 파드는 조용히 떴을 것이다. 즉시 실패시켜 events 에 원인을 남기는 것이 "
     "type 필드의 존재 이유다.", 11, MUTED, KR, "start")
d.legend(672, [("증상", WARN), ("통과한 단계", OK), ("원인", ACC)])
d.save("09-02-diagnosis-conditions-events.svg")
print("ok")
