# 05-01 §5 — GCP VM(lml-os-lab) 실측 기준 루트 디스크(sda)와 실습 디스크(sdb)의 계층 매핑.
#           sda(8:0)는 GPT 파티션 기반으로 LVM 과 무관하고, sdb(8:16)만 PV 로 초기화되어
#           VG vg0 에 속하며, 논리 볼륨 root·data 는 dm-linear 매핑으로 실제 섹터에 대응한다.
# 타입 스펙: type-layers — 디스크에서 마운트까지 4개 층으로 쌓이는 실제 계층 구조. accent 는 활성 LV data.
# 근거: GCP VM(lml-os-lab) 실측(lsblk, pvs, vgs, lvs, dmsetup table).
#       sda: 8:0 (sda1 8:1 ext4 /, sda14 8:14, sda15 8:15 vfat, sda16 259:0 ext4 /boot)
#       sdb: 8:16 LVM2_member (PV vg0, 2559 PE, PE 크기 4 MiB)
#       vg0: #PV 1, #LV 2, 2559 PE (Alloc 306 PE, Free 2253 PE = 8.80 GiB)
#       vg0-root: 252:0 (dm-0), PE 0~49 (200 MiB), dmsetup linear 8:16 2048 (409600 섹터)
#       vg0-data: 252:1 (dm-1), PE 50~305 (1 GiB), dmsetup linear 8:16 411648 (2097152 섹터), ext4 /data
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 960, 712
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §5",
      "실제 디스크와 장치 번호에서 논리 볼륨까지의 매핑",
      "GCP VM(lml-os-lab) 실측: 루트 디스크 sda(8:0)는 파티션 기반으로 LVM 과 무관하고, "
      "실습 디스크 sdb(8:16)만 PV 로 초기화되어 VG vg0 에 속한다. 논리 볼륨 root·data 는 "
      "device-mapper(252:0·252:1)를 통해 sdb 의 실제 섹터 구간에 1:1 선형 매핑된다.",
      "루트 디스크와 실습 디스크는 다른 층 — LVM 은 sdb 안에서 PE 단위로 모으고 dmsetup 이 섹터 구간으로 연결")

# 층 이름 열 (왼쪽)
LX = 32
LAYERS = [
    (170, "1층 · 디스크", "8:0 · 8:16"),
    (290, "2층 · 파티션 · PV", "gpt · lvm2"),
    (422, "3층 · 풀 · 매퍼", "vg0 · dm linear"),
    (552, "4층 · LV · 마운트", "ext4 · /data"),
]
for y, name, sub in LAYERS:
    d.t(LX, y, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 18, sub, 11, SOFT, MONO, "start")

# 열 좌표
# 왼쪽: 루트 디스크 sda (X0=176, X1=396, 폭 220)
# 오른쪽: 실습 디스크 sdb (X2=424, X3=928, 폭 504)
X0, X1 = 176, 396
X2, X3 = 424, 928
CX_A = (X0 + X1) / 2
CX_B = (X2 + X3) / 2

# ─────────────────────────────────────────────────────────────────────────────
# 1층 — 물리 디스크 (Y: 140, H: 64)
# ─────────────────────────────────────────────────────────────────────────────
Y1, H1 = 140, 64
# sda
d.tone(X0, Y1, X1 - X0, H1, MUTED, op="10", sw=1.0)
d.t(CX_A, Y1 + 22, "/dev/sda (8:0)", 13, INK, MONO, "middle", 600)
d.t(CX_A, Y1 + 42, "루트 디스크 · 10 GiB", 13, MUTED, KR)

# sdb
d.tone(X2, Y1, X3 - X2, H1, INFO, op="14", sw=1.2)
d.t(CX_B, Y1 + 22, "/dev/sdb (8:16)", 13, INK, MONO, "middle", 600)
d.t(CX_B, Y1 + 42, "실습 디스크 · 10 GiB · 파티션 없음", 13, INFO, KR)

# 화살표 1층 → 2층
d.arrow([(CX_A, Y1 + H1), (CX_A, Y1 + H1 + 28)], MUTED, "ar")
d.t(CX_A + 8, Y1 + H1 + 18, "parted", 11, MUTED, MONO, "start")

d.arrow([(CX_B, Y1 + H1), (CX_B, Y1 + H1 + 28)], INFO, "info")
d.t(CX_B + 8, Y1 + H1 + 18, "pvcreate", 11, INFO, MONO, "start")

# ─────────────────────────────────────────────────────────────────────────────
# 2층 — 파티션(sda) 대 물리 볼륨 PV(sdb) (Y: 236, H: 98)
# ─────────────────────────────────────────────────────────────────────────────
Y2, H2 = 236, 98
# sda 파티션 영역
d.tone(X0, Y2, X1 - X0, H2, MUTED, op="10", sw=1.0)
d.t(X0 + 12, Y2 + 20, "GPT 파티션 테이블", 13, INK, KR, "start", 600)
d.t(X0 + 12, Y2 + 38, "sda1 (8:1) · 9 GiB · ext4", 11, MUTED, MONO, "start")
d.t(X0 + 12, Y2 + 56, "sda14 (4M) · sda15 (106M)", 11, SOFT, MONO, "start")
d.t(X0 + 12, Y2 + 74, "sda16 (259:0) · 913M · ext4", 11, SOFT, MONO, "start")

