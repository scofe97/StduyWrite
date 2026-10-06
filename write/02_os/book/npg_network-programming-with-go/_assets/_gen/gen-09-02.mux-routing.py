# 타입 스펙: type-sankey
# 09-02 ServeMux 의 8개 테스트 경로와 라우팅 매칭 흐름
# 사실 출처: NPG Ch.9 Listing 9-16 (mux_test.go 8개 테스트 케이스, 경로·패턴·상태코드·본문)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 520
d = D(W, H, "NPG CH.9 — SERVEMUX ROUTING SANKEY",
      "ServeMux 의 8개 테스트 요청 라우팅 흐름",
      "요청 경로 8개가 3개 등록 패턴과 리다이렉트로 흘러가 응답 상태 코드로 분기합니다",
      "정확 일치, 하위 트리 접두사 매칭, 트레일링 슬래시 301 리다이렉트의 흐름")

# Column positions
c1_x, c1_w = 230, 12
c2_x, c2_w = 460, 12
c3_x, c3_w = 690, 12

mid12 = (c1_x + c1_w + c2_x) / 2  # 351
mid23 = (c2_x + c2_w + c3_x) / 2  # 581

# Column headers
d.t(c1_x + c1_w / 2, 106, "REQUEST PATH (8)", 9, SOFT, MONO, "middle")
d.t(c2_x + c2_w / 2, 106, "ROUTING PATTERN", 9, SOFT, MONO, "middle")
d.t(c3_x + c3_w / 2, 106, "RESPONSE STATUS", 9, SOFT, MONO, "middle")

# Helper for Sankey ribbon (smooth cubic bezier)
def ribbon(x1, y1_top, y1_bot, x2, y2_top, y2_bot, mx, c, op="2e"):
    p = (f"M {x1} {y1_top} "
         f"C {mx} {y1_top} {mx} {y2_top} {x2} {y2_top} "
         f"L {x2} {y2_bot} "
         f"C {mx} {y2_bot} {mx} {y1_bot} {x1} {y1_bot} Z")
    d.o.append(f'<path d="{p}" fill="{c}" fill-opacity="{int(op, 16)/255:.2f}" stroke="none"/>')

# --- Col 1 Nodes (k = 28px per unit) ---
# 8 requests, each 28px tall, 8px gap
r1_y = 126
r2_y = r1_y + 36  # 162
r3_y = r2_y + 36  # 198
r4_y = r3_y + 36  # 234 (Redirect case)
r5_y = r4_y + 36  # 270
r6_y = r5_y + 36  # 306
r7_y = r6_y + 36  # 342
r8_y = r7_y + 36  # 378
kh = 28

# --- Col 2 Nodes ---
# Node 1: /hello (1 unit = 28px)
p_hello_y = 126
# Node 2: /hello/there/ (2 units = 56px)
p_tree_y = 186
# Node 3: 리다이렉트 /hello/there/ (1 unit = 28px)
p_redir_y = 266
# Node 4: / (4 units = 112px)
p_root_y = 318

# --- Col 3 Nodes ---
# Node 1: 200 OK (3 units = 84px)
s_200_y = 136
# Node 2: 301 Moved (1 unit = 28px)
s_301_y = 244
# Node 3: 204 NoContent (4 units = 112px)
s_204_y = 296

# ── 1. Ordinary Ribbons (Col 1 -> Col 2) ──
# Req 1 -> Pattern /hello
ribbon(c1_x + c1_w, r1_y, r1_y + kh, c2_x, p_hello_y, p_hello_y + kh, mid12, MUTED, "2a")
# Req 2 -> Pattern /hello/there/ (top half)
ribbon(c1_x + c1_w, r2_y, r2_y + kh, c2_x, p_tree_y, p_tree_y + kh, mid12, MUTED, "2a")
# Req 3 -> Pattern /hello/there/ (bottom half)
ribbon(c1_x + c1_w, r3_y, r3_y + kh, c2_x, p_tree_y + kh, p_tree_y + 2*kh, mid12, MUTED, "2a")
# Req 5 -> Pattern / (part 1)
ribbon(c1_x + c1_w, r5_y, r5_y + kh, c2_x, p_root_y, p_root_y + kh, mid12, MUTED, "2a")
# Req 6 -> Pattern / (part 2)
ribbon(c1_x + c1_w, r6_y, r6_y + kh, c2_x, p_root_y + kh, p_root_y + 2*kh, mid12, MUTED, "2a")
# Req 7 -> Pattern / (part 3)
ribbon(c1_x + c1_w, r7_y, r7_y + kh, c2_x, p_root_y + 2*kh, p_root_y + 3*kh, mid12, MUTED, "2a")
# Req 8 -> Pattern / (part 4)
ribbon(c1_x + c1_w, r8_y, r8_y + kh, c2_x, p_root_y + 3*kh, p_root_y + 4*kh, mid12, MUTED, "2a")

