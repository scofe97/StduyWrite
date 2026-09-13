# 07-03 §3 — 존이 물리 주소 축 위에서 차지하는 구간. 본문 journalctl 출력의 범위를 그대로 옮겼다.
#   DMA [0x1000 - 0xffffff] · DMA32 [0x1000000 - 0xffffffff] · Normal [0x100000000 - 0x4427fffff]
# 막대 길이는 실제 비율이다. DMA 가 눈금에서 사라지는 것이 이 그림의 논점이라 늘리지 않았다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 가로축은 시간이 아니라 물리 주소다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 528
LX, LW = 24, 120
AX, AXW = 160, 792
RY, RH, RS = 176, 36, 52

END = 0x4427fffff + 1            # 18,295,554,048 B = 17.04 GiB
def px(v): return AX + v / END * AXW

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-03 §3",
       "존을 가르는 것은 크기가 아닙니다",
       "한 노드 안의 세 존을 물리 주소 축 위에 실제 비율로 놓았다. ZONE_DMA 는 전체의 0.09% 라 이 눈금에서 보이지 않는데도 별도 존인 이유는, 존을 가르는 기준이 크기가 아니라 그 구간에만 닿을 수 있는 하드웨어가 있다는 사실이기 때문이다.",
       "본문 journalctl 출력의 범위를 그대로 옮겼습니다 — 막대 길이는 실제 비율입니다")

ROWS = [
    ("ZONE_DMA", 0x1000, 0x1000000, "16 MiB · 0.09%", "옛 ISA 장치가 닿는 저주소", ACC),
    ("ZONE_DMA32", 0x1000000, 0x100000000, "4 GiB · 23.4%", "32비트 DMA 가 닿는 범위", INFO),
    ("ZONE_NORMAL", 0x100000000, END, "13 GiB · 76.5%", "나머지 일반 메모리", OK),
]

for i, (name, lo, hi, size, role, c) in enumerate(ROWS):
    y = RY + i * RS
    d.t(LX, y + 23, name, 13, c, MONO, "start", 600)
    x0, x1 = px(lo), px(hi)
    w = max(x1 - x0, 3)
    d.tone(x0, y, w, RH, c, 4, "22" if c is ACC else "18", 1.4 if c is ACC else 1.1)
    # 막대가 오른쪽 끝까지 닿는 행만 라벨을 안에 둔다. 나머지는 막대 오른쪽에 붙인다.
    if x1 > AX + AXW - 40:
        d.t(x0 + 16, y + 23, f"{size}  ·  {role}", 13, c, KR, "start")
    else:
        d.t(x1 + 16, y + 23, f"{size}  ·  {role}", 13, c, KR, "start")

# 주소 눈금 — GiB 단위로 끊는다
TY = RY + len(ROWS) * RS + 8
d.line(AX, TY, AX + AXW, TY, RULE, 1.0)
for g in (0, 4, 8, 12):
    x = px(g * 2**30)
    d.line(x, TY, x, TY + 8, RULE, 1.0)
    d.t(x, TY + 26, f"{g} GiB", 12, SOFT, MONO)
d.line(AX + AXW, TY, AX + AXW, TY + 8, RULE, 1.0)
d.t(AX + AXW, TY + 26, "17.04 GiB", 12, SOFT, MONO, "end")
d.t(LX, TY + 26, "물리 주소", 13, SOFT, KR, "start")

BOT = TY + 56
d.t(LX, BOT, "존 이름과 개수는 부팅 시 커널이 동적으로 정합니다. /proc/buddyinfo 의 맨 왼쪽이 Node 0 하나뿐이면 UMA 입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 24, "존마다 PFN 범위가 할당되고, 자료 구조는 include/linux/mmzone.h 의 struct zone 입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 48, "32비트에는 ZONE_HIGHMEM 도 있었습니다 — 하드웨어 제약이 아니라 커널 VAS 가 모자라 생긴 소프트웨어 난점이었습니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("보이지 않아도 별도 존", ACC), ("32비트 DMA 범위", INFO), ("일반 메모리", OK)])
d.save("07-03.zone-spans.svg")
print("ok 07-03.zone-spans")
