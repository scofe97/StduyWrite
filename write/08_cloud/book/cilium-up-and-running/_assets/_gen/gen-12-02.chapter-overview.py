# 타입 스펙: type-dp-security-matrix — 정책 종류(CiliumNetworkPolicy · CiliumClusterwideNetworkPolicy · CIDR 규칙 · 엔티티 규칙 · deny 규칙)의 범위·셀렉터·우선순위 비교 행렬. 배정된 matrix 가 스펙 목록에 없어 비교 행렬 스펙의 이 타입으로 선언했다.
# 사실 출처: Cilium Up and Running 12장 cil12.txt 줄 585-608(fromEndpoints), 643-690(CCNP), 705-780(엔티티·예약 라벨), 950-985(CIDR 규칙), 1055-1110(Deny 규칙·우선순위)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 470
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 226, 12, 211, 14
HDR_Y, HDR_H = 96, 44
ROW_Y0, ROW_H, STRIDE = 152, 48, 56
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 12-02", "정책 종류별 적용 범위와 셀렉터와 우선순위",
      "Cilium 정책은 identity 를 기반으로 클러스터 내부와 외부, 허용과 거부를 확장한다",
      "Cilium 정책은 identity 를 기반으로 클러스터 내부와 외부, 허용과 거부를 확장한다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 27, "정책 종류", 13, INK, KR, "middle", 600)
for j, (nm, code) in enumerate([("적용 범위", "scope"), ("셀렉터 문법", "selector"), ("우선순위와 동작", "precedence")]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 27, f"{nm} ({code})", 12, INK, KR, "middle", 600)

rows = [
    ("CiliumNetworkPolicy", "단일 네임스페이스", "endpointSelector", "allow 평가 · default deny 진입", INFO, False),
    ("CiliumClusterwideNetworkPolicy", "클러스터 전체", "endpointSelector: {}", "전역 적용 · default deny 주의", INFO, False),
    ("CIDR 규칙", "외부 IP 대역", "toCIDR / fromCIDR", "ipcache 신원 할당 · allow 평가", INFO, False),
    ("엔티티 규칙", "내외부 예약 그룹", "toEntities / fromEntities", "예약 라벨 세트 매칭 · allow 평가", INFO, False),
    ("Deny 규칙", "네임스페이스 또는 클러스터", "ingressDeny / egressDeny", "allow 보다 항상 우선 승리", ACC, True),
]

for i, (kind, scope, selector, prec, col, focal) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 29, kind, 11 if len(kind) > 24 else 12, INK, MONO if "Cilium" in kind else KR, "start", 600)

    # col 0: scope
    d.box(RX[0], y, ROLE_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(RX[0] + ROLE_W / 2, y + 29, scope, 12, INK, KR, "middle")

    # col 1: selector
    d.box(RX[1], y, ROLE_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(RX[1] + ROLE_W / 2, y + 29, selector, 12, INK, MONO, "middle")

    # col 2: precedence
    if focal:
        d.tone(RX[2], y, ROLE_W, ROW_H, ACC, r=4, op="16", sw=1.3)
        d.t(RX[2] + ROLE_W / 2, y + 29, prec, 12, ACC, KR, "middle", 600)
    else:
        d.box(RX[2], y, ROLE_W, ROW_H, PAPER2, RULE, 0.9, 4)
        d.t(RX[2] + ROLE_W / 2, y + 29, prec, 12, INK, KR, "middle")

d.save("12-02.chapter-overview.svg")
