# 05-01 §5 — 디스크 두 개(sda2·sdb)를 VG 하나로 모은 뒤 LV 를 늘리는 세 상태.
#           LV 번호(LE)는 빈틈없이 이어지고 실제 자리(PE)는 두 디스크에 섞인다. LVM 은 그 짝을
#           구간(segment) 단위 표로 기억하고, 늘리면 표 끝에 줄 하나가 붙을 뿐 앞 줄은 그대로다.
# 타입 스펙: type-state — 상태 셋(처음 · sda2 가 커진 뒤 · LV 를 늘린 뒤)을 위→아래로 놓고,
#           전이 = 그 상태를 만든 명령(pvresize · lvextend). accent 는 새로 붙은 구간 LE 20–24.
# 근거: 2026-11-17 OrbStack lml-ubuntu 실측(64 MiB loop 장치 둘, PE 4 MiB).
#       lvs --segments -o lv_name,seg_start_pe,seg_size_pe,seg_pe_ranges vgdemo
#         처음      Start 0  SSize 15  /dev/loop0:0-14
#                   Start 15 SSize 5   /dev/loop1:0-4
#         pvresize  loop0 64 → 96 MiB, PE 15 → 23 (pvs: Alloc 15)
#         lvextend  Start 20 SSize 5   /dev/loop0:15-19 가 셋째 줄로 붙고 앞 두 줄은 같은 값
#       표기: loop0 을 본문의 sda2 자리에, loop1 을 sdb 자리에 놓았다. 숫자는 모두 실측이고
#       본문 pvdisplay 의 57105 PE 와 섞지 않는다. lvextend 에는 PV 를 적어 재현했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 960, 832
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §5",
      "LV 를 늘리면 구간 표 끝에 줄 하나가 붙는다",
      "디스크 두 개 sda2·sdb 를 PV 로 만들어 VG vgdemo 하나에 모은다. LV lvdemo 는 LE 0–14 가 sda2 PE 0–14, "
      "LE 15–19 가 sdb PE 0–4 에 놓여 두 디스크에 걸친다. pvresize 로 sda2 가 15 PE 에서 23 PE 로 커져 "
      "끝에 빈 PE 15–22 가 생겨도 LV 와 구간 표는 그대로다. lvextend 로 5 PE 를 더하면 LV 끝에 "
      "LE 20–24 → sda2 PE 15–19 줄이 붙고 앞 두 줄은 번호도 자리도 바뀌지 않는다. "
      "숫자는 OrbStack VM 에서 64 MiB loop 장치 둘(loop0 을 sda2, loop1 을 sdb 자리)로 재현한 "
      "lvs --segments 값이다.",
      "LV 번호는 빈틈없이 이어지고 실제 자리는 디스크가 섞인다 — 늘리면 표 끝에 줄이 붙을 뿐 옛 데이터는 그대로")

CW = 16                       # PE·LE 한 칸 폭 (stride)
X0 = 200                      # 칸 띠의 왼쪽 끝
LX = 36                       # 왼쪽 이름 열
PX0, PX1 = 16, 944            # 상태 상자 가로 범위
PH = 176                      # 상태 상자 높이
TOPS = (104, 328, 552)        # 상태 상자 위쪽 (stride 224)
TX0, TC1, TC2 = 664, 688, 792 # 표: 색 칸 · LV 구간 · 실제 위치

SEG = {1: INFO, 2: OK, 3: ACC}
LE = {1: (0, 14), 2: (15, 19), 3: (20, 24)}
LOC = {1: ("sda2", 0, 14), 2: ("sdb", 0, 4), 3: ("sda2", 15, 19)}

# 상태마다: 패널 제목, sda2 칸 주인(None=빈 PE), sdb 칸 주인, LV 구간, 표 셋째 줄 자리의 메모
STATES = [
    ("1 · 처음 — LV 가 두 디스크에 걸침",
     [1] * 15, [2] * 5 + [None] * 10, [1, 2], None),
    ("2 · pvresize — sda2 끝에 빈 PE 8 개",
     [1] * 15 + [None] * 8, [2] * 5 + [None] * 10, [1, 2], "LV 그대로 · 표 그대로"),
    ("3 · lvextend — LV 끝에 구간 한 줄",
     [1] * 15 + [3] * 5 + [None] * 3, [2] * 5 + [None] * 10, [1, 2, 3], None),
]


def runs(owners):
    """같은 주인이 이어지는 칸 묶음 [(주인, 첫 칸, 끝 칸)]."""
    out = []
    for i, o in enumerate(owners):
        if out and out[-1][0] == o and out[-1][2] == i - 1:
            out[-1] = (o, out[-1][1], i)
        else:
            out.append((o, i, i))
    return out


