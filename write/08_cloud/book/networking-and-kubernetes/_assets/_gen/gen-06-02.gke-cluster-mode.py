# 타입 스펙: type-dp-security-matrix.md — 행이 routes-based·VPC-native, 열이 각 모드에서 트래픽이 Pod 에 닿는 방식
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 540
d = D(W, H, "GKE CLUSTER MODE · CAN THE LB REACH THE POD",
      "클러스터 모드가 LB 가 Pod 로 직접 갈 수 있는지를 정한다",
      "만들 때 고른 모드 하나가 나중에 LB 의 경로를 정한다. 콘솔과 REST API 의 기본값이 서로 다르다.",
      lead="만들 때 고른 모드가 나중에 LB 의 경로를 정한다")
ddx.band(d, 104, 480, "콘솔 기본값 ≠ REST API 기본값")
ddx.matrix(d, 44,
  [(304, "클러스터 모드"), (284, "Pod 주소가 어디서 오나"), (292, "LB 가 가는 길")],
  [([("routes-based", "REST API 기본값"), ("커스텀 정적 라우트", "VPC 라우트 테이블에"),
     ("노드 경유", "LB → 노드 → Pod · 홉 하나 더")], WARN),
   ([("VPC-native", "콘솔 기본값"), ("alias IP 대역", "서브넷의 보조 대역"),
     ("Pod 직결", "NEG 가 열림 · 지연↓ 개별 관측")], OK)],
  hdr_y=224, row_h=96, gap=16, focal_col=2, sizes=(13, 12))
d.legend(496, [("노드 한 번 더 경유", WARN), ("Pod 직행", OK)])
d.save("06-02.gke-cluster-mode.svg"); print("ok gke-cluster-mode")