# sdb PV 영역
d.tone(X2, Y2, X3 - X2, H2, INFO, op="14", sw=1.2)
d.t(X2 + 16, Y2 + 22, "PV /dev/sdb · FSTYPE LVM2_member", 13, INFO, MONO, "start", 600)
d.t(X2 + 16, Y2 + 42, "PE 2559개 (PE 크기 4 MiB) · 섹터 2048 시작", 13, MUTED, KR, "start")

# PE 할당 띠
BAR_Y, BAR_H = Y2 + 54, 28
BAR_W = X3 - X2 - 32
W_ROOT = 76
W_DATA = 144
W_FREE = BAR_W - W_ROOT - W_DATA
BX0 = X2 + 16
BX1 = BX0 + W_ROOT
BX2 = BX1 + W_DATA

# root PE 띠
d.tone(BX0, BAR_Y, W_ROOT, BAR_H, INFO, r=3, op="33", sw=0.9)
d.t(BX0 + W_ROOT / 2, BAR_Y + 18, "PE 0~49", 11, INFO, MONO)

# data PE 띠
d.tone(BX1, BAR_Y, W_DATA, BAR_H, ACC, r=3, op="33", sw=1.0)
d.t(BX1 + W_DATA / 2, BAR_Y + 18, "PE 50~305 (1 GiB)", 11, ACC, MONO)

