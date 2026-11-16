# 05-01 §5 — 디스크의 파티션이 PV 가 되어 PE 조각으로 잘리고, VG 가 그 PE 를 풀로 모으며,
#           LV 가 풀에서 PE 를 가져가 블록 장치가 되고, 그 위에 파일시스템·스왑이 올라가는 층.
# 타입 스펙: type-layers — 아래 층(디스크)에서 위 층(용도)으로 쌓이는 실제 구조. accent 는 LV.
# 근거: 본문의 pvdisplay·vgs·lvscan 출력(PE 4 MiB, Total PE 57105, Free PE 4, root 56857 PE,
#       swap_1 244 PE). 축약: PE 띠의 한 칸은 약 1,390 PE 다. swap_1 과 여유는 실제로 0.5% 도
#       안 되지만 읽을 수 있게 한 칸씩 주었다. 점선 칸(추가할 디스크·PV)은 출력에 없는 예시다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 960, 712
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §5",
      "PE 조각을 VG 풀에 모았다가 LV 마다 나눠 준다",
      "디스크 /dev/sda 의 파티션 sda2 가 PV 로 초기화되어 4 MiB PE 57105 개로 잘리고, "
      "볼륨 그룹 elementary-vg 가 그 PE 를 풀로 모은다. 논리 볼륨 root 가 56857 PE, "
      "swap_1 이 244 PE 를 가져가고 4 PE 가 남는다. root 에는 ext4 가 올라가 / 에 마운트되고 "
      "swap_1 은 스왑으로 쓰인다. 새 디스크를 PV 로 만들어 같은 VG 에 넣으면 풀이 커진다.",
      "VG 는 나뉘는 쪽이 아니라 모이는 쪽 — 나뉘는 것은 VG 의 PE 를 가져가는 LV 다")

LX = 48                      # 층 이름 열
X0, X1 = 200, 640            # sda2·PV 띠의 가로 범위
XN0, XN1 = 680, 912          # 추가할 디스크·PV 예시 자리

# 층 이름
for y, name, sub in ((178, "디스크", "partition"), (318, "PV · VG", "PE 풀"),
                     (474, "LV", "블록 장치"), (578, "용도", "fs · swap")):
    d.t(LX, y, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 18, sub, 11, SOFT, MONO, "start")

