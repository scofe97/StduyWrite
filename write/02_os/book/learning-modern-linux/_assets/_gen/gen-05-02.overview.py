# 05-02 전체 개요 — 새 디스크가 커널에 잡히고, 파티션 · PV·VG · LV · 파일시스템 · 마운트 지점 · fstab 줄로
#           한 층씩 올라가는 실제 객체를 본문 실습의 값으로 쌓는다. 줄마다 그 층을 만든 명령을 함께 둔다.
# 타입 스펙: type-layers — 아래 층(디스크)에서 위 층(부팅 때 다시 붙이기)으로 쌓이는 운영 층.
#           accent 는 lvextend 로 늘어난 LV 익스텐트.
# 근거: 본문 §1 재스캔 표와 dmesg "[sdX] Attached SCSI disk", §2 parted -s /dev/loop10 … print(p1 1049kB–52.4MB,
#       p2 52.4MB–105MB, Partition Table: gpt)와 growpart /dev/loop10 2, §3 pvresize /dev/loop2 ·
#       vgextend vg0 /dev/loop1 · lvextend -r -L +100M(200.00 MiB 50 extents → 300.00 MiB 75 extents,
#       /dev/mapper/vg0-data is mounted on /mnt/lv), §4 mkfs.ext4 -L datalv · blkid UUID be9ae4e4-…,
#       §5 fstab 줄(UUID=be9ae4e4-… /mnt/lv ext4 defaults,nofail 0 2)과 systemd-fstab-generator.
# 축약: 본문은 층마다 다른 실습 장치를 썼다(파티션은 loop10, LVM 은 vg0 의 loop1·loop2). 파티션 띠의
#       비율은 개략이고, LV 띠는 한 칸이 익스텐트 하나다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W = 920
LX, X0, X1 = 24, 196, 896
GAP = 24
rows = [("1  재스캔", "디스크", 56), ("2  parted", "파티션", 92), ("3  LVM", "PV · VG", 64),
        ("3  LVM", "LV", 80), ("4  mkfs", "파일시스템", 56), ("5  mount", "마운트 지점", 56),
        ("6  fstab", "부팅 때 다시", 64)]
Y = []
y = 100
for _, _, h in rows:
    Y.append((y, y + h)); y += h + GAP
FOOT = y + 4
LEG = FOOT + 20
H = LEG + 48

d = D(W, H, "LEARNING MODERN LINUX · 05-02 OVERVIEW",
      "새 디스크가 부팅 때 다시 붙기까지 쌓이는 층",
      "재스캔으로 커널이 새 디스크를 잡으면 parted 가 GPT 파티션을 나누고 growpart 가 마지막 파티션을 끝까지 늘린다. "
      "PV 는 볼륨 그룹 vg0 에 모이고 LV /dev/vg0/data 는 lvextend -r 로 50 익스텐트에서 75 익스텐트가 된다. "
      "mkfs.ext4 가 라벨 datalv 와 UUID 를 새기고, 파일시스템은 /mnt/lv 에 붙으며, 같은 UUID 를 적은 fstab 줄을 "
      "systemd-fstab-generator 가 부팅 때 .mount 유닛으로 바꾼다.",
      "키울 때는 아래 층부터 — 위 층은 아래 층이 이미 확보한 공간만 쓴다")

# 층 사이 화살표 먼저
CX = (X0 + X1) / 2
for (a0, a1), (b0, b1) in zip(Y, Y[1:]):
    d.arrow([(CX, a1 + 2), (CX, b0 - 3)], MUTED, "ar", 1.2)

for (step, name, _), (y0, y1) in zip(rows, Y):
    d.t(LX, y0 + 20, step, 12, SOFT, MONO, "start")
    d.t(LX, y0 + 40, name, 13, INK, KR, "start", 600)


def row(i, stroke, fill=None):
    y0, y1 = Y[i]
    if fill:
        d.tone(X0, y0, X1 - X0, y1 - y0, fill, 6)
    else:
        d.box(X0, y0, X1 - X0, y1 - y0, PAPER2, stroke, 1.1, 6)
    return y0, y1


# 1 디스크
y0, y1 = row(0, INFO)
d.t(X0 + 14, y0 + 22, "/dev/sdX", 14, INK, MONO, "start", 600)
d.t(X1 - 14, y0 + 22, "dmesg · [sdX] Attached SCSI disk", 12, INFO, MONO, "end")
d.t(X0 + 14, y0 + 44, 'echo "- - -" > /sys/class/scsi_host/host0/scan', 12, MUTED, MONO, "start")

# 2 파티션 — /dev/loop10 의 GPT 띠
y0, y1 = row(1, INFO)
d.t(X0 + 14, y0 + 22, "/dev/loop10", 14, INK, MONO, "start", 600)
d.t(X1 - 14, y0 + 22, "Partition Table: gpt", 12, INFO, MONO, "end")
SX0, SX1, SY = X0 + 14, X1 - 14, y0 + 34
P1, P2, PE = SX0 + 152, SX0 + 304, SX0 + 304
for (a, b), lab in (((SX0, P1), "p1 · 1049kB–52.4MB"), ((P1, P2), "p2 · 52.4MB–105MB")):
    d.o.append(f'<rect x="{a + 1}" y="{SY}" width="{b - a - 2}" height="26" rx="3" fill="{INFO}26" '
               f'stroke="{INFO}" stroke-width="1"/>')
    d.t(a + 10, SY + 18, lab, 12, INK, MONO, "start")
