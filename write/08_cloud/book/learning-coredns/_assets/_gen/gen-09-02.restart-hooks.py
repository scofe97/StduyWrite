# 09-02 §3 — 재시작 때 두 caddy.Instance 가 겹쳐 사는 구간.
# 원문 근거: "When CoreDNS receives a SIGUSR1 or a SIGHUP, it reloads the Corefile, which causes
#            a graceful restart of the server. Internally, a new caddy.Instance is created with
#            the new Corefile, and the file descriptors of the listening sockets are handed over
#            to it." / "so there are in fact two caddy.Instances running during this time"
#            / "Be sure to properly hand off any open ports, rather than attempting to open them
#            anew, which will fail."
# 타입 스펙: type-gantt — 두 인스턴스의 수명이 시간 위에서 겹친다는 것이 논지이고, 그 겹침은
#           막대의 상대 위치로만 보인다. 훅은 시각 표지로 축 위에 얹는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 610
d = D(W, H, "LEARNING COREDNS · 09-02 §3",
      "재시작 때 두 인스턴스가 겹치는 구간",
      "SIGUSR1 이나 SIGHUP 을 받으면 새 인스턴스가 만들어지고 듣던 소켓의 파일 디스크립터가 "
      "넘어간다. 그 사이 두 인스턴스가 같이 산다.",
      "주황이 포트를 새로 열면 실패하는 구간입니다")

X0, X1 = 220, 830
LBLX = 206

d.line(X0, 118, X1, 118, RULE, 0.8)
d.t(X0, 110, "시간", 11, SOFT, KR, "start")

# 두 인스턴스의 수명
d.t(LBLX, 165, "옛 Instance", 11, MUTED, MONO, "end")
d.tone(240, 150, 380, 24, MUTED, 4, "20", 1.2)
d.t(LBLX, 217, "새 Instance", 11, MUTED, MONO, "end")
d.tone(470, 202, 350, 24, MUTED, 4, "20", 1.2)

# 겹치는 구간
d.tone(470, 140, 150, 96, ACC, 6, "0E", 1.3)
d.t(545, 256, "두 인스턴스가 같이 산다", 11, ACC, KR)

# 훅 표지 — 원서는 셋 사이의 순서를 말하지 않으므로 각각을 시각에 못 박지 않고
# 겹치는 구간 하나에 묶어 적는다. 눈금을 매기면 없는 순서를 지어내게 된다.
d.line(470, 268, 470, 296, ACC, 0.8, "3 4")
d.line(620, 268, 620, 296, ACC, 0.8, "3 4")
d.line(470, 296, 620, 296, ACC, 1.0)
d.t(545, 322, "이 구간에 재시작 훅 셋이 불린다", 11, ACC, KR)
d.t(545, 344, "OnShutdown · OnStartup · OnRestart", 11, ACC, MONO)
d.t(545, 366, "원서는 셋 사이의 순서를 말하지 않는다", 11, MUTED, KR)

d.t(220, 402, "재시작이 실패하면 OnRestartFailed 도 이 구간에서 불린다", 11, MUTED, KR, "start")
d.t(220, 424, "OnFinalShutdown 은 프로세스가 아예 끝날 때만 불린다 — 본문 정오 블록의 교정을 따른 배치다", 11, MUTED, KR, "start")

d.box(20, 450, 840, 84, PAPER, RULE, 0.8)
d.t(36, 474, "이 구간에서 포트를 새로 열면 실패한다", 12, ACC, KR, "start", 600)
d.t(36, 498, "듣던 소켓은 새 인스턴스로 넘어가므로, 새로 여는 대신 넘겨받는 쪽으로 다뤄야 한다",
     11, MUTED, KR, "start")
d.t(36, 520, "원서가 이 순서를 설명하는 문장에는 자기모순이 있다 — 본문 정오 블록 참조", 11, MUTED, KR, "start")

d.legend(548, [("재시작 훅이 불리는 구간", ACC)])
d.save("09-02.restart-hooks.svg")
