# 01-01 §1 — 명령 한 줄이 커널의 API 를 부르는 경로.
# 원문("Why an Operating System at All?"): getuid(2) 는 "returns the real user ID of the calling process",
#       셸에서는 "the equivalent id command that in turn uses the getuid syscall" 을 쓰며
#       `id --user` 의 출력은 638114 다. 저자는 이 API 를 syscall 이라 부른다고 적는다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 왕복. accent 는 유저 랜드와 커널이 갈리는 한 줄.
import sys; sys.path.insert(0, ".")
from dd import Seq, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO


def _kr(txt):
    """한글이 섞이면 한글 스택으로. Seq 프리미티브가 MONO 를 하드코딩하는 자리를 덮는다."""
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


d = SeqKR(880, 536, "LEARNING MODERN LINUX · 01-01 §1",
          "id 한 줄이 커널에 묻고 돌아오기까지",
          "원서가 든 예를 시간순으로 편 것. 사용자가 친 id --user 가 getuid 시스템 콜이 되어 커널에 닿고, "
          "실 사용자 ID 를 받아 돌아온다. 색이 붙은 화살표가 유저 랜드와 커널이 갈리는 한 줄이다.",
          "이 한 줄이 없으면 자격증명을 앱이 직접 읽어야 합니다")

d.lanes([("사용자", "shell prompt"),
         ("id 명령", "user land"),
         ("커널", "Linux kernel")])
d.rails(432)

d.msg("사용자", "id 명령", "id --user", 172, INFO, sub="셸이 실행 파일을 띄운다")
d.msg("id 명령", "커널", "getuid()", 236, ACC, mk="acc",
      sub="man 2 getuid — 시스템 콜 경계를 넘는 유일한 통로")
d.state("커널", "자격증명은 여기 안쪽", 280, MUTED)
d.msg("커널", "id 명령", "638114", 336, OK, mk="ok", sub="호출한 프로세스의 real user ID")
d.msg("id 명령", "사용자", "638114", 400, MUTED, sub="표준 출력")

d.t(24, 460, "OS 가 없다면 메모리 관리·인터럽트 처리·I/O 장치와의 대화·파일 관리·네트워크 스택 설정을 "
             "앱이 직접 져야 합니다.", 12, SOFT, KR, "start")
d.legend(484, [("사용자 입력", INFO), ("시스템 콜 경계", ACC), ("반환값", OK)])
d.save("01-01.syscall-ladder.svg")
print("ok 01-01.syscall-ladder")
