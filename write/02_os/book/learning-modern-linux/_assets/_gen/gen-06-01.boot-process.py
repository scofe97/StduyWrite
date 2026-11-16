# 06-01 §2 — 전원에서 셸까지 다섯 단계가 실제로 어디에 놓여 있고, 제어가 어디서 어디로 세 번 넘어가는가.
# 원문("The Linux Startup Process"):
#  1. "In modern environments, the Unified Extensible Firmware Interface (UEFI) spec defines the boot
#      configuration (stored in NVRAM) and the boot loader. In older systems, in this step, after the
#      Power On Self Test (POST) is completed, the Basic I/O System (BIOS ...) would initialize hardware
#      (managing I/O ports and interrupts) and hand over control to the boot loader."
#  2. "The boot loader has one goal: to bootstrap the kernel. ... current (e.g., GRUB 2, systemd-boot,
#      SYSLINUX, rEFInd) and legacy (e.g., LILO, GRUB 1)."
#  3. "The kernel is usually located in the /boot directory in a compressed form. ... After the
#      initialization of its subsystems, filesystems, and drivers ..., the kernel hands over control to
#      the init system, and with that the boot process proper ends."
#  4. "The init system is responsible for launching daemons (service processes) system-wide. This init
#      process is the root of the process hierarchy and with it has the process ID (PID) 1. ... the
#      process with PID 1 runs until you power off the system. Besides being responsible for launching
#      other daemons, the PID 1 process traditionally also takes care of orphaned processes."
#  5. "Usually, some other user-space-level initialization takes place after this, depending on the
#      environment" — 터미널·환경·셸 초기화, GUI 면 디스플레이 매니저와 그래픽 서버.
#  실제 값 — §6 저널 출력의 "systemd[1]: Starting My Greeting Service..." 와 "greeter.sh[21071]".
# 타입 스펙: type-architecture — 단계가 놓인 실제 자리(펌웨어 · 디스크 · 주기억장치)를 존으로 묶고,
#           제어가 넘어가는 세 자리를 번호 붙은 화살표 1·2·3 으로 싣는다. accent 는 PID 1 하나.
# 축약: 부트로더는 GRUB 2 를 대표로 세우고 나머지는 이름만 적었다. 점선은 예전 방식(BIOS)과
#       부모를 잃은 프로세스처럼 늘 있지는 않은 것이다. PID 1 아래 자식은 대표 넷만 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 740
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §2",
      "제어는 세 번 넘어가고, 마지막에 받은 PID 1 은 내려놓지 않는다",
      "펌웨어(UEFI, 설정은 NVRAM)가 디스크의 부트로더 GRUB 2 에 제어를 넘기고, 부트로더가 /boot 의 "
      "압축된 커널을 풀어 주기억장치에 올린다. 커널은 서브시스템·파일시스템·드라이버를 초기화한 뒤 "
      "init 에 제어를 넘기고 여기서 부팅 본체가 끝난다. PID 1 인 systemd[1] 은 데몬과 셸 같은 "
      "사용자 공간 프로세스를 띄우고 고아 프로세스를 거두며 전원을 끌 때까지 돈다.",
      "부팅 본체는 3 에서 끝나지만 PID 1 은 전원을 끌 때까지 돈다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{INK}05" '
               f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 4"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, KR, "start", 600)


def node(x, y, w, h, step, name, sub, c, dashed=False, focal=False, name_font=KR):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif dashed:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" '
                   f'stroke="{c}" stroke-width="1.1" stroke-dasharray="4 3"/>')
    else:
        d.box(x, y, w, h, PAPER2, c, 1.2, 8)
    if step:
        d.t(x + 14, y + 20, step, 12, SOFT, KR, "start")
    d.t(x + 14, y + (42 if step else 28), name, 14, c, name_font, "start", 600)
    d.t(x + 14, y + (62 if step else 48), sub, 12, MUTED, KR, "start")


# 존 — 연결선보다 먼저 그린다
zone(24, 112, 300, 220, "펌웨어 · 메인보드")
zone(348, 112, 588, 220, "디스크 · 부팅 매체")
zone(24, 352, 912, 300, "주기억장치")

# 1단계 — 펌웨어
node(44, 148, 260, 76, "1단계", "UEFI", "부팅 설정은 NVRAM 에", INFO)
node(44, 240, 260, 76, "1단계 · 예전", "BIOS", "POST 뒤 입출력 포트 · 인터럽트", SOFT, dashed=True)

