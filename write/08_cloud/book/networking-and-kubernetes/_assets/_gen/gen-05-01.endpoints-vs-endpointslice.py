# 05-01.endpoints-vs-endpointslice — 주소 하나가 바뀔 때 오가는 양
# 타입 스펙: type-dp-security-matrix.md 2 행 대조. 차이가 '전송량'이라 행 색으로 갈린다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
W, H = 1000, 556
d = D(W, H, "ONE ADDRESS CHANGES · HOW MUCH TRAVELS",
      "주소 하나가 바뀔 때 실제로 전송되는 양",
      "바뀐 것은 주소 하나인데, 오가는 것이 객체 전체냐 조각 하나냐로 갈린다. 노드 수천 대를 곱하면 그 차이가 병목이 된다.",
      lead="바뀐 건 주소 하나인데 오가는 게 전체냐 조각이냐로 갈린다")
ddx.band(d, 104, 500, "노드 수천 대를 곱하면 이 차이가 규모의 한계가 된다")
ddx.matrix(d, 44,
  [(320, "무엇을 쥐고 있나"), (300, "주소 하나가 바뀌면"), (292, "노드마다 받는 양")],
  [([("Endpoints 1 개", "Pod 1000 개 주소 전부"), ("객체 전체 재전송", "주소 1 개만 바뀌어도"),
     ("전량", "kube-proxy × 노드 수천")], BAD),
   ([("EndpointSlice N 개", "기본 100 · 최대 1,000"), ("Slice B 만 변경", "나머지 slice 는 그대로"),
     ("조각 하나", "kube-proxy × 노드 수천")], OK)],
  hdr_y=224, row_h=96, gap=16, focal_col=2)
d.t(36, 476, "쪼개는 것 자체가 목적이 아니라, 바뀐 조각만 보내려고 쪼갠 것이다 — "
             "그래서 slice 크기가 곧 전송 단위다", 12, MUTED, KR, "start")
d.legend(516, [("전량 재전송", BAD), ("조각만 전송", OK)])
d.save("05-01.endpoints-vs-endpointslice.svg"); print("ok endpoints-vs-endpointslice")
