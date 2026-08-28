# 03-02 / 11-01 §Service → Endpoints — 라벨 셀렉터가 Pod 를 자동 등록
# 본문(11-01): kubectl expose 로 ClusterIP 10.96.154.45 가 붙고, Service 는 app=kiada 라벨을
#   가진 Pod 를 스스로 찾아 Endpoints 에 등록한다. Pod 가 늘거나 죽으면 그 목록만 갱신되고
#   ClusterIP 는 그대로라 클라이언트는 영향을 받지 않는다.
# 실측 Pod: 10.244.1.8 / 10.244.1.9 (worker) · 10.244.2.5 (worker2)
# 타입 스펙: type-architecture.md — 이름표 하나가 라벨로 여럿을 물어 오는 구조라 참조 매핑. 중간의 Endpoints 가
#           '갱신되는 목록' 임을 드러내야 하므로 별도 칸으로 세운다.
#           Service → Endpoints → 파드 셋으로 이어지는 참조 매핑이고, 갱신되는 목록인 Endpoints 를
#           가운데 칸으로 세웠다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 640
d = D(W, H, "KUBERNETES IN ACTION · 03-02",
      "라벨이 붙는 순간 Endpoints 가 스스로 늘어난다",
      "Service 는 고정 IP 를 가진 이름표이고, app=kiada 라벨을 가진 Pod 를 스스로 찾아 "
      "Endpoints 에 등록한다. Pod 가 바뀌면 그 목록만 갱신되고 ClusterIP 는 그대로다.",
      lead="Service 를 건드리지 않았는데 새 Pod 가 라벨을 갖자마자 목록에 들어왔다")

# 코리도어가 34px 뿐이라 칩이 Endpoints 상자를 덮었다 — 양쪽을 벌리고 칩을 줄인다
SVC, EP = (150, 330), (500, 330)
PODS = [(845, 246), (845, 344), (845, 442)]

ddx.band(d, 104, 584, "클라이언트가 아는 것은 ClusterIP 하나뿐이고, 뒤의 목록이 바뀌어도 그대로다")

def box(cx, cy, w, h, t, s, tag, c):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 18, ddx.fit(t, 13, w - 18, t), 13, c,
        MONO if all(ord(ch) < 128 or ch in ':.' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, w - 16, t), 11, MUTED, MONO)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, t), 10, SOFT, KR)

box(*SVC, 240, 120, "Service: kiada", "10.96.154.45", "이 IP 는 안 바뀐다", ACC)
d.t(SVC[0], SVC[1] + 82, "셀렉터  app=kiada", 11, ACC, MONO)

d.box(EP[0] - 140, EP[1] - 104, 280, 208, PAPER2, OK, 1.1, 6)
d.t(EP[0], EP[1] - 74, "Endpoints — 자동 갱신", 13, OK, KR, "middle", 600)
for i, ip in enumerate(["10.244.1.8:8080", "10.244.1.9:8080", "10.244.2.5:8080"]):
    d.t(EP[0], EP[1] - 36 + i * 30, ip, 12, MUTED, MONO)
d.t(EP[0], EP[1] + 78, "Pod 가 늘거나 죽으면 이 목록만 바뀐다", 10, SOFT, KR)

for i, (cx, cy) in enumerate(PODS):
    node = "worker2 노드" if i == 2 else "worker 노드"
    box(cx, cy, 230, 84, ["kiada-…-bhgc5", "kiada-…-8phwt", "kiada-…-2vm7s"][i],
        ["10.244.1.8", "10.244.1.9", "10.244.2.5"][i], f"app=kiada · {node}", INFO)

d.path(f"M {SVC[0]+120+6} {SVC[1]} L {EP[0]-140-10} {EP[1]}", ACC, 1.8, m="acc")
d.chip(313, SVC[1], "라벨로", ACC, 11)

SPINE = 690
d.path(f"M {EP[0]+140+6} {EP[1]} L {SPINE} {EP[1]}", MUTED, 1.4)
d.path(f"M {SPINE} {PODS[0][1]} L {SPINE} {PODS[2][1]}", MUTED, 1.4)
for cx, cy in PODS:
    d.path(f"M {SPINE} {cy} L {cx-115-10} {cy}", MUTED, 1.4, m="ar")

d.t(36, 520, "스케일하자 세 Pod 의 IP 를 Service 가 스스로 물었다 — Endpoints 가 자동으로 늘어난 것이다.",
     12, MUTED, KR, "start")
d.t(36, 544, "그중 하나는 다른 노드(worker2)에 있었다 — 라벨만 맞으면 노드는 상관하지 않는다.",
     12, MUTED, KR, "start")
d.legend(600, [("고정 진입점", ACC), ("자동 갱신되는 목록", OK), ("라벨을 가진 Pod", INFO)])
d.save("03-02-service-endpoints-selector.svg")
print("ok service-endpoints-selector")
