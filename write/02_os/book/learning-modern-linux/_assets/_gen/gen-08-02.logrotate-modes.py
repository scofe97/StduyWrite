# 08-02 §4 — create 와 copytruncate 회전에서 쓰는 프로세스의 fd 1 이 어느 inode 를 가리키는지.
# 실측: debian:12 컨테이너, logrotate 3.21.0, 0.1초마다 `>>` 로 한 줄씩 덧붙이는 프로세스 + `logrotate -f` (2026-11-10).
#   create      : 전 4 app.log 260 → 직후 5 app.log 0 · 4 app.log.1 286 → 1초 뒤 5 app.log 0 · 4 app.log.1 520,
#                 /proc/3699/fd/1 -> /data/log/app.log.1
#   copytruncate: 전 6 app.log 260 → 직후 6 app.log 0 · 7 app.log.1 260 → 1초 뒤 6 app.log 260 · 7 app.log.1 260,
#                 /proc/3749/fd/1 -> /data/log/app.log
# 1차 자료: logrotate(8) create "Immediately after rotation ... the log file is created",
#           copytruncate "Truncate the original log file to zero size in place after creating a copy".
# 타입 스펙: type-swimlane — 레인 둘(회전 방식) × 열 셋(시점). 칸마다 파일 행(inode·이름·크기)과
#           fd 1 이 가리키는 행 표시. focal 은 create 1초 뒤에 커지는 app.log.1 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, RULE, PAPER2, KR, MONO

W, H = 960, 496
LX, LW = 24, 148
CX0, CW, CG = 188, 236, 14
LANE_Y, LANE_H, LANE_G = 132, 140, 16
ROW_H = 30
COLS = ["회전 전", "회전 직후", "1초 뒤"]

# (inode, 이름, 크기, 색, fd1 가 가리키는가)
LANES = [
    ("create", "이름 바꾸기 + 새 파일", [
        [(4, "app.log", 260, INFO, True)],
        [(5, "app.log", 0, SOFT, False), (4, "app.log.1", 286, INFO, True)],
        [(5, "app.log", 0, SOFT, False), (4, "app.log.1", 520, ACC, True)],
    ]),
    ("copytruncate", "복사 + 제자리 자르기", [
        [(6, "app.log", 260, INFO, True)],
        [(6, "app.log", 0, INFO, True), (7, "app.log.1", 260, SOFT, False)],
        [(6, "app.log", 260, OK, True), (7, "app.log.1", 260, SOFT, False)],
    ]),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §4",
      "회전 뒤 fd 1 이 가리키는 inode",
      "0.1초마다 한 줄씩 덧붙이는 프로세스를 두고 logrotate -f 로 돌렸다. 칸마다 inode · 이름 · 크기이고, "
      "▶ 표시가 쓰는 프로세스의 fd 1 이 가리키는 파일이다.",
      "create 는 inode 를 옮기고, copytruncate 는 같은 inode 를 0 으로 자릅니다")

for j, name in enumerate(COLS):
    x = CX0 + j * (CW + CG)
    d.t(x + CW / 2, LANE_Y - 14, name, 12.5, MUTED, KR, "middle", 600)

for i, (mode, sub, cells) in enumerate(LANES):
    y = LANE_Y + i * (LANE_H + LANE_G)
    d.box(LX, y, W - 2 * LX, LANE_H, PAPER2, RULE, 0.9, 8)
    d.t(LX + 16, y + 30, mode, 14, INK, MONO, "start", 600)
    d.t(LX + 16, y + 52, sub, 11.5, MUTED, KR, "start")
    for j, rows in enumerate(cells):
        x = CX0 + j * (CW + CG)
        for k, (ino, fname, size, c, fd) in enumerate(rows):
            ry = y + 22 + k * (ROW_H + 10)
            focal = c is ACC
            d.tone(x + 22, ry, CW - 22, ROW_H, c, 5, "2E" if focal else "14", 1.4 if focal else 0.9)
            d.t(x + 34, ry + 20, str(ino), 12, c, MONO, "start", 600)
            d.t(x + 56, ry + 20, fname, 12, INK if fd else MUTED, MONO, "start")
            d.t(x + CW - 12, ry + 20, f"{size} B", 12, c if size else SOFT, MONO, "end", 600 if focal else 400)
            if fd:
                d.t(x + 10, ry + 20, "▶", 11, c, MONO)
        ptr = [r for r in rows if r[4]][0]
        d.t(x + 22, y + LANE_H - 18, f"fd 1 → inode {ptr[0]}", 11.5,
            ptr[3] if ptr[3] in (ACC, OK) else MUTED, MONO, "start")

d.legend(H - 40, [("fd 1 이 가리키는 파일", INFO), ("옛 inode 로 계속 쌓임", ACC),
                  ("같은 이름으로 다시 자람", OK), ("쓰는 쪽이 없는 파일", SOFT)])
d.save("08-02.logrotate-modes.svg")
print("ok 08-02.logrotate-modes")
