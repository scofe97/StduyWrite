# 02-01 §4 — 없는 방을 있는 것처럼 파는 법
# 타입 스펙: type-data-flow — 가상 주소가 페이지 테이블을 거쳐 물리 메모리로 사상되는 경로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, OK, WARN, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §4",
      "페이지 테이블 매핑 — 프로세스 격리와 물리 메모리 공유",
      "각 프로세스는 독립된 가상 주소 공간을 보지만, 페이지 테이블을 거쳐 공유 라이브러리는 같은 물리 페이지 한 벌을 가리킨다.",
      "프로세스별 페이지 테이블을 통한 전용 메모리 격리 vs 라이브러리(libc.so) 물리 메모리 공유")

# 영역 1: 가상 주소 공간 (좌측)
VX = 30
VW = 225
# 영역 2: 페이지 테이블 (가운데)
PTX = 295
PTW = 230
# 영역 3: 물리 메모리 (우측)
PX = 575
PW = 275

# 상단: 프로세스 A
Y_A = 100
H_A = 180
d.box(VX, Y_A, VW, H_A, PAPER2, RULE, 1.0, 8)
d.t(VX + 14, Y_A + 22, "프로세스 A 가상 공간", 12, INK, KR, "start", 600)
d.chip(VX + 182, Y_A + 20, "PID 6756", INFO, 11)

pages_a = [
    ("가상 페이지 0", "힙", INFO),
    ("가상 페이지 1", "스택", INFO),
    ("가상 페이지 2", "libc.so 코드", OK),
]
for k, (pname, paddr, pc) in enumerate(pages_a):
    py = Y_A + 40 + k * 44
    d.box(VX + 10, py, VW - 20, 38, PAPER, RULE, 0.8, 4)
    d.t(VX + 18, py + 16, pname, 11, pc, KR, "start", 600)
    d.t(VX + 18, py + 30, paddr, 11, MUTED, KR, "start")

# 페이지 테이블 A
d.box(PTX, Y_A, PTW, H_A, PAPER2, ACC, 1.0, 8)
d.t(PTX + 14, Y_A + 22, "프로세스 A 페이지 테이블", 12, ACC, KR, "start", 600)

entries_a = [
    ("VPN 0 → PFN 10", "물리 프레임 10 매핑", INFO),
    ("VPN 1 → PFN 25", "물리 프레임 25 매핑", INFO),
    ("VPN 2 → PFN 99", "공유 프레임 99 매핑", OK),
]
for k, (ename, edesc, ec) in enumerate(entries_a):
    ey = Y_A + 40 + k * 44
    d.box(PTX + 10, ey, PTW - 20, 38, PAPER, RULE, 0.8, 4)
    d.t(PTX + 18, ey + 16, ename, 11, ec, MONO, "start", 600)
    d.t(PTX + 18, ey + 30, edesc, 11, MUTED, KR, "start")

# 하단: 프로세스 B
Y_B = 296
H_B = 180
d.box(VX, Y_B, VW, H_B, PAPER2, RULE, 1.0, 8)
d.t(VX + 14, Y_B + 22, "프로세스 B 가상 공간", 12, INK, KR, "start", 600)
d.chip(VX + 182, Y_B + 20, "PID 6790", WARN, 11)

pages_b = [
    ("가상 페이지 2", "libc.so 코드", OK),
    ("가상 페이지 0", "힙", WARN),
    ("가상 페이지 1", "스택", WARN),
]
for k, (pname, paddr, pc) in enumerate(pages_b):
    py = Y_B + 40 + k * 44
    d.box(VX + 10, py, VW - 20, 38, PAPER, RULE, 0.8, 4)
    d.t(VX + 18, py + 16, pname, 11, pc, KR, "start", 600)
    d.t(VX + 18, py + 30, paddr, 11, MUTED, KR, "start")

# 페이지 테이블 B
d.box(PTX, Y_B, PTW, H_B, PAPER2, ACC, 1.0, 8)
d.t(PTX + 14, Y_B + 22, "프로세스 B 페이지 테이블", 12, ACC, KR, "start", 600)

