# 05-01 §5 — 물리 볼륨이 그룹으로 모였다가 논리 볼륨으로 갈라지는 흐름.
# 타입 스펙: type-sankey — 여러 갈래가 한 곳에 모였다가 다시 갈라지는 흐름. accent 는 파티션이
#           못 하고 LV 만 하는 일. 축약: 두 LV 의 실제 용량비는 222.10 GiB 대 976 MiB 라 그대로
#           그리면 아래쪽이 한 줄로 뭉개진다. 그래서 높이를 읽을 수 있게 조정하고 용량은 숫자로 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §5",
      "물리 볼륨을 풀로 모아 두면 논리 볼륨을 자유롭게 분할",
      "물리 볼륨 sda2 가 볼륨 그룹 elementary-vg 로 풀링되고, "
      "그 안에서 root 와 swap_1 두 논리 볼륨으로 나뉘는 Sankey 계층 흐름.",
      "VG 에 여유 PE 가 있으면 사용 중에도 확장 가능")

TOP, TOTAL = 168, 260
PVX, PVW = 48, 176
VGX, VGW = 344, 192
LVX, LVW = 640, 192

d.o.append(f'<path d="M {PVX + PVW} {TOP + 6} L {VGX} {TOP + 6} L {VGX} {TOP + TOTAL - 6} '
           f'L {PVX + PVW} {TOP + TOTAL - 6} Z" fill="{INFO}22" stroke="none"/>')

d.box(PVX, TOP, PVW, TOTAL, PAPER2, INFO, 1.2, 8)
d.t(PVX + PVW / 2, TOP + 34, "물리 볼륨 (PV)", 15, INFO, KR, "middle", 600)
d.t(PVX + PVW / 2, TOP + 56, "Physical Volume", 11, SOFT, MONO, "middle")
d.t(PVX + PVW / 2, TOP + 116, "/dev/sda2", 13, INK, MONO, "middle")
d.t(PVX + PVW / 2, TOP + 138, "223.07 GiB", 12, MUTED, MONO, "middle")
d.t(PVX + PVW / 2, TOP + 160, "PE Size: 4.00 MiB", 11, SOFT, MONO, "middle")
d.t(PVX + PVW / 2, TOP + 200, "파티션 또는 드라이브 전체", 11, MUTED, KR, "middle")
d.t(PVX + PVW / 2, TOP + 222, "단일 물리 블록 장치", 11, MUTED, KR, "middle")

d.box(VGX, TOP, VGW, TOTAL, PAPER2, OK, 1.2, 8)
d.t(VGX + VGW / 2, TOP + 34, "볼륨 그룹 (VG)", 15, OK, KR, "middle", 600)
d.t(VGX + VGW / 2, TOP + 56, "Volume Group", 11, SOFT, MONO, "middle")
d.t(VGX + VGW / 2, TOP + 116, "elementary-vg", 13, INK, MONO, "middle")
d.t(VGX + VGW / 2, TOP + 138, "#PV 1 · #LV 2", 12, MUTED, MONO, "middle")
d.t(VGX + VGW / 2, TOP + 160, "VFree: 16.00 MiB (4 PE)", 11, SOFT, MONO, "middle")
d.t(VGX + VGW / 2, TOP + 200, "PV 들의 자원 통합 풀", 11, MUTED, KR, "middle")
d.t(VGX + VGW / 2, TOP + 222, "LV 를 나눠 주는 풀", 11, MUTED, KR, "middle")

lvs = [("root", "222.10 GiB", "ext4 · / (56857 PE)", TOP, 176, ACC),
       ("swap_1", "976.00 MiB", "[SWAP] (244 PE)", TOP + 188, 72, MUTED)]
srcy = TOP
for name, size, use, y, h, col in lvs:
    d.o.append(f'<path d="M {VGX + VGW} {srcy + 6} L {LVX} {y + 6} L {LVX} {y + h - 6} '
               f'L {VGX + VGW} {srcy + h - 6} Z" fill="{col}22" stroke="none"/>')
    d.box(LVX, y, LVW, h, PAPER2, col, 1.2, 8)
    d.t(LVX + LVW / 2, y + 24, name, 15, col, MONO, "middle", 600)
    d.t(LVX + LVW / 2, y + 42, size, 12, INK, MONO, "middle")
    d.t(LVX + LVW / 2, y + 58, use, 11, MUTED, MONO, "middle")
    srcy += h + 12

d.t(LVX + LVW / 2, TOP - 14, "논리 볼륨 (LV) — Logical Volume", 12, MUTED, KR, "middle", 600)
d.t(LVX + LVW / 2, TOP + 108, "블록 장치 생성 후 포맷", 11, MUTED, KR, "middle")
d.t(LVX + LVW / 2, TOP + 128, "여유 PE 안에서 사용 중 확장", 11, MUTED, KR, "middle")

AY = 456
d.o.append(f'<rect x="{PVX}" y="{AY}" width="{LVX + LVW - PVX}" height="72" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(PVX + 20, AY + 26, "파티션 한계를 넘는 논리 볼륨의 핵심 특성", 13.5, ACC, KR, "start", 600)
d.t(PVX + 20, AY + 46, "여러 PV 를 한 풀(VG)로 묶고 · 여유 PE 안에서 LV 를 사용 중에 확장",
    11.5, INK, KR, "start")
d.t(PVX + 20, AY + 64, "이 VG 의 여유는 4 PE(16 MiB) — 크게 늘리려면 PV 추가가 먼저",
    11, MUTED, KR, "start")

d.legend(556, [("물리 층 (PV)", INFO), ("자원 풀 (VG)", OK), ("논리 볼륨 (LV)", ACC)])
d.save("05-01.lvm.svg")
print("ok 05-01.lvm")
