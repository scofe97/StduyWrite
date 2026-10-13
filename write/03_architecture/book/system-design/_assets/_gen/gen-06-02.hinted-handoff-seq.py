# 타입 스펙: type-sequence — 같은 put(key1, val1) 이 s0·s1 에는 닿고 s2 에는 닿지 않아 s3 가 대신 받은 뒤, s2 가 돌아오면 s3 가 되돌려 준다.
# 사실 출처: 추출본 v2.txt 1788~1799행(느슨한 정족수 · 처음 W 개 건강한 서버 · s2 가 불가하면 s3 가 임시로 처리 · s2 복귀 시 s3 가 넘김),
#   PDF 101쪽 그림(coordinator → s0·s1 put/ACK, s2 ✕),
#   Dynamo 논문 §4.6(https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): 의도한 수신자를 힌트로 메타데이터에 적고 별도 로컬 저장소를 주기적으로 훑어 복귀하면 전달한 뒤 삭제.
# Layout conventions: 레인 5개 폭 150, 메시지 stride 44~56, 장애 구간과 복귀 구간 사이 구분선. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


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
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 960, 664
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §3",
          "응답 없는 s2 몫은 s3 가 받아 두었다가 돌려 준다",
          "s0·s1 의 ACK 로 쓰기는 성공하고, s3 는 s2 에게 줄 값을 힌트와 함께 보관하다 s2 가 돌아오면 넘긴다.",
          "건강한 서버만 세어 쓰기를 받아 주는 느슨한 정족수")

d.lanes([("코디네이터", "요청 받은 노드"),
         ("s0", "복제본"),
         ("s1", "복제본"),
         ("s2", "다운"),
         ("s3", "링의 다음 노드")], lane_w=150)
d.rails(612)

d.t(12, 188, "s2 다운 동안", 13, SOFT, KR, "start", 600)
d.msg("코디네이터", "s0", "put(key1, val1)", 224, MUTED)
d.msg("s0", "코디네이터", "ACK", 268, OK, dash="5 4")
d.msg("코디네이터", "s1", "put(key1, val1)", 324, MUTED)
d.msg("s1", "코디네이터", "ACK", 368, OK, dash="5 4")
d.msg("코디네이터", "s2", "put(key1, val1)", 424, WARN, dash="5 4", sub="응답 없음")
d.msg("코디네이터", "s3", "put(key1, val1)", 496, INFO, sub="힌트: 수신자 s2")

d.line(12, 540, W - 48, 540, RULE, 0.8, "3 6")
d.t(12, 560, "s2 복귀 뒤", 13, SOFT, KR, "start", 600)
d.msg("s3", "s2", "put(key1, val1)", 596, ACC)

d.legend(H - 40, [("성공 응답", OK), ("실패한 전달", WARN), ("대리 수신", INFO), ("힌트 전달", ACC)])
d.save("06-02.hinted-handoff-seq.svg")
