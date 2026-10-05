# 03-01 §5 — 인터럽트가 도착할 때 누가 CPU 위에 있나. 위: 원서 그림 3.5 의 비동기 장면, 아래: 동기 인터럽트 셋.
# 타입 스펙: type-sequence — MySQL · 커널 · 디스크 · Java 네 레인 사이의 시간순 메시지다.
#           축약: 비동기·동기를 combined fragment 대신 머리줄 둘로 나눈다(분기가 아니라 대비라서).
#           옛 손 SVG(시스템 콜 + 인터럽트 두 패널)를 대체한다 — 시스템 콜 쪽은 03-01.mode-vs-context-switch 로 갔다.
#           focal 은 MySQL 이 떠난 CPU 에 도착하는 완료 인터럽트 하나.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq, DK):
    def __init__(s, *a): DK.__init__(s, *a)
    def lanes(s, names, y0=104, lane_w=200):
        s.LX = {}; n = len(names); span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + span * i / (n - 1)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 14, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 39, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 48
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; k = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * k} {y} L {x2 - 12 * k} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 8} L {x + 52} {y - 8} L {x + 52} {y + 8} L {x + 13} {y + 8}", c, 1.4, m="ar")
        s.t(x + 64, y - 2, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 64, y + 16, sub, 12, MUTED, _kr(sub), "start")
    def head(s, y, txt):
        s.line(24, y + 8, s.w - 24, y + 8, RULE, 0.8)
        s.t(24, y, txt, 13, SOFT, KR, "start", 600)

W, H = 960, 732
d = SeqKR(W, H, "SYSTEMS PERFORMANCE · 03-01 §5",
          "인터럽트가 도착할 때 누가 CPU 위에 있나",
          "위: MySQL 이 파일을 읽다 디스크를 기다리는 동안 스케줄러가 Java 로 전환하고, 디스크 완료 인터럽트는 MySQL 이 없는 CPU 0 에 도착한다(원서 그림 3.5). 아래: 동기 인터럽트는 원인 명령이 아직 CPU 위에 있다.",
          "비동기는 기다리던 스레드가 떠난 뒤에 도착할 수 있습니다")
M, K, DK_, J = "MySQL", "커널", "디스크", "Java"
d.lanes([(M, "CPU 0 에서 시작"), (K, "파일시스템 · 스케줄러"), (DK_, "장치"), (J, "다른 스레드")], 100, 176)
d.rails(652)

d.head(184, "비동기 · CPU 0 의 시간 순서")
d.msg(M, K, "read()", 224, MUTED)
d.msg(K, DK_, "I/O 발행", 260, MUTED)
d.selfmsg(K, "block", 296, MUTED, sub="MySQL 은 sleep")
d.msg(K, J, "컨텍스트 전환", 340, MUTED, sub="Java 가 CPU 0 을 씀")
d.msg(DK_, K, "완료 인터럽트", 396, ACC, "acc", sub="CPU 0 위에는 Java")
d.msg(K, M, "깨움 · ready-to-run", 444, MUTED, dash="5 4")

d.head(492, "동기 · 원인 명령이 CPU 위")
d.msg(J, K, "trap · int 0x80", 532, INFO)
d.msg(J, K, "exception · 0 으로 나누기", 572, INFO)
d.msg(J, K, "fault · page fault", 612, INFO)

d.legend(668, [("기다리던 스레드가 떠난 뒤 도착", ACC), ("원인 명령이 CPU 위", INFO), ("호출 · 전환", MUTED)])
d.save("03-01.syscall-and-interrupts.svg")
