# 08-01 §4 「옛 inode 에 남는 쓰기와 copytruncate」 — logrotate 의 이름 바꾸기와 copytruncate 가
#           쓰던 프로세스에 하는 일을 이름 → inode ← fd 의 실제 연결로 보인다.
# 실측(본문 §4 컨테이너, 0.2초마다 한 줄을 붙이는 셸 루프 PID 3502):
#   create 0640 root adm 로 logrotate -f 전후 — app.log 4131778(111 B) → app.log 4132348(0 B, root adm),
#   app.log.1 4131778(111 B), /proc/3502/fd/1 -> /srv/demo/app.log.1, 1초 뒤 줄 수 app.log 0 · app.log.1 20.
#   copytruncate — app.log 의 inode 4132350 이 전후 같고, app.log.1 은 새 inode 4132351 에 다섯 줄.
# 1차 자료: logrotate(8) create·postrotate·copytruncate("some logging data might be lost",
#   copytruncate 를 쓰면 create 는 효과가 없다).
# 구조: 칸마다 왼쪽이 디렉터리의 이름, 가운데가 inode, 아래가 프로세스의 fd 1 이다. fd 화살표는 이름이
#   아니라 inode 에 꽂힌다. 그래서 이름을 바꿔도 fd 는 같은 inode(app.log.1) 를 계속 가리킨다.
# 축약: copytruncate 의 회전 전 크기는 본문에 없어 적지 않았다. 복사와 자르기 사이의 틈은 길이를 재지
#   않았으므로 띠 길이는 비율이 아니다.
# 타입 스펙: type-swimlane — 두 방식(lane)이 같은 세 시점을 지나며 이름·inode·fd 의 연결이 어떻게
#           바뀌는지 보인다. accent 는 fd 가 옛 inode 를 따라간 연결 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 564
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "이름을 바꾸면 fd 는 inode 를 따라가고 copytruncate 는 inode 를 남긴다",
      "0.2초마다 한 줄을 붙이는 셸 루프(PID 3502)를 두고 logrotate -f 로 강제 회전한 전후. 이름 바꾸기 방식에서는 "
      "app.log 가 새 inode 4132348 을 받지만 fd 1 은 옛 inode 4131778(이제 app.log.1)을 계속 가리켜, 1초 뒤 "
      "app.log 는 0 줄, app.log.1 은 20 줄이다. copytruncate 는 app.log 의 inode 4132350 을 그대로 두고 "
      "새 inode 4132351 에 다섯 줄을 복사한 뒤 원본을 자른다.",
      "fd 는 이름이 아니라 inode 를 가리킨다 — 이름을 바꿔도 쓰기는 옛 inode 로 간다")

LX, LW = 24, 108
CX = [136, 400, 664]
CW = 248
HEAD = ["회전 전", "logrotate -f 직후", "그 뒤"]
for x, h in zip(CX, HEAD):
    d.t(x + CW / 2, 112, h, 13, MUTED, KR if any("가" <= c <= "힣" for c in h) else MONO, "middle", 600)

RH = 176
R1, R2 = 128, 128 + RH + 20


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cell(x, y, rows, fd_to, fd_col=MUTED, fd_mk="ar", note=None, note_col=SOFT, focal=False):
    """rows: [(이름, inode, 아래줄, 새 inode 인가)], fd_to: rows 의 인덱스"""
    if focal:
        d.tone(x, y, CW, RH, ACC, 8, "0D", 1.4)
    else:
        d.box(x, y, CW, RH, PAPER2, RULE, 0.9, 8)
    for i, (nm, ino, sub, new) in enumerate(rows):
        iy = y + 16 + i * 52
        c = INFO if new else MUTED
        d.box(x + 12, iy + 7, 84, 30, PAPER, RULE, 1.0, 4)
        d.t(x + 54, iy + 27, nm, 12, INK, MONO, "middle", 600)
        d.arrow([(x + 98, iy + 22), (x + 124, iy + 22)], MUTED, "ar", 1.1)
        d.box(x + 128, iy, 96, 44, PAPER, c if new else SOFT, 1.2, 4)
        d.t(x + 176, iy + 19, ino, 12, INFO if new else INK, MONO, "middle", 600)
        d.t(x + 176, iy + 36, sub, 11, MUTED, kr(sub))
    fy = y + 124
    d.box(x + 128, fy, 96, 24, PAPER, fd_col, 1.2, 4)
    d.t(x + 176, fy + 17, "fd 1", 12, fd_col, MONO, "middle", 600)
    ty = y + 16 + fd_to * 52 + 22
    d.arrow([(x + 224, fy + 12), (x + 238, fy + 12), (x + 238, ty), (x + 228, ty)], fd_col, fd_mk, 1.5)
    if note:
        d.t(x + 12, y + RH - 12, note, 11, note_col, kr(note), "start", 600 if focal else 400)


