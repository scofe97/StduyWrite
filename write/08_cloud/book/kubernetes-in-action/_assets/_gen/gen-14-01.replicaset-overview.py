# 14-01 §1 — 개수를 맡는 쪽과 노출을 맡는 쪽
# 본문이 "복제본을 만드는 일과 하나로 노출하는 일은 별개"라 못박고 둘을 짝으로 둔다.
# 그러니 파드 묶음을 가운데 두고 양쪽에서 각자 맡는 그림이어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 588, "KUBERNETES IN ACTION · 14-01",
      "개수를 맡는 쪽과 노출을 맡는 쪽",
      "ReplicaSet 은 원하는 수만큼 파드를 만들고 그 수를 유지할 뿐이다. 이 파드들을 하나의 대상으로 "
      "노출하는 일은 Service 가 맡는다. 그래서 한 서비스를 제공하는 파드 세트는 둘을 짝으로 둔다.",
      "kiada 서비스 · replicas 5")

d.box(60, 208, 300, 208, PAPER2, INFO, 1.2, 8)
d.t(210, 240, "ReplicaSet", 13, INFO, KR, "middle", 600)
for i, (k, v) in enumerate((("replicas", "5"), ("selector", "app=kiada, rel=stable"),
                            ("template", "Pod 템플릿 — 이름은 없다"))):
    d.t(84, 274 + i * 44, k, 11, INK, MONO, "start", 600)
    d.t(84, 294 + i * 44, v, 10, MUTED, MONO if i < 2 else KR, "start")

d.box(470, 190, 260, 244, PAPER, RULE, 0.9, 8)
d.t(600, 216, "파드 5 벌", 11, SOFT, KR)
for i in range(5):
    ddx.tag(d, 600, 250 + i * 38, f"kiada-{'abcde'[i]}{i}x{i}", OK, 200)

ddx.node(d, 970, 312, "Service", "cluster IP 하나", 220, 96, ACC)

d.path("M 364 312 L 462 312", INFO, 1.6, m="info")
d.t(413, 294, "이만큼 만들고", 11, INFO, KR)
d.t(413, 332, "그 수를 유지한다", 11, INFO, KR)
d.path("M 858 312 L 740 312", ACC, 1.6, m="acc")
d.t(799, 294, "하나로 묶어", 11, ACC, KR)
d.t(799, 332, "노출한다", 11, ACC, KR)

ddx.focal_tag(d, 600, 462, "노드가 죽어도 이 수를 지킨다", 260)

d.t(24, 508, "파드를 하나만 띄울 때도 직접 만들기보다 ReplicaSet 으로 만드는 편이 낫다. "
             "직접 만든 파드는 그 노드가 죽으면 다시 만들기 전까지 서비스가 멈춘다.", 11, MUTED, KR, "start")
d.legend(528, [("개수를 맡는다", INFO), ("파드", OK), ("노출을 맡는다", ACC)])
d.save("14-01-replicaset-overview.svg")
print("ok")
