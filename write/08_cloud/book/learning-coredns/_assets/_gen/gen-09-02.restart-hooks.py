# 09-02 §3 — 재시작 때 두 caddy.Instance 가 겹쳐 사는 구간.
# 소스 근거: coredns/caddy caddy.go Restart — OnRestart(옛) → startWithListenerFds(새, 그 안에서 OnStartup)
#            → i.Stop()(옛) → OnShutdown(옛). SIGHUP 은 sigtrap_posix.go 가 무시한다.
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
      "SIGUSR1 을 받으면 옛 인스턴스의 OnRestart 뒤에 새 인스턴스가 넘겨받은 소켓으로 뜨고, "
      "옛 인스턴스는 그다음에 멈춘다. 그 사이 두 인스턴스가 같이 산다.",
      "주황이 포트를 새로 열면 실패하는 구간입니다")

X0, X1 = 220, 830
LBLX = 206
T_RS, T_ST, T_SD = 360, 470, 620      # OnRestart · 새 OnStartup · 옛 Stop+OnShutdown

d.line(X0, 118, X1, 118, RULE, 0.8)
d.t(X0, 110, "시간", 11, SOFT, KR, "start")

# 두 인스턴스의 수명 — 막대끼리는 겹치지 않게 세로로 떼어 둔다
d.t(LBLX, 165, "옛 Instance", 11, MUTED, MONO, "end")
d.tone(240, 150, T_SD - 240, 24, MUTED, 4, "20", 1.2)
d.t(LBLX, 227, "새 Instance", 11, MUTED, MONO, "end")
d.tone(T_ST, 212, X1 - 10 - T_ST, 24, MUTED, 4, "20", 1.2)

# 겹치는 구간 — 칠하지 않고 두 경계선과 아래 괄호로만 표시한다
d.line(T_ST, 132, T_ST, 262, ACC, 1.0, "4 3")
d.line(T_SD, 132, T_SD, 262, ACC, 1.0, "4 3")
d.line(T_ST, 262, T_SD, 262, ACC, 1.4)
d.t((T_ST + T_SD) / 2, 280, "두 인스턴스가 같이 산다", 11, ACC, KR)

# 훅 표지 — 소스의 호출 순서대로 시각에 못 박는다
def mark(x, y, name, who):
    d.line(x, y - 8, x, y + 8, INK, 1.4)
    d.t(x, y + 26, name, 11, INK, MONO)
    d.t(x, y + 44, who, 10, MUTED, KR)

mark(T_RS, 330, "OnRestart", "1. 옛 쪽")
mark(T_ST, 330, "OnStartup", "2. 새 쪽, 뜨기 직전")
mark(T_SD, 330, "OnShutdown", "3. 옛 쪽, 멈춘 직후")
# 표지를 막대 끝과 잇는 안내선
d.line(T_ST, 262, T_ST, 322, RULE, 0.8, "2 3")
d.line(T_SD, 262, T_SD, 322, RULE, 0.8, "2 3")
d.line(T_RS, 330, T_SD, 330, RULE, 0.8)
d.line(T_RS, 174, T_RS, 322, RULE, 0.8, "2 3")

d.t(220, 412, "새 인스턴스가 못 뜨면 OnRestartFailed 가 불리고 옛 인스턴스가 남는다", 11, MUTED, KR, "start")
d.t(220, 432, "OnFinalShutdown 은 재시작에서 불리지 않는다", 11, MUTED, KR, "start")

d.box(20, 450, 840, 84, PAPER, RULE, 0.8)
d.t(36, 474, "이 구간에서 포트를 새로 열면 실패한다", 12, ACC, KR, "start", 600)
d.t(36, 498, "듣던 소켓은 새 인스턴스로 넘어간다 — 새로 열지 말고 넘겨받기", 11, MUTED, KR, "start")
d.t(36, 520, "순서의 근거는 coredns/caddy 의 Restart 함수다", 11, MUTED, KR, "start")

d.legend(548, [("두 인스턴스가 겹치는 구간", ACC)])
d.save("09-02.restart-hooks.svg")
