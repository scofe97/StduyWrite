# 08-01 §7 — logrotate 의 이름 바꾸기와 copytruncate 가 쓰던 프로세스에 하는 일.
# 실측(Debian 12 컨테이너, logrotate 3.21.0, 0.2초마다 한 줄을 붙이는 셸 루프):
#   create 0640 root adm 로 logrotate -f 전후 — app.log 4131778(111 B) → app.log 4132348(0 B, root adm),
#   app.log.1 4131778(111 B, 15 줄), /proc/3502/fd/1 -> /srv/demo/app.log.1, 1초 뒤 줄 수 app.log 0 · app.log.1 20.
#   (2026-11-10 검증 창 재실측. 첫 실측 기록은 회전 직후 180 B 와 1초 뒤 15 줄이 서로 맞지 않아 바꿨다.)
#   copytruncate — app.log 의 inode 4132350 이 전후 같고, app.log.1 은 새 inode 4132351 에 다섯 줄.
# 1차 자료: logrotate(8) create·postrotate·copytruncate("some logging data might be lost").
# 타입 스펙: type-swimlane — 두 방식(lane)이 같은 세 시점(단계)을 지나며 파일 이름과 inode 의
#           짝이 어떻게 바뀌는지 보인다. accent 는 fd 가 옛 inode 를 따라간 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 496
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "이름을 바꾸면 fd 는 inode 를 따라가고 copytruncate 는 inode 를 남긴다",
      "컨테이너에서 0.2초마다 한 줄을 붙이는 루프를 두고 logrotate -f 로 강제 회전한 전후. "
      "숫자는 ls -i 로 본 inode 다.",
      "새 app.log 는 비어 있고 옛 inode 인 app.log.1 만 자랍니다")

LX, LW = 24, 120
CX = [160, 392, 624]
CW = 216
HEAD = ["회전 전", "logrotate -f 직후", "그 뒤"]
for x, h in zip(CX, HEAD):
    d.t(x + CW / 2, 112, h, 12, MUTED, KR, "middle", 600)

ROWS = [
    ("rename + create", "create 0640", 128, 156, [
        [("app.log · 4131778 · 111 B", RULE, INK)],
        [("app.log · 4132348 · 0 B", INFO, INFO), ("app.log.1 · 4131778 · 111 B", RULE, INK)],
        [("app.log · 0 줄", INFO, INFO), ("app.log.1 · 20 줄", RULE, INK)],
    ], ["fd 1 → app.log", "/proc/3502/fd/1 → app.log.1", "postrotate 신호 → 다시 열기"]),
    ("copytruncate", "inode 유지", 316, 124, [
        [("app.log · 4132350", RULE, INK)],
        [("app.log · 4132350 · 0 B", RULE, INK), ("app.log.1 · 4132351 · 5 줄", INFO, INFO)],
        [("app.log · 4132350", RULE, INK)],
    ], ["fd 1 → 4132350", "fd 1 → 4132350", "신호 불필요"]),
]

for rname, rsub, ry, rh, cells, fds in ROWS:
    d.box(LX, ry, LW, rh, PAPER2, RULE, 1.1, 6)
    d.t(LX + 12, ry + 28, rname, 11, INK, MONO, "start", 600)
    d.t(LX + 12, ry + 48, rsub, 11, MUTED, MONO if rsub.isascii() else KR, "start")
    for k, (x, cards, fd) in enumerate(zip(CX, cells, fds)):
        focal = (rname.startswith("rename") and k == 1)
        if focal:
            d.tone(x, ry, CW, rh, ACC, 6, "10", 1.4)
        else:
            d.box(x, ry, CW, rh, PAPER2, RULE, 0.9, 6)
        for j, (txt, stroke, col) in enumerate(cards):
            cy = ry + 16 + j * 40
            d.box(x + 12, cy, CW - 24, 30, "#0D1117", stroke, 1.0, 4)
            d.t(x + 22, cy + 20, txt, 11, col, MONO if txt.isascii() else KR, "start")
        fy = ry + rh - 18
        d.t(x + 14, fy, fd, 11, ACC if focal else MUTED, MONO if fd.isascii() else KR,
            "start", 600 if focal else 400)
        if k < 2:
            d.arrow([(x + CW + 2, ry + rh / 2), (CX[k + 1] - 4, ry + rh / 2)], MUTED, "ar", 1.2)

d.chip(CX[2] + CW / 2, 316 + 72, "복사와 자르기 사이 유실 가능", WARN, 11)

d.legend(456 - 4, [("fd 가 옛 inode 를 따라간 칸", ACC), ("새로 생긴 inode", INFO),
                   ("유실 위험", WARN)])
d.save("08-01.logrotate-inode.svg")
print("ok 08-01.logrotate-inode")
