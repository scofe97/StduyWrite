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
#   가로 축은 논리 블록 번호에 비례(0..16384 → BX0..BX1). 블록 8192 한 칸만 눈에 보이게 12px 로 키웠다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 940
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "reflink 복사는 extent 를 함께 쓰고, 덮어쓴 4 KiB 만 갈라진다",
      "btrfs 실측이다. 위 컷은 64 MiB 파일 orig.bin 을 cp --reflink=always 로 copy.bin 에 복사한 직후다. "
      "두 파일 모두 논리 블록 0..16383 이 물리 블록 5282848..5299231 한 extent 를 가리키고 filefrag 가 shared 로 "
      "표시한다. 아래 컷은 copy.bin 의 블록 8192 를 4 KiB 덮어쓴 뒤다. copy.bin 은 extent 셋으로 갈라져 블록 8192 만 "
      "물리 6602470 을 가리키고, 0..8191 과 8193..16383 은 여전히 원래 extent 를 shared 로 가리킨다. orig.bin 은 "
      "그대로다. df 사용량은 reflink 복사에 0 바이트, 덮어쓰기에 4096 바이트, cp --reflink=never 복사에 "
      "67108864 바이트 늘었다.",
      "btrfs · 64 MiB 파일 · filefrag -v 와 df -B1 실측 — 공유는 그대로, 쓴 블록 하나만 새 자리로")

LX = 24                         # 컷 이름 열
BX0, BX1 = 200, 632             # 논리·물리 블록 축 (16384 블록 → 432px)
MX0, MX1 = 410, 422             # 블록 8192 한 칸 (눈에 보이게 12px)
MC = (MX0 + MX1) / 2
NX, NW = 704, 104               # 새 물리 블록 자리
BAR_H, GAP = 44, 48
QL, QR = (BX0 + MX0) / 2, (MX1 + BX1) / 2   # 왼쪽·오른쪽 extent 가운데


def seg(x0, x1, y, lab, c, op="1F", size=12):
    d.tone(x0, y, x1 - x0, BAR_H, c, 4, op, 1.1)
    if lab:
        d.t((x0 + x1) / 2, y + 27, lab, size, c, MONO, "middle", 600)


def bar(y, name, segs, c):
    """파일 하나의 논리 블록 막대. segs: (x0, x1, 라벨, 색)"""
    d.t(LX, y + 20, name, 14, c, MONO, "start", 600)
    d.t(LX, y + 36, "논리 블록", 12, MUTED, KR, "start")
    for x0, x1, lab, sc in segs:
        seg(x0, x1, y, lab, sc)


def strip(y, cells, free):
    """디스크 물리 extent 띠. cells: (x0, x1, 라벨, 종류)"""
    d.t(LX, y + 20, "물리 extent", 13, INK, KR, "start", 600)
    d.t(LX, y + 36, "디스크", 12, SOFT, KR, "start")
    for x0, x1, lab, kind in cells:
        if kind == "new":
            d.tone(x0, y, x1 - x0, BAR_H, ACC, 4, "1F", 1.4)
            d.t((x0 + x1) / 2, y + 28, lab, 14, ACC, MONO, "middle", 600)
        elif kind == "orig":
            d.tone(x0, y, x1 - x0, BAR_H, INFO, 2, "55", 1.1)
        else:
            d.box(x0, y, x1 - x0, BAR_H, PAPER, MUTED, 1.1, 4)
            d.t((x0 + x1) / 2, y + 27, lab, 12, INK, MONO, "middle", 600)
    d.t((BX1 + NX) / 2, y + 27, "⋯", 14, SOFT, MONO)
    if free:
        d.o.append(f'<rect x="{NX}" y="{y}" width="{NW}" height="{BAR_H}" rx="4" fill="none" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 3"/>')
        d.t(NX + NW / 2, y + 27, "빈", 12, SOFT, KR)


