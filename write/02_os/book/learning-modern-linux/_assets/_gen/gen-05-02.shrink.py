# 타입 스펙: type-layers
# 05-02 §3 — 축소는 위 층부터: 파일시스템(resize2fs) → LV(lvreduce) 순으로 위부터 줄인다.
#           ext4 는 블록 그룹이 전체에 흩어져 있어 먼저 줄이지 않고 LV 를 자르면 꼬리 블록이 잘려 영구 손실된다.
#           XFS 는 fsadm 이 축소를 거절(unsupported)하므로 백업 뒤 재생성해야 한다.
# 근거: 본문 §3 의 lvreduce -r -L 300M 언마운트 질문, lvreduce -y -r -L 200M /dev/vgx/xfsl 의 거절 출력,
#       커널 XFS Online Fsck Design 문서의 inode 청크 이동 미해결 과제.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "축소는 위 층부터 — 파일시스템 → LV → VG",
      "ext4 를 언마운트해 먼저 줄이고 그다음 LV 를 줄여 PE 를 VG 에 돌려준다. LV 를 먼저 자르면 "
      "파일시스템 뒷부분 블록 그룹이 잘려 영구 손실된다. XFS 는 fsadm 이 축소를 거절한다.",
      "파일시스템 블록을 앞쪽으로 대피시킨 후 하위 LV 를 줄여야 손실을 막는다")

LX = 24
BX = 136
S = 1.0
ROW_H, ROW_GAP = 36, 20


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
        d.t((x0 + x1) / 2, y + 23, label, size, INK if kind == "base" else c, fam)


def layer_name(y, name, sub):
    d.t(LX, y + 15, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 31, sub, 12, SOFT, KR if any('가' <= ch <= '힣' for ch in sub) else MONO, "start")


def step(cx, y, n, c):
    d.o.append(f'<circle cx="{cx}" cy="{y}" r="10" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + 4, n, 12, c, MONO, "middle", 600)


# ── 상단 판: 정상 축소 순서 ───────────────────────────────────────
T1 = 104
FY = T1 + 22
LY = FY + ROW_H + ROW_GAP
VY = LY + ROW_H + ROW_GAP

layer_name(FY, "파일시스템", "ext4 /mnt/lv")
layer_name(LY, "LV", "vg0/data")
layer_name(VY, "VG · PV", "vg0 · PE 풀")

# 목표 크기 점선 (200M 지점)
d.line(x(200), FY - 8, x(200), VY + ROW_H + 6, WARN, 1.2, "4 3")
d.t(x(200), FY - 14, "-L 200M 목표 크기", 12, WARN, KR)

# 위에서 아래로 내려가는 화살표
MX = x(250)
d.arrow([(MX, FY + ROW_H + 4), (MX, LY - 4)], WARN, "warn", 1.5)
d.arrow([(MX, LY + ROW_H + 4), (MX, VY - 4)], WARN, "warn", 1.5)

seg(FY, 0, 200, "앞쪽으로 대피된 블록", MUTED, "base")
seg(FY, 200, 300, "줄일 몫 (언마운트)", ACC, "focal")

seg(LY, 0, 200, "유지할 LV (LE 0~49)", MUTED, "base")
seg(LY, 200, 300, "반환할 LE 25개", WARN, "dash")

seg(VY, 0, 200, "계속 쓰는 PE", MUTED, "base")
seg(VY, 200, 300, "Free PE 풀 복귀", WARN)

CX_STEP = x(300) + 24
for yy, n in ((FY + ROW_H / 2, "1"), (LY + ROW_H / 2, "2"), (VY + ROW_H / 2, "3")):
    step(CX_STEP, yy, n, WARN)

d.t(CX_STEP + 16, FY + 23, "umount · fsck · resize2fs", 12, MUTED, MONO, "start")
d.t(CX_STEP + 16, LY + 23, "lvreduce -L 200M", 12, MUTED, MONO, "start")
d.t(CX_STEP + 16, VY + 23, "VG 의 Free PE 로 전환", 12, MUTED, KR, "start")

# ── 중단: 거꾸로 자르면? ──────────────────────────────────────────
RY = VY + ROW_H + 28
layer_name(RY, "거꾸로 자르면", "LV 먼저 축소 시")
seg(RY, 0, 200, "남은 LV 공간 (200M)", MUTED, "base")
d.o.append(f'<rect x="{x(200):.1f}" y="{RY}" width="{100 * S:.1f}" height="{ROW_H}" rx="4" '
           f'fill="{BAD}1F" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
d.t(x(250), RY + 23, "FS 꼬리 블록 절단", 12, BAD, KR)
d.t(x(300) + 20, RY + 23, "아이노드 테이블 · 데이터 블록 영구 손실!", 12, BAD, KR, "start", 600)

# ── 하단: XFS 축소 거절 ──────────────────────────────────────────
XY = RY + ROW_H + 20
layer_name(XY, "XFS 축소 거절", "vgx/xfsl")
d.box(BX, XY, 180, ROW_H, PAPER2, MUTED, 1, 4)
d.t(BX + 90, XY + 23, "XFS 파일시스템", 12, INK, KR)

d.t(BX + 196, XY + 15, "lvreduce -y -r -L 200M → fsadm: Xfs filesystem shrinking is unsupported.", 12, BAD, MONO, "start")
d.t(BX + 196, XY + 31, "동적 inode · inode 에 AG 번호 포함(청크 이동 미해결) → 백업 후 재생성만 가능", 12, MUTED, KR, "start")

LEG = XY + ROW_H + 42
d.legend(LEG, [("축소 방향", WARN), ("먼저 줄일 층", ACC), ("손실 · 거절", BAD), ("기존 유지 공간", MUTED)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.shrink.svg")
print("ok 05-02.shrink")
