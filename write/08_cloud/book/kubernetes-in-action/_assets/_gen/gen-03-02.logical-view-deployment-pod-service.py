# 03-02 §논리 뷰 — 클러스터 규모와 무관하게 늘 같은 세 오브젝트
# 본문: "Pod 는 휘발성이라 노드 실패·삭제·축출로 언제든 사라지고, 교체된 새 Pod 는 완전히 다른
#        IP 를 갖습니다. 그래서 클라이언트는 Pod IP 가 아니라 Service IP 에 연결해야 하고,
#        Deployment 는 Pod 를 직접 만들지 않고 이 교체·복제 책임을 대신 집니다."
# 타입 스펙: 세 오브젝트의 역할이 서로 다른 방향을 보는 것이 요점이다 — Deployment 는 위에서
#           선언하고, Service 는 앞에서 진입점을 고정한다. 그래서 Pod 줄을 가운데 두고
#           선언은 위에서, 진입은 왼쪽에서 오게 배치한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 620
d = D(W, H, "KUBERNETES IN ACTION · 03-02",
      "Pod 는 갈아 끼워지고 Service IP 만 그대로 있다",
      "Deployment 는 지정된 수의 Pod 를 만들 뿐 그 외엔 관여하지 않고, Service 는 생성 시 받은 "
      "IP 를 생애 내내 유지하며 건강한 Pod 로만 보낸다.",
      lead="그래서 클라이언트는 Pod IP 가 아니라 Service IP 에 연결한다")

DEP = (620, 234)
# Service 를 왼쪽으로 붙여 Pod 열과의 코리도어를 넓힌다 — 칩이 상자를 덮었다
SVC = (140, 400)
PODS = [(430, 400), (640, 400), (850, 400)]
BW, BH, PW = 380, 88, 170

ddx.band(d, 104, 564, "Pod 가 죽고 새 IP 로 교체돼도 Service IP 는 바뀌지 않는다")

def box(cx, cy, w, h, t, s, tag, c, dash=False):
    d.o.append(f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
               f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 20, ddx.fit(t, 13, w - 18, t), 13, c, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, w - 16, t), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, t), 10, SOFT, KR)

box(*DEP, BW, BH, "Deployment: kiada", "이미지와 복제본 수를 선언한다", "그 외엔 관여하지 않는다", INFO)
box(*SVC, 200, 108, "Service: kiada", "생성 시 받은 IP", "생애 내내 안 바뀐다", ACC)
for i, (cx, cy) in enumerate(PODS):
    box(cx, cy, PW, 88, f"Pod {'ABC'[i]}", "고유 IP", "휘발성", OK, dash=(i == 1))

SPINE = 320
d.path(f"M {DEP[0]} {DEP[1]+BH//2+6} L {DEP[0]} {SPINE}", MUTED, 1.4)
d.path(f"M {PODS[0][0]} {SPINE} L {PODS[2][0]} {SPINE}", MUTED, 1.4)
for cx, cy in PODS:
    d.path(f"M {cx} {SPINE} L {cx} {cy-44-10}", MUTED, 1.4, m="ar")
d.t(300, SPINE - 12, "지정된 수만큼 만든다", 11, MUTED, KR, "start")

d.path(f"M {SVC[0]+100+6} {SVC[1]} L {PODS[0][0]-PW//2-10} {PODS[0][1]}", ACC, 1.8, m="acc")
d.chip(292, SVC[1], "건강한 쪽", ACC, 11)

d.chip(PODS[1][0], 476, "소멸 → 새 Pod(다른 IP)로 교체", OK, 11)

d.t(36, 512, "Deployment 는 Pod 를 직접 돌보지 않고 교체·복제 책임을 대신 진다 — 그것이 Pod 를 "
             "직접 만들지 않는 이유다.", 12, MUTED, KR, "start")
d.legend(580, [("선언하는 쪽", INFO), ("갈아 끼워지는 실행 단위", OK), ("고정된 진입점", ACC)])
d.save("03-02-logical-view-deployment-pod-service.svg")
print("ok logical-view")
