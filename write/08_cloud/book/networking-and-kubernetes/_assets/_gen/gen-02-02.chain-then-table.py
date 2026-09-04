# 02-02.chain-then-table — 체인이 바깥이고 테이블이 그 안이라는 것을 레인으로 보인다
# 본문 요구: "실행은 체인이 먼저입니다 — 패킷이 어떤 체인을 발화시키면,
#            그 체인 안에서 테이블 순서(Raw → Mangle → NAT → Filter)로 규칙이 평가됩니다."
#            + "모든 체인이 모든 테이블을 담지는 않습니다."
#            + 원서 단서 상자가 "위 도식의 INPUT 레인에 있는 NAT 칸"을 지목하므로 INPUT 레인은 유지한다.
# 타입 스펙: type-swimlane.md — 레인 = 체인(행위 주체), 레인 안 단계 = 그 체인이 실제로 가진 테이블.
#           레인을 가로지르는 화살표(라우팅 판단)가 스펙이 말하는 handoff 라 focal 을 건다.
#           "레인마다 단계 수가 같을 필요는 없다"는 관례를 써서 없는 테이블은 ghost 로 남긴다.
#           2026-08-29 대조: type-swimlane 정본은 레인을 "one per actor/team" 으로 둔다. 여기 레인은
#           팀이 아니라 Netfilter 훅이다 — 다만 그 훅이 자기 레인의 테이블을 수행하는 주체이고,
#           레인을 넘는 인계 화살표가 실제로 가장 중요한 간선이라 swimlane 을 유지한다.
#           2026-09-03 병합: 따로 있던 two-layer-order-trace(같은 문법·같은 메시지)를 여기로 접었다.
#           칸을 열로 정렬해 nat 열이 PREROUTING 과 POSTROUTING 에서 두 번 켜지는 것이 보이게 했고,
#           라우팅 판단 뒤 갈리는 두 갈래(INPUT · FORWARD)를 둘 다 레인으로 세웠다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 열 stride 200·레인 h 124 하나로 고정하고 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER2, INFO, KR, MONO

W, H = 1000, 936
BW, BH, STRIDE = 160, 64, 200
CX = [264 + i * STRIDE for i in range(4)]          # 264 464 664 864 — 열이 곧 테이블
LANE_X, LANE_W, LANE_H = 24, 952, 124

d = D(W, H, "IPTABLES · CHAIN FIRST, TABLE INSIDE",
      "체인이 바깥이고 테이블이 그 안이다 — 라우팅 판단에서 갈리는 두 갈래",
      "레인 하나가 체인 하나다. 레인 안의 칸이 그 체인에서 Raw·Mangle·NAT·Filter 순으로 평가되는 테이블이고, "
      "점선 칸은 그 체인에 없는 테이블이다. 칸을 열로 맞춰 두어 nat 열이 위아래로 두 번 켜지는 것이 보인다.",
      lead="레인 = 체인(파란 글자가 커널이 같은 자리를 부르는 훅 이름) · 열 = 테이블 · 진한 칸 = 실제로 일이 일어나는 자리")

# 열 머리 — 그 테이블이 어느 체인에 놓일 수 있는지
for cx, (nm, note) in zip(CX, [("Raw", "PREROUTING·OUTPUT 뿐"), ("Mangle", "다섯 체인 전부"),
                               ("NAT", "여기서 두 번 켜진다"), ("Filter", "INPUT·FORWARD·OUTPUT")]):
    d.t(cx, 120, nm, 13, MUTED, MONO, "middle", 600)
    d.t(cx, 136, ddx.fit(note, 13, STRIDE - 16, note), 13, SOFT, KR)


def lane(y, name, sub, hook, note=None):
    """hook — 같은 자리를 커널이 부르는 이름. 체인 이름과 훅 이름이 1:1 이라는 것을
    본문이 §1 에서 말하므로 레인 머리에 함께 적는다."""
    d.box(LANE_X, y, LANE_W, LANE_H, PAPER2, RULE, 1.0, 8)
    d.t(40, y + 28, name, 12, INK, MONO, "start", 600)
    d.t(40, y + 46, ddx.fit(sub, 12, 136, sub), 12, MUTED, KR, "start")
    d.t(40, y + 66, hook, 11, INFO, MONO, "start")
    if note:
        d.t(40, y + 88, ddx.fit(note, 12, 136, note), 12, SOFT, KR, "start")


