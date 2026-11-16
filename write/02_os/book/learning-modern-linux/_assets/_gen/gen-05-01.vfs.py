# 05-01 §4 — VFS 의 실제 자리. 다섯 범주의 파일 시스템 콜이 모두 VFS 로 들어오고, VFS 는 커널 객체
#           file · dentry · inode · super_block 을 거쳐 super_block 의 연산자 테이블(함수 포인터)로
#           파일시스템별 구현에 갈라 보낸다. 갈래 넷은 데이터가 머무는 곳이 서로 다르다.
# 타입 스펙: type-architecture — 시스템 콜 줄 → VFS 구역(객체 넷) → 파일시스템 부류 넷 → 데이터 자리.
#           accent 는 갈라지는 지점인 연산자 테이블.
# 근거: 본문 §4 의 시스템 콜 다섯 범주 표, include/linux/fs.h 의 자료구조 넷(inode · dentry · file ·
#       super_block)과 각 설명, 부류 넷 표(로컬 · 인메모리 · 가짜 · 네트워크와 데이터가 있는 곳),
#       "같은 read() 가 로컬 디스크 파일과 /proc 가상 파일을 다루는 것은 함수 포인터 분기 덕분".
#       객체 사이 화살표는 dentry 가 아이노드를 캐시하고 super_block 이 파일시스템 하나를 맡는다는
#       설명을 포인터로 그린 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 648
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §4",
      "시스템 콜은 VFS 객체를 지나 파일시스템마다 갈라진다",
      "파일 관련 시스템 콜 다섯 범주는 모두 VFS 로 들어온다. VFS 는 프로세스가 연 file, 경로를 캐시하는 "
      "dentry, 디스크 객체를 나타내는 inode, 마운트된 파일시스템 하나를 맡는 super_block 을 거쳐 "
      "super_block 의 연산자 테이블로 구현을 고른다. 로컬 파일시스템은 블록 장치로, tmpfs 는 RAM 으로, "
      "procfs 는 커널 상태로, NFS 는 원격 서버로 간다. 그래서 같은 read() 가 보통 파일과 /proc 파일을 함께 다룬다.",
      "VFS 는 시스템 콜과 파일시스템 구현 사이의 간접 층 — 갈라지는 자리는 함수 포인터다")

# 1줄 — 시스템 콜 다섯 범주
SY0, SY1 = 100, 152
CW5, G5, X5 = 168, 8, 24
calls = [("아이노드", "chmod·chown·stat"), ("파일", "open·read·write…"),
         ("디렉터리", "link·unlink·rename…"), ("파일시스템", "mount·umount·chroot"),
         ("기타", "mmap·poll·sync·flock")]

# VFS 구역과 객체 넷
VZ0, VZ1 = 196, 348
OY0, OY1 = 228, 336
CW4, G4, X4 = 184, 32, 44
cx4 = [X4 + i * (CW4 + G4) + CW4 / 2 for i in range(4)]
# 파일시스템 부류와 데이터 자리
BUS = 372
FY0, FY1 = 396, 476
DY0, DY1 = 504, 552

# VFS 구역 틀 — 연결선보다 먼저
d.box(24, VZ0, W - 48, VZ1 - VZ0, PAPER, INFO, 1.1, 10)
d.t(40, VZ0 + 20, "VFS", 13, INFO, MONO, "start", 600)
d.t(76, VZ0 + 20, "include/linux/fs.h 의 핵심 자료구조", 12, SOFT, KR, "start")

# 연결선은 상자보다 먼저
for i in range(5):
    cx = X5 + i * (CW5 + G5) + CW5 / 2
    d.arrow([(cx, SY1 + 2), (cx, VZ0 - 3)], MUTED, "ar", 1.2)
for i in range(3):
    d.arrow([(X4 + i * (CW4 + G4) + CW4 + 2, OY0 + 30), (X4 + (i + 1) * (CW4 + G4) - 3, OY0 + 30)],
            INFO, "info", 1.4)
d.path(f"M {cx4[3]} {OY1 + 2} L {cx4[3]} {BUS} L {cx4[0]} {BUS}", ACC, 1.6)
for x in cx4:
    d.arrow([(x, BUS), (x, FY0 - 3)], ACC, "acc", 1.4)
