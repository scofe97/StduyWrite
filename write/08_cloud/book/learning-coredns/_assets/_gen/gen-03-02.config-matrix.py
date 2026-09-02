# 03-02 §8 — 원서가 든 세 벌의 Corefile 에 어느 플러그인이 들어가는가.
# 원문 근거: Example 3-37 캐싱 전용(forward · cache · errors · log),
#            Example 3-38 주 서버(root · file · errors · log, 재귀도 맡으면 forward · cache 블록 추가),
#            Example 3-39 보조 서버(logerrors 스니펫으로 errors·log, foo.example 은 root·file,
#            재귀용 . 블록에 forward · cache).
# 타입 스펙: type-dp-security-matrix — 행×열 격자에서 어느 조합이 되고 안 되는가가 논지다.
#           좌표는 스펙 §2 Layout formulas 를 쓰되 이 저장소 D() 머리글만큼 32 내린다. 색은 다크 스킨 계약.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, RIGHT_PAD = 12, 48
COMP_COL_W, COMP_ROLE_GAP = 208, 12
ROLE_COL_W, ROLE_COL_GAP = 148, 16
HEADER_H, ROW_H, ROW_STRIDE = 52, 36, 40
HEADER_Y = 104

configs = [("캐싱 전용", "3-37"), ("주 서버", "3-38"), ("보조 서버", "3-39")]
plugins = [("root", "작업 디렉터리"), ("file", "주 서버로"), ("secondary", "보조 서버로"),
           ("forward", "포워더로"), ("cache", "응답 캐시"), ("errors", "오류 로그"), ("log", "질의 로그")]
cells = {
    (0, 1): ("쓴다", "full"), (0, 2): ("쓴다", "full"),
    (1, 1): ("쓴다", "full"), (1, 2): ("쓴다", "full"),
    (2, 2): ("원서 예제에 빠짐", "focal"),
    (3, 0): ("쓴다", "full"), (3, 1): ("재귀도 맡으면", "read"), (3, 2): ("재귀도 맡으면", "read"),
    (4, 0): ("쓴다", "full"), (4, 1): ("재귀도 맡으면", "read"), (4, 2): ("재귀도 맡으면", "read"),
    (5, 0): ("쓴다", "full"), (5, 1): ("쓴다", "full"), (5, 2): ("스니펫으로", "full"),
    (6, 0): ("쓴다", "full"), (6, 1): ("쓴다", "full"), (6, 2): ("스니펫으로", "full"),
}

n_roles, n_comp = len(configs), len(plugins)
W = LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + n_roles * ROLE_COL_W + (n_roles - 1) * ROLE_COL_GAP + RIGHT_PAD
def row_y(k): return 172 + k * ROW_STRIDE
def role_x(j): return LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)
LEGEND_Y = row_y(n_comp - 1) + ROW_H + 20
H = LEGEND_Y + 44

d = D(W, H, "LEARNING COREDNS · 03-02 §8",
      "세 벌의 설정에 들어가는 플러그인",
      "행이 기본 플러그인 일곱, 열이 원서가 든 세 벌의 Corefile 이다. "
      "캐싱 전용은 권한이 없어 root·file 이 필요 없고, 주 서버와 보조 서버는 재귀까지 맡을 때만 forward·cache 를 더한다.",
      "색이 붙은 칸이 원서 예제에서 빠진 지시어입니다")

d.box(LEFT_PAD, HEADER_Y, COMP_COL_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 24, "플러그인", 12, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 42, "대 서버 유형", 12, MUTED)
for j, (nm, ex) in enumerate(configs):
    x = role_x(j)
    d.box(x, HEADER_Y, ROLE_COL_W, HEADER_H, PAPER2, RULE, 1.4, 6)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 22, nm, 13, INK, KR, "middle", 600)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 40, "Example " + ex, 12, SOFT, MONO)

for k, (nm, hint) in enumerate(plugins):
    y = row_y(k)
    d.box(LEFT_PAD, y, COMP_COL_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT_PAD + 12, y + 23, nm, 12, INK, MONO, "start", 600)
    d.t(LEFT_PAD + COMP_COL_W - 12, y + 23, hint, 12, MUTED, KR, "end")
    for j in range(n_roles):
        x = role_x(j)
        val, lvl = cells.get((k, j), ("안 쓴다", "none"))
        if lvl == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + ROLE_COL_W / 2, y + 17, val, 12, ACC, KR, "middle", 600)
            d.t(x + ROLE_COL_W / 2, y + 31, "본문은 필요하다고 적는다", 11, ACC, KR)
        elif lvl == "full":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{INK}14" stroke="{RULE}" stroke-width="0.6"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, INK, KR, "middle", 600)
        elif lvl == "read":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{MUTED}14" stroke="{RULE}" stroke-width="0.6"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, MUTED, KR)
        else:
            d.box(x, y, ROLE_COL_W, ROW_H, PAPER, RULE, 0.6, 4)
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, SOFT, KR)

d.legend(LEGEND_Y, [("원서 예제가 빠뜨린 칸", ACC), ("그 설정에 들어간다", INK), ("조건부로 더한다", MUTED)])
d.save("03-02.config-matrix.svg")