# ── 2. Ordinary Ribbons (Col 2 -> Col 3) ──
# Pattern /hello -> 200 OK (part 1)
ribbon(c2_x + c2_w, p_hello_y, p_hello_y + kh, c3_x, s_200_y, s_200_y + kh, mid23, OK, "30")
# Pattern /hello/there/ -> 200 OK (parts 2 & 3)
ribbon(c2_x + c2_w, p_tree_y, p_tree_y + 2*kh, c3_x, s_200_y + kh, s_200_y + 3*kh, mid23, OK, "30")
# Pattern / -> 204 No Content (all 4 parts)
ribbon(c2_x + c2_w, p_root_y, p_root_y + 4*kh, c3_x, s_204_y, s_204_y + 4*kh, mid23, MUTED, "2a")

# ── 3. Accent Ribbon (Focal Path: Trailing Slash 301 Redirect) ──
# Req 4 (/hello/there) -> Redirection -> 301 Moved Permanently
ribbon(c1_x + c1_w, r4_y, r4_y + kh, c2_x, p_redir_y, p_redir_y + kh, mid12, ACC, "55")
ribbon(c2_x + c2_w, p_redir_y, p_redir_y + kh, c3_x, s_301_y, s_301_y + kh, mid23, ACC, "55")

# ── 4. Col 1 Node Bars & Labels ──
req_labels = [
    (r1_y, "/hello", "정확 일치 1건"),
    (r2_y, "/hello/there/", "하위 트리 1건"),
    (r3_y, "/hello/there/you", "하위 트리 1건"),
    (r4_y, "/hello/there", "슬래시 누락 1건"),
    (r5_y, "/", "루트 일치 1건"),
    (r6_y, "/hello/and/goodbye", "미일치(루트) 1건"),
    (r7_y, "/something/else/entirely", "미일치(루트) 1건"),
    (r8_y, "/hello/you", "미일치(루트) 1건"),
]

for y, path, sub in req_labels:
    c = ACC if path == "/hello/there" else INK
    d.box(c1_x, y, c1_w, kh, fill=c, stroke=RULE, sw=0.5, r=2)
    d.t(c1_x - 12, y + 12, path, 11, c, MONO, "end", 600)
    d.t(c1_x - 12, y + 25, sub, 11, MUTED, KR, "end")

# ── 5. Col 2 Node Bars & Labels (Beside Node Bars) ──
# Node 1: /hello
d.box(c2_x, p_hello_y, c2_w, kh, fill=INK, stroke=RULE, sw=0.5, r=2)
d.t(c2_x + c2_w + 12, p_hello_y + kh / 2 + 4, '"/hello" (1건)', 11, INK, KR, "start", 600)

# Node 2: /hello/there/
d.box(c2_x, p_tree_y, c2_w, 2 * kh, fill=INK, stroke=RULE, sw=0.5, r=2)
d.t(c2_x + c2_w + 12, p_tree_y + kh + 4, '"/hello/there/" (2건)', 11, INK, KR, "start", 600)

# Node 3: Redirection (ACC)
d.box(c2_x, p_redir_y, c2_w, kh, fill=ACC, stroke=RULE, sw=0.5, r=2)
d.t(c2_x + c2_w + 12, p_redir_y + kh / 2 + 4, '슬래시 추가 301 (1건)', 11, ACC, KR, "start", 600)

# Node 4: /
d.box(c2_x, p_root_y, c2_w, 4 * kh, fill=INK, stroke=RULE, sw=0.5, r=2)
d.t(c2_x + c2_w + 12, p_root_y + 2 * kh + 4, '"/" 기본 (4건)', 11, INK, KR, "start", 600)

# ── 6. Col 3 Node Bars & Labels ──
# Node 1: 200 OK (3건)
d.box(c3_x, s_200_y, c3_w, 3 * kh, fill=OK, stroke=RULE, sw=0.5, r=2)
d.t(c3_x + c3_w + 14, s_200_y + 26, "200 OK (3건)", 12, OK, MONO, "start", 600)
d.t(c3_x + c3_w + 14, s_200_y + 44, '"Hello friend." / "Why, hello there."', 11, MUTED, KR, "start")

# Node 2: 301 Moved (1건)
d.box(c3_x, s_301_y, c3_w, kh, fill=ACC, stroke=RULE, sw=0.5, r=2)
d.t(c3_x + c3_w + 14, s_301_y + 14, "301 Moved Permanently (1건)", 11, ACC, MONO, "start", 600)
d.t(c3_x + c3_w + 14, s_301_y + 28, 'Location: /hello/there/ 리다이렉트', 11, MUTED, KR, "start")

# Node 3: 204 No Content (4건)
d.box(c3_x, s_204_y, c3_w, 4 * kh, fill=MUTED, stroke=RULE, sw=0.5, r=2)
d.t(c3_x + c3_w + 14, s_204_y + 44, "204 No Content (4건)", 12, INK, MONO, "start", 600)
d.t(c3_x + c3_w + 14, s_204_y + 62, '"" (응답 본문 없음)', 11, MUTED, KR, "start")

# 범례
d.legend(456, [
    ("정상 성공 (200 OK)", OK),
    ("후행 슬래시 보정 (301 Moved)", ACC),
    ("기본 일치 (204 No Content)", MUTED),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "09-02.mux-routing.svg")
d.save(out_path)
print("saved:", out_path)
