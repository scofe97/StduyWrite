# 04-01 §5 — passwd 를 실행할 때 프로세스의 UID 넷이 어떻게 움직이는가.
# 근거: credentials(7) "A child process created by fork(2) inherits copies of its parent's user and
#       groups IDs. During an execve(2), a process's real user and group ID and supplementary group IDs
#       are preserved; the effective and saved set IDs may be changed",
#       "Whenever a process's effective user (group) ID is changed, the kernel also automatically changes
#       the filesystem user (group) ID".
#       execve(2) "the effective user ID of the calling process is changed to that of the owner of the
#       program file", "The effective user ID of the process is copied to the saved set-user-ID".
#       proc_pid_status(5) "Uid, Gid: Real, effective, saved set, and filesystem UIDs (GIDs)" — 칩의 순서.
#       passwd(1) FILES 에 /etc/shadow 가 있다. 2026-11-17 데비안 실측으로 suid 사본이
#       "Uid: 501 0 0 0" 을 보인 것을 확인했다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 왕복. accent 는 유효 UID 가 0 이 되는 한 줄.
import sys; sys.path.insert(0, ".")
from dd import Seq, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, WARN, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        han = any("가" <= ch <= "힣" for ch in str(txt))
        w = len(txt) * (12.0 if han else 7.4) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))


d = SeqKR(880, 560, "LEARNING MODERN LINUX · 04-01 §5",
          "passwd 를 실행하면 유효 UID 가 0 이 된다",
          "fork 로 만든 자식은 부모의 UID 사본을 물려받고, setuid 가 켜진 root 소유 파일을 execve 하면 "
          "실제 UID 는 남고 유효·저장·파일시스템 UID 가 0 이 된다.",
          "칩의 Uid 네 값은 실제 · 유효 · 저장 · 파일시스템 순서입니다")

d.lanes([("셸", "uid 1000"),
         ("자식 프로세스", "exec 뒤 passwd"),
         ("커널", "권한 판정")])
d.rails(488)

d.msg("셸", "자식 프로세스", "fork(2)", 172, INFO,
      sub="부모 UID 사본 상속")
d.state("자식 프로세스", "Uid: 1000 1000 1000 1000", 216, INFO)
d.msg("자식 프로세스", "커널", "execve(2) /usr/bin/passwd", 268, ACC, mk="acc",
      sub="setuid · root 소유")
d.state("자식 프로세스", "Uid: 1000 0 0 0", 312, ACC)
d.msg("자식 프로세스", "커널", "/etc/shadow 쓰기", 372, WARN, mk="warn",
      sub="파일시스템 UID 0 으로 판정")
d.state("커널", "허용", 416, OK)
d.msg("커널", "셸", "비밀번호 변경 완료", 464, OK, mk="ok")

d.legend(508, [("물려받음", INFO), ("유효 UID 가 바뀌는 자리", ACC),
               ("판정 대상", WARN), ("결과", OK)])
d.save("04-01.uid-at-exec.svg")
print("ok 04-01.uid-at-exec")
