# 06-01 §4 — systemd 단위의 종류와 단위 파일이 놓이는 세 자리.
# 원문("Units"): "A unit in systemd is a logical grouping with different semantics depending on its
#       function and/or the resource it targets."
#       주요 넷 — service units("Describe how to manage a service or application"),
#       target units("Capture dependencies"), mount units("Define a mountpoint"),
#       timer units("Define timers for cron jobs and the like").
#       덜 중요한 것 — socket("Describes a network or IPC socket"), device("For udev or sysfs
#       filesystems"), automount("Configures automatic mountpoints"), swap("Describes swap space"),
#       path("For path-based activation"), snapshot("Allows for reconstructing the current state of the
#       system after changes"), slice("Associated with cgroups"), scope("Manages sets of system
#       processes created externally").
#       파일 자리 — "/lib/systemd/system: Package-installed units", "/etc/systemd/system: System
#       admin–configured units", "/run/systemd/system: Nonpersistent runtime modifications".
# 타입 스펙: type-tree — 뿌리(단위)에서 갈래로 내려가는 분류, 직교 연결. accent 는 §6 예제가
#           실제로 쓰는 두 종류. 축약: 덜 중요한 여덟은 이름만 칩으로 늘어놓았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §4",
      "무엇을 언제 어떻게 돌릴지는 단위로 말한다",
      "systemd 에게 지시하는 방법은 단위 하나뿐이다. 겨냥하는 자원에 따라 의미가 갈리고, "
      "파일로 직렬화되어야 systemd 가 알아본다.",
      "6절 예제가 쓰는 것은 service 와 timer 둘입니다")

RX, RY, RW, RH = 340, 148, 200, 56
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(RX + RW / 2, RY + 24, "단위", 14, INK, KR, "middle", 600)
d.t(RX + RW / 2, RY + 44, "겨냥하는 자원이 의미를 정한다", 11, MUTED, KR)

BW, GAP, BY, BUS = 200, 16, 268, 232
main = [
    ("service", "서비스나 애플리케이션을", "어떻게 관리할지 서술한다", ACC),
    ("target", "의존성을 잡는다", "", OK),
    ("mount", "마운트 지점을", "정의한다", OK),
    ("timer", "cron 작업 같은 것을 위한", "타이머를 정의한다", ACC),
]
for i, (name, l1, l2, col) in enumerate(main):
    x = 24 + i * (BW + GAP)
    cx = x + BW / 2
    d.path(f"M {RX + RW / 2} {RY + RH} L {RX + RW / 2} {BUS} L {cx} {BUS} L {cx} {BY - 2}",
           col, 1.3, m="acc" if col is ACC else "ok")
    if col is ACC:
        d.o.append(f'<rect x="{x}" y="{BY}" width="{BW}" height="92" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, BY, BW, 92, PAPER2, col, 1.2, 8)
    d.t(x + 16, BY + 28, name, 14, col, MONO, "start", 600)
    d.t(x + 16, BY + 52, l1, 11.5, MUTED, KR, "start")
    if l2:
        d.t(x + 16, BY + 72, l2, 11.5, MUTED, KR, "start")

d.t(24, 400, "덜 중요하다고 저자가 묶어 둔 것들", 12.5, SOFT, KR, "start", 600)
minor = ["socket", "device", "automount", "swap", "path", "snapshot", "slice", "scope"]
cx = 60
for name in minor:
    d.chip(cx, 428, name, MUTED, 11)
    cx += len(name) * 8 + 34

d.t(24, 470, "단위 파일이 놓이는 세 자리", 12.5, SOFT, KR, "start", 600)
paths = [
    ("/lib/systemd/system", "패키지가 설치한 단위", INFO),
    ("/etc/systemd/system", "시스템 관리자가 설정한 단위", INFO),
    ("/run/systemd/system", "영속적이지 않은 런타임 수정", ACC),
]
PW = 272
for i, (p, note, col) in enumerate(paths):
    x = 24 + i * (PW + 12)
    d.box(x, 490, PW, 66, PAPER2, col, 1.1, 6)
    d.t(x + 16, 516, p, 12.5, col, MONO, "start", 600)
    d.t(x + 16, 540, note, 11.5, MUTED, KR, "start")

d.legend(584, [("6절 예제가 쓰는 종류와 자리", ACC), ("나머지 주요 단위", OK),
               ("파일이 놓이는 자리", INFO)])
d.save("06-01.systemd-units.svg")
print("ok 06-01.systemd-units")
