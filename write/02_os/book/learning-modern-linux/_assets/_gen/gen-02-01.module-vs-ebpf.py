# 02-01 §8 — 커널을 밖에서 늘리는 두 길이 겹치는 곳과 갈리는 곳.
# 원문("Kernel Extensions"): 모듈은 "a program that you can load into a kernel on demand. That is, you do
#       not necessarily have to recompile the kernel and/or reboot the machine" 이고, 목록은
#       `find /lib/modules/$(uname -r) -type f -name '*.ko*'`, 적재된 것은 `lsmod`(같은 정보가
#       /proc/modules 에도 있다), 의존성은 `modprobe --show-depends` 로 본다.
#       eBPF 는 "a feature of the Linux kernel, and you'll need the Linux kernel version 3.15 or above",
#       "It enables you to safely and efficiently extend the Linux kernel functions by using the bpf
#       syscall. eBPF is implemented as an in-kernel virtual machine using a custom 64-bit RISC
#       instruction set." 쓰임새로 CNI 플러그인(Cilium·Calico), 관측(bpftrace·Hubble),
#       보안 통제(Falco), 네트워크 부하분산(katran)을 든다.
# 타입 스펙: type-venn — 두 집합의 교집합이 논점이다. 라벨은 원 밖, 교집합 라벨은 겹침 안,
#           focal 은 교집합 한 곳, 중심·반지름은 4의 배수.
#           배타 영역의 가로 폭이 좁으므로 항목은 15자 안쪽으로 끊어 원 안에 담는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, KR, MONO

W, H = 880, 700
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §8",
      "모듈과 eBPF 가 겹치는 곳과 갈리는 곳",
      "커널을 소스에 손대지 않고 늘리는 두 길을 집합으로 놓은 것. 가운데가 둘이 공유하는 성질이고, "
      "양쪽 날개가 각자의 방식이다.",
      "둘 다 커널을 다시 빌드하지 않지만 넣는 방법과 안전 장치가 다릅니다")

LX, RX, CY, R = 340, 540, 356, 188
MID = (LX + RX) // 2

d.o.append(f'<circle cx="{LX}" cy="{CY}" r="{R}" fill="{MUTED}0A" stroke="{MUTED}" stroke-width="1"/>')
d.o.append(f'<circle cx="{RX}" cy="{CY}" r="{R}" fill="{INFO}0A" stroke="{INFO}" stroke-width="1"/>')
d.o.append(f'<circle cx="{MID}" cy="{CY}" r="72" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')

d.t(MID, CY - 20, "공통", 13, ACC, KR, "middle", 600)
d.t(MID, CY + 6, "커널을 다시", 12, ACC, KR)
d.t(MID, CY + 26, "빌드하지 않는다", 12, ACC, KR)

# 라벨은 원 밖에 두고 짧은 연결선으로 잇는다
d.t(232, 124, "KERNEL MODULE", 8, SOFT, MONO, "middle")
d.t(232, 148, "모듈", 16, MUTED, KR, "middle", 600)
d.path(f"M 232 160 L 232 208", MUTED, 0.8, m="ar")

d.t(648, 124, "EXTENDED BPF", 8, SOFT, MONO, "middle")
d.t(648, 148, "eBPF", 16, INFO, MONO, "middle", 600)
d.path(f"M 648 160 L 648 208", INFO, 0.8, m="info")

for k, line in enumerate([".ko 를 필요할 때 적재",
                          "lsmod · /proc/modules",
                          "modprobe 로 의존성",
                          "제조사 드라이버를 끼울 때",
                          "커널 코드 그대로 실행"]):
    d.t(262, 284 + k * 26, line, 12, MUTED, MONO if k == 1 else KR)

for k, line in enumerate(["bpf 시스템 콜로 넣는다",
                          "커널 안 가상 머신에서 실행",
                          "64비트 RISC 명령셋",
                          "커널 3.15 이상 필요",
                          "안전하고 효율적으로 확장"]):
    d.t(618, 284 + k * 26, line, 12, INFO if k < 4 else MUTED, KR)

for k, line in enumerate([
        "재부팅 없이 넣는다는 점은 둘이 같습니다. 갈리는 것은 넣는 통로와 안전 장치입니다.",
        "저자가 든 eBPF 의 쓰임새는 넷입니다. 쿠버네티스 파드 네트워킹의 CNI 플러그인(Cilium · Calico),",
        "커널 트레이싱과 관측(bpftrace · Hubble), 보안 통제(Falco), 네트워크 부하분산(katran)."]):
    d.t(24, 580 + k * 22, line, 12, SOFT if k == 0 else MUTED, KR, "start")

d.legend(648, [("둘이 공유하는 성질", ACC), ("모듈만의 것", MUTED), ("eBPF 만의 것", INFO)])
d.save("02-01.module-vs-ebpf.svg")
print("ok 02-01.module-vs-ebpf")
