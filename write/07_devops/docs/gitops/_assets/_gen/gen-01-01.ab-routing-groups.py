# 타입 스펙: type-flowchart
# 01-01 ### A-B Testing — 조건 분기 기반 사용자 그룹 라우팅과 성과 비교 흐름
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, WARN, INFO, KR, MONO)

W = 960
LEGEND_Y = 372
H = LEGEND_Y + 44  # 416 (margin = 416 - (372+24) = 20 >= 16)

d = D(
    W,
    H,
    "FLOWCHART · A/B TESTING ROUTING",
    "A/B Testing 조건 분기와 성과 비교 흐름",
    "사용자 요청을 x-beta-user 헤더 조건으로 그룹 A(subset: v1)와 그룹 B(subset: v2)에 고정 분기하고 전환율과 체류 시간을 비교해 승자를 승격하는 흐름",
    lead="시간 진행이 아니라 HTTP 헤더·쿠키 조건으로 사용자를 같은 버전에 고정 분기해 비즈니스 성과 승자를 고릅니다",
)


def _fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in str(txt)) else MONO


def oval_node(x, y, w, h, line1, line2, stroke=RULE):
    r = h // 2
    d.box(x, y, w, h, PAPER2, stroke, 1.2, r)
    cx = x + w // 2
    d.t(cx, y + 26, line1, 14, INK, _fam(line1), "middle", 600)
    d.t(cx, y + 46, line2, 13, MUTED, _fam(line2), "middle")


def diamond(cx, cy, hw, hh, line1, line2, c=ACC):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    d.t(cx, cy - 4, line1, 14, c, _fam(line1), "middle", 600)
    d.t(cx, cy + 16, line2, 12, INK, _fam(line2), "middle", 600)


def group_box(x, y, w, h, title, subset, sticky, c):
    d.tone(x, y, w, h, c, r=6, op="14", sw=1.2)
    cx = x + w // 2
    d.t(cx, y + 24, title, 14, c, _fam(title), "middle", 600)
    d.t(cx, y + 44, subset, 12, INK, _fam(subset), "middle", 600)
    d.t(cx, y + 62, sticky, 13, MUTED, _fam(sticky), "middle")


# ── 가로 배치 좌표 (전부 4의 배수) ─────────────────────────────────────
CY = 228
CY_TOP = 148
CY_BOT = 308

# Col 1: Start Oval
X1, W1 = 24, 112
# Col 2: Decision Diamond (Focal ACC)
DCX, DHW, DHH = 260, 76, 48
# Col 3: Group Boxes (A -> v1, B -> v2)
X3, W3, H3 = 416, 152, 72
# Merge Point
MX = 596
# Col 4: Metric Comparison
X4, W4, H4 = 648, 124, 68
# Col 5: End Oval
X5, W5 = 820, 116

# ── 연결선 (z-order: 노드 뒤) ─────────────────────────────────────────
# Start -> Decision
d.arrow([(X1 + W1, CY), (DCX - DHW - 2, CY)], MUTED, "ar", 1.4)

# Decision -> Group A (Top, 기본 v1)
d.arrow([(DCX, CY - DHH), (DCX, CY_TOP), (X3 - 2, CY_TOP)], INFO, "info", 1.4)
d.t(344, CY_TOP - 10, "그 외 기본", 13, INFO, KR, "middle", 600)

# Decision -> Group B (Bottom, x-beta-user: true -> v2)
d.arrow([(DCX, CY + DHH), (DCX, CY_BOT), (X3 - 2, CY_BOT)], OK, "ok", 1.4)
d.t(344, CY_BOT + 22, 'exact: "true"', 12, OK, MONO, "middle", 600)

# Group A & Group B -> Merge Dot -> Comparison
d.path(f"M {X3 + W3} {CY_TOP} L {MX} {CY_TOP} L {MX} {CY - 4}", INFO, 1.3)
d.path(f"M {X3 + W3} {CY_BOT} L {MX} {CY_BOT} L {MX} {CY + 4}", OK, 1.3)
d.o.append(f'<circle cx="{MX}" cy="{CY}" r="4" fill="{INK}"/>')
d.arrow([(MX + 4, CY), (X4 - 2, CY)], WARN, "warn", 1.4)

# Comparison -> Winner End
d.arrow([(X4 + W4, CY), (X5 - 2, CY)], MUTED, "ar", 1.4)

# ── 노드 ───────────────────────────────────────────────────────────────
oval_node(X1, CY - 32, W1, 64, "사용자 요청", "헤더 · 쿠키", MUTED)

diamond(DCX, CY, DHW, DHH, "라우터 조건", "x-beta-user", ACC)

group_box(X3, CY_TOP - H3 // 2, W3, H3, "그룹 A · v1", "subset: v1", "세션 고정", INFO)
group_box(X3, CY_BOT - H3 // 2, W3, H3, "그룹 B · v2", "subset: v2", "세션 고정", OK)

d.tone(X4, CY - H4 // 2, W4, H4, WARN, r=6, op="14", sw=1.2)
d.t(X4 + W4 // 2, CY - 6, "지표 비교", 14, WARN, KR, "middle", 600)
d.t(X4 + W4 // 2, CY + 16, "전환율 · 체류", 13, INK, KR, "middle")

oval_node(X5, CY - 32, W5, 64, "승자 승격", "v1 또는 v2", MUTED)

# ── 범례 ───────────────────────────────────────────────────────────────
d.legend(
    LEGEND_Y,
    [
        ("조건 분기 (핵심)", ACC),
        ("그룹 A (v1)", INFO),
        ("그룹 B (v2)", OK),
        ("성과 비교", WARN),
    ],
)

out_path = sys.argv[1] if len(sys.argv) > 1 else "01-01.ab-routing-groups.svg"
d.save(out_path)
print(f"saved: {out_path}")
