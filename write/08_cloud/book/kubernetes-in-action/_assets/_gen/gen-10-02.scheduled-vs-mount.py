# 10-02 §3 — 선언은 통과했는데 실재가 없다
# 본문의 요점은 스케줄러와 kubelet 이 서로 다른 것을 본다는 것이다. 그러니 시간 순서 위에
# 두 주체의 판단을 나란히 놓고, 통과와 실패가 같은 파드에서 이어지는 것이 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 10-02",
      "스케줄은 통과하고 마운트에서 걸린다",
      "스케줄러는 오브젝트에 적힌 선언을 본다. 그 경로가 그 노드에 실제로 있는지는 보지 않는다. "
      "실재를 확인하는 것은 그 노드의 kubelet 이고, 그때는 이미 배정이 끝난 뒤다.",
      "node affinity 는 맞는데 경로가 없는 node-local PV")

STEP = [("① PVC 가 PV 에 바인딩", "용량·모드·클래스가 맞았다", OK),
        ("② 스케줄러가 노드를 고른다", "PV 의 node affinity 를 본다", OK),
        ("③ PodScheduled: True", "선언상으로는 문제가 없다", OK),
        ("④ kubelet 이 마운트 시도", "그 경로가 실제로 있는가", ACC),
        ("⑤ FailedMount", "없다 — 여기서 처음 드러난다", BAD)]
BW, GP = 216, 30
X0 = (1240 - (5 * BW + 4 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]
for cx, (t, s, c) in zip(CX, STEP):
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="222" width="{BW}" height="96" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - BW // 2, 222, BW, 96, PAPER2, c, 1.2, 6)
    d.t(cx, 256, ddx.fit(t, 12, BW - 16, t), 12, c, KR, "middle", 600)
    d.t(cx, 284, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 270 L {b-BW//2-9} 270", MUTED, 1.4, m="ar")

ddx.bracket(d, 60, 222, 318, "선언을 본다", SOFT)
d.t(CX[3], 356, "여기서부터 실재를 본다", 11, ACC, KR)

d.t(24, 452, "그래서 kubectl get po 의 STATUS 는 ContainerCreating 인데 conditions 에는 PodScheduled: True 가 남는다. "
             "둘이 모순처럼 보이지만 서로 다른 것을 말하고 있다.", 11, MUTED, KR, "start")
d.t(24, 474, "09-02 의 hostPath type 검사 실패와 같은 모양이다 — 조건은 어느 단계까지 통과했는지를, "
             "이벤트가 왜 멈췄는지를 말한다.", 11, MUTED, KR, "start")
d.legend(504, [("통과한 단계", OK), ("실재를 보는 자리", ACC), ("드러나는 지점", BAD)])
d.save("10-02-scheduled-vs-mount.svg")
print("ok")
