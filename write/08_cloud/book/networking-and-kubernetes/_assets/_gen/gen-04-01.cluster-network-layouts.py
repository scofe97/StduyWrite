# 04-01.cluster-network-layouts — 세 레이아웃 × 얻는 것 · 대가
# 본문 요구: "세 레이아웃은 Pod IP 를 밖에 보이느냐로 갈린다" — 각각 얻는 것과 대가가 있다
# 타입 스펙: type-dp-security-matrix.md — 고르는 축이 하나(Pod IP 노출)이고 결과가 둘이라
#           행렬로 놓아야 세 줄을 나란히 견줄 수 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 580
d = D(W, H, "THREE CLUSTER LAYOUTS · WHAT YOU PAY",
      "세 레이아웃은 Pod IP 를 밖에 보이느냐로 갈린다",
      "무엇을 얻는지보다 무엇을 내주는지가 선택을 정한다. 공짜인 배치는 없다.",
      lead="무엇을 얻는지보다 무엇을 내주는지가 선택을 정한다")

ddx.band(d, 104, 520, "판정 축 하나 · Pod IP 를 밖에 보이는가")
ddx.matrix(d, 44,
  [(292, "레이아웃"), (272, "얻는 것"), (324, "내주는 것")],
  [([("Isolated", "노드만 라우팅 가능"), ("IP 공간 재사용", "클러스터끼리 겹쳐도 됨"),
     ("LB·프록시 필요", "Pod 는 밖에서 닫힘")], INFO),
   ([("Flat", "Pod IP 전부 라우팅"), ("단순·저지연", "프록시·재작성 없음"),
     ("크고 연속된 IP 공간", "밖 LB 가 Pod 직결")], OK),
   ([("Island", "노드 뒤에서 SNAT"), ("IP 공간 절약", "Flat 의 요구를 회피"),
     ("IP 기반 식별 상실", "Pod 는 노드에 숨음")], WARN)],
  hdr_y=200, row_h=84, gap=12, focal_col=2, sizes=(13, 12))

d.legend(536, [("Isolated", INFO), ("Flat", OK), ("Island", WARN)])
d.save("04-01.cluster-network-layouts.svg")
print("ok cluster-network-layouts")