entries_b = [
    ("VPN 2 → PFN 99", "공유 프레임 99 매핑", OK),
    ("VPN 0 → PFN 40", "물리 프레임 40 매핑", WARN),
    ("VPN 1 → PFN 55", "물리 프레임 55 매핑", WARN),
]
for k, (ename, edesc, ec) in enumerate(entries_b):
    ey = Y_B + 40 + k * 44
    d.box(PTX + 10, ey, PTW - 20, 38, PAPER, RULE, 0.8, 4)
    d.t(PTX + 18, ey + 16, ename, 11, ec, MONO, "start", 600)
    d.t(PTX + 18, ey + 30, edesc, 11, MUTED, KR, "start")

# 우측: 물리 메모리 (RAM)
PHY_Y = 100
PHY_H = 376
d.box(PX, PHY_Y, PW, PHY_H, PAPER2, RULE, 1.0, 8)
d.t(PX + 16, PHY_Y + 22, "주 메모리 (물리 RAM)", 13, INK, KR, "start", 600)
d.chip(PX + 220, PHY_Y + 20, "물리 프레임", SOFT, 11)

frames = [
    ("프레임 10", "프로세스 A 전용 힙", INFO, PAPER),
    ("프레임 25", "프로세스 A 전용 스택", INFO, PAPER),
    ("프레임 99", "libc.so 코드 (공유 한 벌 · 읽기 전용)", OK, f"{OK}15"),
    ("프레임 40", "프로세스 B 전용 힙", WARN, PAPER),
    ("프레임 55", "프로세스 B 전용 스택", WARN, PAPER),
]

frame_y = {}
for k, (fname, fdesc, fc, ffill) in enumerate(frames):
    fy = PHY_Y + 44 + k * 64
    fh = 54
    frame_y[fname] = fy + fh / 2
    d.box(PX + 12, fy, PW - 24, fh, ffill, fc, 1.2 if fc == OK else 0.8, 6)
    d.t(PX + 22, fy + 20, fname, 12, fc, MONO, "start", 600)
    d.t(PX + 22, fy + 40, fdesc, 11, INK if fc == OK else MUTED, KR, "start")

# 화살표 연결 1: 가상 페이지 -> 페이지 테이블 (A) (수평 직교)
for k in range(3):
    y = Y_A + 59 + k * 44
    c = OK if k == 2 else INFO
    d.arrow([(VX + VW - 10, y), (PTX + 8, y)], c, "ok" if k == 2 else "info", 1.0)

# 화살표 연결 2: 가상 페이지 -> 페이지 테이블 (B) (수평 직교)
for k in range(3):
    y = Y_B + 59 + k * 44
    c = OK if k == 0 else WARN
    d.arrow([(VX + VW - 10, y), (PTX + 8, y)], c, "ok" if k == 0 else "warn", 1.0)

# 직교 화살표 연결 3: 페이지 테이블 -> 물리 메모리
mid_pt_ram = (PTX + PTW + PX) / 2  # (525 + 575) / 2 = 550

def ortho_arrow(x1, y1, x2, y2, c, m, sw=1.1):
    if abs(y1 - y2) < 2:
        d.arrow([(x1, y1), (x2, y2)], c, m, sw)
    else:
        d.arrow([(x1, y1), (mid_pt_ram, y1), (mid_pt_ram, y2), (x2, y2)], c, m, sw)

# A의 프레임 10, 25, 99
ortho_arrow(PTX + PTW - 10, Y_A + 59, PX + 10, frame_y["프레임 10"], INFO, "info", 1.1)
ortho_arrow(PTX + PTW - 10, Y_A + 103, PX + 10, frame_y["프레임 25"], INFO, "info", 1.1)
ortho_arrow(PTX + PTW - 10, Y_A + 147, PX + 10, frame_y["프레임 99"] - 4, OK, "ok", 1.4)

# B의 프레임 99, 40, 55
ortho_arrow(PTX + PTW - 10, Y_B + 59, PX + 10, frame_y["프레임 99"] + 4, OK, "ok", 1.4)
ortho_arrow(PTX + PTW - 10, Y_B + 103, PX + 10, frame_y["프레임 40"], WARN, "warn", 1.1)
ortho_arrow(PTX + PTW - 10, Y_B + 147, PX + 10, frame_y["프레임 55"], WARN, "warn", 1.1)

# 범례
d.legend(496, [
    ("프로세스 A 전용", INFO),
    ("프로세스 B 전용", WARN),
    ("공유 물리 프레임", OK),
    ("페이지 테이블", ACC),
])

d.save("02-01.page-table-share.svg")
print("ok 02-01.page-table-share")
