# 05-01 §8 — 가짜 파일시스템 셋이 각각 무엇을 감싸는가.
# 원문("Pseudo Filesystems"): "Meet pseudo filesystems: they only pretend to be filesystems so that we
#       can interact with them in the usual manner (ls, cd, cat), but really they are wrapping some kernel
#       interface."
#   procfs: "Linux inherited the /proc filesystem (procfs) from UNIX. The original intention was to publish
#            process-related information from the kernel, to make it consumable for system commands such as
#            ps or free. It has very few rules around structure, allows read-write access, and over time
#            many things found their way into it."
#   sysfs:  "Where procfs is pretty Wild West, the /sys filesystem (sysfs) is a Linux-specific, structured
#            way for the kernel to expose select information (such as about devices) using a standardized
#            layout." 디렉토리 여덟 — block/ bus/ class/ dev/ devices/ firmware/ fs/ module/.
#           "You'll find certain information duplicated in sysfs that is also available in procfs, but
#            other information (such as memory information) is only available in procfs."
#   devfs:  "The /dev filesystem (devfs) hosts device special files" — Block · Character · Special devices.
# 주의: /dev 를 오늘날 채우는 것은 devfs 가 아니라 devtmpfs 다. 근거는 저자 자신의 findmnt 출력
#       (`udev  devtmpfs  3.8G  0  3.8G  0%  /dev`)이라 도식에도 그 이름을 함께 적는다.
# 타입 스펙: type-tree — 뿌리에서 갈래로 내려가는 포함 관계, 직교 연결. accent 는 저자가
#           procfs 에만 있다고 못 박은 정보 하나. 축약: 각 갈래의 항목은 저자가 든 것 중 일부만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 656
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "파일시스템인 척하며 커널 인터페이스를 감싼다",
      "셋 다 ls 와 cat 으로 읽히지만 뒤에 블록 장치가 없다. 무엇을 감싸느냐가 다르고, "
      "그래서 성격도 다르다.",
      "저자는 procfs 를 서부 개척지에 빗댑니다")

RX, RY, RW, RH = 340, 148, 200, 56
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(RX + RW / 2, RY + 24, "VFS", 14, INK, KR, "middle", 600)
d.t(RX + RW / 2, RY + 44, "같은 손잡이, 블록 장치 없이", 11.5, MUTED, KR)

BW, GAP, BY = 272, 16, 268
BUS = 232
branches = [
    ("/proc — procfs", "유닉스에서 물려받음", INFO,
     ["구조 규칙이 거의 없고 읽기·쓰기 가능",
      "PID 별 정보와 마운트 · 네트워크",
      "TTY 드라이버 · 메모리 · 업타임",
      "cat /proc/self/status"]),
    ("/sys — sysfs", "리눅스 고유, 표준 배치", OK,
     ["디렉토리 여덟이 표준 배치를 이룹니다",
      "block · bus · class · dev",
      "devices · firmware · fs · module",
      "ls -al /sys/block/sda/"]),
    ("/dev — devtmpfs", "저자는 devfs 라 부름", WARN,
     ["블록 장치 · 문자 장치 · 특수 장치",
      "/dev/null · /dev/random",
      "/dev/tty · /dev/urandom",
      "echo \"something\" > /dev/tty"]),
]
for i, (name, sub, col, items) in enumerate(branches):
    x = 24 + i * (BW + GAP)
    cx = x + BW / 2
    d.path(f"M {RX + RW / 2} {RY + RH} L {RX + RW / 2} {BUS} L {cx} {BUS} L {cx} {BY - 2}",
           col, 1.3, m="ar")
    d.box(x, BY, BW, 176, PAPER2, col, 1.2, 8)
    d.t(x + 16, BY + 28, name, 14, col, MONO, "start", 600)
    d.t(x + 16, BY + 48, sub, 11.5, MUTED, KR, "start")
    d.line(x + 14, BY + 62, x + BW - 14, BY + 62, RULE, 1)
    for j, it in enumerate(items):
        d.t(x + 16, BY + 86 + j * 24, it, 11.5, INK if j < 3 else SOFT,
            KR if j < 3 else MONO, "start")

AY = 476
d.o.append(f'<rect x="24" y="{AY}" width="{BW}" height="72" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(40, AY + 26, "메모리 정보는 여기에만", 13, ACC, KR, "start", 600)
d.t(40, AY + 48, "겹치는 정보가 있지만 저자는 메모리", 11.5, ACC, KR, "start")
d.t(40, AY + 66, "정보가 procfs 에만 있다고 못 박습니다", 11.5, MUTED, KR, "start")
d.path(f"M {24 + BW / 2} {BY + 176} L {24 + BW / 2} {AY - 2}", ACC, 1.3, m="acc", dash="6 5")

d.tone(24 + BW + GAP, AY, BW * 2 + GAP, 72, WARN)
d.t(40 + BW + GAP, AY + 26, "이름이 어긋난 자리", 13, INK, KR, "start", 600)
d.t(40 + BW + GAP, AY + 48,
    "저자는 /dev 를 devfs 라 부르지만, 같은 장 앞쪽의 findmnt 출력 첫 줄은", 11.5, MUTED, KR, "start")
d.t(40 + BW + GAP, AY + 66,
    "udev  devtmpfs  ...  /dev 입니다. 커널이 만들고 그 위에서 udev 가 돕니다.",
    11.5, MUTED, KR, "start")

d.legend(584, [("규칙이 느슨한 쪽", INFO), ("정돈된 쪽", OK),
               ("이름을 확인해야 하는 쪽", WARN), ("여기에만 있는 정보", ACC)])
d.save("05-01.pseudo-fs.svg")
print("ok 05-01.pseudo-fs")
