# 08-01 §2 「journald 에서 rsyslog 로 가는 두 길」 — 한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 길.
# 1차 자료: journald.conf(5) ForwardToSyslog= 와 "usually the second method is used by syslog daemons".
# 실측: Debian 12 컨테이너 rsyslog.conf 의 module(load="imuxsock"), 저널의
#       "imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog'". Rocky Linux 9.3 컨테이너
#       rsyslog.conf 의 module(load="imjournal" StateFile="imjournal.state"), imuxsock SysSock.Use="off".
# 타입 스펙: type-architecture — 존으로 묶은 노드 그래프에 번호 붙은 화살표로 순서를 싣는다.
#           앞부분(앱 → /dev/log → journald → 저널 파일)은 두 배포판이 같아 가운데 한 줄로 한 번만
#           그리고, 거기서 나가는 길을 위(Debian 12, journald 가 소켓으로 밀어 줌)와 아래(Rocky Linux 9,
#           rsyslog 가 저널 파일을 읽어 감)로 가른다. 위는 journald 에서, 아래는 저널 파일에서 출발하는
#           것이 두 길의 차이다.
# 값: 본문 §2 — /dev/log·/run/systemd/journal/dev-log 는 journald 가 듣는 소켓, 저널 파일
#     /run/log/journal 또는 /var/log/journal(Storage=), ForwardToSyslog=yes 와
#     /run/systemd/journal/syslog, 저널 한 줄 "rsyslogd[50]: imuxsock: Acquired UNIX socket ... (fd 3)",
#     imjournal 과 SysSock.Use="off", 위치를 적는 상태 파일. 파일 이름은 §3 표(syslog·auth.log /
#     messages·secure)와 정답 4 의 /var/log/auth.log·/var/log/secure.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 568
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §2",
      "한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 두 길",
      "systemd 배포판에서 /dev/log 로 들어온 줄은 journald 가 먼저 받아 저널 파일에 쓴다. 여기까지는 "
      "두 배포판이 같다. Debian 12 에서는 journald 가 ForwardToSyslog=yes 로 /run/systemd/journal/syslog "
      "소켓에 밀어 주고 rsyslogd 의 imuxsock 이 받는다. Rocky Linux 9 에서는 rsyslogd 의 imjournal 이 "
      "저널 파일을 직접 읽고 읽은 위치를 상태 파일에 적는다. 그 뒤 rsyslog 규칙이 줄을 /var/log 의 "
      "텍스트 파일로 나눈다.",
      "Debian 은 소켓으로 넘겨받고 Rocky 는 저널 파일을 직접 읽습니다")

# 열 — 왼쪽부터 앱, /dev/log, journald, 저널 파일·소켓, rsyslogd, 텍스트 파일
C = [(24, 88), (136, 104), (264, 148), (436, 212), (672, 112), (808, 128)]
def cx(i): return C[i][0] + C[i][1] / 2
def rx(i): return C[i][0] + C[i][1]

NH = 60
Y_DEB, Y_MID, Y_RKY = 132, 260, 412       # 세 줄의 상자 윗변
def cy(y): return y + NH / 2


def zone(x, y, h, label, col, label_y):
    """존은 배포판마다 갈라지는 부분만 감싼다. 공통 줄은 존 밖에 둔다."""
    d.o.append(f'<rect x="{x}" y="{y}" width="{W - 12 - x}" height="{h}" rx="8" '
               f'fill="{col}08" stroke="{col}" stroke-width="0.8" stroke-dasharray="5 4"/>')
    d.t(x + 16, label_y, label, 12, col, KR, "start", 600)


def node(i, y, lines, stroke=RULE, sw=0.9, fill=PAPER2):
    """lines: (글자, 크기, 색, 글꼴, 굵기) 목록. 상자 안에 세로로 고르게 놓는다."""
    x, w = C[i]
    d.box(x, y, w, NH, fill, stroke, sw)
    n = len(lines)
    step = 16 if n == 3 else 18
    y0 = y + NH / 2 - step * (n - 1) / 2 + 4
    for k, (txt, size, col, fam, wt) in enumerate(lines):
        d.t(x + w / 2, y0 + k * step, txt, size, col, fam, "middle", wt)


zone(C[2][0] - 12, Y_DEB - 32, NH + 68, "Debian 12 — journald 가 밀어 줌", INFO, Y_DEB - 14)
zone(C[3][0] - 12, Y_RKY - 32, NH + 64, "Rocky Linux 9 — rsyslog 가 읽어 감", OK, Y_RKY + NH + 18)

