# 05-01 §5 — 물리 볼륨이 그룹으로 모였다가 논리 볼륨으로 갈라지는 흐름.
# 원문("Logical Volume Manager"): "Logical volume manager (LVM) uses a layer of indirection between
#       physical entities (such as drives or partitions) and the file system. This yields a setup that
#       allows for risk-free, zero-downtime expanding and automatic storage extension through the pooling
#       of resources."
#   Physical volumes (PV): "Can be a disk partition, an entire disk drive, and other devices."
#   Logical volumes (LV):  "Are block devices created from VGs. These are conceptually comparable to
#                           partitions. You have to create a filesystem on an LV before you can use it.
#                           You can easily resize LVs while in use."
#   Volume groups (VG):    "Are a go-between between a set of PVs and LVs. Think of a VG as pools of PVs
#                           collectively providing resources."
#   실측 출력 — `vgs` 의 `elementary-vg  1  2  0  wz--n-  <223.07g  16.00m`,
#   `pvdisplay` 의 `PV Name /dev/sda2`, `lvscan` 의 root [<222.10 GiB] · swap_1 [976.00 MiB].
# 타입 스펙: type-sankey — 여러 갈래가 한 곳에 모였다가 다시 갈라지는 흐름. accent 는 파티션이
#           못 하고 LV 만 하는 일. 축약: 두 LV 의 실제 용량비는 222.10 GiB 대 976 MiB 라 그대로
#           그리면 아래쪽이 한 줄로 뭉개진다. 그래서 높이를 읽을 수 있게 조정하고 용량은 숫자로 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §5",
      "물리 볼륨을 풀로 모아 두면 논리 볼륨을 마음대로 자를 수 있다",
      "저자의 실제 설정을 흐름으로 옮긴 것. 물리 볼륨 하나가 볼륨 그룹 하나에 들어가고, "
      "그 그룹에서 논리 볼륨 둘이 나왔다.",
      "논리 볼륨은 쓰는 도중에도 크기를 바꿀 수 있습니다")

TOP, TOTAL = 168, 260
PVX, PVW = 48, 176
VGX, VGW = 344, 192
LVX, LVW = 640, 192

d.o.append(f'<path d="M {PVX + PVW} {TOP + 6} L {VGX} {TOP + 6} L {VGX} {TOP + TOTAL - 6} '
           f'L {PVX + PVW} {TOP + TOTAL - 6} Z" fill="{INFO}22" stroke="none"/>')

d.box(PVX, TOP, PVW, TOTAL, PAPER2, INFO, 1.2, 8)
d.t(PVX + PVW / 2, TOP + 34, "물리 볼륨", 15, INFO, KR, "middle", 600)
d.t(PVX + PVW / 2, TOP + 56, "PV", 12, MUTED, MONO)
d.t(PVX + PVW / 2, TOP + 122, "/dev/sda2", 13, INK, MONO)
d.t(PVX + PVW / 2, TOP + 144, "223.07 GiB", 12, MUTED, MONO)
d.t(PVX + PVW / 2, TOP + 200, "파티션이거나", 11.5, MUTED, KR)
d.t(PVX + PVW / 2, TOP + 222, "드라이브 전체이거나", 11.5, MUTED, KR)

d.box(VGX, TOP, VGW, TOTAL, PAPER2, OK, 1.2, 8)
d.t(VGX + VGW / 2, TOP + 34, "볼륨 그룹", 15, OK, KR, "middle", 600)
d.t(VGX + VGW / 2, TOP + 56, "VG", 12, MUTED, MONO)
d.t(VGX + VGW / 2, TOP + 116, "elementary-vg", 13, INK, MONO)
d.t(VGX + VGW / 2, TOP + 140, "#PV 1 · #LV 2", 12, MUTED, MONO)
d.t(VGX + VGW / 2, TOP + 162, "VFree 16.00m", 12, MUTED, MONO)
d.t(VGX + VGW / 2, TOP + 208, "PV 들이 모여 자원을", 11.5, MUTED, KR)
d.t(VGX + VGW / 2, TOP + 230, "함께 내놓는 풀", 11.5, MUTED, KR)

lvs = [("root", "222.10 GiB", "ext4 · /", TOP, 176, ACC),
       ("swap_1", "976.00 MiB", "[SWAP]", TOP + 188, 72, MUTED)]
srcy = TOP
for name, size, use, y, h, col in lvs:
    d.o.append(f'<path d="M {VGX + VGW} {srcy + 6} L {LVX} {y + 6} L {LVX} {y + h - 6} '
               f'L {VGX + VGW} {srcy + h - 6} Z" fill="{col}22" stroke="none"/>')
    d.box(LVX, y, LVW, h, PAPER2, col, 1.2, 8)
    d.t(LVX + LVW / 2, y + 30, name, 15, col, MONO, "middle", 600)
    d.t(LVX + LVW / 2, y + 50, size, 12, INK, MONO)
    d.t(LVX + LVW / 2, y + 68, use, 11.5, MUTED, MONO)
    srcy += h + 12

d.t(LVX + LVW / 2, TOP - 14, "논리 볼륨 · LV", 12, MUTED, KR, "middle", 600)
d.t(LVX + LVW / 2, TOP + 108, "쓰기 전에 그 위에", 11.5, MUTED, KR)
d.t(LVX + LVW / 2, TOP + 130, "파일시스템을 만들어야", 11.5, MUTED, KR)
d.t(LVX + LVW / 2, TOP + 152, "합니다", 11.5, MUTED, KR)

AY = 456
d.o.append(f'<rect x="{PVX}" y="{AY}" width="{LVX + LVW - PVX}" height="72" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(PVX + 20, AY + 28, "파티션이 못 하고 논리 볼륨만 하는 일", 13.5, ACC, KR, "start", 600)
d.t(PVX + 20, AY + 50, "쓰는 도중에 크기를 바꿀 수 있습니다. 위험 없는 확장과 무중단 확장이 여기에서 나옵니다.",
    12, ACC, KR, "start")
d.t(PVX + 20, AY + 68, "도구 이름도 pv· vg· lv 로 시작해 어느 층을 만지는지가 이름에 드러납니다.",
    11.5, MUTED, KR, "start")

d.legend(556, [("물리 층", INFO), ("풀", OK), ("LV 만 하는 일", ACC)])
d.save("05-01.lvm.svg")
print("ok 05-01.lvm")
