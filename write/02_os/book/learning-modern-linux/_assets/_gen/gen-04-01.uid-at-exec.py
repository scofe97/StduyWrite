# 04-01 §5 — passwd 를 실행할 때 UID 넷이 어떻게 움직이는가.
# 원문("Process Permissions"): credentials(7) 을 인용해 네 가지를 가른다 —
#       Real UID: "the UID of the user that launched the process ... The process itself can obtain its
#                 real UID via getuid(2)".
#       Effective UID: "The Linux kernel uses the effective UID to determine permissions the process has
#                      when accessing shared resources ... A process can obtain its effective UID via
#                      geteuid(2)."
#       Saved set-user-ID: "used in suid cases where a process can assume privileges by switching its
#                          effective UID between the real UID and the saved set-user-ID."
#       Filesystem UID: "used to determine permissions for file access ... usually the filesystem UID is
#                       the same as the effective UID but can be changed via setfsuid(2)."
#       전이 규칙 — "when a child process is created via fork(2), it inherits copies of its parent's UIDs,
#       and during an execve(2) syscall, the process's real UID is preserved, whereas the effective UID
#       and saved set-user-ID may change."
#       예시 — "when you run the passwd command, your effective UID is your UID, let's say 1000. Now,
#       passwd has suid set enabled, which means when you run it, your effective UID is 0 (aka root)."
# 주의: 마지막 쓰기 대상이 /etc/shadow 라는 것은 원문이 이 절에서 잇지 않는다. 저자가 앞 절에
#       "passwords are stored ... in the /etc/shadow file" 라 적은 것과 이 절의 suid 설명을
#       노트가 이은 것이라 도식에는 대상 파일 이름을 적지 않는다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 왕복. accent 는 유효 UID 가 뒤집히는 한 줄.
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


d = SeqKR(880, 620, "LEARNING MODERN LINUX · 04-01 §5",
          "passwd 를 실행하면 유효 UID 가 뒤집힌다",
          "자식 프로세스가 부모의 UID 사본을 물려받고, execve 에서 실제 UID 는 보존되지만 "
          "유효 UID 와 저장된 set-user-ID 는 바뀔 수 있다는 규칙을 시간순으로 편 것.",
          "권한 판정에 쓰이는 것은 실제 UID 가 아니라 유효 UID 입니다")

d.lanes([("셸", "uid 1000"),
         ("passwd 프로세스", "suid 가 켜진 실행 파일"),
         ("커널", "권한을 판정한다")])
d.rails(492)

d.msg("셸", "passwd 프로세스", "fork(2)", 172, INFO,
      sub="부모의 UID 사본을 그대로 물려받는다")
d.state("passwd 프로세스", "real 1000 · effective 1000", 216, INFO)
d.msg("passwd 프로세스", "커널", "execve(2)", 268, ACC, mk="acc",
      sub="real UID 는 보존되고 effective 와 saved 는 바뀔 수 있다")
d.state("passwd 프로세스", "real 1000 · effective 0", 312, ACC)
d.msg("passwd 프로세스", "커널", "root 만 닿는 곳에 쓴다", 372, WARN, mk="warn",
      sub="판정 기준은 effective UID · 대상은 노트가 채운 것")
d.state("커널", "허용", 416, OK)
d.msg("커널", "셸", "비밀번호가 바뀌었다", 464, OK, mk="ok")

d.t(24, 528, "저장된 set-user-ID 는 프로세스가 실제 UID 와 그 값 사이에서 유효 UID 를 오갈 때 씁니다.",
    12, SOFT, KR, "start")
d.t(24, 550, "파일시스템 UID 는 보통 유효 UID 와 같고 커널이 자동으로 따라 바꿉니다.",
    12, SOFT, KR, "start")
d.legend(568, [("물려받음", INFO), ("권한이 뒤집히는 자리", ACC),
               ("판정 대상", WARN), ("결과", OK)])
d.save("04-01.uid-at-exec.svg")
print("ok 04-01.uid-at-exec")
