# 타입 스펙: type-architecture — 세 칸. 칸마다 같은 망(출발지 S · R1~R5 · 멤버 M)을 다시 그리고,
#       라우터 상자 안의 지도 사본과 오른쪽 "같은 지도" 카드가 칸마다 어떻게 달라지는지를 옮긴다.
#       gen-05-02.ospf-ecmp.py · gen-05-02.anycast-break.py 와 같은 전/후 망 그림 문법이다.
# 2026-09-14: type-data-flow(R2·R3 → R1 안 LSDB → 경로 상자)에서 바꿨다. "무엇을 표현하는지 모르겠다"는 지적을 받았다.
#       무슨 일이 어떤 순서로 일어나고 지도에서 무엇이 달라지는지를 시간 순 세 칸으로 둔다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 "Integrated support for unicast and multicast routing" (인쇄 348쪽)
#       "MOSPF uses the existing OSPF link database and adds a new type of link-state advertisement
#        to the existing OSPF link-state broadcast mechanism"
# 원문 밖(RFC 1584 "Multicast Extensions to OSPF", 1994-03, https://www.rfc-editor.org/rfc/rfc1584.txt):
#   2칸 — 광고 이름 group-membership-LSA · "LS type = 6" (부록 A.3).
#         §1 "By adding a new type of link state advertisement, the group-membership-LSA, the location of all
#         multicast group members is pinpointed in the database."
#         §2.3.1 "Like other link state advertisements, the group-membership-LSA is flooded throughout the Autonomous System."
#         같은 절 "The router lists itself in its group-membership-LSA for Group A if ... the router's attached stub
#         networks contain Group A members" → 카드 줄은 호스트 M 이 아니라 라우터 R4 를 적는다.
#         같은 절 "the MOSPF link state database, and the datagram shortest-path trees ... are identical in each router"
#   3칸 — §1 "The path of a multicast datagram can then be calculated by building a shortest-path tree rooted at the
#         datagram's source. All branches not containing multicast members are pruned from the tree. These pruned
#         shortest-path trees are initially built when the first datagram is received (i.e., on demand). The results
#         of the shortest path calculation are then cached for use by subsequent datagrams having the same source
#         and destination."  §2.3.2 "the datagram's source IP network is located in the link state database"
# 노트의 예시: 망 모양(라우터 다섯 · R5 곁가지)과 그룹 이름 G 는 가지 제외가 보이도록 고른 예시다.
#       IGMP 로 멤버를 알아내는 과정은 그리지 않는다.
# focal: 2칸 카드의 새 줄 "그룹 G 멤버 · R4" — MOSPF 가 지도에 더한 단 하나.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 904
d = D(W, H, "SECTION 5.3 · MOSPF",
      "멀티캐스트도 한 줄 더한 같은 지도에서 경로를 뽑습니다",
      "같은 망을 시간 순서로 세 번 그렸다. 1칸에서는 R1 부터 R5 까지 모든 라우터가 링크 상태 광고로 만든 같은 지도를 갖고 "
      "유니캐스트 경로를 계산한다. 2칸에서 R4 에 그룹 G 의 멤버 M 이 붙자 R4 가 group-membership-LSA 를 만들고, "
      "그 광고가 기존 링크 상태 브로드캐스트를 따라 R3·R2·R1·R5 로 퍼져 모든 라우터의 지도에 그룹 G 멤버는 R4 쪽이라는 줄이 더해진다. "
      "3칸에서 출발지 S 가 그룹 G 로 데이터그램을 보내면 라우터는 그 같은 지도에서 S 쪽을 뿌리로 한 최단 경로 트리를 만들고, "
      "멤버가 없는 R5 가지를 잘라 R1·R2·R3·R4 를 거쳐 M 으로 전달한다. 멀티캐스트만을 위한 지도는 따로 없다.",
      "위에서 아래로 시간 순서입니다. 광고 이름과 트리 계산 방식은 RFC 1584 에서 확인한 원문 밖 정보입니다.")

