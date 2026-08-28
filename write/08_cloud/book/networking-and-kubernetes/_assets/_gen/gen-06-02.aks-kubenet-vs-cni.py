# 타입 스펙: type-dp-security-matrix.md — 행이 kubenet·Azure CNI, 열이 4장의 그 선택 축들
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 556
d = D(W, H, "AKS · IS THE POD IP ROUTABLE",
      "Pod IP 가 Vnet 에서 라우팅돼야 하는가 — 그 답이 둘을 가른다",
      "라우팅돼야 하면 IP 를 미리 예약해야 하고, 아니어도 되면 노드 IP 로 감춘다. 그 하나가 나머지를 정한다.",
      lead="라우팅돼야 하면 IP 를 예약해야 하고, 아니어도 되면 노드 뒤로 감춘다")
ddx.band(d, 104, 500, "4 장의 Island 와 Flat 이 여기서 그대로 다시 나온다")
ddx.matrix(d, 44,
  [(320, "모드"), (300, "Pod IP 는"), (292, "치르는 값")],
  [([("kubenet (기본)", "노드만 Vnet IP 수령"), ("Vnet 밖 대역", "Pod→Vnet 은 노드 IP 로 SNAT"),
     ("운영이 단순", "4 장의 Island 레이아웃")], OK),
   ([("Azure CNI", "Pod 가 라우터블 IP"), ("Vnet 대역 그대로", "직접 접근 가능"),
     ("IP 계획이 무겁다", "노드당 최대 Pod 만큼 예약")], WARN)],
  hdr_y=224, row_h=96, gap=16, focal_col=2)
d.t(36, 476, "CNI 를 고르면 노드를 늘리기 전에 IP 부터 모자란다 — IP 설계가 곧 확장 한계가 된다",
     12, MUTED, KR, "start")
d.legend(516, [("감추고 단순하게", OK), ("열고 무겁게", WARN)])
d.save("06-02.aks-kubenet-vs-cni.svg"); print("ok aks-kubenet-vs-cni")
