# 09-01 §6·§7 — kmalloc · vmalloc · kvmalloc 을 같은 여섯 축으로 견준다.
# 본문이 요구한 형태: "용도가 다르지 우열은 아닙니다" — 그래서 축을 정해 세 API 를 같은 줄에서 비교한다.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가. 행은 비교 축, 열은 API.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 672
LX, LW = 24, 208
CW, GAP = 232, 12
C0 = LX + LW + 16
HY, RH, RS = 116, 44, 52

COLS = ["kmalloc()", "vmalloc()", "kvmalloc()"]
CX = [C0 + j * (CW + GAP) for j in range(3)]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-01 §6·§7",
       "물리 연속이 필요한가가 가릅니다",
       "세 API 를 같은 여섯 축으로 견준다. 우열이 아니라 용도가 다르다. 물리 연속이 필요하면 kmalloc, 4MB 를 넘는 큰 소프트웨어 버퍼면 vmalloc, 크기가 불확실하면 kvmalloc 이 kmalloc 을 먼저 시도하고 실패 시 vmalloc 으로 폴백한다.",
       "kvmalloc 의 칸은 어느 쪽이 성공했는지에 따라 갈립니다")

d.box(LX, HY, LW, RH, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, HY + 27, "비교 축", 13, SOFT, KR)
for j, name in enumerate(COLS):
    d.box(CX[j], HY, CW, RH, PAPER2, RULE, 0.9)
    d.t(CX[j] + CW / 2, HY + 27, name, 12, INK, MONO, "middle", 600)

ROWS = [
    ("물리 연속", True, [("보장합니다", OK), ("보장하지 않습니다", BAD), ("성공한 쪽에 달림", WARN)]),
    ("가상 연속", False, [("보장합니다", OK), ("보장합니다", OK), ("보장합니다", OK)]),
    ("한 번에 받는 크기", False, [("최대 4MB", WARN), ("훨씬 큽니다", OK), ("4MB 를 넘겨도 받습니다", OK)]),
    ("호출 컨텍스트", False, [("atomic 도 됩니다", OK), ("프로세스만", WARN), ("프로세스만", WARN)]),
    ("정렬", False, [("cacheline 경계", OK), ("page 경계", OK), ("성공한 쪽에 달림", WARN)]),
    ("virt_to_phys()", False, [("됩니다", OK), ("안 됩니다", BAD), ("확인하고 써야 합니다", WARN)]),
]

for i, (axis, focal, cells) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    if focal:
        d.tone(LX, y, LW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + LW / 2, y + 27, axis, 13, ACC if focal else INK, KR)
    for j, (txt, c) in enumerate(cells):
        d.tone(CX[j], y, CW, RH, c, 6, "18", 1.1)
        d.t(CX[j] + CW / 2, y + 27, txt, 13, c, KR)

BOT = HY + RH + 8 + len(ROWS) * RS
d.t(LX, BOT + 30, "kvmalloc 은 무한 retry 를 하지 않아(__GFP_NORETRY|__GFP_NOWARN) 일반 kmalloc 보다 빠를 때도 있습니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 54, "vmalloc 메모리도 물리 프레임은 즉시 할당됩니다 — 유저 공간 malloc 의 demand paging 과 다릅니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 78, "주소가 vmalloc region 에서 왔는지는 is_vmalloc_addr() 나 /proc/vmallocinfo 로 확인합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("이 축에서 유리", OK), ("조건이 붙음", WARN), ("불가", BAD), ("가르는 축", ACC)])
d.save("09-01.alloc-api-matrix.svg")
print("ok 09-01.alloc-api-matrix")