for x in cx4:
    d.arrow([(x, FY1 + 2), (x, DY0 - 3)], MUTED, "ar", 1.2)

# 시스템 콜 칸
for i, (cat, ex) in enumerate(calls):
    x = X5 + i * (CW5 + G5)
    d.box(x, SY0, CW5, SY1 - SY0, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, SY0 + 20, cat, 13, INK, KR, "start", 600)
    d.t(x + 12, SY0 + 40, ex, 12, MUTED, MONO, "start")

objs = [("file", "프로세스가 연 인스턴스", "오프셋 · 상태 플래그", None),
        ("dentry", "경로 탐색 캐시", "디렉터리 항목 ↔ 아이노드", None),
        ("inode", "디스크 상의 객체", "권한 · 소유자 · 크기", "블록 위치 포인터"),
        ("super_block", "마운트된 파일시스템 하나", "전체 메타데이터", None)]
for i, (name, l1, l2, l3) in enumerate(objs):
    x = X4 + i * (CW4 + G4)
    d.box(x, OY0, CW4, OY1 - OY0, PAPER2, INFO, 1.1, 8)
    d.t(x + 12, OY0 + 22, name, 14, INK, MONO, "start", 600)
    d.t(x + 12, OY0 + 48, l1, 12, MUTED, KR, "start")
    d.t(x + 12, OY0 + 68, l2, 12, MUTED, KR, "start")
    if l3:
        d.t(x + 12, OY0 + 88, l3, 12, MUTED, KR, "start")
# 연산자 테이블 (focal)
x = X4 + 3 * (CW4 + G4)
d.o.append(f'<rect x="{x + 12}" y="{OY0 + 78}" width="{CW4 - 24}" height="22" rx="4" '
           f'fill="{ACC}24" stroke="{ACC}" stroke-width="1.4"/>')
d.t(x + CW4 / 2, OY0 + 94, "연산자 테이블", 12, ACC, KR, "middle", 600)
d.t(cx4[3] + 12, BUS - 6, "함수 포인터로 분기", 12, ACC, KR, "start")

# 파일시스템 부류 넷
fss = [("로컬 파일시스템", "ext4·XFS·FAT·NTFS", "보통 파일의 read()"),
       ("인메모리", "tmpfs", None),
       ("가짜 파일시스템", "procfs·sysfs", "/proc 파일의 read()"),
       ("네트워크 파일시스템", "NFS·CIFS/Samba", None)]
for i, (name, ex, tag) in enumerate(fss):
    x = X4 + i * (CW4 + G4)
    d.box(x, FY0, CW4, FY1 - FY0, PAPER2, RULE, 1.0, 8)
    d.t(x + 12, FY0 + 22, name, 13, INK, KR, "start", 600)
    d.t(x + 12, FY0 + 44, ex, 12, MUTED, MONO, "start")
    if tag:
        d.t(x + 12, FY0 + 66, tag, 12, OK, KR, "start", 600)

# 데이터가 있는 곳
spots = [("SSD · HDD", "디바이스 드라이버"), ("RAM", "블록 장치 없음"),
         ("커널 내부 상태", "디바이스 모델"), ("원격 서버", "네트워크 드라이버")]
for i, (name, sub) in enumerate(spots):
    x = X4 + i * (CW4 + G4)
    d.o.append(f'<rect x="{x}" y="{DY0}" width="{CW4}" height="{DY1 - DY0}" rx="6" fill="none" '
               f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
    d.t(x + 12, DY0 + 21, name, 12, INK, KR, "start", 600)
    d.t(x + 12, DY0 + 39, sub, 12, SOFT, KR, "start")

d.t(24, 580, "점선 칸은 데이터가 머무는 곳 · 객체 사이 화살표는 본문 설명을 포인터로 그린 것", 11, SOFT, KR, "start")
LEG = 600
d.legend(LEG, [("VFS 자료구조", INFO), ("갈라지는 자리", ACC), ("같은 read() 의 두 갈래", OK)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.vfs.svg")
print("ok 05-01.vfs")
