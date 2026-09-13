# 09-02 §3 — free 페이지 수준에 따라 회수가 어느 단계로 들어가는가. 본문 /proc/zoneinfo 값을 그대로 썼다.
#   Node 0 zone Normal — pages free 75060 · min 16188 · low 23952 · high 31716
# 타입 스펙: type-state — 주체 하나(그 node:zone)의 상태 전이와 가드. 가드가 곧 watermark 다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 716
BX, BW = 216, 616
BH, GAP, Y0 = 84, 24, 148

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-02 §3",
       "watermark 셋이 회수 단계를 가릅니다",
       "회수는 node:zone 단위로 일어난다. 커널은 zone 마다 min·low·high 세 watermark 를 페이지 단위로 두고, 자유 페이지가 어느 구간에 있느냐로 회수의 세기를 정한다. min 아래로 떨어지면 회수만 하는 게 아니라 그 zone 의 신규 요청을 거부한다.",
       "본문 /proc/zoneinfo 의 Node 0 zone Normal 값을 그대로 썼습니다")

# (상태, 설명, 색, 그 구간의 아래 경계 라벨)
STATES = [
    ("정상", "회수하지 않습니다. 관측값 75,060 이 여기 있습니다", OK, "high  31,716"),
    ("gentle 회수", "일부 캐시를 evict 하고 조심스럽게 swap 합니다", INFO, "low  23,952"),
    ("aggressive 회수", "캐시를 더 걷어내고 적극적으로 swap 합니다", WARN, "min  16,188"),
    ("경보 — 신규 요청 거부", "회수에 더해 그 zone 의 새 할당을 거절합니다", BAD, None),
]

for i, (name, desc, c, wm) in enumerate(STATES):
    y = Y0 + i * (BH + GAP)
    focal = c is BAD
    d.tone(BX, y, BW, BH, c, 8, "12" if focal else "14", 1.4 if focal else 1.1)
    d.t(BX + 20, y + 34, name, 14, c, KR, "start", 600)
    d.t(BX + 20, y + 58, desc, 13, MUTED, KR, "start")
    d.t(BX - 16, y + 44, f"{i}단계" if i else "평시", 12, SOFT, MONO, "end")
    if wm:
        wy = y + BH + GAP / 2
        d.line(BX - 8, wy, BX + BW - 148, wy, ACC, 1.2, "5 5")
        d.t(BX + BW, wy + 4, wm, 12, ACC, MONO, "end")

# 압박은 아래로, 회수 성공은 위로
d.arrow([(140, Y0 + 16), (140, Y0 + 3 * (BH + GAP) + BH - 16)], BAD, "bad", 1.4)
d.t(120, Y0 + 100, "자유 페이지가", 13, BAD, KR, "end")
d.t(120, Y0 + 122, "줄어듭니다", 13, BAD, KR, "end")
d.arrow([(88, Y0 + 3 * (BH + GAP) + BH - 16), (88, Y0 + 16)], OK, "ok", 1.4)
d.t(72, Y0 + 220, "회수가", 13, OK, KR, "end")
d.t(72, Y0 + 242, "되돌립니다", 13, OK, KR, "end")

BOT = Y0 + 4 * (BH + GAP)
d.t(24, BOT + 28, "캐시가 회수의 첫 희생자입니다. page cache · dentry · inode · slab 이 압박이 커질수록 지능적으로 축소됩니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 52, "회수를 수행하는 것은 kswapd 커널 스레드입니다. free 가 high 위로 올라오면 평시로 돌아갑니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("평시", OK), ("gentle", INFO), ("aggressive", WARN), ("신규 요청 거부", BAD), ("watermark", ACC)])
d.save("09-02.watermark-states.svg")
print("ok 09-02.watermark-states")
