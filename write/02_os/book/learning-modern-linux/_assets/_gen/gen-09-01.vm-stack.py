# 09-01 §2 — 하드웨어 보조 가상화가 아래에서 위로 쌓이는 순서.
# 원문("Virtual Machines"): "you see the virtualization architecture on a conceptual level, comprising
#       the following (starting from the bottom): The CPU — Must support hardware virtualization.
#       The kernel-based virtual machine — Found in the Linux kernel. Components in the user space
#       include the following: A Virtual Machine Monitor (VMM) — Manages VMs and emulates virtual
#       devices, such as QEMU and Firecracker. There is also libvirt, a library that exposes a generic
#       API aiming to standardize VMM ... consider it part of the VMM block. The guest kernel —
#       Typically also a Linux kernel but could also be Windows. The guest processes — Running on the
#       guest kernel."
#       격리는 "The processes that run natively on the host kernel (in Figure 9-1, process 1 and process
#       2) are isolated from the guest processes. This means that in general the physical CPU and memory
#       of the host are not affected by guest activities." 이고, 예외로 "rowhammer or Meltdown and
#       Spectre" 를 든다.
# 주의: 이 도식은 원서 그림 9-1 을 옮긴 것이 아니라 위 서술로 다시 세운 것이다. 저자가 "not explicitly
#       shown in the figure" 라 밝힌 libvirt 도 VMM 칸에 함께 적었다.
# 타입 스펙: type-layers — 아래에서 위로 쌓인 추상 수준. 저자 자신이 "starting from the bottom" 이라
#           적어 순서를 명시한다. accent 는 커널이 하이퍼바이저가 되는 한 층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
LX, LW, LH, GAP, Y0 = 24, 516, 64, 10, 124
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §2",
      "아래에서 위로 — CPU 가 받쳐야 커널이 하이퍼바이저가 된다",
      "저자가 밑에서부터라고 밝힌 순서대로 쌓은 것. 오른쪽은 같은 호스트 커널 위에서 네이티브로 도는 "
      "프로세스들이고, 게스트와 격리된다.",
      "원서 그림을 옮긴 것이 아니라 저자의 서술로 다시 세운 것입니다")

layers = [
    ("게스트 프로세스", "게스트 커널 위에서 돈다", MUTED, False),
    ("게스트 커널", "보통 리눅스지만 윈도우일 수도 있다", MUTED, False),
    ("가상 머신 모니터(VMM)", "VM 을 관리하고 가상 장치를 흉내 낸다 — QEMU · Firecracker · libvirt", OK, False),
    ("KVM", "리눅스 커널 안에 있다 — 커널이 곧 하이퍼바이저다", ACC, True),
    ("CPU", "하드웨어 가상화를 지원해야 한다", INFO, False),
]
for i, (name, note, col, focal) in enumerate(layers):
    y = Y0 + i * (LH + GAP)
    if focal:
        d.tone(LX, y, LW, LH, ACC, 8, "12", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, col, 1.2, 8)
    d.t(LX + 18, y + 26, name, 13.5, col, KR, "start", 600)
    d.t(LX + 18, y + 47, note, 11.5, MUTED, KR, "start")
d.t(LX + LW - 8, Y0 - 12, "위", 10.5, SOFT, KR, "end")
d.t(LX + LW - 8, Y0 + 5 * (LH + GAP) + 4, "아래", 10.5, SOFT, KR, "end")

d.o.append(f'<rect x="{LX}" y="{Y0 - 6}" width="{LW}" height="{3 * (LH + GAP) + 6}" rx="10" '
           f'fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="5 4"/>')
d.t(LX + 12, Y0 - 14, "유저 공간", 10.5, SOFT, KR, "start", 600)

HX = LX + LW + 20
HW = W - HX - 24
d.box(HX, Y0, HW, 3 * (LH + GAP) - GAP, PAPER2, RULE, 1.1, 8)
d.t(HX + 16, Y0 + 26, "호스트 커널 위의", 12.5, INK, KR, "start", 600)
d.t(HX + 16, Y0 + 44, "네이티브 프로세스", 12.5, INK, KR, "start", 600)
for k, nm in enumerate(("프로세스 1", "프로세스 2")):
    d.box(HX + 16, Y0 + 62 + k * 40, HW - 32, 32, PAPER, MUTED, 1.0, 5)
    d.t(HX + 16 + (HW - 32) / 2, Y0 + 82 + k * 40, nm, 11.5, MUTED, KR)
d.t(HX + 16, Y0 + 158, "게스트와 격리됩니다", 11.5, SOFT, KR, "start")

NY = Y0 + 5 * (LH + GAP) + 26
d.t(24, NY, "격리의 뜻은 이것입니다. 대체로 호스트의 물리 CPU 와 메모리는 게스트의 활동에 영향받지 않습니다.",
    12, INK, KR, "start", 600)
d.t(24, NY + 24, "VM 안에서 공격이 일어나도 호스트 커널과 프로세스는 무사합니다. VM 에 호스트 시스템 "
                 "접근을 따로 주지 않은 한에서입니다.", 12, MUTED, KR, "start")
d.t(24, NY + 48, "저자는 실무에서 예외가 있을 수 있다고 덧붙이며 rowhammer 와 Meltdown 과 Spectre 를 듭니다.",
    12, SOFT, KR, "start")

d.legend(NY + 72, [("커널이 하이퍼바이저", ACC), ("하드웨어 조건", INFO),
                   ("유저 공간", OK), ("격리된 프로세스", MUTED)])
d.save("09-01.vm-stack.svg")
print("ok 09-01.vm-stack")
