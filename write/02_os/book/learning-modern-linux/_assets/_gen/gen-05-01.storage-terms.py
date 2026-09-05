# 05-01 §2 — 드라이브에서 아이노드까지 다섯 이름의 포함 관계.
# 원문("Basics"):
#   Drive:       "A (physical) block device such as a hard disk drive (HDD) or a solid-state drive (SSD).
#                 ... for example, /dev/sda (SCSI device) or /dev/sdb (SATA device) or /dev/hda (IDE device)."
#   Partition:   "You can logically split up drives into partitions, a set of storage sectors. For example,
#                 you may decide to create two partitions on your HDD, which then would show up as
#                 /dev/sdb1 and /dev/sdb2."
#   Volume:      "somewhat similar to a partition, but it is more flexible, and it is also formatted for a
#                 specific filesystem."
#   Super block: "When formatted, filesystems have a special section in the beginning that captures the
#                 metadata of the filesystem. This includes things like filesystem type, blocks, state,
#                 and how many inodes per block."
#   Inodes:      "inodes store metadata about files, such as size, owner, location, date, and permissions.
#                 However, inodes do not store the filename and the actual data. This is kept in
#                 directories, which really are just a special kind of regular file, mapping inodes to
#                 filenames."
#   실증은 저자의 `lsblk --exclude 7` 출력 — sda(223.6G) > sda1(512M, /boot/efi) · sda2(223.1G) >
#   elementary--vg-root(222.1G, /) · elementary--vg-swap_1(976M, [SWAP]).
# 타입 스펙: type-nested — 포함 관계로 드러나는 경계. accent 는 이 장에서 가장 중요한 한 줄,
#           곧 아이노드가 담지 '않는' 것. 축약: 슈퍼블록과 아이노드는 볼륨 안쪽 내용이라 오른쪽에 펼쳤다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 632
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §2",
      "드라이브 안에 파티션, 그 안에 볼륨, 그 앞머리에 메타데이터",
      "저자가 정의한 다섯 용어를 포함 관계로 세운 것. 왼쪽은 저자의 lsblk 출력 그대로이고, "
      "오른쪽은 포맷된 볼륨 하나를 열어 본 것이다.",
      "아이노드는 파일 이름과 데이터를 담지 않습니다")

DX, DY, DW, DH = 28, 148, 420, 268
d.o.append(f'<rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
_lbl = "드라이브 — 물리 블록 장치"
_w = sum(12 if "가" <= c <= "힣" else 7 for c in _lbl) + 16
d.o.append(f'<rect x="{DX + 16}" y="{DY - 8}" width="{_w}" height="16" fill="{PAPER}"/>')
d.t(DX + 24, DY + 4, _lbl, 12, INFO, KR, "start", 600)
_cmd = "sda · 223.6G"
_cw = len(_cmd) * 7 + 16
d.o.append(f'<rect x="{DX + DW - 20 - _cw + 8}" y="{DY - 8}" width="{_cw}" height="16" fill="{PAPER}"/>')
d.t(DX + DW - 20, DY + 4, _cmd, 12, INFO, MONO, "end")

PX, PY, PW = DX + 24, DY + 32, DW - 48
d.box(PX, PY, PW, 64, PAPER, MUTED, 1.1, 6)
d.t(PX + 14, PY + 26, "파티션 sda1", 13, INK, KR, "start", 600)
d.t(PX + 14, PY + 48, "512M · /boot/efi · vfat", 12, MUTED, MONO, "start")

P2Y = PY + 80
d.box(PX, P2Y, PW, 148, PAPER, MUTED, 1.1, 6)
d.t(PX + 14, P2Y + 26, "파티션 sda2", 13, INK, KR, "start", 600)
d.t(PX + 14, P2Y + 46, "223.1G · 저장 섹터의 집합", 12, MUTED, KR, "start")

for i, (name, size) in enumerate([("볼륨 elementary--vg-root", "222.1G · ext4 · /"),
                                  ("볼륨 elementary--vg-swap_1", "976M · [SWAP]")]):
    vy = P2Y + 58 + i * 42
    d.o.append(f'<rect x="{PX + 14}" y="{vy}" width="{PW - 28}" height="34" rx="5" '
               f'fill="{OK}12" stroke="{OK}" stroke-width="1.2"/>')
    d.t(PX + 28, vy + 22, name, 12, OK, KR, "start", 600)
    d.t(PX + PW - 28, vy + 22, size, 11.5, MUTED, MONO, "end")

CX, CY_, CW_, CH_ = 480, 148, 372, 268
d.o.append(f'<rect x="{CX}" y="{CY_}" width="{CW_}" height="{CH_}" rx="8" '
           f'fill="{ACC}06" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 6"/>')
_l2 = "포맷된 볼륨 하나를 열면"
_w2 = sum(12 if "가" <= c <= "힣" else 7 for c in _l2) + 16
d.o.append(f'<rect x="{CX + 16}" y="{CY_ - 8}" width="{_w2}" height="16" fill="{PAPER}"/>')
d.t(CX + 24, CY_ + 4, _l2, 12, ACC, KR, "start", 600)

VX, VY, VW = CX + 20, CY_ + 28, CW_ - 40
d.box(VX, VY, VW, 96, PAPER, MUTED, 1.1, 6)
d.t(VX + 16, VY + 26, "슈퍼블록", 14, INK, KR, "start", 600)
d.t(VX + 16, VY + 48, "포맷하면 앞부분에 생기는 특별한 구획", 11.5, MUTED, KR, "start")
d.t(VX + 16, VY + 68, "파일시스템 종류 · 블록 · 상태", 11.5, MUTED, KR, "start")
d.t(VX + 16, VY + 86, "블록당 아이노드 수", 11.5, MUTED, KR, "start")

IY = VY + 112
d.o.append(f'<rect x="{VX}" y="{IY}" width="{VW}" height="128" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(VX + 16, IY + 26, "아이노드", 14, ACC, KR, "start", 600)
d.t(VX + 16, IY + 48, "담는다 — 크기 · 소유자 · 위치 · 날짜 · 권한", 11.5, MUTED, KR, "start")
d.t(VX + 16, IY + 70, "담지 않는다 — 파일 이름 · 실제 데이터", 12, ACC, KR, "start", 600)
d.t(VX + 16, IY + 92, "이름은 디렉토리가 갖는다. 그리고 디렉토리란", 11.5, MUTED, KR, "start")
d.t(VX + 16, IY + 112, "아이노드를 이름에 매핑하는 특별한 일반 파일이다.", 11.5, MUTED, KR, "start")

d.tone(28, 452, W - 56, 70, INFO)
d.t(48, 480, "stat 한 번이면 이 계층이 한 화면에 찍힙니다", 13, INK, KR, "start", 600)
d.t(48, 502, "Device 는 어느 볼륨인지를, Inode 는 그 안에서 어느 메타데이터 항목인지를 가리킵니다.",
    12, MUTED, KR, "start")

d.legend(556, [("드라이브와 파티션", INFO), ("볼륨", OK), ("이 장의 핵심 한 줄", ACC)])
d.save("05-01.storage-terms.svg")
print("ok 05-01.storage-terms")
