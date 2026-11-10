# 08-01 §6 「journald 에서 rsyslog 로 가는 두 길」 — 한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 길.
# 1차 자료: journald.conf(5) ForwardToSyslog= 와 "usually the second method is used by syslog daemons".
# 실측: Debian 12 컨테이너 rsyslog.conf 의 module(load="imuxsock"), 저널의
#       "imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog'". Rocky Linux 9.3 컨테이너
#       rsyslog.conf 의 module(load="imjournal" StateFile="imjournal.state"), imuxsock SysSock.Use="off".
# 타입 스펙: type-data-flow — 데이터(로그 한 줄)가 소스 → journald → 배포판별 입력 모듈 → 파일로 흐른다.
#           두 배포판을 위아래 lane 으로 나누고 journald 에서 갈라지게 그린다. accent 는 모든 줄이
#           먼저 지나는 journald 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 432
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §6",
      "한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 두 길",
      "systemd 배포판에서 /dev/log 로 들어온 줄은 journald 가 먼저 받는다. rsyslog 는 Debian 에서는 "
      "소켓으로 넘겨받고 Rocky 에서는 저널 파일을 직접 읽는다.",
      "Debian 은 소켓으로 넘겨받고 Rocky 는 저널 파일을 직접 읽습니다")

C0, C1, C2, C3, C4 = 24, 180, 336, 576, 720
W0, W1, W2, W3, W4 = 132, 132, 216, 120, 136
LH = 80
LANES = [
    ("Debian 12", 124, INFO,
     ("/run/systemd/journal/syslog", "ForwardToSyslog=yes (기본)"),
     ("imuxsock", "소켓으로 받음", None),
     ("/var/log/syslog", "/var/log/auth.log", "cron.log …")),
    ("Rocky Linux 9", 244, OK,
     ("/var/log/journal/…/*.journal", "Storage= 가 정한 파일"),
     ("imjournal", "저널 파일을 읽음", "SysSock.Use=off"),
     ("/var/log/messages", "/var/log/secure", "cron …")),
]

# 소스와 journald 는 두 lane 의 가운데
MID = (LANES[0][1] + LH / 2 + LANES[1][1] + LH / 2) / 2
SY = MID - 32
d.box(C0, SY, W0, 64, PAPER2, RULE, 1.1, 6)
d.t(C0 + W0 / 2, SY + 26, "/dev/log", 13, INK, MONO, "middle", 600)
d.t(C0 + W0 / 2, SY + 46, "logger · 데몬 · 앱", 11, MUTED, KR)
d.tone(C1, SY, W1, 64, ACC, 6, "14", 1.4)
d.t(C1 + W1 / 2, SY + 26, "systemd-journald", 12, ACC, MONO, "middle", 600)
d.t(C1 + W1 / 2, SY + 46, "모든 줄을 먼저 받음", 11, MUTED, KR)
d.arrow([(C0 + W0, MID), (C1 - 4, MID)], MUTED, "ar", 1.3)

BUS = C1 + W1 + 12
d.line(C1 + W1, MID, BUS, MID, MUTED, 1.3)
for name, y, col, c2, c3, c4 in LANES:
    cy = y + LH / 2
    d.t(C2, y - 8, name, 12, col, KR, "start", 600)
    d.path(f"M {BUS} {MID} L {BUS} {cy} L {C2 - 4} {cy}", col, 1.3, m="ar")
    d.box(C2, y, W2, LH, PAPER2, col, 1.1, 6)
    d.t(C2 + 14, y + 32, c2[0], 11, INK, MONO, "start", 600)
    d.t(C2 + 14, y + 54, c2[1], 11, MUTED, KR, "start")
    d.arrow([(C2 + W2, cy), (C3 - 4, cy)], col, "ar", 1.3)
    d.box(C3, y, W3, LH, PAPER2, col, 1.1, 6)
    d.t(C3 + 14, y + 26, c3[0], 12, col, MONO, "start", 600)
    d.t(C3 + 14, y + 46, c3[1], 11, MUTED, KR, "start")
    if c3[2]:
        d.t(C3 + 14, y + 66, c3[2], 11, SOFT, MONO, "start")
    d.arrow([(C3 + W3, cy), (C4 - 4, cy)], col, "ar", 1.3)
    d.box(C4, y, W4, LH, PAPER2, RULE, 1.0, 6)
    d.t(C4 + 12, y + 26, c4[0], 11, INK, MONO, "start")
    d.t(C4 + 12, y + 46, c4[1], 11, INK, MONO, "start")
    d.t(C4 + 12, y + 66, c4[2], 11, SOFT, MONO, "start")

BY = LANES[1][1] + LH + 20
d.line(C4, BY, C4 + W4, BY, MUTED, 1.0)
d.line(C4, BY - 6, C4, BY, MUTED, 1.0)
d.line(C4 + W4, BY - 6, C4 + W4, BY, MUTED, 1.0)
d.t(C4 + W4, BY + 20, "logrotate 가 돌리는 파일 · §7", 11, MUTED, KR, "end")

d.legend(388, [("모든 줄이 먼저 지나는 자리", ACC), ("Debian 12 경로", INFO),
               ("Rocky Linux 9 경로", OK)])
d.save("08-01.journal-to-rsyslog.svg")
print("ok 08-01.journal-to-rsyslog")
