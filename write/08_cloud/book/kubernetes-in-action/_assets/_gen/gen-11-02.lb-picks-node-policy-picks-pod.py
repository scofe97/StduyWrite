# 11-02 §3 — 결정은 두 번, 주체도 둘이다
# 두 결정을 행으로, 주체·기준·후보를 열로 둔 행렬. 후보 범위가 갈리는 축이라 그 열이 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, KR
import ddx

d = D(1084, 508, "KUBERNETES IN ACTION · 11-02",
      "결정은 두 번, 주체도 둘이다",
      "외부 요청이 파드에 닿기까지 고르는 일이 두 번 있다. 로드밸런서는 노드까지만 고르고 파드는 보지 않으며, "
      "파드를 고르는 것은 도착한 노드의 커널이다. 이 둘을 섞으면 타입과 정책의 역할이 뒤엉킨다.",
      "남의 노드로 넘길 수 있는지는 어디서 갈리는가")

ddx.matrix(
    d, x0=24, hdr_y=140, row_h=92, gap=12, focal_col=3,
    cols=[(190, "결정"), (230, "주체"), (280, "판단 기준"), (300, "후보 범위")],
    rows=[
        ([("첫 번째 결정", "어느 노드로 보낼지"), ("로드밸런서", "클러스터 밖에 있다"),
          ("헬스체크 통과 여부", "죽은 노드를 빼고 균등하게"),
          ("건강한 노드 전부", "파드 수는 보지 않는다")], INFO),
        ([("두 번째 결정", "어느 파드로 넘길지"), ("도착한 노드의 커널", "kube-proxy 가 심은 규칙"),
          ("externalTrafficPolicy", "Cluster ↔ Local"),
          ("정책이 정한다", "Cluster 전체 ↔ Local 이 노드")], ACC),
    ])

d.t(24, 396, "그러니 남의 노드 파드로 넘길 수 있는지는 정책이 정하지 Service 타입이 정하지 않는다. "
             "Cluster 면 NodePort 도 넘기고, Local 이면 LoadBalancer 도 넘기지 못한다.", 11, MUTED, KR, "start")
d.legend(422, [("노드까지", INFO), ("파드는 여기서", ACC)])
d.save("11-02-lb-picks-node-policy-picks-pod.svg")
print("ok")
