# 03-01 §3 — 시스템 콜 세 경로: 모드 전환만 / 모드 전환 + 컨텍스트 전환 / 전환 없음(vDSO).
# 타입 스펙: type-sequence — 스레드 A · 커널 · 스레드 B 세 레인 사이의 시간순 메시지다.
#           축약: 세 경우를 combined fragment 대신 가로 머리줄로 나눈다(경우끼리 분기가 아니라 나란한 예라서).
#           반환은 점선 + 채운 화살촉(스펙 Message kinds). focal 은 블로킹 경우의 컨텍스트 전환 하나.
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

W, H = 928, 724
d = SeqKR(W, H, "SYSTEMS PERFORMANCE · 03-01 §3",
          "모드 전환과 컨텍스트 전환 — 세 가지 syscall 경로",
          "모든 시스템 콜은 커널에 들어가며 모드 전환을 한다. 블로킹되는 시스템 콜은 기다리는 동안 다른 스레드를 돌리려고 컨텍스트 전환을 더한다. vDSO 로 구현된 호출은 커널에 들어가지 않는다.",
          "블로킹 여부가 컨텍스트 전환을 가릅니다")
d.lanes([("스레드 A", "유저 모드"), ("커널", "커널 모드"), ("스레드 B", "유저 모드")], 100, 200)
d.rails(648)
A, K, B = "스레드 A", "커널", "스레드 B"

d.head(184, "블로킹하지 않는 syscall · getpid()")
d.msg(A, K, "getpid()", 228, MUTED, sub="모드 전환")
d.msg(K, A, "반환", 276, MUTED, dash="5 4", sub="모드 전환")

d.head(324, "블로킹 syscall · read()")
d.msg(A, K, "read()", 364, MUTED, sub="모드 전환")
d.selfmsg(K, "디스크 I/O 발행", 404, MUTED, sub="A 는 sleep")
d.msg(K, B, "컨텍스트 전환", 452, ACC, "acc", sub="B 가 CPU 를 씀")
d.selfmsg(K, "완료 인터럽트", 496, INFO, sub="A 를 깨움")
d.msg(K, A, "컨텍스트 전환 · 반환", 540, MUTED, dash="5 4", sub="A 가 CPU 로 복귀")

d.head(588, "vDSO · gettimeofday()")
d.selfmsg(A, "vDSO 안에서 답", 624, OK, sub="전환 없음")

d.legend(664, [("CPU 를 넘기는 컨텍스트 전환", ACC), ("커널 안의 이벤트", INFO), ("커널에 들어가지 않음", OK), ("모드 전환", MUTED)])
d.save("03-01.mode-vs-context-switch.svg")
