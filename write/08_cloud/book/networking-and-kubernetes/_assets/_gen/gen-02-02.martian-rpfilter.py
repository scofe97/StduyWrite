# 02-02.martian-rpfilter — 규칙 목록 밖에서 버려지는 자리
# 본문 요구: "둘 다 Netfilter 훅이 아니라 라우팅 코드에서 발화합니다. iptables -L 로는 보이지
#            않는다는 뜻이라, 규칙을 아무리 뒤져도 원인이 안 나오는 종류의 차단입니다."
#            2026-09-17 복습 1회차에서 이 내용이 1점이었고 오답 노트가 짚은 원인이
#            "패킷을 버리는 일을 전부 Netfilter 훅 안쪽으로 봄" 이다. 그래서 이 그림의 사건은
#            '무엇을 보느냐'(그건 본문 표가 맡는다)가 아니라 '어느 쪽 소유냐' 하나다.
# 타입 스펙: type-swimlane.md — 레인 = 코드 소유자(Netfilter 훅 / 라우팅 코드).
#           단계 상자는 자기 소유자의 레인 안에만 놓고, 레인을 가로지르는 화살표가
#           가장 중요한 엣지라는 정본의 규약을 그대로 쓴다. 그 두 번의 가로지름이
#           곧 iptables 가 보는 영역과 못 보는 영역의 경계다.
#           loopback-not-a-boundary(점선 링을 화살표가 뚫는 구도)와 겹치지 않게
#           경계를 링이 아니라 레인 분할로 세웠다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, PAPER2, KR, MONO

W, H = 1000, 628
d = D(W, H, "ROUTING-LAYER DROPS · OUTSIDE THE IPTABLES VIEW",
      "iptables -L 에 안 보이는 두 검사 — Martian 과 rp_filter",
      "들어온 패킷은 PRE_ROUTING 훅을 지난 뒤 라우팅 코드로 넘어간다. 출발지 주소를 보는 두 검사가 "
      "그 안에서 발화하므로, 여기서 버려진 패킷은 iptables 규칙 목록을 아무리 뒤져도 자국이 없다. "
      "두 검사는 스위치도 따로다 — Martian 은 기본 동작이고 rp_filter 는 sysctl 로 켜고 끈다.",
      lead="버린 주체가 방화벽이 아니라 라우팅 코드다 — 규칙 목록에는 자국이 남지 않는다")

# ── 레이아웃 공식 ─────────────────────────────────────────────
# 레인 둘은 전폭(24..976), 안쪽 여백 20px. 통로는 이 편의 기준인 48px 로 고정한다.
BX, BW = 24, 952
NW, NH_A, NH_B = 192, 76, 84
GAP = 48
X0 = BX + 20                                   # 44
CX = [X0 + NW // 2 + i * (NW + GAP) for i in range(4)]   # 140 380 620 860

LANE_A = (104, 232)          # Netfilter 훅
LANE_B = (280, 428)          # 라우팅 코드 — focal. 레인 통로도 가로 통로와 같은 48px
CY_A, CY_B = 180, 360
CROSS_Y = 256                # 레인 사이 통로(232..280) 한가운데 — 가로지름 라벨 자리
DROP_Y, SINK_Y = 456, 508

ddx.band(d, *LANE_A, "Netfilter 훅 · iptables -L 에 보이는 자리", x=BX, w=BW)
ddx.band(d, *LANE_B, "라우팅 코드 · iptables -L 에 안 보이는 자리", x=BX, w=BW, focal=True)


def _fam(txt):
    """한글이 섞이면 KR 스택으로 — Seq 계열과 같은 함정이라 여기서 갈라 쓴다.
    mono 로 찍으면 자간이 벌어져 스타일 계약의 '서술은 한글 스택' 을 어긴다."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def node(cx, cy, h, title, sub, tag=None, c=RULE, tc=INK):
    """레인 안의 단계 상자. 두 줄(훅)과 세 줄(검사)을 같은 함수로 찍는다."""
    x, y = cx - NW // 2, cy - h // 2
    d.box(x, y, NW, h, PAPER2, c, 1.1, 6)
    ty = cy - 18 if tag else cy - 8
    d.t(cx, ty, ddx.fit(title, 13, NW - 16, title), 13, tc, _fam(title), "middle", 600)
    d.t(cx, ty + 22, ddx.fit(sub, 11, NW - 14, sub), 11, MUTED, KR)
    if tag:
        d.t(cx, ty + 46, ddx.fit(tag, 11, NW - 14, tag), 11, SOFT, _fam(tag))


node(CX[0], CY_A, NH_A, "PRE_ROUTING", "들어온 직후")
node(CX[1], CY_B, NH_B, "Martian 검사", "출발지 주소 자체", "기본 동작")
node(CX[2], CY_B, NH_B, "rp_filter", "되돌아갈 경로", "sysctl 로 켬", c=INFO, tc=INFO)
node(CX[3], CY_A, NH_A, "LOCAL_IN · FORWARD", "목적지에 따라 갈림")

# ── 레인을 가로지르는 두 걸음 — 이 그림의 사건 ──────────────────
# 통로 한가운데에 세로 구간을 세워 직각으로만 꺾는다(dd-lint 는 대각선을 막는다).
MID1 = (CX[0] + NW // 2 + CX[1] - NW // 2) // 2      # 260
MID2 = (CX[2] + NW // 2 + CX[3] - NW // 2) // 2      # 740
d.path(f"M {CX[0] + NW // 2 + 6} {CY_A} L {MID1} {CY_A} L {MID1} {CY_B} "
       f"L {CX[1] - NW // 2 - 10} {CY_B}", ACC, 1.8, m="acc")
d.path(f"M {CX[2] + NW // 2 + 6} {CY_B} L {MID2} {CY_B} L {MID2} {CY_A} "
       f"L {CX[3] - NW // 2 - 10} {CY_A}", ACC, 1.8, m="acc")
d.t(MID1 + 8, CROSS_Y, "훅 밖으로", 11, ACC, KR, "start")
d.t(MID2 + 8, CROSS_Y, "훅 안으로", 11, ACC, KR, "start")

# 레인 안의 한 걸음 — 두 검사는 같은 소유자 아래 나란히 앉는다
d.path(f"M {CX[1] + NW // 2 + 6} {CY_B} L {CX[2] - NW // 2 - 10} {CY_B}", MUTED, 1.5, m="ar")

# ── 폐기 — 레인 밖으로 떨어진다 ────────────────────────────────
for cx in (CX[1], CX[2]):
    d.path(f"M {cx} {CY_B + NH_B // 2} L {cx} {DROP_Y}", BAD, 1.6)
d.path(f"M {CX[1]} {DROP_Y} L {CX[2]} {DROP_Y}", BAD, 1.6)
SINK_X = (CX[1] + CX[2]) // 2
d.path(f"M {SINK_X} {DROP_Y} L {SINK_X} {SINK_Y - 26}", BAD, 1.6, m="bad")
ddx.tag(d, SINK_X, SINK_Y, "조용히 폐기", BAD, 140)
d.t(SINK_X, SINK_Y + 32, "iptables -L 에 남는 자국 없음", 11, SOFT, KR)

d.legend(572, [("iptables -L 에 안 보이는 자리", ACC),
               ("스위치로 켜고 끄는 검사", INFO),
               ("조용히 폐기", BAD)])
d.save("02-02.martian-rpfilter.svg")
print("ok martian-rpfilter")
