# 05-01 §2 — 드라이브에서 아이노드까지 다섯 층위를 본문 출력의 실제 장치로 쌓는다. sda 가 sda1·sda2 로
#           나뉘고, sda2 위에 LVM 볼륨 root·swap_1 이 놓이며, ext4 로 포맷된 볼륨은 앞머리의 슈퍼블록,
#           아이노드, 데이터 블록으로 이루어진다. 아이노드는 이름도 데이터도 갖지 않는다.
# 타입 스펙: type-layers — 드라이브 → 파티션 → 볼륨 → 파일시스템 안(슈퍼블록 · 아이노드)으로 내려가는 층.
#           accent 는 아이노드.
# 근거: 본문 §2 의 lsblk 출력(sda 223.6G 8:0, sda1 512M /boot/efi, sda2 223.1G, elementary--vg-root
#       222.1G 253:0 /, elementary--vg-swap_1 976M [SWAP]), findmnt(elementary--vg-root ext4 217.6G /,
#       /dev/sda1 vfat /boot/ef), stat myfile(Inode 555036, Size 0, Links 1, 0664, Uid 1000, Gid 1001,
#       Device fc01h)과 슈퍼블록 · 아이노드 · 디렉터리 항목 설명.
# 축약: sda1·swap_1 칸은 읽히게 키웠다. 볼륨 안의 세 구역 배치는 개략이다. stat myfile 은 §3 이 밝히듯
#       장치 fc01h(252:1)의 파일이라 위 root(253:0)와 다른 볼륨의 예다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 652
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §2",
      "드라이브에서 아이노드까지 한 줄로 내려간다",
      "드라이브 sda 223.6G 는 파티션 sda1 512M 과 sda2 223.1G 로 나뉜다. sda1 은 vfat 으로 /boot/efi 에 붙고, "
      "sda2 위에는 LVM 볼륨 elementary--vg-root 222.1G 와 swap_1 976M 이 놓인다. ext4 로 포맷된 볼륨 안은 "
      "앞머리의 슈퍼블록, 아이노드, 데이터 블록으로 이루어진다. stat myfile 의 아이노드 555036 은 크기 · 링크 수 · "
      "권한 · 소유자를 갖지만 이름은 디렉터리 항목이, 내용은 데이터 블록이 갖는다.",
      "아이노드는 파일 이름과 실제 데이터를 저장하지 않는다")

LX = 24
X0, X1 = 164, 896
R1 = (100, 148)
R2 = (176, 224)
R3 = (252, 308)
R4 = (352, 400)
R5 = (440, 548)

for (y0, y1), name, sub, fam in ((R1, "드라이브", "disk", MONO), (R2, "파티션", "part", MONO),
                                 (R3, "볼륨", "lvm · fs", MONO), (R4, "파일시스템", "포맷된 볼륨 안", KR),
                                 (R5, "메타데이터", "슈퍼블록 · 아이노드", KR)):
    cy = (y0 + y1) / 2
    d.t(LX, cy - 2, name, 13, INK, KR, "start", 600)
    d.t(LX, cy + 16, sub, 11, SOFT, fam, "start")

# 파티션·볼륨 열
P1 = (X0, 324)              # sda1
P2 = (340, X1)              # sda2
VR = (340, 752)             # root
VS = (768, X1)              # swap_1

# 연결선·확대 띠는 상자보다 먼저
for x in ((P1[0] + P1[1]) / 2, (P2[0] + P2[1]) / 2):
    d.line(x, R1[1] + 2, x, R2[0] - 2, INFO, 1.2)
d.line((P1[0] + P1[1]) / 2, R2[1] + 2, (P1[0] + P1[1]) / 2, R3[0] - 2, MUTED, 1.2)
for x in ((VR[0] + VR[1]) / 2, (VS[0] + VS[1]) / 2):
    d.line(x, R2[1] + 2, x, R3[0] - 2, OK, 1.2)
d.o.append(f'<path d="M {VR[0]} {R3[1]} L {VR[1]} {R3[1]} L {X1} {R4[0]} L {X0} {R4[0]} Z" '
           f'fill="{INFO}14" stroke="none"/>')
d.t((VR[0] + VR[1]) / 2, R3[1] + 30, "ext4 볼륨 하나를 열면 (개략)", 12, SOFT, KR)
SB = (X0, 324)
IN = (332, 600)
DB = (608, X1)
CS = (X0, 392)              # 슈퍼블록 카드
CI = (416, 664)             # 아이노드 카드
CD = (712, X1)              # 디렉터리 항목 카드
d.line(240, R4[1] + 2, 240, R5[0] - 2, INFO, 1.2)
NC, PICK = 10, 5
CWI = (IN[1] - IN[0] - 24) / NC
XP = IN[0] + 12 + (PICK + 0.5) * CWI           # 확대한 아이노드 칸의 중심
d.line(XP, R4[1] + 2, XP, R5[0] - 2, ACC, 1.2, "3 3")
d.t(XP + 12, R4[1] + 26, "한 칸", 12, ACC, KR, "start")
d.arrow([(640, R5[0] - 2), (640, R4[1] + 3)], MUTED, "ar", 1.3)
d.t(652, R4[1] + 26, "저장 위치", 12, MUTED, KR, "start")
d.arrow([(CD[0] - 2, 494), (CI[1] + 3, 494)], MUTED, "ar", 1.3)

# 1층 — 드라이브
d.tone(X0, R1[0], X1 - X0, R1[1] - R1[0], INFO)
d.t(X0 + 14, R1[0] + 29, "/dev/sda", 14, INK, MONO, "start", 600)
d.t(X1 - 14, R1[0] + 29, "223.6G · 8:0 · disk", 12, MUTED, MONO, "end")

