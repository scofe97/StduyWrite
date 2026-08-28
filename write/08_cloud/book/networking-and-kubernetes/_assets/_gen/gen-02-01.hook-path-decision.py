# 02-01.hook-path-decision — 훅 조합을 정하는 두 질문
# 본문 요구: "어떤 패킷이 어느 훅을 지나는지는 두 가지 질문으로 정해집니다 —
#            출발지가 이 호스트인가, 목적지가 이 호스트인가."
#            표 4행(출발지×목적지 → 훅 순서)이 그림으로 없었다. 기존 netfilter-hooks-flow 는
#            네 조합 중 '외부→외부' 하나만 담아 LOCAL_IN·LOCAL_OUT 이 한 번도 안 나온다.
# 타입 스펙: type-flowchart.md — 두 질문이 곧 판단 분기다. 모양이 종류를 나른다
#           (마름모=판단, 사각=훅, 타원=시작·끝). 색은 종류가 아니라 '주소 한쪽이 고정된다'는
#           성질에만 쓴다. §4 기존 도식이 이미 dp-security-matrix 라 같은 절에 같은 문법을 두 번 두지 않는다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 920
d = D(W, H, "NETFILTER HOOKS · WHICH COMBINATION",
      "훅 조합을 정하는 두 질문 — 출발지가 나인가, 목적지가 나인가",
      "패킷이 지나는 Netfilter 훅 조합은 출발지와 목적지가 이 호스트인지 두 질문으로 정해진다. "
      "네 조합과 훅 다섯 개가 모두 나오며, 로컬에서 로컬로 가는 경우만 훅을 넷 지난다.",
      lead="두 질문이 네 갈래를 만들고, 갈래마다 지나는 훅이 다르다")

BW, BH, STRIDE = 136, 56, 72
COL = [140, 380, 620, 860]
OVAL_CY, Q1_CY, Q2_CY, ROW0 = 160, 244, 340, 440
DW, DH = 232, 76                                   # 마름모
Q2X = [260, 740]

def oval(cx, cy, txt, w=168):
    d.box(cx - w // 2, cy - 22, w, 44, PAPER2, RULE, 1.1, 20)
    d.t(cx, cy + 5, ddx.fit(txt, 12, w - 24, txt), 12, MUTED, KR, "middle", 600)

def diamond(cx, cy, txt):
    hw, hh = DW // 2, DH // 2
    d.path(f"M {cx} {cy-hh} L {cx+hw} {cy} L {cx} {cy+hh} L {cx-hw} {cy} Z", RULE, 1.2)
    d.t(cx, cy + 5, ddx.fit(txt, 12, DW - 32, txt), 12, INK, KR, "middle", 600)

def hook(cx, cy, name, sub=None, c=None, dim=False):
    col = c or RULE
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER if dim else PAPER2, col, 1.1, 6)
    tc = SOFT if dim else (c or INK)
    d.t(cx, cy - 6, ddx.fit(name, 12, BW - 16, name), 12, tc, MONO, "middle", 600)
    if sub: d.t(cx, cy + 15, ddx.fit(sub, 11, BW - 14, sub), 11, c or MUTED, KR)

def down(cx, y0, y1, c=MUTED):
    d.path(f"M {cx} {y0} L {cx} {y1-8}", c, 1.5, m="acc" if c is ACC else "ar")

