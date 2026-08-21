# 11-02 전체 지도 — 밖으로 열수록 무엇 하나를 내준다
# 노출 수단이 단계적으로 밖을 향하므로 체인. 마지막 칸이 수단이 아니라 대가를 고르는
# 손잡이라서 그곳만 focal 로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, KR
import ddx

d = D(1180, 400, "KUBERNETES IN ACTION · 11-02",
      "밖으로 열수록 무엇 하나를 내준다",
      "ClusterIP 는 건물 안 내선이다. 노드마다 포트를 열고 그 앞에 로드밸런서를 세우면 밖에서 닿지만, "
      "그 대가로 원래 클라이언트가 누구였는지를 잃거나 일부 파드에 부하가 몰린다.",
      "네 방식과 그 대가")

ddx.stage_chain(
    d, cy=232,
    stages=["§11-01", "§1", "§2", "§3"],
    nodes=[
        ("ClusterIP", "클러스터 안에서만", "밖에서는 닿지 않는다", None),
        ("NodePort", "노드IP:30080", "모든 노드가 문이 된다", None),
        ("LoadBalancer", "건강한 노드로만", "NodePort 의 확장", None),
        ("externalTrafficPolicy", "Cluster ↔ Local", "무엇을 잃을지 고른다", ACC),
    ],
    edges=["밖으로 연다", "앞에 세운다", "대가를 고른다"],
    bw=210, gap=84, x0=30)

d.legend(330, [("대가를 고르는 손잡이", ACC)])
d.save("11-02.chapter-overview.svg")
print("ok")
