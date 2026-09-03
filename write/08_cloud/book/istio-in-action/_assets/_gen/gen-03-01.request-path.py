# 03-01 §2 요청이 Envoy를 지나는 길 — downstream → Listener → Route → Cluster → upstream.
# 본문이 "세 레인", "위 레인 downstream · 가운데 Envoy 세 단계 · 아래 upstream", "색이 붙은 마지막 손잡이가
# 클러스터에서 upstream으로 넘어가는 지점" 이라고 못 박는다. 요청(데이터)이 칸 사이를 건너간다.
# 타입 스펙: type-data-flow — §1 lanes 3 · steps 5 · nodes 5 · arrows 4, §2 공식으로 좌표 산출.
#           축약: 데이터 칩(WB/DB/TB/FL/LS)은 HTTP 요청에 맞는 코드가 없어 생략(스펙이 허용). 글자 크기는
#           스타일 계약(한글 12px 이상)을 따르므로 노드 내부 y 만 스펙보다 아래로 내렸다. 색은 다크 스킨 토큰.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

# §2 공식
label_col_w, step_slot_w, right_pad = 140, 112, 28
lanes = [("DOWNSTREAM", "DWN"), ("ENVOY", "ENV"), ("UPSTREAM", "UPS")]
steps = [("01", "REQUEST"), ("02", "LISTENER"), ("03", "ROUTE"), ("04", "CLUSTER"), ("05", "UPSTREAM")]
FOCAL_STEP = 4
n_steps, n_lanes = len(steps), len(lanes)
vb_w = label_col_w + n_steps * step_slot_w + right_pad        # 728
header_h, lane_h, legend_h = 36, 80, 80
grid_h = header_h + n_lanes * lane_h + legend_h                # 356
Y0 = 88                                                        # 제목 블록(eyebrow·제목·요약) 아래에 격자를 둔다
W, H = vb_w, Y0 + grid_h                                       # 728 × 444

def lane_top(k): return Y0 + header_h + k * lane_h
def lane_mid(k): return lane_top(k) + lane_h / 2
def step_cx(j): return label_col_w + j * step_slot_w + step_slot_w / 2
node_w, node_h = 100, 64
def node_x(j): return step_cx(j) - node_w / 2
def node_y(k): return lane_top(k) + 8
legend_top = Y0 + header_h + n_lanes * lane_h

d = D(W, H, "ISTIO IN ACTION · 03-01 §2",
      "요청은 downstream에서 upstream으로 흐른다",
      "요청이 downstream 에서 Envoy 의 Listener·Route·Cluster 를 차례로 지나 upstream 서비스에 닿는 경로. "
      "색이 붙은 손잡이가 Cluster 에서 upstream 으로 넘어가는 지점이다.",
      "가운데 레인이 Envoy 안의 세 단계. 색이 붙은 손잡이를 디스커버리·로드밸런싱·건강 검사의 자리로 읽는다")

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
    d.t(label_col_w / 2, lane_mid(k) + 4, name, 9, MUTED, MONO, "middle", 600)

# 노드 정의 — (lane, step, title, sub, focal)
nodes = [
    (0, 0, "downstream", "curl · 앱", False),
    (1, 1, "Listener", ":15001", False),
    (1, 2, "Route", 'prefix "/"', False),
    (1, 3, "Cluster", "httpbin_service", False),
    (2, 4, "upstream", "httpbin:8000", True),
]

# 3. 화살표 — 노드보다 먼저. 오른쪽으로 나가 corridor 에서 꺾어 위/아래로 들어간다
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
# 초점 화살표 라벨 — 세로 구간 옆, 종이색 마스크 위
lx, ly = node_x(4) - 8, lane_mid(2) + 4     # upstream 노드 왼쪽, 빈 칸(UPS·step 3) 안
lab = "선택된 인스턴스로"
lw = len(lab) * 12 + 8
d.o.append(f'<rect x="{lx - lw + 4}" y="{ly - 12}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
d.t(lx, ly + 2, lab, 12, ACC, KR, "end")

# 노드
for k, j, title, sub, focal in nodes:
    x, y = node_x(j), node_y(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        d.o.append(f'<rect x="{x + 4}" y="{y + 4}" width="18" height="10" rx="3" fill="{ACC}38"/>')
        d.t(x + 13, y + 12, lanes[k][1], 6, ACC, MONO, "middle", 600)
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.20)" stroke-width="1"/>')
        d.o.append(f'<rect x="{x + 4}" y="{y + 4}" width="18" height="10" rx="3" fill="rgba(245,245,245,0.12)"/>')
        d.t(x + 13, y + 12, lanes[k][1], 6, INK, MONO, "middle", 600)
    d.t(step_cx(j), y + 34, title, 12, INK, KR, "middle", 600)
    d.t(step_cx(j), y + 52, sub, 11, MUTED, MONO, "middle")

# 9. 범례 — STEPS · FLOW 두 줄 (데이터 칩이 없어 DATA TYPE 줄은 없다)
ly1, ly2 = legend_top + 22, legend_top + 52
d.t(label_col_w + 4, ly1, "STEPS", 8, SOFT, MONO, "start", 600)
x = label_col_w + 60
for j, (num, lab) in enumerate(steps):
    focal = (j == FOCAL_STEP)
    d.o.append(f'<rect x="{x}" y="{ly1 - 11}" width="24" height="14" rx="7" fill="{ACC + "38" if focal else "rgba(245,245,245,0.12)"}"/>')
    d.t(x + 12, ly1, num, 8, ACC if focal else INK, MONO, "middle", 600)
    d.t(x + 30, ly1, lab, 8, ACC if focal else MUTED, MONO, "start")
    x += 108
d.t(label_col_w + 4, ly2, "FLOW", 8, SOFT, MONO, "start", 600)
d.path(f"M {label_col_w + 60} {ly2 - 4} H {label_col_w + 92}", MUTED, 1.0, m="ar")
d.t(label_col_w + 100, ly2, "요청 전달", 12, MUTED, KR, "start")
d.path(f"M {label_col_w + 200} {ly2 - 4} H {label_col_w + 232}", ACC, 1.2, m="acc")
d.t(label_col_w + 240, ly2, "Cluster → upstream 손잡이", 12, ACC, KR, "start")

d.save("03-01.request-path.svg")
print("W,H =", W, H, " legend_top =", legend_top)
