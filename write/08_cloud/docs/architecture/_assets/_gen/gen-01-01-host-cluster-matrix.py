# -*- coding: utf-8 -*-
"""01-01 §4 도식 — 물리 호스트 × 클러스터 배치 행렬.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
좌표는 type-dp-security-matrix §2 Layout formulas 를 이 문서의 여백(left_pad 64)에 맞춰 적용했다.
스킨은 writing-method Diagram Design 스타일 계약의 다크 토큰을 쓴다.
"""
import pathlib

# ── 선언 ──────────────────────────────────────────────────────────────
TITLE    = "겹치는 것은 Node 가 아니라 그 아래 호스트입니다"
SUBTITLE = "물리 컴퓨트 호스트 다섯 대 위에 세 클러스터의 노드 VM 이 흩어진 배치"
EYEBROW  = "PHYSICAL HOST x CLUSTER"

CLUSTERS = [                        # 열 (2..6)
    {"name": "클러스터 A", "code": "hosts 1-3"},
    {"name": "클러스터 B", "code": "hosts 3-5"},
    {"name": "클러스터 C", "code": "hosts 2-4"},
]
HOSTS = ["호스트 1", "호스트 2", "호스트 3", "호스트 4", "호스트 5"]   # 행 (2..14)

# level: on | none,  focal 은 정확히 하나
CELLS = {
    (0, 0): "on",
    (1, 0): "on", (1, 2): "on",
    (2, 0): "on", (2, 1): "focal", (2, 2): "on",
    (3, 1): "on", (3, 2): "on",
    (4, 1): "on",
}
ON_LABEL, NONE_LABEL = "노드 VM", "없음"

# ── 레이아웃 공식 ──────────────────────────────────────────────────────
LEFT_PAD, RIGHT_PAD = 64, 64
COMP_COL_W, COMP_ROLE_GAP = 208, 12
ROLE_COL_W, ROLE_COL_GAP = 148, 16
HEADER_Y, HEADER_H = 128, 52
ROW_H, ROW_STRIDE, ROW_Y0 = 36, 40, 196

n_c, n_h = len(CLUSTERS), len(HOSTS)
VB_W = LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + n_c * ROLE_COL_W + (n_c - 1) * ROLE_COL_GAP + RIGHT_PAD
row_y = lambda k: ROW_Y0 + k * ROW_STRIDE
rows_bottom = row_y(n_h - 1) + ROW_H
LEGEND_Y = rows_bottom + 20
VB_H = LEGEND_Y + 44
col_x = lambda j: LEFT_PAD + COMP_COL_W + COMP_ROLE_GAP + j * (ROLE_COL_W + ROLE_COL_GAP)
col_cx = lambda j: col_x(j) + ROLE_COL_W // 2

for v in (VB_W, VB_H, HEADER_Y, ROW_Y0, LEGEND_Y):
    assert v % 4 == 0, f"4의 배수가 아님: {v}"

STYLE = {                                    # fill, stroke, stroke-w, text, weight
    "on":    ("rgba(106,149,216,0.12)", "rgba(106,149,216,0.55)", "1", "var(--info)", "400"),
    "none":  ("rgba(245,245,243,0.02)", "rgba(245,245,243,0.10)", "0.6", "var(--soft)", "400"),
    "focal": ("var(--accent12)",        "var(--accent)",          "1.4", "var(--accent)", "600"),
}

# ── 방출 ──────────────────────────────────────────────────────────────
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-labelledby="t1 d1">')
o.append('<title id="t1">물리 호스트 다섯 대에 세 클러스터의 노드 VM 이 얹힌 배치</title>')
o.append('<desc id="d1">세로축은 물리 컴퓨트 호스트, 가로축은 클러스터입니다. 채워진 칸은 그 호스트 위에 그 클러스터의 노드 가상 머신이 떠 있다는 뜻입니다. 호스트 3만 세 클러스터를 모두 얹고 있으며 그 칸이 강조돼 있습니다.</desc>')
o.append("""<style>
svg{--paper:#0D1117;--paper2:#161B22;--ink:#F5F5F3;--muted:#8B98A9;--soft:#5E6B7E;--rule:rgba(191,192,192,0.22);--accent:#F08A59;--accent12:rgba(240,138,89,0.12);--info:#6A95D8}
.kr{font-family:'Geist','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif}
.mn{font-family:'Geist Mono','Noto Sans Mono CJK KR',monospace}
.eyebrow{fill:var(--soft);font-size:9px;letter-spacing:.14em}
.h1{fill:var(--ink);font-size:20px;font-weight:600}
.sub{fill:var(--muted);font-size:12px}
.hdr{fill:var(--ink);font-size:12px;font-weight:600}
.code{fill:var(--muted);font-size:10px}
.rowlab{fill:var(--ink);font-size:12px}
.cell{font-size:12px}
.leg{fill:var(--muted);font-size:12px}
.hair{stroke:var(--rule);stroke-width:1}
</style>""")
o.append(f'<rect width="{VB_W}" height="{VB_H}" fill="var(--paper)"/>')
o.append(f'<text class="mn eyebrow" x="{LEFT_PAD}" y="44">{EYEBROW}</text>')
o.append(f'<text class="kr h1" x="{LEFT_PAD}" y="76">{TITLE}</text>')
o.append(f'<text class="kr sub" x="{LEFT_PAD}" y="98">{SUBTITLE}</text>')