# 가운데 줄 — 두 배포판 공통
d.t(C[0][0], Y_MID - 12, "두 배포판 공통", 11, SOFT, KR, "start", 600)
node(0, Y_MID, [("앱 · logger", 12.5, INK, KR, 600), ("syslog(3)", 11, MUTED, MONO, 400)])
node(1, Y_MID, [("/dev/log", 12.5, INK, MONO, 600), ("journald 가 들음", 11, MUTED, KR, 400)])
d.tone(C[2][0], Y_MID, C[2][1], NH, ACC, 6, "14", 1.4)
d.t(cx(2), Y_MID + 26, "systemd-journald", 12, ACC, MONO, "middle", 600)
d.t(cx(2), Y_MID + 44, "모든 줄을 먼저 받음", 11, MUTED, KR)
node(3, Y_MID, [("저널 파일 · Storage=", 12, INK, KR, 600), ("/var/log/journal", 11, INFO, MONO, 400),
                ("또는 /run/log/journal", 11, MUTED, MONO, 400)])

for i, n in ((0, "1"), (1, "2")):
    d.arrow([(rx(i) + 2, cy(Y_MID)), (C[i + 1][0] - 4, cy(Y_MID))], MUTED, "ar", 1.3)
    d.t((rx(i) + C[i + 1][0]) / 2, cy(Y_MID) - 8, n, 11, MUTED, MONO, "middle", 600)
d.arrow([(rx(2) + 2, cy(Y_MID)), (C[3][0] - 4, cy(Y_MID))], MUTED, "ar", 1.3)
d.t((rx(2) + C[3][0]) / 2, cy(Y_MID) - 8, "씀", 11, MUTED, KR, "middle", 600)

# 위 — Debian 12: journald 에서 소켓으로
node(3, Y_DEB, [("/run/systemd/journal/syslog", 11.5, INK, MONO, 600), ("유닉스 소켓", 11, MUTED, KR, 400)],
     INFO, 1.1)
node(4, Y_DEB, [("rsyslogd", 13, INK, MONO, 600), ("imuxsock · fd 3", 11, INFO, MONO, 400)], INFO, 1.1)
node(5, Y_DEB, [("/var/log/syslog", 11, INK, MONO, 600), ("/var/log/auth.log", 11, INK, MONO, 600)])
XU = cx(2)
d.path(f"M {XU} {Y_MID} L {XU} {cy(Y_DEB)} L {C[3][0] - 4} {cy(Y_DEB)}", INFO, 1.4, m="info")
d.t(XU + 8, Y_DEB + NH + 24, "3 ForwardToSyslog=yes", 11.5, INFO, MONO, "start", 600)
d.arrow([(rx(3) + 2, cy(Y_DEB)), (C[4][0] - 4, cy(Y_DEB))], INFO, "info", 1.3)
d.arrow([(rx(4) + 2, cy(Y_DEB)), (C[5][0] - 4, cy(Y_DEB))], MUTED, "ar", 1.3)
d.t((rx(4) + C[5][0]) / 2, cy(Y_DEB) - 8, "4", 11, MUTED, MONO, "middle", 600)

# 아래 — Rocky Linux 9: 저널 파일에서 rsyslog 가 읽어 감
XD = cx(3)
d.path(f"M {XD} {Y_MID + NH} L {XD} {cy(Y_RKY)} L {C[4][0] - 4} {cy(Y_RKY)}", OK, 1.4, m="ok")
d.t(XD + 8, Y_MID + NH + 28, "3 직접 읽어 감", 12, OK, KR, "start", 600)
d.t(XD + 8, Y_MID + NH + 46, "Storage= 가 파일을 남겨야", 11, SOFT, KR, "start")
node(4, Y_RKY, [("rsyslogd", 13, INK, MONO, 600), ("imjournal", 11, OK, MONO, 400),
                ("위치 → 상태 파일", 11, MUTED, KR, 400)], OK, 1.1)
d.t(cx(4), Y_RKY + NH + 18, 'SysSock.Use="off"', 11, SOFT, MONO)
node(5, Y_RKY, [("/var/log/messages", 11, INK, MONO, 600), ("/var/log/secure", 11, INK, MONO, 600)])
d.arrow([(rx(4) + 2, cy(Y_RKY)), (C[5][0] - 4, cy(Y_RKY))], MUTED, "ar", 1.3)
d.t((rx(4) + C[5][0]) / 2, cy(Y_RKY) - 8, "4", 11, MUTED, MONO, "middle", 600)

d.t(C[5][0] + C[5][1], Y_RKY + NH + 18, "4 = rsyslog 규칙 · §3", 11, SOFT, KR, "end")

d.legend(Y_RKY + NH + 52, [("journald (모든 줄 수집)", ACC),
                           ("Debian 12 (소켓 전달)", INFO),
                           ("Rocky Linux 9 (저널 읽기)", OK)])
d.save("08-01.journal-to-rsyslog.svg")
print("ok 08-01.journal-to-rsyslog")
