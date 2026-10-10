# 타입 스펙: type-dp-security-matrix — 행(알고리즘 8종) × 열(혼잡 신호 · 증가 규칙 · 감소 규칙) 격자.
# 사실 출처: ch16.txt 2140~2850행 — Reno, HSTCP, BIC, CUBIC, Vegas, FAST, Westwood, Compound 의 혼잡 신호 및 증감 규칙.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad = 12, 36
comp_col_w, comp_role_gap = 148, 12
role_col_w, role_col_gap = 236, 12
header_h, row_h, row_stride = 52, 36, 40
roles = [("혼잡 신호", "감지 기준"), ("증가 규칙", "혼잡 회피 중 창 확대"), ("감소 규칙", "혼잡 감지 시 창 축소")]
comps = ["표준 (Reno)", "HSTCP", "BIC", "CUBIC", "Vegas", "FAST", "Westwood", "Compound"]

cells = {
    (0, 0): ("손실 (중복 ACK 3개 · RTO)", INFO),
    (0, 1): ("AIMD (+1 SMSS / RTT)", OK),
    (0, 2): ("반감 (cwnd × 0.5)", WARN),

    (1, 0): ("손실 (큰 창 p ≤ 10⁻³)", INFO),
    (1, 1): ("동적 가산 (+a(w) / cwnd)", OK),
    (1, 2): ("동적 감쇠 (cwnd × (1 - b(w)))", WARN),

    (2, 0): ("손실 (Wmax 기억)", INFO),
    (2, 1): ("이진 탐색 + 가산 상한 Smax", OK),
    (2, 2): ("승수 감소 (cwnd × 0.8)", WARN),

    (3, 0): ("손실 (손실 사건 · Wmax 기억)", ACC),
    (3, 1): ("시간 삼차 함수 C(t - K)³", ACC),
    (3, 2): ("승수 감소 (cwnd × 0.7)", ACC),

    (4, 0): ("지연 (Diff = Exp - Act)", INFO),
    (4, 1): ("Diff < α 이면 +1 SMSS", OK),
    (4, 2): ("Diff > β 이면 -1 SMSS", WARN),

    (5, 0): ("지연 (기대·실측 처리량 차)", INFO),
    (5, 1): ("2 RTT 마다 속도 갱신", OK),
    (5, 2): ("지연 비례 점진 감속", WARN),

    (6, 0): ("손실 + ACK 속도(ERE)", INFO),
    (6, 1): ("AIMD / Agile Probing", OK),
    (6, 2): ("ssthresh = (ERE × baseRTT)", WARN),

    (7, 0): ("손실(cwnd) + 지연(dwnd)", INFO),
    (7, 1): ("이중 창 (cwnd + dwnd)", OK),
    (7, 2): ("Reno 반감 + dwnd 감쇠", WARN),
}
FOCAL_ROW = 3

n_roles, n_comp = len(roles), len(comps)
W = left_pad + comp_col_w + comp_role_gap + n_roles * role_col_w + (n_roles - 1) * role_col_gap + right_pad
header_y = 104
def row_y(k): return header_y + 64 + k * row_stride
rows_bottom = row_y(n_comp - 1) + row_h
legend_y = rows_bottom + 20
H = legend_y + 44
def role_x(j): return left_pad + comp_col_w + comp_role_gap + j * (role_col_w + role_col_gap)

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-04",
      "혼잡 제어 알고리즘 8종 비교 — 신호와 증감 규칙",
      "표준 Reno부터 고속 망 대안과 지연 기반 알고리즘까지 혼잡 신호의 종류, 창 증가 방식, 감소 규칙을 대조 행렬로 정리한다. CUBIC은 현행 Linux 기본값으로 시간 삼차 함수를 쓴다.",
      "신호가 손실에서 지연·대역폭으로 넓어지고 창 변화가 상수에 묶이지 않습니다")

# 헤더 행
d.box(left_pad, header_y, comp_col_w, header_h, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, header_y + 22, "알고리즘", 13, INK, KR, "middle", 600)
d.t(left_pad + comp_col_w / 2, header_y + 40, "계열 분류", 11, MUTED, KR)
for j, (name, code) in enumerate(roles):
    x = role_x(j)
    d.box(x, header_y, role_col_w, header_h, "#2A3140", RULE, 0.8, 6)
    d.t(x + role_col_w / 2, header_y + 22, name, 13, INK, KR, "middle", 600)
    d.t(x + role_col_w / 2, header_y + 40, code, 11, MUTED, KR)

# 데이터 행
for k, comp in enumerate(comps):
    y = row_y(k)
    is_focal = (k == FOCAL_ROW)
    bg_comp = f"{ACC}15" if is_focal else PAPER2
    border_comp = ACC if is_focal else RULE
    d.box(left_pad, y, comp_col_w, row_h, bg_comp, border_comp, 1.2 if is_focal else 0.8, 4)
    d.t(left_pad + 12, y + 23, comp, 13, ACC if is_focal else INK, KR, "start", 600)
    for j in range(n_roles):
        x = role_x(j); val, col = cells[(k, j)]
        if is_focal:
            d.tone(x, y, role_col_w, row_h, ACC, 4, "15", 1.2)
            d.t(x + 10, y + 23, val, 11, ACC, MONO if any(ch in val for ch in "=+-*²³") else KR, "start", 600)
        else:
            d.tone(x, y, role_col_w, row_h, col, 4, "0C", 0.7)
            d.t(x + 10, y + 23, val, 11, col, MONO if any(ch in val for ch in "=+-*²³") else KR, "start", 400)

d.legend(legend_y, [("현행 표준 초점 (CUBIC)", ACC), ("손실 / 지연 신호", INFO), ("창 증가 규칙", OK), ("창 감소 규칙", WARN)])
d.save("16-04.chapter-overview.svg")
