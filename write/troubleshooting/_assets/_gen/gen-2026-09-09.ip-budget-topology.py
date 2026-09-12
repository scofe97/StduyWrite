# 2026-09-09 D 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "대역과 노드와 Pod 가 어떤 관계로 놓여 있나"이지 계산의 어긋남이 아니다.
# 노드당 소비량이 만드는 상한은 원인 분석 절의 ip-budget 이 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 대역 경계로 소속 관계를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W, H = 820, 408
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-09 D",
      "대역과 노드와 Pod",
      "GKE VPC 네이티브 모드에서 Pod 대역 /16 을 잡아 두었고 노드당 Pod 최대치는 110 이다. "
      "노드는 그 대역 안에서 자기 몫을 받아 가고, Pod 는 그 몫 안에서 주소를 받는다.",
      lead="문서의 최대치는 Pod 수를 말하지 클러스터 상한을 말하지 않습니다")

d.box(40, 118, 740, 76, PAPER2, RULE, 1.0, 8)
d.t(56, 142, "Pod 대역 /16", 13, INK, KR, "start", 600)
d.t(56, 168, "주소 65,536 개", 12, SOFT, MONO, "start")
d.t(764, 142, "클러스터 전체가 나눠 씁니다", 12, SOFT, KR, "end")
d.t(764, 168, "여기서 노드가 자기 몫을 받아 갑니다", 12, MUTED, KR, "end")

for i in range(4):
    x = 64 + i * 180
    d.arrow([(x + 70, 194), (x + 70, 226)], MUTED, "ar", 1.2)
    d.box(x, 230, 140, 92, PAPER2, RULE, 0.9, 6)
    d.t(x + 70, 254, f"노드 {i+1}", 13, INK, KR, "middle", 600)
    d.tone(x + 14, 266, 112, 44, ACC, 5)
    d.t(x + 70, 284, "받은 몫", 12, ACC, KR, "middle")
    d.t(x + 70, 302, "크기는 아직 모름", 11, WARN, KR, "middle")

d.t(W // 2, 356, "지금 노드는 256 대이고 오토스케일러는 더 늘리지 못하고 있습니다",
    13, MUTED, KR, "middle")
d.t(W // 2, 380, "Pod 110 개가 주소를 몇 개 쓰는지는 이 그림에 아직 없습니다",
    12, WARN, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-09.ip-budget-topology.svg"))
print("ok")
