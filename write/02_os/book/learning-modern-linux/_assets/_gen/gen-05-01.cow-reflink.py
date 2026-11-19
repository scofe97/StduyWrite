# 05-01 §8 — CoW 를 실측 값으로. btrfs 에서 64 MiB 파일을 cp --reflink=always 로 복사하면 두 파일이
#           같은 물리 extent 를 가리키고(shared), copy.bin 의 블록 8192 하나를 덮어쓰면 그 블록만
#           새 물리 위치 6602470 으로 가고 나머지는 계속 공유한다.
# 타입 스펙: type-architecture-delta — 같은 extent 배치의 전(복사 직후)·후(4 KiB 덮어쓴 뒤) 두 컷.
#           생긴 것(새 블록 6602470)과 다시 이어진 것(copy.bin 의 블록 8192)을 표시한다. accent 는 새 블록.
#           형제 도식 05-01.cow 의 두 컷 배치·색(file1=info, file2=ok)을 그대로 쓴다.
# 근거: 실측(OrbStack lml-ubuntu, btrfs, 커널 7.2.12-orbstack, coreutils 9.4, 2026-11-16), 폴더 /root/lml-0501/cow.
#   dd if=/dev/urandom of=orig.bin bs=1M count=64 → cp --reflink=always orig.bin copy.bin
#   filefrag -v 두 파일: 0..16383 → 5282848..5299231, 16384 블록, last,shared,eof
#   dd if=/dev/zero of=copy.bin bs=4K count=1 seek=8192 conv=notrunc → sync → filefrag -v copy.bin:
#     0..8191 → 5282848..5291039 shared / 8192 → 6602470 / 8193..16383 → 5291041..5299231 shared
#     orig.bin 은 0..16383 → 5282848..5299231 그대로
#   df -B1 used 차이: reflink 복사 +0, 덮어쓰기 +4096, cp --reflink=never +67108864
#   btrfs 는 덮어쓸 블록을 새 자리에 쓰므로 "복사 후 쓰기" 화살표는 두지 않는다.
# 산수(실측값에서 나온 계산이며 filefrag 출력에는 없다):
#   블록 하나 = 4 KiB = 4096 B (dd bs=4K, df +4096 이 블록 1개). 16384 블록 × 4096 B = 67108864 B = 64 MiB.
#   orig.bin 은 한 extent(5282848..5299231)라서 파일 칸 8192 의 디스크 칸은 5282848 + 8192 = 5291040.
#   5291039 와 5291041 사이에 빠진 번호가 이것이고, 덮어쓴 뒤에는 orig.bin 만 가리킨다.
# 이번 개정(2026-11-19): 숫자가 주인공이던 배치를 칸 띠 + 화살표로 바꿨다. 칸 폭은 축척이 아니다
#   (앞 구간·8192 번 칸·뒤 구간을 192·80·192 px 로 두고 8192 번 칸만 확대). 숫자는 보조 라벨이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W = 880
LX = 24                                   # 행 이름 열
BX0 = 200
LW, PW, RW = 192, 80, 192                 # 앞 구간 · 확대한 8192 번 칸 · 뒤 구간 (축척 아님)
MX0 = BX0 + LW
MX1 = MX0 + PW
BX1 = MX1 + RW
MC = (MX0 + MX1) / 2
QL, QR = (BX0 + MX0) / 2, (MX1 + BX1) / 2  # 앞·뒤 구간 가운데: 화살표 자리
NX, NW = 704, 104                         # 새 디스크 칸 자리
BAR_H, GAP = 44, 48
PANEL_Y, PANEL_H = 96, 72
CW, CG = 264, 20                          # 읽는 법 패널·df 카드 폭과 간격 (3열이 24..856 에 맞는다)

H = 1064
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "reflink 복사는 디스크 칸을 함께 쓰고, 덮어쓴 한 칸만 갈라진다",
      "btrfs 에서 64 MiB 파일 orig.bin 을 cp --reflink=always 로 copy.bin 에 복사한 실측이다. 칸 하나는 4 KiB 이고, "
      "파일 칸 번호는 파일 안에서의 순서, 디스크 칸 번호는 filefrag 가 보여 주는 디스크 위치다. 복사 직후에는 두 파일의 "
      "파일 칸 0 부터 16383 이 모두 디스크 칸 5282848 부터 5299231 을 함께 가리킨다. copy.bin 의 파일 칸 8192 를 "
      "4 KiB 덮어쓰면 그 한 칸만 새 디스크 칸 6602470 을 가리키고, 나머지는 계속 같은 디스크 칸을 함께 쓴다. "
      "orig.bin 은 그대로다. df 사용량은 reflink 복사에 0 바이트, 덮어쓰기에 4096 바이트(1칸), "
      "cp --reflink=never 복사에 67108864 바이트(64 MiB)가 늘었다.",
      "btrfs 실측 · 64 MiB 파일 · 한 칸 = 4 KiB — 공유는 그대로 두고 쓴 칸 하나만 새 자리로")


