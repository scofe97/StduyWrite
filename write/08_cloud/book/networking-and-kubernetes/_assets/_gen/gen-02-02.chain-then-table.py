# 02-02.chain-then-table — 체인이 바깥이고 테이블이 그 안이라는 것을 레인으로 보인다
# 본문 요구: "실행은 체인이 먼저입니다 — 패킷이 어떤 체인을 발화시키면,
#            그 체인 안에서 테이블 순서(Raw → Mangle → NAT → Filter)로 규칙이 평가됩니다."
#            + "모든 체인이 모든 테이블을 담지는 않습니다."
# 타입 스펙: type-swimlane.md — 레인 = 체인(행위 주체), 레인 안 단계 = 그 체인이 실제로 가진 테이블.
#           레인을 가로지르는 화살표(라우팅 판단)가 스펙이 말하는 handoff 라 focal 을 건다.
#           "레인마다 단계 수가 같을 필요는 없다"는 관례를 써서 없는 테이블은 ghost 로 남긴다.
# 좌표: Layout conventions 타입이라 공식이 없다 — stride 192 하나로 고정하고 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, PAPER2, INFO, KR, MONO

W, H = 1000, 712
BW, BH, STRIDE = 160, 64, 200                     # 칸 사이 40px — 연결선이 눈에 잡히는 최소치
CX = [264 + i * STRIDE for i in range(4)]          # 264 464 664 864
MID = 564                                          # CX[1]·CX[2] 의 중점 — handoff 가 서는 자리
LANE_X, LANE_W = 24, 952

d = D(W, H, "IPTABLES · CHAIN FIRST, TABLE INSIDE",
      "체인이 바깥이고 테이블이 그 안이다 — 인바운드 패킷이 이 호스트로 올 때",
      "레인 하나가 체인 하나다. 레인 안의 칸이 그 체인에서 Raw·Mangle·NAT·Filter 순으로 평가되는 테이블이고, "
      "점선 칸은 그 체인에 없는 테이블이다. 레인을 갈아타는 자리가 라우팅 판단이다.",
      lead="레인 = 체인(파란 글자가 커널이 같은 자리를 부르는 훅 이름) · 레인 안 칸 = 그 체인이 실제로 가진 테이블")


def lane(y, h, name, sub, hook=None, mono_name=True):
    """hook — 같은 자리를 커널이 부르는 이름. 체인 이름과 훅 이름이 1:1 이라는 것을
    본문이 §1 에서 말하므로 레인 머리에 함께 적는다."""
    d.box(LANE_X, y, LANE_W, h, PAPER2, RULE, 1.0, 8)
    d.t(40, y + 28, name, 12, INK, MONO if mono_name else KR, "start", 600)
    d.t(40, y + 46, sub, 12, MUTED, KR, "start")
    if hook:
        d.t(40, y + 66, hook, 11, INFO, MONO, "start")


def cell(cx, cy, title, sub, ghost=False):
    x, y = cx - BW // 2, cy - BH // 2
    if ghost:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="none" '
                   f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="6 6"/>')
        d.t(cx, cy - 2, title, 13, SOFT, MONO, "middle", 600)
        d.t(cx, cy + 18, sub, 12, SOFT, KR)
    else:
        d.box(x, y, BW, BH, PAPER2, INFO, 1.1, 6)
        d.t(cx, cy - 2, title, 13, INFO, MONO, "middle", 600)
        d.t(cx, cy + 18, ddx.fit(sub, 12, BW - 16, sub), 12, MUTED, KR)


def step(a, b, y):                                  # 레인 안 진행 — 가로 직선
    d.path(f"M {a + BW // 2 + 8} {y} L {b - BW // 2 - 10} {y}", MUTED, 1.5, m="ar")


# 레인 셋을 먼저 깐다 — 레인 사각형은 불투명 채움이라 나중에 그리면 화살표를 덮는다.
# (2026-08-28 렌더 확인에서 진입 화살표와 INPUT 으로 내려가는 handoff 가 실제로 가려졌다.)
lane(148, 124, "PREROUTING", "체인 · 라우팅 판단 전", "NF_IP_PRE_ROUTING")
lane(296, 76, "라우팅 판단", "체인을 가르는 유일한 분기", mono_name=False)
lane(396, 124, "INPUT", "체인 · 라우팅 판단 후", "NF_IP_LOCAL_IN")

# 인바운드 패킷 — 레인 1 첫 칸으로 내려온다
d.box(CX[0] - BW // 2, 96, BW, 32, PAPER, RULE, 1.0, 6)
d.t(CX[0], 116, "인바운드 패킷", 12, MUTED, KR)
d.path(f"M {CX[0]} 128 L {CX[0]} 192", MUTED, 1.5, m="ar")

# 레인 1 — PREROUTING
cell(CX[0], 228, "Raw", "추적 이전")
cell(CX[1], 228, "Mangle", "헤더 편집·마킹")
cell(CX[2], 228, "NAT", "DNAT")
d.chip(CX[2], 182, "-j KUBE-SERVICES", INFO)
cell(CX[3], 228, "Filter", "이 체인에 없음", ghost=True)
step(CX[0], CX[1], 228)
step(CX[1], CX[2], 228)

# handoff — 레인을 가로지르는 자리라 focal 하나를 여기 건다 (type-swimlane 관례)
d.path(f"M {CX[2]} 260 L {CX[2]} 280 L {MID} 280 L {MID} 306", ACC, 1.6, m="acc")
d.o.append(f'<rect x="{MID - 132}" y="310" width="264" height="48" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(MID, 330, "목적지 = 이 호스트인가", 12, ACC, KR)
d.t(MID, 348, "예 → INPUT · 아니오 → FORWARD", 12, MUTED, KR)
d.path(f"M {MID} 358 L {MID} 380 L {CX[1]} 380 L {CX[1]} 440", ACC, 1.6, m="acc")

# 레인 2 — INPUT
cell(CX[0], 476, "Raw", "이 체인에 없음", ghost=True)
cell(CX[1], 476, "Mangle", "헤더 편집")
cell(CX[2], 476, "NAT", "테이블만 존재")
cell(CX[3], 476, "Filter", "수락·거부")
step(CX[1], CX[2], 476)
step(CX[2], CX[3], 476)

# 로컬 프로세스로 나간다
d.path(f"M {CX[3]} 508 L {CX[3]} 540", MUTED, 1.5, m="ar")
d.box(CX[3] - BW // 2, 544, BW, 32, PAPER, RULE, 1.0, 6)
d.t(CX[3], 564, "로컬 프로세스", 12, MUTED, KR)

d.t(24, 600, "두 레인의 칸이 같은 자리에 놓인 것은 평가 순서가 같기 때문이다. "
             "달라지는 것은 그 체인이 어느 테이블을 갖느냐뿐이다.", 12, MUTED, KR, "start")
d.t(24, 622, "레인 머리의 두 이름은 같은 자리를 가리킨다 — 위가 iptables 가 부르는 체인 이름, "
             "아래가 커널이 부르는 Netfilter 훅 이름이다.", 12, MUTED, KR, "start")
d.legend(644, [("그 체인이 가진 테이블", INFO), ("없는 테이블", SOFT), ("체인을 갈아타는 자리", ACC)])
d.save("02-02.chain-then-table.svg")
print("ok chain-then-table")
