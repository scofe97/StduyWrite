# 11-01 전체 지도 — 변하는 파드 IP 를 변하지 않는 하나의 주소로
# 본문 §진입이 §2→§3→§5·§7 순서를 직접 적어 둔다. 그 순서를 한 줄 체인으로 놓고
# 장 전체가 지키려는 것(바뀌지 않는 번호)에만 focal 을 준다.
# 타입 스펙: type-process.md — 단계마다 같은 의미 슬롯(절 번호·이름·값·한 줄)이 반복된다. 화살표는 데이터가 아니라
#           읽는 순서를 나른다 — semantic-patterns 의 "Stage framework with semantic slots".
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, KR, MONO
import ddx

d = D(1356, 400, "KUBERNETES IN ACTION · 11-01",
      "변하는 파드 IP를 변하지 않는 하나의 주소로",
      "파드 IP는 수시로 바뀐다. label selector 가 뒤에 설 파드를 정하고, ClusterIP 가 바뀌지 않는 번호를 맡고, "
      "cluster DNS 가 그 번호를 이름으로 부르게 하며, 노드 커널의 DNAT 가 실제 파드까지 편지를 옮긴다.",
      "사서함 하나로 이사 잦은 친구에게 편지를 보내는 구조")

ddx.stage_chain(
    d, cy=232,
    stages=["문제", "§2 대상 선정", "§3 주소 발급", "§7 이름 해석", "§5 실제 전달"],
    nodes=[
        ("파드 IP", "10.244.x.x", "언제든 바뀐다", None),
        ("label selector", "app=quote", "라벨로 고른다", None),
        ("ClusterIP", "10.96.74.151", "바뀌지 않는다", ACC),
        ("cluster DNS", "quiz", "이름으로 부른다", None),
        ("파드 IP", "10.244.2.9", "DNAT 로 닿는다", None),
    ],
    edges=["라벨로 묶는다", "번호를 받는다", "이름을 붙인다", "실제로 바꾼다"],
    bw=190, gap=84, x0=30)

d.legend(330, [("변하지 않는 축", ACC)])
d.save("11-01.chapter-overview.svg")
print("ok")
