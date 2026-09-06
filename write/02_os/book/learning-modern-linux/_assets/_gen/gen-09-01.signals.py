# 09-01 §1 — 저자가 익혀 두라고 꼽은 시그널 일곱과 그 네 축.
# 원문(Table 9-1. Common signals) 의 행 그대로:
#       SIGHUP("Tell a daemon process to reread its config file" · "Terminate process" · "nohup or
#       custom handler" · "N/A"), SIGINT("User interruption from keyboard" · "Terminate process" ·
#       "Custom handler" · "Ctrl+C"), SIGQUIT("User quit from keyboard" · "core dump and terminate
#       process" · "Custom handler" · "Ctrl+\"), SIGKILL("Kill signal" · "Terminate process" · "Cannot be
#       handled" · "N/A"), SIGSTOP("Stop process" · "Stop process" · "Cannot be handled" · "N/A"),
#       SIGTSTP("User caused stop from keyboard" · "Stop process" · "Custom handler" · "Ctrl+Z"),
#       SIGTERM("Graceful termination" · "Terminate process" · "Custom handler" · "N/A").
# 1차 자료(signal(7)): "The signals SIGKILL and SIGSTOP cannot be caught, blocked, or ignored." 로
#       마지막 두 행의 "Cannot be handled" 가 확인된다.
# 주의: accent 는 SIGINT 행이다. 저자가 이 시그널로 든 trap 예제의 설명이 본문 정오가 나온 자리다.
# 타입 스펙: type-dp-security-matrix — 행(시그널) × 열(뜻 · 기본 동작 · 핸들 · 키)의 격자. 어느 조합이
#           되고 안 되는지가 논지라 격자가 맞는다. 축약: SIGUSR1·SIGUSR2 는 표 밖이라 본문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 692
LX, LW = 24, 84
C1, C2, C3, C4 = 250, 148, 168, 96
RH, HY, RY = 56, 148, 172

d = D(W, H, "LEARNING MODERN LINUX · 09-01 §1",
      "시그널 일곱을 네 축으로 세우면 둘만 다르다",
      "저자가 익혀 두라고 꼽은 시그널을 원서 표 그대로 옮긴 격자. 마지막 열의 N/A 는 그 시그널에 "
      "정해진 키 조합이 없다는 원서의 표기 그대로다.",
      "핸들할 수 없는 둘이 나머지 다섯과 갈리는 자리입니다")

for name, cw, off in (("뜻", C1, LW), ("기본 동작", C2, LW + C1),
                      ("핸들", C3, LW + C1 + C2), ("키", C4, LW + C1 + C2 + C3)):
    d.t(LX + off + cw / 2, HY, name, 12, MUTED, KR, "middle", 600)
TOT = LW + C1 + C2 + C3 + C4
d.line(LX, HY + 12, LX + TOT, HY + 12, RULE, 1)

ROWS = [
    ("SIGHUP", "데몬에게 설정 파일을 다시 읽으라 이른다", "프로세스 종료", "nohup 또는 커스텀 핸들러", "N/A", OK, False),
    ("SIGINT", "키보드에서 온 사용자 인터럽트", "프로세스 종료", "커스텀 핸들러", "Ctrl+C", OK, True),
    ("SIGQUIT", "키보드에서 온 사용자 종료", "코어 덤프 후 종료", "커스텀 핸들러", "Ctrl+\\", OK, False),
    ("SIGKILL", "죽이는 신호", "프로세스 종료", "핸들할 수 없다", "N/A", BAD, False),
    ("SIGSTOP", "프로세스 정지", "프로세스 정지", "핸들할 수 없다", "N/A", BAD, False),
    ("SIGTSTP", "키보드로 일으킨 정지", "프로세스 정지", "커스텀 핸들러", "Ctrl+Z", OK, False),
    ("SIGTERM", "얌전한 종료", "프로세스 종료", "커스텀 핸들러", "N/A", OK, False),
]
for r, (sig, mean, dflt, hnd, key, col, focal) in enumerate(ROWS):
    y = RY + r * RH
    if focal:
        d.tone(LX, y + 3, TOT, RH - 6, ACC, 6, "12", 1.4)
    elif r % 2 == 0:
        d.box(LX, y + 3, TOT, RH - 6, PAPER2, "none", 0, 6)
    d.t(LX + 12, y + RH / 2 + 5, sig, 13, ACC if focal else col, MONO, "start", 600)
    d.t(LX + LW + 8, y + RH / 2 + 5, mean, 12, ACC if focal else INK, KR, "start")
    d.t(LX + LW + C1 + C2 / 2, y + RH / 2 + 5, dflt, 12, MUTED, KR, "middle")
    d.t(LX + LW + C1 + C2 + C3 / 2, y + RH / 2 + 5, hnd, 12, col, KR, "middle",
        600 if col is BAD else 400)
    d.t(LX + LW + C1 + C2 + C3 + C4 / 2, y + RH / 2 + 5, key, 12, SOFT, MONO, "middle")

BY = RY + len(ROWS) * RH + 10
d.line(LX, BY, LX + TOT, BY, RULE, 1)
d.t(LX, BY + 26, "signal(7) 도 같은 말을 합니다. SIGKILL 과 SIGSTOP 은 잡을 수도 막을 수도 무시할 수도 없습니다.",
    12, MUTED, KR, "start")
d.t(LX, BY + 48, "뜻이 정해지지 않은 SIGUSR1 과 SIGUSR2 도 있습니다. 양쪽이 의미에 합의하면 프로세스끼리 쓸 수 있습니다.",
    12, SOFT, KR, "start")

d.legend(BY + 72, [("본문 정오가 나온 자리", ACC), ("핸들할 수 있다", OK), ("핸들할 수 없다", BAD)])
d.save("09-01.signals.svg")
print("ok 09-01.signals")