def ticks(x0, x1, y):
    """칸 띠 눈금: 위·아래 가장자리에만 짧게 그려 글자와 닿지 않게 한다."""
    x = x0 + 16
    while x < x1 - 8:
        d.line(x, y + 1, x, y + 7, SOFT, 0.8)
        d.line(x, y + BAR_H - 7, x, y + BAR_H - 1, SOFT, 0.8)
        x += 16


def file_cell(x0, x1, y, lab, c, hot=False):
    """파일 칸 띠의 한 구간. hot 이면 덮어쓴 칸(accent)."""
    if hot:
        d.tone(x0, y, x1 - x0, BAR_H, ACC, 4, "1F", 1.6)
    else:
        d.tone(x0, y, x1 - x0, BAR_H, c, 4, "1F", 1.1)
        if x1 - x0 > PW:
            ticks(x0, x1, y)
    d.t((x0 + x1) / 2, y + 27, lab, 12, ACC if hot else c, MONO, "middle", 600)


def file_bar(y, name, c, labs, hot=False):
    d.t(LX, y + 20, name, 14, c, MONO, "start", 600)
    d.t(LX, y + 36, "파일 칸 번호", 12, MUTED, KR, "start")
    file_cell(BX0, MX0, y, labs[0], c)
    file_cell(MX0, MX1, y, labs[1], c, hot)
    file_cell(MX1, BX1, y, labs[2], c)


def disk_cell(x0, x1, y, lines, kind):
    """디스크 칸 띠의 한 구간. kind: shared(함께 쓰는 칸) · orig(orig 만 쓰는 칸) · new(새로 쓴 칸)"""
    if kind == "new":
        d.tone(x0, y, x1 - x0, BAR_H, ACC, 4, "1F", 1.6)
        col = ACC
    elif kind == "orig":
        d.tone(x0, y, x1 - x0, BAR_H, INFO, 4, "33", 1.1)
        col = INFO
    else:
        d.box(x0, y, x1 - x0, BAR_H, PAPER, MUTED, 1.1, 4)
        if x1 - x0 > PW:
            ticks(x0, x1, y)
        col = INK
    if len(lines) == 1:
        d.t((x0 + x1) / 2, y + 27, lines[0], 12, col, MONO, "middle", 600)
    else:
        d.t((x0 + x1) / 2, y + 20, lines[0], 12, col, MONO, "middle", 600)
        d.t((x0 + x1) / 2, y + 36, lines[1], 12, col, KR, "middle")


def disk_strip(y, after):
    d.t(LX, y + 20, "디스크", 14, INK, KR, "start", 600)
    d.t(LX, y + 36, "디스크 칸 번호", 12, MUTED, KR, "start")
    disk_cell(BX0, MX0, y, ["5,282,848 ~ 5,291,039"], "shared")
    if after:
        disk_cell(MX0, MX1, y, ["5,291,040", "orig 전용"], "orig")
    else:
        disk_cell(MX0, MX1, y, ["5,291,040"], "shared")
    disk_cell(MX1, BX1, y, ["5,291,041 ~ 5,299,231"], "shared")
    if after:                              # 복사 직후에는 새 칸이 아직 없다(점선 자리는 실측이 아니라 그리지 않는다)
        d.t((BX1 + NX) / 2, y + 27, "⋯", 14, SOFT, MONO)
        disk_cell(NX, NX + NW, y, ["6,602,470", "새 디스크 칸"], "new")


