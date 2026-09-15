# 타입 스펙: type-sequence — 링크 하나가 끊어졌을 때 컨트롤러 안팎에서 벌어지는 여섯 단계.
#   위 칸은 그 사건이 벌어지는 스위치 넷의 위상 한 컷이다. 연결선은 architecture 관례(직각만)를 따르되,
#   한 장 한 선언이라 논지인 여섯 걸음 쪽으로 둔다. 축약: 위상 칸에는 방향을 우회로 하나에만 준다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.5.3 Figure 5.16 의 1~6 단계
# 2026-09-15: 위상 칸을 더했다. 노드로 그린 스위치가 s1 하나뿐이라 "끊긴 링크에 닿지 않은 s4 의 표가
#             왜 바뀌나"를 그림에서 못 읽었다(복습에서 우회로 자리를 못 짚고 s4 는 안 바뀐다고 오판).
# 간선은 노트 §4 정오 인용이 적은 다섯만 그린다 — s1-s2 · s1-s3 · s1-s4 · s2-s4 · s3-s4.
# 가로 순서 s3 · s1 · s4 · s2: 우회로 s1-s4-s2 가 인접 수평 화살표 둘로 이어지고,
#   먼 쌍 둘은 ㄷ자로 돈다(s1-s2 는 위, s3-s4 는 아래) — 교차가 없다.
# 색: BAD 끊긴 링크·장애 보고 · INFO 컨트롤러 내부 · OK 우회로·새 흐름 표 · ACC(focal) s4 의 표 한 곳.
#   종전에는 5·6 걸음과 바닥 캡션에 ACC 를 걸어 focal 이 여럿이었다. 5 는 컨트롤러 안이라 INFO 로 옮겼다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq 가 한글 라벨·서브라벨을 mono 로 찍는 자리를 한글 스택으로 가른다(계약 §프리미티브가 한글을 mono 로)."""
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start")
        if sub: s.t(x + 68, y + 14, sub, 12, MUTED, _kr(sub), "start")


W, H = 1000, 944
d = SeqKR(W, H, "SECTION 5.5.3 · LINK-STATE CHANGE",
          "링크 하나가 끊어지면 여섯 걸음",
          "위 칸은 스위치 s1·s2·s3·s4 와 링크 다섯(s1-s2, s1-s3, s1-s4, s2-s4, s3-s4). s1-s2 가 끊기면 우회로는 s1-s4-s2 이고, "
          "흐름 표가 바뀌는 곳은 s1·s2·s4 셋이며 s3 는 그대로다. s4 는 끊긴 링크에 닿지 않았는데도 표가 바뀐다. "
          "아래 칸은 그 변화를 만드는 SDN 제어 평면의 여섯 걸음. 다익스트라는 스위치 밖의 앱에서 돌고, 스위치는 서로가 아니라 컨트롤러에게만 알린다.",
          "앞 편에서는 라우터끼리 알렸습니다 — 여기서는 컨트롤러에게만 알립니다")

# ── 위 칸: 스위치 넷 · 링크 다섯 ─────────────────────────────────────
d.t(24, 112, "스위치 넷 · 링크 다섯", 13, INK, KR, "start", 600)

NW, NH = 136, 48                 # 노드 상자
TOP = 184; BOT = TOP + NH        # 184 · 232
MID = TOP + NH // 2              # 208 — 우회로 화살표 높이
ARCH_UP, ARCH_DN = TOP - 36, BOT + 24   # 148 · 256 — 먼 쌍의 ㄷ자 높이
STRIDE, CW, CH, CY = 232, 216, 76, 276  # 열 간격 · 흐름 표 칸 폭·높이·윗변
X0 = 140                         # 네 칸(4×216 + 3×16 = 912)을 레인 폭 24~952 가운데에 둔다
ORDER = ["s3", "s1", "s4", "s2"]
CX = {n: X0 + STRIDE * i for i, n in enumerate(ORDER)}   # 140 · 372 · 604 · 836

