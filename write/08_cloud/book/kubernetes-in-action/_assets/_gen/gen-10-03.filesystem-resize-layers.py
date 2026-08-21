# 10-03 §1 — 벽을 넓히는 일과 대장을 고치는 일
# 앞 도식이 두 층을 세웠으므로 여기서는 그 각각을 누가 언제 하는지가 주제다.
# 두 단계가 다른 주체·다른 시점이라는 것이 요점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 10-03",
      "두 층을 각각 넓혀야 끝난다",
      "PVC 의 용량을 올리면 먼저 밑바탕 블록 디바이스가 커지고, 그다음 그 위 파일시스템이 늘어난 칸을 "
      "쓰도록 확장된다. 둘을 하는 주체와 시점이 다르다.",
      "1Gi → 3Gi")

def layer(y0, label, who, when, what, c, focal):
    ddx.band(d, y0, y0 + 184, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    ddx.node(d, 220, y0 + 104, who, when, 300, 84, c)
    d.box(560, y0 + 62, 560, 84, PAPER2, c, 1.1, 6)
    d.t(840, y0 + 94, what[0], 12, c, KR, "middle", 600)
    d.t(840, y0 + 120, what[1], 11, MUTED, KR)
    d.path(f"M 372 {y0+104} L 552 {y0+104}", c, 1.4, m="ok" if c is OK else "acc")

layer(100, "1 층 — 블록 디바이스", "CSI 컨트롤러", "PVC 를 고친 직후", 
      ("벽에 칸을 더 붙인다", "스토리지 쪽 볼륨이 커진다"), OK, False)
layer(308, "2 층 — 파일시스템", "노드의 kubelet · CSI 노드 플러그인", "그 볼륨을 쓰는 파드가 있는 노드에서",
      ("대장이 늘어난 칸을 쓰게 한다", "resize2fs 같은 확장"), ACC, True)

d.t(24, 536, "그래서 파드가 없으면 2 층이 미뤄진다. 파드를 띄워야 그 노드에서 파일시스템 확장이 일어나고, "
             "그때 df 로 본 크기가 비로소 늘어난다.", 11, MUTED, KR, "start")
d.t(24, 558, "PVC 의 CAPACITY 가 3Gi 인데 컨테이너 안 df 는 1Gi 로 보이는 구간이 이 사이다.", 11, MUTED, KR, "start")
d.legend(584, [("스토리지 쪽", OK), ("노드 쪽", ACC)])
d.save("10-03-filesystem-resize-layers.svg")
print("ok")
