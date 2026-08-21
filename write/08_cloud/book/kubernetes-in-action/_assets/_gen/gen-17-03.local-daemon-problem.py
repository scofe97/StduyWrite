# 17-03 §0 — 무엇이 문제인가
# 세 방법을 다루기 전에 왜 기본 Service 로는 안 되는지가 먼저 서야 한다. 그러니 해법이 아니라
# 실패 장면이어야 하고, 노드를 건너가는 화살표가 그 실패의 증거다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 17-03",
      "같은 노드에 있는데 남의 노드로 간다",
      "보통 Service 는 클러스터 전역의 엔드포인트 중에서 고른다. 그래서 같은 노드에 에이전트가 "
      "있어도 다른 노드의 것으로 갈 수 있다.",
      "로그 수집기·수집 에이전트처럼 노드에 묶여야 하는 호출")

for i, (nm, c) in enumerate((("노드 A", OK), ("노드 B", SOFT))):
    x0 = 90 + i * 540
    d.box(x0, 200, 460, 230, PAPER, RULE, 0.9, 8)
    d.t(x0 + 230, 228, nm, 11, SOFT, KR)
    if i == 0:
        ddx.node(d, x0 + 130, 300, "클라이언트 파드", "여기서 부른다", 200, 62, INFO)
        ddx.node(d, x0 + 340, 300, "에이전트", "바로 옆에 있다", 180, 62, OK)
        d.t(x0 + 230, 388, "가까운데 안 갈 수도 있다", 11, WARN, KR)
    else:
        ddx.node(d, x0 + 230, 300, "에이전트", "다른 노드", 200, 62, SOFT)
        d.t(x0 + 230, 388, "여기로 갈 수 있다", 11, BAD, KR)

d.path("M 320 340 L 380 400 L 700 400 L 860 340", BAD, 1.5, m="bad", dash="6 5")
d.t(590, 424, "Service 는 전역 엔드포인트에서 고른다", 11, BAD, KR)

d.t(24, 502, "노드 로그를 그 노드의 수집기에 보내야 하는데 남의 노드로 가면, 네트워크가 낭비되고 "
             "노드 귀속 메타데이터도 어긋난다.", 11, MUTED, KR, "start")
d.t(24, 524, "그래서 '같은 노드로만'을 강제하는 길이 필요하다 — 이 편이 다루는 셋이 그것이다.",
     11, MUTED, KR, "start")
d.legend(552, [("부르는 쪽", INFO), ("가까운 에이전트", OK), ("실제로 갈 수 있는 곳", BAD)])
d.save("17-03-local-daemon-problem.svg")
print("ok")