def span(y, h, o, a, b, label=None):
    """칸 a..b 를 한 상자로. 칸 경계는 아래쪽 짧은 눈금이라 가운데 라벨을 가르지 않는다."""
    x0, x1 = X0 + a * CW + 1, X0 + (b + 1) * CW - 1
    if o is None:
        c = WARN
        d.o.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="3" fill="none" '
                   f'stroke="{c}" stroke-width="1" stroke-dasharray="4 3"/>')
    else:
        c = SEG[o]
        d.o.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="3" '
                   f'fill="{c}26" stroke="{c}" stroke-width="1"/>')
    for i in range(a + 1, b + 1):
        x = X0 + i * CW
        d.line(x, y + h - 5, x, y + h, c, 0.8)
    if label:
        d.t((x0 + x1) / 2, y + h / 2 + 4, label, 12, WARN if o is None else INK,
            KR if o is None else MONO)


def cells(y, h, owners):
    """PE 칸 띠. 빈 칸은 점선, 다섯 칸 이상 비면 '빈 PE a–b' 라벨."""
    for o, a, b in runs(owners):
        span(y, h, o, a, b, f"빈 PE {a}–{b}" if o is None and b - a >= 4 else None)
    d.t(X0 + len(owners) * CW + 12, y + h / 2 + 4, f"{len(owners)} PE", 12, MUTED, MONO, "start")


for k, (title, sda2, sdb, segs, memo) in enumerate(STATES):
    top = TOPS[k]
    last = k == len(STATES) - 1

    # 상태 상자와 제목
    d.box(PX0, top, PX1 - PX0, PH, PAPER2, RULE, 1.0, 8)
    d.t(LX - 4, top + 26, title, 14, INK, KR, "start", 600)

    # LV 줄 — LE 번호가 빈틈없이 이어지는 띠
    ly, lh = top + 44, 28
    d.t(LX, ly + 19, "LV lvdemo", 13, INK, MONO, "start", 600)
    for s in segs:
        a, b = LE[s]
        span(ly, lh, s, a, b, f"LE {a}–{b}")

    # VG 상자 안의 두 PV — 실제 자리
    vy = top + 80
    d.o.append(f'<rect x="{PX0 + 12}" y="{vy}" width="{640 - PX0 - 12}" height="88" rx="8" '
               f'fill="none" stroke="{MUTED}" stroke-width="1"/>')
    d.t(LX, vy + 18, "VG vgdemo · 웅덩이", 12, MUTED, KR, "start", 600)
    for row, (name, owners) in enumerate((("sda2", sda2), ("sdb", sdb))):
        ry = vy + 28 + row * 32
        d.t(LX, ry + 16, f"PV {name}", 13, INK, MONO, "start")
        cells(ry, 22, owners)

    # 구간 표 — LV 구간 | 실제 위치
    d.t(TC1, top + 54, "LV 구간", 12, SOFT, KR, "start")
    d.t(TC2, top + 54, "실제 위치", 12, SOFT, KR, "start")
    d.line(TX0, top + 64, PX1 - 16, top + 64, RULE, 0.8)
    for r, s in enumerate(segs):
        ry = top + 72 + r * 32
        if last and s == 3:
            d.o.append(f'<rect x="{TX0 - 4}" y="{ry}" width="{PX1 - 16 - TX0 + 4}" height="26" rx="4" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.o.append(f'<rect x="{TX0 + 2}" y="{ry + 7}" width="12" height="12" rx="2" '
                   f'fill="{SEG[s]}33" stroke="{SEG[s]}" stroke-width="1"/>')
        a, b = LE[s]
        dev, pa, pb = LOC[s]
        d.t(TC1, ry + 18, f"LE {a}–{b}", 13, INK, MONO, "start")
        d.t(TC2, ry + 18, f"{dev} PE {pa}–{pb}", 13, INK, MONO, "start")
    if memo:
        d.t(TC1, top + 72 + 2 * 32 + 18, memo, 12, MUTED, KR, "start")

# 전이 — 상태를 바꾼 명령
for k, (cmd, note) in enumerate((("pvresize sda2", "디스크 64 → 96 MiB 뒤"),
                                 ("lvextend -l +5 vgdemo/lvdemo sda2", "LV 에 5 PE"))):
    y0, y1 = TOPS[k] + PH, TOPS[k + 1]
    d.arrow([(96, y0 + 4), (96, y1 - 4)], MUTED, "ar", 1.4)
    d.t(112, (y0 + y1) / 2 + 5, cmd, 13, INK, MONO, "start", 600)
    d.t(112 + len(cmd) * 8 + 16, (y0 + y1) / 2 + 5, note, 12, MUTED, KR, "start")

fy = TOPS[-1] + PH
d.t(16, fy + 24, "실측 loop0 → sda2 · loop1 → sdb · PE 4 MiB", 12, SOFT, KR, "start")
d.t(16, fy + 44, "떼어 올 PV: 할당기가 고르거나 명령에서 지정", 12, SOFT, KR, "start")
d.legend(fy + 60, [("LV 구간 LE 0–14", INFO), ("LE 15–19", OK), ("새 구간 LE 20–24", ACC), ("빈 PE", WARN)])
d.save("05-01.lvm-extend.svg")
print("ok 05-01.lvm-extend")
