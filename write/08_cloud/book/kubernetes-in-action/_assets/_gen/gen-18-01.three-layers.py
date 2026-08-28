# 18-01 §1 — 만드는 주체가 층마다 다르다
# "사용자 → Job → 파드 → 컨테이너"를 한 줄로 그리면 누가 무엇을 만드는지가 뭉개진다.
# 각 층이 어디서 도는지를 함께 놓아야 Job 컨트롤러와 kubelet 의 분업이 보인다.
# 타입 스펙: type-layers.md — 같은 x·같은 폭의 전폭 띠 넷이 세로로 쌓이고 각 띠가 이름 · 어디서 · 무엇을 순으로 읽힌다.
#           선언 → 저장 → 감시 → 집행이 실제로 층위라, "계층이 아닌 것을 층으로 그리지 말라"는
#           정본의 안티패턴에 걸리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 656, "KUBERNETES IN ACTION · 18-01",
      "만드는 주체가 층마다 바뀐다",
      "사용자는 Job 오브젝트만 만든다. 그것을 보고 파드를 만드는 것은 컨트롤 플레인의 Job 컨트롤러이고, "
      "그 파드 안 컨테이너를 실제로 띄우는 것은 워커 노드의 kubelet 이다.",
      "선언 · 감시 · 집행이 각각 다른 자리에 있다")

LAYERS = [("사용자", "kubectl apply", "Job 매니페스트를 낸다", 176, INFO),
          ("API 서버", "오브젝트를 담는다", "Job 이 저장된다", 296, INFO),
          ("Job 컨트롤러", "컨트롤 플레인에서", "파드를 만든다", 416, ACC),
          ("kubelet", "워커 노드에서", "컨테이너를 띄운다", 536, OK)]
for t, where, does, cy, c in LAYERS:
    d.box(120, cy - 40, 960, 80, PAPER2, c, 1.1, 6)
    d.t(160, cy - 8, t, 13, c, KR, "start", 600)
    d.t(400, cy - 8, where, 11, MUTED, KR, "start")
    d.t(700, cy - 8, does, 11, MUTED, KR, "start")
for cy in (176, 296, 416):
    d.path(f"M 600 {cy+44} L 600 {cy+72}", MUTED, 1.4, m="ar")

d.t(24, 600 - 8, "그래서 Job 을 지워도 파드가 곧바로 사라지지 않는 경우가 생긴다 — 지우는 주체와 회수하는 주체가 "
                 "다르기 때문이다.", 11, MUTED, KR, "start")
d.legend(608, [("선언과 저장", INFO), ("파드를 만드는 자", ACC), ("컨테이너를 띄우는 자", OK)])
d.save("18-01-three-layers.svg")
print("ok")