# 행 이름
for y, nm, sub in ((R1, "rename", "+ create"), (R2, "copytruncate", "inode 유지")):
    d.box(LX, y, LW, RH, PAPER2, RULE, 1.1, 8)
    d.t(LX + 10, y + 28, nm, 12, INK, MONO, "start", 600)
    d.t(LX + 10, y + 48, sub, 11, MUTED, kr(sub), "start")
d.t(LX + 10, R1 + 72, "0640", 11, SOFT, MONO, "start")
d.t(LX + 10, R1 + 88, "root adm", 11, SOFT, MONO, "start")

# 1행 — 이름 바꾸기 + create
cell(CX[0], R1, [("app.log", "4131778", "111 B", False)], 0,
     note="PID 3502 가 붙여 씀")
cell(CX[1], R1, [("app.log", "4132348", "0 B", True),
                 ("app.log.1", "4131778", "111 B", False)], 1, ACC, "acc",
     note="/proc/3502/fd/1 → app.log.1", note_col=ACC, focal=True)
cell(CX[2], R1, [("app.log", "4132348", "1초 뒤 0 줄", True),
                 ("app.log.1", "4131778", "1초 뒤 20 줄", False)], 1, ACC, "acc",
     note="postrotate 신호로 다시 열어야 함")

# 2행 — copytruncate
cell(CX[0], R2, [("app.log", "4132350", "", False)], 0)
cell(CX[1], R2, [("app.log", "4132350", "잘려 0 B", False),
                 ("app.log.1", "4132351", "복사본 5 줄", True)], 0, OK, "ok",
     note="fd 는 그대로 4132350")

# 2행 3칸 — 복사와 자르기 사이의 틈
x, y = CX[2], R2
d.box(x, y, CW, RH, PAPER2, RULE, 0.9, 8)
d.t(x + 12, y + 26, "copytruncate 한 번의 순서", 12, MUTED, KR, "start", 600)
BY = y + 72
d.box(x + 12, BY - 14, 72, 28, PAPER, INFO, 1.1, 4)
d.t(x + 48, BY + 5, "복사", 12, INFO, KR, "middle", 600)
d.tone(x + 92, BY - 14, 64, 28, WARN, 4, "22", 1.2)
d.t(x + 124, BY + 5, "틈", 12, WARN, KR, "middle", 600)
d.box(x + 164, BY - 14, 72, 28, PAPER, MUTED, 1.1, 4)
d.t(x + 200, BY + 5, "자르기", 12, INK, KR, "middle", 600)
d.t(x + 124, BY + 38, "이 사이 쓴 줄 유실 가능", 12, WARN, KR, "middle", 600)
d.t(x + 12, y + RH - 32, "신호 불필요", 12, OK, KR, "start")
d.t(x + 12, y + RH - 12, "create 는 효과 없음", 11, SOFT, KR, "start")

# 칸 사이 시간 화살표
for y in (R1, R2):
    for k in range(2):
        d.arrow([(CX[k] + CW + 2, y + RH / 2), (CX[k + 1] - 4, y + RH / 2)], SOFT, "soft", 1.1)

LGY = R2 + RH + 20
d.legend(LGY, [("fd 가 옛 inode 를 따라감", ACC), ("새로 생긴 inode", INFO),
               ("fd 가 같은 inode 에 남음", OK), ("유실 틈", WARN)])
d.save("08-01.logrotate-inode.svg")
print("ok 08-01.logrotate-inode")
