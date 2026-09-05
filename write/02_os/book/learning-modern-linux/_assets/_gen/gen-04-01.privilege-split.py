# 04-01 §6 — 전부 아니면 전무라는 이분법을 깨 온 장치들.
# 원문: 전통은 "Linux traditionally has an all-or-nothing attitude—that is, you are either a superuser
#       who has the power to change everything or you are a normal user with limited access."
#       그리고 커널은 특권 프로세스(effective UID 0)와 비특권 프로세스 둘만 구분한다.
#       capability — "With the introduction of the capabilities syscall in kernel v2.2, this binary
#       worldview has changed: the privileges traditionally associated with root are now broken down into
#       distinct units that can be independently assigned on a per-thread level."
#       seccomp — "Secure computing mode (seccomp) is a Linux kernel feature available since 2005."
#       AppArmor — "included in the Linux kernel since version 2.6.36 and rather popular in the Ubuntu
#       family of Linux distributions".
#       SELinux — "Probably the best-known implementation of mandatory access control for Linux" 이지만
#       원문이 도입 시점을 밝히지 않아 축 위에 두지 않고 아래 문장으로만 적는다.
# 타입 스펙: type-timeline — 사건이 순서 위에 놓이고 세대가 바꾼 것을 보인다.
#           축약: 원문이 둘은 커널 버전으로, 하나는 연도로 밝혀 눈금이 균질하지 않다.
#           그래서 가로축을 척도가 아니라 도입 순서로 두고 각 점에 원문 표기를 그대로 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, RULE, KR, MONO

W, H = 880, 452
d = D(W, H, "LEARNING MODERN LINUX · 04-01 §6",
      "root 냐 아니냐를 쪼개 온 장치들",
      "리눅스가 특권을 둘로만 나누던 자리에 무엇이 언제 들어왔는지를 순서로 편 것. "
      "가로축은 척도가 아니라 도입 순서이고, 각 점의 표기는 원문이 밝힌 그대로다.",
      "원문이 둘은 커널 버전으로, 하나는 연도로 밝힙니다")

X0 = 84
SPAN = W - X0 - 84
BY = 184

events = [
    (0.00, "전통", "root 는 제약이 없다", MUTED, True),
    (0.30, "커널 v2.2", "capability — root 의 특권을 쪼갠다", ACC, False),
    (0.62, "2005년", "seccomp — 쓸 수 있는 시스템 콜을 줄인다", INFO, True),
    (0.94, "커널 v2.6.36", "AppArmor — 강제적 접근 통제", OK, False),
]

sx, ex = X0 + SPAN * 0.30, X0 + SPAN * 0.94
d.tone(sx, BY - 14, ex - sx, 28, ACC, r=4, op="10", sw=0.0)
d.t((sx + ex) / 2, BY + 84, "이분법이 잘게 쪼개지는 구간", 12, ACC, KR, "middle", 600)

d.line(X0, BY, X0 + SPAN, BY, RULE, 1.0)
for frac, label, sub, c, above in events:
    x = X0 + SPAN * frac
    r = 6 if c is ACC else 4
    d.o.append(f'<circle cx="{x}" cy="{BY}" r="{r}" fill="{c}"/>')
    ly = BY - 24 if above else BY + 24
    d.line(x, BY + (-8 if above else 8), x, ly + (6 if above else -6), c, 0.8)
    d.t(x, ly + (0 if above else 14), label, 12.5, INK, KR, "middle", 600)
    d.t(x, ly + (-18 if above else 32), sub, 12, MUTED, KR)

cy = BY + 108
d.tone(X0 - 68, cy, W - 32 - 16, 60, WARN)
d.t(X0 - 50, cy + 26, "가장 널리 알려진 강제적 접근 통제 구현은 SELinux 입니다", 13, INK, KR, "start", 600)
d.t(X0 - 50, cy + 46, "정부 기관의 높은 보안 요구를 맞추려고 개발됐고 규칙이 엄격해 사용성이 떨어집니다. "
                      "원문이 도입 시점을 밝히지 않아 축에 두지 않았습니다.", 12, MUTED, KR, "start")

d.legend(H - 52, [("특권을 쪼개는 장치", ACC), ("시스템 콜을 줄이는 장치", INFO),
                  ("강제적 접근 통제", OK), ("시점이 없는 것", WARN)])
d.save("04-01.privilege-split.svg")
print("ok 04-01.privilege-split")
