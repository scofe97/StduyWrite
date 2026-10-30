# 06-04 §2 — 복제 토폴로지 3종 비교와 all-to-all 메시지 추월(인과 순서 역전).
# 사실 출처: 06-04 §2(L43~L56), DDIA 2판 6장 Figure 6-6 "Replication topologies" 및 Figure 6-7 "With all-to-all replication, writes may arrive in the wrong order"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
H = 600
LEG = H - 46

d = D(W, H, "06-04 · REPLICATION TOPOLOGY", "복제 토폴로지 비교와 all-to-all 메시지 추월",
      "원형·성형·전체 연결 토폴로지의 단일 실패점과, 전체 연결에서 발생하는 메시지 추월 및 인과 역전.",
      "통신 경로 선택 · 단일 실패점 · 링크 속도 차 · version vector")

# 1. 상단: 세 토폴로지 비교
Y_TOP = 104
H_TOP = 196
CW = 264
GAP = 20

# 1-A. 원형 (circular) — 직교 링
X_CIR = 24
d.box(X_CIR, Y_TOP, CW, H_TOP, PAPER2, RULE, 0.9)
d.t(X_CIR + CW / 2, Y_TOP + 24, "원형 토폴로지 (circular)", 13, INK, KR, "middle", 600)

x_l = X_CIR + 54
x_r = X_CIR + CW - 54
y_u = Y_TOP + 52
y_d = Y_TOP + 116

# 4개 노드 박스
d.box(x_l - 18, y_u - 14, 36, 28, PAPER, INFO, 1.0, r=4)
d.t(x_l, y_u + 5, "N1", 12, INK, MONO, "middle", 600)

d.box(x_r - 18, y_u - 14, 36, 28, PAPER, INFO, 1.0, r=4)
d.t(x_r, y_u + 5, "N2", 12, INK, MONO, "middle", 600)

d.box(x_r - 18, y_d - 14, 36, 28, PAPER, INFO, 1.0, r=4)
d.t(x_r, y_d + 5, "N3", 12, INK, MONO, "middle", 600)

d.box(x_l - 18, y_d - 14, 36, 28, PAPER, INFO, 1.0, r=4)
d.t(x_l, y_d + 5, "N4", 12, INK, MONO, "middle", 600)

# 시계 방향 직교 화살표
d.arrow([(x_l + 20, y_u), (x_r - 20, y_u)], INFO, "info", 1.2)
d.arrow([(x_r, y_u + 16), (x_r, y_d - 16)], INFO, "info", 1.2)
d.arrow([(x_r - 20, y_d), (x_l + 20, y_d)], INFO, "info", 1.2)
d.arrow([(x_l, y_d - 16), (x_l, y_u + 16)], INFO, "info", 1.2)

d.tone(X_CIR + 12, Y_TOP + 146, CW - 24, 36, WARN, 4, "12", 1.0)
d.t(X_CIR + CW / 2, Y_TOP + 169, "단일 노드 장애 시 복제 중단", 12, WARN, KR, "middle")


# 1-B. 성형 (star) — 직교 트리
X_STR = X_CIR + CW + GAP
d.box(X_STR, Y_TOP, CW, H_TOP, PAPER2, RULE, 0.9)
d.t(X_STR + CW / 2, Y_TOP + 24, "성형 토폴로지 (star)", 13, INK, KR, "middle", 600)

cx_s = X_STR + CW / 2
cy_s = Y_TOP + 84

# 중앙 루트 노드
d.tone(cx_s - 22, cy_s - 14, 44, 28, ACC, 4, "22", 1.2)
d.t(cx_s, cy_s + 5, "Root", 12, ACC, MONO, "middle", 600)

# 좌우 리프 노드
lx_l = X_STR + 40
lx_r = X_STR + CW - 40
ly_u = Y_TOP + 46
ly_d = Y_TOP + 122

d.box(lx_l - 16, ly_u - 14, 32, 28, PAPER, INFO, 1.0, r=4)
d.t(lx_l, ly_u + 5, "L1", 12, INK, MONO, "middle", 600)

d.box(lx_r - 16, ly_u - 14, 32, 28, PAPER, INFO, 1.0, r=4)
d.t(lx_r, ly_u + 5, "L2", 12, INK, MONO, "middle", 600)

d.box(lx_l - 16, ly_d - 14, 32, 28, PAPER, INFO, 1.0, r=4)
d.t(lx_l, ly_d + 5, "L3", 12, INK, MONO, "middle", 600)