# 2단계 — 부트로더, 커널 파일
node(368, 148, 248, 76, "2단계", "GRUB 2", "커널을 부트스트랩", INFO, name_font=MONO)
d.t(368, 256, "다른 현행  systemd-boot · SYSLINUX · rEFInd", 12, SOFT, MONO, "start")
d.t(368, 280, "레거시  LILO · GRUB 1", 12, SOFT, MONO, "start")
node(688, 148, 228, 76, "", "/boot", "압축된 커널 파일", INFO, name_font=MONO)

# 주기억장치 — 커널 공간 / 사용자 공간
d.t(44, 404, "커널 공간", 12, SOFT, KR, "start", 600)
node(560, 376, 356, 76, "3단계", "커널 (풀린 상태)", "서브시스템 · 파일시스템 · 드라이버 초기화", OK)
d.line(40, 468, 920, 468, RULE, 1, "4 4")
d.t(44, 492, "사용자 공간", 12, SOFT, KR, "start", 600)

# 제어가 넘어가는 세 자리 1·2·3 — 글자보다 먼저 그린다
d.arrow([(304, 186), (366, 186)], INK, "ar", 1.6)
d.t(335, 176, "1", 14, INK, KR, "middle", 600)
d.arrow([(616, 186), (686, 186)], MUTED, "ar", 1.2)
d.t(651, 176, "읽음", 12, MUTED, KR, "middle")
d.arrow([(802, 224), (802, 374)], INK, "ar", 1.6)
d.t(814, 300, "2. 풀어서 적재", 13, INK, KR, "start", 600)
d.arrow([(738, 452), (738, 502)], INK, "ar", 1.6)
d.t(750, 484, "3. 부팅 본체 끝", 13, INK, KR, "start", 600)

# 4단계 — PID 1
PX, PY, PW, PH = 608, 504, 260, 64
d.o.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(PX + 14, PY + 20, "4단계 · init · PID 1", 12, ACC, KR, "start")
d.t(PX + 14, PY + 44, "systemd[1]", 15, ACC, MONO, "start", 600)
d.t(PX + PW - 14, PY + 44, "전원 끌 때까지", 12, MUTED, KR, "end")

# 고아 프로세스 — 부모를 잃으면 PID 1 이 거둔다
d.arrow([(360, 536), (606, 536)], ACC, "acc", 1.2, "4 3")
d.t(483, 526, "거둠", 12, ACC, KR, "middle", 600)
d.o.append(f'<rect x="{120}" y="{508}" width="240" height="56" rx="8" fill="none" '
           f'stroke="{SOFT}" stroke-width="1.1" stroke-dasharray="4 3"/>')
d.t(136, 532, "고아 프로세스", 13, MUTED, KR, "start", 600)
d.t(136, 552, "부모가 먼저 끝남", 12, SOFT, KR, "start")

# PID 1 이 띄운 자식들 — 버스로 연결
kids = [("데몬 (서비스)", "시스템 전역", KR, MUTED),
        ("greeter.sh[21071]", "§6 로그의 그 프로세스", MONO, MUTED),
        ("터미널 · 셸", "5단계", KR, MUTED),
        ("디스플레이 매니저", "5단계 · GUI 라면", KR, MUTED)]
KW, KG, KY, BUS = 208, 16, 600, 584
xs = [44 + i * (KW + KG) for i in range(4)]
d.line(PX + PW / 2, PY + PH, PX + PW / 2, BUS, MUTED, 1.2)
d.line(xs[0] + KW / 2, BUS, xs[-1] + KW / 2, BUS, MUTED, 1.2)
for x in xs:
    d.arrow([(x + KW / 2, BUS), (x + KW / 2, KY - 2)], MUTED, "ar", 1.2)
for x, (name, sub, fam, c) in zip(xs, kids):
    d.box(x, KY, KW, 44, PAPER2, MUTED, 1.0, 6)
    d.t(x + KW / 2, KY + 19, name, 13, INK, fam, "middle", 600)
    d.t(x + KW / 2, KY + 36, sub, 12, MUTED, KR)

d.t(24, 676, "부트로더는 GRUB 2 를 대표로 · 점선은 예전 방식과 늘 있지는 않은 것 · 자식은 대표 넷",
    11, SOFT, KR, "start")
d.legend(692, [("펌웨어 · 디스크", INFO), ("커널", OK), ("PID 1", ACC), ("사용자 공간 프로세스", MUTED)])
d.save("06-01.boot-process.svg")
print("ok 06-01.boot-process")
