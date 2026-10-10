# 타입 스펙: type-dp-security-matrix — 행 = 라우트가 붙는 객체·출발·주소·조건 다섯, 열 = 남북(Gateway 부모)·동서(Service 부모). 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal(Service 와 같은 네임스페이스 조건).
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 686-690(http-app-1 parentRefs my-gateway), 1559-1588(gamma-route·gamma-ns·parentRefs kind Service echo·curl http://echo/v1). docs.cilium.io v1.20 gamma(producer route 만 지원), httproutes CRD v1.6.1(group "")
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 440
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 188, 12, 330, 16
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 44, 52
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(2)]

d = D(W, H, "CILIUM UP AND RUNNING · 07-02 §6", "남북 라우트와 동서 라우트",
      "같은 HTTPRoute 이고 부모 객체만 다르다", "같은 HTTPRoute 이고 부모 객체만 다르다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "항목", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "field", 11, MUTED, MONO)
for j, (nm, sub) in enumerate([("남북 트래픽", "Gateway 가 부모"), ("동서 트래픽", "Service 가 부모")]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, sub, 11, MUTED, KR)

rows = [
    ("라우트", ["http-app-1", "gamma-route"], None),
    ("parentRefs", ["Gateway my-gateway", 'Service echo · group ""'], None),
    ("요청 출발", ["클러스터 밖 curl", "gamma-ns 의 클라이언트"], None),
    ("접근 주소", ["172.18.255.200", "http://echo"], None),
    ("네임스페이스 조건", ["allowedRoutes Same", "Service 와 같은 네임스페이스"], 1),
]
for i, (name, cells, foc) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 27, name, 13, INK, KR if any("가" <= c <= "힣" for c in name) else MONO, "start", 600)
    for j, v in enumerate(cells):
        x = RX[j]
        if foc == j:
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
            col = ACC
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
            col = INK
        d.t(x + ROLE_W / 2, y + 27, v, 12, col, KR if any("가" <= c <= "힣" for c in v) else MONO, "middle", 600)
d.save("07-02.north-south-vs-east-west.svg")
