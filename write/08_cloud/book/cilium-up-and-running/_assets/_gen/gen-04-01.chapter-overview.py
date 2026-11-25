# 04-01 개념도 — 「Pod 대역을 누가 나눠 주는가」 물음에서 갈리는 IPAM 다섯 모드와 밑에 깔린 3단계 분할, 그리고 갈래 밖 주소 계열 선택.
# 본문 요구(04-01 「학습 목표」 개요 문단과 「Pod 대역을 누가 나누는가」): 3단계 분할(§1) 위에서 가운데 단계(노드 PodCIDR)를 누가 나누는지로
#   Host Scope(§2, Kubernetes) / Cluster Scope(§3, 기본값)·Multi-Pool(§4, cilium-operator) / CRD-backed·ENI(§5, 외부 시스템)로 갈리고,
#   주소 계열(§6, IPv4·듀얼 스택·IPv6 전용)은 이 배분 갈래 밖 곁가지로 놓인다.
# 값 근거: 04-01 본문 §1~§6 및 원문 사본 ch04.txt 줄 98-122 · 169-188 · 249-269 · 491-524 · 636-667 · 949-969 · 1083-1133,
#          docs.cilium.io/en/v1.20/network/concepts/ipam/ (1.20.5).
# 타입 스펙: type-tree — 한 질문(노드 PodCIDR 배분 주체)에서 3갈래(5모드)가 아래로 뻗고, 밑바탕 3단계와 곁가지(§6)를 함께 놓은 갈래 지도.
#             고른 이유: 이 장의 줄기가 「누가 나눠 주는가 한 물음에서 다섯 모드가 갈린다」는 분류 갈래이므로 직각 elbow 분기 트리가 가장 정확하다.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 668


def fam(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


d = D(W, H, "CILIUM UP AND RUNNING · 04-01 OVERVIEW",
      "Pod 대역을 누가 나누는지로 갈리는 IPAM 모드 다섯 가지",
      "클러스터 풀을 노드 PodCIDR 과 Pod IP 로 나누는 3단계 가운데, 노드 PodCIDR 을 누가 나눠 주는지에 따라 다섯 모드가 갈립니다. "
      "쿠버네티스가 나누는 Host Scope, 오퍼레이터가 나누는 Cluster Scope(기본값)와 Multi-Pool, 주소 출처가 Cilium 밖에 있는 CRD-backed 와 ENI 입니다. "
      "주소 계열(IPv4·듀얼 스택·IPv6 전용)은 배분 갈래 밖 곁가지입니다.",
      lead="윗줄은 3단계 분할, 가운데 갈래는 노드 대역 배분 주체, 아래 점선 칸은 갈래 밖 주소 계열이고, 칩은 해당 절입니다.")

# 1. 윗줄: 3단계 분할 바탕 (§1)
BY, BH = 96, 56
d.box(24, BY, 932, BH, PAPER2, RULE, 0.9, 6)
d.chip(54, BY + 28, "§1", MUTED, 11)
steps = [
    (88, 224, "1 클러스터 풀", "10.0.0.0/8 · 10.244.0.0/16", INFO),
    (360, 296, "2 노드 몫 · PodCIDR (누가 나눌까?)", "모드를 가르는 갈림길", ACC),
    (704, 232, "3 개별 Pod IP", "노드 에이전트가 로컬 배정", OK),
]
for sx, sw, st, ss, sc in steps:
    if sc == ACC:
        d.tone(sx, BY + 6, sw, BH - 12, ACC, r=5, op="16", sw=1.3)
        tc = ACC
    else:
        d.box(sx, BY + 6, sw, BH - 12, PAPER, RULE, 0.9, 5)
        tc = INK
    d.t(sx + sw / 2, BY + 24, st, 13, tc, KR, "middle", 600)
    d.t(sx + sw / 2, BY + 42, ss, 11, MUTED, fam(ss), "middle")
d.arrow([(314, BY + 28), (358, BY + 28)], MUTED, "ar", 1.4)
d.arrow([(658, BY + 28), (702, BY + 28)], MUTED, "ar", 1.4)

# 트리 루트 → 3갈래 직각 버스 (먼저 선을 그린다)
ROOT_X = 508
ROOT_Y = BY + BH
BUS1_Y = 180
G_XS = [112, 394, 770]  # 갈래 A, B, C 중심 x
GY = 204
GH = 56
GW = [176, 364, 364]

d.line(ROOT_X, ROOT_Y, ROOT_X, BUS1_Y, MUTED, 1.4)
d.line(G_XS[0], BUS1_Y, G_XS[2], BUS1_Y, MUTED, 1.4)
for gx in G_XS:
    d.arrow([(gx, BUS1_Y), (gx, GY - 2)], MUTED, "ar", 1.4)

# 갈래 A → 잎 1
d.arrow([(G_XS[0], GY + GH), (G_XS[0], 294)], INFO, "info", 1.3)

# 갈래 B → 잎 2 (Cluster Scope, Multi-Pool)
B_LEFT, B_RIGHT = 300, 488
BUS_B_Y = 278
d.line(G_XS[1], GY + GH, G_XS[1], BUS_B_Y, OK, 1.3)
d.line(B_LEFT, BUS_B_Y, B_RIGHT, BUS_B_Y, OK, 1.3)
d.arrow([(B_LEFT, BUS_B_Y), (B_LEFT, 294)], ACC, "acc", 1.4)
d.arrow([(B_RIGHT, BUS_B_Y), (B_RIGHT, 294)], OK, "ok", 1.3)

# 갈래 C → 잎 2 (CRD-backed, ENI)
C_LEFT, C_RIGHT = 676, 864
BUS_C_Y = 278
d.line(G_XS[2], GY + GH, G_XS[2], BUS_C_Y, WARN, 1.3)
d.line(C_LEFT, BUS_C_Y, C_RIGHT, BUS_C_Y, WARN, 1.3)
d.arrow([(C_LEFT, BUS_C_Y), (C_LEFT, 294)], WARN, "warn", 1.3)
d.arrow([(C_RIGHT, BUS_C_Y), (C_RIGHT, 294)], WARN, "warn", 1.3)

# 2. 1차 갈래 박스 (주체)
groups = [
    (G_XS[0], GW[0], "갈래 A · 쿠버네티스", "kube-controller-manager", INFO),
    (G_XS[1], GW[1], "갈래 B · Cilium 오퍼레이터 배분", "cilium-operator → CiliumNode", OK),
    (G_XS[2], GW[2], "갈래 C · 주소 출처가 Cilium 밖", "외부 오퍼레이터 · cilium-operator → EC2 API", WARN),
]
for gx, gw, title, sub, col in groups:
    d.tone(gx - gw / 2, GY, gw, GH, col, r=6, op="12", sw=1.1)
    d.t(gx, GY + 24, title, 13, col, KR, "middle", 600)
    d.t(gx, GY + 44, sub, 10 if len(sub) > 20 and fam(sub) == MONO else 11, MUTED, fam(sub), "middle")


def leaf(cx, y, w, h, title, sec, col, lines, focal=False):
    x = cx - w / 2
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="16", sw=1.5)
        tc = ACC
    else:
        d.tone(x, y, w, h, col, r=6, op="10", sw=1.0)
        tc = col
    d.t(x + 12, y + 26, title, 14, tc, MONO, "start", 700)
    d.chip(x + w - 24, y + 21, sec, tc, size=11)
    for idx, (txt, is_mono) in enumerate(lines):
        f = MONO if is_mono and fam(txt) == MONO else KR
        sz = 11 if f == MONO else 13
        clr = INK if idx == 0 else MUTED
        d.t(x + 12, y + 52 + idx * 24, txt, sz, clr, f, "start")


