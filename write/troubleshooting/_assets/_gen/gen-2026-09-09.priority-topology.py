# 2026-09-09 B 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "같은 클러스터에 무엇이 몇 벌 떠 있고 언제 만들어졌나"이지 선점 연쇄가 아니다.
# 밀려나는 연쇄는 원인 분석 절의 preemption-cascade 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 시점 축을 경계로 두 벌을 갈라 놓는다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W, H = 812, 424
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-09 B",
      "같은 클러스터의 두 벌",
      "시계열 수집 서비스가 한 클러스터에 두 벌 떠 있다. 하나는 우선순위 클래스를 만들기 "
      "전부터 돌던 운영용이고, 다른 하나는 장애 당일 배포한 고객 전용이다.",
      lead="두 벌의 차이는 무엇을 하느냐가 아니라 언제 만들어졌느냐입니다")

d.box(40, 116, 736, 60, PAPER2, RULE, 1.0, 8)
d.t(56, 140, "전날 — 우선순위 클래스 넷을 새로 만들고 medium 을 기본값으로 지정", 13, INK, KR, "start")
d.t(56, 162, "이미 떠 있던 Pod 에 무엇이 적용되는지는 이 그림에 없습니다", 12, WARN, KR, "start")

CY = 202
d.box(40, CY, 360, 132, PAPER2, RULE, 1.0, 8)
d.t(56, CY + 24, "운영용 — 변경 이전부터 돌던 것", 12, SOFT, KR, "start", 600)
for i in range(3):
    x = 60 + i * 112
    d.box(x, CY + 40, 96, 72, PAPER2, RULE, 0.9, 5)
    d.t(x + 48, CY + 68, "Pod", 12, INK, KR, "middle", 600)
    d.t(x + 48, CY + 90, "메모리에 상태", 11, SOFT, KR, "middle")

d.box(416, CY, 360, 132, PAPER2, RULE, 1.0, 8)
d.t(432, CY + 24, "고객 전용 — 장애 당일 배포", 12, SOFT, KR, "start", 600)
d.t(760, CY + 24, "매니페스트에 우선순위 누락", 12, WARN, KR, "end")
for i in range(3):
    x = 436 + i * 112
    d.tone(x, CY + 40, 96, 72, ACC, 5)
    d.t(x + 48, CY + 68, "Pod", 12, ACC, KR, "middle", 600)
    d.t(x + 48, CY + 90, "같은 노드 풀", 11, SOFT, KR, "middle")

d.t(W // 2, 372, "아무것도 크래시하지 않았고 노드도 죽지 않았습니다", 13, MUTED, KR, "middle")
d.t(W // 2, 396, "Pod 가 사라진 자리에 남은 이벤트는 Preempted by another pod 하나뿐입니다",
    12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-09.priority-topology.svg"))
print("ok")
