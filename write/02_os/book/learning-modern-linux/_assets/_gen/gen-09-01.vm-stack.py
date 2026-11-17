# 09-01 §3 — 하드웨어 보조 가상화가 아래에서 위로 쌓이는 순서.
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
# 주의: 이 도식은 원서 그림 9-1 을 옮긴 것이 아니라 위 서술과 본문 §3 의 출력으로 다시 세운 것이다.
#       libvirt 는 저자가 그림에 없다고 밝힌 것이라 VMM 위에 따로 둔 작은 칸으로만 적었다.
#       게스트 커널이 Windows 일 수도 있다는 원문 서술은 본문에 없어 그리지 않는다.
# 타입 스펙: type-layers — 아래(CPU)에서 위(유저 공간)로 쌓인 실제 구성. 층마다 본문의 확인 명령과
#           그 출력 값을 붙였다. accent 는 하이퍼바이저가 되는 커널 층 하나.
# 근거: 본문 §3 의 grep 출력(flags 줄의 vmx), lsmod 출력(kvm_intel 253952 0 · kvm 659456 1 kvm_intel),
#       "셋째 열은 쓰는 것의 수 · VM 을 띄우면 올라갑니다", Virtio 드라이버, libvirt, QEMU · Firecracker,
#       격리 예외 rowhammer · Meltdown · Spectre.
# 축약: flags 줄은 vmx 앞뒤만 남겼다. VMM 상자 안의 VM 은 하나만 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 744
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §3",
      "아래에서 위로 — CPU 가 받쳐야 커널이 하이퍼바이저가 된다",
      "가상화 스택을 아래에서 위로 쌓은 것. CPU flags 에 vmx 가 있고, 호스트 리눅스 커널에 kvm_intel 과 "
      "kvm 모듈이 올라와 커널이 하이퍼바이저가 된다. 그 위 유저 공간의 VMM 프로세스(QEMU, Firecracker)가 "
      "VM 하나를 관리하고, VM 안에는 Virtio 드라이버를 쓰는 게스트 커널과 게스트 프로세스가 돈다. "
      "kvm_intel 의 0 은 쓰는 VM 이 아직 없다는 뜻이다.",
      "KVM 한 층에서 리눅스 커널이 하이퍼바이저가 됩니다")

LX, X0, X1 = 24, 136, 836
UY0, UY1 = 100, 368          # 유저 공간
KY0, KY1 = 400, 520          # 호스트 커널
CY0, CY1 = 552, 640          # CPU

for y0, y1, name, sub in ((UY0, UY1, "유저 공간", "VMM · VM"), (KY0, KY1, "호스트 커널", "하이퍼바이저"),
                          (CY0, CY1, "CPU", "하드웨어")):
    d.o.append(f'<rect x="{LX}" y="{y0}" width="{X1 + 20 - LX}" height="{y1 - y0}" rx="8" '
               f'fill="{PAPER2}" fill-opacity="0.45" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(LX + 14, y0 + 26, name, 13, INK, KR, "start", 600)
    d.t(LX + 14, y0 + 44, sub, 12, SOFT, KR, "start")

# 선 먼저
d.arrow([(246, 152), (246, 170)], OK, "ok", 1.3)
d.arrow([(380, 356), (380, 434)], MUTED, "ar", 1.4)
d.arrow([(380, 488), (380, 572)], INFO, "info", 1.4)
d.arrow([(452, 462), (516, 462)], ACC, "acc", 1.3)

# 유저 공간
d.box(X0, 112, 220, 40, PAPER, OK, 1.0, 6)
d.t(X0 + 12, 137, "libvirt", 12, OK, MONO, "start", 600)
d.t(X0 + 80, 137, "VMM 표준화 API", 12, MUTED, KR, "start")
d.tone(X0, 172, 480, 184, OK, 8, "10", 1.2)
d.t(X0 + 16, 194, "VMM 프로세스", 13, OK, KR, "start", 600)
d.t(X0 + 124, 194, "QEMU · Firecracker", 12, INK, MONO, "start")
d.o.append(f'<rect x="{X0 + 16}" y="208" width="448" height="136" rx="6" fill="none" '
           f'stroke="{WARN}" stroke-width="1.2" stroke-dasharray="5 4"/>')
d.t(X0 + 30, 228, "VM", 12, WARN, MONO, "start", 600)
d.t(X0 + 60, 228, "격리 경계", 12, WARN, KR, "start")
d.box(X0 + 30, 240, 420, 40, PAPER, RULE, 1.0, 6)
d.t(X0 + 46, 265, "게스트 프로세스", 13, INK, KR, "start", 600)
d.box(X0 + 30, 292, 420, 40, PAPER, RULE, 1.0, 6)
d.t(X0 + 46, 317, "게스트 커널", 13, INK, KR, "start", 600)
d.t(X0 + 436, 317, "Virtio 드라이버", 12, MUTED, KR, "end")

d.box(656, 172, X1 - 656, 72, PAPER, RULE, 1.0, 8)
d.t(672, 198, "호스트 프로세스", 13, INK, KR, "start", 600)
d.t(672, 224, "VM 밖 · 게스트와 격리", 12, WARN, KR, "start")

d.t(392, 386, "KVM 인스턴스 관리", 12, MUTED, KR, "start")

# 호스트 커널
d.tone(X0, KY0 + 12, X1 - X0, KY1 - KY0 - 24, ACC, 8, "12", 1.4)
d.t(X0 + 16, KY0 + 30, "리눅스 커널 + KVM", 13, ACC, KR, "start", 600)
d.t(X1 - 16, KY0 + 30, "lsmod | grep kvm", 12, SOFT, MONO, "end")
d.box(152, 436, 300, 52, PAPER, ACC, 1.0, 6)
d.t(166, 456, "kvm_intel  253952  0", 12, INK, MONO, "start", 600)
d.t(166, 476, "쓰는 VM 0 · 띄우면 증가", 12, MUTED, KR, "start")
d.box(520, 436, 300, 52, PAPER, ACC, 1.0, 6)
d.t(534, 456, "kvm  659456  1  kvm_intel", 12, INK, MONO, "start", 600)
d.t(534, 476, "1 = kvm_intel 이 씀", 12, MUTED, KR, "start")

d.t(392, 542, "하드웨어 보조 가상화", 12, INFO, KR, "start")

# CPU
d.tone(X0, CY0 + 20, X1 - X0, CY1 - CY0 - 32, INFO, 8, "12", 1.2)
d.t(X0 + 16, CY0 + 42, "Intel VT · AMD-V", 13, INFO, MONO, "start", 600)
d.t(X1 - 16, CY0 + 42, "grep 'svm\\|vmx' /proc/cpuinfo", 12, SOFT, MONO, "end")
d.t(X0 + 16, CY0 + 64, "flags : … ds_cpl vmx tm2 …", 12, INK, MONO, "start")
d.t(X1 - 16, CY0 + 64, "코어마다 한 줄", 12, MUTED, KR, "end")

d.t(LX, 676, "격리 예외 · rowhammer · Meltdown · Spectre  ·  점선 = 격리 경계 · VM 은 하나만 그림",
    11, SOFT, KR, "start")
d.legend(696, [("CPU 조건", INFO), ("커널 = 하이퍼바이저", ACC), ("VMM 프로세스", OK), ("격리 경계", WARN)])
d.save("09-01.vm-stack.svg")
print("ok 09-01.vm-stack")
