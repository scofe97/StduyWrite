# 03-02 §3층 계층 — 그리고 그 구조가 Pod 이름에 박힌다
# 본문·실측: kubectl create deployment 한 줄이 Deployment → ReplicaSet → Pod 세 층을 만든다.
#   실측 Pod 이름 kiada-7bc9cd6878-bhgc5 = Deployment명 - ReplicaSet 해시 - Pod 해시.
# 타입 스펙: type-tree.md — 뿌리에서 잎으로 내려가는 계층이고, 연결선은 직각 엘보로만 긋는다
#           ("never diagonal"). 이름이 곧 계층 지도라는 것이 이 장의 마무리이므로 아래에
#           이름을 세 조각으로 갈라 각 층에 잇는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 700
d = D(W, H, "KUBERNETES IN ACTION · 03-02",
      "세 층이 각각 다른 일을 지고, 그 구조가 이름에 박힌다",
      "Deployment 는 원하는 상태를 선언하고, ReplicaSet 은 개수를 지키고, Pod 가 컨테이너를 "
      "실행한다. Pod 이름의 세 조각이 그대로 이 세 층을 가리킨다.",
      lead="kubectl create deployment 한 줄이 이 세 층을 한꺼번에 만든다")

DEP, RS = (500, 224), (500, 348)
PODS = [(196, 480), (500, 480), (804, 480)]
BW, BH, PW = 420, 84, 260

ddx.band(d, 104, 644, "스케일(replicas=3)은 ReplicaSet 에 걸린다 — Deployment 는 그것을 선언만 한다")

def box(cx, cy, w, t, s, tag, c):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 20, ddx.fit(t, 13, w - 18, t), 13, c, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, w - 16, t), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, t), 10, SOFT, KR)

box(*DEP, BW, "Deployment", "원하는 상태를 선언한다", "이미지·복제본 수·업데이트 전략", INFO)
box(*RS, BW, "ReplicaSet", "개수를 지킨다", "죽으면 즉시 새 Pod 로 대체한다", OK)
for i, (cx, cy) in enumerate(PODS):
    box(cx, cy, PW, "Pod", ["kiada-…-bhgc5", "kiada-…-8phwt", "kiada-…-2vm7s"][i],
        "자기 IP · 호스트명 = Pod 이름", ACC)

d.path(f"M {DEP[0]} {DEP[1]+BH//2+6} L {RS[0]} {RS[1]-BH//2-10}", MUTED, 1.5, m="ar")
d.chip(560, 286, "만든다", MUTED, 11)

# 계층 연결은 직각 엘보 — 줄기 하나에서 세 갈래
SPINE = 412
d.path(f"M {RS[0]} {RS[1]+BH//2+6} L {RS[0]} {SPINE}", MUTED, 1.4)
d.path(f"M {PODS[0][0]} {SPINE} L {PODS[2][0]} {SPINE}", MUTED, 1.4)
for cx, cy in PODS:
    d.path(f"M {cx} {SPINE} L {cx} {cy-BH//2-10}", MUTED, 1.4, m="ar")
d.chip(620, SPINE, "N 개를 만든다", MUTED, 11)

# 이름이 곧 계층 지도
NY = 580
d.t(36, NY - 24, "Pod 이름의 세 조각이 그대로 세 층이다", 12, SOFT, KR, "start")
PARTS = [(180, "kiada", "Deployment 이름", INFO), (460, "7bc9cd6878", "ReplicaSet 해시", OK),
         (740, "bhgc5", "Pod 해시", ACC)]
for cx, txt, note, c in PARTS:
    d.o.append(f'<rect x="{cx-120}" y="{NY-16}" width="240" height="44" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, NY + 6, txt, 13, c, MONO, "middle", 600)
    d.t(cx, NY + 44, note, 10, SOFT, KR)
for x in (320, 600):
    d.t(x, NY + 8, "-", 14, SOFT, MONO)

d.legend(660, [("원하는 상태", INFO), ("개수 유지", OK), ("실행 단위", ACC)])
d.save("03-02-deployment-replicaset-pod-hierarchy.svg")
print("ok deployment-replicaset-pod-hierarchy")
