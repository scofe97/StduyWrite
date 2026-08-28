# 18-01 §6·§7 — 지우는 길이 셋이고 결과가 다르다
# 캡션이 세 경로와 각각의 결과를 준다. 그러니 삭제를 한 동작으로 그리면 안 되고, 파드가
# 어떻게 되는지가 경로마다 달라야 한다.
# 타입 스펙: type-flowchart.md — 완료된 Job 하나에서 지우는 방법을 무엇으로 고르느냐에 따라 파드의 운명이 셋으로 갈린다.
#           세 갈래가 서로 배타적이라 격자가 아니라 분기다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 18-01",
      "지우는 길 셋, 파드의 운명 셋",
      "Job 을 지운다는 같은 말이 파드에 서로 다른 결과를 낸다. 무엇이 회수하느냐와 언제 하느냐가 "
      "경로를 가른다.",
      "완료된 파드를 안 지우면 쌓인다")

ddx.node(d, 150, 320, "완료된 Job", "파드가 Completed 로 남아 있다", 240, 88, INFO)

PATHS = [("kubectl delete job", "사용자가 지운다", "가비지 컬렉터가 파드까지 회수", 190, OK),
         ("--cascade=orphan", "Job 만 지운다", "파드가 독립해 남는다", 320, WARN),
         ("ttlSecondsAfterFinished", "TTL 컨트롤러가", "완료 후 자동으로 지운다", 450, ACC)]

d.path("M 272 320 L 350 320", SOFT, 1.2)
d.path("M 350 190 L 350 450", SOFT, 1.2)
for t, who, result, cy, c in PATHS:
    d.box(430, cy - 38, 320, 76, PAPER2, c, 1.1, 6)
    d.t(450, cy - 10, t, 11, c, MONO, "start", 600)
    d.t(450, cy + 14, who, 10, MUTED, KR, "start")
    d.path(f"M 350 {cy} L 424 {cy}", c, 1.4,
           m="ok" if c is OK else ("warn" if c is WARN else "acc"))
    ddx.node(d, 990, cy, result, "", 380, 60, c)
    d.path(f"M 752 {cy} L 794 {cy}", c, 1.3,
           m="ok" if c is OK else ("warn" if c is WARN else "acc"))

d.t(24, 540, "TTL 을 걸어 두면 사람이 잊어도 정리된다. 컨트롤 플레인이 결국 회수하기는 하지만, "
             "공식 문서가 경계하는 것은 그 사이에 쌓이는 파드다.", 11, MUTED, KR, "start")
d.t(24, 562, "쌓인 파드가 클러스터 성능을 떨어뜨리고 최악의 경우 클러스터를 멈추게 할 수도 있다.",
     11, MUTED, KR, "start")
d.legend(588, [("함께 회수", OK), ("남겨 둔다", WARN), ("자동 정리", ACC)])
d.save("18-01-delete-paths.svg")
print("ok")
