# 06-01 §3 네 시나리오에서 10회 호출이 간 곳 — 원문 6.3.1·6.3.2 의 출력 네 묶음을 센 값.
# 본문: "행이 조건, 열이 두 백엔드. 색이 붙은 칸이 이 절의 논점 — 이상치 감지를 더한 뒤에야 같은 영역으로 모인다."
# 타입 스펙: type-dp-security-matrix — 어느 조합에서 어디로 가는가의 격자. §2 공식으로 좌표 산출.
#           축약: 권한 격자가 아니라 응답 수 격자라 level 어휘(full/rw/read/none)를 분포의 세기로 재사용했다.
#           역할 배너 색과 셀 색은 다크 스킨 토큰으로 바꿨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad, comp_col_w, comp_role_gap, role_col_w, role_col_gap = 12, 48, 260, 12, 240, 16
header_h, row_h, row_stride = 52, 36, 40
roles = [("simple-backend-1", "us-west1-a · simple-web 과 같은 영역"), ("simple-backend-2", "us-west1-b · 이웃 영역")]
comps = [("위치 라벨만 붙임", "6.3.1"), ("+ 이상치 감지", "6.3.1"), ("+ 로컬이 100% 실패", "6.3.1"), ("+ 가중 분배 70/30", "6.3.2")]
n_roles, n_comps = len(roles), len(comps)
Y0 = 40
vb_w = left_pad + comp_col_w + comp_role_gap + n_roles * role_col_w + (n_roles - 1) * role_col_gap + right_pad
header_y = Y0 + 72
def row_y(k): return Y0 + 140 + k * row_stride
rows_bottom = row_y(n_comps - 1) + row_h
legend_top = rows_bottom + 20
W, H = vb_w, legend_top + 48
def role_x(j): return left_pad + comp_col_w + comp_role_gap + j * (role_col_w + role_col_gap)
def role_cx(j): return role_x(j) + role_col_w / 2

d = D(W, H, "ISTIO IN ACTION · 06-01 §3",
      "네 조건에서 10회 호출이 간 곳",
      "같은 호출 열 번을 네 조건에서 반복한 결과. 위치 라벨만으로는 두 영역에 갈리고, 이상치 감지를 더해야 같은 영역으로 모인다. "
      "로컬이 100% 실패하면 이웃 영역으로 전부 넘어가고, 가중 분배를 주면 70/30 에 가깝게 나뉜다.")

d.box(left_pad, header_y, comp_col_w, header_h, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, header_y + 24, "조건", 12, INK, KR, "middle", 600)
d.t(left_pad + comp_col_w / 2, header_y + 40, "vs. 응답한 백엔드", 9, MUTED, MONO)
for j, (name, sub) in enumerate(roles):
    d.box(role_x(j), header_y, role_col_w, header_h, PAPER2, RULE, 0.8, 6)
    d.t(role_cx(j), header_y + 22, name, 12, INK, MONO, "middle", 600)
    d.t(role_cx(j), header_y + 40, sub, 11, MUTED, KR)

# 범례 색과 칸 fill 을 같은 토큰으로 묶는다 — 값은 맞는데 색이 값을 배신하는 일을 막는다
STYLE = {"full": (f"{MUTED}1F", INK, 600), "rw": (f"{MUTED}1F", INK, 400),
         "read": (f"{SOFT}1F", MUTED, 400), "none": (f"{SOFT}1F", SOFT, 400)}
cells = {
    (0, 0): ("5회", "rw", None), (0, 1): ("5회", "rw", None),
    (1, 0): ("10회", "focal", "이상치 감지가 있어야 모인다"), (1, 1): ("0회", "none", None),
    (2, 0): ("0회", "none", None), (2, 1): ("10회", "full", "이웃 영역으로 넘침"),
    (3, 0): ("8회", "full", None), (3, 1): ("2회", "read", None),
}
for k, (name, hint) in enumerate(comps):
    y = row_y(k)
    d.box(left_pad, y, comp_col_w, row_h, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 12, y + 22, name, 12, INK, KR, "start", 600)
    d.t(left_pad + comp_col_w - 12, y + 22, f"원문 {hint}", 9, MUTED, MONO, "end")
    for j in range(n_roles):
        val, lv, sub = cells[(k, j)]
        x = role_x(j)
        if lv == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{role_col_w}" height="{row_h}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(role_cx(j), y + 16, val, 12, ACC, MONO, "middle", 600)
            d.t(role_cx(j), y + 30, sub, 11, ACC, KR, "middle", 400, "0.85")
            continue
        fill, color, weight = STYLE[lv]
        d.o.append(f'<rect x="{x}" y="{y}" width="{role_col_w}" height="{row_h}" rx="4" fill="{fill}" stroke="{RULE}" stroke-width="0.6"/>')
        if sub:
            d.t(role_cx(j), y + 16, val, 12, color, MONO, "middle", weight)
            d.t(role_cx(j), y + 30, sub, 11, MUTED, KR)
        else:
            d.t(role_cx(j), y + 22, val, 12, color, MONO, "middle", weight)
d.legend(legend_top, [("요청이 간 쪽", MUTED), ("안 갔거나 적게 간 쪽", SOFT), ("이 절의 논점", ACC)])
d.save("06-01.locality-matrix.svg")
