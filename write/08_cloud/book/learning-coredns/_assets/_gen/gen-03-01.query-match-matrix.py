# 03-01 §6 — 질의 다섯이 Example 3-15 의 엔트리 다섯 가운데 어디에 붙는가.
# 원문 근거: "For a server block to apply to a given query, the protocol (TLS, gRPC, or plain-vanilla
#            DNS) port on which the query was received and domain name in the query must match the
#            label. In the event that the domain name in the query matches multiple labels, the
#            longest (i.e., most specific) match wins." 이어지는 문단이 질의 다섯의 귀속을 하나씩 적는다.
# 타입 스펙: type-dp-security-matrix — 행×열 격자에서 어느 조합이 되고 안 되는가가 논지다.
#           좌표는 스펙 §2 Layout formulas 를 그대로 쓴다(row_stride 40 등. 열 폭은 viewBox 상한 1000 에 맞춰 148 → 138 로 줄였다).
#           색은 이 저장소의 다크 스킨 계약으로 치환한다 — 스펙의 white/ink 배색은 밝은 테마 전제다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, RIGHT_PAD = 12, 16
COMP_COL_W, COMP_ROLE_GAP = 208, 12
ROLE_COL_W, ROLE_COL_GAP = 138, 12
HEADER_H, ROW_H, ROW_STRIDE = 52, 36, 40
HEADER_Y = 104   # 스펙은 72 지만 이 저장소의 D() 머리글(eyebrow·제목·요약)이 74 까지 쓰므로 32 내린다

entries = [("foo.example", "첫째"), ("tls://foo.example", "둘째"), ("bar.example", "셋째"),
           ("bar.example:1053", "넷째"), (".", "다섯째")]
queries = [("www.foo.example", "53 · 평문"), ("www.foo.example", "853 · TLS"),
           ("bar.example MX", "53 · 평문"), ("bar.example", "1053 · 평문"),
           ("그 밖의 이름", "53 · 평문")]
# (row, col) -> (값, 등급). 등급은 스펙의 닫힌 어휘 full | read | none | focal
cells = {
    (0, 0): ("directive1", "focal"), (0, 4): ("라벨은 맞지만 짧다", "read"),
    (1, 1): ("directive2", "full"),
    (2, 2): ("directive3", "full"), (2, 4): ("라벨은 맞지만 짧다", "read"),
    (3, 3): ("directive4", "full"),
    (4, 4): ("directive5·6", "full"),
}

n_roles, n_comp = len(entries), len(queries)
W = LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + n_roles * ROLE_COL_W + (n_roles - 1) * ROLE_COL_GAP + RIGHT_PAD
def row_y(k): return 172 + k * ROW_STRIDE   # 스펙 140 + 위와 같은 오프셋
def role_x(j): return LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)
rows_bottom = row_y(n_comp - 1) + ROW_H
LEGEND_Y = rows_bottom + 20
H = LEGEND_Y + 44

d = D(W, H, "LEARNING COREDNS · 03-01 §6",
      "질의 하나가 붙는 엔트리는 하나뿐이다",
      "행이 들어온 질의, 열이 Corefile 의 엔트리다. 프로토콜과 포트와 도메인 이름이 모두 라벨과 맞아야 하고, "
      "도메인 이름이 여러 라벨에 맞으면 가장 긴 라벨이 이긴다.",
      "색이 붙은 칸이 최장 일치가 갈리는 자리입니다")

d.box(LEFT_PAD, HEADER_Y, COMP_COL_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 24, "들어온 질의", 12, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_COL_W / 2, HEADER_Y + 42, "대 Corefile 엔트리", 12, MUTED)
for j, (nm, code) in enumerate(entries):
    x = role_x(j)
    d.box(x, HEADER_Y, ROLE_COL_W, HEADER_H, PAPER2, RULE, 1.4, 6)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 22, nm, 12, INK, MONO, "middle", 600)
    d.t(x + ROLE_COL_W / 2, HEADER_Y + 40, code, 12, SOFT, KR)

for k, (nm, hint) in enumerate(queries):
    y = row_y(k)
    d.box(LEFT_PAD, y, COMP_COL_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT_PAD + 12, y + 23, nm, 12, INK, MONO if nm[0].isascii() else KR, "start", 600)
    d.t(LEFT_PAD + COMP_COL_W - 12, y + 23, hint, 12, MUTED, KR, "end")
    for j in range(n_roles):
        x = role_x(j)
        val, lvl = cells.get((k, j), ("맞지 않음", "none"))
        if lvl == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + ROLE_COL_W / 2, y + 17, val, 12, ACC, MONO, "middle", 600)
            d.t(x + ROLE_COL_W / 2, y + 31, "더 긴 라벨이 이긴다", 11, ACC, KR)
        elif lvl == "full":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{INK}14" stroke="{RULE}" stroke-width="0.6"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, INK, MONO, "middle", 600)
        elif lvl == "read":
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{MUTED}14" stroke="{RULE}" stroke-width="0.6"/>')
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, MUTED, KR)
        else:
            d.box(x, y, ROLE_COL_W, ROW_H, PAPER, RULE, 0.6, 4)
            d.t(x + ROLE_COL_W / 2, y + 23, val, 12, SOFT, KR)

d.legend(LEGEND_Y, [("최장 일치가 갈리는 칸", ACC), ("이 엔트리가 적용된다", INK), ("맞지만 더 짧다", MUTED)])
d.save("03-01.query-match-matrix.svg")