# 3. 잎 노드 (5가지 IPAM 모드)
LY, LH = 296, 152
leaf(G_XS[0], LY, 176, LH, "Host Scope", "§2", INFO, [
    ("Node.spec.podCIDRs", True),
    ("10.244.1.0/24", True),
    ("노드당 1개 · 확장 불가", False),
])

leaf(B_LEFT, LY, 176, LH, "Cluster Scope", "§3", ACC, [
    ("기본 모드 (Cilium)", False),
    ("10.0.0.0/8 → /24", True),
    ("정적 풀 · 몫 1개", False),
], focal=True)

leaf(B_RIGHT, LY, 176, LH, "Multi-Pool", "§4", OK, [
    ("CiliumPodIPPool", True),
    ("주석 · 셀렉터 선택", False),
    ("풀별 /27 동적 추가", False),
])

leaf(C_LEFT, LY, 176, LH, "CRD-backed", "§5", WARN, [
    ("spec.ipam.available", True),
    ("status.ipam.inuse", True),
    ("직접 라우팅만", False),
])

leaf(C_RIGHT, LY, 176, LH, "AWS ENI", "§5", WARN, [
    ("status.eni.enis", True),
    ("보조 IP /32 · PD /28", False),
    ("VPC 직접 · NAT 없음", False),
])

# 4. 갈래 밖 곁가지: 주소 계열 (§6)
SY, SH = 480, 108
d.o.append(f'<rect x="24" y="{SY}" width="932" height="{SH}" rx="6" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 4"/>')
d.chip(54, SY + 24, "§6", MUTED, 11)
d.t(88, SY + 28, "갈래 밖 곁가지 — 주소 계열 선택", 14, INK, KR, "start", 600)
d.t(330, SY + 28, "모든 IPAM 모드 위에서 고름 (ENI IPv6 베타)", 13, MUTED, KR, "start")

fams = [
    (40, 224, "IPv4 단독", "호환 최우선 · 기본", MUTED),
    (284, 320, "듀얼 스택 (IPv4 + IPv6)", "10.244.1.117 · fd00:10:244:1::8204", MUTED),
    (624, 316, "IPv6 전용 (SingleStack)", "2001:db8:10:1::4d69 · NAT64·DNS64", MUTED),
]
for fx, fw, ft, fs, fc in fams:
    d.box(fx, SY + 46, fw, 48, PAPER, fc if fc != MUTED else RULE, 1.0, 5)
    d.t(fx + fw / 2, SY + 66, ft, 13, INK if fc == MUTED else fc, KR, "middle", 600)
    d.t(fx + fw / 2, SY + 84, fs, 11 if fam(fs) == MONO else 13, MUTED, fam(fs), "middle")

d.legend(H - 52, [
    ("쿠버네티스 배분", INFO),
    ("기본 모드", ACC),
    ("Cilium 오퍼레이터 배분", OK),
    ("외부 출처", WARN),
    ("갈래 밖 곁가지", MUTED),
])
d.save("04-01.chapter-overview.svg")
print("ok 04-01 overview")
