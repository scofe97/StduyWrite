# 01-02 §7 — 60초 체크리스트(원서 표 1.1) 열 개 명령이 어느 자원을 확인하는가.
# 타입 스펙: type-dp-security-matrix — 명령 × 자원 격자에서 어느 칸이 덮이는지가 논지다.
#           축약: 스펙 공식의 role_col_w 148 을 120 으로 줄여 다섯 열을 944 폭에 넣고,
#           DK 머리(제목 · 리드)와 겹치지 않게 header_y 를 72 → 112, row_y 기준을 140 → 180 으로 40 내린다.
#           level 은 covered(full) · none 둘만 쓴다. 칸 문구는 표 1.1 의 "확인할 것" 열에서 가져왔다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad = 12, 48
comp_col_w, comp_role_gap = 208, 12
role_col_w, role_col_gap = 120, 16
header_h, row_h, row_stride = 52, 36, 40
DY = 40
ROLES = ["시스템 전반", "CPU", "메모리", "디스크", "네트워크"]
COMPS = ["uptime", "dmesg -T | tail", "vmstat -SM 1", "mpstat -P ALL 1", "pidstat 1",
         "iostat -sxz 1", "free -m", "sar -n DEV 1", "sar -n TCP,ETCP 1", "top"]
CELLS = {   # (row, col): (값, focal)
    (0, 0): ("부하 평균", True),
    (1, 0): ("커널 에러 · OOM", False),
    (2, 1): ("런큐 · 전체 사용", False), (2, 2): ("스와핑", False),
    (3, 1): ("CPU별 균형", False),
    (4, 1): ("프로세스별 사용", False),
    (5, 3): ("IOPS · 대기 · busy", False),
    (6, 2): ("사용 · FS 캐시", False),
    (7, 4): ("장치 I/O", False),
    (8, 4): ("TCP · 재전송", False),
    (9, 0): ("전체 개관", False),
}
n_roles, n_comp = len(ROLES), len(COMPS)
W = left_pad + comp_col_w + comp_role_gap + n_roles * role_col_w + (n_roles - 1) * role_col_gap + right_pad
header_y = 72 + DY
def row_y(k): return 140 + DY + k * row_stride
rows_bottom = row_y(n_comp - 1) + row_h
legend_y = rows_bottom + 20
H = legend_y + 56
def rx(j): return left_pad + comp_col_w + comp_role_gap + j * (role_col_w + role_col_gap)

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §7 · TABLE 1.1",
       "60초 체크리스트가 덮는 자원",
       "원서 표 1.1 의 열 개 명령을 확인할 것에 따라 자원 열에 놓았다. 부하 평균부터 TCP 재전송까지, 60초 안에 시스템 전반 · CPU · 메모리 · 디스크 · 네트워크를 한 번씩 훑는다.",
       "CPU 칸이 많은 것은 전체 · CPU별 · 프로세스별을 따로 보기 때문입니다")

d.box(left_pad, header_y, comp_col_w, header_h, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, header_y + 22, "명령", 13, INK, KR, "middle", 600)
d.t(left_pad + comp_col_w / 2, header_y + 40, "실행 순서", 12, MUTED, KR, "middle")
for j, r in enumerate(ROLES):
    d.box(rx(j), header_y, role_col_w, header_h, "#2A313C", RULE, 0.8, 6)
    d.t(rx(j) + role_col_w / 2, header_y + 32, r, 13, INK, KR, "middle", 600)

for k, c in enumerate(COMPS):
    y = row_y(k)
    d.box(left_pad, y, comp_col_w, row_h, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 12, y + 23, f"{k + 1}", 12, SOFT, MONO, "start")
    d.t(left_pad + 36, y + 23, c, 12, INK, MONO, "start", 600)
    for j in range(n_roles):
        v = CELLS.get((k, j))
        if v and v[1]:
            d.tone(rx(j), y, role_col_w, row_h, ACC, 4, "12", 1.4)
            d.t(rx(j) + role_col_w / 2, y + 23, v[0], 12, ACC, KR, "middle", 600)
        elif v:
            d.box(rx(j), y, role_col_w, row_h, "#22272F", RULE, 0.6, 4)
            d.t(rx(j) + role_col_w / 2, y + 23, v[0], 12, INK, KR, "middle", 600)
        else:
            d.box(rx(j), y, role_col_w, row_h, PAPER, RULE, 0.6, 4)

d.legend(legend_y, [("첫 명령 — 부하가 느는지 주는지", ACC), ("확인하는 자원", INK), ("확인하지 않음", SOFT)])
d.save("01-02.sixty-second-coverage.svg")
