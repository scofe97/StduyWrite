# 05-01 §6 — 파티션이나 논리 볼륨을 실제로 쓰기까지의 세 단계.
# 원문("Filesystem Operations"): "There are two steps involved: creating the filesystem—in other non-Linux
#       operating systems, this step is sometimes called formatting—and then mounting it, or inserting it
#       into the filesystem tree."
#       "mkfs takes two primary inputs: the type of filesystem you want to create ... and the device you
#       want to create the filesystem on."
#       "mount takes two main inputs: the device you want to attach and the place in the filesystem tree.
#       In addition, you can provide other inputs, including mount options (via -o) such as read-only, and
#       bind mounts—via --bind—for mounting directories into the filesystem tree."
#       "the mounts are valid only for as long as the system is running, so in order to make it permanent,
#       you need to use the fstab file (/etc/fstab)."
#       fstab 주석 원문 — "Use 'blkid' to print the universally unique identifier for a device; this may be
#       used with UUID= as a more robust way to name devices that works even if disks are added and removed."
# 주의: 붙이기 칸의 예는 원문이 SD 카드 문맥에서 든 `mount -t vfat /dev/sdX2 /media` 를 그대로 쓴다.
#       원문에 없는 명령을 지어내지 않는다.
# 타입 스펙: type-process — 같은 의미 슬롯(명령 · 받는 입력 · 남는 것)이 단계마다 반복되고
#           순서가 화살표로 흐른다. accent 는 저자가 6장에서 다시 보겠다고 미룬 입력 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §6",
      "만들고 붙이고, 재부팅 뒤에도 남게 한다",
      "저자는 두 단계라고 적지만 실제로는 셋이다. 세 번째가 없으면 시스템을 껐다 켜는 순간 "
      "앞의 둘이 사라진다.",
      "mount 는 시스템이 도는 동안에만 유효합니다")

CW, CH, GAP, X0, Y0 = 268, 176, 16, 24, 156
steps = [
    ("mkfs", "만들기", "받는 입력 둘", "파일시스템 종류 · 대상 장치",
     "mkfs -t ext4 /dev/vg/lv", "다른 OS 에서는 포맷이라 부르는 일", INFO),
    ("mount", "붙이기", "받는 입력 둘", "붙일 장치 · 트리 안의 자리",
     "mount -t vfat /dev/sdX2 /media", "만든 종류로 붙여야 합니다", OK),
    ("/etc/fstab", "되살리기", "한 줄에 여섯 칸", "장치 · 지점 · 종류 · 옵션 · dump",
     "UUID=2A11-27C0 /boot/efi vfat", "디스크를 더하고 빼도 어긋나지 않습니다", MUTED),
]
for i, (cmd, name, k1, k2, ex, note, col) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    d.box(x, Y0, CW, CH, PAPER2, col, 1.2, 8)
    d.t(x + 18, Y0 + 28, cmd, 14, col, MONO, "start", 600)
    d.t(x + CW - 18, Y0 + 28, name, 14, INK, KR, "end", 600)
    d.line(x + 14, Y0 + 42, x + CW - 14, Y0 + 42, RULE, 1)
    d.t(x + 18, Y0 + 66, k1, 11.5, SOFT, KR, "start")
    d.t(x + 18, Y0 + 88, k2, 12, MUTED, KR, "start")
    d.o.append(f'<rect x="{x + 14}" y="{Y0 + 104}" width="{CW - 28}" height="28" rx="5" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
    d.t(x + 24, Y0 + 123, ex, 11, INK, MONO, "start")
    d.t(x + 18, Y0 + 156, note, 11.5, MUTED, KR, "start")
    if i < 2:
        d.arrow([(x + CW, Y0 + CH / 2), (x + CW + GAP - 2, Y0 + CH / 2)], MUTED, "ar", 1.4)

BY = 368
d.o.append(f'<rect x="{X0 + CW + GAP}" y="{BY}" width="{CW}" height="76" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(X0 + CW + GAP + 18, BY + 26, "--bind", 13, ACC, MONO, "start", 600)
d.t(X0 + CW + GAP + 18, BY + 48, "디렉토리를 트리의 다른 자리에", 11.5, ACC, KR, "start")
d.t(X0 + CW + GAP + 18, BY + 66, "붙이는 옵션 — 6장에서 다시", 11.5, MUTED, KR, "start")
d.path(f"M {X0 + CW + GAP + CW / 2} {Y0 + CH} L {X0 + CW + GAP + CW / 2} {BY - 2}",
       ACC, 1.4, m="acc", dash="6 5")

d.tone(X0 + 2 * (CW + GAP), BY, CW, 76, MUTED)
d.t(X0 + 2 * (CW + GAP) + 18, BY + 26, "UUID= 로 지목하기", 13, INK, KR, "start", 600)
d.t(X0 + 2 * (CW + GAP) + 18, BY + 48, "blkid 로 찍어서 적으면 장치 이름이", 11.5, MUTED, KR, "start")
d.t(X0 + 2 * (CW + GAP) + 18, BY + 66, "바뀌어도 마운트가 살아 있습니다", 11.5, MUTED, KR, "start")

d.legend(480, [("만들기", INFO), ("붙이기", OK), ("컨테이너로 이어지는 입력", ACC)])
d.save("05-01.mkfs-mount.svg")
print("ok 05-01.mkfs-mount")
