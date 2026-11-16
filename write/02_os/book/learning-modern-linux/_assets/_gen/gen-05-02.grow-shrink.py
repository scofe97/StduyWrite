# 05-02 §3 — 키울 때는 VG → LV → 파일시스템 순으로 띠가 아래부터 늘고, 줄일 때는 파일시스템 →
#           LV 순으로 위부터 준다. 거꾸로 하면 파일시스템 꼬리가 잘리고, XFS 는 줄이기 자체가 막힌다.
# 타입 스펙: type-layers — VG·LV·파일시스템 세 층을 크기 띠로 쌓는다. accent 는 축소의 첫 단계(FS).
# 근거: 본문 §3 의 lvextend -r 출력(vg0/data 200.00 MiB 50 extents → 300.00 MiB 75 extents,
#       /dev/mapper/vg0-data on /mnt/lv, 307200 (1k) blocks), lvreduce -r -L 300M 의 언마운트 질문,
#       lvreduce -y -r -L 200M /dev/vgx/xfsl 의 "Xfs filesystem shrinking is unsupported".
# 축약: 띠 길이는 1 MiB = 1.6px 로 200·300 MiB 의 비율을 지킨다. VG 의 나머지 Free PE 와 축소 전
#       크기는 본문 출력에 없어 점선 "(예)" 로 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 760
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "키울 때는 아래 층부터, 줄일 때는 위 층부터",
      "위 판은 lvextend -r -L +100M 이다. VG 의 Free PE 가 LV vg0/data 로 넘어가 200 MiB(50 extents)가 "
      "300 MiB(75 extents)가 되고, 이어 마운트된 ext4 가 307200 (1k) 블록으로 늘어난다. 아래 판은 줄이기다. "
      "ext4 를 언마운트해 먼저 줄이고 그다음 LV 를 줄여 PE 를 VG 에 돌려준다. LV 를 먼저 자르면 "
      "파일시스템 꼬리가 잘린다. XFS 는 fsadm 이 줄이기를 거절한다.",
      "위 층은 아래 층에 이미 있는 공간만 쓴다 — 그래서 늘리는 순서와 줄이는 순서가 반대다")

LX = 24                   # 층 이름 열
BX = 160                  # 띠 시작
S = 1.6                   # px / MiB
ROW_H, ROW_GAP = 40, 20


def x(mib):
    return BX + mib * S


def seg(y, a, b, label, c, kind="tone", size=12):
    x0, x1 = x(a), x(b)
    if kind == "dash":
        d.o.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="{ROW_H}" rx="4" fill="none" '
                   f'stroke="{c}" stroke-width="1" stroke-dasharray="4 3"/>')
    elif kind == "focal":
        d.o.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="{ROW_H}" rx="4" '
                   f'fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    elif kind == "base":
        d.box(x0, y, x1 - x0, ROW_H, PAPER2, MUTED, 1, 4)
    else:
        d.tone(x0, y, x1 - x0, ROW_H, c, 4)
    if label:
        fam = KR if any('가' <= ch <= '힣' for ch in label) else MONO
        d.t((x0 + x1) / 2, y + 25, label, size, INK if kind == "base" else c, fam)


def layer_name(y, name, sub):
    d.t(LX, y + 17, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 34, sub, 12, SOFT, KR if any('가' <= ch <= '힣' for ch in sub) else MONO, "start")


