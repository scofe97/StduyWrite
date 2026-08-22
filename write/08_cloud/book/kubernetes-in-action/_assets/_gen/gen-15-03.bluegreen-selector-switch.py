# 15-03 §4 — 같은 도구를 정반대로 쓴다
# 본문이 Canary 와 Blue/Green 을 "같은 label selector 를 정반대로 쓴다"로 묶는다. 그러니 전환
# 장면만 그리면 절반이고, 라벨을 같게 주느냐 다르게 주느냐가 함께 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 724, "KUBERNETES IN ACTION · 15-03",
      "selector 한 줄을 바꿔 한 번에 넘긴다",
      "두 그룹이 서로 다른 label 을 쓰므로 selector 는 언제나 한 쪽만 잡는다. 전환은 Service 의 "
      "selector 를 고쳐 쓰는 일이고, Deployment 컨트롤러의 네이티브 전략이 아니다.",
      "strategy.type 에 Blue/Green 을 적을 수는 없다")

def scene(y0, label, sel, blue_on, green_on, note, note_c):
    ddx.band(d, y0, y0 + 232, label, x=24, w=1172)
    d.box(60, y0 + 60, 300, 84, PAPER2, ACC, 1.2, 6)
    d.t(210, y0 + 90, "Service", 13, ACC, KR, "middle", 600)
    d.t(210, y0 + 114, sel, 11, ACC, MONO)
    # ey 는 Service 오른쪽 변에서 나가는 높이다. 한 점에서 같이 나가면 두 길이 겹쳐 그려지고
    # 비스듬히 내려가므로, 각자의 접점을 주고 높이가 다른 쪽만 직각으로 꺾는다.
    for on, nm, col, cy, ey in ((blue_on, "Blue Deployment", "col: blue", y0 + 62, y0 + 84),
                                (green_on, "Green Deployment", "col: green", y0 + 148, y0 + 120)):
        c = OK if on else None
        ddx.node(d, 700, cy + 22, nm, col, 300, 62, c, dim=not on)
        ty = cy + 22
        seg = (f"M 364 {ey} L 544 {ty}" if ey == ty
               else f"M 364 {ey} L 456 {ey} L 456 {ty} L 544 {ty}")
        if on:
            d.path(seg, OK, 1.5, m="ok")
        else:
            d.path(seg, SOFT, 1.2, m="ar", dash="5 5")
    d.t(1040, y0 + 116, note, 11, note_c, KR)

scene(100, "전환 전", "selector  col: blue", True, False, "Green 은 떠 있지만 트래픽이 안 간다", SOFT)
scene(356, "selector 한 줄을 고친 뒤", "selector  col: green", False, True, "한 번에 전부 넘어간다", ACC)

d.t(24, 636, "Canary 와 짝을 이룬다 — Canary 는 두 Deployment 에 같은 라벨을 줘 한 Service 가 둘 다 잡게 하고 "
             "비율을 replica 수로 조절하지만, Blue/Green 은 다른 라벨을 줘 한 번에 한 쪽만 잡히게 한다.",
     11, MUTED, KR, "start")
d.t(24, 658, "그래서 추가 도구가 필요 없다. Service 의 label selector 를 바꾸는 것만으로 된다.", 11, MUTED, KR, "start")
d.legend(676, [("트래픽을 받는 쪽", OK), ("전환을 정하는 한 줄", ACC)])
d.save("15-03-bluegreen-selector-switch.svg")
print("ok")