# 1층 — 디스크와 파티션
DY, DH = 150, 52
d.t(X0 - 40, DY - 10, "/dev/sda", 12, MUTED, MONO, "start")
d.o.append(f'<rect x="{X0 - 40}" y="{DY}" width="40" height="{DH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(X0 - 20, DY + 31, "…", 12, SOFT, MONO)
d.tone(X0, DY, X1 - X0, DH, INFO)
d.t((X0 + X1) / 2, DY + 22, "/dev/sda2", 13, INK, MONO, "middle", 600)
d.t((X0 + X1) / 2, DY + 40, "파티션 · 223.07 GiB", 12, MUTED, KR)
d.o.append(f'<rect x="{XN0}" y="{DY}" width="{XN1 - XN0}" height="{DH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t((XN0 + XN1) / 2, DY + 22, "/dev/sdb (예)", 12, SOFT, MONO)
d.t((XN0 + XN1) / 2, DY + 40, "나중에 붙일 디스크", 12, SOFT, KR)

# pvcreate 화살표
d.arrow([((X0 + X1) / 2, DY + DH + 4), ((X0 + X1) / 2, 278)], INFO, "info")
d.t((X0 + X1) / 2 + 10, 246, "pvcreate", 12, INFO, MONO, "start")
d.arrow([((XN0 + XN1) / 2, DY + DH + 4), ((XN0 + XN1) / 2, 278)], SOFT, "soft", 1.2, "4 3")
d.t((XN0 + XN1) / 2 + 10, 246, "vgextend", 12, SOFT, MONO, "start")

# 2층 — VG 상자 안의 PV(PE 띠)
VY, VH = 226 + 50, 112
d.o.append(f'<rect x="{X0 - 40}" y="{VY - 10}" width="{XN1 - X0 + 52}" height="{VH + 20}" rx="10" '
           f'fill="{OK}0D" stroke="{OK}" stroke-width="1.4"/>')
d.t(X0 - 40, VY - 18, "VG elementary-vg · PE 4 MiB", 12, OK, MONO, "start", 600)

# LV 로 가는 띠는 글자보다 먼저 그린다(글자를 덮지 않게)
PY, PH = VY + 14, 40
N, CW = 44, (X1 - X0) / 44
LY, LH = 444, 62
lvs = [("root", "/dev/elementary-vg/root", "56857 PE · 222.10 GiB", 0, N - 2, X0 - 40, 560, ACC),
       ("swap_1", "/dev/elementary-vg/swap_1", "244 PE · 976 MiB", N - 2, N - 1, 576, 776, MUTED),
       ("여유 (VFree)", "LV 에 아직 안 줌", "4 PE · 16 MiB", N - 1, N, 792, XN1, WARN)]
for name, dev, size, a, b, bx0, bx1, c in lvs:
    sx0, sx1 = X0 + a * CW + 1, X0 + b * CW - 1
    d.o.append(f'<path d="M {sx0:.1f} {PY + PH} L {sx1:.1f} {PY + PH} L {bx1} {LY} L {bx0} {LY} Z" '
               f'fill="{c}18" stroke="none"/>')

owner = ["root"] * (N - 2) + ["swap", "free"]
col = {"root": ACC, "swap": MUTED, "free": WARN}
for i, o in enumerate(owner):
    x = X0 + i * CW
    d.o.append(f'<rect x="{x + 1:.1f}" y="{PY}" width="{CW - 2:.1f}" height="{PH}" rx="2" '
               f'fill="{col[o]}33" stroke="{col[o]}" stroke-width="0.8"/>')
d.t(X0, PY + PH + 20, "PV /dev/sda2 → PE 57105 개", 12, INFO, MONO, "start")
d.o.append(f'<rect x="{XN0}" y="{PY}" width="{XN1 - XN0}" height="{PH}" rx="4" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t((XN0 + XN1) / 2, PY + 25, "새 PV 의 PE 가 풀에 더해짐", 12, SOFT, KR)

# 3층 — LV 상자
for name, dev, size, a, b, bx0, bx1, c in lvs:
    if name.startswith("여유"):
        d.o.append(f'<rect x="{bx0}" y="{LY}" width="{bx1 - bx0}" height="{LH}" rx="6" fill="none" '
                   f'stroke="{c}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        d.t((bx0 + bx1) / 2, LY + 22, name, 13, c, KR, "middle", 600)
        d.t((bx0 + bx1) / 2, LY + 40, dev, 12, MUTED, KR)
    else:
        d.tone(bx0, LY, bx1 - bx0, LH, c)
        d.t((bx0 + bx1) / 2, LY + 22, name, 14, c, MONO, "middle", 600)
        d.t((bx0 + bx1) / 2, LY + 40, dev, 12, INK, MONO)
    d.t((bx0 + bx1) / 2, LY + 56, size, 11, MUTED, MONO)

# 4층 — 용도
UY, UH = 560, 40
uses = [("ext4 → /", "mkfs · mount", X0 - 40, 560, ACC),
        ("[SWAP]", "mkswap · swapon", 576, 776, MUTED),
        ("lvextend 의 재료", "", 792, XN1, WARN)]
for label, cmd, bx0, bx1, c in uses:
    cx = (bx0 + bx1) / 2
    if cmd:
        d.arrow([(cx, LY + LH + 2), (cx, UY - 2)], c, "acc" if c == ACC else "ar")
        d.t(cx + 8, LY + LH + 30, cmd, 11, SOFT, MONO, "start")
        d.box(bx0, UY, bx1 - bx0, UH, PAPER2, c, 1.1, 6)
        d.t(cx, UY + 25, label, 13, INK, MONO)
    else:
        d.arrow([(cx, LY + LH + 2), (cx, UY - 2)], c, "warn", 1.2, "4 3")
        d.t(cx, UY + 25, label, 12, c, KR)

d.t(X0 - 40, 630, "PE 띠 한 칸 ≈ 1,390 PE · swap_1·여유 칸은 읽히게 키움 · 점선은 예시",
    11, SOFT, KR, "start")
d.legend(660, [("디스크 · PV", INFO), ("VG 풀", OK), ("LV root", ACC), ("여유 PE", WARN)])
d.save("05-01.lvm.svg")
print("ok 05-01.lvm")
