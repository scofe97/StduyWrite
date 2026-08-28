# 14-01 §1 — '무시한다'가 무슨 뜻인지까지 그린다
# 본문이 "무시란 세지도 지우지도 않는다는 뜻"이라고 따로 풀어 준다. 매칭 여부만 그리면
# 그 두 결과가 안 보이므로, 안 맞는 파드 쪽에 결과 둘을 붙인다.
# 타입 스펙: type-tree.md — 부모 하나가 자식 셋을 거느린다. 오른쪽 무리는 그 트리에 붙지 못한 노드이고, 화살표가
#           닿지 않는 것이 곧 '무시한다'는 뜻이다.
#           2026-08-28 정정: 처음에 dependency 로 적었으나, 그 정본은 트리로 표현 못 하는 두 가지
#           (한 노드에 부모가 둘인 팬인, 순환)를 위한 타입이고 '둘 다 없으면 Tree 를 쓰고 그렇다고
#           밝히라'고 명시한다. 여기엔 팬인도 순환도 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 14-01",
      "소속을 정하는 것은 위치가 아니라 label 이다",
      "같은 네임스페이스에 나란히 떠 있어도 selector 에 맞지 않으면 이 세트의 파드가 아니다. "
      "무시한다는 것은 세지도 지우지도 않는다는 뜻이다.",
      "selector: app=kiada, rel=stable")

d.box(60, 232, 260, 128, PAPER2, INFO, 1.2, 8)
d.t(190, 264, "ReplicaSet kiada", 12, INFO, KR, "middle", 600)
d.t(190, 292, "app=kiada", 11, MUTED, MONO)
d.t(190, 312, "rel=stable", 11, MUTED, MONO)
d.t(190, 340, "이 둘을 다 가진 파드만", 10, SOFT, KR)

d.box(420, 160, 340, 276, PAPER, OK, 0.9, 8)
d.t(590, 186, "selector 에 맞는다 — 이 세트의 파드", 11, OK, KR)
d.path("M 324 296 L 384 296", OK, 1.3)
d.path("M 384 226 L 384 358", OK, 1.3)
for i in range(3):
    ddx.node(d, 590, 226 + i * 66, f"kiada-{i}", "app=kiada · rel=stable", 280, 52, OK)
    d.path(f"M 384 {226+i*66} L 444 {226+i*66}", OK, 1.3, m="ok")
d.t(590, 414, "replicas 를 채우는 데 셈해진다", 11, OK, KR)

d.box(820, 160, 340, 276, PAPER, WARN, 0.9, 8)
d.t(990, 186, "맞지 않는다 — 무시한다", 11, WARN, KR)
for i, (nm, lab) in enumerate((("quote-0", "app=quote"), ("kiada-canary", "app=kiada · rel=canary"))):
    ddx.node(d, 990, 232 + i * 70, nm, lab, 280, 52, WARN)
ddx.focal_tag(d, 990, 372, "세지도 지우지도 않는다", 250)
d.t(990, 414, "replicas 계산 밖 · 스케일다운 대상 밖", 11, ACC, KR)

d.t(24, 500, "그래서 rel 값 하나만 달라도 세트에서 빠진다. 14-02 에서 문제 파드를 조사할 때 "
             "label 을 바꿔 세트에서 빼는 수가 이 성질을 이용한 것이다.", 11, MUTED, KR, "start")
d.t(24, 522, "template 의 label 은 selector 의 label 을 포함해야 한다 — 아니면 만든 파드가 자기 수에 안 잡혀 "
             "파드가 무한히 생성되므로 API 가 거부한다.", 11, MUTED, KR, "start")
d.legend(548, [("세트의 파드", OK), ("무시되는 파드", WARN), ("무시의 두 뜻", ACC)])
d.save("14-01-replicaset-label-selector.svg")
print("ok")