def step(cx, y, n, c):
    d.o.append(f'<circle cx="{cx}" cy="{y}" r="10" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + 4, n, 12, c, MONO, "middle", 600)


# ── 위 판: 키우기 ───────────────────────────────────────────────
T1 = 104
d.t(LX, T1 + 14, "키우기", 15, OK, KR, "start", 600)
d.t(LX + 64, T1 + 14, "lvextend -r -L +100M /dev/vg0/data", 13, MUTED, MONO, "start")
FY1 = T1 + 32
LY1 = FY1 + ROW_H + ROW_GAP
VY1 = LY1 + ROW_H + ROW_GAP
layer_name(FY1, "파일시스템", "ext4 /mnt/lv")
layer_name(LY1, "LV", "vg0/data")
layer_name(VY1, "VG", "vg0 · PE 풀")
# 아래에서 위로 올라가는 화살표(띠보다 먼저)
MX = x(250)
d.arrow([(MX, VY1 - 2), (MX, LY1 + ROW_H + 3)], OK, "ok", 1.5)
d.arrow([(MX, LY1 - 2), (MX, FY1 + ROW_H + 3)], OK, "ok", 1.5)
seg(VY1, 0, 200, "data 가 쓰던 PE", MUTED, "base")
seg(VY1, 200, 300, "Free PE 100M", OK)
seg(VY1, 300, 340, "(예)", SOFT, "dash")
seg(LY1, 0, 200, "200.00 MiB · 50 extents", MUTED, "base")
seg(LY1, 200, 300, "+100M → 75 extents", OK)
seg(FY1, 0, 200, "ext4 · 마운트된 채", MUTED, "base")
seg(FY1, 200, 300, "307200 (1k) blocks", OK)
for yy, n in ((VY1 + ROW_H / 2, "1"), (LY1 + ROW_H / 2, "2"), (FY1 + ROW_H / 2, "3")):
    step(x(340) + 28, yy, n, OK)
d.t(x(340) + 48, VY1 + 25, "pvresize · vgextend", 12, MUTED, MONO, "start")
d.t(x(340) + 48, LY1 + 25, "lvextend", 12, MUTED, MONO, "start")
d.t(x(340) + 48, FY1 + 25, "resize2fs", 12, MUTED, MONO, "start")

# ── 아래 판: 줄이기 ─────────────────────────────────────────────
T2 = VY1 + ROW_H + 40
d.line(LX, T2 - 16, W - 24, T2 - 16, RULE, 0.8, "2 4")
d.t(LX, T2 + 14, "줄이기", 15, WARN, KR, "start", 600)
d.t(LX + 64, T2 + 14, "lvreduce -r -L 300M /dev/vg0/data", 13, MUTED, MONO, "start")
FY2 = T2 + 32
LY2 = FY2 + ROW_H + ROW_GAP
VY2 = LY2 + ROW_H + ROW_GAP
layer_name(FY2, "파일시스템", "ext4 /mnt/lv")
layer_name(LY2, "LV", "vg0/data")
layer_name(VY2, "VG", "vg0 · PE 풀")
# 목표 크기 선
d.line(x(300), FY2 - 10, x(300), VY2 + ROW_H + 8, WARN, 1.2, "5 3")
d.t(x(300), VY2 + ROW_H + 24, "-L 300M", 12, WARN, MONO)
# 위에서 아래로 내려가는 화살표(띠보다 먼저)
MX2 = x(320)
d.arrow([(MX2, FY2 + ROW_H + 2), (MX2, LY2 - 3)], WARN, "warn", 1.5)
d.arrow([(MX2, LY2 + ROW_H + 2), (MX2, VY2 - 3)], WARN, "warn", 1.5)
seg(FY2, 0, 300, "ext4 · 언마운트 뒤 줄임", MUTED, "base")
seg(FY2, 300, 340, "줄일 몫", ACC, "focal")
seg(LY2, 0, 300, "vg0/data", MUTED, "base")
seg(LY2, 300, 340, "PE 반환", WARN, "dash")
seg(VY2, 0, 300, "data 가 계속 쓰는 PE", MUTED, "base")
seg(VY2, 300, 340, "Free PE", WARN)
for yy, n in ((FY2 + ROW_H / 2, "1"), (LY2 + ROW_H / 2, "2")):
    step(x(340) + 28, yy, n, WARN)
d.t(x(340) + 48, FY2 + 25, "umount·fsck·resize2fs", 12, MUTED, MONO, "start")
d.t(x(340) + 48, LY2 + 25, "lvreduce", 12, MUTED, MONO, "start")
d.t(x(340) + 48, VY2 + 25, "VG 의 Free PE 로", 12, MUTED, KR, "start")

# 거꾸로 했을 때와 XFS
RY = VY2 + ROW_H + 44
layer_name(RY, "거꾸로", "LV 먼저 자르면")
seg(RY, 0, 300, "LV 300M", MUTED, "base")
d.o.append(f'<rect x="{x(300):.1f}" y="{RY}" width="{40 * S:.1f}" height="{ROW_H}" rx="4" '
           f'fill="{BAD}1F" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
d.t(x(320), RY + 25, "FS 꼬리", 12, BAD, KR)
d.t(x(340) + 20, RY + 25, "데이터·메타데이터 손실", 12, BAD, KR, "start", 600)

XY = RY + ROW_H + ROW_GAP
layer_name(XY, "XFS", "vgx/xfsl")
seg(XY, 0, 120, "xfs", MUTED, "base")
d.t(x(120) + 16, XY + 17, "lvreduce -y -r -L 200M", 12, MUTED, MONO, "start")
d.t(x(120) + 16, XY + 34, "fsadm: Xfs filesystem shrinking is unsupported.", 12, BAD, MONO, "start")

d.t(BX, XY + ROW_H + 28, "띠 길이 1 MiB = 1.6px · 점선 Free PE 와 줄이기 전 크기·XFS 띠 길이는 예시", 11, SOFT, KR, "start")
LEG = XY + ROW_H + 48
d.legend(LEG, [("키우는 쪽", OK), ("줄이는 쪽", WARN), ("손실 · 거절", BAD), ("먼저 줄일 층", ACC)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.grow-shrink.svg")
print("ok 05-02.grow-shrink")