d.box(lx_r - 16, ly_d - 14, 32, 28, PAPER, INFO, 1.0, r=4)
d.t(lx_r, ly_d + 5, "L4", 12, INK, MONO, "middle", 600)

# Root <-> 리프 직교 연결선
d.line(cx_s - 22, cy_s - 6, lx_l + 24, cy_s - 6, MUTED, 1.0)
d.line(lx_l + 24, cy_s - 6, lx_l + 24, ly_u + 14, MUTED, 1.0)

d.line(cx_s + 22, cy_s - 6, lx_r - 24, cy_s - 6, MUTED, 1.0)
d.line(lx_r - 24, cy_s - 6, lx_r - 24, ly_u + 14, MUTED, 1.0)

d.line(cx_s - 22, cy_s + 6, lx_l + 24, cy_s + 6, MUTED, 1.0)
d.line(lx_l + 24, cy_s + 6, lx_l + 24, ly_d - 14, MUTED, 1.0)

d.line(cx_s + 22, cy_s + 6, lx_r - 24, cy_s + 6, MUTED, 1.0)
d.line(lx_r - 24, cy_s + 6, lx_r - 24, ly_d - 14, MUTED, 1.0)

d.tone(X_STR + 12, Y_TOP + 146, CW - 24, 36, WARN, 4, "12", 1.0)
d.t(X_STR + CW / 2, Y_TOP + 169, "루트 장애 시 복제 전체 마비", 12, WARN, KR, "middle")


# 1-C. 전체 연결 (all-to-all)
X_ALL = X_STR + CW + GAP
d.box(X_ALL, Y_TOP, CW, H_TOP, PAPER2, OK, 1.1)
d.t(X_ALL + CW / 2, Y_TOP + 24, "전체 연결 토폴로지 (all-to-all)", 13, OK, KR, "middle", 600)

ax_l = X_ALL + 54
ax_r = X_ALL + CW - 54

d.box(ax_l - 18, y_u - 14, 36, 28, PAPER, OK, 1.0, r=4)
d.t(ax_l, y_u + 5, "N1", 12, INK, MONO, "middle", 600)

d.box(ax_r - 18, y_u - 14, 36, 28, PAPER, OK, 1.0, r=4)
d.t(ax_r, y_u + 5, "N2", 12, INK, MONO, "middle", 600)

d.box(ax_r - 18, y_d - 14, 36, 28, PAPER, OK, 1.0, r=4)
d.t(ax_r, y_d + 5, "N3", 12, INK, MONO, "middle", 600)

d.box(ax_l - 18, y_d - 14, 36, 28, PAPER, OK, 1.0, r=4)
d.t(ax_l, y_d + 5, "N4", 12, INK, MONO, "middle", 600)

# 외곽 직교 연결선
d.line(ax_l + 18, y_u, ax_r - 18, y_u, MUTED, 0.9, dash="3 3")
d.line(ax_r, y_u + 14, ax_r, y_d - 14, MUTED, 0.9, dash="3 3")
d.line(ax_r - 18, y_d, ax_l + 18, y_d, MUTED, 0.9, dash="3 3")
d.line(ax_l, y_d - 14, ax_l, y_u + 14, MUTED, 0.9, dash="3 3")

# 내부 교차 직교 연결선 (중앙 축 경유)
cy_m = (y_u + y_d) / 2
d.line(ax_l + 8, y_u + 14, ax_l + 8, cy_m - 4, MUTED, 0.8, dash="2 2")
d.line(ax_l + 8, cy_m - 4, ax_r - 8, cy_m - 4, MUTED, 0.8, dash="2 2")
d.line(ax_r - 8, cy_m - 4, ax_r - 8, y_d - 14, MUTED, 0.8, dash="2 2")

d.line(ax_r - 8, y_u + 14, ax_r - 8, cy_m + 4, MUTED, 0.8, dash="2 2")
d.line(ax_r - 8, cy_m + 4, ax_l + 8, cy_m + 4, MUTED, 0.8, dash="2 2")
d.line(ax_l + 8, cy_m + 4, ax_l + 8, y_d - 14, MUTED, 0.8, dash="2 2")

d.tone(X_ALL + 12, Y_TOP + 146, CW - 24, 36, OK, 4, "14", 1.0)
d.t(X_ALL + CW / 2, Y_TOP + 169, "단일 실패점 없음 · 높은 내고장성", 12, OK, KR, "middle")