# 헤더행
o.append(f'<rect x="{LEFT_PAD}" y="{HEADER_Y}" width="{COMP_COL_W}" height="{HEADER_H}" rx="6" fill="var(--paper2)" stroke="rgba(245,245,243,0.10)" stroke-width="0.8"/>')
o.append(f'<text class="kr hdr" x="{LEFT_PAD + COMP_COL_W // 2}" y="{HEADER_Y + 24}" text-anchor="middle">물리 호스트</text>')
o.append(f'<text class="kr code" x="{LEFT_PAD + COMP_COL_W // 2}" y="{HEADER_Y + 42}" text-anchor="middle">하이퍼바이저가 관리하는 실물</text>')
for j, c in enumerate(CLUSTERS):
    o.append(f'<rect x="{col_x(j)}" y="{HEADER_Y}" width="{ROLE_COL_W}" height="{HEADER_H}" rx="6" fill="var(--paper2)" stroke="rgba(245,245,243,0.10)" stroke-width="0.8"/>')
    o.append(f'<text class="kr hdr" x="{col_cx(j)}" y="{HEADER_Y + 24}" text-anchor="middle">{c["name"]}</text>')
    o.append(f'<text class="mn code" x="{col_cx(j)}" y="{HEADER_Y + 42}" text-anchor="middle">{c["code"]}</text>')

# 데이터행
for k, host in enumerate(HOSTS):
    y = row_y(k)
    o.append(f'<rect x="{LEFT_PAD}" y="{y}" width="{COMP_COL_W}" height="{ROW_H}" rx="4" fill="rgba(245,245,243,0.03)" stroke="rgba(245,245,243,0.10)" stroke-width="0.8"/>')
    o.append(f'<text class="kr rowlab" x="{LEFT_PAD + 12}" y="{y + 23}">{host}</text>')
    for j in range(n_c):
        lvl = CELLS.get((k, j), "none")
        fill, stroke, sw, tc, fw = STYLE[lvl]
        label = NONE_LABEL if lvl == "none" else ON_LABEL
        o.append(f'<rect x="{col_x(j)}" y="{y}" width="{ROLE_COL_W}" height="{ROW_H}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        o.append(f'<text class="kr cell" x="{col_cx(j)}" y="{y + 23}" text-anchor="middle" fill="{tc}" font-weight="{fw}">{label}</text>')

# 범례
o.append(f'<line class="hair" x1="{LEFT_PAD}" y1="{LEGEND_Y}" x2="{VB_W - RIGHT_PAD}" y2="{LEGEND_Y}"/>')
o.append(f'<text class="mn eyebrow" x="{LEFT_PAD}" y="{LEGEND_Y + 26}">LEGEND</text>')
legend = [("on", "노드 VM 이 떠 있음"), ("none", "없음"), ("focal", "세 클러스터가 만나는 자리")]
lx = LEFT_PAD + 72
for lvl, text in legend:
    fill, stroke, sw, tc, _ = STYLE[lvl]
    o.append(f'<rect x="{lx}" y="{LEGEND_Y + 16}" width="14" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    o.append(f'<text class="kr leg" x="{lx + 22}" y="{LEGEND_Y + 26}">{text}</text>')
    lx += 24 + len(text) * 12 + 32

assert lx <= VB_W - RIGHT_PAD, f"범례가 캔버스를 넘음: {lx} > {VB_W - RIGHT_PAD}"
assert sum(1 for v in CELLS.values() if v == "focal") == 1, "focal 은 정확히 하나"
o.append("</svg>")

out = pathlib.Path(__file__).resolve().parents[1] / "01-01-host-cluster-matrix.svg"
out.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"wrote {out}  viewBox={VB_W}x{VB_H}  legend_end={lx}")
