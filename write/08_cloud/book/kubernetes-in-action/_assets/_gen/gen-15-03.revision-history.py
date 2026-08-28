# 15-03 §3 — 히스토리는 Deployment 가 아니라 ReplicaSet 들이다
# 본문이 "revision 히스토리는 Deployment 오브젝트가 아니라 연관된 ReplicaSet 들로 표현된다"고
# 못박는다. 그러니 목록을 그리면 안 되고, 각 revision 이 실재하는 오브젝트여야 한다.
# 타입 스펙: type-tree.md — 부모 하나가 자식 셋을 거느린다 — Deployment 가 ReplicaSet 을 revision 으로 쥐고 있다.
#           자식 중 하나만 파드를 달고 있고 나머지는 replicas 0 이라는 것이 이 트리의 요점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 15-03",
      "revision 은 ReplicaSet 에 저장된다",
      "각 ReplicaSet 이 한 revision 이다. 업데이트가 끝나도 옛 ReplicaSet 을 지우지 않는 이유가 "
      "여기 있다 — 롤백이란 그 숫자를 다시 올리는 일이다.",
      "kubectl rollout history deploy kiada")

ddx.node(d, 180, 236, "Deployment  kiada", "지금 template = 0.7", 280, 84, INFO)

RS = [("kiada-7bffb9bf96", "0.5", 1, 0, SOFT), ("kiada-5d5c5f9d76", "0.6", 2, 0, SOFT),
      ("kiada-6c9d8b4f52", "0.7", 3, 3, ACC)]

# 소유 관계 세 갈래를 한 점에서 비스듬히 뻗지 않는다. 줄기 하나를 세워 거기서 갈라내면
# 세 선이 서로 겹치지도, 남의 선을 건너지도 않는다 — 내려가는 선은 반드시 중간 행의
# 가로선을 건너기 때문이다.
d.path("M 322 236 L 368 236", INFO, 1.3)
d.path("M 368 168 L 368 360", INFO, 1.3)
for i, (nm, ver, rev, n, c) in enumerate(RS):
    cx = 620 + i * 0
    cy = 168 + i * 96
    if c is ACC:
        d.o.append(f'<rect x="{cx-200}" y="{cy-36}" width="400" height="72" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(cx - 200, cy - 36, 400, 72, PAPER2, RULE, 1.0, 6); tc = SOFT
    d.t(cx - 178, cy - 8, nm, 12, tc, MONO, "start", 600)
    d.t(cx - 178, cy + 16, f"ver {ver}   ·   replicas {n}", 10, MUTED, MONO, "start")
    d.t(cx + 178, cy + 4, f"revision {rev}", 11, tc, MONO, "end")
    d.path(f"M 368 {cy} L 412 {cy}", INFO, 1.3, m="info")

for i, (nm, ver, rev, n, c) in enumerate(RS):
    cy = 168 + i * 96
    if n:
        ddx.node(d, 1010, cy, "파드 3 벌", "지금 도는 것", 200, 62, OK)
        d.path(f"M 822 {cy} L 902 {cy}", ACC, 1.4, m="acc")
    else:
        d.t(1010, cy + 4, "파드 없음 — 숫자만 0", 11, SOFT, KR)

d.t(24, 420, "몇 번 업데이트한 클러스터에서 get rs 를 치면 replicas 0 짜리가 줄줄이 보인다. 그게 롤백 이력이다.",
     11, MUTED, KR, "start")
d.t(24, 442, "kubectl rollout undo 는 그 숫자를 반대로 움직인다 — 옛 ReplicaSet 을 다시 올리고 지금 것을 0 으로 내린다.",
     11, MUTED, KR, "start")
d.t(24, 464, "무한정 쌓이지는 않는다. revisionHistoryLimit 이 보관 개수를 정하고 기본값은 10 이다.",
     11, MUTED, KR, "start")
d.legend(496, [("소유 관계", INFO), ("활성 revision", ACC), ("지금 도는 파드", OK)])
d.save("15-03-revision-history.svg")
print("ok")