# ── 좌표 ──
STRIDE = 104                                   # 노드 중심 간격
RW, RH = 80, 44                                # 라우터 상자
HW = 72                                        # 호스트 상자 폭
SX = 84                                        # 출발지 S 중심
RX = [SX + STRIDE * (i + 1) for i in range(4)] # R1~R4 중심 188 · 292 · 396 · 500
MX = SX + STRIDE * 5                           # 멤버 M 중심 604
R5X = RX[2]                                    # R5 는 R3 아래
CX, CW = 664, 288                              # 오른쪽 지도 카드
PANEL_H, PANEL_GAP = 224, 16


def router(cx, top, name, rows_info, acc_row, dashed=False):
    x = cx - RW / 2
    if dashed:
        d.path(f"M {x} {top} L {x + RW} {top} L {x + RW} {top + RH} L {x} {top + RH} Z", MUTED, 1.1, dash="4 3")
    else:
        d.box(x, top, RW, RH, PAPER2, MUTED, 1.1, 6)
    d.t(x + 24, top + 27, name, 13, INK, MONO, "middle", 600)
    # 지도 사본 — 줄 셋은 링크 상태, 넷째 줄은 MOSPF 가 더한 광고
    d.box(x + 44, top + 7, 24, 30, PAPER, RULE, 1.0, 3)
    for k in range(rows_info):
        d.line(x + 48, top + 14 + k * 6, x + 64, top + 14 + k * 6, INFO, 2.0)
    if acc_row:
        d.line(x + 48, top + 32, x + 64, top + 32, ACC, 2.4)


def host(cx, top, label):
    d.box(cx - HW / 2, top, HW, RH, PAPER2, MUTED, 1.1, 6)
    d.t(cx, top + 27, label, 13, INK, KR, "middle", 600)


def hop(x_from, x_to, lane, row_top, c, m):
    d.arrow([(x_from, row_top), (x_from, lane), (x_to, lane), (x_to, row_top)], c, m, 1.6)


def card(y0, acc, output, footnote, focal=False):
    top = y0 + 36
    d.box(CX, top, CW, 180, f"{INK}05", RULE, 1.0, 8)
    d.t(CX + 16, top + 22, "라우터마다 같은 지도", 13, INK, KR, "start", 600)
    d.tone(CX + 16, top + 36, 256, 28, INFO, 4, "18", 1.2)
    d.t(CX + 144, top + 55, "R1 ~ R5 링크 상태", 13, INK, KR)
    # 1칸에는 둘째 줄 자리를 비워 둔다 — 2칸에서 그 자리에 줄이 생기는 것이 곧 변화다
    if acc != "none":
        if focal:
            d.tone(CX + 16, top + 72, 256, 28, ACC, 4, "22", 1.4)
        else:
            d.box(CX + 16, top + 72, 256, 28, PAPER2, ACC, 1.2, 4)
        d.t(CX + 144, top + 91, "그룹 G 멤버 · R4", 13, INK, KR, "middle", 600)
    if output:
        d.arrow([(CX + 144, top + (64 if acc == "none" else 104)), (CX + 144, top + 120)], OK, "ok", 1.4)
        d.tone(CX + 16, top + 124, 256, 28, OK, 4, "18", 1.2)
        d.t(CX + 144, top + 143, output, 13, INK, KR, "middle", 600)
    d.t(CX + 16, top + 172, footnote, 13, MUTED, KR, "start")


