# 05-01 §4 — VFS 가 시스템 콜과 개별 파일시스템 사이에 놓이는 자리.
# 원문("The Virtual File System"): "Linux manages to provide a file-like access to many sorts of resources
#       (in-memory, locally attached, or networked storage) through an abstraction called the virtual file
#       system (VFS). The basic idea is to introduce a layer of indirection between the clients (syscalls)
#       and the individual filesystems implementing operations for a concrete device or other kind of
#       resource. This means that VFS separates the generic operation (open, read, seek) from the actual
#       implementation details."
#       "A file, in Linux, doesn't have any prescribed structure; it's just a stream of bytes. It's up to
#       the client to decide what the bytes mean."
#       네 갈래는 Local filesystems(ext3, XFS, FAT, NTFS) · In-memory filesystems(tmpfs) ·
#       Pseudo filesystems(procfs) · Networked filesystems(NFS, Samba, Netware).
#       "There are over 100 syscalls related to files."
# 타입 스펙: type-layers — 위아래 층과 그 사이의 계약. accent 는 층 하나, 곧 간접이 실제로 일어나는 자리.
#           축약: 시스템 콜 범주 다섯은 본문 표에 두고 도식에는 대표 셋만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 636
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §4",
      "일반적인 연산과 실제 구현을 갈라 놓는 층",
      "같은 open 과 read 가 SSD 로도 가고 /proc 으로도 가는 이유는 그 사이에 층이 하나 있기 때문이다. "
      "VFS 는 파일이라는 패러다임 위에서 자원에 접근하는 공통의 방법을 준다.",
      "리눅스에서 파일은 구조 없는 바이트 스트림입니다")

LX, LW = 40, 800
d.box(LX, 148, LW, 66, PAPER2, RULE, 1.0, 8)
d.t(LX + 20, 174, "클라이언트 — 시스템 콜", 15, INK, KR, "start", 600)
d.t(LX + 20, 196, "파일 관련 시스템 콜만 백 개가 넘습니다. open · read · seek 같은 일반적인 연산입니다.",
    12, MUTED, KR, "start")

d.arrow([(W / 2, 214), (W / 2, 244)], MUTED, "ar", 1.4)

VY = 248
d.o.append(f'<rect x="{LX}" y="{VY}" width="{LW}" height="96" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
d.t(LX + 20, VY + 30, "VFS — 커널 안의 추상 층", 16, ACC, KR, "start", 600)
d.t(LX + 20, VY + 54, "일반적인 연산을 실제 구현 세부와 갈라 놓습니다.", 12.5, ACC, KR, "start")
d.t(LX + 20, VY + 76, "자료구조는 include/linux/fs.h — inode · file · dentry · super_block",
    12, MUTED, MONO, "start")

BW, GAP = 194, 8
BY = 396
kinds = [
    ("로컬", "ext3 · XFS · FAT · NTFS", "드라이버로 블록 장치에", OK),
    ("인메모리", "tmpfs", "주기억장치에 산다", INFO),
    ("가짜", "procfs · sysfs", "커널 인터페이스를 감싼다", WARN),
    ("네트워크", "NFS · Samba", "드라이버가 네트워크를 탄다", MUTED),
]
for i, (name, ex, note, col) in enumerate(kinds):
    x = LX + i * (BW + GAP)
    d.path(f"M {x + BW / 2} {VY + 96} L {x + BW / 2} {BY - 2}", col, 1.3, m="ar")
    d.box(x, BY, BW, 92, PAPER2, col, 1.2, 6)
    d.t(x + BW / 2, BY + 28, name, 14, col, KR, "middle", 600)
    d.t(x + BW / 2, BY + 52, ex, 11.5, INK, MONO)
    d.t(x + BW / 2, BY + 74, note, 11.5, MUTED, KR)

d.tone(LX, 512, LW, 44, MUTED)
d.t(LX + 20, 540, "네트워크 갈래는 드라이버가 네트워크 연산을 포함한다는 이유로 저자가 7장으로 미룹니다.",
    12, MUTED, KR, "start")

d.legend(576, [("간접이 일어나는 층", ACC), ("블록 장치를 쓰는 갈래", OK),
               ("메모리에 사는 갈래", INFO), ("커널을 감싸는 갈래", WARN)])
d.save("05-01.vfs.svg")
print("ok 05-01.vfs")