def cut(top, title, sub, after):
    d.t(LX, top + 14, title, 14, INK, KR, "start", 600)
    d.t(LX, top + 34, sub, 12, MUTED, KR, "start")
    f1y = top + 52
    sy = f1y + BAR_H + GAP
    f2y = sy + BAR_H + GAP
    # 포인터 화살표는 막대·띠보다 먼저 그린다(글자를 덮지 않게)
    d.arrow([(MC, f1y + BAR_H + 2), (MC, sy - 3)], INFO, "info", 1.3)
    if after:
        for x in (QL, QR):
            d.arrow([(x, f2y - 2), (x, sy + BAR_H + 3)], OK, "ok", 1.3)
        ry = f2y - 22
        d.arrow([(MC, f2y - 2), (MC, ry), (NX + NW / 2, ry), (NX + NW / 2, sy + BAR_H + 3)],
                ACC, "acc", 1.6)
    else:
        d.arrow([(MC, f2y - 2), (MC, sy + BAR_H + 3)], OK, "ok", 1.3)

    bar(f1y, "orig.bin", [(BX0, BX1, "0..16383 → 5282848..5299231 · shared", INFO)], INFO)
    if after:
        strip(sy, [(BX0, MX0, "5282848..5291039 · shared", "shared"), (MX0, MX1, "", "orig"),
                   (MX1, BX1, "5291041..5299231 · shared", "shared"), (NX, NX + NW, "6602470", "new")],
              False)
        bar(f2y, "copy.bin", [(BX0, MX0, "0..8191 · shared", OK), (MX0, MX1, "", ACC),
                              (MX1, BX1, "8193..16383 · shared", OK)], OK)
        d.t(BX1 + 16, f2y + 27, "블록 8192 만 새 자리", 12, ACC, KR, "start", 600)
    else:
        strip(sy, [(BX0, BX1, "5282848..5299231 · 16384 블록 · shared", "shared")], True)
        bar(f2y, "copy.bin", [(BX0, BX1, "0..16383 → 5282848..5299231 · shared", OK)], OK)
    return f2y + BAR_H


end1 = cut(104, "1. reflink 복사 직후", "cp --reflink=always · 두 파일이 extent 하나를 공유", False)
d.line(LX, end1 + 20, W - 24, end1 + 20, RULE, 0.8, "2 4")
end2 = cut(end1 + 40, "2. copy.bin 블록 8192 를 4 KiB 덮어쓴 뒤",
           "dd seek=8192 conv=notrunc · 그 블록만 6602470 · 나머지는 계속 shared", True)

# df 사용량 증가 (df -B1 used 차이)
DY = end2 + 40
d.t(LX, DY + 14, "df 증가량", 14, INK, KR, "start", 600)
d.t(LX, DY + 34, "df -B1 used 차이", 12, MUTED, MONO, "start")
CW_, CG = 200, 20
for i, (lab, val, c) in enumerate((("reflink 복사", "+0 B", OK),
                                   ("블록 하나 덮어씀", "+4,096 B", INK),
                                   ("--reflink=never", "+67,108,864 B", WARN))):
    x = BX0 + i * (CW_ + CG)
    d.box(x, DY, CW_, 56, PAPER2, MUTED if c == INK else c, 1.1, 6)
    d.t(x + CW_ / 2, DY + 21, lab, 12, MUTED, KR if i < 2 else MONO, "middle")
    d.t(x + CW_ / 2, DY + 44, val, 15, c, MONO, "middle", 600)

FY = DY + 56 + 36
d.t(LX, FY, "OverlayFS copy-up 은 파일 단위 복사 · btrfs·XFS 위에서는 이 reflink 로 블록 공유", 13, INK, KR, "start", 600)
d.t(LX, FY + 22, "물리 번호는 4 KiB 블록 번호 · 가로 축은 논리 블록에 비례, 블록 8192 칸만 키움", 11, SOFT, KR, "start")

LEG = FY + 44
d.legend(LEG, [("orig.bin 포인터", INFO), ("copy.bin 포인터", OK), ("새로 쓴 블록", ACC), ("전체 복사 비용", WARN)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.cow-reflink.svg")
print("ok 05-01.cow-reflink")
