# 03-01 §2 요청이 Envoy를 지나는 길 — downstream → Listener → Route → Cluster → upstream.
# 값 근거: 03-01 본문 §2 불릿의 예(포트 80 리스너, /catalog 라우트, catalog-v1 클러스터). 책 3.1.1 의 Listener·Routes·Clusters 정의 예와 같은 값이다.
# 타입 스펙: type-data-flow — §1 lanes 3 · steps 5 · nodes 5 · arrows 4, §2 공식으로 좌표 산출.
#           폭을 880(본문 삽입 하한)으로 맞추어 `httpbin_service`가 Cluster 상자 테두리에 닿지 않게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

# §2 공식
label_col_w, step_slot_w, right_pad = 140, 140, 40
lanes = [("DOWNSTREAM", "DWN"), ("ENVOY", "ENV"), ("UPSTREAM", "UPS")]
steps = [("01", "REQUEST"), ("02", "LISTENER"), ("03", "ROUTE"), ("04", "CLUSTER"), ("05", "UPSTREAM")]
FOCAL_STEP = 4
n_steps, n_lanes = len(steps), len(lanes)
vb_w = label_col_w + n_steps * step_slot_w + right_pad        # 880
header_h, lane_h, legend_h = 36, 84, 44
grid_h = header_h + n_lanes * lane_h + legend_h                # 332
Y0 = 88
W, H = vb_w, Y0 + grid_h                                       # 880 x 420

def lane_top(k): return Y0 + header_h + k * lane_h
def lane_mid(k): return lane_top(k) + lane_h / 2
def step_cx(j): return label_col_w + j * step_slot_w + step_slot_w / 2
node_w, node_h = 128, 68
def node_x(j): return step_cx(j) - node_w / 2
def node_y(k): return lane_top(k) + 8
legend_top = Y0 + header_h + n_lanes * lane_h

d = D(W, H, "ISTIO IN ACTION · 03-01 §2",
      "요청은 downstream에서 upstream으로 흐른다",
      "요청이 downstream 에서 Envoy 의 Listener·Route·Cluster 를 차례로 지나 upstream 서비스에 닿는 경로입니다. "
      "색이 붙은 화살표가 Cluster 에서 upstream 으로 넘어가는 지점입니다.",
      "가운데 레인이 Envoy 안의 세 단계입니다. 색이 붙은 화살표는 디스커버리·로드밸런싱·건강 검사가 일하는 자리입니다")

# 2.1 배경 — 레인 띠·구분선·라벨 열 경계
for k in range(n_lanes):
    if k % 2 == 0:
        d.o.append(f'<rect x="{label_col_w}" y="{lane_top(k)}" width="{W - label_col_w}" height="{lane_h}" fill="rgba(245,245,245,0.025)"/>')
    d.line(0, lane_top(k), W, lane_top(k), "rgba(245,245,245,0.12)", 0.8)
d.line(0, legend_top, W, legend_top, "rgba(245,245,245,0.12)", 0.8)
d.line(label_col_w, Y0 + header_h, label_col_w, legend_top, "rgba(245,245,245,0.22)", 1.0)

# 2.2 단계 헤더 칩
for j, (num, lab) in enumerate(steps):
    focal = (j == FOCAL_STEP)
    fill = f"{ACC}38" if focal else "rgba(245,245,245,0.12)"
    d.o.append(f'<rect x="{step_cx(j) - 16}" y="{Y0 + 4}" width="32" height="16" rx="8" fill="{fill}"/>')
    d.t(step_cx(j), Y0 + 16, num, 9, ACC if focal else INK, MONO, "middle", 600)
    d.t(step_cx(j), Y0 + 28, lab, 8, ACC if focal else MUTED, MONO, "middle", 500)

# 2.3 레인 라벨
for k, (name, key) in enumerate(lanes):
    d.t(label_col_w / 2, lane_mid(k) + 4, name, 10, MUTED, MONO, "middle", 600)

nodes = [
    (0, 0, "downstream", "curl · 앱", False),
    (1, 1, "Listener", ":80", False),
    (1, 2, "Route", "/catalog", False),
    (1, 3, "Cluster", "catalog-v1", False),
    (2, 4, "upstream", "catalog-v1 서비스", True),
]

def right(k, j): return node_x(j) + node_w, lane_mid(k)
def hand(k1, j1, k2, j2, c, mk):
    x1, y1 = right(k1, j1)
    if k1 == k2:
        d.path(f"M {x1} {y1} H {node_x(j2) - 2}", c, 1.2 if mk == "acc" else 1.0, m=mk)
        return
    cx = step_cx(j2); down = k2 > k1
    y2 = node_y(k2) - 2 if down else node_y(k2) + node_h + 2
    q = f"Q {cx} {y1} {cx} {y1 + (8 if down else -8)}"
    d.path(f"M {x1} {y1} H {cx - 8} {q} V {y2}", c, 1.2 if mk == "acc" else 1.0, m=mk)

hand(0, 0, 1, 1, MUTED, "ar")
hand(1, 1, 1, 2, MUTED, "ar")
hand(1, 2, 1, 3, MUTED, "ar")
hand(1, 3, 2, 4, ACC, "acc")

lx, ly = node_x(4) - 10, lane_mid(2) + 4
lab = "선택된 인스턴스로"
lw = len(lab) * 12 + 12
d.o.append(f'<rect x="{lx - lw + 4}" y="{ly - 13}" width="{lw}" height="20" rx="3" fill="{PAPER}"/>')
d.t(lx, ly + 2, lab, 12, ACC, KR, "end")

for k, j, title, sub, focal in nodes:
    x, y = node_x(j), node_y(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        d.o.append(f'<rect x="{x + 4}" y="{y + 4}" width="20" height="11" rx="3" fill="{ACC}38"/>')
        d.t(x + 14, y + 12, lanes[k][1], 7, ACC, MONO, "middle", 600)
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.20)" stroke-width="1"/>')
        d.o.append(f'<rect x="{x + 4}" y="{y + 4}" width="20" height="11" rx="3" fill="rgba(245,245,245,0.12)"/>')
        d.t(x + 14, y + 12, lanes[k][1], 7, INK, MONO, "middle", 600)
    d.t(step_cx(j), y + 36, title, 13, INK, KR, "middle", 600)
    d.t(step_cx(j), y + 54, sub, 11, MUTED, MONO, "middle")

ly2 = legend_top + 26
d.t(label_col_w + 4, ly2, "FLOW", 8, SOFT, MONO, "start", 600)
d.path(f"M {label_col_w + 60} {ly2 - 4} H {label_col_w + 92}", MUTED, 1.0, m="ar")
d.t(label_col_w + 100, ly2, "요청 전달", 12, MUTED, KR, "start")
d.path(f"M {label_col_w + 220} {ly2 - 4} H {label_col_w + 252}", ACC, 1.2, m="acc")
d.t(label_col_w + 260, ly2, "Cluster → upstream 전달", 12, ACC, KR, "start")

d.save("03-01.request-path.svg")
print("ok 03-01 request-path")
