# 04-02 §Node 의 status conditions
# 본문·옛 도식: 오브젝트 상태를 단일 필드가 아니라 여러 개의 직교적 condition 리스트로 표현한다.
#   각 condition 의 상태는 True·False·Unknown 셋 중 하나. Ready 는 kubelet 이 준비돼 새 Pod 를
#   받을 수 있는지를 알려주는 가장 중요한 것이고, Pressure 계열 셋은 자원 소진을 신호한다.
# 타입 스펙: 축이 여럿이고 각 축이 서로 독립이라는 것이 요점이므로 비교 행렬. 단일 필드로
#           뭉뚱그리지 않는다는 사실 자체가 행 여럿으로 드러난다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 604
d = D(W, H, "KUBERNETES IN ACTION · 04-02",
      "상태를 한 필드로 뭉치지 않고 여러 축으로 나눠 적는다",
      "Node 의 status 는 서로 독립인 condition 목록이다. 각 축은 True·False·Unknown 셋 중 "
      "하나를 갖고, 어느 축이 왜 그런지는 reason·message 가 따로 말한다.",
      lead="Ready 하나만 보면 왜 안 되는지를 모른다 — 축이 나뉘어 있는 이유다")

ddx.band(d, 104, 548, "축이 직교하므로 하나가 True 여도 다른 하나가 False 일 수 있다")

ddx.matrix(
    d, x0=40, hdr_y=196, row_h=76, gap=10, focal_col=1,
    cols=[(220, "condition"), (150, "이 예의 값"),
          (300, "무엇을 말하나"), (230, "이 값이면")],
    rows=[
        ([("Ready", "가장 중요하다"), ("Unknown", "알 수 없다"),
          ("kubelet 이 새 Pod 를 받을 수 있는가", ""),
          ("새 워크로드를 안 보낸다", "보고가 끊겼다")], BAD),
        ([("MemoryPressure", "자원 소진 신호"), ("True", "압박이 있다"),
          ("메모리가 모자라 가고 있는가", ""),
          ("축출이 일어날 수 있다", "노드가 좁다")], WARN),
        ([("DiskPressure", "자원 소진 신호"), ("False", "괜찮다"),
          ("디스크가 모자라 가고 있는가", ""), ("여유가 있다", "")], OK),
        ([("PIDPressure", "자원 소진 신호"), ("False", "괜찮다"),
          ("프로세스 번호가 모자라 가고 있는가", ""), ("여유가 있다", "")], OK),
    ])

d.t(36, 500, "값은 True·False·Unknown 셋뿐이고, 왜 그런지는 reason(기계용)과 message(사람용)가 "
             "따로 담는다 — 06-01 의 Pod conditions 도 같은 형태다.", 12, MUTED, KR, "start")
d.legend(564, [("보고가 끊긴 축", BAD), ("압박이 있는 축", WARN), ("여유가 있는 축", OK)])
d.save("04-02-node-status-conditions.svg")
print("ok node-status-conditions")