# 링크 — 선을 먼저, 상자를 나중에
d.line(CX["s3"] + NW // 2, MID, CX["s1"] - NW // 2, MID, MUTED, 1.2)                        # s1-s3
d.path(f"M {CX['s3']} {BOT} L {CX['s3']} {ARCH_DN} L {CX['s4']} {ARCH_DN} L {CX['s4']} {BOT}",
       MUTED, 1.2)                                                                           # s3-s4
d.path(f"M {CX['s1']} {TOP} L {CX['s1']} {ARCH_UP} L {CX['s2']} {ARCH_UP} L {CX['s2']} {TOP}",
       BAD, 1.4, dash="5 4")                                                                 # s1-s2 끊김
XB = (CX["s4"] + CX["s2"]) // 2  # 720
d.line(XB - 8, ARCH_UP - 8, XB + 8, ARCH_UP + 8, BAD, 1.8)
d.line(XB - 8, ARCH_UP + 8, XB + 8, ARCH_UP - 8, BAD, 1.8)
d.chip(XB, ARCH_UP - 24, "s1-s2 끊김", BAD, 12, 7)

# 우회로 s1 → s4 → s2 (s1 이 s2 로 보내는 패킷)
d.arrow([(CX["s1"] + NW // 2 + 4, MID), (CX["s4"] - NW // 2 - 4, MID)], OK, "ok", 2.0)
d.arrow([(CX["s4"] + NW // 2 + 4, MID), (CX["s2"] - NW // 2 - 4, MID)], OK, "ok", 2.0)
d.t((CX["s1"] + CX["s4"]) // 2, MID - 12, "우회로", 12, OK, KR)

SUB = {"s3": "우회로가 안 지남", "s1": "끊긴 링크 한쪽 끝",
       "s4": "끊긴 링크에 안 닿음", "s2": "끊긴 링크 다른 쪽 끝"}
for n in ORDER:
    d.box(CX[n] - NW // 2, TOP, NW, NH, PAPER2, MUTED, 1.0, 6)
    d.t(CX[n], TOP + 20, n, 14, INK, MONO, "middle", 600)
    d.t(CX[n], TOP + 38, SUB[n], 12, MUTED, KR)

# 흐름 표 칸 — 노드와 같은 열. 문구는 §4 의 s1 · s2 · s4 목록을 따른다
CELL = {
    "s3": (None, ["그대로"]),
    "s1": (OK, ["s2 행 패킷을", "s4 를 거쳐 보냄"]),
    "s4": (ACC, ["s1 이 s2 로 보내는", "패킷을 나름"]),
    "s2": (OK, ["s1 이 보낸 패킷을", "s4 에게서 받음"]),
}
for n in ORDER:
    c, lines = CELL[n]
    x0 = CX[n] - CW // 2
    if c is None:
        d.box(x0, CY, CW, CH, PAPER2, RULE, 1.0, 6)
    elif c == ACC:
        d.tone(x0, CY, CW, CH, ACC, 6, "12", 1.4)     # focal — 장애를 겪지 않고 표가 바뀐 곳
    else:
        d.tone(x0, CY, CW, CH, c, 6, "14", 1.2)
    d.t(CX[n], CY + 22, f"{n} 의 흐름 표", 12, MUTED, KR)
    for i, ln in enumerate(lines):
        d.t(CX[n], CY + 44 + 20 * i, ln, 13, INK if c else MUTED, KR)

# ── 아래 칸: 여섯 걸음 ─────────────────────────────────────────────
d.line(24, 376, 952, 376, RULE, 1.0)
d.t(24, 408, "컨트롤러 안팎의 여섯 걸음", 13, INK, KR, "start", 600)

LX = d.lanes([("s1", "패킷 스위치"), ("링크 상태 관리자", "컨트롤러 안"),
              ("라우팅 앱", "다익스트라"), ("흐름 표 관리자", "컨트롤러 안")], y0=424, lane_w=196)
d.rails(800)

S0, ST = 500, 56   # 첫 걸음 y · 걸음 간격
d.msg("s1", "링크 상태 관리자", "port-status", S0, BAD, "bad", sub="1 · s2 링크 끊김")
d.selfmsg("링크 상태 관리자", "DB 갱신", S0 + ST, INFO, sub="2 · 링크 상태 DB 를 고침")
d.msg("링크 상태 관리자", "라우팅 앱", "알림", S0 + 2 * ST, INFO, "info", sub="3 · 미리 등록해 둔 앱에게")
d.msg("라우팅 앱", "링크 상태 관리자", "상태 조회", S0 + 3 * ST, MUTED, "ar", sub="4 · 새 최소 비용 경로 계산")
d.msg("라우팅 앱", "흐름 표 관리자", "새 경로", S0 + 4 * ST, INFO, "info", sub="5 · 고칠 표 결정")
d.msg("흐름 표 관리자", "s1", "modify-state", S0 + 5 * ST, OK, "ok", sub="6 · s1 · s2 · s4 의 표를 고침")

d.t(24, 836, "조율 · 프로토콜의 수렴이 아니라 한 곳의 계산", 13, INK, KR, "start", 600)

d.legend(860, [("끊긴 링크 · 장애 보고", BAD), ("컨트롤러 내부", INFO),
               ("우회로 · 새 흐름 표", OK), ("장애 없이 바뀐 표", ACC)])
d.t(960, 914, "KUROSE-ROSS 9E FIG 5.16", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.link-failure.svg"
d.save(out)
print("→", out)