d.o.append(f'<rect x="{P2 + 1}" y="{SY}" width="{SX1 - P2 - 2}" height="26" rx="3" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(P2 + 12, SY + 18, "growpart /dev/loop10 2 · p2 를 끝까지", 12, INFO, KR, "start")
d.arrow([(P2 + 260, SY + 13), (SX1 - 10, SY + 13)], INFO, "info", 1.2, "4 3")
d.t(X0 + 14, y0 + 80, "parted -s /dev/loop10 mklabel gpt mkpart p1 … mkpart p2 …", 12, MUTED, MONO, "start")

# 3 PV · VG
y0, y1 = row(2, OK)
d.t(X0 + 14, y0 + 22, "VG vg0", 14, OK, MONO, "start", 600)
for (a, b), dev, cmd in (((X0 + 128, X0 + 400), "/dev/loop2", "pvresize"),
                         ((X0 + 416, X1 - 14), "/dev/loop1", "pvcreate → vgextend vg0")):
    d.o.append(f'<rect x="{a}" y="{y0 + 10}" width="{b - a}" height="44" rx="4" fill="{OK}12" '
               f'stroke="{OK}" stroke-width="1"/>')
    d.t(a + 12, y0 + 28, f"PV {dev}", 13, INK, MONO, "start", 600)
    d.t(a + 12, y0 + 46, cmd, 12, MUTED, MONO, "start")

# 3 LV — 50 익스텐트 → 75 익스텐트
y0, y1 = row(3, ACC)
d.t(X0 + 14, y0 + 22, "/dev/vg0/data", 14, INK, MONO, "start", 600)
d.t(X1 - 14, y0 + 22, "200.00 MiB (50 extents) → 300.00 MiB (75 extents)", 12, MUTED, MONO, "end")
BX0, BX1, BY = X0 + 14, X1 - 14, y0 + 34
cw = (BX1 - BX0) / 75
for i in range(75):
    new = i >= 50
    c = ACC if new else OK
    d.o.append(f'<rect x="{BX0 + i * cw + 0.6:.1f}" y="{BY}" width="{cw - 1.2:.1f}" height="14" rx="1" '
               f'fill="{c}{"66" if new else "33"}" stroke="{c}" stroke-width="0.6"/>')
d.t(BX0, y0 + 68, "lvextend -r -L +100M /dev/vg0/data", 12, MUTED, MONO, "start")
d.t(BX0 + 50 * cw + 4, y0 + 68, "+25 extents · resize2fs 까지 한 번에", 12, ACC, KR, "start", 600)

# 4 파일시스템
y0, y1 = row(4, RULE)
d.t(X0 + 14, y0 + 22, 'ext4 · LABEL="datalv"', 14, INK, MONO, "start", 600)
d.t(X1 - 14, y0 + 22, 'UUID="be9ae4e4-a6c3-…"', 12, WARN, MONO, "end", 600)
d.t(X0 + 14, y0 + 44, "mkfs.ext4 -L datalv /dev/vg0/data", 12, MUTED, MONO, "start")

# 5 마운트 지점
y0, y1 = row(5, RULE)
d.t(X0 + 14, y0 + 22, "/mnt/lv", 14, INK, MONO, "start", 600)
d.t(X1 - 14, y0 + 22, "/dev/mapper/vg0-data is mounted on /mnt/lv", 12, MUTED, MONO, "end")
d.t(X0 + 14, y0 + 44, "mount -o remount,ro /mnt/lv", 12, MUTED, MONO, "start")

# 6 fstab
y0, y1 = row(6, RULE)
d.t(X0 + 14, y0 + 22, "/etc/fstab", 14, INK, MONO, "start", 600)
d.t(X0 + 116, y0 + 22, "UUID=be9ae4e4-a6c3-…", 13, WARN, MONO, "start", 600)
d.t(X0 + 278, y0 + 22, "/mnt/lv  ext4  defaults,nofail  0  2", 13, INK, MONO, "start")
d.t(X0 + 14, y0 + 46, "systemd-fstab-generator", 12, MUTED, MONO, "start")
d.t(X0 + 196, y0 + 46, "→ 부팅 때 .mount 유닛으로", 12, MUTED, KR, "start")

d.t(LX, FOOT, "실습 장치는 층마다 다름 (loop10 · vg0) · 파티션 띠 비율은 개략 · LV 띠 한 칸 = 익스텐트 하나",
    11, SOFT, KR, "start")
d.legend(LEG, [("디스크 · 파티션", INFO), ("LVM", OK), ("lvextend 로 늘어난 몫", ACC), ("같은 UUID", WARN)])
d.save("05-02.overview.svg")
print("ok 05-02.overview", H)
