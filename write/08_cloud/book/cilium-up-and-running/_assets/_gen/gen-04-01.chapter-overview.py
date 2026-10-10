# 타입 스펙: type-dp-security-matrix — IPAM 다섯 모드 × 대역 결정 주체·노드 배분 주체·노드당 대역 수·쓰는 곳 비교 행렬.
# 사실 출처: 추출본 cil4.txt 줄 98-122 · 133-139 · 209-211 · 358-362 · 636-663, docs.cilium.io/en/stable/network/concepts/ipam/ (1.20.2).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

LP, COMP_W, GAP, ROLE_W, RGAP = 12, 208, 12, 156, 12
HDR_Y, HDR_H, ROW_Y0, STRIDE, ROW_H = 96, 40, 148, 48, 40
roles = ["대역을 정하는 주체", "노드에 나눠 주는 주체", "노드당 대역 수", "쓰는 곳"]
rows = [
    ("Kubernetes Host Scope", "", [("Kubernetes", INFO), ("kube-controller-manager", INFO), ("1개", None), ("어느 클러스터든", None)]),
    ("Cluster Scope", "기본", [("Cilium · Helm 값", INFO), ("cilium-operator", "focal"), ("1개", None), ("어느 클러스터든", None)]),
    ("Multi-Pool", "", [("CiliumPodIPPool", INFO), ("cilium-operator", INFO), ("풀마다 여러 개", None), ("멀티 테넌트", None)]),
    ("CRD-backed", "", [("외부 시스템", WARN), ("외부 오퍼레이터", WARN), ("주소 목록", None), ("관리형 쿠버네티스", None)]),
    ("ENI", "", [("AWS 서브넷", WARN), ("operator · EC2 API", INFO), ("ENI 별 여러 개", None), ("AWS(EKS·EC2)", None)]),
]
W = LP + COMP_W + GAP + 4 * ROLE_W + 3 * RGAP + 48
rows_bottom = ROW_Y0 + (len(rows) - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 24
H = LEG_Y + 46
d = D(W, H, "CILIUM UP AND RUNNING · 04-01", "IPAM 모드 다섯 가지 비교",
      "노드 PodCIDR 을 누가 정하고 누가 나눠 주느냐로 모드가 갈립니다",
      "행 = IPAM 모드 · 열 = 대역을 다루는 방식")

def rx(j): return LP + COMP_W + GAP + j * (ROLE_W + RGAP)

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + COMP_W / 2, HDR_Y + 25, "IPAM 모드", 13, INK, KR, "middle", 600)
for j, r in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 25, r, 13, INK, KR, "middle", 600)

def cell_font(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 25, name, 11, INK, MONO, "start", 600)
    if hint:
        d.t(LP + COMP_W - 12, y + 25, hint, 13, MUTED, KR, "end")
    for j, (txt, c) in enumerate(cells):
        x = rx(j)
        fam = cell_font(txt)
        size = 13 if fam == KR else 10
        if c == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="12", sw=1.4)
            d.t(x + ROLE_W / 2, y + 25, txt, size, ACC, fam, "middle", 600)
        elif c:
            d.tone(x, y, ROLE_W, ROW_H, c, r=4, op="12", sw=1.0)
            d.t(x + ROLE_W / 2, y + 25, txt, size, c, fam, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER, RULE, 0.9, 4)
            d.t(x + ROLE_W / 2, y + 25, txt, size, INK, fam, "middle")

d.legend(LEG_Y, [("클러스터 안이 정함", INFO), ("클러스터 밖이 정함", WARN), ("반복 등장하는 주체", ACC)])
d.save("04-01.chapter-overview.svg")