# free PE 띠
d.o.append(f'<rect x="{BX2}" y="{BAR_Y}" width="{W_FREE}" height="{BAR_H}" rx="3" fill="none" '
           f'stroke="{WARN}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t(BX2 + W_FREE / 2, BAR_Y + 18, "여유 2253 PE (8.80 GiB)", 13, WARN, KR)

# 화살표 2층 → 3층
d.arrow([(CX_A, Y2 + H2), (CX_A, Y2 + H2 + 28)], MUTED, "ar", dash="4 3")
d.t(CX_A + 8, Y2 + H2 + 18, "직접 연결", 13, SOFT, KR, "start")

d.arrow([(CX_B, Y2 + H2), (CX_B, Y2 + H2 + 28)], OK, "ok")
d.t(CX_B + 8, Y2 + H2 + 18, "vgcreate vg0 /dev/sdb", 11, OK, MONO, "start")

# ─────────────────────────────────────────────────────────────────────────────
# 3층 — 풀(VG)과 device-mapper 섹터 매핑 (Y: 366, H: 108)
# ─────────────────────────────────────────────────────────────────────────────
Y3, H3 = 366, 108
# sda 쪽: LVM 우회 (간접 층 없음)
d.o.append(f'<rect x="{X0}" y="{Y3}" width="{X1 - X0}" height="{H3}" rx="6" fill="none" '
           f'stroke="{RULE}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(CX_A, Y3 + 36, "LVM 간접 층 없음", 13, MUTED, KR, "middle", 600)
d.t(CX_A, Y3 + 58, "파티션 테이블 직접 분할", 13, SOFT, KR)
d.t(CX_A, Y3 + 78, "커널 블록 계층 직결", 13, SOFT, KR)

# sdb 쪽: VG vg0 상자
d.tone(X2, Y3, X3 - X2, H3, OK, op="0E", sw=1.3)
d.t(X2 + 16, Y3 + 20, "볼륨 그룹 vg0 · #PV 1 · #LV 2 · VSize <10.00g · VFree 8.80g", 11, OK, MONO, "start", 600)

# dmsetup table 서브 박스 셋 (너비 비례: 154, 180, 142)
DM_Y, DM_H = Y3 + 30, 66
BW_ROOT = 154
BW_DATA = 180
BW_FREE = X3 - X2 - 32 - BW_ROOT - BW_DATA
DMX0 = X2 + 16
DMX1 = DMX0 + BW_ROOT + 6
DMX2 = DMX1 + BW_DATA + 6

# dmsetup root
d.tone(DMX0, DM_Y, BW_ROOT, DM_H, INFO, r=4, op="18", sw=0.9)
d.t(DMX0 + BW_ROOT / 2, DM_Y + 18, "vg0-root 매핑", 13, INFO, KR, "middle", 600)
d.t(DMX0 + BW_ROOT / 2, DM_Y + 36, "0 409600 linear", 11, INK, MONO)
d.t(DMX0 + BW_ROOT / 2, DM_Y + 52, "8:16 섹터 2048", 11, MUTED, MONO)

# dmsetup data (FOCAL)
d.tone(DMX1, DM_Y, BW_DATA, DM_H, ACC, r=4, op="22", sw=1.4)
d.t(DMX1 + BW_DATA / 2, DM_Y + 18, "vg0-data 매핑 (focal)", 13, ACC, KR, "middle", 600)
d.t(DMX1 + BW_DATA / 2, DM_Y + 36, "0 2097152 linear", 11, ACC, MONO, "middle", 600)
d.t(DMX1 + BW_DATA / 2, DM_Y + 52, "8:16 섹터 411648", 11, INK, MONO)

# dmsetup free
d.o.append(f'<rect x="{DMX2}" y="{DM_Y}" width="{BW_FREE}" height="{DM_H}" rx="4" fill="none" '
           f'stroke="{WARN}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t(DMX2 + BW_FREE / 2, DM_Y + 18, "미할당 여유 공간", 13, WARN, KR, "middle", 600)
d.t(DMX2 + BW_FREE / 2, DM_Y + 36, "Free PE 2253개", 11, MUTED, MONO)
d.t(DMX2 + BW_FREE / 2, DM_Y + 52, "8.80 GiB 여유 풀", 13, SOFT, KR)

# 화살표 3층 → 4층
d.arrow([(CX_A, Y3 + H3), (CX_A, Y3 + H3 + 28)], MUTED, "ar")
d.t(CX_A + 8, Y3 + H3 + 18, "mount", 11, MUTED, MONO, "start")

d.arrow([(DMX0 + BW_ROOT / 2, Y3 + H3), (DMX0 + BW_ROOT / 2, Y3 + H3 + 28)], INFO, "info")
d.t(DMX0 + BW_ROOT / 2 + 6, Y3 + H3 + 18, "dm-0", 11, INFO, MONO, "start")

d.arrow([(DMX1 + BW_DATA / 2, Y3 + H3), (DMX1 + BW_DATA / 2, Y3 + H3 + 28)], ACC, "acc")
d.t(DMX1 + BW_DATA / 2 + 6, Y3 + H3 + 18, "dm-1", 11, ACC, MONO, "start")

# ─────────────────────────────────────────────────────────────────────────────
# 4층 — 논리 볼륨(LV) 및 최종 용도 마운트 (Y: 506, H: 104)
# ─────────────────────────────────────────────────────────────────────────────
Y4, H4 = 506, 104
# sda 최종 마운트
d.tone(X0, Y4, X1 - X0, H4, MUTED, op="10", sw=1.0)
d.t(X0 + 12, Y4 + 22, "파일시스템 마운트", 13, INK, KR, "start", 600)
d.t(X0 + 12, Y4 + 44, "sda1 → / (루트 ext4)", 11, INK, MONO, "start")
d.t(X0 + 12, Y4 + 64, "sda15 → /boot/efi (vfat)", 11, MUTED, MONO, "start")
d.t(X0 + 12, Y4 + 84, "sda16 → /boot (ext4)", 11, MUTED, MONO, "start")

# sdb 논리 볼륨 박스 셋
# root LV
d.tone(DMX0, Y4, BW_ROOT, H4, INFO, r=4, op="14", sw=0.9)
d.t(DMX0 + BW_ROOT / 2, Y4 + 22, "/dev/vg0/root", 12, INFO, MONO, "middle", 600)
d.t(DMX0 + BW_ROOT / 2, Y4 + 42, "252:0 (dm-0) · 200M", 11, INK, MONO)
d.t(DMX0 + BW_ROOT / 2, Y4 + 64, "미포맷 (FSTYPE 빈 칸)", 13, WARN, KR)
d.t(DMX0 + BW_ROOT / 2, Y4 + 84, "/dev/mapper/vg0-root", 10, SOFT, MONO)

# data LV (FOCAL)
d.tone(DMX1, Y4, BW_DATA, H4, ACC, r=4, op="20", sw=1.4)
d.t(DMX1 + BW_DATA / 2, Y4 + 22, "/dev/vg0/data", 13, ACC, MONO, "middle", 600)
d.t(DMX1 + BW_DATA / 2, Y4 + 42, "252:1 (dm-1) · 1.0G", 11, INK, MONO)
d.t(DMX1 + BW_DATA / 2, Y4 + 64, "ext4 포맷 · /data", 13, OK, KR, "middle", 600)
d.t(DMX1 + BW_DATA / 2, Y4 + 84, "/dev/mapper/vg0-data", 10, MUTED, MONO)

# free capacity
d.o.append(f'<rect x="{DMX2}" y="{Y4}" width="{BW_FREE}" height="{H4}" rx="4" fill="none" '
           f'stroke="{WARN}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t(DMX2 + BW_FREE / 2, Y4 + 24, "할당 대기 풀", 13, WARN, KR, "middle", 600)
d.t(DMX2 + BW_FREE / 2, Y4 + 46, "8.80 GiB 여유", 13, WARN, KR)
d.t(DMX2 + BW_FREE / 2, Y4 + 68, "새 LV 생성 공간", 13, SOFT, KR)
d.t(DMX2 + BW_FREE / 2, Y4 + 86, "lvextend 확장용 풀", 13, SOFT, KR)

# ─────────────────────────────────────────────────────────────────────────────
# 범례 (Y: 636)
# ─────────────────────────────────────────────────────────────────────────────
LEGEND_Y = 636
d.legend(LEGEND_Y, [
    ("루트 (LVM 밖)", MUTED),
    ("물리 볼륨", INFO),
    ("볼륨 그룹", OK),
    ("활성 LV (focal)", ACC),
    ("여유 PE", WARN),
])

d.save("05-01.lvm-mapping.svg")
