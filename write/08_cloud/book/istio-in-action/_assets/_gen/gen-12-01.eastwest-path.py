# 12-01 §6 교차 클러스터 요청이 지나는 길 — 원문 그림 12.13 · 12.15.
# 본문(원문 12.3.6): 클라이언트(webapp)가 원격 클러스터의 워크로드(catalog)로 연결을 걸 때 자기가 겨냥한
#       Envoy 클러스터 정보를 SNI 에 인코딩한다. 동서 게이트웨이는 SNI 에서 그 정보를 읽어 클라이언트가
#       의도한 워크로드로 트래픽을 프록시한다. 이 모든 것이 워크로드 사이의 상호 인증된 연결을 유지한 채
#       일어난다. SNI 클러스터는 방향·subset·포트·FQDN 으로 이루어진 보통의 Envoy 클러스터와 같은데,
#       그 정보를 전부 SNI 에 싣는다는 점만 다르다. 15443 은 멀티 클러스터 mTLS 트래픽 전용 포트다.
# 타입 스펙: type-data-flow — 요청이 칸 사이를 건너간다. 레인 3 · 단계 5 · 노드 5 · 화살표 4,
#           accent 는 SNI 를 읽어 목적지를 정하는 손잡이 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

label_col_w, step_slot_w, right_pad = 136, 164, 24
lanes = [("WEST-CLUSTER", "WST"), ("NETWORK EDGE", "EDG"), ("EAST-CLUSTER", "EST")]
steps = [("01", "CLIENT"), ("02", "SIDECAR"), ("03", "EW GATEWAY"), ("04", "SNI READ"), ("05", "WORKLOAD")]
FOCAL_STEP = 3
n_steps, n_lanes = len(steps), len(lanes)
vb_w = label_col_w + n_steps * step_slot_w + right_pad
header_h, lane_h, legend_h = 40, 92, 152
Y0 = 96
W, H = vb_w, Y0 + header_h + n_lanes * lane_h + legend_h

def lane_top(k): return Y0 + header_h + k * lane_h
def lane_mid(k): return lane_top(k) + lane_h / 2
def step_cx(j): return label_col_w + j * step_slot_w + step_slot_w / 2
node_w, node_h = 148, 68
def node_x(j): return step_cx(j) - node_w / 2
def node_y(k): return lane_top(k) + 12
legend_top = Y0 + header_h + n_lanes * lane_h

d = D(W, H, "ISTIO IN ACTION · 12-01 §6",
      "목적지를 SNI 에 싣고 관문은 그것만 읽는다",
      "webapp 이 원격의 catalog 를 부를 때 겨냥한 Envoy 클러스터를 SNI 에 인코딩하고, 동서 게이트웨이는 "
      "그 값을 읽어 워크로드로 넘긴다. 색이 붙은 손잡이가 VirtualService 없이 목적지가 정해지는 자리다.",
      "게이트웨이는 TLS 를 풀지 않으므로 안을 못 보고 SNI 만 봅니다")

for k in range(n_lanes):
    if k % 2 == 0:
        d.o.append(f'<rect x="{label_col_w}" y="{lane_top(k)}" width="{W - label_col_w}" height="{lane_h}" fill="rgba(245,245,245,0.025)"/>')
    d.line(0, lane_top(k), W, lane_top(k), "rgba(245,245,245,0.12)", 0.8)
d.line(0, legend_top, W, legend_top, "rgba(245,245,245,0.12)", 0.8)
d.line(label_col_w, Y0 + header_h, label_col_w, legend_top, "rgba(245,245,245,0.22)", 1.0)

for j, (num, lab) in enumerate(steps):
    focal = (j == FOCAL_STEP)
    fill = f"{ACC}38" if focal else "rgba(245,245,245,0.12)"
    d.o.append(f'<rect x="{step_cx(j) - 16}" y="{Y0 + 6}" width="32" height="16" rx="8" fill="{fill}"/>')
    d.t(step_cx(j), Y0 + 18, num, 9, ACC if focal else INK, MONO, "middle", 600)
    d.t(step_cx(j), Y0 + 32, lab, 8, ACC if focal else MUTED, MONO, "middle", 500)
for k, (name, key) in enumerate(lanes):
    d.t(label_col_w / 2, lane_mid(k) + 4, name, 9, MUTED, MONO, "middle", 600)

nodes = [
    (0, 0, "webapp", "요청을 낸다", False),
    (0, 1, "사이드카", "SNI 에 인코딩", False),
    (1, 2, "동서 게이트웨이", "15443 · TLS 유지", False),
    (1, 3, "SNI 클러스터", "AUTO_PASSTHROUGH", True),
    (2, 4, "catalog", "요청을 처리한다", False),
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

hand(0, 0, 0, 1, MUTED, "ar")
hand(0, 1, 1, 2, MUTED, "ar")
hand(1, 2, 1, 3, ACC, "acc")
hand(1, 3, 2, 4, MUTED, "ar")

for k, j, title, sub, focal in nodes:
    x, y = node_x(j), node_y(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="6" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.20)" stroke-width="1"/>')
    d.o.append(f'<rect x="{x + 4}" y="{y + 4}" width="20" height="10" rx="3" fill="{ACC + "38" if focal else "rgba(245,245,245,0.12)"}"/>')
    d.t(x + 14, y + 12, lanes[k][1], 6, ACC if focal else INK, MONO, "middle", 600)
    d.t(step_cx(j), y + 36, title, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(step_cx(j), y + 54, sub, 11, MUTED, KR, "middle")

ly1, ly2, ly3 = legend_top + 26, legend_top + 50, legend_top + 74
d.t(24, ly1, "SNI 에 실리는 것 — 방향 · subset · 포트 · FQDN 을 이어 붙인 Envoy 클러스터 이름", 11, SOFT, KR, "start")
d.t(24, ly2, "sni-dnat 라우터 모드가 SNI 클러스터를 자동으로 만들어 둔다 — 표준 모드에서는 만들지 않는다", 11, MUTED, KR, "start")
d.t(24, ly3, "북남 트래픽은 바깥에서 안으로 들어오는 것이고 동서 트래픽은 내부 망끼리 오가는 것이다", 11, SOFT, KR, "start")
d.legend(legend_top + 96, [("VirtualService 없이 목적지가 정해지는 자리", ACC), ("요청이 지나는 순서", MUTED)])
d.save("12-01.eastwest-path.svg")
print("W,H =", W, H, "legend_top =", legend_top)