def cut(top, title, sub, after):
    d.t(LX, top + 14, title, 14, INK, KR, "start", 600)
    d.t(LX, top + 34, sub, 12, MUTED, KR, "start")
    f1y = top + 48
    sy = f1y + BAR_H + GAP
    f2y = sy + BAR_H + GAP
    # 화살표는 띠보다 먼저 그려 글자를 덮지 않게 한다. 세 자리(앞·가운데·뒤)가 두 컷에서 같다.
    for x in (QL, MC, QR):
        d.arrow([(x, f1y + BAR_H + 2), (x, sy - 3)], INFO, "info", 1.3)
    for x in (QL, QR):
        d.arrow([(x, f2y - 2), (x, sy + BAR_H + 3)], OK, "ok", 1.3)
    if after:
        ry = f2y - 24
        d.arrow([(MC, f2y - 2), (MC, ry), (NX + NW / 2, ry), (NX + NW / 2, sy + BAR_H + 3)],
                ACC, "acc", 1.8)
    else:
        d.arrow([(MC, f2y - 2), (MC, sy + BAR_H + 3)], OK, "ok", 1.3)
    d.t(BX1 + 16, f1y + BAR_H + GAP / 2 + 4, "가리킴", 12, INFO, KR, "start", 600)
    if not after:                          # 둘째 컷은 이 자리를 갈라지는 화살표가 지난다
        d.t(BX1 + 16, sy + BAR_H + GAP / 2 + 4, "가리킴", 12, OK, KR, "start", 600)

    file_bar(f1y, "orig.bin", INFO, ["0 ~ 8,191", "8,192", "8,193 ~ 16,383"])
    disk_strip(sy, after)
    file_bar(f2y, "copy.bin", OK, ["0 ~ 8,191", "8,192", "8,193 ~ 16,383"], hot=after)
    if after:
        d.t(BX1 + 16, f2y + 27, "덮어쓴 칸 (4 KiB)", 12, ACC, KR, "start", 600)
    return f2y + BAR_H


# 숫자 읽는 법: 도식에서 처음 만나는 숫자 셋의 뜻
for i, (ti, rng, desc) in enumerate((
        ("파일 칸 번호", "0 ~ 16,383 · 16,384칸", "파일 안 순서 · 한 칸 = 4 KiB"),
        ("디스크 칸 번호", "5,282,848 ~ 5,299,231", "filefrag 가 보여 주는 디스크 위치"),
        ("df 증가량", "0 · 4 KiB · 64 MiB", "디스크 사용량이 늘어난 양"))):
    x = LX + i * (CW + CG)
    d.box(x, PANEL_Y, CW, PANEL_H, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, PANEL_Y + 22, ti, 14, INK, KR, "start", 600)
    d.t(x + 14, PANEL_Y + 42, rng, 12, INK, MONO, "start")
    d.t(x + 14, PANEL_Y + 61, desc, 12, MUTED, KR, "start")

end1 = cut(PANEL_Y + PANEL_H + 24, "1. reflink 복사 직후", "cp --reflink=always · 두 파일의 모든 칸이 같은 디스크 칸을 가리킴", False)
d.line(LX, end1 + 20, W - 24, end1 + 20, RULE, 0.8, "2 4")
end2 = cut(end1 + 40, "2. copy.bin 의 8,192번 칸을 4 KiB 덮어쓴 뒤",
           "dd seek=8192 conv=notrunc · 그 한 칸만 새 디스크 칸 6,602,470 · 나머지는 계속 같은 칸", True)

# df 사용량 증가 (df -B1 used 차이)
DY = end2 + 40
d.t(LX, DY + 14, "디스크 사용량이 늘어난 양", 14, INK, KR, "start", 600)
d.t(LX, DY + 34, "df -B1 used 의 전후 차이", 12, MUTED, MONO, "start")
CY = DY + 46
for i, (lab, big, small, c) in enumerate((
        ("reflink 복사", "0 B", "df 증가 +0 B", MUTED),
        ("한 칸 덮어쓴 뒤", "4 KiB", "df 증가 +4,096 B · 1칸", ACC),
        ("일반 복사 (--reflink=never)", "64 MiB", "df 증가 +67,108,864 B · 16,384칸", MUTED))):
    x = LX + i * (CW + CG)
    if c == ACC:
        d.tone(x, CY, CW, 76, ACC, 6, "1F", 1.6)
    else:
        d.box(x, CY, CW, 76, PAPER2, c, 1.1, 6)
    d.t(x + CW / 2, CY + 20, lab, 12, MUTED, KR, "middle")
    d.t(x + CW / 2, CY + 46, big, 20, ACC if c == ACC else INK, MONO, "middle", 600)
    d.t(x + CW / 2, CY + 66, small, 12, MUTED, MONO, "middle")

FY = CY + 76 + 34
d.t(LX, FY, "OverlayFS copy-up 은 파일을 통째로 복사 · btrfs 의 reflink 는 블록을 공유", 13, INK, KR, "start", 600)
d.t(LX, FY + 22, "눈금·칸 폭은 축척이 아님 · 8,192번 칸만 확대 · ⋯ 은 번호가 떨어져 있다는 표시", 12, SOFT, KR, "start")

LEG = FY + 42
d.legend(LEG, [("orig.bin 칸", INFO), ("copy.bin 칸", OK), ("새로 쓴 칸", ACC), ("함께 쓰는 디스크 칸", MUTED)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.cow-reflink.svg")
print("ok 05-01.cow-reflink")