# 2. 하단: all-to-all에서의 메시지 추월과 인과 순서 역전
Y_BOT = 316
H_BOT = 214
d.box(24, Y_BOT, W - 48, H_BOT, PAPER2, RULE, 0.9)
d.t(40, Y_BOT + 24, "all-to-all 위험: 네트워크 지연 차이로 인한 메시지 추월과 인과 역전", 12, SOFT, KR, "start", 600)

Y_ND = Y_BOT + 40
H_ND = 96

# 리더 1
X_L1 = 40
W_L1 = 230
d.box(X_L1, Y_ND, W_L1, H_ND, PAPER, INFO, 1.1)
d.chip(X_L1 + 44, Y_ND + 20, "리더 1", INFO, 12)
d.t(X_L1 + 144, Y_ND + 22, "클라이언트 A 쓰기", 12, INK, KR, "middle", 600)
d.tone(X_L1 + 12, Y_ND + 38, W_L1 - 24, 46, INFO, 4, "14", 0.9)
d.t(X_L1 + W_L1 / 2, Y_ND + 58, "insert x = 1", 12, INFO, MONO, "middle", 600)
d.t(X_L1 + W_L1 / 2, Y_ND + 75, "행 삽입 (인과 선행 쓰기)", 12, MUTED, KR, "middle")

# 리더 3
X_L3 = 325
W_L3 = 230
d.box(X_L3, Y_ND, W_L3, H_ND, PAPER, ACC, 1.1)
d.chip(X_L3 + 44, Y_ND + 20, "리더 3", ACC, 12)
d.t(X_L3 + 144, Y_ND + 22, "클라이언트 B 갱신", 12, INK, KR, "middle", 600)
d.tone(X_L3 + 12, Y_ND + 38, W_L3 - 24, 46, ACC, 4, "14", 0.9)
d.t(X_L3 + W_L3 / 2, Y_ND + 58, "update x = x + 1", 12, ACC, MONO, "middle", 600)
d.t(X_L3 + W_L3 / 2, Y_ND + 75, "같은 행 갱신 (인과 후행 쓰기)", 12, MUTED, KR, "middle")

# 리더 2
X_L2 = 610
W_L2 = 230
d.box(X_L2, Y_ND, W_L2, H_ND, PAPER, WARN, 1.1)
d.chip(X_L2 + 44, Y_ND + 20, "리더 2", WARN, 12)
d.t(X_L2 + 144, Y_ND + 22, "도착 순서 역전", 12, WARN, KR, "middle", 600)
d.tone(X_L2 + 12, Y_ND + 38, W_L2 - 24, 46, WARN, 4, "14", 0.9)
d.t(X_L2 + W_L2 / 2, Y_ND + 58, "1 · update 먼저 수신", 12, WARN, KR, "middle", 600)
d.t(X_L2 + W_L2 / 2, Y_ND + 75, "없는 행에 대한 갱신 · insert 는 나중", 12, MUTED, KR, "middle")

# 화살표 1: 리더 1 -> 리더 3 (정상 복제)
d.arrow([(X_L1 + W_L1, Y_ND + 61), (X_L3, Y_ND + 61)], INFO, "info", 1.3)

# 화살표 2: 리더 3 -> 리더 2 (초고속 링크)
d.arrow([(X_L3 + W_L3, Y_ND + 52), (X_L2, Y_ND + 52)], ACC, "acc", 1.4)
d.t((X_L3 + W_L3 + X_L2) / 2, Y_ND + 42, "빠른 링크", 12, ACC, KR, "middle")

# 화살표 3: 리더 1 -> 리더 2 (지연 링크, 하단 우회 직교 화살표)
y_bypass = Y_BOT + 150
d.arrow([(X_L1 + W_L1 / 2, Y_ND + H_ND), (X_L1 + W_L1 / 2, y_bypass), (X_L2 + W_L2 / 2, y_bypass), (X_L2 + W_L2 / 2, Y_ND + H_ND)], WARN, "warn", 1.3, dash="4 3")
d.t((X_L1 + X_L2 + W_L2) / 2, y_bypass + 14, "느린 링크 (insert 늦게 도착)", 12, WARN, KR, "middle")

# 인과 보정 결론 배너
d.tone(40, Y_BOT + 172, W - 80, 28, OK, 4, "12", 0.9)
d.t(W / 2, Y_BOT + 190, "해결: 시계를 믿을 수 없어 타임스탬프로는 부족 · version vector", 12, OK, KR, "middle", 600)

d.legend(LEG, [("선행 쓰기 (insert)", INFO), ("후행 갱신 (update)", ACC), ("내고장성·해결", OK), ("단일 실패점·인과 역전", WARN)])
d.save("06-04.replication-topology.svg")
