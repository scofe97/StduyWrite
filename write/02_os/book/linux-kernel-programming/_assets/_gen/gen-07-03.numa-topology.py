# 07-03 §2 — NUMA 에서 "가장 가까운 노드" 가 무엇을 뜻하는가.
# 본문의 AMD 서버 예시 그대로: 2 소켓 × 8 코어 × 2 hyperthread = 32 코어, 4 뱅크 × 8GB = 32GB, 노드 4개.
# 타입 스펙: type-architecture — 시스템 구성요소와 연결. 소켓 경계를 넘는 선이 곧 비용이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 576
SW, SY, SH = 416, 132, 268
SX = [32, 528]
NW, NH, NY = 184, 96, 244

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-03 §2",
       "가까운 노드에서 먼저 가져옵니다",
       "본문의 AMD 서버 예시. 2 소켓 × 8 코어 × 2 hyperthread 로 32 코어, 8GB 뱅크 넷으로 32GB. 커널이 NUMA 노드 4개를 만들고, 스레드가 도는 코어에서 가장 가까운 노드의 free 페이지 프레임부터 씁니다.",
       "노드가 둘 이상이고 멀티코어면 진짜 NUMA 입니다 — 노드 하나면 UMA 입니다")

for k, sx in enumerate(SX):
    d.box(sx, SY, SW, SH, PAPER, RULE, 1.0, 10)
    d.t(sx + 16, SY + 28, f"소켓 {k}", 13, INK, KR, "start", 600)
    d.t(sx + SW - 16, SY + 28, "코어 8 × 2 HT = 16 스레드", 13, SOFT, KR, "end")
    d.line(sx + 16, SY + 44, sx + SW - 16, SY + 44, RULE, 0.8)
    for j in range(2):
        n = k * 2 + j
        nx = sx + 16 + j * 200
        focal = n == 2
        if focal:
            d.tone(nx, NY, NW, NH, ACC, 8, "12", 1.4)
        else:
            d.tone(nx, NY, NW, NH, INFO, 8, "14", 1.1)
        d.t(nx + NW / 2, NY + 32, f"NUMA 노드 {n}", 13, ACC if focal else INFO, KR, "middle", 600)
        d.t(nx + NW / 2, NY + 56, "RAM 뱅크 8GB", 13, MUTED, KR)
        d.t(nx + NW / 2, NY + 78, f"pg_data_t[{n}]", 12, SOFT, MONO)

# CPU #18 은 소켓 1 의 스레드다 — 거기서 난 요청이 어디로 가는가.
CPU_X, CPU_Y = SX[1] + 16, 172
d.tone(CPU_X, CPU_Y, NW, 44, OK, 6, "14", 1.1)
d.t(CPU_X + NW / 2, CPU_Y + 27, "CPU #18 의 스레드", 13, OK, KR)

d.arrow([(CPU_X + NW / 2, CPU_Y + 44), (CPU_X + NW / 2, NY - 6)], ACC, "acc", 1.6)
d.chip(CPU_X + NW / 2 + 108, CPU_Y + 62, "가까운 노드", ACC, 13)

# 먼 노드로 가려면 소켓 경계를 건넌다 — 노드 행 아래로 돌아 들어간다.
FAR_CX = SX[0] + 216 + NW / 2
d.path(f"M {CPU_X} {CPU_Y + 22} L 488 {CPU_Y + 22} L 488 372 L {FAR_CX} 372 L {FAR_CX} {NY + NH + 6}",
       WARN, 1.4, m="warn", dash="5 5")
d.chip(488, 300, "먼 노드", WARN, 13)
d.t(488, SY + SH + 24, "소켓 경계", 12, SOFT, KR)

d.t(24, 452, "가까운 노드에 free 프레임이 없으면 interconnect 너머 다른 노드로 fallback 합니다 — 동작은 하되 느립니다.", 13, MUTED, KR, "start")
d.t(24, 476, "리눅스는 UMA 도 노드 하나짜리 가짜 NUMA 로 취급합니다. 코드 베이스를 갈래내지 않으려는 설계입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("요청이 난 코어", OK), ("가장 가까운 노드", ACC), ("다른 노드", INFO), ("소켓을 건너는 접근", WARN)])
d.save("07-03.numa-topology.svg")
print("ok 07-03.numa-topology")
