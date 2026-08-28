# 타입 스펙: type-dp-security-matrix.md — 행이 routes-based·VPC-native, 열이 각 모드에서 트래픽이 Pod 에 닿는 방식
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 556
d = D(W, H, "GKE CLUSTER MODE · CAN THE LB REACH THE POD",
      "클러스터 모드가 LB 가 Pod 로 직접 갈 수 있는지를 정한다",
      "만들 때 고른 모드 하나가 나중에 LB 의 경로를 정한다. 콘솔과 REST API 의 기본값이 서로 다르다.",
      lead="만들 때 고른 모드가 나중에 LB 의 경로를 정한다")
ddx.band(d, 104, 500, "콘솔과 REST API 의 기본값이 달라, 어떻게 만들었느냐가 결과를 가른다")
ddx.matrix(d, 44,
  [(320, "클러스터 모드"), (300, "Pod 주소가 어디서 오나"), (292, "LB 가 가는 길")],
  [([("routes-based", "REST API 기본값"), ("커스텀 정적 라우트", "VPC 라우트 테이블에"),
     ("노드 경유", "LB → 노드 → Pod · 홉 하나 더")], WARN),
   ([("VPC-native", "콘솔 기본값"), ("alias IP 대역", "서브넷의 보조 대역"),
     ("Pod 직결", "NEG 가 열림 · 지연↓ 개별 관측")], OK)],
  hdr_y=224, row_h=96, gap=16, focal_col=2)
d.t(36, 476, "직결이 되면 LB 가 Pod 하나하나를 대상으로 볼 수 있어 관측도 그 단위로 내려온다",
     12, MUTED, KR, "start")
d.legend(516, [("노드를 한 번 더 거친다", WARN), ("Pod 로 바로 간다", OK)])
d.save("06-02.gke-cluster-mode.svg"); print("ok gke-cluster-mode")
