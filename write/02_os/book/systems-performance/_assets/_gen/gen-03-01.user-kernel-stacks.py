# 03-01 §8 — 시스템 콜 경계에서 갈리는 유저 스택과 커널 스택, 그리고 본문의 커널 스택 여섯 줄.
# 타입 스펙: type-layers — 앱 → 시스템 라이브러리 → 시스템 콜 → 커널 → 장치로 쌓인 층(원서 그림 3.10).
#           축약: 층 오른쪽에 찍힌 스택(leaf-to-root)을 목록으로 붙이고, 맨 아래 줄을 시스템 콜 층에 잇는다.
#           층 높이 56 · stride 64, 프레임 높이 28 · stride 32.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 600
LX, LW, LH, Y0, ST = 152, 332, 56, 132, 64
FX, FW, FH, FS = 600, 312, 28, 32

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-01 §8",
       "유저 스택과 커널 스택",
       "시스템 콜을 실행하는 스레드는 스택이 둘이다. 경계 위의 앱·라이브러리 호출은 유저 스택에, 경계 아래 커널 실행은 별도의 커널 스택에 쌓인다. 오른쪽은 본문의 TCP 전송 커널 스택을 찍힌 순서(leaf-to-root) 그대로 둔 것이다.",
       "본문의 스택 여섯 줄은 모두 경계 아래에 있습니다")

LAYERS = [("Application", "앱 코드", None), ("System Libraries", "libc 등", None),
          ("System Calls", "커널 입구", ACC), ("Kernel", "커널 코드", None), ("Devices", "장치", None)]
for i, (name, sub, c) in enumerate(LAYERS):
    y = Y0 + i * ST
    if c: d.tone(LX, y, LW, LH, c, 6)
    else: d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(LX + 20, y + 34, name, 14, c if c else INK, MONO, "start", 600)
    d.t(LX + LW - 20, y + 34, sub, 12, MUTED, KR, "end")

# 유저/커널 경계 — Libraries 와 System Calls 사이
BY = Y0 + 2 * ST - 4
d.line(24, BY, LX + LW + 24, BY, WARN, 1.2, "6 4")
d.t(LX + LW + 28, BY - 6, "유저 레벨", 12, WARN, KR, "start")
d.t(LX + LW + 28, BY + 16, "커널 레벨", 12, WARN, KR, "start")

# 왼쪽 범위 괄호
def bracket(y1, y2, label, c):
    x = LX - 24
    d.path(f"M {x + 8} {y1} L {x} {y1} L {x} {y2} L {x + 8} {y2}", c, 1.4)
    d.t(x - 8, (y1 + y2) / 2 + 5, label, 13, c, KR, "end", 600)
bracket(Y0, Y0 + ST + LH, "유저 스택", OK)
bracket(Y0 + 2 * ST, Y0 + 3 * ST + LH, "커널 스택", INFO)

# 찍힌 커널 스택 — leaf 가 위
FRAMES = ["tcp_sendmsg+1", "sock_sendmsg+62", "SYSC_sendto+319", "sys_sendto+14",
          "do_syscall_64+115", "entry_SYSCALL_64_after_hwframe+61"]
FY0 = Y0 + 8
d.t(FX, FY0 - 16, "찍힌 커널 스택", 13, INFO, KR, "start", 600)
for i, f in enumerate(FRAMES):
    y = FY0 + i * FS
    d.box(FX, y, FW, FH, PAPER2, INFO if i in (0, 5) else RULE, 1.0, 4)
    d.t(FX + 12, y + 19, f, 12, INK, MONO, "start")
d.t(FX + FW + 8, FY0 + 19, "leaf", 12, SOFT, MONO, "start")
d.t(FX + FW + 8, FY0 + 5 * FS + 19, "입구", 12, SOFT, KR, "start")
# 맨 아래 줄 → System Calls 층
ly = FY0 + 5 * FS + FH / 2
sy = Y0 + 2 * ST + LH / 2
d.arrow([(FX, ly), (FX - 40, ly), (FX - 40, sy), (LX + LW + 4, sy)], INFO, "info", 1.4)
# 읽는 방향
rx = FX + FW / 2
d.arrow([(rx, FY0 + 6 * FS + 36), (rx, FY0 + 6 * FS + 8)], MUTED, "ar", 1.4)
d.t(rx, FY0 + 6 * FS + 56, "아래에서 위로 · 어떻게 왔나", 13, MUTED, KR, "middle", 600)

d.legend(Y0 + 5 * ST + 24, [("시스템 콜 경계", ACC), ("유저 스택 범위", OK), ("커널 스택 범위", INFO)])
d.save("03-01.user-kernel-stacks.svg")
