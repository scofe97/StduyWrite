# 06-04 §4 — ndots:5 때문에 외부 이름 하나에 질의가 여섯 번 나간다.
# 원문 근거: Example 6-26 의 여섯 줄을 그대로 옮긴다 — example.com.default.svc.cluster.local /
#            .svc.cluster.local / .cluster.local / .c.belamaric-com.internal / .google.internal /
#            example.com. "five failed queries were made before the final successful sixth query.
#            Each one of these was initiated by the client, sent over the network, processed, and
#            responded to by CoreDNS."
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 왕복이고, 되풀이되는 실패 다섯이 논지다.
#           프리미티브의 mono 하드코딩을 SeqKR 로 덮는다(계약 §프리미티브가 한글을 mono 로 내보내는 자리).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, OK, INK, PAPER2, RULE, KR, MONO


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
            s.t(x, y0 + 38, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 11, MUTED, _kr(sub))


W, H = 880, 720
d = SeqKR(W, H, "LEARNING COREDNS · 06-04 §4",
          "외부 이름 하나에 질의가 여섯 번 나간다",
          "kubelet 이 ndots 를 5 로 두어 점이 다섯보다 적은 이름에 검색 경로를 붙인다. "
          "example.com 은 점이 하나라 다섯 번을 헛돌고 여섯 번째에 성공한다.",
          "여섯 번 모두 네트워크를 탄 왕복입니다")

d.lanes([("파드 안 클라이언트", "ndots:5"),
         ("클러스터 DNS", "CoreDNS")], y0=104, lane_w=300)
d.rails(508)

tries = [
    ("example.com.default.svc.cluster.local", BAD, "실패"),
    ("example.com.svc.cluster.local", BAD, "실패"),
    ("example.com.cluster.local", BAD, "실패"),
    ("example.com.c.belamaric-com.internal", BAD, "실패"),
    ("example.com.google.internal", BAD, "실패"),
    ("example.com", ACC, "성공 · NOERROR"),
]
for i, (name, color, result) in enumerate(tries):
    y = 184 + i * 54
    d.msg("파드 안 클라이언트", "클러스터 DNS", name, y, color,
          mk="acc" if color is ACC else "bad", sub=result)

d.t(20, 560, "검색 경로 넷 중 앞 셋은 kubelet 이 클러스터용으로 넣은 것이고 뒤는 호스트의 것이다", 13, MUTED, KR, "start")
d.t(20, 584, "짧은 이름을 쓰게 해 주는 설정의 값을 바깥 이름을 부를 때 치르는 구조다", 13, MUTED, KR, "start")
d.t(20, 608, "외부 조회가 잦은 워크로드라면 이것만으로 CoreDNS 부하가 극적으로 는다", 13, MUTED, KR, "start")

d.legend(636, [("헛도는 다섯", BAD), ("성공하는 여섯째", ACC)])
d.save("06-04.ndots-fanout.svg")
