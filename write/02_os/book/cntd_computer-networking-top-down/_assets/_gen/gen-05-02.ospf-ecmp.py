# 타입 스펙: type-architecture — 전/후 두 칸. 칸마다 같은 망 조각(u · v · w · z)을 다시 그리고 패킷 넷을 옮긴다.
#       gen-05-02.anycast-break.py 와 같은 전/후 망 그림 문법이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 "Multiple same-cost paths" (인쇄 347쪽)
#       "When multiple paths to a destination have the same cost, OSPF allows multiple paths to be used
#        (that is, a single path need not be chosen for carrying all traffic when multiple equal-cost paths exist)"
# 노트의 예시: 링크 비용 1·2 와 노드 이름 u·v·w·z 는 두 경로의 합이 같아지도록 고른 예시다.
#       패킷 개수는 "여러 경로에 실린다"는 표시일 뿐 비율이 아니다. 원문은 트래픽을 나누는 방식을 적지 않으므로 그리지 않는다.
# focal: 둘째 칸 — 본문이 짚는 "여럿을 함께 쓴다".
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, KR, MONO

W, H = 1000, 624
d = D(W, H, "SECTION 5.3 · MULTIPLE SAME-COST PATHS",
      "비용이 같은 두 경로에 트래픽을 함께 싣습니다",
      "출발 라우터 u 에서 목적지 z 로 가는 경로가 v 쪽과 w 쪽 둘이고 경로 비용은 둘 다 3 이다. "
      "경로 하나만 고르면 패킷 넷이 모두 v 쪽으로 가고 w 쪽은 빈다. OSPF 는 비용이 같은 경로를 함께 쓸 수 있어 "
      "같은 패킷 넷이 두 경로에 나뉘어 실린다. 링크 비용은 예시이고 패킷 개수는 비율이 아니다.",
      "위는 경로 하나만 고를 때, 아래는 OSPF 가 같은 비용 경로를 함께 쓸 때입니다. 링크 비용 숫자는 예시입니다.")

NW, NH = 104, 40
UX, VX, ZX = 72, 448, 824                 # u · v(=w) · z 상자 왼변
J1, J2 = 312, 688                         # 갈라지는 자리 · 합쳐지는 자리 x
PW, PHK = 20, 12                          # 패킷 한 개


def node(x, cy, label, stroke=MUTED):
    d.box(x, cy - NH / 2, NW, NH, PAPER2, stroke, 1.1, 6)
    d.t(x + NW / 2, cy + 5, label, 13, INK, KR, "middle", 600)


def packet(cx, cy, c):
    d.tone(cx - PW / 2, cy - PHK / 2, PW, PHK, c, 2, "55", 1.2)


def panel(y0, title, top, bot, top_packets, bot_packets, focal=False):
    if focal:
        d.tone(24, y0, 952, 216, ACC, 10, "0A", 1.4)
    else:
        d.box(24, y0, 952, 216, f"{INK}05", RULE, 1.0, 10)
    d.t(40, y0 + 24, title, 13, INK, KR, "start", 600)
    cu = cz = y0 + 116
    cv, cw = y0 + 68, y0 + 164
    # 빈 경로(점선)를 먼저 그려 겹치는 구간에서 실린 경로가 위에 오게 한다
    routes = sorted(((cv, top, top_packets), (cw, bot, bot_packets)), key=lambda r: r[1][2] is None)
    for cy, (c, sw, dash), n in routes:
        d.path(f"M {UX + NW} {cu} L {J1} {cu} L {J1} {cy} L {VX} {cy}", c, sw, dash=dash)
        d.path(f"M {VX + NW} {cy} L {J2} {cy} L {J2} {cz} L {ZX - 4} {cz}", c, sw, dash=dash,
               m=None if dash else ("warn" if c == WARN else "ok"))
        # 링크마다 패킷을 n 개씩
        for seg0 in (J1, VX + NW):
            for k in range(n):
                packet(seg0 + 44 + k * 32, cy, c)
    # 링크 비용 — 예시
    d.t(380, cv - 16, "비용 1", 13, MUTED, KR)
    d.t(620, cv - 16, "비용 2", 13, MUTED, KR)
    d.t(380, cw + 28, "비용 2", 13, MUTED, KR)
    d.t(620, cw + 28, "비용 1", 13, MUTED, KR)
    node(UX, cu, "출발 u")
    node(VX, cv, "v")
    node(VX, cw, "w")
    node(ZX, cz, "목적지 z")
    return cu, cv, cw


# ── 1. 경로 하나만 고를 때 ──
panel(96, "1. 경로 하나만 고를 때", (WARN, 2.4, None), (MUTED, 1.2, "4 4"), 2, 0)
d.t(960, 120, "u·v·z 비용 3 · 패킷 넷 전부", 13, WARN, KR, "end", 600)
d.t(960, 292, "u·w·z 비용 3 · 빈 경로", 13, MUTED, KR, "end")

# ── 2. OSPF · 같은 비용 경로를 함께 ──
panel(336, "2. OSPF · 같은 비용 경로를 함께", (OK, 2.0, None), (OK, 2.0, None), 1, 1, focal=True)
d.t(960, 360, "u·v·z 비용 3 · 패킷 둘", 13, OK, KR, "end", 600)
d.t(960, 532, "u·w·z 비용 3 · 패킷 둘", 13, OK, KR, "end", 600)

d.legend(576, [("경로 하나에 몰린 트래픽", WARN), ("함께 쓰는 같은 비용 경로", OK), ("본문이 짚는 칸", ACC)])
d.t(960, 616, "KUROSE-ROSS 9E 5.3 P.347 · COSTS ILLUSTRATIVE", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.ospf-ecmp.svg"
d.save(out)
print("→", out)
