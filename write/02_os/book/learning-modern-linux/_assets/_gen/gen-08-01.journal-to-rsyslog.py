# 08-01 §2 「journald 에서 rsyslog 로 가는 두 길」 — 한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 길.
# 1차 자료: journald.conf(5) ForwardToSyslog= 와 "usually the second method is used by syslog daemons".
# 실측: Debian 12 컨테이너 rsyslog.conf 의 module(load="imuxsock"), 저널의
#       "imuxsock: Acquired UNIX socket '/run/systemd/journal/syslog'". Rocky Linux 9.3 컨테이너
#       rsyslog.conf 의 module(load="imjournal" StateFile="imjournal.state"), imuxsock SysSock.Use="off".
# 타입 스펙: type-architecture — 존으로 묶은 노드 그래프에 번호 붙은 화살표로 순서를 싣는다.
#           Debian 12 와 Rocky Linux 9 두 존으로 나누고, journald(focal)에서 소켓으로 밀어 주는 길과
#           저널 파일을 직접 읽어 가는 길의 차이를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 472
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §2",
      "한 줄이 journald 를 거쳐 rsyslog 의 파일로 가는 두 길",
      "systemd 배포판에서 /dev/log 로 들어온 줄은 journald 가 먼저 받는다. rsyslog 는 Debian 에서는 "
      "소켓으로 넘겨받고 Rocky 에서는 저널 파일을 직접 읽는다.",
      "Debian 은 소켓으로 넘겨받고 Rocky 는 저널 파일을 직접 읽습니다")

def zone(x, y, w, h, label, col):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{col}08" stroke="{col}" stroke-width="0.8" stroke-dasharray="5 4"/>')
    lw = len(label) * 8 + 20
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="16" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw / 2, y + 16, label, 11, SOFT, KR, "middle", 600)

def node(x, y, w, h, name, sub=None, fill=PAPER2, stroke=RULE, sw=0.9, fam=KR, name_size=11.5, sub_size=10):
    d.box(x, y, w, h, fill, stroke, sw)
    if sub:
        d.t(x + w / 2, y + 21, name, name_size, INK, fam, "middle", 600)
        d.t(x + w / 2, y + 38, sub, sub_size, MUTED, MONO if any(c.isascii() and c.isalnum() for c in sub) else KR)
    else:
        d.t(x + w / 2, y + 29, name, name_size, INK, fam, "middle", 600)

def num_label(x, y, txt, c=MUTED):
    d.t(x, y, txt, 11, c, KR, "middle", 600)

def alabel(x, y, txt, c=MUTED):
    w = 66
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="15" rx="2" fill="{PAPER}"/>')
    d.t(x, y + 2, txt, 11, c, KR, "middle", 600)

# Zones
zone(24, 96, 832, 152, "Debian 12", INFO)
zone(24, 260, 832, 152, "Rocky Linux 9", OK)

# Debian 12 nodes
# Row 1 (y = 120, cy = 144)
node(36, 120, 68, 48, "앱 · logger", "사용자 공간", name_size=11, sub_size=11)
node(124, 120, 78, 48, "/dev/log", "수신 소켓", fam=MONO, name_size=10.5, sub_size=11)
d.tone(222, 120, 114, 48, ACC, op="14", sw=1.2)
d.t(279, 141, "systemd-journald", 10.5, ACC, MONO, "middle", 600)
d.t(279, 158, "모든 줄 먼저 수집", 11, MUTED, KR, "middle")
node(428, 120, 110, 48, "저널 파일", "/var/log/journal", fam=KR, name_size=11, sub_size=9.0)

# Row 2 (y = 180, cy = 204)
node(428, 180, 110, 48, "/run/.../syslog", "ForwardToSyslog", fam=MONO, name_size=10, sub_size=9.0)
node(630, 180, 88, 48, "rsyslog", "imuxsock", fam=MONO, name_size=11, sub_size=9.5)
node(740, 180, 106, 48, "/var/log/syslog", "auth.log · §3", fam=MONO, name_size=9.5, sub_size=9.0)

# Debian arrows
d.arrow([(104, 144), (120, 144)], MUTED, "ar", 1.3)
num_label(112, 136, "1")
d.arrow([(202, 144), (218, 144)], MUTED, "ar", 1.3)
num_label(210, 136, "2")
d.arrow([(336, 136), (424, 136)], MUTED, "ar", 1.2)
d.t(382, 129, "기록", 11, MUTED, KR, "middle")

# Elbow arrow to socket (mid = 382)
d.path("M 336 152 H 374 Q 382 152 382 160 V 196 Q 382 204 390 204 H 424", INFO, 1.4, m="info")
alabel(382, 178, "3 밀어 줌", INFO)

d.arrow([(538, 204), (626, 204)], INFO, "info", 1.3)
d.arrow([(718, 204), (736, 204)], MUTED, "ar", 1.3)
num_label(727, 196, "4")

# Rocky Linux 9 nodes
# Row 1 (y = 284, cy = 308)
node(36, 284, 68, 48, "앱 · logger", "사용자 공간", name_size=11, sub_size=11)
node(124, 284, 78, 48, "/dev/log", "수신 소켓", fam=MONO, name_size=10.5, sub_size=11)
d.tone(222, 284, 114, 48, ACC, op="14", sw=1.2)
d.t(279, 305, "systemd-journald", 10.5, ACC, MONO, "middle", 600)
d.t(279, 322, "모든 줄 먼저 수집", 11, MUTED, KR, "middle")
node(428, 284, 110, 48, "저널 파일", "/var/log/journal", fam=KR, name_size=11, sub_size=9.0)

# Row 2 (y = 344, cy = 368)
d.box(428, 344, 110, 48, fill=PAPER2, stroke=RULE, sw=0.8)
d.t(483, 365, "소켓 미사용", 11, SOFT, KR, "middle", 500)
d.t(483, 382, 'SysSock.Use="off"', 9.0, SOFT, MONO, "middle")

node(630, 344, 88, 48, "rsyslog", "imjournal", fam=MONO, name_size=11, sub_size=9.5)
node(740, 344, 106, 48, "/var/log/messages", "secure · §3", fam=MONO, name_size=8.8, sub_size=9.0)

# Rocky arrows
d.arrow([(104, 308), (120, 308)], MUTED, "ar", 1.3)
num_label(112, 300, "1")
d.arrow([(202, 308), (218, 308)], MUTED, "ar", 1.3)
num_label(210, 300, "2")
d.arrow([(336, 308), (424, 308)], MUTED, "ar", 1.2)
d.t(382, 301, "기록", 11, MUTED, KR, "middle")

# Elbow arrow from journal file to rsyslog (mid = 584)
d.path("M 538 308 H 576 Q 584 308 584 316 V 360 Q 584 368 592 368 H 626", OK, 1.4, m="ok")
alabel(584, 338, "3 읽어 감", OK)

d.arrow([(718, 368), (736, 368)], MUTED, "ar", 1.3)
num_label(727, 360, "4")

d.legend(428, [("journald (모든 줄 수집)", ACC),
               ("Debian 12 (소켓 전달)", INFO),
               ("Rocky Linux 9 (저널 읽기)", OK)])
d.save("08-01.journal-to-rsyslog.svg")
print("ok 08-01.journal-to-rsyslog")