# 2층 — 파티션
for (x0, x1), name, sub in ((P1, "sda1", "512M · 8:1"), (P2, "sda2", "223.1G · 8:2")):
    d.box(x0, R2[0], x1 - x0, R2[1] - R2[0], PAPER2, INFO, 1.1, 6)
    d.t(x0 + 12, R2[0] + 29, name, 13, INK, MONO, "start", 600)
    d.t(x1 - 12, R2[0] + 29, sub, 12, MUTED, MONO, "end")

# 3층 — 볼륨
x0, x1 = P1
d.o.append(f'<rect x="{x0}" y="{R3[0]}" width="{x1 - x0}" height="{R3[1] - R3[0]}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(x0 + 12, R3[0] + 22, "vfat", 13, INK, MONO, "start", 600)
d.t(x0 + 12, R3[0] + 42, "/boot/efi", 12, MUTED, MONO, "start")
x0, x1 = VR
d.tone(x0, R3[0], x1 - x0, R3[1] - R3[0], OK)
d.t(x0 + 12, R3[0] + 22, "elementary--vg-root", 13, INK, MONO, "start", 600)
d.t(x1 - 12, R3[0] + 22, "222.1G · 253:0", 12, MUTED, MONO, "end")
d.t(x0 + 12, R3[0] + 42, "ext4 · 217.6G → /", 12, OK, MONO, "start")
x0, x1 = VS
d.box(x0, R3[0], x1 - x0, R3[1] - R3[0], PAPER2, OK, 1.1, 6)
d.t(x0 + 12, R3[0] + 22, "swap_1", 13, INK, MONO, "start", 600)
d.t(x0 + 12, R3[0] + 42, "976M [SWAP]", 12, MUTED, MONO, "start")

# 4층 — 볼륨 안의 세 구역
x0, x1 = SB
d.tone(x0, R4[0], x1 - x0, R4[1] - R4[0], INFO, 4)
d.t(x0 + 12, R4[0] + 29, "슈퍼블록", 13, INK, KR, "start", 600)
d.t(x1 - 12, R4[0] + 29, "앞머리", 12, MUTED, KR, "end")
x0, x1 = IN
d.box(x0, R4[0], x1 - x0, R4[1] - R4[0], PAPER2, ACC, 1.1, 4)
for i in range(NC):
    c = ACC if i == PICK else RULE
    d.o.append(f'<rect x="{x0 + 12 + i * CWI + 1:.1f}" y="{R4[0] + 30}" width="{CWI - 2:.1f}" height="10" rx="2" '
               f'fill="{ACC}{"66" if i == PICK else "14"}" stroke="{c}" stroke-width="0.8"/>')
d.t(x0 + 12, R4[0] + 21, "아이노드들", 13, INK, KR, "start", 600)
x0, x1 = DB
d.box(x0, R4[0], x1 - x0, R4[1] - R4[0], PAPER2, RULE, 1.0, 4)
d.t(x0 + 12, R4[0] + 29, "데이터 블록", 13, INK, KR, "start", 600)
d.t(x1 - 12, R4[0] + 29, "파일 내용 · 디렉터리 내용", 12, MUTED, KR, "end")

# 5층 — 슈퍼블록 · 아이노드 · 디렉터리 항목
x0, x1 = CS
d.box(x0, R5[0], x1 - x0, R5[1] - R5[0], PAPER2, INFO, 1.1, 8)
d.t(x0 + 14, R5[0] + 24, "슈퍼블록", 13, INFO, KR, "start", 600)
d.t(x0 + 14, R5[0] + 50, "파일시스템 종류", 12, MUTED, KR, "start")
d.t(x0 + 14, R5[0] + 70, "전체 블록 수 · 블록 크기", 12, MUTED, KR, "start")
d.t(x0 + 14, R5[0] + 90, "블록 그룹당 아이노드 수", 12, MUTED, KR, "start")
x0, x1 = CI
d.tone(x0, R5[0], x1 - x0, R5[1] - R5[0], ACC, 8, "1F", 1.4)
d.t(x0 + 14, R5[0] + 24, "Inode: 555036", 14, ACC, MONO, "start", 600)
d.t(x0 + 14, R5[0] + 50, "Size: 0 · Links: 1", 12, INK, MONO, "start")
d.t(x0 + 14, R5[0] + 70, "0664 · Uid 1000 · Gid 1001", 12, INK, MONO, "start")
d.t(x0 + 14, R5[0] + 94, "이름 없음 · 데이터 없음", 12, ACC, KR, "start", 600)
x0, x1 = CD
d.box(x0, R5[0], x1 - x0, R5[1] - R5[0], PAPER2, RULE, 1.0, 8)
d.t(x0 + 14, R5[0] + 24, "디렉터리 항목", 13, INK, KR, "start", 600)
d.t(x0 + 14, R5[0] + 58, "myfile → 555036", 13, INK, MONO, "start", 600)
d.t(x0 + 14, R5[0] + 82, "이름은 여기에", 12, MUTED, KR, "start")

d.t(LX, 576, "lsblk · findmnt · stat 출력 값 · sda1·swap_1 칸은 키움 · stat myfile 은 장치 fc01h 의 예라 root(253:0) 와 다른 볼륨",
    11, SOFT, KR, "start")
LEG = 600
d.legend(LEG, [("장치 · 슈퍼블록", INFO), ("LVM 볼륨", OK), ("아이노드", ACC)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.storage-terms.svg")
print("ok 05-01.storage-terms")
