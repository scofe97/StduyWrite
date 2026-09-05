# 06-01 §2 — 전원에서 셸까지 다섯 단계와 제어권이 넘어가는 자리.
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
# 타입 스펙: type-flowchart — 순서에 분기가 하나 있다(오늘날 UEFI · 예전 BIOS). 판정 마름모 대신
#           갈래 상자 둘로 그리고 다시 합류시킨다. accent 는 PID 1, 곧 끝나지 않는 단 하나의 단계.
#           축약: 부트로더 목록은 현행 넷·레거시 둘 중 대표만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 684
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §2",
      "제어권이 세 번 넘어가고, 마지막 하나는 끝나지 않는다",
      "전원 버튼에서 셸 프롬프트까지의 다섯 단계. 펌웨어가 부트로더에, 부트로더가 커널에, "
      "커널이 init 시스템에 제어를 넘긴다. 저자는 셋째 단계 끝에서 부팅 본체가 끝난다고 적는다.",
      "PID 1 은 전원을 끌 때까지 돕니다")

X0, CW, CH = 40, 800, 58
Y = 148
GAP = 18

# 1단계 — 갈래 둘
d.t(X0 + 12, Y - 8, "1단계 — 펌웨어", 13, INFO, KR, "start", 600)
HW = (CW - 16) / 2
for i, (name, body) in enumerate([
        ("오늘날 — UEFI", "부팅 설정은 NVRAM 에 · 명세가 부트로더를 정의한다"),
        ("예전 — BIOS", "POST 뒤 하드웨어 초기화 · 입출력 포트와 인터럽트 관리")]):
    x = X0 + i * (HW + 16)
    d.box(x, Y, HW, CH, PAPER2, INFO, 1.2, 8)
    d.t(x + 16, Y + 26, name, 13.5, INFO, KR, "start", 600)
    d.t(x + 16, Y + 48, body, 11.5, MUTED, KR, "start")

steps = [
    ("2단계 — 부트로더", "목표가 하나뿐이다 — 커널을 부트스트랩한다",
     "현행 GRUB 2 · systemd-boot · SYSLINUX · rEFInd  ·  레거시 LILO · GRUB 1", OK),
    ("3단계 — 커널", "/boot 에 압축된 채 있다가 풀려 주기억장치로 올라간다",
     "서브시스템 · 파일시스템 · 드라이버 초기화 뒤 init 에 넘긴다 — 부팅 본체는 여기서 끝", OK),
    ("4단계 — init 시스템", "시스템 전역의 데몬을 띄운다 · 프로세스 계층의 뿌리 · PID 1",
     "전원을 끌 때까지 돌고, 부모 없는 고아 프로세스를 거둔다", ACC),
    ("5단계 — 사용자 공간", "터미널 · 환경 · 셸 초기화",
     "GUI 라면 디스플레이 매니저와 그래픽 서버가 선호와 설정을 반영해 뜬다", MUTED),
]
y = Y + CH + GAP
for name, body, sub, col in steps:
    d.arrow([(W / 2, y - GAP), (W / 2, y - 2)], MUTED, "ar", 1.4)
    focal = (col is ACC)
    if focal:
        d.o.append(f'<rect x="{X0}" y="{y}" width="{CW}" height="{CH + 16}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(X0, y, CW, CH + 16, PAPER2, col, 1.2, 8)
    d.t(X0 + 16, y + 26, name, 14, col if col is not MUTED else INK, KR, "start", 600)
    d.t(X0 + 16, y + 50, body, 12, INK if focal else MUTED, KR, "start")
    d.t(X0 + 16, y + 70, sub, 11.5, MUTED, KR, "start")
    y += CH + 16 + GAP

d.tone(X0, y - GAP + 8, CW, 44, INFO)
d.t(X0 + 20, y - GAP + 36,
    "저자는 이 다섯 중 넷째와 다섯째가 이 책의 문맥에서 가장 중요하다고 적습니다.", 12, MUTED, KR, "start")

d.legend(y + 40, [("제어를 넘기는 쪽", INFO), ("커널까지", OK), ("끝나지 않는 단계", ACC)])
d.save("06-01.boot-process.svg")
print("ok 06-01.boot-process")