def cell(cx, cy, title, sub, kind="has"):
    """kind — ghost(그 체인에 없음) · has(테이블은 있으나 하는 일 없음) · act(일이 일어남)"""
    x, y = cx - BW // 2, cy - BH // 2
    if kind == "ghost":
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="none" '
                   f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="6 6"/>')
        tc, sc = SOFT, SOFT
    elif kind == "act":
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{INFO}14" stroke="{INFO}" stroke-width="1.4"/>')
        tc, sc = INFO, INFO
    else:
        d.box(x, y, BW, BH, PAPER2, INFO, 1.0, 6); tc, sc = INFO, MUTED
    d.t(cx, cy - 2, title, 13, tc, MONO, "middle", 600)
    d.t(cx, cy + 18, ddx.fit(sub, 12, BW - 16, sub), 12, sc, KR)


def order(y):                                       # 레인 안 진행 — 가로 직선
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a + BW // 2 + 8} {y} L {b - BW // 2 - 10} {y}", SOFT, 1.3, m="soft")


# 레인을 먼저 깐다 — 레인 사각형은 불투명 채움이라 나중에 그리면 화살표를 덮는다.
lane(148, "PREROUTING", "라우팅 판단 전", "NF_IP_PRE_ROUTING")
lane(384, "INPUT", "목적지가 이 호스트", "NF_IP_LOCAL_IN", "로컬 프로세스로")
lane(540, "FORWARD", "목적지가 남", "NF_IP_FORWARD", "POSTROUTING 으로")
lane(688, "POSTROUTING", "떠나기 직전", "NF_IP_POST_ROUTING", "노드를 떠난다")

# 레인 1 — PREROUTING
cell(CX[0], 228, "Raw", "추적 이전")
cell(CX[1], 228, "Mangle", "헤더 편집·마킹")
cell(CX[2], 228, "NAT", "DNAT — 목적지 교체", "act")
d.chip(CX[2], 178, "-j KUBE-SERVICES", INFO)
cell(CX[3], 228, "Filter", "이 체인에 없음", "ghost")
order(228)

# handoff — 레인을 가로지르는 자리라 focal 하나를 여기 건다 (type-swimlane 관례)
d.path(f"M {CX[2]} 272 L {CX[2]} 292", ACC, 1.6, m="acc")
d.o.append(f'<rect x="{LANE_X}" y="296" width="{LANE_W}" height="64" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(40, 324, "라우팅 결정", 13, ACC, KR, "start", 600)
d.t(40, 344, "체인을 가르는 유일한 분기", 12, MUTED, KR, "start")
d.t(CX[1], 330, "바뀐 목적지로 길을 찾는다 — DNAT 이 이보다 먼저여야 하는 이유", 13, MUTED, KR)
d.path(f"M {CX[1]} 360 L {CX[1]} 380", ACC, 1.6, m="acc")

# 레인 2 — INPUT (목적지가 이 호스트)
cell(CX[0], 464, "Raw", "이 체인에 없음", "ghost")
cell(CX[1], 464, "Mangle", "헤더 편집")
cell(CX[2], 464, "NAT", "테이블만 존재")
cell(CX[3], 464, "Filter", "수락·거부", "act")
order(464)

d.t(CX[1], 526, "또는 — 목적지가 이 호스트가 아니면 아래 레인으로", 13, SOFT, KR)

# 레인 3 — FORWARD (목적지가 남)
cell(CX[0], 620, "Raw", "이 체인에 없음", "ghost")
cell(CX[1], 620, "Mangle", "헤더 편집")
cell(CX[2], 620, "NAT", "이 체인에 없음", "ghost")
cell(CX[3], 620, "Filter", "수락·거부", "act")
order(620)
d.path(f"M {CX[3]} 664 L {CX[3]} 684", MUTED, 1.5, m="ar")

# 레인 4 — POSTROUTING
cell(CX[0], 768, "Raw", "이 체인에 없음", "ghost")
cell(CX[1], 768, "Mangle", "헤더 편집")
cell(CX[2], 768, "NAT", "SNAT·MASQUERADE", "act")
cell(CX[3], 768, "Filter", "이 체인에 없음", "ghost")
order(768)

d.t(24, 840, "네 레인의 칸이 같은 자리에 놓인 것은 평가 순서가 같기 때문이다. 달라지는 것은 그 체인이 어느 테이블을 갖느냐뿐이다.",
    13, MUTED, KR, "start")
d.t(24, 862, "NAT 열이 맨 위와 맨 아래에서 두 번 켜진다 — 같은 테이블인데 평가되는 시점이 둘이라는 뜻이다.",
    13, MUTED, KR, "start")
d.legend(884, [("그 체인이 가진 테이블", INFO), ("없는 테이블", SOFT),
               ("체인을 갈아타는 자리", ACC)])
d.save("02-02.chain-then-table.svg")
print("ok chain-then-table (merged)")
