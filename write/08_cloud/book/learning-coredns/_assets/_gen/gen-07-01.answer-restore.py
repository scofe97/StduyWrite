# 07-01 §3 — 질문이 복구되는 자리와 복구되지 않는 자리.
# 원문 근거: "With the previous exact match rule, the rewrite plug-in automatically filled in the
#            original question. For the regular expression rules, it does not do this
#            automatically, and so we must use the answer name option" / "some DNS resolver
#            libraries will reject a response from a server if the Question section of the
#            response does not match the Question section of the request that the library sent."
# 타입 스펙: type-sequence — 질문이 언제 바뀌고 언제(안) 돌아오는지가 시간 순서 위에서만 보인다.
#           Seq.msg 는 라벨 글꼴이 MONO 로 고정돼 한글이 뭉개지므로 KR 판별을 얹은 SeqKR 로 쓴다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 62} {y - 10} L {x + 62} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 72, y - 4, label, 11, c, _kr(label), "start")
        if sub:
            s.t(x + 72, y + 13, sub, 11, MUTED, _kr(sub), "start")


W, H = 880, 646
d = SeqKR(W, H, "LEARNING COREDNS · 07-01 §3",
          "질문이 복구되는 자리와 복구되지 않는 자리",
          "정규식 재작성에서 나가는 질의는 바뀌지만 돌아오는 응답의 Question 섹션은 "
          "저절로 돌아오지 않는다. answer name 을 적었느냐가 두 갈래를 만든다.",
          "빨강 갈래에서 클라이언트가 응답을 버립니다")

d.lanes([("클라이언트", "stub resolver"),
         ("rewrite", "plugin"),
         ("kubernetes", "plugin")], y0=104, lane_w=200)
d.rails(496)

d.msg("클라이언트", "rewrite", "api.example.com", 196, INK, "ar",
      sub="클라이언트가 보낸 Question")
d.selfmsg("rewrite", "name regex 로 이름 교체", 244, ACC,
          sub="example.com 을 example.svc.cluster.local 로")
d.msg("rewrite", "kubernetes", "api.example.svc.cluster.local", 300, MUTED)
d.msg("kubernetes", "rewrite", "A 10.7.249.102", 348, MUTED,
      sub="레코드는 정상적으로 찾았다")

d.state("rewrite", "여기서 갈린다", 396, ACC)

d.msg("rewrite", "클라이언트", "Question = api.example.svc.cluster.local", 444, BAD,
      sub="answer name 을 적지 않았을 때")
d.msg("rewrite", "클라이언트", "Question = api.example.com", 492, OK,
      sub="answer name 으로 되돌렸을 때")

d.box(20, 524, 410, 62, PAPER, BAD, 1.0)
d.t(36, 548, "요청과 다른 Question 이 실려 온다", 12, BAD, KR, "start", 600)
d.t(36, 570, "리졸버 라이브러리 상당수가 이 응답을 버린다", 11, MUTED, KR, "start")

d.box(450, 524, 410, 62, PAPER, OK, 1.0)
d.t(466, 548, "요청과 같은 Question 이 실려 온다", 12, OK, KR, "start", 600)
d.t(466, 570, "정확 일치 규칙에서는 이 복구가 자동이다", 11, MUTED, KR, "start")

d.legend(600, [("클라이언트가 버리는 응답", BAD), ("되돌린 응답", OK), ("이름을 바꾸는 자리", ACC)])
d.save("07-01.answer-restore.svg")
