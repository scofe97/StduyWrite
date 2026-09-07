# 01-02 §4 — 원문이 나누는 물리 매체 분류. 파동이 고체를 따라 인도되느냐 퍼지느냐가 첫 갈림이다.
# 타입 스펙: type-tree — 분류 자체가 트리다. 부모의 성질이 자식에게 이어지고,
#           잎마다 원문이 적은 전형적 속도와 특징을 싣는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 952, 568
COLX = [24, 196, 384]
COLW = [148, 164, 544]
NH = 56
LEAF_Y = [128 + i * 68 for i in range(5)]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-02 §4",
      "비트가 타고 건너는 것",
      "원문 1.2.2 의 매체 분류. 첫 갈림은 파동이 고체 매체를 따라 인도되느냐(유도) 대기와 우주로 퍼지느냐(비유도)다. 경로 위의 구간마다 종류가 달라도 된다.",
      "위 층이 감춘 제약 — MTU·충돌·페이딩 — 이 전부 여기서 나옵니다")

def node(col, y, name, sub, c=None, w=None):
    x, ww = COLX[col], (w or COLW[col])
    if c: d.tone(x, y, ww, NH, c, 6)
    else: d.box(x, y, ww, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 24, name, 12, c if c else INK, KR, "start", 600)
    d.t(x + 14, y + 43, sub, 11, MUTED, KR, "start")
    return x, y, ww

def elbow(p, ch):
    px, py, pw = p; cx, cy, cw = ch
    mid = px + pw + (cx - (px + pw)) / 2
    d.arrow([(px + pw, py + NH / 2), (mid, py + NH / 2), (mid, cy + NH / 2), (cx - 4, cy + NH / 2)],
            MUTED, "ar", 1.1)

g_y = (LEAF_Y[0] + LEAF_Y[2]) / 2
u_y = (LEAF_Y[3] + LEAF_Y[4]) / 2
root = node(0, (g_y + u_y) / 2, "물리 매체", "송신기와 수신기 사이")
guided = node(1, g_y, "유도 매체", "고체를 따라 인도")
unguided = node(1, u_y, "비유도 매체", "대기와 우주로 퍼짐")
elbow(root, guided); elbow(root, unguided)

LEAVES = [
    (guided, "꼬임쌍 구리선", "LAN 10 Mbps ~ 10 Gbps · 카테고리 6a 는 100 m 까지 10 Gbps · 가장 싸고 흔합니다", None),
    (guided, "동축 케이블", "수백 Mbps · 두 도체가 동심원 · 유도된 공유 매체로 쓸 수 있습니다", None),
    (guided, "광섬유", "수십 ~ 수백 Gbps · 전자기 간섭 면역 · 100 km 까지 저감쇠 · 도청도 극히 어렵습니다", ACC),
    (unguided, "지상 무선", "1~2 m · 10~수백 m · 수십 km 셋으로 갈립니다 · 경로 손실과 페이딩을 받습니다", None),
    (unguided, "위성 무선", "수백 Mbps · 정지궤도는 36,000 km · 저궤도는 훨씬 가깝습니다", None),
]
for i, (parent, name, sub, c) in enumerate(LEAVES):
    elbow(parent, node(2, LEAF_Y[i], name, sub, c))

d.t(24, 496, "물리 링크의 비용은 자재가 아니라 설치 인건비입니다 — 그래서 건물 지을 때 당장 안 쓸 매체까지 방마다 미리 깔아 둡니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("장거리에서 선호되는 매체", ACC)])
d.save("01-02.physical-media.svg")
