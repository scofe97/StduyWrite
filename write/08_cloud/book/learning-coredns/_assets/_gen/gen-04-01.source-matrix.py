# 04-01 §1 — 존 데이터를 관리하는 네 갈래가 무엇에서 갈리는가.
# 원문 근거: file 은 존 데이터 파일에서 읽고 transfer to 로 전송을 허용한다 /
#            auto 는 디렉터리를 스캔해 db.* 를 읽고 "you can create another zone ... just by creating
#            a new, appropriately named zone data file" / hosts 로 읽은 존은 "aren't really complete
#            zones; they don't have SOA records, for example, so they can't be transferred to another
#            DNS server" / route53 은 "much like a secondary DNS server would transfer zone data"
#            이며 존마다 ZONE:HOSTED_ZONE_ID 를 Corefile 에 적어야 한다.
# 타입 스펙: type-dp-security-matrix — 행×열 격자에서 어느 조합이 되고 안 되는가가 논지다.
#           좌표는 스펙 §2 Layout formulas 를 쓰되 이 저장소 D() 머리글만큼 32 내린다. 색은 다크 스킨 계약.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, RIGHT_PAD = 12, 48
COMP_COL_W, COMP_ROLE_GAP = 208, 12
ROLE_COL_W, ROLE_COL_GAP = 148, 16
HEADER_H, ROW_H, ROW_STRIDE = 52, 36, 40
HEADER_Y = 104

questions = [("존 전체를 담나", "SOA 를 갖나"), ("다른 서버로 전송", "transfer to"), ("새 존 자동 편입", "Corefile 손 안 대고")]
methods = [("file", "존 데이터 파일"), ("auto", "디렉터리 스캔"),
           ("hosts", "호스트 테이블"), ("route53", "AWS Route 53")]
cells = {
    (0, 0): ("담는다", "full"), (0, 1): ("된다", "full"), (0, 2): ("안 된다", "none"),
    (1, 0): ("담는다", "full"), (1, 1): ("된다", "full"), (1, 2): ("된다", "focal"),
    (2, 0): ("SOA 가 없다", "none"), (2, 1): ("못 한다", "none"), (2, 2): ("해당 없음", "none"),
    (3, 0): ("동기화한다", "full"), (3, 1): ("원서에 없음", "read"), (3, 2): ("존:ID 를 적어야", "none"),
}

n_roles, n_comp = len(questions), len(methods)
W = LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + n_roles * ROLE_COL_W + (n_roles - 1) * ROLE_COL_GAP + RIGHT_PAD
def row_y(k): return 172 + k * ROW_STRIDE
def role_x(j): return LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)
LEGEND_Y = row_y(n_comp - 1) + ROW_H + 20
H = LEGEND_Y + 44

d = D(W, H, "LEARNING COREDNS · 04-01 §1",
      "존 데이터를 관리하는 네 갈래",
      "행이 관리 방법 넷, 열이 그것을 가르는 질문 셋이다. "
      "`hosts` 만 존이 아니라 레코드 몇 줄을 싣는 쪽이고, 새 존이 저절로 들어오는 것은 `auto` 뿐이다.",
      "색이 붙은 칸이 이 장이 3장에 더하는 것입니다")

d.box(LEFT_PAD, HEADER_Y, COMP_COL_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 24, "관리 방법", 12, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 42, "대 가르는 질문", 12, MUTED)
for j, (nm, sub) in enumerate(questions):
    x = role_x(j)
    d.box(x, HEADER_Y, ROLE_COL_W, HEADER_H, PAPER2, RULE, 1.4, 6)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 22, nm, 13, INK, KR, "middle", 600)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 40, sub, 12, SOFT, KR)

for k, (nm, hint) in enumerate(methods):
    y = row_y(k)
    d.box(LEFT_PAD, y, COMP_COL_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT_PAD + 12, y + 23, nm, 12, INK, MONO, "start", 600)
    d.t(LEFT_PAD + COMP_COL_W - 12, y + 23, hint, 12, MUTED, KR, "end")
    for j in range(n_roles):
        x = role_x(j)
        val, lvl = cells[(k, j)]
        if lvl == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + ROLE_COL_W / 2, y + 17, val, 12, ACC, KR, "middle", 600)
            d.t(x + ROLE_COL_W / 2, y + 31, "파일만 새로 놓으면 된다", 11, ACC, KR)
        elif lvl == "full":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{INK}14" stroke="{RULE}" stroke-width="0.6"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, INK, KR, "middle", 600)
        elif lvl == "read":
            # 원서가 말하지 않은 칸은 점선으로 — 실선 흐린 칸(안 된다)과 렌더에서 구분되지 않아 범례가 헛짚힌다
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{MUTED}14" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5 4"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, MUTED, KR)
        else:
            d.box(x, y, ROLE_COL_W, ROW_H, PAPER, RULE, 0.6, 4)
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, SOFT, KR)

d.legend(LEGEND_Y, [("auto 만 되는 것", ACC), ("된다고 적힌 칸", INK), ("원서가 말하지 않은 칸 · 점선", MUTED)])
d.save("04-01.source-matrix.svg")
