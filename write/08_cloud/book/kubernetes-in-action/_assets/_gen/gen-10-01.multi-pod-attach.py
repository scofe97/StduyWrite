# 10-01 §5 — 같은 PVC 라도 노드가 다르면 걸린다
# access-mode-matrix 가 정의를 맡으므로 이쪽은 실제로 무슨 일이 나는지만 본다.
# 같은 노드와 다른 노드를 나란히 놓아 어디서 막히는지가 좌표로 보여야 한다.
# 타입 스펙: type-deployment.md — 노드 두 상자가 존이고 그 안의 파드가 artifact 다. 같은 PVC 라도 어느 노드에 놓이느냐가
#           Running 과 Multi-Attach 를 가르므로 배치가 값이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, PAPER, RULE, KR
import ddx

d = D(920, 580, "KUBERNETES IN ACTION · 10-01",
      "붙는 단위가 노드라서 생기는 일",
      "RWO 볼륨은 노드 하나가 붙인다. 같은 노드의 파드끼리는 함께 쓰지만, 다른 노드의 파드가 "
      "같은 볼륨을 붙이려 하면 Multi-Attach 로 걸린다.",
      "generateName 으로 파드를 흩뿌렸을 때")

ddx.node(d, 460, 175, "PVC — RWO", "PV 하나에 바인딩", 280, 72, ACC)

for i, (nm, pods, c, note) in enumerate((
        ("노드 A — 볼륨이 붙은 곳", ("파드 1 · Running", "파드 2 · Running"), OK, "같은 노드의 파드는 함께 마운트"),
        ("노드 B", ("파드 3 · ContainerCreating",), BAD, "Multi-Attach error 로 걸림"))):
    x0 = 40 + i * 440
    d.box(x0, 260, 400, 220, PAPER, RULE, 0.9, 8)
    d.t(x0 + 200, 288, nm, 13, SOFT, KR)
    for j, p in enumerate(pods):
        ddx.node(d, x0 + 200, 342 + j * 58, p, "", 320, 44, c)
    d.t(x0 + 200, 456, note, 12, c, KR)
    sx = 460 + (i * 2 - 1) * 90
    d.path(f"M {sx} 211 L {sx} 238 L {x0+200} 238 L {x0+200} 254", c, 1.5,
           m="ok" if c is OK else "bad", dash=None if c is OK else "5 5")

d.t(24, 510, "RWOP: 제한 단위가 파드 · 같은 노드라도 둘째 파드는 Pending", 12, MUTED, KR, "start")
d.legend(534, [("PVC", ACC), ("함께 씀", OK), ("걸림", BAD)])
d.save("10-01-multi-pod-attach.svg")
print("ok")
