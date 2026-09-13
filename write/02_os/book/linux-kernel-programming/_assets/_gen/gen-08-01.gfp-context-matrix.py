# 08-01 §6 — 어느 컨텍스트에서 어느 GFP 플래그가 되고 안 되는가.
# 본문이 요구한 형태: "황금률 — sleep 안전하면 GFP_KERNEL, sleep 불가능하면 GFP_ATOMIC" + LDV 규칙 둘.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가. 행은 컨텍스트, 열은 플래그.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 612
LX, LW = 24, 268
CW, GAP = 180, 12
C0 = LX + LW + 16
HY, RH, RS = 116, 44, 52

COLS = ["GFP_KERNEL", "GFP_ATOMIC", "GFP_NOIO"]
CX = [C0 + j * (CW + GAP) for j in range(3)]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-01 §6",
       "sleep 해도 되는 자리인지가 전부입니다",
       "GFP 플래그는 모든 할당 API 의 첫 인자다. 고르는 기준은 하나 — 지금 이 코드가 sleep 해도 되는 자리인가. 프로세스 컨텍스트이고 sleep 이 안전하면 GFP_KERNEL, 인터럽트나 spinlock 처럼 sleep 이 불가능하면 GFP_ATOMIC 이다. 어기면 머신이 멈추거나 커널이 죽는다.",
       "sleep 을 일으키는 것은 결국 schedule() 호출입니다")

d.box(LX, HY, LW, RH, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, HY + 27, "지금 어느 자리인가", 13, SOFT, KR)
for j, name in enumerate(COLS):
    d.box(CX[j], HY, CW, RH, PAPER2, RULE, 0.9)
    d.t(CX[j] + CW / 2, HY + 27, name, 12, INK, MONO, "middle", 600)

# (컨텍스트, sleep 가능?, [GFP_KERNEL, GFP_ATOMIC, GFP_NOIO] 판정)
ROWS = [
    ("프로세스 컨텍스트 · sleep 안전", [("씁니다", OK), ("써도 되나 불필요", WARN), ("I/O 금지 시에만", WARN)]),
    ("인터럽트 · atomic 컨텍스트", [("머신이 멈춥니다", BAD), ("이것만 씁니다", OK), ("안 됩니다", BAD)]),
    ("spinlock 을 쥐고 있음", [("LDV 위반 · deadlock", BAD), ("이것만 씁니다", OK), ("안 됩니다", BAD)]),
    ("mutex 를 쥐고 있음", [("씁니다", OK), ("써도 되나 불필요", WARN), ("I/O 금지 시에만", WARN)]),
    ("USB 디바이스 lock 을 쥐고 있음", [("LDV 위반", BAD), ("됩니다", OK), ("이것을 씁니다", OK)]),
]

for i, (ctx, cells) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    focal = i == 2
    if focal:
        d.tone(LX, y, LW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + 16, y + 27, ctx, 13, ACC if focal else INK, KR, "start")
    for j, (txt, c) in enumerate(cells):
        d.tone(CX[j], y, CW, RH, c, 6, "18", 1.1)
        d.t(CX[j] + CW / 2, y + 27, txt, 13, c, KR)

BOT = HY + RH + 8 + len(ROWS) * RS
d.t(LX, BOT + 30, "spinlock 은 쥔 채 sleep 할 수 없고 mutex 는 할 수 있습니다 — 이 차이가 두 줄의 판정을 갈랐습니다.", 13, ACC, KR, "start")
d.t(LX, BOT + 54, "지금이 atomic 인지 모르겠으면 CONFIG_DEBUG_ATOMIC_SLEEP 을 켜고 in_task()·in_atomic() 으로 판별합니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 78, "__GFP_ZERO 를 OR 하면 0 으로 초기화된 메모리를 받습니다. 좋은 관행입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("써도 되는 자리", OK), ("가능하나 권하지 않음", WARN), ("쓰면 안 되는 자리", BAD), ("가장 자주 어기는 줄", ACC)])
d.save("08-01.gfp-context-matrix.svg")
print("ok 08-01.gfp-context-matrix")
