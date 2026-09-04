# 04-01 §4 세 TLS 모드에서 인증서와 종료 지점이 어디에 있는가.
# 본문: "세 모드를 네 질문으로 가른 행렬 — 게이트웨이가 인증서를 갖는가, 클라이언트 인증서를 검증하는가,
# TLS 가 어디서 끝나는가, VirtualService 는 무엇으로 매칭하는가. 색이 붙은 칸이 PASSTHROUGH 의 종료 지점."
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가의 격자. §1 roles 3 × components 5, §2 공식으로 좌표.
#           축약: 역할 배너 색은 다크 스킨 토큰(paper-2)으로, 글자 크기는 스타일 계약(한글 12px)으로 올렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad, comp_col_w, comp_role_gap, role_col_w, role_col_gap = 12, 48, 208, 12, 148, 16
header_h, row_h, row_stride = 52, 36, 40
roles = [("SIMPLE", "4.3.1"), ("MUTUAL", "4.3.3"), ("PASSTHROUGH", "4.4.2")]
# credentialName 힌트는 208px 라벨 칸에 이름과 겹쳐 뺐다 — 본문이 설명한다
comps = [("게이트웨이의 인증서", ""), ("클라이언트 인증서 검증", ""), ("TLS 종료 지점", ""), ("VirtualService 매칭", ""), ("Gateway protocol", "")]
n_roles, n_comps = len(roles), len(comps)
Y0 = 24
vb_w = left_pad + comp_col_w + comp_role_gap + n_roles * role_col_w + (n_roles - 1) * role_col_gap + right_pad   # 756
header_y = Y0 + 72
def row_y(k): return Y0 + 140 + k * row_stride
rows_bottom = row_y(n_comps - 1) + row_h
legend_top = rows_bottom + 20
W, H = vb_w, legend_top + 44
def role_x(j): return left_pad + comp_col_w + comp_role_gap + j * (role_col_w + role_col_gap)
def role_cx(j): return role_x(j) + role_col_w / 2

d = D(W, H, "ISTIO IN ACTION · 04-01 §4",
      "세 TLS 모드 — 인증서와 종료 지점은 어디에 있는가",
      "SIMPLE 과 MUTUAL 은 게이트웨이가 인증서를 갖고 TLS 를 종료한다. MUTUAL 은 ca.crt 로 클라이언트까지 검증한다. "
      "PASSTHROUGH 는 게이트웨이에 인증서가 없고 SNI 만 읽어 백엔드로 넘기며 백엔드가 종료한다.")

# 2.2 헤더행
d.box(left_pad, header_y, comp_col_w, header_h, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, header_y + 24, "질문", 12, INK, KR, "middle", 600)
d.t(left_pad + comp_col_w / 2, header_y + 40, "vs. tls.mode", 9, MUTED, MONO)
for j, (name, sec) in enumerate(roles):
    d.box(role_x(j), header_y, role_col_w, header_h, PAPER2, RULE, 0.8, 6)
    d.t(role_cx(j), header_y + 22, name, 12, INK, MONO, "middle", 600)
    d.t(role_cx(j), header_y + 40, f"원문 {sec}", 11, MUTED, MONO)

# 2.4 셀 스타일 (다크)
# 본문이 이 도식에 요구하는 구분은 "색이 붙은 칸" 하나뿐이다. 나머지를 넷으로 칠하면
# 흰색 투명도 0.10 · 0.06 · 0.02 가 14x12px 범례 스와치에서 서로 구분되지 않아
# 계약이 안티패턴으로 적은 "상태 구분이 죽는" 상태가 된다. 값이 있는가로만 가른다.
STYLE = {
    "full": ("rgba(245,245,245,0.08)", RULE, INK, 600),
    "none": ("rgba(245,245,245,0.02)", RULE, SOFT, 400),
}
cells = {
    (0, 0): ("tls.key · tls.crt", "full", None), (0, 1): ("tls.key · tls.crt", "full", "+ ca.crt"), (0, 2): ("없음", "none", None),
    (1, 0): ("안 함", "none", None), (1, 1): ("함", "full", None), (1, 2): ("원문 언급 없음", "none", None),
    (2, 0): ("게이트웨이", "full", None), (2, 1): ("게이트웨이", "full", None), (2, 2): ("백엔드", "focal", "SNI만 읽음"),
    (3, 0): ("http · Host", "full", None), (3, 1): ("http · Host", "full", None), (3, 2): ("tls · sniHosts", "full", None),
    (4, 0): ("HTTPS", "full", None), (4, 1): ("HTTPS", "full", None), (4, 2): ("TLS", "full", None),
}
for k, (name, hint) in enumerate(comps):
    y = row_y(k)
    d.box(left_pad, y, comp_col_w, row_h, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 12, y + 22, name, 12, INK, KR, "start", 600)
    if hint: d.t(left_pad + comp_col_w - 12, y + 22, hint, 9, MUTED, MONO, "end")
    for j in range(n_roles):
        val, lv, sub = cells[(k, j)]
        x = role_x(j)
        if lv == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{role_col_w}" height="{row_h}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(role_cx(j), y + 15, val, 12, ACC, KR, "middle", 600)
            d.t(role_cx(j), y + 30, sub, 12, ACC, KR, "middle", 400, "0.85")
            continue
        fill, stroke, color, weight = STYLE[lv]
        d.o.append(f'<rect x="{x}" y="{y}" width="{role_col_w}" height="{row_h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="0.6"/>')
        latin = not any('가' <= ch <= '힣' for ch in val)
        if sub:
            d.t(role_cx(j), y + 15, val, 10 if latin else 12, color, MONO if latin else KR, "middle", weight)
            d.t(role_cx(j), y + 29, sub, 10, color, MONO)
        else:
            d.t(role_cx(j), y + 22, val, 10 if latin else 12, color, MONO if latin else KR, "middle", weight)

# 2.5 범례 — 실제로 쓴 스타일만
d.line(left_pad, legend_top, W - right_pad, legend_top, RULE, 0.8)
d.t(left_pad, legend_top + 22, "LEGEND", 8, SOFT, MONO, "start")
x = left_pad + 88
for lab, fill, stroke in [("이 장의 논점", f"{ACC}1F", ACC), ("없거나 원문에 언급 없음", STYLE["none"][0], SOFT)]:
    d.o.append(f'<rect x="{x}" y="{legend_top + 12}" width="14" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.1"/>')
    d.t(x + 22, legend_top + 22, lab, 12, MUTED, KR, "start")
    x += 44 + len(lab) * 12
d.save("04-01.tls-modes.svg")
print("W,H =", W, H)
