# 타입 스펙: type-layers
# 05-02 §3 — 확장은 아래 층부터: VG(Free PE) → LV(lvextend) → 파일시스템(resize2fs) 순으로 공간을 늘린다.
#           ext4 주소는 LV 주소와 같아 두 층 사이에 별도 번역표가 없다. LV 주소 공간이 늘어나지 않으면
#           ext4 새 블록 그룹 메타데이터를 둘 자리가 없어 ext4 를 먼저 늘릴 수 없다.
# 근거: 본문 §3 의 lvextend -r 출력(vg0/data 200.00 MiB 50 extents → 300.00 MiB 75 extents,
#       /dev/mapper/vg0-data on /mnt/lv, 307200 (1k) blocks), dmsetup table 의 linear 매핑.
import sys; sys.path.insert(0, ".")
from dd import D, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "확장은 아래 층부터 — PV → VG → LV → 파일시스템",
      "VG 에 Free PE 를 확보하고 lvextend 로 LV 를 확장한 뒤 resize2fs 로 ext4 블록 그룹을 추가한다. "
      "ext4 주소는 LV 주소와 같아 LV 가 커지기 전에 ext4 를 먼저 늘릴 수 없다.",
      "위 층은 아래 층에 이미 확보된 공간만 쓴다 — 그래서 확장은 아래 층부터 올라간다")

LX = 24
BX = 136
S = 0.85
ROW_H, ROW_GAP = 38, 24


def x(mib):
    return BX + mib * S


def seg(y, a, b, label, c, kind="tone", size=12):
    x0, x1 = x(a), x(b)
    if kind == "dash":
        d.o.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="{ROW_H}" rx="4" fill="none" '
                   f'stroke="{c}" stroke-width="1" stroke-dasharray="4 3"/>')
    elif kind == "base":
        d.box(x0, y, x1 - x0, ROW_H, PAPER2, MUTED, 1, 4)
    else:
        d.tone(x0, y, x1 - x0, ROW_H, c, 4)
    if label:
        fam = KR if any('가' <= ch <= '힣' for ch in label) else MONO
        d.t((x0 + x1) / 2, y + 24, label, size, INK if kind == "base" else c, fam)


def layer_name(y, name, sub):
    d.t(LX, y + 16, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 33, sub, 12, SOFT, KR if any('가' <= ch <= '힣' for ch in sub) else MONO, "start")


def step(cx, y, n, c):
    d.o.append(f'<circle cx="{cx}" cy="{y}" r="10" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + 4, n, 12, c, MONO, "middle", 600)


# ── 세 층 배치 ──────────────────────────────────────────────────
T1 = 104
FY = T1 + 24
LY = FY + ROW_H + ROW_GAP
VY = LY + ROW_H + ROW_GAP

layer_name(FY, "파일시스템", "ext4 /mnt/lv")
layer_name(LY, "LV", "vg0/data")
layer_name(VY, "VG · PV", "/dev/sdb · PE 풀")

# 아래에서 위로 올라가는 화살표
MX = x(250)
d.arrow([(MX, VY - 4), (MX, LY + ROW_H + 4)], OK, "ok", 1.5)
d.arrow([(MX, LY - 4), (MX, FY + ROW_H + 4)], OK, "ok", 1.5)

seg(VY, 0, 200, "기존 PE 50개", MUTED, "base")
seg(VY, 200, 300, "Free PE 25개", OK)
seg(VY, 300, 350, "(예)", SOFT, "dash")

seg(LY, 0, 200, "200M (LE 0~49)", MUTED, "base")
seg(LY, 200, 300, "+100M", OK)

seg(FY, 0, 200, "기존 블록 그룹", MUTED, "base")
seg(FY, 200, 300, "새 블록 그룹 추가", OK)

# 단계 번호 및 도구
CX_STEP = x(350) + 20
for yy, n in ((VY + ROW_H / 2, "1"), (LY + ROW_H / 2, "2"), (FY + ROW_H / 2, "3")):
    step(CX_STEP, yy, n, OK)

d.t(CX_STEP + 16, VY + 24, "pvresize · vgextend", 12, MUTED, MONO, "start")
d.t(CX_STEP + 16, LY + 24, "lvextend -L +100M", 12, MUTED, MONO, "start")
d.t(CX_STEP + 16, FY + 24, "resize2fs", 12, MUTED, MONO, "start")

# ── 오른쪽 설명 상자: 두 층의 매핑과 거꾸로 순서 ─────────────────
BX2 = 624
BY2 = FY
BW2 = 272
BH2 = VY + ROW_H - FY

d.box(BX2, BY2, BW2, BH2, PAPER2, RULE, 1, 6)
d.t(BX2 + 14, BY2 + 22, "ext4 주소 = LV 주소", 13, INK, KR, "start", 600)
d.t(BX2 + 14, BY2 + 42, "• 두 층 사이 번역표 없음 (1:1)", 12, MUTED, KR, "start")
d.t(BX2 + 14, BY2 + 62, "• LVM 표는 LE→PE 한 곳뿐", 12, MUTED, KR, "start")

d.line(BX2 + 12, BY2 + 76, BX2 + BW2 - 12, BY2 + 76, RULE, 0.8)

d.t(BX2 + 14, BY2 + 96, "ext4 먼저 키우면?", 13, BAD, KR, "start", 600)
d.t(BX2 + 14, BY2 + 118, "하위 LV 가 늘어나지 않아 새 블록", 12, BAD, KR, "start")
d.t(BX2 + 14, BY2 + 136, "그룹 메타데이터를 쓸 주소가 없음", 12, BAD, KR, "start")
d.t(BX2 + 14, BY2 + 154, "→ 아래 장치부터 키워야 함", 12, BAD, KR, "start")

# 실무 도우미 팁
d.box(LX, VY + ROW_H + 24, W - 48, 38, PAPER2, RULE, 1, 4)
d.t(LX + 14, VY + ROW_H + 48, "실무 팁: lvextend -r (--resizefs) — 2단계(LV 확장)와 3단계(resize2fs) 일괄 처리", 12, INK, KR, "start")

LEG = VY + ROW_H + 82
d.legend(LEG, [("확장 방향", OK), ("기존 할당 공간", MUTED), ("새로 확장된 영역", OK), ("거절 · 불가", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.grow.svg")
print("ok 05-02.grow")
