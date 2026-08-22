# 10-01 §5 — 같은 PVC 라도 노드가 다르면 걸린다
# access-mode-matrix 가 정의를 맡으므로 이쪽은 실제로 무슨 일이 나는지만 본다.
# 같은 노드와 다른 노드를 나란히 놓아 어디서 막히는지가 좌표로 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 10-01",
      "붙는 단위가 노드라서 생기는 일",
      "RWO 볼륨은 노드 하나가 붙인다. 같은 노드의 파드끼리는 함께 쓰지만, 다른 노드의 파드가 "
      "같은 볼륨을 붙이려 하면 Multi-Attach 로 걸린다.",
      "generateName 으로 파드를 흩뿌렸을 때")

ddx.node(d, 610, 200, "PVC — RWO", "PV 하나에 바인딩", 300, 76, ACC)

for i, (nm, pods, c, note) in enumerate((
        ("노드 A — 볼륨이 붙은 곳", ("파드 1  Running", "파드 2  Running"), OK, "같은 노드라 함께 쓴다"),
        ("노드 B", ("파드 3  ContainerCreating",), BAD, "Multi-Attach 로 걸린다"))):
    x0 = 90 + i * 560
    d.box(x0, 320, 460, 200, PAPER, RULE, 0.9, 8)
    d.t(x0 + 230, 348, nm, 11, SOFT, KR)
    for j, p in enumerate(pods):
        ddx.node(d, x0 + 230, 396 + j * 62, p, "", 380, 48, c)
    d.t(x0 + 230, 492, note, 11, c, KR)
    sx = 610 + (i * 2 - 1) * 90
    d.path(f"M {sx} 242 L {sx} 280 L {x0+230} 280 L {x0+230} 312", c, 1.5,
           m="ok" if c is OK else "bad", dash=None if c is OK else "5 5")

d.t(24, 560, "RWOP 라면 이야기가 더 좁아진다 — 같은 노드라도 둘째 파드가 Pending 이다. "
             "제한 단위가 노드가 아니라 파드이기 때문이다.", 11, MUTED, KR, "start")
d.legend(584, [("PVC", ACC), ("붙어서 쓴다", OK), ("걸린다", BAD)])
d.save("10-01-multi-pod-attach.svg")
print("ok")