def panel(i, title, *, member, acc_rows, flood, datagram, card_args):
    y0 = 96 + i * (PANEL_H + PANEL_GAP)
    d.box(24, y0, 952, PANEL_H, f"{INK}05", RULE, 1.0, 10)
    d.t(40, y0 + 24, title, 13, INK, KR, "start", 600)
    lane, top, bot = y0 + 52, y0 + 68, y0 + 112
    r5_top = y0 + 148
    cy = top + RH / 2

    # 링크 — 화살표와 상자보다 먼저
    d.line(SX + HW / 2, cy, RX[0] - RW / 2, cy, MUTED, 1.2)
    for a, b in zip(RX, RX[1:]):
        d.line(a + RW / 2, cy, b - RW / 2, cy, MUTED, 1.2)
    if member:
        d.line(RX[3] + RW / 2, cy, MX - HW / 2, cy, MUTED, 1.2)
    d.line(R5X, bot, R5X, r5_top, MUTED, 1.2, dash="4 3" if datagram else None)

    # 2칸 — group-membership-LSA 가 R4 에서 기존 브로드캐스트를 따라 퍼진다
    if flood:
        d.t((RX[0] + RX[3]) / 2, y0 + 42, "group-membership-LSA · 기존 링크 상태 브로드캐스트", 13, ACC, KR, "middle", 600)
        for a, b in ((3, 2), (2, 1), (1, 0)):
            hop(RX[a] - 12, RX[b] + 12, lane, top, ACC, "acc")
        d.arrow([(R5X + 16, bot), (R5X + 16, r5_top)], ACC, "acc", 1.6)

    # 3칸 — 데이터그램이 트리를 따라 S → R1 → R2 → R3 → R4 → M
    if datagram:
        xs = [SX] + RX + [MX]
        for a, b in zip(xs, xs[1:]):
            hop(a + 12, b - 12, lane, top, OK, "ok")
        d.t(SX - HW / 2, y0 + 136, "뿌리 · S 의 네트워크", 13, OK, KR, "start", 600)
        d.t(R5X + RW / 2 + 12, y0 + 174, "멤버 없음 · 트리에서 제외", 13, MUTED, KR, "start")

    host(SX, top, "출발지 S")
    for k, x in enumerate(RX):
        router(x, top, f"R{k + 1}", 3, acc_rows)
    router(R5X, r5_top, "R5", 3, acc_rows, dashed=datagram)
    if member:
        host(MX, top, "멤버 M")
        d.t(MX, y0 + 136, "그룹 G", 13, MUTED, KR)
    card(y0, *card_args)
    return y0, top, bot


# ── 1. 출발점 ──
y0, top, bot = panel(0, "1. 모든 라우터가 같은 지도 · 유니캐스트 경로 계산",
                     member=False, acc_rows=False, flood=False, datagram=False,
                     card_args=("none", "유니캐스트 경로", "라우터마다 다익스트라"))
# 라우터 상자 안의 작은 카드가 지도 사본이라는 표시 — 1칸에만
gx = RX[0] - RW / 2 + 56
d.arrow([(gx, y0 + 136), (gx, bot + 4)], MUTED, "ar", 1.2)
d.t(gx, y0 + 156, "라우터 안 · 지도 사본", 13, MUTED, KR)

# ── 2. 멤버가 붙음 ──
panel(1, "2. R4 에 멤버 M 이 붙음 · 새 광고가 기존 브로드캐스트를 탐",
      member=True, acc_rows=True, flood=True, datagram=False,
      card_args=("focal", None, "R1 ~ R5 지도에 모두 한 줄 추가", True))

# ── 3. 보냄 ──
panel(2, "3. S 가 그룹 G 로 보냄 · 같은 지도에서 전달 경로를 뽑음",
      member=True, acc_rows=True, flood=False, datagram=True,
      card_args=("row", "멀티캐스트 전달 경로", "첫 데이터그램 때 계산 · RFC 1584"))

d.t(24, 832, "지도는 끝까지 한 종류 · 멀티캐스트용 지도를 따로 만들지 않음", 13, INK, KR, "start", 600)

d.legend(856, [("기존 링크 상태 광고", INFO), ("MOSPF 가 더한 광고", ACC), ("멀티캐스트 전달 경로", OK)])
d.t(960, 896, "KUROSE-ROSS 9E 5.3 P.348 · RFC 1584", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.ospf-mospf.svg"
d.save(out)
print("→", out)
