# 05-02 §3 — 스토리지 계층 확장과 축소 방향성 및 XFS 축소 불가 갈래.
# 타입 스펙: type-layers — 확장(아래->위)과 축소(위->아래)의 반대 방향 경로를 나란히 대조하고,
#           XFS 파일시스템 축소 실패 분기를 명시한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "키울 때는 아래 층부터, 줄일 때는 위 층부터",
      "확장은 물리 PV 에서 파일시스템으로 아래에서 위로 올라가며 안전하게 진행하지만, "
      "축소는 파일시스템부터 줄여야 블록 손상을 막는다. lvreduce -r 은 XFS 축소를 거절한다.",
      "lvextend -r 은 LV 와 파일시스템 확장을 한 번에 처리")

COL_W, GAP = 396, 28
X_EXP, X_SHR = 24, 24 + COL_W + GAP
TOP_Y = 122

# 왼쪽 열: 확장 (아래 -> 위)
d.box(X_EXP, TOP_Y, COL_W, 342, PAPER2, OK, 1.2, 8)
d.t(X_EXP + 20, TOP_Y + 28, "1. 스토리지 확장 (아래 층 -> 위 층)", 15, OK, KR, "start", 600)
d.t(X_EXP + 20, TOP_Y + 50, "물리 공간을 먼저 확보해야 상위 논리 볼륨과 파일시스템을 확장 가능", 11, MUTED, KR, "start")

exp_layers = [
    ("4. 파일시스템 확장", "resize2fs / xfs_growfs", "온라인 확장 지원 (lvextend -r 이 자동 호출)", 182, 275, OK),
    ("3. 논리 볼륨 (LV) 확장", "lvextend -L +100M / +100%FREE", "VG 여유 공간에서 LV PE 할당 (200M -> 300M -> 1.16G)", 182 + 68, 275, OK),
    ("2. 볼륨 그룹 (VG) 확장", "vgextend vg0 /dev/loop1", "새 PV 를 VG 풀에 편입해 가용 PE 증가", 182 + 68 * 2, 275, OK),
    ("1. 물리 볼륨 (PV) 확장", "pvresize /dev/loop2", "디스크 확장 인식 (196M -> 396M, PSize 반영)", 182 + 68 * 3, 275, OK),
]

for title, cmd, desc, y, _, col in exp_layers:
    d.box(X_EXP + 16, y, COL_W - 32, 54, PAPER, col, 1.0, 6)
    d.t(X_EXP + 28, y + 20, title, 12, col, KR, "start", 600)
    d.t(X_EXP + COL_W - 28, y + 20, cmd, 11, INK, MONO, "end")
    d.t(X_EXP + 28, y + 42, desc, 11, MUTED, KR, "start")

# 확장 상향 화살표
d.arrow([(X_EXP + COL_W - 8, TOP_Y + 318), (X_EXP + COL_W - 8, TOP_Y + 70)], OK, "ok", 2.0)

# 오른쪽 열: 축소 (위 -> 아래)
d.box(X_SHR, TOP_Y, COL_W, 342, PAPER2, ACC, 1.2, 8)
d.t(X_SHR + 20, TOP_Y + 28, "2. 스토리지 축소 (위 층 -> 아래 층)", 15, ACC, KR, "start", 600)
d.t(X_SHR + 20, TOP_Y + 50, "파일시스템보다 LV 를 먼저 줄이면 뒤쪽 블록이 잘려 데이터 유실", 11, MUTED, KR, "start")

shr_layers = [
    ("1. 파일시스템 축소", "resize2fs /dev/vg0/data 300M", "데이터 블록을 앞쪽으로 압축 (언마운트 필수)", 182, ACC),
    ("2. 논리 볼륨 (LV) 축소", "lvreduce -L 300M /dev/vg0/data", "상위 파일시스템 크기에 맞춰 PE 반환", 182 + 68, ACC),
    ("3. 볼륨 그룹 (VG) 축소", "vgreduce vg0 /dev/loop1", "비어 있는 PV 를 VG 풀에서 제외", 182 + 68 * 2, MUTED),
    ("4. 물리 볼륨 (PV) 제거", "pvremove /dev/loop1", "LVM 라벨 삭제 후 물리 디스크 회수", 182 + 68 * 3, MUTED),
]

for title, cmd, desc, y, col in shr_layers:
    d.box(X_SHR + 16, y, COL_W - 32, 54, PAPER, col, 1.0, 6)
    d.t(X_SHR + 28, y + 20, title, 12, col, KR, "start", 600)
    d.t(X_SHR + COL_W - 28, y + 20, cmd, 11, INK, MONO, "end")
    d.t(X_SHR + 28, y + 42, desc, 11, MUTED, KR, "start")

# 축소 하향 화살표
d.arrow([(X_SHR + COL_W - 8, TOP_Y + 70), (X_SHR + COL_W - 8, TOP_Y + 318)], ACC, "acc", 2.0)

# 하단 XFS 축소 불가 경고 박스
FY = TOP_Y + 356
d.tone(24, FY, W - 48, 54, BAD)
d.t(40, FY + 22, "XFS 축소 시도 시 fsadm 이 거절 (실측)", 12.5, BAD, KR, "start", 600)
d.t(40, FY + 42, "fsadm: Xfs filesystem shrinking is unsupported. (exit 5) — lvreduce -r 이 거절, LV 를 줄이려면 백업 → 재생성 → 복원", 11, INK, KR, "start")

d.legend(548, [("확장 순서 (하위 -> 상위)", OK), ("축소 순서 (상위 -> 하위)", ACC), ("XFS 축소 거절", BAD)])
d.save("05-02.grow-shrink.svg")
print("ok 05-02.grow-shrink")