# ── 시작과 두 질문 ─────────────────────────────────────────────
oval(500, OVAL_CY, "패킷 하나")
down(500, OVAL_CY + 22, Q1_CY - DH // 2)
diamond(500, Q1_CY, "이 호스트가 만든 패킷인가?")
for sx, qx, lab in ((500 - DW // 2, Q2X[0], "아니오 — 밖에서 왔다"),
                    (500 + DW // 2, Q2X[1], "예 — 내가 만들었다")):
    d.path(f"M {sx} {Q1_CY} L {qx} {Q1_CY} L {qx} {Q2_CY-DH//2-8}", MUTED, 1.5, m="ar")
    d.t(qx, Q1_CY - 12, lab, 11, SOFT, KR)
for qx in Q2X:
    diamond(qx, Q2_CY, "목적지가 이 호스트인가?")

# ── 각 질문에서 두 열로 ────────────────────────────────────────
TRUNK = 392
for qi, qx in enumerate(Q2X):
    for side, lab in ((0, "예"), (1, "아니오")):
        cx = COL[qi * 2 + side]
        d.path(f"M {qx} {Q2_CY+DH//2} L {qx} {TRUNK} L {cx} {TRUNK} L {cx} {ROW0-BH//2-8}",
               MUTED, 1.5, m="ar")
        d.t((qx + cx) // 2, TRUNK - 6, lab, 11, SOFT, KR)

# ── 네 갈래의 훅 사슬 ──────────────────────────────────────────
def chain(cx, steps):
    """steps: (종류, 이름, 부제, 색) — 종류는 hook | oval | gap"""
    y = ROW0
    prev = None
    for kind, name, sub, c in steps:
        if kind == "gap":
            y += STRIDE; continue
        if prev is not None:
            down(cx, prev, y - BH // 2 if kind == "hook" else y - 22,
                 ACC if name == "__acc__" else MUTED)
        if kind == "hook":
            hook(cx, y, name, sub, c, dim=(c is None and sub == "다시 지난다"))
            prev = y + BH // 2
        else:
            oval(cx, y, name); prev = y + 22
        y += STRIDE

chain(COL[0], [("hook", "PRE_ROUTING", None, None),
               ("hook", "LOCAL_IN", "dst = 내 IP", INFO),
               ("oval", "로컬 소켓으로", None, None)])
chain(COL[1], [("hook", "PRE_ROUTING", None, None),
               ("hook", "FORWARD", "둘 다 내가 아님", None),
               ("hook", "POST_ROUTING", None, None),
               ("oval", "밖으로", None, None)])
chain(COL[3], [("hook", "LOCAL_OUT", "src = 내 IP", INFO),
               ("hook", "POST_ROUTING", None, None),
               ("oval", "밖으로", None, None)])

# 로컬 → 로컬만 훅을 넷 지난다 — 나갔다 재진입하기 때문. focal 은 이 한 곳.
cx = COL[2]
hook(cx, ROW0, "LOCAL_OUT", "src = 내 IP", INFO)
down(cx, ROW0 + BH // 2, ROW0 + STRIDE - BH // 2)
hook(cx, ROW0 + STRIDE, "POST_ROUTING", None, None)
# 위 상자 아래끝(ROW0+STRIDE+BH//2)과 아래 상자 위끝(ROW0+2*STRIDE+BH//2) 사이 통로의 한가운데.
# 눈대중으로 두면 위 상자에 3px 까지 붙는다 — 통로를 반으로 나눠 위아래 여유를 같게 준다.
REENTER_CY = ROW0 + STRIDE + BH // 2 + STRIDE // 2
d.path(f"M {cx} {ROW0+STRIDE+BH//2} L {cx} {REENTER_CY-13}", ACC, 1.6)
ddx.tag(d, cx, REENTER_CY, "lo 로 나갔다 다시 들어온다", ACC, 196)
d.path(f"M {cx} {REENTER_CY+13} L {cx} {ROW0+2*STRIDE+BH//2-8}", ACC, 1.6, m="acc")
hook(cx, ROW0 + 2 * STRIDE + BH, "PRE_ROUTING", "다시 지난다", None, dim=True)
down(cx, ROW0 + 2 * STRIDE + BH + BH // 2, ROW0 + 3 * STRIDE + BH - BH // 2)
hook(cx, ROW0 + 3 * STRIDE + BH, "LOCAL_IN", "dst = 내 IP", INFO)
down(cx, ROW0 + 3 * STRIDE + BH + BH // 2, ROW0 + 4 * STRIDE + BH - 22)
oval(cx, ROW0 + 4 * STRIDE + BH, "로컬 소켓으로")

d.t(36, 856, "LOCAL_ 이 붙은 두 훅만 주소 한쪽이 고정된다 — LOCAL_IN 은 목적지가, LOCAL_OUT 은 출발지가 이 호스트다. "
             "두 번째 질문에 답하는 것은 라우팅 판단이다.", 12, MUTED, KR, "start")
d.legend(870, [("주소 한쪽이 이 호스트로 고정", INFO), ("나갔다 다시 들어온다", ACC)])
d.save("02-01.hook-path-decision.svg")
print("ok hook-path-decision")
